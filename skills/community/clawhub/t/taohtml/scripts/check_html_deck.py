#!/usr/bin/env python3
"""Browser QA for local HTML decks.

Checks the runtime contract, routing, staged reveals, source modals, media
loading, console errors, screenshots, and visible content bounds. Requires Playwright:
  python -m pip install playwright
  python -m playwright install chromium
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CONTROLLED_STEP_CONTRACT = "fragment-v1"
CONTROLLED_STEP_SELECTOR = ".fragment"
TEXT_COLLISION_GAP_PX = 1.0
TEXT_COLLISION_FONT_METRIC_SLACK_PX = 0.25
CANVAS_TOLERANCE_RATIO = 0.005
FULLSCREEN_CONTROL_STABILITY_MS = 550


CONTROLLED_STEP_CHECK = f"""() => {{
  const deck = document.querySelector('.deck');
  const declared = deck?.getAttribute('data-taohtml-step-contract');
  const contract = declared || '{CONTROLLED_STEP_CONTRACT}';
  const pages = [...document.querySelectorAll('.slide')].map((slide, index) => {{
    const nodes = [...slide.querySelectorAll('{CONTROLLED_STEP_SELECTOR}')];
    const steps = nodes.reduce((maximum, node) => {{
      const normalized = Number.parseInt(node.dataset.taohtmlStep || '', 10);
      const authored = Number.parseInt(node.dataset.step || '', 10);
      return Math.max(maximum, Number.isInteger(normalized) ? normalized : authored || 0);
    }}, 0);
    return {{ page: index + 1, controlled_nodes: nodes.length, controlled_steps: steps }};
  }});
  return {{
    contract,
    declared: Boolean(declared),
    supported: contract === '{CONTROLLED_STEP_CONTRACT}',
    initial_mode: deck?.dataset.mode === 'reading' ? 'reading' : 'presentation',
    controlled_nodes: pages.reduce((total, item) => total + item.controlled_nodes, 0),
    controlled_steps: pages.reduce((total, item) => total + item.controlled_steps, 0),
    pages,
  }};
}}"""


CANVAS_COVERAGE_CHECK = f"""() => {{
  const deck = document.querySelector('.deck');
  const slide = document.querySelector('.slide.active');
  if (!deck || !slide) return {{ valid: false, error: 'missing deck or active slide' }};
  const d = deck.getBoundingClientRect();
  const s = slide.getBoundingClientRect();
  const toleranceX = Math.max(2, d.width * {CANVAS_TOLERANCE_RATIO});
  const toleranceY = Math.max(2, d.height * {CANVAS_TOLERANCE_RATIO});
  const deltas = {{
    left: s.left - d.left,
    top: s.top - d.top,
    width: s.width - d.width,
    height: s.height - d.height,
  }};
  const round = value => Math.round(value * 100) / 100;
  return {{
    valid: Math.abs(deltas.left) <= toleranceX &&
      Math.abs(deltas.top) <= toleranceY &&
      Math.abs(deltas.width) <= toleranceX &&
      Math.abs(deltas.height) <= toleranceY,
    tolerance: {{ x: round(toleranceX), y: round(toleranceY) }},
    deck: {{ left: round(d.left), top: round(d.top), width: round(d.width), height: round(d.height) }},
    slide: {{ left: round(s.left), top: round(s.top), width: round(s.width), height: round(s.height) }},
    deltas: Object.fromEntries(Object.entries(deltas).map(([key, value]) => [key, round(value)])),
    coverage: {{
      width_ratio: d.width ? round(s.width / d.width) : 0,
      height_ratio: d.height ? round(s.height / d.height) : 0,
    }},
  }};
}}"""


TEXT_COLLISION_CHECK = rf"""() => {{
  const root = document.querySelector('.slide.active');
  if (!root) return {{ collisions: [], intra_element_collisions: [], opt_outs: [],
    invalid_opt_outs: [], normal_flow_metric_exclusions: [] }};
  const safetyGap = {TEXT_COLLISION_GAP_PX};
  const fontMetricSlack = {TEXT_COLLISION_FONT_METRIC_SLACK_PX};
  const blockSelector = 'p,h1,h2,h3,h4,h5,h6,li,button,label,figcaption,td,th,caption,dt,dd,summary,legend,[data-qa-text-label]';
  const round = value => Math.round(value * 100) / 100;

  function visible(element) {{
    if (!(element instanceof Element)) return false;
    if (typeof element.checkVisibility === 'function' &&
        !element.checkVisibility({{ checkOpacity: true, checkVisibilityCSS: true }})) return false;
    const style = getComputedStyle(element);
    if (style.display === 'none' || style.visibility === 'hidden' ||
        style.visibility === 'collapse' || Number.parseFloat(style.opacity || '1') <= 0) return false;
    return true;
  }}

  function selectorFor(element) {{
    if (element.id) return `#${{CSS.escape(element.id)}}`;
    const parts = [];
    let current = element;
    while (current && current !== root && parts.length < 5) {{
      let part = current.localName || current.tagName.toLowerCase();
      if (current.classList?.length) {{
        part += '.' + [...current.classList].slice(0, 2).map(value => CSS.escape(value)).join('.');
      }}
      const parent = current.parentElement;
      if (parent) {{
        const siblings = [...parent.children].filter(item => item.localName === current.localName);
        if (siblings.length > 1) part += `:nth-of-type(${{siblings.indexOf(current) + 1}})`;
      }}
      parts.unshift(part);
      current = parent;
    }}
    return '.slide.active > ' + parts.join(' > ');
  }}

  function localOptOut(owner) {{
    if (!owner.hasAttribute('data-qa-ignore-text-collision')) return null;
    const reason = owner.getAttribute('data-qa-ignore-text-collision')?.trim() || '';
    return reason ? reason : '__invalid_empty_reason__';
  }}

  const labels = new Map();
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let textNode;
  while ((textNode = walker.nextNode())) {{
    const text = textNode.textContent?.replace(/\s+/g, ' ').trim();
    const parent = textNode.parentElement;
    if (!text || !parent || parent.closest('svg text') || !visible(parent)) continue;
    const semantic = parent.closest(blockSelector);
    const owner = semantic && root.contains(semantic) ? semantic : parent;
    if (!visible(owner)) continue;
    if (!labels.has(owner)) labels.set(owner, {{ owner, text: [], rects: [], kind: 'html' }});
    const range = document.createRange();
    range.selectNodeContents(textNode);
    const rects = [...range.getClientRects()]
      .filter(rect => rect.width > 0 && rect.height > 0)
      .map(rect => ({{ left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom,
        width: rect.width, height: rect.height }}));
    labels.get(owner).text.push(text);
    labels.get(owner).rects.push(...rects);
  }}

  for (const owner of root.querySelectorAll('svg text')) {{
    const text = owner.textContent?.replace(/\s+/g, ' ').trim();
    const rect = owner.getBoundingClientRect();
    if (!text || !visible(owner) || rect.width <= 0 || rect.height <= 0) continue;
    labels.set(owner, {{
      owner,
      text: [text],
      rects: [{{ left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom,
        width: rect.width, height: rect.height }}],
      kind: 'svg-text',
    }});
  }}

  const optOuts = [];
  const invalidOptOuts = [];
  const active = [];
  for (const label of labels.values()) {{
    const reason = localOptOut(label.owner);
    const normalized = {{
      owner: label.owner,
      text: label.text.join(' ').replace(/\s+/g, ' ').trim().slice(0, 120),
      selector: selectorFor(label.owner),
      kind: label.kind,
      rects: label.rects,
      layoutRect: (() => {{
        const rect = label.owner.getBoundingClientRect();
        return {{ left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom,
          width: rect.width, height: rect.height }};
      }})(),
    }};
    if (reason === '__invalid_empty_reason__') {{
      invalidOptOuts.push({{ text: normalized.text, selector: normalized.selector }});
      active.push(normalized);
    }} else if (reason) {{
      optOuts.push({{ text: normalized.text, selector: normalized.selector, reason }});
    }} else {{
      active.push(normalized);
    }}
  }}

  function sameInlineFlow(first, second) {{
    const a = first.owner;
    const b = second.owner;
    const sa = getComputedStyle(a);
    const sb = getComputedStyle(b);
    return a.parentElement === b.parentElement && sa.position === 'static' && sb.position === 'static' &&
      sa.display.startsWith('inline') && sb.display.startsWith('inline');
  }}

  function isStaticUntransformedHtml(label) {{
    if (label.kind !== 'html') return false;
    const style = getComputedStyle(label.owner);
    const noIndependentTransform = style.transform === 'none' &&
      (!style.translate || style.translate === 'none') &&
      (!style.scale || style.scale === 'none') &&
      (!style.rotate || style.rotate === 'none');
    return style.position === 'static' && style.float === 'none' && noIndependentTransform;
  }}

  function normalFlowMetricExclusion(
    first, second, overlapX, overlapY, horizontalGap, verticalGap
  ) {{
    if (!isStaticUntransformedHtml(first) || !isStaticUntransformedHtml(second)) return null;
    const a = first.layoutRect;
    const b = second.layoutRect;
    const layoutOverlapX = Math.min(a.right, b.right) - Math.max(a.left, b.left);
    const layoutOverlapY = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
    if (layoutOverlapX > 0 && layoutOverlapY > 0) return null;
    const intersects = overlapX > 0 && overlapY > 0;
    const gapDepths = [];
    if (overlapY > 0 && horizontalGap < safetyGap) gapDepths.push(safetyGap - horizontalGap);
    if (overlapX > 0 && verticalGap < safetyGap) gapDepths.push(safetyGap - verticalGap);
    const metricDepth = intersects
      ? Math.min(overlapX, overlapY)
      : (gapDepths.length ? Math.min(...gapDepths) : 0);
    if (metricDepth > safetyGap + fontMetricSlack) return null;
    return {{
      layout_clearance: {{
        x: round(Math.max(b.left - a.right, a.left - b.right, 0)),
        y: round(Math.max(b.top - a.bottom, a.top - b.bottom, 0)),
      }},
      metric_overlap_depth: round(metricDepth),
      metric_overlap_limit: round(safetyGap + fontMetricSlack),
      reason: 'static-untransformed HTML layout boxes are separate; shallow Range overlap is font metrics',
    }};
  }}

  function lineBands(rects) {{
    const bands = [];
    for (const rect of [...rects].sort((a, b) => a.top - b.top || a.left - b.left)) {{
      const center = (rect.top + rect.bottom) / 2;
      const band = bands.find(candidate => {{
        const tolerance = Math.max(1, Math.min(candidate.maxHeight, rect.height) * .35);
        return Math.abs(candidate.center - center) <= tolerance;
      }});
      if (band) {{
        band.left = Math.min(band.left, rect.left);
        band.top = Math.min(band.top, rect.top);
        band.right = Math.max(band.right, rect.right);
        band.bottom = Math.max(band.bottom, rect.bottom);
        band.maxHeight = Math.max(band.maxHeight, rect.height);
        band.center = (band.top + band.bottom) / 2;
      }} else {{
        bands.push({{
          left: rect.left,
          top: rect.top,
          right: rect.right,
          bottom: rect.bottom,
          maxHeight: rect.height,
          center,
        }});
      }}
    }}
    return bands.sort((a, b) => a.top - b.top || a.left - b.left);
  }}

  const intraElementCollisions = [];
  for (const label of active) {{
    if (label.kind !== 'html') continue;
    const bands = lineBands(label.rects);
    if (bands.length < 2) continue;
    const style = getComputedStyle(label.owner);
    for (let index = 0; index < bands.length - 1; index += 1) {{
      const firstLine = bands[index];
      const secondLine = bands[index + 1];
      const overlapX = Math.min(firstLine.right, secondLine.right) -
        Math.max(firstLine.left, secondLine.left);
      const verticalGap = secondLine.top - firstLine.bottom;
      if (overlapX <= 0 || verticalGap >= safetyGap) continue;
      intraElementCollisions.push({{
        collision_scope: 'same-owner-lines',
        first: {{
          text: `${{label.text}} [line ${{index + 1}}]`,
          selector: label.selector,
          kind: 'html',
        }},
        second: {{
          text: `${{label.text}} [line ${{index + 2}}]`,
          selector: label.selector,
          kind: 'html',
        }},
        overlap: {{ x: round(overlapX), y: round(Math.max(-verticalGap, 0)) }},
        clearance: {{ x: 0, y: round(Math.max(verticalGap, 0)) }},
        safety_gap: safetyGap,
        lines: {{ first: index + 1, second: index + 2, total: bands.length }},
        typography: {{
          font_size: style.fontSize,
          line_height: style.lineHeight,
          font_family: style.fontFamily,
        }},
      }});
    }}
  }}

  const collisions = [];
  const normalFlowMetricExclusions = [];
  for (let i = 0; i < active.length; i += 1) {{
    for (let j = i + 1; j < active.length; j += 1) {{
      const first = active[i];
      const second = active[j];
      if (first.owner.contains(second.owner) || second.owner.contains(first.owner)) continue;
      let pairHandled = false;
      for (const a of first.rects) {{
        for (const b of second.rects) {{
          const overlapX = Math.min(a.right, b.right) - Math.max(a.left, b.left);
          const overlapY = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
          const horizontalGap = Math.max(b.left - a.right, a.left - b.right, 0);
          const verticalGap = Math.max(b.top - a.bottom, a.top - b.bottom, 0);
          const intersects = overlapX > 0 && overlapY > 0;
          const closeHorizontal = overlapY > 0 && horizontalGap < safetyGap;
          const closeVertical = overlapX > 0 && verticalGap < safetyGap;
          const unsafeGap = !sameInlineFlow(first, second) && (closeHorizontal || closeVertical);
          if (!intersects && !unsafeGap) continue;
          const metricExclusion = normalFlowMetricExclusion(
            first, second, overlapX, overlapY, horizontalGap, verticalGap
          );
          if (metricExclusion) {{
            normalFlowMetricExclusions.push({{
              first: {{ text: first.text, selector: first.selector, kind: first.kind }},
              second: {{ text: second.text, selector: second.selector, kind: second.kind }},
              range_overlap: {{ x: round(Math.max(overlapX, 0)), y: round(Math.max(overlapY, 0)) }},
              ...metricExclusion,
            }});
            pairHandled = true;
            break;
          }}
          collisions.push({{
            first: {{ text: first.text, selector: first.selector, kind: first.kind }},
            second: {{ text: second.text, selector: second.selector, kind: second.kind }},
            overlap: {{ x: round(Math.max(overlapX, 0)), y: round(Math.max(overlapY, 0)) }},
            clearance: {{ x: round(horizontalGap), y: round(verticalGap) }},
            safety_gap: safetyGap,
          }});
          pairHandled = true;
          break;
        }}
        if (pairHandled) break;
      }}
    }}
  }}
  return {{ collisions, intra_element_collisions: intraElementCollisions,
    opt_outs: optOuts, invalid_opt_outs: invalidOptOuts,
    normal_flow_metric_exclusions: normalFlowMetricExclusions }};
}}"""


OVERFLOW_CHECK = """() => {
  const root = document.querySelector('.slide.active');
  if (!root) return [];
  const bounds = root.getBoundingClientRect();
  const selector = 'h1,h2,h3,h4,p,li,button,img,video,table,svg,[data-qa-bounds]';
  return [...root.querySelectorAll(selector)]
    .filter(el => {
      if (el.closest('[data-qa-ignore-overflow]')) return false;
      const r = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return false;
      if (r.width === 0 || r.height === 0) return false;
      return r.left < bounds.left - 2 || r.top < bounds.top - 2 ||
        r.right > bounds.right + 2 || r.bottom > bounds.bottom + 2;
    })
    .slice(0, 20)
    .map(el => {
      const r = el.getBoundingClientRect();
      return {
        tag: el.tagName,
        cls: typeof el.className === 'string' ? el.className : '',
        text: (el.textContent || '').trim().slice(0, 80),
        rect: { left: r.left, top: r.top, right: r.right, bottom: r.bottom },
      };
    });
}"""

RHYTHM_CHECK = """() => {
  const root = document.querySelector('.slide.active');
  if (!root) return [];
  return [...root.querySelectorAll('[data-rhythm-check]')]
    .map(container => {
      const token = container.getAttribute('data-rhythm-check') || '';
      const axis = container.getAttribute('data-rhythm-axis') || 'block';
      const from = container.querySelector(':scope > [data-rhythm-from]');
      const to = container.querySelector(':scope > [data-rhythm-to]');
      const expected = Number.parseFloat(getComputedStyle(container).getPropertyValue(token));
      if (!from || !to || !Number.isFinite(expected) || !['block', 'inline'].includes(axis)) {
        return { token, axis, error: 'invalid rhythm contract' };
      }
      const fromRect = from.getBoundingClientRect();
      const toRect = to.getBoundingClientRect();
      const actual = axis === 'inline'
        ? toRect.left - fromRect.right
        : toRect.top - fromRect.bottom;
      if (Math.abs(actual - expected) <= 1.25) return null;
      return {
        token,
        axis,
        expected,
        actual: Math.round(actual * 100) / 100,
        container: typeof container.className === 'string' ? container.className : '',
        from: (from.textContent || '').trim().slice(0, 60),
        to: (to.textContent || '').trim().slice(0, 60),
      };
    })
    .filter(Boolean)
    .slice(0, 20);
}"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run browser QA for an HTML deck.")
    parser.add_argument("html", type=Path, help="HTML file to test.")
    parser.add_argument("output_dir", type=Path, help="Directory for screenshots and report.")
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--max-pages", type=int, default=0, help="Limit slide count. 0 means all.")
    parser.add_argument(
        "--executable-path",
        type=Path,
        help="Optional Chromium executable path for environments without Playwright's headless shell.",
    )
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit("Playwright is required. Install with: python -m pip install playwright") from exc

    args.output_dir.mkdir(parents=True, exist_ok=True)
    url = args.html.resolve().as_uri()
    results: dict[str, object] = {
        "url": url,
        "viewport": {"width": args.width, "height": args.height},
        "pages": [],
    }
    failures: list[str] = []

    with sync_playwright() as pw:
        launch_options = {}
        if args.executable_path:
            if not args.executable_path.is_file():
                raise SystemExit(f"Chromium executable not found: {args.executable_path}")
            launch_options["executable_path"] = str(args.executable_path)
        browser = pw.chromium.launch(**launch_options)
        page = browser.new_page(viewport={"width": args.width, "height": args.height})
        console_errors: list[str] = []
        page_errors: list[str] = []
        page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
        page.on("pageerror", lambda error: page_errors.append(str(error)))

        page.goto(url, wait_until="load")
        controlled_steps = page.evaluate(CONTROLLED_STEP_CHECK)
        results["controlled_step_contract"] = controlled_steps
        if not controlled_steps["supported"]:
            failures.append(
                "Unsupported controlled-step contract: "
                f"{controlled_steps['contract']}."
            )
        elif (
            controlled_steps["initial_mode"] == "presentation"
            and controlled_steps["controlled_steps"] == 0
        ):
            failures.append(
                "Presentation mode has zero controlled presentation steps under "
                f"{controlled_steps['contract']}."
            )
        slide_count = page.locator(".slide").count()
        if args.max_pages:
            slide_count = min(slide_count, args.max_pages)
        if slide_count == 0:
            failures.append("No .slide elements found.")

        runtime_methods = [
            "getState",
            "setMode",
            "showPage",
            "nextStep",
            "previousStep",
            "nextPage",
            "previousPage",
            "toggleFullscreen",
            "setEditing",
        ]
        runtime_contract = page.evaluate(
            """methods => {
              const runtime = window.TaoHtmlRuntime;
              return {
                available: Boolean(runtime),
                missing: runtime ? methods.filter(name => typeof runtime[name] !== 'function') : methods,
              };
            }""",
            runtime_methods,
        )
        results["runtime_contract"] = runtime_contract
        if not runtime_contract["available"] or runtime_contract["missing"]:
            failures.append(f"Runtime contract is incomplete: {runtime_contract}")

        runtime_behavior: dict[str, object] = {"tested": False}
        if runtime_contract["available"] and slide_count >= 2:
            page.goto(f"{url}#1")
            reset_presentation = """index => {
              const runtime = window.TaoHtmlRuntime;
              if (runtime.getState().mode === 'presentation') runtime.setMode('reading');
              runtime.showPage(index);
              runtime.setMode('presentation');
            }"""
            page.evaluate(reset_presentation, 0)
            first_step_count = page.locator(
                f".slide.active {CONTROLLED_STEP_SELECTOR}"
            ).evaluate_all(
                "els => Math.max(0, ...els.map(el => Number.parseInt(el.dataset.taohtmlStep || '0', 10)))"
            )

            before_left_at_zero = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.keyboard.press("ArrowLeft")
            after_left_at_zero = page.evaluate("() => window.TaoHtmlRuntime.getState()")

            page.evaluate(reset_presentation, 0)
            page.keyboard.press("ArrowRight")
            after_arrow_right = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.evaluate(reset_presentation, 0)
            page.keyboard.press("Space")
            after_space = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.evaluate(reset_presentation, 0)
            page.evaluate(
                """() => document.querySelector('.slide.active').dispatchEvent(
                  new MouseEvent('click', { bubbles: true, cancelable: true, button: 0 })
                )"""
            )
            after_blank_click = page.evaluate("() => window.TaoHtmlRuntime.getState()")

            page.evaluate(reset_presentation, 0)
            for _ in range(first_step_count):
                page.keyboard.press("ArrowRight")
            after_last_step = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.keyboard.press("ArrowRight")
            after_step_boundary = page.evaluate("() => window.TaoHtmlRuntime.getState()")

            page.evaluate(reset_presentation, 0)
            page.keyboard.press("PageDown")
            after_page_down = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.keyboard.press("PageUp")
            after_page_up = page.evaluate("() => window.TaoHtmlRuntime.getState()")

            page.evaluate(reset_presentation, 0)
            if first_step_count:
                page.keyboard.press("ArrowRight")
            page.keyboard.press("PageDown")
            page.keyboard.press("PageUp")
            after_return = page.evaluate("() => window.TaoHtmlRuntime.getState()")

            page.evaluate(reset_presentation, 1)
            second_before_left_at_zero = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.keyboard.press("ArrowLeft")
            second_after_left_at_zero = page.evaluate("() => window.TaoHtmlRuntime.getState()")

            page.evaluate(reset_presentation, 0)
            page.locator("#next").click()
            after_next_button = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.locator("#prev").click()
            after_prev_button = page.evaluate("() => window.TaoHtmlRuntime.getState()")

            page.evaluate("() => document.activeElement?.blur?.()")
            page.evaluate("() => window.TaoHtmlRuntime.setMode('reading')")
            page.evaluate("() => window.TaoHtmlRuntime.showPage(0)")
            page.wait_for_timeout(520)
            reading_visible = page.evaluate(
                """selector => [...document.querySelectorAll(`.slide.active ${selector}`)]
                .every(el => getComputedStyle(el).opacity === '1')""",
                CONTROLLED_STEP_SELECTOR,
            )
            reading_state = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.keyboard.press("ArrowRight")
            reading_after_right = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.evaluate("() => window.TaoHtmlRuntime.showPage(0)")
            page.keyboard.press("Space")
            reading_after_space = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.evaluate("() => window.TaoHtmlRuntime.showPage(0)")
            page.evaluate(
                """() => document.querySelector('.slide.active').dispatchEvent(
                  new MouseEvent('click', { bubbles: true, cancelable: true, button: 0 })
                )"""
            )
            reading_after_blank_click = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.evaluate("() => window.TaoHtmlRuntime.showPage(1)")
            page.keyboard.press("ArrowLeft")
            reading_after_left = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.evaluate("() => window.TaoHtmlRuntime.showPage(0)")
            page.keyboard.press("PageDown")
            reading_after_page_down = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.keyboard.press("PageUp")
            reading_after_page_up = page.evaluate("() => window.TaoHtmlRuntime.getState()")

            page.evaluate(reset_presentation, 0)
            if first_step_count:
                page.keyboard.press("ArrowRight")
            page.evaluate("() => window.TaoHtmlRuntime.setMode('reading')")
            page.evaluate("() => window.TaoHtmlRuntime.setMode('presentation')")
            presentation_reset = page.evaluate("() => window.TaoHtmlRuntime.getState()")

            page.evaluate(reset_presentation, 0)
            protected_before = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            protected_clicks = page.evaluate(
                """() => {
                  const slide = document.querySelector('.slide.active');
                  const sandbox = document.createElement('div');
                  sandbox.id = 'taohtml-runtime-interaction-sandbox';
                  sandbox.innerHTML = `
                    <a data-kind="link" href="#1">link</a>
                    <button data-kind="button">button</button>
                    <div data-kind="attachment" data-taohtml-attachment>attachment</div>
                    <div data-kind="chart" class="ri-chart">chart</div>
                    <div data-kind="interactive" data-taohtml-interactive>interactive</div>
                    <form data-kind="form">form</form>
                    <div data-kind="editable" contenteditable="true">editable</div>
                    <div data-kind="dialog" role="dialog">dialog</div>
                    <canvas data-kind="canvas"></canvas>
                    <svg data-kind="svg"></svg>`;
                  slide.appendChild(sandbox);
                  const states = {};
                  sandbox.querySelectorAll('[data-kind]').forEach(target => {
                    target.dispatchEvent(new MouseEvent('click', {
                      bubbles: true, cancelable: true, button: 0,
                    }));
                    states[target.dataset.kind] = window.TaoHtmlRuntime.getState();
                  });
                  sandbox.remove();
                  return states;
                }"""
            )
            page.evaluate(
                """() => {
                  document.querySelector('#modal').classList.add('open');
                  document.querySelector('#modal').setAttribute('aria-hidden', 'false');
                  document.querySelector('.slide.active').dispatchEvent(
                    new MouseEvent('click', { bubbles: true, cancelable: true, button: 0 })
                  );
                }"""
            )
            protected_modal = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.evaluate("() => document.querySelector('#modalClose').click()")

            control_before = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.locator("#moreToggle").focus()
            page.keyboard.press("Space")
            control_after = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            control_menu_open = page.locator("#moreMenu:not([hidden])").count() == 1
            page.wait_for_timeout(2200)
            menu_stays_open = page.locator("#moreMenu:not([hidden])").count() == 1
            page.locator("#moreToggle").click()
            page.locator("#moreToggle").click()
            page.locator("#fullscreenToggle").click()
            page.wait_for_function(
                "() => Boolean(document.fullscreenElement)"
            )
            page.wait_for_timeout(FULLSCREEN_CONTROL_STABILITY_MS)
            fullscreen_entered = page.evaluate(
                """() => ({
                  menuHidden: document.querySelector('#moreMenu').hidden,
                  expanded: document.querySelector('#moreToggle').getAttribute('aria-expanded'),
                  controlsHidden: document.querySelector('#deck').classList.contains('controls-hidden'),
                  pageIndicatorVisible: (() => {
                    const indicator = document.querySelector('#pageIndicator');
                    const style = getComputedStyle(indicator);
                    const box = indicator.getBoundingClientRect();
                    return style.opacity !== '0' && style.visibility !== 'hidden' && box.width > 0 && box.height > 0;
                  })(),
                })"""
            )
            page.keyboard.press("ArrowRight")
            keyboard_kept_hidden = page.locator("#deck.controls-hidden").count() == 1
            page.dispatch_event("#deck", "pointerdown")
            pointerdown_kept_hidden = page.locator("#deck.controls-hidden").count() == 1
            page.evaluate(
                """() => document.querySelector('.slide.active').dispatchEvent(
                  new MouseEvent('click', { bubbles: true, cancelable: true, button: 0 })
                )"""
            )
            blank_click_kept_hidden = page.locator("#deck.controls-hidden").count() == 1
            page.evaluate("() => document.dispatchEvent(new Event('fullscreenchange'))")
            fullscreenchange_kept_hidden = page.locator("#deck.controls-hidden").count() == 1
            page.wait_for_timeout(FULLSCREEN_CONTROL_STABILITY_MS)

            page.mouse.move(args.width // 3 - 6, args.height // 3)
            page.mouse.move(args.width // 3 + 6, args.height // 3)
            page.wait_for_function(
                "() => !document.querySelector('#deck').classList.contains('controls-hidden')"
            )
            mousemove_revealed = page.locator("#deck:not(.controls-hidden)").count() == 1
            page.wait_for_timeout(2200)
            idle_hidden = page.locator("#deck.controls-hidden").count() == 1

            prev_box = page.locator("#prev").bounding_box()
            if prev_box:
                page.mouse.move(
                    prev_box["x"] + prev_box["width"] / 2 - 2,
                    prev_box["y"] + prev_box["height"] / 2,
                )
                page.mouse.move(
                    prev_box["x"] + prev_box["width"] / 2 + 2,
                    prev_box["y"] + prev_box["height"] / 2,
                )
            page.wait_for_timeout(2200)
            control_interaction_pinned = page.locator("#deck:not(.controls-hidden)").count() == 1
            page.mouse.move(args.width // 3, args.height // 3)
            page.wait_for_timeout(2200)
            after_control_idle_hidden = page.locator("#deck.controls-hidden").count() == 1

            more_box = page.locator("#moreToggle").bounding_box()
            if more_box:
                page.mouse.move(
                    more_box["x"] + more_box["width"] / 2,
                    more_box["y"] + more_box["height"] / 2,
                )
            page.locator("#moreToggle").click()
            page.wait_for_timeout(2200)
            menu_pinned_controls = (
                page.locator("#moreMenu:not([hidden])").count() == 1
                and page.locator("#deck:not(.controls-hidden)").count() == 1
            )
            page.locator("#moreToggle").click()
            page.mouse.move(args.width // 3, args.height // 3)
            page.wait_for_timeout(2200)
            after_menu_close_hidden = page.locator("#deck.controls-hidden").count() == 1
            page.keyboard.press("Space")
            hidden_more_keyboard_blocked = (
                page.locator("#deck.controls-hidden").count() == 1
                and page.locator("#moreMenu[hidden]").count() == 1
            )

            page.evaluate("() => window.TaoHtmlRuntime.setEditing(true)")
            page.wait_for_timeout(2200)
            edit_mode_pinned_controls = page.locator("#deck:not(.controls-hidden)").count() == 1
            page.evaluate("() => window.TaoHtmlRuntime.setEditing(false)")
            page.wait_for_timeout(2200)
            after_edit_hidden = page.locator("#deck.controls-hidden").count() == 1

            page.evaluate("() => document.exitFullscreen()")
            page.wait_for_function(
                """() => !document.fullscreenElement &&
                  !document.querySelector('#deck').classList.contains('controls-hidden')"""
            )
            fullscreen_exited = page.evaluate(
                """() => ({
                  menuHidden: document.querySelector('#moreMenu').hidden,
                  expanded: document.querySelector('#moreToggle').getAttribute('aria-expanded'),
                  controlsHidden: document.querySelector('#deck').classList.contains('controls-hidden'),
                })"""
            )
            grouped_step = page.evaluate(
                """selector => {
                  const targetIndex = [...document.querySelectorAll('.slide')]
                    .findIndex(slide => slide.querySelectorAll(selector).length >= 2);
                  if (targetIndex < 0) return { tested: false };
                  const runtime = window.TaoHtmlRuntime;
                  runtime.showPage(targetIndex);
                  runtime.setMode('reading');
                  document.querySelectorAll(`.slide.active ${selector}`)
                    .forEach(el => { el.dataset.taohtmlStep = '1'; });
                  runtime.setMode('presentation');
                  runtime.nextStep();
                  return {
                    tested: true,
                    state: runtime.getState(),
                    total: document.querySelectorAll(`.slide.active ${selector}`).length,
                    visible: document.querySelectorAll(`.slide.active ${selector}.visible`).length,
                  };
                }""",
                CONTROLLED_STEP_SELECTOR,
            )

            expected_stage = 1 if first_step_count else 0
            runtime_behavior = {
                "tested": True,
                "presentation": {
                    "before_left_at_zero": before_left_at_zero,
                    "after_left_at_zero": after_left_at_zero,
                    "after_arrow_right": after_arrow_right,
                    "after_space": after_space,
                    "after_blank_click": after_blank_click,
                    "after_last_step": after_last_step,
                    "after_step_boundary": after_step_boundary,
                    "after_page_down": after_page_down,
                    "after_page_up": after_page_up,
                    "after_return": after_return,
                    "second_before_left_at_zero": second_before_left_at_zero,
                    "second_after_left_at_zero": second_after_left_at_zero,
                    "after_next_button": after_next_button,
                    "after_prev_button": after_prev_button,
                },
                "reading": {
                    "state": reading_state,
                    "visible": reading_visible,
                    "after_right": reading_after_right,
                    "after_space": reading_after_space,
                    "after_blank_click": reading_after_blank_click,
                    "after_left": reading_after_left,
                    "after_page_down": reading_after_page_down,
                    "after_page_up": reading_after_page_up,
                    "presentation_reset": presentation_reset,
                },
                "protected_clicks": protected_clicks,
                "protected_modal": protected_modal,
                "control_keyboard": {
                    "before": control_before,
                    "after": control_after,
                    "menu_open": control_menu_open,
                    "menu_stays_open": menu_stays_open,
                },
                "fullscreen": {
                    "entered": fullscreen_entered,
                    "stability_wait_ms": FULLSCREEN_CONTROL_STABILITY_MS,
                    "keyboard_kept_hidden": keyboard_kept_hidden,
                    "pointerdown_kept_hidden": pointerdown_kept_hidden,
                    "blank_click_kept_hidden": blank_click_kept_hidden,
                    "fullscreenchange_kept_hidden": fullscreenchange_kept_hidden,
                    "mousemove_revealed": mousemove_revealed,
                    "idle_hidden": idle_hidden,
                    "control_interaction_pinned": control_interaction_pinned,
                    "after_control_idle_hidden": after_control_idle_hidden,
                    "menu_pinned_controls": menu_pinned_controls,
                    "after_menu_close_hidden": after_menu_close_hidden,
                    "hidden_more_keyboard_blocked": hidden_more_keyboard_blocked,
                    "edit_mode_pinned_controls": edit_mode_pinned_controls,
                    "after_edit_hidden": after_edit_hidden,
                    "exited": fullscreen_exited,
                },
                "grouped_step": grouped_step,
            }
            if after_left_at_zero != before_left_at_zero or second_after_left_at_zero != second_before_left_at_zero:
                failures.append("ArrowLeft at step zero must not perform whole-page navigation or mutate stored stages.")
            for label, observed in (
                ("ArrowRight", after_arrow_right),
                ("Space", after_space),
                ("blank-page click", after_blank_click),
            ):
                if observed["index"] != 0 or observed["stages"][0] != expected_stage:
                    failures.append(f"{label} did not advance exactly one presentation step.")
            if after_last_step["index"] != 0 or after_last_step["stages"][0] != first_step_count:
                failures.append("Completing the last presentation step changed pages too early.")
            if after_step_boundary["index"] != 1:
                failures.append("Advancing after the last presentation step did not enter the next page.")
            if after_page_down["index"] != 1 or after_page_down["stages"][0] != 0:
                failures.append("PageDown did not jump directly to the next page without completing steps.")
            if after_page_up["index"] != 0 or after_page_up["stages"][0] != 0:
                failures.append("PageUp did not return directly to the previous whole page.")
            if after_return["index"] != 0 or after_return["stages"][0] != expected_stage:
                failures.append("Returning to a page did not restore its presentation stage.")
            if after_next_button["index"] != 1 or after_prev_button["index"] != 0:
                failures.append("Previous/next screen controls did not navigate by whole page.")
            if reading_state["mode"] != "reading" or not reading_visible:
                failures.append("Reading mode did not expose all current-page fragments.")
            for label, observed, expected_index in (
                ("ArrowRight", reading_after_right, 1),
                ("Space", reading_after_space, 1),
                ("blank-page click", reading_after_blank_click, 1),
                ("ArrowLeft", reading_after_left, 0),
                ("PageDown", reading_after_page_down, 1),
                ("PageUp", reading_after_page_up, 0),
            ):
                if observed["mode"] != "reading" or observed["index"] != expected_index:
                    failures.append(f"{label} did not perform whole-page navigation in reading mode.")
            if presentation_reset["mode"] != "presentation" or presentation_reset["stages"][0] != 0:
                failures.append("Switching from reading to presentation did not reset the current page.")
            if any(observed != protected_before for observed in protected_clicks.values()) or protected_modal != protected_before:
                failures.append("An interactive region or open modal advanced the report.")
            if control_after != control_before or not control_menu_open or not menu_stays_open:
                failures.append("Focused controls did not consume Space without advancing the report.")
            if fullscreen_entered != {
                "menuHidden": True,
                "expanded": "false",
                "controlsHidden": True,
                "pageIndicatorVisible": True,
            }:
                failures.append("Presentation fullscreen did not begin with navigation and more controls hidden while keeping the page number visible.")
            if not all((keyboard_kept_hidden, pointerdown_kept_hidden, blank_click_kept_hidden, fullscreenchange_kept_hidden)):
                failures.append("A non-mousemove input revealed presentation fullscreen controls.")
            if not mousemove_revealed or not idle_hidden:
                failures.append("A real mousemove did not reveal controls or idle time did not hide them again.")
            if not all((control_interaction_pinned, after_control_idle_hidden, menu_pinned_controls, after_menu_close_hidden, hidden_more_keyboard_blocked, edit_mode_pinned_controls, after_edit_hidden)):
                failures.append("Control interaction, menu, or edit mode did not pin and rearm fullscreen auto-hide correctly.")
            if fullscreen_exited != {"menuHidden": True, "expanded": "false", "controlsHidden": False}:
                failures.append("Exiting fullscreen left stale more-menu state behind.")
            if grouped_step["tested"] and grouped_step["visible"] != grouped_step["total"]:
                failures.append("Elements sharing one data-step did not reveal together.")
        results["runtime_behavior"] = runtime_behavior
        page.reload(wait_until="load")
        page.add_style_tag(
            content="""
              *, *::before, *::after {
                transition-duration: 0s !important;
                transition-delay: 0s !important;
                animation-duration: 0s !important;
                animation-delay: 0s !important;
              }
            """
        )

        for i in range(slide_count):
            console_start = 0 if i == 0 else len(console_errors)
            page_error_start = 0 if i == 0 else len(page_errors)
            page.goto(f"{url}#{i + 1}")
            page.wait_for_timeout(150)

            active = page.locator(".slide.active")
            active_count = active.count()
            active_index = page.evaluate(
                "() => [...document.querySelectorAll('.slide')].indexOf(document.querySelector('.slide.active'))"
            )
            route_ok = active_count == 1 and active_index == i

            fragment_count = (
                active.locator(CONTROLLED_STEP_SELECTOR).count()
                if active_count == 1
                else 0
            )
            step_count = (
                active.locator(CONTROLLED_STEP_SELECTOR).evaluate_all(
                    "els => Math.max(0, ...els.map(el => Number.parseInt(el.dataset.taohtmlStep || '0', 10)))"
                )
                if active_count == 1
                else 0
            )
            initial_mode = page.evaluate(
                "() => window.TaoHtmlRuntime?.getState().mode || "
                "(document.querySelector('.deck')?.dataset.mode === 'reading' ? 'reading' : 'presentation')"
            )
            text_collision_states: list[dict[str, object]] = []

            def capture_text_state(label: str) -> None:
                state_result = page.evaluate(TEXT_COLLISION_CHECK)
                text_collision_states.append({"state": label, **state_result})

            capture_text_state(f"{initial_mode}-initial")
            if initial_mode == "reading" and fragment_count and runtime_contract["available"]:
                page.evaluate("() => window.TaoHtmlRuntime.setMode('presentation')")
                page.wait_for_timeout(40)
                capture_text_state("presentation-step-0")

            for step_index in range(step_count):
                page.keyboard.press("ArrowRight")
                page.wait_for_timeout(40)
                capture_text_state(f"presentation-step-{step_index + 1}")
            visible_fragments = (
                active.locator(f"{CONTROLLED_STEP_SELECTOR}.visible").count()
                if active_count == 1
                else 0
            )
            for _ in range(step_count):
                page.keyboard.press("ArrowLeft")
                page.wait_for_timeout(40)
            rewound_fragments = (
                active.locator(f"{CONTROLLED_STEP_SELECTOR}.visible").count()
                if active_count == 1
                else 0
            )
            for _ in range(step_count):
                page.keyboard.press("ArrowRight")
                page.wait_for_timeout(40)
            if initial_mode == "reading" and runtime_contract["available"]:
                page.evaluate("() => window.TaoHtmlRuntime.setMode('reading')")
                page.wait_for_timeout(40)

            source_failures: list[str] = []
            source_buttons = active.locator(".source-btn") if active_count == 1 else page.locator(".never-match")
            for source_index in range(source_buttons.count()):
                button = source_buttons.nth(source_index)
                source = button.get_attribute("data-source") or "<missing data-source>"
                button.click()
                page.wait_for_timeout(200)
                modal_open = page.locator("#modal.open").count() == 1
                if not modal_open:
                    source_failures.append(f"{source}: modal did not open")
                media_error = page.locator("#modalBody").get_attribute("data-media-error")
                if media_error:
                    source_failures.append(f"{source}: failed to load")
                source_media_failed = page.evaluate(
                    """() => {
                      const media = document.querySelector('#modalBody img, #modalBody video');
                      if (!media) return Boolean(document.querySelector('#modalBody [data-media-error], #modalBody .source-error'));
                      if (media.tagName === 'IMG') return !media.complete || media.naturalWidth === 0;
                      return Boolean(media.error);
                    }"""
                )
                if source_media_failed and not media_error:
                    source_failures.append(f"{source}: media element failed")
                if modal_open:
                    page.locator("#modalClose").click()

            # Capture the stable page state rather than a fragment mid-transition.
            page.wait_for_timeout(520)

            image_failures = page.evaluate(
                """() => [...document.images]
                .filter(img => !img.complete || img.naturalWidth === 0)
                .map(img => img.getAttribute('src') || '')"""
            )
            overflow = page.evaluate(OVERFLOW_CHECK)
            rhythm_failures = page.evaluate(RHYTHM_CHECK)
            canvas_coverage = page.evaluate(CANVAS_COVERAGE_CHECK)
            text_collisions = [
                {"state": state["state"], **collision}
                for state in text_collision_states
                for collision in [
                    *state["collisions"],
                    *state["intra_element_collisions"],
                ]
            ]
            intra_element_text_collisions = [
                {"state": state["state"], **collision}
                for state in text_collision_states
                for collision in state["intra_element_collisions"]
            ]
            opt_out_records = {
                (item["selector"], item["reason"], item["text"]): item
                for state in text_collision_states
                for item in state["opt_outs"]
            }
            invalid_opt_outs = {
                (item["selector"], item["text"]): item
                for state in text_collision_states
                for item in state["invalid_opt_outs"]
            }
            normal_flow_metric_exclusions = {
                (
                    item["first"]["selector"],
                    item["second"]["selector"],
                    item["reason"],
                ): item
                for state in text_collision_states
                for item in state["normal_flow_metric_exclusions"]
            }
            screenshot = args.output_dir / f"page-{i + 1:02d}.png"
            page.screenshot(path=str(screenshot), full_page=False)
            current_console_errors = console_errors[console_start:]
            current_page_errors = page_errors[page_error_start:]

            page_result = {
                "page": i + 1,
                "title": active.get_attribute("data-title") if active_count == 1 else None,
                "screenshot": str(screenshot),
                "route_ok": route_ok,
                "fragments": {
                    "total": fragment_count,
                    "steps": step_count,
                    "visible": visible_fragments,
                    "rewound": rewound_fragments,
                },
                "source_failures": source_failures,
                "image_failures": image_failures,
                "offscreen_elements": overflow,
                "rhythm_failures": rhythm_failures,
                "canvas_coverage": canvas_coverage,
                "text_collision_states": text_collision_states,
                "text_collisions": text_collisions,
                "intra_element_text_collisions": intra_element_text_collisions,
                "text_collision_opt_outs": list(opt_out_records.values()),
                "invalid_text_collision_opt_outs": list(invalid_opt_outs.values()),
                "normal_flow_text_metric_exclusions": list(
                    normal_flow_metric_exclusions.values()
                ),
                "console_errors": current_console_errors,
                "page_errors": current_page_errors,
            }
            results["pages"].append(page_result)

            if not route_ok:
                failures.append(f"Page {i + 1}: hash route did not activate the expected slide.")
            if visible_fragments != fragment_count:
                failures.append(
                    f"Page {i + 1}: only {visible_fragments}/{fragment_count} fragments became visible."
                )
            if rewound_fragments != 0:
                failures.append(
                    f"Page {i + 1}: {rewound_fragments}/{fragment_count} fragments remained after rewind."
                )
            if source_failures:
                failures.append(f"Page {i + 1}: source modal failures: {source_failures}")
            if image_failures:
                failures.append(f"Page {i + 1}: image failed to load: {image_failures}")
            if overflow:
                failures.append(f"Page {i + 1}: visible content exceeds slide bounds: {overflow[:3]}")
            if rhythm_failures:
                failures.append(
                    f"Page {i + 1}: semantic rhythm differs from declared tokens: {rhythm_failures[:3]}"
                )
            if not canvas_coverage["valid"]:
                failures.append(
                    f"Page {i + 1}: active slide does not cover the deck canvas: "
                    f"deck={canvas_coverage.get('deck')}, slide={canvas_coverage.get('slide')}, "
                    f"deltas={canvas_coverage.get('deltas')}, tolerance={canvas_coverage.get('tolerance')}."
                )
            for invalid in invalid_opt_outs.values():
                failures.append(
                    f"Page {i + 1}: text-collision opt-out requires a local reason: "
                    f"{invalid['text']!r} ({invalid['selector']})."
                )
            for collision in text_collisions:
                if collision.get("collision_scope") == "same-owner-lines":
                    failures.append(
                        f"Page {i + 1} state {collision['state']}: multiline text collision "
                        f"inside {collision['first']['selector']} between lines "
                        f"{collision['lines']['first']} and {collision['lines']['second']}: "
                        f"overlap_y={collision['overlap']['y']}px; "
                        f"clearance_y={collision['clearance']['y']}px; "
                        f"required_gap={collision['safety_gap']}px; "
                        f"font_size={collision['typography']['font_size']}; "
                        f"line_height={collision['typography']['line_height']}."
                    )
                else:
                    failures.append(
                        f"Page {i + 1} state {collision['state']}: text collision between "
                        f"{collision['first']['text']!r} ({collision['first']['selector']}) and "
                        f"{collision['second']['text']!r} ({collision['second']['selector']}): "
                        f"overlap={collision['overlap']['x']}px x {collision['overlap']['y']}px; "
                        f"clearance={collision['clearance']['x']}px x {collision['clearance']['y']}px; "
                        f"required_gap={collision['safety_gap']}px."
                    )
            if current_console_errors:
                failures.append(f"Page {i + 1}: console errors: {current_console_errors}")
            if current_page_errors:
                failures.append(f"Page {i + 1}: page errors: {current_page_errors}")
        browser.close()

    report = args.output_dir / "qa-report.json"
    report.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    if failures:
        print("HTML_DECK_QA_FAILED")
        for failure in failures:
            print(failure)
        print(report)
        return 1
    print("HTML_DECK_QA_OK")
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
