---
name: review-radar
description: 显示器评测视频情报提取。给 OpenClaw 一个 B 站/YouTube 评测视频链接，自动转写口播音频并产出结构化评测情报卡（实测数据、优缺点、博主结论、竞品提及），也可批量处理多个链接并汇总。当用户提到"总结评测视频""显示器评测报告""批量看评测""评测情报"时使用。
---

# Review Radar Skill

调用本机 Review Radar 服务（localhost:8787），把评测视频变成结构化情报。

## 前置检查

先确认服务在线：`bash scripts/health.sh`
若不在线，提示用户启动：`cd <review-radar目录> && python cli.py serve`

## 常用操作

1. **单个视频出报告**（同步等待结果）：
   `bash scripts/submit.sh <视频URL>`
   输出 Markdown 情报卡。视频较长时可能需 1-3 分钟（字幕直取通常秒级）。

2. **批量处理**：
   `bash scripts/batch.sh <URL1> <URL2> ...`
   提交后异步执行；用 `bash scripts/status.sh <job_id>` 逐个查询，
   全部 done 后用 `bash scripts/report.sh <job_id>` 逐个取回，再汇总对比。

3. **手动文本兜底**（视频接口失效时）：
   `bash scripts/submit_text.sh <文本文件路径> [标题]`
   文本支持 `[mm:ss] 内容` 格式带时间戳。

4. **报告库检索**：
   `bash scripts/list_reports.sh [产品型号关键词]`

## 输出解读

- 报告每个数据点带原文引用和时间戳回跳链接，✅=已通过证据校验
- job.status 为 `degraded` 表示多条引用未通过校验，采信度需打折
- 转写来源 source: caption(字幕直取) > audio_asr(本地ASR) > manual(手动文本)

## 聚合建议

拿到多个报告后，按产品型号分组，生成「共识/分歧矩阵」：
哪些实测指标多个博主一致、哪些观点存在分歧——这是给产品/研发最有价值的产出。
