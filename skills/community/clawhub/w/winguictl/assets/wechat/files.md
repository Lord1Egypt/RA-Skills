# 文件操作

## 导出聊天记录中的文件

### 步骤1：打开聊天记录窗口（参考消息操作-获取聊天记录）

```powershell
```

### 步骤2：切换到"文件"标签页

```powershell
python scripts\winguictl.py find --window-id <history_window_id> uia --text "文件" --control-type TabItem
python scripts\winguictl.py action --window-id <history_window_id> click --element-id <file_tab_element_id>
```

### 步骤3：遍历文件列表，右键点击文件

```powershell
python scripts\winguictl.py find --window-id <history_window_id> uia --control-type ListItem
python scripts\winguictl.py action --window-id <history_window_id> right-click --element-id <file_element_id>
```

### 步骤4：选择"另存为"或"复制"

```powershell
python scripts\winguictl.py find --window-id <history_window_id> uia --text "另存为" --control-type MenuItem
python scripts\winguictl.py action --window-id <history_window_id> click --element-id <save_as_element_id>
```

## 导出最近文件

### 步骤1：打开"聊天文件"窗口

```powershell
# 点击"更多" -> "聊天文件"
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "更多" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <more_element_id>
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "聊天文件" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <chat_files_element_id>
```

### 步骤2：等待窗口弹出

```powershell
Start-Sleep -Seconds 1.5
```

### 步骤3：获取聊天文件窗口 ID

```powershell
python scripts\winguictl.py window list
```

### 步骤4：遍历文件列表并导出

```powershell
python scripts\winguictl.py snapshot --window-id <chatfiles_window_id> uia
```

## 导出视频

```powershell
# 微信视频存储路径（需先获取 wxid 文件夹）
# 视频路径：%WXID_FOLDER%\msg\video\YYYY-MM\
# 使用文件系统操作直接复制
Copy-Item -Path "$wxidFolder\msg\video\2025-01\*.mp4" -Destination "D:\导出视频\" -Recurse
```

## 导出聊天文件（按年月）

```powershell
# 聊天文件路径：%WXID_FOLDER%\msg\file\YYYY-MM\
Copy-Item -Path "$wxidFolder\msg\file\2025-01\*" -Destination "D:\导出文件\" -Recurse
```
