#!/usr/bin/env python3
"""提交蜀宁 OA 工时记录，支持直接提交或保存草稿"""
import argparse
import json
import os
import sys

from runtime_bootstrap import ensure_runtime

ensure_runtime(["requests", "ddddocr", "PIL", "chinese_calendar"])

from oa_utils import (
    build_session,
    is_workday,
    load_credentials,
    login,
    resolve_base_url,
    submit_time_entry,
)

DEFAULT_CREDS = os.path.expanduser("~/.openclaw/workspace/memory/sn-work-record-credentials.md")


def main():
    parser = argparse.ArgumentParser(description="提交蜀宁 OA 工时记录")
    parser.add_argument("fill_date", nargs="?", help="填写日期，格式 YYYY-MM-DD")
    parser.add_argument("--fill-date", dest="fill_date_flag", help="填写日期，格式 YYYY-MM-DD")
    parser.add_argument("--job-desc", required=True, help="工时描述")
    parser.add_argument("--man-hour", type=float, default=8, help="工时时长，默认 8")
    parser.add_argument("--project-id", help="项目 ID；不传则尝试使用凭据中的默认项目ID")
    parser.add_argument("--project-name", help="项目名称；不传则尝试使用凭据中的默认项目名称")
    parser.add_argument("--project-phase", default="1", help="项目阶段，默认 1")
    parser.add_argument("--work-type", default="5", help="工作类型，默认 5")
    parser.add_argument("--bo-to-pm-status", type=int, default=1, help="默认 1")
    parser.add_argument("--fill-type", default="1", help="填报类型，默认 1")
    parser.add_argument("--save-draft", action="store_true", help="仅保存草稿，不直接提交")
    parser.add_argument("--credentials", default=DEFAULT_CREDS)
    parser.add_argument("--base-url", dest="base_url", default=None)
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    fill_date = args.fill_date_flag or args.fill_date
    if not fill_date:
        parser.error("请提供填写日期，例如：2026-04-11")

    try:
        username, password, base_url, default_project_id, default_project_name = load_credentials(
            args.credentials, require_project=True
        )
        base_url = resolve_base_url(base_url, args.base_url)
        project_id = args.project_id or default_project_id
        project_name = args.project_name or default_project_name
        if not project_id or not project_name:
            raise ValueError("请提供 --project-id/--project-name，或先在凭据文件中设置默认项目")
        if not args.save_draft and not is_workday(fill_date):
            raise ValueError("节假日期间无需填写工时~")

        print("正在登录 OA 系统...", file=sys.stderr)
        token = login(username, password, base_url)
        session = build_session(token)
        print(f"正在提交 {fill_date} 的工时...", file=sys.stderr)
        result = submit_time_entry(
            session,
            base_url,
            fill_date=fill_date,
            project_id=project_id,
            project_name=project_name,
            job_desc=args.job_desc,
            man_hour=args.man_hour,
            save_or_submit=0 if args.save_draft else 1,
            project_phase=args.project_phase,
            work_type=args.work_type,
            bo_to_pm_status=args.bo_to_pm_status,
            fill_type=args.fill_type,
        )
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return

        action_text = "草稿已保存" if args.save_draft else "工时提交成功"
        state_text = "草稿" if args.save_draft else "审批中"
        print(f"{fill_date} {action_text}！\n")
        print(f"项目：{project_name}")
        print(f"项目ID：{project_id}")
        print(f"时长：{args.man_hour}h")
        print(f"描述：{args.job_desc}")
        print(f"状态：{state_text}")
    except FileNotFoundError as e:
        print(f"文件未找到: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"凭据错误: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知异常: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
