# 收藏与笔记

## 打开收藏

```powershell
# 点击"更多" -> "收藏"
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "更多" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <more_element_id>
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "收藏" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <collections_element_id>
```

## 新建笔记

### 步骤1：打开收藏后，点击"新建笔记"

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "新建笔记" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <new_note_element_id>
```

### 步骤2：等待笔记窗口弹出

```powershell
Start-Sleep -Seconds 1
```

### 步骤3：输入笔记内容

```powershell
python scripts\winguictl.py find --window-id <note_window_id> uia --control-type Edit
python scripts\winguictl.py action --window-id <note_window_id> type --text "这是笔记内容"
```

### 步骤4：粘贴文件（可选）

```powershell
python scripts\winguictl.py action --window-id <note_window_id> hotkey --keys "{CTRL}" "{V}"
```

### 步骤5：保存（Ctrl+S）

```powershell
python scripts\winguictl.py action --window-id <note_window_id> hotkey --keys "{CTRL}" "{S}"
```

### 步骤6：分享到朋友圈（可选）

```powershell
python scripts\winguictl.py find --window-id <note_window_id> uia --text "更多" --control-type Button
python scripts\winguictl.py action --window-id <note_window_id> click --element-id <more_element_id>
python scripts\winguictl.py action --window-id <note_window_id> press-key --key "{UP}"
python scripts\winguictl.py action --window-id <note_window_id> press-key --key "{UP}"
python scripts\winguictl.py action --window-id <note_window_id> press-key --key "{ENTER}"
```

## 获取收藏链接 URL

### 步骤1：打开收藏窗口

```powershell
```

### 步骤2：双击打开链接列表

```powershell
python scripts\winguictl.py find --window-id <collections_window_id> uia --text "链接" --control-type ListItem
python scripts\winguictl.py action --window-id <collections_window_id> double-click --element-id <link_element_id>
```

### 步骤3：右键点击链接项，选择"复制链接"

```powershell
python scripts\winguictl.py action --window-id <collections_window_id> right-click --element-id <link_item_element_id>
python scripts\winguictl.py find --window-id <collections_window_id> uia --text "复制链接" --control-type MenuItem
python scripts\winguictl.py action --window-id <collections_window_id> click --element-id <copy_link_element_id>
```

### 步骤4：从剪贴板读取 URL（需外部脚本）

```powershell
```
