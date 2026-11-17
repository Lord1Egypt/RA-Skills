---
name: zqcc-skill
description: "企查查中转站 Skill。用于通过 zqcc 统一中转的企查查 MCP 和 Chat API 查询企业工商、股东、联系方式、风险、知识产权、经营、董监高和历史记录，也用于注册 zqcc AppKey 或配置企查查中转站 MCP。"
version: 1.0.2
metadata:
  openclaw:
    requires:
      env:
        - ZQCC_APP_KEY
      bins:
        - curl
        - jq
    primaryEnv: ZQCC_APP_KEY
    envVars:
      - name: ZQCC_APP_KEY
        required: true
        description: "在 https://zqcc.mkstone.club 完成手机号登录后获取的企查查中转站 AppKey"
      - name: ZQCC_BASE_URL
        required: false
        description: "可选的企查查中转站 API 地址，默认为 https://zqcc.mkstone.club"
    homepage: https://zqcc.mkstone.club
---

# 企查查中转站

企查查中转站通过 zqcc 提供统一、带鉴权的企业数据入口，将企查查的 6 类、185 项能力汇聚到一个 MCP 地址，并提供自然语言 Chat API。需要查询中国企业工商、股东、风险、知识产权、经营、董监高或历史记录时使用本 Skill。

## 开始之前

1. 打开企查查中转站：<https://zqcc.mkstone.club>。
2. 完成图片验证码和短信登录，新手机号会自动注册。
3. 进入用户控制台，复制以 `zqcc_` 开头的 AppKey。
4. 通过环境变量保存，不要写入提示词、源代码或日志：

```bash
export ZQCC_APP_KEY='<YOUR_ZQCC_APP_KEY>'
```

AppKey 是企查查中转站的计费凭证，成功的业务调用会消耗 zqcc 积分。它不是网站控制台使用的登录 JWT。

## 选择调用方式

### 直接调用 MCP 工具

需要结构化结果或明确的数据能力时使用。

1. 调用前先获取实时工具和参数 schema：

```bash
./scripts/zqcc.sh tools-list
```

2. 使用 JSON 参数对象调用工具：

```bash
./scripts/zqcc.sh tools-call get_company_registration_info \
  '{"searchKey":"深圳市腾讯计算机系统有限公司"}'
```

上游参数可能变化，应以实时 `tools/list` 返回的 schema 为准。[references/tools.md](references/tools.md) 仅用于从 185 项能力中选择合适工具。

### 自然语言企业查询

当问题需要组合多个企查查工具或生成综合结论时，使用企查查中转站 Chat API：

```bash
./scripts/zqcc.sh chat customer-001 \
  '查询深圳市腾讯计算机系统有限公司的工商信息、司法风险和经营动态'
```

连续对话应复用稳定的 `sessionId`；不同用户或任务应使用不同 ID 隔离上下文。

### 生成 MCP 客户端配置

```bash
./scripts/zqcc.sh config
```

该命令输出企查查中转站 MCP 地址 `https://zqcc.mkstone.club/mcp/stream` 的 JSON 配置。输出中包含 AppKey，必须按敏感信息处理。

## 能力选择

- `company`：企业识别、工商信息、股东、联系方式、分支机构、投资、实际控制人和财务数据。
- `risk`：被执行、失信、诉讼、处罚、经营异常、限高、质押和拍卖等风险数据。
- `ipr`：专利、商标、著作权、APP、网站、社媒账号、店铺和知识产权出质。
- `operation`：招投标、融资、年报、资质、招聘、新闻、许可、土地和产品等经营数据。
- `executive`：董监高任职、投资、控制企业、个人风险和历史风险。
- `history`：历史工商、股东、高管、投资、风险、处罚、诉讼和知识产权记录。

企业名称不明确时，先调用 `get_company_by_query` 完成实体识别，再用准确企业名称继续查询。董监高类工具通常需要同时提供企业名称和人员姓名，具体参数以实时 schema 为准。

## 响应处理

- MCP 成功结果通常位于 `result.content[]`；文本项包含 JSON 时，应继续解析为结构化数据。
- `401` 表示 AppKey 缺失、无效、已禁用，或所属用户已禁用。
- `402` 表示企查查中转站积分不足。
- `503` 表示当前没有可用的上游企查查密钥，或上游额度均已耗尽。
- 不要自动重试 `401` 或 `402`；对临时 `502`、`503` 仅做保守重试。
- JSON-RPC 响应含有 `error` 或 `result.isError: true` 时，不得报告调用成功。

完整接口契约、示例、计费行为和故障排查见 [references/api.md](references/api.md)。

## 安全规则

- 不得泄露、回显、记录、提交 `ZQCC_APP_KEY`，也不得将它发送到企查查中转站 HTTPS 域名之外。
- 不得把 AppKey 放入 URL 查询参数。
- 不得调用管理员接口。
- 轮换 AppKey 会立即禁用原有活跃密钥，执行前必须征得用户确认。
- 仅返回任务所需的企业数据；结果含手机号、地址、诉讼或董监高个人记录时尤其要控制范围。
