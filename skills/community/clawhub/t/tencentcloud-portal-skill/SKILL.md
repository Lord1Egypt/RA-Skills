---
name: tencentcloud-portal-skill
description: '在用户需要使用腾讯云官网公共（Tencent Cloud Portal）能力时加载。公共能力是腾讯云官网（cloud.tencent.com）的统一服务入口，通过 TCCLI 的 ``portal`` 系列接口调用。当前提供的能力：文档搜索（查询云产品文档、操作指南、API 文档、最佳实践、故障排查等）。触发词示例："搜索腾讯云文档"、"腾讯云官网搜索"、"查一下腾讯云…怎么配置"、"腾讯云文档搜索"、"帮我搜腾讯云…的文档"、"查云产品文档"、"portal search"、"search tencent cloud docs"。不适用于：操作云资源（CVM/轻量服务器/VPC 等）——本技能面向官网门户信息类能力，不管理资源。'
---

# 腾讯云官网门户（Tencent Cloud Portal）

通过 TCCLI 的 `portal` 系列接口调用腾讯云官网门户的**信息类能力**（非资源管理）。当前提供：**文档搜索**（`SearchDocuments`）。

## 前置条件

```bash
tccli --version
python3 -c "import tencentcloud.portal"   # 自检 portal 模块
```

- 未安装，或报 `No module named 'tencentcloud.portal'` → 见 `references/install.md`。
- 凭证配置（OAuth / 无浏览器 / agent 非交互 / AK/SK）→ 见 `references/auth.md`。默认 `tccli auth login`。

## 能力路由

| 用户意图 | 接口 | 参考文档 |
|----------|------|----------|
| 搜索腾讯云官网文档 / 操作指南 / API 文档 | `SearchDocuments` | `references/search-documents.md` |
| 其它 portal 操作 | — | `tccli portal help` |

**执行前先读对应参考文档。** 参数不确定时用 `tccli portal <Action> help` 核对（你对参数的了解可能过时）。

## 调用约定

- 形式：`tccli portal <Action> [参数...]`；复杂参数加 `--cli-unfold-argument`，用 `--Name value` 而非 JSON。
- 地域可选，无需 `--region`。

## 结果呈现

- 只呈现接口实际返回的数据，**不得编造** URL / 标题 / 摘要等；失败时报告错误与 `RequestId`。
- 分页能力先报总数，有更多结果再询问是否翻页。

## 错误处理

| 现象 | 处理 |
|------|------|
| `command not found` / `No module named 'tencentcloud.portal'` | 见 `references/install.md` |
| `AuthFailure` / 凭证过期 / `EOF when reading a line` / `invalid state` | 见 `references/auth.md` |
| `InvalidParameter(Value)` | 用 `tccli portal <Action> help` 核对参数与取值范围 |
| 频率超限 | 放慢请求节奏重试 |
| 空结果 | 换关键词，见 `references/search-documents.md` |

同类错误多次重试仍失败时，停止重试，引导用户参照官方文档手动处理。

## 渠道输出兼容性

部分渠道会转换 Markdown 破坏输出：CLI/JSON 用代码块包裹；URL 中的 `_` 若被吞则替换为 `%5F`；标识符用行内反引号包裹。
