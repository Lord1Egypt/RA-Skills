---
name: xiaohongshu-搬运
description: 小红书笔记搬运到 Facebook 和 WordPress 的自动化流程。当用户要求搬运小红书笔记、发布小红书内容到 Facebook/WordPress 时使用。
---

# 小红书搬运 Skill

自动化搬运小红书笔记到 Facebook 和 WordPress。

## 工作流程

### 1. 小红书下载

**关键：必须先进入目标账户主页！**

```
1. 打开小红书网站
2. 进入目标账户主页（如 https://www.xiaohongshu.com/user/profile/64902d2d000000001c0294eb）
3. 在账户主页点击日记
4. 提取日记标题、内容、图片URL
```

### 2. 图片下载

```bash
# 带 Referer 头绕过防盗链
curl -H "Referer: https://www.xiaohongshu.com/" -o image.jpg "图片URL"

# webp 转 jpg（如果需要）
python3 -c "
from PIL import Image
img = Image.open('image.webp')
if img.mode == 'RGBA':
    img = img.convert('RGB')
img.save('image.jpg', 'JPEG', quality=95)
"
```

### 3. 本地保存

```
~/Downloads/铁头/[账号主体]/[日记标题]/
├── 内容.txt
└── 图片*.jpg
```

**重要区分：**
| 用途 | 目录 |
|------|------|
| 日记永久保存 | `~/Downloads/铁头/[账号主体]/[日记标题]/` |
| 发布临时上传 | `/tmp/openclaw/uploads/` |

### 4. Facebook 发布

**推荐：Meta Business Suite**

URL: `https://business.facebook.com/latest/?asset_id=797431390121236`

流程：
1. 创建帖子 → 输入文字
2. 点击"添加照片" → browser upload
3. 使用 osascript 操作 macOS 文件对话框：

```bash
osascript << 'EOF'
tell application "System Events"
    tell process "com.apple.appkit.xpc.openAndSavePanelService"
        set frontmost to true
        delay 0.5
        
        -- Command+Shift+G
        keystroke "g" using {command down, shift down}
        delay 1.0
        
        -- 输入路径
        keystroke "/tmp/openclaw/uploads/"
        delay 0.5
        
        -- 确认
        keystroke return
        delay 0.5
        
        -- 全选
        keystroke "a" using command down
        delay 0.3
        
        -- 打开
        keystroke return
    end tell
end tell
EOF
```

### 5. WordPress 发布

**REST API**

```bash
curl -X POST "https://public-api.wordpress.com/wp/v2/sites/252834205/posts" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "标题",
    "content": "内容（换行符需转换为<br/>或<p>）",
    "status": "publish"
  }'
```

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 图片下载失败 | 添加 `Referer: https://www.xiaohongshu.com/` |
| webp 无法打开 | Pillow 转换为 jpg |
| Facebook 上传卡住 | 使用 Meta Business Suite |
| WordPress JSON 解析失败 | 换行符转 `<br/>` 或 `<p>` |
| macOS 文件对话框无法操作 | 操作 `com.apple.appkit.xpc.openAndSavePanelService` 进程 |

## 账号信息

| 账号 | 小红书ID | 存放文件夹 |
|------|---------|-----------|
| 学未教育（上海） | 64902d2d000000001c0294eb | `~/Downloads/铁头/学未教育/` |
| 西安学未教育 | 652417a1000000002b0010e7 | `~/Downloads/铁头/西安学未/` |

## 发布顺序

```
Facebook → WordPress
```

**每次发布前必须清空 `/tmp/openclaw/uploads/` 目录！**

## 铁律

1. **任何数据操作必须先备份**
2. **长期任务做版本管理**
3. **所有任务进度在论坛留痕**