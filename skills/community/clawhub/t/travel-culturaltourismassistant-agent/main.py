# 安全模块导入
from core.security import (
    validate_user_input, sanitize_user_input, is_prompt_injection,
    filter_sensitive_data, validate_city_name, validate_date, validate_parameters
)

async def handle_comparison_analysis(args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理多城市对比分析命令
    格式：对比分析 <城市1> <城市2> [城市3...] [开始日期] [结束日期]
    """
    user_id = context.get('user_id', 'unknown')
    
    # 权限验证
    has_permission, permission_msg = subscription_manager.has_permission(user_id, "comparison_analysis")
    if not has_permission:
        return {
            "status": "error",
            "message": permission_msg,
            "render": "markdown"
        }
    
    if len(args) < 2:
        return {
            "status": "error",
            "message": "参数错误，正确格式：对比分析 <城市1> <城市2> [城市3...] [开始日期] [结束日期]\n示例：对比分析 北京 上海 2024-05-01 2024-05-07"
        }
    
    # 解析参数：提取城市和日期
    cities = []
    start_date = None
    end_date = None
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    
    for arg in args:
        if re.match(date_pattern, arg):
            # 验证日期合法性
            if not validate_date(arg):
                return {
                    "status": "error",
                    "message": f"⚠️ 日期格式错误：{arg}，请使用 YYYY-MM-DD 格式",
                    "render": "markdown"
                }
            if not start_date:
                start_date = arg
            else:
                end_date = arg
        else:
            # 验证城市名称合法性
            if not validate_city_name(arg):
                return {
                    "status": "error",
                    "message": f"⚠️ 城市名称包含非法字符：{arg}",
                    "render": "markdown"
                }
            cities.append(arg)
    
    if len(cities) < 2:
        return {
            "status": "error",
            "message": "至少需要对比2个城市，最多支持5个城市对比"
        }
    
    if len(cities) > 5:
        return {
            "status": "error",
            "message": "最多支持5个城市同时对比"
        }
    
    # 默认日期范围：未来7天
    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    elif not end_date:
        end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d")
    
    # 验证日期格式
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return {
            "status": "error",
            "message": "日期格式错误，请使用 YYYY-MM-DD 格式，例如：2024-05-01"
        }
    
    if start > end:
        return {
            "status": "error",
            "message": "开始日期不能晚于结束日期"
        }
    
    if (end - start).days > 30:
        return {
            "status": "error",
            "message": "对比时间范围不能超过30天"
        }
    
    logger.info(f"开始多城市对比分析：{', '.join(cities)}，时间范围：{start_date}至{end_date}")
    
    # 记录用户偏好
    if user_id:
        for city in cities:
            preference_manager.record_preference(user_id, "compared_cities", city)
    
    # 执行对比分析
    try:
        comparison_result = await skill_orchestrator.execute_comparison_analysis(
            cities=cities,
            start_date=start_date,
            end_date=end_date
        )
        
        # 生成对比报告
        report = report_generator.generate_comparison_report(
            cities=cities,
            start_date=start_date,
            end_date=end_date,
            data=comparison_result
        )
        
        return {
            "status": "success",
            "message": f"✅ {len(cities)}城文旅数据对比报告",
            "data": report,
            "render": "markdown"
        }
        
    except Exception as e:
        logger.error(f"对比分析失败：{str(e)}")
        return {
            "status": "error",
            "message": f"对比分析失败：{str(e)}\n请检查 API Key 配置是否正确"
        }

async def handle_scheduled_push(args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理定时推送设置命令
    格式：定时推送 <城市> <频率> <时间>
    """
    user_id = context.get('user_id', 'unknown')
    
    # 权限验证
    has_permission, permission_msg = subscription_manager.has_permission(user_id, "scheduled_push")
    if not has_permission:
        return {
            "status": "error",
            "message": permission_msg,
            "render": "markdown"
        }
    
    if len(args) < 3:
        return {
            "status": "error",
            "message": "参数错误，正确格式：定时推送 <城市> <频率> <时间>\n示例：定时推送 北京 每日 09:00\n频率支持：每日/每周/每月"
        }
    
    city = args[0]
    frequency = args[1]
    push_time = args[2]
    
    # 验证频率
    if frequency not in ["每日", "每周", "每月", "daily", "weekly", "monthly"]:
        return {
            "status": "error",
            "message": "频率格式错误，支持：每日/每周/每月 或 daily/weekly/monthly"
        }
    
    # 验证时间格式
    time_pattern = r'^\d{2}:\d{2}$'
    if not re.match(time_pattern, push_time):
        return {
            "status": "error",
            "message": "时间格式错误，请使用 HH:MM 格式，例如：09:00"
        }
    
    # 转换为标准频率标识
    freq_map = {
        "每日": "daily",
        "每周": "weekly",
        "每月": "monthly",
        "daily": "daily",
        "weekly": "weekly",
        "monthly": "monthly"
    }
    frequency = freq_map[frequency]
    
    logger.info(f"设置定时推送：城市={city}，频率={frequency}，时间={push_time}，用户={user_id}")
    
    try:
        # 设置定时推送任务
        result = await skill_orchestrator.setup_scheduled_push(
            user_id=user_id,
            city=city,
            frequency=frequency,
            push_time=push_time
        )
        
        return {
            "status": "success",
            "message": "✅ 定时推送设置成功",
            "data": f"""
# 🕒 定时推送设置成功
**城市**：{city}
**频率**：{frequency}
**推送时间**：{push_time}

推送内容包含：
- 当日天气预报和出行建议
- 热门景点人流量预测
- 文旅舆情动态
- 定制化出行建议

系统会在设定时间自动将报告推送给你，如需修改或取消，请重新设置。
""",
            "render": "markdown"
        }
        
    except Exception as e:
        logger.error(f"定时推送设置失败：{str(e)}")
        return {
            "status": "error",
            "message": f"设置失败：{str(e)}"
        }

async def handle_custom_report(args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理自定义报告命令
    格式：自定义报告 <模板名称> [参数]
    """
    user_id = context.get('user_id', 'unknown')
    
    # 权限验证
    has_permission, permission_msg = subscription_manager.has_permission(user_id, "custom_report")
    if not has_permission:
        return {
            "status": "error",
            "message": permission_msg,
            "render": "markdown"
        }
    
    if len(args) < 1:
        return {
            "status": "error",
            "message": "参数错误，正确格式：自定义报告 <模板名称> [参数]\n可用模板：daily_report, weekly_summary, trip_guide\n示例：自定义报告 weekly_summary 北京"
        }
    
    template_name = args[0]
    params = args[1:] if len(args) > 1 else []
    
    # 加载模板
    try:
        # 从用户配置中获取自定义模板，或使用内置模板
        template_config = config.get_custom_template(template_name)
        if not template_config:
            return {
                "status": "error",
                "message": f"模板 {template_name} 不存在，可用模板：daily_report, weekly_summary, trip_guide"
            }
        
        # 生成报告
        report_data = await skill_orchestrator.generate_custom_report(
            template_name=template_name,
            params=params,
            user_id=user_id
        )
        
        report = report_generator.generate_custom_report(
            template=template_config["content"],
            data=report_data
        )
        
        return {
            "status": "success",
            "message": f"✅ 自定义报告生成成功",
            "data": report,
            "render": "markdown"
        }
        
    except Exception as e:
        logger.error(f"自定义报告生成失败：{str(e)}")
        return {
            "status": "error",
            "message": f"生成失败：{str(e)}"
        }

async def handle_usage_stats(args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理使用统计命令
    格式：使用统计
    """
    user_id = context.get('user_id', 'unknown')
    
    try:
        stats = await usage_tracker.get_user_usage(user_id)
        subscription = await subscription_manager.get_user_subscription(user_id)
        
        return {
            "status": "success",
            "message": "✅ 使用统计查询成功",
            "data": f"""
# 📊 使用统计
**用户ID**：{user_id}
**订阅等级**：{subscription.get('tier', '免费版')}
**有效期至**：{subscription.get('expires_at', '永久有效')}

---

## 📈 本月使用情况
| 功能 | 已使用 | 剩余额度 |
|------|--------|----------|
| 文旅监测 | {stats.get('travel_monitor_count', 0)} 次 | {stats.get('travel_monitor_remaining', '无限制') if subscription.get('tier') in ['pro', 'enterprise'] else max(0, 3 - stats.get('travel_monitor_count', 0))} 次 |
| 行程规划 | {stats.get('trip_planner_count', 0)} 次 | {stats.get('trip_planner_remaining', '无限制') if subscription.get('tier') in ['pro', 'enterprise'] else '需升级专业版'} |
| 对比分析 | {stats.get('comparison_count', 0)} 次 | {stats.get('comparison_remaining', '无限制') if subscription.get('tier') in ['pro', 'enterprise'] else '需升级专业版'} |
| 定时推送 | {stats.get('scheduled_push_count', 0)} 次 | {stats.get('scheduled_push_remaining', '无限制') if subscription.get('tier') in ['pro', 'enterprise'] else '需升级专业版'} |

---

## 💰 API费用统计
| 项目 | 金额 |
|------|------|
| 本月累计费用 | ¥ {stats.get('total_cost', 0):.2f} |
| 本月剩余额度 | ¥ {max(0, config.get_setting('cost_alert_threshold', 10) - stats.get('total_cost', 0)):.2f} |
| 上次扣费时间 | {stats.get('last_charge_time', '无')} |

---

## 💡 升级提示
当前为{subscription.get('tier', '免费版')}，升级到专业版（¥9.9/月）即可享受：
✅ 不限次数使用所有功能
✅ 高级行程规划
✅ 多城市对比分析
✅ 定时推送服务
✅ 自定义报告模板
""",
            "render": "markdown"
        }
        
    except Exception as e:
        logger.error(f"获取使用统计失败：{str(e)}")
        return {
            "status": "error",
            "message": f"获取统计失败：{str(e)}"
        }

async def handle_help(args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理帮助命令
    格式：文旅帮助
    """
    user_id = context.get('user_id', 'unknown')
    subscription = await subscription_manager.get_user_subscription(user_id)
    tier = subscription.get('tier', 'free')
    
    help_content = f"""
# 🎯 文旅智能体使用帮助
当前版本：{config.get('version', '1.0.0')}
当前订阅：{ '免费版' if tier == 'free' else '专业版' if tier == 'pro' else '企业版' }

---

## 📋 可用命令
"""
    
    # 基础命令（所有用户可用）
    help_content += """
### 🆓 基础功能（免费版可用）
| 命令 | 功能 | 示例 |
|------|------|------|
| 监测文旅 <城市> <开始日期> <结束日期> | 文旅监测报告 | `监测文旅 北京 2024-05-01 2024-05-07` |
| 天气查询 <城市> [日期] | 查询天气信息 | `天气查询 北京 2024-05-01` |
| 景点推荐 <城市> [分类] [数量] | 景点推荐 | `景点推荐 北京 文化古迹 5` |
| 使用统计 | 查看使用情况和费用 | `使用统计` |
| 文旅帮助 | 查看帮助文档 | `文旅帮助` |
"""
    
    # 专业版功能
    if tier in ['pro', 'enterprise']:
        help_content += """
### 💎 高级功能（专业版/企业版可用）
| 命令 | 功能 | 示例 |
|------|------|------|
| 行程规划 <城市> <天数> [偏好] | 智能行程规划 | `行程规划 北京 3 文化,美食` |
| 对比分析 <城市1> <城市2> [城市3...] [日期] | 多城市对比分析 | `对比分析 北京 上海 2024-05-01` |
| 定时推送 <城市> <频率> <时间> | 设置定时推送 | `定时推送 北京 每日 09:00` |
| 自定义报告 <模板> [参数] | 生成自定义报告 | `自定义报告 weekly_summary 北京` |
"""
    else:
        help_content += """
### 💎 升级专业版解锁更多功能
专业版仅需 ¥9.9/月，即可解锁：
✅ 智能行程规划
✅ 多城市对比分析
✅ 定时推送服务
✅ 自定义报告模板
✅ 不限使用次数
"""
    
    help_content += """
---

## ⚙️ 配置说明
第一次使用需要配置以下 API Key：
1. 大模型 API Key（支持 OpenAI、通义千问、文心一言等）
2. 百度搜索 API Key 和 Secret Key

配置完成后即可正常使用所有功能。如有问题请联系技术支持。
"""
    
    return {
        "status": "success",
        "message": "📖 文旅智能体使用帮助",
        "data": help_content,
        "render": "markdown"
    }

# 命令路由
COMMAND_HANDLERS = {
    "监测文旅": handle_travel_monitor,
    "行程规划": handle_trip_planner,
    "天气查询": handle_weather_query,
    "景点推荐": handle_attraction_recommendation,
    "对比分析": handle_comparison_analysis,
    "定时推送": handle_scheduled_push,
    "自定义报告": handle_custom_report,
    "使用统计": handle_usage_stats,
    "文旅帮助": handle_help
}

# Skill 入口函数
async def main(command: str, args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Skill 主入口函数
    """
    # 全局安全检查
    try:
        # 1. 检测提示词注入
        full_input = f"{command} {' '.join(args)}"
        if is_prompt_injection(full_input):
            logger.warning(f"检测到提示词注入攻击，用户：{context.get('user_id', 'unknown')}，输入：{full_input[:100]}...")
            return {
                "status": "error",
                "message": "⚠️ 输入包含不安全内容，请求已被拦截",
                "render": "markdown"
            }
        
        # 2. 验证并清理所有用户输入
        sanitized_args = []
        for arg in args:
            if not validate_user_input(arg):
                return {
                    "status": "error",
                    "message": f"⚠️ 参数 '{arg[:20]}...' 包含非法内容",
                    "render": "markdown"
                }
            sanitized_args.append(sanitize_user_input(arg))
        
        # 3. 过滤上下文中的敏感数据
        safe_context = {k: filter_sensitive_data(str(v)) for k, v in context.items()}
        logger.info(f"收到命令：{command}，参数：{sanitized_args}，上下文：{safe_context}")
        
        # 使用清理后的参数
        args = sanitized_args
        
    except Exception as e:
        logger.error(f"安全检查失败：{str(e)}")
        return {
            "status": "error",
            "message": "⚠️ 安全检查失败，请稍后重试",
            "render": "markdown"
        }
    
    # 初始化全局实例
    global config, skill_orchestrator, subscription_manager, usage_tracker, preference_manager, report_generator
    
    try:
        # 加载配置
        config = SkillConfig(context.get('config', {}))
        
        # 初始化工具
        cache = CacheManager(config)
        usage_tracker = UsageTracker(config)
        preference_manager = UserPreferenceManager(config)
        subscription_manager = SubscriptionManager(config)
        
        # 初始化报告生成器
        report_generator = ReportGenerator(config)
        
        # 初始化技能编排器
        skill_orchestrator = SkillOrchestrator(
            config=config,
            cache=cache,
            preference_manager=preference_manager,
            usage_tracker=usage_tracker
        )
        
        # 注入报告生成器
        skill_orchestrator.report_generator = report_generator
        
        # 处理命令
        handler = COMMAND_HANDLERS.get(command)
        if not handler:
            return {
                "status": "error",
                "message": f"未知命令：{command}\n可用命令：{', '.join(COMMAND_HANDLERS.keys())}\n输入「文旅帮助」查看详细说明"
            }
        
        # 执行命令
        result = await handler(args, context)
        
        # 记录使用情况
        user_id = context.get('user_id', 'unknown')
        await usage_tracker.track_usage(user_id, command, 1)
        
        return result
        
    except Exception as e:
        logger.error(f"命令执行失败：{str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"执行失败：{str(e)}\n请检查配置是否正确，或联系技术支持"
        }