#!/bin/bash
# AI Self-Improvement Error Detector Hook
# Triggers on PostToolUse for Bash to detect model API errors, inference failures,
# RAG issues, and other AI/LLM-related problems
# Reads CLAUDE_TOOL_OUTPUT environment variable

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ERROR_PATTERNS=(
    "rate limit"
    "quota exceeded"
    "context length"
    "token limit"
    "max_tokens"
    "model not found"
    "deprecated"
    "hallucination"
    "factual error"
    "embedding"
    "vector"
    "retrieval"
    "chunk"
    "fine-tune"
    "training loss"
    "eval loss"
    "CUDA"
    "GPU"
    "out of memory"
    "OOM"
    "inference"
    "latency"
    "timeout"
    "modality"
    "unsupported format"
    "content filter"
    "guardrail"
    "blocked"
    "safety"
    "refusal"
    "RateLimitError"
    "APIError"
    "AuthenticationError"
    "InvalidRequestError"
    "ContextWindowExceededError"
    "ModelNotFoundError"
    "ServiceUnavailableError"
    "overloaded"
    "capacity"
    "throttle"
    "429"
    "503"
)

contains_error=false
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_error=true
        break
    fi
done

if [ "$contains_error" = true ]; then
    cat << 'EOF'
<ai-error-detected>
An AI/model error was detected in command output. Consider logging to .learnings/ if:
- Rate limit or quota exceeded → MODEL_ISSUES.md [MDL-YYYYMMDD-XXX] with provider details
- Context window overflow → LEARNINGS.md with context_management category
- Model not found or deprecated → MODEL_ISSUES.md with migration notes
- Inference timeout or latency spike → MODEL_ISSUES.md with latency measurement
- Fine-tuning loss anomaly → LEARNINGS.md with fine_tune_regression category
- GPU/CUDA out of memory → MODEL_ISSUES.md with model size and hardware specs
- Content filter or guardrail block → LEARNINGS.md with guardrails note
- Embedding or retrieval failure → MODEL_ISSUES.md with RAG pipeline details

Include model name, provider, parameters, token usage, and latency.
</ai-error-detected>
EOF
fi
