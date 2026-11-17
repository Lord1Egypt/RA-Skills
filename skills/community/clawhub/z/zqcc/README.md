# 企查查中转站

企查查中转站是一个公开的 OpenClaw/ClawHub Skill，通过 zqcc 将企查查企业数据能力统一中转为 MCP 和 Chat API。一个 AppKey、一个 MCP 地址，即可使用 6 类、共 185 项企业数据工具。

详细中文说明：[README.zh-CN.md](README.zh-CN.md)

## 核心能力

- 一个企查查中转站 MCP 地址，统一访问 185 项企业数据工具。
- 工商、企业识别、股东、联系方式、分支机构、投资、实际控制人和财务数据。
- 诉讼、被执行、失信、处罚、经营异常、限高、质押等风险数据。
- 专利、商标、著作权、APP、网站、社媒账号、线上店铺和知识产权出质。
- 招投标、融资、资质、招聘、新闻、许可、土地和经营记录。
- 董监高任职、投资、控制企业、个人风险和历史关联。
- 历史工商、股东、高管、投资、司法、经营和知识产权记录。
- 通过 `/api/v1/chat` 使用自然语言组合多个企查查工具完成企业查询。

## AppKey 注册

在企查查中转站 <https://zqcc.mkstone.club> 注册或登录。新手机号登录时自动创建账户，并签发以 `zqcc_` 开头的 AppKey。在用户控制台复制后导出环境变量：

```bash
export ZQCC_APP_KEY='<YOUR_ZQCC_APP_KEY>'
```

企查查中转站按成功业务调用消耗积分。AppKey 必须保密，禁止提交到 Git。

## 快速开始

```bash
chmod +x scripts/zqcc.sh
./scripts/zqcc.sh health
./scripts/zqcc.sh tools-list
./scripts/zqcc.sh tools-call get_company_registration_info \
  '{"searchKey":"深圳市腾讯计算机系统有限公司"}'
./scripts/zqcc.sh chat customer-001 \
  '查询深圳市腾讯计算机系统有限公司的工商信息和司法风险'
```

[SKILL.md](SKILL.md) 是默认中文 Agent 指令，[references/api.md](references/api.md) 是完整接口契约，[references/tools.md](references/tools.md) 是 185 项能力离线目录。

## MCP 配置

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

## 发布到 ClawHub

ClawHub Skill 使用 MIT-0 许可。发布前先检查公开包：

```bash
npm install -g clawhub
clawhub login
clawhub skill publish . --slug zqcc --name "企查查中转站" --version 1.0.2 --dry-run
clawhub skill publish . --slug zqcc --name "企查查中转站" --version 1.0.2
```

仓库包含 GitHub Actions 工作流。添加名为 `CLAWHUB_TOKEN` 的仓库 Secret 后，可手动运行 `ClawHub Publish` 并填写新的 SemVer 版本和更新说明。Pull Request 只运行固定版本 CLI 的 dry-run；工作流始终发布到 `zqcc` slug，公开展示名为“企查查中转站”，并记录 GitHub 来源 commit。

## 仓库结构

```text
.
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── LICENSE
├── .github/workflows/clawhub-publish.yml
├── scripts/
│   └── zqcc.sh
└── references/
    ├── api.md
    └── tools.md
```

## 许可

MIT-0。企查查中转站服务、企查查数据、账户和积分消耗仍分别受对应服务条款约束。
