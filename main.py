from nanodjango import Django, defer

with defer:
    from wagtail.models import Page
    from wagtail.fields import RichTextField


app = Django(
    WAGTAIL_SITE_NAME="Hello from Nanotail!",
    WAGTAILAILADMIN_BASE_URL="http://localhost:8000",
)


class HomePage(Page):
    parent_page_types = ["wagtailcore.Page"]


class ContentPage(Page):
    body = RichTextField()

    parent_page_types = ["main.HomePage", "main.ContentPage"]

    content_panels = Page.content_panels + [
        "body",
    ]


if __name__ == "__main__":
    app.run()
