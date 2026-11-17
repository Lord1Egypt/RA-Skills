# zqcc Qichacha Relay

English OpenClaw/ClawHub skill for querying Qichacha-backed Chinese enterprise data through the zqcc MCP and Chat API. One AppKey and one MCP endpoint provide access to 185 enterprise-data tools across six capability groups.

Optional Chinese reference: [README.zh-CN.md](README.zh-CN.md)

## Capabilities

- One MCP endpoint for 185 enterprise-data tools.
- Company registration, entity matching, shareholders, contacts, branches, investments, controllers, and finance.
- Litigation, enforcement, dishonesty, penalties, abnormal operations, restrictions, pledges, and other risk data.
- Patents, trademarks, copyrights, apps, websites, social accounts, online stores, and IP pledges.
- Bidding, financing, qualifications, recruitment, news, licenses, land, and operational records.
- Executive roles, investments, controlled companies, personal risks, and historical associations.
- Historical registration, shareholder, executive, investment, judicial, operational, and intellectual-property records.
- Natural-language multi-tool research through `/api/v1/chat`.

## AppKey Registration

Register or log in at <https://zqcc.mkstone.club>. Phone login automatically creates an account for a new number and issues a `zqcc_...` AppKey. Copy it from the user console, then export it:

```bash
export ZQCC_APP_KEY='<YOUR_ZQCC_APP_KEY>'
```

zqcc is an external metered service. Successful calls consume credits. Keep the AppKey secret and never commit it to Git.

## Quick Start

```bash
chmod +x scripts/zqcc.sh
./scripts/zqcc.sh health
./scripts/zqcc.sh tools-list
./scripts/zqcc.sh tools-call get_company_registration_info \
  '{"searchKey":"深圳市腾讯计算机系统有限公司"}'
./scripts/zqcc.sh chat customer-001 \
  '查询深圳市腾讯计算机系统有限公司的工商信息和司法风险'
```

Read [SKILL.md](SKILL.md) for agent instructions, [references/api.md](references/api.md) for the complete contract, and [references/tools.md](references/tools.md) for the offline tool catalog.

## MCP Configuration

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

## Publish to ClawHub

ClawHub publishes skills under MIT-0. Review the public bundle before publishing:

```bash
npm install -g clawhub
clawhub login
clawhub skill publish . --slug zqcc-skill-en --name "zqcc Qichacha Relay" --version 1.0.0 --dry-run
clawhub skill publish . --slug zqcc-skill-en --name "zqcc Qichacha Relay" --version 1.0.0
```

The repository also includes a GitHub Actions workflow. Add a repository secret named `CLAWHUB_TOKEN`, then run `ClawHub Publish` manually with a new SemVer version and changelog. Pull requests run only a pinned-CLI dry-run preview; the workflow always publishes to the `zqcc-skill-en` slug and records the GitHub source commit.

## Repository Layout

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

## License

MIT-0. The zqcc service, Qichacha data, account, and credit usage remain subject to their respective service terms.
