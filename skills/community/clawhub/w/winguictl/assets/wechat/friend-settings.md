# 好友设置

## 打开聊天信息/好友设置

```powershell
# 在聊天窗口中点击右上角"聊天信息"按钮（三个点）
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "聊天信息" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <chat_info_element_id>
```

## 设置消息免打扰

### 步骤1：打开聊天信息

```powershell
```

### 步骤2：找到"消息免打扰"复选框

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "消息免打扰" --control-type CheckBox
# 获取 toggle state
python scripts\winguictl.py uia-control --window-id <wx_window_id> --element-id <mute_checkbox_id> get-toggle-state
```

### 步骤3：根据需要切换状态

```powershell
# 开启
python scripts\winguictl.py uia-control --window-id <wx_window_id> --element-id <mute_checkbox_id> toggle
# 或关闭（再次 toggle）
```

## 设置置顶聊天

```powershell
# 找到"置顶聊天"复选框
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "置顶聊天" --control-type CheckBox
python scripts\winguictl.py uia-control --window-id <wx_window_id> --element-id <pin_checkbox_id> toggle
```

## 设置折叠聊天

```powershell
# 找到"折叠该聊天"复选框（仅在开启免打扰后可用）
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "折叠该聊天" --control-type CheckBox
python scripts\winguictl.py uia-control --window-id <wx_window_id> --element-id <fold_checkbox_id> toggle
```

## 清空聊天记录

### 步骤1：打开聊天信息

```powershell
```

### 步骤2：点击"清空聊天记录"

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "清空聊天记录" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <clear_element_id>
```

### 步骤3：确认清空

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "清空" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <confirm_clear_element_id>
```
