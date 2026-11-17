#!/usr/bin/env python3
"""
🎭 Four Masters Vote v1.0 - 4 大师视角对抗
基于 ai-berkshire /investment-team + /investment-research

核心: 段永平/巴菲特/芒格/李录 4 大师 各自 独立 打分
强制 冲突 (不 取 平均) / 揭示 真实 矛盾

用法:
  python3 four_masters_vote.py --code 300757
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime


HOLDINGS_META = {
    '603259': {
        'name': '药明康德', 'sector': 'CXO/医药',
        'business': '全球 Top 3 CXO / CDMO / TIDES / ATU',
        'moat': '一体化服务 + 全球客户网络 + 高转换成本',
        'management': '李革 (创始人) / 稳健',
        'risks': '美国 客户 70% + 生物安全法案',
        'valuation': 'PE 18.7 / DCF ¥179 (+47%)',
        'ten_year': 'CXO 长期渗透率 提升 / GLP-1 长期 受益',
    },
'300757': {
        'name': '罗博特科', 'sector': 'CPO/半导体设备',
        'business': '业务转型期 - 光伏 (老/正剥离) + CPO/硅光设备 (新/高毛利/高增)',
        'moat': 'ficonTEC 全球CPO设备寡头 + 英伟达/台积电/博通/Lumentum 客户矩阵',
        'management': '戴军 (董事长 有远见 / 完成 2019-2024 跨国收购 / 曾有警示)',
        'risks': '短期亏损 (光伏拖累) / H股上市溢价收敛 / CPO量产延后到 2028 (SemiAnalysis)',
        'valuation': '看新业务: 2026年1-4月新增光电子订单 ¥10.21亿 (占2024年营收92%) / 高盛目标 ¥688 (+30%)',
        'ten_year': 'CPO 长期主升 (1.6T→3.2T→CPO) / 全球AI算力 光互连 卡脖子设备 / 你7/1心法: 短期看情绪 长期看业绩',
        'note': '⚠️ 分拆看: 光伏业务 (老) 正 出清 → 短期亏损假象; CPO/硅光业务 (新) 高毛利+高增 = 真长线',
    },

    '600522': {
        'name': '中天科技', 'sector': '半导体/AI 算力/海缆',
        'business': 'AI 算力 + 海缆 + 光模块',
        'moat': '海缆 全球 前 5 / 客户 稳定',
        'management': '薛济萍 / 稳健',
        'risks': '半导体 板块 兑现 压力',
        'valuation': 'PE 25 / DCF ¥80+ (+55%)',
        'ten_year': 'AI 数据中心 长期 建设',
    },
    '000988': {
        'name': '华工科技', 'sector': 'CPO/光通信',
        'business': '光模块 + 激光 + 传感',
        'moat': '光模块 国内 Top 3',
        'management': '马新强 / 稳健',
        'risks': 'CPO 量产延后 / 美国 出口 管制',
        'valuation': 'PE 32 / v2.1 92 分',
        'ten_year': '光通信 长期 主升 (1.6T → 3.2T)',
    },
}


def duan_yongping(meta):
    """段永平 - 商业模式 视角"""
    score = 3
    reasons = []
    
    if '寡头' in meta['moat'] or 'Top 3' in meta['moat'] or '客户网络' in meta['moat'] or '客户矩阵' in meta['moat']:
        score += 1.0
        reasons.append('好生意 (寡头/网络)')
    
    # ⭐ 业务转型 v2: 若 新业务 高毛利+高增 → +分 而非 -分
    business = meta['business']
    note = meta.get('note', '')
    if '转型' in business and ('高毛利' in business or '高毛利' in note or '高增' in business):
        score += 0.8  # 加分 (新业务 是 好生意)
        reasons.append('新业务 高毛利+高增 (好生意 拐点)')
    elif '转型' in business and '亏' in meta.get('risks', ''):
        # 老业务 出清 短期 影响 / 不 大扣
        score -= 0.2
        reasons.append('业务转型期 / 短期扰动')
    
    # 有远见 管理层 加分
    if '远见' in meta['management'] or '战略' in meta['management']:
        score += 0.5
        reasons.append('管理 有远见 (跨国收购)')
    if '稳健' in meta['management']:
        score += 0.5
        reasons.append('管理 稳健')
    if '警示' in meta['management']:
        score -= 0.3  # 减少 惩罚 (仅 曾有 警示 / 已 过去)
        reasons.append('管理 有 历史 污点 (但 战略正确)')
    
    return {
        'master': '段永平',
        'view': '商业模式',
        'score': round(min(5, max(0, score)), 1),
        'reasons': reasons,
        'quote': f'"生意本质: {meta["business"]}. 好生意 = 用户越多, 商家越多"',
    }


def buffett(meta):
    """巴菲特 - 财务估值 视角"""
    score = 3
    reasons = []
    val = meta['valuation']
    
    # ⭐ 若 "看新业务" 有 大订单 → 加分 (不 拘泥 PE)
    if '订单' in val or '在手订单' in val or '合同' in val:
        try:
            yi_match = re.search(r'¥(\d+\.?\d*)\s*亿', val)
            if yi_match:
                yi = float(yi_match.group(1))
                if yi >= 10: score += 1.5; reasons.append(f'新订单 ¥{yi}亿 = 未来 兑现 印钞')
                elif yi >= 5: score += 1.0; reasons.append(f'新订单 ¥{yi}亿')
        except: pass
    
    # 高盛/机构 目标 加分
    if '高盛' in val or '机构' in val:
        try:
            pct = int(re.search(r'\+(\d+)%', val).group(1))
            if pct >= 30: score += 1.5; reasons.append(f'机构目标 +{pct}%')
            elif pct >= 15: score += 0.8; reasons.append(f'机构目标 +{pct}%')
        except: pass
    
    # DCF 加分
    if 'DCF' in val and '+' in val:
        try:
            pct = int(re.search(r'DCF.*?\+(\d+)%', val).group(1))
            if pct >= 30: score += 1.5; reasons.append(f'DCF +{pct}%')
        except: pass
    
    # PE 减分 (但 若 转型期 减 弱)
    if 'PE 亏损' in val or 'PE 亏' in val:
        if '转型' in meta.get('business', ''):
            score -= 0.3  # 减轻 (转型期 PE 假象)
            reasons.append('PE 亏损 (但 转型期 / 分业务 看)')
        else:
            score -= 1.5
            reasons.append('PE 亏损 (业绩差)')
    elif 'PE' in val:
        try:
            pe = float(re.search(r'PE (\d+\.?\d*)', val).group(1))
            if pe < 20: score += 0.8; reasons.append(f'PE {pe} 便宜')
            elif pe < 40: score += 0.3; reasons.append(f'PE {pe} 合理')
            else: score -= 0.5; reasons.append(f'PE {pe} 偏贵')
        except: pass
    
    if '高转换成本' in meta['moat'] or '客户 稳定' in meta['moat'] or '客户矩阵' in meta['moat']:
        score += 0.5
        reasons.append('印钞机 特征 (客户 深锁定)')
    
    return {
        'master': '巴菲特',
        'view': '财务估值',
        'score': round(min(5, max(0, score)), 1),
        'reasons': reasons,
        'quote': f'"估值: {val}. 价格 是 你付的 / 价值 是 你得的"',
    }


def munger(meta):
    """芒格 - 逆向思考 视角 (什么情况会死)"""
    score = 3
    reasons = []
    risks = meta['risks']
    
    # 反向 找 致命 风险 (但 转型期 有 订单 = 减 惩罚)
    fatal_keywords = ['亏', '管制', '生物安全', '收敛', '延后', '警示']  # 移除 '兑现'
    has_order_evidence = ('订单' in meta.get('valuation', '') or '合同' in meta.get('valuation', ''))
    penalty = 0.25 if has_order_evidence and '转型' in meta.get('business', '') else 0.4
    for kw in fatal_keywords:
        if kw in risks:
            score -= penalty
            reasons.append(f'致命风险: {kw}')
        elif kw in meta.get('management', '') and kw == '警示':
            score -= 0.2
            reasons.append(f'管理层 曾有 {kw} (已过去)')
    
    # 护城河 深度
    if '一体化' in meta['moat'] or '网络' in meta['moat']:
        score += 0.8
        reasons.append('护城河 深')
    elif '全球寡头' in meta['moat']:
        score += 1.0
        reasons.append('全球寡头 (最强 护城河)')
    
    # 如果 明天 消失?
    if 'CXO' in meta['sector']:
        reasons.append('消失 = 全球药企 供应链 断裂')
        score += 0.3
    elif 'CPO' in meta['sector'] or '海缆' in meta['business']:
        reasons.append('消失 = AI 算力 建设 受阻')
        score += 0.2
    
    return {
        'master': '芒格',
        'view': '逆向思考 (什么情况会死)',
        'score': round(min(5, max(0, score)), 1),
        'reasons': reasons,
        'quote': f'"反过来想: {risks}. 若这些成真 会 -50%"',
    }


def li_lu(meta):
    """李录 - 长期确定性 (10 年 后 是否 还在?)"""
    score = 3
    reasons = []
    ten_year = meta.get('ten_year', '')
    
    if '长期' in ten_year and ('渗透率' in ten_year or '主升' in ten_year):
        score += 1.5
        reasons.append('文明级 长期 需求')
    
    # ⭐ 卡脖子 设备 大幅 加分
    if '卡脖子' in ten_year or '寡头' in meta.get('moat', ''):
        score += 1.0
        reasons.append('卡脖子/寡头 = 长期 印钞')
    
    if 'AI' in meta['sector'] or 'CXO' in meta['sector'] or 'GLP' in ten_year:
        score += 0.5
        reasons.append('顺应 文明 趋势')
    
    if 'CPO' in ten_year and '主升' in ten_year:
        score += 0.5
        reasons.append('CPO 主升浪 明确')
    
    # 转型期 - 若 新业务 有 大订单 → 不扣 (兑现 中)
    if '亏' in meta.get('risks', '') and '转型' in meta['business']:
        val = meta.get('valuation', '')
        if '订单' in val or '合同' in val:
            score -= 0.2  # 减轻 (订单 = 兑现 依据)
            reasons.append('转型期 / 但 订单 兑现 中')
        else:
            score -= 0.8
            reasons.append('转型 期 / 10 年 兑现 待验证')
    
    if '不 确定' in ten_year or '不确定' in ten_year:
        score -= 1.0
        reasons.append('10 年 确定性 弱')
    
    return {
        'master': '李录',
        'view': '10 年 确定性',
        'score': round(min(5, max(0, score)), 1),
        'reasons': reasons,
        'quote': f'"10 年 后: {ten_year}. 不确定 就 不买"',
    }


def analyze(code):
    if code not in HOLDINGS_META: return None
    meta = HOLDINGS_META[code]
    return {
        'code': code,
        'meta': meta,
        'masters': [duan_yongping(meta), buffett(meta), munger(meta), li_lu(meta)],
    }


def format_report(r):
    if not r: return ""
    m = r['meta']
    
    out = f"""
╔══════════════════════════════════════════════════════════╗
║  🎭 {m['name']} ({r['code']}) - 4 大师 视角 对抗
╚══════════════════════════════════════════════════════════╝

📌 公司 快照:
  🏢 主业: {m['business']}
  🛡 护城河: {m['moat']}
  👔 管理层: {m['management']}
  🚨 风险: {m['risks']}
  💰 估值: {m['valuation']}
  🔭 10 年: {m['ten_year']}

📊 4 大师 独立 打分 (0-5):
"""
    
    for master in r['masters']:
        stars = '⭐' * int(master['score']) + '✩' * (5 - int(master['score']))
        out += f"\n  🎯 {master['master']} - {master['view']}: {master['score']}/5\n"
        out += f"     {stars}\n"
        out += f"     {master['quote']}\n"
        for reason in master['reasons']:
            out += f"     • {reason}\n"
    
    # 对抗 分析
    scores = [m['score'] for m in r['masters']]
    max_s = max(scores)
    min_s = min(scores)
    diff = max_s - min_s
    avg = sum(scores) / 4
    
    out += f"\n📊 对抗 分析:\n"
    out += f"  最高: {max_s} ({[m['master'] for m in r['masters'] if m['score'] == max_s][0]})\n"
    out += f"  最低: {min_s} ({[m['master'] for m in r['masters'] if m['score'] == min_s][0]})\n"
    out += f"  分歧: {diff}\n"
    out += f"  平均: {avg:.1f}\n"
    
    if diff >= 2:
        out += f"  🚨 严重 分歧! 关键 变量 决定 (深度 研究)\n"
    elif diff >= 1:
        out += f"  ⚠️ 中度 分歧 / 谨慎 决策\n"
    else:
        out += f"  ✅ 高度 共识\n"
    
    # 综合 决策 (ai-berkshire 风格)
    if avg >= 4.0:
        verdict = '🌟🌟🌟🌟🌟 通过 (可重仓)'
    elif avg >= 3.5:
        verdict = '🌟🌟🌟🌟 有条件 通过'
    elif avg >= 3.0:
        verdict = '❓ 灰色 地带 (深度研究)'
    elif avg >= 2.5:
        verdict = '🟡 观望'
    else:
        verdict = '🔴 不通过'
    
    out += f"\n💎 综合 决策: {verdict}\n"
    
    # 4 大师 综合 建议
    out += f"\n🎯 综合 建议:\n"
    if r['masters'][0]['score'] >= 4:  # 段永平
        out += f"  ✅ 段永平: 好生意\n"
    if r['masters'][1]['score'] >= 4:  # 巴菲特
        out += f"  ✅ 巴菲特: 好价格\n"
    if r['masters'][2]['score'] <= 2.5:  # 芒格
        out += f"  🚨 芒格: 反面 场景 严重\n"
    if r['masters'][3]['score'] >= 4:  # 李录
        out += f"  ✅ 李录: 10 年 确定\n"
    elif r['masters'][3]['score'] <= 2.5:
        out += f"  🔴 李录: 10 年 不确定\n"
    
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--code', help='单股')
    args = parser.parse_args()
    
    print(f"🎭 Four Masters Vote v1.0 (段永平 + 巴菲特 + 芒格 + 李录)")
    print(f"⏰ {datetime.now():%Y-%m-%d %H:%M}  / 基于 ai-berkshire\n")
    
    codes = [args.code] if args.code else ['603259', '300757', '600522', '000988']
    
    for code in codes:
        r = analyze(code)
        print(format_report(r))
    
    if not args.code:
        # 汇总
        print("\n" + "=" * 60)
        print("📊 全持仓 4 大师 综合")
        print("=" * 60)
        print(f"{'股票':<10s} {'段':>4s} {'巴':>4s} {'芒':>4s} {'李':>4s} {'均':>5s}")
        print("-" * 50)
        for code in codes:
            r = analyze(code)
            if r:
                scores = [m['score'] for m in r['masters']]
                avg = sum(scores) / 4
                print(f"  {r['meta']['name']:<8s} {scores[0]:>3.1f} {scores[1]:>3.1f} {scores[2]:>3.1f} {scores[3]:>3.1f}  {avg:>4.1f}")


if __name__ == '__main__':
    main()
