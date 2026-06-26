# SGLang Server Configuration & Parallel Strategy

Reference for parallelism strategies, config reasoning, and how the launch scripts work.

## GPU HBM Reference


| GPU    | HBM per GPU | Architecture |
| ------ | ----------- | ------------ |
| MI355X | 288 GB      | gfx950       |
| MI300X | 192 GB      | gfx942       |
| MI308X | 192 GB      | gfx942       |


## Parallel Config Naming Convention

For **dense models**, config is simply TP/DP (e.g., `TP8`, `TP4_DP2`).

For **MoE models**, the convention is `<attention_parallel>+<MoE_parallel>`:

- `TP8+TP8` — TP=8 for both attention and MoE
- `TP4+EP4` — TP=4 for attention, EP=4 for MoE experts
- `DP4+EP4` — DP-attention=4 for attention, EP=4 for MoE experts
- `DP4+TP4` — DP-attention=4 for attention, TP=4 for MoE

## Parallelism Types

### TP (Tensor Parallelism)

Splits each layer's weight tensors across GPUs. Every GPU participates in computing every token, then results are all-reduced.

- Reduces per-token latency, but adds all-reduce communication overhead per layer.
- Use for attention layers when KV heads >= TP. Also works for MoE layers as an alternative to EP.

### DP (Data Parallelism / DP-Attention)

For **dense models**: Creates multiple independent replicas. Each replica handles different requests.

For **MoE models**: DP means **dp-attention** — parallelizes the attention computation across GPUs while MoE layers use a different strategy (usually EP). DP-attention is most commonly paired with EP, but can also pair with TP for MoE. Do NOT combine TP+DP for the attention side unless user explicitly asks.

### EP (Expert Parallelism)

Only for MoE models. Distributes experts across GPUs. Two modes:


| EP Mode           | Communication | Description                                                                             |
| ----------------- | ------------- | --------------------------------------------------------------------------------------- |
| **All-to-All EP** | All-to-all    | Each GPU holds a subset of experts. Tokens routed to the owning GPU. Uses mori backend. |
| **All-Reduce EP** | All-reduce    | Each GPU computes on a subset of experts, results combined via all-reduce.              |


Always ask the user which EP mode they want.

## How serve.sh Works

The `scripts/serve.sh` script handles server launch. Always use it (with `DRY_RUN=1` to preview) — don't construct commands manually. Here's what it does for each CONFIG:

### CONFIG parsing and sglang flags

`--tp-size` in sglang is the **world size** (total GPUs), NOT tensor parallelism degree. The script derives it from the first number in CONFIG (e.g., `DP4EP4` → `--tp-size 4`).


| CONFIG       | sglang flags generated                                                                                 | Why                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| `TP8`        | `--tp-size 8`                                                                                          | Pure TP, 8 GPUs                                                              |
| `DP4EP4`     | `--tp-size 4 --dp-size 4 --enable-dp-attention --enable-dp-lm-head --ep-size 4`                        | DP-attention requires both `--enable-dp-attention` AND `--enable-dp-lm-head` |
| `DP8EP8_A2A` | `--tp-size 8 --dp-size 8 --enable-dp-attention --enable-dp-lm-head --ep-size 8 --moe-a2a-backend mori` | All-to-all EP uses mori backend                                              |
| `TP4EP4`     | `--tp-size 4 --ep-size 4`                                                                              | TP for attention + EP for MoE, no DP flags                                   |
| `DP4TP4`     | `--tp-size 4 --dp-size 4 --enable-dp-attention --enable-dp-lm-head`                                    | DP-attention + TP for MoE, no EP                                             |


### Critical rules the script enforces

- **When DP > 1**: Always adds `--enable-dp-attention` AND `--enable-dp-lm-head`. These are required — without them, DP-attention will not work correctly.
- **When EP with all-to-all**: Adds `--moe-a2a-backend mori`. This requires the mori library to be installed.
- `**--disable-radix-cache`**: On by default (`DISABLE_RADIX_CACHE=1`) for reproducible benchmarking. User can opt out with `DISABLE_RADIX_CACHE=0`.
- `**--load-format dummy**`: On by default (`LOAD_DUMMY=1`) for fast startup without loading real weights. Set `LOAD_DUMMY=0` for real benchmarks with actual weights.
- `**--trust-remote-code**`: Always added.

### Env vars


| Env var               | Required | Default | Description                                                         |
| --------------------- | -------- | ------- | ------------------------------------------------------------------- |
| `MODEL_PATH`          | Yes      | —       | Path to model weights or HuggingFace model ID (must exist in cache) |
| `CONFIG`              | Yes      | —       | Parallel config string (e.g., `DP8EP8`, `TP4`, `DP4EP4_A2A`)        |
| `LOG_DIR`             | No       | `.`     | Directory for server log                                            |
| `PORT`                | No       | `30000` | Server port                                                         |
| `MTP`                 | No       | `0`     | MTP steps: `0`=off, `N`>0=enable with N speculative steps           |
| `MTP_ALGO`            | When MTP>0 | —     | Speculative algorithm: `NEXTN` or `EAGLE` (model-dependent)         |
| `LOAD_DUMMY`          | No       | `1`     | Use dummy weights: `0` for real weights                             |
| `DISABLE_RADIX_CACHE` | No       | `1`     | Disable radix cache: `0` to keep it enabled                         |
| `BACKGROUND`          | No       | `0`     | Run server in background: `1` for nohup, `0` for foreground tee     |
| `DRY_RUN`             | No       | `0`     | Print command without executing: `1` to preview                     |
| `EXTRA_ARGS`          | No       | —       | Additional sglang flags appended to command                         |


## Reading Model Architecture from config.json

Read the model's `config.json` from the weights directory directly. The file is usually short — read the whole thing carefully rather than relying on a script, because field names vary across model families.

**Important:** Some models (especially multimodal ones) nest architecture fields under a sub-key like `text_config`. If top-level fields look sparse, check for nested config objects.

**Key fields to look for** (names may vary — search for similar names):


| What you need            | Common field names                                     |
| ------------------------ | ------------------------------------------------------ |
| Q head count             | `num_attention_heads`, `n_head`                        |
| KV head count            | `num_key_value_heads`, `num_kv_heads`, `n_head_kv`     |
| Expert count             | `num_experts`, `num_local_experts`, `n_routed_experts` |
| Active experts per token | `num_experts_per_tok`, `num_selected_experts`, `top_k` |
| Hidden size              | `hidden_size`, `d_model`                               |
| Number of layers         | `num_hidden_layers`, `n_layer`                         |


**Attention type detection:**

- **MLA** (Multi-Latent Attention): look for `qk_nope_head_dim`, `kv_lora_rank`, or `q_lora_rank` — MLA-specific fields (DeepSeek-V3/R1)
- **GQA**: KV head count < Q head count
- **MHA**: KV head count == Q head count
- **Hybrid attention**: some models mix attention types (e.g., linear + full attention) — look for separate head counts or per-layer attention type fields

**MTP detection:** look for `mtp_num_hidden_layers` or similar fields

**MTP speculative algorithm by model:**

| Model family       | MTP Algorithm | Notes                                    |
| ------------------- | ------------- | ---------------------------------------- |
| Qwen3.5 (397B MoE) | `NEXTN`       | Uses `--speculative-algorithm NEXTN`     |
| DeepSeek-V3/R1      | `EAGLE`       | Uses `--speculative-algorithm EAGLE`     |

When launching with `MTP>0`, set `MTP_ALGO` to the correct algorithm for the model.

## How to Reason About Parallel Config

Use the config.json values and GPU specs to analyze these factors:

### 1. Weight size vs GPU memory — which TP values fit?

`weight_size / world_size` must be less than GPU HBM (use ~70-80% of HBM for weights, rest for KV cache + activations).

Estimate weight size: for FP8, roughly `total_params_in_billions * 1 GB`. For BF16, `total_params * 2 GB`.

Example: 400GB FP8 model on MI355X (288GB): world_size=2 (200GB/GPU), 4 (100GB/GPU), 8 (50GB/GPU) — all fit.

### 2. Attention type and KV heads — TP vs DP for attention

- **MLA** (detected by `qk_nope_head_dim` or `kv_lora_rank`): Compresses KV into a latent representation (effectively 1 KV head). High TP for attention wastes KV cache. **DP-attention is strongly preferred for MLA models.**
- **GQA**: If `num_key_value_heads >= TP`, TP is efficient. If `num_key_value_heads < TP`, KV cache gets replicated wastefully.
- **MHA**: TP splits heads evenly. Usually fine up to TP = num_heads.

### 3. MoE vs Dense — which parallelism strategies apply?

- **Dense models** (no expert fields): Only TP/DP. Higher TP = lower latency; higher DP = more replicas = higher throughput.
- **MoE models**: DP+EP is the most popular config. Expert count determines EP granularity (EP must evenly divide expert count).

### 4. Putting it together — example analyses

**MLA MoE model (e.g., DeepSeek-R1) on 8x MI355X:**

- MLA → DP-attention preferred (not TP for attention)
- MoE → EP for experts
- Suggestion: DP8+EP8, DP4+EP4, plus TP8+TP8 as baseline

**GQA MoE model (e.g., Qwen3.5-397B) on 8x MI355X:**

- GQA with N KV heads → check if TP <= KV heads for attention efficiency
- MoE → DP+EP most popular
- ~400GB FP8 → world_size 2/4/8 all fit
- Suggestion: DP+EP configs, plus TP+EP hybrid

**GQA Dense model (e.g., Llama-70B) on 8x MI355X:**

- ~70GB FP8 → fits 1 GPU
- 8 KV heads → TP up to 8 efficient
- Suggestion: TP1_DP8, TP2_DP4, TP4_DP2, TP8

## Configuration Constraints

- **TP * DP** must equal total GPU count (for dense models without EP)
- **TP * EP** or **DP * EP** must equal total GPU count (for MoE with EP)
- EP must evenly divide the model's expert count
- EP is only meaningful for MoE models
- For MoE: attention and MoE layers can use different parallelism
- Do NOT combine TP+DP for the attention side unless user explicitly asks

## AMD-Specific Environment Variables

```bash
# Required: enable AITER optimized kernels
export SGLANG_USE_AITER=1

# Multi-node NCCL settings (adjust to your network)
export GLOO_SOCKET_IFNAME=<network_interface>
```

