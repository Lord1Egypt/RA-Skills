"""Minimal Tkinter i18n template — 中文即 key + _EN 表 + 自动检测 + 手动切换 + 重启生效。

用法：直接跑这个文件即可看到双语效果；右上角下拉切语言会重启进程。
"""
import ctypes
import locale
import os
import sys
import tkinter as tk
from tkinter import ttk

# ---- 语言配置（写在用户目录，跨进程记住选择）----
LANG_FILE = os.path.join(os.path.expanduser("~"), ".workbuddy", "demo_app.lang")
LANG_ORDER = ["zh", "en"]
LANG_NAMES = {"zh": "中文", "en": "English"}


def _detect_lang():
    """Windows 用 GetUserDefaultUILanguage；非 Windows 退回 locale。"""
    try:
        if sys.platform == "win32":
            if ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0xFF == 0x04:
                return "zh"
        elif locale.getdefaultlocale()[0] and locale.getdefaultlocale()[0].lower().startswith("zh"):
            return "zh"
    except Exception:
        pass
    return "en"


def _load_lang():
    try:
        with open(LANG_FILE, encoding="utf-8") as f:
            v = f.read().strip()
        if v in LANG_ORDER:
            return v
    except Exception:
        pass
    return _detect_lang()


def _save_lang(code):
    os.makedirs(os.path.dirname(LANG_FILE), exist_ok=True)
    with open(LANG_FILE, "w", encoding="utf-8") as f:
        f.write(code)


_current_lang = _load_lang()

# ---- 翻译表：未命中的 key 原样返回（中文即源语言，绝不空白）----
_EN = {
    "语言": "Language",
    "你好，世界": "Hello, world",
    "切换语言": "Switch language",
    "关于": "About",
}


def t(key, *args):
    s = _EN.get(key, key)
    if args:
        try:
            s = s % args
        except Exception:
            pass
    return s


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(t("你好，世界"))
        self.geometry("360x200")

        # 语言下拉（手动切换 -> 写盘 -> 重启进程）
        bar = tk.Frame(self)
        bar.pack(fill="x", padx=8, pady=6)
        tk.Label(bar, text=t("语言")).pack(side="left")
        self.combo = ttk.Combobox(bar, state="readonly", values=[LANG_NAMES[c] for c in LANG_ORDER], width=10)
        try:
            self.combo.current(LANG_ORDER.index(_current_lang))
        except Exception:
            self.combo.current(0)
        self.combo.pack(side="left", padx=4)
        self.combo.bind("<<ComboboxSelected>>", self._on_lang)

        tk.Label(self, text=t("切换语言"), font=("Microsoft YaHei", 14)).pack(pady=30)
        tk.Button(self, text=t("关于"), command=lambda: print(t("关于"))).pack()

    def _on_lang(self, _e=None):
        name = self.combo.get()
        code = next((c for c in LANG_ORDER if LANG_NAMES[c] == name), None)
        if code and code != _current_lang:
            _save_lang(code)
            self.destroy()
            os.execv(sys.executable, [sys.executable] + sys.argv)


if __name__ == "__main__":
    App().mainloop()
