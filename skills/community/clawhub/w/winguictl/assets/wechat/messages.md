# 消息操作

## 打开联系人/群聊聊天窗口

### 方式A：在会话列表中查找

#### 步骤1：点击左侧"微信"按钮（会话列表）

- 先 snapshot 找到 Sidebar 中"微信"按钮的位置
  `python scripts\winguictl.py snapshot --window-id <wx_window_id> uia`
- 找到 "微信" 或对应语言的 Button
  `python scripts\winguictl.py find --window-id <wx_window_id> uia --text "微信" --control-type Button`
- 使用 element-id 点击
  `python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <weixin_btn_element_id>`

#### 步骤2：在会话列表中滚动查找好友

##### 获取会话列表区域，使用滚轮向下滚动

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> scroll --direction down --amount 3
```

##### 每次滚动后检查是否出现目标好友

每次滚动后使用 find ocr 或 snapshot 检查。

#### 步骤3：找到后点击好友 ListItem

一定要用`action click`点击，`uia-control invoke` 对微信控件无效。

##### 查找好友

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "好友备注名" --control-type ListItem
```

##### 点击好友

使用返回的 element_id 点击。

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <friend_element_id>
```

### 方式B：通过顶部搜索栏搜索

当会话列表中没有目标好友时，参见 [search.md](./search.md)，搜索联系人或群聊后点击结果即可打开聊天窗口。

## 发送文本消息

> 前提：已打开好友聊天窗口
> 参考：pyweixin 中 `Messages.send_messages_to_friend` 的实现

### 步骤1：定位聊天输入框

聊天输入框的特征：
- `control_type="Edit"`
- `class="mmui::ChatInputField"`
- `automation_id="chat_input_field"`

#### 方式A：通过 automation_id 查找（推荐）

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --automation-id chat_input_field
```

#### 方式B：通过 class 查找

```powershell
python scripts\winguictl.py snapshot --window-id <wx_window_id> uia --class ChatInputField
```

查找 `class="mmui::ChatInputField"` 的 Edit 控件，记录其 `runtime_id`。

### 步骤2：等待输入框可用

#### 等待聊天输入框出现

```powershell
python scripts\winguictl.py wait uia --window-id <wx_window_id> --automation-id chat_input_field --timeout 3
```

#### 聚集输入框

> ⚠️ **注意**：`uia-control invoke` 对微信控件可能无效，推荐使用 `action click`。

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id chat_input_field
```

### 步骤3：设置消息内容

#### 方式A：使用 uia-control set-text（推荐）

```powershell
python scripts\winguictl.py uia-control --window-id <wx_window_id> --element-id <chat_input_runtime_id> set-text "你好，这是测试消息"
```

#### 方式B：先点击输入框，再输入

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <chat_input_element_id>
python scripts\winguictl.py action --window-id <wx_window_id> type --text "你好，这是测试消息"
```

### 步骤4：发送消息

#### 使用快捷键 Alt+S 发送

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{ALT}" "{S}"
```

### 步骤5：等待消息发送完成

#### 等待消息出现在聊天记录中（OCR 方式）

```powershell
python scripts\winguictl.py wait text --window-id <wx_window_id> "你好，这是测试消息" --timeout 5
```

#### 完整示例：向文件传输助手发送消息

##### 步骤1：获取微信主窗口ID

```powershell
python scripts\winguictl.py window list
```

假设微信窗口ID为 4399352。

##### 步骤2：聚焦微信窗口

```powershell
python scripts\winguictl.py window --window-id 4399352 focus
```

##### 步骤3：获取UIA快照，找到文件传输助手

```powershell
python scripts\winguictl.py snapshot --window-id 4399352 uia --skip-actions --skip-state
```

找到 `session_item_文件传输助手` 的 `runtime_id`。

##### 步骤4：点击文件传输助手打开聊天窗口

> ⚠️ **注意**：`uia-control invoke` 对微信控件可能无效，推荐使用 `action click`。

```powershell
python scripts\winguictl.py action --window-id 4399352 click --element-id <file_transfer_runtime_id>
```

##### 步骤5：等待聊天输入框出现

```powershell
python scripts\winguictl.py wait uia --window-id 4399352 --automation-id chat_input_field --timeout 3
```

##### 步骤6：获取聊天输入框的 runtime_id

```powershell
python scripts\winguictl.py find --window-id 4399352 uia --automation-id chat_input_field
```

假设 `runtime_id` 为 `42-4399352-4--2147482732`。

##### 步骤7：设置消息内容

```powershell
python scripts\winguictl.py uia-control --window-id 4399352 --element-id "42-4399352-4--2147482732" set-text "收到"
```

##### 步骤8：发送消息

```powershell
python scripts\winguictl.py action --window-id 4399352 hotkey --keys "{ALT}" "{S}"
```

##### 步骤9：等待消息发送完成

```powershell
python scripts\winguictl.py wait uia --window-id 4399352 --text "收到" --control-type ListItem --timeout 5
```

#### 长文本处理（超过2000字）

##### 创建包含长文本的临时文件

```powershell
$longText = "...超过2000字的文本..."
$tempFile = "$env:TEMP\LongText.txt"
$longText | Out-File -FilePath $tempFile -Encoding UTF8
```

##### 将文件复制到剪贴板并粘贴

需借助 Python 脚本或外部工具将文件复制到剪贴板，然后粘贴到微信输入框。

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{CTRL}" "{V}"
```

##### 等待文件加载并发送

```powershell
python scripts\winguictl.py wait sleep 1000
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{ALT}" "{S}"
```

## 发送文件

> **推荐方式**：使用剪贴板方法发送文件，比通过文件选择对话框更稳定可靠。

### 方式A：剪贴板方法（推荐）

#### 步骤1：激活聊天输入框

操作方法同前

#### 步骤2：将文件复制到剪贴板

```powershell
python scripts\winguictl.py clipboard copy-files "D:\path\to\file.pdf"
```

#### 步骤3：在聊天窗口中粘贴

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{CTRL}" "{V}"
```

#### 步骤4：等待文件加载后发送

##### 等待文件预览加载

```powershell
python scripts\winguictl.py wait sleep 3000
```

##### 发送

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{ALT}" "{S}"
```

##### 等待发送完成

```powershell
python scripts\winguictl.py wait sleep 5000
```

### 方式B：通过发送文件按钮（不推荐）

略

### 发送成功验证

#### 方式1：检查会话列表中的文件状态

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "文件"/"图片" --control-type ListItem
```

#### 方式2：通过UIA快照检查聊天记录中是否有文件消息

```powershell
python scripts\winguictl.py snapshot --window-id <wx_window_id> uia --skip-actions --skip-state
```

查找包含文件名的 `ListItem`。

### 发送文件注意事项

1. **文件大小限制**：单文件不超过 1GB
2. **等待时间**：大文件需要更长的加载和发送时间
3. **网络状态**：确保网络连接正常
4. **避免重复发送**：发送前确认文件未发送过

## 发送语音（4.1.9+ 版本支持）

### 步骤1：打开聊天窗口

参见 [window.md](./window.md) 中的窗口定位与激活方法

### 步骤2：找到"发语音"按钮并点击

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "发语音" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <audio_btn_element_id>
```

### 步骤3：播放音频到虚拟音频设备（需配置 VB-Cable 等虚拟声卡）

使用 `sounddevice` 播放音频，同时微信录制。

### 步骤4：点击结束录音（再次点击语音按钮或等待自动结束）

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <audio_btn_element_id>
```

## @群成员

### 输入 @ 符号

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> type --text "@"
```

### 等待成员选择框弹出

```powershell
python scripts\winguictl.py wait sleep 500
```

### 输入成员昵称筛选

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> type --text "成员昵称"
```

### 按 Enter 选择

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{ENTER}"
```

### @所有人

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> type --text "@所有人"
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{ENTER}"
```

## 发起接龙

### 步骤1：打开群聊窗口

参见 [window.md](./window.md) 中的窗口定位与激活方法，然后通过会话列表或搜索打开目标群聊。

### 步骤2：输入 #接龙

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> type --text "#接龙"
```

### 步骤3：按 Down + Enter 触发接龙窗口

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{DOWN}"
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{ENTER}"
```

### 步骤4：等待接龙窗口弹出，填写内容

#### 等待接龙窗口弹出

```powershell
python scripts\winguictl.py wait sleep 1000
```

#### 或者等待接龙窗口出现

```powershell
python scripts\winguictl.py wait window "接龙" --timeout 3
```

#### 填写内容

使用 `snapshot` 找到接龙窗口，填写主题、示例、描述等。

## 获取聊天记录

### 步骤1：打开好友聊天窗口

参见上方 [## 打开联系人/群聊聊天窗口](#打开联系人群聊聊天窗口) 打开目标好友的聊天窗口。

### 步骤2：点击右上角"聊天记录"按钮

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "聊天记录" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <history_btn_element_id>
```

### 步骤3：等待聊天记录窗口弹出

```powershell
python scripts\winguictl.py wait uia --window-id <wx_window_id> --text "搜索" --control-type Edit --timeout 3
```

### 步骤4：使用 snapshot 或 find 遍历聊天记录列表

```powershell
python scripts\winguictl.py snapshot --window-id <history_window_id> uia
```

### 步骤5：滚动加载更多记录

```powershell
python scripts\winguictl.py action --window-id <history_window_id> scroll --direction down --amount 3
```

## 检查新消息

### 步骤1：确保在会话列表界面

```powershell
python scripts\winguictl.py window --window-id <wx_window_id> focus
```

### 步骤2：使用 OCR 扫描左侧会话列表中的新消息提示

```powershell
python scripts\winguictl.py snapshot --window-id <wx_window_id> ocr
```

查找包含 `"[数字]条"` 或 `"[数字]"` 的文本（根据语言不同）。

### 步骤3：点击有新消息的好友

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> ocr "[3条]"
```

使用返回的 `element_id` 点击。

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <msg_element_id>
```

### 步骤4：等待新消息出现

#### 等待新消息提示出现（OCR 方式）

```powershell
python scripts\winguictl.py wait ocr --window-id <wx_window_id> "[1条]" --timeout 60
```

#### 等待新消息提示消失（表示已读）

```powershell
python scripts\winguictl.py wait ocr --window-id <wx_window_id> "[1条]" --disappear --timeout 5
```

## 等待消息发送完成

### 发送消息后，等待输入框清空

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> type --text "测试消息"
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{ALT}" "{S}"
```

### 等待消息出现在聊天记录中

```powershell
python scripts\winguictl.py wait text --window-id <wx_window_id> "测试消息" --timeout 5
```

---

## 最佳实践

### 控件操作方法选择

微信的 UIA 控件对 `invoke` 方法支持有限，建议按以下优先级选择操作方法：

| 优先级 | 方法 | 适用场景 | 可靠性 |
|--------|------|----------|--------|
| 1 | `action click` | 点击按钮、列表项等控件 | ⭐⭐⭐⭐⭐ 最可靠 |
| 2 | `action hotkey` | 系统级操作（粘贴、发送等） | ⭐⭐⭐⭐⭐ 最可靠 |
| 3 | `uia-control set-text` | 文本输入 | ⭐⭐⭐⭐ 可靠 |
| 4 | `uia-control invoke` | 微信控件支持不完善 | ⭐⭐ 不推荐 |

**示例对比**：

#### 推荐：使用 action click 点击控件

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <element_id>
```

#### 不推荐：使用 uia-control invoke 点击联系人（可能无效）

```powershell
python scripts\winguictl.py uia-control --window-id <wx_window_id> --element-id <id> invoke
```

### 等待时机的重要性

UI 状态更新需要时间，特别是文件操作和网络传输。关键操作后必须添加等待时间：

| 操作类型 | 建议等待时间 | 说明 |
|----------|--------------|------|
| 搜索联系人后 | 1500ms | 等待搜索结果加载 |
| 点击联系人后 | 1500ms | 等待聊天窗口打开 |
| 文件粘贴后 | 3000ms | 等待文件预览加载 |
| 文件发送后 | 5000ms | 等待上传完成 |
| 普通消息发送后 | 1000ms | 等待消息显示 |
