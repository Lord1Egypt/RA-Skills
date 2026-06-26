# 微信设置

## 打开设置

```powershell
# 点击"更多" -> "设置"
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "更多" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <more_element_id>
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "设置" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <settings_element_id>

# 等待设置窗口弹出
Start-Sleep -Seconds 1.5
```

## 修改主题样式

### 步骤1：打开设置窗口

```powershell
```

### 步骤2：点击"通用"

```powershell
python scripts\winguictl.py find --window-id <settings_window_id> uia --text "通用" --control-type Button
python scripts\winguictl.py action --window-id <settings_window_id> click --element-id <general_element_id>
```

### 步骤3：点击外观/主题设置按钮

```powershell
python scripts\winguictl.py find --window-id <settings_window_id> uia --text "跟随系统" --control-type Text
# 点击其父元素中的按钮
python scripts\winguictl.py action --window-id <settings_window_id> click --element-id <theme_btn_element_id>
```

### 步骤4：使用键盘选择主题

```powershell
# 先回到顶部
python scripts\winguictl.py action --window-id <settings_window_id> press-key --key "{UP}"
# 0:跟随系统(已在顶部), 1:浅色模式(按1次Down), 2:深色模式(按2次Down)
python scripts\winguictl.py action --window-id <settings_window_id> press-key --key "{DOWN}"
python scripts\winguictl.py action --window-id <settings_window_id> press-key --key "{ENTER}"
```

## 修改语言

### 步骤1：打开设置 -> 通用

```powershell
```

### 步骤2：点击语言设置

```powershell
python scripts\winguictl.py find --window-id <settings_window_id> uia --text "简体中文" --control-type Text
python scripts\winguictl.py action --window-id <settings_window_id> click --element-id <lang_btn_element_id>
```

### 步骤3：使用键盘选择语言

```powershell
# 顺序：跟随系统, 简体中文, English, 繁體中文
python scripts\winguictl.py action --window-id <settings_window_id> press-key --key "{UP}"
# 1:简体中文(Down 1), 2:English(Down 2), 3:繁體中文(Down 3)
python scripts\winguictl.py action --window-id <settings_window_id> press-key --key "{DOWN}"
python scripts\winguictl.py action --window-id <settings_window_id> press-key --key "{ENTER}"
```

### 步骤4：确认重启提示

```powershell
python scripts\winguictl.py find --window-id <settings_window_id> uia --text "确定" --control-type Button
python scripts\winguictl.py action --window-id <settings_window_id> click --element-id <confirm_element_id>
```

## 修改自动下载文件大小

### 步骤1：打开设置 -> 通用

```powershell
```

### 步骤2：找到自动下载设置区域

```powershell
python scripts\winguictl.py snapshot --window-id <settings_window_id> uia
```

### 步骤3：点击输入框修改大小

```powershell
python scripts\winguictl.py find --window-id <settings_window_id> uia --control-type Edit
python scripts\winguictl.py action --window-id <settings_window_id> click --element-id <size_edit_element_id>
python scripts\winguictl.py action --window-id <settings_window_id> hotkey --keys "{CTRL}" "{A}"
python scripts\winguictl.py action --window-id <settings_window_id> press-key --key "{DELETE}"
python scripts\winguictl.py action --window-id <settings_window_id> type --text "1024"
```

## 退出登录

### 步骤1：打开设置 -> 账号设置

```powershell
python scripts\winguictl.py find --window-id <settings_window_id> uia --text "账号设置" --control-type Button
python scripts\winguictl.py action --window-id <settings_window_id> click --element-id <account_element_id>
```

### 步骤2：点击"退出登录"

```powershell
python scripts\winguictl.py find --window-id <settings_window_id> uia --text "退出登录" --control-type Button
python scripts\winguictl.py action --window-id <settings_window_id> click --element-id <logout_element_id>
```

### 步骤3：确认

```powershell
python scripts\winguictl.py find --window-id <settings_window_id> uia --text "确定" --control-type Button
python scripts\winguictl.py action --window-id <settings_window_id> click --element-id <confirm_element_id>
```
