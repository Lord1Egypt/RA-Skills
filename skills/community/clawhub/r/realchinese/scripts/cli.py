#!/usr/bin/env python3
"""RealChinese CLI — 中文AI文本真人化引擎."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from detector import AIFingerprint
from rewriter import rewrite, deep_rewrite, list_platforms


def main():
    if len(sys.argv) < 2:
        print("RealChinese v1.1.2 — 中文AI文本真人化引擎")
        print()
        print("Commands:")
        print("  detect <text>              检测AI痕迹（29项特征）")
        print("  rewrite <text> <platform>  按平台风格改写（基础）")
        print("  deep-rewrite <text> <plat> 深层润色（复杂文本，结构重组+句式变化）")
        print("  platforms                  列出支持的平台")
        print()
        print("Examples:")
        print("  python cli.py detect '这是一个非常有效的方法...'")
        print("  python cli.py rewrite 'AI写的文字' 小红书")
        print("  python cli.py deep-rewrite '长文本...' 公众号")
        print("  echo '文本...' | python cli.py detect --stdin")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "detect":
        if len(sys.argv) > 2 and sys.argv[2] == "--stdin":
            text = sys.stdin.read()
        else:
            text = " ".join(sys.argv[2:])
        fp = AIFingerprint(text)
        print(fp.report())
        print(f"\n综合评分: {fp.score:.2f}")

    elif cmd == "rewrite":
        if len(sys.argv) < 4:
            print("Usage: python cli.py rewrite <text> <platform>")
            print(f"Platforms: {', '.join(list_platforms())}")
            print("For complex texts, try: python cli.py deep-rewrite <text> <platform>")
            sys.exit(1)
        text = sys.argv[2]
        platform = sys.argv[3]
        result = rewrite(text, platform)
        print(result)

    elif cmd == "deep-rewrite":
        if len(sys.argv) < 4:
            print("Usage: python cli.py deep-rewrite <text> <platform>")
            print(f"Platforms: {', '.join(list_platforms())}")
            sys.exit(1)
        text = sys.argv[2]
        platform = sys.argv[3]
        result = deep_rewrite(text, platform)
        print(result)

    elif cmd == "platforms":
        for p in list_platforms():
            from rewriter import PLATFORM_STYLES
            info = PLATFORM_STYLES[p]
            print(f"  {info['name']} ({p}) — {info['tone']}")

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
