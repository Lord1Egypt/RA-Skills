#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一条命令跑全部 research 判据 —— research-first skill 入口

用法: python run_all.py <纪要.md>

依次跑：
  1. check_journal.py    —— 结论站不站得住（S1–S5）
  2. check_expansion.py  —— 方向有没有漏（D1–D9）

退出码: 0 = 两个都过 / 1 = 有红项 / 2 = 至少一个解析失败
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script, journal):
    p = subprocess.run([sys.executable, os.path.join(HERE, script), journal],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def main(journal):
    if not os.path.isfile(journal):
        print(f'⛔ 找不到纪要文件: {journal}')
        sys.exit(2)
    codes = {}
    print('═' * 66)
    print('① 结论判据 check_journal（S1–S5）')
    print('═' * 66)
    rc, out = run('check_journal.py', journal)
    codes['journal'] = (rc, out)
    print(out)
    print('═' * 66)
    print('② 联想判据 check_expansion（D1–D9）')
    print('═' * 66)
    codes['expansion'] = run('check_expansion.py', journal)
    print(codes['expansion'][1])

    print('═' * 66)
    j, e = codes['journal'][0], codes['expansion'][0]
    verdict = ('✅ 两关都过' if j == 0 and e == 0 else
               '❌ 有红项 —— 不许据此宣称 research 完成')
    print(f'汇总：check_journal={j}  check_expansion={e}  ⇒  {verdict}')
    if 2 in (j, e):
        print('⛔ 至少一个判据解析失败（空过防护）—— 格式先对，结论先别下')
    sys.exit(0 if (j == 0 and e == 0) else 1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('用法: python run_all.py <纪要.md>')
        sys.exit(2)
    main(sys.argv[1])
