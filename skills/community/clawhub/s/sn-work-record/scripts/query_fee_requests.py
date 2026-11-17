#!/usr/bin/env python3
"""查询蜀宁 OA 报销申请状态，可选展开当前审批进度。"""

import argparse
import json
import os
import sys

from runtime_bootstrap import ensure_runtime

ensure_runtime(["requests", "ddddocr", "PIL"])

from oa_utils import (
    OAAuth,
    fee_state_to_text,
    fee_type_to_text,
    get_workflow_process_detail,
    load_credentials,
    query_fee_requests,
    reimburse_company_to_text,
    resolve_base_url,
)

DEFAULT_CREDS = os.path.expanduser("~/.openclaw/workspace/memory/sn-work-record-credentials.md")
STATE_ALIASES = {
    "撤回": "-1",
    "已撤回": "-1",
    "作废": "0",
    "已作废": "0",
    "待提交": "10",
    "审批中": "20",
    "通过": "30",
    "已通过": "30",
    "驳回": "40",
    "已驳回": "40",
}


def normalize_state(value):
    if value is None:
        return None
    return STATE_ALIASES.get(value, value)


def current_approval(progress):
    """从流程历史中提取尚未完成的审批节点。"""
    nodes = progress.get("historyProcNodeList", []) or []
    pending = [
        node
        for node in nodes
        if node.get("activityType") == "userTask" and not node.get("endTime")
    ]
    return pending[0] if pending else None


def main():
    parser = argparse.ArgumentParser(description="查询蜀宁 OA 报销申请状态")
    parser.add_argument("--start-date", default="", help="申请开始日期，如 2026-09-01")
    parser.add_argument("--end-date", default="", help="申请结束日期，如 2026-09-30")
    parser.add_argument("--state", help="客户端筛选状态码或中文状态，如 20/审批中")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--size", type=int, default=20)
    parser.add_argument("--with-progress", action="store_true", help="同时查询审批中申请的当前节点和审批人")
    parser.add_argument("--credentials", default=DEFAULT_CREDS)
    parser.add_argument("--base-url", dest="base_url", default=None)
    parser.add_argument("--token", default=None, help="复用已有 OA token，跳过登录（配合 sn_oa_login.py 的 agent 识别流程）")
    parser.add_argument("--json", action="store_true", help="输出接口原始 JSON；配合 --with-progress 时附带流程数据")
    args = parser.parse_args()

    if args.page < 1 or args.size < 1:
        parser.error("--page 和 --size 必须大于 0")

    try:
        username, password, base_url = load_credentials(args.credentials)
        base_url = resolve_base_url(base_url, args.base_url)

        auth = OAAuth(base_url, username, password, args.token)

        print("正在查询报销申请...", file=sys.stderr)
        items, page_data, result = auth.call(
            lambda s: query_fee_requests(
                s,
                base_url,
                page=args.page,
                size=args.size,
                start_time=args.start_date,
                end_time=args.end_date,
            )
        )

        state_filter = normalize_state(args.state)
        if state_filter is not None:
            items = [item for item in items if str(item.get("state")) == state_filter]

        progress_by_id = {}
        if args.with_progress:
            for item in items:
                proc_ins_id = item.get("procInsId")
                if not proc_ins_id:
                    continue
                try:
                    progress, _ = auth.call(
                        lambda s: get_workflow_process_detail(s, base_url, proc_ins_id)
                    )
                    progress_by_id[str(item.get("id", proc_ins_id))] = progress
                except Exception as exc:
                    progress_by_id[str(item.get("id", proc_ins_id))] = {"_error": str(exc)}

        if args.json:
            output = result
            if state_filter is not None or args.with_progress:
                output = dict(result)
                output["data"] = dict(page_data)
                output["data"]["content"] = items
                if args.with_progress:
                    output["workflowProgress"] = progress_by_id
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return

        if not items:
            print("没有符合条件的报销申请")
            return

        total = page_data.get("totalElements")
        shown = len(items)
        if state_filter is None and total is not None:
            print(f"报销申请共 {total} 条，本页显示 {shown} 条：\n")
        else:
            print(f"符合条件的报销申请 {shown} 条：\n")

        for i, item in enumerate(items, 1):
            state = str(item.get("state", ""))
            print(f"{i}. {item.get('createdTime', '')} · {fee_state_to_text(state)}")
            print(f"   项目：{item.get('projectName') or '未关联项目'}")
            print(f"   类型：{fee_type_to_text(item.get('feeType'))}")
            print(f"   金额：¥{item.get('sumAmount', '')}")
            print(f"   公司：{reimburse_company_to_text(item.get('reimburseCompany'))}")
            print(f"   更新时间：{item.get('updatedTime', '')}")
            if item.get("rejectReason"):
                print(f"   驳回原因：{item.get('rejectReason')}")

            progress = progress_by_id.get(str(item.get("id", item.get("procInsId", ""))))
            if progress:
                if progress.get("_error"):
                    print(f"   审批进度：查询失败（{progress['_error']}）")
                else:
                    node = current_approval(progress)
                    if node:
                        print(f"   当前节点：{node.get('activityName') or '审批中'}")
                        print(f"   当前审批人：{node.get('assigneeName') or '未分配'}")
                    else:
                        process_status = (progress.get("taskVariables") or {}).get("processStatus")
                        print(f"   流程状态：{process_status or '已结束/无待办节点'}")
            if i != len(items):
                print()

    except FileNotFoundError as exc:
        print(f"文件未找到: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"凭据错误: {exc}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"未知异常: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
