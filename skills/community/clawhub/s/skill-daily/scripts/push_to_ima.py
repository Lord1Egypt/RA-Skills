"""
IMA 知识库推送脚本
将 ClawHub Daily 推荐简报推送到腾讯 IMA 知识库

使用方法：
  python scripts/push_to_ima.py --recommendation data/recommended/2026-06-03.json

凭证从 references/config.json 的 ima_client_id / ima_api_key / ima_kb_id 读取

IMA 推送方式（任选其一）：

方式 A：调用 ima-skill CLI（推荐）
  - 前置条件：已安装 ima-skill（`pip install ima-skill` 或 `npm i -g ima-skill`）
  - 自动检测命令，subprocess 调用

方式 B：直接调用 IMA HTTP API
  - 需要在 config.json 中配置 ima_api_endpoint
  - 自定义 HTTP 协议（请参考 IMA 官方文档）
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import requests


def load_config(config_path):
    """从 config.json 加载 IMA 凭证"""
    path = Path(config_path)
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"  [Warn] 读取 config 失败: {e}")
        return None


def push_via_cli(kb_id, content, title):
    """通过 ima-skill CLI 推送（方式 A）"""
    # 检测可能的 CLI 命令名
    cli_candidates = ["ima", "ima-skill", "ima_cli", "ima_push"]
    for cli in cli_candidates:
        try:
            result = subprocess.run(
                [cli, "push", "--kb-id", kb_id, "--title", title, "--content", content],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                print(f"  [IMA-CLI] 推送成功（via {cli}）")
                return True, result.stdout
            else:
                print(f"  [Warn] {cli} 失败: {result.stderr}")
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"  [Warn] {cli} 异常: {e}")
    return False, "未找到可用的 ima CLI"


def push_via_api(api_endpoint, client_id, api_key, kb_id, content, title):
    """通过 HTTP API 推送（方式 B）"""
    try:
        resp = requests.post(
            f"{api_endpoint.rstrip('/')}/knowledge/push",
            json={
                "client_id": client_id,
                "api_key": api_key,
                "kb_id": kb_id,
                "title": title,
                "content": content,
                "format": "markdown"
            },
            timeout=30
        )
        if resp.status_code == 200:
            print(f"  [IMA-API] 推送成功")
            return True, resp.text
        else:
            return False, f"HTTP {resp.status_code}: {resp.text}"
    except Exception as e:
        return False, f"请求异常: {e}"


def main():
    parser = argparse.ArgumentParser(description="推送推荐到 IMA 知识库")
    parser.add_argument("--recommendation", required=True, help="daily_recommend.py 生成的 JSON")
    parser.add_argument("--config", default="references/config.json", help="凭证配置文件路径")
    parser.add_argument("--client-id", default=None, help="IMA client_id（也可放 config.json）")
    parser.add_argument("--api-key", default=None, help="IMA api_key（也可放 config.json）")
    parser.add_argument("--kb-id", default=None, help="IMA kb_id（也可放 config.json）")
    parser.add_argument("--api-endpoint", default=None, help="IMA API endpoint（HTTP 模式）")
    parser.add_argument("--mode", choices=["cli", "api", "auto"], default="auto",
                        help="推送方式：cli（CLI）/ api（HTTP）/ auto（自动检测）")
    args = parser.parse_args()

    # 凭证优先级：CLI 参数 > config.json
    config = load_config(args.config) or {}
    client_id = args.client_id or config.get("ima_client_id")
    api_key = args.api_key or config.get("ima_api_key")
    kb_id = args.kb_id or config.get("ima_kb_id")
    api_endpoint = args.api_endpoint or config.get("ima_api_endpoint")

    if not kb_id:
        print("[Error] 缺少 IMA kb_id。请通过 --kb-id 或 config.json 提供。")
        return 1
    if not client_id or not api_key:
        print("[Error] 缺少 IMA 凭证（client_id / api_key）。")
        print("  请通过 --client-id/--api-key 或 config.json 提供。")
        return 1

    rec_path = Path(args.recommendation)
    if not rec_path.exists():
        print(f"[Error] 推荐文件不存在: {rec_path}")
        return 1

    with open(rec_path, "r", encoding="utf-8") as f:
        rec = json.load(f)

    date = rec['date']
    dimension = rec['dimension']
    recs = rec['recommendations']
    total_scanned = rec.get('total_scanned', 0)
    deduplicated = rec.get('deduplicated', 0)

    # 准备内容
    md_path = Path(rec_path).with_suffix('.md')
    content = ""
    if md_path.exists():
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        # 从 JSON 拼接
        lines = [f"# ClawHub 每日洞察 | {date} ({dimension}维度)\n"]
        lines.append(f"\n扫描 {total_scanned} 个 Skill → 推荐 {len(recs)} 个，去重 {deduplicated} 个\n\n")
        for i, r in enumerate(recs, 1):
            lines.append(f"## {i}. {r['display_name']}\n\n")
            lines.append(f"- 链接: {r['url']}\n")
            lines.append(f"- 数据: ⭐{r['stars']} | 📥{r['downloads']}\n")
            if r.get('chinese_one_liner'):
                lines.append(f"- 能力解读: {r['chinese_one_liner']}\n")
            if r.get('recommend_reason'):
                lines.append(f"- 推荐理由: {r['recommend_reason']}\n")
            if r.get('next_action'):
                lines.append(f"- 下一步: {r['next_action']}\n")
            lines.append("\n")
        content = "\n".join(lines)

    title = f"ClawHub Daily {date} - {dimension}维度"
    print(f"[IMA] 推送 {date} ({dimension}) - {len(recs)} 个推荐 - {len(content)} 字")

    # 决定推送方式
    if args.mode == "auto":
        # 自动检测：先试 CLI，再试 API
        success, msg = push_via_cli(kb_id, content, title)
        if not success and api_endpoint:
            print(f"  [Info] CLI 失败，尝试 HTTP API: {api_endpoint}")
            success, msg = push_via_api(api_endpoint, client_id, api_key, kb_id, content, title)
    elif args.mode == "cli":
        success, msg = push_via_cli(kb_id, content, title)
    else:  # api
        if not api_endpoint:
            print("[Error] API 模式需要 --api-endpoint 或 config.json 中的 ima_api_endpoint")
            return 1
        success, msg = push_via_api(api_endpoint, client_id, api_key, kb_id, content, title)

    if success:
        print(f"[IMA] 推送成功 ✓")
        return 0
    else:
        print(f"[Error] IMA 推送失败: {msg}")
        print("\n排查建议：")
        print("  1. 确认 IMA 凭证有效（client_id / api_key / kb_id）")
        print("  2. 方式 A：安装 ima-skill CLI（`pip install ima-skill`）")
        print("  3. 方式 B：在 config.json 配置 ima_api_endpoint（参考 IMA 官方文档）")
        print("  4. 详细文档：https://github.com/EdwardWason/clawhub-daily")
        return 1


if __name__ == "__main__":
    sys.exit(main())
