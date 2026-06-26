# 自动回复与消息监听

## 监听单个聊天窗口消息

### 步骤1：打开独立聊天窗口（双击会话列表中的好友）

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "好友备注名" --control-type ListItem
python scripts\winguictl.py action --window-id <wx_window_id> double-click --element-id <friend_element_id>
```

### 步骤2：获取独立聊天窗口 ID

```powershell
python scripts\winguictl.py window list
```

### 步骤3：最小化窗口（可选，方便后台监听）

```powershell
python scripts\winguictl.py window --window-id <dialog_window_id> minimize
```

### 步骤4：循环检查新消息

```powershell
# 使用 snapshot 或 OCR 定期检查最后一条消息的变化
# 记录初始最后一条消息的 runtime_id 或文本内容

# 示例：每分钟检查一次
for ($i = 0; $i -lt 10; $i++) {
    Start-Sleep -Seconds 6
    python scripts\winguictl.py snapshot --window-id <dialog_window_id> uia --skip-actions
    # 比较最后一条 ListItem 的 runtime_id 或文本，判断是否为新消息
}
```

## 自动回复实现思路

```powershell
# 自动回复需要结合外部脚本实现回调逻辑：
# 1. 使用 winguictl 监听消息
# 2. 检测到新消息后，调用外部处理函数生成回复内容
# 3. 使用 winguictl 发送回复

# 示例流程：
# while (监听中) {
#     $lastMessage = 获取当前最后一条消息文本
#     if ($lastMessage -ne $previousMessage) {
#         $reply = python my_reply_bot.py "$lastMessage"  # 调用回复生成逻辑
#         python scripts\winguictl.py action --window-id <dialog_window_id> type --text $reply
#         python scripts\winguictl.py action --window-id <dialog_window_id> hotkey --keys "{ALT}" "{S}"
#         $previousMessage = $lastMessage
#     }
#     Start-Sleep -Seconds 2
# }
```

## 开启监听模式（防止息屏）

```powershell
# 使用 Windows API 阻止屏幕关闭
# PowerShell 调用 kernel32.dll SetThreadExecutionState
$code = @"
[DllImport("kernel32.dll")]
public static extern uint SetThreadExecutionState(uint esFlags);
"@
$kernel32 = Add-Type -MemberDefinition $code -Name "Kernel32" -PassThru
$ES_DISPLAY_REQUIRED = 0x00000002
$ES_CONTINUOUS = 0x80000000
$kernel32::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_DISPLAY_REQUIRED)

# 恢复正常（关闭监听模式）
$kernel32::SetThreadExecutionState($ES_CONTINUOUS)
```
