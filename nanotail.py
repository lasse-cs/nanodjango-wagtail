from types import MethodType

from django.urls import include, path, re_path

from nanodjango import Django, hookimpl
from nanodjango.urls import urlpatterns


@hookimpl
def django_pre_setup(app: Django):
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
        if wagtail_app in app.settings.INSTALLED_APPS:
            continue
        app.settings.INSTALLED_APPS.append(wagtail_app)

    redirect_middleware = "wagtail.contrib.redirects.middleware.RedirectMiddleware"
    app.settings.MIDDLEWARE.append(redirect_middleware)

    _prepare = app._prepare

    # We need to monkeypatch _prepare in order
    # to ensure that the wagtail catchall url is added last
    def monkey_prepare(self, is_prod=False):
        if self._prepared:
            return

        # If have admin but no admin url
        # move the django-admin to "django-admin/"
        if not self.settings.ADMIN_URL and self.has_admin:
            self.settings.ADMIN_URL = "django-admin/" 

        _prepare(is_prod)

        # Add the wagtail admin urrls
        from wagtail.admin import urls as wagtailadmin_urls
        urlpatterns.append(
            path("admin/", include(wagtailadmin_urls)),
        )

        # Need to add wagtail catch all url as last
        from wagtail import urls as wagtail_urls
        urlpatterns.append(re_path(r"", include(wagtail_urls)))

    app._prepare = MethodType(monkey_prepare, app)

@hookimpl
def django_post_setup(app: Django):
    # Add the wagtail document urls
    from wagtail.documents import urls as wagtaildocs_urls
    urlpatterns.append(
        path("documents/", include(wagtaildocs_urls)),
    )