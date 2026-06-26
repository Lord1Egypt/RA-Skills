"""
为知笔记迁移技能 - Python 包入口

提供完整的为知笔记数据迁移功能：
1. 自动检测为知笔记数据目录
2. 生成详细导出操作指南
3. 批量迁移附件文件
"""

__version__ = "1.0.0"
__author__ = "OpenClaw Assistant"

from scripts.detector import detect_wiz_data_dir, validate_data_dir
from scripts.guide_generator import generate_export_guide, append_migration_log
from scripts.migrator import run_attachment_migration, find_attachments

__all__ = [
    "detect_wiz_data_dir",
    "validate_data_dir",
    "generate_export_guide",
    "append_migration_log",
    "run_attachment_migration",
    "find_attachments",
    "start_wizard"
]

# 导入主程序中的 start_wizard 函数
try:
    from bin.wiz-migrate import start_wizard
    __all__.append("start_wizard")
except ImportError:
    pass


def quick_start():
    """
    快速启动向导
    
    相当于: start_wizard()
    """
    from bin.wiz-migrate import start_wizard
    start_wizard()


if __name__ == "__main__":
    quick_start()
