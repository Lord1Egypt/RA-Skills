# Security — smart-research (standalone)

## 设计

- **无后端、无 Token、无 JWT** — 仅调用公开 API（Crossref、PubMed NCBI）
- **无硬编码密钥** — 可选 `CROSSREF_MAILTO` 由用户配置
- **LLM 在 OpenClaw 侧** — 由用户 openclaw.json 管理，Skill 不接触 API Key

## 发布检查

- [ ] 无 `.env`、`.token`、个人路径
- [ ] `research/sessions/` 仅含模板，无用户真实数据

## 隐私

- `research/sessions/` 存用户研究问题与综述，**留在本地**，不随 ClawHub 发布（已在 `.gitignore` / `.clawhubignore`）
- Agent 输出时注意勿将 session 内容泄露到不受信渠道

## 网络

- Crossref: `api.crossref.org`
- PubMed: `eutils.ncbi.nlm.nih.gov`
