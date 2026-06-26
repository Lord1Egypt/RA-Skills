"""
core/prompt_compiler.py
PromptCompiler - 将人格定义编译为 prompt 片段
"""

from typing import Dict, Any, Optional


class PromptCompiler:
    """Prompt 编译器 - 将人格定义转换为各平台可用的 prompt 文本"""
    
    def compile_overlay(self, persona_def: Dict[str, Any]) -> str:
        """
        编译叠加模式（Stack）人格片段
        保留 V1.0 的 INSERT_TO_SOUL.md 格式
        """
        meta = persona_def["meta"]
        identity = persona_def.get("identity", {})
        behavior = persona_def.get("behavior", {})
        phrases = persona_def.get("phrases", {})
        
        lines = []
        lines.append("## 【心灵补手】谄媚模块 v3.0")
        lines.append(f"**人格**: {meta.get('name', meta['id'])}")
        lines.append("")
        lines.append("### 身份")
        
        # 身份声明
        identity_stmts = identity.get("identity_statements", {})
        if "greeting" in identity_stmts:
            lines.append(identity_stmts["greeting"])
        
        # 人称
        pronouns = identity.get("pronouns", {})
        lines.append(f"第一人称：{pronouns.get('first_person', '奴才')}")
        lines.append(f"第二人称：{pronouns.get('second_person', '主子')}")
        
        lines.append("")
        lines.append("### 当前配置")
        lines.append(f"- 程度：{behavior.get('level', 5)}/10")
        lines.append(f"- 语气：{behavior.get('tone', '正常')}")
        lines.append(f"- 模式：{behavior.get('mode', 'normal')}")
        
        lines.append("")
        lines.append("### 触发时机")
        trigger_keywords = behavior.get("activation", {}).get("trigger_keywords", [])
        if trigger_keywords:
            lines.append(f"检测到以下关键词时触发：{', '.join(trigger_keywords)}")
        else:
            lines.append("检测到情绪时机时自动触发")
        
        lines.append("")
        lines.append("### 话术规则")
        
        # 程度对应话术示例
        level = behavior.get("level", 5)
        if level <= 3:
            lines.append("程度1-3：委婉暗示，简短1句")
        elif level <= 6:
            lines.append("程度4-6：正常赞美，1-2句话")
        elif level <= 9:
            lines.append("程度7-9：强烈吹捧，2-3句话")
        else:
            lines.append("程度10：无脑崇拜，3+句话 [Debug Mode]")
        
        # 种子话术
        seeds = phrases.get("seeds", {})
        if seeds:
            lines.append("")
            lines.append("### 话术种子（智能扩展）")
            for scenario, tiers in seeds.items():
                lines.append(f"**{scenario}**:")
                for tier, phrases_list in tiers.items():
                    for p in phrases_list[:2]:
                        lines.append(f"- {p}")
        
        return "\n".join(lines)
    
    def compile_inherit(
        self,
        base_prompt: str,
        persona_def: Dict[str, Any]
    ) -> str:
        """
        编译继承模式（Inherit）人格片段
        在 base prompt 基础上追加人格覆盖
        """
        overlay = self.compile_overlay(persona_def)
        
        return f"""{base_prompt}

{'='*60}
【人格覆盖层 - 继承自 base prompt】
{'='*60}
{overlay}
"""
    
    def compile_independent(self, persona_def: Dict[str, Any]) -> str:
        """
        编译独立模式（Independent）人格片段
        完整的人格定义，不依赖 base
        """
        meta = persona_def["meta"]
        identity = persona_def.get("identity", {})
        behavior = persona_def.get("behavior", {})
        phrases = persona_def.get("phrases", {})
        
        lines = []
        lines.append(f"# {meta.get('name', meta['id'])} 人格")
        lines.append("")
        lines.append(f"**版本**: {meta.get('version', '1.0.0')}")
        lines.append(f"**角色**: {identity.get('role', 'AI助手')}")
        lines.append("")
        
        # 身份声明
        identity_stmts = identity.get("identity_statements", {})
        for key, value in identity_stmts.items():
            lines.append(f"**{key}**: {value}")
        
        lines.append("")
        lines.append("## 行为规则")
        lines.append(f"**语气**: {behavior.get('tone', '专业')}")
        lines.append(f"**程度**: {behavior.get('level', 5)}/10")
        
        # 话术种子
        seeds = phrases.get("seeds", {})
        if seeds:
            lines.append("")
            lines.append("## 话术库")
            for scenario, tiers in seeds.items():
                lines.append(f"### {scenario}")
                for tier, phrases_list in tiers.items():
                    lines.append(f"**{tier}**:")
                    for p in phrases_list[:3]:
                        lines.append(f"- {p}")
        
        return "\n".join(lines)
