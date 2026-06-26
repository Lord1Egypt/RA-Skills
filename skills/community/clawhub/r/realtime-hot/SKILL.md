---
name: realtime-hot
description: 获取并整理多平台实时热点新闻，按跨平台热度共识筛选，输出高热度事件的简报。
---

# 实时热点 Skill

## 执行步骤

1. 抓取数据：`node ./scripts/index.js`
   - 结果写入 `./scripts/hot-data.json`（微博/抖音/头条/百度/知乎/腾讯六平台各前50条）

2. 读取并聚类：`node ./scripts/format.js`
   - 读取 hot-data.json
   - Jaccard 聚类（2-gram，阈值0.10）
   - 过滤：百度置顶稿、微博广告位、"总书记/主席/领导人"相关
   - 标题优先选非微博、5-20字最短
   - 输出固定格式 markdown 到 stdout

3. 发送：用 message 工具发送 format.js 的 stdout 输出
   - action=send
   - channel=feishu

## 强制规则

- 模型只负责运行脚本，不得自行生成或修改格式
- 只用 exec 和 read，禁止 browser、agent-browser、web_fetch
