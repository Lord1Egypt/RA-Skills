#!/usr/bin/env python3
"""
记忆系统强制执行器 v2.0
确保所有记忆都通过update_memory工具处理，绝不创建md文件
同时检查是否正确使用了workbuddy-add-memory技能
"""

import os
import sys
import json
import re
from datetime import datetime

class MemorySystemEnforcer:
    """记忆系统强制执行器，确保遵守主人指令"""
    
    def __init__(self):
        self.memory_path = "/Users/josieyang/.workbuddy/unified_memory/raw/"
        self.skill_name = "workbuddy-add-memory"
        self.required_skill_tag = "@skill://workbuddy-add-memory"
        
        self.forbidden_actions = [
            "创建md文件",
            "创建.md文件",
            "创建记忆文件",
            "创建总结文件",
            "创建错误总结"
        ]
        
        self.required_tool = "update_memory"
        self.required_skill_actions = [
            "use_skill.*workbuddy-add-memory",
            "python.*start_work.py",
            "cd.*workbuddy-add-memory.*start_work.py"
        ]
        
        # 技能使用历史
        self.skill_usage_history = {
            "total_checks": 0,
            "skill_used": 0,
            "skill_not_used": 0,
            "last_check_time": None,
            "error_patterns": []
        }
        
    def check_intent(self, task_description):
        """检查任务意图是否涉及记忆操作"""
        memory_keywords = [
            "记忆", "总结", "错误", "经验", "教训", "记录", 
            "学习", "分析", "反思", "评估", "检查"
        ]
        
        for keyword in memory_keywords:
            if keyword in task_description:
                return True
        return False
    
    def check_forbidden_actions(self, task_description):
        """检查是否包含禁止的操作"""
        violations = []
        for action in self.forbidden_actions:
            if action in task_description:
                violations.append(action)
        return violations
    
    def get_correct_action(self, task_description):
        """获取正确的操作方法"""
        if any(keyword in task_description for keyword in ["错误", "教训", "问题", "失败"]):
            return "使用update_memory工具记录错误教训"
        elif any(keyword in task_description for keyword in ["经验", "成功", "完成", "成果"]):
            return "使用update_memory工具记录成功经验"
        elif any(keyword in task_description for keyword in ["学习", "分析", "研究"]):
            return "使用update_memory工具记录学习心得"
        else:
            return "使用update_memory工具记录相关记忆"
    
    def check_skill_usage(self, task_description, actual_actions=None):
        """检查是否使用了workbuddy-add-memory技能"""
        self.skill_usage_history["total_checks"] += 1
        self.skill_usage_history["last_check_time"] = datetime.now().isoformat()
        
        # 检查任务是否应该使用技能
        should_use_skill = self._should_use_skill(task_description)
        
        if not should_use_skill:
            return True, "无需使用技能"
        
        # 检查实际动作
        skill_used = False
        if actual_actions:
            for pattern in self.required_skill_actions:
                if re.search(pattern, actual_actions, re.IGNORECASE):
                    skill_used = True
                    break
        
        if skill_used:
            self.skill_usage_history["skill_used"] += 1
            return True, "正确使用了workbuddy-add-memory技能"
        else:
            self.skill_usage_history["skill_not_used"] += 1
            error_msg = f"未使用workbuddy-add-memory技能（任务：{task_description[:50]}...）"
            self.skill_usage_history["error_patterns"].append({
                "time": datetime.now().isoformat(),
                "task": task_description,
                "error": "忘记使用技能"
            })
            return False, error_msg
    
    def _should_use_skill(self, task_description):
        """判断任务是否应该使用技能"""
        # 任务类型检查
        skill_related_keywords = [
            "记忆", "总结", "经验", "教训", "错误", "学习",
            "分析", "反思", "评估", "检查", "优化", "改进",
            "Excel", "报表", "预算", "数据", "文件",
            "技能", "安装", "开发", "测试",
            "工作", "任务", "项目", "流程"
        ]
        
        for keyword in skill_related_keywords:
            if keyword in task_description:
                return True
        
        # 技能标签检查
        if self.required_skill_tag in task_description:
            return True
        
        # 任务长度检查
        if len(task_description) > 30:
            return True
        
        return False
    
    def get_skill_usage_stats(self):
        """获取技能使用统计"""
        total = self.skill_usage_history["total_checks"]
        used = self.skill_usage_history["skill_used"]
        not_used = self.skill_usage_history["skill_not_used"]
        
        if total == 0:
            return "暂无技能使用统计"
        
        usage_rate = (used / total) * 100
        return f"技能使用统计：{used}/{total} ({usage_rate:.1f}%)"
    
    def generate_checklist(self, task_description, actual_actions=None):
        """生成检查清单"""
        is_memory_related = self.check_intent(task_description)
        violations = self.check_forbidden_actions(task_description)
        correct_action = self.get_correct_action(task_description)
        
        # 检查技能使用
        skill_ok, skill_message = self.check_skill_usage(task_description, actual_actions)
        
        checklist = {
            "任务描述": task_description,
            "检查时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "是否记忆相关": "是" if is_memory_related else "否",
            "发现禁止操作": violations if violations else "无",
            "正确操作方法": correct_action if is_memory_related else "无需记忆操作",
            "技能使用检查": "通过" if skill_ok else f"失败：{skill_message}",
            "技能使用统计": self.get_skill_usage_stats(),
            "主人指令": [
                "所有记忆都通过记忆系统 @skill://workbuddy-add-memory 来处理",
                "所有后续工作都要通过workbuddy-add-memory技能进行记忆和管理",
                "看到@skill://workbuddy-add-memory就立即使用技能"
            ],
            "绝对禁止": [
                "创建md文件",
                "忘记使用workbuddy-add-memory技能"
            ],
            "必须使用": [
                "update_memory工具",
                "use_skill('workbuddy-add-memory')",
                "python start_work.py '任务描述'"
            ]
        }
        
        return checklist
    
    def enforce_memory_system(self, task_description, actual_actions=None):
        """强制执行记忆系统规则"""
        print("\n" + "="*70)
        print("🧠 记忆系统强制执行检查 (v2.0)")
        print("="*70)
        
        checklist = self.generate_checklist(task_description, actual_actions)
        
        # 打印检查结果
        for key, value in checklist.items():
            if isinstance(value, list):
                print(f"{key}:")
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"{key}: {value}")
        
        print("-"*70)
        
        # 检查是否有违规
        all_passed = True
        error_messages = []
        
        if checklist["是否记忆相关"] == "是":
            if checklist["发现禁止操作"] != "无":
                all_passed = False
                error_messages.append("🚨 **记忆操作违规**：发现禁止操作")
                for violation in checklist["发现禁止操作"]:
                    error_messages.append(f"   ❌ {violation}")
        
        if checklist["技能使用检查"].startswith("失败"):
            all_passed = False
            error_messages.append("🚨 **技能使用违规**：未正确使用workbuddy-add-memory技能")
            error_messages.append(f"   ❌ {checklist['技能使用检查']}")
        
        # 输出结果
        if not all_passed:
            print("\n".join(error_messages))
            print(f"\n✅ **正确做法**：")
            for item in checklist["必须使用"]:
                print(f"   - {item}")
            print(f"\n📋 **主人指令**：")
            for item in checklist["主人指令"]:
                print(f"   - {item}")
            return False
        else:
            if checklist["是否记忆相关"] == "是":
                print(f"✅ **检查通过**：{checklist['正确操作方法']}")
            print(f"✅ **技能使用**：{checklist['技能使用检查']}")
            return True
    
    def create_reminder(self):
        """创建每日提醒"""
        reminder = {
            "title": "记忆系统与技能使用每日提醒",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "技能使用统计": self.get_skill_usage_stats(),
            "reminders": [
                "🚫 绝不创建md文件",
                "🚫 绝不忘记使用workbuddy-add-memory技能",
                "✅ 所有记忆都通过update_memory工具处理",
                "✅ 看到@skill://workbuddy-add-memory就立即使用技能",
                "📋 严格执行主人指令：'所有记忆都通过记忆系统 @skill://workbuddy-add-memory 来处理'",
                "📋 严格执行主人指令：'所有后续工作都要通过workbuddy-add-memory技能进行记忆和管理'",
                "🧠 每次任务前检查：1.是否应使用技能 2.是否调用use_skill 3.是否运行start_work.py",
                "💪 让做什么就做什么，不添加不减少"
            ]
        }
        
        reminder_file = f"/Users/josieyang/.workbuddy/memory_reminder_{datetime.now().strftime('%Y%m%d')}.json"
        with open(reminder_file, 'w', encoding='utf-8') as f:
            json.dump(reminder, f, ensure_ascii=False, indent=2)
        
        return reminder_file

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python memory_system_enforcer.py \"任务描述\"")
        sys.exit(1)
    
    task_description = sys.argv[1]
    enforcer = MemorySystemEnforcer()
    
    # 执行检查
    result = enforcer.enforce_memory_system(task_description)
    
    # 创建每日提醒
    reminder_file = enforcer.create_reminder()
    print(f"\n📅 每日提醒已创建：{reminder_file}")
    
    # 返回结果
    if not result:
        print("\n🔴 **检查不通过**：发现违规操作，必须纠正！")
        sys.exit(1)
    else:
        print("\n🟢 **检查通过**：可以继续执行任务")
        sys.exit(0)

if __name__ == "__main__":
    main()