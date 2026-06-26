# -*- coding: utf-8 -*-
"""
订阅管理模块，对接 Claw Mart 订阅系统
"""
from typing import Dict, Any, Optional
from loguru import logger
from utils.usage_tracker import UsageTracker
# 尝试导入 Claw Mart 订阅 SDK
try:
    from claw_mart import check_subscription, get_user_tier, get_feature_access
    CLAW_MART_AVAILABLE = True
except ImportError:
    CLAW_MART_AVAILABLE = False
    logger.warning("Claw Mart SDK 不可用，使用本地模拟订阅系统")
class SubscriptionManager:
    """
    订阅管理器，处理订阅验证和权限控制
    """
    
    def __init__(self, usage_tracker: UsageTracker):
        self.usage_tracker = usage_tracker
        self.free_daily_limit = 3  # 免费版每日调用限制
        self.trial_premium_daily_limit = 10  # 体验期每日高级功能调用限制
    
    def check_subscription(self, user_id: str) -> Dict[str, Any]:
        """
        检查用户订阅状态
        :param user_id: 用户ID
        :return: 订阅信息字典
        """
        if CLAW_MART_AVAILABLE:
            # 使用 Claw Mart 官方订阅系统
            try:
                subscription = check_subscription(user_id, "travel-ai-skill")
                return {
                    "tier": subscription.get("tier", "free"),
                    "is_active": subscription.get("is_active", True),
                    "features": subscription.get("features", []),
                    "remaining_days": subscription.get("remaining_days", 0),
                    "source": "claw_mart"
                }
            except Exception as e:
                logger.error(f"Claw Mart 订阅查询失败：{str(e)}，使用本地订阅信息")
        
        # 使用本地订阅系统
        local_subscription = self.usage_tracker.get_subscription(user_id)
        return {
            "tier": local_subscription.get("tier", "free"),
            "is_active": local_subscription.get("is_active", True),
            "features": local_subscription.get("features", []),
            "remaining_days": local_subscription.get("remaining_days", 0),
            "source": "local"
        }
    
    def has_permission(self, user_id: str, feature: str) -> tuple[bool, str]:
        """
        检查用户是否有指定功能的权限
        :param user_id: 用户ID
        :param feature: 功能名称
        :return: (是否有权限, 提示信息)
        """
        subscription = self.check_subscription(user_id)
        tier = subscription["tier"]
        is_active = subscription["is_active"]
        
        # 检查是否为新用户，自动激活7天体验期
        if self.usage_tracker.is_new_user(user_id):
            self.usage_tracker.activate_trial_period(user_id)
            remaining_days = 7
            return True, f"🎉 欢迎新用户！已为你激活7天专业版体验资格，剩余{remaining_days}天\n💡 体验期内每天可使用10次高级功能，到期后可订阅专业版继续使用"
        
        # 检查是否在体验期内
        is_in_trial = self.usage_tracker.is_in_trial_period(user_id)
        trial_remaining_days = self.usage_tracker.get_trial_remaining_days(user_id)
        
        if not is_active:
            # 体验期内用户即使订阅过期也可以使用高级功能
            if not is_in_trial:
                return False, "❌ Your subscription has expired, please renew to continue using advanced features"
        
        # 功能权限映射
        feature_tiers = {
            # 免费功能
            "monitor_travel": ["free", "pro", "enterprise"],
            "weather_query": ["free", "pro", "enterprise"],
            "attraction_recommendation": ["free", "pro", "enterprise"],
            "usage_stats": ["free", "pro", "enterprise"],
            "help": ["free", "pro", "enterprise"],
            
            # 专业版功能
            "trip_planner": ["pro", "enterprise"],
            "comparison_analysis": ["pro", "enterprise"],
            "scheduled_push": ["pro", "enterprise"],
            "custom_template": ["pro", "enterprise"],
            
            # 企业版功能
            "api_access": ["enterprise"],
            "custom_development": ["enterprise"],
            "technical_support": ["enterprise"]
        }
        
        allowed_tiers = feature_tiers.get(feature, [])
        is_premium_feature = feature in ["trip_planner", "comparison_analysis", "scheduled_push", "custom_template"]
        
        # 体验期内可以使用所有专业版功能
        if is_premium_feature and is_in_trial:
            # 检查体验期每日调用限制
            if not self.usage_tracker.check_premium_daily_limit(user_id, self.trial_premium_daily_limit):
                usage = self.usage_tracker.get_daily_premium_usage(user_id)
                return False, f"⚠️ 今日高级功能调用次数已用完（体验期每日限制{self.trial_premium_daily_limit}次）\n💡 明天可以继续使用，或订阅专业版解锁无限次数"
            
            # 记录调用次数
            self.usage_tracker.record_premium_usage(user_id)
            
            # 添加体验期提示
            remaining = self.usage_tracker.get_trial_remaining_days(user_id)
            usage = self.usage_tracker.get_daily_premium_usage(user_id)
            return True, f"ℹ️ 体验期剩余{remaining}天，今日已用高级功能{usage}/{self.trial_premium_daily_limit}次"
        
        # 正常权限检查
        if tier not in allowed_tiers:
            # 体验期已过期提示
            if is_premium_feature and trial_remaining_days == 0 and self.usage_tracker.get_trial_remaining_days(user_id) == 0:
                return False, f"⏰ 你的7天专业版体验期已结束\n\n💡 Upgrade to Pro to continue using:\n- Unlimited advanced features\n- Scheduled push service\n- Multi-city comparative analysis\n- Custom report templates\n\n仅需¥9.9/月，即可畅享所有专业功能！"
            
            # 获取需要的最低订阅等级
            required_tier = "Pro" if "pro" in allowed_tiers else "Enterprise"
            return False, f"✨ This feature requires {required_tier} subscription\n\n💡 Upgrade to Pro to unlock:\n- Unlimited usage\n- Advanced trip planning\n- Scheduled push function\n- Multi-city comparative analysis\n- Custom report templates\n\nGo to Claw Mart to subscribe and unlock all advanced features immediately!"
        
        # 检查免费版每日调用限制
        if tier == "free" and feature in ["monitor_travel", "weather_query", "attraction_recommendation"]:
            if not self.usage_tracker.check_daily_limit(user_id, self.free_daily_limit):
                return False, f"⚠️ Today's free call limit has been used up (limited to {self.free_daily_limit} times per day)\n\n💡 Upgrade to Pro to unlock unlimited usage, and there are more advanced features waiting for you to experience!"
        
        # 专业版/企业版用户记录高级功能调用
        if is_premium_feature and tier in ["pro", "enterprise"]:
            self.usage_tracker.record_premium_usage(user_id)
        
        return True, "Permission verification passed"
    
    def get_user_tier(self, user_id: str) -> str:
        """获取用户订阅等级"""
        subscription = self.check_subscription(user_id)
        return subscription["tier"]
    
    def is_free_user(self, user_id: str) -> bool:
        """是否是免费用户"""
        return self.get_user_tier(user_id) == "free"
    
    def is_pro_user(self, user_id: str) -> bool:
        """是否是专业版用户"""
        return self.get_user_tier(user_id) == "pro"
    
    def is_enterprise_user(self, user_id: str) -> bool:
        """是否是企业版用户"""
        return self.get_user_tier(user_id) == "enterprise"
    
    def get_feature_list(self, user_id: str) -> list:
        """获取用户可用功能列表"""
        subscription = self.check_subscription(user_id)
        return subscription.get("features", [])
    
    def generate_subscription_info(self, user_id: str) -> str:
        """生成订阅信息报告（Markdown格式）"""
        subscription = self.check_subscription(user_id)
        tier = subscription["tier"]
        is_active = subscription["is_active"]
        remaining_days = subscription["remaining_days"]
        source = subscription["source"]
        
        # 订阅等级显示
        tier_info = {
            "free": {
                "name": "🆓 Free Version",
                "price": "Free",
                "features": [
                    "✅ 3 cultural tourism monitoring per day",
                    "✅ Weather query",
                    "✅ Attraction recommendation",
                    "❌ Trip planning",
                    "❌ Scheduled push",
                    "❌ Multi-city comparison"
                ]
            },
            "pro": {
                "name": "💎 Pro Version",
                "price": "¥9.9/month",
                "features": [
                    "✅ Unlimited usage",
                    "✅ Advanced trip planning",
                    "✅ Scheduled push function",
                    "✅ Multi-city comparative analysis",
                    "✅ Custom report templates",
                    "❌ API access",
                    "❌ Customized service"
                ]
            },
            "enterprise": {
                "name": "🏢 Enterprise Version",
                "price": "¥99/month",
                "features": [
                    "✅ All Pro version features",
                    "✅ API interface access",
                    "✅ Enterprise-level deployment",
                    "✅ Customized development",
                    "✅ Exclusive technical support"
                ]
            }
        }
        
        info = tier_info.get(tier, tier_info["free"])
        
        report = f"""# 💳 Subscription Information
**Current Tier**：{info['name']}
**Subscription Status**：{'✅ Active' if is_active else '❌ Expired'}
"""
        
        if tier != "free" and is_active:
            report += f"**Remaining Validity**：{remaining_days} days\n"
        
        if source == "claw_mart":
            report += "**Subscription Source**：Claw Mart official subscription\n"
        else:
            report += "**Subscription Source**：Local test subscription\n"
        
        report += """
## 💰 Pricing
| Version | Price |
|---------|-------|
| 🆓 Free | Free forever |
| 💎 Pro | ¥9.9/month |
| 🏢 Enterprise | ¥99/month |
## 🎯 Feature Comparison
"""
        
        for feature in info["features"]:
            report += f"- {feature}\n"
        
        if tier == "free":
            report += """
## Upgrade to Pro
Upgrade to Pro now to unlock:
- Unlimited usage of all features
- Advanced intelligent trip planning
- Scheduled push of cultural tourism monitoring reports
- Multi-city cultural tourism data comparison analysis
- Custom report templates
- Priority technical support
Search for "Cultural Tourism Agent" on Claw Mart to subscribe!
"""
        elif tier == "pro":
            report += """
## Upgrade to Enterprise
Upgrade to Enterprise for more exclusive services:
- API interface access, can be integrated into own system
- Enterprise-level private deployment
- Customized feature development
- Dedicated technical support team
- Service level agreement guarantee
Contact customer service for detailed enterprise version solutions!
"""
        
        return report
