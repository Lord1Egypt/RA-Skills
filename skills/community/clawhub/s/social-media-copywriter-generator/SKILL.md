---
name: 自媒体文案生成器
version: 0.1.0
description: 一键生成多平台爆款文案 - 小红书/抖音/公众号/知乎
author: 小爱
dependencies: []
---

# 自媒体文案生成器

一键生成多平台爆款文案，支持小红书、抖音、公众号、知乎。

---

## 快速开始

```bash
# 生成小红书文案
python generate.py "AI 写作技巧" -p xiaohongshu

# 生成公众号文章
python generate.py "职场沟通" -p wechat -l long

# 生成标题选项
python generate.py "副业赚钱" --titles-only
```

---

## 功能特点

- 🎯 4 平台支持（小红书/抖音/公众号/知乎）
- 📝 智能文案生成
- 🏷️ 标签推荐
- 🎨 语气调节
- 📏 长度控制

---

## 用法

### 命令行

```bash
python generate.py "主题" \
  -p [平台] \
  -t [语气] \
  -l [长度] \
  -o [输出文件]
```

### 参数

| 参数 | 说明 | 默认值 |
|:---|:---|:---|
| topic | 文案主题 | 必填 |
| -p, --platform | 平台：xiaohongshu/douyin/wechat/zhihu | xiaohongshu |
| -t, --tone | 语气：自然/专业/幽默/温暖 | 自然 |
| -l, --length | 长度：short/medium/long | medium |
| -k, --keywords | 关键词列表 | 无 |
| -a, --audience | 目标受众 | 通用 |
| -o, --output | 输出文件 | 屏幕输出 |
| --titles-only | 只生成标题 | False |
| --no-tags | 不生成标签 | False |

---

## 示例

### 小红书

```bash
python generate.py "AI 工具提升效率" \
  -p xiaohongshu \
  -k AI 效率 工具 \
  -a "25-35 岁职场人" \
  -o output/xiaohongshu.md
```

### 抖音

```bash
python generate.py "美妆教程" -p douyin -t 幽默
```

### 公众号

```bash
python generate.py "职场沟通技巧" -p wechat -l long
```

### 知乎

```bash
python generate.py "如何提升学习效率" -p zhihu
```

---

## 输出格式

### 小红书
- 标题：20 字以内，含 emoji
- 正文：300-800 字，口语化
- 标签：#标签 1 #标签 2

### 抖音
- 标题：15 字以内，悬念
- 正文：100-300 字，口播稿
- 标签：#标签 1#标签 2

### 公众号
- 标题：20-30 字，可副标题
- 正文：800-2000 字，有深度
- 标签：无（或少量）

### 知乎
- 标题：问题式或直接点题
- 正文：500-1500 字，专业
- 标签：话题 1, 话题 2

---

## 开发状态

**Sprint 1 (MVP)** - 🚧 开发中

- ✅ 核心生成器
- ✅ 标签推荐
- 🚧 标题优化
- 🚧 单元测试
- 🚧 文档

**预计完成**: 2 周

---

## 技术栈

- Python 3.7+
- 标准库（无外部依赖）
- 可扩展 LLM 接入

---

## 待办事项

- [ ] 接入真实 LLM API
- [ ] 添加 Few-shot 示例
- [ ] 批量生成
- [ ] 热点追踪
- [ ] Web UI

---

## License

MIT License
