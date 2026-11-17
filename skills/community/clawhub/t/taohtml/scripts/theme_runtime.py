#!/usr/bin/env python3
"""Load and validate built-in or project-specific TaoHtml theme assets."""

from __future__ import annotations

import base64
import hashlib
import io
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, NamedTuple


SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from project_theme_layout import EXECUTABLE_LAYOUT_OPTIONS, validate_layout_values


SKILL_ROOT = Path(__file__).resolve().parents[1]
SYSTEMS_ROOT = SKILL_ROOT / "assets" / "visual-systems"
BUILT_IN_THEME_IDS = (
    "black-white-fluorescent-cards",
    "rigorous-consulting-report",
    "corporate-annual-report",
    "editorial-collage",
    "deep-data-dashboard",
    "warm-brand-narrative",
    "minimal-product-whitespace",
    "formal-government-bluewhite",
)
PROJECT_THEME_FILES = {"theme.json", "theme.css", "templates.html", "provenance.json"}
PROJECT_ID = re.compile(r"^project-[a-z0-9]+(?:-[a-z0-9]+)*$")
REGION_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REMOTE_ASSET = re.compile(
    r"(?:src|href)\s*=\s*['\"]\s*(?:https?:)?//|@import\b|url\(\s*['\"]?\s*(?:https?:)?//",
    re.IGNORECASE,
)
SHA256 = re.compile(r"^[0-9a-f]{64}$")
FAMILY_ROLES = ("cover", "toc", "section", "content", "data")
REPLACEMENT_PROVENANCE_FIELDS = {
    "id",
    "source_page_id",
    "source_bbox",
    "replacement",
    "replacement_strategy",
    "status",
    "basis",
    "asset_id",
    "crop_pixel_bbox",
    "source_pixel_bbox",
    "source_pixels_sha256",
    "replacement_background_rgba",
}
CORPORATE_FIXED_SHELL_CLASS = "pt-corporate-fixed-shell"
CORPORATE_FIXED_REGION_CLASS = "pt-corporate-fixed-region"
CORPORATE_EDITABLE_CLASS = "pt-corporate-editable"
ACTIVE_TEMPLATE_TAGS = {
    "applet",
    "embed",
    "iframe",
    "link",
    "object",
    "script",
    "style",
    "animate",
    "animatemotion",
    "animatetransform",
    "set",
}


class _CssDeclaration(NamedTuple):
    name: str
    value: str
    important: bool


class _CssRule(NamedTuple):
    selector: str
    declarations: tuple[_CssDeclaration, ...]


class _ElementShape(NamedTuple):
    tag: str
    classes: frozenset[str]
    element_id: str | None


class _ProtectedElement(NamedTuple):
    label: str
    tag: str
    classes: frozenset[str]
    element_id: str | None
    ancestors: tuple[_ElementShape, ...]


class ThemeBundle(NamedTuple):
    theme_id: str
    display_name: str
    kind: str
    root: Path
    manifest: dict[str, Any]
    css: str
    templates: str
    target_mode: str | None


class _CorporateTemplateParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.sections: list[dict[str, Any]] = []
        self._section: dict[str, Any] | None = None

    @staticmethod
    def _attrs(raw: list[tuple[str, str | None]]) -> dict[str, str]:
        attrs: dict[str, str] = {}
        for key, value in raw:
            if key in attrs:
                raise ValueError(
                    f"Corporate templates must not duplicate the {key} attribute."
                )
            attrs[key] = value or ""
        return attrs

    def handle_starttag(self, tag: str, raw_attrs: list[tuple[str, str | None]]) -> None:
        attrs = self._attrs(raw_attrs)
        classes = set(attrs.get("class", "").split())
        protected_classes = {
            CORPORATE_FIXED_SHELL_CLASS,
            CORPORATE_FIXED_REGION_CLASS,
            CORPORATE_EDITABLE_CLASS,
        }
        if tag in ACTIVE_TEMPLATE_TAGS:
            raise ValueError(
                f"Corporate templates must not contain active {tag} elements."
            )
        for name, value in attrs.items():
            if name.startswith("on"):
                raise ValueError(
                    f"Corporate templates must not contain event attribute {name}."
                )
            compact_value = re.sub(r"[\x00-\x20]+", "", value).lower()
            if "javascript:" in compact_value:
                raise ValueError(
                    f"Corporate templates must not contain javascript: in {name}."
                )
        if tag == "section" and "slide" in classes:
            if self._section is not None:
                raise ValueError("Corporate template sections must not be nested.")
            self._section = {
                "attrs": attrs,
                "fixed_shells": [],
                "fixed": [],
                "editable": [],
            }
            self.sections.append(self._section)
            return
        if self._section is None:
            if classes & protected_classes:
                raise ValueError(
                    "Corporate protected elements must remain inside a routed page section."
                )
            return
        if tag == "div" and CORPORATE_FIXED_SHELL_CLASS in classes:
            self._section["fixed_shells"].append(attrs)
        elif tag == "img" and CORPORATE_FIXED_REGION_CLASS in classes:
            self._section["fixed"].append(attrs)
        elif tag == "div" and CORPORATE_EDITABLE_CLASS in classes:
            self._section["editable"].append(attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == "section":
            self._section = None


def _parse_corporate_templates(templates: str) -> list[dict[str, Any]]:
    parser = _CorporateTemplateParser()
    try:
        parser.feed(templates)
        parser.close()
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("Corporate templates are not parseable HTML.") from exc
    if len(parser.sections) != 5:
        raise ValueError("Corporate themes must compile exactly five shell-routed pages.")
    return parser.sections


def _bbox_style(raw: object, label: str) -> str:
    if (
        not isinstance(raw, list)
        or len(raw) != 4
        or any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in raw)
    ):
        raise ValueError(f"{label} must be a four-number normalized bbox.")
    x, y, width, height = (float(value) for value in raw)
    if (
        x < 0
        or y < 0
        or width <= 0
        or height <= 0
        or x + width > 1 + 1e-9
        or y + height > 1 + 1e-9
    ):
        raise ValueError(f"{label} is outside normalized canvas bounds.")
    return (
        f"left:{x * 100:.6f}%;top:{y * 100:.6f}%;"
        f"width:{width * 100:.6f}%;height:{height * 100:.6f}%"
    )


def _bbox_overlap(first: object, second: object, label: str) -> bool:
    _bbox_style(first, f"{label}.first")
    _bbox_style(second, f"{label}.second")
    assert isinstance(first, list) and isinstance(second, list)
    ax, ay, aw, ah = (float(value) for value in first)
    bx, by, bw, bh = (float(value) for value in second)
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def _bbox_contains(outer: object, inner: object, label: str) -> bool:
    _bbox_style(outer, f"{label}.outer")
    _bbox_style(inner, f"{label}.inner")
    assert isinstance(outer, list) and isinstance(inner, list)
    ox, oy, ow, oh = (float(value) for value in outer)
    ix, iy, iw, ih = (float(value) for value in inner)
    tolerance = 1e-9
    return (
        ix >= ox - tolerance
        and iy >= oy - tolerance
        and ix + iw <= ox + ow + tolerance
        and iy + ih <= oy + oh + tolerance
    )


def _pixel_bbox(raw: object, label: str) -> list[int]:
    if (
        not isinstance(raw, list)
        or len(raw) != 4
        or any(not isinstance(value, int) for value in raw)
    ):
        raise ValueError(f"{label} must contain four integer pixel bounds.")
    left, top, right, bottom = raw
    if left < 0 or top < 0 or right <= left or bottom <= top:
        raise ValueError(f"{label} has invalid pixel bounds.")
    return raw


def _decode_fixed_crop(attrs: dict[str, str], expected: dict[str, Any], label: str) -> None:
    declared_hash = expected.get("crop_sha256")
    if not isinstance(declared_hash, str) or not SHA256.fullmatch(declared_hash):
        raise ValueError(f"{label} manifest crop SHA-256 is invalid.")
    source = attrs.get("src", "")
    prefix = "data:image/png;base64,"
    if not source.startswith(prefix):
        raise ValueError(f"{label} must embed a PNG data URI with the declared MIME type.")
    try:
        payload = base64.b64decode(source[len(prefix) :], validate=True)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"{label} data URI is not valid base64.") from exc
    if hashlib.sha256(payload).hexdigest() != declared_hash:
        raise ValueError(f"{label} embedded crop bytes do not match the manifest SHA-256.")
    try:
        from PIL import Image

        with Image.open(io.BytesIO(payload)) as image:
            actual_format = image.format
            actual_size = list(image.size)
            frame_count = int(getattr(image, "n_frames", 1))
            image.verify()
    except (ImportError, OSError, ValueError) as exc:
        raise ValueError(f"{label} embedded crop is not a decodable PNG.") from exc
    if actual_format != "PNG" or frame_count != 1:
        raise ValueError(f"{label} embedded crop must be one static PNG frame.")
    if actual_size != expected.get("crop_size"):
        raise ValueError(f"{label} embedded crop dimensions do not match the manifest.")
    replacements = expected.get("replaceable_regions", [])
    if replacements:
        try:
            from PIL import Image

            with Image.open(io.BytesIO(payload)) as image:
                rgba = image.convert("RGBA")
                for region in replacements:
                    pixel_bbox = region.get("crop_pixel_bbox")
                    background = region.get("replacement_background_rgba")
                    if (
                        not isinstance(pixel_bbox, list)
                        or len(pixel_bbox) != 4
                        or any(not isinstance(value, int) for value in pixel_bbox)
                        or not isinstance(background, list)
                        or len(background) != 4
                        or any(not isinstance(value, int) or not 0 <= value <= 255 for value in background)
                    ):
                        raise ValueError(
                            f"{label} replaceable-region pixel provenance is invalid."
                        )
                    cleaned = rgba.crop(tuple(pixel_bbox))
                    expected_bytes = bytes(background) * (cleaned.width * cleaned.height)
                    if cleaned.tobytes() != expected_bytes:
                        raise ValueError(
                            f"{label} still contains source pixels inside a replaceable region."
                        )
        except (ImportError, OSError, ValueError) as exc:
            if isinstance(exc, ValueError):
                raise
            raise ValueError(f"{label} replaceable-region verification failed.") from exc


def _strip_css_comments(css: str) -> str:
    stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    if "/*" in stripped or "*/" in stripped:
        raise ValueError("Corporate theme CSS contains an unterminated comment.")
    return stripped


def _find_css_delimiter(text: str, start: int, delimiter: str) -> int:
    quote = ""
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = ""
            continue
        if char in {'"', "'"}:
            quote = char
            continue
        if char == delimiter:
            return index
    return -1


def _find_css_block_end(text: str, start: int) -> int:
    depth = 1
    quote = ""
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = ""
            continue
        if char in {'"', "'"}:
            quote = char
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    return -1


def _split_css_value(raw: str, delimiter: str) -> list[str]:
    values: list[str] = []
    start = 0
    quote = ""
    escaped = False
    parentheses = 0
    brackets = 0
    for index, char in enumerate(raw):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = ""
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == "(":
            parentheses += 1
        elif char == ")":
            parentheses -= 1
        elif char == "[":
            brackets += 1
        elif char == "]":
            brackets -= 1
        elif char == delimiter and parentheses == 0 and brackets == 0:
            values.append(raw[start:index].strip())
            start = index + 1
        if parentheses < 0 or brackets < 0:
            raise ValueError("Corporate theme CSS has unbalanced selector syntax.")
    if quote or parentheses != 0 or brackets != 0:
        raise ValueError("Corporate theme CSS has unbalanced selector syntax.")
    values.append(raw[start:].strip())
    return values


def _parse_css_declarations(body: str) -> tuple[_CssDeclaration, ...]:
    declarations: list[_CssDeclaration] = []
    for raw in _split_css_value(body, ";"):
        if not raw:
            continue
        parts = _split_css_value(raw, ":")
        if len(parts) < 2:
            raise ValueError("Corporate theme CSS contains an invalid declaration.")
        name = parts[0].strip().lower()
        value = ":".join(parts[1:]).strip()
        if not name or not value:
            raise ValueError("Corporate theme CSS contains an invalid declaration.")
        important_match = re.search(r"\s*!\s*important\s*$", value, re.IGNORECASE)
        important = important_match is not None
        if important_match:
            value = value[: important_match.start()].strip()
        declarations.append(
            _CssDeclaration(name, " ".join(value.lower().split()), important)
        )
    return tuple(declarations)


def _iter_css_rules(css: str) -> list[_CssRule]:
    text = _strip_css_comments(css)
    rules: list[_CssRule] = []
    cursor = 0
    while cursor < len(text):
        if not text[cursor:].strip():
            break
        open_index = _find_css_delimiter(text, cursor, "{")
        if open_index < 0:
            raise ValueError("Corporate theme CSS has trailing content outside a rule.")
        prelude = text[cursor:open_index].strip()
        if not prelude:
            raise ValueError("Corporate theme CSS contains a rule without a selector.")
        close_index = _find_css_block_end(text, open_index + 1)
        if close_index < 0:
            raise ValueError("Corporate theme CSS contains an unterminated rule.")
        body = text[open_index + 1 : close_index]
        cursor = close_index + 1
        if ";" in prelude:
            raise ValueError(
                "Corporate theme CSS statement at-rules are unsupported for protected validation."
            )
        if prelude.startswith("@"):
            at_name = prelude[1:].split(None, 1)[0].lower()
            if at_name.endswith("keyframes") or at_name in {
                "font-face",
                "page",
                "property",
                "counter-style",
            }:
                continue
            if "{" in body:
                rules.extend(_iter_css_rules(body))
            continue
        if "{" in body or "}" in body:
            raise ValueError(
                "Corporate theme CSS nesting is unsupported for protected validation."
            )
        selectors = _split_css_value(prelude, ",")
        if not selectors or any(not selector for selector in selectors):
            raise ValueError("Corporate theme CSS contains an invalid selector list.")
        declarations = _parse_css_declarations(body)
        if not declarations:
            raise ValueError("Corporate theme CSS contains an empty rule.")
        for selector in selectors:
            rules.append(_CssRule(selector, declarations))
    return rules


def _css_compounds(selector: str) -> list[str]:
    compounds: list[str] = []
    start = 0
    quote = ""
    escaped = False
    parentheses = 0
    brackets = 0
    for index, char in enumerate(selector):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = ""
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == "(":
            parentheses += 1
        elif char == ")":
            parentheses -= 1
        elif char == "[":
            brackets += 1
        elif char == "]":
            brackets -= 1
        elif parentheses == 0 and brackets == 0 and (
            char.isspace() or char in ">+~"
        ):
            value = selector[start:index].strip()
            if value:
                compounds.append(value)
            start = index + 1
    value = selector[start:].strip()
    if value:
        compounds.append(value)
    return compounds


def _top_level_css_compound(compound: str) -> str:
    output: list[str] = []
    quote = ""
    escaped = False
    parentheses = 0
    brackets = 0
    for char in compound:
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = ""
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == "(":
            parentheses += 1
        elif char == ")":
            parentheses -= 1
        elif char == "[":
            brackets += 1
        elif char == "]":
            brackets -= 1
        elif parentheses == 0 and brackets == 0:
            output.append(char)
    return "".join(output)


def _compound_may_match(compound: str, shape: _ElementShape) -> bool:
    if not compound:
        return True
    if "\\" in compound or "|" in compound or "&" in compound:
        return True
    if re.search(
        r"(?::before|:after|::before|::after|::marker|::placeholder|::selection)\s*$",
        compound,
        re.IGNORECASE,
    ):
        return False
    functional = re.fullmatch(
        r":(?:is|where)\((?P<body>.*)\)", compound, re.IGNORECASE | re.DOTALL
    )
    if functional:
        return any(
            _compound_may_match(option, shape)
            for option in _split_css_value(functional.group("body"), ",")
        )
    top_level = _top_level_css_compound(compound)
    required_ids = set(re.findall(r"#([A-Za-z_][\w-]*)", top_level))
    if required_ids and required_ids != (
        {shape.element_id} if shape.element_id else set()
    ):
        return False
    required_classes = set(re.findall(r"\.([A-Za-z_][\w-]*)", top_level))
    if not required_classes.issubset(shape.classes):
        return False
    tag_match = re.match(r"^(?:\*|([A-Za-z][\w-]*))", top_level)
    if tag_match and tag_match.group(1) and tag_match.group(1).lower() != shape.tag:
        return False
    return True


def _selector_may_target(selector: str, element: _ProtectedElement) -> bool:
    if "\\" in selector:
        return True
    compounds = _css_compounds(selector)
    if not compounds:
        return True
    protected_classes = element.classes & {
        "pt-corporate-page",
        CORPORATE_FIXED_SHELL_CLASS,
        CORPORATE_FIXED_REGION_CLASS,
        CORPORATE_EDITABLE_CLASS,
    }
    subject = compounds[-1].lower()
    if any(protected_class.lower() in subject for protected_class in protected_classes):
        return True
    element_shape = _ElementShape(
        element.tag, element.classes, element.element_id
    )
    if not _compound_may_match(compounds[-1], element_shape):
        return False
    for compound in compounds[:-1]:
        if not any(
            _compound_may_match(compound, ancestor)
            for ancestor in element.ancestors
        ):
            return False
    return True


def _is_protected_css_property(name: str) -> bool:
    if name.startswith("--"):
        return False
    if "\\" in name:
        return True
    normalized = re.sub(r"^-[a-z]+-", "", name.lower())
    exact = {
        "all",
        "position",
        "left",
        "top",
        "right",
        "bottom",
        "width",
        "height",
        "inline-size",
        "block-size",
        "translate",
        "rotate",
        "scale",
        "display",
        "visibility",
        "opacity",
        "zoom",
        "z-index",
        "isolation",
        "pointer-events",
        "object-fit",
        "box-sizing",
    }
    prefixes = (
        "animation",
        "transition",
        "transform",
        "inset",
        "overflow",
        "margin",
        "min-width",
        "max-width",
        "min-height",
        "max-height",
        "min-inline-size",
        "max-inline-size",
        "min-block-size",
        "max-block-size",
        "offset",
    )
    return normalized in exact or normalized.startswith(prefixes)


def _declaration_map(
    declarations: tuple[_CssDeclaration, ...], label: str
) -> dict[str, tuple[str, bool]]:
    values: dict[str, tuple[str, bool]] = {}
    for declaration in declarations:
        if declaration.name in values:
            raise ValueError(f"{label} repeats the {declaration.name} declaration.")
        values[declaration.name] = (declaration.value, declaration.important)
    return values


def _validate_fixed_css(css: str, theme_id: str) -> None:
    scope = f'.deck[data-theme="{theme_id}"]'
    expected_rules = {
        f"{scope} .slide.pt-corporate-page": {
            "position": ("absolute", False),
            "isolation": ("isolate", False),
            "overflow": ("hidden", False),
            "padding": ("0", False),
            "background": ("var(--pt-canvas)", False),
        },
        f"{scope} .{CORPORATE_FIXED_SHELL_CLASS}": {
            "position": ("absolute", False),
            "inset": ("0", False),
            "z-index": ("3", False),
            "overflow": ("hidden", False),
            "pointer-events": ("none", False),
            "animation": ("none", True),
            "transition": ("none", True),
            "transform": ("none", True),
        },
        f"{scope} .{CORPORATE_FIXED_REGION_CLASS}": {
            "position": ("absolute", False),
            "z-index": ("1", False),
            "display": ("block", False),
            "object-fit": ("fill", False),
            "pointer-events": ("none", False),
            "animation": ("none", True),
            "transition": ("none", True),
            "transform": ("none", True),
        },
        f"{scope} .{CORPORATE_EDITABLE_CLASS}": {
            "position": ("absolute", False),
            "z-index": ("2", False),
            "display": ("grid", False),
            "align-content": ("center", False),
            "overflow": ("hidden", False),
            "padding": ("18px", False),
        },
    }
    html = _ElementShape("html", frozenset(), None)
    body = _ElementShape("body", frozenset(), None)
    deck = _ElementShape("main", frozenset({"deck"}), "deck")
    generic_page = _ElementShape(
        "section", frozenset({"slide", "pt-corporate-page"}), None
    )
    active_family_page = _ElementShape(
        "section", frozenset({"slide", "active", "pt-corporate-page"}), None
    )
    active_legacy_cover = _ElementShape(
        "section",
        frozenset({"slide", "active", "pt-cover", "pt-corporate-page"}),
        None,
    )
    page_ancestors = (deck, body, html)
    page_shapes = (generic_page, active_family_page, active_legacy_cover)
    shell = _ElementShape(
        "div", frozenset({CORPORATE_FIXED_SHELL_CLASS}), None
    )
    protected_pages = (
        _ProtectedElement(
            "corporate page",
            "section",
            frozenset({"slide", "pt-corporate-page"}),
            None,
            page_ancestors,
        ),
        _ProtectedElement(
            "active corporate page",
            "section",
            frozenset({"slide", "active", "pt-corporate-page"}),
            None,
            page_ancestors,
        ),
        _ProtectedElement(
            "legacy corporate cover",
            "section",
            frozenset({"slide", "active", "pt-cover", "pt-corporate-page"}),
            None,
            page_ancestors,
        ),
    )
    protected_fixed = (
        _ProtectedElement(
            "fixed shell",
            "div",
            frozenset({CORPORATE_FIXED_SHELL_CLASS}),
            None,
            page_shapes + page_ancestors,
        ),
        _ProtectedElement(
            "fixed region",
            "img",
            frozenset({CORPORATE_FIXED_REGION_CLASS}),
            None,
            (shell,) + page_shapes + page_ancestors,
        ),
    )
    protected_editable = (
        _ProtectedElement(
            "editable region",
            "div",
            frozenset({CORPORATE_EDITABLE_CLASS}),
            None,
            page_shapes + page_ancestors,
        ),
    )
    found = {selector: 0 for selector in expected_rules}
    for rule in _iter_css_rules(css):
        if rule.selector in expected_rules:
            found[rule.selector] += 1
            actual = _declaration_map(
                rule.declarations, f"Corporate canonical CSS rule {rule.selector}"
            )
            if actual != expected_rules[rule.selector]:
                raise ValueError(
                    "Corporate fixed shell CSS must disable fixed-element animation "
                    "and preserve protected geometry."
                )
            continue
        non_custom = [
            declaration
            for declaration in rule.declarations
            if not declaration.name.startswith("--")
        ]
        if non_custom:
            for element in protected_fixed:
                if _selector_may_target(rule.selector, element):
                    properties = ", ".join(
                        sorted({declaration.name for declaration in non_custom})
                    )
                    raise ValueError(
                        f"Corporate fixed-layer CSS rule {rule.selector!r} is not "
                        f"the unique canonical rule and declares: {properties}."
                    )
        risky = [
            declaration
            for declaration in rule.declarations
            if _is_protected_css_property(declaration.name)
        ]
        if not risky:
            continue
        for element in protected_pages + protected_editable:
            if _selector_may_target(rule.selector, element):
                properties = ", ".join(
                    sorted({declaration.name for declaration in risky})
                )
                raise ValueError(
                    f"Corporate protected CSS rule {rule.selector!r} may override "
                    f"{element.label} properties: {properties}."
                )
    if any(count != 1 for count in found.values()):
        raise ValueError(
            "Corporate fixed shell CSS must define every canonical protected rule exactly once."
        )


def _validate_exact_attributes(
    attrs: dict[str, str], expected: dict[str, str], label: str
) -> None:
    if attrs != expected:
        raise ValueError(f"{label} attributes or classes drifted from the allowlist.")


def _validate_section_attributes(
    attrs: dict[str, str], page_index: int, *, family: bool
) -> None:
    expected_class = "slide pt-corporate-page"
    if page_index == 0:
        expected_class = (
            "slide active pt-corporate-page"
            if family
            else "slide active pt-cover pt-corporate-page"
        )
    expected_keys = {"class", "data-title", "data-layout"}
    if family:
        expected_keys |= {
            "data-shell-role",
            "data-shell-status",
            "data-source-page-id",
        }
    if set(attrs) != expected_keys or attrs.get("class") != expected_class:
        raise ValueError(
            f"Corporate page {page_index + 1} attributes or classes drifted from the allowlist."
        )


def _validate_fixed_shell_attributes(attrs: dict[str, str], label: str) -> None:
    _validate_exact_attributes(
        attrs,
        {
            "class": CORPORATE_FIXED_SHELL_CLASS,
            "aria-hidden": "true",
            "data-fixed-motion": "none",
        },
        label,
    )


def _validate_editable_attributes(attrs: dict[str, str], label: str) -> None:
    expected_keys = {
        "class",
        "data-editable-region",
        "data-content-role",
        "style",
    }
    if set(attrs) != expected_keys or attrs.get("class") != CORPORATE_EDITABLE_CLASS:
        raise ValueError(f"{label} attributes or classes drifted from the allowlist.")


def _validate_actual_fixed_element(
    attrs: dict[str, str], expected: dict[str, Any], label: str
) -> None:
    expected_keys = {
        "class",
        "data-locked-region",
        "data-fixed-element-type",
        "data-crop-sha256",
        "src",
        "alt",
        "style",
    }
    if "asset_id" in expected:
        expected_keys |= {"data-asset-id", "data-source-page-id"}
    if (
        set(attrs) != expected_keys
        or attrs.get("class") != CORPORATE_FIXED_REGION_CLASS
        or attrs.get("alt") != ""
    ):
        raise ValueError(f"{label} attributes or classes drifted from the allowlist.")
    expected_attrs = {
        "data-locked-region": expected.get("id"),
        "data-fixed-element-type": expected.get("type"),
        "data-crop-sha256": expected.get("crop_sha256"),
    }
    if "asset_id" in expected:
        expected_attrs["data-asset-id"] = expected.get("asset_id")
        expected_attrs["data-source-page-id"] = expected.get("source_page_id")
    for name, value in expected_attrs.items():
        if not isinstance(value, str) or attrs.get(name) != value:
            raise ValueError(f"{label} attribute {name} drifted from the manifest.")
    if attrs.get("style") != _bbox_style(expected.get("bbox"), f"{label}.bbox"):
        raise ValueError(f"{label} fixed placement drifted from the manifest bbox.")
    if "fragment" in attrs.get("class", "").split():
        raise ValueError(f"{label} must never use fragment motion.")
    _decode_fixed_crop(attrs, expected, label)


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"{label} is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} is not valid JSON: {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"{label} must be a JSON object: {path}")
    return raw


def _read_theme_assets(root: Path, manifest: dict[str, Any]) -> tuple[str, str]:
    files = manifest.get("files")
    if not isinstance(files, dict):
        raise ValueError(f"Theme manifest files must be an object: {root / 'theme.json'}")
    if files.get("tokens") != "theme.css" or files.get("templates") != "templates.html":
        raise ValueError("Theme manifest must route tokens to theme.css and templates to templates.html.")
    css_path = root / "theme.css"
    templates_path = root / "templates.html"
    try:
        css = css_path.read_text(encoding="utf-8").strip()
        templates = templates_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise ValueError(f"Theme asset is missing: {exc.filename}") from exc
    if not css or not templates:
        raise ValueError(f"Theme CSS and templates must be non-empty: {root}")
    if "</style" in css.lower():
        raise ValueError(f"Theme CSS contains a closing style tag: {root}")
    if REMOTE_ASSET.search(css + templates):
        raise ValueError(f"Theme contains a remote asset reference: {root}")
    if templates.count('<section class="slide') < 5:
        raise ValueError("A theme must provide at least five slide templates.")
    for marker in ("data-layout=", "fragment", "data-step="):
        if marker not in templates:
            raise ValueError(f"Theme templates are missing required marker: {marker}")
    return css, templates


def _validate_legacy_corporate_shell(
    shell: dict[str, Any], sections: list[dict[str, Any]]
) -> None:
    fixed = shell.get("fixed_elements")
    editable = shell.get("editable_region")
    if (
        not isinstance(fixed, list)
        or not fixed
        or not isinstance(editable, dict)
        or shell.get("fixed_motion") != "none"
        or shell.get("content_motion_scope") != "editable_region_only"
        or shell.get("full_screenshot_background") is not False
        or shell.get("logo_redraw") is not False
    ):
        raise ValueError("Corporate shell safety contract is incomplete.")
    ids = [region.get("id") for region in fixed if isinstance(region, dict)]
    if len(ids) != len(fixed) or any(not isinstance(value, str) for value in ids) or len(set(ids)) != len(ids):
        raise ValueError("Corporate fixed element ids must be unique strings.")
    editable_id = editable.get("id")
    allowed = editable.get("allowed_content")
    if not isinstance(editable_id, str) or not isinstance(allowed, list):
        raise ValueError("Corporate editable region contract is invalid.")
    for page_index, section in enumerate(sections):
        _validate_section_attributes(section["attrs"], page_index, family=False)
        if len(section["fixed_shells"]) != 1:
            raise ValueError(f"Corporate page {page_index + 1} must contain one static fixed shell.")
        _validate_fixed_shell_attributes(
            section["fixed_shells"][0],
            f"Corporate page {page_index + 1} fixed shell",
        )
        actual_fixed = section["fixed"]
        if len(actual_fixed) != len(fixed):
            raise ValueError(f"Corporate page {page_index + 1} fixed crop count drifted.")
        actual_by_id = {item.get("data-locked-region"): item for item in actual_fixed}
        if set(actual_by_id) != set(ids):
            raise ValueError(f"Corporate page {page_index + 1} fixed region ids drifted.")
        for expected in fixed:
            if _bbox_overlap(
                expected.get("bbox"), editable.get("bbox"), "legacy corporate shell"
            ):
                raise ValueError("Corporate fixed element overlaps the editable region.")
            _validate_actual_fixed_element(
                actual_by_id[expected["id"]], expected, f"corporate page {page_index + 1} region {expected['id']}"
            )
        if len(section["editable"]) != 1:
            raise ValueError(f"Corporate page {page_index + 1} must contain one editable region.")
        actual_editable = section["editable"][0]
        _validate_editable_attributes(
            actual_editable, f"Corporate page {page_index + 1} editable region"
        )
        if (
            actual_editable.get("data-editable-region") != editable_id
            or actual_editable.get("data-content-role") not in allowed
            or actual_editable.get("style")
            != _bbox_style(editable.get("bbox"), "corporate_shell.editable_region.bbox")
        ):
            raise ValueError(f"Corporate page {page_index + 1} editable region drifted.")


def _validate_corporate_family(
    family: dict[str, Any], sections: list[dict[str, Any]]
) -> None:
    pages = family.get("reference_pages")
    assets = family.get("shared_assets")
    shells = family.get("shell_variants")
    grammar = family.get("shared_brand_grammar")
    extensions = family.get("extension_pages")
    replacements = family.get("replaceable_regions", [])
    if not all(
        isinstance(value, list)
        for value in (pages, assets, shells, extensions, replacements)
    ) or not isinstance(grammar, dict):
        raise ValueError("Corporate template family contract is incomplete.")
    if (
        grammar.get("fixed_motion") != "none"
        or grammar.get("content_motion_scope") != "editable_regions_only"
        or grammar.get("asset_strategy") != "source_crops_only"
        or grammar.get("canvas_aspect_ratio") != "16:9"
        or grammar.get("full_screenshot_background") is not False
        or grammar.get("logo_redraw") is not False
    ):
        raise ValueError("Corporate template family safety grammar is invalid.")
    page_by_id: dict[str, dict[str, Any]] = {}
    role_sources: dict[str, str] = {}
    for page in pages:
        if not isinstance(page, dict):
            raise ValueError("Corporate reference page must be an object.")
        page_id, role = page.get("id"), page.get("role")
        if (
            not isinstance(page_id, str)
            or page_id in page_by_id
            or role not in FAMILY_ROLES
            or role in role_sources
            or page.get("status") != "observed"
        ):
            raise ValueError("Corporate reference page role or id is invalid.")
        _bbox_style(page.get("canvas_bbox"), f"reference page {page_id}.canvas_bbox")
        page_by_id[page_id] = page
        role_sources[str(role)] = page_id
    if not 1 <= len(page_by_id) <= 3:
        raise ValueError("Corporate template family must bind one to three source pages.")

    asset_by_id: dict[str, dict[str, Any]] = {}
    for asset in assets:
        if not isinstance(asset, dict):
            raise ValueError("Corporate shared asset must be an object.")
        asset_id = asset.get("id")
        source_page_id = asset.get("source_page_id")
        if (
            not isinstance(asset_id, str)
            or asset_id in asset_by_id
            or source_page_id not in page_by_id
            or asset.get("status") != "observed"
            or asset.get("extraction") != "crop"
            or asset.get("source_image_sha256")
            != page_by_id[str(source_page_id)].get("source_image", {}).get("sha256")
            or not isinstance(asset.get("crop_sha256"), str)
            or not SHA256.fullmatch(asset["crop_sha256"])
        ):
            raise ValueError("Corporate shared asset provenance is invalid.")
        crop_size = asset.get("crop_size")
        source_pixel_bbox = _pixel_bbox(
            asset.get("source_pixel_bbox"),
            f"shared asset {asset_id}.source_pixel_bbox",
        )
        if (
            not isinstance(crop_size, list)
            or len(crop_size) != 2
            or any(not isinstance(value, int) or value <= 0 for value in crop_size)
            or crop_size
            != [
                source_pixel_bbox[2] - source_pixel_bbox[0],
                source_pixel_bbox[3] - source_pixel_bbox[1],
            ]
        ):
            raise ValueError("Corporate shared asset crop geometry is invalid.")
        asset_replacements = asset.get("replaceable_regions", [])
        if not isinstance(asset_replacements, list) or len(asset_replacements) > 12:
            raise ValueError("Corporate shared asset replaceable regions are invalid.")
        source_crop_sha256 = asset.get("source_crop_sha256")
        if (
            source_crop_sha256 is not None
            and (
                not isinstance(source_crop_sha256, str)
                or not SHA256.fullmatch(source_crop_sha256)
            )
        ) or (asset_replacements and source_crop_sha256 is None):
            raise ValueError("Corporate shared asset source-crop provenance is invalid.")
        for region in asset_replacements:
            if (
                not isinstance(region, dict)
                or set(region) != REPLACEMENT_PROVENANCE_FIELDS
                or not isinstance(region.get("id"), str)
                or not REGION_ID.fullmatch(region["id"])
                or region.get("asset_id") != asset_id
                or region.get("source_page_id") != source_page_id
                or region.get("replacement") != "runtime_page_number"
                or region.get("replacement_strategy") != "sampled_edge_fill"
                or region.get("status") != "observed"
                or not isinstance(region.get("basis"), str)
                or not region["basis"].strip()
                or not isinstance(region.get("source_pixels_sha256"), str)
                or not SHA256.fullmatch(region["source_pixels_sha256"])
                or not isinstance(region.get("replacement_background_rgba"), list)
                or len(region["replacement_background_rgba"]) != 4
                or any(
                    not isinstance(value, int) or not 0 <= value <= 255
                    for value in region["replacement_background_rgba"]
                )
                or not _bbox_contains(
                    asset.get("source_bbox"),
                    region.get("source_bbox"),
                    f"shared asset {asset_id} replacement {region.get('id')}",
                )
            ):
                raise ValueError("Corporate shared asset replacement provenance is invalid.")
            crop_pixel_bbox = _pixel_bbox(
                region.get("crop_pixel_bbox"),
                f"shared asset {asset_id} replacement crop_pixel_bbox",
            )
            replacement_source_bbox = _pixel_bbox(
                region.get("source_pixel_bbox"),
                f"shared asset {asset_id} replacement source_pixel_bbox",
            )
            if (
                crop_pixel_bbox[2] > crop_size[0]
                or crop_pixel_bbox[3] > crop_size[1]
                or replacement_source_bbox
                != [
                    source_pixel_bbox[0] + crop_pixel_bbox[0],
                    source_pixel_bbox[1] + crop_pixel_bbox[1],
                    source_pixel_bbox[0] + crop_pixel_bbox[2],
                    source_pixel_bbox[1] + crop_pixel_bbox[3],
                ]
            ):
                raise ValueError("Corporate shared asset replacement geometry is invalid.")
        _bbox_style(asset.get("source_bbox"), f"shared asset {asset_id}.source_bbox")
        if asset.get("source_bbox") == [0.0, 0.0, 1.0, 1.0]:
            raise ValueError("Corporate shared asset must not be a complete screenshot canvas.")
        asset_by_id[asset_id] = asset
    if not asset_by_id:
        raise ValueError("Corporate template family must contain shared cropped assets.")
    flattened_replacements = [
        region
        for asset in assets
        if isinstance(asset, dict)
        for region in asset.get("replaceable_regions", [])
    ]
    replacement_ids = {
        region.get("id") for region in flattened_replacements
    }
    if (
        len(replacements) > 12
        or len(replacement_ids) != len(flattened_replacements)
        or replacements != flattened_replacements
    ):
        raise ValueError("Corporate replaceable-region manifest does not match cleaned assets.")

    shell_by_role: dict[str, dict[str, Any]] = {}
    extension_roles = {
        item.get("role")
        for item in extensions
        if isinstance(item, dict) and item.get("status") == "extension"
    }
    for shell in shells:
        if not isinstance(shell, dict):
            raise ValueError("Corporate shell variant must be an object.")
        role = shell.get("role")
        status = shell.get("status")
        source_page_id = shell.get("reference_page_id")
        if role not in FAMILY_ROLES or role in shell_by_role or status not in {"observed", "extension"}:
            raise ValueError("Corporate shell role or status is invalid.")
        if status == "observed":
            if source_page_id != role_sources.get(str(role)):
                raise ValueError(f"Corporate {role} shell source-page mapping drifted.")
        elif source_page_id is not None or role in role_sources or role not in extension_roles:
            raise ValueError(f"Corporate {role} extension shell mapping is invalid.")
        editable = shell.get("editable_region")
        fixed = shell.get("fixed_regions")
        if (
            not isinstance(editable, dict)
            or editable.get("allowed_content") != [role]
            or not isinstance(fixed, list)
            or not fixed
        ):
            raise ValueError(f"Corporate {role} shell regions are invalid.")
        _bbox_style(editable.get("bbox"), f"corporate {role} editable bbox")
        fixed_ids: set[str] = set()
        for placement in fixed:
            if not isinstance(placement, dict):
                raise ValueError(f"Corporate {role} fixed region must be an object.")
            region_id, asset_id = placement.get("id"), placement.get("asset_id")
            asset = asset_by_id.get(str(asset_id))
            if (
                not isinstance(region_id, str)
                or region_id in fixed_ids
                or asset is None
                or placement.get("type") != asset.get("type")
                or placement.get("source_page_id") != asset.get("source_page_id")
                or placement.get("source_image_sha256") != asset.get("source_image_sha256")
                or placement.get("source_bbox") != asset.get("source_bbox")
                or placement.get("source_pixel_bbox") != asset.get("source_pixel_bbox")
                or placement.get("source_crop_sha256") != asset.get("source_crop_sha256")
                or placement.get("replaceable_regions") != asset.get("replaceable_regions")
                or placement.get("crop_sha256") != asset.get("crop_sha256")
                or placement.get("crop_size") != asset.get("crop_size")
                or placement.get("status") != status
            ):
                raise ValueError(f"Corporate {role} fixed region provenance drifted.")
            fixed_ids.add(region_id)
            _bbox_style(placement.get("bbox"), f"corporate {role} region {region_id}.bbox")
            if _bbox_overlap(
                placement.get("bbox"), editable.get("bbox"), f"corporate {role} shell"
            ):
                raise ValueError(f"Corporate {role} fixed region overlaps its editable region.")
        shell_by_role[str(role)] = shell
    if tuple(role for role in FAMILY_ROLES if role in shell_by_role) != FAMILY_ROLES or len(shell_by_role) != 5:
        raise ValueError("Corporate template family must define all five shell roles.")
    if extension_roles != {role for role, shell in shell_by_role.items() if shell["status"] == "extension"}:
        raise ValueError("Corporate extension page declarations do not match shell variants.")

    actual_roles: list[str] = []
    for page_index, section in enumerate(sections):
        _validate_section_attributes(section["attrs"], page_index, family=True)
        attrs = section["attrs"]
        role = attrs.get("data-shell-role")
        actual_roles.append(str(role))
        shell = shell_by_role.get(str(role))
        if shell is None:
            raise ValueError("Corporate page routed to an unknown shell role.")
        if (
            attrs.get("data-shell-status") != shell["status"]
            or attrs.get("data-source-page-id") != (shell["reference_page_id"] or "")
        ):
            raise ValueError(f"Corporate {role} page role or source mapping drifted.")
        if len(section["fixed_shells"]) != 1:
            raise ValueError(f"Corporate {role} page must contain one static fixed shell.")
        _validate_fixed_shell_attributes(
            section["fixed_shells"][0], f"Corporate {role} fixed shell"
        )
        fixed = shell["fixed_regions"]
        actual_fixed = section["fixed"]
        if len(actual_fixed) != len(fixed):
            raise ValueError(f"Corporate {role} fixed crop count drifted.")
        actual_by_id = {item.get("data-locked-region"): item for item in actual_fixed}
        if set(actual_by_id) != {item["id"] for item in fixed}:
            raise ValueError(f"Corporate {role} fixed region ids drifted.")
        for expected in fixed:
            _validate_actual_fixed_element(
                actual_by_id[expected["id"]], expected, f"corporate {role} region {expected['id']}"
            )
        if len(section["editable"]) != 1:
            raise ValueError(f"Corporate {role} page must contain one editable region.")
        actual_editable = section["editable"][0]
        _validate_editable_attributes(
            actual_editable, f"Corporate {role} editable region"
        )
        editable = shell["editable_region"]
        if (
            actual_editable.get("data-editable-region") != editable.get("id")
            or actual_editable.get("data-content-role") != role
            or actual_editable.get("style")
            != _bbox_style(editable.get("bbox"), f"corporate {role} editable bbox")
        ):
            raise ValueError(f"Corporate {role} editable region drifted.")
    if actual_roles != list(FAMILY_ROLES):
        raise ValueError("Corporate report pages must route cover, toc, section, content, and data in order.")


def _validate_project_structure(
    manifest: dict[str, Any], provenance: dict[str, Any], templates: str, css: str
) -> None:
    layout = manifest.get("executable_layout")
    sources = manifest.get("structure_sources")
    if not isinstance(layout, dict) or set(layout) != set(EXECUTABLE_LAYOUT_OPTIONS):
        raise ValueError("Project theme executable_layout contract is incomplete.")
    if not isinstance(sources, dict) or set(sources) != set(EXECUTABLE_LAYOUT_OPTIONS):
        raise ValueError("Project theme structure_sources contract is incomplete.")
    for field, options in EXECUTABLE_LAYOUT_OPTIONS.items():
        if layout[field] not in options:
            raise ValueError(f"Project theme executable_layout.{field} is invalid.")
    validate_layout_values(layout)

    raw_records = provenance.get("boundary_records")
    raw_fallbacks = provenance.get("fallback_records")
    if not isinstance(raw_records, list) or not isinstance(raw_fallbacks, list):
        raise ValueError("Project theme provenance must include boundary and fallback records.")
    records = {
        record.get("path"): record for record in raw_records if isinstance(record, dict)
    }
    fallbacks = {
        record.get("field"): record
        for record in raw_fallbacks
        if isinstance(record, dict) and isinstance(record.get("field"), str)
    }
    for record in raw_records:
        if not isinstance(record, dict):
            raise ValueError("Project theme provenance boundary record must be an object.")
        compiled = record.get("compiled")
        eligible = record.get("eligible")
        usage = record.get("usage")
        if not isinstance(compiled, bool) or not isinstance(eligible, bool) or not isinstance(usage, list):
            raise ValueError("Project theme provenance eligible, compiled, and usage fields are invalid.")
        if eligible != (record.get("status") in {"observed", "extension"}):
            raise ValueError("Project theme provenance eligibility does not match boundary status.")
        if compiled != bool(usage) or (compiled and record.get("status") == "unknown"):
            raise ValueError("Project theme provenance compiled state does not match usage targets.")

    for field, source in sources.items():
        if not isinstance(source, dict):
            raise ValueError(f"Project theme structure_sources.{field} must be an object.")
        status = source.get("status")
        usage = source.get("usage")
        source_path = source.get("source")
        if not isinstance(usage, list) or not usage:
            raise ValueError(f"Project theme structure_sources.{field} requires usage targets.")
        contract_path = f"executable_layout.{field}"
        if status == "fallback":
            fallback = fallbacks.get(contract_path)
            boundary = records.get(contract_path)
            if (
                source_path != "compiler-neutral-default"
                or not isinstance(fallback, dict)
                or fallback.get("status") != "fallback"
                or fallback.get("value") != layout[field]
                or set(fallback.get("usage", [])) != set(usage)
                or not isinstance(boundary, dict)
                or boundary.get("status") != "unknown"
                or boundary.get("compiled") is not False
            ):
                raise ValueError(f"Project theme fallback provenance mismatch for {field}.")
        else:
            record = records.get(contract_path)
            if (
                source_path != contract_path
                or status not in {"observed", "extension"}
                or not isinstance(record, dict)
                or record.get("status") != status
                or record.get("value") != layout[field]
                or record.get("compiled") is not True
                or set(record.get("usage", [])) != set(usage)
            ):
                raise ValueError(f"Project theme compiled provenance mismatch for {field}.")

    variants = manifest.get("layout_variants")
    if not isinstance(variants, list) or any(
        not isinstance(item, dict) or not isinstance(item.get("id"), str)
        for item in variants
    ):
        raise ValueError("Project theme layout_variants contract is invalid.")
    manifest_ids = [item["id"] for item in variants]
    template_ids = re.findall(r'data-layout="([^"]+)"', templates)
    if template_ids != manifest_ids:
        raise ValueError("Project theme templates do not match manifest layout_variants.")
    identity = manifest.get("identity")
    if not isinstance(identity, dict) or not isinstance(identity.get("composition"), str) or not identity["composition"].strip():
        raise ValueError("Project theme identity.composition must be non-empty.")

    project = manifest.get("project")
    reference_mode = project.get("reference_mode", "reconstruct") if isinstance(project, dict) else None
    if reference_mode not in {"reconstruct", "corporate_fidelity"}:
        raise ValueError("Project theme reference_mode is invalid.")
    if reference_mode == "corporate_fidelity":
        sections = _parse_corporate_templates(templates)
        family = manifest.get("corporate_template_family")
        shell = manifest.get("corporate_shell")
        provenance_contract = provenance.get("corporate_fidelity")
        if family is not None:
            if not isinstance(family, dict) or shell is not None or provenance_contract != family:
                raise ValueError("Corporate template family manifest and provenance must match exactly.")
            _validate_corporate_family(family, sections)
        else:
            if not isinstance(shell, dict) or provenance_contract != shell:
                raise ValueError("Corporate shell manifest and provenance must match exactly.")
            _validate_legacy_corporate_shell(shell, sections)
        theme_id = manifest.get("id")
        if not isinstance(theme_id, str):
            raise ValueError("Corporate project theme id is invalid.")
        _validate_fixed_css(css, theme_id)


def load_built_in_theme(theme_id: str) -> ThemeBundle:
    if theme_id not in BUILT_IN_THEME_IDS:
        raise ValueError(f"Unknown theme: {theme_id}")
    root = SYSTEMS_ROOT / theme_id
    manifest = _load_json(root / "theme.json", "Theme manifest")
    if manifest.get("id") != theme_id:
        raise ValueError(f"Theme manifest id mismatch: {root / 'theme.json'}")
    css, templates = _read_theme_assets(root, manifest)
    return ThemeBundle(
        theme_id=theme_id,
        display_name=str(manifest.get("display_name", theme_id)),
        kind="built-in",
        root=root,
        manifest=manifest,
        css=css,
        templates=templates,
        target_mode=None,
    )


def load_project_theme(theme_dir: Path) -> ThemeBundle:
    supplied = theme_dir.expanduser()
    if supplied.is_symlink():
        raise ValueError(f"Project theme directory must not be a symlink: {supplied}")
    try:
        root = supplied.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"Project theme directory does not exist: {theme_dir}") from exc
    if not root.is_dir():
        raise ValueError(f"Project theme path is not a directory: {root}")
    actual = {path.name for path in root.iterdir()}
    if actual != PROJECT_THEME_FILES:
        missing = ", ".join(sorted(PROJECT_THEME_FILES - actual)) or "none"
        extra = ", ".join(sorted(actual - PROJECT_THEME_FILES)) or "none"
        raise ValueError(
            f"Project theme directory is incomplete; missing: {missing}; extra: {extra}."
        )
    if any(path.is_symlink() or not path.is_file() for path in root.iterdir()):
        raise ValueError(f"Project theme assets must be regular files, not symlinks: {root}")

    manifest = _load_json(root / "theme.json", "Project theme manifest")
    if manifest.get("schema_version") != "1.0" or manifest.get("kind") != "project":
        raise ValueError("Project theme manifest must declare schema_version 1.0 and kind project.")
    theme_id = manifest.get("id")
    if not isinstance(theme_id, str) or not PROJECT_ID.fullmatch(theme_id):
        raise ValueError("Project theme id must use the project-<slug> form.")
    if manifest.get("files") != {
        "tokens": "theme.css",
        "templates": "templates.html",
        "provenance": "provenance.json",
    }:
        raise ValueError("Project theme manifest files contract is invalid.")
    project = manifest.get("project")
    if not isinstance(project, dict) or project.get("target_mode") not in {
        "reading",
        "presentation",
    }:
        raise ValueError("Project theme target mode must be reading or presentation.")

    provenance = _load_json(root / "provenance.json", "Project theme provenance")
    if provenance.get("schema_version") != "1.0" or provenance.get("theme_id") != theme_id:
        raise ValueError("Project theme provenance does not match the manifest.")
    css, templates = _read_theme_assets(root, manifest)
    _validate_project_structure(manifest, provenance, templates, css)
    selector = f'.deck[data-theme="{theme_id}"]'
    if selector not in css:
        raise ValueError(f"Project theme CSS is not scoped to {selector}.")
    return ThemeBundle(
        theme_id=theme_id,
        display_name=str(manifest.get("display_name", theme_id)),
        kind="project",
        root=root,
        manifest=manifest,
        css=css,
        templates=templates,
        target_mode=str(project["target_mode"]),
    )
