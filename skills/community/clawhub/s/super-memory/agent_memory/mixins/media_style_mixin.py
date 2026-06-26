from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class MediaStyleMixin:
    def process_media_for_style(self, file_path: str) -> dict:
        """
        处理媒体文件并提取风格特征。
        
        参数:
            file_path: 媒体文件路径
        
        返回: 风格分析结果
        """
        if not self.media_processor or not self.style_analyzer:
            return {"success": False, "reason": "所需组件不可用"}
        
        # 处理媒体文件
        result = self.media_processor.process_for_style(file_path)
        if not result.get("success"):
            return result
        
        # 分析风格
        content = result.get("content", "")
        if not content:
            return {"success": False, "reason": "未提取到内容"}
        
        style = self.style_analyzer.analyze(content)
        result["style"] = style
        return result

    def create_role_from_media(self, file_path: str, role_name: str) -> dict:
        """
        从媒体文件创建角色模板。
        
        参数:
            file_path: 媒体文件路径
            role_name: 角色名称
        
        返回: 创建结果
        """
        # 处理媒体文件并提取风格
        process_result = self.process_media_for_style(file_path)
        if not process_result.get("success"):
            return {"created": False, "reason": process_result.get("reason", "process failed")}
        
        # 创建角色模板
        style = process_result.get("style", {})
        from ..style_analyzer import create_role_from_style
        role_data = create_role_from_style(style, role_name)
        
        # 生成角色 ID
        import hashlib
        role_id = f"media_{hashlib.md5((role_name + str(process_result.get('media_type', ''))).encode()).hexdigest()[:8]}"
        
        # 保存角色
        return self.create_role(
            role_id=role_id,
            name=role_name,
            prompt_template=role_data["prompt_template"],
            personality_traits=role_data["personality_traits"],
            speaking_style=role_data["speaking_style"],
            topic_preferences=role_data["topic_preferences"],
            emotional_tone=role_data["emotional_tone"]
        )