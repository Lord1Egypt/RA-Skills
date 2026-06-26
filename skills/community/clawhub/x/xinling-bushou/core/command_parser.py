"""
命令解析器
解析用户命令词，提取配置变更请求
"""
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class CommandType(Enum):
    """命令类型"""
    ENABLE = "enable"
    DISABLE = "disable"
    SET_LEVEL = "set_level"
    ADJUST_LEVEL = "adjust_level"
    SET_PERSONA = "set_persona"
    SET_MODE = "set_mode"
    STATUS = "status"
    UNKNOWN = "unknown"


@dataclass
class ParsedCommand:
    """解析后的命令"""
    command_type: CommandType
    raw_command: str
    args: Dict[str, Any]
    requires_confirmation: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "command_type": self.command_type.value,
            "raw_command": self.raw_command,
            "args": self.args,
            "requires_confirmation": self.requires_confirmation
        }


class CommandParser:
    """命令解析器"""
    
    # 命令模式定义
    COMMAND_PATTERNS = {
        # 启用/关闭
        CommandType.ENABLE: [
            r"进入心灵补手",
            r"开启心灵补手", 
            r"启动心灵补手",
            r"打开心灵补手",
            r"心灵补手开启",
        ],
        CommandType.DISABLE: [
            r"关闭心灵补手",
            r"退出心灵补手",
            r"停止心灵补手",
            r"禁用心灵补手",
            r"心灵补手关闭",
        ],
        
        # 程度设置
        CommandType.SET_LEVEL: [
            r"补手程度(\d+)",
            r"补手级别(\d+)",
            r"程度[:：]?(\d+)",
            r"级别[:：]?(\d+)",
            r"level[:：]?(\d+)",
        ],
        CommandType.ADJUST_LEVEL: [
            r"补手全开",
            r"补手拉满",
            r"补手最大",
            r"程度调高",
            r"程度增加",
            r"厉害一点",
            r"夸多一点",
            r"补手收敛",
            r"补手低调",
            r"程度调低", 
            r"程度减小",
            r"温柔一点",
            r"夸少一点",
        ],
        
        # 风格设置
        CommandType.SET_PERSONA: [
            r"补手风格大太监",
            r"风格大太监",
            r"大太监模式",
            r"补手风格小丫鬟",
            r"风格小丫鬟", 
            r"小丫鬟模式",
            r"补手风格早喵",
            r"风格早喵",
            r"早喵模式",
            r"补手风格搞事早喵",
            r"风格搞事早喵",
            r"搞事早喵模式",
            r"补手风格司机",
            r"风格司机",
            r"司机模式",
            r"补手风格来问司机",
            r"风格来问司机",
            r"来问司机模式",
        ],
        
        # 模式设置
        CommandType.SET_MODE: [
            r"补手模式情侣",
            r"情侣模式",
            r"甜蜜模式",
        ],
        
        # 状态查询
        CommandType.STATUS: [
            r"补手状态",
            r"心灵补手状态",
            r"查看补手",
            r"补手查看",
            r"当前补手配置",
        ],
    }
    
    # persona别名映射
    PERSONA_ALIASES = {
        "大太监": "taijian",
        "小丫鬟": "xiaoyahuan",
        "早喵": "zaomiao",
        "搞事早喵": "zaomiao",
        "来问司机": "siji",
        "司机": "siji",
        "taijian": "taijian",
        "xiaoyahuan": "xiaoyahuan",
        "zaomiao": "zaomiao",
        "siji": "siji",
    }
    
    # mode别名映射
    MODE_ALIASES = {
        "情侣": "couple",
        "甜蜜": "couple",
        "normal": "normal",
        "couple": "couple",
    }
    
    def __init__(self):
        self._compile_patterns()
    
    def _compile_patterns(self) -> None:
        """编译正则表达式"""
        self._compiled_patterns: Dict[CommandType, List[re.Pattern]] = {}
        for cmd_type, patterns in self.COMMAND_PATTERNS.items():
            self._compiled_patterns[cmd_type] = [
                re.compile(p) for p in patterns
            ]
    
    def _normalize_text(self, text: str) -> str:
        """规范化文本"""
        # 去除首尾空格
        text = text.strip()
        # 转换为小写（但保留中文）
        # 不转小写，保持中文匹配
        return text
    
    def _match_command(self, text: str, cmd_type: CommandType) -> Optional[re.Match]:
        """匹配命令"""
        for pattern in self._compiled_patterns.get(cmd_type, []):
            match = pattern.search(text)
            if match:
                return match
        return None
    
    def _extract_level_from_match(self, match: re.Match) -> int:
        """从匹配中提取level"""
        groups = match.groups()
        for g in groups:
            if g is not None:
                try:
                    return int(g)
                except ValueError:
                    continue
        return 5  # 默认
    
    def parse(self, text: str) -> ParsedCommand:
        """
        解析命令
        
        Args:
            text: 用户输入文本
            
        Returns:
            ParsedCommand: 解析后的命令
        """
        text = self._normalize_text(text)
        
        # 尝试每个命令类型
        for cmd_type in CommandType:
            if cmd_type == CommandType.UNKNOWN:
                continue
            match = self._match_command(text, cmd_type)
            if match:
                return self._build_command(cmd_type, text, match)
        
        # 没有匹配的命令
        return ParsedCommand(
            command_type=CommandType.UNKNOWN,
            raw_command=text,
            args={}
        )
    
    def _build_command(self, cmd_type: CommandType, text: str, match: re.Match) -> ParsedCommand:
        """构建命令对象"""
        args = {}
        requires_confirmation = False
        
        if cmd_type == CommandType.ENABLE:
            args = {"enabled": True}
            
        elif cmd_type == CommandType.DISABLE:
            args = {"enabled": False}
            
        elif cmd_type == CommandType.SET_LEVEL:
            level = self._extract_level_from_match(match)
            level = max(1, min(10, level))  # 限制在1-10
            args = {"level": level}
            
        elif cmd_type == CommandType.ADJUST_LEVEL:
            # 判断是调高还是调低
            if any(k in text for k in ["全开", "拉满", "最大", "调高", "增加", "厉害", "夸多"]):
                args = {"level": 10}
            elif any(k in text for k in ["收敛", "低调", "调低", "减小", "温柔", "夸少"]):
                args = {"level": 3}
            else:
                args = {"level": 5}
                
        elif cmd_type == CommandType.SET_PERSONA:
            persona = None
            for alias, persona_id in self.PERSONA_ALIASES.items():
                if alias in text:
                    persona = persona_id
                    break
            if persona:
                args = {"persona": persona}
                
        elif cmd_type == CommandType.SET_MODE:
            mode = None
            for alias, mode_id in self.MODE_ALIASES.items():
                if alias in text:
                    mode = mode_id
                    break
            if mode:
                args = {"mode": mode}
                if mode == "couple":
                    requires_confirmation = True
                    
        elif cmd_type == CommandType.STATUS:
            args = {}
        
        return ParsedCommand(
            command_type=cmd_type,
            raw_command=text,
            args=args,
            requires_confirmation=requires_confirmation
        )
    
    def parse_all(self, text: str) -> List[ParsedCommand]:
        """
        解析所有可能的命令（用于同时包含多个命令的情况）
        """
        results = []
        # 简单的分割逻辑，按标点或空格分割
        parts = re.split(r'[,，;；\s]+', text)
        for part in parts:
            if part.strip():
                result = self.parse(part)
                if result.command_type != CommandType.UNKNOWN:
                    results.append(result)
        return results


# 快捷函数
_parser: Optional[CommandParser] = None


def get_parser() -> CommandParser:
    """获取解析器单例"""
    global _parser
    if _parser is None:
        _parser = CommandParser()
    return _parser


def parse_command(text: str) -> Dict[str, Any]:
    """快捷函数：解析命令"""
    result = get_parser().parse(text)
    return result.to_dict()


def parse_all_commands(text: str) -> List[Dict[str, Any]]:
    """快捷函数：解析所有命令"""
    results = get_parser().parse_all(text)
    return [r.to_dict() for r in results]
