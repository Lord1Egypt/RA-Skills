"""
PageSnapshot stub — minimal placeholder for url2pdf-mk scripts.

The url2pdf-mk scripts don't use PageSnapshot directly (they pass None
as the snapshot argument to BrowserActions), but browser_actions.py
imports it, so we need this class present.
"""


class PageSnapshot:
    """Minimal PageSnapshot stub — not used by url2pdf-mk scrape scripts."""

    def __init__(self, client):
        self.client = client
        self.refs = {}  # empty refs dict (scrape scripts pass None anyway)

    def accessibility_tree(self):
        return {}
