"""
Sum2Slides - 总结成PPT
将对话、任务、讨论总结成演示文稿
"""

import os
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from .core.base_generator import PPTStructure, SlideContent, PPTSoftware, PPTTemplate, GeneratorFactory
from .core.content_planner import ContentPlanner
from .platforms.base_platform import PlatformConfig, PlatformType, PlatformFactory
from .config.settings import get_config_manager
from .utils.logger import setup_logger


logger = setup_logger("sum2slides")


class ConversationAnalyzer:
    """对话分析器"""
    
    def __init__(self):
        self.patterns = {
            "decision": r"(决定|决定要|确定|确认|选择|采用|使用|采用|实施|执行)",
            "conclusion": r"(结论|总结|总的来说|综上所述|因此|所以|最终)",
            "action_item": r"(需要|要|应该|必须|务必|记得|提醒|安排|计划|准备)",
            "key_point": r"(重点|关键|核心|要点|主要|重要|特别|尤其)",
            "number_list": r"(\d+[\.、]|\d+\)|•|·|-)",
            "question": r"(问题|疑问|困惑|不清楚|不明白|请教|请问)",
            "solution": r"(解决|方案|方法|办法|对策|措施|建议|提议)"
        }
    
    def analyze_conversation(self, conversation_text: str) -> Dict[str, Any]:
        """
        分析对话内容
        
        Args:
            conversation_text: 对话文本
            
        Returns:
            分析结果
        """
        logger.info(f"🔍 分析对话内容，长度: {len(conversation_text)}字符")
        
        # 基础分析
        lines = conversation_text.split('\n')
        messages = [line.strip() for line in lines if line.strip()]
        
        # 提取关键信息
        analysis_result = {
            "total_messages": len(messages),
            "total_length": len(conversation_text),
            "key_decisions": self._extract_pattern(conversation_text, "decision"),
            "conclusions": self._extract_pattern(conversation_text, "conclusion"),
            "action_items": self._extract_pattern(conversation_text, "action_item"),
            "key_points": self._extract_pattern(conversation_text, "key_point"),
            "questions": self._extract_pattern(conversation_text, "question"),
            "solutions": self._extract_pattern(conversation_text, "solution"),
            "numbered_items": self._extract_numbered_items(conversation_text),
            "topics": self._extract_topics(conversation_text)
        }
        
        logger.info(f"✅ 对话分析完成")
        logger.info(f"   关键决策: {len(analysis_result['key_decisions'])}个")
        logger.info(f"   行动项: {len(analysis_result['action_items'])}个")
        logger.info(f"   关键要点: {len(analysis_result['key_points'])}个")
        
        return analysis_result
    
    def _extract_pattern(self, text: str, pattern_name: str) -> List[str]:
        """
        提取特定模式的内容
        
        Args:
            text: 文本
            pattern_name: 模式名称
            
        Returns:
            匹配的内容列表
        """
        pattern = self.patterns.get(pattern_name, "")
        if not pattern:
            return []
        
        matches = []
        lines = text.split('\n')
        
        for line in lines:
            if re.search(pattern, line):
                # 提取包含关键词的句子
                sentences = re.split(r'[。！？；]', line)
                for sentence in sentences:
                    if re.search(pattern, sentence):
                        clean_sentence = sentence.strip()
                        if clean_sentence and len(clean_sentence) > 5:
                            matches.append(clean_sentence)
        
        return list(set(matches))[:10]  # 去重并限制数量
    
    def _extract_numbered_items(self, text: str) -> List[str]:
        """
        提取编号列表项
        
        Args:
            text: 文本
            
        Returns:
            编号项列表
        """
        items = []
        lines = text.split('\n')
        
        for line in lines:
            # 匹配数字开头的行
            match = re.match(r'(\d+)[\.、\)]\s*(.+)', line.strip())
            if match:
                items.append(match.group(2).strip())
            
            # 匹配项目符号
            elif re.match(r'[•·\-]\s*(.+)', line.strip()):
                items.append(re.sub(r'^[•·\-]\s*', '', line.strip()))
        
        return items
    
    def _extract_topics(self, text: str) -> List[str]:
        """
        提取主题
        
        Args:
            text: 文本
            
        Returns:
            主题列表
        """
        # 简单的主题提取：基于高频词
        words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        
        if not words:
            return []
        
        # 统计词频
        from collections import Counter
        word_counts = Counter(words)
        
        # 返回高频词（排除常见词）
        common_words = {'这个', '那个', '我们', '你们', '他们', '可以', '需要', '应该', '就是', '还是'}
        topics = [word for word, count in word_counts.most_common(10) 
                 if word not in common_words and count > 1]
        
        return topics[:5]


class Sum2Slides:
    """Sum2Slides 主类"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化Sum2Slides
        
        Args:
            config_file: 配置文件路径
        """
        self.config_manager = get_config_manager(config_file)
        self.conversation_analyzer = ConversationAnalyzer()
        self.content_planner = ContentPlanner()
        self.logger = logger
        
        # 默认设置
        self.default_software = "powerpoint"
        self.default_platform = "feishu"
        self.default_template = "business"
    
    def summarize_to_ppt(self, conversation_text: str, 
                        title: Optional[str] = None,
                        software: Optional[str] = None,
                        platform: Optional[str] = None,
                        template: Optional[str] = None) -> Dict[str, Any]:
        """
        将对话总结成PPT
        
        Args:
            conversation_text: 对话文本
            title: PPT标题
            software: PPT软件类型
            platform: 目标平台
            template: 模板类型
            
        Returns:
            结果字典
        """
        self.logger.info("🚀 开始Sum2Slides工作流")
        
        # 使用默认值或参数值
        software = software or self.default_software
        platform = platform or self.default_platform
        template = template or self.default_template
        
        try:
            # 1. 分析对话
            self.logger.info("🔍 步骤1: 分析对话内容")
            analysis = self.conversation_analyzer.analyze_conversation(conversation_text)
            
            # 2. 生成PPT标题
            ppt_title = title or self._generate_title(conversation_text, analysis)
            
            # 3. 创建PPT结构
            self.logger.info("📝 步骤2: 创建PPT结构")
            structure = self._create_structure_from_analysis(ppt_title, analysis, template)
            
            # 4. 生成PPT
            self.logger.info("🎨 步骤3: 生成PPT文件")
            ppt_file = self._generate_ppt(structure, software)
            
            # 5. 上传到平台（如果指定了平台）
            upload_result = None
            if platform:
                self.logger.info(f"📤 步骤4: 上传到{platform}")
                upload_result = self._upload_to_platform(ppt_file, platform)
            
            # 6. 返回结果
            result = {
                "success": True,
                "conversation_analysis": {
                    "title": ppt_title,
                    "total_messages": analysis["total_messages"],
                    "key_decisions": analysis["key_decisions"],
                    "action_items": analysis["action_items"],
                    "key_points": analysis["key_points"]
                },
                "ppt_info": {
                    "file_path": ppt_file,
                    "slide_count": len(structure.slides),
                    "software": software,
                    "template": template
                }
            }
            
            if upload_result and upload_result.get("success"):
                result["upload_info"] = upload_result
                result["file_url"] = upload_result.get("file_url")
            
            self.logger.info("🎉 Sum2Slides工作流完成")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Sum2Slides失败: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            
            return {
                "success": False,
                "error": str(e),
                "conversation_preview": conversation_text[:100] + "..."
            }
    
    def _generate_title(self, conversation_text: str, analysis: Dict[str, Any]) -> str:
        """
        生成PPT标题
        
        Args:
            conversation_text: 对话文本
            analysis: 分析结果
            
        Returns:
            PPT标题
        """
        # 尝试从对话中提取标题
        first_line = conversation_text.split('\n')[0].strip()
        if len(first_line) < 50 and not first_line.startswith(('http', '#')):
            return first_line[:30]
        
        # 使用主题作为标题
        if analysis.get("topics"):
            topic = analysis["topics"][0] if analysis["topics"] else "对话"
            return f"{topic}总结"
        
        # 默认标题
        message_count = analysis.get("total_messages", 0)
        if message_count > 0:
            return f"对话总结 ({message_count}条消息)"
        
        return "对话总结"
    
    def _create_structure_from_analysis(self, title: str, analysis: Dict[str, Any], 
                                       template: str) -> PPTStructure:
        """
        从分析结果创建PPT结构
        
        Args:
            title: PPT标题
            analysis: 分析结果
            template: 模板类型
            
        Returns:
            PPT结构
        """
        # 确定模板
        template_type = self._determine_template(analysis, template)
        
        # 创建幻灯片列表
        slides = []
        
        # 1. 封面页
        slides.append(SlideContent(
            title=title,
            content=[f"基于{analysis['total_messages']}条对话内容总结"],
            type="content"
        ))
        
        # 2. 对话概览
        if analysis["total_messages"] > 0:
            slides.append(SlideContent(
                title="对话概览",
                content=[
                    f"总消息数: {analysis['total_messages']}",
                    f"关键决策: {len(analysis['key_decisions'])}个",
                    f"行动项: {len(analysis['action_items'])}个",
                    f"关键要点: {len(analysis['key_points'])}个"
                ],
                type="content"
            ))
        
        # 3. 关键决策
        if analysis["key_decisions"]:
            slides.append(SlideContent(
                title="关键决策",
                content=analysis["key_decisions"][:5],  # 限制前5个
                type="content"
            ))
        
        # 4. 行动项
        if analysis["action_items"]:
            slides.append(SlideContent(
                title="行动项",
                content=analysis["action_items"][:5],  # 限制前5个
                type="content"
            ))
        
        # 5. 关键要点
        if analysis["key_points"]:
            slides.append(SlideContent(
                title="关键要点",
                content=analysis["key_points"][:5],  # 限制前5个
                type="content"
            ))
        
        # 6. 编号项（如果有）
        if analysis["numbered_items"]:
            slides.append(SlideContent(
                title="详细列表",
                content=analysis["numbered_items"][:8],  # 限制前8个
                type="content"
            ))
        
        # 7. 总结页
        slides.append(SlideContent(
            title="总结",
            key_points=[
                "对话内容已成功总结",
                f"共提取{len(analysis['key_decisions']) + len(analysis['action_items'])}个关键点",
                "使用Sum2Slides自动生成"
            ],
            conclusion="总结完成，可分享给相关人员",
            type="summary"
        ))
        
        # 创建结构
        return PPTStructure(
            title=title,
            subtitle="对话总结",
            author="Sum2Slides",
            date=datetime.now().strftime("%Y年%m月%d日"),
            slides=slides,
            template=template_type
        )
    
    def _determine_template(self, analysis: Dict[str, Any], default_template: str) -> PPTTemplate:
        """
        确定PPT模板
        
        Args:
            analysis: 分析结果
            default_template: 默认模板
            
        Returns:
            PPT模板
        """
        from .core.base_generator import PPTTemplate
        
        # 根据内容类型选择模板
        template_map = {
            "business": PPTTemplate.BUSINESS,
            "technical": PPTTemplate.TECHNICAL,
            "education": PPTTemplate.EDUCATION,
            "creative": PPTTemplate.CREATIVE,
            "minimalist": PPTTemplate.MINIMALIST
        }
        
        # 检查关键词确定模板
        text = str(analysis).lower()
        
        if any(word in text for word in ["技术", "开发", "代码", "系统"]):
            return PPTTemplate.TECHNICAL
        elif any(word in text for word in ["教育", "学习", "培训", "课程"]):
            return PPTTemplate.EDUCATION
        elif any(word in text for word in ["设计", "创意", "艺术", "创新"]):
            return PPTTemplate.CREATIVE
        else:
            return template_map.get(default_template, PPTTemplate.BUSINESS)
    
    def _generate_ppt(self, structure: PPTStructure, software: str) -> str:
        """
        生成PPT文件
        
        Args:
            structure: PPT结构
            software: 软件类型
            
        Returns:
            PPT文件路径
        """
        from .core.base_generator import PPTSoftware
        
        # 创建生成器
        software_type = PPTSoftware(software)
        generator = GeneratorFactory.create_generator(software_type)
        
        # 生成PPT
        ppt_file = generator.generate_from_structure(structure)
        
        # 保存到桌面
        output_dir = os.path.expanduser("~/Desktop/Sum2Slides")
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in structure.title if c.isalnum() or c in (' ', '-', '_')).strip()
        if not safe_title:
            safe_title = "对话总结"
        
        file_name = f"Sum2Slides_{safe_title}_{timestamp}.pptx"
        output_path = os.path.join(output_dir, file_name)
        
        # 保存文件
        saved_file = generator.save_ppt(output_path)
        
        self.logger.info(f"✅ PPT生成成功: {saved_file}")
        return saved_file
    
    def _upload_to_platform(self, ppt_file: str, platform: str) -> Dict[str, Any]:
        """
        上传PPT到平台
        
        Args:
            ppt_file: PPT文件路径
            platform: 平台名称
            
        Returns:
            上传结果
        """
        try:
            from .platforms.base_platform import PlatformType, PlatformConfig, PlatformFactory
            
            # 获取平台配置
            platform_config_dict = self.config_manager.get_platform_config(platform)
            
            if not platform_config_dict:
                self.logger.warning(f"⚠️ 平台{platform}未配置，跳过上传")
                return {"success": False, "error": f"平台{platform}未配置"}
            
            # 创建平台配置
            platform_type = PlatformType(platform)
            platform_config = PlatformConfig(
                platform_type=platform_type,
                **platform_config_dict
            )
            
            # 创建平台实例
            platform_instance = PlatformFactory.create_platform(platform_type, platform_config)
            
            # 上传文件
            upload_result = platform_instance.upload_and_share(ppt_file)
            
            if upload_result.get("success"):
                self.logger.info(f"✅ 上传成功: {upload_result.get('file_url')}")
            else:
                self.logger.warning(f"⚠️ 上传失败: {upload_result.get('error')}")
            
            return upload_result
            
        except Exception as e:
            self.logger.error(f"❌ 上传到平台失败: {e}")
            return {"success": False, "error": str(e)}


# 快捷函数
def sum2slides(conversation_text: str, 
              title: Optional[str] = None,
              software: str = "powerpoint",
              platform: Optional[str] = None,
              template: str = "business") -> Dict[str, Any]:
    """
    快捷函数：将对话总结成PPT
    
    Args:
        conversation_text: 对话文本
        title: PPT标题
        software: PPT软件类型
        platform: 目标平台
        template: 模板类型
        
    Returns:
        结果字典
    """
    processor = Sum2Slides()
    return processor.summarize_to_ppt(
        conversation_text=conversation_text,
        title=title,
        software=software,
        platform=platform,
        template=template
    )


# 测试函数
def test_sum2slides():
    """测试Sum2Slides"""
    print("🎯 测试Sum2Slides")
    print("=" * 50)
    
    # 测试对话文本
    test_conversation = """
会议讨论：OpenClaw PPT制作Skill开发

1. 我们需要开发一个PPT制作Skill
2. 这个Skill应该支持多种PPT软件
   - Microsoft PowerPoint
   - WPS Office
   - Google Slides（未来支持）
3. 需要支持多种通信平台
   • 飞书（优先支持）
   • 微信/QQ
   • 钉钉
   • Slack
4. 关键决策：
   a) 采用模块化架构设计
   b) 使用python-pptx作为基础生成器
   c) 为WPS开发AppleScript自动化
5. 行动项：
   - 完成核心模块开发
   - 测试飞书上传功能
   - 创建用户文档
6. 总结：
   这个Skill将大大提高PPT制作效率，特别适合将对话总结成演示文稿。
   我们决定将其命名为"Sum2Slides"（总结成PPT）。
    """
    
    print("🔍 测试对话:")
    print(test_conversation[:200] + "...")
    
    try:
        # 使用Sum2Slides
        result = sum2slides(
            conversation_text=test_conversation,
            title="PPT制作Skill开发会议总结",
            software="powerpoint",
            platform=None,  # 先不测试上传
            template="business"
        )
        
        if result.get("success"):
            print("\n✅ Sum2Slides测试成功!")
            print(f"   PPT标题: {result['conversation_analysis']['title']}")
            print(f"   消息数: {result['conversation_analysis']['total_messages']}")
            print(f"   关键决策: {len(result['conversation_analysis']['key_decisions'])}个")
            print(f"   行动项: {len(result['conversation_analysis']['action_items'])}个")
            print(f"   幻灯片数: {result['ppt_info']['slide_count']}")
            print(f"   PPT文件: {result['ppt_info']['file_path']}")
            
            # 检查文件是否生成
            if os.path.exists(result['ppt_info']['file_path']):
                file_size = os.path.getsize(result['ppt_info']['file_path'])
                print(f"   文件大小: {file_size}字节")
                return True
            else:
                print("❌ PPT文件未生成")
                return False
        else:
            print(f"❌ Sum2Slides失败: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Sum2Slides - 总结成PPT")
    print("=" * 60)
    
    success = test_sum2slides()
    
    if success:
        print("\n🎉 Sum2Slides测试完成！")
        print("现在你可以使用sum2slides()函数将对话总结成PPT了！")
    else:
        print("\n⚠️ Sum2Slides测试失败，请检查错误信息")