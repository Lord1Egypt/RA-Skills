#!/usr/bin/env python3
"""旅行保险聪明买 - 智能旅行保险推荐与理赔指南"""

import json

# ============================================================
# 知识库：旅行保险数据库
# ============================================================

# 目的地风险等级与保险要求
DESTINATION_PROFILES = {
    # 申根区 - 强制3万欧元医疗保额
    "申根": {"risk": "中", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根签证强制要求3万欧元(约30万CNY)以上医疗保障"},
    "法国": {"risk": "中", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "德国": {"risk": "中", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "意大利": {"risk": "中", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "西班牙": {"risk": "中", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "瑞士": {"risk": "中", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "荷兰": {"risk": "中", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "希腊": {"risk": "中", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "奥地利": {"risk": "中", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "瑞典": {"risk": "低", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "挪威": {"risk": "低", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "芬兰": {"risk": "低", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "丹麦": {"risk": "低", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "葡萄牙": {"risk": "低", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "捷克": {"risk": "低", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "匈牙利": {"risk": "低", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    "波兰": {"risk": "低", "medical_min": 300000, "currency": "CNY", "required": True, "note": "申根区，必须满足3万欧元医疗保额"},
    # 东南亚 - 医疗水平参差，传染病风险
    "泰国": {"risk": "中", "medical_min": 200000, "currency": "CNY", "required": False, "note": "登革热等热带传染病风险，建议含传染病保障"},
    "越南": {"risk": "中", "medical_min": 200000, "currency": "CNY", "required": False, "note": "医疗条件有限，建议含紧急医疗转运"},
    "柬埔寨": {"risk": "高", "medical_min": 300000, "currency": "CNY", "required": False, "note": "医疗条件较差，必须含紧急医疗转运"},
    "缅甸": {"risk": "高", "medical_min": 300000, "currency": "CNY", "required": False, "note": "医疗条件差，强烈建议含紧急医疗转运"},
    "印尼": {"risk": "中", "medical_min": 200000, "currency": "CNY", "required": False, "note": "巴厘岛等热门地区医疗条件尚可，偏远地区差"},
    "菲律宾": {"risk": "中", "medical_min": 200000, "currency": "CNY", "required": False, "note": "台风多，建议含行程变更保障"},
    "马来西亚": {"risk": "低", "medical_min": 150000, "currency": "CNY", "required": False, "note": "医疗条件较好，基础保障即可"},
    "新加坡": {"risk": "低", "medical_min": 200000, "currency": "CNY", "required": False, "note": "医疗费用高，保额建议充足"},
    # 日韩
    "日本": {"risk": "低", "medical_min": 200000, "currency": "CNY", "required": False, "note": "医疗费用较高，地震多发，建议含自然灾害保障"},
    "韩国": {"risk": "低", "medical_min": 150000, "currency": "CNY", "required": False, "note": "医疗条件好，基础保障即可"},
    # 北美 - 医疗费用极高
    "美国": {"risk": "高", "medical_min": 500000, "currency": "CNY", "required": False, "note": "医疗费用全球最高，一次急诊可能数万美元，保额务必充足"},
    "加拿大": {"risk": "中", "medical_min": 300000, "currency": "CNY", "required": False, "note": "医疗费用高，建议充足保额"},
    # 大洋洲
    "澳大利亚": {"risk": "低", "medical_min": 200000, "currency": "CNY", "required": False, "note": "医疗费用较高，建议含户外活动保障"},
    "新西兰": {"risk": "低", "medical_min": 200000, "currency": "CNY", "required": False, "note": "户外运动天堂，如计划蹦极/跳伞需加购高风险运动保障"},
    # 中东
    "阿联酋": {"risk": "低", "medical_min": 200000, "currency": "CNY", "required": False, "note": "医疗费用高，建议充足保额"},
    "沙特": {"risk": "中", "medical_min": 200000, "currency": "CNY", "required": True, "note": "朝觐签证强制要求医疗保险"},
    # 非洲
    "埃及": {"risk": "高", "medical_min": 300000, "currency": "CNY", "required": False, "note": "医疗条件差，必须含紧急医疗转运"},
    "肯尼亚": {"risk": "高", "medical_min": 300000, "currency": "CNY", "required": False, "note": "黄热病等传染病风险，建议含传染病保障"},
    "南非": {"risk": "中", "medical_min": 200000, "currency": "CNY", "required": False, "note": "治安风险较高，建议含个人财物保障"},
    "摩洛哥": {"risk": "中", "medical_min": 200000, "currency": "CNY", "required": False, "note": "医疗条件一般，建议含紧急医疗转运"},
    # 南美
    "巴西": {"risk": "高", "medical_min": 300000, "currency": "CNY", "required": False, "note": "黄热病/登革热风险，治安需注意"},
    "阿根廷": {"risk": "中", "medical_min": 200000, "currency": "CNY", "required": False, "note": "医疗条件尚可，建议含财物保障"},
    # 国内
    "国内": {"risk": "低", "medical_min": 50000, "currency": "CNY", "required": False, "note": "医保覆盖，旅行险主要保意外和行程变更"},
    "西藏": {"risk": "中", "medical_min": 100000, "currency": "CNY", "required": False, "note": "高原反应风险，建议含高原病保障"},
    "新疆": {"risk": "低", "medical_min": 50000, "currency": "CNY", "required": False, "note": "距离远，建议含航班延误和行程取消保障"},
}

# 险种数据库
INSURANCE_TYPES = {
    "medical": {
        "name": "旅行医疗保险",
        "core": True,
        "desc": "保障旅行期间的意外伤害和突发疾病的医疗费用，含门诊和住院",
        "key_points": [
            "覆盖意外伤害+突发疾病（非既往症）",
            "含紧急医疗转运/送返",
            "门诊和住院均需覆盖",
            "注意免赔额（通常0-500元）"
        ],
        "coverage_range": "5万-100万",
        "price_range": "5-80元/天",
    },
    "flight_delay": {
        "name": "航班延误/取消险",
        "core": False,
        "desc": "航班延误或取消时获得赔偿，通常延误2-4小时起赔",
        "key_points": [
            "延误起赔时间：2-6小时不等",
            "取消和延误赔付标准不同",
            "部分产品需航班确认延误后自动理赔",
            "天气原因导致的延误是否赔付看条款"
        ],
        "coverage_range": "200-1000元/次",
        "price_range": "5-30元/次",
    },
    "baggage": {
        "name": "行李延误/丢失险",
        "core": False,
        "desc": "行李延误或丢失时获得赔偿，含随身物品和托运行李",
        "key_points": [
            "延误通常6-8小时起赔",
            "丢失需航空公司出具丢失证明",
            "贵重物品（珠宝、电子设备）通常限额赔付",
            "现金和有价证券一般不在保障范围内"
        ],
        "coverage_range": "500-5000元",
        "price_range": "3-20元/次",
    },
    "trip_cancellation": {
        "name": "行程取消/变更险",
        "core": False,
        "desc": "因特定原因导致行程取消或变更时的经济损失赔偿",
        "key_points": [
            "通常只覆盖"不可抗力"原因",
            "个人主观原因取消一般不赔",
            "需提供取消证明材料",
            "部分产品含隔离/滞留保障(疫情期间常见)"
        ],
        "coverage_range": "机票+酒店实际损失",
        "price_range": "10-50元/次",
    },
    "personal_liability": {
        "name": "个人责任险",
        "core": False,
        "desc": "因意外造成第三方人身伤害或财产损失的赔偿责任",
        "key_points": [
            "滑雪/潜水等运动撞伤他人可赔",
            "损坏酒店物品可赔",
            "故意行为不赔",
            "保额建议不低于50万(出境游)"
        ],
        "coverage_range": "10万-100万",
        "price_range": "3-15元/次",
    },
    "adventure_sport": {
        "name": "高风险运动保障",
        "core": False,
        "desc": "扩展覆盖潜水、滑雪、蹦极、跳伞等高风险运动",
        "key_points": [
            "普通旅行险通常排除高风险运动",
            "必须单独加购或在投保时勾选",
            "各产品覆盖的运动种类不同，仔细核对",
            "专业级运动（如深潜>30米）可能需专用保险"
        ],
        "coverage_range": "同医疗保额",
        "price_range": "10-50元/次",
    },
    "pre_existing": {
        "name": "既往症保障",
        "core": False,
        "desc": "覆盖投保前已存在的疾病急性发作（非维持治疗）",
        "key_points": [
            "绝大多数旅行险不保既往症",
            "少数产品提供"既往症急性发作"保障",
            "需如实告知健康状况，否则理赔可能被拒",
            "慢性病患者务必关注此项"
        ],
        "coverage_range": "1万-10万",
        "price_range": "加费20%-50%",
    },
    "emergency_rescue": {
        "name": "紧急救援服务",
        "core": True,
        "desc": "24小时紧急救援热线、医疗转运、遗体送返等服务",
        "key_points": [
            "出境游最重要的保障之一",
            "含医疗转运回国的费用（可能数万至数十万）",
            "好的救援服务比高保额更实用",
            "关注救援公司口碑：国际SOS、安盛援助等"
        ],
        "coverage_range": "实际费用",
        "price_range": "通常包含在医疗险中",
    },
}

# 条款概念解读数据库
COVERAGE_CONCEPTS = {
    "免赔额": {
        "alias": ["自付额", "deductible", "起赔线"],
        "explain": "免赔额就是"保险不赔的那部分钱"。比如免赔额500元，你看病花了2000元，保险只赔1500元（2000-500）。",
        "tips": [
            "优先选0免赔额的产品，虽然贵一点但理赔体验好",
            "部分产品用"次免赔额"（每次就诊都扣），部分用"年度免赔额"（全年累计扣一次）",
            "航班延误险的"起赔时间"本质也是免赔额",
        ],
        "example": "小明在泰国食物中毒，门诊花费3000泰铢(约600元)。如果免赔额500元，则赔付100元；如果0免赔额，则赔付600元。"
    },
    "等待期": {
        "alias": ["观察期", "waiting period"],
        "explain": "等待期是投保后一段时间内，特定疾病不赔。主要是防止带病投保。",
        "tips": [
            "意外伤害一般无等待期（生效即赔）",
            "疾病医疗通常有等待期（7-90天不等）",
            "旅行险的等待期通常较短，但仍需确认",
            "等待期内发病不赔，等待期后发病才赔"
        ],
        "example": "小张投保旅行险后第3天突发阑尾炎。如果等待期为7天，则不赔；如果无等待期或已过等待期，则可赔。"
    },
    "除外责任": {
        "alias": ["不赔的情况", "exclusion", "免责条款"],
        "explain": "除外责任是保险明确不赔的情况，是拒赔的最常见原因。",
        "tips": [
            "最常见除外：既往症、酒驾、自伤、战争、核辐射",
            "高风险运动通常是除外——除非单独加购",
            "美容、体检、心理咨询等非治疗性费用不赔",
            "既往症是拒赔重灾区，务必如实告知"
        ],
        "example": "小李去巴厘岛潜水受伤，但他的旅行险将潜水列为除外责任，结果不赔。如果他加购了高风险运动保障，就可以赔。"
    },
    "既往症": {
        "alias": ["已有疾病", "pre-existing condition", "基础病"],
        "explain": "既往症是投保前已确诊或应知的疾病，绝大多数旅行险不赔。",
        "tips": [
            "高血压、糖尿病、心脏病等慢性病都是既往症",
            "即使停药了，只要之前确诊过，仍是既往症",
            "少数产品保"既往症急性发作"，但条件严格",
            "如实告知健康状况，隐瞒会导致整单拒赔"
        ],
        "example": "王阿姨有高血压，投保时未告知。旅行中因高血压引发脑溢血，保险公司调查后拒赔，且退还保费解除合同。"
    },
    "保额": {
        "alias": ["保险金额", "coverage", "赔偿限额"],
        "explain": "保额是保险最多赔多少钱。不是花了多少就赔多少，而是有上限。",
        "tips": [
            "出境游医疗保额建议至少30万CNY（美国/加拿大建议50万+）",
            "保额≠实际赔付，实际赔付≤实际花费且≤保额",
            "注意分项限额：比如医疗总保额50万，但门诊限5万",
            "紧急救援/送返费用通常单独计算保额"
        ],
        "example": "小赵在美国突发急性阑尾炎，手术花费8万美元(约57万CNY)。如果保额50万，则最多赔50万，自掏7万。"
    },
    "保险期间": {
        "alias": ["保障期", "coverage period", "有效期"],
        "explain": "保险期间是保险生效的时间范围，必须覆盖整个出行期间。",
        "tips": [
            "从出发日到回国日，建议前后各多加1-2天",
            "注意时差：保险起止时间按北京时间还是当地时间",
            "行程延期自动顺延的条款很有用（如航班取消滞留）",
            "出境游建议保险起始时间包含出发当天"
        ],
        "example": "小陈的行程是6月1日-6月10日，保险买的是6月1日0时-6月10日24时。如果6月10日航班取消滞留到11日，没有延期条款的保险不保11日。"
    },
    "受益人": {
        "alias": ["理赔受领人", "beneficiary"],
        "explain": "受益人是出险后有权领取保险金的人，分法定和指定两种。",
        "tips": [
            "身故受益人建议指定（法定需所有继承人签字，手续复杂）",
            "医疗险受益人通常是被保险人本人",
            "为家人投保时，受益人可指定为配偶或父母",
            "旅行险的身故保额不高，但指定受益人能省很多麻烦"
        ],
        "example": "小刘出国旅行意外身故，保额50万。指定受益人是妻子，妻子凭身份证和关系证明即可领款。如果是法定受益人，需所有第一顺序继承人签字。"
    },
}

# 理赔场景数据库
CLAIM_SCENARIOS = {
    "医疗理赔": {
        "triggers": ["生病", "看病", "门诊", "住院", "急诊", "受伤", "意外伤害"],
        "steps": [
            "1️⃣ 立即拨打保险公司24小时救援热线报案",
            "2️⃣ 在保险公司指定的网络医院就诊（如有可能）",
            "3️⃣ 保留所有原始单据：挂号单、处方、发票、检查报告",
            "4️⃣ 获取医生诊断证明（中英文均可，境外需翻译公证）",
            "5️⃣ 回国后15-30天内提交理赔申请",
        ],
        "materials": [
            "理赔申请表（保险公司官网下载）",
            "护照出入境页复印件",
            "医院诊断证明",
            "医疗费用发票原件",
            "费用明细清单",
            "处方复印件（如有用药）",
            "检查报告（X光/B超/化验等）",
            "银行账户信息"
        ],
        "tips": [
            "⚠️ 未经保险公司同意自行转运，转运费可能不赔",
            "⚠️ 门诊和住院的材料要求不同，住院需更完整",
            "⚠️ 境外就诊先确认是否在救援网络内",
            "💡 保留所有花费凭证，包括交通费（去医院）",
            "💡 拍照备份所有原始单据，防丢失"
        ],
        "common_rejection": [
            "既往症发作（投保前已确诊）",
            "等待期内发病",
            "非急诊的体检/美容/心理咨询",
            "酒后行为导致的伤害",
            "无法提供完整的就诊记录"
        ],
    },
    "航班延误": {
        "triggers": ["航班延误", "飞机晚点", "航班取消", "delay", "航班延误险"],
        "steps": [
            "1️⃣ 确认延误原因和时间（航空公司出具延误证明）",
            "2️⃣ 部分产品自动理赔（与航司系统对接，无需手动申请）",
            "3️⃣ 非自动理赔：保留登机牌+延误证明",
            "4️⃣ 在APP或官网提交理赔申请",
        ],
        "materials": [
            "登机牌原件或电子登机牌截图",
            "航班延误证明（航空公司柜台/APP开具）",
            "护照信息页",
            "理赔申请表"
        ],
        "tips": [
            "⚠️ 延误起赔时间要看清：2h/3h/4h/6h各不同",
            "⚠️ 取消≠延误，赔付标准不同",
            "💡 部分产品"延误2小时起赔200元，每多1小时加100"",
            "💡 航空公司已安排替代航班可能影响赔付"
        ],
        "common_rejection": [
            "延误时间未达到起赔标准",
            "无法提供延误证明",
            "非承保航班（如中转段不在保障内）",
            "已获航空公司赔偿（部分产品不允许重复索赔）"
        ],
    },
    "行李丢失": {
        "triggers": ["行李丢失", "行李延误", "行李损坏", "行李没到"],
        "steps": [
            "1️⃣ 立即向航空公司报失，获取行李事故报告(PIR)",
            "2️⃣ 保留行李牌和登机牌",
            "3️⃣ 行李延误：购买必要生活用品并保留发票",
            "4️⃣ 行李丢失：21天后航空公司确认丢失，再申请理赔",
            "5️⃣ 向保险公司提交理赔申请"
        ],
        "materials": [
            "行李事故报告(PIR)原件",
            "登机牌和行李牌",
            "购买必要用品的发票（延误场景）",
            "行李内物品清单及价值证明",
            "航空公司确认丢失的书面文件",
            "护照信息页",
            "理赔申请表"
        ],
        "tips": [
            "⚠️ 贵重物品（珠宝、电子产品）有单独限额，通常很低",
            "⚠️ 现金和有价证券不在保障范围内",
            "💡 拍照记录行李外观和内物，方便证明",
            "💡 延误和丢失是两个不同理赔，材料要求不同"
        ],
        "common_rejection": [
            "无法提供PIR报告",
            "贵重物品超过分项限额",
            "现金/证券损失（不在保障范围）",
            "行李未实际丢失（只是延误，21天内找回）"
        ],
    },
    "行程取消": {
        "triggers": ["行程取消", "旅行取消", "取消行程", "去不了", "trip cancellation"],
        "steps": [
            "1️⃣ 确认取消原因是否在保障范围内",
            "2️⃣ 收集取消证明材料",
            "3️⃣ 尽快通知航空公司和酒店取消预订",
            "4️⃣ 保留所有退改凭证和损失证明",
            "5️⃣ 向保险公司提交理赔申请"
        ],
        "materials": [
            "行程取消的书面证明（如医生证明、天气预警、罢工公告）",
            "机票/酒店退改凭证",
            "未退款的发票和付款凭证",
            "损失金额的明细计算",
            "护照信息页",
            "理赔申请表"
        ],
        "tips": [
            "⚠️ 个人主观原因取消（不想去了、改主意了）不赔",
            "⚠️ 只有保单约定的"特定原因"才赔",
            "💡 常见可赔原因：本人/家属重病、直系亲属身故、自然灾害",
            "💡 航空公司已退票的部分不能再向保险索赔"
        ],
        "common_rejection": [
            "取消原因不在保障范围内",
            "无法提供取消原因的证明材料",
            "航空公司/酒店已全额退款（无实际损失）",
            "投保前已知晓可能导致取消的情况"
        ],
    },
    "个人责任": {
        "triggers": ["撞到人", "损坏物品", "赔偿", "第三方损失", "个人责任"],
        "steps": [
            "1️⃣ 立即拨打保险公司热线报案",
            "2️⃣ 不要私下承诺赔偿金额",
            "3️⃣ 收集事故证明和第三方损失证据",
            "4️⃣ 保险公司指导后续处理",
            "5️⃣ 由保险公司与第三方协商赔偿"
        ],
        "materials": [
            "事故经过书面说明",
            "第三方提出的赔偿要求",
            "损失证明（照片、评估报告）",
            "证人证言（如有）",
            "警方报告（如涉及）",
            "理赔申请表"
        ],
        "tips": [
            "⚠️ 不要私下和解，保险公司可能不认",
            "⚠️ 故意行为不赔（只保意外）",
            "💡 滑雪场撞人、酒店损坏设施是最常见场景",
            "💡 保留现场照片和对方联系方式"
        ],
        "common_rejection": [
            "故意行为导致第三方损失",
            "私下和解且保险公司不认可",
            "无法证明事故经过",
            "损失金额无法核实"
        ],
    },
}

# 保险公司产品参考
INSURANCE_PROVIDERS = {
    "平安": {
        "products": ["平安东南亚旅行险", "平安申根旅行险", "平安全球旅行险"],
        "features": "覆盖范围广，救援服务为国际SOS，理赔效率较高",
        "url": "https://health.pingan.com/lvyouxian/"
    },
    "人保": {
        "products": ["人保境外旅行险", "人保国内旅行险"],
        "features": "央企品牌，网点多，线下理赔方便",
        "url": "https://www.picc.com/"
    },
    "太平洋": {
        "products": ["太保境外旅行险", "太保申根旅行险"],
        "features": "申根签证通过率高，含紧急医疗转运",
        "url": "https://www.cpic.com.cn/"
    },
    "安联": {
        "products": ["安联环球旅行险", "安联申根旅行险"],
        "features": "全球救援网络最强（德国安联总部），适合长途出境游",
        "url": "https://www.allianz.com.cn/"
    },
    "美亚": {
        "products": ["美亚万国游踪", "美亚畅游神州"],
        "features": "AIG旗下，境外理赔经验丰富，适合欧美游",
        "url": "https://www.aig.com.cn/"
    },
    "史带": {
        "products": ["史带境外旅行险"],
        "features": "含既往症急性发作保障，对中老年友好",
        "url": "https://www.starrchina.cn/"
    },
}

# 购买渠道链接
PURCHASE_CHANNELS = {
    "飞猪": {
        "desc": "飞猪旅行保险频道，支持支付宝支付，出单快",
        "search_url": "https://www.fliggy.com/insurance/list.htm",
        "tips": "搜索"旅游保险"即可看到各公司产品"
    },
    "支付宝·蚂蚁保": {
        "desc": "支付宝内置保险平台，支持月缴和年缴",
        "search_url": "https://render.alipay.com/p/s/insurance-mall/ins-mall-home/index.html",
        "tips": "在支付宝搜索"旅行险"即可"
    },
    "微信·微保": {
        "desc": "微信内置保险平台，操作便捷",
        "search_url": "https://ab.weixin.qq.com/",
        "tips": "在微信搜索"微保"→旅行险"
    },
    "保险公司官网": {
        "desc": "直接在保险公司官网购买，产品最全",
        "search_url": None,
        "tips": "选择目标保险公司官网直接投保"
    },
}


# ============================================================
# 工具1：recommend_insurance - 场景化保险推荐
# ============================================================

def recommend_insurance(destination: str, trip_type: str = "休闲", days: int = 7,
                        people: int = 1, has_elderly: bool = False, has_children: bool = False,
                        activities: str = "") -> str:
    """
    根据出行信息推荐旅行保险方案。

    Args:
        destination: 目的地（国家/地区名或"国内"）
        trip_type: 出行类型（休闲/商务/探亲/留学）
        days: 出行天数
        people: 出行人数
        has_elderly: 是否有60岁以上老人
        has_children: 是否有未成年人
        activities: 特殊活动（滑雪/潜水/跳伞/蹦极等）
    """

    # 匹配目的地档案
    dest_profile = _match_destination(destination)
    is_domestic = destination in ["国内", "中国"] or dest_profile is None

    # 构建推荐方案
    result_parts = []
    result_parts.append("🛡️ 旅行保险推荐方案\n")

    # 出行信息概要
    dest_name = destination if is_domestic else destination
    risk_level = dest_profile.get("risk", "低") if dest_profile else "低"
    result_parts.append(f"📍 出行信息：{dest_name} · {days}天 · {people}人 · {trip_type}行")
    result_parts.append(f"🎯 风险等级：{risk_level}\n")

    # 核心保障（必买）
    result_parts.append("【核心保障】（必买）\n")

    # 医疗保障
    medical_min = dest_profile.get("medical_min", 50000) if dest_profile else 50000
    if is_domestic:
        medical_recommend = "5万-20万"
        medical_price = "3-10元/天"
    else:
        if medical_min >= 300000:
            medical_recommend = f"{medical_min//10000}万+"
            medical_price = "20-80元/天"
        elif medical_min >= 200000:
            medical_recommend = "20万-50万"
            medical_price = "15-50元/天"
        else:
            medical_recommend = "10万-30万"
            medical_price = "10-30元/天"

    result_parts.append(f"- 险种：旅行医疗保险 | 保额建议：{medical_recommend} | 保费参考：{medical_price}")
    result_parts.append(f"  保障范围：意外伤害+突发疾病医疗+紧急医疗转运/送返")

    # 紧急救援（出境游）
    if not is_domestic:
        result_parts.append(f"- 险种：紧急救援服务 | 保额建议：实际费用 | 保费参考：通常含在医疗险中")
        result_parts.append(f"  保障范围：24小时救援热线+医疗转运回国+遗体送返")

    # 申根特殊要求
    if dest_profile and dest_profile.get("required"):
        result_parts.append(f"\n⚠️ 签证要求：{dest_profile.get('note', '')}")

    # 美国特殊提醒
    if destination in ["美国", "加拿大"]:
        result_parts.append(f"\n⚠️ 医疗费用极高：{dest_profile.get('note', '建议50万+保额')}")

    # 增强保障（建议买）
    result_parts.append("\n【增强保障】（建议买）\n")

    # 航班延误/取消
    if not is_domestic or days > 3:
        result_parts.append(f"- 险种：航班延误/取消险 | 保额建议：200-1000元/次 | 保费参考：5-30元/次")
        result_parts.append(f"  适合：国际航班/中转航班/旺季出行")

    # 行李保障
    if not is_domestic:
        result_parts.append(f"- 险种：行李延误/丢失险 | 保额建议：1000-5000元 | 保费参考：3-20元/次")
        result_parts.append(f"  适合：托运行李较多/携带贵重物品")

    # 行程取消
    if not is_domestic and days > 5:
        result_parts.append(f"- 险种：行程取消/变更险 | 保额建议：覆盖机票+酒店 | 保费参考：10-50元/次")
        result_parts.append(f"  适合：提前预订了不可退改的机票酒店")

    # 个人责任
    if not is_domestic:
        result_parts.append(f"- 险种：个人责任险 | 保额建议：50万+ | 保费参考：3-15元/次")
        result_parts.append(f"  适合：出境游防止意外造成第三方损失")

    # 可选保障（按需买）
    result_parts.append("\n【可选保障】（按需买）\n")

    # 高风险运动
    high_risk_activities = ["滑雪", "潜水", "跳伞", "蹦极", "攀岩", "冲浪", "漂流", "滑翔", "跳伞", "马术", "赛车"]
    activity_list = [a.strip() for a in activities.replace("，", ",").split(",") if a.strip()]
    has_high_risk = any(a in high_risk_activities for a in activity_list)

    if has_high_risk or not is_domestic:
        matched_activities = [a for a in activity_list if a in high_risk_activities]
        act_desc = f"（您提到的{'+'.join(matched_activities)}）" if matched_activities else "（如计划参与）"
        result_parts.append(f"- 险种：高风险运动保障{act_desc} | 保额建议：同医疗保额 | 保费参考：10-50元/次")
        result_parts.append(f"  适合：计划参与滑雪/潜水/蹦极等运动")

    # 既往症
    if has_elderly:
        result_parts.append(f"- 险种：既往症急性发作保障 | 保额建议：1万-10万 | 保费参考：加费20%-50%")
        result_parts.append(f"  适合：同行有60岁以上老人，可能突发慢性病")

    # 特殊人群提示
    special_notes = []
    if has_children:
        special_notes.append("👶 未成年人医疗保额可适当降低，但意外伤害保额建议充足")
    if has_elderly:
        special_notes.append("👴 老年人注意投保年龄限制（多数产品限70-80岁），超龄可选史带等特殊产品")
    if trip_type == "留学":
        special_notes.append("🎓 留学建议购买专门的留学保险，旅行险保障期不够长")
    if trip_type == "商务":
        special_notes.append("💼 商务出行建议确认公司是否已购买团体商旅险，避免重复投保")

    # 保费预估
    if is_domestic:
        total_low = days * 3 * people
        total_high = days * 15 * people
    else:
        base_low = max(days * 10, 30) * people
        base_high = max(days * 50, 100) * people
        total_low = base_low
        total_high = base_high

    result_parts.append(f"\n💰 方案预估：{total_low}-{total_high}元（核心保障+增强保障）")

    # 购买渠道
    result_parts.append("\n🔗 购买渠道：")
    for channel, info in PURCHASE_CHANNELS.items():
        if info.get("search_url"):
            result_parts.append(f"- {channel}：{info['search_url']}")
        else:
            result_parts.append(f"- {channel}：{info['tips']}")

    # 保险公司推荐
    if not is_domestic:
        result_parts.append("\n🏢 推荐保险公司：")
        if dest_profile and dest_profile.get("risk") == "高":
            result_parts.append("- 安联（全球救援网络最强）| https://www.allianz.com.cn/")
            result_parts.append("- 美亚（境外理赔经验丰富）| https://www.aig.com.cn/")
        elif destination in ["日本", "韩国", "新加坡", "马来西亚", "泰国"]:
            result_parts.append("- 平安（覆盖广+国际SOS救援）| https://health.pingan.com/lvyouxian/")
            result_parts.append("- 安联（全球救援网络强）| https://www.allianz.com.cn/")
        else:
            result_parts.append("- 平安（覆盖广+国际SOS救援）| https://health.pingan.com/lvyouxian/")
            result_parts.append("- 太平洋（申根签证通过率高）| https://www.cpic.com.cn/")
        if has_elderly:
            result_parts.append("- 史带（含既往症急性发作保障，对中老年友好）| https://www.starrchina.cn/")

    # 投保前必看
    result_parts.append("\n⚠️ 投保前必看：")
    result_parts.append("1. 如实告知健康状况，隐瞒既往症会导致拒赔")
    result_parts.append("2. 保险期间覆盖出发到回国全程，建议前后各多加1-2天")
    if not is_domestic:
        result_parts.append("3. 记下保险公司24小时救援电话，随身携带保单号")
    if has_high_risk:
        result_parts.append("4. ⚠️ 您计划参与高风险运动，务必加购对应保障或确认已包含")
    if dest_profile and dest_profile.get("note"):
        result_parts.append(f"5. 📋 {dest_profile['note']}")

    return "\n".join(result_parts)


# ============================================================
# 工具2：explain_coverage - 条款白话解读
# ============================================================

def explain_coverage(concept: str) -> str:
    """
    白话解读旅行保险条款中的关键概念。

    Args:
        concept: 要解读的条款概念（如"免赔额""等待期""除外责任"等）
    """

    # 匹配概念
    matched = _match_concept(concept)

    if not matched:
        # 提供所有可解读的概念列表
        all_concepts = list(COVERAGE_CONCEPTS.keys())
        result = f"未找到"{concept}"的解读。以下是可解读的条款概念：\n\n"
        for c in all_concepts:
            aliases = ", ".join(COVERAGE_CONCEPTS[c]["alias"])
            result += f"- **{c}**（{aliases}）\n"
        result += "\n请告诉我您想了解哪个概念？"
        return result

    key, data = matched

    result_parts = []
    result_parts.append(f"📖 条款解读：{key}\n")
    result_parts.append(f"💡 {data['explain']}\n")

    result_parts.append("🔑 要点：")
    for i, tip in enumerate(data["tips"], 1):
        result_parts.append(f"  {i}. {tip}")

    result_parts.append(f"\n📝 举例说明：")
    result_parts.append(f"  {data['example']}")

    return "\n".join(result_parts)


# ============================================================
# 工具3：claim_guide - 理赔指南
# ============================================================

def claim_guide(scenario: str) -> str:
    """
    提供旅行保险理赔流程指引。

    Args:
        scenario: 理赔场景描述（如"航班延误""行李丢失""看病""行程取消"等）
    """

    # 匹配理赔场景
    matched = _match_claim_scenario(scenario)

    if not matched:
        # 提供所有理赔场景
        all_scenarios = list(CLAIM_SCENARIOS.keys())
        result = f"未找到"{scenario}"的理赔场景。以下是支持的理赔场景：\n\n"
        for s in all_scenarios:
            triggers = ", ".join(CLAIM_SCENARIOS[s]["triggers"][:3])
            result += f"- **{s}**（关键词：{triggers}）\n"
        result += "\n请告诉我您遇到的是哪种情况？"
        return result

    key, data = matched

    result_parts = []
    result_parts.append(f"📋 理赔指南：{key}\n")

    # 操作步骤
    result_parts.append("🔄 操作步骤：")
    for step in data["steps"]:
        result_parts.append(f"  {step}")

    # 所需材料
    result_parts.append("\n📄 所需材料：")
    for mat in data["materials"]:
        result_parts.append(f"  ☐ {mat}")

    # 注意事项
    result_parts.append("\n⚠️ 注意事项：")
    for tip in data["tips"]:
        result_parts.append(f"  {tip}")

    # 常见拒赔原因
    result_parts.append("\n🚫 常见拒赔原因：")
    for rej in data["common_rejection"]:
        result_parts.append(f"  • {rej}")

    # 通用理赔提醒
    result_parts.append("\n💡 通用理赔提醒：")
    result_parts.append("  • 拨打保险公司24小时热线报案是第一步，越早越好")
    result_parts.append("  • 所有原始单据务必保留，拍照备份")
    result_parts.append("  • 理赔时效通常为事故发生后2年内，但建议尽快申请")
    result_parts.append("  • 对理赔结果有异议可申请复议或向银保监会投诉")

    return "\n".join(result_parts)


# ============================================================
# 辅助函数
# ============================================================

def _match_destination(query: str) -> dict:
    """模糊匹配目的地档案"""
    q = query.strip()
    # 精确匹配
    if q in DESTINATION_PROFILES:
        return DESTINATION_PROFILES[q]
    # 模糊匹配
    for key, val in DESTINATION_PROFILES.items():
        if q in key or key in q:
            return val
    # 申根区关键词
    schengen_keywords = ["申根", "欧洲", "EU"]
    for kw in schengen_keywords:
        if kw in q:
            return DESTINATION_PROFILES["申根"]
    return None


def _match_concept(query: str) -> tuple:
    """模糊匹配条款概念"""
    q = query.strip().lower()
    for key, data in COVERAGE_CONCEPTS.items():
        if q == key.lower() or q in key.lower() or key.lower() in q:
            return (key, data)
        for alias in data["alias"]:
            if q == alias.lower() or q in alias.lower():
                return (key, data)
    return None


def _match_claim_scenario(query: str) -> tuple:
    """模糊匹配理赔场景"""
    q = query.strip().lower()
    for key, data in CLAIM_SCENARIOS.items():
        if q == key.lower() or q in key.lower() or key.lower() in q:
            return (key, data)
        for trigger in data["triggers"]:
            if trigger.lower() in q or q in trigger.lower():
                return (key, data)
    return None


# ============================================================
# 入口函数
# ============================================================

def main(params: dict) -> str:
    """技能入口函数"""
    tool_name = params.get("tool", "recommend_insurance")

    if tool_name == "recommend_insurance":
        return recommend_insurance(
            destination=params.get("destination", ""),
            trip_type=params.get("trip_type", "休闲"),
            days=int(params.get("days", 7)),
            people=int(params.get("people", 1)),
            has_elderly=params.get("has_elderly", False),
            has_children=params.get("has_children", False),
            activities=params.get("activities", ""),
        )
    elif tool_name == "explain_coverage":
        return explain_coverage(
            concept=params.get("concept", ""),
        )
    elif tool_name == "claim_guide":
        return claim_guide(
            scenario=params.get("scenario", ""),
        )
    else:
        return f"未知工具：{tool_name}。可用工具：recommend_insurance, explain_coverage, claim_guide"


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])
    else:
        params = {"tool": "recommend_insurance", "destination": "日本", "days": 7}
    print(main(params))
