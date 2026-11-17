#!/usr/bin/env python3
"""小红书笔记发布前合规自查（零依赖，纯本地规则检测）。

检测三类高危内容：
  1. 绝对化用语（广告法红线）
  2. 医疗/功效断言（限流与违规高发）
  3. 站外引流特征（微信号变体等，限流封号最高危）

用法:
    python3 content_check.py <文本文件>
    echo "文案内容" | python3 content_check.py -

退出码: 0=通过 1=有警告 2=有高危项
"""
import re
import sys

ABSOLUTE = ["第一", "唯一", "最好", "最佳", "最强", "最先进", "顶级",
            "极品", "首选", "全网最低", "史上", "百分百", "100%有效",
            "全国领先", "国家级", "绝无仅有", "永久"]

MEDICAL = ["治疗", "治愈", "根治", "疗效", "祛疤", "祛痘印", "美白淡斑",
           "消炎", "杀菌", "抗癌", "降血压", "降血糖", "减肥神器",
           "瘦十斤", "三天见效", "七天见效", "无副作用", "药到病除"]

DIVERSION = [
    (r"[vV威薇微][信xX芯]|weixin|wechat", "疑似微信引流"),
    (r"[+＋加][vV微]|[vV]:：?\s*[a-zA-Z0-9_-]{5,}", "疑似留联系方式"),
    (r"[qQ扣][qQ扣]?\s*[:：]?\s*\d{6,}", "疑似QQ号"),
    (r"电话|手机号|1[3-9]\d{9}", "疑似电话号码"),
    (r"某宝|某鱼|某多|淘宝店|闲鱼|拼多多", "站外平台指引(软性违规)"),
    (r"私[信聊我]|滴滴我|dd我", "私信引导(适度可用,高频有风险)"),
]


def check(text: str):
    high, warn = [], []
    for w in ABSOLUTE:
        if w in text:
            high.append(f"绝对化用语: 「{w}」(广告法红线,改为具体数据或主观表述)")
    for w in MEDICAL:
        if w in text:
            high.append(f"医疗功效断言: 「{w}」(化妆品/食品类目严禁,改为使用感受)")
    for pat, label in DIVERSION:
        m = re.search(pat, text)
        if m:
            (high if "微信" in label or "联系" in label or "QQ" in label
             or "电话" in label else warn).append(f"{label}: 「{m.group(0)}」")
    if len(text) < 50:
        warn.append("正文过短(<50字),难以进入推荐池")
    exclam = text.count("！") + text.count("!")
    if exclam > 8:
        warn.append(f"感叹号过多({exclam}个),情绪堆砌无真实锚点易被判低质")
    return high, warn


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    src = sys.stdin if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8")
    text = src.read()
    high, warn = check(text)
    for h in high:
        print(f"❌ {h}")
    for w in warn:
        print(f"⚠️  {w}")
    if not high and not warn:
        print("✅ 未命中高危规则(规则库有限,平台判定仍以官方为准)")
    sys.exit(2 if high else (1 if warn else 0))


if __name__ == "__main__":
    main()
