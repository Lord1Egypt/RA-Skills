"""
IMA 知识库推送脚本
将 ClawHub Daily 推荐简报推送到腾讯 IMA 知识库

使用方法：
  python scripts/push_to_ima.py --recommendation data/recommended/2026-06-03.json

凭证优先级：CLI 参数 > 环境变量 > references/config.json
  - 环境变量：IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY
  - config.json：ima_client_id / ima_api_key / ima_kb_id

IMA 推送方式（auto 模式按优先级尝试）：

方式 A：IMA 官方 OpenAPI（推荐）
  - 两步流程：import_doc 创建笔记 → add_knowledge 添加到知识库
  - 凭证从环境变量或 config.json 读取
  - 默认推送到 FIM 知识库

方式 B：调用 ima-skill CLI
  - 前置条件：已安装 ima-skill（`pip install ima-skill` 或 `npm i -g ima-skill`）
  - 自动检测命令，subprocess 调用
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import requests

# FIM 知识库 ID（默认推送目标）
DEFAULT_FIM_KB_ID = "aFEGG-4YH3z_CaCSNVNC5dSJR5cutjlatcEQcNZjtlA="

# IMA 官方 OpenAPI 端点（注意：是 ima.qq.com，不是 ima.tencent.com）
IMA_API_BASE = "https://ima.qq.com"


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


def push_via_official_api(client_id, api_key, kb_id, content, title):
    """通过 IMA 官方 OpenAPI 推送（方式 A，推荐）

    两步流程：
    1. POST /openapi/note/v1/import_doc 创建笔记 → 返回 note_id
    2. POST /openapi/wiki/v1/add_knowledge 添加到知识库

    认证 header：ima-openapi-clientid + ima-openapi-apikey
    """
    headers = {
        "ima-openapi-clientid": client_id,
        "ima-openapi-apikey": api_key,
        "Content-Type": "application/json",
    }

    # Step 1: 创建笔记（import_doc）
    # IMA API: content_format=1 表示 MARKDOWN；不传 title，标题从 content 的第一个 H1 提取
    import_doc_url = f"{IMA_API_BASE}/openapi/note/v1/import_doc"
    # 确保 content 以 H1 标题开头（IMA 从 H1 提取标题）
    if not content.startswith("# "):
        content = f"# {title}\n\n{content}"
    import_payload = {
        "content_format": 1,  # 1=MARKDOWN
        "content": content,
    }

    try:
        print(f"  [IMA-API] Step 1: 创建笔记 (import_doc)...")
        resp1 = requests.post(import_doc_url, headers=headers, json=import_payload, timeout=30)
        resp1_data = resp1.json() if resp1.headers.get("Content-Type", "").startswith("application/json") else {}

        if resp1.status_code != 200:
            return False, f"import_doc 失败: HTTP {resp1.status_code} - {resp1.text[:200]}"

        # IMA API 返回格式: {"code":0, "data":{"note_id":"..."}}
        if resp1_data.get("code") != 0:
            return False, f"import_doc API 错误: {resp1_data.get('msg', '未知')} (code={resp1_data.get('code')})"

        # 从 data 中提取 note_id
        note_id = resp1_data.get("data", {}).get("note_id")
        if not note_id:
            return False, f"import_doc 未返回 note_id，响应: {json.dumps(resp1_data, ensure_ascii=False)[:300]}"

        print(f"  [IMA-API] Step 1 成功: note_id={note_id}")

    except requests.exceptions.RequestException as e:
        return False, f"import_doc 请求异常: {e}"
    except Exception as e:
        return False, f"import_doc 异常: {e}"

    # Step 2: 添加到知识库（add_knowledge）
    # IMA API: 用 knowledge_base_id（不是 kb_id），media_type=11 表示笔记
    add_kb_url = f"{IMA_API_BASE}/openapi/wiki/v1/add_knowledge"
    add_kb_payload = {
        "media_type": 11,
        "title": title,
        "knowledge_base_id": kb_id,
        "note_info": {
            "content_id": note_id,
        },
    }

    try:
        print(f"  [IMA-API] Step 2: 添加到知识库 (kb_id={kb_id[:16]}...)...")
        resp2 = requests.post(add_kb_url, headers=headers, json=add_kb_payload, timeout=30)
        resp2_data = resp2.json() if resp2.headers.get("Content-Type", "").startswith("application/json") else {}

        if resp2.status_code != 200:
            return False, f"add_knowledge 失败: HTTP {resp2.status_code} - {resp2.text[:200]}"

        if resp2_data.get("code") != 0:
            return False, f"add_knowledge API 错误: {resp2_data.get('msg', '未知')} (code={resp2_data.get('code')})"

        print(f"  [IMA-API] Step 2 成功: 已添加到知识库")
        return True, f"note_id={note_id}, kb_id={kb_id}"

    except requests.exceptions.RequestException as e:
        return False, f"add_knowledge 请求异常: {e}"
    except Exception as e:
        return False, f"add_knowledge 异常: {e}"


def push_via_cli(kb_id, content, title):
    """通过 ima-skill CLI 推送（方式 B）"""
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


def main():
    parser = argparse.ArgumentParser(description="推送推荐到 IMA 知识库")
    parser.add_argument("--recommendation", required=True, help="daily_recommend.py 生成的 JSON")
    parser.add_argument("--config", default="references/config.json", help="凭证配置文件路径")
    parser.add_argument("--client-id", default=None, help="IMA client_id（优先级：CLI > 环境变量 > config）")
    parser.add_argument("--api-key", default=None, help="IMA api_key（优先级：CLI > 环境变量 > config）")
    parser.add_argument("--kb-id", default=None, help="IMA kb_id（默认：FIM 知识库）")
    parser.add_argument("--mode", choices=["official", "cli", "auto"], default="auto",
                        help="推送方式：official（官方OpenAPI）/ cli（CLI）/ auto（自动检测，默认）")
    args = parser.parse_args()

    # 凭证优先级：CLI 参数 > 环境变量 > config.json
    config = load_config(args.config) or {}
    client_id = (
        args.client_id
        or os.environ.get("IMA_OPENAPI_CLIENTID")
        or config.get("ima_client_id")
    )
    api_key = (
        args.api_key
        or os.environ.get("IMA_OPENAPI_APIKEY")
        or config.get("ima_api_key")
    )
    # kb_id：CLI 参数 > config.json > FIM 默认值（过滤占位符）
    config_kb_id = config.get("ima_kb_id")
    if config_kb_id and config_kb_id.startswith("<"):
        config_kb_id = None  # 占位符，忽略
    kb_id = args.kb_id or config_kb_id or DEFAULT_FIM_KB_ID

    if not client_id or not api_key:
        print("[Error] 缺少 IMA 凭证（client_id / api_key）。")
        print("  优先级：CLI 参数 > 环境变量 > config.json")
        print("  环境变量：IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY")
        return 1

    print(f"[IMA] 凭证来源: client_id={'CLI/ENV' if args.client_id or os.environ.get('IMA_OPENAPI_CLIENTID') else 'config'}")
    print(f"[IMA] 知识库: {kb_id[:16]}... ({'FIM默认' if kb_id == DEFAULT_FIM_KB_ID else '自定义'})")

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
        # 优先级：官方 OpenAPI > CLI
        print("  [Info] auto 模式：优先尝试官方 OpenAPI...")
        success, msg = push_via_official_api(client_id, api_key, kb_id, content, title)
        if not success:
            print(f"  [Info] 官方 API 失败，尝试 CLI...")
            success, msg = push_via_cli(kb_id, content, title)
    elif args.mode == "official":
        success, msg = push_via_official_api(client_id, api_key, kb_id, content, title)
    else:  # cli
        success, msg = push_via_cli(kb_id, content, title)

    if success:
        print(f"[IMA] 推送成功 ✓")
        return 0
    else:
        print(f"[Error] IMA 推送失败: {msg}")
        print("\n排查建议：")
        print("  1. 确认 IMA 凭证有效（环境变量 IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY）")
        print("  2. 方式 A（推荐）：官方 OpenAPI，凭证从环境变量读取")
        print("  3. 方式 B：安装 ima-skill CLI（`pip install ima-skill`）")
        print("  4. 详细文档：https://github.com/EdwardWason/clawhub-daily")
        return 1


if __name__ == "__main__":
    sys.exit(main())
