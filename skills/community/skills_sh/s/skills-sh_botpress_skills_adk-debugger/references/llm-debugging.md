# LLM Behavior Debugging

When the bot's code runs fine but the LLM makes bad decisions — wrong tools, fabricated data, refusals, or loops. These issues live in the model's reasoning, not in your runtime code.

Always use `adk traces --format json` to inspect `think` and `tool_call` spans.

---

## 1. Wrong Tool Selected

**Symptom:** The model picks a different tool than expected for the user's request.

**How to diagnose:**

```bash
adk traces --format json
```

1. Find the `think` span before the `tool_call` — this shows the model's reasoning
2. Compare the tool it chose vs the tool you expected
3. Read both tools' `description` fields — is the wrong tool's description a better match for the input?

**Common causes:**

- Tool descriptions are too similar or ambiguous
- The correct tool's description doesn't clearly cover the use case
- Too many tools available — the model gets confused with a large tool set

**Fixes:**

- **Sharpen descriptions:** Make each tool's purpose unambiguous. Include what the tool does NOT do.
- **Add negative examples:** "Do NOT use this tool for X — use Y instead."
- **Reduce tool count:** If tools are rarely used, consider consolidating or removing them
- **Last resort, use `confirm: true`:** Require user confirmation before executing, giving the user a chance to correct

---

## 2. Hallucinated Parameters

**Symptom:** The model invokes the right tool but fills in parameter values that the user never provided.

**How to diagnose:**

```bash
adk traces --format json
```

Check the `tool_call` span's `input` field against what the user actually said.

**Common causes:**

- Input schema is too loose (e.g., free-form `z.string()` where `z.enum()` would be better)
- No validation in the handler — the hallucinated value passes through
- The model infers values from context that don't exist

**Fixes:**

- **Tighten input schemas:** Use `z.enum()` for known values, add `.describe()` to clarify what each field expects
- **Add handler validation:** Check that input values make sense before using them
- **Last resort, require confirmation:** Set `confirm: true` on the tool so the user sees parameters before execution

---

## 3. Refusal

**Symptom:** The model refuses to perform an action, saying it can't or shouldn't do something.

**How to diagnose:**

```bash
adk traces --format json
```

Check `think` spans for safety-related reasoning. The model may cite content policy, uncertainty, or ethical concerns.

**Common causes:**

- The system prompt or instructions don't explicitly authorize the action
- The tool description sounds potentially harmful or sensitive
- The user's request is ambiguous and the model errs on the side of caution

**Fixes:**

- **Update instructions:** Explicitly authorize the actions in your conversation's `instructions` field
- **Soften tool descriptions:** Remove language that sounds risky (e.g., "delete all" → "remove selected")
- **Check `confirm` settings:** If `confirm: true` is set, the model knows the user will approve — make sure instructions reflect this

---

## 4. Token Limit Issues

**Symptom:** The model's responses are truncated, it loses context from earlier in the conversation, or it starts repeating itself.

**How to diagnose:**

- Long conversations with many turns
- Large tool outputs filling the context window
- `adk traces --format json` may show degraded reasoning in later `think` spans

**Common causes:**

- Conversation history is too long — no pruning or summarization
- Tool outputs are large (e.g., full database dumps, long API responses)
- Model configuration doesn't match the conversation's needs

**Fixes:**

- **Check model configuration:** Verify model settings in `agent.config.ts` — consider using a model with a larger context window
- **Trim tool outputs:** Return only what the model needs, not everything
- **Summarize long conversations:** Use Zai to summarize earlier turns before they fill the window
- **Use `maxIterations`:** Set a reasonable limit on agent iterations to prevent runaway conversations

---

## 5. Poor Extraction Quality

**Symptom:** Using `adk.zai.extract()` or similar `zai` operations returns incorrect or incomplete structured data.

**Common causes:**

- Schema descriptions are vague — the model doesn't know what each field means
- Input text is ambiguous or poorly formatted
- Wrong model for the task — some models extract better than others

**Fixes:**

- **Improve schema descriptions:** Add `.describe()` to every field with clear, specific descriptions
- **Provide examples:** Show the model what good output looks like
- **Try a different model:** Some models handle extraction better; check model configuration
- **Pre-process input:** Clean up or normalize the text before extraction
- See the **Edge Cases & Gotchas** section in [zai-agent-reference.md](../../adk/references/zai-agent-reference.md) for common pitfalls like hallucinated fields and chunk-window issues

---

## 6. Looping

**Symptom:** The model calls the same tool repeatedly, or cycles between tools without making progress.

**How to diagnose:**

```bash
adk traces --format json
```

Look for repeated `tool_call` spans with the same `tool_name` in sequence.

**Common causes:**

- Tool output doesn't clearly indicate success or completion — the model retries
- Instructions are ambiguous about when to stop
- The tool fails silently (returns empty/null) and the model keeps trying
- No iteration limit set

**Fixes:**

- **Improve tool output clarity:** Return clear success/failure messages that tell the model it's done
- **Add `onBeforeTool` guardrail:** Detect repeated calls and abort

  ```typescript
  // Create per-conversation to avoid leaking state across turns
  const makeLoopGuard = () => {
    const seen = new Set<string>()
    const onBeforeTool: Autonomous.Hooks['onBeforeTool'] = async ({ tool, input, controller }) => {
      const key = `${tool.name}:${JSON.stringify(input)}`
      if (seen.has(key)) {
        controller.abort('Already called this tool with these parameters')
        return
      }
      seen.add(key)
    }
    return { onBeforeTool }
  }
  ```

- **Set `maxIterations`:** Limit how many tool calls the agent can make per turn
- **Check instructions:** Add explicit stopping criteria ("after completing X, respond to the user")

---

## 7. Reading Model Reasoning

The `think` span type captures the model's internal reasoning before it acts. This is the most valuable debugging tool for LLM behavior issues.

**How to access:**

```bash
# Via CLI
adk traces --format json
# Look for spans with type "think" — the "content" field has the reasoning
```

**Via `onTrace` hook in code:**

```typescript
const onTrace: Autonomous.Hooks['onTrace'] = ({ trace }) => {
  if (trace.type === 'think') {
    console.debug(`[MODEL REASONING] ${trace.content}`)
  }
}
```

**What to look for:**

- Does the model correctly understand the user's intent?
- Does it consider the right tools?
- Does it have accurate context about the conversation state?
- Is it making assumptions that aren't supported by the input?

If the reasoning is wrong, the fix is usually in the instructions, tool descriptions, or the information available to the model — not in the code.
