# Qwen Routing Matrix

Route by workload first, then by surface.

| Workload | Primary Goal | Preferred Qwen Family | Best Starting Surface | Notes |
|----------|--------------|-----------------------|-----------------------|-------|
| Fast interactive chat | Short latency | smaller instruct or chat-capable Qwen route | hosted or small local model | Keep prompts short and skip heavy reasoning mode |
| Deep reasoning | better chain quality | thinking-focused Qwen route | hosted or strong GPU server | Do not combine this with strict downstream parsing in one pass |
| Coding agent | tool use plus code edits | Qwen3-Coder family | hosted or vLLM/SGLang | Validate tool-calling behavior before production |
| Deterministic JSON | stable machine-readable output | instruct route with low temperature | hosted or local after schema checks | Use a second pass if the main prompt needs creativity |
| Vision or multimodal | image understanding | Qwen VL-capable route | hosted first | Confirm multimodal support from live model list |
| Cheap local experimentation | privacy and low cash cost | small Qwen route or quantized checkpoint | Ollama or llama.cpp-style local stack | Accept lower quality and tighter context |
| Team GPU serving | throughput and central control | medium or large Qwen route | vLLM or SGLang | Separate server tuning from prompt tuning |

## Practical Decision Loop

1. Identify the workload.
2. Check whether hosted, local, or hybrid constraints apply.
3. Fetch live model IDs from the current surface.
4. Test one minimal payload per candidate.
5. Save one primary route and one fallback if the workflow is recurring.

## Two-Pass Pattern

Use this whenever the workflow needs both reasoning and strict automation:

1. Reasoning pass: let Qwen analyze, compare, or plan.
2. Normalization pass: ask for strict JSON only, with no extra prose.

This is more reliable than demanding perfect reasoning and perfect machine-readable output from the same response.
