/**
 * Self-Improving AI Hook for OpenClaw
 *
 * Injects an AI/LLM-specific reminder to evaluate learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

const REMINDER_CONTENT = `
## AI / LLM Self-Improvement Reminder

After completing tasks, evaluate if any AI/model learnings should be captured:

**Log model issues when:**
- Model response quality dropped after provider update → \`.learnings/MODEL_ISSUES.md\`
- Inference latency spiked or exceeded threshold → \`.learnings/MODEL_ISSUES.md\`
- RAG retrieval returned irrelevant or stale chunks → \`.learnings/MODEL_ISSUES.md\`
- Embedding quality degraded after reindex → \`.learnings/MODEL_ISSUES.md\`
- Multimodal input failed (image/audio/video/PDF) → \`.learnings/MODEL_ISSUES.md\`
- Guardrail misfire (false positive or bypass) → \`.learnings/MODEL_ISSUES.md\`

**Log learnings when:**
- Better model or config discovered for a task → \`.learnings/LEARNINGS.md\` (model_selection)
- Prompt tweak significantly improved output → \`.learnings/LEARNINGS.md\` (prompt_optimization)
- Hallucination detected in factual response → \`.learnings/LEARNINGS.md\` (hallucination_rate)
- Context window overflow caused truncation → \`.learnings/LEARNINGS.md\` (context_management)
- Fine-tuned model regressed on eval set → \`.learnings/LEARNINGS.md\` (fine_tune_regression)
- Token cost exceeded budget projections → \`.learnings/LEARNINGS.md\` (cost_efficiency)

**Log feature requests when:**
- Missing AI capability (model A/B testing, eval framework, etc.) → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven:**
- Model behavior patterns → SOUL.md (e.g., "Claude 4 tends to over-qualify, use direct prompting")
- Model selection and workflow → AGENTS.md (e.g., "Use fast model for triage, capable model for code gen")
- Model/tool configuration → TOOLS.md (e.g., "Set temperature 0.1 for code, 0.7 for creative")

Log model name, provider, parameters (temperature, top-p), token usage, and latency with every entry.
`.trim();

const handler = async (event) => {
  if (!event || typeof event !== 'object') {
    return;
  }

  if (event.type !== 'agent' || event.action !== 'bootstrap') {
    return;
  }

  if (!event.context || typeof event.context !== 'object') {
    return;
  }

  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'AI_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
