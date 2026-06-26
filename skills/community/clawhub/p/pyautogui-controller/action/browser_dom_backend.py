import json
import os
import subprocess
import sys
import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, List


@dataclass
class DOMLocateResult:
    success: bool
    detail: str = ""
    selector: Optional[str] = None
    extra: Optional[Dict] = None


class BrowserDOMBackend:
    """Bridge interface for structured-browser integrations."""

    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.bridge_cmd = os.environ.get("BROWSER_DOM_BRIDGE_CMD", "").strip()
        self.default_url = os.environ.get("BROWSER_DOM_DEFAULT_URL", "").strip()
        self.cdp_url = os.environ.get("DOM_BRIDGE_CDP_URL", "").strip()
        self.bridge_script = Path(__file__).resolve().parent.parent / "bridges" / "playwright_dom_bridge.py"

    def _resolve_command(self) -> List[str]:
        if self.bridge_cmd:
            return shlex.split(self.bridge_cmd, posix=False)
        if self.bridge_script.exists():
            return [sys.executable, str(self.bridge_script)]
        return []

    def is_available(self) -> bool:
        return bool(self.enabled and self._resolve_command())

    def locate(self, target_text: Optional[str] = None, role: Optional[str] = None, url: Optional[str] = None) -> DOMLocateResult:
        return self._invoke("locate", target_text=target_text, role=role, url=url)

    def focus_input(self, target_text: Optional[str] = None, url: Optional[str] = None) -> DOMLocateResult:
        return self._invoke("focus_input", target_text=target_text, role="textbox", url=url)

    def click(self, target_text: Optional[str] = None, role: Optional[str] = None, url: Optional[str] = None) -> DOMLocateResult:
        return self._invoke("click", target_text=target_text, role=role, url=url)

    def type_into(self, text: str, target_text: Optional[str] = None, role: Optional[str] = None, url: Optional[str] = None) -> DOMLocateResult:
        return self._invoke("type_into", target_text=target_text, role=role or "textbox", url=url, text=text)

    def _invoke(self, action: str, target_text: Optional[str] = None, role: Optional[str] = None, url: Optional[str] = None, text: Optional[str] = None) -> DOMLocateResult:
        command = self._resolve_command()
        if not self.enabled:
            return DOMLocateResult(False, detail="dom backend disabled")
        if not command:
            return DOMLocateResult(False, detail="dom backend unavailable: bridge command not configured")
        payload = {
            "action": action,
            "target_text": target_text,
            "role": role,
            "url": url or self.default_url,
            "cdp_url": self.cdp_url or None,
            "text": text,
        }
        try:
            out = subprocess.check_output(command + [json.dumps(payload, ensure_ascii=False)], stderr=subprocess.STDOUT, timeout=20)
            data = json.loads(out.decode("utf-8", errors="replace"))
            return DOMLocateResult(bool(data.get("success")), detail=str(data.get("detail", "")), selector=data.get("selector"), extra=data)
        except subprocess.CalledProcessError as exc:
            raw = exc.output.decode("utf-8", errors="replace") if exc.output else str(exc)
            try:
                data = json.loads(raw)
                return DOMLocateResult(bool(data.get("success")), detail=str(data.get("detail", "bridge failed")), selector=data.get("selector"), extra=data)
            except Exception:
                return DOMLocateResult(False, detail="dom bridge error: {0}".format(raw.strip() or exc))
        except Exception as exc:
            return DOMLocateResult(False, detail="dom bridge error: {0}".format(exc))
