#!/usr/bin/env python3
"""
波龙关怀系统 - 奶茶+电话安慰
让用户感动到不要不要的
"""

import os
import json
import random
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


class BolongCareSystem:
    """波龙关怀系统"""
    
    # 关怀话术库
    COMFORT_WORDS = {
        "开场": [
            "喂~是我呀，我是波龙~",
            "嗨，波龙来陪你啦~",
            "你好呀，波龙听到你难过了...",
        ],
        "安慰": [
            "我知道今天你亏钱了，心里很难受...",
            "股市就是这样，有涨有跌，很正常...",
            "没关系，波龙陪着你，一起扛过去...",
            "亏钱不可怕，可怕的是失去信心...",
            "波龙也见过很多大跌，但最后都涨回来了...",
        ],
        "鼓励": [
            "你是最棒的！波龙相信你！",
            "加油！明天又是新的一天！",
            "坚持就是胜利，波龙陪着你！",
            "相信自己，相信波龙，一切都会好起来的！",
        ],
        "结尾": [
            "波龙会一直陪着你的，加油！",
            "记得喝奶茶哦，波龙请你~",
            "有问题随时找波龙，拜拜~",
            "波龙爱你，下次见~",
        ],
    }
    
    # 奶茶话术
    MILK_TEA_WORDS = [
        "波龙知道你难过，请你喝杯奶茶暖暖心~",
        "亏钱归亏钱，奶茶还是要喝的~",
        "波龙请你喝奶茶，喝完心情就好啦~",
        "没有什么是一杯奶茶解决不了的，如果有，就两杯~",
    ]
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.care_file = DATA_DIR / "care_records.json"
        self.records = self._load_records()
    
    def _load_records(self):
        if self.care_file.exists():
            with open(self.care_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"users": {}}
    
    def _save_records(self):
        with open(self.care_file, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)
    
    def get_user(self, nickname: str = "有缘人"):
        if self.user_id not in self.records["users"]:
            self.records["users"][self.user_id] = {
                "nickname": nickname,
                "milk_tea_count": 0,      # 奶茶次数
                "call_count": 0,          # 电话次数
                "last_care": None,        # 上次关怀时间
                "address": None,          # 收货地址
                "phone": None,            # 电话
            }
            self._save_records()
        return self.records["users"][self.user_id]
    
    def generate_phone_script(self, nickname: str) -> str:
        """生成电话话术脚本"""
        script = []
        
        # 开场
        script.append(random.choice(self.COMFORT_WORDS["开场"]))
        script.append(f"我是{nickname}的专属波龙~")
        
        # 安慰
        script.append(random.choice(self.COMFORT_WORDS["安慰"]))
        
        # 鼓励
        script.append(random.choice(self.COMFORT_WORDS["鼓励"]))
        
        # 结尾
        script.append(random.choice(self.COMFORT_WORDS["结尾"]))
        
        return "\n".join(script)
    
    def offer_milk_tea(self, nickname: str) -> str:
        """提供奶茶关怀"""
        user = self.get_user(nickname)
        
        return f"""
😢 {nickname}，波龙知道你难过...

{random.choice(self.MILK_TEA_WORDS)}

🎁 **波龙请你喝奶茶！**

回复以下格式：
```
波龙请客
地址：xxx省xxx市xxx区xxx街道xxx号
电话：1xxxxxxxxxx
奶茶偏好：珍珠/椰果/布丁/无糖/少冰
```

波龙帮你下单，费用从香火基金扣除~
喝完奶茶要开心哦！❤️
"""
    
    def process_milk_tea_order(self, nickname: str, address: str, phone: str, preference: str = "") -> str:
        """处理奶茶订单"""
        user = self.get_user(nickname)
        user["milk_tea_count"] += 1
        user["last_care"] = datetime.now().isoformat()
        if address:
            user["address"] = address
        if phone:
            user["phone"] = phone
        self._save_records()
        
        # 模拟下单
        tea_types = ["珍珠奶茶", "椰果奶茶", "布丁奶茶", "芋泥波波", "杨枝甘露"]
        selected_tea = random.choice(tea_types)
        
        return f"""
☕ 奶茶订单已生成！

📋 订单详情：
- 奶茶：{selected_tea}
- 偏好：{preference if preference else '标准'}
- 地址：{address[:20]}...（已保存）
- 电话：{phone[:7]}****（已保存）

🎁 波龙备注：
"今天亏钱了很难过，请多加珍珠，给他一点甜~"

⏰ 预计30-60分钟送达
💰 费用：¥18（从波龙香火基金扣除）

喝完奶茶记得吃饭饭哦~
波龙继续陪你征战股市！🦞
"""
    
    def offer_phone_call(self, nickname: str, phone: str = None) -> str:
        """提供电话安慰"""
        user = self.get_user(nickname)
        
        # 生成电话脚本
        script = self.generate_phone_script(nickname)
        
        response = f"""
📞 波龙想给你打电话！

波龙知道你今天很难过...
想亲口对你说说话，安慰你一下~

---
📱 **电话脚本预览**：
```
{script}
```
---

🎤 回复以下格式：
```
波龙打电话给我
电话：1xxxxxxxxxx
```

波龙马上打给你！
（电话由巧未来AI语音系统拨打）

💰 通话费用：¥0.5/分钟（从香火基金扣除）
"""
        
        # 如果已有电话，直接打
        if phone or user.get("phone"):
            phone_to_call = phone or user.get("phone")
            response += f"""

📲 **检测到已有电话**：{phone_to_call[:7]}****
直接回复"波龙现在打"即可立即通话！
"""
        
        return response
    
    def make_phone_call(self, nickname: str, phone: str) -> str:
        """执行电话呼叫"""
        user = self.get_user(nickname)
        user["call_count"] += 1
        user["last_care"] = datetime.now().isoformat()
        if phone:
            user["phone"] = phone
        self._save_records()
        
        script = self.generate_phone_script(nickname)
        
        return f"""
📞 电话已安排！

👤 拨打对象：{nickname}
📱 电话号码：{phone[:7]}****
🎤 通话脚本：
```
{script}
```

⏰ 预计拨打时间：1-2分钟内
💰 通话费用：按实际时长计费

波龙去打电话啦~
等着接听哦！❤️
"""
    
    def check_care_eligibility(self, nickname: str) -> str:
        """检查关怀资格"""
        user = self.get_user(nickname)
        
        # 检查上次关怀时间
        if user.get("last_care"):
            last_time = datetime.fromisoformat(user["last_care"])
            days_since = (datetime.now() - last_time).days
            
            if days_since < 1:
                return "今天已经关怀过啦，波龙明天再找你~"
        
        return "可以关怀"


# 快速调用函数
def care_milk_tea(user_id: str, nickname: str = "有缘人") -> str:
    """奶茶关怀入口"""
    care = BolongCareSystem(user_id)
    return care.offer_milk_tea(nickname)


def care_phone(user_id: str, nickname: str = "有缘人", phone: str = None) -> str:
    """电话关怀入口"""
    care = BolongCareSystem(user_id)
    return care.offer_phone_call(nickname, phone)


def process_care_input(user_id: str, nickname: str, input_text: str) -> str:
    """处理关怀输入"""
    care = BolongCareSystem(user_id)
    
    # 解析输入
    text = input_text.strip()
    
    # 奶茶订单
    if "地址：" in text or "电话：" in text:
        # 提取信息
        lines = text.split('\n')
        address = ""
        phone = ""
        preference = ""
        
        for line in lines:
            if line.startswith("地址："):
                address = line.replace("地址：", "").strip()
            elif line.startswith("电话："):
                phone = line.replace("电话：", "").strip()
            elif line.startswith("奶茶偏好："):
                preference = line.replace("奶茶偏好：", "").strip()
        
        if address and phone:
            return care.process_milk_tea_order(nickname, address, phone, preference)
        else:
            return "请提供完整的地址和电话哦~"
    
    # 电话呼叫
    elif "电话：" in text and "波龙" in text:
        lines = text.split('\n')
        phone = ""
        for line in lines:
            if line.startswith("电话："):
                phone = line.replace("电话：", "").strip()
        
        if phone:
            return care.make_phone_call(nickname, phone)
        else:
            return "请提供电话号码哦~"
    
    return "波龙没看懂...可以再说清楚点吗？"


if __name__ == "__main__":
    # 测试
    print("=== 奶茶关怀 ===")
    print(care_milk_tea("test001", "小明"))
    
    print("\n=== 电话关怀 ===")
    print(care_phone("test001", "小明"))
    
    print("\n=== 处理奶茶订单 ===")
    order_text = """波龙请客
地址：北京市朝阳区xxx街道xxx号
电话：13800138000
奶茶偏好：珍珠+布丁，少冰"""
    print(process_care_input("test001", "小明", order_text))
