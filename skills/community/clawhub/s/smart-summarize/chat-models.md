# Chat Models

| Model ID | Description |
|----------|-------------|
| `bedrock/claude-4-6-opus` | Claude 4.6 Opus — most powerful, 1M context |
| `bedrock/claude-4-5-sonnet` | Claude 4.5 Sonnet — balanced performance and cost |
| `bedrock/claude-4-5-haiku` | Claude 4.5 Haiku — fastest, simple tasks |
| `bedrock/claude-4-sonnet` | Claude 4 Sonnet |
| `bedrock/claude-3-7-sonnet` | Claude 3.7 Sonnet |
| `openai/gpt-5` | GPT-5 latest |
| `openai/gpt-5-mini` | GPT-5 Mini |
| `openai/gpt-4.1` | GPT-4.1 |
| `openai/gpt-4.1-mini` | GPT-4.1 Mini |
| `openai/gpt-4o` | GPT-4o multimodal |
| `openai/gpt-4o-mini` | GPT-4o Mini — fast and economical |
| `openai/o4-mini` | O4 Mini reasoning |
| `openai/o3-mini` | O3 Mini reasoning |
| `openai/o1` | O1 advanced reasoning |
| `vertex/gemini-2.5-pro` | Gemini 2.5 Pro |
| `vertex/gemini-2.5-flash` | Gemini 2.5 Flash — fast |
| `vertex/gemini-3-pro-preview` | Gemini 3 Pro Preview |
| `vertex/gemini-3-flash-preview` | Gemini 3 Flash Preview |
| `openrouter/deepseek/deepseek-r1` | DeepSeek R1 |
| `openrouter/google/gemini-2.5-pro-preview` | Gemini 2.5 Pro via OpenRouter |
| `openrouter/qwen/qwen3-coder-plus` | Qwen 3 Coder Plus |
| `perplexity/sonar-pro` | AI search with citations |
| `perplexity/sonar` | AI search |
| `minimax/abab6.5s-chat` | Chinese optimized (fast) |
| `huggingface/{org}/{model}` | Any HuggingFace model — dynamic, no pre-registration |

```bash
run.mjs --model bedrock/claude-4-5-sonnet --prompt "Explain quantum computing"
run.mjs --model openai/gpt-4o-mini --prompt "Summarize this" --context "Be concise"
```