#!/usr/bin/env python3
"""
AI运动计划生成器
- 基于用户画像生成个性化运动计划
- 支持多种目标：减脂/增肌/提升耐力/塑形/保持健康
- 集成《中国居民运动指南》建议
- 支持不同器材条件
"""

from datetime import date, timedelta
try:
    from .motion_db import CHINESE_EXERCISE_GUIDELINES, EXERCISE_LIBRARY
    from .calorie_calc import CalorieCalc
except ImportError:
    from motion_db import CHINESE_EXERCISE_GUIDELINES, EXERCISE_LIBRARY
    from calorie_calc import CalorieCalc


class PlanGenerator:
    def __init__(self):
        self.calc = CalorieCalc()

    def generate(self, profile: dict = None) -> dict:
        """根据用户档案生成个性化运动计划"""
        if profile is None:
            profile = self.calc.load_profile() or self._default_profile()

        goal = profile.get("goal", "保持健康")
        level = profile.get("level", "初级")
        equipment = profile.get("equipment", ["徒手"])
        days_per_week = profile.get("days_per_week", 3)
        time_per_session = profile.get("time_per_session", 45)

        plan = {
            "profile_summary": self._profile_summary(profile),
            "weekly_schedule": [],
            "warmup_routine": self._get_warmup(level),
            "cooldown_routine": self._get_cooldown(level),
            "guidelines": self._get_goal_guidelines(goal),
            "progression_tips": self._get_progression(level),
            "safety_reminders": self._get_safety(goal),
        }

        # 生成每周安排
        plan["weekly_schedule"] = self._build_weekly_schedule(
            goal=goal,
            level=level,
            days=days_per_week,
            time=time_per_session,
            equipment=equipment,
        )

        # 统计
        total_duration = sum(s["duration_min"] for s in plan["weekly_schedule"])
        plan["weekly_stats"] = {
            "total_sessions": len(plan["weekly_schedule"]),
            "total_duration_min": total_duration,
            "estimated_weekly_calories": self._estimate_weekly_calories(plan["weekly_schedule"], profile),
        }

        return plan

    def _default_profile(self) -> dict:
        return {
            "body": {"age": 30, "gender": "male", "height_cm": 170, "weight_kg": 70},
            "goal": "保持健康",
            "level": "初级",
            "equipment": ["徒手"],
            "days_per_week": 3,
            "time_per_session": 45,
        }

    def _profile_summary(self, profile: dict) -> str:
        body = profile.get("body", {})
        goal_map = {
            "减脂": "减脂塑形",
            "增肌": "增肌增重",
            "提升耐力": "提升心肺耐力",
            "塑形": "身体塑形",
            "保持健康": "保持健康体魄",
        }
        level_map = {"初级": "运动新手", "中级": "有一定基础", "高级": "经验丰富"}
        return (
            f"{body.get('age', 30)}岁 {body.get('gender', 'male')}，"
            f"{body.get('height_cm', 170)}cm {body.get('weight_kg', 70)}kg，"
            f"目标: {goal_map.get(profile.get('goal', '保持健康'), '保持健康')}，"
            f"水平: {level_map.get(profile.get('level', '初级'), '初级')}"
        )

    def _build_weekly_schedule(self, goal: str, level: str, days: int, time: int, equipment: list) -> list:
        """构建一周训练安排"""
        schedule = []
        templates = self._get_templates(goal)

        if days >= 7:
            # 每天都有安排，需要轮换
            rotation = templates[:days] * (days // len(templates) + 1)
            for i in range(days):
                day_name = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][i]
                t = rotation[i % len(rotation)]
                schedule.append(self._format_session(day_name, t, level, time, equipment))
        elif days >= 5:
            rest_days = 7 - days
            pattern = []
            for i in range(days):
                pattern.append("train")
                if i < rest_days:
                    pattern.append("rest")
            if len(pattern) < 7:
                pattern.extend(["rest"] * (7 - len(pattern)))
            
            day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
            ti = 0
            for i, dn in enumerate(day_names):
                if pattern[i] == "train" and ti < len(templates):
                    schedule.append(self._format_session(dn, templates[ti % len(templates)], level, time, equipment))
                    ti += 1
                else:
                    schedule.append({"day": dn, "type": "休息日", "activities": ["主动恢复: 散步30分钟或轻度拉伸"], "duration_min": 0})
        elif days >= 3:
            day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
            positions = []
            if days == 3:
                positions = [0, 2, 4]  # 周一三五
            elif days == 4:
                positions = [0, 2, 4, 6]  # 周一三五日

            for i, dn in enumerate(day_names):
                if i in positions and len(schedule) < len(templates):
                    schedule.append(self._format_session(dn, templates[len(schedule) % len(templates)], level, time, equipment))
                else:
                    schedule.append({"day": dn, "type": "休息日", "activities": ["休息，让身体恢复"], "duration_min": 0})
        else:
            # 1-2天
            day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
            for i in range(days):
                schedule.append(self._format_session(day_names[i * 3], templates[i % len(templates)], level, time, equipment))

        return schedule

    def _get_templates(self, goal: str) -> list:
        """根据目标获取训练模板"""
        templates_map = {
            "减脂": [
                {"type": "HIIT+力量循环", "activities": [
                    "热身5分钟（开合跳+高抬腿）",
                    "A1. 波比跳 30秒 × 4组",
                    "A2. 深蹲跳 15次 × 4组",
                    "A3. 登山跑 30秒 × 4组",
                    "A4. 俯卧撑 12次 × 4组",
                    "B. 跳绳 10分钟",
                    "拉伸放松5分钟",
                ]},
                {"type": "有氧耐力", "activities": [
                    "热身5分钟",
                    "慢跑/快走 30-40分钟（心率保持在燃脂区间）",
                    "拉伸放松5-10分钟",
                ]},
                {"type": "全身力量+核心", "activities": [
                    "热身5分钟",
                    "A1. 哑铃深蹲 12次 × 3组",
                    "A2. 哑铃划船 12次 × 3组",
                    "A3. 哑铃推举 12次 × 3组",
                    "B1. 平板支撑 45秒 × 3组",
                    "B2. 仰卧卷腹 20次 × 3组",
                    "B3. 俄罗斯转体 20次 × 3组",
                    "拉伸放松5分钟",
                ]},
            ],
            "增肌": [
                {"type": "上肢力量（推）", "activities": [
                    "热身5分钟（肩关节环绕+弹力带激活）",
                    "A1. 杠铃/哑铃卧推 10次 × 4组",
                    "A2. 哑铃推举 10次 × 3组",
                    "A3. 俯卧撑（负重） 12次 × 3组",
                    "B1. 侧平举 15次 × 3组",
                    "B2. 三头臂屈伸 12次 × 3组",
                    "拉伸放松5分钟",
                ]},
                {"type": "下肢力量", "activities": [
                    "热身5分钟",
                    "A1. 杠铃深蹲 8次 × 4组",
                    "A2. 罗马尼亚硬拉 10次 × 4组",
                    "A3. 保加利亚分腿蹲 10次/腿 × 3组",
                    "B1. 小腿提踵 20次 × 3组",
                    "拉伸放松5-10分钟",
                ]},
                {"type": "上肢力量（拉）+ 核心", "activities": [
                    "热身5分钟",
                    "A1. 引体向上/高位下拉 8次 × 4组",
                    "A2. 杠铃划船 10次 × 4组",
                    "A3. 哑铃弯举 12次 × 3组",
                    "B1. 悬垂举腿 15次 × 3组",
                    "B2. 平板支撑 60秒 × 3组",
                    "拉伸放松5分钟",
                ]},
            ],
            "提升耐力": [
                {"type": "耐力跑", "activities": [
                    "热身10分钟（慢跑+动态拉伸）",
                    "主课: 配速跑 30-40分钟（目标配速）",
                    "冷身5分钟慢走",
                    "拉伸放松10分钟",
                ]},
                {"type": "间歇训练", "activities": [
                    "热身10分钟",
                    "间歇跑: 400m × 6组（组间慢跑200m恢复）",
                    "或: 快跑1分钟+慢跑1分钟 × 10组",
                    "冷身5分钟",
                    "拉伸放松10分钟",
                ]},
                {"type": "交叉训练", "activities": [
                    "热身5分钟",
                    "骑行/游泳/椭圆机 30分钟（中等强度）",
                    "核心训练: 平板支撑+卷腹+侧桥 × 3组",
                    "拉伸放松5分钟",
                ]},
            ],
            "塑形": [
                {"type": "普拉提+瑜伽", "activities": [
                    "瑜伽拜日式 3轮热身",
                    "普拉提核心序列 20分钟",
                    "瑜伽塑形体式（战士系列+三角式+桥式）15分钟",
                    "大休息式放松5分钟",
                ]},
                {"type": "小重量高次数力量", "activities": [
                    "热身5分钟",
                    "A1. 哑铃深蹲 20次 × 3组（轻重量）",
                    "A2. 哑铃划船 20次 × 3组",
                    "A3. 哑铃飞鸟 15次 × 3组",
                    "B1. 臀桥 20次 × 3组",
                    "B2. 驴踢 15次/腿 × 3组",
                    "拉伸放松5分钟",
                ]},
                {"type": "有氧+核心", "activities": [
                    "跳绳/快走 20分钟",
                    "核心循环: 平板支撑+卷腹+俄罗斯转体+超人式 × 3轮",
                    "拉伸放松10分钟",
                ]},
            ],
            "保持健康": [
                {"type": "全身综合训练", "activities": [
                    "热身5分钟",
                    "快走/慢跑 15分钟",
                    "徒手力量: 深蹲+俯卧撑+平板支撑+臀桥 各3组",
                    "拉伸放松5-10分钟",
                ]},
                {"type": "有氧日", "activities": [
                    "热身5分钟",
                    "选择一项喜欢的有氧: 跑步/骑行/游泳/跳绳 30分钟",
                    "拉伸放松5分钟",
                ]},
                {"type": "柔韧日", "activities": [
                    "热身5分钟",
                    "瑜伽/太极/拉伸 30分钟",
                    "大休息式放松5分钟",
                ]},
            ],
        }

        return templates_map.get(goal, templates_map["保持健康"])

    def _format_session(self, day_name: str, template: dict, level: str, time: int, equipment: list) -> dict:
        """格式化训练课"""
        # 根据水平调整强度
        level_multiplier = {"初级": 0.7, "中级": 1.0, "高级": 1.3}
        mult = level_multiplier.get(level, 1.0)

        # 根据器材可用性调整
        has_equipment = any(e in str(equipment) for e in ["哑铃", "杠铃", "器械"])
        activities = template["activities"]
        if not has_equipment:
            # 徒手替代方案
            activities = [
                a.replace("哑铃", "徒手").replace("杠铃", "徒手").replace("器械", "徒手")
                for a in activities
            ]
            # 调整次数（徒手替代哑铃时增加次数）
            activities = [
                re.sub(r'(\d+)次', lambda m: str(int(int(m.group(1)) * 1.5)) + '次', a)
                if '徒手' in a else a
                for a in activities
            ]
        
        import re as _re

        return {
            "day": day_name,
            "type": template["type"],
            "activities": activities,
            "duration_min": int(time * mult),
        }

    def _get_warmup(self, level: str) -> list:
        if level == "高级":
            return [
                "动态拉伸: 抱膝走 20步，股四头肌拉伸 20步",
                "关节活动: 肩/髋/膝/踝关节环绕各10次",
                "激活: 弹力带臀桥 15次，肩胛骨激活 15次",
                "低强度有氧: 慢跑/跳绳 3-5分钟",
            ]
        return [
            "慢走/开合跳 3-5分钟",
            "动态拉伸: 抱膝走 10步/侧，腿后侧拉伸 10次/侧",
            "关节环绕: 颈部→肩→髋→膝→踝",
            "动作准备: 徒手深蹲 10次，俯卧撑 5次（唤醒身体）",
        ]

    def _get_cooldown(self, level: str) -> list:
        return [
            "低强度有氧 3-5分钟（慢走至心率恢复）",
            "静态拉伸: 每个部位保持20-30秒",
            "重点拉伸当天训练过的肌群",
            "深呼吸放松 1-2分钟",
        ]

    def _get_goal_guidelines(self, goal: str) -> dict:
        guidelines = CHINESE_EXERCISE_GUIDELINES.copy()
        if goal in guidelines:
            return guidelines[goal]
        return guidelines["adult"]

    def _get_progression(self, level: str) -> list:
        if level == "初级":
            return [
                "第1-2周: 以掌握动作为主，不追求强度",
                "第3-4周: 逐渐增加运动时长和组数",
                "第5-8周: 可开始小幅增加负重（2.5-5kg）",
                "持续记录感受，根据身体反馈调整",
            ]
        elif level == "中级":
            return [
                "每2周评估一次，调整训练量和强度",
                "可以尝试新的训练模式（递减组、超级组等）",
                "加入周期性训练概念（增负荷周+减负荷周）",
            ]
        else:
            return [
                "采用周期化训练，每4-6周更换训练重点",
                "关注训练质量而非数量，避免过度训练",
                "可加入竞赛/挑战目标保持动力",
            ]

    def _get_safety(self, goal: str) -> list:
        reminders = [
            "每次运动前必须热身，运动后必须拉伸",
            "运动中如感到头晕、胸闷、剧痛，立即停止",
            "保证充足睡眠（7-8小时），睡眠是恢复的关键",
            "运动后30分钟内补充蛋白质和碳水",
        ]
        if goal == "增肌":
            reminders.append("确保每日蛋白质摄入达到每kg体重1.6-2.2g")
        elif goal == "减脂":
            reminders.append("减脂期保持热量缺口300-500 kcal，但不过度节食")
        return reminders

    def _estimate_weekly_calories(self, schedule: list, profile: dict) -> int:
        """估算一周总消耗"""
        weight = profile.get("body", {}).get("weight_kg", 70)
        total = 0
        for session in schedule:
            if session["type"] == "休息日":
                continue
            dur_h = session["duration_min"] / 60.0
            # 估算综合MET
            if "HIIT" in session["type"]:
                met = 10
            elif "力量" in session["type"]:
                met = 5
            elif "有氧" in session["type"] or "跑" in session["type"]:
                met = 8
            elif "瑜伽" in session["type"] or "普拉提" in session["type"]:
                met = 3
            elif "柔韧" in session["type"]:
                met = 2.5
            else:
                met = 6
            total += met * weight * dur_h
        return int(total)

    def format_plan_text(self, plan: dict) -> str:
        """将计划格式化为可读文本"""
        lines = [
            "=" * 50,
            "🏋️  个性化运动计划",
            "=" * 50,
            "",
            f"👤 {plan['profile_summary']}",
            "",
            "📅 每周训练安排",
            "-" * 30,
        ]

        for session in plan["weekly_schedule"]:
            icon = "🛌" if session["type"] == "休息日" else "🔥"
            lines.append(f"\n{icon} {session['day']}: {session['type']}")
            if session["duration_min"] > 0:
                lines.append(f"   时长: ~{session['duration_min']}分钟")
            for act in session.get("activities", []):
                lines.append(f"   • {act}")

        lines.extend([
            "",
            "🔥 热身流程",
            "-" * 30,
        ])
        for step in plan["warmup_routine"]:
            lines.append(f"  • {step}")

        lines.extend([
            "",
            "🧊 放松流程",
            "-" * 30,
        ])
        for step in plan["cooldown_routine"]:
            lines.append(f"  • {step}")

        stats = plan["weekly_stats"]
        lines.extend([
            "",
            "📊 本周统计",
            "-" * 30,
            f"  训练次数: {stats['total_sessions']} 次",
            f"  总时长: {stats['total_duration_min']} 分钟",
            f"  预估消耗: ~{stats['estimated_weekly_calories']} kcal",
        ])

        lines.extend([
            "",
            "📈 进阶建议",
            "-" * 30,
        ])
        for tip in plan["progression_tips"]:
            lines.append(f"  • {tip}")

        lines.extend([
            "",
            "⚠️  安全提醒",
            "-" * 30,
        ])
        for r in plan["safety_reminders"]:
            lines.append(f"  • {r}")

        return "\n".join(lines)


import re as _re
