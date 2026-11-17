"""Findings and the fix hints a model gets with them."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional

HINTS: Dict[str, str] = {
    "size-raw": "Keep the HTML under 32768 bytes of UTF-8.",
    "size-compressed": "Shrink the widget: drop comments and unused CSS, shorten class names, "
                       "move repeated values into CSS variables, draw with CSS/SVG instead of data: images, "
                       "and put long text and numbers into chat_data instead of the HTML.",
    "html-invalid": "Send valid UTF-8 text without the NUL character (U+0000).",
    "html-unsupported": "Telegram removes this element before drawing. Use the elements listed in "
                        "references/widget-rules.md (div, span, p, h1-h6, lists, table, details, button, "
                        "inline SVG, canvas, img with a data: URL).",
    "html-form-control": "Widgets have no inputs or keyboard. Use <button> elements and taps instead.",
    "html-attr-unsupported": "Telegram drops this attribute. Use CSS instead of presentational attributes, "
                             "and nothing that needs focus or the keyboard.",
    "html-external": "Widgets never load anything from the network. Inline the script/style, and use "
                     "inline SVG or a data: PNG/JPEG/GIF/WebP image.",
    "svg-unsupported": "Telegram removes this SVG feature. Use shapes, paths, gradients, text and CSS animation.",
    "css-unsupported": "Telegram removes this CSS before drawing, so the widget will look different than in a "
                       "browser. Use the replacement named in the message or see references/widget-rules.md.",
    "js-syntax": "Fix the JavaScript syntax error: the whole <script> fails to run in Telegram.",
    "js-network": "Widgets have no network access: every network API throws. Put the data into "
                  "chat_data/public_data when sending, or update it later with the edit command.",
    "js-dynamic-code": "Code built from strings cannot be checked. Write the code out directly; do not use "
                       "eval, Function, constructor tricks, atob, fromCharCode, unicode escapes in names or "
                       "dynamic import.",
    "js-string-splice": "Write the text as one string literal. Gluing string literals together hides what "
                        "they say from the checker.",
    "js-navigation": "Widgets cannot navigate. Use a button whose click handler calls "
                     "TelegramWidget.openLink('https://allowed.example/...') with a literal, allowlisted URL.",
    "js-html-injection": "Build the DOM with document.createElement, textContent and appendChild/"
                         "replaceChildren. HTML parsed from strings can turn state text into links the checker "
                         "cannot see.",
    "js-unsupported": "Telegram does not provide this API in widgets. See references/widget-rules.md for what "
                      "works (copyText instead of navigator.clipboard, openLink instead of window.open, ...).",
    "js-ignored": "This call does nothing in a widget; remove it.",
    "js-event-unsupported": "Widgets get click and pointer events only: no touch, keyboard, focus, wheel or "
                            "scroll events. Use pointerdown/pointermove/pointerup/click.",
    "js-computed-access": "Use dot access (obj.name). Computed access with string keys, or any computed access "
                          "on window/document/TelegramWidget, can hide forbidden names.",
    "js-widget-escape": "Use TelegramWidget only as TelegramWidget.<member> (or through one alias such as "
                        "const TW = window.TelegramWidget). Do not pass it around, spread it or enumerate it.",
    "js-global-escape": "Use window, self and document only as window.<member> (document.getElementById(...)). "
                        "Do not assign them to variables, pass them to functions, return or store them.",
    "js-element": "Create elements with a literal tag name, and never script, iframe, object, embed, link, "
                  "meta, base or form elements.",
    "js-timer-string": "Pass a function to setTimeout/setInterval, never a string of code.",
    "js-id-global": "Element ids are not global variables in widgets: use document.getElementById('id').",
    "js-requests": "TelegramWidget.request() only gets answers if the bot handles widget_query updates and the "
                   "widget is sent with --allow-queries. This skill's frameworks do not route widget_query yet: "
                   "draw from chat_data instead and update it with the edit command.",
    "js-copy-text": "copyText copies text the checker cannot see. Prefer a literal, or make sure the copied "
                    "value comes from data you wrote yourself.",
    "link-dynamic": "Open links only as TelegramWidget.openLink('https://...'), "
                    "TelegramWidget.openTelegramLink('https://t.me/...'), window.open('https://...') or "
                    "<a href=\"https://...\">, each with one literal URL. Never build URLs or link elements "
                    "in code.",
    "link-not-allowed": "Only URLs on the operator's allowlist (TG_WIDGETS_ALLOWED_LINKS) may appear in a "
                        "widget. Remove the link, or ask the operator to allowlist the host. Never add hosts "
                        "to the allowlist yourself.",
    "limits": "Stay inside the widget limits (references/widget-rules.md, LIMITS).",
    "state-invalid": "chat_data and public_data are each a text of at most 1024 bytes of UTF-8 without NUL; "
                     "keep them compact JSON with short keys.",
    "render-error": "Fix the runtime error: the widget stops at the first uncaught exception.",
    "render-height": "Make the widget fit in 600 px at 320 px width (pages, tabs or 'show more'); content "
                     "below is clipped and nothing scrolls.",
    "render-network": "The widget tried to load something from the network, which never works in Telegram.",
    "render-limits": "Stay inside the widget limits (references/widget-rules.md, LIMITS).",
}


@dataclass
class Issue:
    rule: str
    message: str
    line: Optional[int] = None
    severity: str = "error"

    def to_dict(self, with_hint: bool = True) -> dict:
        d = asdict(self)
        if d["line"] is None:
            del d["line"]
        if with_hint and self.rule in HINTS:
            d["hint"] = HINTS[self.rule]
        return d


@dataclass
class Report:
    issues: List[Issue] = field(default_factory=list)
    stats: dict = field(default_factory=dict)
    _seen: set = field(default_factory=set, repr=False)

    def add(self, rule: str, message: str, line: Optional[int] = None, severity: str = "error") -> None:
        key = (rule, message, line)
        if key in self._seen:
            return
        self._seen.add(key)
        self.issues.append(Issue(rule, message, line, severity))

    def warn(self, rule: str, message: str, line: Optional[int] = None) -> None:
        self.add(rule, message, line, "warning")

    @property
    def errors(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict:
        errors = sorted(self.errors, key=lambda i: (i.line or 0))
        warnings = sorted(self.warnings, key=lambda i: (i.line or 0))
        return {
            "ok": self.ok,
            "errors": [i.to_dict() for i in errors],
            "warnings": [i.to_dict() for i in warnings],
            "stats": self.stats,
        }
