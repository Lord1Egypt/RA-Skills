from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class RoleMixin:
    def list_roles(self) -> dict:
        """
        列出所有可用的角色模板。
        
        返回: {role_id: {name, source, version, speaking_style, topic_preferences}}
        """
        if not self.role_manager:
            return {}
        return self.role_manager.list_roles()

    def get_role(self, role_id: str) -> dict:
        """
        获取特定角色模板。
        
        参数:
            role_id: 角色 ID
        
        返回: 角色模板数据，或 None
        """
        if not self.role_manager:
            return None
        role = self.role_manager.get_role(role_id)
        if role:
            return {
                "name": role.name,
                "prompt_template": role.prompt_template,
                "personality_traits": role.personality_traits,
                "speaking_style": role.speaking_style,
                "topic_preferences": role.topic_preferences,
                "emotional_tone": role.emotional_tone,
                "source": role.source,
                "version": role.version
            }
        return None

    def apply_role(self, role_id: str, weight: float = 0.4) -> dict:
        """
        应用角色风格到个人人格。
        
        参数:
            role_id: 角色 ID
            weight: 角色风格权重（0-1）
        
        返回: 混合后的人格画像
        """
        if not self.role_manager or not self.digital_twin:
            return {}
        role = self.role_manager.get_role(role_id)
        if not role:
            return {}
        return self.digital_twin.apply_role_style(role, weight)

    def create_role(self, role_id: str, name: str, prompt_template: str, 
                   personality_traits: dict, speaking_style: str = "",
                   topic_preferences: list = None, emotional_tone: str = "") -> dict:
        """
        创建新角色模板。
        
        参数:
            role_id: 角色 ID
            name: 角色名称
            prompt_template: 提示词模板
            personality_traits: 人格特质
            speaking_style: 说话风格
            topic_preferences: 主题偏好
            emotional_tone: 情感基调
        
        返回: 创建结果
        """
        if not self.role_manager:
            return {"created": False, "reason": "role_manager not available"}
        from ..role_template import RoleTemplate
        role = RoleTemplate(
            name=name,
            prompt_template=prompt_template,
            personality_traits=personality_traits,
            speaking_style=speaking_style,
            topic_preferences=topic_preferences,
            emotional_tone=emotional_tone,
            source="custom"
        )
        self.role_manager.create_role(role_id, role)
        return {"created": True, "role_id": role_id}

    def delete_role(self, role_id: str) -> dict:
        """
        删除角色模板。
        
        参数:
            role_id: 角色 ID
        
        返回: 删除结果
        """
        if not self.role_manager:
            return {"deleted": False, "reason": "role_manager not available"}
        self.role_manager.delete_role(role_id)
        return {"deleted": True, "role_id": role_id}