import markdown
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from mkdocs.structure.toc import get_toc
from .mistletoe_interop import MarkdownInterop


def render(self, config: MkDocsConfig, files: Files) -> None:
    """
    Convert the Markdown source file to HTML as per the config.
    """
    original_markdown = markdown.Markdown
    markdown.Markdown = MarkdownInterop
    self._original_render(config, files)
    markdown.Markdown = original_markdown

# Page.render = render

class CommonMark(BasePlugin):
    def on_pre_build(self, config, **kwargs):
        if not hasattr(Page, "_original_render"):
            Page._original_render = Page.render
        Page.render = render

    def on_post_build(self, config, **kwargs):
        Page.render = Page._original_render
