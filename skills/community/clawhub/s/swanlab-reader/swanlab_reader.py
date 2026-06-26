#!/usr/bin/env python3
"""
SwanLab Reader
  runs <project>                — 项目下所有 run
  info <url>                    — 指标列表 + 配置
  history <url> <key...>        — 历史序列（支持 plot 模式）
  plot <url> <key>              — ASCII 趋势图
  compare <url1> <url2>...     — 多 run 对比
"""

import sys
import os
import re

import json
import numpy as np
import swanlab
import urllib.request
import urllib.error

BASE_URL = "https://swanlab.cn"
CONFIG_DIR = os.path.expanduser("~/.config/swanlab")
CONFIG_KEY_FILE = os.path.join(CONFIG_DIR, "key")


def api_get(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url)
    token = get_api_key()
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def api_post(path, data):
    url = f"{BASE_URL}{path}"
    token = get_api_key()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def get_api_key():
    # 1. 环境变量
    key = os.environ.get("SWANLAB_KEY") or os.environ.get("SWANLAB_API_KEY")
    if key:
        return key
    # 2. 配置文件
    if os.path.exists(CONFIG_KEY_FILE):
        with open(CONFIG_KEY_FILE) as f:
            key = f.read().strip()
        if key:
            return key
    return None


def save_api_key(key):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_KEY_FILE, "w") as f:
        f.write(key)


def make_api():
    key = get_api_key()
    if not key:
        print("ERROR: No API key. Run: swanlab set-key <key>", file=sys.stderr)
        print("       Or set SWANLAB_KEY env var.", file=sys.stderr)
        sys.exit(1)
    return swanlab.Api(api_key=key)


def parse_url(raw):
    raw = raw.strip().rstrip("/")
    from urllib.parse import urlparse
    if raw.startswith("http"):
        parts = [p for p in urlparse(raw).path.split("/") if p]
        if parts[0].startswith("@") and len(parts) >= 4:
            return parts[0][1:], parts[1], parts[3]
    else:
        parts = [p for p in raw.split("/") if p]
        if len(parts) == 3:
            return parts[0], parts[1], parts[2]
    raise ValueError(f"无法解析: {raw}")


def flatten(d, prefix=""):
    items = []
    for k, v in d.items():
        nk = f"{prefix}/{k}" if prefix else k
        if isinstance(v, dict) and "_target_" not in v:
            items.extend(flatten(v, nk).items())
        else:
            items.append((nk, v))
    return dict(items)


def cmd_runs(project):
    """列出项目下所有 run"""
    api = make_api()
    try:
        runs_list = list(api.runs(project))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"=== {project} ===  ({len(runs_list)} runs)")
    print(f"{'Name':<45} {'State':<10} {'ID':<25}")
    print("-" * 82)
    for r in runs_list:
        e = {"RUNNING": "🟢", "CRASHED": "🔴", "FINISHED": "✅", "FAILED": "❌"}.get(r.state, "⚪")
        print(f"{r.name:<45} {r.state:<10} {r.id:<25} {e}")
    print()


def cmd_info(url):
    """展示指标列表 + 配置，末尾打印 history 命令"""
    u, p, r = parse_url(url)
    api = make_api()
    exp = api.run(f"{u}/{p}/{r}")

    emoji = {"RUNNING": "🟢", "CRASHED": "🔴", "FINISHED": "✅", "FAILED": "❌"}.get(exp.state, "⚪")
    print(f"{emoji} {exp.name}  [{exp.state}]")
    print(f"   {url.rstrip('/chart')}")
    print()

    # Config
    flat = flatten(exp.profile.config)
    highlights = [
        "actor/lr", "actor/grad_clip",
        "algorithm/kl_ctrl", "algorithm/adv_estimator", "algorithm/norm_adv_by_std_in_grpo",
        "rag_entropy/format_base", "rag_entropy/entropy_base",
        "rag_entropy/format_decay", "rag_entropy/entropy_decay",
        "rag_entropy/max_search_calls", "rag_entropy/retrieval_topk",
        "data/max_prompt_length", "data/max_response_length",
        "rollout/multi_turn", "rollout/max_assistant_turns",
        "rollout/response_length", "rollout/tensor_model_parallel_size",
        "rollout/gpu_memory_utilization",
        "actor/ppo_micro_batch_size_per_gpu", "actor/ppo_mini_batch_size",
    ]
    print("--- Config ---")
    for k in highlights:
        if k in flat:
            v = flat[k]
            if isinstance(v, dict):
                print(f"  {k}: {json.dumps(v)}")
            else:
                print(f"  {k}: {v}")
    print()

    # Scalar keys
    scalar_data = api_post(f"/api/project/{u}/{p}/runs/scalar/keys", {"cuids": [r]})
    scalar_keys = scalar_data.get("scalarKeys", [])
    groups = {}
    for k in sorted(set(k.replace("_timestamp","") for k in scalar_keys if not k.endswith("_timestamp"))):
        pre = k.split("/")[0]
        groups.setdefault(pre, []).append(k)

    print(f"--- Scalar Keys ({len(scalar_keys)} 项) ---")
    for pre in ["rag", "actor", "critic", "response", "num_turns", "search_count",
                "timing_s", "perf", "training", "val-aux", "global_seqlen"]:
        if pre in groups:
            keys = sorted(set(groups[pre]))
            print(f"  [{pre}] ({len(keys)})")
            for k in keys:
                print(f"    {k}")

    # history 命令模板
    default_keys = [f"rag/accuracy", f"actor/grad_norm"]
    print()
    print("--- 快速查询 ---")
    cmd = f"uv run python skills/swanlab-reader/swanlab_reader.py history {url}"
    print(f"  {cmd}")
    print(f"  {cmd} {' '.join(default_keys)}")
    print()


def cmd_history(url, keys, plot=False, width=60):
    """查看历史序列"""
    u, p, r = parse_url(url)
    api = make_api()
    exp = api.run(f"{u}/{p}/{r}")

    if not keys:
        print("用法: history <url> <key1> [key2] ...", file=sys.stderr)
        return

    df = exp.metrics(keys=list(keys), sample=None)
    cols = [c for c in df.columns if not c.endswith("_timestamp")]
    df = df[cols]

    emoji = {"RUNNING": "🟢", "CRASHED": "🔴", "FINISHED": "✅", "FAILED": "❌"}.get(exp.state, "⚪")
    steps = len(df)
    print(f"{emoji} {exp.name}  steps={steps}")
    print()

    for key in keys:
        if key not in df.columns:
            print(f"[{key}] ❌ 不存在")
            continue
        v = df[key].dropna()
        if len(v) == 0:
            continue

        mean, std, mn, mx = v.mean(), v.std(), v.min(), v.max()
        slope = np.polyfit(np.arange(len(v)), v.values, 1)[0] if len(v) > 1 else 0
        trend = "↗" if slope > 0.0005 else ("↘" if slope < -0.0005 else "→")

        flag = ""
        if "accuracy" in key and mean < 0.3:
            flag = " 🔴"
        elif "clip_ratio" in key and mn >= 1.0:
            flag = " 🔴"
        elif "grad_norm" in key and mean > 5:
            flag = " 🔴"

        print(f"[{key}]{flag}")
        print(f"  mean={mean:.4f} std={std:.4f} min={mn:.4f} max={mx:.4f}  {trend}{abs(slope):.6f}")
        print(f"  前5步: {v.iloc[:5].values}")
        print(f"  后5步: {v.iloc[-5:].values}")

        if plot:
            print(f"  趋势（ASCII）:")
            _plot_ascii(v, width=width)

        print()


def _plot_ascii(series, width=60, height=8):
    """绘制简易 ASCII 趋势图"""
    v = series.dropna().values
    if len(v) == 0:
        return

    # 归一化到 [0, 1]
    mn, mx = v.min(), v.max()
    rng = mx - mn if mx != mn else 1
    norm = (v - mn) / rng

    # 采样到 width 个点
    n = len(norm)
    if n > width:
        idx = np.linspace(0, n - 1, width, dtype=int)
        norm = norm[idx]

    # 构建字符图
    rows = height
    bins = np.linspace(0, 1, rows + 1)
    canvas = [[" "] * len(norm) for _ in range(rows)]

    for i, x in enumerate(norm):
        bin_idx = int((1 - x) * rows)
        bin_idx = max(0, min(rows - 1, bin_idx))
        canvas[bin_idx][i] = "█"

    # 打印
    rng_display = mx - mn
    for row in canvas:
        print("  " + "".join(row))

    # 标注
    print(f"  └{'─' * len(norm)}┘")
    print(f"   {mn:>10.4f}  {'':>{len(norm)//2 - 5}}  {mx:.<10.4f}")
    print(f"   step=0{rng_display:>+10.4f}/step")
    print()


def cmd_plot(url, key, width=60):
    """绘制单个指标的 ASCII 趋势图"""
    u, p, r = parse_url(url)
    api = make_api()
    exp = api.run(f"{u}/{p}/{r}")

    emoji = {"RUNNING": "🟢", "CRASHED": "🔴", "FINISHED": "✅", "FAILED": "❌"}.get(exp.state, "⚪")
    print(f"{emoji} {exp.name}  [{key}]")
    print()

    df = exp.metrics(keys=[key], sample=None)
    cols = [c for c in df.columns if not c.endswith("_timestamp")]
    v = df[cols[0]].dropna()
    print(f"  steps={len(v)}  mean={v.mean():.4f}  min={v.min():.4f}  max={v.max():.4f}")
    print()
    _plot_ascii(v, width=width)


def cmd_compare(urls):
    runs = []
    for url in urls:
        try:
            u, p, r = parse_url(url)
        except:
            print(f"无法解析: {url}", file=sys.stderr)
            continue
        api = make_api()
        exp = api.run(f"{u}/{p}/{r}")
        try:
            scalar_keys = exp.scalar_keys
            keys = [k for k in scalar_keys if not k.endswith("_timestamp")]
            df = exp.metrics(keys=keys, sample=1)
            latest = {c: df[c].iloc[-1] for c in df.columns if not c.endswith("_timestamp")}
        except:
            latest = {}
        e = {"RUNNING": "🟢", "CRASHED": "🔴", "FINISHED": "✅", "FAILED": "❌"}.get(exp.state, "⚪")
        runs.append({"name": exp.name[:22], "state": exp.state, "latest": latest, "steps": len(df)})

    if not runs:
        print("无可用 run 数据", file=sys.stderr)
        return

    all_keys = set()
    for rn in runs:
        all_keys.update(rn["latest"].keys())
    all_keys = sorted(all_keys)

    print(f"{'Metric':<35}", end="")
    for rn in runs:
        print(f" | {rn['name']} {rn['state']}({rn['steps']})", end="")
    print()
    print("-" * (37 + 26 * len(runs)))

    for key in all_keys:
        print(f"{key:<35}", end="")
        for rn in runs:
            v = rn["latest"].get(key)
            if v is None or (isinstance(v, float) and np.isnan(v)):
                print(f" | {'-':>24}", end="")
            elif isinstance(v, float):
                flag = ""
                if "accuracy" in key and v < 0.3:
                    flag = "🔴"
                elif "grad_norm" in key and v > 5:
                    flag = "🔴"
                print(f" | {v:>22.4f}{flag}", end="")
            else:
                print(f" | {str(v):>24}", end="")
        print()
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1]

    if action == "set-key":
        if len(sys.argv) < 3:
            print("用法: swanlab set-key <key>")
            sys.exit(1)
        save_api_key(sys.argv[2])
        print("Key 已保存到 ~/.config/swanlab/key")
        sys.exit(0)

    try:
        if action == "runs":
            if len(sys.argv) < 3:
                print("用法: swanlab runs <username/project>")
                sys.exit(1)
            cmd_runs(sys.argv[2])

        elif action == "info":
            if len(sys.argv) < 3:
                print("用法: swanlab info <url>")
                sys.exit(1)
            cmd_info(sys.argv[2])

        elif action == "history":
            if len(sys.argv) < 4:
                print("用法: swanlab history <url> <key1> [key2] ...")
                sys.exit(1)
            plot = "--plot" in sys.argv
            keys = [k for k in sys.argv[3:] if k != "--plot"]
            cmd_history(sys.argv[2], keys, plot=plot)

        elif action == "plot":
            if len(sys.argv) < 4:
                print("用法: swanlab plot <url> <key>")
                sys.exit(1)
            cmd_plot(sys.argv[2], sys.argv[3])

        elif action == "compare":
            if len(sys.argv) < 3:
                print("用法: swanlab compare <url1> <url2> ...")
                sys.exit(1)
            cmd_compare(sys.argv[2:])

        else:
            print(f"未知命令: {action}", file=sys.stderr)
            print(__doc__)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
