# 小红书搬运踩坑记录

## 🔴 必须先进入目标账户主页

**错误：** 直接在小红书首页/推荐页点击日记下载
**正确：** 先进入目标账户主页，再在主页中点击日记

```
正确流程：
小红书首页 → 搜索账户名 → 进入账户主页 → 点击日记
```

## 🔴 图片目录不要混用

| 目录 | 用途 | 说明 |
|------|------|------|
| `~/Downloads/铁头/[账号]/[标题]/` | **永久保存** | 日记原始内容 |
| `/tmp/openclaw/uploads/` | **临时上传** | 发布时临时存放，每次清空 |

**教训：** 不要用上传目录保存日记，多任务时容易混乱

## 🔴 每次发布前必须清空上传目录

```bash
rm -rf /tmp/openclaw/uploads/*
```

## 🔴 macOS 文件对话框属于独立进程

**错误：** 用 `tell process "Google Chrome"` 操作文件对话框
**正确：** 用 `tell process "com.apple.appkit.xpc.openAndSavePanelService"`

## 🔴 WordPress 换行符需转换

**错误：** 直接发送带换行符的内容，JSON 解析失败
**正确：** 换行符转换为 `<br/>` 或 `<p>` 标签

## 🔴 图片下载需带 Referer

```bash
curl -H "Referer: https://www.xiaohongshu.com/" -o image.jpg "$URL"
```

## 🔴 webp 格式需转换

小红书部分图片是 webp 格式，WordPress 不支持，需转换为 jpg