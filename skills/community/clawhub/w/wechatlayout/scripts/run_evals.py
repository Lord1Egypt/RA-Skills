#!/usr/bin/env python3
"""回归测试：校验 evals/fixtures/ 下的黄金对照 HTML 产物。

每个 golden HTML 必须通过 validate_output.analyze() 的严重检查（errors=0），
否则视为回归失败。这是 validate_output.py 规则变更时的确定性兜底，
补上"改组件库/校验规则后无人回归验证"的洞。

用法:
    run_evals.py                # 检查全部 fixtures
    run_evals.py <name.html>    # 只检查指定文件

退出码: 0 = 全部通过, 1 = 存在失败
"""

import sys
from pathlib import Path

from validate_output import analyze


def main():
    fixtures_dir = Path(__file__).resolve().parent.parent / "evals" / "fixtures"
    if not fixtures_dir.is_dir():
        print(f"❌ 未找到 fixtures 目录: {fixtures_dir}")
        sys.exit(1)

    if len(sys.argv) > 1:
        targets = [Path(a) for a in sys.argv[1:]]
    else:
        targets = sorted(fixtures_dir.glob("*.html"))

    failures = 0
    for t in targets:
        if not t.is_file():
            print(f"❌ 找不到文件: {t}")
            failures += 1
            continue
        report = analyze(t.read_text(encoding="utf-8"))
        status = "✅ 通过" if not report["errors"] else "❌ 失败"
        rel = t.relative_to(fixtures_dir)
        print(f"{status} {rel}  (严重 {len(report['errors'])}, 提醒 {len(report['warnings'])})")
        for err in report["errors"]:
            print(f"    - {err}")
        if report["errors"]:
            failures += 1

    print(f"\n结果: {len(targets) - failures}/{len(targets)} 通过")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
