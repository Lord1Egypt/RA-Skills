# readwise_article_saver

An [OpenClaw](https://docs.openclaw.ai/) skill that saves article links to [Readwise Reader](https://readwise.io/read) with automatic LLM-powered tagging. Specialized handling for WeChat Official Account (微信公众号) articles.

## How it works

```
User sends URL → agent triggers skill
  │
  ├── Step 1: exec save_article.py   → Fetch HTML, save to Readwise, output JSON
  │
  ├── Step 2: llm-task                → Classify content → ["AI agent", "China"]
  │
  ├── Step 3: exec update_tags.py     → Apply tags to the saved article
  │
  └── Step 4: Report ✅/⚠️/❌ to user
```

The skill separates **deterministic operations** (fetch, validate, save) from **LLM classification** (tagging). The Python scripts handle network I/O, while OpenClaw's built-in `llm-task` tool handles content classification — so the tagging model is configured through OpenClaw's provider system, not hardcoded.

## Install

### 1. Copy the skill

```bash
cp -r readwise_article_saver ~/.openclaw/workspace/skills/
```

Or clone directly:

```bash
git clone https://github.com/YOUR_USERNAME/readwise_article_saver.git \
  ~/.openclaw/workspace/skills/readwise_article_saver
```

### 2. Configure environment variables

Merge the settings from `openclaw.example.json` into your `~/.openclaw/openclaw.json`:

```jsonc
{
  "skills": {
    "entries": {
      "readwise_article_saver": {
        "enabled": true,
        "env": {
          "READWISE_TOKEN": "your_token_here",       // from readwise.io/access_token
          "OPENROUTER_API_KEY": "your_key_here"       // from openrouter.ai/keys
        }
      }
    }
  },
  "plugins": {
    "entries": {
      "llm-task": {
        "enabled": true,
        "config": {
          "defaultProvider": "openrouter",
          "defaultModel": "minimax/minimax-m2.7"
        }
      }
    }
  }
}
```

### 3. Ensure tools are allowed

Make sure `exec` and `llm-task` are in your agent's tool allowlist:

```json
{
  "agents": {
    "list": [{ "id": "main", "tools": { "allow": ["exec", "llm-task"] } }]
  }
}
```

### 4. Reload

```bash
/new
# or
openclaw gateway restart
```

### 5. Verify

```bash
openclaw skills list
# should show: readwise_article_saver
```

## Usage

Just send a URL:

```
You:     https://mp.weixin.qq.com/s/AbCdEfGhIjKlMnOp
Agent:   ✅ 「深度学习在金融领域的应用」已保存到 Readwise Reader。标签: AI agent, China
```

## File structure

```
readwise_article_saver/
├── SKILL.md                   # Skill instructions (agent reads this)
├── save_article.py            # Fetch + save script (called via exec)
├── update_tags.py             # Tag update script (called via exec)
├── openclaw.example.json      # Config snippet to merge into openclaw.json
└── README.md                  # This file (for humans, not loaded by agent)
```

## Changing the tagging model

The tagging model is configured in `openclaw.json` under `plugins.entries.llm-task.config.defaultModel`. Change it without touching any skill files:

```jsonc
// MiniMax M2.7 (default)
"defaultModel": "minimax/minimax-m2.7"

// Or any OpenRouter model:
"defaultModel": "anthropic/claude-sonnet-4"
"defaultModel": "google/gemini-2.5-flash"
"defaultModel": "deepseek/deepseek-r1"
```

## Customizing the taxonomy

The tag taxonomy is embedded in SKILL.md inside the `llm-task` prompt. To add, remove, or modify tags, edit the taxonomy section in SKILL.md directly. Changes are picked up on the next agent turn (no restart needed if `load.watch` is enabled).

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Script not found | Wrong install path | Ensure skill is at `~/.openclaw/workspace/skills/readwise_article_saver/` |
| `READWISE_TOKEN not set` | Env var missing | Add to `openclaw.json` → `skills.entries` |
| Tags always "openclaw" | `llm-task` not enabled | Enable in `plugins.entries` and allow in agent tools |
| WeChat content garbled | Fetch failed (link expired) | Save manually from WeChat |
| `exec` denied | Tool not allowed | Add `exec` to agent tool allowlist |

## License

MIT
