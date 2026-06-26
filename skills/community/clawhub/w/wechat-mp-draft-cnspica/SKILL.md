---
name: wechat-mp-draft
description: 将本地 Markdown 文章上传到微信公众号草稿箱。当用户提到"上传文章到公众号"、"发布到微信公众号"、"推送到公众号草稿"等场景时应使用本技能。本技能通过调用微信公众平台 API，自动完成 Markdown 转 HTML、封面图生成/上传、创建草稿等全流程操作。
---

# 微信公众号草稿上传技能

## 技能概述

本技能将本地 Markdown 文件自动转换为微信公众号格式的 HTML，上传封面图素材，并通过微信公众平台 API 创建草稿，最终文章出现在公众号后台「草稿箱」中等待发布。

## 使用前提

在执行前，向用户确认以下信息：

1. **AppID** 和 **AppSecret**（公众平台后台 → 开发 → 基本配置）
2. **Markdown 文件路径**（本地绝对路径）
3. **封面图路径**（可选；不提供则自动生成绿色渐变占位图）
4. **作者名称**（可选）
5. **文章摘要**（可选，不填则自动截取正文前 100 字）

> ⚠️ **IP 白名单**：若运行环境 IP 未加入白名单，API 会返回 40164 错误。提示用户在公众平台 → 开发 → 基本配置 → IP白名单中添加当前出口 IP。

## 执行流程

### Step 1：检查 Python 环境

```bash
python --version
```

若 Python 不可用，提示用户安装 Python 3.7+。

可选安装 Pillow（用于生成高质量封面图）：
```bash
pip install Pillow
```
不安装 Pillow 也可运行（会自动下载免费占位图）。

### Step 2：运行上传脚本

脚本位于本技能的 `scripts/upload_draft.py`。

**基础用法（自动生成封面）：**
```bash
python scripts/upload_draft.py \
  --appid "YOUR_APPID" \
  --secret "YOUR_APPSECRET" \
  --md "C:/path/to/article.md" \
  --author "作者名"
```

**指定封面图：**
```bash
python scripts/upload_draft.py \
  --appid "YOUR_APPID" \
  --secret "YOUR_APPSECRET" \
  --md "C:/path/to/article.md" \
  --cover "C:/path/to/cover.jpg" \
  --author "作者名" \
  --digest "文章摘要，最多120字"
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--appid` | ✅ | 公众号 AppID |
| `--secret` | ✅ | 公众号 AppSecret |
| `--md` | ✅ | Markdown 文件绝对路径 |
| `--cover` | ❌ | 封面图路径（JPG/PNG），不填则自动生成 |
| `--author` | ❌ | 文章作者 |
| `--digest` | ❌ | 摘要（最多120字），不填则截取正文 |

### Step 3：验证结果

脚本成功输出示例：
```
✅ 获取 access_token 成功（有效期 7200 秒）
✅ 封面图上传成功，media_id = xxx
✅ 草稿创建成功！草稿 media_id = yyy
🎉 完成！文章《智慧养老正式进入AI时代》已成功上传至草稿箱。
```

告知用户登录 [微信公众平台](https://mp.weixin.qq.com/) → **内容** → **草稿箱** 查看文章。

## 常见问题处理

| 错误 | 原因 | 解决 |
|------|------|------|
| `40001` access_token 无效 | AppID/AppSecret 错误 | 重新确认凭证 |
| `40164` IP 不合法 | 当前 IP 不在白名单 | 在公众平台添加 IP |
| `40007` media_id 无效 | 封面图上传失败 | 检查图片格式和大小（≤10MB） |
| 封面图下载失败 | 无网络或 Pillow 未装 | 手动提供一张 JPG/PNG 封面图 |

## 参考资料

详细 API 规范见 `references/wechat_api.md`。
