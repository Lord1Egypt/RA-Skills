# 🎬 video-finder

> 一个 OpenClaw Agent skill — 搜点学习资料看看。

ClawHub：[@xiaoka520/video-finder](https://clawhub.ai/xiaoka520/skills/video-finder)

## 功能概览

| 模块 | 说明 |
|---|---|
| 🔍 搜一搜 | 根据你的喜好搜点东西，自动过滤你不想要的 |
| 📥 下回来 | 后台拉取 + 定时看进度，开多线程跑满带宽 |
| 🎯 记喜好 | 第一次用告诉你记什么，以后自动按着来 |
| 🌐 网络检测 | 自动试能不能连上，网络不通会问你有没有代理 |
| 📊 问问看法 | 看完之后问你觉得怎么样，好的记住坏的拉黑 |
| 📝 历史记录 | 下了什么、觉得怎么样，都记着 |

## 快速开始

### 1. 安装

```bash
openclaw skills install @xiaoka520/video-finder
```

### 2. 第一次用

说点关键词就会启动了，会问你喜欢什么类型的、多长算够、哪些不要。

### 3. 大概长这样

```
你: 找点东西看看
Bot: 搜到这几个，看看哪个合胃口：
     1️⃣ [标题] — 15:20
     2️⃣ [标题] — 12:45
     你挑一个？

你: 第一个吧
Bot: 存哪个目录？
```

## 目录结构

```
~/.openclaw/skills/video-finder/
├── SKILL.md
├── LICENSE
├── README.md
├── .gitignore
├── preferences.json   ← 你的口味设定（自动生成）
├── proxy.json         ← 代理设置（自动生成）
└── history.md         ← 浏览记录（自动生成）
```

## 下载流程

1. 你点头了，后台开始拉
2. 按剩余时间动态查进度（10秒～2分钟查一次）
3. 大文件过一会儿会给你说一声到哪了
4. 下好了告诉你放哪了

## 声明
请在遵守您所在地区法律的情况下使用此skill

## 许可证
MIT
