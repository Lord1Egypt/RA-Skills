#!/usr/bin/env python3
"""
Generate styled HTML resume from JSON data.
Supports multiple themes and languages.
"""

import argparse
import html as html_escape
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from resume_utils import (
    DEFAULT_THEME,
    SUPPORTED_LANGUAGES,
    list_available_themes,
    get_localized_text,
    normalize_resume_data,
    resolve_theme_assets,
    resolve_photo_src,
    validate_resume_data,
    ensure_string_list,
)


def escape_text(text):
    """Escape HTML special characters to prevent injection."""
    if text is None:
        return ""
    return html_escape.escape(str(text))


# Whitelisted CSS color keywords for the ==text|color== syntax.
_COLOR_NAMED = {
    "black", "white", "red", "crimson", "firebrick", "darkred",
    "orange", "darkorange", "coral",
    "gold", "yellow", "goldenrod",
    "green", "forestgreen", "seagreen", "darkgreen", "olive", "teal",
    "blue", "navy", "royalblue", "steelblue", "deepskyblue", "darkblue",
    "purple", "indigo", "darkviolet", "mediumorchid",
    "brown", "saddlebrown", "sienna",
    "gray", "grey", "darkgray", "darkgrey", "dimgray", "slategray",
    "maroon",
}
_COLOR_HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
# ==text|colorspec== — text may contain anything except `|` and `==`.
_COLOR_RUN_RE = re.compile(r"==([^|=]+)\|([^=]+)==")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC_RE = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)")
_UNDERLINE_RE = re.compile(r"(?<![_\w])_([^_\n]+)_(?![_\w])")


def _validate_color(spec):
    """Return a safe CSS color value or None if the spec is not whitelisted."""
    spec = spec.strip()
    if not spec:
        return None
    if _COLOR_HEX_RE.match(spec):
        return spec
    lowered = spec.lower()
    if lowered in _COLOR_NAMED:
        return lowered
    return None


def render_rich_text(text):
    """Render a restricted Markdown subset to an HTML string.

    Supported inline syntax (after HTML-escaping the raw text):
      **bold**    -> <strong>bold</strong>
      *italic*    -> <em>italic</em>
      _underline_ -> <u>underline</u>
      ==text|colorspec== -> <span style="color:...">text</span>
                           (colorspec must be a hex color or whitelisted
                            CSS named color; otherwise the run is left as
                            literal text).

    The order matters: color runs are parsed first so their inner contents
    can still carry bold/italic/underline. Bold before italic to avoid the
    `**` consuming single `*` markers.
    """
    if text is None:
        return ""
    raw = str(text)
    escaped = html_escape.escape(raw)

    def color_repl(match):
        inner_text = match.group(1)
        color_spec = match.group(2)
        safe_color = _validate_color(color_spec)
        if safe_color is None:
            # Leave the original literal in place — safe failure.
            return match.group(0)
        # Allow bold/italic/underline inside the colored run.
        rendered_inner = (
            _UNDERLINE_RE.sub(r"<u>\1</u>",
                _ITALIC_RE.sub(r"<em>\1</em>",
                    _BOLD_RE.sub(r"<strong>\1</strong>", inner_text)))
        )
        return f'<span style="color:{safe_color}">{rendered_inner}</span>'

    # Color runs first (their inner text gets bold/italic/underline applied).
    escaped = _COLOR_RUN_RE.sub(color_repl, escaped)
    # Standalone bold/italic/underline (outside color runs).
    escaped = _BOLD_RE.sub(r"<strong>\1</strong>", escaped)
    escaped = _ITALIC_RE.sub(r"<em>\1</em>", escaped)
    escaped = _UNDERLINE_RE.sub(r"<u>\1</u>", escaped)
    return escaped


def load_template(theme_path):
    """Load HTML template file."""
    with open(theme_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_css(css_path):
    """Load CSS stylesheet."""
    with open(css_path, 'r', encoding='utf-8') as f:
        return f.read()


def theme_hides_photo(css_text):
    """Return True if the theme CSS effectively hides .resume-photo.

    Scans every `.resume-photo { ... }` block in source order and records the
    last `display:` value seen. If the final value is `none`, the photo is
    treated as hidden. This handles the common pattern (used by
    user-themes/zh-with-photo) where a base rule sets `display: none` and a
    later rule overrides it with `display: block`. It does not parse cascading
    specificity or media queries — by design, anyone writing a custom theme
    has already opted in and a heuristic is good enough for the warning.
    """
    last_display = None
    for block in re.finditer(r"\.resume-photo\s*\{([^}]*)\}", css_text, re.DOTALL):
        m = re.search(r"display\s*:\s*([a-zA-Z!-]+)", block.group(1), re.IGNORECASE)
        if m:
            last_display = m.group(1).lower()
    return last_display is not None and last_display.split("!")[0].strip() == "none"


def build_edit_script(resume_data, language, resume_json_path=None, sync_config=None):
    """Build inline JS/CSS for edit mode. Returns HTML string to inject before </body>.

    sync_config is None when sync is disabled; otherwise it is a dict with
    keys: path, port, token. The page reads this to know where to POST edits.
    """
    labels = get_localized_text(language)
    json_snapshot = json.dumps(resume_data, ensure_ascii=False, indent=2)
    # Escape for safe embedding in HTML
    json_snapshot_escaped = json_snapshot.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')

    if sync_config is None:
        sync_config_block = '<script type="application/json" id="resume-sync-config">null</script>'
    else:
        sync_config_payload = {
            "path": sync_config.get("path", ""),
            "port": sync_config.get("port", 0),
            "token": sync_config.get("token", ""),
        }
        sync_config_json = json.dumps(sync_config_payload, ensure_ascii=False)
        sync_config_escaped = sync_config_json.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
        sync_config_block = f'<script type="application/json" id="resume-sync-config">{sync_config_escaped}</script>'

    return f'''
<script type="application/json" id="resume-source-data">
{json_snapshot_escaped}
</script>
{sync_config_block}
<style>
/* Edit button */
#resume-edit-btn {{
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 99999;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    background: rgba(30, 41, 59, 0.85);
    color: #fff;
    font-size: 18px;
    cursor: pointer;
    opacity: 0.25;
    transition: opacity 0.2s, transform 0.15s;
    box-shadow: 0 2px 8px rgba(0,0,0,0.18);
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
}}
#resume-edit-btn:hover {{
    opacity: 1;
    transform: scale(1.08);
}}
/* Toolbar */
#resume-edit-toolbar {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100000;
    height: 48px;
    background: #1e293b;
    color: #f1f5f9;
    display: none;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.2);
}}
#resume-edit-toolbar.visible {{
    display: flex;
}}
#resume-edit-toolbar .toolbar-label {{
    font-weight: 600;
    letter-spacing: 0.02em;
}}
#resume-edit-toolbar .toolbar-actions {{
    display: flex;
    gap: 8px;
    align-items: center;
}}
#resume-edit-toolbar button {{
    padding: 6px 16px;
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.15s;
}}
.toolbar-btn-copy {{
    background: transparent;
    color: #f1f5f9;
    border: 1px solid rgba(255,255,255,0.32);
}}
.toolbar-btn-copy:hover {{
    background: rgba(255,255,255,0.08);
    border-color: rgba(255,255,255,0.5);
}}
.toolbar-btn-cancel {{
    background: #ef4444;
    color: #fff;
}}
.toolbar-btn-cancel:hover {{
    background: #dc2626;
}}
/* Icon-style close button (replaces the solid red Done button) */
.toolbar-btn-icon {{
    width: 32px;
    height: 32px;
    padding: 0;
    background: transparent;
    color: #cbd5e1;
    border: 1px solid rgba(255,255,255,0.18);
    font-size: 16px;
    line-height: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}}
.toolbar-btn-icon:hover {{
    color: #f8fafc;
    background: rgba(239, 68, 68, 0.18);
    border-color: rgba(239, 68, 68, 0.55);
}}
/* Rich text format buttons */
.toolbar-btn-format {{
    width: 32px;
    height: 32px;
    padding: 0;
    background: rgba(255,255,255,0.08);
    color: #f1f5f9;
    border: 1px solid rgba(255,255,255,0.12);
    font-weight: 700;
    font-size: 14px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}}
.toolbar-btn-format:hover {{
    background: rgba(255,255,255,0.18);
}}
.toolbar-btn-format[disabled] {{
    opacity: 0.4;
    cursor: not-allowed;
}}
.toolbar-btn-save {{
    background: #3b82f6;
    color: #fff;
}}
.toolbar-btn-save:hover {{
    background: #2563eb;
}}
.toolbar-btn-save[disabled] {{
    opacity: 0.4;
    cursor: not-allowed;
}}
.toolbar-divider {{
    width: 1px;
    height: 24px;
    background: rgba(255,255,255,0.15);
    margin: 0 4px;
}}
/* Color picker dropdown */
#resume-color-popover {{
    position: fixed;
    z-index: 100002;
    background: #fff;
    border-radius: 8px;
    padding: 10px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    display: none;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}}
#resume-color-popover.visible {{
    display: block;
}}
#resume-color-popover .swatch-section[hidden] {{
    display: none;
}}
#resume-color-popover .section-label {{
    margin: 0 0 6px;
    color: #64748b;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}}
#resume-color-popover .swatch-section + .swatch-section {{
    margin-top: 8px;
}}
#resume-color-popover .swatch-grid {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 6px;
    margin-bottom: 8px;
}}
#resume-color-popover .swatch-grid.recent-grid {{
    grid-template-columns: repeat(5, 1fr);
    margin-bottom: 0;
}}
#resume-color-popover .swatch {{
    width: 24px;
    height: 24px;
    border-radius: 4px;
    border: 1px solid rgba(0,0,0,0.1);
    cursor: pointer;
    padding: 0;
}}
#resume-color-popover .swatch:hover {{
    transform: scale(1.12);
}}
#resume-color-popover .swatch-none {{
    background: linear-gradient(135deg, #fff 45%, #ef4444 45%, #ef4444 55%, #fff 55%);
    border: 1px solid #cbd5e1;
}}
#resume-color-popover .hex-row {{
    display: flex;
    gap: 6px;
    align-items: center;
}}
#resume-color-popover input[type="color"] {{
    width: 32px;
    height: 28px;
    padding: 0;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    background: #fff;
    cursor: pointer;
}}
#resume-color-popover input[type="text"] {{
    flex: 1;
    padding: 4px 8px;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    font-size: 12px;
    font-family: monospace;
}}
/* Toast notification */
#resume-edit-toast {{
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100001;
    background: #1e293b;
    color: #f1f5f9;
    padding: 10px 24px;
    border-radius: 8px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 14px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    display: none;
    opacity: 0;
    transition: opacity 0.25s;
}}
#resume-edit-toast.show {{
    display: block;
    opacity: 1;
}}
/* Editable state visual cues */
body.resume-editing {{
    padding-top: 48px !important;
}}
body.resume-editing [contenteditable="true"] {{
    outline: 1px dashed rgba(100, 116, 200, 0.45);
    outline-offset: 3px;
    border-radius: 2px;
    transition: outline-color 0.15s, background 0.15s;
}}
body.resume-editing [contenteditable="true"]:focus {{
    outline: 1px solid rgba(100, 116, 200, 0.7);
    background: rgba(66, 133, 244, 0.05);
}}
/* Dark background override (sidebar / gradient header) */
body.resume-editing .sidebar [contenteditable="true"],
body.resume-editing .resume-header [contenteditable="true"] {{
    outline-color: rgba(200, 200, 255, 0.4);
}}
body.resume-editing .sidebar [contenteditable="true"]:focus,
body.resume-editing .resume-header [contenteditable="true"]:focus {{
    outline-color: rgba(200, 200, 255, 0.7);
    background: rgba(255, 255, 255, 0.08);
}}
/* List add/remove buttons */
.edit-add-btn, .edit-remove-btn {{
    display: none;
}}
/* Section-level "Add entry" buttons (hidden outside edit mode) */
.edit-add-entry-btn {{
    display: none;
}}
body.resume-editing .edit-add-entry-btn {{
    display: inline-block;
    margin-top: 12px;
    padding: 6px 14px;
    border: 1px dashed rgba(100, 116, 200, 0.6);
    border-radius: 6px;
    background: rgba(100, 116, 200, 0.08);
    color: rgba(100, 116, 200, 1);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.15s;
}}
body.resume-editing .edit-add-entry-btn:hover {{
    background: rgba(100, 116, 200, 0.18);
}}
body.resume-editing .edit-add-btn {{
    display: inline-block;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    border: 1px dashed rgba(100, 116, 200, 0.5);
    background: transparent;
    color: rgba(100, 116, 200, 0.7);
    font-size: 14px;
    line-height: 1;
    cursor: pointer;
    margin-left: 4px;
    vertical-align: middle;
    transition: background 0.15s;
}}
body.resume-editing .edit-add-btn:hover {{
    background: rgba(100, 116, 200, 0.12);
}}
body.resume-editing li,
body.resume-editing .skill-item {{
    position: relative;
}}
body.resume-editing li .edit-remove-btn,
body.resume-editing .skill-item .edit-remove-btn {{
    display: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    border: none;
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
    font-size: 12px;
    line-height: 1;
    cursor: pointer;
    transition: background 0.15s;
    vertical-align: middle;
    margin-left: 4px;
    padding: 0;
}}
/* li: overlay button absolutely positioned to the right */
body.resume-editing li .edit-remove-btn {{
    position: absolute;
    right: -4px;
    top: 50%;
    transform: translateY(-50%);
}}
body.resume-editing li:hover .edit-remove-btn,
body.resume-editing .skill-item:hover .edit-remove-btn,
body.resume-editing .skill-item:focus-within .edit-remove-btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
}}
body.resume-editing li .edit-remove-btn:hover,
body.resume-editing .skill-item .edit-remove-btn:hover {{
    background: rgba(239, 68, 68, 0.3);
}}
/* Print: hide all edit UI */
@media print {{
    #resume-edit-btn,
    #resume-edit-toolbar,
    #resume-edit-toast,
    #resume-color-popover,
    .edit-add-btn,
    .edit-remove-btn,
    .edit-add-entry-btn,
    .toolbar-btn-format,
    .toolbar-btn-save,
    .toolbar-btn-icon,
    .toolbar-divider {{
        display: none !important;
    }}
    body.resume-editing {{
        padding-top: 0 !important;
    }}
    body.resume-editing [contenteditable] {{
        outline: none !important;
        background: transparent !important;
    }}
}}
</style>
<button id="resume-edit-btn" title="{escape_text(labels["edit_resume"])}">&#9998;</button>
<div id="resume-edit-toolbar">
    <span class="toolbar-label">{escape_text(labels["editing_resume"])}</span>
    <div class="toolbar-actions">
        <button class="toolbar-btn-format" id="edit-bold-btn" title="{escape_text(labels["bold"])}" disabled><strong>B</strong></button>
        <button class="toolbar-btn-format" id="edit-italic-btn" title="{escape_text(labels["italic"])}" disabled><em>I</em></button>
        <button class="toolbar-btn-format" id="edit-underline-btn" title="{escape_text(labels["underline"])}" disabled style="text-decoration: underline;">U</button>
        <button class="toolbar-btn-format" id="edit-color-btn" title="{escape_text(labels["color"])}" disabled>&#9728;</button>
        <span class="toolbar-divider"></span>
        <button class="toolbar-btn-copy" id="edit-copy-btn">{escape_text(labels["copy_json"])}</button>
        <button class="toolbar-btn-save" id="edit-save-btn" disabled>{escape_text(labels["save"])}</button>
        <button class="toolbar-btn-icon" id="edit-cancel-btn" title="{escape_text(labels["done"])}" aria-label="{escape_text(labels["done"])}">&#10005;</button>
    </div>
</div>
<div id="resume-color-popover">
    <div class="swatch-section" id="resume-recent-colors-section" hidden>
        <div class="section-label">{escape_text(labels["recent_colors"])}</div>
        <div class="swatch-grid recent-grid" id="resume-recent-color-swatches"></div>
    </div>
    <div class="swatch-section">
        <div class="swatch-grid" id="resume-color-swatches"></div>
    </div>
    <div class="hex-row">
        <input type="color" id="resume-color-picker" value="#c0392b">
        <input type="text" id="resume-color-hex" placeholder="#rrggbb" maxlength="9">
    </div>
</div>
<div id="resume-edit-toast"></div>
<script>
(function() {{
    var btn = document.getElementById('resume-edit-btn');
    var toolbar = document.getElementById('resume-edit-toolbar');
    var copyBtn = document.getElementById('edit-copy-btn');
    var cancelBtn = document.getElementById('edit-cancel-btn');
    var toast = document.getElementById('resume-edit-toast');
    var boldBtn = document.getElementById('edit-bold-btn');
    var italicBtn = document.getElementById('edit-italic-btn');
    var underlineBtn = document.getElementById('edit-underline-btn');
    var colorBtn = document.getElementById('edit-color-btn');
    var saveBtn = document.getElementById('edit-save-btn');
    var colorPopover = document.getElementById('resume-color-popover');
    var recentColorSection = document.getElementById('resume-recent-colors-section');
    var recentColorSwatches = document.getElementById('resume-recent-color-swatches');
    var colorSwatches = document.getElementById('resume-color-swatches');
    var colorPicker = document.getElementById('resume-color-picker');
    var colorHex = document.getElementById('resume-color-hex');
    var isEditing = false;
    var originalHtml = null;
    var RECENT_COLOR_STORAGE_KEY = 'resume-edit-recent-colors-v1';
    var MAX_RECENT_COLORS = 5;
    var PRESET_COLORS = [
        '#c0392b', '#e67e22', '#f1c40f', '#27ae60', '#2980b9', '#8e44ad',
        '#000000', '#555555', '#999999', '#16a085', '#2c3e50', '#d35400'
    ];
    var recentColors = [];
    var lastAppliedPickerColor = null;

    // Fields that serialize rich text back to the Markdown subset.
    // Everything else uses plain textContent.
    var RICH_TEXT_SELECTORS = [
        '[data-section="summary"] p',
        '.experience-item .experience-description',
        '.experience-item .achievements li',
        '.experience-item .responsibilities li',
        '.education-item .honors',
        '.project-item .project-description',
        '.project-item .achievements li'
    ];

    function isRichTextField(el) {{
        if (!el) return false;
        return RICH_TEXT_SELECTORS.some(function(sel) {{
            try {{ return el.matches(sel); }} catch (e) {{ return false; }}
        }});
    }}

    function getSyncConfig() {{
        var el = document.getElementById('resume-sync-config');
        if (!el) return null;
        try {{
            var cfg = JSON.parse(el.textContent);
            if (cfg && cfg.port && cfg.token && cfg.path) return cfg;
        }} catch (e) {{}}
        return null;
    }}

    // --- Rich text: DOM -> Markdown subset string ---
    function serializeInlineMarkup(rootEl) {{
        var parts = [];
        function pushNode(node, tags) {{
            // tags: {{bold:bool, italic:bool, underline:bool, color:string|null}}
            if (node.nodeType === Node.TEXT_NODE) {{
                var txt = node.nodeValue || '';
                // Encode the markers themselves so they round-trip safely.
                // We escape `*`, `_`, `=`, `|`, `\` by prefixing with backslash.
                txt = txt.replace(/[\\*_=\|]/g, function(ch) {{
                    return '\\\\' + ch;
                }});
                parts.push({{text: txt, tags: tags}});
                return;
            }}
            if (node.nodeType !== Node.ELEMENT_NODE) return;
            // Skip edit control buttons (remove × buttons etc.)
            if (node.getAttribute && node.getAttribute('data-edit-control') !== null) return;
            var el = node;
            var tag = (el.tagName || '').toLowerCase();
            var style = el.getAttribute ? (el.getAttribute('style') || '') : '';
            var nextTags = Object.assign({{}}, tags);
            if (tag === 'strong' || tag === 'b') nextTags.bold = true;
            if (tag === 'em' || tag === 'i') nextTags.italic = true;
            if (tag === 'u') nextTags.underline = true;
            if (tag === 'span') {{
                var m = /color\s*:\s*([^;]+)/i.exec(style);
                if (m) {{
                    var c = m[1].trim();
                    if (/^#[0-9a-fA-F]{{3,8}}$/.test(c) || /^[a-z]+$/i.test(c)) {{
                        nextTags.color = c;
                    }} else {{
                        // Browsers often normalize hex to rgb()/rgba() — convert back.
                        var rgbMatch = /^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/i.exec(c);
                        if (rgbMatch) {{
                            var toHex = function(n) {{
                                var h = parseInt(n, 10).toString(16);
                                return h.length === 1 ? '0' + h : h;
                            }};
                            nextTags.color = '#' + toHex(rgbMatch[1]) + toHex(rgbMatch[2]) + toHex(rgbMatch[3]);
                        }}
                    }}
                }}
            }}
            for (var i = 0; i < el.childNodes.length; i++) {{
                pushNode(el.childNodes[i], nextTags);
            }}
        }}
        pushNode(rootEl, {{}});

        // Now join runs, wrapping each contiguous run with the appropriate markers.
        // Color is the outermost (because that's how the renderer nests them).
        var out = '';
        parts.forEach(function(p) {{
            var t = p.text;
            // Skip empty text nodes that aren't intentional whitespace — keep
            // single spaces/newlines since they carry meaning between runs.
            if (t === '') return;
            // Underline (innermost in our renderer's nesting).
            if (p.tags.underline) t = '_' + t + '_';
            if (p.tags.italic) t = '*' + t + '*';
            if (p.tags.bold) t = '**' + t + '**';
            if (p.tags.color) t = '==' + t + '|' + p.tags.color + '==';
            out += t;
        }});
        return out;
    }}

    function getFieldText(el) {{
        if (!el) return '';
        // Check rich-text classification against the live element (with its
        // ancestors) — cloneNode produces a detached subtree where descendant
        // CSS selectors in matches() no longer match.
        var isRich = isRichTextField(el);
        var clone = el.cloneNode(true);
        clone.querySelectorAll('[data-edit-control]').forEach(function(n) {{ n.remove(); }});
        if (isRich) {{
            return serializeInlineMarkup(clone).replace(/\s+$/, '').replace(/^\s+/, '');
        }}
        return clone.textContent.trim();
    }}

    // --- Rich text: selection -> wrap with markup ---
    function getSelectionHostEditable() {{
        var sel = window.getSelection();
        if (!sel || sel.rangeCount === 0) return null;
        var node = sel.anchorNode;
        if (!node) return null;
        var el = node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
        while (el) {{
            if (el.getAttribute && el.getAttribute('contenteditable') === 'true') return el;
            el = el.parentElement;
        }}
        return null;
    }}

    function selectionIsCollapsedOrMissing() {{
        var sel = window.getSelection();
        return !sel || sel.rangeCount === 0 || sel.isCollapsed;
    }}

    function normalizeColorValue(color) {{
        if (!color) return null;
        var normalized = String(color).trim().toLowerCase();
        if (/^#[0-9a-f]{{3,8}}$/.test(normalized)) return normalized;
        if (/^[a-z]+$/.test(normalized)) return normalized;
        return null;
    }}

    function colorPickerInputValue(color) {{
        var normalized = normalizeColorValue(color);
        if (!normalized || normalized.charAt(0) !== '#') return '#c0392b';
        if (/^#[0-9a-f]{{6}}$/.test(normalized)) return normalized;
        if (/^#[0-9a-f]{{3}}$/.test(normalized)) {{
            return '#' + normalized[1] + normalized[1] + normalized[2] + normalized[2] + normalized[3] + normalized[3];
        }}
        if (/^#[0-9a-f]{{4}}$/.test(normalized)) {{
            return '#' + normalized[1] + normalized[1] + normalized[2] + normalized[2] + normalized[3] + normalized[3];
        }}
        if (/^#[0-9a-f]{{8}}$/.test(normalized)) return '#' + normalized.slice(1, 7);
        return '#c0392b';
    }}

    function loadRecentColors() {{
        try {{
            var raw = window.localStorage.getItem(RECENT_COLOR_STORAGE_KEY);
            if (!raw) return [];
            var parsed = JSON.parse(raw);
            if (!Array.isArray(parsed)) return [];
            return parsed
                .map(normalizeColorValue)
                .filter(function(color, index, list) {{
                    return !!color && list.indexOf(color) === index;
                }})
                .slice(0, MAX_RECENT_COLORS);
        }} catch (e) {{
            return [];
        }}
    }}

    function persistRecentColors() {{
        try {{
            window.localStorage.setItem(
                RECENT_COLOR_STORAGE_KEY,
                JSON.stringify(recentColors.slice(0, MAX_RECENT_COLORS))
            );
        }} catch (e) {{}}
    }}

    function buildColorSwatch(color, onSelect) {{
        var swatch = document.createElement('button');
        swatch.type = 'button';
        swatch.className = 'swatch';
        swatch.style.background = color;
        swatch.title = color;
        swatch.setAttribute('aria-label', color);
        swatch.addEventListener('mousedown', function(e) {{
            e.preventDefault();
        }});
        swatch.addEventListener('click', function(e) {{
            e.preventDefault();
            onSelect(color);
        }});
        return swatch;
    }}

    function renderRecentColorSwatches() {{
        recentColorSwatches.innerHTML = '';
        if (!recentColors.length) {{
            recentColorSection.hidden = true;
            return;
        }}
        recentColorSection.hidden = false;
        recentColors.forEach(function(color) {{
            recentColorSwatches.appendChild(buildColorSwatch(color, function(selectedColor) {{
                applyColorSelection(selectedColor, {{ remember: true, closePopover: true }});
            }}));
        }});
    }}

    function rememberRecentColor(color) {{
        var normalized = normalizeColorValue(color);
        if (!normalized) return;
        recentColors = [normalized].concat(recentColors.filter(function(existingColor) {{
            return existingColor !== normalized;
        }})).slice(0, MAX_RECENT_COLORS);
        persistRecentColors();
        renderRecentColorSwatches();
    }}

    function wrapSelectionWithTag(tagName) {{
        if (selectionIsCollapsedOrMissing()) return false;
        var sel = window.getSelection();
        var range = sel.getRangeAt(0);
        // Reject selections that cross edit-control buttons.
        var host = getSelectionHostEditable();
        if (!host) return false;
        if (!host.contains(range.commonAncestorContainer) && host !== range.commonAncestorContainer) return false;

        var wrapper = document.createElement(tagName);
        try {{
            wrapper.appendChild(range.extractContents());
            range.insertNode(wrapper);
            // Reselect the wrapped content so the user sees what happened.
            var newRange = document.createRange();
            newRange.selectNodeContents(wrapper);
            sel.removeAllRanges();
            sel.addRange(newRange);
        }} catch (e) {{
            return false;
        }}
        return true;
    }}

    function wrapSelectionWithColor(color) {{
        if (selectionIsCollapsedOrMissing()) return false;
        var sel = window.getSelection();
        var range = sel.getRangeAt(0);
        var host = getSelectionHostEditable();
        if (!host) return false;
        if (!host.contains(range.commonAncestorContainer) && host !== range.commonAncestorContainer) return false;

        if (!color) {{
            // Remove color from selection: unwrap <span style=color> ancestors.
            var fragment = range.extractContents();
            var tmp = document.createElement('div');
            tmp.appendChild(fragment);
            tmp.querySelectorAll('span').forEach(function(span) {{
                if (/color\s*:/i.test(span.getAttribute('style') || '')) {{
                    var parent = span.parentNode;
    while (span.firstChild) parent.insertBefore(span.firstChild, span);
    parent.removeChild(span);
                }}
            }});
            while (tmp.firstChild) range.insertNode(tmp.firstChild);
            return true;
        }}

        var wrapper = document.createElement('span');
        wrapper.style.color = color;
        try {{
            wrapper.appendChild(range.extractContents());
            range.insertNode(wrapper);
            var newRange = document.createRange();
            newRange.selectNodeContents(wrapper);
            sel.removeAllRanges();
            sel.addRange(newRange);
        }} catch (e) {{
            return false;
        }}
        return true;
    }}

    function applyColorSelection(color, options) {{
        options = options || {{}};
        var normalizedColor = color == null ? null : normalizeColorValue(color);
        if (color != null && !normalizedColor) return false;
        var applied = wrapSelectionWithColor(normalizedColor);
        if (!applied) return false;
        if (normalizedColor && options.remember) {{
            rememberRecentColor(normalizedColor);
        }}
        if (options.closePopover) {{
            hideColorPopover();
        }}
        return true;
    }}

    function updateFormatButtonStates() {{
        var sel = window.getSelection();
        var hasSelection = sel && !sel.isCollapsed && sel.rangeCount > 0;
        var inEditable = hasSelection && !!getSelectionHostEditable();
        [boldBtn, italicBtn, underlineBtn, colorBtn].forEach(function(b) {{
            b.disabled = !inEditable;
        }});
        // Save button is enabled whenever there's a sync server.
        saveBtn.disabled = !getSyncConfig();
    }}

    function hideColorPopover() {{
        colorPopover.classList.remove('visible');
    }}

    function showColorPopover() {{
        recentColors = loadRecentColors();
        renderRecentColorSwatches();

        // Build preset swatches once.
        if (!colorSwatches.children.length) {{
            PRESET_COLORS.forEach(function(color) {{
                colorSwatches.appendChild(buildColorSwatch(color, function(selectedColor) {{
                    applyColorSelection(selectedColor, {{ remember: true, closePopover: true }});
                }}));
            }});
            var none = document.createElement('button');
            none.type = 'button';
            none.className = 'swatch swatch-none';
            none.title = {json.dumps(labels["color"], ensure_ascii=False)};
            none.addEventListener('mousedown', function(e) {{
                e.preventDefault();
            }});
            none.addEventListener('click', function(e) {{
                e.preventDefault();
                applyColorSelection(null, {{ closePopover: true }});
            }});
            colorSwatches.appendChild(none);
        }}

        // Position below the color button.
        var rect = colorBtn.getBoundingClientRect();
        colorPopover.style.top = (rect.bottom + 6) + 'px';
        colorPopover.style.left = rect.left + 'px';
        colorPopover.classList.add('visible');
        colorPicker.value = colorPickerInputValue(recentColors[0]);
        colorHex.value = '';
        lastAppliedPickerColor = null;
    }}

    // --- Save back to disk via sync server ---
    function saveJson() {{
        var cfg = getSyncConfig();
        if (!cfg) {{
            showToast({json.dumps(labels["sync_offline"], ensure_ascii=False)}, 3500);
            return;
        }}
        var data = extractToJson();
        saveBtn.disabled = true;
        var originalLabel = saveBtn.textContent;
        saveBtn.textContent = {json.dumps(labels["saving"], ensure_ascii=False)};

        fetch('http://127.0.0.1:' + cfg.port + '/sync', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + cfg.token
            }},
            body: JSON.stringify({{ path: cfg.path, data: data }})
        }}).then(function(resp) {{
            return resp.json().then(function(body) {{
                if (resp.ok && body && body.ok) {{
                    showToast({json.dumps(labels["saved"], ensure_ascii=False)}, 2500);
                }} else {{
                    showToast({json.dumps(labels["save_failed"], ensure_ascii=False)}, 3500);
                }}
            }});
        }}).catch(function() {{
            showToast({json.dumps(labels["sync_offline"], ensure_ascii=False)}, 3500);
        }}).finally(function() {{
            saveBtn.disabled = false;
            saveBtn.textContent = originalLabel;
        }});
    }}

    var EDITABLE_SELECTORS = [
        '.resume-header .name',
        '.contact-email a',
        '.contact-phone',
        '.contact-location',
        '.contact-linkedin a',
        '.contact-github a',
        '[data-section="summary"] p',
        '.experience-item .company-name',
        '.experience-item .position',
        '.experience-item .period',
        '.experience-item .location',
        '.experience-item .experience-description',
        '.experience-item .achievements li',
        '.experience-item .responsibilities li',
        '.education-item .institution',
        '.education-item .degree',
        '.education-item .period',
        '.education-item .location',
        '.education-item .gpa',
        '.education-item .honors',
        '.project-item .project-name',
        '.project-item .role',
        '.project-item .period',
        '.project-item .technologies',
        '.project-item .project-description',
        '.project-item .achievements li',
        '.skill-category .category-title',
        '.skill-category .skill-item'
    ];

    var LIST_CONTAINERS = '.achievements, .responsibilities, .skill-list';

    function getOriginalData() {{
        var el = document.getElementById('resume-source-data');
        if (!el) return {{}};
        return JSON.parse(el.textContent);
    }}

    function showToast(msg, duration) {{
        toast.textContent = msg;
        toast.classList.add('show');
        toast.style.display = 'block';
        setTimeout(function() {{
            toast.classList.remove('show');
            setTimeout(function() {{ toast.style.display = 'none'; }}, 300);
        }}, duration || 2000);
    }}

    function toggleEditMode() {{
        if (!isEditing) {{
            enterEditMode();
        }} else {{
            exitEditMode(true);
        }}
    }}

    function enterEditMode() {{
        isEditing = true;
        document.body.classList.add('resume-editing');
        toolbar.classList.add('visible');
        btn.innerHTML = '&#10005;';
        btn.title = {json.dumps(labels["exit_edit_mode"], ensure_ascii=False)};

        EDITABLE_SELECTORS.forEach(function(sel) {{
            var els = document.querySelectorAll(sel);
            els.forEach(function(el) {{
                el.setAttribute('contenteditable', 'true');
            }});
        }});

        // Suppress link navigation during editing
        document.querySelectorAll('.contact-info a').forEach(function(a) {{
            a.addEventListener('click', preventNav);
        }});

        // Add list item management buttons
        addListButtons();
        addEntryButtons();
    }}

    function preventNav(e) {{
        if (isEditing) {{
            e.preventDefault();
            e.stopPropagation();
        }}
    }}

    function exitEditMode(save) {{
        if (!isEditing) return;
        isEditing = false;
        document.body.classList.remove('resume-editing');
        toolbar.classList.remove('visible');
        btn.innerHTML = '&#9998;';
        btn.title = {json.dumps(labels["edit_resume"], ensure_ascii=False)};

        EDITABLE_SELECTORS.forEach(function(sel) {{
            var els = document.querySelectorAll(sel);
            els.forEach(function(el) {{
                el.removeAttribute('contenteditable');
            }});
        }});

        // Restore link navigation
        document.querySelectorAll('.contact-info a').forEach(function(a) {{
            a.removeEventListener('click', preventNav);
        }});

        removeListButtons();
        removeEntryButtons();
    }}

    function makeEntryButton(label, sectionType) {{
        var btn = document.createElement('button');
        btn.className = 'edit-add-entry-btn';
        btn.setAttribute('data-edit-control', '');
        btn.setAttribute('data-section-type', sectionType);
        btn.textContent = '+ ' + label;
        btn.addEventListener('click', function() {{ appendBlankEntry(sectionType); }});
        return btn;
    }}

    function addEntryButtons() {{
        var sectionMap = [
            ['experience', {json.dumps(labels["add_experience"], ensure_ascii=False)}],
            ['education', {json.dumps(labels["add_education"], ensure_ascii=False)}],
            ['projects', {json.dumps(labels["add_project"], ensure_ascii=False)}],
        ];
        sectionMap.forEach(function(pair) {{
            var sectionEl = document.querySelector('[data-section="' + pair[0] + '"]');
            if (sectionEl) sectionEl.appendChild(makeEntryButton(pair[1], pair[0]));
        }});
    }}

    function removeEntryButtons() {{
        document.querySelectorAll('.edit-add-entry-btn').forEach(function(b) {{ b.remove(); }});
    }}

    function applyEditableToEntry(root) {{
        // Mark text fields editable and attach list buttons within a newly added entry
        var selectorsByType = {{
            experience: ['.company-name', '.position', '.period', '.location',
                         '.experience-description', '.achievements li', '.responsibilities li'],
            education: ['.institution', '.degree', '.period', '.location', '.gpa', '.honors'],
            projects: ['.project-name', '.role', '.period', '.technologies',
                       '.project-description', '.achievements li'],
        }};
        var selectors = selectorsByType[root.getAttribute('data-entry-type')] || [];
        selectors.forEach(function(sel) {{
            root.querySelectorAll(sel).forEach(function(el) {{
                el.setAttribute('contenteditable', 'true');
            }});
        }});
        root.querySelectorAll(LIST_CONTAINERS).forEach(function(container) {{
            var isSkillList = container.classList.contains('skill-list');
            var addBtn = document.createElement('button');
            addBtn.className = 'edit-add-btn';
            addBtn.setAttribute('data-edit-control', '');
            addBtn.textContent = '+';
            addBtn.title = {json.dumps(labels["add_item"], ensure_ascii=False)};
            addBtn.addEventListener('click', function() {{
                var item = document.createElement(isSkillList ? 'span' : 'li');
                if (isSkillList) item.className = 'skill-item';
                item.setAttribute('contenteditable', 'true');
                item.textContent = {json.dumps(labels["new_item"], ensure_ascii=False)};
                attachRemoveBtn(item);
                container.appendChild(item);
                item.focus();
            }});
            container.parentNode.insertBefore(addBtn, container.nextSibling);
            var itemSelector = isSkillList ? '.skill-item' : 'li';
            container.querySelectorAll(itemSelector).forEach(attachRemoveBtn);
        }});
    }}

    function appendBlankEntry(sectionType) {{
        var sectionEl = document.querySelector('[data-section="' + sectionType + '"]');
        if (!sectionEl) return;
        var node = document.createElement('div');
        // Template mirrors generate_html.py output structure
        if (sectionType === 'experience') {{
            node.innerHTML =
                '<div class="experience-item" data-entry-type="experience">' +
                '<div class="experience-header"><h3 class="company-name">Company</h3>' +
                '<div class="position-period"><span class="position">Position</span>' +
                '<span class="period"></span></div></div>' +
                '<p class="experience-description"></p>' +
                '<ul class="responsibilities"></ul><ul class="achievements"></ul></div>';
        }} else if (sectionType === 'education') {{
            node.innerHTML =
                '<div class="education-item" data-entry-type="education">' +
                '<div class="education-header"><h3 class="institution">Institution</h3>' +
                '<div class="degree-period"><span class="degree">Degree</span>' +
                '<span class="period"></span></div></div></div>';
        }} else if (sectionType === 'projects') {{
            node.innerHTML =
                '<div class="project-item" data-entry-type="projects">' +
                '<div class="project-header"><h3 class="project-name">Project</h3>' +
                '<span class="role"></span><span class="period"></span></div>' +
                '<p class="project-description"></p><ul class="achievements"></ul></div>';
        }}
        var entry = node.firstElementChild;
        // Insert before the "+ Add" button
        sectionEl.insertBefore(entry, sectionEl.querySelector('.edit-add-entry-btn'));
        applyEditableToEntry(entry);
        entry.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        var firstField = entry.querySelector('.company-name, .institution, .project-name');
        if (firstField) {{
            firstField.focus();
            var range = document.createRange();
            range.selectNodeContents(firstField);
            var sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
        }}
    }}

    function addListButtons() {{
        document.querySelectorAll(LIST_CONTAINERS).forEach(function(container) {{
            container.style.position = 'relative';
            var isSkillList = container.classList.contains('skill-list');
            var addBtn = document.createElement('button');
            addBtn.className = 'edit-add-btn';
            addBtn.textContent = '+';
            addBtn.title = {json.dumps(labels["add_item"], ensure_ascii=False)};
            addBtn.addEventListener('click', function() {{
                var item = document.createElement(isSkillList ? 'span' : 'li');
                if (isSkillList) item.className = 'skill-item';
                item.setAttribute('contenteditable', 'true');
                item.textContent = {json.dumps(labels["new_item"], ensure_ascii=False)};
                attachRemoveBtn(item);
                container.appendChild(item);
                item.focus();
                var range = document.createRange();
                range.selectNodeContents(item);
                var sel = window.getSelection();
                sel.removeAllRanges();
                sel.addRange(range);
            }});
            container.parentNode.insertBefore(addBtn, container.nextSibling);

            var itemSelector = isSkillList ? '.skill-item' : 'li';
            container.querySelectorAll(itemSelector).forEach(attachRemoveBtn);
        }});
    }}

    function attachRemoveBtn(item) {{
        var rmBtn = document.createElement('button');
        rmBtn.className = 'edit-remove-btn';
        rmBtn.setAttribute('aria-hidden', 'true');
        rmBtn.setAttribute('data-edit-control', '');
        rmBtn.textContent = '\\u00d7';
        rmBtn.title = {json.dumps(labels["remove_item"], ensure_ascii=False)};
        rmBtn.addEventListener('click', function(e) {{
            e.stopPropagation();
            item.remove();
        }});
        item.appendChild(rmBtn);
    }}

    function textWithoutControls(el) {{
        var clone = el.cloneNode(true);
        clone.querySelectorAll('[data-edit-control]').forEach(function(n) {{ n.remove(); }});
        return clone.textContent.trim();
    }}

    function removeListButtons() {{
        document.querySelectorAll('.edit-add-btn').forEach(function(b) {{ b.remove(); }});
        document.querySelectorAll('.edit-remove-btn').forEach(function(b) {{ b.remove(); }});
    }}

    function extractToJson() {{
        var src = getOriginalData();
        var result = JSON.parse(JSON.stringify(src)); // deep clone

        // Personal
        var name = document.querySelector('.resume-header .name');
        if (name && result.personal) result.personal.name = name.textContent.trim();

        var emailLink = document.querySelector('.contact-email a');
        if (emailLink && result.personal) {{
            result.personal.email = emailLink.textContent.trim();
        }}

        var phone = document.querySelector('.contact-phone');
        if (phone && result.personal) result.personal.phone = phone.textContent.trim();

        var location = document.querySelector('.contact-location');
        if (location && result.personal) result.personal.location = location.textContent.trim();

        var linkedin = document.querySelector('.contact-linkedin a');
        if (linkedin && result.personal) result.personal.linkedin = linkedin.textContent.trim();

        var github = document.querySelector('.contact-github a');
        if (github && result.personal) result.personal.github = github.textContent.trim();

        // Summary
        var summaryP = document.querySelector('[data-section="summary"] p');
        if (summaryP) result.summary = getFieldText(summaryP);

        // Experience
        if (result.experience) {{
            var expItems = document.querySelectorAll('.experience-item');
            for (var i = 0; i < expItems.length; i++) {{
                if (!result.experience[i]) result.experience[i] = {{}};
                var item = expItems[i];
                var el;

                el = item.querySelector('.company-name');
                if (el) result.experience[i].company = el.textContent.trim();

                el = item.querySelector('.position');
                if (el) result.experience[i].position = el.textContent.trim();

                el = item.querySelector('.period');
                if (el) result.experience[i].period = el.textContent.trim();

                el = item.querySelector('.location');
                if (el) result.experience[i].location = el.textContent.trim();

                el = item.querySelector('.experience-description');
                if (el) result.experience[i].description = getFieldText(el);

                el = item.querySelector('.responsibilities');
                if (el) {{
                    result.experience[i].responsibilities = [];
                    el.querySelectorAll('li').forEach(function(li) {{
                        var t = getFieldText(li);
                        if (t) result.experience[i].responsibilities.push(t);
                    }});
                }}

                el = item.querySelector('.achievements');
                if (el) {{
                    result.experience[i].achievements = [];
                    el.querySelectorAll('li').forEach(function(li) {{
                        var t = getFieldText(li);
                        if (t) result.experience[i].achievements.push(t);
                    }});
                }}
            }}
        }}

        // Education
        if (result.education) {{
            var eduItems = document.querySelectorAll('.education-item');
            for (var i = 0; i < eduItems.length; i++) {{
                if (!result.education[i]) result.education[i] = {{}};
                var item = eduItems[i];
                var el;

                el = item.querySelector('.institution');
                if (el) result.education[i].institution = el.textContent.trim();

                el = item.querySelector('.degree');
                if (el) result.education[i].degree = el.textContent.trim();

                el = item.querySelector('.period');
                if (el) result.education[i].period = el.textContent.trim();

                el = item.querySelector('.location');
                if (el) result.education[i].location = el.textContent.trim();

                el = item.querySelector('.gpa');
                if (el) {{
                    var gpaText = el.textContent.trim();
                    result.education[i].gpa = gpaText.replace(/^GPA:\\s*/, '');
                }}

                el = item.querySelector('.honors');
                if (el) {{
                    var honorsText = getFieldText(el);
                    var cleaned = honorsText.replace(/^[^:]+:\\s*/, '');
                    result.education[i].honors = cleaned.split(',').map(function(s) {{ return s.trim(); }}).filter(Boolean);
                }}
            }}
        }}

        // Projects
        if (result.projects) {{
            var projItems = document.querySelectorAll('.project-item');
            for (var i = 0; i < projItems.length; i++) {{
                if (!result.projects[i]) result.projects[i] = {{}};
                var item = projItems[i];
                var el;

                el = item.querySelector('.project-name');
                if (el) result.projects[i].name = el.textContent.trim();

                el = item.querySelector('.role');
                if (el) result.projects[i].role = el.textContent.trim();

                el = item.querySelector('.period');
                if (el) result.projects[i].period = el.textContent.trim();

                el = item.querySelector('.technologies');
                if (el) {{
                    var techText = el.textContent.trim();
                    var cleaned = techText.replace(/^[^:]+:\\s*/, '');
                    result.projects[i].technologies = cleaned.split(',').map(function(s) {{ return s.trim(); }}).filter(Boolean);
                }}

                el = item.querySelector('.project-description');
                if (el) result.projects[i].description = getFieldText(el);

                el = item.querySelector('.achievements');
                if (el) {{
                    result.projects[i].achievements = [];
                    el.querySelectorAll('li').forEach(function(li) {{
                        var t = getFieldText(li);
                        if (t) result.projects[i].achievements.push(t);
                    }});
                }}
            }}
        }}

        // Skills — clear existing then rebuild from DOM to avoid stale keys
        if (result.skills) {{
            Object.keys(result.skills).forEach(function(k) {{ delete result.skills[k]; }});
            var newSkills = {{}};

            document.querySelectorAll('.skill-category').forEach(function(cat) {{
                var titleEl = cat.querySelector('.category-title');
                var listEl = cat.querySelector('.skill-list');
                if (!titleEl || !listEl) return;

                var title = titleEl.textContent.trim();
                // Decide the JSON key for this category:
                //  - If the user renamed the category in the editor (title no
                //    longer matches the last-rendered display), use the new
                //    title verbatim as the key.
                //  - Otherwise reuse the stable data-key so a round-trip
                //    (render -> edit -> save) does not mutate the key.
                //  - For brand-new categories added in the editor, also use
                //    the title verbatim — slugifying would destroy casing
                //    ("AI / LLM" -> "ai_/_llm") and break CJK names.
                var dataKey = cat.getAttribute('data-key');
                var lastDisplay = cat.getAttribute('data-display');
                var jsonKey;
                if (!dataKey) {{
                    jsonKey = title;
                }} else if (lastDisplay && title !== lastDisplay) {{
                    jsonKey = title;
                }} else {{
                    jsonKey = dataKey;
                }}

                var skillEls = listEl.querySelectorAll('.skill-item');
                var skillsArr = [];
                skillEls.forEach(function(el) {{
                    var t = textWithoutControls(el);
                    if (t) skillsArr.push(t);
                }});
                if (skillsArr.length > 0) {{
                    newSkills[jsonKey] = skillsArr;
                }} else if (title) {{
                    // Preserve the (now empty) category so the user's edit isn't lost
                    newSkills[jsonKey] = [];
                }}
            }});
            result.skills = newSkills;
        }}

        return result;
    }}

    function copyJson() {{
        var data = extractToJson();
        var jsonStr = JSON.stringify(data, null, 2);

        if (navigator.clipboard && navigator.clipboard.writeText) {{
            navigator.clipboard.writeText(jsonStr).then(function() {{
                showToast({json.dumps(labels["json_copied"], ensure_ascii=False)}, 2500);
            }}).catch(function() {{
                fallbackCopy(jsonStr);
            }});
        }} else {{
            fallbackCopy(jsonStr);
        }}
    }}

    function fallbackCopy(jsonStr) {{
        console.log('=== RESUME JSON ===');
        console.log(jsonStr);
        console.log('=== END RESUME JSON ===');
        showToast({json.dumps(labels["json_console"], ensure_ascii=False)}, 3500);
    }}

    btn.addEventListener('click', toggleEditMode);
    copyBtn.addEventListener('click', copyJson);
    cancelBtn.addEventListener('click', function() {{ exitEditMode(true); }});

    boldBtn.addEventListener('mousedown', function(e) {{
        // Prevent stealing focus/selection from the editable region.
        e.preventDefault();
        wrapSelectionWithTag('strong');
        updateFormatButtonStates();
    }});
    italicBtn.addEventListener('mousedown', function(e) {{
        e.preventDefault();
        wrapSelectionWithTag('em');
        updateFormatButtonStates();
    }});
    underlineBtn.addEventListener('mousedown', function(e) {{
        e.preventDefault();
        wrapSelectionWithTag('u');
        updateFormatButtonStates();
    }});
    colorBtn.addEventListener('click', function(e) {{
        e.preventDefault();
        if (colorPopover.classList.contains('visible')) {{
            hideColorPopover();
        }} else {{
            showColorPopover();
        }}
    }});
    colorPicker.addEventListener('input', function(e) {{
        if (applyColorSelection(e.target.value, {{ remember: false }})) {{
            lastAppliedPickerColor = normalizeColorValue(e.target.value);
        }}
    }});
    colorPicker.addEventListener('change', function(e) {{
        var selectedColor = lastAppliedPickerColor;
        if (!selectedColor && applyColorSelection(e.target.value, {{ remember: false }})) {{
            selectedColor = normalizeColorValue(e.target.value);
        }}
        if (selectedColor) {{
            rememberRecentColor(selectedColor);
            hideColorPopover();
        }}
        lastAppliedPickerColor = null;
    }});
    colorHex.addEventListener('keydown', function(e) {{
        if (e.key === 'Enter') {{
            e.preventDefault();
            var v = colorHex.value.trim();
            if (/^#[0-9a-fA-F]{{3,8}}$/.test(v)) {{
                applyColorSelection(v, {{ remember: true, closePopover: true }});
            }}
        }}
    }});
    // Hide color popover on outside click.
    document.addEventListener('mousedown', function(e) {{
        if (!colorPopover.classList.contains('visible')) return;
        if (colorPopover.contains(e.target) || colorBtn.contains(e.target)) return;
        hideColorPopover();
    }});
    // Update format button states on selection changes inside editables.
    document.addEventListener('selectionchange', updateFormatButtonStates);
    document.addEventListener('mouseup', updateFormatButtonStates);
    document.addEventListener('keyup', updateFormatButtonStates);

    saveBtn.addEventListener('click', function(e) {{
        e.preventDefault();
        saveJson();
    }});

    // Keyboard shortcuts inside editables: Ctrl/Cmd+B/I/U.
    document.addEventListener('keydown', function(e) {{
        if (!isEditing) return;
        if (!(e.ctrlKey || e.metaKey)) return;
        var key = e.key.toLowerCase();
        if (key === 'b' || key === 'i' || key === 'u') {{
            // Allow the browser's default execCommand to run, which produces
            // <b>/<i>/<u> (or <strong>/<em> in some browsers) — both are
            // handled by serializeInlineMarkup.
            // We just don't preventDefault.
            setTimeout(updateFormatButtonStates, 0);
        }}
    }});

    // Expose for programmatic extraction (e.g. Playwright) per SKILL.md
    window.extractToJson = extractToJson;
}})();
</script>
'''


def generate_resume_html(resume_data, theme="modern", language="en", editable=False,
                         resume_json_path=None, sync_config=None):
    """
    Generate HTML resume from JSON data with specified theme and language.

    sync_config (optional): dict with path/port/token. When provided, the
    editable toolbar includes a Save button that POSTs edits to a local sync
    server (scripts/_edit_sync_server.py) which writes them to resume.json.
    """
    theme = theme or DEFAULT_THEME
    language = language if language in SUPPORTED_LANGUAGES else "en"

    theme_assets = resolve_theme_assets(theme, Path(__file__).parent.parent)
    template_path = theme_assets["template_path"]
    css_path = theme_assets["css_path"]

    template = load_template(template_path)
    css = load_css(css_path)

    # Warn the user when their resume declares a photo but the active theme
    # hides it. The built-in themes all hide .resume-photo by design; a custom
    # theme is required to actually display the photo. Surfacing this here
    # saves the user from re-exporting and wondering why the photo is missing.
    personal = resume_data.get("personal", {}) if isinstance(resume_data, dict) else {}
    if personal.get("photo") and theme_hides_photo(css):
        print(
            "Note: resume has a `personal.photo` set, but theme "
            f"'{theme}' hides it. Use a custom theme that enables "
            "`.resume-photo { display: block }` (see user-themes/zh-with-photo "
            "for an example) to show the photo.",
            file=sys.stderr,
        )

    # Build HTML content
    html_content = build_sections(resume_data, language, resume_json_path)

    # Build edit script payload if editable mode is enabled
    if editable:
        edit_payload = build_edit_script(
            resume_data, language,
            resume_json_path=resume_json_path,
            sync_config=sync_config,
        )
    else:
        edit_payload = ""

    # Insert CSS, content, language, and edit script into template
    full_html = template.replace("{{CSS}}", css)
    full_html = full_html.replace("{{CONTENT}}", html_content)
    full_html = full_html.replace("{{LANG}}", language)
    full_html = full_html.replace("{{EDIT_SCRIPT}}", edit_payload)

    return full_html


def build_sections(resume_data, language, resume_json_path=None):
    """Build HTML sections from resume data."""
    sidebar_sections = []
    main_sections = []

    # Header (Personal Info) — always in sidebar
    sidebar_sections.append(build_header(resume_data.get("personal", {}), language, resume_json_path))

    # Summary
    if resume_data.get("summary"):
        main_sections.append(build_summary(resume_data["summary"], language))

    # Experience
    if resume_data.get("experience"):
        main_sections.append(build_experience(resume_data["experience"], language))

    # Education
    if resume_data.get("education"):
        main_sections.append(build_education(resume_data["education"], language))

    # Projects
    if resume_data.get("projects"):
        main_sections.append(build_projects(resume_data["projects"], language))

    # Skills — always in sidebar
    if resume_data.get("skills"):
        sidebar_sections.append(build_skills(resume_data["skills"], language))

    sidebar_html = '<aside class="sidebar">' + "\n".join(sidebar_sections) + '</aside>'
    main_html = '<main class="main-content">' + "\n".join(main_sections) + '</main>'

    return sidebar_html + "\n" + main_html


def build_header(personal, language, resume_json_path=None):
    """Build header section with personal info."""
    name = escape_text(personal.get("name", "Your Name"))
    email = escape_text(personal.get("email", ""))
    phone = escape_text(personal.get("phone", ""))
    location = escape_text(personal.get("location", ""))
    linkedin = escape_text(personal.get("linkedin", ""))
    github = escape_text(personal.get("github", ""))
    photo_src = resolve_photo_src(personal.get("photo", ""), resume_json_path)

    contact_items = []
    if email:
        contact_items.append(f'<span class="contact-item contact-email"><a href="mailto:{email}">{email}</a></span>')
    if phone:
        contact_items.append(f'<span class="contact-item contact-phone">{phone}</span>')
    if location:
        contact_items.append(f'<span class="contact-item contact-location">{location}</span>')
    if linkedin:
        contact_items.append(f'<span class="contact-item contact-linkedin"><a href="{linkedin}" target="_blank">LinkedIn</a></span>')
    if github:
        contact_items.append(f'<span class="contact-item contact-github"><a href="{github}" target="_blank">GitHub</a></span>')

    contact_html = "\n".join(contact_items) if contact_items else ""
    # Photo is opt-in per theme. Built-in themes hide .resume-photo via CSS;
    # a custom theme enables it by setting display: block (or similar).
    photo_html = f'<img class="resume-photo" src="{photo_src}" alt="">\n' if photo_src else ""

    return f"""
<header class="resume-header">
    {photo_html}<h1 class="name">{name}</h1>
    <div class="contact-info">{contact_html}</div>
</header>
"""


def build_summary(summary, language):
    """Build summary section."""
    labels = get_localized_text(language)
    title = labels["summary"]
    return f"""
<section class="resume-section" data-section="summary">
    <h2 class="section-title">{title}</h2>
    <p>{render_rich_text(summary)}</p>
</section>
"""


def build_experience(experience, language):
    """Build experience section."""
    labels = get_localized_text(language)
    title = labels["experience"]
    html = f'<section class="resume-section" data-section="experience"><h2 class="section-title">{title}</h2>'

    for exp in experience:
        company = escape_text(exp.get("company", "Company Name"))
        position = escape_text(exp.get("position", "Position"))
        period = escape_text(exp.get("period", ""))
        location = escape_text(exp.get("location", ""))
        description = render_rich_text(exp.get("description", ""))
        responsibilities = exp.get("responsibilities", [])
        achievements = exp.get("achievements", [])

        html += f"""
<div class="experience-item">
    <div class="experience-header">
        <h3 class="company-name">{company}</h3>
        <div class="position-period">
            <span class="position">{position}</span>
            <span class="period">{period}</span>
        </div>
    </div>
    {f'<div class="location">{location}</div>' if location else ''}
"""

        if description:
            html += f"<p class='experience-description'>{description}</p>"

        if responsibilities:
            html += "<ul class='responsibilities'>"
            for resp in responsibilities:
                html += f"<li>{render_rich_text(resp)}</li>"
            html += "</ul>"

        if achievements:
            html += "<ul class='achievements'>"
            for ach in achievements:
                html += f"<li>{render_rich_text(ach)}</li>"
            html += "</ul>"

        html += "</div>"

    html += "</section>"
    return html


def build_education(education, language):
    """Build education section."""
    labels = get_localized_text(language)
    title = labels["education"]
    html = f'<section class="resume-section" data-section="education"><h2 class="section-title">{title}</h2>'

    for edu in education:
        institution = escape_text(edu.get("institution", "Institution Name"))
        degree = escape_text(edu.get("degree", "Degree"))
        period = escape_text(edu.get("period", ""))
        location = escape_text(edu.get("location", ""))
        gpa = escape_text(edu.get("gpa", ""))
        honors = edu.get("honors", [])

        html += f"""
<div class="education-item">
    <div class="education-header">
        <h3 class="institution">{institution}</h3>
        <div class="degree-period">
            <span class="degree">{degree}</span>
            <span class="period">{period}</span>
        </div>
    </div>
    {f'<div class="location">{location}</div>' if location else ''}
    {f'<div class="gpa">{escape_text(labels["gpa"])}: {gpa}</div>' if gpa else ''}
"""

        if honors:
            html += f"<div class='honors'><strong>{escape_text(labels['honors'])}:</strong> " + ", ".join([render_rich_text(h) for h in honors]) + "</div>"

        html += "</div>"

    html += "</section>"
    return html


def build_projects(projects, language):
    """Build projects section."""
    labels = get_localized_text(language)
    title = labels["projects"]
    html = f'<section class="resume-section" data-section="projects"><h2 class="section-title">{title}</h2>'

    for proj in projects:
        name = escape_text(proj.get("name", "Project Name"))
        role = escape_text(proj.get("role", ""))
        period = escape_text(proj.get("period", ""))
        technologies = proj.get("technologies", [])
        description = render_rich_text(proj.get("description", ""))
        achievements = proj.get("achievements", [])

        html += f"""
<div class="project-item">
    <div class="project-header">
        <h3 class="project-name">{name}</h3>
        {f'<span class="role">{role}</span>' if role else ''}
        {f'<span class="period">{period}</span>' if period else ''}
    </div>
"""

        if technologies:
            escaped_techs = [escape_text(t) for t in technologies]
            html += f"<div class='technologies'><strong>{escape_text(labels['technologies'])}:</strong> {', '.join(escaped_techs)}</div>"

        if description:
            html += f"<p class='project-description'>{description}</p>"

        if achievements:
            html += "<ul class='achievements'>"
            for ach in achievements:
                html += f"<li>{render_rich_text(ach)}</li>"
            html += "</ul>"

        html += "</div>"

    html += "</section>"
    return html


def build_skills(skills, language):
    """Build skills section."""
    labels = get_localized_text(language)
    title = labels["skills"]
    html = f'<section class="resume-section" data-section="skills"><h2 class="section-title">{title}</h2>'

    for category, skill_list in skills.items():
        category_escaped = escape_text(category)
        category_key = escape_text(category)
        display_title = category_escaped.replace('_', ' ').title()
        items = ensure_string_list(skill_list)
        item_spans = "".join(
            f'<span class="skill-item">{escape_text(s)}</span>' for s in items
        )
        # data-key: stable JSON key (preserved on save unless the user renames
        # the category). data-display: the title as last rendered, so the save
        # path can detect a user rename and update the key accordingly.
        html += f"""
<div class="skill-category" data-key="{category_key}" data-display="{display_title}">
    <h3 class="category-title">{display_title}</h3>
    <div class="skill-list">{item_spans}</div>
</div>
"""

    html += "</section>"
    return html


def start_sync_server(resume_json_path, sidecar_path=None):
    """Start the local edit-sync server in the background.

    Returns a dict {path, port, token, process, reused} on success, or None
    on failure. The server writes browser edits back to resume_json_path.

    If a sidecar_path is given and points at an existing server that responds
    on its recorded port, that server is reused (we don't know its token, so
    in that case we still spin up a fresh one — see note below). To avoid
    orphan accumulation, we look for an existing sidecar for this same target
    path and reuse it when possible; if its pid is dead, we ignore it.
    """
    if not resume_json_path:
        return None
    try:
        target_path = str(Path(resume_json_path).expanduser().resolve())
    except Exception:
        return None

    server_script = Path(__file__).resolve().parent / "_edit_sync_server.py"
    if not server_script.exists():
        return None

    try:
        # Suppress SIGINT inheritance so Ctrl-C on the parent doesn't kill
        # the server mid-write. We rely on the sidecar file for cleanup.
        proc = subprocess.Popen(
            [sys.executable, str(server_script), "--target", target_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            # Keep the server alive after this process exits so the user
            # can keep editing in the browser even after the agent moves on.
            # The sidecar file records the pid for explicit cleanup.
        )
    except Exception as e:
        print(f"Warning: failed to start edit-sync server: {e}", file=sys.stderr)
        return None

    # Read startup banner (3 lines). Block briefly — server is fast.
    port = None
    token = None
    try:
        for _ in range(3):
            line = proc.stdout.readline()
            if not line:
                break
            line = line.strip()
            if line.startswith("RESUME_SYNC_PORT="):
                port = int(line.split("=", 1)[1])
            elif line.startswith("RESUME_SYNC_TOKEN="):
                token = line.split("=", 1)[1].strip()
    except Exception as e:
        print(f"Warning: edit-sync server did not report a port: {e}", file=sys.stderr)
        return None

    if not port or not token:
        return None

    return {
        "path": target_path,
        "port": port,
        "token": token,
        "process": proc,
    }


def reap_dead_sync_servers(target_path):
    """Kill any sync servers in sidecar files pointing at target_path whose
    pid is alive. Prevents orphan accumulation across re-exports.

    Looks at sidecars next to the resume JSON and any in the same directory
    matching *.sync.json. Returns nothing.
    """
    import signal
    target = Path(target_path).expanduser().resolve()
    candidates = set()
    # Sidecar next to resume JSON
    candidates.add(target.with_suffix(target.suffix + ".sync.json"))
    # Sidecars in the same dir
    try:
        for p in target.parent.glob("*.sync.json"):
            candidates.add(p)
    except Exception:
        pass

    for sidecar in candidates:
        if not sidecar.exists():
            continue
        try:
            payload = json.loads(sidecar.read_text(encoding="utf-8"))
            sid = payload.get("target", "")
            spid = payload.get("pid")
            if not spid:
                continue
            try:
                resolved_sid = str(Path(sid).expanduser().resolve())
            except Exception:
                resolved_sid = sid
            if resolved_sid != str(target):
                continue
            # Check if pid is alive
            try:
                os.kill(spid, 0)
            except (OSError, ProcessLookupError):
                # Dead — stale sidecar, leave it alone (or remove).
                try:
                    sidecar.unlink()
                except Exception:
                    pass
                continue
            # Alive — kill it; we're about to start a fresh one.
            try:
                os.kill(spid, signal.SIGTERM)
            except Exception:
                pass
            try:
                sidecar.unlink()
            except Exception:
                pass
        except Exception:
            continue


def write_sidecar(output_html_path, sync_config):
    """Record sync server pid/port next to the output HTML for later cleanup."""
    if not sync_config:
        return
    sidecar = Path(output_html_path).with_suffix(Path(output_html_path).suffix + ".sync.json")
    try:
        payload = {
            "pid": sync_config["process"].pid,
            "port": sync_config["port"],
            "target": sync_config["path"],
        }
        sidecar.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description='Generate HTML resume from JSON data')
    parser.add_argument('resume_json', help='Path to resume JSON file')
    parser.add_argument('output_html', help='Path to output HTML file')
    parser.add_argument(
        '--theme',
        default=DEFAULT_THEME,
        help='Resume theme name, a user-themes/<name> custom theme, or a path to a custom theme directory',
    )
    parser.add_argument('--lang', default='en', choices=SUPPORTED_LANGUAGES,
                        help='Language (default: en)')
    parser.add_argument('--editable', action='store_true',
                        help='Add inline editing capabilities to the HTML output')
    parser.add_argument('--no-sync', action='store_true',
                        help='Disable starting the local edit-sync server (editable mode only). '
                             'When set, the user must use the Copy JSON button to capture edits.')

    args = parser.parse_args()

    # Load resume data with error handling
    try:
        with open(args.resume_json, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Resume file not found: {args.resume_json}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.resume_json}")
        print(f"Details: {e}")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: Failed to read file. Please ensure it's UTF-8 encoded: {args.resume_json}")
        sys.exit(1)

    resume_data = normalize_resume_data(resume_data)

    # Validate resume data
    validation_errors = validate_resume_data(resume_data)
    if validation_errors:
        print("Error: Resume data validation failed:")
        for error in validation_errors:
            print(f"  - {error}")
        sys.exit(1)

    # Start sync server first (editable + sync enabled) so we can embed its
    # port/token into the HTML.
    sync_config = None
    if args.editable and not args.no_sync:
        # Kill any prior live sync server for this target so we don't accumulate
        # orphans across re-exports.
        reap_dead_sync_servers(args.resume_json)
        sync_config = start_sync_server(args.resume_json)
        if sync_config is None:
            print(
                "Warning: edit-sync server could not start — Save button will be "
                "disabled. User can still use Copy JSON to capture edits.",
                file=sys.stderr,
            )

    # Generate HTML
    print(f"Generating HTML resume with theme '{args.theme}' in {args.lang}...")
    try:
        html = generate_resume_html(
            resume_data,
            theme=args.theme,
            language=args.lang,
            editable=args.editable,
            resume_json_path=args.resume_json,
            sync_config=sync_config,
        )
    except ValueError as e:
        print("Error: Invalid theme configuration")
        print(f"Details: {e}")
        print(f"Available themes: {', '.join(list_available_themes(Path(__file__).parent.parent))}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to generate HTML")
        print(f"Details: {e}")
        sys.exit(1)

    # Save to file with error handling
    try:
        with open(args.output_html, 'w', encoding='utf-8') as f:
            f.write(html)
    except Exception as e:
        print(f"Error: Failed to write output file: {args.output_html}")
        print(f"Details: {e}")
        sys.exit(1)

    if sync_config:
        write_sidecar(args.output_html, sync_config)
        print(f"Edit-sync server: http://127.0.0.1:{sync_config['port']} "
              f"(writing to {sync_config['path']})")
        print(f"To stop the server later: kill {sync_config['process'].pid}")

    print(f"Resume generated: {args.output_html}")
    print(f"Open in browser to view: file://{Path(args.output_html).absolute()}")


if __name__ == "__main__":
    main()
