#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""合规敏感词扫描器（交付前闸门）

用途：对生成的 HTML 报告做敏感词扫描，确保符合"公开信息整理+可视化+观赛辅助"定位，
不出现任何赛果判断/预测/投注/赔率/盘口类用语。

关键设计：区分「违规用语」与「打假语境」。
诸如"稳赚""必中"这类词，若出现在防骗盾的否定/揭穿句中（如"警惕稳赚话术"），
属于合规的反诈内容，不应误判为违规。故对每次命中都抽取上下文并判定语境。

用法：
    python compliance_scan.py <file1.html> [file2.html ...]
退出码：0 = 通过；1 = 存在真实违规命中
"""
import io
import re
import sys

# 硬违规：任何语境下都不应出现
HARD_BAN = [
    '投注', '下注', '赔率', '盘口', '让球', '亚盘', '欧指', '水位',
    '独赢', '波胆', '大球', '小球', '竞彩', '博彩', '彩票',
    '推荐比分', '预测比分', '胜负彩', '串关',
]

# 软违规：仅在「打假/否定语境」中允许（防骗盾会主动揭穿这些话术）
SOFT_BAN = ['稳赚', '包中', '必中', '必胜', '确定性赛果', '绝对正确']

# 判定为打假语境的标志词（出现在命中词附近即视为反诈内容）
DEBUNK_MARKERS = [
    '警惕', '诈骗', '骗', '假', '不保证', '不承诺', '不提供', '识别',
    '话术', '谎', '陷阱', '风险', '拒绝', '揭穿', '打假', '均为', '都是',
    '任何', '声称', '所谓',
]

TAG_RE = re.compile(r'<[^>]+>')


def strip_tags(html: str) -> str:
    """去掉标签，保留纯文本，便于语境判断。"""
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html,
                  flags=re.S | re.I)
    return TAG_RE.sub(' ', text)


def find_contexts(text: str, word: str, radius: int = 60):
    """返回该词每次出现的上下文片段。"""
    out = []
    start = 0
    while True:
        i = text.find(word, start)
        if i < 0:
            break
        seg = text[max(0, i - radius): i + len(word) + radius]
        out.append(re.sub(r'\s+', ' ', seg).strip())
        start = i + len(word)
    return out


def is_debunk(ctx: str) -> bool:
    return any(m in ctx for m in DEBUNK_MARKERS)


def scan(path: str):
    html = io.open(path, encoding='utf-8').read()
    text = strip_tags(html)

    violations = []   # 真实违规
    debunked = []     # 打假语境（合规）

    for word in HARD_BAN:
        for ctx in find_contexts(text, word):
            violations.append((word, ctx, 'HARD'))

    for word in SOFT_BAN:
        for ctx in find_contexts(text, word):
            if is_debunk(ctx):
                debunked.append((word, ctx))
            else:
                violations.append((word, ctx, 'SOFT'))

    return violations, debunked


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2

    total_bad = 0
    for path in argv[1:]:
        try:
            violations, debunked = scan(path)
        except OSError as exc:
            print('[跳过] %s → %s' % (path, exc))
            continue

        name = path.replace('\\', '/').rsplit('/', 1)[-1]
        status = '通过 ✅' if not violations else '存在违规 ❌'
        print('[%s] %s' % (name, status))
        print('    硬违规词库=%d 项 / 软违规词库=%d 项' %
              (len(HARD_BAN), len(SOFT_BAN)))

        if debunked:
            print('    打假语境命中 %d 处（合规，属反诈内容）：' % len(debunked))
            for word, ctx in debunked:
                print('      · "%s" → …%s…' % (word, ctx))

        if violations:
            total_bad += len(violations)
            print('    ⚠️ 真实违规 %d 处：' % len(violations))
            for word, ctx, kind in violations:
                print('      · [%s] "%s" → …%s…' % (kind, word, ctx))
        print()

    print('=== 汇总 ===  文件=%d  真实违规=%d' % (len(argv) - 1, total_bad))
    print('结论：%s' % ('通过 ✅' if total_bad == 0 else '不通过 ❌'))
    return 0 if total_bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
