# 降 AI 改写与复检

普通用户只需说：“帮我降低 AI 率，改完检测一下，看看需不需要重试。”下面命令由 AI 助手处理。使用现有优稿连接，缺 Key 时打开 https://yougao.top/app/api-keys ，注册或登录后点「复制给 AI」。不要求用户配置环境。

默认以 AI 特征不超过20%为目标，最多首次改写加额外两轮；每次额外重试先询问。人工特征、疑似 AI、AI 特征始终分别报告。比例不是作者身份或原创性证明，改写效果不能保证。

```text
python scripts/refine.py prepare --text-file article.md --dir output/refine-001
python scripts/refine.py run --dir output/refine-001 --approved
```

用户已授权自动处理时：

```text
python scripts/refine.py prepare --text-file article.md --target 20 --retry auto --max-retries 2 --max-points 30 --dir output/refine-002
python scripts/refine.py run --dir output/refine-002 --approved
```

`--max-retries` 是首次改写之外的次数，0–5，默认2。`--max-points` 包含原文检测、所有改写与复检；省略不另设总上限，0禁止消费。首次/额外一轮估算基于原文字数，之后每项按真实正文预览，预算不足不启动。剩余预算可能只够改写而不够复检，此时候选会标记未复检，最佳稿仍取已检测版本。

严格模式把疑似也计入目标：`--metric combined`。通常使用 `--metric ai` 与网站 AI 特征口径一致；AI 达标但疑似很高时必须明确告诉用户，不能宣称“全人工”。

## 接续与重试

每次脚本最多等待60秒。AI 工具在本机推进流程，服务端执行每个已提交任务。AI 工具关掉后，已提交的操作可继续，未提交的下一步不会凭空运行；再次使用同一目录接续即可。

```text
python scripts/refine.py status --dir output/refine-001
python scripts/refine.py resume --dir output/refine-001
```

`resume` 查询或接续已授权的流程，不会批准等待中的新一轮。`awaiting_retry` 时给用户前后对比、预计额外一轮费用，询问是否再试。用户已明确授权自动重试，应在首次 prepare 选择 auto，不必每轮再问。

```text
python scripts/refine.py retry --dir output/refine-001 --round 2
python scripts/refine.py finish --dir output/refine-001
```

这两条是二选一；round 使用 status 返回的 nextRound，不凭空递增。同一轮批准可安全重放，不会多授权下一轮。即使用户允许重试，无改善、达标、次数用完、未知结果、报告错误和数字变化也会停止，不为消耗完次数继续改。

`needs_attention` 先处理 detail；429遵守 retryAfter。未提交的过期计划可 `reprice --dir 原目录` 重新报价，然后核对新费用，用 run --approved；任何尝试提交过的计划禁止换编号。Key失效可先在官网恢复原Key状态，不能换账号重跑未知交易。不会自动撤销Key或修改余额。

## 成果

- index.html：可本机打开的前后对比与文件入口。
- article.md：检测指标最优的有效版本；有可能是原文。
- original.md：完整原稿，独立保留。
- round-N.md、round-N-detection.txt：每轮真实稿件与三类占比，含实际送检正文。
- candidate-unverified.md：仅异常或预算中断有未完成复检的候选时提供，不能冒称已达标。
- report.txt、result.json：停止原因、已核清费用、待核对操作与网页继续编辑入口。

所有文件都写入新的 delivery-* 目录。`export --dir 原目录` 离线导出，无需Key，不扣点，不覆盖用户手动修改的交付文件。过程目录中的 refine.json 和各步骤 task.json/result.json 是恢复依据；不要删除或修改其中的原稿、预算、幂等编号。

只处理完整文本，不引入图像、发布或其他付费步骤。若用户提供图文，保留优稿里的原稿与排版，不能用文本流程丢弃图片后重建。
