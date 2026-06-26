# Visual Bug Hunter 🕵️‍♂️

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/visual-bug-hunter.svg)](https://badge.fury.io/py/visual-bug-hunter)

> **🚀 想要跨平台的 AI 调试体验？**  
> 如果你希望在悟空、WorkBuddy、Cursor 等工具中通过自然语言直接调用此技能，请切换到 **[mcp-version](https://github.com/yitao2027/visual-bug-hunter/tree/mcp-version)** 分支。该版本遵循通用 MCP 标准，实现“一次安装，多端兼容”。

**AI-powered visual bug detection and fixing tool for GUI apps.**

![Visual Bug Hunter Demo](https://raw.githubusercontent.com/yitao2027/visual-bug-hunter/main/assets/demo.gif) 

Let AI "see" and "click" like a human tester to find UI bugs, locate the exact code, and apply minimal fixes. Perfect for **Vibe Coding** users who want their AI agents to self-verify UI changes.

---

## 🚀 Why Visual Bug Hunter?

When building GUI apps with AI (Tauri, Electron, Tkinter, Qt), you often face:
- **"The button doesn't work!"** → Is it disabled? Is the event handler missing?
- **"Elements are overlapping!"** → Did the AI render the same widget twice?
- **"The layout is broken!"** → Where in the 1000-line file is the styling wrong?

Visual Bug Hunter solves this by closing the loop:
1. **See**: Analyze screenshots with Vision AI.
2. **Click**: Test UI interactions programmatically.
3. **Locate**: Scan code for common UI anti-patterns.
4. **Fix**: Generate minimal diffs (not full file rewrites).
5. **Verify**: Screenshot again to prove the fix worked.

---

## 📦 Installation

```bash
pip install visual-bug-hunter
```

Or from source:
```bash
git clone https://github.com/yitao2027/visual-bug-hunter.git
cd visual-bug-hunter
pip install -e .
```

---

## 🛠️ Usage

### 1. Scan a Project (Static Analysis)
Find potential UI bugs without running the app:
```bash
vbh scan /path/to/your/project
```

### 2. Analyze a Screenshot
Provide a screenshot to detect visual anomalies:
```bash
vbh analyze --screenshot bug.png --project /path/to/project
```

### 3. Launch & Test an App
Automatically start a Python/Tkinter or macOS app and capture its initial state:
```bash
vbh test --app my_app.py
```

---

## 🔍 How It Works

| Module | Function |
|--------|----------|
| **Utils** | Cross-platform screenshot capture (`screencapture`, `scrot`). |
| **Analyzer** | Vision AI prompt engineering for UI bug detection. |
| **Locator** | AST-based scanning for disabled widgets and duplicate renders. |
| **Reporter** | Generates structured JSON reports with code snippets. |
| **CLI** | User-friendly command-line interface. |

### Specialized Detectors
- **Disabled Widgets**: Finds `setEnabled(False)`, `state=DISABLED`, etc.
- **Duplicate Renders**: Detects multiple `.pack()` or `.grid()` calls on the same widget.

---

## 🤝 Contributing

Contributions are welcome! Please read the [BUG_RULES.md](BUG_RULES.md) to understand our core workflow.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🌟 Acknowledgements

- Built for the **Vibe Coding** community.
- Inspired by the need for AI agents that can self-verify their own UI work.
