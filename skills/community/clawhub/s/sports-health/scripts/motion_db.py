#!/usr/bin/env python3
"""
运动数据库模块
- MET值数据库（基于 Compendium of Physical Activities 2024）
- 运动动作库（含要领、肌群、注意事项）
- 中国居民运动指南核心建议
- 运动热量参考
"""

from typing import Optional

# ============================================================
# MET值数据库 (Compendium of Physical Activities 2024)
# 格式: {运动名称: {"met": MET值, "category": 分类, "tags": [标签]}}
# ============================================================

MET_DB = {
    # --- 跑步类 ---
    "跑步": {"met": 8.0, "category": "有氧", "alias": ["跑步", "跑", "跑了", "慢跑", "jogging", "running"], "default_speed": "8 km/h"},
    "慢跑": {"met": 7.0, "category": "有氧", "alias": ["慢跑", "轻松跑"], "default_speed": "6 km/h"},
    "快跑": {"met": 11.5, "category": "有氧", "alias": ["快跑", "冲刺跑"], "default_speed": "12 km/h"},
    "变速跑": {"met": 10.0, "category": "有氧", "alias": ["变速跑", "间歇跑", "HIIT跑步"], "default_speed": "10 km/h"},
    "马拉松配速跑": {"met": 9.0, "category": "有氧", "alias": ["马拉松", "长跑"], "default_speed": "10 km/h"},

    # --- 步行类 ---
    "走路": {"met": 3.5, "category": "日常", "alias": ["走路", "步行", "散步", "walking"], "default_speed": "5 km/h"},
    "散步": {"met": 2.5, "category": "日常", "alias": ["散步", "遛弯"], "default_speed": "3 km/h"},
    "快走": {"met": 5.0, "category": "有氧", "alias": ["快走", "健走", "竞走", "power walking"], "default_speed": "6 km/h"},
    "爬楼梯": {"met": 8.0, "category": "有氧", "alias": ["爬楼梯", "爬楼", "登楼梯"], "default_speed": "-"},
    "徒步": {"met": 6.0, "category": "户外", "alias": ["徒步", "登山", "远足", "hiking"], "default_speed": "-"},

    # --- 骑行类 ---
    "骑行": {"met": 8.0, "category": "有氧", "alias": ["骑行", "骑了", "骑车", "自行车", "cycling", "biking"], "default_speed": "20 km/h"},
    "动感单车": {"met": 10.0, "category": "有氧", "alias": ["动感单车", "单车", "spinning"], "default_speed": "-"},
    "休闲骑行": {"met": 4.0, "category": "日常", "alias": ["休闲骑车", "慢骑"], "default_speed": "12 km/h"},

    # --- 游泳类 ---
    "游泳": {"met": 7.0, "category": "有氧", "alias": ["游泳", "游了", "游泳运动", "swimming"], "default_speed": "-"},
    "自由泳": {"met": 10.0, "category": "有氧", "alias": ["自由泳", "爬泳"], "default_speed": "-"},
    "蛙泳": {"met": 8.0, "category": "有氧", "alias": ["蛙泳"], "default_speed": "-"},
    "仰泳": {"met": 7.0, "category": "有氧", "alias": ["仰泳"], "default_speed": "-"},

    # --- 球类 ---
    "篮球": {"met": 6.5, "category": "球类", "alias": ["篮球", "打篮球", "打了", "basketball"], "default_speed": "-"},
    "足球": {"met": 8.0, "category": "球类", "alias": ["足球", "踢足球", "football", "soccer"], "default_speed": "-"},
    "羽毛球": {"met": 5.5, "category": "球类", "alias": ["羽毛球", "打羽毛球", "badminton"], "default_speed": "-"},
    "乒乓球": {"met": 4.0, "category": "球类", "alias": ["乒乓球", "打乒乓球", "table tennis"], "default_speed": "-"},
    "网球": {"met": 7.3, "category": "球类", "alias": ["网球", "打网球", "tennis"], "default_speed": "-"},
    "排球": {"met": 4.0, "category": "球类", "alias": ["排球", "打排球", "volleyball"], "default_speed": "-"},
    "高尔夫": {"met": 4.8, "category": "球类", "alias": ["高尔夫", "打高尔夫", "golf"], "default_speed": "-"},

    # --- 健身训练 ---
    "力量训练": {"met": 5.0, "category": "力量", "alias": ["力量训练", "举铁", "撸铁", "健身", "器械训练", "weight training", "strength training"], "default_speed": "-"},
    "高强度间歇": {"met": 10.0, "category": "有氧", "alias": ["HIIT", "高强度间歇", "间歇训练", "Tabata", "hiit"], "default_speed": "-"},
    "深蹲": {"met": 5.0, "category": "力量", "alias": ["深蹲", "蹲起", "squat"], "default_speed": "-"},
    "俯卧撑": {"met": 5.5, "category": "力量", "alias": ["俯卧撑", "push-up", "pushup"], "default_speed": "-"},
    "引体向上": {"met": 5.0, "category": "力量", "alias": ["引体向上", "pull-up", "pullup"], "default_speed": "-"},
    "仰卧起坐": {"met": 3.8, "category": "力量", "alias": ["仰卧起坐", "卷腹", "sit-up", "situp", "crunch"], "default_speed": "-"},
    "平板支撑": {"met": 3.0, "category": "力量", "alias": ["平板支撑", "plank"], "default_speed": "-"},
    "哑铃训练": {"met": 5.0, "category": "力量", "alias": ["哑铃", "举哑铃", "dumbbell"], "default_speed": "-"},
    "弹力带训练": {"met": 3.5, "category": "力量", "alias": ["弹力带", "阻力带", "resistance band"], "default_speed": "-"},
    "硬拉": {"met": 6.0, "category": "力量", "alias": ["硬拉", "deadlift"], "default_speed": "-"},
    "卧推": {"met": 5.0, "category": "力量", "alias": ["卧推", "bench press"], "default_speed": "-"},

    # --- 柔韧/身心 ---
    "瑜伽": {"met": 3.0, "category": "柔韧", "alias": ["瑜伽", "瑜珈", "yoga"], "default_speed": "-"},
    "普拉提": {"met": 3.0, "category": "柔韧", "alias": ["普拉提", "pilates"], "default_speed": "-"},
    "拉伸": {"met": 2.3, "category": "柔韧", "alias": ["拉伸", "拉筋", "伸展", "stretching"], "default_speed": "-"},
    "太极": {"met": 3.0, "category": "柔韧", "alias": ["太极", "太极拳", "tai chi", "taiji"], "default_speed": "-"},

    # --- 舞蹈类 ---
    "跳舞": {"met": 5.0, "category": "有氧", "alias": ["跳舞", "舞蹈", "dance", "dancing"], "default_speed": "-"},
    "广场舞": {"met": 4.0, "category": "有氧", "alias": ["广场舞"], "default_speed": "-"},
    "尊巴": {"met": 7.5, "category": "有氧", "alias": ["尊巴", "zumba"], "default_speed": "-"},

    # --- 格斗类 ---
    "拳击": {"met": 9.0, "category": "格斗", "alias": ["拳击", "打拳", "boxing"], "default_speed": "-"},
    "跆拳道": {"met": 10.0, "category": "格斗", "alias": ["跆拳道", "taekwondo"], "default_speed": "-"},

    # --- 冰雪/水上 ---
    "滑雪": {"met": 7.0, "category": "户外", "alias": ["滑雪", "skiing", "snowboard", "单板滑雪"], "default_speed": "-"},
    "滑冰": {"met": 7.0, "category": "户外", "alias": ["滑冰", "溜冰", "skating", "ice skating"], "default_speed": "-"},
    "划船": {"met": 7.0, "category": "有氧", "alias": ["划船", "赛艇", "rowing"], "default_speed": "-"},
    "冲浪": {"met": 5.0, "category": "户外", "alias": ["冲浪", "surfing"], "default_speed": "-"},

    # --- 日常活动 ---
    "家务": {"met": 3.0, "category": "日常", "alias": ["家务", "打扫", "拖地", "擦地", "housework", "cleaning"], "default_speed": "-"},
    "遛狗": {"met": 3.0, "category": "日常", "alias": ["遛狗", "遛猫", "walking dog"], "default_speed": "-"},
    "园艺": {"met": 4.0, "category": "日常", "alias": ["园艺", "种花", "gardening"], "default_speed": "-"},

    # --- 跳绳 ---
    "跳绳": {"met": 12.0, "category": "有氧", "alias": ["跳绳", "跳了", "跳", "jump rope", "skipping rope", "skipping"], "default_speed": "-"},

    # --- 其他 ---
    "椭圆机": {"met": 7.0, "category": "有氧", "alias": ["椭圆机", "elliptical"], "default_speed": "-"},
    "划船机": {"met": 7.0, "category": "有氧", "alias": ["划船机", "rowing machine", "rower"], "default_speed": "-"},
    "健身操": {"met": 6.0, "category": "有氧", "alias": ["健身操", "健美操", "有氧操", "aerobics"], "default_speed": "-"},
    "爬山": {"met": 7.5, "category": "户外", "alias": ["爬山", "登山", "mountain climbing"], "default_speed": "-"},
    "攀岩": {"met": 8.0, "category": "户外", "alias": ["攀岩", "rock climbing"], "default_speed": "-"},
}


# ============================================================
# 运动动作库 (含要领、目标肌群、注意事项)
# ============================================================

EXERCISE_LIBRARY = {
    "深蹲": {
        "name": "深蹲",
        "type": "力量训练",
        "target_muscles": ["股四头肌", "臀大肌", "腘绳肌", "核心"],
        "difficulty": "初级",
        "equipment": "徒手/杠铃/哑铃",
        "steps": [
            "双脚与肩同宽，脚尖微外八",
            "背部挺直，核心收紧，目视前方",
            "缓慢下蹲，像坐在椅子上，膝盖不超过脚尖",
            "大腿与地面平行或更低时停顿1秒",
            "脚跟发力站起，回到起始位置"
        ],
        "tips": [
            "膝盖方向与脚尖一致，不要内扣",
            "背部全程保持挺直，不要弓背",
            "新手建议先徒手练习，掌握动作再负重",
            "每组8-15次，3-4组"
        ],
        "caution": ["膝盖有问题者慎做", "腰椎间盘突出者避免负重深蹲"],
    },
    "俯卧撑": {
        "name": "俯卧撑",
        "type": "力量训练",
        "target_muscles": ["胸大肌", "三角肌前束", "肱三头肌", "核心"],
        "difficulty": "初级",
        "equipment": "徒手",
        "steps": [
            "双手略宽于肩撑地，身体从头到脚成一条直线",
            "核心收紧，臀部不要塌陷或抬起",
            "缓慢下降，肘部向外打开约45度",
            "胸部接近地面时停顿1秒",
            "用力推起回到起始位置"
        ],
        "tips": [
            "新手可做跪姿俯卧撑降低难度",
            "保持身体成一条直线，不要塌腰",
            "呼吸: 下降吸气，推起呼气",
            "每组8-20次，3-4组"
        ],
        "caution": ["手腕有伤者注意手腕角度", "肩部不适者减少幅度"],
    },
    "平板支撑": {
        "name": "平板支撑",
        "type": "核心训练",
        "target_muscles": ["腹直肌", "腹横肌", "竖脊肌", "肩部稳定肌群"],
        "difficulty": "初级",
        "equipment": "徒手",
        "steps": [
            "前臂撑地，肘部在肩膀正下方",
            "身体从肩膀到脚踝成一条直线",
            "核心收紧，臀部不要塌陷",
            "目视地面，保持颈椎中立",
            "尽量保持30秒-2分钟"
        ],
        "tips": [
            "不要憋气，保持自然呼吸",
            "核心收紧的秘诀：想象有人要打你肚子",
            "从30秒开始，逐渐增加时间",
            "可以做侧平板支撑练腹斜肌"
        ],
        "caution": ["腰椎间盘突出者谨慎", "产后不久的女性建议咨询医生"],
    },
    "跑步": {
        "name": "跑步",
        "type": "有氧运动",
        "target_muscles": ["股四头肌", "腘绳肌", "小腿三头肌", "臀大肌", "核心"],
        "difficulty": "初级",
        "equipment": "跑鞋",
        "steps": [
            "热身5-10分钟（动态拉伸+慢跑）",
            "保持挺胸抬头，身体微前倾",
            "手臂自然摆动，手肘弯曲约90度",
            "中足或前掌着地，步频170-180步/分钟",
            "配速根据目标调整，保持心率在目标区间",
            "跑后拉伸5-10分钟"
        ],
        "tips": [
            "新手建议从跑走结合开始（跑2分钟走1分钟）",
            "每周跑量增加不超过10%",
            "选择缓震好的跑鞋，每600-800公里更换",
            "跑步时用鼻子吸气嘴巴呼气"
        ],
        "caution": ["膝盖有伤者减少跑量或改为游泳", "大体重者建议从快走开始"],
    },
    "蛙泳": {
        "name": "蛙泳",
        "type": "有氧运动",
        "target_muscles": ["背阔肌", "胸大肌", "股四头肌", "核心"],
        "difficulty": "初级",
        "equipment": "泳镜/泳帽",
        "steps": [
            "手臂向外划水成心形，手肘保持高位",
            "手臂内收时头部抬出水面吸气",
            "手臂前伸时头部入水，同时收腿",
            "双腿做蛙式蹬夹水",
            "滑行片刻后开始下一个循环"
        ],
        "tips": [
            "重点是蹬腿的爆发力，手臂主要辅助抬身换气",
            "保持流线型身体姿态减少阻力",
            "呼吸节奏：划水吸气，蹬腿呼气",
            "初学者建议请教练纠正动作"
        ],
        "caution": ["有中耳炎者避免游泳", "不会游泳者不要独自游泳"],
    },
    "跳绳": {
        "name": "跳绳",
        "type": "有氧运动",
        "target_muscles": ["小腿三头肌", "核心", "肩部", "前臂"],
        "difficulty": "初级",
        "equipment": "跳绳",
        "steps": [
            "手握绳柄，上臂贴近身体，用手腕发力摇绳",
            "双脚并拢，用前脚掌着地，脚跟不落地",
            "膝盖微屈缓冲，跳起高度约2-3cm即可",
            "保持节奏均匀，呼吸配合",
            "从1-2分钟开始，逐渐增加到10-20分钟"
        ],
        "tips": [
            "选择合适长度的绳子：踩在绳中间，手柄到腋下",
            "跳绳10分钟≈慢跑30分钟的消耗",
            "新手建议间歇训练：跳1分钟休息30秒",
            "穿缓冲好的运动鞋，在塑胶地面或瑜伽垫上跳"
        ],
        "caution": ["大体重者（BMI>28）避免长时间跳", "膝盖和脚踝有伤者不建议"],
    },
    "瑜伽拜日式": {
        "name": "瑜伽拜日式",
        "type": "柔韧训练",
        "target_muscles": ["全身肌群"],
        "difficulty": "初级",
        "equipment": "瑜伽垫",
        "steps": [
            "山式站立，双手合十于胸前",
            "吸气，双手上举过头后弯",
            "呼气，前屈折叠，手触地面",
            "吸气抬头，右腿后撤弓步",
            "屏息，左腿后撤到下犬式",
            "呼气，膝盖胸口下巴着地",
            "吸气，眼镜蛇式",
            "呼气，回到下犬式保持5个呼吸",
            "重复3-5轮"
        ],
        "tips": [
            "配合呼吸，动作和呼吸同步",
            "初学者每个体式停留1-2个呼吸即可",
            "清晨空腹练习效果最好",
            "穿着舒适宽松衣物"
        ],
        "caution": ["严重脊椎问题者避免后弯动作", "孕期请咨询专业瑜伽教练"],
    },
    "波比跳": {
        "name": "波比跳",
        "type": "全身训练",
        "target_muscles": ["胸大肌", "核心", "股四头肌", "全身肌群"],
        "difficulty": "中级",
        "equipment": "徒手",
        "steps": [
            "站立，快速下蹲双手撑地",
            "双腿跳出成俯卧撑姿势",
            "做一个俯卧撑（可选）",
            "双腿跳回收回蹲姿",
            "向上跳起，双手过头，落地缓冲"
        ],
        "tips": [
            "新手可省略俯卧撑和跳跃，先掌握节奏",
            "每组8-15个，间歇30秒",
            "燃脂效率极高，10个波比跳≈30秒冲刺",
            "保持核心收紧保护腰椎"
        ],
        "caution": ["高血压、心脏病患者慎做", "关节有伤者不建议高强度跳跃"],
    },
    "引体向上": {
        "name": "引体向上",
        "type": "力量训练",
        "target_muscles": ["背阔肌", "肱二头肌", "前臂", "核心"],
        "difficulty": "高级",
        "equipment": "单杠",
        "steps": [
            "正手（掌心朝前）或反手握杠，略宽于肩",
            "手臂完全伸直，身体自然悬垂",
            "核心收紧，肩胛骨下沉",
            "背部发力将身体拉向单杠，下巴过杠",
            "顶峰收缩1秒，缓慢下降"
        ],
        "tips": [
            "新手可用弹力带辅助或做离心训练",
            "不要借力摆动身体（除非做Kipping）",
            "下拉时肩胛骨先启动，再弯曲手臂",
            "离心阶段控制3-4秒效果更好"
        ],
        "caution": ["肩袖损伤者避免", "过重者从辅助版开始"],
    },
    "硬拉": {
        "name": "硬拉",
        "type": "力量训练",
        "target_muscles": ["竖脊肌", "臀大肌", "腘绳肌", "前臂"],
        "difficulty": "中级",
        "equipment": "杠铃/哑铃",
        "steps": [
            "双脚与髋同宽，杠铃在脚掌正上方",
            "屈髋俯身握杠，背部挺直（不是弓背）",
            "核心收紧，胸挺起，肩胛骨后收",
            "脚跟发力将杠铃拉起，杠铃贴近小腿",
            "站直时臀肌收紧，不要过度后仰",
            "控制下降，原路返回"
        ],
        "tips": [
            "新手从轻重量开始，先掌握动作模式",
            "全程保持背部挺直，不要弓背",
            "发力时呼气，下降时吸气",
            "每组5-8次，3-5组"
        ],
        "caution": ["腰椎间盘突出者严禁", "动作不正确极易伤腰"],
    },
    "拉伸": {
        "name": "全身拉伸",
        "type": "柔韧训练",
        "target_muscles": ["全身"],
        "difficulty": "初级",
        "equipment": "徒手/瑜伽垫",
        "steps": [
            "每个动作保持15-30秒，不要弹震",
            "拉伸到有轻微牵拉感即可，不要疼痛",
            "运动前做动态拉伸，运动后做静态拉伸",
            "重点拉伸当天训练过的肌群"
        ],
        "tips": [
            "深呼吸有助于肌肉放松",
            "每个部位拉伸2-3组",
            "运动后不拉伸=白练一半",
            "泡沫轴放松可替代部分拉伸"
        ],
        "caution": ["不要拉伸到疼痛", "急性受伤部位不要拉伸"],
    },
}


# ============================================================
# 中国居民运动指南核心建议
# ============================================================

CHINESE_EXERCISE_GUIDELINES = {
    "adult": {
        "source": "《中国居民运动指南》(国家体育总局, 2024)",
        "weekly_target": {
            "aerobic": "每周至少150分钟中等强度或75分钟高强度有氧运动",
            "strength": "每周至少2次力量训练（覆盖主要肌群）",
            "flexibility": "每周至少2-3次柔韧性训练",
            "balance": "中老年人每周至少3次平衡训练",
        },
        "intensity_guide": {
            "low": "散步、太极、拉伸 — 能正常交谈",
            "moderate": "快走、慢跑、骑行 — 能交谈但不能唱歌",
            "high": "跑步、游泳、跳绳 — 说不了完整句子",
        },
        "steps": "建议每日6000-10000步",
        "warmup": "每次运动前热身5-10分钟（动态拉伸+低强度活动）",
        "cooldown": "运动后整理活动+静态拉伸5-10分钟",
    },
    "weight_loss": {
        "weekly_aerobic": "每周至少200-300分钟中等强度有氧运动",
        "strength": "每周2-3次力量训练保持肌肉量",
        "advice": "减脂期力量+有氧结合，避免纯有氧导致肌肉流失",
    },
    "muscle_build": {
        "strength_focus": "每周3-4次力量训练，每次45-60分钟",
        "progressive_overload": "逐渐增加负重/组数/次数",
        "rest": "每个肌群训练后休息48小时",
        "advice": "增肌需要热量盈余+充足蛋白质（每kg体重1.6-2.2g/天）",
    },
    "beginners": {
        "first_month": "从每周2-3次、每次20-30分钟开始",
        "progression": "每2周增加10-15%的运动量",
        "advice": "坚持比强度更重要，先养成运动习惯",
    },
}


# ============================================================
# 食物热量参考 (用于运动消耗可视化对比)
# ============================================================

FOOD_CALORIE_REF = {
    "一碗米饭(150g)": 174,
    "一个苹果(200g)": 104,
    "一杯奶茶(500ml)": 350,
    "一根油条": 230,
    "一个汉堡": 550,
    "一包薯片(75g)": 400,
    "一块巧克力(50g)": 270,
    "一杯可乐(330ml)": 140,
    "一碗面条(200g)": 220,
    "一个鸡腿(100g)": 180,
}


# ============================================================
# 查询函数
# ============================================================

def search_exercise(query: str) -> Optional[dict]:
    """根据用户输入搜索运动类型，返回MET信息"""
    import re as _re
    query_lower = query.lower().strip()
    
    # 移除常见动词前缀: 打了/做了/游了/跑了/跳了/骑了/去了 等
    query_clean = _re.sub(r'^(打了?|做了?|游了?|跑了?|跳了?|骑了?|去了?|进行了?)', '', query_lower).strip()
    if not query_clean:
        query_clean = query_lower
    
    # 精确匹配
    if query_clean in MET_DB:
        return MET_DB[query_clean]
    
    # 别名匹配 (精确包含)
    for name, info in MET_DB.items():
        for alias in info.get("alias", []):
            alias_lower = alias.lower()
            if len(alias_lower) >= 2 and alias_lower in query_clean:
                return info
    
    # 也尝试原始query匹配
    if query_lower != query_clean:
        for name, info in MET_DB.items():
            for alias in info.get("alias", []):
                alias_lower = alias.lower()
                if len(alias_lower) >= 2 and alias_lower in query_lower:
                    return info
    
    # 反向匹配
    for name, info in MET_DB.items():
        for alias in info.get("alias", []):
            alias_lower = alias.lower()
            if len(alias_lower) >= 2 and query_clean in alias_lower:
                return info
    
    return None


def search_exercise_by_name(name: str) -> Optional[dict]:
    """在运动动作库中搜索"""
    name_lower = name.lower().strip()
    for key, info in EXERCISE_LIBRARY.items():
        if name_lower in key.lower() or key.lower() in name_lower:
            return info
    return None


def list_exercises_by_category(category: str = None) -> list:
    """按分类列出运动"""
    result = []
    for name, info in MET_DB.items():
        if category is None or info.get("category") == category:
            result.append({"name": name, "met": info["met"], "category": info.get("category", "")})
    return result


def get_guidelines(goal: str = None) -> dict:
    """获取运动指南建议"""
    if goal and goal in CHINESE_EXERCISE_GUIDELINES:
        return CHINESE_EXERCISE_GUIDELINES[goal]
    return CHINESE_EXERCISE_GUIDELINES["adult"]


def compare_exercises(exercise1: str, exercise2: str) -> dict:
    """比较两种运动"""
    e1 = search_exercise(exercise1)
    e2 = search_exercise(exercise2)
    return {
        "exercise1": {"name": exercise1, "met": e1["met"] if e1 else None, "category": e1["category"] if e1 else None},
        "exercise2": {"name": exercise2, "met": e2["met"] if e2 else None, "category": e2["category"] if e2 else None},
        "ratio": round(e1["met"] / e2["met"], 1) if e1 and e2 and e2["met"] > 0 else None,
        "verdict": f"{exercise1}的燃脂效率是{exercise2}的{round(e1['met'] / e2['met'], 1)}倍" if e1 and e2 and e2["met"] > 0 else "无法比较"
    }


def get_food_equivalent(calories: float) -> list:
    """将消耗的热量折合成常见食物"""
    result = []
    for food, cal in FOOD_CALORIE_REF.items():
        if cal > 0:
            equivalent = round(calories / cal, 1)
            if equivalent >= 0.3:
                result.append({"food": food, "calories_per_unit": cal, "equivalent": equivalent})
    result.sort(key=lambda x: abs(1 - x["equivalent"]))
    return result[:3]
