---
name: tkinter-i18n
slug: tkinter-i18n
version: 1.0.4
displayName: "Tkinter 中英国际化"
category: dev-programming
subCategories: [dev-script, dev-code-gen]
agent_created: true
description: "Add Chinese/English (or multi-language) internationalization to a Tkinter desktop app. This skill should be used when a user wants a Tkinter GUI to auto-detect the system UI language, offer a manual language switcher, persist the choice, and apply it without gettext. The approach uses a t(key) function with Chinese-as-key plus an _EN translation table, detects language via Windows GetUserDefaultUILanguage, persists to a config file, and restarts the process to apply changes cleanly."
agent_created: true
---

# Tkinter i18n (中文即 key)

A lightweight, gettext-free i18n scheme for Tkinter apps. Chinese strings are the
dictionary keys; an `_EN` table holds English; unknown keys fall back to the
Chinese source so the UI never shows blank/missing text.

## When to use

- A user wants a Tkinter tool bilingual (中文 / English) or multi-language.
- Need auto-detect of system language + a manual dropdown + "remember my choice".
- Avoid gettext (it does not survive PyInstaller `--onefile` freezing cleanly).

## Pattern

1. Define `t(key, *args)` — returns `_EN.get(key, key)`, then `str % args` if
   args present. Never raises on missing keys.
2. Keep one `_EN = {...}` table. Add an entry for every user-visible string.
3. `_detect_lang()` — Windows: `ctypes.windll.kernel32.GetUserDefaultUILanguage()`
   `& 0xFF == 0x04` → Chinese, else English. Fallback to `locale` on non-Windows.
4. Persist choice to `~/.workbuddy/APP.lang` (`zh`/`en`); load at startup.
5. Manual switch: write the file, then restart the process
   (`os.execv(sys.executable, [sys.executable] + sys.argv)`) so every widget
   rebuilds with the new language. Per-widget live redraw is fragile — restart
   is simpler and reliable.

See `references/i18n_template.py` for a complete, runnable minimal app.

## Wiring checklist

- [ ] Import `t` at top; wrap **every** user-visible string (titles, buttons,
      labels, messageboxes, status text, model display names, dropdown labels).
- [ ] Add a language `ttk.Combobox` (top-right) bound to the switch handler.
- [ ] `LANG_ORDER = ["zh", "en"]`, `LANG_NAMES = {"zh": "中文", "en": "English"}`.
- [ ] Restart-on-change writes config then `os.execv`.
- [ ] Adding a language later = add a branch in `_detect_lang` + a new translation
      table + extend `LANG_ORDER`/`LANG_NAMES`.

## Notes

- Frozen (PyInstaller) safe: no external `.mo` files, no `gettext` runtime.
- The language config path should live under `~/.workbuddy/` so it is shared with
  the agent's config dir, or under the app's own dir — pick one and be consistent.
