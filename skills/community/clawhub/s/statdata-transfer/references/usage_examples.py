"""Usage Examples | 使用示例 for statdata-transfer v2.0.0
All examples run in Python 3.10+ | 所有代码示例均可在 Python 3.10+ 环境中运行。
"""

# ---------------------------------------------------------------------------
# 基础读入 | Basic read
# ---------------------------------------------------------------------------

from scripts.reader_core import read_stat_file

result = read_stat_file("data.sav")
df = result["dataframe"]
meta = result["metadata"]
warnings = result["warnings"]

print(f"数据维度 Data dims: {meta['row_count']} 行rows × {meta['column_count']} 列cols")
print(f"变量标签 Var labels: {meta['variable_labels']}")

# ---------------------------------------------------------------------------
# 读入 Excel 所有工作表 | Read all Excel sheets
# ---------------------------------------------------------------------------

from scripts.reader_core import read_all_sheets

results = read_all_sheets("data.xlsx")
for sheet_name, result in results.items():
    print(f"{sheet_name}: {result['metadata']['row_count']} 行rows")

# ---------------------------------------------------------------------------
# 读入 RDA 所有对象 | Read all R objects
# ---------------------------------------------------------------------------

from scripts.reader_core import read_all_r_objects

results = read_all_r_objects("data.rda")
for obj_name, result in results.items():
    print(f"{obj_name}: {result['metadata']['row_count']} 行rows")

# ---------------------------------------------------------------------------
# 应用值标签 | Apply value labels
# ---------------------------------------------------------------------------

from scripts.reader_core import apply_value_labels

df_labeled = apply_value_labels(df, meta["value_labels"])

# ---------------------------------------------------------------------------
# 格式转换 | Format conversion
# ---------------------------------------------------------------------------

from scripts.reader_core import convert_stat_file

result = convert_stat_file("data.sav", "output.dta")
# {'src_format': 'spss_sav', 'dst_format': '.dta', 'rows': 100, 'columns': 10, 'warnings': []}

# ---------------------------------------------------------------------------
# 直接写出 | Direct write
# ---------------------------------------------------------------------------

from scripts.reader_core import read_stat_file, write_stat_file

result = read_stat_file("data.sav")
df = result["dataframe"]
meta = result["metadata"]

# 写出到任意格式 | Write to any format
write_stat_file(df, "output.sav", meta)      # SPSS
write_stat_file(df, "output.dta", meta)      # Stata
write_stat_file(df, "output.xlsx", meta)     # Excel
write_stat_file(df, "output.parquet", meta)  # Parquet

# Parquet/Feather/HDF5/JSON: 元数据嵌入 schema.metadata
# Parquet/Feather/HDF5/JSON: metadata embedded in schema.metadata

# ---------------------------------------------------------------------------
# 元数据丢失检查 | Metadata loss check
# ---------------------------------------------------------------------------

from scripts.writer import conversion_has_metadata_loss

# 检查从 .sav 到 .csv 是否有元数据丢失 | Check .sav → .csv metadata loss
warning = conversion_has_metadata_loss(".sav", ".csv")
if warning:
    print(f"⚠️ 警告Warning: {warning}")
