"""
内容规划器
支持AI分析和智能内容规划
"""

from .base_generator import PPTStructure, SlideContent, PPTTemplate
from typing import List, Dict, Any, Optional
import re
from datetime import datetime


class ContentPlanner:
    """内容规划器"""
    
    def __init__(self, enable_ai: bool = False):
        """
        初始化内容规划器
        
        Args:
            enable_ai: 是否启用AI分析
        """
        self.enable_ai = enable_ai
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Any]:
        """
        加载内容模板
        
        Returns:
            模板字典
        """
        return {
            "business_report": {
                "name": "商务报告",
                "template": PPTTemplate.BUSINESS,
                "slides": [
                    {"type": "cover", "title": "商务报告"},
                    {"type": "content", "title": "执行摘要"},
                    {"type": "content", "title": "市场分析"},
                    {"type": "two_column", "title": "SWOT分析"},
                    {"type": "content", "title": "财务表现"},
                    {"type": "comparison", "title": "竞争分析"},
                    {"type": "summary", "title": "结论与建议"}
                ]
            },
            "technical_presentation": {
                "name": "技术演示",
                "template": PPTTemplate.TECHNICAL,
                "slides": [
                    {"type": "cover", "title": "技术演示"},
                    {"type": "content", "title": "技术背景"},
                    {"type": "content", "title": "技术架构"},
                    {"type": "two_column", "title": "功能对比"},
                    {"type": "content", "title": "实施计划"},
                    {"type": "summary", "title": "技术总结"}
                ]
            },
            "education_lecture": {
                "name": "教育讲座",
                "template": PPTTemplate.EDUCATION,
                "slides": [
                    {"type": "cover", "title": "教育讲座"},
                    {"type": "content", "title": "课程目标"},
                    {"type": "content", "title": "主要内容"},
                    {"type": "two_column", "title": "知识点解析"},
                    {"type": "content", "title": "案例分析"},
                    {"type": "summary", "title": "学习要点"}
                ]
            },
            "creative_pitch": {
                "name": "创意提案",
                "template": PPTTemplate.CREATIVE,
                "slides": [
                    {"type": "cover", "title": "创意提案"},
                    {"type": "content", "title": "创意概念"},
                    {"type": "content", "title": "市场机会"},
                    {"type": "two_column", "title": "方案对比"},
                    {"type": "content", "title": "实施路线图"},
                    {"type": "summary", "title": "核心价值"}
                ]
            }
        }
    
    def plan_from_input(self, user_input: str) -> PPTStructure:
        """
        根据用户输入规划PPT结构
        
        Args:
            user_input: 用户需求描述
            
        Returns:
            PPT结构
        """
        print(f"📋 分析用户需求: {user_input}")
        
        # 1. 提取关键信息
        title = self._extract_title(user_input)
        template_type = self._detect_template(user_input)
        slide_count = self._estimate_slide_count(user_input)
        
        # 2. 确定模板
        template_info = self._select_template(template_type)
        
        # 3. 生成幻灯片内容
        slides = self._generate_slides(user_input, template_info, slide_count)
        
        # 4. 创建结构
        structure = PPTStructure(
            title=title,
            subtitle=self._generate_subtitle(user_input),
            author="OpenClaw PPT Maker",
            date=datetime.now().strftime("%Y年%m月%d日"),
            slides=slides,
            template=template_info["template"]
        )
        
        print(f"✅ PPT结构规划完成:")
        print(f"   标题: {title}")
        print(f"   模板: {template_info['name']}")
        print(f"   幻灯片数: {len(slides)}")
        
        return structure
    
    def _extract_title(self, user_input: str) -> str:
        """
        从用户输入提取标题
        
        Args:
            user_input: 用户输入
            
        Returns:
            提取的标题
        """
        # 尝试从输入中提取标题
        patterns = [
            r'关于(.+?)的PPT',
            r'制作(.+?)的演示文稿',
            r'主题是(.+?)的PPT',
            r'(.+?)的汇报',
            r'(.+?)的报告'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input)
            if match:
                return match.group(1).strip()
        
        # 如果没有匹配，使用默认标题
        if len(user_input) > 20:
            return user_input[:20] + "..."
        else:
            return user_input or "演示文稿"
    
    def _detect_template(self, user_input: str) -> str:
        """
        检测模板类型
        
        Args:
            user_input: 用户输入
            
        Returns:
            模板类型
        """
        input_lower = user_input.lower()
        
        # 关键词检测
        business_keywords = ['报告', '汇报', '商务', '商业', '财务', '市场', '销售']
        technical_keywords = ['技术', '开发', '代码', '系统', '架构', '算法', '数据']
        education_keywords = ['教育', '教学', '课程', '学习', '培训', '讲座', '知识']
        creative_keywords = ['创意', '设计', '艺术', '创新', '提案', '策划', '营销']
        
        for keyword in business_keywords:
            if keyword in input_lower:
                return "business_report"
        
        for keyword in technical_keywords:
            if keyword in input_lower:
                return "technical_presentation"
        
        for keyword in education_keywords:
            if keyword in input_lower:
                return "education_lecture"
        
        for keyword in creative_keywords:
            if keyword in input_lower:
                return "creative_pitch"
        
        # 默认使用商务报告
        return "business_report"
    
    def _select_template(self, template_type: str) -> Dict[str, Any]:
        """
        选择模板
        
        Args:
            template_type: 模板类型
            
        Returns:
            模板信息
        """
        return self.templates.get(template_type, self.templates["business_report"])
    
    def _estimate_slide_count(self, user_input: str) -> int:
        """
        估计幻灯片数量
        
        Args:
            user_input: 用户输入
            
        Returns:
            估计的幻灯片数量
        """
        # 根据输入长度和复杂度估计
        length = len(user_input)
        
        if length < 50:
            return 3  # 简短内容
        elif length < 200:
            return 5  # 中等内容
        elif length < 500:
            return 7  # 详细内容
        else:
            return 10  # 非常详细
    
    def _generate_slides(self, user_input: str, template_info: Dict[str, Any], 
                        slide_count: int) -> List[SlideContent]:
        """
        生成幻灯片内容
        
        Args:
            user_input: 用户输入
            template_info: 模板信息
            slide_count: 幻灯片数量
            
        Returns:
            幻灯片内容列表
        """
        slides = []
        
        # 使用模板的幻灯片结构
        template_slides = template_info.get("slides", [])
        
        # 调整幻灯片数量
        if len(template_slides) > slide_count:
            template_slides = template_slides[:slide_count]
        elif len(template_slides) < slide_count:
            # 添加额外的内容页
            for i in range(len(template_slides), slide_count):
                template_slides.append({
                    "type": "content",
                    "title": f"内容页 {i+1}"
                })
        
        # 生成幻灯片内容
        for i, slide_info in enumerate(template_slides):
            slide_type = slide_info.get("type", "content")
            slide_title = slide_info.get("title", f"幻灯片 {i+1}")
            
            # 生成内容
            content = self._generate_slide_content(user_input, slide_type, slide_title, i)
            
            # 创建幻灯片对象
            slide = SlideContent(
                title=slide_title,
                type=slide_type,
                content=content.get("main", []),
                left_content=content.get("left", []),
                right_content=content.get("right", []),
                key_points=content.get("key_points", []),
                conclusion=content.get("conclusion", "")
            )
            
            slides.append(slide)
        
        return slides
    
    def _generate_slide_content(self, user_input: str, slide_type: str, 
                               slide_title: str, slide_index: int) -> Dict[str, Any]:
        """
        生成幻灯片内容
        
        Args:
            user_input: 用户输入
            slide_type: 幻灯片类型
            slide_title: 幻灯片标题
            slide_index: 幻灯片索引
            
        Returns:
            内容字典
        """
        if self.enable_ai and self._can_use_ai():
            return self._generate_with_ai(user_input, slide_type, slide_title, slide_index)
        else:
            return self._generate_with_rules(user_input, slide_type, slide_title, slide_index)
    
    def _generate_with_rules(self, user_input: str, slide_type: str, 
                            slide_title: str, slide_index: int) -> Dict[str, Any]:
        """
        使用规则生成内容
        
        Args:
            user_input: 用户输入
            slide_type: 幻灯片类型
            slide_title: 幻灯片标题
            slide_index: 幻灯片索引
            
        Returns:
            内容字典
        """
        # 根据幻灯片类型生成不同内容
        if slide_type == "cover":
            return {
                "main": [f"基于用户需求: {user_input[:50]}..."],
                "conclusion": "自动化生成的演示文稿"
            }
        
        elif slide_type == "content":
            points = [
                f"这是第{slide_index+1}页内容",
                f"主题: {slide_title}",
                f"基于用户需求: {user_input[:30]}...",
                "这里可以添加详细内容",
                "使用OpenClaw PPT Maker生成"
            ]
            return {"main": points}
        
        elif slide_type == "two_column":
            left_points = ["左侧要点1", "左侧要点2", "左侧要点3"]
            right_points = ["右侧要点1", "右侧要点2", "右侧要点3"]
            return {"left": left_points, "right": right_points}
        
        elif slide_type == "comparison":
            left_points = ["方案A的优势", "方案A的特点", "方案A的适用场景"]
            right_points = ["方案B的优势", "方案B的特点", "方案B的适用场景"]
            return {"left": left_points, "right": right_points}
        
        elif slide_type == "summary":
            key_points = [
                "核心观点总结",
                "主要发现",
                "关键建议",
                "下一步行动"
            ]
            conclusion = "感谢观看！使用OpenClaw PPT Maker轻松创建专业演示文稿。"
            return {"key_points": key_points, "conclusion": conclusion}
        
        else:
            return {"main": [f"默认内容: {slide_title}"]}
    
    def _generate_with_ai(self, user_input: str, slide_type: str, 
                         slide_title: str, slide_index: int) -> Dict[str, Any]:
        """
        使用AI生成内容（需要配置API）
        
        Args:
            user_input: 用户输入
            slide_type: 幻灯片类型
            slide_title: 幻灯片标题
            slide_index: 幻灯片索引
            
        Returns:
            内容字典
        """
        # TODO: 集成AI服务（如OpenAI API）
        # 这里暂时使用规则生成
        return self._generate_with_rules(user_input, slide_type, slide_title, slide_index)
    
    def _can_use_ai(self) -> bool:
        """
        检查是否可以使用AI
        
        Returns:
            是否可以使用AI
        """
        # TODO: 检查API配置和可用性
        return False
    
    def _generate_subtitle(self, user_input: str) -> str:
        """
        生成副标题
        
        Args:
            user_input: 用户输入
            
        Returns:
            副标题
        """
        # 根据用户输入生成副标题
        if "报告" in user_input or "汇报" in user_input:
            return "专业报告"
        elif "演示" in user_input or "展示" in user_input:
            return "演示文稿"
        elif "教学" in user_input or "培训" in user_input:
            return "教学材料"
        else:
            return "自动化生成"