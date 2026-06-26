---
name: windows-ui-controller
description: 'Windows 软件自动化控制技能包 - 使用 pywinauto 控制微信/QQ/网易云等任何 Windows 应用。包含完整教程、依赖包、最佳实践。'
metadata:
  {
    "openclaw":
      {
        "emoji": "🖱️",
        "os": ["windows"],
        "requires": { "bins": ["python"] },
        "install":
          [
            {
              "id": "pywinauto",
              "kind": "pip",
              "package": "pywinauto",
              "label": "Install pywinauto (pip)",
            },
          ],
      },
  }
---

# Windows UI Controller

🖱️ **让 AI 控制任何 Windows 软件 - 微信/QQ/网易云/百度网盘...**

---

## 📦 这是什么？

**Windows UI Controller** 是一个技能包，让 AI 能够：
- ✅ 扫描 Windows 软件界面（按钮、输入框、菜单等）
- ✅ 点击任意按钮
- ✅ 输入文字
- ✅ 智能识别控件（搜索框 vs 聊天输入框）
- ✅ 每步操作后验证成功

---

## 🛠️ 安装依赖

### 离线安装（使用本技能包自带的依赖）

```bash
cd dependencies
pip install --no-index --find-links=. pywinauto
```

### 在线安装

```bash
pip install pywinauto
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd dependencies
pip install --no-index --find-links=. pywinauto
```

### 2. 学习使用

**详细教程请查看**: `README.md`

包含：
- pywinauto 是什么
- 完整使用示例
- ⚠️ 关键警告（每步验证）
- 💡 智能缓存建议
- 📸 视觉辅助纠错
- 编码设置
- 最佳实践
- API 参考
- 常见问题

---

## ⚠️ 关键警告

**每步操作必须扫描验证！不要一次执行多步！**

详见 `README.md` 中的详细说明。

---

## 📁 文件结构

```
windows-ui-controller/
├── SKILL.md              # 本文件
├── README.md             # 完整教程（20 KB）
└── dependencies/         # Python 依赖包
    ├── pywinauto-0.6.9-py2.py3-none-any.whl
    ├── six-1.17.0-py2.py3-none-any.whl
    ├── comtypes-1.4.16-py3-none-any.whl
    └── pywin32-311-cp312-cp312-win_amd64.whl
```

---

## 💡 核心功能

### 1. 每步验证
操作后必须扫描确认成功

### 2. 智能缓存
记住按钮位置和功能，越用越熟练

### 3. 视觉辅助
失败时截图分析原因

---

## 📖 学习资源

- **完整教程**: `README.md`
- **pywinauto 官方文档**: https://pywinauto.readthedocs.io/
- **GitHub**: https://github.com/pywinauto/pywinauto

---

**版本**: 1.0.0  
**创建时间**: 2026-03-30  
**系统**: Windows 10/11  
**Python**: 3.8+  
**许可证**: MIT-0
