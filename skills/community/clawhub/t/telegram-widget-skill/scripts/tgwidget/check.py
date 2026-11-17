"""The static widget check: size, HTML, CSS, JavaScript and links."""

from __future__ import annotations

import re
import zlib
from html.parser import HTMLParser
from typing import List, Optional, Tuple

from .css import CssChecker
from .jslex import LexError, tokenize
from .jsrules import ScriptChecker
from .jssyntax import available_engine, check_syntax
from .report import Report
from .urls import AllowEntry, link_problem, scan_text

MAX_HTML_BYTES = 32768
MAX_COMPRESSED_BYTES = 4096
MAX_STATE_BYTES = 1024
MAX_NODES = 2000
MAX_ATTRIBUTE = 8192

UNSUPPORTED_TAGS = {
    "ruby", "rt", "rp", "bdi", "bdo", "center", "font", "big", "tt", "strike", "nobr", "marquee", "blink",
    "progress", "meter", "dialog", "audio", "video", "source", "track", "iframe", "frame", "frameset",
    "object", "embed", "link", "meta", "base", "portal", "template", "slot", "math", "fencedframe",
    "map", "area", "applet", "param", "noscript", "picture",
}
FORM_CONTROLS = {"input", "select", "option", "optgroup", "textarea", "fieldset", "legend", "datalist",
                 "output", "keygen"}
FORM_SOFT = {"form": "<form> becomes a plain block", "label": "<label> becomes a plain inline box"}
SVG_UNSUPPORTED = {
    "clippath": "clipPath", "mask": "mask", "pattern": "pattern", "marker": "marker", "filter": "filter",
    "animate": "SMIL animate", "animatetransform": "SMIL animateTransform",
    "animatemotion": "SMIL animateMotion", "set": "SMIL set", "mpath": "SMIL mpath",
    "foreignobject": "foreignObject", "image": "SVG <image>",
}
LEGACY_ATTRS = {"align", "valign", "bgcolor", "border", "cellpadding", "cellspacing", "color", "face", "nowrap"}
FOCUS_ATTRS = {"contenteditable", "spellcheck", "inputmode", "enterkeyhint", "autocapitalize", "draggable",
               "tabindex", "autofocus", "accesskey", "popover", "popovertarget", "popovertargetaction"}
LINKISH_ATTRS = {"srcset", "action", "formaction", "ping", "background", "poster", "manifest", "data", "codebase"}
DATA_IMAGE = re.compile(r"(?i)^\s*data:image/(png|jpe?g|gif|webp)[;,]")
JS_TYPES = {"", "text/javascript", "application/javascript", "module", "text/ecmascript", "application/ecmascript"}


class _Scanner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements: List[Tuple[str, list, int, bool]] = []  # tag, attrs, line, in_svg
        self.scripts: List[Tuple[str, int, dict]] = []  # code, first line, attrs
        self.styles: List[Tuple[str, int]] = []
        self.texts: List[Tuple[str, int]] = []
        self.nodes = 0
        self.svg_depth = 0
        self._raw: Optional[Tuple[str, int, dict]] = None  # open <script>/<style>
        self._raw_parts: List[str] = []

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        self.nodes += 1
        in_svg = self.svg_depth > 0 or tag == "svg"
        self.elements.append((tag, attrs, line, in_svg))
        if tag == "svg":
            self.svg_depth += 1
        if tag in ("script", "style"):
            self._raw = (tag, line, dict(attrs))
            self._raw_parts = []

    def handle_startendtag(self, tag, attrs):
        line = self.getpos()[0]
        self.nodes += 1
        self.elements.append((tag, attrs, line, self.svg_depth > 0 or tag == "svg"))

    def handle_endtag(self, tag):
        if tag == "svg" and self.svg_depth:
            self.svg_depth -= 1
        if self._raw and tag == self._raw[0]:
            kind, line, attrs = self._raw
            code = "".join(self._raw_parts)
            if kind == "script":
                self.scripts.append((code, line, attrs))
            else:
                self.styles.append((code, line))
            self._raw = None

    def handle_data(self, data):
        if self._raw:
            self._raw_parts.append(data)
            return
        if data.strip():
            self.nodes += 1
            self.texts.append((data, self.getpos()[0]))

    def handle_comment(self, data):
        self.nodes += 1

    def close_unclosed(self):
        if self._raw:  # <script> without </script>
            self.handle_endtag(self._raw[0])


def _check_size(report: Report, raw: bytes) -> Optional[str]:
    size = len(raw)
    compressed = len(zlib.compress(raw, 9))
    report.stats.update({
        "bytes": size, "bytes_limit": MAX_HTML_BYTES,
        "compressed_bytes": compressed, "compressed_limit": MAX_COMPRESSED_BYTES,
        "compressed_headroom": MAX_COMPRESSED_BYTES - compressed,
    })
    if size == 0:
        report.add("html-invalid", "the HTML is empty")
    if size > MAX_HTML_BYTES:
        report.add("size-raw", "%d bytes of HTML (limit %d)" % (size, MAX_HTML_BYTES))
    if compressed > MAX_COMPRESSED_BYTES:
        report.add("size-compressed", "%d bytes after zlib level 9 (limit %d, %d over)"
                   % (compressed, MAX_COMPRESSED_BYTES, compressed - MAX_COMPRESSED_BYTES))
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        report.add("html-invalid", "not valid UTF-8 (byte %d)" % e.start)
        return None
    if "\x00" in text:
        report.add("html-invalid", "contains the NUL character (U+0000)", text.count("\n", 0, text.index("\x00")) + 1)
    return text


def _check_js(code: str, line: int, scripts: ScriptChecker, report: Report, what: str) -> None:
    found = check_syntax(code)
    if found:
        msg, rel_line, severity, _ = found
        abs_line = line + rel_line - 1 if rel_line else line
        report.add("js-syntax", "%s: %s" % (what, msg), abs_line, severity)
    try:
        tokens = tokenize(code, first_line=line)
    except LexError as e:
        if "escape in an identifier" in str(e):
            report.add("js-dynamic-code", "%s: %s" % (what, e), e.line)
        elif not found:
            report.add("js-syntax", "%s: %s" % (what, e), e.line)
        return
    scripts.check(tokens)


def _check_attr_url(report: Report, allow: List[AllowEntry], tag: str, name: str, value: str,
                    line: int) -> bool:
    """Judge href-like attributes. Returns True if the value was judged as a link."""
    if name in ("href", "xlink:href"):
        v = value.strip()
        if v.startswith("#"):
            return True
        if tag != "a":
            report.add("html-external", "<%s %s=%r>: only #fragment references work" % (tag, name, v[:60]), line)
            return True
        problem = link_problem(v, allow, "href")
        if problem:
            report.add("link-not-allowed", "<a href=%r>: %s" % (v[:80], problem), line)
        return True
    if name == "src":
        v = value.strip()
        if tag == "img" and DATA_IMAGE.match(v):
            return True
        if tag == "img" and v.lower().startswith("data:image/svg"):
            report.add("html-unsupported", "<img src=\"data:image/svg+xml...\"> is removed: use inline <svg>", line)
        elif tag == "script":
            report.add("html-external", "<script src> never loads: inline the code", line)
        else:
            report.add("html-external", "<%s src=%r> never loads: use inline SVG or a data: PNG/JPEG/GIF/WebP "
                                        "image" % (tag, v[:60]), line)
        return True
    if name in LINKISH_ATTRS and tag not in ("object",):
        report.add("link-not-allowed", "<%s %s=...>: this attribute is not allowed" % (tag, name), line)
        return True
    return False


def check_html(raw: bytes, allow: List[AllowEntry]) -> Report:
    report = Report()
    text = _check_size(report, raw)
    report.stats["js_engine"] = available_engine()
    if text is None:
        return report

    scan = _Scanner()
    try:
        scan.feed(text)
        scan.close()
    except Exception as e:  # HTMLParser is lenient; this is a guard
        report.add("html-invalid", "cannot parse the HTML: %s" % e)
        return report
    scan.close_unclosed()

    element_ids = {v for _, attrs, _, _ in scan.elements for k, v in attrs if k == "id" and v}
    css = CssChecker(report, allow)
    scripts = ScriptChecker(report, allow, element_ids)

    for tag, attrs, line, in_svg in scan.elements:
        if in_svg and tag in SVG_UNSUPPORTED:
            report.add("svg-unsupported", "SVG %s is removed" % SVG_UNSUPPORTED[tag], line)
        elif tag in FORM_CONTROLS:
            report.add("html-form-control", "<%s> is removed with its content (no inputs in widgets)" % tag, line)
        elif tag in FORM_SOFT:
            report.warn("html-form-control", FORM_SOFT[tag], line)
        elif tag in UNSUPPORTED_TAGS:
            report.add("html-unsupported", "<%s> is removed" % tag, line)
        for name, value in attrs:
            value = value or ""
            if len(value) > MAX_ATTRIBUTE:
                report.add("limits", "<%s %s> is %d characters (limit %d per attribute: the widget stops)"
                           % (tag, name, len(value), MAX_ATTRIBUTE), line)
            if name.startswith("on"):
                if name[2:] in ("touchstart", "touchmove", "touchend", "touchcancel", "keydown", "keyup",
                                "keypress", "input", "wheel", "scroll", "focus", "blur", "focusin", "focusout",
                                "beforeinput", "change", "submit"):
                    report.add("js-event-unsupported", "%s never fires in a widget" % name, line)
                _check_js(value, line, scripts, report, "<%s %s>" % (tag, name))
                continue
            if name == "style":
                css.check_declarations(value, line)
                continue
            if not in_svg and name in LEGACY_ATTRS and tag not in ("svg",):
                report.add("html-attr-unsupported", "<%s %s> is removed (use CSS)" % (tag, name), line)
            if name in FOCUS_ATTRS:
                report.add("html-attr-unsupported", "<%s %s> is removed" % (tag, name), line)
            if re.search(r"(?i)\bjavascript\s*:", value):
                report.add("link-not-allowed", "<%s %s> contains a javascript: URL" % (tag, name), line)
                continue
            if _check_attr_url(report, allow, tag, name, value, line):
                continue
            for url, problem in scan_text(value, allow):
                report.add("link-not-allowed", "<%s %s> mentions %r: %s" % (tag, name, url[:80], problem), line)

    for code, line, attrs in scan.scripts:
        if "src" in attrs:
            continue  # reported with the attributes
        stype = (attrs.get("type") or "").strip().lower()
        if stype not in JS_TYPES:
            # a data block (application/json, ...) does not run, but code can read and show it
            for url, problem in scan_text(code, allow):
                report.add("link-not-allowed", "<script type=%s> mentions %r: %s" % (stype, url[:80], problem), line)
            continue
        if stype == "module":
            report.warn("html-unsupported", "<script type=module>: use a classic script", line)
        _check_js(code, line, scripts, report, "<script>")
    scripts.finish()
    if scripts.uses_requests:
        report.warn("js-requests", "the widget calls TelegramWidget.request()")

    for code, line in scan.styles:
        css.check_stylesheet(code, line)
    rules, keyframes = css.finish()

    for data, line in scan.texts:
        for url, problem in scan_text(data, allow):
            report.add("link-not-allowed", "text mentions %r: %s" % (url[:80], problem), line)

    if scan.nodes > MAX_NODES:
        report.add("limits", "%d nodes in the HTML (limit %d: the widget stops)" % (scan.nodes, MAX_NODES))
    report.stats.update({
        "elements": len(scan.elements), "scripts": len(scan.scripts), "css_rules": rules,
        "keyframes": keyframes, "uses_requests": scripts.uses_requests,
    })
    return report


def check_state(name: str, value: Optional[str], allow: List[AllowEntry], report: Report) -> None:
    """chat_data / public_data: size, NUL, and no links the widget could show."""
    if value is None:
        return
    raw = value.encode("utf-8")
    if len(raw) > MAX_STATE_BYTES:
        report.add("state-invalid", "%s is %d bytes (limit %d)" % (name, len(raw), MAX_STATE_BYTES))
    if "\x00" in value:
        report.add("state-invalid", "%s contains the NUL character" % name)
    if re.search(r"(?i)\bjavascript\s*:", value):
        report.add("link-not-allowed", "%s contains a javascript: URL" % name)
    for url, problem in scan_text(value, allow):
        report.add("link-not-allowed", "%s mentions %r: %s" % (name, url[:80], problem))
    if re.search(r"(?i)<\s*a\b|href\s*=", value):
        report.add("link-not-allowed", "%s contains link markup" % name)
