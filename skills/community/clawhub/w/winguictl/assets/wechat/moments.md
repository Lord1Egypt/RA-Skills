# 朋友圈操作

## 打开朋友圈

```powershell
# 点击左侧"朋友圈"按钮
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "朋友圈" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <moments_element_id>

# 等待加载
Start-Sleep -Seconds 2
```

## 发布朋友圈

### 步骤1：打开朋友圈后，点击"发表"或相机图标

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "发表" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <post_element_id>
```

### 步骤2：输入文本内容

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --control-type Edit
python scripts\winguictl.py action --window-id <wx_window_id> type --text "今天天气不错~"
```

### 步骤3：点击"发表"

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "发表" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <post_btn_element_id>
```

## 浏览好友朋友圈

### 步骤1：打开好友资料页

```powershell
```

### 步骤2：点击"朋友圈"入口

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "朋友圈" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <moments_entry_element_id>
```

### 步骤3：滚动浏览

```powershell
python scripts\winguictl.py action --window-id <moments_window_id> scroll --direction down --amount 3
```

## 点赞/评论朋友圈

### 步骤1：找到朋友圈内容下方的灰色省略号按钮

```powershell
# 使用 OCR 或图像匹配定位
python scripts\winguictl.py find --window-id <moments_window_id> image --image-path assets\ellipsis.png
python scripts\winguictl.py action --window-id <moments_window_id> click --element-id <ellipsis_element_id>
```

### 步骤2：点击"赞"或"评论"

```powershell
python scripts\winguictl.py find --window-id <moments_window_id> uia --text "赞" --control-type Button
python scripts\winguictl.py action --window-id <moments_window_id> click --element-id <like_element_id>
```

### 评论

```powershell
python scripts\winguictl.py find --window-id <moments_window_id> uia --text "评论" --control-type Button
python scripts\winguictl.py action --window-id <moments_window_id> click --element-id <comment_element_id>
python scripts\winguictl.py action --window-id <moments_window_id> type --text "赞！"
# 点击绿色发送按钮（需颜色识别或坐标点击）
```
