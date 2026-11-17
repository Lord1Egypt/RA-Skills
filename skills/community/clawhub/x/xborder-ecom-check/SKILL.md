---
name: xborder-ecom-check
description: |
  Cross-Border E-Commerce Compliance Check — Cross-border e-commerce rules: customs, product safety, consumer protection, tax (VAT/GST), advertising, and data privacy of destination markets.

  Free to install; scoring runs on the CQDev cloud compliance engine.
  No Key? The skill auto-runs an anonymous trial (5 real cloud-scored
  runs, 7-day window) before asking you to register. Covers 12 core items.
  Use when: the user explicitly asks to run the xborder-ecom-check skill (e.g. "run xborder-ecom-check",
  "use the xborder-ecom-check skill"). Do NOT activate on generic mentions of "跨境电商" or "cross-border ecommerce"
  in ordinary conversation — this skill transmits answers to a third-party cloud and must be
  opted into explicitly by name.
  Trigger (explicit opt-in only): xborder-ecom-check, run xborder-ecom-check, use xborder-ecom-check skill, run the xborder-ecom-check skill
  Pricing: Free skill; cloud scoring is free (anonymous trial 5 runs, then register for a free API Key with 100 calls)
  ⚠️ Cloud scoring sends your answers to compliancehub.cn. The free preview (--non-interactive / --non-interactive-json)
  runs FULLY OFFLINE using the bundled 12-item set and never contacts the cloud (no network, no IP/UA leakage).
  Scored runs fetch the latest check items from the cloud rule library and transmit your answers (scored online).
  Without a Key the skill runs an anonymous trial (up to 5 scored runs) using a local random anon_id; registering gives a free Key with 100 calls.
  🔑 API Key is user-supplied (not auto-provisioned): get a free Key on the account page, then set
  COMPLIANCEHUB_API_KEY or save it to ~/.config/compliancehub/xborder-ecom-check.key (mode 0600). No email/password
  is ever collected by this skill.
  🌐 Language: bilingual (中文/English). Guidance and recommendations default to Chinese for Chinese-speaking
  compliance teams; legal/regulatory terms keep English originals. Users may request English output at any time.

  💡 Free preview: --non-interactive lists the 12 items without a Key
permissions:
  network:
    - "https://compliancehub.cn"
  filesystem:
    write:
      - "~/.config/compliancehub"
  env:
    - "COMPLIANCEHUB_API_KEY"
---

# 🔒 Cross-Border E-Commerce Compliance Check (跨境电商合规检查) — Free, Cloud-Scored

## Overview
跨境电商合规检查 is a **free** 检查 based on 跨境电商相关规则：海关申报、商品安全（CE/REACH/CPSC 等）、消费者权益、税务（VAT/GST）、广告法与目的地数据隐私.
It covers 12 core items. Scoring runs on the CQDev cloud compliance engine.

## How it works (free + cloud)
> ⚠️ **Your answers leave this machine.** When you run a *scored* 检查, your responses are
> transmitted to the CQDev cloud at `compliancehub.cn` for scoring. The free `--non-interactive` preview runs
> **fully offline** using the bundled 12-item set and never contacts the cloud (no network, no IP/UA leakage).

- The skill is free to install.
- Check items are bundled in the skill (12 items); scored runs may refresh them from the cloud rule library.
- Scoring + quota are computed in the cloud; you get a professional report locally.
- Scoring: no Key? The anonymous trial (5 real cloud-scored runs) runs automatically. Register for a free API Key (100 calls) to keep going.

## What it checks (12 items)
| # | Check | Authority |
|---|-------|-----------|
| 1 | 主体与平台注册 | 目的地市场准入 |
| 2 | 原产国标注 | 海关与原产地规则 |
| 3 | 海关申报合规 | 海关法 |
| 4 | 关税与进口税 | 关税法 |
| 5 | CE 标志（欧盟） | EU 法规 (如 MDR/LVD) |
| 6 | 商品安全环保 | REACH / CPSC / 目的地法规 |
| 7 | 标签与说明书语言 | 目的地标签法规 |
| 8 | 消费者权益 | 目的地消保法 |
| 9 | 广告与直播话术 | 广告法/跨境 |
| 10 | 买家数据隐私 | GDPR / CCPA 等 |
| 11 | 知识产权 | 商标/专利/版权法 |
| 12 | 增值税/VAT 申报 | EU OSS/IOSS、UK VAT 等 |

## Usage
### Free preview (no Key)
```bash
python3 scripts/xborder-ecom-check.py --non-interactive
```
### Anonymous trial (no Key)
Just run the full 检查 — without a Key the skill issues a local random anon_id and scores in the cloud
(5 free runs / 7-day window). When the trial runs out it prints the one-click registration page,
carrying your anon_id so the trial progress carries over after registering.

### Get a free API Key
```bash
# 1. Open the account page and create a free account (100 free calls):
#    https://compliancehub.cn/account.html?skill=xborder-ecom-check
# 2. Copy your API Key.
# 3a. Export it as an environment variable:
export COMPLIANCEHUB_API_KEY=your_key
# 3b. Or save it to a file (mode 0600):
echo your_key > ~/.config/compliancehub/xborder-ecom-check.key && chmod 600 ~/.config/compliancehub/xborder-ecom-check.key
```
Or open: https://compliancehub.cn/account.html?skill=xborder-ecom-check

### Full 检查 + report
```bash
python3 scripts/xborder-ecom-check.py --format html -o xborder-ecom-check-report.html
```

## Agent guide
When a user asks for a 跨境电商合规检查:
1. Run `--non-interactive` to preview the 12 items (no Key needed, fully offline).
2. Run the full 检查. Without a Key it automatically uses the anonymous trial (5 real cloud-scored runs) — the user gets the complete report immediately. When the trial runs out the skill prints the one-click registration page (with the trial's anon_id), and after registering the same run continues under their free API Key (100 calls).

## Security & data handling
- **No credentials collected:** This skill never prompts for or transmits any email/password. The API Key is
  supplied by you (env var or key file) — provisioned manually on the account page, not by this skill.
- **Where data goes:** Check items are fetched from, and your answers are scored by, the CQDev cloud at
  `https://compliancehub.cn` (the operator's official endpoint). Scoring transmits only your item answers, plus
  either the free API Key (as a Bearer token) when registered, or the local random anon_id during the anonymous trial.
- **API Key storage:** read from `COMPLIANCEHUB_API_KEY` or `~/.config/compliancehub/xborder-ecom-check.key` (0600),
  outside the skill folder. The skill never writes the file itself; you create it.
- **Anonymous trial id:** A local random `anon_id` (`~/.config/compliancehub/xborder-ecom-check.anon_id`,
  0600, carries no personal data) persists only to continue the anonymous trial; your answers are never stored locally.
- **No shell execution:** stdlib only (`urllib`, `json`, `ssl`); no shell, no external binaries.
- **Not a rogue/autonomous agent:** The stored file is an ordinary API-key (0600), not an auto-start,
  session, or background process. No state is kept beyond that single key file.
- **Preview mode:** `--non-interactive` / `--non-interactive-json` run FULLY OFFLINE using the bundled 12-item set
  and NEVER contact the cloud — no IP/UA/timing leakage. Only scored runs fetch rules + send answers.
- Always confirm the destination is `compliancehub.cn` before running a scored check.

## Legal disclaimer
This tool provides general compliance guidance only and is **not legal advice**. Consult qualified counsel.

## License
MIT.
