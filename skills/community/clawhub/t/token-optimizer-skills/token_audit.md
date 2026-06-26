---
name: token-audit
description: Audits the agent's context window for token consumption and bloat. Use this skill when asked to "analyze token usage", "find context bloat", "check token limits", or "diagnose high token usage" to evaluate how much space skills, conversation history, and prompts are taking.
---

# Token Audit Skill

This skill allows you to diagnose and report on the token consumption of the current context window, identifying bloat, inefficiencies, and memory hogs.

## 1. Auditing Workflow

When asked to audit token consumption, follow this sequence:

1. **Calculate the System Prompt & Skills Cost**
   Identify which skills are currently loaded. Extract their metadata and SKILL.md sizes.
2. **Calculate Conversation History Cost**
   Examine how long the current conversation has run and estimate the lengths of recent tool outputs (e.g., grep results, large file reads).
3. **Run the Math**
   You can estimate visually (1000 chars approximates ~250-300 tokens) or, for precise files, run `python <SKILL_PATH>/scripts/count_tokens.py --input <filename>`.
4. **Generate the "Token Budget Report"**
   Produce the final report in Markdown.

## 2. Token Budget Report Format

Use this format to present your findings to the user:

```markdown
## 📊 Token Budget Report

**Total Estimated Tokens:** `~<NUM>k (of 128k/200k limit)`

### 🍰 Breakdown by Layer
| Layer | Estimated Tokens | % of Total | Status |
|---|---|---|---|
| 🛠️ System + KIs + Skills | X,XXX | XX% | `Healthy / Bloated` |
| 💬 Conversation History | X,XXX | XX% | `Healthy / Too Long` |
| 📄 Open Documents | X,XXX | XX% | `Normal` |
| 🧠 Tool Outputs | X,XXX | XX% | `Warning: Huge outputs detected!` |

### 🚨 Bloat Warnings
- **[Skill / File Name]:** Takes up XXXX tokens unnecessarily.
- **[Conversation]:** You have multiple large RAG/Search dumps in the chat loop.

### 💡 Optimization Recommendations
1. Recommend using `token-optimizer`'s compression tools.
2. Recommend summarizing conversation.
3. Recommend lazy-loading skills.
```

## 3. Identifying Anti-Patterns

Watch for these specific memory-wasting anti-patterns:
- **Verbatim Tool Outputs:** Dumping a 500-line grep search into the context rather than returning matches only.
- **Overloaded Metadata:** A loaded skill or KI has a frontmatter description that is too long (description should be concise).
- **Repetitive Instructions:** The user task contains overlapping instructions or pasted boilerplates that could be consolidated using the `token-optimizer`.

## 4. Helper Scripts
Location: `scripts/count_tokens.py`

This script can evaluate a file or text and return precise token counts across different tokenizers.
```bash
# Example
echo "Hello world" | python scripts/count_tokens.py --model gemma-3
python scripts/count_tokens.py --input my_prompt.txt --model gpt-4o
```

*For more details on tokenizers, read `references/model-tokenizer-map.md`.*
