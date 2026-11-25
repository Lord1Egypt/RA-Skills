"""Tolerant HTML collector used by check_html.py and check_links.py. Standard library only.

It records raw facts (tags, attributes, text). It does not judge anything; judging
happens in check_html.py so the rules are in one place.
"""
import re
import urllib.parse
from collections import Counter
from html.parser import HTMLParser

SKIP_TEXT = {"script", "style", "noscript", "template"}
NO_LABEL_TYPES = {"hidden", "submit", "button", "image", "reset"}
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
RESOURCE_ATTR = {"img": "src", "script": "src", "iframe": "src", "source": "src",
                 "audio": "src", "video": "src", "embed": "src", "track": "src",
                 "object": "data"}


def clean(s):
    return re.sub(r"\s+", " ", s or "").strip()


class PageParser(HTMLParser):
    def __init__(self, base_url=""):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.tags = Counter()
        self.roles = set()
        self.lang = None
        self.in_head = False
        self.titles = []
        self._title = None
        self._svg = 0
        self.metas = []
        self.link_tags = []
        self.headings = []
        self._heading = None
        self.images = []
        self.anchors = []
        self._anchor = None
        self.buttons = []
        self._button = None
        self.controls = []
        self.label_for = set()
        self._label_depth = 0
        self.forms = []
        self.has_password = False
        self.scripts = []
        self._script = None
        self.jsonld = []
        self.resources = []
        self.tabindex_positive = 0
        self.aria_hidden_focusable = []
        self.text = []
        self._skip = 0

    def _res(self, tag, url):
        if url:
            self.resources.append({"tag": tag, "url": url})

    def _snippet(self):
        return (self.get_starttag_text() or "")[:160]

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        self.tags[tag] += 1
        if "role" in a:
            self.roles.add(a["role"].strip().lower())

        tabint = None
        if "tabindex" in a:
            try:
                tabint = int(a["tabindex"].strip())
            except ValueError:
                tabint = None
        if tabint is not None and tabint > 0:
            self.tabindex_positive += 1
        focusable = ((tag == "a" and "href" in a) or tag in ("button", "select", "textarea")
                     or (tag == "input" and a.get("type", "").lower() != "hidden")
                     or (tabint is not None and tabint >= 0))
        if tabint == -1:
            focusable = False
        if focusable and a.get("aria-hidden", "").strip().lower() == "true":
            self.aria_hidden_focusable.append(self._snippet())

        if tag in RESOURCE_ATTR:
            self._res(tag, a.get(RESOURCE_ATTR[tag], ""))

        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "head":
            self.in_head = True
        elif tag == "body":
            self.in_head = False
        elif tag == "base" and a.get("href"):
            self.base_url = urllib.parse.urljoin(self.base_url, a["href"])
        elif tag == "svg":
            self._svg += 1
        elif tag == "title" and self._svg == 0:
            self._title = []
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.link_tags.append(a)
            if "stylesheet" in a.get("rel", "").lower().split():
                self._res("link", a.get("href", ""))
        elif tag in HEADING_TAGS:
            self._heading = [int(tag[1]), []]
        elif tag == "img":
            rec = {"src": a.get("src", ""), "has_alt": "alt" in a, "alt": a.get("alt"),
                   "has_width": "width" in a, "has_height": "height" in a,
                   "loading": a.get("loading", "").lower(), "snippet": self._snippet()}
            self.images.append(rec)
            if self._anchor is not None and a.get("alt", "").strip():
                self._anchor["img_alt"].append(a["alt"].strip())
        elif tag == "a" and "href" in a:
            if self._anchor is not None:
                self.anchors.append(self._anchor)
            self._anchor = {"href": a["href"], "text": [], "aria_label": a.get("aria-label", "").strip(),
                            "aria_labelledby": a.get("aria-labelledby", "").strip(),
                            "title": a.get("title", "").strip(), "img_alt": [],
                            "snippet": self._snippet()}
        elif tag == "button":
            self._button = {"text": [], "aria_label": a.get("aria-label", "").strip(),
                            "aria_labelledby": a.get("aria-labelledby", "").strip(),
                            "title": a.get("title", "").strip(), "snippet": self._snippet()}
        elif tag in ("input", "select", "textarea"):
            ctype = a.get("type", "text").lower() if tag == "input" else tag
            if ctype not in NO_LABEL_TYPES:
                self.controls.append({"tag": tag, "type": ctype, "id": a.get("id", ""),
                                      "aria_label": a.get("aria-label", "").strip(),
                                      "aria_labelledby": a.get("aria-labelledby", "").strip(),
                                      "title": a.get("title", "").strip(),
                                      "placeholder": a.get("placeholder", ""),
                                      "in_label": self._label_depth > 0,
                                      "snippet": self._snippet()})
                if ctype == "password":
                    self.has_password = True
        elif tag == "label":
            self._label_depth += 1
            if a.get("for"):
                self.label_for.add(a["for"])
        elif tag == "form":
            self.forms.append({"action": a.get("action", ""), "method": a.get("method", "get").lower()})
        elif tag == "script":
            self._script = {"src": a.get("src", ""), "async": "async" in a, "defer": "defer" in a,
                            "type": a.get("type", "").lower(), "integrity": a.get("integrity", ""),
                            "in_head": self.in_head, "inline_bytes": 0, "_buf": []}
            self.scripts.append(self._script)

        if tag in SKIP_TEXT:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title" and self._title is not None:
            self.titles.append(clean("".join(self._title)))
            self._title = None
        elif tag == "svg":
            self._svg = max(0, self._svg - 1)
        elif tag in HEADING_TAGS and self._heading:
            self.headings.append({"level": self._heading[0], "text": clean("".join(self._heading[1]))[:120]})
            self._heading = None
        elif tag == "a" and self._anchor is not None:
            self.anchors.append(self._anchor)
            self._anchor = None
        elif tag == "button" and self._button is not None:
            self.buttons.append(self._button)
            self._button = None
        elif tag == "label":
            self._label_depth = max(0, self._label_depth - 1)
        elif tag == "head":
            self.in_head = False
        if tag in SKIP_TEXT:
            self._skip = max(0, self._skip - 1)
            if tag == "script" and self._script is not None:
                if self._script["type"] == "application/ld+json":
                    self.jsonld.append("".join(self._script["_buf"]))
                self._script.pop("_buf", None)
                self._script = None

    def handle_data(self, data):
        if self._title is not None:
            self._title.append(data)
        if self._script is not None:
            if not self._script["src"]:
                self._script["inline_bytes"] += len(data.encode("utf-8", "replace"))
            self._script["_buf"].append(data)
            return
        if self._skip:
            return
        self.text.append(data)
        if self._heading:
            self._heading[1].append(data)
        if self._anchor is not None:
            self._anchor["text"].append(data)
        if self._button is not None:
            self._button["text"].append(data)

    def visible_text(self):
        return clean(" ".join(self.text))


def parse_page(html, base_url=""):
    p = PageParser(base_url)
    p.feed(html)
    p.close()
    return p
