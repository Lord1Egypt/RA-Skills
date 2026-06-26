---
name: publish-agent-skill-infinite
description: 将本地技能发布到 ClawHub。触发场景：发布技能、上传技能到ClawHub、发布skill、ClawHub发布。
version: 1.0.1
---

# 发布Agent技能_无限

将本地技能文件夹上传并发布到 ClawHub（clawhub.ai）。

## 触发场景

用户说：
- "发布技能"
- "发布skill"
- "上传技能到ClawHub"
- "发布到ClawHub"
- "ClawHub发布技能"
- "发布agent技能"

## 前置条件

用户必须提供：
- **技能文件夹路径**（包含 SKILL.md 等文件的完整路径）

## 核心原则

- 使用 xb CLI 操作浏览器，**禁止使用内置 browser 工具**
- **禁止硬编码 ref 值** — 每次页面加载后 ref 会变化，必须实时从快照获取
- **每次点击前必须先滚动**，确保目标元素在视口中可见，否则点击无效
- 除登录、支付、删除等核心操作外，所有问题自己解决，不指挥用户

---

## 操作流程

### 第零步：初始化 xbrowser

```powershell
$NODE = $env:QCLAW_CLI_NODE_BINARY; if (-not $NODE) { $NODE = "node" }
& $NODE "D:\soft\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs" init
```

- `ok=true` → 继续
- `ok=false` → 按 hint 修复后重试

---

### 第一步：打开发布页面

```powershell
& $NODE "D:\soft\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs" run --browser default --headed open "https://clawhub.ai/publish-skill"
& $NODE "D:\soft\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs" run --browser default --headed wait --load networkidle
& $NODE "D:\soft\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs" run --browser default --headed snapshot -i
```

确认页面标题为 "Publish a skill"，已登录账号。

---

### 第二步：填写表单

从快照中找到 SLUG 和 DISPLAY NAME 输入框的 ref，依次填写：

```powershell
# 填写 SLUG（技能英文名，即文件夹名）
& $NODE "...xb.cjs" run --browser default --headed fill "@<SLUG的ref>" "技能文件夹名称"

# 填写 DISPLAY NAME（技能中文名）
& $NODE "...xb.cjs" run --browser default --headed fill "@<DISPLAY_NAME的ref>" "技能中文名称"
```

> SLUG 示例：`create-wechat-channel-collection-infinite`
> DISPLAY NAME 示例：`创建微信视频号合集_无限`

---

### 第三步：删除 SKILL.md.bak（如存在）

⚠️ 上传前必须清理，否则可能导致上传异常。

```powershell
Remove-Item -Force "技能文件夹完整路径\SKILL.md.bak" -ErrorAction SilentlyContinue
```

---

### 第四步：向下滚动，使上传区域进入视口

⚠️ **不可省略！** ClawHub 发布页面较长，"Drop a folder" 默认不在视口中，不滚动直接点击无效。

```powershell
& $NODE "...xb.cjs" run --browser default --headed press PageDown
```

滚动后重新 `snapshot -i`，确认快照中出现 "Drop a folder" 按钮。

---

### 第五步：点击 "Drop a folder" 触发系统文件对话框

⚠️ **必须点击大区域 "Drop a folder"，绝对不能点 "Choose folder" 按钮！**

从快照中找到 role=button、name 包含 "Drop a folder" 的 ref（通常是 e32 附近，但每次不同，必须从快照读取）：

```powershell
& $NODE "...xb.cjs" run --browser default --headed click "@<Drop_a_folder的ref>"
```

> PowerShell 中 `@ref` 必须用双引号包裹，如 `click "@e32"`，否则 PowerShell 会将 `@` 解析为数组。

---

### 第六步：pyautogui 输入文件夹路径

点击后**立即**运行以下脚本（脚本内部已含 3 秒等待，等系统对话框出现）：

```powershell
Start-Sleep -Seconds 3; python -c "
import pyautogui, time, tkinter as tk

time.sleep(1)

# Ctrl+L 聚焦地址栏
pyautogui.keyDown('ctrl'); pyautogui.keyDown('l'); pyautogui.keyUp('l'); pyautogui.keyUp('ctrl')
time.sleep(0.5)

# Ctrl+A 全选 + Delete 清空原有内容
pyautogui.keyDown('ctrl'); pyautogui.keyDown('a'); pyautogui.keyUp('a'); pyautogui.keyUp('ctrl')
time.sleep(0.2)
pyautogui.press('delete')
time.sleep(0.3)

# 用 tkinter 写入剪贴板（避免中文乱码）
folder_path = r'技能文件夹完整路径'
r = tk.Tk(); r.withdraw(); r.clipboard_clear(); r.clipboard_append(folder_path); r.destroy()

# 粘贴路径
pyautogui.keyDown('ctrl'); pyautogui.keyDown('v'); pyautogui.keyUp('v'); pyautogui.keyUp('ctrl')
time.sleep(0.5)

# 回车进入文件夹
pyautogui.press('return')
print('done')
"
```

**关键要点：**
- `Start-Sleep -Seconds 3` 在 PowerShell 层等待，确保系统对话框已弹出
- 使用 `Ctrl+L` 聚焦地址栏（不是 Alt+D）
- 先 `Ctrl+A` + `Delete` 清空地址栏原有内容，再粘贴
- 路径必须用原始字符串 `r'...'`，避免 `\f`、`\n` 等被转义
- 用 tkinter 写剪贴板，避免 PowerShell `Set-Clipboard` 中文乱码

---

### 第七步：用户手动点击"上传"按钮

⚠️ **AI 不负责点击系统对话框的按钮，由用户手动操作。**

1. 确认系统对话框已打开正确的文件夹
2. 点击对话框右下角的 **"上传"** 按钮
3. 对话框关闭后，网页显示 "1 files · X KB" 即为成功

完成后告知 AI 继续。

---

### 第八步：向下滚动，使协议复选框进入视口

⚠️ **不可省略！** 上传完成后页面可能回滚，协议复选框同样不在视口中，不滚动直接点击无效。

```powershell
& $NODE "...xb.cjs" run --browser default --headed press PageDown
```

---

### 第九步：勾选 MIT-0 协议

从快照中找到 role=checkbox、name 包含 "MIT-0" 的 ref：

```powershell
& $NODE "...xb.cjs" run --browser default --headed click "@<checkbox的ref>"
```

点击后重新 `snapshot -i`，**确认 `checked=true`**，否则重试。

---

### 第十步：点击发布

协议勾选后，"Publish skill" 按钮从 `disabled` 变为可用。从快照中找到其 ref：

```powershell
& $NODE "...xb.cjs" run --browser default --headed click "@<Publish_skill的ref>"
```

等待 5 秒后 `snapshot -i`，确认页面跳转到技能详情页（URL 格式：`https://clawhub.ai/<owner>/<slug>`）即发布成功。

---

## 关键元素速查

| 元素 | 快照中的特征 | 操作 |
|------|------------|------|
| SLUG 输入框 | role=textbox, name="SLUG" | fill |
| DISPLAY NAME 输入框 | role=textbox, name="DISPLAY NAME" | fill |
| Drop a folder 区域 | role=button, name 含 "Drop a folder" | click（需先 PageDown） |
| Choose folder 按钮 | role=button, name="Choose folder" | ❌ 不要点这个 |
| MIT-0 协议复选框 | role=checkbox, name 含 "MIT-0" | click（需先 PageDown） |
| Publish skill 按钮 | role=button, name="Publish skill" | click（勾选协议后才可用） |

---

## 技术要点总结

1. **两次 PageDown** — 第四步（上传前）和第八步（勾选前）各需一次，缺一不可
2. **点 Drop a folder，不点 Choose folder** — 两个按钮相邻，必须点大区域那个
3. **pyautogui 在 PowerShell 的 Start-Sleep 之后运行** — 确保系统对话框已出现
4. **Ctrl+L 聚焦地址栏** — Windows 文件选择对话框标准快捷键
5. **tkinter 写剪贴板** — 避免中文路径乱码，不用 Set-Clipboard
6. **勾选后验证 checked=true** — 快照确认，否则重试
7. **禁止硬编码 ref** — 每次页面加载 ref 都会变化

---

## 常见失败原因

| 错误 | 正确做法 |
|------|---------|
| 点击前未 PageDown | 每次点击前先滚动，确保元素在视口中 |
| 点了 "Choose folder" | 必须点 "Drop a folder" 大区域 |
| pyautogui 操作了浏览器地址栏 | 点击后先 `Start-Sleep -Seconds 3` 再运行 pyautogui |
| 地址栏路径拼接错误 | 先 Ctrl+A + Delete 清空，再粘贴 |
| 中文路径乱码 | 用 tkinter 写剪贴板，路径用 `r'...'` 原始字符串 |
| 复选框点击无效（checked 仍为 false） | 先 PageDown 滚动，再点击，再 snapshot 验证 |
| PowerShell @ref 报错 | `@ref` 必须用双引号包裹：`click "@e32"` |
| 上传了 SKILL.md.bak | 上传前先 Remove-Item 删除 |
| Publish skill 按钮仍 disabled | 检查复选框是否真正 checked=true |
