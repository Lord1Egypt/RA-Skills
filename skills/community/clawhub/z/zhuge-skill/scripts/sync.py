"""
共同进化 — 晶体池同步（v1.0.1 起：只读取，不上传）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
架构级隐私合约（不可绕过）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

本 skill 从 v1.0.1 起采取**单向消费**设计：
  ✓ 可以 pull —— 从公共晶体池拉取别人贡献的匿名晶体
  ✗ 不可以 push —— 本模块**没有上传通道**

这是**架构保证**，不是"现在没写以后可能加"：
  - 你的预测历史、比赛记录、API key、任何本地数据永远不会被本 skill 上传到任何地方
  - 作者 / skill 维护者也无法通过本 skill 读到你的数据——因为没有通道
  - 如果你未来 fork 本 skill 并想加共享功能，请自觉遵循白名单脱敏（见 PRIVACY.md）

工作模式：
  pull:   从公共 GitHub Release 拉匿名晶体（单向入）
  status: 本地查看晶体池

用法：
    python scripts/sync.py pull               # 拉公共晶体
    python scripts/sync.py status             # 查看本地晶体池

远程地址（可被 ZHUGE_REMOTE_CRYSTAL_URL 环境变量覆盖）：
    https://raw.githubusercontent.com/yangfei222666-9/zhuge-crystals/main/crystals.jsonl
    —— 这是一个**公共只读** URL，curl 一下就能看到内容，完全透明。
"""
import sys
import json
import os
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.crystallizer import (CRYSTALS_LOCAL, CRYSTALS_SHARED, load_crystals,
                                crystallize)
from core.welcome import (NEON_CYAN, NEON_GREEN, NEON_YELLOW, GOLD,
                          DIM, BOLD, RESET, HOT_RED as RED)

REMOTE_URL = os.getenv("ZHUGE_REMOTE_CRYSTAL_URL",
    "https://raw.githubusercontent.com/yangfei222666-9/zhuge-crystals/main/crystals.jsonl")

# ===== 隐私白名单（给 fork 者的参考常量，本脚本自身不使用） =====
# 如果你 fork 后想加共享功能，请只上传这些字段，绝不包括其它
ALLOWED_SHARED_FIELDS = {
    "crystal_id",   # 匿名 hash，不含用户标识
    "version",      # 晶体 schema 版本
    "trigger",      # {hexagram, yang_count} — 纯结构化特征
    "outcome",      # 如 "1x2=home" — 枚举值
    "stats",        # {matches, hits, rate, ci_95} — 纯数值
    "tags",         # 分类标签
}


def status():
    local = load_crystals()

    print(f"\n  {NEON_CYAN}╔═══ 晶体池状态 {' ' * 30}═══╗{RESET}")
    print(f"  {NEON_CYAN}║{RESET}")
    print(f"  {NEON_CYAN}║{RESET}  本地晶体: {GOLD}{len(local)}{RESET} 个")
    print(f"  {NEON_CYAN}║{RESET}  远程地址: {DIM}{REMOTE_URL}{RESET}")
    print(f"  {NEON_CYAN}║{RESET}  {DIM}（单向消费架构：本 skill 不上传任何数据）{RESET}")
    print(f"  {NEON_CYAN}║{RESET}")

    if local:
        print(f"  {NEON_CYAN}║{RESET}  {BOLD}本地晶体一览（按命中率）{RESET}")
        sorted_crystals = sorted(local, key=lambda c: -c['stats']['rate'])
        for c in sorted_crystals[:10]:
            t = c['trigger']
            s = c['stats']
            print(f"  {NEON_CYAN}║{RESET}    {GOLD}[{c['crystal_id']}]{RESET} "
                  f"{t.get('hexagram','?')}卦 阳{t.get('yang_count','?')}/6 → "
                  f"{c['outcome']}  {NEON_GREEN}{s['rate']*100:.0f}%{RESET} ({s['hits']}/{s['matches']})")
    print(f"  {NEON_CYAN}╚{'═' * 50}╝{RESET}\n")


def pull():
    """从远程公共仓库拉晶体（只入不出）"""
    try:
        import requests
    except ImportError:
        print(f"\n  {RED}需要 requests，pip install requests{RESET}\n")
        return

    print(f"\n  从公共仓库拉取: {DIM}{REMOTE_URL}{RESET}")
    print(f"  {DIM}（此请求是只读的 HTTP GET，不携带任何本地数据）{RESET}")
    try:
        r = requests.get(REMOTE_URL, timeout=10)
        if not r.ok:
            print(f"  {RED}拉取失败 (HTTP {r.status_code}){RESET}")
            print(f"  {DIM}（可能仓库还没建。也可以手动维护 data/crystals_shared.jsonl）{RESET}\n")
            return
        new_crystals = []
        for line in r.text.splitlines():
            if line.strip():
                try:
                    new_crystals.append(json.loads(line))
                except Exception:
                    pass

        existing_ids = set()
        if CRYSTALS_SHARED.exists():
            with open(CRYSTALS_SHARED, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            existing_ids.add(json.loads(line)["crystal_id"])
                        except Exception:
                            pass

        CRYSTALS_SHARED.parent.mkdir(parents=True, exist_ok=True)
        added = 0
        with open(CRYSTALS_SHARED, "a", encoding="utf-8") as f:
            for c in new_crystals:
                if c.get("crystal_id") and c["crystal_id"] not in existing_ids:
                    f.write(json.dumps(c, ensure_ascii=False) + "\n")
                    added += 1

        print(f"  {NEON_GREEN}✓{RESET} 拉取完成: 远程 {len(new_crystals)} 个 → 本地新增 {added} 个\n")
    except Exception as e:
        print(f"  {RED}拉取出错: {e}{RESET}\n")


def main():
    p = argparse.ArgumentParser(
        description="晶体池同步 — v1.0.1 起单向消费架构（只 pull 不 push）"
    )
    p.add_argument("action", choices=["status", "pull"],
                   help="status=本地查看 / pull=从公共池拉匿名晶体")
    args = p.parse_args()

    if args.action == "status":
        status()
    elif args.action == "pull":
        pull()


if __name__ == "__main__":
    main()
