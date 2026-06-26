#!/usr/bin/env python3
"""Video Subtitle Extractor - Text Calibration

Applies rule-based text corrections to raw ASR output.
Covers: homophone fixes, company/product names, financial terms,
traditional→simplified conversion.

Note: This handles mechanical corrections. For context-aware fixes
(company names, semantic errors), LLM review is still recommended.
"""

import os
import re
import sys


# ============================================================
# Calibration rules — extend this dict to add new patterns.
# Format: 'wrong_pattern': 'correction'
# ============================================================
REPLACEMENTS = {
    # ---- Homophone fixes (同音字) ----
    '硬钢': '硬扛',
    '抛押': '抛压',
    '膜光': '磨光',
    '流通骨': '流通股',
    '金接盘': '新接盘',
    '跟锋': '跟风',
    '微转就': '微赚就',
    '落带为安': '落袋为安',
    '互盘': '护盘',
    '军线': '均线',
    '再计': '在即',
    '没装': '没仓',
    '拉身': '拉升',
    '收14星': '收十字星',
    '手凑': '手搓',
    '圆码': '源码',
    # ---- Financial terms ----
    '逼散互买': '逼散户卖',
    'K线收14星': 'K线收十字星',
    '下部比率': '夏普比率',
    '最大回车': '最大回撤',
    '回车': '回测',
    '累测': '回测',
    '知性度': '置信度',
    '多头并列': '多头排列',
    '买出': '卖出',
    '进度调': '进度条',
    '白行柱状图': '横向柱状图',
    '调形图': '条形图',
    '每颗模块': '每个模块',
    '指数退币': '指数退避',
    '重视功能': '重试功能',
    '去虫按': '去重按',
    # ---- AI / Tech companies & terms ----
    '中繼續創': '中际旭创',
    '新益勝': '新易盛',
    '天賦通信': '天孚通信',
    '元傑科技': '源杰科技',
    'Deepseat': 'DeepSeek',
    'ChadGPT': 'ChatGPT',
    'HPM': 'HBM',
    '光膜块': '光模块',
    '夜冷': '液冷',
    '巨深智能': '具身智能',
    '端側推理': '端侧推理',
    '推測解碼': '推测解码',
    '主能板块': '储能板块',
    'Moe價構': 'MoE架构',
    '莫架构': 'MoE架构',
    # ---- Semiconductor / Hardware ----
    '韬定律': '道定律',
    '掏定率': '道定律',
    '刀定率': '道定律',
    '维持寸论': '摩尔定律',
    '摩尔定力': '摩尔定律',
    '全站协同': '全栈协同',
    '全站三维': '全栈三维',
    '全站设计': '全栈设计',
    '量子碎穿': '量子隧穿',
    '希腊字母掏': '希腊字母τ',
    '吸片': '芯片',
    '猥琐': '微缩',
    '硬降': '硬仗',
    '灵区总线': '灵渠总线',
    '半导体闪电': '半导体界',
    '单层平方小区': '单层平铺小区',
    '系统及经济管密度': '系统级晶体管密度',
    '电磁续航': '电池续航',
    '制的飞跃': '质的飞跃',
    '十之超越': '甚至超越',
    '奈米': '纳米',
    '阵站': '正站',
    '重靠': '仅靠',
    '战略性结构': '战略性破局',
    'EUV光刻机成本': 'EUV光刻机',
    '时间常数实言': '时间常数',
    '平坡的房间': '平铺的房间',
    '垂直落起来': '垂直摞起来',
    '立体抽屉罐': '立体抽屉柜',
    '挨家以虎': '挨家挨户',
    '曾鈺群': '曾毓群',
    # ---- Company names ----
    '阿力': '阿里',
    '曾鈺群': '曾毓群',
    '汪濤': '汪滔',
    '洪稀效应': '虹吸效应',
    '洪稀': '虹吸',
    # ---- Common substitutions ----
    '再美': '在美国',
    '底層界AI': '底层借AI',
    '考工考研': '考公考研',
    '幾過千萬人': '挤过千万人',
    '應借簡歷': '应届简历',
    '外谷歌機甲': '外骨骼机甲',
    '風頭': '风投',
    '風神': '封神',
    '精密血統': '精密协同',
    '幾年磨一件': '几年磨一剑',
    '裁美': '踩美',
    '中步行論': '中国崩溃论',
    'GROG': 'Grok',
    '韓5G': '寒武纪',
    # ---- Traditional → Simplified (high-frequency) ----
    # (full conversion handled separately below)
}


# Traditional → Simplified mapping (high-frequency chars)
TRAD_TO_SIMP = {
    '發': '发', '來': '来', '時': '时', '會': '会', '體': '体',
    '報': '报', '機': '机', '線': '线', '構': '构', '購': '购',
    '業': '业', '電': '电', '纜': '缆', '銅': '铜', '鏈': '链',
    '條': '条', '關': '关', '註': '注', '數': '数', '據': '据',
    '萬': '万', '長': '长', '門': '门', '們': '们', '個': '个',
    '隊': '队', '網': '网', '點': '点', '兩': '两', '雙': '双',
    '億': '亿', '個': '个', '麼': '么', '對': '对', '從': '从',
    '學': '学', '開': '开', '進': '进', '過': '过', '還': '还',
    '沒': '没', '說': '说', '讓': '让', '認': '认', '識': '识',
    '話': '话', '講': '讲', '讀': '读', '寫': '写', '聽': '听',
    '實': '实', '現': '现', '當': '当', '後': '后', '動': '动',
    '應': '应', '邊': '边', '頭': '头', '風': '风', '為': '为',
    '準': '准', '備': '备', '標': '标', '準': '准', '際': '际',
    '轉': '转', '連': '连', '運': '运', '遠': '远', '選': '选',
    '錢': '钱', '鐵': '铁', '銀': '银', '錯': '错', '問': '问',
    '間': '间', '門': '门', '單': '单', '車': '车', '輕': '轻',
    '較': '较', '軟': '软', '農': '农', '軍': '军', '護': '护',
    '盤': '盘', '買': '买', '賣': '卖', '貸': '贷', '資': '资',
    '險': '险', '劃': '划', '劉': '刘', '張': '张', '楊': '杨',
    '陳': '陈', '黃': '黄', '吳': '吴', '鄭': '郑', '鄧': '邓',
    '趙': '赵', '馬': '马', '孫': '孙', '羅': '罗', '華': '华',
    '蔣': '蒋', '韓': '韩', '馮': '冯', '董': '董', '蕭': '萧',
    '鎮': '镇', '創': '创', '幣': '币', '擔': '担', '斷': '断',
    '奮': '奋', '復': '复', '幹': '干', '劃': '划', '獲': '获',
    '節': '节', '儘': '尽', '驚': '惊', '舊': '旧', '絕': '绝',
    '況': '况', '礦': '矿', '擴': '扩', '勞': '劳', '樂': '乐',
    '麗': '丽', '歷': '历', '聯': '联', '練': '练', '戀': '恋',
    '靈': '灵', '陸': '陆', '倫': '伦', '亂': '乱', '滿': '满',
    '腦': '脑', '鳥': '鸟', '寧': '宁', '農': '农', '歐': '欧',
    '貧': '贫', '質': '质', '親': '亲', '慶': '庆', '窮': '穷',
    '確': '确', '讓': '让', '熱': '热', '傷': '伤', '勝': '胜',
    '聖': '圣', '勢': '势', '試': '试', '樹': '树', '術': '术',
    '順': '顺', '絲': '丝', '隨': '随', '歲': '岁', '孫': '孙',
    '態': '态', '談': '谈', '討': '讨', '統': '统', '圖': '图',
    '團': '团', '衛': '卫', '無': '无', '務': '务', '誤': '误',
    '係': '系', '細': '细', '顯': '显', '險': '险', '縣': '县',
    '響': '响', '項': '项', '協': '协', '興': '兴', '許': '许',
    '亞': '亚', '陽': '阳', '養': '养', '業': '业', '義': '义',
    '優': '优', '餘': '余', '與': '与', '預': '预', '園': '园',
    '員': '员', '約': '约', '雲': '云', '雜': '杂', '則': '则',
    '紮': '扎', '戰': '战', '這': '这', '爭': '争', '證': '证',
    '隻': '只', '紙': '纸', '製': '制', '種': '种', '眾': '众',
    '週': '周', '豬': '猪', '專': '专', '壯': '壮', '總': '总',
    '組': '组', '衛': '卫', '廠': '厂', '處': '处', '黨': '党',
    '導': '导', '兒': '儿', '飛': '飞', '豐': '丰', '婦': '妇',
    '剛': '刚', '廣': '广', '國': '国', '號': '号', '紅': '红',
    '劃': '划', '環': '环', '擊': '击', '積': '积', '極': '极',
    '紀': '纪', '價': '价', '檢': '检', '簡': '简', '劍': '剑',
    '獎': '奖', '腳': '脚', '緊': '紧', '鏡': '镜', '劇': '剧',
    '決': '决', '軍': '军', '蘭': '兰', '離': '离', '龍': '龙',
    '樓': '楼', '綠': '绿', '媽': '妈', '碼': '码', '嗎': '吗',
    '慢': '慢', '貓': '猫', '麼': '么', '夢': '梦', '滅': '灭',
    '哪': '哪', '難': '难', '補': '补', '產': '产', '處': '处',
    '反': '反', '異': '异', '詞': '词', '謀': '谋', '黨': '党',
    '區': '区', '幣': '币', '異': '异', '扳': '扳', '觀': '观',
    # Common words
    '併購': '并购', '並購': '并购', '幷購': '并购',
    '咝': '嘶', '嘩': '哗', '嚇': '吓', '噁': '恶',
    '國產': '国产', '國内': '国内', '國外': '国外',
    '市場': '市场', '公司': '公司', '企業': '企业',
    '根據': '根据', '報告': '报告', '結果': '结果',
    '資產': '资产', '投資': '投资', '商業': '商业',
    '技術': '技术', '數據': '数据', '產品': '产品',
    '服務': '服务', '部門': '部门', '集團': '集团',
    '銀行': '银行', '證券': '证券', '基金': '基金',
    '風險': '风险', '標準': '标准', '業務': '业务',
    '經濟': '经济', '財政': '财政', '貿易': '贸易',
    '金融': '金融', '保險': '保险', '製造': '制造',
    '增長': '增长', '競爭': '竞争', '領導': '领导',
    '環境': '环境', '資源': '资源', '未來': '未来',
    '發展': '发展', '支持': '支持', '影響': '影响',
    '情況': '情况', '表現': '表现', '方式': '方式',
    '能力': '能力', '策略': '策略', '經驗': '经验',
    '設計': '设计', '建設': '建设', '執行': '执行',
    '合作': '合作', '要求': '要求', '研究': '研究',
    '項目': '项目', '政策': '政策', '創新': '创新',
    '為什麼': '为什么', '怎麼樣': '怎么样',
    '問題': '问题', '關係': '关系', '信息': '信息',
    '然後': '然后', '還是': '还是', '通過': '通过',
    '應該': '应该', '已經': '已经', '這麼': '这么',
    '隻': '只', '種': '种', '顆': '颗', '個': '个',
    '條': '条', '張': '张', '塊': '块', '篇': '篇',
    '當時': '当时', '發現': '发现', '覺得': '觉得',
}


def convert_traditional_to_simplified(text):
    """Convert traditional Chinese characters to simplified."""
    result = []
    for ch in text:
        result.append(TRAD_TO_SIMP.get(ch, ch))
    return ''.join(result)


def apply_replacements(text):
    """Apply all regex-based replacements from the rule table."""
    count = 0
    for wrong, correct in REPLACEMENTS.items():
        new_text = text.replace(wrong, correct)
        if new_text != text:
            count += 1
            text = new_text
    return text, count


def calibrate_text(input_path, output_path=None):
    """Apply calibration rules to a raw transcription file.

    Args:
        input_path: Path to raw .txt transcription
        output_path: Output path (default: input_path with _calibrated suffix)

    Returns:
        Path to calibrated output file, or None on failure.
    """
    if not os.path.exists(input_path):
        print(f'[ERROR] Input file not found: {input_path}')
        return None

    if output_path is None:
        base = os.path.splitext(input_path)[0]
        output_path = f'{base}_calibrated.txt'

    # Read raw text
    with open(input_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    original_len = len(raw)
    total_corrections = 0

    # Phase 1: traditional → simplified
    simplified = convert_traditional_to_simplified(raw)
    if simplified != raw:
        trad_count = sum(1 for a, b in zip(raw, simplified) if a != b)
        total_corrections += trad_count

    # Phase 2: pattern replacements
    calibrated, pat_count = apply_replacements(simplified)
    total_corrections += pat_count

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(calibrated)

    print(f'[OK] Calibrated text saved: {output_path}')
    print(f'     Characters: {original_len} → {len(calibrated)}')
    print(f'     Corrections: {total_corrections} (trad→simp: {trad_count if simplified != raw else 0}, '
          f'patterns: {pat_count})')

    return output_path


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Apply rule-based text calibration to ASR output'
    )
    parser.add_argument('input', help='Path to raw .txt transcription')
    parser.add_argument('--output', '-o', default=None,
                        help='Output path (default: <input>_calibrated.txt)')
    parser.add_argument('--no-tradsimp', action='store_true',
                        help='Skip traditional→simplified conversion')

    args = parser.parse_args()

    # If --no-tradsimp, temporarily clear the trad→simp map
    if args.no_tradsimp:
        orig_map = TRAD_TO_SIMP.copy()
        TRAD_TO_SIMP.clear()

    result = calibrate_text(args.input, args.output)

    if args.no_tradsimp:
        TRAD_TO_SIMP.update(orig_map)

    sys.exit(0 if result else 1)