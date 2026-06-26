import time
from dataclasses import asdict, is_dataclass
from typing import Optional

from action.browser_backend import BrowserBackend
from action.desktop_backend import DesktopBackend
from action.keyboard import KeyboardController
from action.mouse import MouseController
from action.verifier import ActionVerifier
from app.config import AppConfig
from app.logger import setup_logger
from core.context import build_runtime_context
from core.failure_store import FailureStore
from core.planner import Planner
from core.session_state import SessionStateStore
from core.types import ActionType, ElementType, ExecutionResult
from nlu.parser import CommandParser
from perception.vision_engine import VisionEngine
from strategy.fallback import relax_text_match
from strategy.mode_switch import ModeSwitch
from strategy.retry import bounded_candidates


class Orchestrator:
    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig()
        self.logger = setup_logger(debug=self.config.runtime.debug)
        self.context = build_runtime_context(self.config.runtime.mode)
        self.parser = CommandParser()
        self.planner = Planner()
        self.vision = VisionEngine(self.config.vision)
        self.mouse = MouseController(self.config.input)
        self.keyboard = KeyboardController(self.config.input)
        self.verifier = ActionVerifier(self.vision.capture, self.vision.ocr)
        self.browser = BrowserBackend(self.config, self.mouse, self.keyboard)
        self.desktop = DesktopBackend()
        self.mode_switch = ModeSwitch()
        self.failure_store = FailureStore()
        self.session_state = SessionStateStore()

    def execute(self, command: str):
        intent = self.parser.parse(command)
        steps = self.planner.plan(intent)
        self._refresh_runtime_state()
        self._apply_recent_target_from_state()

        results = []
        for step in steps:
            results.append(self._run_step(step, command=command, intent=intent))
        return {
            "command": command,
            "intent": intent,
            "steps": steps,
            "results": results,
            "success": all(r.success for r in results),
            "runtime": {
                "active_window": self.context.active_window,
                "backend_mode": self.context.backend_mode.value,
                "expected_app_keywords": self.context.safety_flags.get("expected_app_keywords", []),
            },
        }

    def _apply_recent_target_from_state(self):
        recent = self.session_state.get_recent(ttl_seconds=180)
        if not recent:
            return
        kws = recent.get("expected_app_keywords") or []
        if kws and not self.context.safety_flags.get("expected_app_keywords"):
            self.context.safety_flags["expected_app_keywords"] = kws
        if recent.get("last_window_title") and not self.context.active_window:
            self.context.active_window = recent.get("last_window_title")

    def _persist_expected_target(self, app_name: str, keywords, window_title: Optional[str], resolved_path: str, resolved_source: str):
        self.session_state.update(
            last_target_app=app_name,
            expected_app_keywords=keywords or [],
            last_window_title=window_title or "",
            resolved_path=resolved_path,
            resolved_source=resolved_source,
        )

    def _refresh_runtime_state(self):
        active = self.browser.window_manager.get_active_window()
        if active:
            self.context.active_window = active.title

        browser_window = self.browser.get_browser_window()
        if browser_window and not self.context.active_window:
            self.context.active_window = browser_window.title

        backend = self.mode_switch.choose_backend(
            has_dom=self.browser.dom.is_available(),
            window_available=bool(browser_window) or bool(self.context.safety_flags.get("window_manager_available")),
            target_kind="browser",
        )
        self.context.backend_mode = backend

    def _run_step(self, step, command: str, intent):
        self.logger.info("执行步骤 | %s | %s", step.id, step.description)
        before = self.verifier.snapshot_state()
        try:
            if step.action == ActionType.NAVIGATE:
                result = self._navigate(step.params["url"], before)
            elif step.action == ActionType.FOCUS_INPUT:
                result = self._focus_target(step.params, before)
            elif step.action == ActionType.TYPE:
                result = self._type_text(step.params, before)
            elif step.action == ActionType.CLICK:
                result = self._click_target(step.params, before)
            elif step.action == ActionType.WAIT:
                time.sleep(float(step.params.get("seconds", 1)))
                after = self.verifier.snapshot_state()
                result = ExecutionResult(True, action="wait", before_state=before, after_state=after)
            elif step.action == ActionType.SCREENSHOT:
                after = self.verifier.snapshot_state()
                result = ExecutionResult(True, action="screenshot", before_state=before, after_state=after, evidence=after)
            elif step.action == ActionType.OPEN_APP:
                result = self._open_app(step.params["app_name"], before)
            else:
                result = ExecutionResult(False, action=step.action.value, error="unsupported step", before_state=before)
        except Exception as exc:
            self.logger.exception("步骤失败")
            result = ExecutionResult(False, action=step.action.value, error=str(exc), before_state=before)

        if not result.success:
            failure_path = self._record_failure(command, intent, step, result)
            result.evidence["failure_record"] = failure_path

        self.context.history.append({"step": step.description, "success": result.success, "error": result.error})
        return result

    def _record_failure(self, command: str, intent, step, result: ExecutionResult) -> str:
        payload = {
            "command": command,
            "intent": self._safe(intent),
            "step": self._safe(step),
            "result": self._safe(result),
            "runtime": {
                "active_window": self.context.active_window,
                "backend_mode": self.context.backend_mode.value,
                "last_target": self._safe(self.context.last_target),
                "history_tail": self.context.history[-5:],
            },
        }
        return self.failure_store.record(payload)

    def _safe(self, obj):
        if obj is None:
            return None
        if is_dataclass(obj):
            return asdict(obj)
        if isinstance(obj, dict):
            return {k: self._safe(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._safe(v) for v in obj]
        return obj

    def _is_browser_target(self, params) -> bool:
        if self.context.safety_flags.get("expected_app_keywords"):
            return False
        if self.context.backend_mode.value in ("browser", "hybrid"):
            return True
        app_name = params.get("app_name") if isinstance(params, dict) else None
        if app_name and any(word in str(app_name).lower() for word in ["chrome", "edge", "firefox", "browser"]):
            return True
        return False

    def _dom_evidence(self, dom_result, action_name: str, target_text: Optional[str], before, after, extra=None):
        evidence = {
            "backend": "dom",
            "detail": dom_result.detail,
            "selector": getattr(dom_result, "selector", None),
            "dom_extra": getattr(dom_result, "extra", None),
        }
        if extra:
            evidence.update(extra)
        return ExecutionResult(True, action=action_name, target=target_text, before_state=before, after_state=after, evidence=evidence)

    def _navigate(self, url: str, before):
        cmd = self.browser.navigate(url)
        time.sleep(2.0)
        after = self.verifier.snapshot_state()
        return ExecutionResult(cmd.success, action="navigate", target=url, before_state=before, after_state=after, evidence={"url": url, "detail": cmd.detail, "backend": self.context.backend_mode.value})

    def _locate_target(self, params, default_type: str):
        target_type = ElementType(params.get("target_type", default_type))
        target_text = params.get("target_text")
        results = []
        for text_variant in relax_text_match(target_text):
            candidates = self.vision.locate_candidates(
                target_text=text_variant,
                target_type=target_type,
                position_hint=params.get("position_hint"),
            )
            if candidates:
                results.extend(candidates)
                break
        return results

    def _browser_fullscreen_like(self):
        active = self.browser.window_manager.get_active_window()
        if not active:
            return False
        browserish = any(k in active.title.lower() for k in ["edge", "chrome", "firefox", "browser"])
        large = active.width >= self.context.screen_size[0] - 8 and active.height >= self.context.screen_size[1] - 8
        return browserish and large

    def _focus_expected_app(self):
        keywords = self.context.safety_flags.get("expected_app_keywords") or []
        if not keywords:
            return False, None, "none"

        wm = self.browser.window_manager
        if wm.activate_window(keywords):
            time.sleep(0.25)
            win = wm.find_window(keywords) or wm.get_active_window()
            if win:
                self.context.active_window = win.title
                return True, win, "direct"

        if self._browser_fullscreen_like():
            self.keyboard.hotkey("f11")
            time.sleep(0.8)
            if wm.activate_window(keywords):
                time.sleep(0.25)
                win = wm.find_window(keywords) or wm.get_active_window()
                if win:
                    self.context.active_window = win.title
                    return True, win, "after_exit_fullscreen"

        win = wm.wait_for_window(keywords, timeout=2.0)
        if win:
            wm.activate_window(keywords)
            time.sleep(0.25)
            self.context.active_window = win.title
            return True, win, "waited"

        return False, None, "not_found"

    def _focus_target(self, params, before):
        expected_keywords = self.context.safety_flags.get("expected_app_keywords") or []
        if expected_keywords and not params.get("target_text"):
            ok, win, source = self._focus_expected_app()
            if ok and win:
                x = int(win.left + max(80, win.width * 0.5))
                y = int(win.top + max(100, win.height * 0.45))
                self.mouse.click_point(x, y, safe=True)
                after = self.verifier.snapshot_state(region=(max(0, x - 150), max(0, y - 40), 300, 80))
                return ExecutionResult(True, action="focus_input", target=win.title, before_state=before, after_state=after, evidence={"backend": "window", "point": (x, y), "window": win.title, "window_focus_source": source})
            return ExecutionResult(False, action="focus_input", error="expected app window not found/activated", before_state=before, evidence={"backend": "window", "expected_app_keywords": expected_keywords, "window_focus_source": source})

        if self._is_browser_target(params) and self.browser.dom.is_available():
            dom_result = self.browser.dom.focus_input(target_text=params.get("target_text"), url=params.get("url"))
            if dom_result.success:
                after = self.verifier.snapshot_state()
                return self._dom_evidence(dom_result, "focus_input", params.get("target_text"), before, after)

        candidates = self._locate_target(params, "input")
        if not candidates:
            return ExecutionResult(False, action="focus_input", error="input not found", before_state=before, evidence={"fallback": "vision", "dom_attempted": self._is_browser_target(params) and self.browser.dom.is_available()})

        for attempt, target in bounded_candidates(candidates, self.config.runtime.max_retries):
            point = self.mouse.click_bbox(target.bbox, safe=True)
            after = self.verifier.snapshot_state(region=self.verifier.focus_region(target.bbox))
            self.context.last_target = target
            if self.verifier.state_changed(before, after):
                return ExecutionResult(True, action="focus_input", target=target.text or params.get("target_text"), before_state=before, after_state=after, evidence={"backend": "vision", "point": point, "bbox": target.bbox, "source": target.source}, attempts=attempt)
        return ExecutionResult(False, action="focus_input", error="focus verification failed", before_state=before, attempts=min(len(candidates), self.config.runtime.max_retries), evidence={"backend": "vision"})

    def _type_text(self, params, before):
        text = params["text"]

        if not self.context.safety_flags.get("expected_app_keywords"):
            self._apply_recent_target_from_state()

        focused_source = "none"
        if self.context.safety_flags.get("expected_app_keywords"):
            ok, _win, focused_source = self._focus_expected_app()
            if not ok:
                return ExecutionResult(False, action="type", before_state=before, error="expected app window not found/activated", evidence={"backend": "keyboard", "expected_app_keywords": self.context.safety_flags.get("expected_app_keywords", []), "window_focus_source": focused_source})

        if self._is_browser_target(params) and self.browser.dom.is_available():
            dom_result = self.browser.dom.type_into(text=text, target_text=params.get("target_text"), role=params.get("target_type"), url=params.get("url"))
            if dom_result.success:
                after = self.verifier.snapshot_state()
                return self._dom_evidence(dom_result, "type", params.get("target_text"), before, after, extra={"text_length": len(text), "text_via": "dom"})

        self.keyboard.type_text(text)
        after = self.verifier.snapshot_state()
        changed = self.verifier.state_changed(before, after)

        readback = ""
        readback_region = None
        if self.context.last_target:
            readback_region = self.verifier.focus_region(self.context.last_target.bbox, padding=24)
            try:
                readback = self.verifier.read_region_text(readback_region)
            except Exception:
                readback = ""
        elif self.context.safety_flags.get("expected_app_keywords"):
            active = self.browser.window_manager.get_active_window()
            if active:
                x = max(0, int(active.left + active.width * 0.15))
                y = max(0, int(active.top + active.height * 0.18))
                w = max(300, int(active.width * 0.7))
                h = max(120, int(active.height * 0.5))
                readback_region = (x, y, w, h)
                try:
                    readback = self.verifier.read_region_text(readback_region)
                except Exception:
                    readback = ""

        compact_text = "".join(str(text).split())
        compact_readback = "".join(str(readback).split())
        verify_token = compact_text[: min(8, max(2, len(compact_text)))]
        text_verified = bool(compact_readback and verify_token and verify_token in compact_readback)

        return ExecutionResult(changed or bool(text), action="type", before_state=before, after_state=after, evidence={
            "backend": "keyboard",
            "text_length": len(text),
            "changed": changed,
            "readback": readback,
            "readback_region": readback_region,
            "text_verified": text_verified,
            "verify_token": verify_token,
            "expected_window": self.context.active_window,
            "window_focus_source": focused_source,
        })

    def _click_target(self, params, before):
        if self._is_browser_target(params) and self.browser.dom.is_available():
            dom_result = self.browser.dom.click(target_text=params.get("target_text"), role=params.get("target_type"), url=params.get("url"))
            if dom_result.success:
                after = self.verifier.snapshot_state()
                return self._dom_evidence(dom_result, "click", params.get("target_text"), before, after)

        candidates = self._locate_target(params, "button")
        if not candidates:
            return ExecutionResult(False, action="click", error="target not found", before_state=before, evidence={"fallback": "vision", "dom_attempted": self._is_browser_target(params) and self.browser.dom.is_available()})

        for attempt, target in bounded_candidates(candidates, self.config.runtime.max_retries):
            pixel_before = None
            try:
                pixel_before = self.verifier.read_pixel(target.center)
            except Exception:
                pixel_before = None

            point = self.mouse.click_bbox(target.bbox, safe=True)
            after = self.verifier.snapshot_state(region=self.verifier.focus_region(target.bbox))
            self.context.last_target = target
            state_ok = self.verifier.state_changed(before, after)
            pixel_ok = self.verifier.pixel_changed(target.center, pixel_before) if pixel_before else False
            if state_ok or pixel_ok:
                return ExecutionResult(True, action="click", target=target.text or params.get("target_text"), before_state=before, after_state=after, evidence={"backend": "vision", "point": point, "bbox": target.bbox, "source": target.source, "state_ok": state_ok, "pixel_ok": pixel_ok}, attempts=attempt)

        return ExecutionResult(False, action="click", error="click verification failed", before_state=before, attempts=min(len(candidates), self.config.runtime.max_retries), evidence={"backend": "vision"})

    def _open_app(self, app_name: str, before):
        errors = []
        for attempt in range(2):
            try:
                cmd = self.desktop.open_app(app_name)
                keywords = cmd.app_keywords or []
                self.context.safety_flags["expected_app_keywords"] = keywords

                win = self.browser.window_manager.wait_for_window(keywords, timeout=3.5) if keywords else None
                focused = False
                if win and keywords:
                    focused = self.browser.window_manager.activate_window(keywords)
                    self.context.active_window = win.title

                self._persist_expected_target(
                    app_name=app_name,
                    keywords=keywords,
                    window_title=win.title if win else "",
                    resolved_path=cmd.resolved_path,
                    resolved_source=cmd.resolved_source,
                )

                after = self.verifier.snapshot_state()
                return ExecutionResult(True, action="open_app", target=app_name, before_state=before, after_state=after, evidence={
                    "command": cmd.detail,
                    "resolved_path": cmd.resolved_path,
                    "resolved_source": cmd.resolved_source,
                    "window": win.title if win else "",
                    "window_focused": focused,
                    "attempt": attempt + 1,
                })
            except Exception as exc:
                errors.append(str(exc))
                if attempt == 0 and self._browser_fullscreen_like():
                    self.keyboard.hotkey("f11")
                    time.sleep(1.0)
                    continue
                raise

        raise RuntimeError("; ".join(errors))
