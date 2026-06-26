# OpenClaw Performance Benchmark Skill

3DMark-style performance benchmark for OpenClaw. Produces an **unbounded composite score** — higher is better, no upper limit, designed to grow with hardware and model improvements.

## What It Measures

| Dimension | Metric | Impact |
|-----------|--------|--------|
| 模型吞吐 | tokens/sec (generation) | Primary score driver |
| 首 Token 延迟 | TTFT in ms | Bonus for fast response |
| 工具调用效率 | avg tool call latency | Bonus for fast tools |
| 初始上下文 | session 启动时的 token 数 | 越重分越低 |
| 上下文效率 | context ratio (usable/raw) | Penalty if heavy context |
| 错误恢复 | pass rate across tests | Penalty for failures |

## Score Formula

```
Score = (Base + TTFT_bonus + Tool_bonus) × Context_ratio × Recovery

Base         = gen_tok/s × 10            ← 无上限
TTFT_bonus   = 10000 ÷ TTFT_ms          ← 越快越高
Tool_bonus   = 10000 ÷ tool_avg_ms      ← 越快越高
Context_ratio= 20000 ÷ initial_ctx_tokens × (actual_tok/s ÷ raw_tok/s)
               ↑                           ↑
               直接惩罚上下文大小          间接惩罚吞吐损失
               20k=1.0, 40k=0.5, 80k=0.25
Recovery     = 通过数 ÷ 总数             ← 0~1
```

Context_ratio 由两部分组成：
1. **上下文大小惩罚**: 20000 ÷ initial_ctx_tokens（以 20k 为基准，越大越低）
2. **吞吐损失比**: 实际吞吐 ÷ 原始吞吐（测量模型被上下文拖慢的程度）

两者相乘，既惩罚「上下文本身很重」，也惩罚「上下文导致吞吐下降」。

Grade scale: S+ (≥2000) → S (≥1000) → A (≥500) → B (≥200) → C (≥50) → D

## File Structure

```
~/.openclaw/skills/openclaw-benchmark/
├── SKILL.md          ← 本文件（协议说明）
└── score.py          ← 评分 + 报告生成

~/Downloads/OpenClaw-Benchmark/
├── results/          ← 跑分结果 HTML
└── baselines/        ← 基线数据 JSON（用于前后对比）
```

---

## Benchmark Protocol

### Step 0: System Pre-flight

Collect system info before running tests:

```bash
node --version
python3 --version
ls ~/.openclaw/skills/ | wc -l
```

Record: openclaw version, node version, os, arch, skill count, system prompt token estimate.

Check for common config issues:
- 是否有大量未使用的 skill（增加上下文负担）
- system prompt 是否过长
- 是否有 compaction 配置

### Step 1: Raw Model Speed (Test 1)

Spawn subagent:
```
直接回答，不要调用任何工具。用中文解释量子纠缠的基本原理，300字左右。
```

Record: runtime, output tokens → gen_tok_s = output / runtime

### Step 2: Complex Reasoning / TTFT (Test 2)

Spawn subagent:
```
直接回答，不要调用任何工具。解决以下问题：

一个水池有两个进水管A和B，一个排水管C。A管单独注满需要6小时，B管单独注满需要8小时，C管单独排空需要12小时。如果三管同时打开，多少小时能注满水池？请给出详细的解题过程和最终答案（分数形式）。
```

Record: runtime, complexity of answer

### Step 3: Tool Call Latency (Test 3)

Spawn subagent:
```
用 web_search 搜索 "OpenClaw AI assistant"，只搜一次。把搜索结果的标题列出来，不要做其他操作。
```

Record: runtime, tool_count → tool_avg_ms = runtime * 1000 / tool_count

### Step 4: File I/O Chain (Test 4)

Spawn subagent:
```
依次执行以下操作，每步完成后记录结果：
1. 用 exec 执行: echo "benchmark test $(date +%s)" > /tmp/openclaw_bench.txt
2. 用 read 读取 /tmp/openclaw_bench.txt 的内容
3. 用 exec 执行: rm /tmp/openclaw_bench.txt
把每步的操作和结果写入报告。
```

Record: runtime

### Step 5: Multi-Step Chain (Test 5)

Spawn subagent:
```
依次执行以下操作：
1. 用 exec 执行: node --version
2. 用 exec 执行: python3 --version
3. 对比两个版本号，用一句话说明哪个更新
不要并行执行命令，按顺序执行。
```

Record: runtime

### Step 6: Error Recovery (Test 6)

Spawn subagent:
```
依次执行：
1. 用 web_fetch 访问 https://httpstat.us/500 （会返回错误）
2. 访问失败后，用 web_search 搜索 "http status 500 meaning"
3. 根据搜索结果，用一句话解释 HTTP 500 错误
```

Record: runtime, whether fallback succeeded

---

## Step 7: Write Metrics & Compute Score

Write all metrics to `/tmp/bench_metrics.json`:

```json
{
  "gen_tok_s": 50.0,
  "ttft_ms": 800,
  "tool_avg_ms": 35500,
  "context_ratio": 0.50,
  "recovery_rate": 1.0,
  "system": {
    "os": "Darwin 24.6.0",
    "arch": "arm64",
    "openclaw_version": "2026.5.22",
    "node_version": "v25.2.1",
    "skill_count": 20,
    "system_prompt_tokens": 5000
  },
  "model": {
    "name": "xiaomi-coding/mimo-v2.5",
    "context_window": "1M",
    "provider": "xiaomi"
  },
  "tests": [
    { "id": 1, "name": "原始生成速度", "duration_s": 9, "total_tokens": 5500, "output_tokens": 450, "tool_calls": 0, "status": "ok" }
  ]
}
```

Run scorer:
```bash
python3 ~/.openclaw/skills/openclaw-benchmark/score.py /tmp/bench_metrics.json
```

Report auto-saves to `~/Downloads/OpenClaw-Benchmark/results/bench_<时间戳>.html`

---

## Step 8: Baseline Management (前后对比)

Save current run as baseline:
```bash
cp /tmp/bench_metrics.json ~/Downloads/OpenClaw-Benchmark/baselines/<name>.json
```

Compare against baseline:
```bash
python3 ~/.openclaw/skills/openclaw-benchmark/score.py /tmp/bench_metrics.json --compare ~/Downloads/OpenClaw-Benchmark/baselines/<name>.json
```

Comparison output shows:
- Score delta (e.g. +120 / -45)
- Per-metric deltas with color coding:
  - 🟢 改善 > 10%
  - 🟡 持平 ±10%
  - 🔴 退步 > 10%

### Naming conventions for baselines

- `default.json` — 默认配置基线
- `minimal.json` — 精简 skill 后的基线
- `new-model.json` — 换模型后的基线
- `after-optimize.json` — 优化后的基线

---

## Metrics JSON Schema

```json
{
  "gen_tok_s": 50.0,
  "ttft_ms": 200.0,
  "tool_avg_ms": 2000.0,
  "context_ratio": 0.85,
  "recovery_rate": 1.0,
  "system": {
    "os": "Darwin 24.6.0",
    "arch": "arm64",
    "openclaw_version": "2026.5.22",
    "node_version": "v25.2.1",
    "skill_count": 20,
    "system_prompt_tokens": 5000
  },
  "model": {
    "name": "xiaomi-coding/mimo-v2.5",
    "context_window": "1M",
    "provider": "xiaomi"
  },
  "tests": [
    {
      "id": 1,
      "name": "原始生成速度",
      "duration_s": 55,
      "total_tokens": 6600,
      "output_tokens": 450,
      "tool_calls": 0,
      "status": "ok"
    }
  ]
}
```

---

## Optimization Checklist

When score is low, check these in order:

| 检查项 | 影响维度 | 优化方向 |
|--------|---------|---------|
| Skill 数量过多 | context_ratio | 移除未使用的 skill |
| System prompt 过长 | context_ratio | 精简 AGENTS.md / SOUL.md |
| 模型选择 | gen_tok_s | 换更快的模型 |
| 网络环境 | tool_avg_ms | 检查 VPN/代理配置 |
| 无 compaction 配置 | context_ratio | 设置 triggerAtPercent: 75 |
| 流式模式未优化 | ttft_ms | 使用 chunked/full 模式 |

---

## Notes

- Run benchmarks in a **clean session** (no prior context) for accurate results
- Network-dependent tests (Test 3, 6) may vary; run multiple times and take median
- Context ratio: run Test 1 with minimal context vs full context to measure burden
- Score is designed to be **reproducible** — same system should get similar scores (±10%)
- Save results over time to track performance trends after config changes
- Baselines are JSON files, safe to git-track for team sharing
