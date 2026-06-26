---
name: Digital Human Operations Assistant
slug: bank-digital-human
description: AI-powered digital human (virtual avatar) operations assistant for financial institutions — covers script design, content planning, live streaming management, interaction optimization, and performance analytics. Built for bank and insurance digital marketing teams. Keywords: digital human, virtual avatar, live streaming, virtual spokesperson, financial marketing, 数字人, 虚拟主播, 直播运营, 虚拟形象, 金融营销, AI主播, 数字人运营, 虚拟人设.
version: "3.0.1"
---

# Digital Human Operations Assistant / 数字人运营助手


### 银行监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 银行监管 | 2026年Q1银行业合规管理有效性评估要求提升 | 数字人运营合规审核清单需更新 |
| 银行监管 | 数字人运营需纳入合规审查流程，确保内容合规 | 数字人运营合规审核清单需更新 |
| 银行监管 | 理财信息披露'三清'推进，数字人营销话术需更新 | 数字人运营合规审核清单需更新 |

> **数据截止**: 2026-05-25 | 来源：国家金融监督管理总局、安永Q1分析、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

> **English:** AI-powered digital human operations assistant — covers script design, content planning, live streaming, and performance analytics.
>
> **中文:** 数字人运营助手——覆盖话术设计、内容策划、直播管理、互动优化、效果分析。

---

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **内容创作耗时** | 数字人内容生产成本高 | AI自动生成脚本 |
| **互动性差** | 数字人缺乏人情味 | 个性化互动设计 |
| **场景单一** | 数字人应用场景受限 | 多场景内容矩阵 |
| **效果难评估** | 直播效果难以量化 | 数据分析模板 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** digital human, virtual avatar, live streaming, virtual spokesperson, AI streamer, content marketing

**中文触发词（优先）：** 数字人 / 虚拟主播 / 直播运营 / 虚拟形象 / AI主播 / 数字人直播 / 元宇宙 / 虚拟代言人 / 品牌IP / 内容创作 / 直播脚本 / 短视频 / 虚拟客服 / 数字员工

---

## Core Capabilities / 核心能力

### 1. Script Generation / 脚本生成

```python
SCRIPT_TEMPLATES = {
    "产品介绍类": {
        "时长": "2-3分钟",
        "结构": """
        【开场 Hook】（0-15秒）
        - 痛点引入："你是不是也遇到过...？"
        - 数据吸引："90%的人都不知道的..."
        
        【自我介绍】（15-30秒）
        - 虚拟形象介绍
        - 今日主题预告
        
        【核心内容】（1-2分钟）
        - 产品/服务介绍（3个卖点）
        - 场景化案例
        - 限时优惠/福利
        
        【行动号召 CTA】（15-30秒）
        - 关注引导
        - 评论区互动
        - 私信/链接
        
        【结尾】（0-15秒）
        - 回顾要点
        - 下期预告
        """
    },
    
    "知识科普类": {
        "时长": "1-2分钟",
        "结构": """
        【开场】："今天教你一个..."
        【问题】："为什么..."
        【解答】："因为..."
        【案例】："举个例子..."
        【总结】："所以..."
        """
    }
}

def generate_script(script_type: str, params: dict) -> dict:
    """
    生成数字人直播/视频脚本
    """
    template = SCRIPT_TEMPLATES.get(script_type)
    if not template:
        return {"error": "未知脚本类型"}
    
    # 生成台词
    script_content = generate_script_content(script_type, params)
    
    # 生成AI提示词
    ai_prompts = generate_ai_prompts(script_type, params)
    
    # 生成分镜
    storyboard = generate_storyboard(script_type, params)
    
    return {
        "script_type": script_type,
        "duration": template.get("时长", ""),
        "structure": template.get("结构", ""),
        "content": script_content,
        "ai_prompts": ai_prompts,
        "storyboard": storyboard
    }
```

### 2. Content Calendar / 内容日历

```markdown
## 数字人内容日历模板

### 周内容规划

| 日期 | 内容类型 | 主题 | 数字人形象 | KPI目标 |
|-----|---------|------|-----------|--------|
| 周一 | 产品种草 | 周一理财推荐 | 职业装版 | 点赞+100 |
| 周二 | 知识科普 | 金融小知识 | 学院风 | 收藏+50 |
| 周三 | 互动问答 | 粉丝答疑 | 休闲风 | 评论+30 |
| 周四 | 案例分享 | 客户故事 | 职业装版 | 转发+20 |
| 周五 | 直播带货 | 周五秒杀 | 活力版 | GMV+X万 |
| 周六 | 用户UGC | 晒单有礼 | - | UGC+10 |
| 周日 | 下周预告 | 剧透福利 | 创意版 | 关注+50 |
```

### 数字人人设设定

```python
DIGITAL_HUMAN_PERSONAS = {
    "专业理财师": {
        "外观": "职业西装，30岁左右女性",
        "性格": "专业、亲切、值得信赖",
        "语言风格": "专业术语+通俗解释",
        "口头禅": "理财有道，生活无忧",
        "适用场景": "产品介绍、理财建议"
    },
    
    "活力小姐姐": {
        "外观": "休闲时尚，25岁左右女性",
        "性格": "活泼、亲切、有趣",
        "语言风格": "网络用语、emoji",
        "口头禅": "冲冲冲！买它！",
        "适用场景": "直播带货、互动活动"
    },
    
    "专业分析师": {
        "外观": "商务男装，35岁左右男性",
        "性格": "理性、严谨、权威",
        "语言风格": "数据分析、图表解读",
        "口头禅": "数据不会说谎",
        "适用场景": "市场分析、宏观解读"
    }
}
```

### 3. Performance Analytics / 效果分析

```python
class DigitalHumanAnalytics:
    """数字人效果分析"""
    
    def analyze_performance(self, video_stats: dict) -> dict:
        """
        分析视频/直播效果
        """
        # 核心指标
        metrics = {
            "播放量": video_stats.get("views", 0),
            "完播率": video_stats.get("completion_rate", 0),
            "点赞数": video_stats.get("likes", 0),
            "评论数": video_stats.get("comments", 0),
            "转发数": video_stats.get("shares", 0),
            "关注转化": video_stats.get("follows", 0)
        }
        
        # 计算互动率
        engagement_rate = (
            (metrics["点赞数"] + metrics["评论数"] + metrics["转发数"]) /
            max(metrics["播放量"], 1) * 100
        )
        
        # 评分
        score = self._calculate_content_score(metrics)
        
        return {
            "metrics": metrics,
            "engagement_rate": round(engagement_rate, 2),
            "content_score": score,
            "optimization_suggestions": self._get_suggestions(metrics),
            "benchmark_comparison": self._compare_to_benchmark(metrics)
        }
    
    def _calculate_content_score(self, metrics: dict) -> float:
        """内容评分（满分100）"""
        score = 0
        
        # 完播率（30分）
        score += min(metrics["完播率"] / 100 * 30, 30)
        
        # 互动率（40分）
        engagement = (
            (metrics["点赞数"] + metrics["评论数"]) /
            max(metrics["播放量"], 1)
        )
        score += min(engagement * 400, 40)  # 2.5%互动率=满分
        
        # 关注转化（30分）
        follow_rate = metrics["关注转化"] / max(metrics["播放量"], 1)
        score += min(follow_rate * 3000, 30)  # 1%关注率=满分
        
        return round(score, 1)
```

---

## Disclaimer

This skill provides digital human content planning tools for educational purposes. All content must comply with applicable advertising and financial marketing regulations.
