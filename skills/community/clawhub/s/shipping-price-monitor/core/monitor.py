# -*- coding: utf-8 -*-
"""
文件监控引擎
监控目录中的Excel文件变化，触发价格分析
"""

import os
import time
import json
import yaml
import datetime
import hashlib
from pathlib import Path
from threading import Thread, Event
from typing import List, Optional, Callable

SKILL_DIR = Path(__file__).parent.parent
CONFIG_DIR = SKILL_DIR / "config"
DATA_DIR = SKILL_DIR / "data"


class FileMonitor:
    def __init__(self):
        self.settings = self._load_settings()
        self.rules = self._load_rules()
        self._stop_event = Event()
        self._thread: Optional[Thread] = None
        self._file_hashes: dict = {}
        self._on_alert_callback: Optional[Callable] = None
    
    def _load_settings(self) -> dict:
        settings_file = CONFIG_DIR / "settings.yaml"
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def _load_rules(self) -> dict:
        rules_file = CONFIG_DIR / "rules.json"
        if rules_file.exists():
            with open(rules_file, 'r', encoding='utf-8') as f:
                return json.load(f) or {}
        return {"rules": []}
    
    def _save_settings(self):
        settings_file = CONFIG_DIR / "settings.yaml"
        with open(settings_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.settings, f, allow_unicode=True, default_flow_style=False)
    
    def _save_rules(self):
        rules_file = CONFIG_DIR / "rules.json"
        with open(rules_file, 'w', encoding='utf-8') as f:
            json.dump(self.rules, f, ensure_ascii=False, indent=2)
    
    def get_enabled_rules(self) -> List[dict]:
        return [r for r in self.rules.get("rules", []) if r.get("enabled", True)]
    
    def enable(self) -> bool:
        self.settings["monitor"]["enabled"] = True
        self._save_settings()
        return True
    
    def disable(self) -> bool:
        self.settings["monitor"]["enabled"] = False
        self._save_settings()
        return True
    
    def is_enabled(self) -> bool:
        return self.settings.get("monitor", {}).get("enabled", False)
    
    def set_watch_directory(self, directory: str):
        self.settings["monitor"]["watch_directory"] = str(directory)
        self._save_settings()
    
    def set_excel_path(self, path: str):
        self.settings["monitor"]["excel_path"] = str(path)
        self._save_settings()
    
    def set_check_interval(self, seconds: int):
        self.settings["monitor"]["check_interval"] = seconds
        self._save_settings()
    
    def get_watch_directory(self) -> str:
        return self.settings.get("monitor", {}).get("watch_directory", "") or str(DATA_DIR / "watch")
    
    def get_excel_path(self) -> str:
        return self.settings.get("monitor", {}).get("excel_path", "")
    
    def _get_file_hash(self, filepath: str) -> str:
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""
    
    def scan_excel_files(self, directory: str = None) -> List[str]:
        if directory is None:
            directory = self.get_watch_directory()
        
        if not directory or not os.path.exists(directory):
            return []
        
        excel_files = []
        for file in os.listdir(directory):
            if file.endswith(('.xlsx', '.xls')) and not file.startswith('~$'):
                excel_files.append(os.path.join(directory, file))
        
        return sorted(excel_files, key=lambda x: os.path.getmtime(x), reverse=True)
    
    def get_latest_excel(self, directory: str = None) -> Optional[str]:
        files = self.scan_excel_files(directory)
        return files[0] if files else None
    
    def is_file_changed(self, filepath: str) -> bool:
        current_hash = self._get_file_hash(filepath)
        previous_hash = self._file_hashes.get(filepath, "")
        
        if current_hash and current_hash != previous_hash:
            self._file_hashes[filepath] = current_hash
            return True
        return False
    
    def set_on_alert(self, callback: Callable):
        self._on_alert_callback = callback
    
    def _monitor_loop(self):
        watch_dir = self.get_watch_directory()
        interval = self.settings.get("monitor", {}).get("check_interval", 60)
        
        self._log(f"文件监控已启动，监控目录: {watch_dir}，检查间隔: {interval}秒")
        
        while not self._stop_event.is_set():
            try:
                if self.is_enabled():
                    latest_file = self.get_latest_excel(watch_dir)
                    if latest_file and self.is_file_changed(latest_file):
                        self._log(f"检测到文件变化: {latest_file}")
                        if self._on_alert_callback:
                            self._on_alert_callback(latest_file)
            except Exception as e:
                self._log(f"监控检查出错: {e}")
            
            self._stop_event.wait(interval)
        
        self._log("文件监控已停止")
    
    def start(self) -> bool:
        if self._thread and self._thread.is_alive():
            self._log("文件监控已在运行中")
            return True
        
        self._stop_event.clear()
        self._thread = Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        return True
    
    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
            self._thread = None
    
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()
    
    def _log(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = SKILL_DIR / "monitor.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"[{timestamp}] {message}")
    
    def get_status(self) -> dict:
        return {
            "enabled": self.is_enabled(),
            "running": self.is_running(),
            "watch_directory": self.get_watch_directory(),
            "excel_path": self.get_excel_path(),
            "check_interval": self.settings.get("monitor", {}).get("check_interval", 60),
            "rules_count": len(self.get_enabled_rules())
        }
