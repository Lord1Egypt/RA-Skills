# 通讯录与联系人操作

## 打开通讯录

```powershell
# 点击左侧"通讯录"按钮
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "通讯录" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <contacts_element_id>
```

## 获取好友列表

### 步骤1：打开通讯录

```powershell
```

### 步骤2：获取通讯录列表控件（List）

```powershell
python scripts\winguictl.py snapshot --window-id <wx_window_id> uia
```

### 步骤3：遍历 ListItem 获取好友名称

```powershell
# 使用 find 查找所有 ListItem
python scripts\winguictl.py find --window-id <wx_window_id> uia --control-type ListItem
```

### 步骤4：滚动加载更多好友

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> scroll --direction down --amount 3
```

## 获取好友个人资料

### 步骤1：在通讯录或会话列表中点击好友

```powershell
```

### 步骤2：点击打开好友资料（可能需要右键或点击头像）

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> right-click --element-id <friend_element_id>
```

### 步骤3：选择"查看资料"或类似选项

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "查看资料" --control-type MenuItem
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <menu_element_id>
```

### 步骤4：使用 snapshot 获取资料面板上的文本信息

```powershell
python scripts\winguictl.py snapshot --window-id <profile_window_id> uia
```

## 获取共同群聊

### 步骤1：打开好友资料页

```powershell
```

### 步骤2：找到"共同群聊"区域

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "共同群聊" --control-type Text
```

### 步骤3：点击展开查看全部

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "查看全部" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <view_all_element_id>
```

### 步骤4：记录弹出的群聊列表

```powershell
python scripts\winguictl.py snapshot --window-id <wx_window_id> uia
```

## 添加新朋友

### 步骤1：点击"添加朋友"按钮

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "添加朋友" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <add_btn_element_id>
```

### 步骤2：在搜索框输入微信号/手机号

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --control-type Edit
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <search_element_id>
python scripts\winguictl.py action --window-id <wx_window_id> type --text "wxid_xxx"
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{ENTER}"
```

### 步骤3：点击"添加到通讯录"

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "添加到通讯录" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <add_contact_element_id>
```

### 步骤4：填写验证信息（可选）

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --control-type Edit
python scripts\winguictl.py action --window-id <wx_window_id> type --text "你好，我是..."
```

### 步骤5：点击"确定"

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "确定" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <confirm_element_id>
```

## 检查新的朋友（好友验证）

### 步骤1：打开通讯录，点击"新的朋友"

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "新的朋友" --control-type ListItem
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <new_friends_element_id>
```

### 步骤2：遍历验证请求列表

```powershell
python scripts\winguictl.py snapshot --window-id <wx_window_id> uia
```

### 步骤3：点击"前往验证"

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "前往验证" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <verify_element_id>
```

### 步骤4：点击"确定"通过验证

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "确定" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <confirm_element_id>
```
