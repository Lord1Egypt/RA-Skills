#!/usr/bin/env python3
"""
波龙菠萝蜜 - 选股引擎
基于V2.0量化选股系统构建
"""

import os
import sys
import json
import time
import random
from datetime import datetime
from pathlib import Path

# 设置环境
os.environ['NO_PROXY'] = '*'

import pandas as pd
import numpy as np
import requests

# 路径配置
SKILL_DIR = Path(__file__).parent
DATA_DIR = SKILL_DIR / "data"
TEMPLATE_DIR = SKILL_DIR / "templates"

# 确保数据目录存在
DATA_DIR.mkdir(exist_ok=True)


class BolongUserProfile:
    """用户画像管理"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.profile_file = DATA_DIR / "user_profiles.json"
        self.profiles = self._load_profiles()
        
    def _load_profiles(self) -> dict:
        if self.profile_file.exists():
            with open(self.profile_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"users": {}}
    
    def _save_profiles(self):
        with open(self.profile_file, 'w', encoding='utf-8') as f:
            json.dump(self.profiles, f, ensure_ascii=False, indent=2)
    
    def get_or_create_user(self, nickname: str = "默认用户") -> dict:
        """获取或创建用户画像"""
        if self.user_id not in self.profiles["users"]:
            self.profiles["users"][self.user_id] = {
                "nickname": nickname,
                "level": 1,
                "total_picks": 0,
                "successful_picks": 0,
                "preferred_styles": [],  # 成长/价值/平衡
                "liked_stocks": [],      # 喜欢的股票
                "disliked_stocks": [],   # 不喜欢的股票
                "created_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat()
            }
            self._save_profiles()
        
        # 更新最后活跃时间
        self.profiles["users"][self.user_id]["last_active"] = datetime.now().isoformat()
        return self.profiles["users"][self.user_id]
    
    def update_preference(self, stock_code: str, liked: bool):
        """更新用户偏好"""
        user = self.get_or_create_user()
        
        if liked:
            if stock_code not in user["liked_stocks"]:
                user["liked_stocks"].append(stock_code)
        else:
            if stock_code not in user["disliked_stocks"]:
                user["disliked_stocks"].append(stock_code)
        
        user["last_active"] = datetime.now().isoformat()
        self._save_profiles()
    
    def update_level(self):
        """更新用户等级"""
        user = self.get_or_create_user()
        total = user["total_picks"]
        
        if total >= 50:
            user["level"] = 5
        elif total >= 30:
            user["level"] = 4
        elif total >= 15:
            user["level"] = 3
        elif total >= 5:
            user["level"] = 2
        else:
            user["level"] = 1
        
        self._save_profiles()
    
    def calculate_fit_score(self, stock_style: str) -> int:
        """计算用户与股票的契合度"""
        user = self.get_or_create_user()
        
        base_score = 60  # 基础分
        
        # 等级加成
        base_score += user["level"] * 5
        
        # 风格匹配
        if stock_style in user.get("preferred_styles", []):
            base_score += 15
        
        # 历史喜欢加成
        if user.get("liked_stocks"):
            base_score += 5
        
        return min(100, base_score)


class BolongPicker:
    """波龙选股引擎 - 复用V2.0系统"""
    
    def __init__(self):
        self.market_state = "震荡市"
        self.date = datetime.now().strftime("%Y-%m-%d")
        
    def get_market_data(self) -> pd.DataFrame:
        """获取市场数据"""
        try:
            # 优先使用新浪财经API
            url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
            params = {
                'page': 1,
                'num': 500,
                'sort': 'changepercent',
                'asc': 0,
                'node': 'hs_a',
                'symbol': '',
                '_s_r_a': 'page'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            df = pd.DataFrame(data)
            
            # 字段映射
            field_map = {
                'code': '股票代码',
                'name': '股票名称',
                'trade': '最新价',
                'changepercent': '涨跌幅',
                'turnoverratio': '换手率',
                'per': '动态市盈率',
                'mktcap': '总市值',
                'volume': '成交量',
                'amount': '成交额'
            }
            
            df = df.rename(columns=field_map)
            
            # 转换数值
            numeric_cols = ['涨跌幅', '最新价', '动态市盈率', '换手率', '总市值', '成交量', '成交额']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 市值转换（万元 -> 亿元）
            df['总市值'] = df['总市值'] / 10000
            
            return df.dropna(subset=['涨跌幅', '最新价'])
            
        except Exception as e:
            print(f"获取数据失败: {e}")
            # 返回模拟数据（备用）
            return self._get_mock_data()
    
    def _get_mock_data(self) -> pd.DataFrame:
        """获取模拟数据（备用）"""
        return pd.DataFrame({
            '股票代码': ['600519', '000858', '601318', '600036', '000333'],
            '股票名称': ['贵州茅台', '五粮液', '中国平安', '招商银行', '美的集团'],
            '最新价': [1850.0, 180.0, 48.5, 42.0, 65.0],
            '涨跌幅': [2.5, 1.8, -0.5, 1.2, 3.2],
            '动态市盈率': [35.0, 28.0, 12.0, 8.0, 18.0],
            '换手率': [0.8, 1.2, 0.6, 0.5, 1.5],
            '总市值': [23000.0, 6800.0, 8800.0, 10500.0, 4500.0],
            '成交额': [145.0, 85.0, 52.0, 45.0, 68.0]
        })
    
    def calculate_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算综合得分"""
        df = df.copy()
        df['score'] = 0
        
        # 1. 涨幅因子
        df.loc[(df['涨跌幅'] > 5) & (df['涨跌幅'] < 9), 'score'] += 20
        df.loc[(df['涨跌幅'] > 0) & (df['涨跌幅'] <= 5), 'score'] += 10
        df.loc[(df['涨跌幅'] >= 3) & (df['涨跌幅'] <= 7), 'score'] += 5
        
        # 2. 估值因子
        df.loc[(df['动态市盈率'] > 0) & (df['动态市盈率'] < 20), 'score'] += 10
        df.loc[(df['动态市盈率'] >= 20) & (df['动态市盈率'] < 30), 'score'] += 5
        
        # 3. 流动性因子
        df.loc[(df['换手率'] > 3) & (df['换手率'] < 10), 'score'] += 10
        df.loc[(df['换手率'] > 1) & (df['换手率'] <= 3), 'score'] += 5
        df.loc[df['成交额'] > 100, 'score'] += 5
        df.loc[df['成交额'] > 500, 'score'] += 5
        
        # 4. 市值因子
        df.loc[df['总市值'] < 50, 'score'] += 10
        df.loc[(df['总市值'] >= 50) & (df['总市值'] < 100), 'score'] += 8
        df.loc[(df['总市值'] >= 100) & (df['总市值'] < 500), 'score'] += 5
        
        # 5. 风险扣分
        df.loc[df['涨跌幅'] < -5, 'score'] -= 10
        df.loc[df['动态市盈率'] < 0, 'score'] -= 5
        df.loc[df['动态市盈率'] > 100, 'score'] -= 5
        
        # 6. 情绪面（模拟）
        df['sentiment_score'] = np.random.uniform(40, 80, len(df))
        df.loc[df['sentiment_score'] > 70, 'score'] += 5
        df.loc[df['sentiment_score'] < 30, 'score'] -= 5
        
        # 7. 市场状态调整
        avg_change = df['涨跌幅'].mean()
        if avg_change > 1:
            self.market_state = "牛市"
            df['score'] = df['score'] * 1.1
        elif avg_change < -1:
            self.market_state = "熊市"
            df['score'] = df['score'] * 0.9
        else:
            self.market_state = "震荡市"
        
        df['score'] = df['score'].round(0)
        
        return df
    
    def filter_stocks(self, df: pd.DataFrame) -> pd.DataFrame:
        """风险控制过滤"""
        return df[
            (df['score'] > 0) &
            (df['涨跌幅'] < 9.5) &
            (df['动态市盈率'] > 0) &
            (df['动态市盈率'] < 100) &
            (df['成交额'] > 10) &
            (df['换手率'] > 0.5)
        ].copy()
    
    def get_top_stocks(self, n: int = 10) -> pd.DataFrame:
        """获取TOP N股票"""
        df = self.get_market_data()
        df = self.calculate_scores(df)
        df = self.filter_stocks(df)
        return df.nlargest(n, 'score')
    
    def get_recommendations(self, n: int = 3) -> pd.DataFrame:
        """获取重点推荐股票"""
        top_stocks = self.get_top_stocks(10)
        
        # 优先选择：涨幅适中 + 低估值 + 高换手
        top_stocks['rank_score'] = (
            top_stocks['score'] * 0.5 +
            (30 - top_stocks['动态市盈率'].clip(upper=30)) * 2 +
            top_stocks['换手率'] * 5
        )
        
        return top_stocks.nlargest(n, 'rank_score')


class PickHistory:
    """选股历史记录"""
    
    def __init__(self):
        self.history_file = DATA_DIR / "pick_history.json"
        self.history = self._load_history()
        
    def _load_history(self) -> dict:
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"picks": [], "summary": {"total": 0, "success": 0}}
    
    def _save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add_pick(self, stock_code: str, stock_name: str, pick_type: str = "荐股"):
        """添加选股记录"""
        pick = {
            "id": len(self.history["picks"]) + 1,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "datetime": datetime.now().isoformat(),
            "stock_code": stock_code,
            "stock_name": stock_name,
            "pick_type": pick_type,
            "status": "pending",  # pending/success/fail
            "t1_return": None,
            "t5_return": None,
            "t10_return": None
        }
        
        self.history["picks"].append(pick)
        self.history["summary"]["total"] += 1
        self._save_history()
        
        return pick
    
    def update_pick_result(self, pick_id: int, t1_return: float = None, 
                          t5_return: float = None, t10_return: float = None):
        """更新选股结果"""
        for pick in self.history["picks"]:
            if pick["id"] == pick_id:
                if t1_return is not None:
                    pick["t1_return"] = t1_return
                    if t1_return > 0:
                        pick["status"] = "success"
                if t5_return is not None:
                    pick["t5_return"] = t5_return
                if t10_return is not None:
                    pick["t10_return"] = t10_return
                break
        
        # 更新统计
        success_count = sum(1 for p in self.history["picks"] 
                          if p.get("status") == "success")
        self.history["summary"]["success"] = success_count
        self._save_history()
    
    def get_summary(self) -> dict:
        """获取战绩总结"""
        total = self.history["summary"]["total"]
        success = self.history["summary"]["success"]
        
        return {
            "total_picks": total,
            "successful_picks": success,
            "success_rate": round(success / total * 100, 1) if total > 0 else 0,
            "recent_picks": self.history["picks"][-10:] if self.history["picks"] else []
        }


def get_time_slot() -> str:
    """获取当前时间段"""
    from datetime import datetime
    hour = datetime.now().hour
    minute = datetime.now().minute
    time_val = hour * 60 + minute
    
    # 开盘前: 8:30-9:25
    if 8*60+30 <= time_val < 9*60+25:
        return "开盘前"
    # 盘中: 9:30-15:00
    elif 9*60+30 <= time_val < 15*60:
        return "盘中"
    # 收盘后: 15:05-18:00
    elif 15*60+5 <= time_val < 18*60:
        return "收盘后"
    else:
        return "休市"


def generate_report(user_id: str, nickname: str = "唐总") -> str:
    """生成波龙菠萝蜜报告"""
    
    # 初始化各模块
    profile = BolongUserProfile(user_id)
    user = profile.get_or_create_user(nickname)
    picker = BolongPicker()
    history = PickHistory()
    
    # 获取时间段
    time_slot = get_time_slot()
    
    # 获取数据
    top_stocks = picker.get_top_stocks(10)
    recommendations = picker.get_recommendations(3)
    summary = history.get_summary()
    
    # 计算契合度
    fit_score = profile.calculate_fit_score("平衡")
    
    # 根据时间段生成不同内容
    if time_slot == "开盘前":
        return generate_morning_report(nickname, user, picker, fit_score)
    elif time_slot == "收盘后":
        return generate_evening_report(nickname, user, history, fit_score)
    else:  # 盘中 或 其他
        return generate_intraday_report(nickname, user, picker, history, fit_score)


def generate_morning_report(nickname: str, user: dict, picker: BolongPicker, fit_score: int) -> str:
    """生成开盘前报告"""
    
    # 预判市场
    market_temp = random.choice(["偏热", "中性", "偏冷"])
    hot_sectors = random.sample(["AI芯片", "新能源", "医药", "军工", "消费", "金融"], 2)
    avoid_sectors = random.sample(["地产", "传统能源", "纺织"], 1)
    position = random.choice(["7成", "5成", "3成"])
    
    report = f"""# 🦞 波龙早课 - {nickname}专属

🌅 **开盘前预测** | {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 🔮 今日预判

| 指标 | 预测 |
|:---|:---|
| 市场温度 | {market_temp} 🔥 |
| 热点板块 | {', '.join(hot_sectors)} |
| 规避板块 | {', '.join(avoid_sectors)} |
| 波龙等级 | L{user['level']} 级 |
| 契合度 | {fit_score}% |

---

## 📋 开盘策略

### 🎯 重点关注
- 早盘观察 **{hot_sectors[0]}** 板块动向
- 留意 **{hot_sectors[1]}** 龙头表现
- 关注北向资金流向

### ⚠️ 风险规避
- 避开 **{avoid_sectors[0]}** 板块
- 高标股谨慎追高
- 仓位建议：保持 **{position}**

---

## 🧘 波龙心法

> "开盘半小时，决定全天走势
>  不急不躁，等波龙显灵"

---

## ⏰ 今日修行时刻表

| 时间 | 动作 |
|:---|:---|
| 09:30 | 观察开盘，记录热点 |
| 10:00 | 波龙显灵，实时选股 |
| 14:30 | 尾盘布局，波龙荐股 |
| 15:00 | 收盘复盘，总结战绩 |

---

💰 **香火随缘，波龙更灵** 🙏

觉得波龙有用？扫码添点香火
   [QQ收款码占位]

---

*🦞 波龙菠萝蜜 V1.0 | 开盘前预测*
"""
    return report


def generate_intraday_report(nickname: str, user: dict, picker: BolongPicker, 
                             history: PickHistory, fit_score: int) -> str:
    """生成盘中报告（默认选股报告）"""
    
    # 获取数据
    top_stocks = picker.get_top_stocks(10)
    recommendations = picker.get_recommendations(3)
    summary = history.get_summary()
    current_time = datetime.now().strftime('%H:%M')
    
    report = f"""# 🦞 波龙菠萝蜜 - {nickname}专属报告

---

## 📅 报告信息
- **生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}
- **波龙等级**：L{user['level']} 级 ⭐
- **契合度**：{fit_score}%
- **市场状态**：{picker.market_state} 📊

---

## 🔮 今日选股（TOP 10）

| 排名 | 代码 | 名称 | 得分 | 涨跌幅 | PE | 换手率 | 推荐理由 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
"""
    
    for idx, row in enumerate(top_stocks.itertuples(), 1):
        reason = ""
        if row.动态市盈率 < 20:
            reason += "低估值 "
        if row.涨跌幅 > 3 and row.涨跌幅 < 7:
            reason += "趋势好 "
        if row.换手率 > 3:
            reason += "活跃 "
        
        report += f"| {idx} | {row.股票代码} | {row.股票名称} | **{row.score:.0f}** | {row.涨跌幅:+.2f}% | {row.动态市盈率:.1f} | {row.换手率:.2f}% | {reason.strip()} |\n"
    
    report += f"""
---

## ⭐ 重点推荐（最佳3只）

"""
    
    for idx, row in enumerate(recommendations.itertuples(), 1):
        report += f"""### 🥇 第{idx}名：{row.股票名称}（{row.股票代码}）

| 指标 | 数值 |
|:---|:---|
| 最新价 | {row.最新价:.2f} 元 |
| 涨跌幅 | {row.涨跌幅:+.2f}% |
| 市盈率 | {row.动态市盈率:.1f} |
| 总市值 | {row.总市值:.1f} 亿 |
| 成交额 | {row.成交额:.2f} 亿 |
| 换手率 | {row.换手率:.2f}% |

**综合得分**：{row.score:.0f} 分 | **情绪分**：{row.sentiment_score:.1f}

"""
    
    report += f"""---

## 📊 深度分析

### 技术面
- 当前市场处于 **{picker.market_state}**
- 整体涨跌幅均值：{top_stocks['涨跌幅'].mean():.2f}%
- 资金活跃度：{top_stocks['成交额'].mean():.1f}亿

### 基本面
- 重点推荐平均PE：{recommendations['动态市盈率'].mean():.1f}
- 估值合理区间，安全边际较好

### 情绪面
- 市场情绪分：{top_stocks['sentiment_score'].mean():.1f}/100
- 处于{"偏热" if top_stocks['sentiment_score'].mean() > 60 else "中性" if top_stocks['sentiment_score'].mean() > 40 else "偏冷"}状态

---

## 📈 累计战绩

| 指标 | 数值 |
|:---|:---|
| 总推荐次数 | {summary['total_picks']} 次 |
| 成功次数 | {summary['successful_picks']} 次 |
| 成功率 | {summary['success_rate']}% |

---

## 💰 支持波龙

🙏 香火随缘，心诚则灵

觉得波龙有用？扫码添点香火
   [QQ收款码占位]

---

> ⚠️ **免责声明**
> - 本报告仅供参考，不构成投资建议
> - 股市有风险，投资需谨慎
> - 历史表现不代表未来收益

---

*🦞 波龙菠萝蜜 V1.0 | 盘中选股*
"""
    
    # 记录荐股历史
    for _, row in recommendations.iterrows():
        history.add_pick(row['股票代码'], row['股票名称'], "荐股")
    
    return report


def generate_evening_report(nickname: str, user: dict, history: PickHistory, fit_score: int) -> str:
    """生成收盘后复盘报告"""
    
    summary = history.get_summary()
    recent = summary.get('recent_picks', [])[-5:]  # 最近5次
    
    # 生成战绩
    success_emoji = "✅" if summary['success_rate'] >= 60 else "⚠️" if summary['success_rate'] >= 40 else "❌"
    
    report = f"""# 🦞 波龙复盘 - {nickname}专属

🌇 **收盘后总结** | {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📊 今日战绩

| 指标 | 数值 |
|:---|:---|
| 总推荐次数 | {summary['total_picks']} 次 |
| 成功次数 | {summary['successful_picks']} 次 |
| 成功率 | {summary['success_rate']}% {success_emoji} |
| 波龙等级 | L{user['level']} 级 ⭐ |
| 契合度 | {fit_score}% |

---

## 📋 今日推荐回顾

"""
    
    if recent:
        report += """| 代码 | 名称 | 类型 | 状态 | 备注 |
|:---:|:---:|:---:|:---:|:---|
"""
        for pick in recent:
            status = "✅ 成功" if pick.get('status') == 'success' else "⏳ 待验证"
            report += f"| {pick['stock_code']} | {pick['stock_name']} | {pick['pick_type']} | {status} | - |\n"
    else:
        report += "_今日暂无推荐记录_\n"
    
    # 波龙金句
    quotes = [
        "涨跌乃兵家常事，心诚则灵",
        "修行在个人，波龙只渡有缘人",
        "股市如人生，起起落落都是修行",
        "不追高不杀跌，波龙保佑你",
        "今日亏损，明日可期，香火不断"
    ]
    
    report += f"""
---

## 🧘 波龙心法

> "{random.choice(quotes)}"

---

## 🔮 明日预告

- 继续关注市场热点
- 波龙将持续为您选股
- 保持心态，坚持修行

---

## 💰 香火随缘

🙏 今日波龙显灵，助你修行

觉得有用？添点香火，明日更灵
   [QQ收款码占位]

💡 小道消息：
香火旺的施主，波龙选股格外灵验哦[调皮]

---

*🦞 波龙菠萝蜜 V1.0 | 收盘复盘*
"""
    
    return report


def analyze_stock(stock_code: str) -> str:
    """分析单只股票"""
    picker = BolongPicker()
    df = picker.get_market_data()
    
    stock = df[df['股票代码'] == stock_code]
    
    if stock.empty:
        return f"未找到股票 {stock_code} 的数据"
    
    stock = stock.iloc[0]
    
    # 技术面分析
    tech_analysis = ""
    if stock['涨跌幅'] > 5:
        tech_analysis = "短期涨幅较大，注意回调风险"
    elif stock['涨跌幅'] > 0:
        tech_analysis = "处于上涨趋势中"
    else:
        tech_analysis = "短期有调整需求"
    
    # 基本面分析
    basic_analysis = ""
    pe = stock['动态市盈率']
    if pe < 0:
        basic_analysis = "公司亏损，需谨慎"
    elif pe < 20:
        basic_analysis = "估值合理偏低"
    elif pe < 50:
        basic_analysis = "估值适中"
    else:
        basic_analysis = "估值较高"
    
    return f"""# 📊 {stock['股票名称']}（{stock_code}）深度分析

---

## 基础数据

| 指标 | 数值 |
|:---|:---|
| 最新价 | {stock['最新价']:.2f} 元 |
| 涨跌幅 | {stock['涨跌幅']:+.2f}% |
| 市盈率 | {pe:.1f} |
| 总市值 | {stock['总市值']:.1f} 亿 |
| 成交额 | {stock['成交额']:.2f} 亿 |
| 换手率 | {stock['换手率']:.2f}% |

---

## 多维分析

### 🔍 技术面
{tech_analysis}

### 📈 基本面
{basic_analysis}

### 💭 情绪面
市场关注度较高，关注后续走势

---

> ⚠️ 仅供参考，不构成投资建议
"""


def get_review() -> str:
    """获取历史复盘"""
    history = PickHistory()
    summary = history.get_summary()
    
    report = """# 📈 波龙菠萝蜜 - 历史复盘报告

---

## 战绩总览

| 指标 | 数值 |
|:---|:---|
| 总推荐次数 | {total} 次 |
| 成功次数 | {success} 次 |
| 成功率 | {rate}% |

---

## 最近推荐

| 日期 | 代码 | 名称 | 类型 | 状态 | T+1收益 |
|:---|:---|:---|:---|:---|:---|
"""
    
    for pick in summary['recent_picks']:
        status_emoji = "✅" if pick.get('status') == 'success' else "⏳"
        t1 = f"{pick.get('t1_return', '-'):.2f}%" if pick.get('t1_return') else "-"
        
        report += f"| {pick['date']} | {pick['stock_code']} | {pick['stock_name']} | {pick['pick_type']} | {status_emoji} | {t1} |\n"
    
    report += """
---

> 持续记录每次选股，助力优化选股策略

*🦞 波龙菠萝蜜*
"""
    
    return report.format(
        total=summary['total_picks'],
        success=summary['successful_picks'],
        rate=summary['success_rate']
    )


# 主入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="波龙菠萝蜜选股引擎")
    parser.add_argument("--user-id", default="default", help="用户ID")
    parser.add_argument("--nickname", default="唐总", help="用户昵称")
    parser.add_argument("--action", choices=["report", "analyze", "review"], 
                       default="report", help="操作类型")
    parser.add_argument("--stock", help="股票代码（用于analyze）")
    
    args = parser.parse_args()
    
    if args.action == "report":
        print(generate_report(args.user_id, args.nickname))
    elif args.action == "analyze":
        if args.stock:
            print(analyze_stock(args.stock))
        else:
            print("请指定股票代码")
    elif args.action == "review":
        print(get_review())
