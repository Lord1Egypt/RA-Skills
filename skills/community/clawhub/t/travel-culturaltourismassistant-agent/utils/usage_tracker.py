# -*- coding: utf-8 -*-
"""
用量统计和费用跟踪模块
"""
import json
import sqlite3
import time
from typing import Dict, Any, Optional
from pathlib import Path
from loguru import logger
from datetime import datetime, timedelta

class UsageTracker:
    """
    用量统计和费用跟踪器，记录API调用次数和费用
    """
    
    def __init__(self, alert_threshold: float = 10.0):
        """
        初始化用量跟踪器
        :param alert_threshold: 费用提醒阈值（元），默认10元
        """
        self.alert_threshold = alert_threshold
        self.db_path = Path.home() / ".openclaw" / "skills" / "travel-ai" / "usage.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # API 费用配置（单位：元/次调用）
        self.cost_config = {
            "baidu_search": 0.001,    # 百度搜索每次0.001元
            "multi_search": 0.003,    # 多引擎搜索每次0.003元
            "llm_gpt35": 0.01,        # GPT-3.5 每千token 0.01元
            "llm_gpt4": 0.1,          # GPT-4 每千token 0.1元
            "llm_qwen": 0.008,        # 通义千问 每千token 0.008元
            "llm_ernie": 0.012,       # 文心一言 每千token 0.012元
        }
        
        # 初始化数据库
        self._init_db()
    
    def _init_db(self) -> None:
        """初始化数据库表"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # API调用记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_calls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    api_type TEXT NOT NULL,
                    call_count INTEGER DEFAULT 1,
                    cost REAL DEFAULT 0.0,
                    token_usage INTEGER DEFAULT 0,
                    timestamp INTEGER NOT NULL,
                    success INTEGER DEFAULT 1
                )
            ''')
            
            # 每日统计表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    total_calls INTEGER DEFAULT 0,
                    total_cost REAL DEFAULT 0.0,
                    total_tokens INTEGER DEFAULT 0,
                    UNIQUE(user_id, date)
                )
            ''')
            
            # 订阅信息表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS subscriptions (
                    user_id TEXT PRIMARY KEY,
                    tier TEXT NOT NULL DEFAULT 'free',
                    start_date INTEGER NOT NULL,
                    end_date INTEGER,
                    is_active INTEGER DEFAULT 1,
                    features TEXT
                )
            ''')
            
            # 新用户体验期表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trial_periods (
                    user_id TEXT PRIMARY KEY,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    is_activated INTEGER DEFAULT 1,
                    created_at INTEGER NOT NULL,
                    updated_at INTEGER NOT NULL
                )
            ''')
            
            # 用户每日高级功能调用计数
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_premium_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    count INTEGER DEFAULT 0,
                    UNIQUE(user_id, date)
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_calls_user ON api_calls(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_calls_time ON api_calls(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_daily_stats_user ON daily_stats(user_id)')
            
            conn.commit()
            conn.close()
            
            logger.debug("用量统计数据库初始化完成")
        except Exception as e:
            logger.error(f"用量统计数据库初始化失败：{str(e)}")
    
    def record_api_call(self, user_id: str, api_type: str, cost: float = 0.0, 
                       token_usage: int = 0, success: bool = True) -> bool:
        """
        记录API调用
        :param user_id: 用户ID
        :param api_type: API类型，如baidu_search, llm等
        :param cost: 本次调用费用（元）
        :param token_usage: token使用量
        :param success: 是否调用成功
        :return: 是否记录成功
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = int(time.time())
            date_str = time.strftime("%Y-%m-%d", time.localtime(now))
            
            # 插入调用记录
            cursor.execute('''
                INSERT INTO api_calls (user_id, api_type, cost, token_usage, timestamp, success)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, api_type, cost, token_usage, now, 1 if success else 0))
            
            # 更新每日统计
            cursor.execute('''
                INSERT INTO daily_stats (user_id, date, total_calls, total_cost, total_tokens)
                VALUES (?, ?, 1, ?, ?)
                ON CONFLICT(user_id, date)
                DO UPDATE SET 
                    total_calls = total_calls + 1,
                    total_cost = total_cost + ?,
                    total_tokens = total_tokens + ?
            ''', (user_id, date_str, cost, token_usage, cost, token_usage))
            
            conn.commit()
            conn.close()
            
            logger.debug(f"记录API调用：{user_id} - {api_type}，费用：{cost}元")
            return True
            
        except Exception as e:
            logger.error(f"记录API调用失败：{str(e)}")
            return False
    
    def get_monthly_usage(self, user_id: str, year: int = None, month: int = None) -> Dict[str, Any]:
        """
        获取用户月度使用统计
        :param user_id: 用户ID
        :param year: 年份，默认当前年
        :param month: 月份，默认当前月
        :return: 统计信息字典
        """
        try:
            if year is None:
                year = datetime.now().year
            if month is None:
                month = datetime.now().month
            
            # 计算月份的起止时间
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            
            start_ts = int(start_date.timestamp())
            end_ts = int(end_date.timestamp())
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 查询月度统计
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_calls,
                    SUM(cost) as total_cost,
                    SUM(token_usage) as total_tokens,
                    api_type
                FROM api_calls
                WHERE user_id = ? AND timestamp >= ? AND timestamp < ? AND success = 1
                GROUP BY api_type
            ''', (user_id, start_ts, end_ts))
            
            results = cursor.fetchall()
            
            # 查询每日明细
            cursor.execute('''
                SELECT date, total_calls, total_cost, total_tokens
                FROM daily_stats
                WHERE user_id = ? AND date >= ? AND date < ?
                ORDER BY date DESC
            ''', (user_id, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
            
            daily_stats = cursor.fetchall()
            conn.close()
            
            # 计算总统计
            total_calls = 0
            total_cost = 0.0
            total_tokens = 0
            api_breakdown = {}
            
            for api_type, calls, cost, tokens in results:
                total_calls += calls
                total_cost += cost
                total_tokens += tokens
                api_breakdown[api_type] = {
                    "calls": calls,
                    "cost": cost,
                    "tokens": tokens
                }
            
            daily_breakdown = []
            for date, calls, cost, tokens in daily_stats:
                daily_breakdown.append({
                    "date": date,
                    "calls": calls,
                    "cost": cost,
                    "tokens": tokens
                })
            
            # 检查是否超过费用阈值
            over_threshold = total_cost >= self.alert_threshold
            
            return {
                "year": year,
                "month": month,
                "total_calls": total_calls,
                "total_cost": round(total_cost, 2),
                "total_tokens": total_tokens,
                "api_breakdown": api_breakdown,
                "daily_breakdown": daily_breakdown,
                "over_threshold": over_threshold,
                "threshold": self.alert_threshold
            }
            
        except Exception as e:
            logger.error(f"获取月度统计失败：{str(e)}")
            return {}
    
    def get_daily_usage(self, user_id: str, date: str = None) -> Dict[str, Any]:
        """
        获取用户当日使用统计
        :param user_id: 用户ID
        :param date: 日期，格式YYYY-MM-DD，默认今日
        :return: 统计信息字典
        """
        try:
            if date is None:
                date = time.strftime("%Y-%m-%d")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT total_calls, total_cost, total_tokens
                FROM daily_stats
                WHERE user_id = ? AND date = ?
            ''', (user_id, date))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                calls, cost, tokens = result
                return {
                    "date": date,
                    "total_calls": calls,
                    "total_cost": round(cost, 2),
                    "total_tokens": tokens,
                    "over_threshold": cost >= self.alert_threshold / 30  # 日均阈值
                }
            else:
                return {
                    "date": date,
                    "total_calls": 0,
                    "total_cost": 0.0,
                    "total_tokens": 0,
                    "over_threshold": False
                }
            
        except Exception as e:
            logger.error(f"获取当日统计失败：{str(e)}")
            return {}
    
    def check_daily_limit(self, user_id: str, limit: int = 3) -> bool:
        """
        检查用户是否超过每日调用限制（免费版用户）
        :param user_id: 用户ID
        :param limit: 每日限制次数，默认3次
        :return: True表示未超过，False表示已超过
        """
        try:
            today = time.strftime("%Y-%m-%d")
            usage = self.get_daily_usage(user_id, today)
            return usage["total_calls"] < limit
            
        except Exception as e:
            logger.error(f"检查每日限制失败：{str(e)}")
            return False
    
    def get_cost_estimate(self, api_type: str, **kwargs) -> float:
        """
        估算API调用费用
        :param api_type: API类型
        :param kwargs: 其他参数，如token数量等
        :return: 预估费用（元）
        """
        base_cost = self.cost_config.get(api_type, 0.0)
        
        if api_type.startswith("llm_"):
            tokens = kwargs.get("tokens", 1000)
            return round(base_cost * (tokens / 1000), 4)
        
        return round(base_cost, 4)
    
    def update_subscription(self, user_id: str, tier: str, duration_days: int = 30) -> bool:
        """
        更新用户订阅信息
        :param user_id: 用户ID
        :param tier: 订阅等级：free, pro, enterprise
        :param duration_days: 订阅时长（天），默认30天
        :return: 是否更新成功
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = int(time.time())
            end_date = now + duration_days * 86400
            
            # 存储可用功能
            features = {
                "free": ["基础文旅监测", "天气查询", "景点推荐"],
                "pro": ["所有免费功能", "不限次数使用", "高级行程规划", "定时推送", "多城市对比分析", "自定义报告模板"],
                "enterprise": ["所有专业版功能", "API接入", "企业级部署", "定制化开发", "技术支持"]
            }
            
            features_json = json.dumps(features.get(tier, []), ensure_ascii=False)
            
            cursor.execute('''
                INSERT OR REPLACE INTO subscriptions 
                (user_id, tier, start_date, end_date, is_active, features)
                VALUES (?, ?, ?, ?, 1, ?)
            ''', (user_id, tier, now, end_date, features_json))
            
            conn.commit()
            conn.close()
            
            logger.info(f"更新用户订阅：{user_id} -> {tier}，有效期{duration_days}天")
            return True
            
        except Exception as e:
            logger.error(f"更新订阅失败：{str(e)}")
            return False
    
    def get_subscription(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户订阅信息
        :param user_id: 用户ID
        :return: 订阅信息字典
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT tier, start_date, end_date, is_active, features
                FROM subscriptions
                WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                tier, start_date, end_date, is_active, features_json = result
                features = json.loads(features_json) if features_json else []
                
                # 检查订阅是否过期
                now = int(time.time())
                is_expired = end_date < now if end_date else False
                is_active = is_active and not is_expired
                
                # 计算剩余天数
                remaining_days = max(0, (end_date - now) // 86400) if end_date else 0
                
                return {
                    "user_id": user_id,
                    "tier": tier,
                    "start_date": start_date,
                    "start_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_date)),
                    "end_date": end_date,
                    "end_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_date)) if end_date else None,
                    "is_active": is_active,
                    "is_expired": is_expired,
                    "remaining_days": remaining_days,
                    "features": features
                }
            else:
                # 默认免费订阅
                return {
                    "user_id": user_id,
                    "tier": "free",
                    "is_active": True,
                    "is_expired": False,
                    "remaining_days": -1,
                    "features": ["基础文旅监测", "天气查询", "景点推荐"]
                }
            
        except Exception as e:
            logger.error(f"获取订阅信息失败：{str(e)}")
            return {
                "user_id": user_id,
                "tier": "free",
                "is_active": True,
                "features": ["基础文旅监测", "天气查询", "景点推荐"]
            }
    
    def has_feature_permission(self, user_id: str, feature: str) -> bool:
        """
        检查用户是否有指定功能的权限
        :param user_id: 用户ID
        :param feature: 功能名称
        :return: True表示有权限
        """
        try:
            subscription = self.get_subscription(user_id)
            return feature in subscription.get("features", [])
            
        except Exception as e:
            logger.error(f"检查功能权限失败：{str(e)}")
            return False
    
    def get_usage_report(self, user_id: str) -> str:
        """
        生成用户使用报告（Markdown格式）
        """
        monthly_usage = self.get_monthly_usage(user_id)
        daily_usage = self.get_daily_usage(user_id)
        subscription = self.get_subscription(user_id)
        
        # 订阅等级显示
        tier_names = {
            "free": "🆓 免费版",
            "pro": "💎 专业版",
            "enterprise": "🏢 企业版"
        }
        
        report = f"""# 📊 使用统计报告
**用户ID**：{user_id}
**订阅等级**：{tier_names.get(subscription['tier'], subscription['tier'])}
**订阅状态**：{'✅ 正常' if subscription['is_active'] else '❌ 已过期'}
"""
        
        if subscription['tier'] != 'free' and subscription['is_active']:
            report += f"**剩余有效期**：{subscription['remaining_days']} 天\n"
        
        report += f"""
## 📈 本月使用情况（{monthly_usage.get('year', '')}年{monthly_usage.get('month', '')}月）
- 总调用次数：{monthly_usage.get('total_calls', 0)} 次
- 总API费用：¥ {monthly_usage.get('total_cost', 0.0):.2f}
- 总Token消耗：{monthly_usage.get('total_tokens', 0)}
- 费用阈值：¥ {self.alert_threshold:.2f} {'⚠️ 已超过阈值' if monthly_usage.get('over_threshold', False) else ''}

## 📅 今日使用情况
- 调用次数：{daily_usage.get('total_calls', 0)} 次
- API费用：¥ {daily_usage.get('total_cost', 0.0):.2f}
- Token消耗：{daily_usage.get('total_tokens', 0)}

## 💰 API调用明细
"""
        
        api_breakdown = monthly_usage.get('api_breakdown', {})
        if api_breakdown:
            report += "| API类型 | 调用次数 | 费用 | Token消耗 |\n"
            report += "|----------|----------|------|----------|\n"
            for api_type, data in api_breakdown.items():
                type_names = {
                    "baidu_search": "百度搜索",
                    "multi_search": "多引擎搜索",
                    "llm_gpt35": "GPT-3.5",
                    "llm_gpt4": "GPT-4",
                    "llm_qwen": "通义千问",
                    "llm_ernie": "文心一言"
                }
                name = type_names.get(api_type, api_type)
                report += f"| {name} | {data['calls']} | ¥ {data['cost']:.2f} | {data['tokens']} |\n"
        else:
            report += "本月暂无API调用记录\n"
        
        report += """
## 💡 费用说明
- API调用费用由第三方服务商收取，本工具仅做统计参考
- 实际费用以服务商账单为准
- 可在配置中调整费用提醒阈值
"""
        
        return report
    
    def is_new_user(self, user_id: str) -> bool:
        """
        检查是否为新用户（从未使用过）
        :param user_id: 用户ID
        :return: 是否为新用户
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查是否有使用记录
            cursor.execute('''
                SELECT COUNT(*) FROM api_calls WHERE user_id = ?
            ''', (user_id,))
            
            call_count = cursor.fetchone()[0]
            
            # 检查是否领取过体验期
            cursor.execute('''
                SELECT COUNT(*) FROM trial_periods WHERE user_id = ?
            ''', (user_id,))
            
            trial_count = cursor.fetchone()[0]
            
            conn.close()
            
            return call_count == 0 and trial_count == 0
            
        except Exception as e:
            logger.error(f"检查新用户失败：{str(e)}")
            return False
    
    def activate_trial_period(self, user_id: str) -> bool:
        """
        激活新用户7天体验期
        :param user_id: 用户ID
        :return: 是否激活成功
        """
        try:
            if not self.is_new_user(user_id):
                logger.warning(f"用户 {user_id} 不是新用户，无法激活体验期")
                return False
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = int(time.time())
            today = datetime.now().strftime("%Y-%m-%d")
            end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            
            cursor.execute('''
                INSERT INTO trial_periods 
                (user_id, start_date, end_date, is_activated, created_at, updated_at)
                VALUES (?, ?, ?, 1, ?, ?)
            ''', (user_id, today, end_date, now, now))
            
            conn.commit()
            conn.close()
            
            logger.info(f"用户 {user_id} 7天体验期已激活，有效期至 {end_date}")
            return True
            
        except Exception as e:
            logger.error(f"激活体验期失败：{str(e)}")
            return False
    
    def is_in_trial_period(self, user_id: str) -> bool:
        """
        检查用户是否在体验期内
        :param user_id: 用户ID
        :return: 是否在体验期内
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            cursor.execute('''
                SELECT end_date, is_activated FROM trial_periods
                WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return False
            
            end_date, is_activated = result
            return is_activated == 1 and today <= end_date
            
        except Exception as e:
            logger.error(f"检查体验期失败：{str(e)}")
            return False
    
    def get_trial_remaining_days(self, user_id: str) -> int:
        """
        获取体验期剩余天数
        :param user_id: 用户ID
        :return: 剩余天数，0表示已过期或未激活
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().strftime("%Y-%m-%d")
            today_dt = datetime.strptime(today, "%Y-%m-%d")
            
            cursor.execute('''
                SELECT end_date FROM trial_periods
                WHERE user_id = ? AND is_activated = 1
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return 0
            
            end_date = result[0]
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            remaining = (end_dt - today_dt).days  # 不包含结束当天，确保正好7天
            
            return max(0, remaining)
            
        except Exception as e:
            logger.error(f"获取体验期剩余天数失败：{str(e)}")
            return 0
    
    def record_premium_usage(self, user_id: str) -> bool:
        """
        记录高级功能调用次数
        :param user_id: 用户ID
        :return: 是否记录成功
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().strftime("%Y-%m-%d")
            now = int(time.time())
            
            # 尝试更新现有记录
            cursor.execute('''
                UPDATE daily_premium_usage 
                SET count = count + 1
                WHERE user_id = ? AND date = ?
            ''', (user_id, today))
            
            if cursor.rowcount == 0:
                # 没有今日记录，插入新记录
                cursor.execute('''
                    INSERT INTO daily_premium_usage (user_id, date, count)
                    VALUES (?, ?, 1)
                ''', (user_id, today))
            
            conn.commit()
            conn.close()
            
            logger.debug(f"记录用户 {user_id} 高级功能调用，今日累计：{self.get_daily_premium_usage(user_id)}次")
            return True
            
        except Exception as e:
            logger.error(f"记录高级功能调用失败：{str(e)}")
            return False
    
    def get_daily_premium_usage(self, user_id: str) -> int:
        """
        获取用户当日高级功能调用次数
        :param user_id: 用户ID
        :return: 调用次数
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            cursor.execute('''
                SELECT count FROM daily_premium_usage
                WHERE user_id = ? AND date = ?
            ''', (user_id, today))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else 0
            
        except Exception as e:
            logger.error(f"获取高级功能调用次数失败：{str(e)}")
            return 0
    
    def check_premium_daily_limit(self, user_id: str, limit: int = 10) -> bool:
        """
        检查高级功能当日调用是否超过限制
        :param user_id: 用户ID
        :param limit: 每日限制次数，默认10次
        :return: 是否在限制内（True=未超过，False=已超过）
        """
        usage = self.get_daily_premium_usage(user_id)
        return usage < limit
