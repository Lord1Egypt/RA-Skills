# Windows 鼠标键盘 RPA 控制

通过 PowerShell 脚本实现 Windows 鼠标键盘自动化控制，模拟人工操作。

---

## 📁 脚本列表

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `rpa-dingtalk-smart.ps1` | 智能钉钉发消息 | **推荐** - 自动查找钉钉窗口 |
| `rpa-dingtalk-send-message.ps1` | 钉钉发消息（基础版） | 钉钉已打开时使用 |
| `mouse-click.ps1` | 鼠标点击 | 精准位置点击 |
| `send-keys.ps1` | 键盘输入 | 文本/快捷键输入 |
| `test-control.ps1` | 测试脚本 | 功能测试 |

---

## 🚀 快速开始

### 示例：给韩文瀚发消息

```powershell
# 智能版（推荐）- 自动查找并激活钉钉窗口
powershell -ExecutionPolicy Bypass -File "C:\Users\xl\.openclaw\workspace\skills\win-control\scripts\rpa-dingtalk-smart.ps1" `
  -Recipient "韩文瀚" `
  -Message "你好，我是通过 RPA 给你发的消息"
```

---

## 📋 参数说明

### rpa-dingtalk-smart.ps1

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `-Recipient` | 否 | "韩文瀚" | 联系人姓名 |
| `-Message` | 否 | "你好，我是通过 RPA 给你发的消息" | 消息内容 |

### 示例

```powershell
# 基础用法（使用默认参数）
powershell -ExecutionPolicy Bypass -File scripts/rpa-dingtalk-smart.ps1

# 自定义联系人和消息
powershell -ExecutionPolicy Bypass -File scripts/rpa-dingtalk-smart.ps1 `
  -Recipient "张三" `
  -Message "下午 3 点开会"

# 发送长消息
powershell -ExecutionPolicy Bypass -File scripts/rpa-dingtalk-smart.ps1 `
  -Recipient "李四" `
  -Message "关于明天会议的安排：1. 准备材料 2. 预定会议室 3. 通知参会人员"
```

---

## 🔧 其他脚本用法

### 鼠标点击

```powershell
# 点击指定坐标
powershell -ExecutionPolicy Bypass -File scripts/mouse-click.ps1 -X 500 -Y 300 -ClickType Left

# ClickType 可选值：Left, Right, Double
```

### 键盘输入

```powershell
# 发送文本
powershell -ExecutionPolicy Bypass -File scripts/send-keys.ps1 -Text "Hello World"

# 发送快捷键
powershell -ExecutionPolicy Bypass -File scripts/send-keys.ps1 -Keys "CTRL+C,CTRL+V,ENTER"
```

### 测试功能

```powershell
# 测试鼠标移动
powershell -ExecutionPolicy Bypass -File scripts/test-control.ps1 -TestMouse

# 测试键盘输入
powershell -ExecutionPolicy Bypass -File scripts/test-control.ps1 -TestKeyboard
```

---

## ⌨️ 快捷键代码

| 快捷键 | SendKeys 代码 |
|--------|--------------|
| Ctrl+C | `^c` |
| Ctrl+V | `^v` |
| Ctrl+A | `^a` |
| Ctrl+Z | `^z` |
| Alt+Tab | `%{TAB}` |
| Win 键 | `{WIN}` |
| Enter | `{ENTER}` |
| ESC | `{ESC}` |
| TAB | `{TAB}` |
| F1-F12 | `{F1}` - `{F12}` |
| Backspace | `{BACKSPACE}` |
| Delete | `{DELETE}` |
| Home | `{HOME}` |
| End | `{END}` |

---

## ⚠️ 注意事项

### 安全提示

| 注意 | 说明 |
|------|------|
| 🔒 活动窗口 | 脚本会操作当前活动窗口，请提前确认 |
| ⚠️ 干扰 | 运行时会影响你的鼠标键盘，不要同时操作 |
| 🧪 测试 | 建议先在测试环境验证 |
| 🛑 权限 | 某些操作可能需要管理员权限 |

### 使用建议

1. **首次使用**：先用测试脚本验证功能
2. **生产环境**：建议先用 API 方案（更稳定）
3. **复杂场景**：考虑结合鼠标键盘 + API 混合方案

---

## 🔍 故障排除

### 问题 1：钉钉窗口未找到

```
症状：提示"未找到钉钉窗口"
解决：
1. 确保钉钉已启动
2. 检查钉钉窗口标题是否为"钉钉"或"DingTalk"
3. 手动激活钉钉窗口后重试
```

### 问题 2：消息发送失败

```
症状：搜索不到联系人或发送失败
解决：
1. 确认联系人姓名正确（包括大小写）
2. 确认钉钉已登录
3. 检查网络连接
```

### 问题 3：输入法干扰

```
症状：输入的文字不对
解决：
1. 切换到英文输入法
2. 或使用 API 方案（不受输入法影响）
```

---

## 📊 API 方案 vs 鼠标键盘方案

| 特性 | API 方案 | 鼠标键盘方案 |
|------|----------|--------------|
| 稳定性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 速度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 准确性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 灵活性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 权限要求 | API 权限 | 无 |
| 推荐场景 | 批量发送 | 特殊 UI 操作 |

---

## 📝 更新日志

- **v1.0** (2026-04-08)
  - 初始版本
  - 支持钉钉消息发送
  - 支持鼠标键盘基础操作

---

## 📞 支持

如有问题，请检查：
1. PowerShell 版本（建议 5.1+）
2. .NET Framework 版本
3. 钉钉客户端版本
