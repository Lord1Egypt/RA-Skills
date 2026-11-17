# WenYan · Agent Integration Guide（各智能体接入指南）

> **中文导读**：WenYan 是**通用古风语体引擎**，不绑定任何框架。核心 = 纯 JSON 风格配置 + Python 引擎。任何能塞 system prompt 的智能体都能用。
> 三步接入：① 生成提示词 → ② 设为该智能体的 system prompt → ③ 用引擎校验回复质量（可选）。

WenYan is a **framework-agnostic** classical Chinese style engine. Its core is **pure JSON style configs + a Python engine** — no dependency on any model framework or chat platform. If your agent accepts a system prompt, it can use WenYan.

---

## Quick Start (3 Steps)

### Step 1 — Generate a system prompt

```bash
python scripts/style_engine.py prompt <style_id>
```

Where `<style_id>` ∈ `ruya | wuxia | sanguo | zhanguo | shiji | baihua | shijing | chan`

The output is a complete, ready-to-paste system prompt: core rules, address system, forbidden words, vocabulary mapping, sentence templates, and quality standards.

### Step 2 — Install it as the agent's system prompt

See [Per-Agent Setup](#per-agent-setup) for platform-specific instructions.

### Step 3 — Validate & score replies (optional)

```bash
# bash / Linux / macOS
echo "你的回复文本" | python scripts/style_engine.py validate sanguo
echo "你的回复文本" | python scripts/style_engine.py score sanguo

# Windows PowerShell
"你的回复文本" | python scripts/style_engine.py validate sanguo
```

`validate` returns JSON with errors (forbidden words) and warnings (length / drift). `score` adds a 0–100 style score.

---

## Engine Command Reference

| Command | Description |
|---------|-------------|
| `prompt <style_id>` | Generate the system prompt for a style |
| `map <style_id>` | Read text from stdin, apply the vocabulary mapping |
| `validate <style_id>` | Read text from stdin, check forbidden words / length / drift → JSON |
| `score <style_id>` | Read text from stdin, compute style score → JSON |
| `all` | List all available style IDs |

```bash
# List styles
python scripts/style_engine.py all

# Generate the Sanguo (Three Kingdoms) prompt
python scripts/style_engine.py prompt sanguo
```

---

## 8 Styles

| ID | Name | Era | Character |
|----|------|-----|-----------|
| `ruya` | 儒雅 | Tang/Song | Elegant scholar, classical allusions |
| `wuxia` | 武侠 | Ming/Qing | Martial hero, chivalric |
| `sanguo` | 三国 | Late Han | Strategist, Three Kingdoms |
| `zhanguo` | 战国 | Pre-Qin | Diplomatic strategist, 磅礴气势 |
| `shiji` | 史记 | Western Han | Grand Historian's pen |
| `baihua` | 白话 | Ming/Qing | Storyteller, colloquial |
| `shijing` | 诗经 | Ancient | Four-character odes |
| `chan` | 禅意 | Tang/Song | Zen master, 空灵 |

## Intensity Levels

| Level | Classical Ratio | Use Case |
|-------|-----------------|----------|
| 1 (浅度) | ~20% | Daily chat with classical flavor |
| 2 (中度) | ~60% | Semi-classical, modern logic preserved |
| 3 (深度) | 90%+ | Full classical, structured sentences |

> **Note on intensity**: each JSON config encodes the **deep** style. To run at a lighter intensity, add an instruction to the system prompt such as *"apply the classical style at ~20% / ~60% density"*. The engine's validation thresholds are tuned for the deep (level 3) style.

---

## Per-Agent Setup

### OpenClaw
```bash
openclaw skills install wenyan
```
Then simply tell the AI: **切换三国风3** / **Switch to Sanguo 3**. OpenClaw reads `SKILL.md` and `state.json` automatically, so the style persists across turns until you exit.

### Claude (claude.ai / API)
- **Web**: generate the prompt → paste into **Settings → System prompt** (account-level) or the chat's custom instructions.
- **API**: send the prompt as the `system` field in the messages payload.

```json
{
  "model": "claude-sonnet-4-5",
  "system": "<output of: python scripts/style_engine.py prompt ruya>",
  "messages": [{"role": "user", "content": "你好"}]
}
```

### ChatGPT (GPT-4 / GPT-5)
- **Web**: paste the prompt into **Settings → Personalities → "How ChatGPT should respond to you"**, or create a **Project** and put it in the **Instructions**.
- **API**: send as the `system` role message.

### Gemini / Grok / other Web AI
Paste the prompt into **Settings → System instructions** / custom prompt.

### Dify / Coze / FastGPT
Fill the app's **System Prompt / 系统提示词** field with the prompt output. Then your whole app speaks classical Chinese.

### Ollama (local models)
- **Option A** — bake it in: write the prompt into a Modelfile `SYSTEM` field, then `ollama create -f Modelfile mymodel`.
- **Option B** — per request: send the prompt as the `system` parameter in every `/api/chat` call.

### Cursor / Cline / Continue (code assistants)
Paste the prompt into `.cursorrules` / `clinerules` / `.continuerules`. Best used for Chinese-facing tasks, changelog prose, or commit messages.

### Custom API services
Send the prompt as the `system` field to any model. For a **quality gate**, pipe the reply through `validate`/`score` and re-prompt if the score is below threshold:

```python
import subprocess
def style_ok(text, style_id):
    out = subprocess.run(
        ["python", "scripts/style_engine.py", "validate", style_id],
        input=text.encode("utf-8"), capture_output=True
    )
    import json
    result = json.loads(out.stdout.decode("utf-8"))
    return result["valid"]
# if not style_ok(reply, "sanguo"): re-prompt the model with the error list
```

---

## Custom Styles

Each style = one JSON file in `references/styles/<id>.style.json`. Copy an existing one and edit:

| Field | Meaning |
|-------|---------|
| `name`, `era` | Display metadata |
| `rules` | Core behavioral rules |
| `address_system` | self / other / authority / time words |
| `forbidden_replacements` | modern → classical word map |
| `style_templates` | Required sentence templates per situation |
| `rhetoric` | `must_use` / `forbidden` rhetorical devices |
| `quality_thresholds` | `max_sentence_length`, `max_modern_ratio`, `style_score_min` |

Then it is picked up automatically — **no code changes**:

```bash
python scripts/style_engine.py prompt mystyle
```

---

## Quality Loop (optional)

```
prompt → system prompt → model reply → validate/score → (below threshold?) re-prompt → done
```

This is what makes WenYan a **deterministic** style engine rather than a loose prompt: the same JSON drives both generation and grading.

---

**Made with ❤️ by [Pondsi](https://github.com/Pondsi)** — MIT License, attribution required.
