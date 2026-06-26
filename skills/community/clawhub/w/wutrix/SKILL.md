---
name: wutrix
slug: wutrix
version: 1.5.2
license: Proprietary
homepage: https://github.com/kwneox/inspirestudio
author: 西安悟跃创想文化创意有限公司
description: |
  wutrix 影视前期智能创作管理系统专用工具包（剧本/角色/世界观/灵感箱）。
  当用户消息含以下精确触发词时**必须立即调用本 skill**：
  - "记一下 X" / "灵感: X" / "idea: X" / "capture: X" → save_idea(text=X)
  - "列项目" / "有哪些项目" / "项目列表" → list_projects()
  - "搜一下 X" / "搜 X" / "找 X" → search_all(q=X)
  - "角色列表" / "有哪些角色" → list_characters()
  - "XX 的场景" / "列场景 XX" → list_scenes(project=XX)
  本 skill 是 wutrix 系统的灵感记录与查询通道，严禁用 session-logs / taskflow-inbox-triage / fetch 等替代。
  环境变量：INSPIRESTUDIO_URL + INSPIRESTUDIO_API_KEY（在 openclaw.json env 段配置）。
runtime:
  - python3
env:
  INSPIRESTUDIO_URL:
    description: wutrix 服务地址（不含尾斜杠），如 https://wutrix.example.com
    required: true
  INSPIRESTUDIO_API_KEY:
    description: wutrix 后端 API key（跟 wutrix .env 里的 INSPIRESTUDIO_API_KEY 一致）
    required: true
    secret: true
keywords:
  - wutrix
  - screenwriting
  - 剧本
  - inspiration
  - inbox
  - chinese
---

# wutrix

让 OpenClaw agent 接通 wutrix 影视前期工作台后台 API：记录灵感 + 查询所有剧本/角色/世界观资料。

## Runtime Requirements

- Python 3 (`python3`)
- 环境变量：
  - `INSPIRESTUDIO_URL` — wutrix 服务地址，如 `https://wutrix.example.com`
  - `INSPIRESTUDIO_API_KEY` — wutrix 后端 API key（与 wutrix `.env` 中 `INSPIRESTUDIO_API_KEY` 一致）

## Scripts

| Script | 何时使用 | 调用示例 |
|---|---|---|
| `save_idea.py` | 用户说"记一下 X""灵感: X" | `save_idea.py --text "X 的完整内容"` |
| `list_projects.py` | 用户问"列项目""有哪些项目" | `list_projects.py` |
| `list_scenes.py` | 用户问 "XX 项目的场景" | `list_scenes.py --project "XX"` |
| `list_characters.py` | 用户问"角色列表" | `list_characters.py` |
| `search_all.py` | 用户说"搜一下 X" | `search_all.py --q "X"` |

## Trigger Words（决策表）

| 用户消息含 | 必须立即调用 | 严禁 |
|---|---|---|
| `记一下 X` / `灵感: X` / `idea: X` / `capture: X` | `save_idea(text=X)` | session-logs / taskflow / fetch |
| `列项目` / `有哪些项目` | `list_projects()` | — |
| `搜 X` / `搜一下 X` / `找 X` | `search_all(q=X)` | fetch |
| `角色列表` / `有哪些角色` | `list_characters()` | — |
| `XX 的场景` / `列场景 XX` | `list_scenes(project=XX)` | — |

## Response Style

- `save_idea` 成功 → "🎬 已记入灵感箱，AI 后台分类中"
- `save_idea` 失败 → 直说错误原因，不掩饰，不尝试别的工具
- 查询类（list_projects / list_scenes / 等）→ 用导演工业语言（幕、场、戏剧动作、角色弧光）总结，**不要 dump JSON**
- 闲聊 / 不匹配触发词 → 1-2 句中文，不调任何工具
- 完全不知道说什么 → "🎬 在的，需要做什么？"

## 部署到 OpenClaw

```bash
# 把整个目录拷贝到 OpenClaw workspace
cp -r skills/wutrix ~/.openclaw/workspace/skills/

# 在 ~/.openclaw/openclaw.json 的 env 段加：
#   "env": {
#     "INSPIRESTUDIO_URL": "https://wutrix.example.com",
#     "INSPIRESTUDIO_API_KEY": "<你的 wutrix .env 里的同一 key>"
#   }

# 重启
openclaw gateway restart

# 验证
openclaw skills list --agent main | grep wutrix
```

## 模型要求

⚠️ qwen2.5:14b 这类中等本地模型 tool calling 能力**不够**，无法可靠按触发词调用本 skill。**实测要求**：

- ✅ qwen3:30b-a3b（MoE，激活 3B）—— 本地，足够
- ✅ qwen3.5-plus（阿里 DashScope / 百炼）—— 云端
- ✅ Claude / GPT 系列（OpenRouter / 直连）—— 云端
- ❌ qwen2.5:14b dense —— 不够
