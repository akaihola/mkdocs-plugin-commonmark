from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import (
    Page, _ExtractTitleTreeprocessor, _RelativePathTreeprocessor
)

from mkdocs.structure.toc import get_toc
from .mistletoe_interop import MarkdownInterop


def render(self, config: MkDocsConfig, files: Files) -> None:
    """
    Convert the Markdown source file to HTML as per the config.
    """
    if self.markdown is None:
        raise RuntimeError("`markdown` field hasn't been set (via `read_source`)")

    md = MarkdownInterop(
        extensions=config['markdown_extensions'],
        extension_configs=config['mdx_configs'] or {},
    )

    relative_path_ext = _RelativePathTreeprocessor(self.file, files, config)
    relative_path_ext._register(md)

    extract_title_ext = _ExtractTitleTreeprocessor()
    extract_title_ext._register(md)

    self.content = md.convert(self.markdown)
    self.toc = get_toc(getattr(md, 'toc_tokens', []))
    self._title_from_render = extract_title_ext.title

# Page.render = render

class CommonMark(BasePlugin):
    original_render = None

    def on_pre_build(self, config, **kwargs):
        if not self.original_render:
            self.original_render = Page.render
        Page.render = render

    def on_post_build(self, config, **kwargs):
        Page.render = self.original_render
