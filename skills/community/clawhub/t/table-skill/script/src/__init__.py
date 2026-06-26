"""Skills 依赖的工具函数包。

从 script/utils 复制而来，使 skills 独立运行。
只导出被三个 skills 直接使用的函数。
"""

from .split_region import (
    split_workbook_all_sheets_return_worksheets,
    preprocess_excel,
    preprocess_merge,
    ws_to_df,
    split_df_by_blank_rows,
    preprocess_merge_xlrd,
    process_csv,
)
from .table_cleaning import (
    remove_blank_rows_and_columns,
    process_complex_header_table,
)
from .table_description import (
    transfer_to_csv_in_memory,
    describe_single_table,
    get_table_schema_origin,
    get_table_abstract,
    df_to_markdown,
)
from .llm_service import (
    OpenAILLMService,
    get_llm_service,
)

__all__ = [
    # split_region.py - 被 split_table_skill.py 使用
    "split_workbook_all_sheets_return_worksheets",
    "preprocess_excel",
    "preprocess_merge",
    "preprocess_merge_xlrd",
    "process_csv",
    # table_cleaning.py - 被 clean_table_skill.py 使用
    "remove_blank_rows_and_columns",
    "process_complex_header_table",
    # table_description.py - 被 describe_table_skill.py 使用
    "transfer_to_csv_in_memory",
    "describe_single_table",
    "get_table_schema_origin",
    "get_table_abstract",
    "df_to_markdown",
    # llm_service.py - LLM 服务
    "OpenAILLMService",
    "get_llm_service",
    "ws_to_df",
    "split_df_by_blank_rows",
]
