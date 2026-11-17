#!/usr/bin/env python3
"""Resolve live Chinese OA choices, then preview or submit ordinary work."""
import argparse
import json
import os
import sys
import math
import re
from datetime import date
from pathlib import Path

from runtime_bootstrap import ensure_runtime
ensure_runtime(['requests', 'ddddocr', 'PIL', 'chinese_calendar'])

from oa_utils import OAAuth, is_workday, load_credentials, resolve_base_url, submit_time_entry
from oa_options import discover_options, resolve_selection
from personal_settings import DEFAULT_SETTINGS, resolve_settings
from submission_guard import SubmissionUncertain

DEFAULT_CREDS = os.path.expanduser('~/.openclaw/workspace/memory/sn-work-record-credentials.md')


def prepare_choices(args, account, host):
    """Read only confirmed account-bound defaults; overrides never persist."""
    path = Path(args.settings).expanduser()
    if path.is_symlink():
        raise ValueError('个人设置不得为符号链接')
    defaults = resolve_settings(path, account, host, {}) if path.exists() else {}
    choices = {field: getattr(args, field) if getattr(args, field) is not None else defaults.get(field)
               for field in ('fill_type', 'project_phase', 'work_type', 'man_hour')}
    selectors = [value for value in (args.project, args.project_id) if value is not None]
    if len(selectors) > 1:
        raise ValueError('项目选择只能提供 --project 或 --project-id 之一')
    choices['project'] = selectors[0] if selectors else defaults.get('project_id')
    missing = [field for field, value in choices.items() if value is None]
    if missing:
        raise ValueError('缺少已确认选择: ' + ', '.join(missing))
    hours = choices['man_hour']
    if isinstance(hours, bool) or not isinstance(hours, (int, float)) or not math.isfinite(hours) or hours <= 0:
        raise ValueError('时长必须为有限正数')
    return choices


def preview_summary(catalog, values, fill_date, job_desc, *, draft=False, include_codes=False):
    result: dict = dict(preview_only=True, fill_date=fill_date, project_name=values['project_name'],
                  man_hour=values['man_hour'], job_desc=job_desc,
                  action='草稿（仅预览）' if draft else '提交（仅预览）')
    for field in ('fill_type', 'project_phase', 'work_type'):
        result[field] = next(item['label'] for item in catalog[field]['options'] if item['value'] == values[field])
    if include_codes:
        result['codes'] = {key: values[key] for key in ('project_id', 'fill_type', 'project_phase', 'work_type', 'bo_to_pm_status')}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('fill_date', nargs='?', help='填写日期 YYYY-MM-DD')
    parser.add_argument('--fill-date', dest='fill_date_flag')
    parser.add_argument('--job-desc', required=True)
    parser.add_argument('--man-hour', type=float, help='已确认时长；无默认 8h')
    parser.add_argument('--project', help='精确项目中文名称或代码')
    parser.add_argument('--project-id', help='兼容旧入口；仍需通过当前项目列表验证')
    parser.add_argument('--project-name', help='可选项目名称断言；不能覆盖当前项目名称')
    parser.add_argument('--bo-to-pm-status', help='可选项目属性断言（精确 0/1）；不作为默认或覆盖')
    for field in ('project_phase', 'work_type', 'fill_type'):
        parser.add_argument('--' + field.replace('_', '-'), help='精确中文标签或已验证代码')
    parser.add_argument('--save-draft', action='store_true')
    parser.add_argument('--preview', action='store_true', help='相同提交解析路径，只读预览；不保存设置或工时')
    parser.add_argument('--include-codes', action='store_true', help='显式在预览中显示内部代码')
    parser.add_argument('--credentials', default=DEFAULT_CREDS)
    parser.add_argument('--base-url')
    parser.add_argument('--token')
    parser.add_argument('--settings', default=str(DEFAULT_SETTINGS))
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    fill_date = args.fill_date_flag or args.fill_date
    if not fill_date:
        parser.error('请提供填写日期 YYYY-MM-DD')
    try:
        if args.fill_date_flag and args.fill_date and args.fill_date_flag != args.fill_date:
            raise ValueError('填写日期冲突')
        if not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', fill_date):
            raise ValueError('填写日期必须为 YYYY-MM-DD')
        date.fromisoformat(fill_date)
        if not args.job_desc.strip():
            raise ValueError('描述必须显式提供且非空')
        if args.bo_to_pm_status is not None and args.bo_to_pm_status not in ('0', '1'):
            raise ValueError('项目属性断言必须为精确代码 0 或 1')
        account, password, host = load_credentials(args.credentials, require_project=False)
        host = resolve_base_url(host, args.base_url)
        choices = prepare_choices(args, account, host)
        if not args.save_draft and not is_workday(fill_date):
            raise ValueError('节假日期间无需填写工时~')
        auth = OAAuth(host, account, password, args.token)
        catalog = auth.call(lambda session: discover_options(session, host))
        values = resolve_selection(catalog, choices)
        if args.project_name is not None and args.project_name != values['project_name']:
            raise ValueError('项目名称与当前选项不符')
        if args.bo_to_pm_status is not None and args.bo_to_pm_status != str(values['bo_to_pm_status']):
            raise ValueError('项目属性与当前选项不符；属性必须由项目派生')
        if values['fill_type'] != '1':
            raise ValueError('此入口仅支持普通工作；请假填报尚未实现，不能伪造项目提交')
        if args.preview:
            summary = preview_summary(catalog, values, fill_date, args.job_desc,
                                      draft=args.save_draft, include_codes=args.include_codes)
            if args.json:
                print(json.dumps(summary, ensure_ascii=False, indent=2))
            else:
                print('仅预览；未提交、未保存工时或个人设置。')
                for key, value in summary.items():
                    if key != 'preview_only':
                        print(f'{key}: {value}')
            return
        result = auth.call(lambda session: submit_time_entry(
            session, host, fill_date=fill_date, job_desc=args.job_desc,
            save_or_submit=0 if args.save_draft else 1, **values), allow_relogin=False)
        if not isinstance(result, dict) or result.get('verified') is not True or result.get('submission_status') not in ('skipped-existing','submitted-confirmed','observed-after-uncertain'):
            raise RuntimeError('工时结果未核实')
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            status = result['submission_status']
            message = {'skipped-existing':'已存在完全相同的已提交工时；未重复提交',
                       'submitted-confirmed':'工时提交成功（已只读核实）',
                       'observed-after-uncertain':'写入响应不确定；只读查询已确认匹配工时，未重发'}[status]
            print(f"{fill_date} {message}！")
            print(f"项目：{values['project_name']}\n时长：{values['man_hour']}h\n描述：{args.job_desc}")
    except SubmissionUncertain:
        parser.exit(1, '工时写入结果未知、冲突或存在历史未核实写入；禁止重发/覆盖，请只读核实。\n')
    except ValueError as exc:
        parser.exit(1, f'选择或输入错误: {exc}\n')
    except Exception:
        # Network/library exceptions can contain private host or credentials.
        parser.exit(1, 'OA 查询或提交失败；未自动重试写入。请核实服务端记录后再操作。\n')


if __name__ == '__main__':
    main()
