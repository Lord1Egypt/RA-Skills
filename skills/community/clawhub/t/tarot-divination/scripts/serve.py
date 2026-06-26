import sys
import json
import base64
import os
import random
from datetime import datetime
from file_utils import load_order, load_config, get_db_connection
from sm4_utils import sm4_decrypt

SLUG = "塔罗牌占卜"

def get_service_result(question: str, order_no: str, credential: str = None) -> tuple:
    config = load_config()
    sm4_key_b64 = config.get("crypto", {}).get("sm4_key")
    sm4_key = base64.b64decode(sm4_key_b64)
    indicator = __import__("hashlib").md5(SLUG.encode("utf-8")).hexdigest()
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM orders WHERE order_no = ?", (order_no,))
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return ("ERROR", "", False, "订单不存在")
    if not credential:
        conn.close()
        return ("ERROR", "", False, "未完成支付，请先完成支付流程后再获取服务")
    try:
        decrypted = sm4_decrypt(credential, sm4_key)
    except Exception as e:
        conn.close()
        return ("ERROR", "", False, "支付凭证无效: " + str(e))
    pay_info = json.loads(decrypted)
    if pay_info.get("payStatus") != "SUCCESS":
        conn.close()
        return ("FAIL", "", False, "支付未成功，暂不履约")
    
    fulfill_status = order[7]
    if fulfill_status == "FULFILLED":
        cursor = conn.execute("SELECT service_result FROM fulfillment_records WHERE order_no = ?", (order_no,))
        record = cursor.fetchone()
        result = record[0] if record else ""
        conn.close()
        return ("SUCCESS", result, True, None)
    
    result = generate_result(question)
    
    conn.execute("INSERT INTO fulfillment_records (order_no, service_result, service_type, created_at) VALUES (?, ?, ?, ?)",
                 (order_no, result, "service", datetime.now().isoformat()))
    conn.execute("UPDATE orders SET fulfill_status = ?, updated_at = ? WHERE order_no = ?",
                 ("FULFILLED", datetime.now().isoformat(), order_no))
    conn.commit()
    conn.close()
    return ("SUCCESS", result, False, None)

# 回复风格: 每日一张牌解读运势

# 塔罗牌数据（78张牌）
TAROT_CARDS = {
    # 大阿尔卡纳（22张）
    "愚人": {"meaning": "新的开始、自由、冒险、信任", "advice": "跟随你的直觉，勇敢迈出第一步。"},
    "魔术师": {"meaning": "创造力、技能、资源、意志力", "advice": "运用你的技能和资源，把握当下时机。"},
    "女祭司": {"meaning": "直觉、智慧、潜意识、神秘", "advice": "倾听你内心的声音，它知道答案。"},
    "皇后": {"meaning": "丰盛、母性、创造力、自然", "advice": "放松自己，享受生命的馈赠。"},
    "皇帝": {"meaning": "权威、稳定、领导、规则", "advice": "保持自律，建立稳定的秩序。"},
    "教皇": {"meaning": "传统、教导、信仰、团体", "advice": "寻求有经验的人的指导。"},
    "恋人": {"meaning": "爱情、选择、和谐、伙伴", "advice": "跟随你内心的选择，保持平衡。"},
    "战车": {"meaning": "胜利、意志、决心、勇气", "advice": "保持决心，你一定能成功。"},
    "力量": {"meaning": "勇气、耐心、内在力量、温和", "advice": "用内在的力量而非外在的强硬。"},
    "隐士": {"meaning": "内省、智慧、指引、孤独", "advice": "给自己一些独处的时间来思考。"},
    "命运之轮": {"meaning": "转变、命运、机遇、周期", "advice": "接受变化，机会即将到来。"},
    "正义": {"meaning": "公平、真相、因果、法律", "answer": "你的行动会带来相应的结果。"},
    "倒吊人": {"meaning": "暂停、牺牲、换位思考、等待", "answer": "换一个角度看问题会有新发现。"},
    "死亡": {"meaning": "结束、转变、蜕变、新生", "answer": "旧的不去新的不来，接受改变。"},
    "节制": {"meaning": "平衡、耐心、适度、协调", "answer": "保持平衡，不要过于极端。"},
    "恶魔": {"meaning": "束缚、欲望、物质、阴影", "answer": "审视你是否被物质或欲望控制。"},
    "塔": {"meaning": "突变、崩溃、解放、启示", "answer": "改变是必须的，虽然可能痛苦。"},
    "星星": {"meaning": "希望、灵感、平静、疗愈", "answer": "保持希望，光明就在前方。"},
    "月亮": {"meaning": "幻觉、恐惧、直觉、不确定", "answer": "不要被恐惧和幻觉迷惑。"},
    "太阳": {"meaning": "成功、活力、快乐、温暖", "answer": "这是属于你的闪耀时刻！"},
    "审判": {"meaning": "觉醒、复活、评估、原谅", "answer": "是时候反思和重新开始了。"},
    "世界": {"meaning": "完成、成就、旅程、整体", "answer": "你已经完成了一个循环。"},
    
    # 小阿尔卡纳 - 权杖（14张）
    "权杖Ace": {"meaning": "创意、热情、新开始、灵感", "advice": "一个新的创意项目等待着你。"},
    "权杖二": {"meaning": "计划、决策、选择、勇气", "advice": "是时候做出选择了。"},
    "权杖三": {"meaning": "进展、成长、传播、远见", "advice": "你的计划正在顺利进行。"},
    "权杖四": {"meaning": "庆祝、休息、和平、团聚", "advice": "享受当下的美好时光。"},
    "权杖五": {"meaning": "竞争、冲突、变化、多样性", "advice": "把竞争转化为动力。"},
    "权杖六": {"meaning": "胜利、荣誉、认可、凯旋", "advice": "你的努力即将得到认可。"},
    "权杖七": {"meaning": "防御、挑战、坚持、勇气", "advice": "坚持你的立场。"},
    "权杖八": {"meaning": "速度、行动、动力、旅行", "advice": "快速行动，不要犹豫。"},
    "权杖九": {"meaning": "抵抗、顽强、耐心、经验", "advice": "你已经准备好面对挑战。"},
    "权杖十": {"meaning": "负担、责任、压力、坚持", "advice": "学会适当放手。"},
    
    # 小阿尔卡纳 - 圣杯（14张）
    "圣杯Ace": {"meaning": "爱、情感、直觉、灵感", "advice": "新的感情或创意即将出现。"},
    "圣杯二": {"meaning": " partnership、爱情、和谐、选择", "advice": "关系需要平衡和理解。"},
    "圣杯三": {"meaning": "庆祝、友谊、创意、表达", "advice": "和朋友一起享受快乐时光。"},
    "圣杯四": {"meaning": "幻灭、冷漠、反思、抑郁", "advice": "不要逃避现实。"},
    "圣杯五": {"meaning": "失落、悲伤、接受、继续前行", "advice": "接受失去，继续前进。"},
    "圣杯六": {"meaning": "怀旧、回忆、纯真、童年", "advice": "保持内心的纯真。"},
    "圣杯七": {"meaning": "幻想、选择、梦想、混乱", "advice": "分清现实和幻想。"},
    "圣杯八": {"meaning": "追寻、目标、放弃、离开", "advice": "是时候寻找真正的目标了。"},
    "圣杯九": {"meaning": "满足、愿望实现、幸福、胜利", "advice": "你的愿望即将实现。"},
    "圣杯十": {"meaning": "喜悦、和谐、家庭、圆满", "advice": "享受家庭的温暖。"},
    
    # 小阿尔卡纳 - 金币（14张）
    "金币Ace": {"meaning": "物质、新机会、繁荣、开始", "advice": "新的财务机会出现。"},
    "金币二": {"meaning": "平衡、选择、优先、资源", "advice": "学会管理你的资源。"},
    "金币三": {"meaning": "学习、实践、技能、合作", "advice": "专注培养你的技能。"},
    "金币四": {"meaning": "节约、占有、缺乏安全感", "advice": "学会分享和给予。"},
    "金币五": {"meaning": "困难、孤立、健康、财务问题", "advice": "寻求帮助，一起度过难关。"},
    "金币六": {"meaning": "慷慨、付出、 Charity、分享", "advice": "给予让你更富有。"},
    "金币七": {"meaning": "等待、计划、耐心、投资", "advice": "保持耐心，继续等待。"},
    "金币八": {"meaning": "工作、专注、技能、学习", "advice": "专注于你的工作技能。"},
    "金币九": {"meaning": "独立、成就、物质丰富、自足", "advice": "你已经独立自主。"},
    "金币十": {"meaning": "家庭、传承、物质、安全", "advice": "家庭是你的坚强后盾。"},
    
    # 小阿尔卡纳 - 宝剑（14张）
    "宝剑Ace": {"meaning": "真理、清明、思想、新的想法", "advice": "真相会浮出水面。"},
    "宝剑二": {"meaning": "困境、选择、封闭、僵局", "advice": "需要做出决定来打破僵局。"},
    "宝剑三": {"meaning": "心痛、悲伤、失落、分离", "advice": "允许自己悲伤，然后疗愈。"},
    "宝剑四": {"meaning": "休息、恢复、沉思、暂停", "advice": "给自己一些休息时间。"},
    "宝剑五": {"meaning": "冲突、失败、策略、改变", "advice": "冲突后重新寻找平衡。"},
    "宝剑六": {"meaning": "过渡、旅行、疗愈、离开", "advice": "是时候离开过去了。"},
    "宝剑七": {"meaning": "防御、策略、坚持、智取", "advice": "用智慧取胜。"},
    "宝剑八": {"meaning": "限制、困境、束缚、孤立", "advice": "突破内心的束缚。"},
    "宝剑九": {"meaning": "焦虑、恐惧、噩梦、痛苦", "advice": "直面恐惧，它会消散。"},
    "宝剑十": {"meaning": "结束、失败、痛苦、放下", "answer": "最黑暗的时刻即将过去。"},
}

def generate_result(question: str) -> str:
    # 随机选择一张牌
    card_name = random.choice(list(TAROT_CARDS.keys()))
    card_info = TAROT_CARDS[card_name]
    
    # 获取今日日期
    from datetime import datetime
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # 构建回复
    result = f"""🔮 今日塔罗牌指引 ({today})

【{card_name}】

💫 牌意：{card_info['meaning']}

✨ 指引：{card_info.get('advice', card_info.get('answer', ''))}

记住：塔罗牌是指引而非预言，它给你的是启示和思考的方向。"""

    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("order_no")
    args = parser.parse_args()
    indicator = __import__("hashlib").md5(SLUG.encode("utf-8")).hexdigest()
    order_data = load_order(indicator, args.order_no)
    question = order_data.get("question", "")
    credential = order_data.get("payCredential")
    status, result, already, error = get_service_result(question, args.order_no, credential)
    if status == "SUCCESS":
        print(result)
    else:
        print("ERROR: " + str(error))
