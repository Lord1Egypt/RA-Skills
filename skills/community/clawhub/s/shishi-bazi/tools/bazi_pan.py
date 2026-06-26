#!/usr/bin/env python3
"""
八字排盘 CLI 工具（完整版）
包含：四柱排盘 + 大运排列 + 起运年龄 + 流年

用法:
  python3 bazi_pan.py <阳历日期> <时辰> [性别]
  python3 bazi_pan.py --json <阳历日期> <时辰> [性别]

示例:
  python3 bazi_pan.py 1990-5-15 8:00 male
  python3 bazi_pan.py --json 1990-5-15 8:00 female
"""

import sys
import json
import lunar_python as lunar
from datetime import datetime, date

# ============================================================
# 常量
# ============================================================

TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
JIEQI_12 = ['立春', '惊蛰', '清明', '立夏', '芒种', '小暑',
             '立秋', '白露', '寒露', '立冬', '大雪', '小寒']

def is_yang_gan(g): return g in ['甲', '丙', '戊', '庚', '壬']
def gan_index(g): return TIANGAN.index(g)
def zhi_index(z): return DIZHI.index(z)
def next_gan(g, n=1): return TIANGAN[(gan_index(g) + n) % 10]
def prev_gan(g, n=1): return TIANGAN[(gan_index(g) - n) % 10]
def next_zhi(z, n=1): return DIZHI[(zhi_index(z) + n) % 12]
def prev_zhi(z, n=1): return DIZHI[(zhi_index(z) - n) % 12]

CANGGAN = {
    '子': {'本气': '癸水', '中气': None, '余气': None},
    '丑': {'本气': '己土', '中气': '癸水', '余气': '辛金'},
    '寅': {'本气': '甲木', '中气': '丙火', '余气': '戊土'},
    '卯': {'本气': '乙木', '中气': None, '余气': None},
    '辰': {'本气': '戊土', '中气': '乙木', '余气': '癸水'},
    '巳': {'本气': '丙火', '中气': '庚金', '余气': '戊土'},
    '午': {'本气': '丁火', '中气': '己土', '余气': None},
    '未': {'本气': '己土', '中气': '丁火', '余气': '乙木'},
    '申': {'本气': '庚金', '中气': '壬水', '余气': '戊土'},
    '酉': {'本气': '辛金', '中气': None, '余气': None},
    '戌': {'本气': '戊土', '中气': '辛金', '余气': '丁火'},
    '亥': {'本气': '壬水', '中气': '甲木', '余气': None},
}

GAN_WUXING = {'甲': '木', '乙': '木', '丙': '火', '丁': '火',
               '戊': '土', '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'}
ZHI_WUXING = {'子': '水', '丑': '土', '寅': '木', '卯': '木',
               '辰': '土', '巳': '火', '午': '火', '未': '土',
               '申': '金', '酉': '金', '戌': '土', '亥': '水'}

# 十二长生表（阳干顺行，阴干逆行）
# 阶段顺序：长生→沐浴→冠带→临官→帝旺→衰→病→死→墓→绝→胎→养
SHICHANG = ['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养']

# 各天干的十二长生地支（阳干顺排）
CHANG_SHENG = {
    '甲': '亥', '丙': '寅', '戊': '寅', '庚': '巳', '壬': '申',  # 阳干
    '乙': '午', '丁': '酉', '己': '酉', '辛': '子', '癸': '卯',  # 阴干
}


def get_shichang_position(gan, zhi):
    """
    判断某天干在地支的十二长生状态
    返回: (阶段名, 得令否)
    """
    start_zhi = CHANG_SHENG.get(gan)
    if not start_zhi:
        return None, False
    start_idx = DIZHI.index(start_zhi)
    zhi_idx = DIZHI.index(zhi)
    # 阳干顺行，阴干逆行
    if is_yang_gan(gan):
        offset = (zhi_idx - start_idx) % 12
    else:
        offset = (start_idx - zhi_idx) % 12
    stage = SHICHANG[offset]
    # 得令：长生、临官、帝旺
    de_ling = stage in ['长生', '临官', '帝旺']
    return stage, de_ling


def assess_dayzhu_strength(day_gan, month_zhi, wx_cnt, all_canggan):
    """
    评估日主强弱（简化版）
    day_gan: 日干
    month_zhi: 月支
    wx_cnt: 五行计数 dict
    all_canggan: 所有藏干五行列表
    """
    # 1. 得令：月支是否为日干的长生/临官/帝旺
    stage, de_ling = get_shichang_position(day_gan, month_zhi)

    # 2. 得地：其他地支是否有根（藏干中有同五行）
    day_wuxing = GAN_WUXING.get(day_gan, '')
    total_roots = wx_cnt.get(day_wuxing, 0)

    # 3. 得势：天干有无比劫印星
    # （这里简化：看日干五行数量是否较多）

    # 综合判断
    score = 0
    if de_ling:
        score += 3  # 得令最重要
    if total_roots >= 3:
        score += 2
    elif total_roots >= 1:
        score += 1

    if score >= 4:
        strength = '身旺'
        tendency = '偏抑'
    elif score >= 2:
        strength = '身较强'
        tendency = '略抑'
    elif score >= 1:
        strength = '身较弱'
        tendency = '略扶'
    else:
        strength = '身弱'
        tendency = '偏扶'

    return {
        '日主': day_gan,
        '日主五行': day_wuxing,
        '月支': month_zhi,
        '长生阶段': stage,
        '得令': de_ling,
        '地支根数': total_roots,
        '强弱判定': strength,
        '调候倾向': tendency,
    }

# ============================================================
# 节气日期查找
# ============================================================

def _get_jie_list(solar_year, solar_month, solar_day):
    """用 Solar -> Lunar 获取某公历日期附近的节气表"""
    s = lunar.Solar.fromYmd(solar_year, solar_month, solar_day)
    l = s.getLunar()
    table = l.getJieQiTable()
    result = []
    for kname in JIEQI_12:
        if kname in table:
            ss = table[kname]
            dt = date(int(ss.getYear()), int(ss.getMonth()), int(ss.getDay()))
            result.append((dt, kname))
    result.sort()
    return result


def find_jie_for_dayun(birth_date, direction):
    """
    找起运所需的节气。
    direction: 'forward' → 顺排，找出生日期之后的第一个节
               'backward' → 逆排，找出生日期之前的最后一个节
    返回: (datetime.date, 节气名) 或 (None, None)
    """
    all_jie = []
    for y in range(birth_date.year - 1, birth_date.year + 2):
        for m in range(1, 13):
            try:
                all_jie.extend(_get_jie_list(y, m, 1))
            except Exception:
                pass
    all_jie.sort()
    if direction == 'forward':
        for dt, kname in all_jie:
            if dt > birth_date:
                return dt, kname
    else:
        for dt, kname in reversed(all_jie):
            if dt < birth_date:
                return dt, kname
    return None, None


# ============================================================
# 大运计算
# ============================================================

def calc_dayun(birth_date, month_gan, month_zhi, year_gan, gender):
    """
    计算大运排列
    """
    yang_year = is_yang_gan(year_gan)
    gender = gender.lower() if gender else 'male'

    if (yang_year and gender == 'male') or (not yang_year and gender == 'female'):
        direction = '顺'
        jie_date, jie_name = find_jie_for_dayun(birth_date, 'forward')
    else:
        direction = '逆'
        jie_date, jie_name = find_jie_for_dayun(birth_date, 'backward')

    if jie_date:
        days = abs((jie_date - birth_date).days)
        qiyun = round(days / 3)
        remainder = days % 3
        adjust = {0: '整', 1: '+4月', 2: '+8月'}[remainder]
    else:
        days, qiyun, adjust, jie_name = 0, 3, '约3岁', '查表'

    # 排列大运（10步）
    dayun_list = []
    for i in range(10):
        if direction == '顺':
            g = next_gan(month_gan, i + 1)
            z = next_zhi(month_zhi, i + 1)
        else:
            g = prev_gan(month_gan, i + 1)
            z = prev_zhi(month_zhi, i + 1)
        age_start = qiyun + i * 10
        dayun_list.append({
            '序号': i + 1,
            '年龄': f'{age_start}-{age_start + 9}岁',
            '干支': g + z,
            '天干': g,
            '地支': z,
        })

    return {
        '方向': direction,
        '起运年龄': qiyun,
        '间隔天数': days,
        '余数调整': adjust,
        '参考节气': jie_name,
        '大运列表': dayun_list,
    }


def calc_xiaoyun(qiyun_age, month_ganzhi):
    """小运（起运前，用月柱）"""
    return {
        '说明': f'未交大运前（0-{qiyun_age - 1}岁），以月柱[{month_ganzhi}]作为小运分析',
        '月柱干支': month_ganzhi,
    }


def calc_liunian(birth_year, gender, current_year=None):
    """计算近5年流年"""
    if current_year is None:
        current_year = datetime.now().year
    results = []
    for year in range(current_year - 2, current_year + 3):
        s = lunar.Solar.fromYmd(year, 7, 1)
        l = s.getLunar()
        gz = l.getYearInGanZhi()
        gan, zhi = gz[0], gz[1]
        wuxing = GAN_WUXING.get(gan, '') + ZHI_WUXING.get(zhi, '')
        results.append({
            '年份': year,
            '干支': gz,
            '天干': gan,
            '地支': zhi,
            '五行': wuxing,
            '今年': year == current_year,
        })
    return results


# ============================================================
# 核心排盘
# ============================================================

def get_bazi(year, month, day, hour=12, minute=0, gender=None):
    """获取完整八字信息（含大运、流年）"""
    d = lunar.Lunar.fromYmdHms(year, month, day, hour, minute, 0)

    year_gz = d.getYearInGanZhi()
    month_gz = d.getMonthInGanZhi()
    day_gz = d.getDayInGanZhi()
    time_gz = d.getTimeInGanZhi()

    year_gan = d.getYearGan()
    year_zhi = d.getYearZhi()
    month_gan = d.getMonthGan()
    month_zhi = d.getMonthZhi()
    day_gan = d.getDayGan()
    day_zhi = d.getDayZhi()
    time_gan = d.getTimeGan()
    time_zhi = d.getTimeZhi()

    ss_gan = d.getBaZiShiShenGan()
    ss_zhi = d.getBaZiShiShenZhi()

    def get_cg(z):
        return CANGGAN.get(z, {'本气': None, '中气': None, '余气': None})

    # 五行统计（天干+地支）
    all_ch = year_gz + month_gz + day_gz + time_gz
    wx_cnt = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
    for ch in all_ch:
        if ch in GAN_WUXING: wx_cnt[GAN_WUXING[ch]] += 1
        if ch in ZHI_WUXING: wx_cnt[ZHI_WUXING[ch]] += 1

    # 日主强弱评估
    dayzhu_strength = assess_dayzhu_strength(day_gan, month_zhi, wx_cnt, None)

    nayin = d.getBaZiNaYin()

    # 大运
    gender_norm = gender.lower() if gender else 'male'
    birth_date = date(year, month, day)
    dayun = calc_dayun(birth_date, month_gan, month_zhi, year_gan, gender_norm)
    xiaoyun = calc_xiaoyun(dayun['起运年龄'], month_gz)
    liunian = calc_liunian(year, gender_norm)

    return {
        '四柱': {
            '年柱': year_gz, '月柱': month_gz,
            '日柱': day_gz, '时柱': time_gz,
        },
        '天干地支': {
            '年': {'干': year_gan, '支': year_zhi},
            '月': {'干': month_gan, '支': month_zhi},
            '日': {'干': day_gan, '支': day_zhi},
            '时': {'干': time_gan, '支': time_zhi},
        },
        '阴阳': {
            '年干阴阳': '阳年' if is_yang_gan(year_gan) else '阴年',
            '年干': year_gan,
        },
        '十神': {
            '年干': ss_gan[0], '年支': ss_zhi[0],
            '月干': ss_gan[1], '月支': ss_zhi[1],
            '日干': '日主', '日支': ss_zhi[2],
            '时干': ss_gan[3], '时支': ss_zhi[3],
        },
        '藏干': {
            '年支': get_cg(year_zhi), '月支': get_cg(month_zhi),
            '日支': get_cg(day_zhi), '时支': get_cg(time_zhi),
        },
        '五行': wx_cnt,
        '纳音': {
            '年柱': nayin[0], '月柱': nayin[1],
            '日柱': nayin[2], '时柱': nayin[3],
        },
        '节气': {
            '前一节': str(d.getPrevJie()), '后一节': str(d.getNextJie()),
        },
        '其他': {
            '生肖': d.getAnimal(),
            '日冲': d.getDayChong(), '日冲描述': d.getDayChongDesc(),
        },
        '大运': dayun,
        '小运': xiaoyun,
        '流年': liunian,
        '日主强弱': dayzhu_strength,
        '原始数据': {
            '阳历日期': f'{year}-{month:02d}-{day:02d}',
            '出生时辰': f'{hour:02d}:{minute:02d}',
            '性别': gender or '未指定',
        }
    }


# ============================================================
# 格式化输出
# ============================================================

def format_text(r):
    p = r['四柱']
    orig = r['原始数据']
    td = r['天干地支']
    ss = r['十神']
    cg = r['藏干']
    wx = r['五行']
    ny = r['纳音']
    dy = r['大运']
    xy = r['小运']
    ln_list = r['流年']

    day_gan = td['日']['干']

    lines = []
    lines.append("=" * 46)
    lines.append("   四柱八字排盘（完整版）")
    lines.append("=" * 46)
    lines.append("四柱：%s 年 · %s 月 · %s 日 · %s 时" % (
        p['年柱'], p['月柱'], p['日柱'], p['时柱']))
    lines.append("阳历：%s %s | 性别：%s" % (
        orig['阳历日期'], orig['出生时辰'], orig['性别']))
    lines.append("生肖：%s | %s" % (r['其他']['生肖'], r['阴阳']['年干阴阳']))
    lines.append("")

    lines.append("【天干地支】")
    for col in ['年', '月', '日', '时']:
        lines.append("  %s柱：天干[%s] 地支[%s]" % (col, td[col]['干'], td[col]['支']))

    lines.append("")
    lines.append("【十神】（以日干[%s]为基准）" % day_gan)
    lines.append("  年干[%s] · 年支[%s]" % (td['年']['干'], ss['年支']))
    lines.append("  月干[%s] · 月支[%s]" % (td['月']['干'], ss['月支']))
    lines.append("  日干[日主] · 日支[%s]" % ss['日支'])
    lines.append("  时干[%s] · 时支[%s]" % (td['时']['干'], ss['时支']))

    lines.append("")
    lines.append("【藏干】")
    for col in ['年支', '月支', '日支', '时支']:
        c = cg[col]
        lines.append("  %s：本气[%s] 中气[%s] 余气[%s]" % (
            col, c['本气'] or '—', c['中气'] or '—', c['余气'] or '—'))

    lines.append("")
    lines.append("【五行统计】%s日主 | " % GAN_WUXING.get(day_gan, ''))
    lines.append("  " + "  ".join("%s=%d" % (k, v) for k, v in wx.items()))

    ds = r['日主强弱']
    lines.append("")
    lines.append("【日主强弱】")
    lines.append("  %s (%s) 生于 %s（月支=%s，长生=%s）" % (
        ds['日主'], ds['日主五行'], ds['月支'], ds['月支'],
        ds['长生阶段']))
    lines.append("  得令：%s | 地支根数：%d | 强弱：%s | 调候倾向：%s" % (
        '是 ✓' if ds['得令'] else '否 ✗', ds['地支根数'],
        ds['强弱判定'], ds['调候倾向']))

    lines.append("")
    lines.append("【纳音】年[%s] 月[%s] 日[%s] 时[%s]" % (
        ny['年柱'], ny['月柱'], ny['日柱'], ny['时柱']))

    lines.append("")
    lines.append("【节气】前[%s] 后[%s]" % (
        r['节气']['前一节'], r['节气']['后一节']))

    lines.append("")
    lines.append("【冲煞】日冲：%s %s" % (
        r['其他']['日冲'], r['其他']['日冲描述']))

    lines.append("")
    lines.append("─" * 46)
    lines.append("【大运】方向：%s  起运年龄：%d岁（%s）  参考节气：%s" % (
        dy['方向'], dy['起运年龄'], dy['余数调整'], dy['参考节气']))
    lines.append("【小运】%s" % xy['说明'])
    lines.append("")
    lines.append("  %-5s %-12s %-6s %-4s %-4s" % ('序号', '年龄范围', '干支', '天干', '地支'))
    for d_item in dy['大运列表']:
        lines.append("  %-5d %-12s %-6s %-4s %-4s" % (
            d_item['序号'], d_item['年龄'], d_item['干支'],
            d_item['天干'], d_item['地支']))

    lines.append("")
    lines.append("─" * 46)
    lines.append("【近五年流年】")
    lines.append("  %-5s %-8s %-4s %-4s %-5s %s" % (
        '年份', '干支', '天干', '地支', '五行', '备注'))
    for ln in ln_list:
        note = " ◀ 今年" if ln['今年'] else ""
        lines.append("  %-5d %-8s %-4s %-4s %-5s%s" % (
            ln['年份'], ln['干支'], ln['天干'], ln['地支'], ln['五行'], note))

    lines.append("")
    lines.append("=" * 46)
    return '\n'.join(lines)


# ============================================================
# CLI
# ============================================================

if __name__ == '__main__':
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    is_json = '--json' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]

    if len(args) < 1:
        print(__doc__)
        sys.exit(1)

    date_parts = args[0].split('-')
    year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])

    if len(args) >= 2:
        tp = args[1].split(':')
        hour, minute = int(tp[0]), int(tp[1]) if len(tp) > 1 else 0
    else:
        hour, minute = 12, 0

    gender = args[2] if len(args) >= 3 else None

    result = get_bazi(year, month, day, hour, minute, gender)

    if is_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text(result))
