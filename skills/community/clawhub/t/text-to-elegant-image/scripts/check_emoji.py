#!/usr/bin/env python3
"""检查 HTML 中是否含 emoji（无头环境会渲染成黑方块）。
用法: python3 check_emoji.py <html文件路径>
退出码: 0=通过 1=发现emoji 2=参数/文件错误"""
import re
import sys


EMOJI_PATTERN = re.compile(
    r'[\U0001F300-\U0001FAFF]'   # 表情/符号/扩展块
    r'|[\U00002600-\U000027BF]'  # 杂项符号 + 装饰符号
    r'|[\U0001F000-\U0001F2FF]'  # 麻将/骨牌/封闭字符
    r'|[\u2B00-\u2BFF]'          # 杂项符号与箭头（⬆⭐等）
    r'|[\uFE0F]'                 # 变体选择符
    r'|[\u2049\u203C]'           # ‼⁉
)


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: python3 check_emoji.py <html文件路径>")
        return 2
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        print(f"无法读取文件: {e}")
        return 2

    found = EMOJI_PATTERN.findall(content)
    if found:
        uniq = sorted(set(found))
        print(f"FAIL 发现 {len(found)} 处 emoji（{len(uniq)} 种），必须替换后再截图：")
        for ch in uniq:
            # 定位首次出现的行号方便修改
            for i, line in enumerate(content.splitlines(), 1):
                if ch in line:
                    print(f"  U+{ord(ch):04X} {ch!r}  首现于第 {i} 行")
                    break
        return 1
    print("PASS 无 emoji，可以截图")
    return 0


if __name__ == "__main__":
    sys.exit(main())
