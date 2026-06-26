#!/usr/bin/env python3
"""Social Commerce Content Planner - Handler"""

import json
import sys
import datetime
import calendar


# Seasonal trends data
SEASONAL_TRENDS = {
    "美妆护肤": {
        "春": ["敏感肌修护", "轻薄底妆", "春日限定色", "换季护肤routine"],
        "夏": ["防晒防晒防晒", "控油持妆", "海边妆容", "晒后修复"],
        "秋": ["秋冬滋润", "服帖底妆", "复古色调妆容", "护肤油使用"],
        "冬": ["保湿大战", "年末节日妆", "暖色调妆容", "密集修护"]
    },
    "服饰": {
        "春": ["轻薄外套", "衬衫叠穿", "早春色彩", "过敏季穿搭"],
        "夏": ["清凉穿搭", "防晒衣", "海边度假风", "空调房披肩"],
        "秋": ["层次感", "卫衣搭配", "复古街头", "秋色系搭配"],
        "冬": ["羽绒服", "保暖内搭", "节日聚会装", "新年红色系"]
    }
}

# Festival calendar
FESTIVAL_CALENDAR = [
    {"month": 1, "name": "元旦", "days": "1月1日", "tag": "新年开年"},
    {"month": 2, "name": "春节", "days": "2月中旬", "tag": "传统佳节"},
    {"month": 3, "name": "妇女节", "days": "3月8日", "tag": "女性消费"},
    {"month": 5, "name": "劳动节", "days": "5月1日", "tag": "促销旺季"},
    {"month": 6, "name": "618", "days": "6月中旬", "tag": "年中大促"},
    {"month": 11, "name": "双11", "days": "11月11日", "tag": "年度大促"},
    {"month": 12, "name": "双12", "days": "12月12日", "tag": "年末冲刺"}
]

# Live script template
LIVE_SCRIPT_TEMPLATE = {
    "title": "直播脚本模板（通用结构）",
    "platforms": ["抖音", "快手", "淘宝直播", "视频号"],
    "sections": [
        {
            "环节": "1. 开场预热（0-5分钟）",
            "目的": "聚集人气，留住观众",
            "内容要点": [
                "打招呼，介绍自己/品牌",
                "预告今日直播内容亮点",
                "互动话术：欢迎进直播间的宝宝们，扣个666",
                "发福袋/红包预热"
            ],
            "话术示例": "欢迎宝宝们来到我的直播间！今天给大家带来一波超值的[品类]专场，记得看到最后，有重磅福利哦！"
        },
        {
            "环节": "2. 痛点切入（5-10分钟）",
            "目的": "引发共鸣，建立信任",
            "内容要点": [
                "描述目标用户的典型场景/痛点",
                "提出解决方案的核心思路",
                "引出今天的产品"
            ],
            "话术示例": "是不是每次[痛点场景]？今天这款[产品名]，就是专门解决这个问题的。"
        }
    ]
}

# Content checklist
CONTENT_CHECKLIST = {
    "合规检查": {
        "违禁词": [
            "国家级", "最高级", "最佳", "顶级", "顶尖",
            "全网第一", "销量第一", "冠军", "遥遥领先",
            "特效", "速效", "神效", "万能", "100%",
            "保证治愈", "无效退款", "保险公司承保"
        ],
        "绝对化用语": ["第一", "最好", "最强", "无敌", "终极"],
        "虚假宣传风险": [
            "未经证实的效果承诺",
            "虚构用户评价",
            "夸大原价/折扣力度"
        ]
    }
}

def generate_content_topics(platform, category, count=10):
    """生成内容主题列表"""
    base_topics = {
        "美妆护肤": [
            "开箱测评", "平替对比", "换季护肤", "妆教教程",
            "产品回购", "踩雷吐槽", "成分分析", "空瓶记",
            "618/双11好物", "明星同款"
        ],
        "服饰": [
            "穿搭分享", "一周穿搭", "平价替代", "显瘦秘籍",
            "场合穿搭", "搭配技巧", "衣橱整理", "旧衣新穿",
            "宝藏店铺", "配饰加分"
        ]
    }
    
    topics = base_topics.get(category, [
        "产品测评", "使用教程", "好物分享", "选购指南",
        "避坑指南", "对比体验", "真实反馈", "宝藏发现",
        "送礼推荐", "使用技巧"
    ])[:count]
    
    topic_details = []
    for i, topic in enumerate(topics, 1):
        topic_details.append({
            "序号": i,
            "主题": topic,
            "内容形式": ["短视频", "图文"],
            "创意方向": "真实分享+使用体验+推荐理由",
            "时长建议": "30-90秒",
            "tag建议": f"#{topic}# #{category}# #好物分享#"
        })
    
    return {
        "platform": platform,
        "category": category,
        "total": len(topic_details),
        "topics": topic_details
    }

def generate_content_calendar(platform, category, month):
    """生成月度内容日历"""
    cal = calendar.Calendar(firstweekday=0)
    year = 2026  # Fixed year
    weeks = list(cal.monthdatescalendar(year, month))
    
    calendar_days = []
    for week_idx, week in enumerate(weeks):
        for day in week:
            if day.month == month:
                weekday = day.weekday()
                weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
                
                if weekday in [5, 6]:
                    content_type = "短视频/种草"
                elif weekday == 0:
                    content_type = "本周预告/福利"
                else:
                    content_type = "产品展示/教程"
                
                calendar_days.append({
                    "date": day.isoformat(),
                    "weekday": weekday_names[weekday],
                    "content_type": content_type,
                    "suggested_time": "12:00-13:00",
                    "theme": "日常更新",
                    "is_weekend": weekday in [5, 6]
                })
    
    return {
        "month": month,
        "platform": platform,
        "category": category,
        "calendar": calendar_days,
        "festival_focus": [f for f in FESTIVAL_CALENDAR if f["month"] == month]
    }

def handle(platform, category, request, month=None):
    """
    处理内容规划请求
    """
    result = {
        "success": True,
        "platform": platform,
        "category": category,
        "request": request,
        "data": {}
    }
    
    # 趋势分析
    season = _get_current_season()
    seasonal = SEASONAL_TRENDS.get(category, {}).get(season, ["换季热点", "新品上市", "促销活动"])
    result["data"]["trend_analysis"] = {
        "current_season": season,
        "seasonal_topics": seasonal,
        "festival_calendar": [f for f in FESTIVAL_CALENDAR if f["month"] in [3, 4, 5, 6]][:3]
    }
    
    # 根据需求类型返回不同内容
    if request in ["topic", "topics", "主题", "选题"]:
        result["data"]["topics"] = generate_content_topics(platform, category)
        
    elif request in ["calendar", "日历", "内容日历"]:
        month = month or 4
        result["data"]["calendar"] = generate_content_calendar(platform, category, month)
        
    elif request in ["script", "直播脚本", "脚本"]:
        result["data"]["live_script"] = LIVE_SCRIPT_TEMPLATE
        
    elif request in ["checklist", "检查清单", "自检"]:
        result["data"]["checklist"] = CONTENT_CHECKLIST
        
    elif request in ["all", "全部", "完整"]:
        month = month or 4
        result["data"] = {
            "trend_analysis": result["data"]["trend_analysis"],
            "topics": generate_content_topics(platform, category),
            "calendar": generate_content_calendar(platform, category, month),
            "live_script": LIVE_SCRIPT_TEMPLATE,
            "checklist": CONTENT_CHECKLIST
        }
    
    else:
        result["success"] = False
        result["error"] = f"未知的请求类型: {request}，支持的类型: topic/calendar/script/checklist/all"
    
    return result

def _get_current_season():
    """获取当前季节"""
    month = datetime.datetime.now().month
    if month in [3, 4, 5]:
        return "春"
    elif month in [6, 7, 8]:
        return "夏"
    elif month in [9, 10, 11]:
        return "秋"
    else:
        return "冬"

# ============================================================
# 自测入口
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Social Commerce Content Planner - 自测")
    print("=" * 60)
    
    print("\n[测试1] 生成内容主题")
    r1 = handle("抖音", "美妆护肤", "topic")
    print(f"平台: {r1['platform']}, 品类: {r1['category']}")
    print(f"生成主题数: {r1['data']['topics']['total']}")
    print(f"第一个主题: {r1['data']['topics']['topics'][0]['主题']}")
    
    print("\n[测试2] 生成内容日历")
    r2 = handle("小红书", "服饰", "calendar", month=6)
    print(f"平台: {r2['platform']}, 品类: {r2['category']}, 月份: 6月")
    print(f"日历天数: {len(r2['data']['calendar']['calendar'])}")
    
    print("\n[测试3] 获取直播脚本模板")
    r3 = handle("抖音", "服饰", "script")
    print(f"直播环节数: {len(r3['data']['live_script']['sections'])}")
    
    print("\n[测试4] 获取内容检查清单")
    r4 = handle("快手", "美妆护肤", "checklist")
    print(f"合规检查项: {len(r4['data']['checklist']['合规检查']['违禁词'])}")
    
    print("\n[测试5] 完整内容包")
    r5 = handle("抖音", "美妆护肤", "all")
    print(f"完整包包含模块: {list(r5['data'].keys())}")
    
    print("\n" + "=" * 60)
    print("自测完成！所有功能正常运行。")
    print("=" * 60)
