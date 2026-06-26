# 小红书笔记搬运 Skill

自动化搬运小红书笔记到 Facebook 和 WordPress。

## 功能

- 小红书笔记下载（图片 + 文字）
- 图片处理（webp → jpg，带 Referer）
- Facebook Meta Business Suite 自动发布
- WordPress REST API 发布
- macOS 文件对话框自动化

## 安装

```bash
clawhub install xiaohongshu-搬运
```

## 使用

### 基本流程

1. 进入小红书目标账户主页
2. 点击日记，提取内容
3. 下载图片到本地
4. 发布到 Facebook
5. 发布到 WordPress

### 目录结构

```
~/Downloads/铁头/[账号主体]/[日记标题]/
├── 内容.txt
└── 图片*.jpg
```

### 发布平台

| 平台 | 方式 |
|------|------|
| Facebook | Meta Business Suite + osascript |
| WordPress | REST API |

## 脚本

- `scripts/download_images.sh` - 图片下载
- `scripts/prepare_upload.py` - 上传准备
- `scripts/wp_publish.py` - WordPress 发布

## 参考

- `references/platforms.md` - 平台配置信息
- `references/pitfalls.md` - 踩坑记录

## 版本

- 1.0.0 (2026-03-31) - 首次发布

## 作者

铁铁团队 - 铁头 🤖