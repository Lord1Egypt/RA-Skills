#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""vkey-bid-standardizer 统一 CLI

Usage:
    standardize.py all <input.docx> [-o out] [--profile standard] [--dry-run] [--backup] [-v]
    standardize.py fix <input.docx> [-o out] [--profile standard]
    standardize.py renumber <input.docx> [-o out] [--profile standard]
    standardize.py auto-number <input.docx> [-o out] [--profile standard]
    standardize.py review <input.docx>
    standardize.py convert-md <input.md> [-o out] [--profile standard]
    standardize.py validate-patterns [--profile standard]
"""
import argparse
import json
import os
import sys

import sys
import os

# 把脚本所在目录加入 sys.path，使兄弟目录 vkey_bid_standardizer/ 可被 import
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from vkey_bid_standardizer import load_profile
from vkey_bid_standardizer.pipeline import (
    run_full,
    run_step_renumber,
    run_step_fix,
    run_step_auto_number,
    review,
    convert_md,
)
from vkey_bid_standardizer.patterns import load_patterns, match_pattern, resolve_number


PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--profile', default='standard',
                        help='profile 名（默认 standard；bid 是别名）')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--dry-run', action='store_true', help='只输出计划，不写文件')
    parser.add_argument('--backup', action='store_true', help='先把 input 备份到 input.bak')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细日志')


def cmd_all(args, profile):
    result = run_full(
        args.input, args.output, profile,
        dry_run=args.dry_run, backup=args.backup,
    )
    print('pipeline 步骤: ' + ' | '.join(result.steps))
    print('重编号: %d 处' % result.renumbered)
    print('修复样式: %d 处' % result.fixed)
    print('自动编号: %d 个样式绑定' % result.auto_numbered)
    if result.warnings:
        print('警告 (%d):' % len(result.warnings))
        for w in result.warnings[:20]:
            print('  ' + w)
    print('输出: ' + result.output)


def cmd_fix(args, profile):
    result = run_step_fix(args.input, args.output, profile)
    print('修复样式: %d 处' % result.fixed)
    print('输出: ' + result.output)


def cmd_renumber(args, profile):
    result = run_step_renumber(args.input, args.output, profile)
    print('重编号: %d 处' % result.renumbered)
    if result.warnings:
        print('警告 (%d):' % len(result.warnings))
        for w in result.warnings[:20]:
            print('  ' + w)
    print('输出: ' + result.output)


def cmd_auto_number(args, profile):
    result = run_step_auto_number(args.input, args.output, profile)
    print('自动编号: %d 个样式绑定' % result.auto_numbered)
    print('输出: ' + result.output)


def cmd_review(args, profile):
    report = review(args.input, profile)
    print(json.dumps(report, ensure_ascii=False, indent=2))


def cmd_convert_md(args, profile):
    result = convert_md(args.input, args.output, profile)
    print('生成: ' + result.output)


def cmd_validate_patterns(args, profile):
    patterns = load_patterns(profile)
    issues = []
    total_rules = 0

    for level in ('h1', 'h2', 'h3', 'h4', 'h5'):
        rules = patterns.get(level, [])
        total_rules += len(rules)
        for rule in rules:
            sample_ok = {
                'h1': '一、概述',
                'h2': '（一）适用范围',
                'h3': '1. 整体架构',
                'h4': '1.1.1.1 详细',
                'h5': '1.1.1.1.1 极详细',
            }.get(level, '')
            rule_obj, m, title = match_pattern([rule], sample_ok)
            if rule_obj is None:
                continue
            num = resolve_number(rule_obj, m)
            if num <= 0 and not rule.get('name', '').startswith('wps'):
                issues.append(f'[{level}] 规则 {rule["name"]} 样本 "{sample_ok}" 解析为 0')

    print(f'校验模式: {total_rules} 条规则')
    if issues:
        print('发现问题 (%d):' % len(issues))
        for i in issues:
            print('  ' + i)
    else:
        print('所有规则样本测试通过 [OK]')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='standardize',
        description='vkey-bid-standardizer 统一 CLI（首次发布 v1.0）',
    )
    sub = parser.add_subparsers(dest='cmd', required=True)

    common = argparse.ArgumentParser(add_help=False)
    _add_common_args(common)

    p_all = sub.add_parser('all', parents=[common], help='全流水线：renumber → fix → auto-number')
    p_all.add_argument('input')

    p_fix = sub.add_parser('fix', parents=[common], help='仅修复样式')
    p_fix.add_argument('input')

    p_ren = sub.add_parser('renumber', parents=[common], help='仅重编号')
    p_ren.add_argument('input')

    p_an = sub.add_parser('auto-number', parents=[common], help='仅自动编号')
    p_an.add_argument('input')

    p_rev = sub.add_parser('review', parents=[common], help='只读审计（JSON 输出）')
    p_rev.add_argument('input')

    p_md = sub.add_parser('convert-md', parents=[common], help='Markdown → docx')
    p_md.add_argument('input')

    p_vp = sub.add_parser('validate-patterns', parents=[common], help='校验编号模式注册表')
    return parser


COMMANDS = {
    'all': cmd_all,
    'fix': cmd_fix,
    'renumber': cmd_renumber,
    'auto-number': cmd_auto_number,
    'review': cmd_review,
    'convert-md': cmd_convert_md,
    'validate-patterns': cmd_validate_patterns,
}


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        profile = load_profile(args.profile)
    except FileNotFoundError as e:
        print('ERROR: ' + str(e), file=sys.stderr)
        return 2
    handler = COMMANDS[args.cmd]
    handler(args, profile)
    return 0


if __name__ == '__main__':
    sys.exit(main())
