"""
为知笔记迁移技能

用于帮助用户将为知笔记数据迁移到其他笔记软件。

主要功能：
1. 智能检测为知笔记数据目录
2. 生成详细的 HTML 导出操作指南
3. 批量迁移附件文件
4. 提供完整的交互式向导

用法:
  python -m wiz_migration          # 启动交互向导
  python -m wiz_migration detect   # 仅检测数据目录
  python -m wiz_migration guide    # 仅生成导出指南
  python -m wiz_migration migrate  # 仅迁移附件
  
或者使用技能入口:
  python bin/wiz-migrate
"""

__version__ = "1.0.0"
