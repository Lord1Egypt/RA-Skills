#!/usr/bin/env python3
"""Resolve Chinese OA choices read-only; save only with explicit consent."""
import argparse
import json
import os
from oa_utils import load_credentials, resolve_base_url
from personal_settings import DEFAULT_SETTINGS, save_settings
from oa_options import discover_options, resolve_selection
DEFAULT_CREDS = os.path.expanduser('~/.openclaw/workspace/memory/sn-work-record-credentials.md')


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--credentials', default=DEFAULT_CREDS)
    parser.add_argument('--base-url')
    parser.add_argument('--settings', default=str(DEFAULT_SETTINGS))
    parser.add_argument('--confirm-save', action='store_true')
    parser.add_argument('--project', required=True, help='精确项目名称或代码')
    parser.add_argument('--man-hour', required=True, type=float)
    for field in ('fill_type', 'project_phase', 'work_type'):
        parser.add_argument('--' + field.replace('_', '-'), required=True, help='精确中文标签或代码')
    args = parser.parse_args()
    try:
        # Validate explicit hours before authentication; no default hours.
        import math
        if not math.isfinite(args.man_hour) or args.man_hour <= 0:
            raise ValueError('时长必须为有限正数')
        from oa_utils import OAAuth
        account, password, host = load_credentials(args.credentials)
        host = resolve_base_url(host, args.base_url)
        auth = OAAuth(host, account, password)
        catalog = auth.call(lambda session: discover_options(session, host))
        values = resolve_selection(catalog, {field: getattr(args, field) for field in ('project', 'man_hour', 'fill_type', 'project_phase', 'work_type')})
        if args.confirm_save:
            save_settings(args.settings, account, host, values, confirmed=True)
    except (ValueError, OSError):
        parser.error('无法解析或保存设置；检查已确认选项、凭据和文件权限')
    except Exception:
        parser.exit(1, '只读选项查询失败；未保存、未提交。\n')
    print(json.dumps(values, ensure_ascii=False, indent=2))
    print('个人设置已保存（0600）；未提交工时。' if args.confirm_save else '仅本次预览；未保存、未提交工时。')


if __name__ == '__main__':
    from runtime_bootstrap import ensure_runtime
    ensure_runtime(['requests', 'ddddocr', 'PIL'])
    main()
