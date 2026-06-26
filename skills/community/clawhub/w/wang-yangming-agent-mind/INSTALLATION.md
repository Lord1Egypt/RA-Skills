# Installation Guide — wang-yangming-agent-mind

How to install this skill across different agent platforms and runtimes.

---

## OpenClaw

OpenClaw loads skills from the agent's configured skills directory.

**Via filesystem:**
```bash
# Copy the skill directory to the OpenClaw skills registry
cp -r wang-yangming-agent-mind ~/.openclaw/skills/
```

**Via OpenClaw config (gateway `config/patch`):**
```json
{
  "skills": {
    "directories": [
      "~/.openclaw/skills",
      "/path/to/shared/skills"
    ]
  }
}
```

**Activation:** The skill activates automatically when the agent's context matches the trigger conditions in `SKILL.md`. No manual activation needed.

---

## Claude (Anthropic Desktop/Web App)

Claude does not currently support third-party skills in the public release. For **Claude Code** (CLI):

```bash
mkdir -p ~/.claude/skills
cp -r wang-yangming-agent-mind ~/.claude/skills/
```

---

## Cursor IDE

**Method 1 — .cursorrules:**
```bash
cat wang-yangming-agent-mind/SKILL.md >> .cursorrules
```

**Method 2 — Custom Rule File:**
```bash
mkdir -p .cursor/rules
cp wang-yangming-agent-mind/SKILL.md .cursor/rules/wang-yangming-agent-mind.md
```

**Activate:** Add to `.cursor/config.json`:
```json
{ "rules": [ "wang-yangming-agent-mind" ] }
```

---

## VS Code Copilot (GitHub Copilot Chat)

**Method 1 — Copilot Instructions:**
```bash
cat wang-yangming-agent-mind/SKILL.md >> .github/copilot-instructions.md
```

**Method 2 — VS Code Settings:**
```json
{
  "github.copilot.chat.instructions": [
    "Refer to ./.github/copilot-instructions.md for domain-specific guidance"
  ]
}
```

---

## Windsurf (Codeium)

**Method 1 — File-based:**
```bash
mkdir -p .windsurf
cp wang-yangming-agent-mind/SKILL.md .windsurf/wang-yangming-agent-mind.md
```

**Method 2 — Environment variable:**
```bash
export WINDSURF_INSTRUCTIONS=$(cat wang-yangming-agent-mind/SKILL.md)
```

---

## Continue (VS Code / JetBrains)

**config.json:**
```json
{
  "skills": [
    {
      "name": "wang-yangming-agent-mind",
      "description": "Heart-Mind doctrine for agent decision-making",
      "skillDir": "~/.continue/skills/wang-yangming-agent-mind"
    }
  ]
}
```

---

## Roo Code (VS Code Extension)

```json
{
  "rooCode.skillFiles": [
    "path/to/wang-yangming-agent-mind/SKILL.md"
  ]
}
```

---

## Vertex AI / Google AI Studio

Upload `SKILL.md` content as a **System Instruction** in Google AI Studio → Create Agent → System Instructions.

---

## LM Studio / Ollama (Local Models)

**Modelfile:**
```dockerfile
FROM your-model.gguf
PARAMETER temperature 0.7
SYSTEM """
[Paste full SKILL.md content here]
"""
```

```bash
ollama create wang-yangming-agent-mind -f /path/to/modelfile
ollama run wang-yangming-agent-mind
```

---

## Custom Agent (LangChain / LlamaIndex)

```python
from pathlib import Path

skill_dir = Path("wang-yangming-agent-mind")
skill_md = (skill_dir / "SKILL.md").read_text()

# Load as system prompt
prompt = SystemMessage(content=skill_md)
agent = ConversationalChatAgent(system_message=prompt, llm=llm, tools=tools)
```

---

## Platform Checklist

| Platform | Status | Method |
|---|---|---|
| OpenClaw | ✅ Full | Skills directory |
| Claude Code | ⚠️ Limited | `~/.claude/skills/` |
| Cursor | ⚠️ Via rules | `.cursor/rules/` |
| GitHub Copilot | ⚠️ Instruction file | `.github/copilot-instructions.md` |
| Windsurf | ⚠️ Via env/rc | `.windsurfrc` |
| Continue | ⚠️ Config | `config.json` |
| Roo Code | ⚠️ Skill file | `settings.json` |
| Vertex AI | ⚠️ System instruction | Upload as text |
| LM Studio / Ollama | ⚠️ Modelfile | Modelfile injection |
| Custom (LangChain) | ✅ Full | System prompt |

---

## Publishing to agent-skills-collections

```bash
# Fork https://github.com/fuleinist/agent-skills-collections
# Add wang-yangming-agent-mind/ directory to your fork
# Open a Pull Request to the main repo
```

---

## Quick Install (OpenClaw)

```bash
mkdir -p ~/.openclaw/skills
cp -r wang-yangming-agent-mind ~/.openclaw/skills/
# Restart agent session for auto-discovery
```