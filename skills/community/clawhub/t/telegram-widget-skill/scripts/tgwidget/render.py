"""Optional render check in headless Chromium (needs `playwright`).

The widget runs under the TelegramWidget stand-in from the official docs
("Testing > A first look in a browser"), with an approximation of Telegram's
default styles, at a phone bubble width. This catches runtime errors, network
attempts, the content height and the counted limits, and produces a
screenshot a vision model can look at. A browser draws everything, including
what Telegram removes, so a clean render does not replace `check`.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

PALETTES = {
    # light: the values of the docs' stand-in; dark: an approximation of a dark incoming bubble
    "light": {
        "bg_color": "#ffffff", "text_color": "#000000", "hint_color": "#707579", "link_color": "#3390ec",
        "button_color": "#3390ec", "button_text_color": "#ffffff", "secondary_bg_color": "#f1f1f4",
        "accent_text_color": "#3390ec", "subtitle_text_color": "#707579", "destructive_text_color": "#e53935",
        "section_bg_color": "#ffffff", "section_header_text_color": "#3390ec",
        "section_separator_color": "#e7e7e7", "header_bg_color": "#ffffff", "bottom_bar_bg_color": "#ffffff",
    },
    "dark": {
        "bg_color": "#182533", "text_color": "#f5f5f5", "hint_color": "#708499", "link_color": "#6ab3f3",
        "button_color": "#5288c1", "button_text_color": "#ffffff", "secondary_bg_color": "#232e3c",
        "accent_text_color": "#6ab2f2", "subtitle_text_color": "#708499", "destructive_text_color": "#ef5b5b",
        "section_bg_color": "#182533", "section_header_text_color": "#6ab3f3",
        "section_separator_color": "#0f1923", "header_bg_color": "#17212b", "bottom_bar_bg_color": "#17212b",
    },
}

_DEFAULTS_CSS = """
@layer tg-defaults {
  html { font-family: system-ui, sans-serif; font-size: var(--tg-text-font-size);
         line-height: var(--tg-text-line-height); color: var(--tg-theme-text-color); }
  body { margin: 8px 12px; padding: 0 0 env(safe-area-inset-bottom); }
  a { color: var(--tg-theme-link-color); }
  hr, td, th { border-color: var(--tg-theme-section-separator-color); }
  button { background: var(--tg-button-bg); color: var(--tg-button-text); border: 0;
           border-radius: var(--tg-button-radius); font: var(--tg-button-font);
           padding: var(--tg-button-padding); min-height: var(--tg-button-height); }
  button:active { opacity: var(--tg-button-pressed-opacity); }
  button[disabled] { opacity: var(--tg-button-disabled-opacity); }
}
"""

_MEASURE_JS = """
() => {
  const all = Array.from(document.querySelectorAll('*'));
  let text = 0; const w = document.createTreeWalker(document, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_COMMENT);
  while (w.nextNode()) text++;
  let heavy = 0, backdrop = 0;
  const blurred = (s) => s && s !== 'none' && /(?:^|\\s|\\))\\s*-?[\\d.]+px\\s+-?[\\d.]+px\\s+([\\d.]+)px/.test(s)
    && parseFloat(RegExp.$1) > 0;
  for (const el of all) {
    for (const pseudo of [null, '::before', '::after']) {
      const cs = getComputedStyle(el, pseudo);
      if (pseudo && (cs.content === 'none' || cs.content === 'normal')) continue;
      const bf = cs.backdropFilter || cs.webkitBackdropFilter;
      if (bf && bf !== 'none') backdrop++;
      if ((cs.filter && cs.filter !== 'none') || (bf && bf !== 'none') || parseFloat(cs.opacity) < 1
          || blurred(cs.boxShadow)) heavy++;
    }
  }
  return { height: Math.ceil(document.documentElement.scrollHeight), nodes: all.length + text,
           heavy, backdrop };
}
"""


def _stub(chat_data: Optional[str], public_data: Optional[str], scheme: str) -> str:
    palette = PALETTES[scheme]
    css_vars = "".join("--tg-theme-%s:%s;" % (k.replace("_", "-"), v) for k, v in palette.items())
    css_vars += (
        "--tg-color-scheme:%s;--tg-text-font-size:15px;--tg-text-line-height:1.35;--tg-text-padding:8px 12px;"
        "--tg-button-bg:%s;--tg-button-text:%s;--tg-button-radius:8px;--tg-button-font:500 15px system-ui;"
        "--tg-button-padding:6px 14px;--tg-button-height:36px;--tg-button-pressed-opacity:.7;"
        "--tg-button-disabled-opacity:.5;--tg-content-safe-area-inset-top:0px;"
        "--tg-content-safe-area-inset-right:0px;--tg-content-safe-area-inset-bottom:0px;"
        "--tg-content-safe-area-inset-left:0px;--tg-content-safe-area-corner-left:0px;"
        "--tg-content-safe-area-corner-right:0px;color-scheme:%s;"
        % (scheme, palette["button_color"], palette["button_text_color"], scheme)
    )
    state = json.dumps({"chatData": chat_data, "publicData": public_data, "scheme": scheme, "theme": palette})
    return (
        "<style>:root{%s}html{background:var(--tg-theme-bg-color)}%s</style>" % (css_vars, _DEFAULTS_CSS)
        + "<script>(function(){var s=%s;var h={};" % state
        + "window.__tgw_calls=[];function log(k,v){window.__tgw_calls.push([k,v]);}"
        "window.TelegramWidget={profile:1,isProfileAtLeast:function(n){return typeof n==='number'&&n<=1},"
        "colorScheme:s.scheme,themeParams:Object.freeze(s.theme),isActive:true,isPreview:false,isForward:false,"
        "chatType:'private',viewer:{id:1,first_name:'Test'},chatData:s.chatData,publicData:s.publicData,"
        "wallet:null,contentSafeAreaInset:{top:0,right:0,bottom:0,left:0,cornerLeft:0,cornerRight:0},"
        "HapticFeedback:{impactOccurred:function(){return this},notificationOccurred:function(){return this},"
        "selectionChanged:function(){return this}},"
        "onEvent:function(t,f){(h[t]=h[t]||[]).push(f)},offEvent:function(t,f){h[t]=(h[t]||[]).filter(function(g){return g!==f})},"
        "ready:function(){log('ready')},setResizeAnchor:function(e){log('setResizeAnchor',e)},"
        "watchPublicData:function(){},unwatchPublicData:function(){},"
        "openLink:function(u){log('openLink',u)},openTelegramLink:function(u){log('openTelegramLink',u)},"
        "copyText:function(t){log('copyText',t)},"
        "request:function(d){log('request',d);return Promise.resolve({result:null})}};})();</script>"
    )


def render(html: str, out_path: Optional[str], width: int = 320, scheme: str = "light",
           chat_data: Optional[str] = None, public_data: Optional[str] = None,
           settle_ms: int = 600) -> Dict[str, Any]:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception:
        return {"ok": False, "errors": [{
            "rule": "render-unavailable",
            "message": "render needs Playwright: pip install playwright && python -m playwright install chromium",
        }]}

    errors, warnings, network = [], [], []
    page_html = "<!doctype html>" + _stub(chat_data, public_data, scheme) + html
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": width, "height": 50}, device_scale_factor=2,
                                    color_scheme=scheme)

            def on_route(route):
                network.append(route.request.url[:120])
                route.abort()

            page.route("**/*", on_route)
            page.on("pageerror", lambda e: errors.append({"rule": "render-error", "message": str(e)[:300]}))
            page.on("console", lambda m: m.type == "error" and errors.append(
                {"rule": "render-error", "message": "console.error: " + m.text[:300]}))
            page.set_content(page_html, wait_until="load")
            page.wait_for_timeout(settle_ms)
            m = page.evaluate(_MEASURE_JS)
            calls = page.evaluate("window.__tgw_calls")
            height = m["height"]
            if height > 600:
                errors.append({"rule": "render-height",
                               "message": "content is %d px tall at %d px width; the bubble shows 600 px and "
                                          "clips the rest" % (height, width)})
            elif height > 560:
                warnings.append({"rule": "render-height",
                                 "message": "content is %d px tall at %d px width: close to the 600 px cap "
                                            "(the docs advise staying under about 560 px)" % (height, width)})
            if m["nodes"] > 2000:
                errors.append({"rule": "render-limits", "message": "%d DOM nodes (limit 2000)" % m["nodes"]})
            if m["heavy"] > 16 or m["backdrop"] > 2:
                errors.append({"rule": "render-limits",
                               "message": "%d elements with filter/backdrop-filter/opacity<1/blurred shadow "
                                          "(limit 16, of them %d with backdrop-filter, limit 2)"
                                          % (m["heavy"], m["backdrop"])})
            for url in network:
                errors.append({"rule": "render-network", "message": "tried to load %s" % url})
            if out_path:
                page.set_viewport_size({"width": width, "height": max(50, min(height, 600))})
                page.wait_for_timeout(100)
                page.screenshot(path=out_path)
        finally:
            browser.close()
    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "stats": {"width": width, "height": height, "scheme": scheme, "nodes": m["nodes"],
                  "heavy_elements": m["heavy"], "calls_at_start": calls},
        "screenshot": out_path,
    }
