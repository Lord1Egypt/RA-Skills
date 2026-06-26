# Zipsa Technical Reference

Zipsa is an OpenAI-compatible gateway that sits between your app and Claude, ChatGPT, or Gemini. It inspects each request locally, decides which parts are identity-bound, company-confidential, or safe to abstract, and routes only the prompts that genuinely need cloud knowledge.

## Why This Matters

Zipsa solves the privacy-utility tradeoff by:
- **Local-first**: personal data, internal business context, and security-sensitive details stay within your private zone.
- **Smart routing**: automatically decides what can stay local, what can be abstracted, and what actually needs cloud knowledge.
- **Semantic reformulation**: rewrites the entire question to abstract identity and proprietary context while preserving the technical, legal, clinical, or operational facts.

## Configuration

| Variable | Default | Notes |
| :--- | :--- | :--- |
| `LOCAL_MODEL` | `qwen3.5:9b` | Ollama model |
| `LOCAL_HOST` | `http://localhost:11434` | Ollama server |
| `EXTERNAL_PROVIDER` | `anthropic` | Choose: anthropic, gemini, openai |
| `CLAUDE_MODEL` | `claude-sonnet-4-6` | If using Anthropic |
| `GEMINI_MODEL` | `gemini-3-flash-preview` | If using Gemini |
| `OPENAI_MODEL` | `gpt-4o-mini` | If using OpenAI |

## Dual-Thread Sessions

Zipsa keeps two separate conversation threads:
1. **Full thread (private zone)**: everything, including all your personal, business, and operational context.
2. **Cloud thread (safe)**: only the turns where you went hybrid.

They diverge when you ask local-only questions, and re-converge on hybrid ones. Both stay in sync.

## Examples

### Case 1: Sensitive record lookup (stays local)
- User: "Look up John's SSN 123-45-6789 and payroll record"
- Zipsa: Uses local model, never sends to cloud.

### Case 2: Domain knowledge with personal data (goes hybrid)
- User: "Jane Smith (DOB 1985, SSN 123-45-6789) is a physician with HbA1c 8.4%. Treatment options?"
- Sent to cloud: "Healthcare professional, late 30s, with diabetes. HbA1c 8.4%. What escalation strategies exist?"
- Result: Cloud knowledge + Jane's actual context applied back locally.

## Multi-Turn Conversations

To maintain continuity over multiple turns, pass a `session_id` in the `extra_body`:

```python
response = client.chat.completions.create(
    model="zipsa",
    messages=[{"role": "user", "content": "..."}],
    extra_body={"session_id": "case-001"}
)
```
