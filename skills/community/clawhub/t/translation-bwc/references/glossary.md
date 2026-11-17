# BWC Glossary — Terminology Source of Truth

> Fill this in before production translation. Each BWC concept must map to ONE
> approved 中文 term and ONE approved English term. Never re-translate an approved
> term. Mark rows you have not decided yet with `TBD` in the target column.

## How to Use

- When translating, look up the source term here first.
- If a term is absent, insert it with both language forms and a short note, then
  continue. Keep the table the single source of truth.
- Columns: `中文` / `English` / `缩写/代码` / `禁止译法` (variants to reject) /
  `备注`.

## Master Term Table

| 中文 | English | 缩写/代码 | 禁止译法 | 备注 |
|------|---------|-----------|----------|------|
| _示例：工作流_ | _Workflow_ | _WF_ | _流程(易歧义)_ | _核心模块_ |
| _示例：租户_ | _Tenant_ | — | _客户/用户_ | _多租户架构_ |
| 采集站 | Docking Station | — | 对接站/停靠站 | 数据采集硬件节点 |
| 采集 | offload | — | 收集/获取/collect | 动词；按时态变化 offloads/offloaded/offloading；数据卸载/导出 |
| TBD | TBD | — | — | — |

## Product & Module Names

| 名称 | 中文 | English | 说明 |
|------|------|---------|------|
| BWC | 执法记录仪 | Body Camera（单/复数） | 源文 BWC/bwc 按目标语言渲染：中文→执法记录仪；英文→Body Camera（据语境取单数/复数） |
| _模块A_ | _TBD_ | _TBD_ | _TBD_ |

## API Concepts

| 概念 | 中文 | English | 备注 |
|------|------|---------|------|
| endpoint | 接口 / 端点 | endpoint | 技术文档优先用"接口" |
| request / response | 请求 / 响应 | request / response | — |
| pagination | 分页 | pagination | — |
| webhook | Webhook | webhook | 不翻译 |
| rate limit | 限流 / 速率限制 | rate limit | — |

## Error Codes

> Preserve the raw code string. Provide the approved 中文 message only.

| 错误码 | 中文说明 | English | 备注 |
|--------|----------|---------|------|
| `BWC_0001` | _TBD_ | _TBD_ | _TBD_ |

## UI Labels (if needed)

| 标签 | 中文 | English |
|------|------|---------|
| _保存_ | 保存 | Save |
| _取消_ | 取消 | Cancel |
|_提交_ | 提交 | Submit |
