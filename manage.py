#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import app_manage

gettext = lambda s: s


def install_auth_user_model(settings, value):
    if value is None:
        return
    custom_user_app = 'cms.test_utils.project.' + value.split('.')[0]
    settings['INSTALLED_APPS'].insert(
        settings['INSTALLED_APPS'].index('cms'),
        custom_user_app
    )
    settings['AUTH_USER_MODEL'] = value


def _get_migration_modules(apps):
    modules = {}
    for module in apps:
        module_name = '%s.migrations_django' % module
        try:
            __import__(module_name)
        except ImportError:
            pass
        else:
            modules[module] = module_name
    return modules


if __name__ == '__main__':
    os.environ.setdefault(
        'DJANGO_LIVE_TEST_SERVER_ADDRESS',
        'localhost:8000-9000'
    )
    PROJECT_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'cms', 'test_utils')
    )

    INSTALLED_APPS = [
        'debug_toolbar',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'djangocms_admin_style',
        'django.contrib.admin',
        'django.contrib.sites',
        'django.contrib.staticfiles',
        'django.contrib.messages',
        'treebeard',
        'cms',
        'menus',
        'djangocms_text_ckeditor',
        'djangocms_column',
        'djangocms_picture',
        'djangocms_file',
        'djangocms_flash',
        'djangocms_googlemap',
        'djangocms_teaser',
        'djangocms_video',
        'djangocms_inherit',
        'djangocms_style',
        'djangocms_link',
        'cms.test_utils.project.sampleapp',
        'cms.test_utils.project.placeholderapp',
        'cms.test_utils.project.pluginapp.plugins.manytomany_rel',
        'cms.test_utils.project.pluginapp.plugins.extra_context',
        'cms.test_utils.project.pluginapp.plugins.meta',
        'cms.test_utils.project.pluginapp.plugins.one_thing',
        'cms.test_utils.project.fakemlng',
        'cms.test_utils.project.fileapp',
        'cms.test_utils.project.objectpermissionsapp',
        'cms.test_utils.project.bunch_of_plugins',
        'cms.test_utils.project.extensionapp',
        'cms.test_utils.project.mti_pluginapp',
        'reversion',
        'sekizai',
        'hvad',
        'better_test',
    ]

    dynamic_configs = {
        'TEMPLATES': [{
            'NAME': 'django',
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'DIRS': [os.path.abspath(os.path.join(PROJECT_PATH, 'project', 'templates'))],
            'OPTIONS': {
                'context_processors': [
                    "django.contrib.auth.context_processors.auth",
                    'django.contrib.messages.context_processors.messages',
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.template.context_processors.media",
                    'django.template.context_processors.csrf',
                    "cms.context_processors.cms_settings",
                    "sekizai.context_processors.sekizai",
                    "django.template.context_processors.static",
                ],
                'debug': True,
            }
        }],
    }

    plugins = ('djangocms_column', 'djangocms_file', 'djangocms_flash', 'djangocms_googlemap',
               'djangocms_inherit', 'djangocms_link', 'djangocms_picture', 'djangocms_style',
               'djangocms_teaser', 'djangocms_video')

    migrate = '--migrate' in sys.argv and '--no-migrations' not in sys.argv
    if '--migrate' in sys.argv and '--no-migrations' in sys.argv:
        print('Both --migrate and --no-migrations have been provided. --no-migrations is in effect.')
    if '--migrate' in sys.argv:
        sys.argv.remove('--migrate')

    dynamic_configs['MIGRATION_MODULES'] = _get_migration_modules(plugins)
    if not dynamic_configs.get('TESTS_MIGRATE', migrate):
        # Disable migrations
        class DisableMigrations(object):

            def __contains__(self, item):
                return True

            def __getitem__(self, item):
                return 'notmigrations'

        dynamic_configs['MIGRATION_MODULES'] = DisableMigrations()

    app_manage.main(
        ['cms', 'menus'],
        app_manage.Argument(
            config=app_manage.Config(
                arg='--auth-user-model',
                env='AUTH_USER_MODEL',
                default=None,
            ),
            callback=install_auth_user_model
        ),
        PROJECT_PATH=PROJECT_PATH,
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            }
        },
        SESSION_ENGINE="django.contrib.sessions.backends.cache",
        CACHE_MIDDLEWARE_ANONYMOUS_ONLY=True,
        DEBUG=True,
        DATABASE_SUPPORTS_TRANSACTIONS=True,
        DATABASES=app_manage.DatabaseConfig(
            env='DATABASE_URL',
            arg='--db-url',
            default='sqlite://localhost/local.sqlite'
        ),
        USE_TZ=app_manage.Config(
            env='USE_TZ',
            arg=app_manage.Flag('--use-tz'),
            default=False,
        ),
        TIME_ZONE='UTC',
        SITE_ID=1,
        USE_I18N=True,
        MEDIA_ROOT=app_manage.TempDir(),
        STATIC_ROOT=app_manage.TempDir(),
        CMS_MEDIA_ROOT=app_manage.TempDir(),
        CMS_MEDIA_URL='/cms-media/',
        MEDIA_URL='/media/',
        STATIC_URL='/static/',
        ADMIN_MEDIA_PREFIX='/static/admin/',
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        MIDDLEWARE_CLASSES=[
            'django.middleware.cache.UpdateCacheMiddleware',
            'django.middleware.http.ConditionalGetMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.common.CommonMiddleware',
            'cms.middleware.language.LanguageCookieMiddleware',
            'cms.middleware.user.CurrentUserMiddleware',
            'cms.middleware.page.CurrentPageMiddleware',
            'cms.middleware.toolbar.ToolbarMiddleware',
            'django.middleware.cache.FetchFromCacheMiddleware',
        ],
        INSTALLED_APPS=INSTALLED_APPS,
        DEBUG_TOOLBAR_PATCH_SETTINGS = False,
        INTERNAL_IPS = ['127.0.0.1'],
        AUTHENTICATION_BACKENDS=(
            'django.contrib.auth.backends.ModelBackend',
            'cms.test_utils.project.objectpermissionsapp.backends.ObjectPermissionBackend',
        ),
        LANGUAGE_CODE="en",
        LANGUAGES=(
            ('en', gettext('English')),
            ('fr', gettext('French')),
            ('de', gettext('German')),
            ('pt-br', gettext('Brazilian Portuguese')),
            ('nl', gettext("Dutch")),
            ('es-mx', u'Español'),
        ),
        CMS_LANGUAGES={
            1: [
                {
                    'code': 'en',
                    'name': gettext('English'),
                    'fallbacks': ['fr', 'de'],
                    'public': True,
                },
                {
                    'code': 'de',
                    'name': gettext('German'),
                    'fallbacks': ['fr', 'en'],
                    'public': True,
                },
                {
                    'code': 'fr',
                    'name': gettext('French'),
                    'public': True,
                },
                {
                    'code': 'pt-br',
                    'name': gettext('Brazilian Portuguese'),
                    'public': False,
                },
                {
                    'code': 'es-mx',
                    'name': u'Español',
                    'public': True,
                },
            ],
            2: [
                {
                    'code': 'de',
                    'name': gettext('German'),
                    'fallbacks': ['fr'],
                    'public': True,
                },
                {
                    'code': 'fr',
                    'name': gettext('French'),
                    'public': True,
                },
            ],
            3: [
                {
                    'code': 'nl',
                    'name': gettext('Dutch'),
                    'fallbacks': ['de'],
                    'public': True,
                },
                {
                    'code': 'de',
                    'name': gettext('German'),
                    'fallbacks': ['nl'],
                    'public': False,
                },
            ],
            'default': {
                'hide_untranslated': False,
            },
        },
        CMS_TEMPLATES=(
            ('col_two.html', gettext('two columns')),
            ('col_three.html', gettext('three columns')),
            ('nav_playground.html', gettext('navigation examples')),
            ('simple.html', 'simple'),
            ('static.html', 'static placeholders'),
        ),
        CMS_PLACEHOLDER_CONF={
            'col_sidebar': {
                'plugins': ('FilePlugin', 'FlashPlugin', 'LinkPlugin', 'PicturePlugin',
                'TextPlugin', 'SnippetPlugin'),
                'name': gettext("sidebar column")
            },
            'col_left': {
                'plugins': ('FilePlugin', 'FlashPlugin', 'LinkPlugin', 'PicturePlugin',
                'TextPlugin', 'SnippetPlugin', 'GoogleMapPlugin', 'MultiColumnPlugin', 'StylePlugin'),
                'name': gettext("left column"),
                'plugin_modules': {
                    'LinkPlugin': 'Different Grouper'
                },
                'plugin_labels': {
                    'LinkPlugin': gettext('Add a link')
                },
            },
            'col_right': {
                'plugins': ('FilePlugin', 'FlashPlugin', 'LinkPlugin', 'PicturePlugin',
                'TextPlugin', 'SnippetPlugin', 'GoogleMapPlugin', 'MultiColumnPlugin', 'StylePlugin'),
                'name': gettext("right column")
            },
            'extra_context': {
                "plugins": ('TextPlugin',),
                "extra_context": {"width": 250},
                "name": "extra context"
            },
        },
        CMS_PERMISSION=True,
        CMS_PUBLIC_FOR='all',
        CMS_CACHE_DURATIONS={
            'menus': 0,
            'content': 0,
            'permissions': 0,
        },
        CMS_APPHOOKS=[],
        CMS_PLUGIN_PROCESSORS=(),
        CMS_PLUGIN_CONTEXT_PROCESSORS=(),
        CMS_SITE_CHOICES_CACHE_KEY='CMS:site_choices',
        CMS_PAGE_CHOICES_CACHE_KEY='CMS:page_choices',
        CMS_NAVIGATION_EXTENDERS=[
            ('cms.test_utils.project.sampleapp.menu_extender.get_nodes',
             'SampleApp Menu'),
        ],
        ROOT_URLCONF='cms.test_utils.project.urls',
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
        ALLOWED_HOSTS=['localhost'],
        TEST_RUNNER='django.test.runner.DiscoverRunner',
        **dynamic_configs
    )
