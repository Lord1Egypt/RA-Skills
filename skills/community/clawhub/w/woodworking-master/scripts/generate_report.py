#!/usr/bin/env python3
"""木工大师 HTML 报告生成器 — 根据查询主题生成交互式可视化报告"""

import json
import sys
import os
import io
from datetime import datetime

# 确保 Windows 下 stdout 使用 UTF-8 编码
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── 主题知识数据 ──────────────────────────────────────────────

KNOWLEDGE_DATA = {
    "燕尾榫": {
        "title": "燕尾榫 (Dovetail Joint)",
        "icon": "🪵",
        "alias": "万榫之母、鸠尾榫",
        "difficulty": 4,
        "difficulty_label": "★★★★☆ (中高)",
        "summary": "梯形榫头与榫尾阴阳相扣，抗拉力极强。是手工木工的标志性技艺，兼具美观与强度。",
        "categories": [
            {"name": "通燕尾榫 (Through)", "desc": "榫头贯穿，外露可见，最经典形式"},
            {"name": "半隐燕尾榫 (Half-blind)", "desc": "单面可见，抽屉正面常用"},
            {"name": "全隐燕尾榫 (Mitered)", "desc": "两面均不可见，最高级"},
            {"name": "斜燕尾榫 (Sliding)", "desc": "滑动嵌入，架子搁板常用"},
        ],
        "tools": ["燕尾锯", "凿子(6-12mm)", "燕尾规", "划线器", "角尺"],
        "steps": [
            "1. 确定角度：软木1:6(约9.5°)，硬木1:8(约7.1°)",
            "2. 尾板划线：用燕尾规标出榫尾角度和间距",
            "3. 锯切尾板：沿划线精确锯切，留线外",
            "4. 凿除废料：从两侧各凿一半，防劈裂",
            "5. 转移划线：将尾板对准头板，用划线刀转移轮廓",
            "6. 锯切头板：沿转移线精确锯切",
            "7. 凿除头板废料：方法同尾板",
            "8. 试装调整：轻敲入位，过紧则微修，过松需重做",
            "9. 胶合固定：涂胶→敲入→夹具固定→待干→齐平打磨",
        ],
        "tolerance": "间隙≤0.1mm，过盈配合0.05mm为佳",
        "applications": ["抽屉", "盒子", "柜体角接", "高档家具"],
        "tips": [
            "划线刀优于铅笔 — 刀痕更精确且有引导作用",
            "留线锯切(不锯到线)，凿到线内，最后修整",
            "每次只做一个接头，做完再划下一个",
            "第一对失败很正常，木工是'错误修复的艺术'",
        ],
    },
    "指接榫": {
        "title": "指接榫 (Finger / Box Joint)",
        "icon": "🪚",
        "alias": "箱接榫、梳齿榫",
        "difficulty": 3,
        "difficulty_label": "★★★☆☆ (中等)",
        "summary": "矩形指状凸起交错咬合，胶合面积大。比燕尾榫简单但实用性强，可用台锯批量生产。",
        "categories": [
            {"name": "手工指接", "desc": "划线→锯→凿，精度依赖手艺"},
            {"name": "台锯夹具指接", "desc": "用自制夹具可批量高精度生产"},
            {"name": "雕刻机指接", "desc": "用指接夹具+雕刻机，效率极高"},
        ],
        "tools": ["台锯+自制夹具(推荐)", "夹背锯(手工)", "凿子", "角尺"],
        "steps": [
            "1. 计算指宽：通常为板厚1-1.5倍，指距与指宽相等",
            "2. 两板同步划线：确保完全对齐",
            "3. 锯切指槽：留线锯切",
            "4. 凿除废料/修整：确保指槽垂直",
            "5. 试装：应紧密贴合，微修调整",
            "6. 胶合+夹具：胶水涂布均匀",
        ],
        "tolerance": "指宽公差±0.2mm",
        "applications": ["箱子", "抽屉", "长料拼接", "工具柜"],
        "tips": [
            "台锯+自制指接夹具是效率最高的方式",
            "指宽=板厚时视觉效果最协调",
            "外露指接用不同颜色木材可做装饰效果",
        ],
    },
    "粽角榫": {
        "title": "粽角榫 (Three-Way Miter Joint)",
        "icon": "🏯",
        "alias": "三角齐尖、综角榫、三碰肩",
        "difficulty": 5,
        "difficulty_label": "★★★★★ (极高)",
        "summary": "三根方材在顶点交汇，六个45°格角斜线，三面观均为45°。明式家具最高技艺之一，集力学与美学于一体。",
        "categories": [
            {"name": "传统粽角榫", "desc": "经典三材角接，纯手工制作"},
            {"name": "双榫粽角榫", "desc": "增强版，双榫头提升强度"},
            {"name": "带板粽角榫", "desc": "加装面板的变体"},
        ],
        "tools": ["手刨", "凿子(全套)", "框锯/夹背锯", "角尺", "划线器", "斜度规"],
        "steps": [
            "1. 原理理解：三根方材顶点交汇，每根都有榫头与卯眼",
            "2. 精确划线：这是成败关键！标记每个切点和线条，误差≤0.1mm",
            "3. 榫头加工：立柱顶端开长短两个榫头，带榫肩",
            "4. 卯眼加工：用凿子逐层清理内部卯眼，确保垂直平整",
            "5. 避榫设计：内部榫头交错处做避让，防止冲突",
            "6. 反复试装：先干装检查，再逐面调整至严丝合缝",
            "7. 胶合固定：涂胶→组装→角夹固定→检查角度",
        ],
        "tolerance": "45°角精度±0.1°，配合间隙≤0.05mm",
        "applications": ["明式桌子角", "四面平柜子", "书架角连接", "无束腰家具"],
        "tips": [
            "先做废料练习2-3次，绝不在第一次尝试就用好料",
            "划线阶段花费总时间60%以上是正常的",
            "内部避榫让位是关键 — 三材内部互不冲突",
            "整角完成后从三面检查45°格角线是否齐整",
        ],
    },
    "方材丁字接合": {
        "title": "方材丁字接合 (Mortise & Tenon)",
        "icon": "🔗",
        "alias": "榫卯基本形",
        "difficulty": 3,
        "difficulty_label": "★★★☆☆",
        "summary": "木工最基础的榫卯接合。一材开榫头(Tenon)，一材凿卯眼(Mortise)，直角或非直角连接。",
        "categories": [
            {"name": "贯通榫", "desc": "榫头穿透，外露可见"},
            {"name": "暗榫(不贯通)", "desc": "榫头不穿透，外面不可见"},
            {"name": "加楔榫", "desc": "打入楔子增大榫头，越用越紧"},
            {"name": "双榫", "desc": "大料用两个榫头增加强度"},
        ],
        "tools": ["台锯/框锯", "榫凿(打眼凿)", "角尺", "划线器"],
        "steps": [
            "1. 确定尺寸：榫头厚度≈料厚1/3，宽度≈料宽1/2",
            "2. 划线：榫头线+卯眼线同步标注",
            "3. 锯榫头：留线锯切",
            "4. 凿卯眼：分层下凿，凿子斜面朝内",
            "5. 修整：榫头四角倒角，卯眼四壁清理",
            "6. 试装：适度紧密，过松松垮失效",
        ],
        "tolerance": "榫头宽度公差±0.1mm",
        "applications": ["桌椅腿与横枨", "门框", "窗框", "床架"],
        "tips": [
            "榫头厚度=凿子宽度 — 选好凿子再定榫头尺寸",
            "卯眼先钻后凿效率高 — 用电钻钻排孔再凿通",
            "暗榫留3-5mm底部不凿穿 — 保正面美观",
        ],
    },
    "手刨": {
        "title": "手刨 (Hand Plane)",
        "icon": "🔧",
        "alias": "木工灵魂工具",
        "difficulty": 2,
        "difficulty_label": "★★☆☆☆ (入门)至 ★★★★☆ (精通)",
        "summary": "木工最重要的手工具。用于刨平、刨光、修整尺寸和角度。一把好刨+好的研磨技术是手工木工的基石。",
        "categories": [
            {"name": "中式推刨", "desc": "推式操作，分短刨(粗刨)和长刨(光刨)"},
            {"name": "日式拉刨", "desc": "拉式操作更省力，日式木工标志"},
            {"name": "西式金属刨", "desc": "调节方便，精确度高，#4(光刨)+#5(粗刨)必备"},
        ],
        "steps": [
            "1. 研磨刀刃至镜面：1000#→3000#→6000#→10000#",
            "2. 装刀调刃：刀刃伸出粗刨0.3-0.5mm，光刨0.05-0.1mm",
            "3. 刨削：顺木纹方向，入刀和出刀时下压防「啃头啃尾」",
            "4. 直角检查：用角尺检查刨出的面和边的直角",
        ],
        "tips": [
            "刀刃研磨是决定成败的80% — 钝刀毁一切",
            "刃口背面必须完全平整(用#10000目水磨石终磨)",
            "听到沙沙声而非哗哗声时刀刃需要研磨",
            "刨花越薄越透明证明刀越锋利",
        ],
    },
    "手锯": {
        "title": "手锯 (Hand Saw)",
        "icon": "🪚",
        "difficulty": 1,
        "difficulty_label": "★★☆☆☆",
        "summary": "木工最基本的切割工具。不同锯齿和锯型适合不同场景，正确使用才能做到又快又直。",
        "categories": [
            {"name": "框锯", "desc": "中式传统主力锯，换锯条适用不同场景"},
            {"name": "夹背锯", "desc": "精密榫头切割，锯齿细密"},
            {"name": "日式双面锯", "desc": "一面纵切一面横切，入门神器"},
            {"name": "燕尾锯", "desc": "锯齿极细，专用于燕尾榫"},
        ],
        "tips": [
            "中式/日式拉切(拉时切割)，西式推切 — 搞清楚方向",
            "起锯时用拇指引导锯片，轻拉2-3次建立锯路",
            "锯身垂直是关键 — 眼看锯面与木面的反射光",
            "锯路(齿尖左右开)不夹锯，但锯路越宽精度越低",
        ],
    },
    "凿子": {
        "title": "凿子 (Chisel)",
        "icon": "🔨",
        "difficulty": 2,
        "difficulty_label": "★★☆☆☆ (至精通 ★★★★☆)",
        "summary": "榫卯加工的精密工具。打眼、修榫、清理卯底，一把锋利的凿子是无价之宝。",
        "categories": [
            {"name": "平凿", "desc": "3-30mm，打眼修榫万能"},
            {"name": "打眼凿(榫凿)", "desc": "6-16mm，刀身厚实，专凿深孔"},
            {"name": "斜凿", "desc": "修角、去废料"},
        ],
        "tips": [
            "永远保持锋利 — 钝凿是危险的",
            "打眼时分层下凿，每层2-3mm，勿贪深",
            "卯眼四壁要垂直 — 用角尺反复检查",
            "凿子不用时插在凿架上，刃口绝不碰硬物",
        ],
    },
    "台锯": {
        "title": "台锯 (Table Saw)",
        "icon": "⚙️",
        "difficulty": 3,
        "difficulty_label": "★★★☆☆ (操作) / ★★★★★ (安全要求)",
        "summary": "木工房的「心脏」。纵切、横切、斜切、开槽皆可，精度与效率的核心。也是最危险的木工机械。",
        "categories": [
            {"name": "台面式(Jobsite)", "desc": "便携轻便，适合现场作业"},
            {"name": "承包商级(Contractor)", "desc": "铸铁台面，家用黄金选择"},
            {"name": "柜式(Cabinet)", "desc": "重铸铁+大功率，专业级"},
        ],
        "safety": [
            "⚠️ 手指绝不靠近锯片10cm内 — 用推把/推块！",
            "劈刀(Riving Knife)永远在位 — 防反弹！",
            "护罩保持正常工作状态",
            "不戴手套操作台锯 — 卷入风险！",
            "站在锯片侧面 — 远离反弹弹道线",
        ],
        "selection": [
            "锯片10寸(250mm)家用黄金尺寸",
            "靠山精度 > 电机功率 — 靠山不准一切白费",
            "铸铁台面 > 铝台面(减振)",
            "必配推把(Push Stick)+ 横切推台(Crosscut Sled)",
        ],
        "tips": [
            "新锯片到手先做5切测试检查方正度",
            "推把两个以上：一个推料、一个辅助侧压",
            "从不站在锯片正后方 — 反弹弹道上",
        ],
    },
}

# 综合主题的数据更精简
GENERAL_TOPICS = {
    "木材": {
        "title": "木材知识大全",
        "icon": "🌳",
        "sections": [
            ("硬木 vs 软木", "硬木来自落叶阔叶树(橡木/胡桃木/樱桃木)，通常密度大纹理丰富；软木来自针叶树(松木/杉木)，通常轻软易加工。注意：硬度≠硬木分类，轻木(Balsa)是硬木但极软。"),
            ("选材原则", "1.含水率8-12% 2.同批木材纹理匹配 3.避开裂/节疤/虫眼 4.顺纹强度>横纹 5.购后适应环境1-2周"),
            ("入门推荐木材", "松木(便宜练手) → 红橡/白蜡木(性价比进阶) → 黑胡桃/樱桃木(高阶精美)"),
        ],
    },
    "安全": {
        "title": "木工安全规范",
        "icon": "🛡️",
        "sections": [
            ("PPE黄金四件", "1.安全眼镜(必戴) 2.听力保护(>85dB) 3.防尘口罩(N95+) 4.工作围裙(防卷入)"),
            ("机械安全铁律", "绝不徒手靠近旋转部件10cm内 / 护罩永不拆除 / 断电换刀 / 不穿宽松衣物 / 不疲劳操作"),
            ("粉尘控制", "集尘器连大设备 → 吸尘器配手持工具 → 空气净化器循环过滤 → 打磨必戴口罩"),
        ],
    },
    "涂装": {
        "title": "木工表面处理",
        "icon": "🎨",
        "sections": [
            ("打磨递进", "80#→120#→180#→220#→320# 逐级递进，不可跳目！顺木纹方向打磨。"),
            ("涂装方式对比", "木蜡油(渗透型/环保) | 清漆(成膜型/最耐久) | 虫胶(传统天然/易修复) | 大漆(中式传统/极复杂)"),
            ("标准涂装流程", "打磨→除尘→涂装→干燥→轻磨→除尘→涂装(重复3-5道)→最终抛光"),
        ],
    },
    "入门": {
        "title": "木工入门指南",
        "icon": "🚪",
        "sections": [
            ("零基础入门路径", "1.买一套入门工具(约500-1000元) 2.先做砧板练打磨涂装 3.再做置物架练测量组装 4.然后做边桌练基本榫接 5.最后挑战手工燕尾榫"),
            ("首批工具清单(预算版)", "日式双面锯+中式刨(短+长)+凿套装(4把)+角尺+划线器+F夹×4+磨石套装+木工锤"),
            ("第一个项目推荐", "实木砧板 — 只需打磨和涂装，2-3小时完成，成就感爆棚"),
        ],
    },
    "项目": {
        "title": "木工项目案例库",
        "icon": "📐",
        "sections": [
            ("入门项目(2-5h)", "砧板 → 置物架 → 调料架 → 花架 → 挂衣架"),
            ("进阶项目(10-35h)", "书桌 → 餐椅 → 鞋柜 → 六斗柜 → 床架"),
            ("高级项目(30-80h)", "明式圈椅 → 八仙桌 → 手工燕尾工具柜 → 明式书柜"),
            ("通用制作流程", "设计→选材→备料→加工→组装→打磨→涂装→五金安装"),
        ],
    },
    "机械": {
        "title": "木工机械设备指南",
        "icon": "⚙️",
        "sections": [
            ("设备优先级", "P0台锯(核心) → P1修边机+手电钻 → P2压刨+带锯 → P3平刨+台钻"),
            ("台锯选购", "10寸锯片/铸铁台面/靠山精度优先/2000-4000元家用入门"),
            ("安全第一", "集尘系统+推把推块+劈刀护罩=安全三件套"),
        ],
    },
}

# ── HTML 模板 ─────────────────────────────────────────────────

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - 木工大师</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #f5f0e8; color: #3e2723; line-height:1.7; }}
.header {{ background: linear-gradient(135deg, #5d4037, #8d6e63); color: #fff; padding: 40px 24px; text-align: center; }}
.header .icon {{ font-size: 64px; display:block; margin-bottom: 12px; }}
.header h1 {{ font-size: 2.4em; margin-bottom: 8px; }}
.header .alias {{ font-size: 1.1em; opacity: 0.85; }}
.header .summary {{ font-size: 1.05em; margin-top: 16px; max-width: 700px; margin-left:auto; margin-right:auto; }}
.container {{ max-width: 960px; margin: 0 auto; padding: 32px 20px; }}
.card {{ background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 24px; overflow: hidden; }}
.card-header {{ background: #efebe9; padding: 16px 24px; font-weight: 700; font-size: 1.15em; border-left: 4px solid #8d6e63; }}
.card-body {{ padding: 20px 24px; }}
.difficulty {{ display:inline-flex; align-items:center; gap:8px; padding:6px 16px; border-radius: 20px; font-weight:600; font-size:0.95em; }}
.diff-1, .diff-2 {{ background:#e8f5e9; color:#2e7d32; }}
.diff-3 {{ background:#fff3e0; color:#e65100; }}
.diff-4, .diff-5 {{ background:#fce4ec; color:#c62828; }}
.tags {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }}
.tag {{ background:#d7ccc8; color:#4e342e; padding:4px 12px; border-radius: 14px; font-size:0.85em; }}
.step {{ padding: 10px 0; border-bottom: 1px dashed #e0e0e0; font-size: 0.95em; }}
.step:last-child {{ border-bottom: none; }}
.step-num {{ color:#8d6e63; font-weight:700; margin-right:8px; }}
.tip {{ background: #fff8e1; border-left: 4px solid #ffc107; padding: 12px 16px; margin: 8px 0; border-radius: 0 8px 8px 0; }}
.tool-list {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.tool-chip {{ background: #efebe9; border: 1px solid #bcaaa4; padding: 4px 12px; border-radius: 6px; font-size:0.9em; }}
.safety {{ background: #ffebee; border-left: 4px solid #e53935; padding: 12px 16px; margin: 8px 0; border-radius: 0 8px 8px 0; }}
.section-title {{ font-weight: 700; color: #5d4037; font-size: 1.05em; margin: 16px 0 8px 0; }}
table {{ width:100%; border-collapse:collapse; margin:8px 0; }}
th {{ background:#5d4037; color:#fff; padding:8px 12px; text-align:left; font-weight:600; }}
td {{ padding:8px 12px; border-bottom:1px solid #e0e0e0; }}
tr:hover {{ background:#f5f5f5; }}
.footer {{ text-align:center; padding: 24px; color: #8d6e63; font-size: 0.85em; opacity:0.7; }}
a {{ color: #5d4037; }}
</style>
</head>
<body>

<div class="header">
  <span class="icon">{icon}</span>
  <h1>{title}</h1>
  <div class="alias">{alias}</div>
  <div class="summary">{summary}</div>
</div>

<div class="container">
{content}
</div>

<div class="footer">
  木工大师 · AI 木工制作指南<br>
  生成时间: {timestamp} · 安全第一，享受木作 🪵
</div>

</body>
</html>"""


# ── 生成函数 ──────────────────────────────────────────────────

def make_detail_report(topic_key: str) -> str:
    """生成单个主题的详细报告"""
    data = KNOWLEDGE_DATA[topic_key]
    
    cards = []
    
    # 难度卡片
    diff_class = "diff-1" if data["difficulty"] <= 2 else ("diff-3" if data["difficulty"] == 3 else "diff-4")
    cards.append(f"""<div class="card">
    <div class="card-header">📊 基本信息</div>
    <div class="card-body">
    <p><strong>难度等级：</strong><span class="difficulty {diff_class}">{data['difficulty_label']}</span></p>
    <p style="margin-top:12px"><strong>适用场景：</strong>{" / ".join(data.get('applications', data.get('categories', [c['name'] for c in data['categories']]))[:5])}</p>
    </div>
    </div>""")
    
    # 分类卡片
    if "categories" in data and data["categories"]:
        rows = ""
        for c in data["categories"]:
            rows += f"<tr><td><strong>{c['name']}</strong></td><td>{c['desc']}</td></tr>"
        cards.append(f"""<div class="card">
    <div class="card-header">📂 分类与变体</div>
    <div class="card-body"><table><tr><th>类型</th><th>说明</th></tr>{rows}</table></div>
    </div>""")
    
    # 工具卡片
    if "tools" in data:
        chips = "".join(f'<span class="tool-chip">{t}</span>' for t in data["tools"])
        cards.append(f"""<div class="card">
    <div class="card-header">🛠️ 所需工具</div>
    <div class="card-body"><div class="tool-list">{chips}</div></div>
    </div>""")
    
    # 步骤卡片
    if "steps" in data:
        steps_html = "".join(f'<div class="step"><span class="step-num">{i+1}.</span>{s.replace(f"{i+1}. ", "")}</div>' for i, s in enumerate(data["steps"]))
        cards.append(f"""<div class="card">
    <div class="card-header">📋 制作步骤</div>
    <div class="card-body">{steps_html}</div>
    </div>""")
    
    # 精度要求
    if "tolerance" in data:
        cards.append(f"""<div class="card">
    <div class="card-header">📏 精度要求</div>
    <div class="card-body"><p style="font-size:1.2em; font-weight:600; color:#5d4037;">{data['tolerance']}</p></div>
    </div>""")
    
    # 安全须知（针对机械类）
    if "safety" in data:
        safety_html = "".join(f"<div style='margin:4px 0'>{s}</div>" for s in data["safety"])
        cards.append(f"""<div class="card">
    <div class="card-header" style="border-left-color:#e53935;">⚠️ 安全须知</div>
    <div class="card-body"><div class="safety">{safety_html}</div></div>
    </div>""")
    
    # 选购建议（针对机械类）
    if "selection" in data:
        sel_html = "".join(f"<div style='margin:4px 0'>• {s}</div>" for s in data["selection"])
        cards.append(f"""<div class="card">
    <div class="card-header">🛒 选购建议</div>
    <div class="card-body">{sel_html}</div>
    </div>""")
    
    # 技巧提示
    if "tips" in data:
        tips_html = "".join(f'<div class="tip">💡 {t}</div>' for t in data["tips"])
        cards.append(f"""<div class="card">
    <div class="card-header">💡 技巧与提示</div>
    <div class="card-body">{tips_html}</div>
    </div>""")
    
    content = "".join(cards)
    return HTML_TEMPLATE.format(
        title=data["title"],
        icon=data["icon"],
        alias=data.get("alias", ""),
        summary=data.get("summary", ""),
        content=content,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )


def make_general_report(topic_key: str) -> str:
    """生成综合主题报告"""
    data = GENERAL_TOPICS[topic_key]
    
    cards = []
    for section_title, section_text in data["sections"]:
        # Convert newlines to HTML paragraphs
        text_html = "".join(f"<p>{line}</p>" for line in section_text.split("\n") if line.strip())
        cards.append(f"""<div class="card">
    <div class="card-header">{section_title}</div>
    <div class="card-body">{text_html}</div>
    </div>""")
    
    content = "".join(cards)
    return HTML_TEMPLATE.format(
        title=data["title"],
        icon=data["icon"],
        alias="",
        summary="",
        content=content,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )


def make_full_index() -> str:
    """生成完整知识索引"""
    items = []
    for key, data in KNOWLEDGE_DATA.items():
        diff_class = "diff-1" if data["difficulty"] <= 2 else ("diff-3" if data["difficulty"] == 3 else "diff-4")
        items.append(f"""<tr>
    <td>{data['icon']}</td>
    <td><strong>{data['title']}</strong></td>
    <td>{data.get('alias', '')}</td>
    <td><span class="difficulty {diff_class}">{data['difficulty_label']}</span></td>
    </tr>""")
    
    for key, data in GENERAL_TOPICS.items():
        items.append(f"""<tr>
    <td>{data['icon']}</td>
    <td><strong>{data['title']}</strong></td>
    <td>综合指南</td>
    <td><span class="difficulty diff-1">全等级</span></td>
    </tr>""")
    
    rows = "".join(items)
    content = f"""<div class="card">
    <div class="card-header">📚 知识模块索引</div>
    <div class="card-body">
    <table><tr><th></th><th>主题</th><th>别名/分类</th><th>难度</th></tr>{rows}</table>
    </div>
    </div>
    
    <div class="card">
    <div class="card-header">🚀 快速导航</div>
    <div class="card-body">
    <p>在对话中输入以下任意关键词获取详细报告：</p>
    <div class="tags" style="margin-top:12px">
    <span class="tag">燕尾榫</span><span class="tag">指接榫</span><span class="tag">粽角榫</span>
    <span class="tag">方材丁字接合</span><span class="tag">手刨</span><span class="tag">手锯</span>
    <span class="tag">凿子</span><span class="tag">台锯</span><span class="tag">木材</span>
    <span class="tag">安全</span><span class="tag">涂装</span><span class="tag">入门</span>
    <span class="tag">项目</span><span class="tag">机械</span>
    </div>
    </div>
    </div>"""
    
    return HTML_TEMPLATE.format(
        title="木工大师 · 知识索引",
        icon="🪵",
        alias="AI 木工制作指南",
        summary="榫卯结构 / 手工具 / 木工机械 / 木材知识 / 安全规范 / 表面处理 / 项目案例",
        content=content,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )


# ── 主入口 ────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        # 默认生成索引
        html = make_full_index()
        output_path = "woodworking_index.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(json.dumps({"status": "ok", "file": output_path, "type": "index"}))
        sys.exit(0)
    
    mode = sys.argv[1]
    # 输出文件路径: --output <path> 或默认 workbuddy_report.html
    output_path = "woodworking_report.html"
    args = sys.argv[2:]
    if "--output" in args:
        idx = args.index("--output")
        output_path = args[idx + 1]
        args = [a for i, a in enumerate(args) if i not in (idx, idx+1)]
    
    topic = args[0] if args else ""
    
    if mode == "--index":
        html = make_full_index()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(json.dumps({"status": "ok", "file": output_path, "type": "index"}))
    
    elif mode == "--detail":
        if topic in KNOWLEDGE_DATA:
            html = make_detail_report(topic)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(json.dumps({"status": "ok", "file": output_path, "type": "detail", "topic": topic}))
        else:
            print(json.dumps({"status": "error", "message": f"未知主题: {topic}", "available": list(KNOWLEDGE_DATA.keys())}))
            sys.exit(1)
    
    elif mode == "--general":
        if topic in GENERAL_TOPICS:
            html = make_general_report(topic)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(json.dumps({"status": "ok", "file": output_path, "type": "general", "topic": topic}))
        else:
            print(json.dumps({"status": "error", "message": f"未知综合主题: {topic}", "available": list(GENERAL_TOPICS.keys())}))
            sys.exit(1)
    
    elif mode == "--topics":
        detail = list(KNOWLEDGE_DATA.keys())
        general = list(GENERAL_TOPICS.keys())
        print(json.dumps({"detail": detail, "general": general}))
        sys.exit(0)
    
    else:
        print(json.dumps({"status": "error", "message": f"未知模式: {mode}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
