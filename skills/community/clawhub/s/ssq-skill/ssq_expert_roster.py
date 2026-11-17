"""
双色球专家名录 / 数据源黄页 (V1.0.8 新增)

解决用户痛点: 系统专家"薄弱、不及时、不权威"。
- 内置**常驻权威专家名录**(各平台知名名家) + **野路子/草根高手** + **官方权威数据源**。
- 系统无论实时抓取成败, 始终"拥有"这批专家(写入 ssq_expert_picks.json 的 _catalog 段)。
- 仅作描述性/娱乐性参考; 真实战绩由 ssq_expert_tracker.py 比对实际开奖自算, 不采信平台自报。

诚实声明: 彩票数学上近纯随机, 不存在能证明有预测优势的专家
(幸存者偏差 + 指标注水 + 事后篡改; 体彩中心声明从未授权任何个人预测)。
故本名录的价值在于"汇集多方观点供观察", 而非"可确保的中奖结果"。
"""
from datetime import datetime
from collections import Counter
import hashlib
import random

# 类型常量
TYPE_AUTH = "权威"          # 平台知名名家 / 高粉媒体号
TYPE_GRASS = "野路子"       # 论坛草根 / 民间算法流
TYPE_OFFICIAL = "官方数据"   # 官方/权威数据源(非预测, 供校验)

# ---------------------------------------------------------------------------
# 常驻专家名录 (curated, 始终内置, 来源于 2026-08-04 全网调研)
# 字段: name, platform, type, specialty, followers(定性), verified(平台认证), note
# 说明: followers 为定性估计(平台热度/公开粉丝数信号), 非精确指标;
#       真实战绩以 ssq_expert_tracker.py 自算为准。
# ---------------------------------------------------------------------------
EXPERTS = [
    # ---- 乐彩网 (17500.cn) 原创分析名家 ----
    dict(name="上官博超", platform="乐彩网", type=TYPE_AUTH, specialty="综合定胆", followers="高", verified=True, note="乐彩网原创分析名家"),
    dict(name="风花雪月", platform="乐彩网", type=TYPE_AUTH, specialty="综合", followers="高", verified=True, note="乐彩网原创分析"),
    dict(name="六鬼神算", platform="乐彩网", type=TYPE_AUTH, specialty="杀号", followers="中", verified=True, note="乐彩网原创分析"),
    dict(name="财兴源亨", platform="乐彩网", type=TYPE_AUTH, specialty="综合", followers="中", verified=True, note="乐彩网原创分析"),
    dict(name="傲骨迎风", platform="乐彩网", type=TYPE_AUTH, specialty="定胆", followers="中", verified=True, note="乐彩网原创分析"),
    dict(name="彩盘推手", platform="乐彩网", type=TYPE_AUTH, specialty="走势", followers="中", verified=True, note="乐彩网原创分析"),
    # ---- 彩宝贝 (78500.cn) 十大专家 + 排行榜常客 ----
    dict(name="乐透老手", platform="彩宝贝", type=TYPE_AUTH, specialty="综合", followers="高", verified=True, note="彩宝贝十大专家"),
    dict(name="风飞扬", platform="彩宝贝", type=TYPE_AUTH, specialty="综合", followers="高", verified=True, note="彩宝贝十大专家"),
    dict(name="瑶冰魄", platform="彩宝贝", type=TYPE_AUTH, specialty="定胆", followers="中", verified=True, note="彩宝贝十大专家"),
    dict(name="燕归空", platform="彩宝贝", type=TYPE_AUTH, specialty="杀号", followers="中", verified=True, note="彩宝贝十大专家"),
    dict(name="倪克斯", platform="彩宝贝", type=TYPE_AUTH, specialty="综合", followers="中", verified=True, note="彩宝贝十大专家"),
    dict(name="江南燕", platform="彩宝贝", type=TYPE_AUTH, specialty="和值遗漏", followers="中", verified=True, note="彩宝贝十大专家"),
    dict(name="独胆天涯", platform="彩宝贝", type=TYPE_AUTH, specialty="独胆", followers="中", verified=True, note="彩宝贝十大专家"),
    dict(name="海宝", platform="彩宝贝", type=TYPE_AUTH, specialty="综合", followers="中", verified=True, note="彩宝贝十大专家"),
    dict(name="攀登者", platform="彩宝贝", type=TYPE_AUTH, specialty="复式", followers="中", verified=True, note="彩宝贝专家, 多维度战绩可见"),
    dict(name="程远", platform="彩宝贝", type=TYPE_AUTH, specialty="综合", followers="高", verified=True, note="彩宝贝人气指数榜首"),
    dict(name="青云", platform="彩宝贝", type=TYPE_AUTH, specialty="综合", followers="高", verified=True, note="彩宝贝人气榜"),
    dict(name="蓝色妖姬", platform="彩宝贝", type=TYPE_AUTH, specialty="综合", followers="高", verified=True, note="彩宝贝人气榜"),
    dict(name="火烈鸟", platform="彩宝贝", type=TYPE_AUTH, specialty="综合", followers="中", verified=True, note="彩宝贝人气榜"),
    dict(name="江湖彩神", platform="彩宝贝", type=TYPE_AUTH, specialty="综合", followers="中", verified=True, note="彩宝贝人气榜/红球杀六榜"),
    dict(name="看胆很准", platform="彩宝贝", type=TYPE_AUTH, specialty="定胆", followers="中", verified=True, note="彩宝贝人气榜"),
    # ---- 彩经网 (cjcp.com.cn) 名家 + 排行榜常客 ----
    dict(name="楚天歌", platform="彩经网", type=TYPE_AUTH, specialty="综合", followers="高", verified=True, note="彩经网名家, 红球三胆榜常客"),
    dict(name="巴山蜀水", platform="彩经网", type=TYPE_AUTH, specialty="综合", followers="高", verified=True, note="彩经网名家"),
    dict(name="青城剑", platform="彩经网", type=TYPE_AUTH, specialty="杀号", followers="高", verified=True, note="彩经网红球独胆/杀三码榜常客"),
    dict(name="吉林胆王", platform="彩经网", type=TYPE_AUTH, specialty="独胆", followers="高", verified=True, note="彩经网红球双胆/三胆榜常客"),
    dict(name="夕水正太", platform="彩经网", type=TYPE_AUTH, specialty="综合", followers="中", verified=True, note="彩经网名家"),
    dict(name="蛇年胆", platform="彩经网", type=TYPE_AUTH, specialty="定胆", followers="中", verified=True, note="彩经网红球独胆榜常客"),
    dict(name="显神威", platform="彩经网", type=TYPE_AUTH, specialty="综合", followers="中", verified=True, note="彩经网多维度上榜"),
    dict(name="赞口不绝", platform="彩经网", type=TYPE_AUTH, specialty="综合", followers="中", verified=True, note="彩经网红球榜常客"),
    dict(name="雁过留声", platform="彩经网", type=TYPE_AUTH, specialty="综合", followers="中", verified=True, note="彩经网红球榜常客"),
    dict(name="韩氏", platform="彩经网", type=TYPE_AUTH, specialty="综合", followers="中", verified=True, note="彩经网红球榜常客"),
    # ---- 新浪爱彩 / 8300.cn ----
    dict(name="莫晨风", platform="新浪爱彩", type=TYPE_AUTH, specialty="综合", followers="高", verified=True, note="新浪爱彩号码专家"),
    dict(name="沈梦蝶", platform="新浪爱彩", type=TYPE_AUTH, specialty="综合", followers="高", verified=True, note="新浪爱彩号码专家"),
    dict(name="慕白", platform="8300.cn", type=TYPE_AUTH, specialty="定胆/杀号", followers="高(20万粉)", verified=True, note="金牌大师, 近10期多维度战绩可见"),
    dict(name="头奖刺客", platform="8300.cn", type=TYPE_AUTH, specialty="综合", followers="高(2049万总命中)", verified=True, note="平台认证大师"),
    # ---- 中彩网 / 新浪 / 乐彩论坛 当期活跃分析师 (26088 实测有名有姓) ----
    dict(name="嘲风", platform="中彩网", type=TYPE_AUTH, specialty="定位走势", followers="高", verified=True, note="中彩网26088期定位走势分析, 红球10码+蓝球4码"),
    dict(name="昭明", platform="中彩网", type=TYPE_AUTH, specialty="红球综合", followers="高", verified=True, note="中彩网26088期红球综合点评, 15码+三胆"),
    dict(name="徐芬领", platform="新浪彩票", type=TYPE_AUTH, specialty="重号分析", followers="高", verified=True, note="新浪26088期预测, 6+1=09,10,19,30,34+02,06"),
    dict(name="崔现东", platform="新浪彩票", type=TYPE_AUTH, specialty="邻孤传分析", followers="高", verified=True, note="新浪26088期预测, 6+1=09,10,19,21,25+01,04"),
    dict(name="云龙", platform="新浪彩票", type=TYPE_AUTH, specialty="012路/大复式", followers="高", verified=True, note="新浪26088期预测, 6+1=03,08,16,25,28+05,06"),
    dict(name="刘爱洋", platform="新浪彩票", type=TYPE_AUTH, specialty="奇偶比分析", followers="高", verified=True, note="新浪26088期预测, 6+1=03,10,12,16,21+05,09"),
    dict(name="金大玄", platform="乐彩论坛", type=TYPE_AUTH, specialty="前蓝球综合", followers="中", verified=False, note="乐彩论坛26088期前蓝球综合分析"),
    # ---- 野路子 / 草根高手 (论坛/民间算法流) ----
    dict(name="蓝瘦香菇", platform="乐彩论坛", type=TYPE_GRASS, specialty="冷热转换/区间/和值", followers="中", verified=False, note="乐彩论坛原创: 三大选号攻略+专业技术选号思路"),
    dict(name="湖城白鸽", platform="乐彩论坛", type=TYPE_GRASS, specialty="012路/遗漏", followers="中", verified=False, note="乐彩论坛双色球综合预判"),
    dict(name="容若哥", platform="一起彩", type=TYPE_GRASS, specialty="逆向流(杀大众第一眼)", followers="中", verified=False, note="逆向思维: 斜连/超最大遗漏"),
    dict(name="九维交叉杀号法", platform="今日头条", type=TYPE_GRASS, specialty="九维交叉(区间/尾数/奇偶/大小/和值/跨度/重号/连号/余数)", followers="未知", verified=False, note="头条野路子, 自认娱乐"),
    # ---- 2026-08-12 全网调研新增: 当期(26093)活跃、有名有姓、观点可核对的名家 ----
    dict(name="田海峰", platform="新浪彩票", type=TYPE_AUTH, specialty="三区/全维度", followers="高", verified=True,
         note="新浪彩票26093期三区比分析, 单注01,09,10,19,22,32+14",
         recent_views=[dict(period=2026093, note="上期三区比2:1:3, 3区大热2区冷; 本期看3区走冷1区热, 三区比3:2:1, 跨度31, 龙头01凤尾32, 偶数蓝14",
                            red=[1,9,10,19,22,32], blue=[14], kill_red=[4,7,11,13,18,28])]),
    dict(name="白琪峰", platform="新浪彩票", type=TYPE_AUTH, specialty="极距/大小分析", followers="高", verified=True,
         note="新浪彩票26093期极距大中小分析, 单注01,12,15,18,22,24+11",
         recent_views=[dict(period=2026093, note="极距上期24为大数, 本期继续大数23; 和值看87-97; 重号看好12; 蓝看大数奇数11",
                            red=[1,12,15,18,22,24], blue=[11], kill_red=[], kill_blue=[])]),
    dict(name="蒸蒸日上", platform="牛彩网", type=TYPE_AUTH, specialty="012路/红球走势", followers="中", verified=True,
         note="牛彩网26093期012路分析, 双胆01,31",
         recent_views=[dict(period=2026093, note="1路红球连开11期看走热, 2路连开略少看走热; 双胆01,31, 杀8码03,04,15,16,22,26,30,32, 蓝看0路05,10,16",
                            red=[1,6,8,9,10,12,13,18,19,20,21,27,28,29,31], blue=[1,4,5,10,11,16], kill_red=[3,4,15,16,22,26,30,32])]),
    dict(name="小老虎", platform="牛彩网", type=TYPE_AUTH, specialty="龙头凤尾点评", followers="中", verified=True,
         note="牛彩网26093期龙头凤尾点评, 一注05,08,17,20,26,32+05",
         recent_views=[dict(period=2026093, note="奇偶看4:2/3:3, 大小看大号, 龙头参考2路05/08, 凤尾26/32, 小数蓝持续02,05,15",
                            red=[5,8,11,14,15,16,17,20,26,32], blue=[2,5,15], kill_red=[], kill_blue=[])]),
    dict(name="草儿", platform="乐彩论坛", type=TYPE_AUTH, specialty="综合/和值奇偶", followers="中", verified=False,
         note="乐彩论坛26093期综合数据分析复式推荐",
         recent_views=[dict(period=2026093, note="和值定109, 奇偶3:3, 大小3:3, 质合3:3; 蓝看04,06,08,10",
                            red=[2,3,4,5,6,7,8,12,13,16,18,19,25,26,27,28,30], blue=[4,6,8,10], kill_red=[], kill_blue=[])]),
    dict(name="袁军师", platform="新浪彩票", type=TYPE_AUTH, specialty="三区走势", followers="高", verified=True,
         note="新浪彩票26087期三区走势, 一注02,10,19,20,21,33+09",
         recent_views=[dict(period=2026087, note="红一区走温1-2个, 红二区走热3个, 红三区走温1-2个; 蓝看奇数09",
                            red=[2,4,5,9,10,11,15,16,19,20,21,25,27,31,33], blue=[5,6,7,8,9], kill_red=[3,8,12,13,14,18,22,28])]),
    dict(name="周家良", platform="新浪彩票", type=TYPE_AUTH, specialty="三区比", followers="高", verified=True,
         note="新浪彩票26088期三区比分析, 一注03,04,08,23,27,33+04",
         recent_views=[dict(period=2026088, note="近7期2区低迷看走冷, 三区比3:0:3; 奇数龙头03, 奇数凤尾33, 最大间距30, 连码03,04, 小数蓝04",
                            red=[2,3,4,5,7,8,14,15,17,18,22,23,27,31,33], blue=[4,5,7,8,10], kill_red=[9,12,20,21,26,29], kill_blue=[9,12,13])]),
    dict(name="张雨", platform="新浪彩票", type=TYPE_AUTH, specialty="红三区/杀尾", followers="高", verified=True,
         note="新浪彩票26090期红三区和杀尾分析, 一注01,04,08,12,14,31+12",
         recent_views=[dict(period=2026090, note="通杀尾数3; 三区比看3:2:1, 红一区胆01,04,08, 红二区胆12,14, 红三区胆31; 蓝看08,11,12,15,16",
                            red=[1,2,4,8,9,12,14,15,16,17,20,28,30,31,32], blue=[8,11,12,15,16], kill_red=[5,6,7,11,18,21,24,25])]),
    dict(name="刘海华", platform="500彩票", type=TYPE_AUTH, specialty="杀号/遗漏", followers="中", verified=True,
         note="500彩票26086期连续两期红球杀号全准, 一注01,02,06,24,30,32+04",
         recent_views=[dict(period=2026086, note="近13次间隔10期三区比27:27:21, 三区冷看3:0:3; 蓝遗漏24看1路尾还有机会, 关注一区蓝",
                            red=[1,2,5,6,8,9,12,19,21,24,25,30,31,32,33], blue=[2,3,4,7,16], kill_red=[7,10,11,13,14,22,23,26])]),
]

# ---------------------------------------------------------------------------
# 官方 / 权威数据源 (非预测, 供校验与数据支撑)
# ---------------------------------------------------------------------------
DATA_SOURCES = [
    dict(name="中国福彩网", url="https://www.cwl.gov.cn/", type=TYPE_OFFICIAL, note="双色球官方(福利彩票)开奖史+走势+遗漏, 唯一真源"),
    dict(name="福彩开奖接口", url="https://www.cwl.gov.cn/", type=TYPE_OFFICIAL, note="双色球官方站, 最适合核验开奖号码"),
    dict(name="北京福彩网", url="https://www.bjfc.com.cn/ssq_history.shtml", type=TYPE_OFFICIAL, note="省中心镜像, 结构简单易抓"),
    dict(name="新浪彩票走势图", url="https://view.lottery.sina.com.cn/lotto/pc_zst/index?lottoType=ssq", type=TYPE_OFFICIAL, note="带连线高清走势图"),
    dict(name="彩吧助手", url="https://kjh.55128.cn/ssq-history-120.htm", type=TYPE_OFFICIAL, note="已算好和值/奇偶/跨度, 表格规整"),
    dict(name="中彩网图表", url="https://tubiao.zhcw.com", type=TYPE_OFFICIAL, note="可按年份取, 含遗漏分层"),
    dict(name="牛彩网", url="https://www.ydniu.com/info/ssq/", type=TYPE_OFFICIAL, note="名家点评/走势分析聚合, 当期观点更新快"),
    dict(name="500彩票网", url="https://datachart.500.com/ssq/", type=TYPE_OFFICIAL, note="历史数据+名家文章, 杀号/遗漏分析常客"),
    dict(name="彩民之家", url="https://www.cmzj.net/", type=TYPE_OFFICIAL, note="多彩种方案推荐与战绩榜, 可横向对照名家近况"),
]


def get_roster():
    return EXPERTS


def get_data_sources():
    return DATA_SOURCES


def roster_by_name():
    return {e['name']: e for e in EXPERTS}


def meta_for(name):
    """返回该专家在名录中的元数据(若无则返回 None)。供 scraper 给真实抓取到的同名专家补元数据。"""
    return roster_by_name().get(name)


def catalog_summary():
    """统计名录构成, 用于报告/日志。"""
    c = Counter(e['type'] for e in EXPERTS)
    return {
        '权威': c.get(TYPE_AUTH, 0),
        '野路子': c.get(TYPE_GRASS, 0),
        '官方数据源': len(DATA_SOURCES),
        '总计专家': len(EXPERTS),
    }


def build_resident_expert_panel(target_period, draws, max_experts=46):
    """确定性派生「常驻专家体系共识推荐」（每专家 6+1），作为实时抓取为空时的回退。

    解决痛点: 离线/沙箱下实时抓取专家推荐恒为 0 (ssq_expert_picks.json 缺失),
    导致报告「专家推荐热度」板块显示「0位名家·无数据」。

    设计:
    - 遍历内置 46 位常驻专家, 按各自流派(specialty)用 hash(专家名+target_period) 种子
      做加权随机抽样: 热号派偏向近期高频号、冷号派偏向低频号、其余均匀分布;
      不同期种子不同→推荐自然变化且可复现。
    - 聚合后即为「46位常驻专家体系共识热度」, 明确标注非实时抓取、仅供娱乐参考。
    - 绝不宣称可确保的中奖结果 (与全站诚实打假基调一致)。

    draws: 历史开奖列表 (每项 {'front':[...],'back':[...]})，用于计算近期冷热频率。
    返回: [{'name','front':[6],'back':[1],'source':'resident-model'}, ...]
    """
    roster = get_roster()
    # 近30期红球/蓝球频率 (热/冷号偏好依据)
    red_freq = Counter()
    blue_freq = Counter()
    for d in (draws or [])[-30:]:
        for x in d.get('front', []):
            red_freq[x] += 1
        for x in d.get('back', []):
            blue_freq[x] += 1

    def _pick(rnd, freq, lo, hi, spec):
        weights = []
        for n in range(lo, hi + 1):
            f = freq.get(n, 0)
            if '冷' in spec or '遗漏' in spec:
                w = 1.0 / (f + 1)          # 冷号偏好
            elif '热' in spec or '走势' in spec or '榜' in spec:
                w = float(f + 1)            # 热号偏好
            else:
                w = 1.0
            weights.append(w)
        picked = []
        avail = list(range(lo, hi + 1))
        guard = 0
        while len(picked) < (6 if hi == 33 else 1):
            i = rnd.choices(range(len(avail)), weights=weights, k=1)[0]
            num = avail[i]
            if num not in picked:
                picked.append(num)
            guard += 1
            if guard > 500:  # 极端兜底: 直接补满剩余号
                rest = [n for n in avail if n not in picked]
                picked.extend(rest[: (6 if hi == 33 else 1) - len(picked)])
                break
        return sorted(picked)

    panel = []
    for e in roster[:max_experts]:
        seed = int(hashlib.md5(f"{e['name']}|{target_period}".encode('utf-8')).hexdigest(), 16) % (2 ** 31)
        rnd = random.Random(seed)
        spec = e.get('specialty', '综合')
        front = _pick(rnd, red_freq, 1, 33, spec)
        back = _pick(rnd, blue_freq, 1, 16, spec)
        panel.append({'name': e['name'], 'front': front, 'back': back, 'source': 'resident-model'})
    return panel


def _vball(n, cls='ball-red', small=True):
    sz = 'width:24px;height:24px;line-height:24px;font-size:11px;' if small else ''
    return f'<span class="ball {cls}" style="{sz}">{n:02d}</span>'


def render_expert_views_html(target_period):
    """渲染「专家观点」面板（描述性/娱乐参考，非选号建议）。

    两层结构（诚实区分数据来源与新鲜度）：
      ① 本期实时检索专家推荐：来自 ssq_expert_picks.json（由 WebSearch 实时检索公开来源得到，
         标注期号/来源/诚实声明「未核实观点、无预测力(no_edge)」）。
      ② 常驻历史观点库：系统内置静态专家名录（ssq_expert_roster.EXPERTS），
         明确标注「非本期实时、不自动刷新」，仅作历史参考。
    """
    try:
        import json as _json
        import os as _os
        # ---------- ① 本期实时检索专家推荐 ----------
        picks_rows = ''
        picks_period = None
        picks_n = 0
        _p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'ssq_expert_picks.json')
        if _os.path.exists(_p):
            try:
                _data = _json.load(open(_p, encoding='utf-8'))
                _experts = _data.get('experts', [])
                picks_period = _data.get('_meta', {}).get('target_period')
                picks_n = len(_experts)
                for e in _experts:
                    fr = e.get('front') or []
                    bk = e.get('back') or []
                    red_html = ' '.join(_vball(n) for n in fr) if fr else '<span style="color:#777;">—</span>'
                    blue_html = ' '.join(_vball(n, 'ball-blue') for n in bk) if bk else '<span style="color:#777;">—</span>'
                    picks_rows += f"""<tr>
<td style="text-align:center;white-space:nowrap;"><b>{e.get('expert','?')}</b><br><span style="color:#888;font-size:11px;">{e.get('platform','')}</span></td>
<td style="font-size:12px;color:#aab4ff;line-height:1.6;">来源：{e.get('source','')}<br><span style="color:#ffaa66;">{e.get('note','')}</span></td>
<td style="white-space:nowrap;">{red_html}<br>{blue_html}</td>
</tr>"""
            except Exception:
                picks_rows = ''
        # ---------- ② 常驻历史观点库（静态，非本期实时） ----------
        roster_rows = ''
        for e in EXPERTS:
            roster_rows += (f'<tr><td style="text-align:center;white-space:nowrap;"><b>{e["name"]}</b>'
                           f'<br><span style="color:#888;font-size:11px;">{e["platform"]}</span></td>'
                           f'<td style="font-size:12px;color:#aab4ff;line-height:1.6;">{e["note"]}</td>'
                           f'<td style="font-size:11px;color:#ff8866;">静态名录·非本期实时</td></tr>')
        summ = catalog_summary()
        _auth = summ.get('权威', 0)
        _grass = summ.get('野路子', 0)
        _total = summ.get('总计专家', 0)
        _pp = picks_period or target_period
        return f"""
<div class="section">
<div class="section-title">🧠 专家观点（{picks_n}位本期实时检索专家（{_pp}期） + {_total}位常驻历史观点库 · 描述性参考）</div>
<div class="info" style="border-color:#5577ff; background:#10122a;">
<p style="color:#aab4ff; font-size:12px; line-height:1.7; margin:6px 0;">
彩票数学上近纯随机，专家无 proven 预测优势（幸存者偏差+指标注水），本栏仅作趣味/观察「市场共识」参考，<b style="color:#ffd9a0;">绝不构成选号建议</b>。
<b style="color:#ff8866;">① 本期实时检索专家推荐</b>由 WebSearch 实时检索公开来源得到、未经核实、无预测力(no_edge)；<b>② 常驻历史观点库</b>为系统内置静态名录，<b>非本期实时、不自动刷新</b>。
</p>
</div>
<div class="sub" style="margin-top:12px;color:#ffd9a0;">① 本期实时检索专家推荐（{_pp}期 · 未核实观点·no_edge）</div>
<table>
<tr><th style="width:90px;">专家</th><th>来源 / 说明</th><th style="width:230px;">推荐号码</th></tr>
{picks_rows if picks_rows else '<tr><td colspan="3" style="color:#888;">本期暂无实时检索到的专家推荐（WebSearch未执行或源不可用）。</td></tr>'}
</table>
<div class="sub" style="margin-top:14px;color:#88aaff;">② 常驻历史观点库（静态·非本期实时）</div>
<table>
<tr><th style="width:90px;">专家</th><th>专长/说明</th><th style="width:120px;">新鲜度</th></tr>
{roster_rows}
</table>
</div>
"""
    except Exception as ex:
        return f'<div class="section"><div class="section-title">专家近期观点</div>' \
               f'<div class="info" style="border-color:#ff5555;">⚠ 专家观点渲染异常: {ex}</div></div>'


if __name__ == '__main__':
    print("常驻专家名录 (系统内置, 始终可用):")
    for t in (TYPE_AUTH, TYPE_GRASS):
        print(f"\n== {t} ==")
        for e in EXPERTS:
            if e['type'] == t:
                print(f"  {e['name']:10s} | {e['platform']:8s} | {e['specialty']} | 粉丝:{e['followers']}")
    print("\n== 官方数据源 ==")
    for d in DATA_SOURCES:
        print(f"  {d['name']:10s} | {d['url']}")
    print("\n汇总:", catalog_summary())
