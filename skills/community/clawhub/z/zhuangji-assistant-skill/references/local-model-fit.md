# 本地大模型与硬件适配

本叶子只做本地文本生成推理的容量规划。用户问“这张显卡能跑多大模型”“16/24/32/96GB 显存适合什么模型”“30B/32B/70B 需要什么显卡”时读取；训练、LoRA/全参微调、吞吐、首 token 延迟、多卡互联和具体推理后端性能不在本估算范围内。

## 必须运行的查询

- 从模型反推显卡：运行 `python -B scripts/query_model_fit.py --params-b 30 --json`。若用户给出离线样本名，改用 `--model qwen3-30b-a3b`。给出明确量化和总上下文时，加 `--quantization q4/q5/q8/bf16 --context-tokens N`。
- 从现有硬件推模型：优先传库内 `--gpu-id`、`--memory-id`；只有用户只给容量时才传 `--vram-gib`、`--ram-gib`。用户 overlay 继续用 `--overlay`，不得从文字猜硬件 ID。
- 查显卡候选只采用脚本返回的 `minimum_gpu_candidates` 与 `recommended_gpu_candidates`。候选仍需按整机预算查询其余配件，并运行完整兼容检查。

## 双向口径

- 反向问题先给两档：`minimum_vram_gib` 是指定量化、上下文和单并发下的最低尝试档；`recommended_vram_gib` 是留出约 20% 规划余量的稳妥档。30B/32B 默认按 Q4：24GB 只写“短上下文、余量较小、条件可跑”，32GB 写“更稳妥”，并优先列 RTX 5090/5090D 32GB 类当前候选。不得把 RTX 5090D V2 24GB 与 32GB 版混为同一档。
- 正向问题按显存容量给默认模型档：16GB 主推 7–8B Q4，14B Q4 只作条件项；24GB 主推 14B、24B Q4，30/32B Q4 只作短上下文条件项；32GB 主推 24B/30B/32B Q4；96GB 主推 32B Q8 和 70/72B Q4/Q5。最终以脚本逐模型结果为准，不只复述档位表。
- MoE 必须按总参数量规划权重。Qwen3 30B A3B 虽每 token 激活约 3.3B，加载规划仍按 30.5B；不得用激活参数量冒充显存需求。

## 估算边界

脚本把显存拆成模型权重、运行余量和 KV cache。量化会减少权重占用；上下文、批大小和并发会增加 KV cache。Hugging Face 官方说明 Dynamic Cache 随生成增长，KV offload 和量化 cache 都以吞吐或延迟为代价。因此：

- 模型卡的 32K/128K/131K 是架构上限，不是消费卡可无约束使用的推荐上下文。超过默认上下文必须按模型配置重算。
- 离线样本缺层数、KV heads 或 head dimension 时，4K 以上返回 `needs_model_config`；不得补猜结构后给推荐。
- `recommended` 是容量估算，不是速度承诺；`conditional`/`needs_offload` 要写明短上下文、单并发或 offload 降速；`ram_insufficient`/`not_recommended` 不得改写为“能跑”。
- 系统内存容量影响 offload；频率只在发生 CPU/KV offload 时提示。DDR4 低于 2666 MT/s、DDR5 低于 4800 MT/s 或频率未知只产生速度警告，不能靠更高频率把模型档位升级。

## 用户可见表达

先回答结论，再写假设。例如：

> 30B 模型按 4 位量化、约 4K–8K 总上下文、单并发估算，24GB 显存可以尝试，但余量较小；32GB 更稳妥，当前消费级候选主要是 RTX 5090/5090D 32GB。系统内存至少 32GB，若要长上下文或 offload，建议 64GB。模型卡标注的最大上下文不代表这张卡能直接跑满。

不要写“任何 30B 都一定能跑”“5090 能跑满 128K”“96GB 可无约束跑 70B”。用户给出具体 Hugging Face repo 时，若离线样本未收录，联网读取该 repo 的官方 `config.json` 和模型卡，再把总参数、层数、attention heads、KV heads、hidden/head dimension 与目标总 token 代入同一公式；不要收集作者未公开的第三方推测数据。

## 官方依据

- Hugging Face 量化概览：<https://huggingface.co/docs/transformers/main/en/quantization>
- Hugging Face KV cache：<https://huggingface.co/docs/transformers/kv_cache>
- Hugging Face Accelerate 大模型加载/offload：<https://huggingface.co/docs/accelerate/main/concept_guides/big_model_inference>
- 离线校准样本：<https://huggingface.co/Qwen/Qwen3-8B>、<https://huggingface.co/Qwen/Qwen3-30B-A3B>、<https://huggingface.co/Qwen/Qwen3-32B>、<https://huggingface.co/Qwen/Qwen2.5-72B-Instruct>、<https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503>、<https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B>。
