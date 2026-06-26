# -*- coding: utf-8 -*-
"""
小说质量检查工具 - 违禁词+高频词+替代表达扫描
用法: python freq_check.py <文件路径>
"""
import re
import sys
import os

# ============================================================
# 第一类：违禁词（出现即违规，必须修改）
# ============================================================
METAPHOR = ['像', '如同', '仿佛', '好像', '如']
XLE_X = ['顿了顿', '掂了掂', '紧了紧', '攥了攥', '偏了偏', '收了收', '摇了摇', '抖了抖',
         '动了动', '摸了摸', '闻了闻', '沉了沉', '白了白', '红了红',
         '没出声', '翻了翻', '瞥了瞥', '盯了盯', '白了白', '咬了咬']
DISABLE_ADV = ['猛然', '陡然', '骤然', '缓缓', '却', '但', '于是', '然后']
DISABLE_PAT = ['冷笑一声', '一阵剧痛', '涌来', '腥气', '腥甜', '绷得发白', '哆嗦了半天',
               '没人说话', '没人吭声', '盯着帐顶发呆', '可他不去找她她就不会来找他',
               'preY', 'prey', 'Prey', '指节', '指尖', '眼眶通红', '绷得发白',
               '整整', '脸上没有任何表情']
废话 = ['他知道', '她知道', '它知道', '我知道', '我觉得', '她觉得', '它觉得']
哑词 = ['哑得', '哑得厉害', '嗓子哑', '声音哑']
HIGH_WORDS = ['眼神', '眼睛', '目光', '心脏', '心里']

ALL_FORBIDDEN = (METAPHOR + DISABLE_ADV + DISABLE_PAT + 废话 + 哑词)

# ============================================================
# 第二类：替代表达库（模板词 -> 画面/动作替代，不近义词替换）
# ============================================================
REPLACE_MAP = {
    # 抽象心理 -> 具体动作/身体反应
    '心里一沉': '胃拧了一下',
    '心脏猛地一缩': '胸口发紧',
    '心脏狠狠一跳': '呼吸一滞',
    '眼神冷了下来': '他把脸别开了',
    '眼神里有一瞬间的茫然': '她歪了歪头，在辨认他',
    '目光没有温度': '他的目光没有焦点',

    # 重复动作描写 -> 场景替换
    '扫了一眼': '目光落在',
    '扫了': None,
    '扫了他一眼': '他瞥了对方一眼',

    # 身体部位 -> 动作替代
    '指节泛白': '手指发僵',
    '攥紧了任务单': '他捏着任务单',
    '攥紧了手里的': '他捏着',

    # 高频心理 -> 画面替代
    '脸色复杂': '他没说话',
    '眼神里闪过': '他的眼睛动了动',
}

def check_file(target):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'freq_result.txt')

    with open(target, 'r', encoding='utf-8') as f:
        text = f.read()
    lines = text.split('\n')

    # ---- 高频词 ----
    words = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    # ---- 违禁词扫描 ----
    forbidden_results = []
    for i, line in enumerate(lines, 1):
        issues = []
        # 违禁词检查
        for kw in ALL_FORBIDDEN:
            if kw in line:
                idx = line.index(kw)
                start = max(0, idx - 10)
                end = min(len(line), idx + len(kw) + 10)
                snippet = line[start:end]
                issues.append(f'[{kw}] ...{snippet}...')
        # X了X格式
        for kw in XLE_X:
            if kw in line:
                idx = line.index(kw)
                start = max(0, idx - 10)
                end = min(len(line), idx + len(kw) + 10)
                snippet = line[start:end]
                issues.append(f'[X了X:{kw}] ...{snippet}...')
        # 替代表达
        for kw, rep in REPLACE_MAP.items():
            if kw in line:
                idx = line.index(kw)
                start = max(0, idx - 10)
                end = min(len(line), idx + len(kw) + 10)
                snippet = line[start:end]
                note = f'建议替: {rep}' if rep else '建议删除'
                issues.append(f'[替:{kw}] ...{snippet}... | {note}')
        # 高频词警告（眼神/眼睛/目光/心脏+心理词组合）
        for hw in HIGH_WORDS:
            if hw in line and any(k in line for k in ['里了', '里透', '里闪', '里浮']):
                idx = line.index(hw)
                start = max(0, idx - 5)
                end = min(len(line), idx + 20)
                snippet = line[start:end]
                issues.append(f'[高频组合:{hw}...] ...{snippet}...')

        if issues:
            for issue in issues:
                forbidden_results.append(f'  L{i}: {issue}')

    # ---- 高频词汇总（次数>=2）----
    high_freq = [(w, c) for w, c in freq.items() if c >= 2]
    high_freq.sort(key=lambda x: -x[1])

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('=== 高频词（出现次数>=2）===\n')
        if high_freq:
            for w, c in high_freq:
                f.write(f'  {w}: {c}\n')
        else:
            f.write('  无\n')

        f.write('\n=== 违禁词+替代表达扫描 ===\n')
        if forbidden_results:
            f.write('发现问题：\n')
            for r in forbidden_results:
                f.write(r + '\n')
        else:
            f.write('  无违禁词 ✅\n')

    print(f'Done. 结果已写入: {output_path}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python freq_check.py <文件路径>")
        sys.exit(1)
    check_file(sys.argv[1])
