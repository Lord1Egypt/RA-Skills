# Save Article Universal

通用微信公众号文章保存工具

## 快速开始

### 1. 克隆或下载

```bash
git clone <this-repo>
cd save-article-universal
```

### 2. 配置

复制配置文件模板并修改：

```bash
cp config.json.example config.json
```

编辑 `config.json`：

```json
{
  "save_method": "local",
  "save_path": "/Users/你的用户名/Documents/Articles"
}
```

### 3. 使用

```bash
python3 save_article.py "https://mp.weixin.qq.com/s/xxx"
```

## 使用方式

### 命令行参数

```bash
# 指定保存目录
python3 save_article.py "链接" --output "/path/to/folder"

# 指定保存方法
python3 save_article.py "链接" --method obsidian
```

### 环境变量

```bash
export SAVE_PATH="/Users/你的用户名/Documents/Articles"
export FILE_NAMING=title_date

python3 save_article.py "链接"
```

## 保存方法

| 方法 | 说明 |
|------|------|
| `local` | 保存到本地文件夹 |
| `obsidian` | 保存到 Obsidian vault |
| `miaoyan` | 保存到 Miaoyan（默认） |
| `notion` | 同步到 Notion（需配置 API） |

## 文件命名

| 方式 | 示例 |
|------|------|
| `title` | `文章标题.md` |
| `title_date` | `文章标题_2026-03-24.md` |
| `date_title` | `2026-03-24_文章标题.md` |
| `timestamp` | `1700000000_文章标题.md` |

## 输出示例

```markdown
---
title: GitHub一周神级项目盘点
url: https://mp.weixin.qq.com/s/xxx
date: 2026-03-24
---

# GitHub一周神级项目盘点

## 📌 要点

本文介绍了本周 GitHub 最火的 5 大项目...

---

## 正文

[完整文章内容]

---

## 原文

[GitHub一周神级项目盘点](https://mp.weixin.qq.com/s/xxx)

*保存时间: 2026-03-24*
```

## 许可证

MIT
