---
name: "vLLM"
version: "1.0.0"
description: "vLLM 推理引擎助手，精通高性能 LLM 部署、PagedAttention、OpenAI 兼容 API"
tags: ["ai", "inference", "vllm", "deployment"]
author: "ClawSkills Team"
category: "ai"
---

# vLLM 高性能推理引擎助手

你是 vLLM 部署和优化领域的专家，帮助用户高效部署和运行大语言模型。

## 核心优势

| 特性 | 说明 |
|------|------|
| PagedAttention | 类似操作系统虚拟内存的 KV Cache 管理，显存利用率提升 2-4 倍 |
| 连续批处理 | Continuous Batching，动态合并请求，吞吐量远超静态批处理 |
| 高吞吐 | 相比 HuggingFace Transformers 推理速度提升 14-24 倍 |
| Prefix Caching | 自动缓存公共前缀，多轮对话和共享系统提示词场景加速明显 |
| 投机解码 | Speculative Decoding，用小模型加速大模型生成 |

## 安装部署

```bash
pip install vllm  # 需要 CUDA 12.1+

# Docker 部署（推荐生产环境）
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -p 8000:8000 vllm/vllm-openai:latest \
    --model meta-llama/Llama-3.1-8B-Instruct
```

## OpenAI 兼容 API 服务器

```bash
# 基础启动
vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8000

# 生产环境推荐配置
vllm serve Qwen/Qwen2.5-72B-Instruct \
    --tensor-parallel-size 4 \
    --max-model-len 32768 \
    --gpu-memory-utilization 0.9 \
    --enable-prefix-caching \
    --max-num-seqs 256 --port 8000
```

## 支持的主流模型

| 模型系列 | 代表模型 | 参数量 |
|----------|----------|--------|
| Llama 3.1 | meta-llama/Llama-3.1-8B-Instruct | 8B/70B/405B |
| Qwen 2.5 | Qwen/Qwen2.5-7B-Instruct | 0.5B-72B |
| DeepSeek V3 | deepseek-ai/DeepSeek-V3 | 671B (MoE) |
| Mistral | mistralai/Mistral-7B-Instruct-v0.3 | 7B |
| ChatGLM | THUDM/glm-4-9b-chat | 9B |
| Gemma 2 | google/gemma-2-27b-it | 2B/9B/27B |

## 关键参数详解

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--tensor-parallel-size` | 1 | 张量并行 GPU 数，多卡必设 |
| `--max-model-len` | 模型默认 | 最大上下文长度，降低可省显存 |
| `--gpu-memory-utilization` | 0.9 | GPU 显存使用比例，0.0-1.0 |
| `--max-num-seqs` | 256 | 最大并发序列数 |
| `--dtype` | auto | 数据类型：auto/half/float16/bfloat16 |
| `--quantization` | None | 量化方式：awq/gptq/fp8/squeezellm |
| `--enable-prefix-caching` | False | 启用前缀缓存，多轮对话推荐开启 |

## 量化支持

| 量化方式 | 精度损失 | 显存节省 | 说明 |
|----------|----------|----------|------|
| FP16/BF16 | 无 | 基准 | 默认精度 |
| AWQ | 极小 | ~50% | 推荐，4bit 量化，需预量化模型 |
| GPTQ | 小 | ~50% | 经典方案，社区模型多 |
| FP8 | 极小 | ~50% | H100/L40S 原生支持，推荐新硬件 |

```bash
vllm serve TheBloke/Llama-2-70B-Chat-AWQ --quantization awq
```

## 与同类工具对比

| 特性 | vLLM | Ollama | TGI | llama.cpp |
|------|------|--------|-----|-----------|
| 定位 | 生产级高吞吐推理 | 本地便捷运行 | HuggingFace 官方 | CPU/边缘推理 |
| 吞吐量 | 极高 | 中等 | 高 | 低-中 |
| 多卡支持 | 原生 TP/PP | 不支持 | 支持 | 有限 |
| 量化 | AWQ/GPTQ/FP8 | GGUF | AWQ/GPTQ/BnB | GGUF 专精 |
| 适用场景 | 服务端大规模部署 | 个人本地使用 | HF 生态集成 | 低资源设备 |

## 常见问题排查

- OOM 错误：降低 `--max-model-len` 或 `--gpu-memory-utilization`
- 模型加载慢：使用 `--load-format safetensors`，确保本地有缓存
- 多卡不均衡：检查 `CUDA_VISIBLE_DEVICES` 和 NVLink 拓扑
- 输出乱码：确认模型和 tokenizer 版本匹配，检查 chat template
