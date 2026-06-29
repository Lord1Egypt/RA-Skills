#!/usr/bin/env python3
"""旅行紧急助手 - Travel Emergency Guide
7大紧急场景行动指南 + 各国紧急电话 + 中国驻外使领馆信息
纯知识型，零API依赖
"""
import json
import sys
from datetime import datetime

# ========== 各国/地区紧急电话数据库 ==========
EMERGENCY_NUMBERS = {
    "中国": {"police": "110", "ambulance": "120", "fire": "119", "traffic": "122"},
    "美国": {"police": "911", "ambulance": "911", "fire": "911", "note": "统一911"},
    "加拿大": {"police": "911", "ambulance": "911", "fire": "911"},
    "英国": {"police": "999", "ambulance": "999", "fire": "999", "non_emergency": "101"},
    "法国": {"police": "17", "ambulance": "15", "fire": "18", "eu_emergency": "112"},
    "德国": {"police": "110", "ambulance": "112", "fire": "112"},
    "意大利": {"police": "113", "ambulance": "118", "fire": "115", "carabinieri": "112"},
    "西班牙": {"police": "091", "ambulance": "061", "fire": "080", "eu_emergency": "112"},
    "日本": {"police": "110", "ambulance": "119", "fire": "119", "note": "报警110，消防急救119"},
    "韩国": {"police": "112", "ambulance": "119", "fire": "119"},
    "泰国": {"police": "191", "ambulance": "1669", "tourist_police": "1155", "note": "旅游警察1155可中文服务"},
    "新加坡": {"police": "999", "ambulance": "995", "fire": "995"},
    "马来西亚": {"police": "999", "ambulance": "999", "fire": "994", "tourist_police": "03-2149 6590"},
    "越南": {"police": "113", "ambulance": "115", "fire": "114"},
    "柬埔寨": {"police": "117", "ambulance": "119", "tourist_police": "012-942 484"},
    "印度尼西亚": {"police": "110", "ambulance": "118", "fire": "113"},
    "菲律宾": {"police": "117", "ambulance": "911", "fire": "117"},
    "印度": {"police": "100", "ambulance": "102", "fire": "101", "women_helpline": "1091"},
    "阿联酋": {"police": "999", "ambulance": "998", "fire": "997"},
    "土耳其": {"police": "155", "ambulance": "112", "fire": "110", "tourist_police": "0212-527 4503"},
    "俄罗斯": {"police": "102", "ambulance": "103", "fire": "101", "unified": "112"},
    "澳大利亚": {"police": "000", "ambulance": "000", "fire": "000", "note": "统一000"},
    "新西兰": {"police": "111", "ambulance": "111", "fire": "111"},
    "巴西": {"police": "190", "ambulance": "192", "fire": "193"},
    "墨西哥": {"police": "911", "ambulance": "911", "fire": "911", "tourist_police": "078"},
    "埃及": {"police": "122", "ambulance": "123", "tourist_police": "126"},
    "南非": {"police": "10111", "ambulance": "10177", "cellphone": "112"},
    "以色列": {"police": "100", "ambulance": "101", "fire": "102"},
    "瑞士": {"police": "117", "ambulance": "144", "fire": "118", "eu_emergency": "112"},
    "荷兰": {"police": "112", "ambulance": "112", "fire": "112", "non_emergency": "0900-8844"},
    "希腊": {"police": "100", "ambulance": "166", "fire": "199", "eu_emergency": "112"},
    "葡萄牙": {"police": "112", "ambulance": "112", "fire": "112"},
    "捷克": {"police": "158", "ambulance": "155", "fire": "150", "unified": "112"},
    "匈牙利": {"police": "107", "ambulance": "104", "fire": "105", "unified": "112"},
    "波兰": {"police": "112", "ambulance": "112", "fire": "112"},
    "瑞典": {"police": "112", "ambulance": "112", "fire": "112", "non_emergency": "114 14"},
    "挪威": {"police": "02800", "ambulance": "113", "fire": "110", "unified": "112"},
    "芬兰": {"police": "112", "ambulance": "112", "fire": "112"},
    "丹麦": {"police": "112", "ambulance": "112", "fire": "112", "non_emergency": "114"},
    "冰岛": {"police": "112", "ambulance": "112", "fire": "112"},
    "爱尔兰": {"police": "999", "ambulance": "999", "fire": "999", "eu_emergency": "112"},
    "奥地利": {"police": "133", "ambulance": "144", "fire": "122", "eu_emergency": "112"},
    "比利时": {"police": "101", "ambulance": "100", "fire": "100", "eu_emergency": "112"},
    "克罗地亚": {"police": "192", "ambulance": "194", "fire": "193", "eu_emergency": "112"},
    "阿根廷": {"police": "911", "ambulance": "107", "fire": "100"},
    "智利": {"police": "133", "ambulance": "131", "fire": "132"},
    "哥伦比亚": {"police": "123", "ambulance": "123", "fire": "123"},
    "秘鲁": {"police": "105", "ambulance": "116", "fire": "116"},
    "肯尼亚": {"police": "999", "ambulance": "999", "fire": "999"},
    "摩洛哥": {"police": "19", "ambulance": "15", "fire": "15", "tourist_police": "0522-206 060"},
    "尼泊尔": {"police": "100", "ambulance": "102", "tourist_police": "01-424 7041"},
    "斯里兰卡": {"police": "119", "ambulance": "110", "tourist_police": "01-242 1451"},
    "缅甸": {"police": "199", "ambulance": "192", "tourist_police": "01-252 939"},
    "老挝": {"police": "191", "ambulance": "195", "fire": "190"},
    "蒙古": {"police": "102", "ambulance": "103", "fire": "101"},
}

# ========== 中国驻外使领馆数据库（主要国家） ==========
CHINESE_EMBASSIES = {
    "美国": {
        "embassy": {
            "name": "中国驻美国大使馆",
            "address": "3505 International Place NW, Washington DC 20008",
            "phone": "+1-202-4952216",
            "duty_phone": "+1-202-4952216",
            "email": "chinaembpress_us@mfa.gov.cn",
            "consular_phone": "+1-202-8551555",
            "consular_email": "visa_us@mfa.gov.cn",
        },
        "consulates": [
            {"city": "纽约", "phone": "+1-212-2449392", "duty_phone": "+1-212-2449392"},
            {"city": "旧金山", "phone": "+1-415-8525924", "duty_phone": "+1-415-2168525"},
            {"city": "洛杉矶", "phone": "+1-213-8068088", "duty_phone": "+1-213-8068088"},
            {"city": "芝加哥", "phone": "+1-312-8059838", "duty_phone": "+1-312-8059838"},
        ]
    },
    "日本": {
        "embassy": {
            "name": "中国驻日本大使馆",
            "address": "3-4-33 Moto-Azabu, Minato-ku, Tokyo",
            "phone": "+81-3-34033380",
            "duty_phone": "+81-3-34033380",
            "email": "chinaemb_jp@mfa.gov.cn",
        },
        "consulates": [
            {"city": "大阪", "phone": "+81-6-64459481", "duty_phone": "+81-6-64459481"},
            {"city": "名古屋", "phone": "+81-52-9321098", "duty_phone": "+81-52-9321098"},
            {"city": "札幌", "phone": "+81-11-5635563", "duty_phone": "+81-11-5635563"},
            {"city": "福冈", "phone": "+81-92-7520088", "duty_phone": "+81-92-7520088"},
            {"city": "长崎", "phone": "+81-95-8493311", "duty_phone": "+81-95-8493311"},
        ]
    },
    "泰国": {
        "embassy": {
            "name": "中国驻泰国大使馆",
            "address": "57 Ratchadaphisek Rd, Bangkok 10400",
            "phone": "+66-2-2450088",
            "duty_phone": "+66-2-2457010",
            "email": "chinaemb_th@mfa.gov.cn",
        },
        "consulates": [
            {"city": "清迈", "phone": "+66-53-280380", "duty_phone": "+66-53-276125"},
            {"city": "宋卡", "phone": "+66-74-322034", "duty_phone": "+66-74-322034"},
            {"city": "孔敬", "phone": "+66-43-224653", "duty_phone": "+66-43-224653"},
        ]
    },
    "韩国": {
        "embassy": {
            "name": "中国驻韩国大使馆",
            "address": "54 Hyoja-dong, Jongno-gu, Seoul",
            "phone": "+82-2-7381038",
            "duty_phone": "+82-2-7550572",
            "email": "chinaemb_kr@mfa.gov.cn",
        },
        "consulates": [
            {"city": "釜山", "phone": "+82-51-7430725", "duty_phone": "+82-51-7430725"},
            {"city": "光州", "phone": "+82-62-3858801", "duty_phone": "+82-62-3858801"},
            {"city": "济州", "phone": "+82-64-7228803", "duty_phone": "+82-64-7228803"},
        ]
    },
    "法国": {
        "embassy": {
            "name": "中国驻法国大使馆",
            "address": "11 avenue George V, 75008 Paris",
            "phone": "+33-1-49521950",
            "duty_phone": "+33-1-49521950",
            "email": "chinaemb_fr@mfa.gov.cn",
        },
        "consulates": [
            {"city": "马赛", "phone": "+33-4-91320000", "duty_phone": "+33-4-91320000"},
            {"city": "斯特拉斯堡", "phone": "+33-3-88453232", "duty_phone": "+33-3-88453232"},
            {"city": "里昂", "phone": "+33-4-78946400", "duty_phone": "+33-4-78946400"},
        ]
    },
    "英国": {
        "embassy": {
            "name": "中国驻英国大使馆",
            "address": "49 Portland Place, London W1B 1JL",
            "phone": "+44-20-72994049",
            "duty_phone": "+44-20-72994049",
            "email": "chinaemb_uk@mfa.gov.cn",
        },
        "consulates": [
            {"city": "曼彻斯特", "phone": "+44-161-2247473", "duty_phone": "+44-161-2247473"},
            {"city": "爱丁堡", "phone": "+44-131-3373220", "duty_phone": "+44-131-3373220"},
            {"city": "贝尔法斯特", "phone": "+44-28-90246094", "duty_phone": "+44-28-90246094"},
        ]
    },
    "德国": {
        "embassy": {
            "name": "中国驻德国大使馆",
            "address": "Brückenstraße 10, 10179 Berlin",
            "phone": "+49-30-275880",
            "duty_phone": "+49-30-27588221",
            "email": "chinaemb_de@mfa.gov.cn",
        },
        "consulates": [
            {"city": "汉堡", "phone": "+49-40-82276013", "duty_phone": "+49-40-82276013"},
            {"city": "慕尼黑", "phone": "+49-89-17301618", "duty_phone": "+49-89-17301618"},
            {"city": "法兰克福", "phone": "+49-69-75085500", "duty_phone": "+49-69-75085500"},
        ]
    },
    "澳大利亚": {
        "embassy": {
            "name": "中国驻澳大利亚大使馆",
            "address": "15 Coronation Drive, Yarralumla ACT 2600",
            "phone": "+61-2-62734780",
            "duty_phone": "+61-2-62283948",
            "email": "chinaemb_au@mfa.gov.cn",
        },
        "consulates": [
            {"city": "悉尼", "phone": "+61-2-85958002", "duty_phone": "+61-2-85958002"},
            {"city": "墨尔本", "phone": "+61-3-98043271", "duty_phone": "+61-3-98043271"},
            {"city": "珀斯", "phone": "+61-8-92220333", "duty_phone": "+61-8-92220333"},
            {"city": "布里斯班", "phone": "+61-7-32106509", "duty_phone": "+61-7-32106509"},
        ]
    },
    "新加坡": {
        "embassy": {
            "name": "中国驻新加坡大使馆",
            "address": "150 Tanglin Road, Singapore 247980",
            "phone": "+65-64750165",
            "duty_phone": "+65-64750165",
            "email": "chinaemb_sg@mfa.gov.cn",
        },
    },
    "马来西亚": {
        "embassy": {
            "name": "中国驻马来西亚大使馆",
            "address": "229 Jalan Ampang, 50450 Kuala Lumpur",
            "phone": "+60-3-21428495",
            "duty_phone": "+60-3-21636812",
            "email": "chinaemb_my@mfa.gov.cn",
        },
        "consulates": [
            {"city": "槟城", "phone": "+60-4-2634488", "duty_phone": "+60-4-2634488"},
            {"city": "古晋", "phone": "+60-82-453344", "duty_phone": "+60-82-453344"},
            {"city": "哥打基纳巴卢", "phone": "+60-88-385488", "duty_phone": "+60-88-385488"},
        ]
    },
    "俄罗斯": {
        "embassy": {
            "name": "中国驻俄罗斯大使馆",
            "address": "ul. Druzhby, 6, Moscow 117330",
            "phone": "+7-495-9561168",
            "duty_phone": "+7-495-9561168",
            "email": "chinaemb_ru@mfa.gov.cn",
        },
        "consulates": [
            {"city": "圣彼得堡", "phone": "+7-812-7146230", "duty_phone": "+7-812-7146230"},
            {"city": "哈巴罗夫斯克", "phone": "+7-4212-302590", "duty_phone": "+7-4212-302590"},
            {"city": "伊尔库茨克", "phone": "+7-3952-781442", "duty_phone": "+7-3952-781442"},
            {"city": "叶卡捷琳堡", "phone": "+7-343-2535778", "duty_phone": "+7-343-2535778"},
        ]
    },
    "阿联酋": {
        "embassy": {
            "name": "中国驻阿联酋大使馆",
            "address": "Plot 26, Sector W59, Abu Dhabi",
            "phone": "+971-2-4434276",
            "duty_phone": "+971-2-4434276",
            "email": "chinaemb_ae@mfa.gov.cn",
        },
        "consulates": [
            {"city": "迪拜", "phone": "+971-4-3944733", "duty_phone": "+971-4-3983357"},
        ]
    },
    "印度尼西亚": {
        "embassy": {
            "name": "中国驻印度尼西亚大使馆",
            "address": "Jl. Mega Kuningan No.2, Jakarta",
            "phone": "+62-21-5764139",
            "duty_phone": "+62-21-5764139",
            "email": "chinaemb_id@mfa.gov.cn",
        },
        "consulates": [
            {"city": "泗水", "phone": "+62-31-5675383", "duty_phone": "+62-31-5675383"},
            {"city": "棉兰", "phone": "+62-61-4533144", "duty_phone": "+62-61-4533144"},
            {"city": "登巴萨(巴厘岛)", "phone": "+62-361-285017", "duty_phone": "+62-361-285017"},
        ]
    },
    "越南": {
        "embassy": {
            "name": "中国驻越南大使馆",
            "address": "46 Hoang Dieu, Ba Dinh, Hanoi",
            "phone": "+84-24-38453736",
            "duty_phone": "+84-24-38453736",
            "email": "chinaemb_vn@mfa.gov.cn",
        },
        "consulates": [
            {"city": "胡志明市", "phone": "+84-28-38292457", "duty_phone": "+84-28-38292457"},
            {"city": "岘港", "phone": "+84-236-3821655", "duty_phone": "+84-236-3821655"},
        ]
    },
    "柬埔寨": {
        "embassy": {
            "name": "中国驻柬埔寨大使馆",
            "address": "Blvd. Mao Tse Toung, Phnom Penh",
            "phone": "+855-12-901923",
            "duty_phone": "+855-12-901923",
            "email": "chinaemb_kh@mfa.gov.cn",
        },
        "consulates": [
            {"city": "西哈努克", "phone": "+855-34-933018", "duty_phone": "+855-34-933018"},
        ]
    },
    "菲律宾": {
        "embassy": {
            "name": "中国驻菲律宾大使馆",
            "address": "4896 Pasay Road, Makati City",
            "phone": "+63-2-88442148",
            "duty_phone": "+63-2-88442148",
            "email": "chinaemb_ph@mfa.gov.cn",
        },
        "consulates": [
            {"city": "宿务", "phone": "+63-32-2563433", "duty_phone": "+63-32-2563433"},
            {"city": "拉瓦格", "phone": "+63-72-7720506", "duty_phone": "+63-72-7720506"},
        ]
    },
    "土耳其": {
        "embassy": {
            "name": "中国驻土耳其大使馆",
            "address": "Gölköy Mah. Fethi Bey Cad. No.16, Ankara",
            "phone": "+90-312-4360628",
            "duty_phone": "+90-312-4360628",
            "email": "chinaemb_tr@mfa.gov.cn",
        },
        "consulates": [
            {"city": "伊斯坦布尔", "phone": "+90-212-2992188", "duty_phone": "+90-212-2992188"},
        ]
    },
    "埃及": {
        "embassy": {
            "name": "中国驻埃及大使馆",
            "address": "14 Bahgat Ali Street, Zamalek, Cairo",
            "phone": "+20-2-27361219",
            "duty_phone": "+20-2-27361219",
            "email": "chinaemb_eg@mfa.gov.cn",
        },
        "consulates": [
            {"city": "亚历山大", "phone": "+20-3-3916953", "duty_phone": "+20-3-3916953"},
        ]
    },
    "南非": {
        "embassy": {
            "name": "中国驻南非大使馆",
            "address": "972 Church Street, Arcadia, Pretoria",
            "phone": "+27-12-4316500",
            "duty_phone": "+27-12-4316500",
            "email": "chinaemb_za@mfa.gov.cn",
        },
        "consulates": [
            {"city": "约翰内斯堡", "phone": "+27-11-8835073", "duty_phone": "+27-11-8835073"},
            {"city": "开普敦", "phone": "+27-21-6740059", "duty_phone": "+27-21-6740059"},
            {"city": "德班", "phone": "+27-31-2016571", "duty_phone": "+27-31-2016571"},
        ]
    },
    "巴西": {
        "embassy": {
            "name": "中国驻巴西大使馆",
            "address": "SES - Av. das Nações, Quadra 8, Lote 51, Brasília",
            "phone": "+55-61-21958200",
            "duty_phone": "+55-61-99631988",
            "email": "chinaemb_br@mfa.gov.cn",
        },
        "consulates": [
            {"city": "圣保罗", "phone": "+55-11-30626165", "duty_phone": "+55-11-996389888"},
            {"city": "里约热内卢", "phone": "+55-21-32376612", "duty_phone": "+55-21-32376612"},
        ]
    },
    "印度": {
        "embassy": {
            "name": "中国驻印度大使馆",
            "address": "50-D, Shantipath, Chanakyapuri, New Delhi",
            "phone": "+91-11-26112345",
            "duty_phone": "+91-11-26112345",
            "email": "chinaemb_in@mfa.gov.cn",
        },
        "consulates": [
            {"city": "孟买", "phone": "+91-22-66320803", "duty_phone": "+91-22-66320803"},
            {"city": "加尔各答", "phone": "+91-33-40030258", "duty_phone": "+91-33-40030258"},
        ]
    },
}

# ========== 7大紧急场景行动指南 ==========
EMERGENCY_GUIDES = {
    "passport_lost": {
        "name": "护照丢失",
        "icon": "🛂",
        "priority": 1,  # 最高优先级
        "steps": [
            {"step": 1, "action": "立即报警", "detail": "到当地警察局报案，获取报案记录（Police Report）。这是补办证件的必要材料。", "urgent": True},
            {"step": 2, "action": "联系中国使领馆", "detail": "拨打中国驻当地使领馆领保电话，说明情况。使领馆会指导你补办旅行证或护照。", "urgent": True},
            {"step": 3, "action": "准备补办材料", "detail": "① 护照复印件/照片（如有）② 报案记录 ③ 近期证件照2张 ④ 填写《中华人民共和国护照/旅行证申请表》", "urgent": False},
            {"step": 4, "action": "前往使领馆办理", "detail": "旅行证通常1-4个工作日可取，紧急情况可申请加急（当天或次日）。护照换发需15个工作日。", "urgent": False},
            {"step": 5, "action": "通知保险公司", "detail": "如购买了旅行保险，联系保险公司报案，护照丢失通常在保障范围内。", "urgent": False},
        ],
        "tips": [
            "出国前务必拍下护照信息页和签证页，存手机和云端",
            "旅行证可替代护照用于回国，但不可用于第三国签证",
            "使领馆节假日/周末也提供紧急领保服务",
            "加急旅行证需提供航班行程单证明紧急性",
        ],
        "related_links": [
            "中国领事服务网: http://cs.mfa.gov.cn",
            "外交部全球领保热线: +86-10-12308 或 +86-10-65612308",
        ],
    },
    "flight_cancelled": {
        "name": "航班取消/延误",
        "icon": "✈️",
        "priority": 2,
        "steps": [
            {"step": 1, "action": "确认航班状态", "detail": "通过航司APP/官网确认航班最新状态，确认是取消还是延误，了解预计延误时长。", "urgent": True},
            {"step": 2, "action": "了解您的权利", "detail": "① 航司原因取消：免费改签/退票+可能补偿 ② 天气/不可抗力：免费改签/退票，无额外补偿 ③ EU261条款(欧洲)：最高600欧元补偿", "urgent": True},
            {"step": 3, "action": "立即改签", "detail": "通过航司APP/柜台/电话改签。越早改签可选航班越多。优先选择同一联盟/代码共享航班。", "urgent": True},
            {"step": 4, "action": "住宿安排（如需过夜）", "detail": "航司原因：航司应提供免费住宿。天气原因：通常自理，但可协商。保留所有票据用于后续理赔。", "urgent": False},
            {"step": 5, "action": "保险理赔", "detail": "联系旅行保险公司报案，航班延误/取消通常4小时起赔。保留：登机牌、航班取消证明、改签票据。", "urgent": False},
        ],
        "tips": [
            "国内航班延误4小时以上可获200-400元补偿（航司原因）",
            "改签时优先选同一航空联盟航班，里程不浪费",
            "EU261适用于从EU机场出发的任何航司，或EU航司到达EU的航班",
            "保留所有票据和截图，理赔时必备",
            "高德/飞常准可查航班实时动态",
        ],
        "compensation_rules": {
            "国内延误": "航司原因：4h+补偿200元，8h+补偿400元",
            "EU261": "≤1500km取消/延误3h+: €250; 1500-3500km: €400; >3500km: €300-600",
            "美国": "无统一补偿规则，但非天气原因可协商",
        },
    },
    "medical_emergency": {
        "name": "突发疾病/受伤",
        "icon": "🏥",
        "priority": 2,
        "steps": [
            {"step": 1, "action": "拨打当地急救电话", "detail": "立即拨打当地救护车/急救电话。如不确定号码，先拨当地通用紧急号码。", "urgent": True},
            {"step": 2, "action": "说明情况（语言技巧）", "detail": "① 用简单英语说明：I need help, I'm at [地址], [症状] ② 出示保险卡/保险电子凭证 ③ 如有过敏史/慢性病，随身携带英文说明卡", "urgent": True},
            {"step": 3, "action": "联系保险公司", "detail": "24小时救援热线（保单上可找到），保险公司可：① 推荐合作医院 ② 安排医疗转运 ③ 预付医疗费（部分保险）", "urgent": True},
            {"step": 4, "action": "前往医院", "detail": "优先选择保险公司合作医院。如自费就医，保留所有单据、处方、诊断书（原件+翻译件）。", "urgent": False},
            {"step": 5, "action": "保留理赔材料", "detail": "① 门诊/住院病历 ② 医疗费原始收据 ③ 处方和用药清单 ④ 如涉及第三方责任，保留报警记录", "urgent": False},
        ],
        "tips": [
            "出国前准备：常用药+英文说明书、过敏史/病史英文卡片、保险救援热线存手机",
            "部分国家（如泰国）私立医院需预付押金，保险可担保函免押金",
            "欧美医疗费极贵：美国急诊可能$2000+起，务必确认保险覆盖",
            "食物过敏者随身携带多语言过敏卡（可网上下载模板）",
            "热射病/中暑在东南亚常见，注意补水和防晒",
        ],
    },
    "theft_robbery": {
        "name": "被盗/被抢",
        "icon": "🔒",
        "priority": 2,
        "steps": [
            {"step": 1, "action": "确保人身安全", "detail": "不要追赶或与劫匪对抗。人身安全第一，财物可以补办。如遇持械抢劫，配合对方要求。", "urgent": True},
            {"step": 2, "action": "报警", "detail": "到最近的警察局报案，获取报案记录（Police Report/报案回执）。这是保险理赔和证件补办的必要文件。", "urgent": True},
            {"step": 3, "action": "挂失银行卡和手机", "detail": "① 银行卡：拨打发卡行国际客服电话挂失 ② 手机：联系运营商远程锁定/擦除 ③ 支付宝/微信：冻结账号", "urgent": True},
            {"step": 4, "action": "补办证件", "detail": "如护照被盗，参考「护照丢失」流程。如身份证在国内丢失，可委托家人代办。", "urgent": False},
            {"step": 5, "action": "保险理赔", "detail": "48小时内联系保险公司报案。需要：报案记录、物品购买凭证（照片/小票）、丢失清单及价值估算。", "urgent": False},
        ],
        "tips": [
            "常见被盗场景：巴黎地铁、罗马景点周边、巴塞罗那兰布拉大道、曼谷考山路",
            "防盗建议：贵重物品分开放、背包前背、酒店保险箱存放护照原件",
            "欧洲旅游税（City Tax）酒店另收，与被盗无关但常被忽略",
            "手机开启远程查找功能（iPhone: Find My / Android: Find My Device）",
            "备份重要证件到云端（护照、签证、保险单）",
        ],
        "high_risk_areas": [
            "巴黎：地铁1号线、圣心大教堂周边",
            "罗马：特米尼火车站、斗兽场周边",
            "巴塞罗那：兰布拉大道、圣家堂排队区",
            "曼谷：考山路、暹罗广场",
            "伊斯坦布尔：大巴扎、塔克西姆广场",
        ],
    },
    "natural_disaster": {
        "name": "自然灾害/极端天气",
        "icon": "🌊",
        "priority": 3,
        "steps": [
            {"step": 1, "action": "关注官方预警", "detail": "① 当地气象部门APP/网站 ② 酒店前台/当地电台 ③ 中国使领馆安全提醒（领事直通车微信公众号）", "urgent": True},
            {"step": 2, "action": "前往安全地带", "detail": "① 地震：远离建筑，到空旷地带 ② 台风：留在室内，远离窗户 ③ 洪水：往高处转移 ④ 海啸：往内陆高处跑，不要留在海岸", "urgent": True},
            {"step": 3, "action": "联系使领馆报平安", "detail": "灾后主动联系中国使领馆报平安。使领馆会组织撤离和救助。", "urgent": True},
            {"step": 4, "action": "调整行程", "detail": "① 联系航司了解航班恢复情况 ② 联系酒店协商退改 ③ 保留所有变更凭证用于保险理赔", "urgent": False},
            {"step": 5, "action": "保险理赔", "detail": "自然灾害通常在旅行保险承保范围内（注意：部分保险对「已知灾害」出发后不赔）。保留所有票据和官方灾害证明。", "urgent": False},
        ],
        "tips": [
            "东南亚台风季：6-11月，日本台风季：7-10月",
            "出发前关注目的地天气预警，购买含自然灾害保障的旅行险",
            "下载当地应急APP：日本Yurekuru Call（地震预警）、泰国ThaiAlert",
            "外交部领事直通车微信公众号可接收安全提醒",
            "海啸预警：感觉强震后立即远离海岸，不要等官方预警",
        ],
    },
    "accident_traffic": {
        "name": "交通事故",
        "icon": "🚗",
        "priority": 2,
        "steps": [
            {"step": 1, "action": "确保安全+检查伤情", "detail": "① 开启危险报警灯 ② 转移到安全地带 ③ 如有人受伤，立即拨打急救电话", "urgent": True},
            {"step": 2, "action": "报警", "detail": "拨打当地交警电话。海外事故必须报警，没有交警事故报告保险公司可能拒赔。", "urgent": True},
            {"step": 3, "action": "记录现场", "detail": "① 拍照：车辆受损、道路状况、对方车牌、伤情 ② 记录：对方信息（姓名、电话、保险公司、车牌号）③ 如有目击者，留下联系方式", "urgent": True},
            {"step": 4, "action": "联系租车公司（如适用）", "detail": "① 通知租车公司事故情况 ② 确认保险覆盖范围 ③ 了解当地修车/换车流程", "urgent": False},
            {"step": 5, "action": "保险理赔", "detail": "① 联系旅行保险/车险公司 ② 提供交警事故报告、现场照片、对方信息 ③ 保留所有医疗和修车单据", "urgent": False},
        ],
        "tips": [
            "海外自驾务必购买全险（含第三者责任险），基本险不够",
            "部分国家（如泰国）靠左行驶，注意方向",
            "租车时拍下交车时车辆状况（划痕、凹陷），避免还车纠纷",
            "国际驾照/驾照翻译件提前办好",
            "如涉及人员受伤，不要离开现场，等待警察到来",
        ],
    },
    "legal_trouble": {
        "name": "法律纠纷/被捕",
        "icon": "⚖️",
        "priority": 3,
        "steps": [
            {"step": 1, "action": "保持冷静，配合执法", "detail": "① 不要与执法人员争执或暴力抵抗 ② 不要签署看不懂的文件 ③ 要求提供中文翻译", "urgent": True},
            {"step": 2, "action": "联系中国使领馆", "detail": "被拘押时有权利联系本国领事官员。使领馆可以：① 推荐当地律师 ② 协助联系家人 ③ 进行领事探视", "urgent": True},
            {"step": 3, "action": "聘请律师", "detail": "① 使领馆可提供当地律师名单 ② 不要在无律师在场情况下做正式陈述 ③ 如无力支付律师费，询问是否有法律援助", "urgent": True},
            {"step": 4, "action": "通知家人", "detail": "通过使领馆或律师通知家人，安排律师费和生活费。", "urgent": False},
            {"step": 5, "action": "了解当地法律", "detail": "常见海外法律陷阱：① 部分国家公共场所禁止饮酒 ② 某些药品在国外属于违禁品 ③ 拍照可能涉及军事禁区", "urgent": False},
        ],
        "tips": [
            "常见法律陷阱：新加坡禁口香糖、阿联酋公共场所禁酒、泰国不敬王室罪极重",
            "随身携带护照复印件（原件放酒店保险箱），警察可能随时查证件",
            "部分国家（如日本）海关对某些药品管控严格，出行前确认",
            "不要替陌生人携带行李或包裹",
            "使领馆不能做的事：干预司法、支付律师费、安排保释金",
        ],
    },
}

# ========== 中国外交部全球领保热线 ==========
GLOBAL_HOTLINE = {
    "phone": "+86-10-12308",
    "phone_alt": "+86-10-65612308",
    "wechat": "领事直通车",
    "description": "中国外交部全球领事保护与服务应急热线，24小时服务",
    "when_to_call": [
        "护照丢失/被盗需紧急补办",
        "遭遇重大安全事故",
        "自然灾害需紧急撤离",
        "被当地警方拘押",
        "遇到歧视性或暴力侵害",
        "其他需要领事保护的紧急情况",
    ],
}


def _match_country(query):
    """模糊匹配国家名"""
    query_lower = query.lower()
    # 精确匹配
    for country in EMERGENCY_NUMBERS:
        if country == query or query in country:
            return country
    # 模糊匹配
    for country in EMERGENCY_NUMBERS:
        if query_lower in country.lower() or country.lower() in query_lower:
            return country
    # 别名映射（含常见城市→国家映射）
    aliases = {
        "usa": "美国", "us": "美国", "america": "美国", "united states": "美国",
        "纽约": "美国", "洛杉矶": "美国", "旧金山": "美国", "芝加哥": "美国",
        "夏威夷": "美国", "拉斯维加斯": "美国", "西雅图": "美国",
        "uk": "英国", "united kingdom": "英国", "england": "英国",
        "伦敦": "英国", "曼彻斯特": "英国", "爱丁堡": "英国",
        "jp": "日本", "japan": "日本",
        "东京": "日本", "大阪": "日本", "京都": "日本", "北海道": "日本",
        "冲绳": "日本", "名古屋": "日本", "福冈": "日本",
        "kr": "韩国", "korea": "韩国", "south korea": "韩国",
        "首尔": "韩国", "釜山": "韩国", "济州": "韩国", "济州岛": "韩国",
        "th": "泰国", "thailand": "泰国",
        "曼谷": "泰国", "清迈": "泰国", "普吉": "泰国", "普吉岛": "泰国",
        "芭提雅": "泰国", "苏梅岛": "泰国",
        "sg": "新加坡", "singapore": "新加坡",
        "my": "马来西亚", "malaysia": "马来西亚",
        "吉隆坡": "马来西亚", "槟城": "马来西亚", "沙巴": "马来西亚",
        "vn": "越南", "vietnam": "越南",
        "河内": "越南", "胡志明": "越南", "岘港": "越南", "芽庄": "越南",
        "kh": "柬埔寨", "cambodia": "柬埔寨",
        "金边": "柬埔寨", "暹粒": "柬埔寨", "西哈努克": "柬埔寨",
        "id": "印度尼西亚", "indonesia": "印度尼西亚", "印尼": "印度尼西亚",
        "巴厘岛": "印度尼西亚", "雅加达": "印度尼西亚", "泗水": "印度尼西亚",
        "ph": "菲律宾", "philippines": "菲律宾",
        "马尼拉": "菲律宾", "宿务": "菲律宾", "长滩岛": "菲律宾",
        "in": "印度", "india": "印度",
        "新德里": "印度", "孟买": "印度", "加尔各答": "印度",
        "uae": "阿联酋", "dubai": "阿联酋", "迪拜": "阿联酋",
        "阿布扎比": "阿联酋",
        "tr": "土耳其", "turkey": "土耳其", "türkiye": "土耳其",
        "伊斯坦布尔": "土耳其", "安卡拉": "土耳其", "卡帕多奇亚": "土耳其",
        "ru": "俄罗斯", "russia": "俄罗斯",
        "莫斯科": "俄罗斯", "圣彼得堡": "俄罗斯", "海参崴": "俄罗斯",
        "au": "澳大利亚", "australia": "澳大利亚", "澳洲": "澳大利亚",
        "悉尼": "澳大利亚", "墨尔本": "澳大利亚", "布里斯班": "澳大利亚",
        "珀斯": "澳大利亚", "黄金海岸": "澳大利亚",
        "nz": "新西兰", "new zealand": "新西兰",
        "奥克兰": "新西兰", "皇后镇": "新西兰",
        "br": "巴西", "brazil": "巴西",
        "里约": "巴西", "圣保罗": "巴西",
        "mx": "墨西哥", "mexico": "墨西哥",
        "坎昆": "墨西哥", "墨西哥城": "墨西哥",
        "eg": "埃及", "egypt": "埃及",
        "开罗": "埃及", "亚历山大": "埃及",
        "za": "南非", "south africa": "南非",
        "开普敦": "南非", "约翰内斯堡": "南非",
        "de": "德国", "germany": "德国",
        "柏林": "德国", "慕尼黑": "德国", "法兰克福": "德国", "汉堡": "德国",
        "fr": "法国", "france": "法国",
        "巴黎": "法国", "马赛": "法国", "里昂": "法国", "尼斯": "法国",
        "it": "意大利", "italy": "意大利",
        "罗马": "意大利", "米兰": "意大利", "威尼斯": "意大利", "佛罗伦萨": "意大利",
        "es": "西班牙", "spain": "西班牙",
        "巴塞罗那": "西班牙", "马德里": "西班牙",
        "ch": "瑞士", "switzerland": "瑞士",
        "苏黎世": "瑞士", "日内瓦": "瑞士", "因特拉肯": "瑞士",
        "nl": "荷兰", "netherlands": "荷兰",
        "阿姆斯特丹": "荷兰",
        "gr": "希腊", "greece": "希腊",
        "雅典": "希腊", "圣托里尼": "希腊",
        "pt": "葡萄牙", "portugal": "葡萄牙",
        "里斯本": "葡萄牙",
        "cz": "捷克", "czech": "捷克", "czechia": "捷克",
        "布拉格": "捷克",
        "at": "奥地利", "austria": "奥地利",
        "维也纳": "奥地利",
        "be": "比利时", "belgium": "比利时",
        "布鲁塞尔": "比利时",
        "se": "瑞典", "sweden": "瑞典",
        "斯德哥尔摩": "瑞典",
        "no": "挪威", "norway": "挪威",
        "奥斯陆": "挪威",
        "fi": "芬兰", "finland": "芬兰",
        "赫尔辛基": "芬兰",
        "dk": "丹麦", "denmark": "丹麦",
        "哥本哈根": "丹麦",
        "is": "冰岛", "iceland": "冰岛",
        "雷克雅未克": "冰岛",
        "ie": "爱尔兰", "ireland": "爱尔兰",
        "都柏林": "爱尔兰",
        "hr": "克罗地亚", "croatia": "克罗地亚",
        "萨格勒布": "克罗地亚", "杜布罗夫尼克": "克罗地亚",
        "ar": "阿根廷", "argentina": "阿根廷",
        "布宜诺斯艾利斯": "阿根廷",
        "cl": "智利", "chile": "智利",
        "co": "哥伦比亚", "colombia": "哥伦比亚",
        "pe": "秘鲁", "peru": "秘鲁",
        "利马": "秘鲁", "库斯科": "秘鲁",
        "ke": "肯尼亚", "kenya": "肯尼亚",
        "内罗毕": "肯尼亚",
        "ma": "摩洛哥", "morocco": "摩洛哥",
        "马拉喀什": "摩洛哥",
        "np": "尼泊尔", "nepal": "尼泊尔",
        "加德满都": "尼泊尔",
        "lk": "斯里兰卡", "sri lanka": "斯里兰卡",
        "科伦坡": "斯里兰卡",
        "mm": "缅甸", "myanmar": "缅甸",
        "仰光": "缅甸", "曼德勒": "缅甸",
        "la": "老挝", "laos": "老挝",
        "万象": "老挝", "琅勃拉邦": "老挝",
        "mn": "蒙古", "mongolia": "蒙古",
        "乌兰巴托": "蒙古",
        "il": "以色列", "israel": "以色列",
        "特拉维夫": "以色列", "耶路撒冷": "以色列",
        "hu": "匈牙利", "hungary": "匈牙利",
        "布达佩斯": "匈牙利",
        "pl": "波兰", "poland": "波兰",
        "华沙": "波兰",
    }
    for alias, country in aliases.items():
        if query_lower == alias:
            return country
    return None


def _match_scenario(query):
    """匹配紧急场景"""
    scenario_keywords = {
        "passport_lost": ["护照", "passport", "丢护照", "护照丢", "护照丢失", "护照被盗", "证件丢", "旅行证"],
        "flight_cancelled": ["航班", "flight", "取消", "cancel", "延误", "delay", "改签", "飞机取消", "航班取消"],
        "medical_emergency": ["疾病", "medical", "生病", "医院", "hospital", "急救", "ambulance", "受伤", "injury", "过敏", "中暑", "发烧"],
        "theft_robbery": ["被盗", "theft", "被偷", "偷窃", "抢劫", "robbery", "钱包", "被盗", "手机被偷", "行李被偷"],
        "natural_disaster": ["台风", "typhoon", "地震", "earthquake", "洪水", "flood", "海啸", "tsunami", "暴风雨", "极端天气", "自然灾害"],
        "accident_traffic": ["车祸", "accident", "交通事故", "撞车", "car accident", "租车", "自驾"],
        "legal_trouble": ["被捕", "arrest", "警察", "police", "拘留", "法律", "legal", "官司", "律师"],
    }
    query_lower = query.lower()
    best_match = None
    best_score = 0
    for scenario, keywords in scenario_keywords.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > best_score:
            best_score = score
            best_match = scenario
    return best_match


# ========== 工具1: 查询紧急电话 ==========
def cmd_emergency_number(country, scenario=None):
    """查询指定国家/地区的紧急电话"""
    matched = _match_country(country)
    if not matched:
        return {
            "status": "error",
            "message": f"未找到「{country}」的紧急电话数据。目前支持{len(EMERGENCY_NUMBERS)}个国家/地区，请尝试英文名或常用别名。",
        }

    numbers = EMERGENCY_NUMBERS[matched]
    result = f"📞 **{matched}紧急电话**\n\n"
    result += f"| 类型 | 号码 |\n|------|------|\n"
    result += f"| 🚔 报警 | {numbers.get('police', '-')} |\n"
    result += f"| 🚑 急救 | {numbers.get('ambulance', '-')} |\n"
    result += f"| 🚒 消防 | {numbers.get('fire', '-')} |\n"
    if numbers.get("tourist_police"):
        result += f"| 👮 旅游警察 | {numbers['tourist_police']} |\n"
    if numbers.get("non_emergency"):
        result += f"| 📞 非紧急 | {numbers['non_emergency']} |\n"
    if numbers.get("eu_emergency"):
        result += f"| 🇪🇺 欧盟统一 | {numbers['eu_emergency']} |\n"
    if numbers.get("unified"):
        result += f"| 📞 统一紧急 | {numbers['unified']} |\n"
    if numbers.get("note"):
        result += f"\n> 💡 {numbers['note']}\n"

    # 附加中国使领馆信息
    if matched in CHINESE_EMBASSIES:
        emb = CHINESE_EMBASSIES[matched]["embassy"]
        result += f"\n🏛️ **中国驻{matched}使领馆**\n\n"
        result += f"- **大使馆**：{emb['name']}\n"
        result += f"  - 值班电话：{emb.get('duty_phone', emb['phone'])}\n"
        if emb.get("consular_phone"):
            result += f"  - 领事电话：{emb['consular_phone']}\n"

        consulates = CHINESE_EMBASSIES[matched].get("consulates", [])
        if consulates:
            result += f"\n**领事馆**：\n"
            for c in consulates:
                result += f"- {c['city']}：{c.get('duty_phone', c['phone'])}\n"

    result += f"\n---\n🌐 外交部全球领保热线：{GLOBAL_HOTLINE['phone']} / {GLOBAL_HOTLINE['phone_alt']}"
    return result


# ========== 工具2: 紧急场景行动指南 ==========
def cmd_emergency_guide(scenario):
    """根据紧急场景类型提供行动指南"""
    matched = _match_scenario(scenario)
    if not matched:
        # 尝试直接匹配key
        if scenario in EMERGENCY_GUIDES:
            matched = scenario
        else:
            available = "、".join([f"{g['icon']}{g['name']}" for g in EMERGENCY_GUIDES.values()])
            return {
                "status": "error",
                "message": f"未识别紧急场景「{scenario}」。支持的场景：{available}",
            }

    guide = EMERGENCY_GUIDES[matched]
    result = f"{guide['icon']} **{guide['name']} - 紧急行动指南**\n\n"
    result += "> ⚠️ 请按顺序执行以下步骤，标注🚨的为最紧急动作\n\n"

    for step in guide["steps"]:
        urgent_mark = " 🚨" if step.get("urgent") else ""
        result += f"**步骤 {step['step']}：{step['action']}**{urgent_mark}\n"
        result += f"{step['detail']}\n\n"

    if guide.get("tips"):
        result += "### 💡 重要提示\n\n"
        for tip in guide["tips"]:
            result += f"- {tip}\n"

    if guide.get("compensation_rules"):
        result += "\n### 💰 补偿标准参考\n\n"
        for region, rule in guide["compensation_rules"].items():
            result += f"- **{region}**：{rule}\n"

    if guide.get("high_risk_areas"):
        result += "\n### ⚠️ 高风险区域\n\n"
        for area in guide["high_risk_areas"]:
            result += f"- {area}\n"

    if guide.get("related_links"):
        result += "\n### 🔗 相关资源\n\n"
        for link in guide["related_links"]:
            result += f"- {link}\n"

    result += f"\n---\n🌐 外交部全球领保热线：{GLOBAL_HOTLINE['phone']} / {GLOBAL_HOTLINE['phone_alt']}\n"
    result += f"📱 微信公众号：{GLOBAL_HOTLINE['wechat']}"
    return result


# ========== 工具3: 使领馆查询 ==========
def cmd_embassy_info(country):
    """查询中国驻外使领馆信息"""
    matched = _match_country(country)
    if not matched:
        return {
            "status": "error",
            "message": f"未找到「{country}」的使领馆数据。目前支持{len(CHINESE_EMBASSIES)}个主要国家。",
        }

    if matched not in CHINESE_EMBASSIES:
        return {
            "status": "partial",
            "message": f"暂无{matched}的详细使领馆数据，请直接拨打外交部全球领保热线：{GLOBAL_HOTLINE['phone']}",
        }

    data = CHINESE_EMBASSIES[matched]
    emb = data["embassy"]
    result = f"🏛️ **中国驻{matched}使领馆信息**\n\n"
    result += f"### 大使馆\n\n"
    result += f"- **名称**：{emb['name']}\n"
    result += f"- **地址**：{emb['address']}\n"
    result += f"- **电话**：{emb['phone']}\n"
    result += f"- **值班/领保电话**：{emb.get('duty_phone', emb['phone'])} 🚨\n"
    if emb.get("consular_phone"):
        result += f"- **领事部电话**：{emb['consular_phone']}\n"
    if emb.get("email"):
        result += f"- **邮箱**：{emb['email']}\n"
    if emb.get("consular_email"):
        result += f"- **领事部邮箱**：{emb['consular_email']}\n"

    consulates = data.get("consulates", [])
    if consulates:
        result += f"\n### 领事馆\n\n"
        for c in consulates:
            result += f"- **{c['city']}**：电话 {c['phone']}｜值班 {c.get('duty_phone', c['phone'])}\n"

    result += f"\n### 何时联系使领馆\n\n"
    for item in GLOBAL_HOTLINE["when_to_call"]:
        result += f"- {item}\n"

    result += f"\n---\n🌐 外交部全球领保热线：{GLOBAL_HOTLINE['phone']} / {GLOBAL_HOTLINE['phone_alt']}\n"
    result += f"📱 微信公众号：{GLOBAL_HOTLINE['wechat']}\n"
    result += f"🌐 领事服务网：http://cs.mfa.gov.cn"
    return result


# ========== 主入口 ==========
def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "用法: emergency.py <command> [args]\n命令: emergency_number <国家> | guide <场景> | embassy <国家>",
        }, ensure_ascii=False))
        return

    command = sys.argv[1]

    if command == "emergency_number":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "message": "请指定国家/地区名称"}, ensure_ascii=False))
            return
        country = " ".join(sys.argv[2:])
        result = cmd_emergency_number(country)
        if isinstance(result, dict):
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(result)

    elif command == "guide":
        if len(sys.argv) < 3:
            # 列出所有场景
            scenarios = []
            for key, guide in EMERGENCY_GUIDES.items():
                scenarios.append(f"{guide['icon']} {guide['name']} (关键词: {key})")
            print("可用紧急场景指南：\n" + "\n".join(scenarios))
            return
        scenario = " ".join(sys.argv[2:])
        result = cmd_emergency_guide(scenario)
        if isinstance(result, dict):
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(result)

    elif command == "embassy":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "message": "请指定国家名称"}, ensure_ascii=False))
            return
        country = " ".join(sys.argv[2:])
        result = cmd_embassy_info(country)
        if isinstance(result, dict):
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(result)

    else:
        print(json.dumps({
            "status": "error",
            "message": f"未知命令: {command}\n支持: emergency_number | guide | embassy",
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
