# zqcc Qichacha Relay 中文参考

这是 `zqcc-skill-en` 英文版 Skill 的可选中文参考。GitHub 默认 README、ClawHub 展示内容和 `SKILL.md` 均使用英文。

English documentation: [README.md](README.md)

## 功能与能力

zqcc 对外提供一个 MCP 地址，统一代理 6 类、共 185 个企业数据工具：

| 能力分类 | 工具数 | 主要内容 |
| --- | ---: | --- |
| 企业基座 `company` | 16 | 企业识别、工商信息、股东、联系方式、分支机构、对外投资、实际控制人、财务数据 |
| 风控大脑 `risk` | 38 | 企业风险扫描、被执行、失信、限高、经营异常、行政处罚、裁判文书、股权冻结与质押 |
| 知产引擎 `ipr` | 18 | 专利、商标、软件著作权、作品著作权、APP、网站、社媒账号、线上店铺、知产出质 |
| 经营罗盘 `operation` | 35 | 招投标、融资、资质、招聘、新闻舆情、行政许可、土地、产品与经营记录 |
| 董监高画像 `executive` | 44 | 任职、投资、控制企业、关联企业、个人风险和历史风险 |
| 历史存档 `history` | 34 | 历史工商、股东、主要人员、投资、司法风险、经营记录和知识产权 |

自然语言 Chat API 可以根据问题自动组合多个工具并生成综合回答，适合企业尽调、风险核查、客户背景调查、供应商核验和知识产权检索。

## AppKey 注册地址

注册地址和用户控制台：<https://zqcc.mkstone.club>

1. 打开注册地址。
2. 输入中国大陆手机号。
3. 完成图片验证码并获取短信验证码。
4. 点击“登录 / 自动注册”。新手机号会自动创建账户。
5. 在用户控制台复制以 `zqcc_` 开头的 AppKey。

AppKey 用于 MCP 和 Chat API，不是网页登录 JWT。成功业务调用会扣除 zqcc 积分，具体余额、调用记录和扣费流水以用户控制台为准。

建议通过环境变量保存 AppKey：

```bash
export ZQCC_APP_KEY='<YOUR_ZQCC_APP_KEY>'
```

不要把真实 AppKey 写入 Git、公开文档、聊天消息、截图、日志或 URL 查询参数。

## 快速使用

检查服务状态：

```bash
chmod +x scripts/zqcc.sh
./scripts/zqcc.sh health
```

获取实时工具及参数 schema：

```bash
./scripts/zqcc.sh tools-list
```

查询企业工商信息：

```bash
./scripts/zqcc.sh tools-call get_company_registration_info \
  '{"searchKey":"深圳市腾讯计算机系统有限公司"}'
```

使用自然语言综合查询：

```bash
./scripts/zqcc.sh chat customer-001 \
  '查询深圳市腾讯计算机系统有限公司的工商信息、司法风险和经营动态'
```

同一段连续对话应复用稳定的 `sessionId`；不同用户或任务应使用不同 ID。

## MCP 配置

MCP 地址：`https://zqcc.mkstone.club/mcp/stream`

```json
{
  "mcpServers": {
    "zqcc": {
      "url": "https://zqcc.mkstone.club/mcp/stream",
      "headers": {
        "Authorization": "Bearer <ZQCC_APP_KEY>"
      }
    }
  }
}
```

建议将请求与响应超时设置为 300 秒。当前接口按无状态 JSON-RPC POST 工作，不应依赖 SSE 输出或服务端 MCP 会话。

## 使用建议

- 企业名称不确定时，先调用 `get_company_by_query` 做企业实体识别。
- 调用具体工具前优先执行 `tools/list`，以实时返回的 `inputSchema` 为准。
- [references/tools.md](references/tools.md) 是 2026-07-28 的 185 工具离线索引，仅用于选择能力。
- 董监高工具通常需要企业名称和人员姓名两个锚点，参数以实时 schema 为准。
- `401` 表示 AppKey 缺失或无效；`402` 表示积分不足；`502`、`503` 通常是上游暂时不可用。
- HTTP 200 也可能包含 JSON-RPC `error` 或 `result.isError: true`，必须同时检查响应体。

## 文档索引

- [SKILL.md](SKILL.md)：OpenClaw Agent 的工作流与安全规则。
- [references/api.md](references/api.md)：MCP、Chat API、鉴权、计费与错误说明。
- [references/tools.md](references/tools.md)：185 个工具的分类、名称和中文能力标题。

## ClawHub 发布

```bash
npm install -g clawhub
clawhub login
clawhub skill publish . --slug zqcc-skill-en --name "zqcc Qichacha Relay" --version 1.0.0 --dry-run
clawhub skill publish . --slug zqcc-skill-en --name "zqcc Qichacha Relay" --version 1.0.0
```

ClawHub 上发布的 Skill 使用 MIT-0 许可。zqcc 服务、企查查数据、账户和积分消耗仍分别受对应服务条款约束。
