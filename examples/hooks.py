from nanodjango import Django

from wagtail import hooks


app = Django(
    WAGTAIL_SITE_NAME="Hello from Nanotail!",
    WAGTAILADMIN_BASE_URL="http://localhost:8000",
)


@hooks.register("before_serve_page")
def log(page, request, serve_args, serve_kwargs):
    print("Hello from a hook")