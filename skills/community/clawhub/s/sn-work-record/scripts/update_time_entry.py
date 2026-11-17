#!/usr/bin/env python3
"""修改蜀宁 OA 工时记录，支持按 ID 更新描述；删除/恢复暂禁"""

import argparse
import json
import os
import sys

from runtime_bootstrap import ensure_runtime

ensure_runtime(["requests", "ddddocr", "PIL"])

from amendment_guard import amend_time_entry
from submission_guard import SubmissionUncertain
from oa_utils import OAAuth, get_time_entry_details, load_credentials, resolve_base_url, state_to_text, update_time_entry

DEFAULT_CREDS = os.path.expanduser("~/.openclaw/workspace/memory/sn-work-record-credentials.md")


def main():
    parser = argparse.ArgumentParser(description="修改蜀宁 OA 工时记录")
    parser.add_argument("entry_id", help="工时 ID")
    parser.add_argument("--job-desc", help="新的工时描述")
    parser.add_argument("--delete", action="store_true", help="暂禁：无可靠恢复契约")
    parser.add_argument("--restore-deleted", action="store_true", help="暂禁：无可靠恢复契约")
    parser.add_argument("--confirm-entry-id", help="显式确认删除/恢复目标 ID（必须与位置参数一致）")
    parser.add_argument("--preview", action="store_true", help="只读预览已有审批中普通工时的撤回重提；不写入")
    parser.add_argument("--withdraw-resubmit", action="store_true", help="明确授权撤回已有审批中普通工时并以原 ID 修改描述后重新提交")
    parser.add_argument("--credentials", default=DEFAULT_CREDS)
    parser.add_argument("--base-url", dest="base_url", default=None)
    parser.add_argument("--token", default=None, help="复用已有 OA token，跳过登录（配合 sn_oa_login.py 的 agent 识别流程）")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    amendment_mode = args.preview or args.withdraw_resubmit
    deletion_mode = args.delete or args.restore_deleted
    if deletion_mode:
        parser.error('删除/恢复暂禁：服务端无可靠恢复契约；不会读取凭据或连接 OA')
    if deletion_mode and (args.delete == args.restore_deleted or amendment_mode or args.job_desc is not None or args.confirm_entry_id != args.entry_id):
        parser.error('删除/恢复须单独操作，并通过 --confirm-entry-id 显式确认同一目标 ID')
    if amendment_mode and args.delete:
        parser.error("--delete 不得与 --preview/--withdraw-resubmit 合用")
    if amendment_mode and (not isinstance(args.job_desc, str) or not args.job_desc.strip()):
        parser.error("预览或撤回重提必须提供非空 --job-desc")
    if args.job_desc is None and not deletion_mode:
        parser.error("请至少提供 --job-desc 或 --delete 之一")

    try:
        username, password, base_url = load_credentials(args.credentials)
        base_url = resolve_base_url(base_url, args.base_url)

        auth = OAAuth(base_url, username, password, args.token)

        if amendment_mode:
            result = auth.call(
                lambda s: amend_time_entry(s, base_url, args.entry_id, args.job_desc,
                                          preview=args.preview, withdraw_resubmit=args.withdraw_resubmit),
                allow_relogin=False,
            )
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return
            status = result.get('amendment_status')
            messages = {
                'preview':'只读预览：将撤回原记录并以同一 ID 修改描述后重新提交；尚未写入',
                'skipped-existing':'已有完全相同的审批中工时，未撤回或重提',
                'amended-confirmed':'工时描述已更新并重新提交，已核实原 ID 与业务字段',
                'observed-after-uncertain':'写响应不确定，已只读核实原记录的新描述与审批中状态；未重发',
            }
            print(messages.get(status, '修改结果未知，禁止重发，请只读核实'))
            detail = result.get('detail', {})
            print(f"日期：{detail.get('fillDate', '')}")
            print(f"描述：{detail.get('jobDesc', '')}")
            print(f"状态：{state_to_text(detail.get('state'))}")
            return

        print(f"正在修改工时 {args.entry_id} ...", file=sys.stderr)
        result = auth.call(
            lambda s: update_time_entry(
                s,
                base_url,
                args.entry_id,
                job_desc=args.job_desc,
                is_deleted=(1 if args.delete else 0) if deletion_mode else None,
                **({'confirm_entry_id': args.confirm_entry_id} if deletion_mode else {}),
            ),
            allow_relogin=False,
        )
        if deletion_mode:
            if result.get('verified') is not True:
                raise SubmissionUncertain('删除/恢复未核实；禁止重发，请只读核实')
            print(json.dumps(result, ensure_ascii=False) if args.json else '删除/恢复已读回核实；保留原始备份与全部提交保护记录')
            return
        detail, _ = auth.call(lambda s: get_time_entry_details(s, base_url, args.entry_id))

        if args.json:
            print(json.dumps({"update": result, "detail": detail}, ensure_ascii=False, indent=2))
            return

        state = str(detail.get("state", ""))
        print(f"工时修改成功：{args.entry_id}\n")
        print(f"日期：{detail.get('fillDate', '')}")
        print(f"项目：{detail.get('projectName', '')}")
        print(f"时长：{detail.get('manHour', '')}h")
        print(f"描述：{detail.get('jobDesc', '')}")
        print(f"状态：{state_to_text(state)} ({state})")
        print(f"是否删除：{detail.get('isDeleted', '')}")
        print(f"更新时间：{detail.get('updatedTime', '')}")

    except Exception as e:
        if deletion_mode:
            print(str(e) if isinstance(e, SubmissionUncertain) else '删除/恢复未完成，结果未知；保留备份和保护日志，禁止重发，请只读核实', file=sys.stderr)
        elif amendment_mode:
            # Only our guarded phase diagnostics are safe to expose. Requests,
            # auth and credential exceptions may include origin or token data.
            message = str(e) if isinstance(e, SubmissionUncertain) else '修改/预览未完成；撤回/重新提交状态未知，未自动重发，请先只读核实'
            print(message, file=sys.stderr)
        elif isinstance(e, FileNotFoundError):
            print(f"文件未找到: {e}", file=sys.stderr)
        elif isinstance(e, ValueError):
            print(f"凭据错误: {e}", file=sys.stderr)
        elif isinstance(e, RuntimeError):
            print(f"{e}", file=sys.stderr)
        else:
            print(f"未知异常: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
