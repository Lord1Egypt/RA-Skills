# Publish to ClawHub

本目录是 Tencent IMA Hermes Edition 发布到 ClawHub 商店的完整包。

## 一步发布（用 hermes skills 自带 publish 子命令）

> 暂未启用 hermes skills publish 子命令的 clawhub tap；改走下面手动流程。

## 手动发布步骤

### 1) 在 GitHub 创建仓库

登录 https://github.com/wat2012 → New repository：

- **Repository name**: `tencent-ima-skill`
- **Description**: 腾讯 IMA OpenAPI 的 Hermes Agent 适配版。基于腾讯官方 v1.1.7 包改造，22 个端点 + 1 个便利封装
- **Public**
- **不要**勾 "Initialize with README"（本仓已有）

### 2) 推送本目录到 GitHub

```bash
cd ~/Desktop/tencent-ima-skill-publish

git init
git add .
git commit -m "feat: initial release v1.1.7-hermes.1

- 基于腾讯 IMA 官方 OpenAPI v1.1.7 改造
- OpenClaw 风格 frontmatter → Hermes 风格
- bin/ima.sh CLI 桥接（22 个子命令）
- 探针发现 5 个未文档化但真实存在的端点
- 凭证路径对齐 Hermes .env 约定

详细见 SKILL.md / README.md / CHANGELOG.md"

git branch -M main
git remote add origin git@github.com:wat2012/tencent-ima-skill.git
git push -u origin main
```

### 3) 在 ClawHub 走 publish 流程

1. 访问 https://clawhub.ai/skills/publish
2. 用 GitHub 账号登录（OAuth）
3. 填表：

   | 字段 | 值 |
   | --- | --- |
   | 仓库 URL | https://github.com/wat2012/tencent-ima-skill |
   | Slug | `tencent-ima-hermes` |
   | Display Name | 腾讯 IMA (Hermes Edition) |
   | Summary | 腾讯 IMA OpenAPI 的 Hermes Agent 适配版。22 个端点、bin/ima.sh CLI 桥接、OpenAPI 官方凭证（不走 cookie） |
   | Category | productivity |
   | Tags | ima, tencent, knowledge-base, notes, openapi, hermes |
   | License | MIT-0 |
   | Min Hermes | 0.15.0 |

4. clawhub 自动拉仓、跑审核（llm_review）
5. 审核通过后上架

## Slug 选择

| 候选 | 说明 |
| --- | --- |
| `tencent-ima-skill` | ❌ 已被 hyddd v1.0.1 占用 |
| `tencent-ima-skill-hermes` | 较直观但偏长 |
| `tencent-ima-hermes` | **推荐**：短、明确强调区别于 hyddd |
| `ima-openapi-hermes` | 强调 OpenAPI 路线但偏技术 |

## Verification Before Publish

```bash
# 1) 端到端真测试（替换 <your-client-id> 为你自己的 IMA OpenAPI ClientID）
export IMA_OPENAPI_CLIENTID='<your-client-id>'
export IMA_OPENAPI_APIKEY='*** /home/jerome/.hermes/skills/ima/bin/ima.sh list-kb | python3 -c "import json,sys; d=json.load(sys.stdin); print('code:', d['code'], 'count:', len(d['data']['info_list']))"
# 期望: code: 0  count: 14+

# 2) 22 个子命令全在
grep -cE '^  [a-z-]+\)$' /home/jerome/.hermes/skills/ima/bin/ima.sh
# 期望: 22

# 3) --help 头
/home/jerome/.hermes/skills/ima/bin/ima.sh --help | head -5
```

## 发布后

- clawhub 上线后 → 用户能通过 `hermes skills install tencent-ima-hermes` 装
- 自动绑定 GitHub 仓库（更新即触发 clawhub 拉新版）
