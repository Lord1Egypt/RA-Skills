# Excel 样式处理模块 - 已废弃
# 
# 本模块原有 update_excel_status 函数用于标记状态（已弃用，当前为只读模式，不写Excel）
# 现已改为纯只读模式，所有Excel写入操作已禁用
# 
# Excel处理逻辑已迁移到 core/excel_handler.py
# ExcelHandler 类中的 update_platform_status、update_publish_date、save_excel_with_style
# 方法已改为只记录日志，不执行任何实际写入操作
#
# 约束：程序运行全程仅读取Excel，不修改任何内容、格式、样式

# 保留空文件以兼容可能的外部引用
def update_excel_status(df, excel_path):
    """已废弃 - Excel纯只读模式，不再执行写入操作"""
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("update_excel_status 已废弃，Excel为纯只读模式")
    return None