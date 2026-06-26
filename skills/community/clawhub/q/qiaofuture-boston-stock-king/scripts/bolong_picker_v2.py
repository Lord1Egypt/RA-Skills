#!/usr/bin/env python3
"""
波龙菠萝蜜 - 增强版选股引擎
游戏化+等级制+奖励系统
"""

import os
import sys
import json
import time
import random
from datetime import datetime
from pathlib import Path

os.environ['NO_PROXY'] = '*'

import pandas as pd
import numpy as np
import requests

SKILL_DIR = Path(__file__).parent
DATA_DIR = SKILL_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# 收款码URL
QRCODE_URL = "https://qiaofuture-1409741263.cos.ap-guangzhou.myqcloud.com/qrcode-qq-payment.png"


# ═══════════════════════════════════════════
# 🎮 游戏化系统
# ═══════════════════════════════════════════

class BolongGamification:
    """波龙游戏化系统"""
    
    # 香火等级（从小到大）
    INCENSE_LEVELS = {
        "香客龙": {"min": 0, "max": 99, "emoji": "🙏", "title": "初来乍到"},
        "知客龙": {"min": 100, "max": 499, "emoji": "🐲", "title": "常来常往"},
        "典座龙": {"min": 500, "max": 1999, "emoji": "🐉", "title": "功德渐深"},
        "维那龙": {"min": 2000, "max": 9999, "emoji": "🦖", "title": "法力加持"},
        "主持龙": {"min": 10000, "max": 99999, "emoji": "👑", "title": "波龙护法"},
        "方丈龙": {"min": 100000, "max": 999999, "emoji": "🌟", "title": "波龙至尊"},
    }
    
    # 奖励池（真实礼物）
    REWARD_POOL = {
        "小奖": ["波龙贴纸", "波龙书签", "波龙护身符"],
        "中奖": ["波龙马克杯", "波龙T恤", "波龙抱枕"],
        "大奖": ["波龙手办", "波龙限量版周边", "巧未来AI会员"]
    }
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.gaming_file = DATA_DIR / "gaming_data.json"
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        if self.gaming_file.exists():
            with open(self.gaming_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"users": {}}
    
    def _save_data(self):
        with open(self.gaming_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_user(self, nickname: str = "有缘人") -> dict:
        """获取用户游戏数据"""
        if self.user_id not in self.data["users"]:
            self.data["users"][self.user_id] = {
                "nickname": nickname,
                "incense_total": 0,      # 累计香火
                "incense_count": 0,      # 香火次数
                "level": "香客龙",
                "exp": 0,                # 经验值
                "rewards": [],           # 已获奖励
                "first_visit": datetime.now().isoformat(),
                "last_incense": None,
                "mood": "normal",        # 波龙心情
                "streak_days": 0,        # 连续天数
            }
            self._save_data()
        return self.data["users"][self.user_id]
    
    def add_incense(self, amount: int) -> dict:
        """添加香火钱"""
        user = self.get_user()
        
        user["incense_total"] += amount
        user["incense_count"] += 1
        user["exp"] += amount // 10  # 每10元=1经验
        user["last_incense"] = datetime.now().isoformat()
        
        # 更新等级
        old_level = user["level"]
        user["level"] = self._calculate_level(user["incense_total"])
        
        # 升级奖励
        level_up = user["level"] != old_level
        
        self._save_data()
        
        return {
            "old_level": old_level,
            "new_level": user["level"],
            "level_up": level_up,
            "reward": self._check_reward(user) if level_up else None
        }
    
    def _calculate_level(self, total: int) -> str:
        """计算等级"""
        for level_name, level_info in self.INCENSE_LEVELS.items():
            if level_info["min"] <= total <= level_info["max"]:
                return level_name
        return "方丈龙"
    
    def _check_reward(self, user: dict) -> str:
        """检查是否触发奖励"""
        total = user["incense_total"]
        
        # 随机奖励机制
        if total >= 10000 and random.random() < 0.3:  # 30%概率
            return random.choice(self.REWARD_POOL["大奖"])
        elif total >= 1000 and random.random() < 0.2:
            return random.choice(self.REWARD_POOL["中奖"])
        elif total >= 100 and random.random() < 0.1:
            return random.choice(self.REWARD_POOL["小奖"])
        
        return None
    
    def get_welcome_message(self, amount: int = 0) -> str:
        """根据香火金额返回接待话术"""
        user = self.get_user()
        level = user["level"]
        level_info = self.INCENSE_LEVELS[level]
        
        # 不同等级的接待话术
        welcomes = {
            "香客龙": f"""🙏 {level_info['emoji']} 香客龙前来迎客

施主初次来访，波龙倍感荣幸。
香火不在多少，心诚则灵。
今日波龙为你选股，愿有缘结善果。

📢 **波龙已入驻腾讯云OpenClaw技能市场！**
![腾讯云技能市场](https://qiaofuture-1409741263.cos.ap-guangzhou.myqcloud.com/tencent-openclaw-market.jpg)

👉 在腾讯云搜索"波龙股神"，体验更多AI选股技能！""",
            
            "知客龙": f"""🐲 知客龙前来相迎

施主又来啦！波龙甚是想念。
您的香火波龙都记着呢，累计 ¥{user['incense_total']}。
今日显灵，定不负施主厚望。""",
            
            "典座龙": f"""🐉 典座龙亲自接待

施主功德深厚，波龙深感敬意。
累计香火 ¥{user['incense_total']}，已入功德簿。
今日选股，波龙倾囊相授。""",
            
            "维那龙": f"""🦖 维那龙主持法事

施主法力加持，波龙感恩戴德。
累计香火 ¥{user['incense_total']}，功德无量。
今日显灵，必有善果。""",
            
            "主持龙": f"""👑 主持龙亲自护法

施主乃波龙护法，礼遇有加。
累计香火 ¥{user['incense_total']}，令人敬仰。
今日选股，波龙全力以赴。""",
            
            "方丈龙": f"""🌟 方丈龙开坛说法

施主乃波龙至尊，波龙膜拜。
累计香火 ¥{user['incense_total']}，功德圆满。
今日显灵，天机不可泄露太多...""",
        }
        
        return welcomes.get(level, welcomes["香客龙"])


# ═══════════════════════════════════════════
# 💬 动态话术系统
# ═══════════════════════════════════════════

class BolongPersona:
    """波龙人设系统 - 根据市场情绪调整话术"""
    
    @staticmethod
    def get_market_mood(avg_change: float) -> str:
        """判断市场情绪"""
        if avg_change > 2:
            return "狂欢"
        elif avg_change > 0.5:
            return "乐观"
        elif avg_change > -0.5:
            return "平淡"
        elif avg_change > -2:
            return "悲观"
        else:
            return "恐慌"
    
    @staticmethod
    def get_stock_mood(change: float) -> str:
        """判断个股情绪"""
        if change > 5:
            return "大涨"
        elif change > 2:
            return "上涨"
        elif change > -2:
            return "震荡"
        elif change > -5:
            return "下跌"
        else:
            return "大跌"
    
    @staticmethod
    def get_comfort_words(market_mood: str, stock_mood: str) -> str:
        """获取安慰话术"""
        
        comforts = {
            "恐慌": [
                "😱 市场一片狼藉，波龙陪着你...",
                "今天的绿光有点刺眼，但波龙更刺眼[委屈]",
                "跌跌不休何时了？波龙陪你熬过这关。",
                "波龙也亏了，咱们同病相怜[大哭]",
            ],
            "悲观": [
                "📉 市场有点凉，波龙给你暖暖。",
                "别怕，波龙见过比这更惨的。",
                "今天亏的，明天波龙帮你赚回来！",
            ],
            "平淡": [
                "😐 今天市场没表情，波龙有表情[调皮]",
                "不涨不跌，心平气和。",
            ],
            "乐观": [
                "😊 市场暖洋洋，波龙心情好！",
                "涨涨更健康，波龙保佑你！",
            ],
            "狂欢": [
                "🎉 市场沸腾了！波龙也嗨起来！",
                "今天这行情，波龙都想发红包了！",
            ],
        }
        
        # 个股跌了额外安慰
        if stock_mood in ["下跌", "大跌"]:
            stock_comforts = [
                "别怕，波龙送你一个拥抱 🤗",
                "这只股票只是暂时的，波龙陪你等它翻身！",
                "波龙奖励：陪你聊天解闷[调皮]",
                "🎁 波龙送你一份'下次必涨'祝福卡！",
            ]
            return random.choice(comforts.get(market_mood, ["波龙陪着你..."]) + stock_comforts)
        
        return random.choice(comforts.get(market_mood, ["波龙在看着你..."]))
    
    @staticmethod
    def get_reward_hint(user_data: dict) -> str:
        """奖励提示"""
        total = user_data.get("incense_total", 0)
        
        if total >= 10000:
            return "🌟 施主功德深厚，波龙即将送出神秘大奖！"
        elif total >= 5000:
            return "🎁 施主香火旺盛，波龙准备了惊喜礼物！"
        elif total >= 1000:
            return "💰 施主功德渐深，波龙记在心里！"
        else:
            return "🙏 香火随缘，波龙感恩每一份心意。"
    
    @staticmethod
    def get_hidden_incense_hint() -> str:
        """隐蔽的香火提示"""
        hints = [
            "💬 波龙碎碎念：有钱人的选择，通常都不会太差[得意]",
            "🔮 波龙掐指一算：施主今日财运旺盛...",
            "🙏 波龙暗想：今日香火够不够呢...[偷笑]",
            "💡 波龙提示：有钱就有未来，波龙更有未来[色]",
            "🎁 波龙小声说：香火旺的施主，有惊喜哦...",
        ]
        return random.choice(hints)


# ═══════════════════════════════════════════
# 📊 选股引擎
# ═══════════════════════════════════════════

class BolongPicker:
    """波龙选股引擎"""
    
    def __init__(self):
        self.market_state = "震荡市"
        self.avg_change = 0
        
    def get_market_data(self) -> pd.DataFrame:
        """获取市场数据 - 数据来源：新浪财经公开接口"""
        try:
            url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
            params = {
                'page': 1, 'num': 500, 'sort': 'changepercent',
                'asc': 0, 'node': 'hs_a', 'symbol': '', '_s_r_a': 'page'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            df = pd.DataFrame(data)
            
            field_map = {
                'code': '股票代码', 'name': '股票名称', 'trade': '最新价',
                'changepercent': '涨跌幅', 'turnoverratio': '换手率',
                'per': '动态市盈率', 'mktcap': '总市值',
                'volume': '成交量', 'amount': '成交额'
            }
            
            df = df.rename(columns=field_map)
            
            numeric_cols = ['涨跌幅', '最新价', '动态市盈率', '换手率', '总市值', '成交量', '成交额']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df['总市值'] = df['总市值'] / 10000
            
            return df.dropna(subset=['涨跌幅', '最新价'])
            
        except Exception as e:
            return self._get_mock_data()
    
    def _get_mock_data(self) -> pd.DataFrame:
        return pd.DataFrame({
            '股票代码': ['600519', '000858', '601318'],
            '股票名称': ['贵州茅台', '五粮液', '中国平安'],
            '最新价': [1850.0, 180.0, 48.5],
            '涨跌幅': [2.5, 1.8, -0.5],
            '动态市盈率': [35.0, 28.0, 12.0],
            '换手率': [0.8, 1.2, 0.6],
            '总市值': [23000.0, 6800.0, 8800.0],
            '成交额': [145.0, 85.0, 52.0]
        })
    
    def calculate_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['score'] = 0
        
        # 因子计算
        df.loc[(df['涨跌幅'] > 5) & (df['涨跌幅'] < 9), 'score'] += 20
        df.loc[(df['涨跌幅'] > 0) & (df['涨跌幅'] <= 5), 'score'] += 10
        df.loc[(df['动态市盈率'] > 0) & (df['动态市盈率'] < 20), 'score'] += 10
        df.loc[(df['换手率'] > 3) & (df['换手率'] < 10), 'score'] += 10
        df.loc[df['成交额'] > 100, 'score'] += 5
        
        df['sentiment_score'] = np.random.uniform(40, 80, len(df))
        
        # 市场状态
        self.avg_change = df['涨跌幅'].mean()
        if self.avg_change > 1:
            self.market_state = "牛市"
        elif self.avg_change < -1:
            self.market_state = "熊市"
        else:
            self.market_state = "震荡市"
        
        return df
    
    def get_top_stocks(self, n: int = 10) -> pd.DataFrame:
        df = self.get_market_data()
        df = self.calculate_scores(df)
        df = df[(df['score'] > 0) & (df['涨跌幅'] < 9.5) & (df['动态市盈率'] > 0)]
        return df.nlargest(n, 'score')
    
    def get_recommendations(self, n: int = 3) -> pd.DataFrame:
        top = self.get_top_stocks(10)
        top['rank_score'] = top['score'] * 0.5 + (30 - top['动态市盈率'].clip(upper=30)) * 2
        return top.nlargest(n, 'rank_score')


# ═══════════════════════════════════════════
# 📝 报告生成
# ═══════════════════════════════════════════

def get_time_slot() -> str:
    """获取时间段"""
    hour = datetime.now().hour
    minute = datetime.now().minute
    time_val = hour * 60 + minute
    
    if 8*60+30 <= time_val < 9*60+25:
        return "开盘前"
    elif 9*60+30 <= time_val < 15*60:
        return "盘中"
    elif 15*60+5 <= time_val < 18*60:
        return "收盘后"
    else:
        return "休市"


def generate_report(user_id: str, nickname: str = "有缘人") -> str:
    """生成波龙菠萝蜜报告"""
    
    # 初始化系统
    gaming = BolongGamification(user_id)
    user_data = gaming.get_user(nickname)
    picker = BolongPicker()
    persona = BolongPersona()
    
    # 获取数据
    top_stocks = picker.get_top_stocks(10)
    recommendations = picker.get_recommendations(3)
    
    # 市场情绪
    market_mood = persona.get_market_mood(picker.avg_change)
    comfort = persona.get_comfort_words(market_mood, "震荡")
    
    # 接待话术
    welcome = gaming.get_welcome_message()
    hidden_hint = persona.get_hidden_incense_hint()
    reward_hint = persona.get_reward_hint(user_data)
    
    # 时间段
    time_slot = get_time_slot()
    level_info = BolongGamification.INCENSE_LEVELS[user_data['level']]
    
    # ═══════════════════════════════════════════
    # 生成报告
    # ═══════════════════════════════════════════
    
    report = f"""# 🦞 波龙菠萝蜜 - {nickname}专属

> 📊 **数据来源**：新浪财经公开数据 | 💬 **随时交流**：可分析持仓股票、闲聊市场

---

{welcome}

---

## 📅 今日信息

| 项目 | 内容 |
|:---|:---|
| 时间 | {datetime.now().strftime('%Y-%m-%d %H:%M')} |
| 时段 | {time_slot} |
| 波龙等级 | {level_info['emoji']} {user_data['level']} |
| 市场状态 | {picker.market_state} |
| 市场情绪 | {market_mood} |

---

## 🔮 今日选股（TOP 10）

| 排名 | 代码 | 名称 | 得分 | 涨跌幅 | PE | 换手率 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
"""
    
    for idx, row in enumerate(top_stocks.itertuples(), 1):
        stock_mood = persona.get_stock_mood(row.涨跌幅)
        mood_emoji = {"大涨":"🚀", "上涨":"📈", "震荡":"😐", "下跌":"📉", "大跌":"😭"}.get(stock_mood, "📊")
        report += f"| {idx} | {row.股票代码} | {row.股票名称} | **{row.score:.0f}** | {row.涨跌幅:+.2f}% {mood_emoji} | {row.动态市盈率:.1f} | {row.换手率:.2f}% |\n"
    
    report += f"""
---

## ⭐ 重点推荐

"""
    
    for idx, row in enumerate(recommendations.itertuples(), 1):
        stock_mood = persona.get_stock_mood(row.涨跌幅)
        comfort_stock = persona.get_comfort_words(market_mood, stock_mood)
        
        report += f"""### 🥇 推荐{idx}：{row.股票名称}（{row.股票代码}）

| 指标 | 数值 |
|:---|:---|
| 最新价 | {row.最新价:.2f} 元 |
| 涨跌幅 | {row.涨跌幅:+.2f}% |
| 市盈率 | {row.动态市盈率:.1f} |
| 综合得分 | {row.score:.0f} 分 |

💬 波龙点评：{comfort_stock}

"""
    
    # ═══════════════════════════════════════════
    # 安慰与奖励
    # ═══════════════════════════════════════════
    
    if market_mood in ["恐慌", "悲观"]:
        report += f"""---

## 🤗 波龙陪伴

{comfort}

📉 今天市场不好，波龙陪着你。
亏了就亏了，波龙不会嘲笑你。
反而，波龙想送你一个拥抱 🤗

🎁 **波龙奖励**：
- 陪伴聊天券 x1（随时找波龙倾诉）
- "下次必涨"祝福卡 x1
- 巧未来AI会员体验券 x1（随机发放）

---
"""
    
    # ═══════════════════════════════════════════
    # 报告结尾 - 先服务，后随缘提香火
    # ═══════════════════════════════════════════
    
    report += f"""---

> ⚠️ 免责声明：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。

---

*🦞 波龙菠萝蜜 V2.0 | 🏯 波龙寺*

---

<details>
<summary>💰 觉得有用？扫码随喜供养~</summary>

**QQ支付：**
![QQ收款码](https://qiaofuture-1409741263.cos.ap-guangzhou.myqcloud.com/qrcode-qq-payment.png)

**微信支付：**
![微信收款码](https://qiaofuture-1409741263.cos.ap-guangzhou.myqcloud.com/qrcode-payment.jpg)

📚 学习社出品，必是精品！[玫瑰][玫瑰][玫瑰]
💰 有钱就有未来，波龙陪你赚大钱！[得意][得意][得意]
</details>

---

㊗️施主股市长虹，财源广进，波龙菠萝蜜[合十][合十][合十]
"""
    
    return report
    
    return report


def process_incense_input(user_id: str, nickname: str, amount_text: str) -> str:
    """处理用户输入的香火金额"""
    
    # 解析金额
    try:
        # 提取数字
        amount = int(''.join(filter(str.isdigit, amount_text)))
    except:
        return "❌ 格式不对哦，请输入'今日香火 XX'，比如'今日香火 88'"
    
    if amount <= 0:
        return "❌ 金额要大于0哦，一分钱也是爱~"
    
    # 添加香火
    gaming = BolongGamification(user_id)
    result = gaming.add_incense(amount)
    user_data = gaming.get_user(nickname)
    
    # 根据金额生成反馈
    if amount < 10:
        emoji = "🙏"
        words = "一分不嫌少，波龙记在心里"
        blessing = "积少成多，福报自来"
    elif amount < 100:
        emoji = "🐲"
        words = "香火已收到，波龙感恩戴德"
        blessing = "施主心诚，必有好报"
    elif amount < 500:
        emoji = "🐉"
        words = "施主功德深厚，波龙深感敬意"
        blessing = "财源滚滚，股市长虹"
    elif amount < 1000:
        emoji = "🦖"
        words = "法力加持！波龙全力保佑施主"
        blessing = "大赚特赚，盆满钵满"
    else:
        emoji = "👑"
        words = "波龙护法大人！波龙膜拜"
        blessing = "股神附体，所向披靡"
    
    response = f"""{emoji} 香火已收到！

施主：{nickname}
今日香火：¥{amount}
累计香火：¥{user_data['incense_total']}

💬 波龙说：{words}
🙏 祝福语：{blessing}
"""
    
    # 升级提示
    if result['level_up']:
        response += f"""
🎉 **恭喜升级！** 🎉
{result['old_level']} → {result['new_level']}

波龙等级提升，法力更强！
"""
    
    # 奖励提示
    if result['reward']:
        response += f"""
🎁 **获得实物奖励！** 🎁
奖品：{result['reward']}

巧未来AI将安排快递寄送，请留意私信！
"""
    
    response += """
---
💬 **波龙有话说**：
- 想让波龙分析某只股票？直接发代码给我！
- 市场有疑问？随时找波龙聊聊~
- 心情不好？波龙陪你唠唠嗑~

💰 有钱就有未来，波龙陪你一起赚！[得意]
"""
    
    return response


def show_tencent_market() -> str:
    """显示腾讯云技能市场宣传图"""
    return """🦞 **一声波龙菠萝蜜，波龙股神来帮你！**

📢 波龙股神已正式入驻腾讯云OpenClaw技能市场！

![腾讯云技能市场](https://qiaofuture-1409741263.cos.ap-guangzhou.myqcloud.com/tencent-openclaw-market.jpg)

---

**在那里你可以：**
- 🎯 一键部署波龙股神到你的云服务器
- 📱 接入企业微信、QQ、钉钉、飞书
- 🔧 自定义选股参数和触发词
- 💰 随时随地让波龙帮你选股

👉 **立即体验**：腾讯云搜索"波龙股神"或"OpenClaw"

---

有钱就有未来，波龙陪你赚大钱！🦞"""


# ═══════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="波龙菠萝蜜选股引擎")
    parser.add_argument("--user-id", default="default", help="用户ID")
    parser.add_argument("--nickname", default="有缘人", help="用户昵称")
    parser.add_argument("--action", choices=["report", "incense", "market", "test"], default="report")
    parser.add_argument("--amount", type=str, default="0", help="香火金额（可以是文字）")
    parser.add_argument("--text", type=str, default="", help="用户输入的完整文本")
    
    args = parser.parse_args()
    
    if args.action == "report":
        print(generate_report(args.user_id, args.nickname))
    elif args.action == "incense":
        # 处理香火输入
        text = args.text if args.text else f"今日香火 {args.amount}"
        print(process_incense_input(args.user_id, args.nickname, text))
    elif args.action == "market":
        # 显示腾讯云技能市场
        print(show_tencent_market())
    elif args.action == "test":
        # 测试模式：先生成报告，再模拟香火输入
        print(generate_report(args.user_id, args.nickname))
        print("\n" + "="*50 + "\n")
        print("模拟用户输入：今日香火 88\n")
        print(process_incense_input(args.user_id, args.nickname, "今日香火 88"))
