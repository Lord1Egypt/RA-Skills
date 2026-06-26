"""
心灵补手核心模块

提供触发检测、命令解析、话术生成、配置管理功能。
"""

from .config_manager import (
    ConfigManager,
    XinlingConfig,
    get_config_manager,
    load_config,
    save_config,
    update_config,
    get_config,
    reset_config,
)

from .trigger_detector import (
    TriggerDetector,
    TriggerResult,
    Scenario,
    get_detector,
    detect_trigger,
)

from .command_parser import (
    CommandParser,
    CommandType,
    ParsedCommand,
    get_parser,
    parse_command,
    parse_all_commands,
)

from .phrase_generator import (
    PhraseGenerator,
    GenerationResult,
    get_generator,
    generate_phrases,
    generate_care_message,
)

__all__ = [
    # Config
    "ConfigManager",
    "XinlingConfig",
    "get_config_manager",
    "load_config",
    "save_config",
    "update_config",
    "get_config",
    "reset_config",
    # Trigger
    "TriggerDetector",
    "TriggerResult",
    "Scenario",
    "get_detector",
    "detect_trigger",
    # Command
    "CommandParser",
    "CommandType",
    "ParsedCommand",
    "get_parser",
    "parse_command",
    "parse_all_commands",
    # Phrase
    "PhraseGenerator",
    "GenerationResult",
    "get_generator",
    "generate_phrases",
    "generate_care_message",
]

__version__ = "1.0.0"
