"""Rules over the tokens of one script (or one inline on* handler).

The link rules follow one principle: if the checker cannot prove where a link
goes, the widget is refused. Links may only be opened with a literal URL in
one of the sanctioned forms, and everything that could assemble a name or a
URL out of pieces (eval, Function, atob, computed access with strings, HTML
parsed from strings, ...) is refused outright.
"""

from __future__ import annotations

import re
from typing import Iterable, List, Optional, Set

from .jslex import Token
from .report import Report
from .urls import AllowEntry, link_problem, scan_text

NETWORK = {
    "fetch", "XMLHttpRequest", "WebSocket", "EventSource", "RTCPeerConnection", "sendBeacon",
    "importScripts", "Worker", "SharedWorker", "BroadcastChannel", "serviceWorker",
}
DYNAMIC_CODE = {
    "eval", "Function", "atob", "fromCharCode", "fromCodePoint", "unescape", "decodeURI",
    "decodeURIComponent", "Reflect", "Proxy", "globalThis", "__proto__", "__defineGetter__",
    "__defineSetter__", "__lookupGetter__", "__lookupSetter__", "getOwnPropertyDescriptor",
    "getOwnPropertyDescriptors", "getOwnPropertyNames", "getPrototypeOf", "setPrototypeOf",
    "defineProperty", "defineProperties",
}
HTML_INJECTION = {
    "innerHTML", "outerHTML", "insertAdjacentHTML", "createContextualFragment", "DOMParser",
    "parseFromString", "setHTMLUnsafe", "parseHTMLUnsafe", "srcdoc",
}
UNSUPPORTED = {
    "attachShadow": "shadow DOM", "customElements": "custom elements", "Blob": "Blob",
    "FileReader": "FileReader", "createObjectURL": "URL.createObjectURL",
    "requestFullscreen": "fullscreen", "getImageData": "canvas pixel read-back",
    "putImageData": "canvas pixel writes", "createImageData": "canvas pixel buffers",
    "toDataURL": "canvas.toDataURL", "toBlob": "canvas.toBlob", "captureStream": "canvas streams",
    "createPattern": "canvas patterns", "createConicGradient": "canvas conic gradients",
    "globalCompositeOperation": "canvas compositing", "shadowBlur": "canvas shadows",
    "shadowColor": "canvas shadows", "shadowOffsetX": "canvas shadows", "shadowOffsetY": "canvas shadows",
    "OffscreenCanvas": "OffscreenCanvas", "Notification": "notifications",
    "requestPointerLock": "pointer lock",
}
NAVIGATOR_UNSUPPORTED = {"clipboard", "share", "vibrate", "geolocation", "mediaDevices", "serviceWorker"}
DIALOGS = {"alert", "confirm", "prompt"}
UNSUPPORTED_EVENTS = {
    "touchstart", "touchmove", "touchend", "touchcancel", "keydown", "keyup", "keypress",
    "beforeinput", "input", "wheel", "mousewheel", "scroll", "scrollend", "focus", "blur",
    "focusin", "focusout",
}
WIDGET_EVENTS = {
    "themeChanged", "activated", "deactivated", "chatDataChanged", "publicDataChanged",
    "contentSafeAreaChanged",
}
WIDGET_MEMBERS = {
    "profile", "isProfileAtLeast", "colorScheme", "themeParams", "isActive", "isPreview", "isForward",
    "chatType", "viewer", "publicData", "chatData", "watchPublicData", "unwatchPublicData", "request",
    "copyText", "openLink", "openTelegramLink", "HapticFeedback", "contentSafeAreaInset", "wallet",
    "setResizeAnchor", "ready", "onEvent", "offEvent", "theme", "onTheme",
}
LINK_PROPS = {"href", "src", "srcset", "srcdoc", "action", "formAction", "formaction", "xlinkHref", "ping"}
LINK_ATTRS = {"href", "xlink:href", "src", "srcset", "srcdoc", "action", "formaction", "ping", "background"}
BANNED_TAGS = {
    "script", "iframe", "frame", "frameset", "object", "embed", "link", "meta", "base", "form",
    "input", "select", "textarea", "portal", "fencedframe", "template", "foreignobject", "image",
}
GLOBAL_OBJECTS = {"window", "self", "top", "parent", "frames", "document", "globalThis"}
# Globals that may not be used as a value at all (assigned, passed, returned, stored): an alias of
# window could reach window.open where the checker no longer sees it. top, parent and frames double
# as ordinary variable names (`fillRect(left, top, ...)`), so those are only tracked through plain
# assignments; globalThis is refused outright (DYNAMIC_CODE).
VALUE_ESCAPE_GLOBALS = {"window", "self", "document"}
# What may follow an expression that ends at a token: the end of a statement or of an argument
EXPR_END = (";", ",", ")", "}", "]", "||", "??", "&&", ":", "?")
DATA_IMAGE = re.compile(r"(?i)^data:image/(png|jpe?g|gif|webp)[;,]")


def _literal(tok: Optional[Token]) -> Optional[str]:
    """The text of a plain string literal (or a template without ${}), else None."""
    if tok is None:
        return None
    if tok.kind == "str":
        return tok.value
    if tok.kind == "template" and not tok.has_subst:
        return tok.parts[0] if tok.parts else ""
    return None


def _string_texts(tok: Token) -> List[str]:
    if tok.kind == "str":
        return [tok.value]
    if tok.kind == "template":
        return tok.parts
    return []


class ScriptChecker:
    def __init__(self, report: Report, allow: List[AllowEntry], element_ids: Iterable[str] = ()):
        self.report = report
        self.allow = allow
        self.element_ids = set(element_ids)
        self.uses_requests = False
        self._globals: Set[str] = set(GLOBAL_OBJECTS)  # plus aliases, per script in check()
        # tokens of every script, for the cross-script id check
        self.all_tokens: List[Token] = []

    # helpers -------------------------------------------------------------
    def _err(self, rule: str, msg: str, tok: Token) -> None:
        self.report.add(rule, msg, tok.line)

    def check(self, tokens: List[Token]) -> None:
        self.all_tokens.extend(tokens)
        aliases = self._widget_aliases(tokens)
        # window and its kin, plus names assigned from them (`w = window`, `p = top`)
        self._globals = GLOBAL_OBJECTS | self._global_aliases(tokens)
        open_refs = self._open_refs(tokens)  # names holding some object's .open method
        validated: Set[int] = set()  # ids of string tokens already judged as link targets

        for idx, t in enumerate(tokens):
            prev = tokens[idx - 1] if idx > 0 else None
            prev2 = tokens[idx - 2] if idx > 1 else None
            nxt = tokens[idx + 1] if idx + 1 < len(tokens) else None
            after_dot = prev is not None and prev.is_punct(".", "?.")

            if t.kind == "punct" and t.value == "+" and prev is not None and nxt is not None:
                if _literal(prev) is not None and _literal(nxt) is not None:
                    self._err("js-string-splice", "string literals joined with +", t)

            if t.kind == "punct" and t.value == "[" and prev is not None:
                self._computed_access(tokens, idx, prev, aliases)

            if t.kind != "ident":
                continue
            name = t.value

            if name in NETWORK:
                self._err("js-network", "%s: widgets have no network access" % name, t)
            elif name in DYNAMIC_CODE:
                self._err("js-dynamic-code", "%s is not allowed" % name, t)
            elif name == "constructor" and after_dot:
                self._err("js-dynamic-code", ".constructor is not allowed", t)
            elif name == "raw" and after_dot and prev2 is not None and prev2.is_ident("String"):
                self._err("js-dynamic-code", "String.raw is not allowed", t)
            elif name == "import" and not after_dot:
                self._err("js-dynamic-code", "import is not allowed (no modules, no dynamic import)", t)
            elif name == "with" and not after_dot and nxt is not None and nxt.is_punct("("):
                self._err("js-dynamic-code", "with statements are not allowed", t)
            elif name in HTML_INJECTION or (
                name in ("write", "writeln") and after_dot and prev2 is not None and prev2.value in self._globals
            ):
                self._err("js-html-injection", "%s parses HTML from a string" % name, t)
            elif name in UNSUPPORTED:
                self._err("js-unsupported", "%s is not available in widgets" % UNSUPPORTED[name], t)
            elif name in NAVIGATOR_UNSUPPORTED and after_dot and prev2 is not None and prev2.is_ident("navigator"):
                self._err("js-unsupported", "navigator.%s is not available in widgets" % name, t)
            elif name in DIALOGS and nxt is not None and nxt.is_punct("(") and (
                not after_dot or (prev2 is not None and prev2.value in self._globals)
            ):
                self._err("js-unsupported", "%s() shows nothing in a widget" % name, t)
            elif name == "print" and after_dot and prev2 is not None and prev2.is_ident("window"):
                self._err("js-unsupported", "window.print() does nothing in a widget", t)
            elif name in ("focus", "blur") and after_dot and nxt is not None and nxt.is_punct("("):
                self.report.warn("js-ignored", ".%s() does nothing in a widget" % name, t.line)
            elif name == "sendMessage" and after_dot:
                self._err("js-unsupported", "TelegramWidget.sendMessage does not exist", t)
            elif name in ("location", "history"):
                self._navigation(t, prev, prev2, nxt, tokens, idx)
            elif name in ("openLink", "openTelegramLink"):
                self._link_call(tokens, idx, name, after_dot, validated)
            elif name == "open":
                self._open(tokens, idx, prev, prev2, after_dot, validated)
            elif name in LINK_PROPS:
                self._link_prop(tokens, idx, name, validated)
            elif name in ("setAttribute", "setAttributeNS") and after_dot:
                self._set_attribute(tokens, idx, name == "setAttributeNS")
            elif name in ("createElement", "createElementNS") and after_dot:
                self._create_element(tokens, idx, name == "createElementNS")
            elif name in ("setTimeout", "setInterval") and nxt is not None and nxt.is_punct("("):
                arg = tokens[idx + 2] if idx + 2 < len(tokens) else None
                if arg is not None and arg.kind in ("str", "template"):
                    self._err("js-timer-string", "%s with a string of code" % name, t)
            elif name == "addEventListener" and after_dot:
                arg = _literal(tokens[idx + 2] if idx + 2 < len(tokens) else None)
                if arg is not None and arg.lower() in UNSUPPORTED_EVENTS:
                    self._err("js-event-unsupported", "the %r event never fires in a widget" % arg, t)
            elif name.startswith("on") and name[2:].lower() in UNSUPPORTED_EVENTS and after_dot:
                self._err("js-event-unsupported", "%s never fires in a widget" % name, t)
            elif name == "getContext" and after_dot:
                arg = _literal(tokens[idx + 2] if idx + 2 < len(tokens) else None)
                if arg is not None and arg != "2d":
                    self._err("js-unsupported", "getContext(%r): only the 2d canvas works" % arg, t)
            elif name == "copyText" and after_dot and nxt is not None and nxt.is_punct("("):
                arg = tokens[idx + 2] if idx + 2 < len(tokens) else None
                if _literal(arg) is None:
                    self.report.warn("js-copy-text", "copyText with a computed value", t.line)
            elif name == "request" and after_dot and nxt is not None and nxt.is_punct("("):
                if prev2 is not None and (prev2.value in aliases or prev2.value == "TelegramWidget"):
                    self.uses_requests = True
            elif name == "onEvent" and after_dot:
                arg = _literal(tokens[idx + 2] if idx + 2 < len(tokens) else None)
                if arg is not None and arg not in WIDGET_EVENTS:
                    self.report.warn("js-unsupported", "TelegramWidget has no %r event" % arg, t.line)

            if name == "TelegramWidget" or name in aliases:
                self._widget_use(tokens, idx, aliases)
            if name in VALUE_ESCAPE_GLOBALS and not after_dot:
                self._global_use(tokens, idx)
            if name in open_refs and not after_dot:
                self._open_ref_use(tokens, idx, validated)

        # every string literal: URLs must be allowlisted, no javascript: URLs
        for t in tokens:
            if id(t) in validated:
                continue
            for text in _string_texts(t):
                if re.search(r"(?i)\bjavascript\s*:", text):
                    self._err("link-not-allowed", "a javascript: URL in a string", t)
                for url, problem in scan_text(text, self.allow):
                    self._err("link-not-allowed", "URL %r in a string: %s" % (url[:80], problem), t)

    # rules ---------------------------------------------------------------
    @staticmethod
    def _widget_aliases(tokens: List[Token]) -> Set[str]:
        """Names bound to the TelegramWidget object: `TW = window.TelegramWidget`, `X = TW`, ..."""
        aliases: Set[str] = set()
        changed = True
        while changed:
            changed = False
            for i, t in enumerate(tokens):
                if not (t.is_ident("TelegramWidget") or (t.kind == "ident" and t.value in aliases)):
                    continue
                after = tokens[i + 1] if i + 1 < len(tokens) else None
                if after is not None and after.is_punct(".", "?.", "[", "("):
                    continue  # `x = TW.chatData` binds a member, not the object
                j = i - 1
                if j >= 1 and tokens[j].is_punct(".", "?.") and tokens[j - 1].is_ident("window", "self"):
                    j -= 2
                if j >= 1 and tokens[j].is_punct("=") and tokens[j - 1].kind == "ident":
                    name = tokens[j - 1].value
                    if name != "TelegramWidget" and name not in aliases:
                        aliases.add(name)
                        changed = True
        return aliases

    def _widget_use(self, tokens: List[Token], idx: int, aliases: Set[str]) -> None:
        t = tokens[idx]
        prev = tokens[idx - 1] if idx > 0 else None
        nxt = tokens[idx + 1] if idx + 1 < len(tokens) else None
        # the alias declaration itself: `TW = window.TelegramWidget`
        if nxt is not None and nxt.is_punct("=") and t.value in aliases:
            return
        if prev is not None and prev.is_punct(".", "?."):
            # window.TelegramWidget: judged like a bare TelegramWidget
            if t.value != "TelegramWidget":
                return  # some_obj.TW is not our alias
        if nxt is None:
            return
        if nxt.is_punct(".", "?."):
            member = tokens[idx + 2] if idx + 2 < len(tokens) else None
            if member is not None and member.kind == "ident" and member.value not in WIDGET_MEMBERS:
                self.report.warn("js-unsupported", "TelegramWidget has no member %r" % member.value, member.line)
            return
        if prev is not None and prev.is_ident("return", "yield", "throw"):
            self._err("js-widget-escape", "%s returned from a function" % t.value, t)
            return
        if nxt.is_punct("&&", "||", "??", "?", ";", "==", "===", "!=", "!==", ":"):
            return
        if nxt.is_punct(","):
            # `const TW = window.TelegramWidget, $ = ...` is a declaration list
            j = idx - 1
            if j >= 1 and tokens[j].is_punct(".", "?.") and tokens[j - 1].is_ident("window", "self"):
                j -= 2
            if j >= 0 and tokens[j].is_punct("="):
                return
        if nxt.is_punct(")"):
            depth, j = 0, idx + 1
            while j > 0:
                j -= 1
                if tokens[j].is_punct(")"):
                    depth += 1
                elif tokens[j].is_punct("("):
                    if depth == 0:
                        break
                    depth -= 1
            before = tokens[j - 1] if j > 0 else None
            if before is None or before.is_ident("if", "while", "return", "typeof") or (
                before.kind == "punct" and before.value not in (")", "]")
            ):
                return
        if nxt.kind == "punct" and nxt.value == "=" and t.value in aliases:
            return
        self._err("js-widget-escape", "%s used as a value (passed, spread or enumerated)" % t.value, t)

    def _computed_access(self, tokens: List[Token], idx: int, prev: Token, aliases: Set[str]) -> None:
        member_access = (
            prev.kind in ("ident", "str", "template")
            and not (prev.kind == "ident" and prev.value in (
                "return", "typeof", "case", "in", "of", "new", "delete", "void", "throw", "yield", "await",
                "let", "const", "var", "else", "do"))
        ) or prev.is_punct(")", "]", "?.")
        if not member_access:
            return
        obj = tokens[idx - 2] if prev.is_punct("?.") and idx >= 2 else prev
        if obj.kind == "ident" and (obj.value in self._globals or obj.value == "TelegramWidget"
                                    or obj.value in aliases):
            self._err("js-computed-access", "computed access on %s" % obj.value, tokens[idx])
            return
        depth = 0
        for j in range(idx, len(tokens)):
            tj = tokens[j]
            if tj.is_punct("["):
                depth += 1
            elif tj.is_punct("]"):
                depth -= 1
                if depth == 0:
                    break
            elif depth == 1 and tj.kind in ("str", "template"):
                self._err("js-computed-access", "computed access with a string key", tj)
                return

    def _navigation(self, t, prev, prev2, nxt, tokens, idx) -> None:
        after_dot = prev is not None and prev.is_punct(".", "?.")
        if after_dot:
            if prev2 is not None and prev2.value in self._globals:
                self._err("js-navigation", "%s.%s: widgets cannot navigate" % (prev2.value, t.value), t)
            return
        if nxt is not None and (nxt.is_punct("=") or (
            nxt.is_punct(".") and idx + 2 < len(tokens) and tokens[idx + 2].value in (
                "href", "assign", "replace", "reload", "pushState", "replaceState", "back", "forward", "go")
        )):
            self._err("js-navigation", "%s: widgets cannot navigate" % t.value, t)

    def _single_literal_arg(self, tokens: List[Token], idx: int) -> Optional[Token]:
        """tokens[idx] is a callee name: return the string token if the call is name('literal')."""
        if idx + 3 >= len(tokens) or not tokens[idx + 1].is_punct("("):
            return None
        arg, close = tokens[idx + 2], tokens[idx + 3]
        if _literal(arg) is None or not close.is_punct(")"):
            return None
        return arg

    def _judge_link(self, arg: Token, method: str, validated: Set[int]) -> None:
        validated.add(id(arg))
        problem = link_problem(_literal(arg), self.allow, method)
        if problem:
            self._err("link-not-allowed", "%s(%r): %s" % (method, _literal(arg)[:80], problem), arg)

    def _link_call(self, tokens, idx, name, after_dot, validated) -> None:
        t = tokens[idx]
        arg = self._single_literal_arg(tokens, idx)
        if not after_dot or arg is None:
            self._err("link-dynamic", "%s must be called as TelegramWidget.%s('https://...') with one "
                                      "literal URL" % (name, name), t)
            return
        self._judge_link(arg, name, validated)

    def _open(self, tokens, idx, prev, prev2, after_dot, validated) -> None:
        t = tokens[idx]
        nxt = tokens[idx + 1] if idx + 1 < len(tokens) else None
        if not after_dot and nxt is not None and nxt.is_punct(":"):
            return  # object key (`{open: x}` destructuring is tracked by _open_refs)
        if not after_dot and prev is not None and prev.is_ident("let", "const", "var", "function"):
            return
        if nxt is not None and nxt.is_punct("(") and self._is_definition(tokens, idx + 1):
            return  # a method named open: `open(i) { ... }`
        on_global = not after_dot or (prev2 is not None and prev2.value in self._globals)
        if not on_global:
            # details.open, menu.open(): usually not window.open, but the object may be window under a
            # name the checker cannot follow (a parameter, `this`), so a call that passes anything
            # must pass one literal URL, and the method may not be taken off the object.
            if nxt is not None and nxt.is_punct(".") and idx + 2 < len(tokens) and tokens[idx + 2].is_ident(
                    "call", "apply", "bind"):
                self._err("link-dynamic", ".open.%s: open links as window.open('https://...')"
                          % tokens[idx + 2].value, t)
            elif nxt is not None and nxt.is_punct("(") and not (
                    idx + 2 < len(tokens) and tokens[idx + 2].is_punct(")")):
                self._call_with_literal_url(tokens, idx, validated,
                                            ".open(...) with an argument must take one literal URL, since its "
                                            "object could be window; name other methods differently (show, expand)")
            return
        if nxt is not None and nxt.is_punct("(") and idx + 2 < len(tokens) and tokens[idx + 2].is_punct(")"):
            return  # window.open(): no destination
        self._call_with_literal_url(tokens, idx, validated, "window.open must be called with one literal URL")

    def _call_with_literal_url(self, tokens, idx, validated, message) -> None:
        arg = self._single_literal_arg(tokens, idx)
        if arg is None:
            self._err("link-dynamic", message, tokens[idx])
        else:
            self._judge_link(arg, "href", validated)

    @staticmethod
    def _is_definition(tokens: List[Token], open_paren: int) -> bool:
        """tokens[open_paren] is '(' after a name: is this `name(...) {`, a method definition?"""
        depth = 0
        for j in range(open_paren, len(tokens)):
            if tokens[j].is_punct("("):
                depth += 1
            elif tokens[j].is_punct(")"):
                depth -= 1
                if depth == 0:
                    return j + 1 < len(tokens) and tokens[j + 1].is_punct("{")
        return False

    @staticmethod
    def _global_aliases(tokens: List[Token]) -> Set[str]:
        """Names assigned a global object as a whole: `w = window`, `p = top`, `x = w`."""
        names: Set[str] = set()
        changed = True
        while changed:
            changed = False
            for i, t in enumerate(tokens):
                if t.kind != "ident" or not (t.value in GLOBAL_OBJECTS or t.value in names):
                    continue
                if i >= 1 and tokens[i - 1].is_punct(".", "?."):
                    continue  # obj.window is some property
                after = tokens[i + 1] if i + 1 < len(tokens) else None
                if after is not None and after.kind == "punct" and after.value not in EXPR_END:
                    continue  # `x = top + 5`, `x = window.foo`: not the object itself
                if i >= 2 and tokens[i - 1].is_punct("=") and tokens[i - 2].kind == "ident":
                    name = tokens[i - 2].value
                    if name not in GLOBAL_OBJECTS and name not in names:
                        names.add(name)
                        changed = True
        return names

    @staticmethod
    def _open_refs(tokens: List[Token]) -> Set[str]:
        """Names that hold some object's open method: `o = w.open`, `const {open: o} = w`."""
        names: Set[str] = set()
        for i, t in enumerate(tokens):
            if not t.is_ident("open"):
                continue
            after = tokens[i + 1] if i + 1 < len(tokens) else None
            if i >= 1 and tokens[i - 1].is_punct(".", "?.") and (
                    after is None or after.kind != "punct" or after.value in EXPR_END):
                j = i - 1  # walk back over `a.b.c.` to the start of the member chain
                while j >= 1 and tokens[j].is_punct(".", "?.") and tokens[j - 1].kind == "ident":
                    j -= 2
                if j >= 1 and tokens[j].is_punct("=") and tokens[j - 1].kind == "ident":
                    names.add(tokens[j - 1].value)
            elif after is not None and after.is_punct(":") and i + 2 < len(tokens) and tokens[i + 2].kind == "ident":
                names.add(tokens[i + 2].value)
        names.discard("open")
        return names

    def _open_ref_use(self, tokens: List[Token], idx: int, validated: Set[int]) -> None:
        t = tokens[idx]
        prev = tokens[idx - 1] if idx > 0 else None
        nxt = tokens[idx + 1] if idx + 1 < len(tokens) else None
        if nxt is None or (prev is not None and prev.is_ident("let", "const", "var", "function")):
            return
        if nxt.is_punct(".") and idx + 2 < len(tokens) and tokens[idx + 2].is_ident("call", "apply", "bind"):
            self._err("link-dynamic", "%s holds an open method: open links as window.open('https://...')" % t.value, t)
        elif nxt.is_punct("(") and not (idx + 2 < len(tokens) and tokens[idx + 2].is_punct(")")):
            self._call_with_literal_url(tokens, idx, validated,
                                        "%s holds an open method: call it with one literal URL" % t.value)

    def _global_use(self, tokens: List[Token], idx: int) -> None:
        """window, self or document anywhere but `window.x`: as a value it could become an alias."""
        t = tokens[idx]
        prev = tokens[idx - 1] if idx > 0 else None
        nxt = tokens[idx + 1] if idx + 1 < len(tokens) else None
        if nxt is not None and nxt.is_punct(".", "?.", "[", "&&", "?", "===", "!==", "==", "!="):
            return  # member access ([ is judged as computed access), a test, a comparison
        if prev is not None and (prev.is_ident("typeof", "in", "let", "const", "var", "function", "class")
                                 or prev.is_punct("!", "===", "!==", "==", "!=")):
            return  # typeof window, 'x' in window, declaring a local named self
        if nxt is not None and nxt.is_punct("="):
            return  # assigned to, not read
        if nxt is not None and nxt.is_punct(":") and prev is not None and prev.is_punct("{", ","):
            return  # an object key named window
        self._err("js-global-escape", "%s used as a value (assigned, passed, returned or stored): use %s.<member> "
                                      "directly" % (t.value, t.value), t)

    def _link_prop(self, tokens, idx, name, validated) -> None:
        t = tokens[idx]
        prev = tokens[idx - 1] if idx > 0 else None
        if name == "src" and prev is not None and prev.is_punct("."):
            eq = tokens[idx + 1] if idx + 1 < len(tokens) else None
            val = tokens[idx + 2] if idx + 2 < len(tokens) else None
            if eq is not None and eq.is_punct("=") and _literal(val) is not None and DATA_IMAGE.match(_literal(val)):
                validated.add(id(val))
                return
        self._err("link-dynamic", "%s cannot be set or read in code (only a literal data: image src)" % name, t)

    def _set_attribute(self, tokens, idx, ns: bool) -> None:
        t = tokens[idx]
        if idx + 1 >= len(tokens) or not tokens[idx + 1].is_punct("("):
            self._err("link-dynamic", "%s used as a value" % t.value, t)
            return
        pos = idx + 2
        if ns:
            # skip the namespace argument up to the first top-level comma
            depth = 0
            while pos < len(tokens):
                tp = tokens[pos]
                if tp.is_punct("(", "[", "{"):
                    depth += 1
                elif tp.is_punct(")", "]", "}"):
                    depth -= 1
                elif tp.is_punct(",") and depth == 0:
                    pos += 1
                    break
                pos += 1
        name = _literal(tokens[pos] if pos < len(tokens) else None)
        if name is None:
            self._err("link-dynamic", "%s with a computed attribute name" % t.value, t)
            return
        low = name.lower()
        if low in LINK_ATTRS or low.split(":")[-1] in LINK_ATTRS:
            self._err("link-dynamic", "%s(%r): links and sources cannot be set in code" % (t.value, name), t)
        elif low.startswith("on"):
            self._err("js-dynamic-code", "%s(%r): handlers from strings are not allowed" % (t.value, name), t)

    def _create_element(self, tokens, idx, ns: bool) -> None:
        t = tokens[idx]
        pos = idx + 2
        if ns:
            depth = 0
            while pos < len(tokens):
                tp = tokens[pos]
                if tp.is_punct("(", "[", "{"):
                    depth += 1
                elif tp.is_punct(")", "]", "}"):
                    depth -= 1
                elif tp.is_punct(",") and depth == 0:
                    pos += 1
                    break
                pos += 1
        tag = _literal(tokens[pos] if pos < len(tokens) else None)
        # A computed tag is fine: script/iframe/... inserted from code never run or load
        # (they are removed), and links stay unreachable because href/src cannot be set.
        if tag is not None and tag.lower() in BANNED_TAGS:
            self._err("js-element", "%s(%r) is not allowed" % (t.value, tag), t)

    def finish(self) -> None:
        """Checks that need every script: element ids used as globals."""
        if not self.element_ids:
            return
        declared = set()
        for i, t in enumerate(self.all_tokens):
            if t.kind == "ident" and i > 0 and self.all_tokens[i - 1].is_ident(
                    "const", "let", "var", "function", "class"):
                declared.add(t.value)
            if t.kind == "ident" and i + 1 < len(self.all_tokens) and self.all_tokens[i + 1].is_punct("=>"):
                declared.add(t.value)
        for i, t in enumerate(self.all_tokens):
            if t.kind != "ident" or t.value not in self.element_ids or t.value in declared:
                continue
            prev = self.all_tokens[i - 1] if i > 0 else None
            nxt = self.all_tokens[i + 1] if i + 1 < len(self.all_tokens) else None
            if prev is not None and prev.is_punct(".", "?."):
                continue
            if nxt is not None and nxt.is_punct("."):
                self.report.warn("js-id-global", "%r is an element id, not a variable" % t.value, t.line)
