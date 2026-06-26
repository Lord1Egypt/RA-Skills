# 🔍 zhida-content

> 知乎内容搜索与分析工具。搜索话题、热度分析、选题推荐。

## 功能

- **话题搜索** — 按关键词搜索知乎问题
- **热榜获取** — 实时获取知乎热榜
- **机会评分** — 高价值问题识别（关注多+回答少=蓝海）
- **选题推荐** — 按机会评分排序，推荐最佳创作目标
- **内容方向** — 每个问题给出具体写作建议

## 快速开始

```bash
# 获取热榜
python3 scripts/fetch_zhida.py --hot --limit 10

# 搜索话题
python3 scripts/fetch_zhida.py --search "AI副业"

# 选题推荐（最佳机会）
python3 scripts/fetch_zhida.py --topic "AI" --limit 20
```

## 机会评分说明

- 🟢 蓝海：无回答，先发优势最大
- 🟢 高机会：回答少+关注多
- 🟡 中机会：竞争适中
- 🔴 竞争激烈：回答多但流量大

## 安装

```bash
# OpenClaw 用户直接安装
clawhub install freedompixels/zhida-content

# 或手动复制到 skills 目录
cp -r zhida-content ~/.qclaw/skills/
```
