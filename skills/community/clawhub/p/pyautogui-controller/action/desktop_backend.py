import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass
class DesktopCommandResult:
    success: bool
    detail: str = ""
    resolved_path: str = ""
    resolved_source: str = ""
    app_keywords: Optional[List[str]] = None


class DesktopBackend:
    def __init__(self):
        self.mapping = {
            "记事本": "notepad.exe",
            "notepad": "notepad.exe",
            "notepad++": "notepad++.exe",
            "npp": "notepad++.exe",
            "chrome": "chrome.exe",
            "谷歌": "chrome.exe",
            "google": "chrome.exe",
            "浏览器": "chrome.exe",
            "firefox": "firefox.exe",
            "火狐": "firefox.exe",
            "edge": "msedge.exe",
            "计算器": "calc.exe",
            "cmd": "cmd.exe",
            "burp": "burpsuitepro.exe",
        }
        self.desktop_dirs = [Path.home() / "Desktop"]
        self.search_roots = [
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")),
            Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")),
            Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))),
            Path("E:/tool"),
        ]

    def open_app(self, app_name: str) -> DesktopCommandResult:
        cleaned = self._normalize_app_name(app_name)
        resolved = self._resolve_app(cleaned)
        if not resolved:
            raise FileNotFoundError(f"unable to resolve desktop app: {app_name}")

        target, kind, source = resolved
        if kind == "command":
            subprocess.Popen([target], shell=False)
        else:
            os.startfile(target)
        time.sleep(1.5)
        return DesktopCommandResult(
            True,
            detail=cleaned,
            resolved_path=target,
            resolved_source=source,
            app_keywords=self._keywords_for(cleaned, target),
        )

    def _normalize_app_name(self, app_name: str) -> str:
        text = (app_name or "").strip().lower()
        for noise in ["桌面上的", "我桌面的", "桌面快捷方式", "桌面快捷", "桌面上", "桌面", "上的", "打开", "启动", "运行"]:
            text = text.replace(noise, "")
        replacements = {
            "谷歌浏览器": "chrome",
            "chrome浏览器": "chrome",
            "谷歌": "chrome",
            "google chrome": "chrome",
            "google": "chrome",
            "火狐浏览器": "firefox",
            "firefox浏览器": "firefox",
            "火狐": "firefox",
            "微软浏览器": "edge",
            "edge浏览器": "edge",
        }
        for src, dst in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
            text = text.replace(src, dst)
        return text.strip(" ' \"　")

    def _resolve_app(self, cleaned: str) -> Optional[Tuple[str, str, str]]:
        mapped = self.mapping.get(cleaned, cleaned)

        alias_hit = self._resolve_known_binary(mapped)
        if alias_hit:
            return alias_hit

        desktop_hit = self._find_on_desktop(cleaned)
        if desktop_hit:
            return str(desktop_hit), "startfile", "desktop_shortcut"

        direct_hit = self._resolve_known_binary(cleaned)
        if direct_hit:
            return direct_hit

        install_hit = self._find_installed_binary(cleaned, mapped)
        if install_hit:
            return str(install_hit), "startfile", "installed_binary"

        maybe_path = Path(mapped)
        if maybe_path.exists():
            return str(maybe_path), "startfile", "explicit_path"

        return None

    def _resolve_known_binary(self, name: str) -> Optional[Tuple[str, str, str]]:
        candidates = []
        if name:
            candidates.append(name)
            if not name.endswith(".exe"):
                candidates.append(name + ".exe")

        seen = set()
        for candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)

            which_hit = shutil.which(candidate)
            if which_hit:
                return which_hit, "command", "path"

            for root in self.search_roots:
                if not root.exists():
                    continue
                direct = root / candidate
                if direct.exists():
                    return str(direct), "startfile", "installed_binary"

        return None

    def _find_on_desktop(self, cleaned: str) -> Optional[Path]:
        aliases = {cleaned, cleaned.replace("++", ""), cleaned.replace(" ", "")}
        for root in self.desktop_dirs:
            if not root.exists():
                continue
            for item in root.iterdir():
                name = item.stem.lower().replace(" ", "")
                raw = item.name.lower().replace(" ", "")
                if any(a and (a in name or a in raw or name in a) for a in aliases):
                    if item.suffix.lower() in {".lnk", ".url", ".exe", ".bat", ".cmd"}:
                        return item
        return None

    def _find_installed_binary(self, cleaned: str, mapped: str) -> Optional[Path]:
        probes = []
        normalized = cleaned.replace(" ", "")
        mapped_name = mapped if mapped.endswith(".exe") else mapped + ".exe"

        is_chrome = cleaned in {"chrome", "谷歌", "google"} or mapped_name.lower() == "chrome.exe"
        is_firefox = cleaned in {"firefox", "火狐"} or mapped_name.lower() == "firefox.exe"
        is_notepadpp = cleaned in {"notepad++", "npp"} or mapped_name.lower() == "notepad++.exe"
        is_burp = cleaned == "burp" or "burp" in mapped_name.lower()

        for root in self.search_roots:
            if not root.exists():
                continue

            base_probes = [
                root / mapped_name,
                root / cleaned / mapped_name,
                root / normalized / mapped_name,
            ]
            probes.extend(base_probes)

            if is_chrome:
                probes.extend([
                    root / "Google" / "Chrome" / "Application" / "chrome.exe",
                    root / "Chrome" / "Application" / "chrome.exe",
                ])
            if is_firefox:
                probes.append(root / "Mozilla Firefox" / "firefox.exe")
            if is_notepadpp:
                probes.append(root / "Notepad++" / "notepad++.exe")
            if is_burp:
                probes.extend([
                    root / "BurpSuitePro" / "BurpSuitePro.exe",
                    root / "burpsuite" / "burpsuitepro.exe",
                ])

        seen = set()
        for p in probes:
            key = str(p).lower()
            if key in seen:
                continue
            seen.add(key)
            if p.exists():
                return p

        for root in self.search_roots:
            if not root.exists():
                continue
            try:
                for hit in root.rglob(mapped_name):
                    return hit
            except Exception:
                continue
        return None

    def _keywords_for(self, cleaned: str, target: str) -> List[str]:
        base = Path(target).stem.lower() if target else cleaned
        keywords = {cleaned, base, base.replace(".exe", "")}
        target_lower = (target or "").lower()

        if cleaned in {"notepad++", "npp"} or "notepad++" in target_lower:
            keywords.update({"notepad++", "npp", "new 1", "*新文件", " - Notepad++"})
        if cleaned in {"记事本", "notepad"} or "notepad.exe" in target_lower:
            keywords.update({"记事本", " - 记事本"})
        if cleaned in {"chrome", "谷歌", "google"} or "chrome.exe" in target_lower:
            keywords.update({"chrome", "google chrome", "谷歌浏览器", "chrome浏览器", " - Google Chrome"})
        if cleaned in {"firefox", "火狐"} or "firefox.exe" in target_lower:
            keywords.update({"firefox", "火狐浏览器", " - Mozilla Firefox"})
        if cleaned == "burp" or "burp" in target_lower:
            keywords.update({"burp", "burpsuite"})

        return [k for k in keywords if k]
