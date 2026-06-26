#!/usr/bin/env python3
"""
小红书热点半自动化发布页面生成器
根据用户提供的主题生成小红书风格的内容发布页面

版本: 1.1.0
作者: 蒲公英 (Dandelion)
创建时间: 2026年3月16日
最后更新: 2026年3月17日
"""

import json
import os
import sys
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import argparse

class XiaohongshuHotPublishGenerator:
    """小红书热点发布页面生成器"""
    
    def __init__(self, theme: str, brand_name: str = "蒲公英AI编程"):
        """
        初始化生成器
        
        Args:
            theme: 内容主题
            brand_name: 品牌名称
        """
        self.theme = theme.strip()
        self.brand_name = brand_name.strip()
        self.current_date = datetime.now()
        self.contents = []
        
        # 验证参数
        if not self.theme:
            raise ValueError("主题不能为空")
        if not self.brand_name:
            raise ValueError("品牌名称不能为空")
    
    def generate_contents(self, num_contents: int = 3) -> List[Dict[str, Any]]:
        """
        基于主题生成小红书内容
        
        Args:
            num_contents: 生成的内容数量 (1-5)
            
        Returns:
            内容列表
            
        Raises:
            ValueError: 如果内容数量不在有效范围内
        """
        if num_contents < 1 or num_contents > 5:
            raise ValueError("内容数量必须在1-5之间")
        
        # 根据主题生成不同的内容类型
        content_types = self._get_content_types()
        
        # 确保有足够的内容类型
        if len(content_types) < num_contents:
            # 重复内容类型或使用通用类型
            while len(content_types) < num_contents:
                content_types.append(random.choice(content_types[:3]))
        
        for i in range(num_contents):
            content_type = content_types[i % len(content_types)]
            content = self._generate_single_content(i + 1, content_type)
            self.contents.append(content)
            
        return self.contents
    
    def _get_content_types(self) -> List[str]:
        """根据主题获取内容类型"""
        theme_lower = self.theme.lower()
        
        # 技术类主题
        if any(keyword in theme_lower for keyword in ['python', '编程', '代码', '开发', '前端', '后端', '算法']):
            return ['基础教程', '项目实战', '工具推荐', '学习路径', '常见问题', '面试准备']
        
        # AI/机器学习主题
        elif any(keyword in theme_lower for keyword in ['ai', '人工智能', '机器学习', '深度学习', '神经网络']):
            return ['入门指南', '工具对比', '实战案例', '未来趋势', '学习资源', '模型解析']
        
        # 效率工具主题
        elif any(keyword in theme_lower for keyword in ['效率', '工具', '工作流', '自动化', '时间管理']):
            return ['工具推荐', '工作流优化', '时间管理', '效率技巧', '案例分享', '避坑指南']
        
        # 学习教育主题
        elif any(keyword in theme_lower for keyword in ['学习', '教育', '教程', '课程', '读书', '阅读']):
            return ['学习计划', '资源推荐', '方法技巧', '避坑指南', '成功案例', '经验分享']
        
        # 生活健康主题
        elif any(keyword in theme_lower for keyword in ['健身', '健康', '饮食', '运动', '养生', '睡眠']):
            return ['健身计划', '饮食建议', '运动技巧', '健康知识', '经验分享', '工具推荐']
        
        # 旅行摄影主题
        elif any(keyword in theme_lower for keyword in ['旅行', '旅游', '摄影', '拍照', '景点', '攻略']):
            return ['旅行攻略', '摄影技巧', '景点推荐', '装备建议', '经验分享', '避坑指南']
        
        # 美食烹饪主题
        elif any(keyword in theme_lower for keyword in ['美食', '烹饪', '食谱', '烘焙', '食材', '餐厅']):
            return ['食谱分享', '烹饪技巧', '食材推荐', '美食探店', '健康饮食', '工具推荐']
        
        # 通用主题
        else:
            return ['实用技巧', '经验分享', '工具推荐', '案例分析', '趋势解读', '资源整理']
    
    def _generate_single_content(self, index: int, content_type: str) -> Dict[str, Any]:
        """生成单个内容"""
        # 生成标题
        title = self._generate_title(index, content_type)
        
        # 生成内容
        content_text = self._generate_content_text(index, content_type)
        
        # 生成标签
        tags = self._generate_tags(content_type)
        
        # 生成时间建议
        time_suggestion = self._generate_time_suggestion(index, content_type)
        
        # 生成emoji
        emoji = self._get_content_emoji(content_type)
        
        return {
            'id': index,
            'title': title,
            'content': content_text,
            'tags': tags,
            'time_suggestion': time_suggestion,
            'emoji': emoji,
            'content_type': content_type,
            'published': False,
            'created_at': self.current_date.isoformat(),
            'word_count': len(content_text)
        }
    
    def _generate_title(self, index: int, content_type: str) -> str:
        """生成标题"""
        emoji = self._get_content_emoji(content_type)
        
        # 标题模板库
        title_templates = [
            f"{emoji}{content_type}｜{self.theme}的完整指南",
            f"{emoji}{self.theme}｜{content_type}全解析",
            f"{emoji}{content_type}｜掌握{self.theme}的关键技巧",
            f"{emoji}{self.theme}{content_type}｜从入门到精通",
            f"{emoji}{content_type}｜{self.theme}高效学习法",
            f"{emoji}爆款{content_type}｜{self.theme}这样学最有效",
            f"{emoji}{self.theme}{content_type}｜小白也能轻松上手",
            f"{emoji}{content_type}秘籍｜{self.theme}快速入门",
            f"{emoji}{self.theme}｜{content_type}避坑指南",
            f"{emoji}{content_type}实战｜{self.theme}应用案例"
        ]
        
        # 根据索引选择不同的模板
        template_index = (index - 1) % len(title_templates)
        return title_templates[template_index]
    
    def _generate_content_text(self, index: int, content_type: str) -> str:
        """生成内容文本"""
        # 小红书风格的开头
        openings = [
            "姐妹们！今天分享一个超实用的技巧！",
            "宝子们！我发现了一个超好用的方法！",
            "家人们！这个技巧你一定要知道！",
            "姐妹们！今天来聊聊这个话题！",
            "宝子们！这个经验分享给你们！",
            "🌟 独家分享：",
            "💫 今日干货：",
            "🎉 重磅推荐：",
            "🔥 热点话题：",
            "📚 知识分享："
        ]
        
        opening = random.choice(openings)
        
        # 根据内容类型生成不同的内容结构
        content_generators = {
            '基础教程': self._generate_tutorial_content,
            '项目实战': self._generate_project_content,
            '工具推荐': self._generate_tools_content,
            '学习路径': self._generate_learning_path_content,
            '常见问题': self._generate_faq_content,
            '入门指南': self._generate_guide_content,
            '工具对比': self._generate_comparison_content,
            '实战案例': self._generate_case_study_content,
            '未来趋势': self._generate_trend_content,
            '学习资源': self._generate_resources_content,
            '工作流优化': self._generate_workflow_content,
            '时间管理': self._generate_time_management_content,
            '效率技巧': self._generate_efficiency_content,
            '案例分享': self._generate_case_share_content,
            '学习计划': self._generate_study_plan_content,
            '资源推荐': self._generate_resource_recommendation_content,
            '方法技巧': self._generate_method_content,
            '避坑指南': self._generate_pitfall_content,
            '成功案例': self._generate_success_case_content,
            '实用技巧': self._generate_practical_tips_content,
            '经验分享': self._generate_experience_content,
            '案例分析': self._generate_analysis_content,
            '趋势解读': self._generate_trend_analysis_content
        }
        
        # 获取对应的内容生成器
        generator = content_generators.get(content_type, self._generate_general_content)
        return generator(opening)
    
    def _generate_tutorial_content(self, opening: str) -> str:
        """生成教程类内容"""
        return f"""{opening}

📅 今日重点：{self.theme}基础入门

💡 为什么学习{self.theme}？
- 市场需求大，薪资待遇高
- 应用场景广泛，实用性强
- 学习曲线平缓，适合初学者

🚀 学习{self.theme}的完整步骤：

1️⃣ **环境搭建**
   - 安装必要的工具和软件
   - 配置开发环境
   - 测试安装是否成功

2️⃣ **基础语法**
   - 掌握核心语法规则
   - 理解数据类型和结构
   - 练习基础代码编写

3️⃣ **实战练习**
   - 完成小项目练习
   - 解决实际问题
   - 积累项目经验

4️⃣ **进阶学习**
   - 学习高级特性
   - 掌握框架和库
   - 了解最佳实践

5️⃣ **项目实战**
   - 参与真实项目
   - 团队协作开发
   - 作品集建设

🎯 我的学习建议：
- 每天坚持学习1-2小时
- 理论与实践相结合
- 多参与社区交流
- 定期复习和总结

💼 实际效果：
学习{self.theme}后：
- 工作效率提升50%+
- 解决问题的能力增强
- 职业发展空间扩大
- 收入水平显著提高

👇 你在学习{self.theme}时遇到什么问题？评论区一起讨论！

#{self.theme} #基础教程 #学习教程 #技术分享 #小红书热点"""
    
    def _generate_tools_content(self, opening: str) -> str:
        """生成工具推荐类内容"""
        return f"""{opening}

📅 今日重点：{self.theme}必备工具推荐

💡 为什么需要专业工具？
- 提高工作效率，节省时间
- 减少错误，提升质量
- 学习曲线更平缓

🚀 5个{self.theme}必备工具：

1️⃣ **开发工具**
   - 功能：代码编辑、调试、版本控制
   - 优点：功能全面，社区活跃
   - 适合：所有级别的开发者

2️⃣ **学习工具**
   - 功能：教程、练习、互动学习
   - 优点：学习路径清晰，反馈及时
   - 适合：初学者和中级学习者

3️⃣ **效率工具**
   - 功能：自动化、模板、快捷操作
   - 优点：大幅提升工作效率
   - 适合：追求效率的开发者

4️⃣ **协作工具**
   - 功能：团队协作、代码审查、项目管理
   - 优点：促进团队合作，提高质量
   - 适合：团队开发项目

5️⃣ **资源工具**
   - 功能：资源搜索、文档查询、社区支持
   - 优点：快速解决问题，获取帮助
   - 适合：遇到问题的开发者

🎯 我的工具使用心得：
- 根据需求选择合适的工具
- 不要盲目追求新工具
- 熟练掌握核心工具
- 定期评估工具效果

💼 实际效果：
使用专业工具后：
- 开发效率提升60%+
- 代码质量显著提高
- 学习速度加快
- 团队协作更顺畅

👇 你用过哪些好用的{self.theme}工具？评论区分享！

#{self.theme} #工具推荐 #效率提升 #技术工具 #小红书热点"""
    
    def _generate_project_content(self, opening: str) -> str:
        """生成项目实战类内容"""
        return f"""{opening}

📅 今日重点：{self.theme}实战项目

💡 为什么需要项目实战？
- 理论知识需要实践验证
- 项目经验是求职关键
- 实际问题锻炼能力

🚀 {self.theme}实战项目推荐：

1️⃣ **入门项目**
   - 难度：⭐
   - 时间：1-2天
   - 目标：掌握基础应用
   - 收获：建立信心，理解流程

2️⃣ **中级项目**
   - 难度：⭐⭐⭐
   - 时间：1-2周
   - 目标：解决实际问题
   - 收获：提升技能，积累经验

3️⃣ **高级项目**
   - 难度：⭐⭐⭐⭐⭐
   - 时间：1个月+
   - 目标：完整系统开发
   - 收获：全面能力，作品集亮点

🎯 项目实战步骤：

📋 **第1步：需求分析**
   - 明确项目目标
   - 分析用户需求
   - 制定功能清单

📋 **第2步：技术选型**
   - 选择合适的技术栈
   - 评估工具和框架
   - 设计系统架构

📋 **第3步：开发实现**
   - 分模块开发
   - 定期测试验证
   - 代码质量保证

📋 **第4步：测试部署**
   - 全面测试功能
   - 性能优化
   - 部署上线

📋 **第5步：总结反思**
   - 项目复盘
   - 经验总结
   - 持续改进

💼 我的项目经验：
- 从简单项目开始，逐步提升
- 注重代码质量和文档
- 积极参与开源项目
- 定期分享项目经验

👇 你想做什么样的{self.theme}项目？评论区聊聊！

#{self.theme} #项目实战 #编程学习 #实战经验 #小红书热点"""
    
    def _generate_general_content(self, opening: str) -> str:
        """生成通用内容"""
        return f"""{opening}

📅 今日重点：{self.theme}

💡 核心要点：
- 理解{self.theme}的基本概念
- 掌握关键技巧和方法
- 应用于实际场景

🚀 实施步骤：

1️⃣ **准备阶段**
   - 明确学习目标
   - 收集相关资源
   - 制定详细计划

2️⃣ **学习阶段**
   - 系统学习理论知识
   - 动手实践验证
   - 记录学习心得

3️⃣ **应用阶段**
   - 应用于实际项目
   - 解决具体问题
   - 优化改进方案

4️⃣ **总结阶段**
   - 复盘学习过程
   - 总结经验教训
   - 规划下一步学习

🎯 我的建议：
- 保持学习的持续性
- 理论与实践结合
- 多与他人交流分享
- 定期回顾和调整

💼 学习效果：
掌握{self.theme}后：
- 技能水平显著提升
- 解决问题的能力增强
- 职业竞争力提高
- 个人成长加速

👇 你对{self.theme}有什么疑问？评论区交流！

#{self.theme} #学习分享 #经验交流 #知识分享 #小红书热点"""
    
    # 其他内容生成方法（简略实现）
    def _generate_learning_path_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "学习路径")
    
    def _generate_faq_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "常见问题解答")
    
    def _generate_guide_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "入门指南")
    
    def _generate_comparison_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "工具对比")
    
    def _generate_case_study_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "实战案例")
    
    def _generate_trend_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "未来趋势")
    
    def _generate_resources_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "学习资源")
    
    def _generate_workflow_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "工作流优化")
    
    def _generate_time_management_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "时间管理")
    
    def _generate_efficiency_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "效率技巧")
    
    def _generate_case_share_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "案例分享")
    
    def _generate_study_plan_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "学习计划")
    
    def _generate_resource_recommendation_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "资源推荐")
    
    def _generate_method_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "方法技巧")
    
    def _generate_pitfall_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "避坑指南")
    
    def _generate_success_case_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "成功案例")
    
    def _generate_practical_tips_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "实用技巧")
    
    def _generate_experience_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "经验分享")
    
    def _generate_analysis_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "案例分析")
    
    def _generate_trend_analysis_content(self, opening: str) -> str:
        return self._generate_general_content(opening).replace("今日重点", "趋势解读")
    
    def _generate_tags(self, content_type: str) -> List[str]:
        """生成标签"""
        # 基础标签
        base_tags = [self.theme, content_type, '技术分享', '学习教程']
        
        # 热门标签库
        hot_tags = [
            '小红书热点', '干货分享', '经验总结', '实用技巧',
            '知识分享', '学习打卡', '成长记录', '效率提升',
            '工具推荐', '项目实战', '避坑指南', '资源整理'
        ]
        
        # 根据内容类型添加特定标签
        type_specific_tags = {
            '基础教程': ['新手入门', '学习指南', '教程分享'],
            '项目实战': ['实战经验', '项目分享', '作品展示'],
            '工具推荐': ['效率工具', '软件推荐', '神器分享'],
            '学习路径': ['学习规划', '路径指南', '成长路线'],
            '常见问题': ['问题解答', 'FAQ', '疑难解答']
        }
        
        # 合并所有标签
        all_tags = base_tags + hot_tags + type_specific_tags.get(content_type, [])
        
        # 去重并随机选择6-8个标签
        unique_tags = list(set(all_tags))
        num_tags = random.randint(6, min(8, len(unique_tags)))
        selected_tags = random.sample(unique_tags, num_tags)
        
        return selected_tags
    
    def _generate_time_suggestion(self, index: int, content_type: str) -> Dict[str, Any]:
        """生成时间建议"""
        # 根据内容和索引生成不同的时间
        base_times = ['10:30', '13:30', '16:30', '19:30', '21:30']
        
        # 确保索引在范围内
        time_index = (index - 1) % len(base_times)
        publish_time = base_times[time_index]
        
        # 判断时间状态
        current_hour = self.current_date.hour
        current_minute = self.current_date.minute
        
        # 解析发布时间
        publish_hour = int(publish_time.split(':')[0])
        publish_minute = int(publish_time.split(':')[1])
        
        time_status = "future"
        if index == 1:
            time_status = "now"
        elif current_hour > publish_hour or (current_hour == publish_hour and current_minute > publish_minute):
            time_status = "past"
            
        return {
            'time': publish_time,
            'status': time_status,
            'display': f"{'立即发布' if time_status == 'now' else '计划发布'} ({publish_time})"
        }
    
    def _get_content_emoji(self, content_type: str) -> str:
        """获取内容对应的emoji"""
        emoji_map = {
            '基础教程': '📚',
            '项目实战': '🚀',
            '工具推荐': '🛠️',
            '学习路径': '🗺️',
            '常见问题': '❓',
            '入门指南': '🎯',
            '工具对比': '⚖️',
            '实战案例': '💼',
            '未来趋势': '🔮',
            '学习资源': '📖',
            '工作流优化': '⚡',
            '时间管理': '⏰',
            '效率技巧': '✨',
            '案例分享': '📊',
            '学习计划': '📅',
            '资源推荐': '🌟',
            '方法技巧': '🎨',
            '避坑指南': '⚠️',
            '成功案例': '🏆',
            '实用技巧': '💡',
            '经验分享': '🤝',
            '案例分析': '🔍',
            '趋势解读': '📈'
        }
        
        return emoji_map.get(content_type, '📝')
    
    def generate_html_page(self, output_path: str = None) -> str:
        """
        生成HTML页面
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            HTML内容
            
        Raises:
            ValueError: 如果没有生成内容
        """
        if not self.contents:
            raise ValueError("请先生成内容，调用generate_contents()方法")
        
        # 读取HTML模板
        html_template = self._get_html_template()
        
        # 替换模板变量
        html_content = html_template.replace('{{BRAND_NAME}}', self.brand_name)
        html_content = html_content.replace('{{THEME}}', self.theme)
        html_content = html_content.replace('{{CURRENT_DATE}}', self._format_date())
        
        # 生成内容选择器
        content_selector = self._generate_content_selector()
        html_content = html_content.replace('{{CONTENT_SELECTOR}}', content_selector)
        
        # 生成内容区域
        content_sections = self._generate_content_sections()
        html_content = html_content.replace('{{CONTENT_SECTIONS}}', content_sections)
        
        # 生成JavaScript数据
        js_data = self._generate_js_data()
        html_content = html_content.replace('{{JS_DATA}}', js_data)
        
        # 保存文件
        if output_path:
            # 确保目录存在
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ 页面已生成: {output_path}")
            
            # 同时保存JSON数据
            json_path = output_path.replace('.html', '.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'theme': self.theme,
                    'brand_name': self.brand_name,
                    'generated_date': self.current_date.isoformat(),
                    'contents': self.contents,
                    'metadata': {
                        'version': '1.1.0',
                        'generator': 'XiaohongshuHotPublishGenerator',
                        'content_count': len(self.contents)
                    }
                }, f, ensure_ascii=False, indent=2)
            print(f"📊 数据已保存: {json_path}")
        
        return html_content
    
    def _format_date(self) -> str:
        """格式化日期"""
        # 中文日期格式
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        weekday = weekdays[self.current_date.weekday()]
        
        return f"{self.current_date.year}年{self.current_date.month}月{self.current_date.day}日 {weekday} {self.current_date.hour:02d}:{self.current_date.minute:02d}"
    
    def _generate_content_selector(self) -> str:
        """生成内容选择器"""
        selector_html = '<div class="content-selector">\n'
        
        for i, content in enumerate(self.contents, 1):
            active_class = 'active' if i == 1 else ''
            selector_html += f'    <div class="content-tab {active_class}" onclick="selectContent({i})">\n'
            selector_html += f'        {content["emoji"]} {content["content_type"]}\n'
            selector_html += '    </div>\n'
            
        selector_html += '</div>'
        return selector_html
    
    def _generate_content_sections(self) -> str:
        """生成内容区域"""
        sections_html = ''
        
        for i, content in enumerate(self.contents, 1):
            active_class = 'active' if i == 1 else ''
            
            # 时间徽章类
            time_badge_class = content['time_suggestion']['status']
            
            sections_html += f'''
            <!-- 内容{i}：{content["content_type"]} -->
            <div class="section {active_class}" id="content-section-{i}">
                <div class="section-header">
                    <div class="section-title">
                        <span class="emoji">{content["emoji"]}</span>
                        <span id="title{i}">{content["title"]}</span>
                    </div>
                    <div class="time-badge {time_badge_class}">{content["time_suggestion"]["display"]}</div>
                </div>
                
                <div class="content-box">
                    <button class="btn-copy" onclick="copyContent({i})">
                        <span>📋</span> 一键复制
                    </button>
                    
                    <div class="content-text" id="content{i}">
{self._escape_html(content["content"])}</div>
                    
                    <div class="tags">
            '''
            
            # 添加标签
            for tag in content['tags']:
                hot_class = 'hot-tag' if '热点' in tag or '热门' in tag else ''
                sections_html += f'<span class="tag {hot_class}">#{tag}</span>\n'
            
            sections_html += f'''
                    </div>
                    
                    <div class="buttons">
                        <button class="btn btn-primary" onclick="copyContent({i})">
                            <span>📋</span> 复制内容
                        </button>
                        <button class="btn btn-secondary" onclick="openXiaohongshu()">
                            <span>🌐</span> 打开小红书
                        </button>
                        <button class="btn btn-success" onclick="markAsPublished({i})">
                            <span>✅</span> 标记为已发布
                        </button>
                    </div>
                </div>
            </div>
            '''
        
        return sections_html
    
    def _escape_html(self, text: str) -> str:
        """转义HTML特殊字符"""
        html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;"
        }
        
        for char, escape in html_escape_table.items():
            text = text.replace(char, escape)
        
        return text
    
    def _generate_js_data(self) -> str:
        """生成JavaScript数据"""
        # 创建简化的数据副本，避免循环引用
        simplified_contents = []
        for content in self.contents:
            simplified_contents.append({
                'id': content['id'],
                'title': content['title'],
                'content_type': content['content_type'],
                'emoji': content['emoji'],
                'time_suggestion': content['time_suggestion']
            })
        
        data = {
            'theme': self.theme,
            'brand_name': self.brand_name,
            'contents': simplified_contents,
            'generated_at': self.current_date.isoformat()
        }
        return json.dumps(data, ensure_ascii=False)
    
    def _get_html_template(self) -> str:
        """获取HTML模板"""
        template_path = os.path.join(os.path.dirname(__file__), 'template.html')
        
        if os.path.exists(template_path):
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"⚠️ 读取模板文件失败: {e}")
                return self._get_basic_template()
        else:
            print(f"⚠️ 模板文件不存在: {template_path}")
            return self._get_basic_template()
    
    def _get_basic_template(self) -> str:
        """获取基本HTML模板"""
        # 这里返回一个简化的模板，实际使用时应该从文件读取
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>小红书热点一键发布 - {{BRAND_NAME}}</title>
    <style>
        /* 基本样式将在template.html中定义 */
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥小红书热点一键发布🌼</h1>
            <div class="subtitle">{{BRAND_NAME}} - 热点结合半自动化发布系统</div>
            <div class="date" id="current-date">{{CURRENT_DATE}}</div>
        </div>
        
        <div class="content">
            {{CONTENT_SELECTOR}}
            {{CONTENT_SECTIONS}}
        </div>
    </div>
    
    <script>
        // JavaScript代码将在template.html中定义
    </script>
</body>
</html>'''


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='小红书热点发布页面生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s "Python学习" --brand "蒲公英AI编程"
  %(prog)s "AI工具推荐" --num 4 --output "ai_tools.html"
  %(prog)s "健身计划" --brand "健身达人" --num 5 --verbose
        '''
    )
    
    parser.add_argument('theme', help='内容主题')
    parser.add_argument('--brand', default='蒲公英AI编程', help='品牌名称 (默认: 蒲公英AI编程)')
    parser.add_argument('--output', help='输出文件路径 (默认自动生成)')
    parser.add_argument('--num', type=int, default=3, choices=range(1, 6), 
                       help='生成内容数量 (1-5, 默认: 3)')
    parser.add_argument('--verbose', action='store_true', help='显示详细信息')
    
    args = parser.parse_args()
    
    try:
        # 生成页面
        if args.verbose:
            print(f"🎯 开始生成小红书发布页面")
            print(f"   主题: {args.theme}")
            print(f"   品牌: {args.brand}")
            print(f"   内容数量: {args.num}")
        
        generator = XiaohongshuHotPublishGenerator(args.theme, args.brand)
        contents = generator.generate_contents(args.num)
        
        # 设置输出路径
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_theme = args.theme.replace(' ', '_').replace('/', '_')[:20]
            output_path = f'xiaohongshu_{safe_theme}_{timestamp}.html'
        
        # 生成HTML页面
        html_content = generator.generate_html_page(output_path)
        
        if args.verbose:
            print(f"\n📊 生成的内容摘要:")
            print("-" * 50)
            for i, content in enumerate(contents, 1):
                print(f"\n{i}. {content['title']}")
                print(f"   类型: {content['content_type']}")
                print(f"   时间: {content['time_suggestion']['display']}")
                print(f"   标签: {', '.join(['#' + tag for tag in content['tags'][:3]])}...")
                print(f"   字数: {content['word_count']}")
            
            print(f"\n✅ 生成完成!")
            print(f"   主文件: {output_path}")
            print(f"   数据文件: {output_path.replace('.html', '.json')}")
            print(f"\n💡 使用提示:")
            print(f"   1. 在浏览器中打开 {output_path}")
            print(f"   2. 点击内容标签切换不同内容")
            print(f"   3. 使用『📋 一键复制』按钮复制内容")
            print(f"   4. 发布后点击『✅ 标记为已发布』")
        
        return html_content
        
    except ValueError as e:
        print(f"❌ 参数错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 生成过程中出现错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()