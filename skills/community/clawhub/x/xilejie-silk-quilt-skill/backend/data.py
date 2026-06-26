# -*- coding: utf-8 -*-
"""
喜乐姐真蚕丝喜被 - 产品数据与业务逻辑
所有产品信息、常见问题、售后政策都在这里维护。
海叔要改价格、加新品，改这个文件就行。
"""

# ============================================================
# 品牌信息
# ============================================================
BRAND_INFO = {
    "name": "喜乐姐真蚕丝喜被",
    "slogan": "一床好蚕丝被，盖一辈子",
    "story": (
        "喜乐姐从事蚕丝被行业多年，坚持只做100%桑蚕长丝被。"
        "从选茧、煮茧、剥丝、拉网，每一步都是手工完成。"
        "工厂直发，没有中间商，把省下来的钱让给顾客。"
        "我们敢说假一赔十，因为每一床被子都经得起检验。"
    ),
    "origin": "浙江桐乡（中国蚕丝之都）",
    "craft": "手工桑蚕长丝，传统拉网工艺",
    "certifications": [
        "每床附质检报告",
        "支持燃烧法/84溶解法现场验真",
        "假一赔十承诺"
    ],
    "contact": {
        "wechat": "18637535738",
        "phone": "请通过微信联系"
    }
}

# ============================================================
# 产品列表
# 海叔改价格就改这里的 price 字段
# 加新品就照着格式加一条
# ============================================================
PRODUCTS = [
    # --- 夏凉被 ---
    {
        "id": "XL-S-150",
        "name": "夏凉被 150×200cm",
        "category": "夏凉被",
        "size": "150×200cm",
        "bed_width": "1.2米",
        "filling_weight": "0.5斤",
        "filling_type": "100%桑蚕长丝",
        "price": 398,
        "description": "薄款，适合夏天空调房。轻盈透气，贴身不闷。",
        "in_stock": True
    },
    {
        "id": "XL-S-200",
        "name": "夏凉被 200×230cm",
        "category": "夏凉被",
        "size": "200×230cm",
        "bed_width": "1.5米",
        "filling_weight": "0.75斤",
        "filling_type": "100%桑蚕长丝",
        "price": 498,
        "description": "薄款，适合夏天空调房。双人床常用尺寸。",
        "in_stock": True
    },
    {
        "id": "XL-S-220",
        "name": "夏凉被 220×240cm",
        "category": "夏凉被",
        "size": "220×240cm",
        "bed_width": "1.8米/2米",
        "filling_weight": "1斤",
        "filling_type": "100%桑蚕长丝",
        "price": 598,
        "description": "薄款，适合夏天空调房。大床推荐。",
        "in_stock": True
    },
    # --- 春秋被 ---
    {
        "id": "CQ-S-150",
        "name": "春秋被 150×200cm",
        "category": "春秋被",
        "size": "150×200cm",
        "bed_width": "1.2米",
        "filling_weight": "2斤",
        "filling_type": "100%桑蚕长丝",
        "price": 898,
        "description": "中厚款，春秋两季最舒服的厚度。",
        "in_stock": True
    },
    {
        "id": "CQ-S-200",
        "name": "春秋被 200×230cm",
        "category": "春秋被",
        "size": "200×230cm",
        "bed_width": "1.5米",
        "filling_weight": "2.5斤",
        "filling_type": "100%桑蚕长丝",
        "price": 1098,
        "description": "中厚款，双人床春秋首选。",
        "in_stock": True
    },
    {
        "id": "CQ-S-220",
        "name": "春秋被 220×240cm",
        "category": "春秋被",
        "size": "220×240cm",
        "bed_width": "1.8米/2米",
        "filling_weight": "3斤",
        "filling_type": "100%桑蚕长丝",
        "price": 1298,
        "description": "中厚款，大床春秋首选。",
        "in_stock": True
    },
    # --- 冬被 ---
    {
        "id": "DB-S-150",
        "name": "冬被 150×200cm",
        "category": "冬被",
        "size": "150×200cm",
        "bed_width": "1.2米",
        "filling_weight": "4斤",
        "filling_type": "100%桑蚕长丝",
        "price": 1598,
        "description": "加厚款，适合冬天、没暖气的地方。",
        "in_stock": True
    },
    {
        "id": "DB-S-200",
        "name": "冬被 200×230cm",
        "category": "冬被",
        "size": "200×230cm",
        "bed_width": "1.5米",
        "filling_weight": "5斤",
        "filling_type": "100%桑蚕长丝",
        "price": 1898,
        "description": "加厚款，双人床冬天用。",
        "in_stock": True
    },
    {
        "id": "DB-S-220",
        "name": "冬被 220×240cm",
        "category": "冬被",
        "size": "220×240cm",
        "bed_width": "1.8米/2米",
        "filling_weight": "6斤",
        "filling_type": "100%桑蚕长丝",
        "price": 2198,
        "description": "加厚款，大床冬天首选。暖和又不压身。",
        "in_stock": True
    },
    # --- 子母被（四季通用） ---
    {
        "id": "ZM-S-200",
        "name": "子母被 200×230cm（四季通用）",
        "category": "子母被",
        "size": "200×230cm",
        "bed_width": "1.5米",
        "filling_weight": "1斤+3斤（两条组合）",
        "filling_type": "100%桑蚕长丝",
        "price": 1498,
        "description": "一薄一厚两条被子，春秋盖薄的，冬天合起来盖，夏天都不盖。最划算的四季方案。",
        "in_stock": True
    },
    {
        "id": "ZM-S-220",
        "name": "子母被 220×240cm（四季通用）",
        "category": "子母被",
        "size": "220×240cm",
        "bed_width": "1.8米/2米",
        "filling_weight": "1.5斤+4斤（两条组合）",
        "filling_type": "100%桑蚕长丝",
        "price": 1898,
        "description": "一薄一厚两条被子，大床四季通用。",
        "in_stock": True
    },
    # --- 喜被（婚庆定制） ---
    {
        "id": "XB-S-200",
        "name": "喜被 200×230cm（含龙凤绣花被套）",
        "category": "喜被",
        "size": "200×230cm",
        "bed_width": "1.5米",
        "filling_weight": "3斤",
        "filling_type": "100%桑蚕长丝",
        "price": 1698,
        "description": "婚庆专用，含大红龙凤绣花被套。可定制绣字（新人名字+日期）。",
        "in_stock": True
    },
    {
        "id": "XB-S-220",
        "name": "喜被 220×240cm（含龙凤绣花被套）",
        "category": "喜被",
        "size": "220×240cm",
        "bed_width": "1.8米/2米",
        "filling_weight": "4斤",
        "filling_type": "100%桑蚕长丝",
        "price": 2098,
        "description": "婚庆专用，大床款。含大红龙凤绣花被套，可定制绣字。",
        "in_stock": True
    },
]

# ============================================================
# 选购推荐逻辑
# ============================================================
SIZE_GUIDE = {
    "1.2米": "150×200cm",
    "1.2": "150×200cm",
    "1.5米": "200×230cm",
    "1.5": "200×230cm",
    "1.8米": "220×240cm",
    "1.8": "220×240cm",
    "2米": "220×240cm",
    "2.0米": "220×240cm",
    "2.0": "220×240cm",
    "2": "220×240cm",
}

SEASON_GUIDE = {
    "夏天": "夏凉被",
    "夏季": "夏凉被",
    "夏": "夏凉被",
    "春秋": "春秋被",
    "春天": "春秋被",
    "秋天": "春秋被",
    "春季": "春秋被",
    "秋季": "春秋被",
    "冬天": "冬被",
    "冬季": "冬被",
    "冬": "冬被",
    "四季": "子母被",
    "四季通用": "子母被",
    "全年": "子母被",
}

PURPOSE_GUIDE = {
    "结婚": "喜被",
    "婚庆": "喜被",
    "婚礼": "喜被",
    "嫁妆": "喜被",
    "送礼": "春秋被",
    "乔迁": "春秋被",
    "搬家": "春秋被",
    "自用": "春秋被",
    "日常": "春秋被",
}


def get_recommendation(bed_width=None, season=None, purpose=None, budget=None):
    """根据用户需求推荐合适的产品"""
    results = list(PRODUCTS)

    # 按用途筛选类别
    target_category = None
    if purpose:
        for key, cat in PURPOSE_GUIDE.items():
            if key in purpose:
                target_category = cat
                break

    # 按季节筛选类别（如果用途没命中）
    if not target_category and season:
        for key, cat in SEASON_GUIDE.items():
            if key in season:
                target_category = cat
                break

    if target_category:
        results = [p for p in results if p["category"] == target_category]

    # 按床宽筛选尺寸
    if bed_width:
        target_size = None
        for key, size in SIZE_GUIDE.items():
            if key in bed_width:
                target_size = size
                break
        if target_size:
            results = [p for p in results if p["size"] == target_size]

    # 按预算筛选
    if budget:
        try:
            if "以内" in budget or "以下" in budget:
                max_price = int("".join(filter(str.isdigit, budget)))
                results = [p for p in results if p["price"] <= max_price]
            elif "以上" in budget:
                min_price = int("".join(filter(str.isdigit, budget)))
                results = [p for p in results if p["price"] >= min_price]
            elif "-" in budget:
                parts = budget.split("-")
                min_price = int("".join(filter(str.isdigit, parts[0])))
                max_price = int("".join(filter(str.isdigit, parts[1])))
                results = [p for p in results if min_price <= p["price"] <= max_price]
        except (ValueError, IndexError):
            pass

    if not results:
        results = [p for p in PRODUCTS if p["category"] == "春秋被"]

    return results


# ============================================================
# 蚕丝真伪鉴别
# ============================================================
SILK_AUTH_GUIDE = {
    "commitment": "喜乐姐承诺：假一赔十。每床被子都附质检报告，随时欢迎验货。",
    "methods": [
        {
            "name": "燃烧法",
            "steps": "抽几根蚕丝，用打火机点燃。",
            "real_silk": "真蚕丝烧起来有烧头发的焦味，离火即熄，灰烬用手一捏就碎成粉末。",
            "fake_silk": "化纤烧起来有刺鼻的塑料味，会持续燃烧，灰烬结成硬块捏不碎。"
        },
        {
            "name": "84消毒液溶解法",
            "steps": "取少量蚕丝，泡进84消毒液（原液）中。",
            "real_silk": "真蚕丝是蛋白质纤维，5-10分钟就会完全溶解消失。",
            "fake_silk": "化纤不会溶解，泡多久都还在。"
        },
        {
            "name": "拉丝法",
            "steps": "从被子拉链口取出一小撮蚕丝，试着拉扯。",
            "real_silk": "真桑蚕长丝可以拉很长（几十厘米甚至更长），韧性好，不容易拉断。",
            "fake_silk": "短纤维或化纤一拉就断，长度很短。"
        }
    ]
}

# ============================================================
# 洗涤保养
# ============================================================
CARE_GUIDE = {
    "daily_care": [
        "蚕丝被内胆不能水洗、不能干洗、不能机洗——只洗外面的被套就行",
        "被套可以正常机洗，建议用中性洗衣液",
        "有小面积污渍时，用湿毛巾蘸中性洗涤剂轻轻擦拭，自然晾干"
    ],
    "sun_exposure": (
        "蚕丝怕紫外线，暴晒会让蚕丝变脆、发黄。"
        "需要除湿除味时，放在通风阴凉处晾1-2小时就够了，避开正午烈日。"
    ),
    "storage": [
        "不要用真空压缩袋——会把蚕丝压扁结块，回弹不了",
        "叠好后放在透气的棉布袋里",
        "放几粒干燥剂/防潮剂，防止受潮",
        "上面不要压重物",
        "避免和樟脑丸放一起（樟脑丸会让蚕丝蛋白质变性）"
    ],
    "common_mistakes": [
        "误区1：蚕丝被不能晒太阳 → 可以晒，但不能暴晒，1-2小时通风就行",
        "误区2：新被子有味道是质量问题 → 新蚕丝被有轻微蚕蛹味是正常的，通风晾一天就没了",
        "误区3：蚕丝被不暖和 → 蚕丝的保暖性很好，4斤以上冬天完全够用"
    ]
}

# ============================================================
# 售后政策
# ============================================================
POLICIES = {
    "shipping": {
        "method": "顺丰/京东物流",
        "cost": "全国包邮（新疆、西藏、内蒙古等偏远地区需补运费差价）",
        "time": "下单后48小时内发货，正常3-5天到"
    },
    "payment": {
        "method": "货到付款",
        "note": "快递送到后验货再付钱，不用提前转账。也支持微信/支付宝提前付款。"
    },
    "return_policy": {
        "period": "7天无理由退换",
        "condition": "未拆封、不影响二次销售",
        "shipping_cost": "退换运费由我们承担",
        "note": "已拆封使用的，如有质量问题仍可退换"
    },
    "warranty": {
        "period": "3年质保",
        "coverage": "非人为损坏（如开线、跑丝等），免费维修或更换",
        "note": "超过质保期也可以联系我们，酌情处理"
    },
    "inspection": {
        "note": "支持开箱验货，快递员在场时可以打开检查。发现任何问题可以当场拒收。"
    }
}

# ============================================================
# 最新活动（海叔定期更新这里）
# ============================================================
LATEST_NEWS = [
    {
        "date": "2026-05-01",
        "title": "五一上新：子母被新增1.5米规格",
        "content": "应顾客要求，子母被新增200×230cm规格（1斤+3斤），售价1498元。一套搞定四季，最划算。"
    },
    {
        "date": "2026-04-20",
        "title": "喜被定制服务上线",
        "content": "喜被现在可以定制绣字了！新人名字+结婚日期，绣在被套上，独一无二的婚礼礼物。定制不加价。"
    },
    {
        "date": "2026-04-10",
        "title": "老客户回购优惠",
        "content": "凡是买过喜乐姐蚕丝被的老客户，再次购买任意款式立减100元。把截图发给客服即可。"
    }
]
