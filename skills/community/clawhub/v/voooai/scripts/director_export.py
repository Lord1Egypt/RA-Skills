#!/usr/bin/env python3
"""编导模式 · 导出工作流并出片：GET /api/director/v2/<session_id>/export-workflow。

基于 Stage 3 分镜数据导出 ReactFlow 工作流 {nodes, edges}，本脚本自动归一化为
node-builder 执行格式 {nodes, connections}（镜像前端画布→执行转换），可：
  - 保存到文件（--output）供 execute_workflow.py 使用
  - 直接执行（--execute）：POST /api/node-builder/execute → 轮询 → 下载

鉴权：Authorization: Bearer vooai_xxx（AccessKey，需付费会员）。
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import (
    http_request, json_output, error_exit, format_business_error, reactflow_to_workflow,
)
from _director import require_session
from get_status import poll_until_complete, DEFAULT_POLL_INTERVAL, DEFAULT_TIMEOUT
from download_results import extract_result_urls, download_file, get_extension_from_url


def _download_execution_results(final_state: dict, output_dir: str, prefix: str = "") -> dict:
    """从 node-builder 执行完成态提取结果 URL 并下载到本地。"""
    urls = extract_result_urls(final_state)
    os.makedirs(output_dir, exist_ok=True)
    downloaded, errors = [], []
    for i, item in enumerate(urls, 1):
        url = item.get("url", "")
        if not url:
            continue
        ext = get_extension_from_url(url, ".bin")
        name = f"{prefix}_{i:02d}{ext}" if prefix else f"{i:02d}{ext}"
        filepath = os.path.join(output_dir, name)
        fp, err = download_file(url, filepath)
        if err:
            errors.append({"file": fp, "url": url, "error": err})
            print(f"✗ 下载失败: {os.path.basename(filepath)}", file=sys.stderr)
        else:
            downloaded.append(fp)
            print(f"✓ 已下载: {os.path.basename(filepath)}", file=sys.stderr)
    return {"downloaded_files": downloaded, "errors": errors, "total_urls": len(urls)}


def main():
    parser = argparse.ArgumentParser(
        description="导出编导工作流（可选直接执行出片）",
        epilog="""
环境变量:
  VOOOAI_ACCESS_KEY  必填，Bearer 鉴权（需付费会员）
  VOOOAI_BASE_URL    可选，默认 https://voooai.com

示例:
  # 导出并保存工作流 JSON（供 execute_workflow.py 使用）
  python3 director_export.py --output ./drama_workflow.json

  # 导出 + 直接执行 + 轮询 + 下载（一条龙）
  python3 director_export.py --execute --output-dir ./out/drama

  # 导出并打印归一化后的完整工作流到 stdout（便于管道）
  python3 director_export.py --print-workflow

  # 指定会话
  python3 director_export.py --session-id dv2_xxxxxxxxxxxx --execute

注意:
  - 需先在编导会话中完成 Stage 3 分镜设计，否则导出为空
  - --execute 会真实提交执行并消耗积分，调用前应向用户确认
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--session-id", default="", help="会话 ID（缺省读状态文件）")
    parser.add_argument("--tab-id", default=None, help="页签 ID（缺省读状态文件）")
    parser.add_argument("--state-file", default="", help="会话状态文件路径")
    parser.add_argument("--output", default="", help="保存归一化工作流 JSON 到该文件")
    parser.add_argument("--print-workflow", action="store_true", help="在 stdout JSON 中包含完整工作流")
    parser.add_argument("--execute", action="store_true", help="导出后直接提交 node-builder 执行")
    parser.add_argument("--no-wait", action="store_true", help="配合 --execute：仅提交不轮询")
    parser.add_argument("--output-dir", default="", help="配合 --execute：执行完成后下载结果到该目录")
    parser.add_argument("--prefix", default="", help="下载文件名前缀")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help=f"执行轮询超时秒数（默认 {DEFAULT_TIMEOUT}）")
    parser.add_argument("--interval", type=int, default=DEFAULT_POLL_INTERVAL, help=f"执行轮询间隔秒数（默认 {DEFAULT_POLL_INTERVAL}）")
    args = parser.parse_args()

    session_id, tab_id = require_session(args)

    qs = f"?tab_id={tab_id}" if tab_id else ""
    print("正在导出编导工作流...", file=sys.stderr)
    code, data = http_request("GET", f"/api/director/v2/{session_id}/export-workflow{qs}")
    if code != 200 or not (isinstance(data, dict) and data.get("success")):
        err = data if isinstance(data, dict) else {"message": str(data)}
        error_exit(format_business_error(code, {"error_code": err.get("error_code", ""),
                                                "message": err.get("error") or err.get("message", ""),
                                                "details": {}}))

    workflow = data.get("workflow", {}) or {}
    normalized = reactflow_to_workflow(workflow, director_session_id=session_id)
    node_count = len(normalized.get("nodes", []) or [])
    conn_count = len(normalized.get("connections", []) or [])

    out = {
        "success": True,
        "session_id": session_id,
        "node_count": node_count,
        "connection_count": conn_count,
        "metadata": workflow.get("metadata", {}),
        "warnings": data.get("warnings", []),
    }

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(normalized, f, ensure_ascii=False, indent=2)
            out["workflow_file"] = args.output
            print(f"工作流已保存: {args.output}", file=sys.stderr)
        except IOError as e:
            error_exit(f"无法写入 {args.output}: {e}")

    if args.print_workflow:
        out["workflow"] = normalized

    if args.execute:
        if node_count == 0:
            error_exit("导出的工作流为空（请先在编导会话完成 Stage 3 分镜设计）")
        print("正在提交工作流执行...", file=sys.stderr)
        ecode, edata = http_request("POST", "/api/node-builder/execute",
                                    {"workflow": normalized}, timeout=120)
        if ecode not in (200, 201, 202) or not (isinstance(edata, dict) and edata.get("success")):
            error_exit(format_business_error(ecode, edata if isinstance(edata, dict) else {"message": str(edata)}))
        execution_id = edata.get("execution_id") or edata.get("exec_id", "")
        out["execution_id"] = execution_id
        out["execution_status"] = edata.get("status", "pending")
        if edata.get("points_consumed") is not None:
            out["points_consumed"] = edata["points_consumed"]

        if not args.no_wait and execution_id:
            final = poll_until_complete(execution_id, timeout=args.timeout, interval=args.interval)
            out["execution_status"] = final.get("status")
            if final.get("status") == "completed":
                result_urls = [u.get("url") for u in extract_result_urls(final)]
                out["result_urls"] = result_urls
                if args.output_dir:
                    dl = _download_execution_results(final, args.output_dir, args.prefix)
                    out["output_dir"] = args.output_dir
                    out["downloaded_files"] = dl["downloaded_files"]
                    if dl["errors"]:
                        out["download_errors"] = dl["errors"]
            elif final.get("status") == "failed":
                out["success"] = False
                out["error_message"] = final.get("error") or final.get("message", "执行失败")
            elif final.get("status") == "timeout":
                out["hint"] = final.get("message", "执行轮询超时，请稍后用 get_status.py 查询")

    json_output(out)
    if not out.get("success", True):
        sys.exit(1)


if __name__ == "__main__":
    main()
