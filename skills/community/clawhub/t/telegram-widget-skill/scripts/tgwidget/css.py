"""CSS checks against widget profile 1 (https://core.telegram.org/bots/widgets.md#css)."""

from __future__ import annotations

import re
from typing import List, Tuple

from .report import Report
from .urls import AllowEntry

GENERIC_FONTS = {
    "system-ui", "sans-serif", "serif", "monospace", "ui-sans-serif", "ui-serif", "ui-monospace",
    "ui-rounded", "-apple-system", "inherit", "initial", "unset", "revert", "revert-layer",
}
BANNED_AT_RULES = {
    "font-face", "import", "namespace", "container", "layer", "property", "counter-style",
    "starting-style", "scope", "page", "font-feature-values", "font-palette-values", "position-try",
    "document", "view-transition",
}
MEDIA_FEATURES_OK = {
    "width", "min-width", "max-width", "aspect-ratio", "min-aspect-ratio", "max-aspect-ratio",
    "orientation", "prefers-color-scheme", "prefers-reduced-motion",
}
MEDIA_TYPES_OK = {"all", "screen", "only", "not", "and", "or"}
BANNED_PSEUDO = re.compile(
    r"(?i)(:has\(|::?first-letter|::?first-line|::marker|:focus(?:-visible|-within)?\b|:checked\b|"
    r":valid\b|:invalid\b|:placeholder-shown\b|::placeholder|:host(?:-context)?\b|::slotted|::part\b|"
    r":scope\b|:target\b|:indeterminate\b|:required\b|:optional\b|:read-only\b|:read-write\b|"
    r":in-range\b|:out-of-range\b|:autofill\b|:user-invalid\b|:user-valid\b|:popover-open\b|:modal\b|"
    r":fullscreen\b|::backdrop|::file-selector-button)"
)
HEIGHT_UNITS = re.compile(
    r"(?i)(?<![\w-])-?(?:\d+\.?\d*|\.\d+)(vh|svh|lvh|dvh|vb|svb|lvb|dvb|cqh|cqw|cqi|cqb|cqmin|cqmax)\b"
)
LOGICAL = re.compile(
    r"^(?:(?:margin|padding|inset|border|scroll-margin|scroll-padding|overscroll-behavior)-(?:inline|block)"
    r"(?:-|$)|(?:min-|max-)?(?:inline|block)-size$|border-(?:start|end)-(?:start|end)-radius$)"
)
MULTICOL = {"columns", "column-count", "column-width", "column-rule", "column-rule-width",
            "column-rule-style", "column-rule-color", "column-span", "column-fill"}
COLOR_FN = re.compile(r"(?i)(?<![\w-])(hwb|lab|lch|oklab|oklch|color|color-mix|light-dark-mix)\(")
TRANSFORM_3D = re.compile(r"(?i)\b(rotateX|rotateY|rotate3d|translateZ|translate3d|scaleZ|scale3d|matrix3d|perspective)\(")
FILTER_FN = re.compile(r"(?i)\b([a-z-]+)\(")
URL_FN = re.compile(r"(?i)\burl\(\s*(['\"]?)(.*?)\1\s*\)")
DATA_IMAGE = re.compile(r"(?i)^data:image/(png|jpe?g|gif|webp)[;,]")
ENV_FN = re.compile(r"(?i)\benv\(\s*([a-z-]+)")
FONT_SHORTHAND = re.compile(
    r"(?i)(?:\d*\.?\d+(?:px|em|rem|%|pt|ex|ch|vw)|xx-small|x-small|small|medium|large|x-large|xx-large|"
    r"larger|smaller|math)(?:\s*/\s*[^\s,]+)?\s+(.+)$"
)
UNSUPPORTED_PROPS = {
    "text-shadow": "text-shadow", "-webkit-line-clamp": "multi-line clamp", "line-clamp": "multi-line clamp",
    "writing-mode": "vertical text", "text-orientation": "vertical text", "perspective": "3D transforms",
    "perspective-origin": "3D transforms", "transform-style": "3D transforms",
    "backface-visibility": "3D transforms", "mix-blend-mode": "blend modes", "isolation": "blend modes",
    "background-blend-mode": "blend modes", "clip-path": "clip-path", "-webkit-clip-path": "clip-path",
    "container": "container queries", "container-type": "container queries",
    "container-name": "container queries", "-webkit-text-stroke": "text stroke",
    "-webkit-text-fill-color": "gradient text",
}


def _strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), css, flags=re.S)


def _mask_strings(css: str) -> str:
    """Blank out string contents (keeping newlines), so `content:"100vh"` is not a unit."""
    def repl(m):
        s = m.group(0)
        return s[0] + re.sub(r"[^\n]", " ", s[1:-1]) + s[-1]
    return re.sub(r"\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'", repl, css)


class CssChecker:
    def __init__(self, report: Report, allow: List[AllowEntry]):
        self.report = report
        self.allow = allow
        self.rule_count = 0
        self.keyframes = 0

    def _err(self, rule: str, msg: str, line: int) -> None:
        self.report.add(rule, msg, line)

    def check_stylesheet(self, css: str, first_line: int) -> None:
        css = _strip_comments(css)
        masked = _mask_strings(css)
        # stack entries: "rule", "keyframes", "group" (@media/@supports), "other"
        stack: List[str] = []
        buf_start = 0
        i = 0
        n = len(masked)
        while i < n:
            c = masked[i]
            if c == "{":
                raw = masked[buf_start:i]
                prelude = raw.strip()
                orig = css[buf_start:i].strip()
                line = first_line + masked.count("\n", 0, buf_start + len(raw) - len(raw.lstrip()))
                top = stack[-1] if stack else None
                if top == "rule":
                    # a block inside a style rule: CSS nesting (declarations before it were checked already)
                    self._err("css-unsupported", "CSS nesting is removed (write flat selectors)", line)
                    stack.append("other")
                elif top == "keyframes":
                    stack.append("frame")
                elif prelude.startswith("@"):
                    stack.append(self._at_rule(prelude, orig, line))
                else:
                    self.rule_count += 1
                    self._selector(prelude, line)
                    stack.append("rule")
                buf_start = i + 1
            elif c == "}":
                top = stack.pop() if stack else None
                if top in ("rule", "frame"):
                    self._declarations(css[buf_start:i], masked[buf_start:i],
                                       first_line + masked.count("\n", 0, buf_start))
                buf_start = i + 1
            elif c == ";" and (not stack or stack[-1] in ("group", "keyframes")):
                prelude = masked[buf_start:i].strip()
                if prelude.startswith("@"):
                    line = first_line + masked.count("\n", 0, buf_start)
                    self._at_rule(prelude, css[buf_start:i].strip(), line)
                buf_start = i + 1
            elif c == ";" and stack and stack[-1] == "rule":
                pass  # declarations are checked when the block closes
            i += 1

    def check_declarations(self, text: str, line: int) -> None:
        text = _strip_comments(text)
        self._declarations(text, _mask_strings(text), line)

    # pieces ----------------------------------------------------------------
    def _at_rule(self, prelude: str, orig: str, line: int) -> str:
        m = re.match(r"@(-[a-z]+-)?([a-z-]+)", prelude, re.I)
        name = (m.group(2) if m else "").lower()
        if name in BANNED_AT_RULES:
            self._err("css-unsupported", "@%s is removed" % name, line)
            if name == "import":
                self._err("html-external", "@import never loads", line)
            return "other"
        if name == "keyframes":
            self.keyframes += 1
            return "keyframes"
        if name == "media":
            q = prelude[len(m.group(0)):].lower()
            for feat in re.findall(r"\(\s*(?:[\d.]+[a-z%]*\s*[<>=]+\s*)?([a-z-]+)", q):
                if feat not in MEDIA_FEATURES_OK:
                    self._err("css-unsupported", "@media (%s) is not supported: only width, aspect-ratio, "
                                                 "orientation, prefers-color-scheme and "
                                                 "prefers-reduced-motion" % feat, line)
            bare = re.sub(r"\([^)]*\)", " ", q)
            for word in re.findall(r"[a-z-]+", bare):
                if word not in MEDIA_TYPES_OK:
                    self._err("css-unsupported", "@media %s is not supported" % word, line)
            return "group"
        if name == "supports":
            return "group"
        return "other"

    def _selector(self, sel: str, line: int) -> None:
        m = BANNED_PSEUDO.search(sel)
        if m:
            self._err("css-unsupported", "selector %s is removed" % m.group(1), line)
        if "&" in sel:
            self._err("css-unsupported", "CSS nesting (&) is removed", line)

    def _declarations(self, orig: str, masked: str, first_line: int) -> None:
        pos = 0
        for part_masked in masked.split(";"):
            start = pos
            pos += len(part_masked) + 1
            part_orig = orig[start:start + len(part_masked)]
            line = first_line + masked.count("\n", 0, start + len(part_masked) - len(part_masked.lstrip()))
            if ":" not in part_masked:
                continue
            prop, _, value = part_masked.partition(":")
            prop = prop.strip().lower()
            ovalue = part_orig.partition(":")[2]
            if not prop or prop.startswith("--"):
                # custom properties may hold anything; still check url()s and units used later
                self._urls(ovalue, line)
                continue
            self._declaration(prop, value.strip().lower(), ovalue.strip(), line)

    def _declaration(self, prop: str, value: str, ovalue: str, line: int) -> None:
        value = re.sub(r"\s*!important\s*$", "", value)
        if HEIGHT_UNITS.search(value):
            unit = HEIGHT_UNITS.search(value).group(1)
            self._err("css-unsupported", "%s: %s units are removed (height-relative); use px, em, %% or vw"
                      % (prop, unit), line)
        if LOGICAL.match(prop):
            self._err("css-unsupported", "%s: logical properties are removed; use left/right/top/bottom" % prop, line)
        if prop in MULTICOL:
            self._err("css-unsupported", "%s: multi-column layout is removed; use grid or flex" % prop, line)
        if prop in UNSUPPORTED_PROPS and value not in ("none", "initial", "unset", "auto", "normal"):
            self._err("css-unsupported", "%s is removed (%s)" % (prop, UNSUPPORTED_PROPS[prop]), line)
        if prop == "position" and "sticky" in value:
            self._err("css-unsupported", "position: sticky becomes relative", line)
        if prop in ("overflow", "overflow-x", "overflow-y") and re.search(r"\b(auto|scroll|overlay)\b", value):
            self._err("css-unsupported", "%s: %s becomes hidden (nothing scrolls inside a widget)" % (prop, value), line)
        if prop == "display" and re.search(r"\b(contents|flow-root|list-item)\b", value):
            self._err("css-unsupported", "display: %s is removed" % value, line)
        m = COLOR_FN.search(value)
        if m:
            self._err("css-unsupported", "%s() colors are removed; use hex, rgb(), hsl() or light-dark()" % m.group(1), line)
        if prop in ("background-clip", "-webkit-background-clip") and "text" in value:
            self._err("css-unsupported", "background-clip: text is removed", line)
        if prop.startswith("mask") or prop.startswith("-webkit-mask"):
            self._err("css-unsupported", "%s is removed (masks)" % prop, line)
        if prop in ("transform", "transform-function") or prop in ("translate", "rotate", "scale"):
            m3 = TRANSFORM_3D.search(ovalue)
            if m3:
                self._err("css-unsupported", "%s(): 3D transforms are removed" % m3.group(1), line)
        if prop in ("filter", "-webkit-filter"):
            self._filters(prop, value, {"blur", "brightness", "drop-shadow"}, line)
        if prop in ("backdrop-filter", "-webkit-backdrop-filter"):
            self._filters(prop, value, {"blur", "brightness"}, line)
        if "image-set(" in value:
            self._err("css-unsupported", "image-set() is removed", line)
        for env in ENV_FN.findall(value):
            if not re.fullmatch(r"safe-area-inset-(top|right|bottom|left)", env):
                self._err("css-unsupported", "env(%s) is removed (only safe-area-inset-*)" % env, line)
        if prop == "font-family":
            self._fonts(ovalue, line)
        elif prop == "font":
            m = FONT_SHORTHAND.search(ovalue.strip())
            if m:
                self._fonts(m.group(1), line)
        self._urls(ovalue, line)

    def _filters(self, prop: str, value: str, allowed: set, line: int) -> None:
        if value in ("none", "initial", "unset"):
            return
        for fn in FILTER_FN.findall(value):
            if fn not in allowed and fn not in ("rgb", "rgba", "hsl", "hsla", "var", "calc"):
                self._err("css-unsupported", "%s: %s() is removed (only %s)" % (prop, fn, ", ".join(sorted(allowed))), line)

    def _fonts(self, families: str, line: int) -> None:
        names = [f.strip().strip("'\"").strip().lower() for f in families.split(",") if f.strip()]
        names = [n for n in names if not n.startswith("var(")]
        if not names:
            return
        named = [n for n in names if n not in GENERIC_FONTS]
        if named and len(named) == len(names):
            self._err("css-unsupported", "font %r is removed and no generic family is left: use system-ui, "
                                         "sans-serif, serif, monospace or ui-*" % named[0], line)
        elif named:
            self.report.warn("css-unsupported", "named fonts %s are removed (only generic families work); "
                                                "drop them to save bytes" % ", ".join(repr(n) for n in named), line)

    def _urls(self, value: str, line: int) -> None:
        for _, target in URL_FN.findall(value):
            target = target.strip()
            if target.startswith("#") or DATA_IMAGE.match(target):
                continue
            if target.lower().startswith("data:image/svg"):
                self._err("css-unsupported", "url(data:image/svg+xml...) is removed: use inline SVG", line)
            else:
                self._err("html-external", "url(%s) never loads: only data: PNG/JPEG/GIF/WebP images or "
                                           "#fragments" % target[:60], line)

    def finish(self) -> Tuple[int, int]:
        if self.rule_count > 400:
            self._err("limits", "%d CSS rules (limit 400)" % self.rule_count, None)
        if self.keyframes > 32:
            self._err("limits", "%d @keyframes (limit 32)" % self.keyframes, None)
        return self.rule_count, self.keyframes
