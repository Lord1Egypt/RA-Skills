# 小红书搬运 Skill - 参考文档

## 常用账号

| 账号名称 | 小红书ID | 主页URL |
|---------|---------|---------|
| 学未教育（上海） | 64902d2d000000001c0294eb | https://www.xiaohongshu.com/user/profile/64902d2d000000001c0294eb |
| 西安学未教育 | 652417a1000000002b0010e7 | https://www.xiaohongshu.com/user/profile/652417a1000000002b0010e7 |

## 发布平台配置

### Facebook (Meta Business Suite)
- 主页ID: 797431390121236
- 主页名: Easy Talk
- URL: https://business.facebook.com/latest/?asset_id=797431390121236

### WordPress
- Blog ID: 252834205
- 站点: https://studyfuture0.wordpress.com
- API: https://public-api.wordpress.com/wp/v2/sites/252834205/posts

## 图片处理命令

```bash
# 下载图片（带 Referer）
curl -H "Referer: https://www.xiaohongshu.com/" -o image.jpg "URL"

# webp 转 jpg
python3 -c "
from PIL import Image
img = Image.open('input.webp').convert('RGB')
img.save('output.jpg', 'JPEG', quality=95)
"
```

## macOS 文件对话框自动化

```bash
osascript << 'EOF'
tell application "System Events"
    tell process "com.apple.appkit.xpc.openAndSavePanelService"
        set frontmost to true
        keystroke "g" using {command down, shift down}
        delay 1
        keystroke "/tmp/openclaw/uploads/"
        keystroke return
        delay 0.5
        keystroke "a" using command down
        keystroke return
    end tell
end tell
EOF
```

## 已验证的发布流程

1. 小红书 → 进入账户主页 → 点击日记
2. 下载图片到 `~/Downloads/铁头/[账号]/[标题]/`
3. 复制到 `/tmp/openclaw/uploads/`
4. Meta Business Suite → 添加照片 → osascript 操作
5. WordPress API → 发布文章