# smart-router-coding

Route coding queries to the right model.  
Fast for lint, deep for architecture, never waste money on a premium model for a one-liner.

## How it works

```
INPUT: coding query
  ↓
Is it simple? → DeepSeek V4 Flash (fast, cheap)
Is it complex? → Kimi K2.7 Code (deep architecture)
Default → DeepSeek V4 Flash (standard)
```

## What you save

| Setup | Cost per 1k queries |
|-------|-------------------|
| All on premium reasoning model | $15+ |
| All on DeepSeek V4 Flash | $0.20 |
| **With smart-router-coding** | **~$0.20 avg** |

DeepSeek V4 Flash handles nearly all coding queries. Kimi K2.7 Code is reserved for architecture, system design, security audit, and optimization work.

## Usage

```bash
clawhub install smart-router-coding
```

## Author

Created by CertainLogic — deterministic AI infrastructure.
certainlogic.ai