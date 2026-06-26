---
name: seesaw-agent
description: "Interact with SeeSaw Prediction Market — list markets, get quotes, buy/sell shares, check balance and positions."
metadata:
  {
    "openclaw":
      {
        "emoji": "🎯",
        "homepage": "https://app.seesaw.fun",
        "primaryEnv": "SEESAW_API_KEY",
        "requires":
          {
            "anyBins": ["python3", "python"],
            "env": ["SEESAW_BASE_URL", "SEESAW_API_KEY", "SEESAW_API_SECRET"],
          },
        "install":
          [
            {
              "kind": "brew",
              "package": "python",
              "label": "Install Python 3",
            },
          ],
      },
  }
---

# SeeSaw Prediction Market

## Install

Recommended ClawHub flow:

```bash
clawhub install seesaw-agent
pip install -r skills/seesaw/requirements.txt
openclaw skills check
```

Then configure the skill in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "seesaw-agent": {
        "enabled": true,
        "env": {
          "SEESAW_BASE_URL": "https://app.seesaw.fun/v1",
          "SEESAW_API_KEY": "",
          "SEESAW_API_SECRET": ""
        }
      }
    }
  }
}
```

If your OpenClaw environment includes a helper wrapper, you can bootstrap usage with:

```bash
openclaw skill run --api-key "xxx" --api-secret "xxx"
```

GitHub/manual install fallback:

```bash
git clone https://github.com/SeesawTech/SeeSaw-Claw.git
mkdir -p ~/.openclaw/workspace/skills
cp -R SeeSaw-Claw/skills/seesaw ~/.openclaw/workspace/skills/
pip install -r ~/.openclaw/workspace/skills/seesaw/requirements.txt
openclaw skills check
```

## Configuration

These variables are managed via the OpenClaw Gateway Config (`openclaw.json`) under `env.vars`. The `seesaw.py` script automatically reads them from the environment:

- `SEESAW_BASE_URL`: API Base URL (e.g., `https://app.seesaw.fun/v1`)
- `SEESAW_API_KEY`: Your API Key
- `SEESAW_API_SECRET`: Your API Secret

To update these, use the `gateway config.patch` tool or edit `openclaw.json` directly.

## Usage

All operations are handled by the `seesaw.py` script.

> **Note:** Paths below assume execution from the repository root.

### Wallet

```bash
python skills/seesaw/scripts/seesaw.py balance
python skills/seesaw/scripts/seesaw.py transactions --page 1 --limit 20
python skills/seesaw/scripts/seesaw.py credit-history
python skills/seesaw/scripts/seesaw.py monthly-card-status
```

### Markets

```bash
python skills/seesaw/scripts/seesaw.py list-markets --status active --page 1 --limit 20
python skills/seesaw/scripts/seesaw.py get-market <market_id>
python skills/seesaw/scripts/seesaw.py market-activity <market_id>
python skills/seesaw/scripts/seesaw.py price-history <market_id>
python skills/seesaw/scripts/seesaw.py traders <market_id>
```

### Trade

```bash
python skills/seesaw/scripts/seesaw.py quote <market_id> <option_uuid> <amount> --action buy
python skills/seesaw/scripts/seesaw.py buy <market_id> <option_uuid> <amount>
python skills/seesaw/scripts/seesaw.py sell <market_id> <option_uuid> <shares>
python skills/seesaw/scripts/seesaw.py claim <market_id>
python skills/seesaw/scripts/seesaw.py positions
python skills/seesaw/scripts/seesaw.py trade-history
```

### User & Social

```bash
python skills/seesaw/scripts/seesaw.py profile <user_id>
python skills/seesaw/scripts/seesaw.py leaderboard
python skills/seesaw/scripts/seesaw.py followers <user_id>
python skills/seesaw/scripts/seesaw.py following <user_id>
python skills/seesaw/scripts/seesaw.py favorites <user_id>
python skills/seesaw/scripts/seesaw.py follow <user_id>
python skills/seesaw/scripts/seesaw.py unfollow <user_id>
python skills/seesaw/scripts/seesaw.py set-avatar <avatar_url_or_index>
python skills/seesaw/scripts/seesaw.py default-avatars
python skills/seesaw/scripts/seesaw.py block <user_id>
python skills/seesaw/scripts/seesaw.py unblock <user_id>
```

### Comments

```bash
python skills/seesaw/scripts/seesaw.py comments <market_id>
python skills/seesaw/scripts/seesaw.py add-comment <market_id> "content here"
python skills/seesaw/scripts/seesaw.py delete-comment <market_id> <comment_id>
python skills/seesaw/scripts/seesaw.py favorite <market_id>
python skills/seesaw/scripts/seesaw.py unfavorite <market_id>
```

### Challenges

```bash
python skills/seesaw/scripts/seesaw.py challenges
python skills/seesaw/scripts/seesaw.py claim-challenge <challenge_id>
```

### Oracle

```bash
python skills/seesaw/scripts/seesaw.py oracle-status <prediction_id>
python skills/seesaw/scripts/seesaw.py assert <prediction_id> <option_id>
python skills/seesaw/scripts/seesaw.py dispute <prediction_id> <option_id>
python skills/seesaw/scripts/seesaw.py vote <prediction_id> <option_id>
python skills/seesaw/scripts/seesaw.py settle <prediction_id> <winner_option_id>
```

### Categories

```bash
python skills/seesaw/scripts/seesaw.py categories
```

### Create Market

```bash
# 1. Upload image (optional)
python skills/seesaw/scripts/seesaw.py upload /path/to/image.jpg
# Returns {"file_url": "..."}

# 2. Create market
python skills/seesaw/scripts/seesaw.py create-market \
  --title "Will X happen?" \
  --options "Yes" "No" \
  --probs 60 40 \
  --end-time "2026-12-31T23:59:59Z" \
  --images "https://cdn.example.com/uploads/abc123.jpg"
```

### Share

```bash
# Create a share link for a market
python skills/seesaw/scripts/seesaw.py create-share-link <market_id> \
  [--image-url <url>] \
  [--share-source <source>] \
  [--share-target <target>]

# Returns:
# {
#   "share_id": "...",     // 分享链接 ID
#   "share_url": "...",    // 完整的分享链接 URL
#   "title": "...",        // 可选，分享标题（微信用标题+副标题，朋友圈用标题）
#   "subtitle": "..."      // 可选，分享副标题（仅微信使用）
# }
```

## Automated Workflows

The skill includes several scripts for automated trading and market management. All scripts support `--dry-run` to simulate actions without executing trades or creating markets.

**Configuration:**
Edit `skills/seesaw/config.json` to set:

- `max_position_size`: Max shares to buy per trade.
- `max_daily_loss`: Daily loss limit (not fully implemented yet).
- `dry_run`: Set to `true` to enable dry-run by default.

### Generate Topics

Search for recent news, generate prediction market proposals (ranked by LLM), find images, and create them upon Slack confirmation.

```bash
python skills/seesaw/scripts/generate_topic.py [--dry-run]
```

### Adjust Positions

Monitor held positions, check news, and adjust (buy/sell/hold) or settle completed markets. Checks wallet balance before buying.

```bash
python skills/seesaw/scripts/adjust_position.py [--dry-run]
```

### Open Positions

Scan for new or hot markets, analyze value based on news (checking probabilities), and open new positions if confidence is high.

```bash
python skills/seesaw/scripts/open_position.py [--dry-run]
```

### Claim Rewards

Automatically claim completed challenge rewards.

```bash
python skills/seesaw/scripts/claim_rewards.py [--dry-run]
```

### Auto Assert (Market Manager)

运营话题脚本：检查活跃话题、查询进展、断言、评论。

```bash
python skills/seesaw/scripts/auto_assert.py [--dry-run]
```

**功能：**

1. 查询自己创建的活跃话题
2. 查询话题相关事件的最新进展
3. 已过期且可断言的话题 → 自动断言
4. 未过期但有新进展 → 在话题下评论最新情况

**Prerequisites:**

- `OPENAI_API_KEY`: Required for LLM analysis.
- `SLACK_BOT_TOKEN` & `SLACK_CHANNEL_ID`: Required for notifications.
- `BRAVE_API_KEY`: Required for web search and image search in the automation scripts.

## Setup

Ensure `requests` is installed:

```bash
pip install -r skills/seesaw/requirements.txt
```

## API Coverage

| Category       | Endpoints                                                      |
| -------------- | -------------------------------------------------------------- |
| **Wallet**     | balance, transactions, credit-history, monthly-card-status     |
| **Markets**    | list, get, activity, price-history, traders                    |
| **Trade**      | quote, buy, sell, claim, positions, history                    |
| **User**       | profile, leaderboard, followers, following, favorites, avatars |
| **Social**     | follow, unfollow, block, unblock, comments, favorite           |
| **Challenges** | list, claim                                                    |
| **Oracle**     | status, assert, dispute, vote, settle                          |
| **Categories** | list                                                           |
