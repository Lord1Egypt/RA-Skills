# 微博热点日报

获取微博热搜榜单，智能分类热点话题，生成分段式结构化日报。

## 开源

- https://github.com/renyuzhuo/WeiboHotSkills

## 功能特性

- 从微博热搜源获取最新榜单
- 智能分类热点（财经科技/社会民生/文体娱乐/网络热点）
- 过滤政治敏感话题
- 分段展示不同类型热点

## 使用方法

```
用户：微博热点日报
用户：今天的微博热搜
用户：生成微博热点日报
```

## 输出格式

```
【微博热点日报 | YYYY-MM-DD】

📊 财经科技
- 热点1
- 热点2

📰 社会民生
- 热点1
- 热点2

🎬 文体娱乐
- 热点1
- 热点2

🔥 网络热点
- 热点1
- 热点2

---
by OpenClaw
```

## 安装

```bash
# 解压到 skills 目录
cd ~/.openclaw/skills
tar -xzvf weibo-hot-daily.tar.gz
```

## 文件说明

- `SKILL.md` - 技能说明文档
- `scripts/weibo_hot_daily.py` - Python 辅助脚本
- `README.md` - 本文件

## 依赖

- Python 3
- curl

## 版本

v1.1.1 (2026-03-31)
- 初始版本
