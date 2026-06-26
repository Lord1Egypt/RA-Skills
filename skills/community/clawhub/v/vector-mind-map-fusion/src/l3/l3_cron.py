#!/usr/bin/env python3
"""
L3 Cron Entry Point
被 OpenClaw cron 触发，执行完整的 L3 pipeline。
触发时间：每两天 03:00（Asia/Shanghai）

路径基于项目根目录（不依赖 /workspace/fusion）

用法:
  python3 src/l3/l3_cron.py --user-open-id ou_xxx
"""

import sys
import os
import time as time_module
import json
import argparse
from datetime import datetime
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT / "src" / "l3"))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
os.chdir(str(PROJECT_ROOT / "src" / "l3"))

from l3_biweekly_consolidate import run, L3Processor, INFINITYDB_DIR, InfinityDBLite
from utils.cost_tracker import track_layer
from l3_manifest import write_manifest, read_manifest


def get_feishu_tenant_token(app_id: str, app_secret: str) -> str:
    """获取飞书 tenant access token"""
    import urllib.request
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
    return result.get("tenant_access_token", "")


def send_feishu_card(user_open_id: str, manifest: dict, app_id: str, app_secret: str):
    """发送飞书富文本卡片消息（manifest 汇总）"""
    import urllib.request

    # 获取 token
    token = get_feishu_tenant_token(app_id, app_secret)
    if not token:
        print("[L3 Cron] 飞书: 获取 tenant token 失败")
        return

    # 构造卡片内容
    l3 = manifest.get("l3", {})
    l1 = manifest.get("l1_cost", {})
    l2 = manifest.get("l2_cost", {})

    # 格式化 duration
    dur_ms = l3.get("duration_ms", 0)
    dur_str = f"{dur_ms / 1000:.1f}s" if dur_ms else "N/A"

    # manifest 时间（UTC → CST）
    run_at = manifest.get("run_at", "N/A")
    if run_at != "N/A":
        try:
            dt = datetime.fromisoformat(run_at.replace("+00:00", "+08:00").replace("Z", "+08:00"))
            run_at_str = dt.strftime("%m-%d %H:%M") + " CST"
        except Exception:
            run_at_str = run_at
    else:
        run_at_str = "N/A"

    card = {
        "receive_id": user_open_id,
        "msg_type": "interactive",
        "content": json.dumps({
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "🧠 L3 Biweekly 运行报告"},
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "note",
                    "elements": [
                        {"tag": "plain_text", "content": f"运行时间: {run_at_str}"}
                    ]
                },
                {"tag": "hr"},
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            f"**L3 本层**\n"
                            f"  • chunks_in: `{l3.get('chunks_in', 0)}`\n"
                            f"  • neurons_written: `{l3.get('neurons_written', 0)}`\n"
                            f"  • schemas: `{l3.get('schemas_written', 0)}` | relations: `{l3.get('relations_written', 0)}`\n"
                            f"  • ollama_calls: `{l3.get('ollama_calls', 0)}` | tokens≈ `{l3.get('tokens_approx', 0)}`\n"
                            f"  • duration: `{dur_str}`\n"
                            f"  • InfinityDB nodes: `{l3.get('infinitydb_nodes_before', '?')}` → `{l3.get('infinitydb_nodes_after', '?')}` (+`{l3.get('infinitydb_nodes_delta', 0)}`)"
                        )
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            f"**L1 上游**  (`{l1.get('chunks_in', 0)}`→`{l1.get('chunks_out', 0)}`) "
                            f"ollama `{l1.get('ollama_calls', 0)}` | dedup {l1.get('dedup', {})} "
                            f"| {l1.get('duration_ms', 0) / 1000:.1f}s"
                        )
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            f"**L2 上游**  (`{l2.get('chunks_in', 0)}`→`{l2.get('chunks_out', 0)}`) "
                            f"ollama `{l2.get('ollama_calls', 0)}` | dedup {l2.get('dedup', {})} "
                            f"| {l2.get('duration_ms', 0) / 1000:.1f}s"
                        )
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            f"**L2 清理**: `{', '.join(l3.get('l2_files_cleared', []) or ['无'])}`"
                        )
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            f"**Errors**: `{(l3.get('errors', []) or ['无'])}`"
                        )
                    }
                },
            ]
        })
    }

    data = json.dumps(card).encode()
    req = urllib.request.Request(
        f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            if result.get("code") == 0:
                print(f"[L3 Cron] 飞书卡片已发送")
            else:
                print(f"[L3 Cron] 飞书发送失败: {result.get('msg')}")
    except Exception as e:
        print(f"[L3 Cron] 飞书请求异常: {e}")


def main():
    parser = argparse.ArgumentParser(description="L3 Cron")
    parser.add_argument("--user-open-id", dest="user_open_id", default=os.environ.get("FEISHU_USER_OPEN_ID", ""))
    args, _ = parser.parse_known_args()

    t0 = time_module.time()
    print(f"[L3 Cron] 开始执行: {datetime.now().isoformat()}")

    # 记录运行前的 InfinityDB 节点数
    infinitydb_before = InfinityDBLite(str(INFINITYDB_DIR))
    nodes_before = len(infinitydb_before.data.get("neurons", {}))
    del infinitydb_before

    stats = run()
    duration_ms = int((time_module.time() - t0) * 1000)

    # 记录运行后的 InfinityDB 节点数
    infinitydb_after = InfinityDBLite(str(INFINITYDB_DIR))
    nodes_after = len(infinitydb_after.data.get("neurons", {}))
    del infinitydb_after

    # 写 cost tracker
    if stats and stats.get("neurons_written", 0) > 0:
        track_layer(
            layer="l3",
            ollama_calls=stats.get("ollama_calls", 0),
            tokens_approx=stats.get("tokens_approx", 0),
            chunks_in=stats.get("chunks_in", 0),
            chunks_out=stats.get("neurons_written", 0),
            duration_ms=duration_ms,
            extra={
                "schemas_written": stats.get("schemas_written", 0),
                "relations_written": stats.get("relations_written", 0),
            },
        )
    else:
        track_layer(
            layer="l3",
            chunks_in=0,
            chunks_out=0,
            duration_ms=duration_ms,
        )

    # 写 manifest
    l2_files_cleared = stats.get("l2_files_cleared", []) if stats else []
    stats["duration_ms"] = duration_ms
    write_manifest(
        l3_stats=stats,
        infinitydb_nodes_before=nodes_before,
        infinitydb_nodes_after=nodes_after,
        l2_files_cleared=l2_files_cleared,
    )
    print(f"[L3 Cron] manifest 已写入")

    # 发送飞书通知
    if args.user_open_id:
        manifest = read_manifest()
        # 注入 nodes 信息到 manifest（write_manifest 内部不返回这些）
        if manifest:
            manifest["l3"]["infinitydb_nodes_before"] = nodes_before
            manifest["l3"]["infinitydb_nodes_after"] = nodes_after
            manifest["l3"]["infinitydb_nodes_delta"] = nodes_after - nodes_before

        # 读取飞书 credentials（不走 env，cron 执行时 env 不会透传给子进程）
        app_id = "cli_a9637ebd21785ccd"
        secrets_file = Path.home() / ".openclaw/credentials/lark.secrets.json"
        app_secret = None
        if secrets_file.exists():
            with open(secrets_file) as f:
                app_secret = json.load(f).get("lark", {}).get("appSecret")

        if app_id and app_secret and manifest:
            send_feishu_card(args.user_open_id, manifest, app_id, app_secret)
        else:
            print(f"[L3 Cron] 飞书: 缺少 credentials (app_id={'有' if app_id else '无'}, app_secret={'有' if app_secret else '无'})")
    else:
        print(f"[L3 Cron] 飞书: 未传入 --user-open-id，跳过通知")

    print(f"[L3 Cron] 结束: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
