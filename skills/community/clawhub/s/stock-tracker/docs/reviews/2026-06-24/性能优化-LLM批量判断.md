# 任务复盘：性能优化 - LLM 批量判断

## 任务信息

- **项目名称**：stock-tracker
- **任务目标**：将 LLM 标题判断从逐条调用改为批量调用，减少 API 请求次数
- **完成日期**：2026-06-24
- **最终 commit**：7f18197 (feat: LLM batch judgment - reduce API calls from N to N/10)

## 标签

- #全部顺利
- #性能问题

## 完成度评估

- [x] 全部完成

## 验证结果

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 项目能启动 | 通过 | Flask Dashboard 正常启动在 http://localhost:5001 |
| 新功能可用 | 通过 | LLM 批量判断正常工作，169 条公告仅需 17 次 API 调用 |
| 原有功能正常 | 通过 | 公告抓取、过滤、入库、Dashboard 展示均正常 |
| 已截图存档 | 是 | 01-dashboard-home.png, 02-dashboard-stock-detail.png |
| 已提交 commit | 是 | 7f18197 |

## 改动文件清单

| 文件 | 改动类型 | 说明 |
|------|----------|------|
| `scripts/llm_judge.py` | 新增方法 | +judge_batch(), +_judge_batch_single(), +_parse_batch_response(), +_normalize_batch_item(), +BATCH_SYSTEM_PROMPT |
| `scripts/ann_detail.py` | 修改方法 | Phase 1b 从 ThreadPoolExecutor 逐条调用改为 judge_batch() 批量调用，移除 judge_workers 参数 |

## 遇到的问题

无。

## 做得好的地方

- 保留了 judge() 单条方法作为兼容接口
- 批量响应解析兼容多种格式（JSON 数组、JSON 对象、正则提取）
- 从 169 次 API 调用减少到 17 次，减少 90%
- 106/107 测试通过，唯一失败是已知的编码问题

## 下次可以改进的地方

- 可以考虑动态调整 batch_size，根据 API 响应时间自动优化
- 可以添加批量判断的单元测试

## 截图位置

`d:\project\stock-tracker\docs\screenshots\2026-06-24\`
