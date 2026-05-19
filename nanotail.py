from types import MethodType

from django.urls import include, path, re_path

from nanodjango import Django, hookimpl
from nanodjango.urls import urlpatterns


@hookimpl
def django_pre_setup(app: Django):
    _prepare = app._prepare

    from django.conf import settings

    apps = [
        "wagtail.contrib.forms",
        "wagtail.contrib.redirects",
        "wagtail.embeds",
        "wagtail.sites",
        "wagtail.users",
        "wagtail.snippets",
        "wagtail.documents",
        "wagtail.images",
        "wagtail.search",
        "wagtail.admin",
        "wagtail",
        "taggit",
        "modelcluster",
    ]

    for wagtail_app in apps:
        if wagtail_app in settings.INSTALLED_APPS:
            continue
        settings.INSTALLED_APPS.append(wagtail_app)

    redirect_middleware = "wagtail.contrib.redirects.middleware.RedirectMiddleware"
    settings.MIDDLEWARE.append(redirect_middleware)

    def monkey_prepare(self, is_prod=False):
        if self._prepared:
            return

        _prepare(is_prod)

        from wagtail import urls as wagtail_urls
        from wagtail.admin import urls as wagtailadmin_urls
        from wagtail.documents import urls as wagtaildocs_urls
        
        urlpatterns.append(
            path("admin/", include(wagtailadmin_urls)),
        )
        urlpatterns.append(
            path("documents/", include(wagtaildocs_urls)),
        )
        urlpatterns.append(re_path(r"", include(wagtail_urls)))

    app._prepare = MethodType(monkey_prepare, app)

@hookimpl
def django_post_setup(app: Django):
    pass
