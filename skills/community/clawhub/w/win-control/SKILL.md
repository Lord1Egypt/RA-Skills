# Windows 鼠标键盘控制

## 功能
通过 PowerShell 脚本控制 Windows 鼠标和键盘操作。

## 可用命令

### 鼠标控制
```powershell
# 点击鼠标
powershell -ExecutionPolicy Bypass -File skills/win-control/scripts/mouse-click.ps1 -X 500 -Y 300 -ClickType Left
```

### 键盘控制
```powershell
# 发送文本
powershell -ExecutionPolicy Bypass -File skills/win-control/scripts/send-keys.ps1 -Text "Hello World"

# 发送快捷键
powershell -ExecutionPolicy Bypass -File skills/win-control/scripts/send-keys.ps1 -Keys "CTRL+C,CTRL+V"
```

## 支持的快捷键
- ENTER, ESC, TAB
- CTRL+C, CTRL+V, CTRL+A
- ALT+TAB, WIN
- F1-F12
- BACKSPACE, DELETE, HOME, END

## ⚠️ 安全提示
- 鼠标键盘控制可能影响当前操作
- 建议在测试环境先验证
- 避免在生产环境自动化关键操作
