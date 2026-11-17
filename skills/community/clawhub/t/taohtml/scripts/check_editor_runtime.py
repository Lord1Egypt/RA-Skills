#!/usr/bin/env python3
"""Exercise the bundled TaoHtml content editor in Chromium/Chrome."""

from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path

from check_assets import extract_resource_refs, is_absolute_local, is_remote


PNG_PAYLOAD = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAASCAIAAAC1qksFAAAAMklEQVR42mPktk9joCVgYqAx"
    "GPoWsOCSaJkykySDanLSR+Ng1IJRCwbKAsbR0nTALQAAoMMEhd/eaXUAAAAASUVORK5CYII="
)
TEXT_MARKER = "TaoHtml 编辑器浏览器 QA 文本"
EDITOR_IMAGE_URI = (
    "data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20"
    "viewBox='0%200%20160%2090'%3E%3Crect%20width='160'%20height='90'%20"
    "fill='%230b3f66'/%3E%3C/svg%3E"
)
ACTION_FIXTURE = """
<section class="slide" data-title="Editor action fixture" data-taohtml-editor-qa-fixture>
  <div style="position:absolute;inset:120px;display:grid;gap:24px;align-content:center">
    <a data-editor-qa="link" href="#999" onclick="window.__taohtmlQaLinkActions=(window.__taohtmlQaLinkActions||0)+1">可编辑报告链接</a>
    <button type="button" data-editor-qa="button" data-taohtml-edit="text" onclick="window.__taohtmlQaButtonActions=(window.__taohtmlQaButtonActions||0)+1">可编辑行动按钮</button>
    <img class="fragment" data-step="1" data-editor-qa="image" src="__EDITOR_IMAGE_URI__" alt="编辑器图片操作测试" style="width:160px;height:90px;object-fit:cover">
    <button type="button" class="source-btn" data-source="编辑器 QA 来源" data-taohtml-edit-lock>来源</button>
    <button type="button" data-editor-qa="locked" data-taohtml-edit="text" data-taohtml-edit-lock onclick="window.__taohtmlQaLockedActions=(window.__taohtmlQaLockedActions||0)+1">锁定系统按钮</button>
    <div hidden data-editor-qa="hard-boundaries">
      <script type="application/json" data-editor-qa-hard data-taohtml-edit="text">{"fixture":true}</script>
      <style data-editor-qa-hard data-taohtml-edit="text">.taohtml-editor-hard-fixture { display: none; }</style>
      <noscript data-editor-qa-hard data-taohtml-edit="text">noscript</noscript>
      <template data-editor-qa-hard data-taohtml-edit="text">template</template>
      <svg data-editor-qa-hard data-taohtml-edit="text"><text>svg</text></svg>
      <math data-editor-qa-hard data-taohtml-edit="text"><mi>math</mi></math>
      <video data-editor-qa-hard data-taohtml-edit="text"></video>
      <audio data-editor-qa-hard data-taohtml-edit="text"></audio>
      <canvas data-editor-qa-hard data-taohtml-edit="text"></canvas>
      <iframe data-editor-qa-hard data-taohtml-edit="text" title="fixture"></iframe>
      <object data-editor-qa-hard data-taohtml-edit="text"></object>
      <embed data-editor-qa-hard data-taohtml-edit="text">
      <input data-editor-qa-hard data-taohtml-edit="text" value="input">
      <textarea data-editor-qa-hard data-taohtml-edit="text">textarea</textarea>
      <select data-editor-qa-hard data-taohtml-edit="text"><option data-editor-qa-hard data-taohtml-edit="text">option</option></select>
    </div>
  </div>
</section>
""".replace("__EDITOR_IMAGE_URI__", EDITOR_IMAGE_URI)


def portable_input(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    external = sorted(
        ref
        for ref in extract_resource_refs(text)
        if ref
        and not ref.startswith(("data:", "blob:", "#"))
        and (is_remote(ref) or is_absolute_local(ref) or not ref.startswith("--"))
    )
    return not external, external


def build_browser_fixture(source: Path, output: Path) -> Path:
    text = source.read_text(encoding="utf-8")
    marker = "<!-- TAOHTML_SLIDES_END -->"
    if marker not in text:
        raise RuntimeError("Editor QA requires the standard slide boundary marker.")
    fixture = output / "editor-browser-fixture.html"
    fixture.write_text(text.replace(marker, ACTION_FIXTURE + marker, 1), encoding="utf-8")
    return fixture


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run deterministic Chromium QA for the TaoHtml content editor."
    )
    parser.add_argument("html", type=Path, help="Self-contained editor-enabled HTML.")
    parser.add_argument("output_dir", type=Path, help="Directory for JSON, screenshots, and exported HTML.")
    parser.add_argument("--executable-path", type=Path, help="Optional Chrome/Chromium executable.")
    args = parser.parse_args()

    html_path = args.html.resolve()
    if not html_path.is_file():
        raise SystemExit(f"HTML not found: {html_path}")
    is_portable, external = portable_input(html_path)
    if not is_portable:
        raise SystemExit(
            "Editor export/reopen QA requires a self-contained HTML; external assets: "
            + ", ".join(external)
        )

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit("Playwright is required. Install the TaoHtml requirements first.") from exc

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    browser_fixture = build_browser_fixture(html_path, output_dir)
    exported_path = output_dir / "editor-exported.html"
    results: dict[str, object] = {
        "input": str(html_path),
        "browser_fixture": str(browser_fixture),
        "browser": "chromium",
        "checks": {},
        "exported_html": str(exported_path),
    }
    checks: dict[str, object] = results["checks"]  # type: ignore[assignment]
    failures: list[str] = []

    def check(name: str, condition: bool, detail: object | None = None) -> None:
        checks[name] = {"passed": bool(condition), "detail": detail}
        if not condition:
            failures.append(name)

    try:
        with sync_playwright() as playwright:
            launch_options: dict[str, object] = {}
            if args.executable_path:
                executable = args.executable_path.resolve()
                if not executable.is_file():
                    raise RuntimeError(f"Chromium executable not found: {executable}")
                launch_options["executable_path"] = str(executable)
            browser = playwright.chromium.launch(**launch_options)
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            console_errors: list[str] = []
            page_errors: list[str] = []
            page.on(
                "console",
                lambda message: console_errors.append(message.text)
                if message.type == "error"
                else None,
            )
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            page.add_init_script(
                """(() => {
                  const nativeSetTimeout = window.setTimeout.bind(window);
                  window.setTimeout = (callback, delay = 0, ...parameters) =>
                    nativeSetTimeout(callback, delay === 450 ? 5000 : delay, ...parameters);
                })()"""
            )
            page.goto(browser_fixture.as_uri(), wait_until="load")
            page.wait_for_function(
                "() => Boolean(window.TaoHtmlRuntime && window.TaoHtmlEditor)"
            )

            contract = page.evaluate(
                """() => ({
                  runtime: ['getState', 'setEditing', 'setMode', 'nextStep', 'previousStep']
                    .every(name => typeof window.TaoHtmlRuntime?.[name] === 'function'),
                  editor: ['getState', 'enter', 'requestExit', 'undo', 'redo', 'exportHtml', 'getReportIrPatch']
                    .every(name => typeof window.TaoHtmlEditor?.[name] === 'function'),
                  editButton: Boolean(document.querySelector('#editToggle')),
                  textTargets: document.querySelectorAll('[data-taohtml-editor-kind="text"]').length,
                  imageTargets: document.querySelectorAll('[data-taohtml-editor-kind="image"]').length,
                  fragments: document.querySelectorAll('.fragment').length,
                })"""
            )
            check(
                "module_contract",
                contract["runtime"]
                and contract["editor"]
                and contract["editButton"]
                and contract["textTargets"] > 0
                and contract["imageTargets"] > 0
                and contract["fragments"] > 0,
                contract,
            )

            page.locator("#moreToggle").click()
            page.locator("#editToggle").click()
            page.wait_for_function("() => window.TaoHtmlEditor.getState().active")
            initial_runtime = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            check("runtime_editing_flag", initial_runtime["editing"] is True, initial_runtime)

            locked_state = page.evaluate(
                """() => ({
                  page: document.querySelector('#pageIndicator')?.getAttribute('contenteditable'),
                  menu: document.querySelector('#moreMenu')?.getAttribute('contenteditable'),
                  source: document.querySelector('.source-btn')?.getAttribute('contenteditable') ?? null,
                  navLocked: document.querySelector('.nav')?.hasAttribute('data-taohtml-edit-lock'),
                  moreLocked: document.querySelector('.more')?.hasAttribute('data-taohtml-edit-lock'),
                  pageLocked: document.querySelector('#pageIndicator')?.hasAttribute('data-taohtml-edit-lock'),
                  sourceLocked: document.querySelector('.source-btn')?.hasAttribute('data-taohtml-edit-lock'),
                  lockedTargets: document.querySelectorAll('[data-taohtml-edit-lock] [contenteditable="true"]').length,
                })"""
            )
            check(
                "system_controls_locked",
                locked_state["page"] is None
                and locked_state["menu"] is None
                and locked_state["source"] is None
                and locked_state["navLocked"]
                and locked_state["moreLocked"]
                and locked_state["pageLocked"]
                and locked_state["sourceLocked"]
                and locked_state["lockedTargets"] == 0,
                locked_state,
            )

            page.locator(".slide:has(.fragment)").first.evaluate(
                "element => window.TaoHtmlRuntime.showPage([...document.querySelectorAll('.slide')].indexOf(element))"
            )
            state_before_pause = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.keyboard.press("ArrowRight")
            page.locator(".slide.active").click(position={"x": 8, "y": 8})
            state_after_pause = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            fragment_pause = page.locator(".slide.active .fragment").first.evaluate(
                """element => ({
                  opacity: getComputedStyle(element).opacity,
                  transitionDuration: getComputedStyle(element).transitionDuration,
                  animationPlayState: getComputedStyle(element).animationPlayState,
                })"""
            )
            check(
                "navigation_and_motion_paused",
                state_before_pause == state_after_pause
                and fragment_pause["opacity"] == "1"
                and fragment_pause["transitionDuration"] == "0s"
                and fragment_pause["animationPlayState"] == "paused",
                {"before": state_before_pause, "after": state_after_pause, "fragment": fragment_pause},
            )
            page.locator("#next").click()
            after_page_button = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            page.locator("#prev").click()
            after_page_return = page.evaluate("() => window.TaoHtmlRuntime.getState()")
            check(
                "page_buttons_available_during_edit",
                after_page_button["index"] == min(
                    state_before_pause["index"] + 1,
                    len(state_before_pause["stages"]) - 1,
                )
                and after_page_return["index"] == state_before_pause["index"]
                and after_page_return["stages"] == state_before_pause["stages"],
                {"next": after_page_button, "return": after_page_return},
            )

            action_fixture = page.locator('[data-taohtml-editor-qa-fixture]')
            action_fixture.evaluate(
                "element => window.TaoHtmlRuntime.showPage([...document.querySelectorAll('.slide')].indexOf(element))"
            )
            action_contract = page.evaluate(
                """() => ({
                  link: document.querySelector('[data-editor-qa="link"]')?.getAttribute('contenteditable'),
                  button: document.querySelector('[data-editor-qa="button"]')?.getAttribute('contenteditable'),
                  locked: document.querySelector('[data-editor-qa="locked"]')?.getAttribute('contenteditable'),
                  lockedTarget: document.querySelector('[data-editor-qa="locked"]')?.hasAttribute('data-taohtml-editor-kind'),
                  hardBoundaries: [...document.querySelectorAll('[data-editor-qa-hard]')].map(element => ({
                    tag: element.tagName,
                    contenteditable: element.getAttribute('contenteditable'),
                    target: element.hasAttribute('data-taohtml-editor-kind'),
                  })),
                })"""
            )
            check(
                "report_actions_editable_and_hard_boundaries_rejected",
                action_contract["link"] == "true"
                and action_contract["button"] == "true"
                and action_contract["locked"] is None
                and not action_contract["lockedTarget"]
                and len(action_contract["hardBoundaries"]) == 16
                and all(
                    item["contenteditable"] is None and not item["target"]
                    for item in action_contract["hardBoundaries"]
                ),
                action_contract,
            )

            action_hash = page.evaluate("() => location.hash")
            page.locator('[data-editor-qa="link"]').click()
            page.locator('[data-editor-qa="button"]').click()
            page.locator('[data-editor-qa="locked"]').click()
            action_results = page.evaluate(
                """expectedHash => ({
                  link: window.__taohtmlQaLinkActions || 0,
                  button: window.__taohtmlQaButtonActions || 0,
                  locked: window.__taohtmlQaLockedActions || 0,
                  hashUnchanged: location.hash === expectedHash,
                })""",
                action_hash,
            )
            source_target = page.locator('.source-btn').first
            source_target.evaluate(
                "element => window.TaoHtmlRuntime.showPage([...document.querySelectorAll('.slide')].indexOf(element.closest('.slide')))"
            )
            source_target.click()
            source_suppressed = page.evaluate(
                "() => !document.querySelector('#modal')?.classList.contains('open')"
            )
            check(
                "report_and_source_actions_suppressed_during_edit",
                action_results["link"] == 0
                and action_results["button"] == 0
                and action_results["locked"] == 0
                and action_results["hashUnchanged"]
                and source_suppressed,
                {"actions": action_results, "source_suppressed": source_suppressed},
            )

            action_fixture.evaluate(
                "element => window.TaoHtmlRuntime.showPage([...document.querySelectorAll('.slide')].indexOf(element))"
            )
            action_original = page.evaluate(
                """() => ({
                  link: document.querySelector('[data-editor-qa="link"]').innerHTML,
                  button: document.querySelector('[data-editor-qa="button"]').innerHTML,
                })"""
            )
            for selector, marker in (
                ('[data-editor-qa="link"]', "已修改报告链接"),
                ('[data-editor-qa="button"]', "已修改行动按钮"),
            ):
                page.locator(selector).evaluate(
                    """(element, value) => {
                      element.focus();
                      element.textContent = value;
                      element.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertText'}));
                    }""",
                    marker,
                )
            page.evaluate("() => window.TaoHtmlEditor.requestExit()")
            page.locator('[data-action="discard"]').click()
            discarded = page.evaluate(
                """() => ({
                  link: document.querySelector('[data-editor-qa="link"]').innerHTML,
                  button: document.querySelector('[data-editor-qa="button"]').innerHTML,
                  editor: window.TaoHtmlEditor.getState(),
                })"""
            )
            check(
                "dirty_exit_discard",
                discarded["link"] == action_original["link"]
                and discarded["button"] == action_original["button"]
                and not discarded["editor"]["active"]
                and not discarded["editor"]["dirty"],
                discarded,
            )
            page.evaluate("() => window.TaoHtmlEditor.enter()")
            report_ir_edit = page.evaluate(
                """() => {
                  const target = document.querySelector(
                    '[data-ir-edit-kind="text"][data-ir-edit-key]'
                  );
                  if (!target) return {available: false, patch: null};
                  target.focus();
                  target.textContent = `${target.textContent || ''} `;
                  target.dispatchEvent(new InputEvent('input', {
                    bubbles: true,
                    inputType: 'insertText',
                    data: ' ',
                  }));
                  return {
                    available: true,
                    key: target.dataset.irEditKey,
                    patch: window.TaoHtmlEditor.getReportIrPatch(),
                  };
                }"""
            )
            check(
                "report_ir_patch_preview",
                not report_ir_edit["available"]
                or (
                    report_ir_edit["patch"] is not None
                    and report_ir_edit["patch"]["operation_count"] >= 1
                    and any(
                        operation["target"]["key"] == report_ir_edit["key"]
                        for operation in report_ir_edit["patch"]["operations"]
                    )
                ),
                report_ir_edit,
            )

            text_target = page.locator(
                '.slide.active [data-taohtml-editor-kind="text"]'
            ).first
            image_target = page.locator(
                '.slide.active [data-taohtml-editor-kind="image"]'
            ).first
            if image_target.count() == 0:
                image_target = page.locator('[data-taohtml-editor-kind="image"]').first
                image_target.evaluate(
                    "element => window.TaoHtmlRuntime.showPage([...document.querySelectorAll('.slide')].indexOf(element.closest('.slide')))"
                )
                text_target = page.locator(
                    '.slide.active [data-taohtml-editor-kind="text"]'
                ).first

            original_text = text_target.evaluate("element => element.innerHTML")
            original_image = image_target.evaluate(
                "element => ({state: element.getAttribute('src'), position: element.style.objectPosition, rect: element.getBoundingClientRect().toJSON()})"
            )

            fast_text_marker = TEXT_MARKER + " / fast image"
            text_target.evaluate(
                """(element, marker) => {
                  element.focus();
                  element.textContent = marker;
                  element.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertText', data: marker}));
                }""",
                fast_text_marker,
            )
            with page.expect_file_chooser() as fast_chooser_info:
                image_target.click()
            fast_chooser_info.value.set_files(
                {
                    "name": "taohtml-editor-fast-qa.png",
                    "mimeType": "image/png",
                    "buffer": PNG_PAYLOAD,
                }
            )
            page.wait_for_function(
                """() => document.querySelector(
                  '.slide.active [data-taohtml-editor-kind="image"]'
                )?.getAttribute('src')?.startsWith('data:image/png')"""
            )
            page.keyboard.press("Control+z")
            fast_first_undo = {
                "text": text_target.evaluate("element => element.textContent"),
                "src": image_target.get_attribute("src"),
            }
            page.keyboard.press("Control+z")
            fast_second_undo = {
                "text": text_target.evaluate("element => element.innerHTML"),
                "src": image_target.get_attribute("src"),
            }
            page.keyboard.press("Control+Shift+z")
            fast_first_redo = {
                "text": text_target.evaluate("element => element.textContent"),
                "src": image_target.get_attribute("src"),
            }
            page.keyboard.press("Control+Shift+z")
            fast_second_redo = {
                "text": text_target.evaluate("element => element.textContent"),
                "src": image_target.get_attribute("src"),
            }
            check(
                "fast_text_then_image_history_order",
                fast_first_undo["text"] == fast_text_marker
                and fast_first_undo["src"] == original_image["state"]
                and fast_second_undo["text"] == original_text
                and fast_second_undo["src"] == original_image["state"]
                and fast_first_redo["text"] == fast_text_marker
                and fast_first_redo["src"] == original_image["state"]
                and fast_second_redo["text"] == fast_text_marker
                and str(fast_second_redo["src"]).startswith("data:image/png"),
                {
                    "first_undo": fast_first_undo,
                    "second_undo": fast_second_undo,
                    "first_redo": fast_first_redo,
                    "second_redo": fast_second_redo,
                },
            )
            page.keyboard.press("Control+z")
            page.keyboard.press("Control+z")

            fast_crop_marker = TEXT_MARKER + " / fast crop"
            text_target.evaluate(
                """(element, marker) => {
                  element.focus();
                  element.textContent = marker;
                  element.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertText', data: marker}));
                }""",
                fast_crop_marker,
            )
            fast_crop_box = image_target.bounding_box()
            if fast_crop_box is None:
                raise RuntimeError("Editable image has no rendered bounding box.")
            page.mouse.move(
                fast_crop_box["x"] + fast_crop_box["width"] * 0.5,
                fast_crop_box["y"] + fast_crop_box["height"] * 0.5,
            )
            page.mouse.down()
            page.mouse.move(
                fast_crop_box["x"] + fast_crop_box["width"] * 0.75,
                fast_crop_box["y"] + fast_crop_box["height"] * 0.3,
            )
            page.mouse.up()
            fast_crop_position = image_target.evaluate("element => element.style.objectPosition")
            page.keyboard.press("Control+z")
            fast_crop_first_undo = {
                "text": text_target.evaluate("element => element.textContent"),
                "position": image_target.evaluate("element => element.style.objectPosition"),
            }
            page.keyboard.press("Control+z")
            fast_crop_second_undo = {
                "text": text_target.evaluate("element => element.innerHTML"),
                "position": image_target.evaluate("element => element.style.objectPosition"),
            }
            page.keyboard.press("Control+Shift+z")
            fast_crop_first_redo = {
                "text": text_target.evaluate("element => element.textContent"),
                "position": image_target.evaluate("element => element.style.objectPosition"),
            }
            page.keyboard.press("Control+Shift+z")
            fast_crop_second_redo = {
                "text": text_target.evaluate("element => element.textContent"),
                "position": image_target.evaluate("element => element.style.objectPosition"),
            }
            check(
                "fast_text_then_crop_history_order",
                bool(fast_crop_position)
                and fast_crop_first_undo["text"] == fast_crop_marker
                and fast_crop_first_undo["position"] == original_image["position"]
                and fast_crop_second_undo["text"] == original_text
                and fast_crop_second_undo["position"] == original_image["position"]
                and fast_crop_first_redo["text"] == fast_crop_marker
                and fast_crop_first_redo["position"] == original_image["position"]
                and fast_crop_second_redo["text"] == fast_crop_marker
                and fast_crop_second_redo["position"] == fast_crop_position,
                {
                    "first_undo": fast_crop_first_undo,
                    "second_undo": fast_crop_second_undo,
                    "first_redo": fast_crop_first_redo,
                    "second_redo": fast_crop_second_redo,
                },
            )
            page.keyboard.press("Control+z")
            page.keyboard.press("Control+z")

            text_target.evaluate(
                """(element, marker) => {
                  element.focus();
                  element.textContent = marker;
                  element.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertText', data: marker}));
                }""",
                TEXT_MARKER,
            )
            page.wait_for_timeout(520)

            with page.expect_file_chooser() as chooser_info:
                image_target.click()
            chooser_info.value.set_files(
                {
                    "name": "taohtml-editor-qa.png",
                    "mimeType": "image/png",
                    "buffer": PNG_PAYLOAD,
                }
            )
            page.wait_for_function(
                """() => document.querySelector(
                  '.slide.active [data-taohtml-editor-kind="image"]'
                )?.getAttribute('src')?.startsWith('data:image/png')"""
            )
            replaced_rect = image_target.evaluate(
                "element => element.getBoundingClientRect().toJSON()"
            )
            frame_preserved = (
                abs(original_image["rect"]["width"] - replaced_rect["width"]) <= 0.75
                and abs(original_image["rect"]["height"] - replaced_rect["height"]) <= 0.75
            )

            box = image_target.bounding_box()
            if box is None:
                raise RuntimeError("Editable image has no rendered bounding box.")
            page.mouse.move(box["x"] + box["width"] * 0.5, box["y"] + box["height"] * 0.5)
            page.mouse.down()
            page.mouse.move(box["x"] + box["width"] * 0.82, box["y"] + box["height"] * 0.24)
            page.mouse.up()
            crop_position = image_target.evaluate("element => element.style.objectPosition")
            changed = {
                "text": text_target.evaluate("element => element.textContent"),
                "src": image_target.get_attribute("src"),
                "position": crop_position,
                "frame": replaced_rect,
            }
            check(
                "continuous_text_image_crop_edit",
                changed["text"] == TEXT_MARKER
                and str(changed["src"]).startswith("data:image/png")
                and bool(crop_position)
                and frame_preserved,
                changed,
            )

            for _ in range(3):
                page.keyboard.press("Control+z")
            undone = {
                "text": text_target.evaluate("element => element.innerHTML"),
                "src": image_target.get_attribute("src"),
                "position": image_target.evaluate("element => element.style.objectPosition"),
            }
            for _ in range(3):
                page.keyboard.press("Control+Shift+z")
            redone = {
                "text": text_target.evaluate("element => element.textContent"),
                "src": image_target.get_attribute("src"),
                "position": image_target.evaluate("element => element.style.objectPosition"),
            }
            check(
                "unified_undo_redo",
                undone["text"] == original_text
                and undone["src"] == original_image["state"]
                and undone["position"] == original_image["position"]
                and redone["text"] == TEXT_MARKER
                and str(redone["src"]).startswith("data:image/png")
                and redone["position"] == crop_position,
                {"undone": undone, "redone": redone},
            )

            page.evaluate("() => window.TaoHtmlEditor.requestExit()")
            dialog_visible = page.locator(
                '.taohtml-editor-dialog:not([hidden])'
            ).count() == 1
            page.locator('[data-action="continue"]').click()
            continued = page.evaluate("() => window.TaoHtmlEditor.getState()")
            check(
                "dirty_exit_continue",
                dialog_visible and continued["active"] and continued["dirty"],
                {"dialog": dialog_visible, "state": continued},
            )

            page.reload(wait_until="load")
            page.wait_for_function("() => Boolean(window.TaoHtmlEditor)")
            restored = page.evaluate(
                """marker => ({
                  editor: window.TaoHtmlEditor.getState(),
                  text: [...document.querySelectorAll('[data-taohtml-editor-kind="text"]')]
                    .some(element => element.textContent === marker),
                  image: [...document.querySelectorAll('[data-taohtml-editor-kind="image"]')]
                    .some(element => element.getAttribute('src')?.startsWith('data:image/png')),
                  crop: [...document.querySelectorAll('[data-taohtml-editor-kind="image"]')]
                    .some(element => element.style.objectPosition),
                })""",
                TEXT_MARKER,
            )
            check(
                "refresh_recovery",
                restored["editor"]["dirty"]
                and not restored["editor"]["active"]
                and restored["text"]
                and restored["image"]
                and restored["crop"],
                restored,
            )

            page.evaluate("() => window.TaoHtmlEditor.enter()")
            report_ir_image = page.locator(
                '[data-ir-edit-kind="image"][data-ir-edit-key]'
            ).first
            report_ir_image_detail: dict[str, object] = {"available": False}
            if report_ir_image.count() > 0:
                report_ir_image.evaluate(
                    """element => window.TaoHtmlRuntime.showPage(
                      [...document.querySelectorAll('.slide')].indexOf(element.closest('.slide'))
                    )"""
                )
                with page.expect_file_chooser() as report_ir_chooser_info:
                    report_ir_image.click()
                report_ir_chooser_info.value.set_files(
                    {
                        "name": "taohtml-report-ir-editor-qa.png",
                        "mimeType": "image/png",
                        "buffer": PNG_PAYLOAD,
                    }
                )
                report_ir_key = report_ir_image.get_attribute("data-ir-edit-key")
                page.wait_for_function(
                    """key => document.querySelector(
                      `[data-ir-edit-key="${CSS.escape(key)}"]`
                    )?.getAttribute('src')?.startsWith('data:image/png')""",
                    arg=report_ir_key,
                )
                report_ir_image.evaluate(
                    "element => { element.style.objectPosition = '61.00% 39.00%'; }"
                )
                report_ir_patch = page.evaluate(
                    "() => window.TaoHtmlEditor.getReportIrPatch()"
                )
                report_ir_image_detail = {
                    "available": True,
                    "key": report_ir_key,
                    "patch": report_ir_patch,
                }
                check(
                    "report_ir_image_patch_preview",
                    report_ir_patch is not None
                    and any(
                        operation["op"] == "replace_image"
                        and operation["target"]["key"] == report_ir_key
                        for operation in report_ir_patch["operations"]
                    ),
                    report_ir_image_detail,
                )
            else:
                check("report_ir_image_patch_preview", True, report_ir_image_detail)
            page.evaluate("() => window.TaoHtmlEditor.requestExit()")
            with page.expect_download() as download_info:
                page.locator('[data-action="export"]').click()
            download_info.value.save_as(exported_path)
            page.wait_for_function(
                "() => !window.TaoHtmlEditor.getState().active && !window.TaoHtmlEditor.getState().dirty"
            )
            post_export = page.evaluate(
                """() => ({
                  editor: window.TaoHtmlEditor.getState(),
                  sessionRecords: Object.keys(sessionStorage)
                    .filter(key => key.startsWith('taohtml:editor:')).length,
                })"""
            )
            check(
                "export_clears_temporary_state",
                exported_path.is_file()
                and not post_export["editor"]["dirty"]
                and post_export["sessionRecords"] == 0,
                post_export,
            )

            exported_page = browser.new_page(viewport={"width": 1440, "height": 900})
            exported_errors: list[str] = []
            exported_page.on("pageerror", lambda error: exported_errors.append(str(error)))
            exported_page.goto(exported_path.as_uri(), wait_until="load")
            exported_page.wait_for_function(
                "() => Boolean(window.TaoHtmlRuntime && window.TaoHtmlEditor)"
            )
            reopened = exported_page.evaluate(
                """marker => {
                  const runtime = window.TaoHtmlRuntime;
                  const editor = window.TaoHtmlEditor;
                  const text = [...document.querySelectorAll('[data-taohtml-editor-kind="text"]')]
                    .some(element => element.textContent === marker);
                  const image = document.querySelector('[data-editor-qa="image"]');
                  runtime.setMode('reading');
                  const reading = runtime.getState();
                  runtime.setMode('presentation');
                  const presentation = runtime.getState();
                  const imageSlide = image?.closest('.slide');
                  const imageSlideIndex = imageSlide
                    ? [...document.querySelectorAll('.slide')].indexOf(imageSlide)
                    : -1;
                  if (imageSlideIndex >= 0) runtime.showPage(imageSlideIndex);
                  const imageFragment = image?.closest('.fragment');
                  const beforeModifiedReveal = runtime.getState();
                  runtime.nextStep();
                  const afterModifiedReveal = runtime.getState();
                  const fragment = imageFragment || document.querySelector('.slide.active .fragment');
                  const transitionDuration = fragment ? getComputedStyle(fragment).transitionDuration : null;
                  return {
                    text,
                    image: Boolean(image),
                    crop: image?.style.objectPosition || '',
                    editor: editor.getState(),
                    reading,
                    presentation,
                    modifiedMotion: {
                      before: beforeModifiedReveal,
                      after: afterModifiedReveal,
                      opacity: fragment ? getComputedStyle(fragment).opacity : null,
                    },
                    transitionDuration,
                  };
                }""",
                TEXT_MARKER,
            )
            check(
                "export_reopen_runtime_content_motion",
                reopened["text"]
                and reopened["image"]
                and reopened["crop"] == crop_position
                and not reopened["editor"]["active"]
                and not reopened["editor"]["dirty"]
                and reopened["reading"]["mode"] == "reading"
                and reopened["presentation"]["mode"] == "presentation"
                and reopened["modifiedMotion"]["after"]["stages"]
                != reopened["modifiedMotion"]["before"]["stages"]
                and reopened["modifiedMotion"]["opacity"] == "1"
                and reopened["transitionDuration"] != "0s"
                and not exported_errors,
                {**reopened, "page_errors": exported_errors},
            )
            exported_page.screenshot(path=str(output_dir / "editor-exported.png"), full_page=True)
            page.screenshot(path=str(output_dir / "editor-source-after-export.png"), full_page=True)
            check(
                "console_clean",
                not console_errors and not page_errors,
                {"console_errors": console_errors, "page_errors": page_errors},
            )
            browser.close()
    except Exception as exc:  # pragma: no cover - preserves browser evidence on failure
        failures.append("qa_exception")
        checks["qa_exception"] = {"passed": False, "detail": f"{type(exc).__name__}: {exc}"}

    results["passed"] = not failures
    results["failures"] = failures
    report_path = output_dir / "editor-qa.json"
    report_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(report_path)
    if failures:
        print("EDITOR_QA_FAILED " + ", ".join(failures), file=sys.stderr)
        return 1
    print("EDITOR_QA_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
