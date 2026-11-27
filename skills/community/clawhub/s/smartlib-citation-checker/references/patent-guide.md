# 专利检索与专利报告（`owl.py patent` / `owl.py patent-report`）

> 按需读取：用户说「查新 / 新颖性 / 这个方案有没有人做过 / 技术交底书 / 竞品专利 /
> 专利布局 / OA 答复 / 创新升级 / 下载专利报告」时读。
>
> **这是 CLI/HTTP 能力，不是 MCP 工具**——不要说「我用 owl_patent 工具帮你查」，
> 说「我用专利检索命令帮你查」。

## 第一步：判断用户要什么（别一上来就提交付费报告）

- 只想知道「有没有类似专利」→ **同步检索**（秒级）：
  ```
  owl.py patent --action patent_search --query "<技术方案关键词>"
  ```
  有公开号要看权利要求 / 全文 → `--action patent_detail --pn <公开号> --kind claims`；
  看相似专利 → `--action patent_similar --pn <公开号>`；
  查某公司专利画像 → `--action patent_portrait --company "<公司名>"`。
- 要**正式报告**（查新 / 交底书 / 布局）→ **异步报告**（分钟级，见下）。
  先问清标题、技术方案文本与报告类型；用户没明确类型时按「查新 = novelty」默认，其余按说法选。

## 第二步：报告类型与交付形态（先讲清，否则用户以为都能下载 Word）

| `--type` | 用途 | 交付物 |
|---|---|---|
| `novelty` | 专利查新 / 新颖性报告 | Word（docx） |
| `disclosure` | 技术交底书 | Word（docx） |
| `competitive` | 竞品专利分析 | Word（docx） |
| `roadmap` | 专利布局规划 | Word（docx） |
| `oa_answer` | OA 答复辅助 | Word（docx） |
| `idea_upgrade` | 技术创新升级 | **结构化方向清单 JSON**（无 Word，别去下 docx） |

## 第三步：先报价、用户点头、再提交

```
owl.py quote --action patent_report --params '{"report_type":"novelty","title":"<标题>"}'
```
把 `est_points` 折成钱讲给用户 → 用户同意后才执行。提交前如实说明：
「每账号同时只能跑一个报告；上游超时或失败不收费；超过 24 小时自动取消并全额退」。

## 第四步：提交与轮询

```
owl.py patent-report --op submit --type novelty --title "<标题>" --solution "<技术方案>"
# 需额外字段（竞品/subject/OA 文本等）时用 --extra-json '{"competitors":"..."}'
owl.py patent-report --op status --run-id <run_id>       # 反复查到 succeeded/failed/cancelled
owl.py patent-report --op artifact --run-id <run_id> --url "<status 里的 download_url>" --dest ./报告.docx
```

- `status` 返回 `status=succeeded` 且 `download_url` 非空时才能下载；
  `kind=json` 时产物是 `.docx` 以外的结构化清单，按 `download_url` 原样保存，
  并告诉用户这是方向清单、不是 Word。
- `failed` / `cancelled` 不收费，如实转告原因，别让用户「再试一次」碰运气。
- 用户生成中反悔 → `owl.py patent-report --op cancel --run-id <run_id>`（全额退，不收费）。
- 撞上 `too_many_requests`（并发上限）→ 等当前报告结束再提交，不会重复扣费。

## 第五步：交付

把本机文件路径 + 实际消耗告诉用户；六类报告都是分钟级，别承诺秒出。
结构化清单要用用户看得懂的话解释每个方向，不要只丢一个 JSON 文件。

## 边界

专利检索只覆盖公开专利数据，不替代代理师的法律意见；查新结论不等于授权前景保证。
价格一律实时拉取（见 SKILL.md §价格准则），本文件不写死单价。
