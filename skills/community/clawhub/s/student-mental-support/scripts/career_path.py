#!/usr/bin/env python3
"""
职业路径可视化工具
为大学生生成可视化职业发展路径
"""

def generate_career_path(major, interests, skills, timeframe="5年"):
    """
    生成职业发展路径
    
    Parameters:
    major: str, 专业
    interests: list, 兴趣列表
    skills: list, 技能列表
    timeframe: str, 时间框架
    """
    
    # 职业领域匹配
    career_fields = match_career_fields(major, interests, skills)
    
    # 生成路径
    path = {
        "major": major,
        "timeframe": timeframe,
        "career_fields": career_fields,
        "path_stages": generate_path_stages(career_fields, timeframe),
        "recommended_path": get_recommended_path(career_fields)
    }
    
    return path

def match_career_fields(major, interests, skills):
    """
    匹配职业领域
    
    Parameters:
    major: str, 专业
    interests: list, 兴趣列表
    skills: list, 技能列表
    """
    
    # 专业领域匹配
    field_mapping = {
        "计算机科学": ["软件开发", "数据分析", "人工智能", "网络安全"],
        "软件工程": ["软件开发", "项目管理", "系统架构", "测试工程"],
        "电子信息": ["硬件开发", "嵌入式系统", "通信工程", "电路设计"],
        "机械工程": ["机械设计", "自动化控制", "制造工程", "设备维护"],
        "电气工程": ["电力系统", "电气设计", "自动化控制", "能源管理"],
        "土木工程": ["建筑设计", "施工管理", "结构分析", "项目管理"],
        "工商管理": ["市场营销", "人力资源管理", "项目管理", "运营管理"],
        "会计": ["财务会计", "审计", "税务", "财务分析"],
        "经济学": ["经济分析", "金融分析", "市场研究", "投资分析"],
        "法学": ["法律实务", "合规管理", "法律研究", "咨询服务"],
        "教育学": ["教学", "教育管理", "课程设计", "教育研究"],
        "心理学": ["心理咨询", "人力资源管理", "用户体验", "研究分析"],
        "生物科学": ["生物技术", "医药研发", "环境科学", "食品科学"]
    }
    
    # 获取基本领域
    fields = field_mapping.get(major, ["相关领域", "专业相关", "技能匹配"])
    
    # 根据兴趣调整
    for interest in interests:
        interest_fields = {
            "技术研究": ["研发工程师", "技术专家", "研究人员"],
            "项目管理": ["项目经理", "产品经理", "项目协调"],
            "创意设计": ["设计师", "创意策划", "用户体验"],
            "沟通交流": ["销售", "市场", "公关", "客户服务"],
            "数据分析": ["数据分析师", "商业分析师", "研究分析"],
            "团队协作": ["团队管理", "团队协作", "团队支持"]
        }
        
        if interest in interest_fields:
            fields.extend(interest_fields[interest])
    
    # 根据技能调整
    for skill in skills:
        skill_fields = {
            "编程": ["软件开发", "网站开发", "应用开发"],
            "数据分析": ["数据分析师", "商业分析师", "统计分析"],
            "设计": ["设计师", "创意设计", "用户体验设计"],
            "沟通": ["市场营销", "公关", "客户服务"],
            "管理": ["项目管理", "团队管理", "运营管理"],
            "创新": ["创新管理", "产品开发", "研究开发"]
        }
        
        if skill in skill_fields:
            fields.extend(skill_fields[skill])
    
    # 去重和排序
    fields = list(set(fields))
    fields.sort()
    
    return fields

def generate_path_stages(career_fields, timeframe):
    """
    生成各阶段路径
    
    Parameters:
    career_fields: list, 职业领域列表
    timeframe: str, 时间框架
    """
    
    stages = {}
    
    if timeframe == "1年":
        stages["短期"] = [
            "完成毕业设计或论文",
            "准备求职材料和面试",
            "参加校园招聘和宣讲会",
            "开始实习或兼职工作"
        ]
        
    elif timeframe == "3年":
        stages["短期"] = [
            "完成学业和毕业",
            "找到初始工作岗位",
            "适应职场环境和要求",
            "建立初步职业基础"
        ]
        
        stages["中期"] = [
            "深化专业技能",
            "积累工作经验",
            "建立职业网络",
            "明确发展方向"
        ]
        
    else:  # 5年
        stages["短期"] = [
            "毕业和求职",
            "入职和适应",
            "专业技能入门",
            "职业基础建立"
        ]
        
        stages["中期"] = [
            "专业能力提升",
            "岗位职责拓展",
            "管理能力培养",
            "职业网络扩大"
        ]
        
        stages["长期"] = [
            "专业领域深入",
            "职业发展规划",
            "个人成长提升",
            "社会影响力建立"
        ]
    
    return stages

def get_recommended_path(career_fields):
    """
    获取推荐路径
    
    Parameters:
    career_fields: list, 职业领域列表
    """
    
    # 根据领域推荐路径
    recommendations = []
    
    for field in career_fields:
        if field in ["软件开发", "网站开发", "应用开发"]:
            recommendations.append({
                "field": "软件开发",
                "path": "初级开发 → 高级开发 → 技术专家 → 架构师",
                "steps": ["学习核心技术", "参与项目开发", "掌握系统设计", "培养架构能力"]
            })
            
        elif field in ["数据分析", "商业分析师", "研究分析"]:
            recommendations.append({
                "field": "数据分析",
                "path": "数据助理 → 数据分析师 → 分析专家 → 数据科学家",
                "steps": ["掌握数据分析工具", "学习统计方法", "理解业务逻辑", "培养数据科学能力"]
            })
            
        elif field in ["项目管理", "产品经理", "项目协调"]:
            recommendations.append({
                "field": "项目管理",
                "path": "项目助理 → 项目经理 → 项目总监 → 高层管理",
                "steps": ["学习项目管理方法", "培养沟通能力", "掌握资源调配", "提升战略思维"]
            })
            
        elif field in ["市场营销", "公关", "客户服务"]:
            recommendations.append({
                "field": "市场营销",
                "path": "市场助理 → 营销专员 → 营销经理 → 市场总监",
                "steps": ["学习市场知识", "培养沟通能力", "掌握市场分析", "提升策划能力"]
            })
            
        else:
            recommendations.append({
                "field": field,
                "path": "初级职位 → 中级职位 → 高级职位 → 专家职位",
                "steps": ["基础学习", "经验积累", "能力提升", "专业深化"]
            })
    
    return recommendations

def print_path(path):
    """
    打印职业路径
    
    Parameters:
    path: dict, 职业路径
    """
    print(f"专业：{path['major']}")
    print(f"时间框架：{path['timeframe']}")
    print()
    
    print("可能的职业领域：")
    for field in path['career_fields']:
        print(f"  - {field}")
    print()
    
    print("发展阶段：")
    for stage_name, stage_activities in path['path_stages'].items():
        print(f"{stage_name}（{path['timeframe']}）：")
        for activity in stage_activities:
            print(f"  - {activity}")
        print()
    
    print("推荐发展路径：")
    for recommendation in path['recommended_path']:
        print(f"{recommendation['field']}：")
        print(f"  发展路径：{recommendation['path']}")
        print(f"  关键步骤：")
        for step in recommendation['steps']:
            print(f"    - {step}")
        print()

def generate_template():
    """
    生成职业路径模板
    """
    template = {
        "基本信息": {
            "专业": "",
            "年级": "",
            "毕业时间": "",
            "求职阶段": ""
        },
        
        "自我评估": {
            "兴趣领域": [],
            "核心技能": [],
            "价值观": [],
            "期望薪资": "",
            "期望工作地点": "",
            "期望工作性质": ""
        },
        
        "职业探索": {
            "已了解行业": [],
            "感兴趣行业": [],
            "待了解行业": [],
            "优先考虑因素": []
        },
        
        "发展规划": {
            "短期目标": [],
            "中期目标": [],
            "长期目标": [],
            "风险控制": []
        },
        
        "行动计划": {
            "本周行动": [],
            "本月行动": [],
            "本学期行动": [],
            "毕业前行动": []
        },
        
        "支持资源": {
            "校内资源": [],
            "校外资源": [],
            "亲友支持": [],
            "专业指导": []
        }
    }
    
    return template

def print_template(template):
    """
    打印职业路径模板
    
    Parameters:
    template: dict, 职业路径模板
    """
    print("职业路径规划模板")
    print("=================")
    print()
    
    for section, content in template.items():
        print(f"{section}：")
        if isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, list):
                    print(f"  {key}:")
                    for item in value:
                        print(f"    - {item}")
                else:
                    print(f"  {key}: {value}")
        elif isinstance(content, list):
            for item in content:
                print(f"  - {item}")
        else:
            print(f"  {content}")
        print()

if __name__ == "__main__":
    # 示例用户信息
    major = "计算机科学"
    interests = ["技术研究", "数据分析", "项目管理"]
    skills = ["编程", "数据分析", "沟通"]
    
    # 生成职业路径
    path = generate_career_path(major, interests, skills, "5年")
    
    # 打印路径
    print_path(path)
    
    # 显示模板
    template = generate_template()
    print_template(template)