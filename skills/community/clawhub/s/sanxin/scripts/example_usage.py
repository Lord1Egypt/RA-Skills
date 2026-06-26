# -*- coding: utf-8 -*-
"""
示例：使用 form_filler 填写申报表

这个脚本展示了如何使用 form_filler 模块来填写申报表。
"""

from form_filler import fill_form

# ==================== 配置区域 ====================

# 申报报告路径
SOURCE_DOC = r"C:\Users\11666\Downloads\申报报告.docx"

# 申请表路径（空表）
FORM_DOC = r"C:\Users\11666\Desktop\论文工作办公室\2026年\空表申报表.doc"

# 输出路径
OUTPUT_PATH = r"C:\Users\11666\Desktop\申报表_已填写.docx"

# 主表格索引（通常是第2个表格）
TABLE_INDEX = 2

# ==================== 内容映射 ====================

# 定义每个章节的内容
# 键：行号（从1开始）
# 值：该章节的完整内容

CONTENT_MAP = {
    1: """第一章内容...
    
这里填写完整的章节内容，包括：
- 项目背景
- 研究现状
- 参考文献
""",

    2: """第二章内容...

（一）适应症
...

（二）开展目的
...

（三）开展意义
...
""",

    # 继续添加其他章节...
}

# ==================== 执行填写 ====================

if __name__ == "__main__":
    success = fill_form(
        source_doc=SOURCE_DOC,
        form_doc=FORM_DOC,
        output_path=OUTPUT_PATH,
        content_map=CONTENT_MAP,
        table_index=TABLE_INDEX
    )
    
    if success:
        print("填写完成！")
    else:
        print("填写失败，请检查配置。")