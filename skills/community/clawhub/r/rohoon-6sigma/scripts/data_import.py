"""
数据批量导入模块
支持 CSV、Excel 格式数据导入
"""

import io
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

import pandas as pd


class ImportResult(BaseModel):
    """导入结果"""
    success: bool
    total_rows: int
    imported_rows: int
    failed_rows: int
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


def validate_measurement_data(
    df: pd.DataFrame,
    required_columns: List[str]
) -> ImportResult:
    """验证测量数据"""
    errors = []
    warnings = []
    
    # 检查必需列
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        errors.append(f"缺少必需列：{', '.join(missing_cols)}")
        return ImportResult(
            success=False,
            total_rows=len(df),
            imported_rows=0,
            failed_rows=len(df),
            errors=errors,
            warnings=warnings
        )
    
    # 检查空值
    for col in required_columns:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            warnings.append(f"列 '{col}' 有 {null_count} 个空值")
    
    # 检查数值列
    numeric_cols = ['measurement_value', 'usl', 'lsl', 'target']
    for col in numeric_cols:
        if col in df.columns:
            non_numeric = df[pd.to_numeric(df[col], errors='coerce').isnull() & df[col].notnull()]
            if len(non_numeric) > 0:
                errors.append(f"列 '{col}' 包含 {len(non_numeric)} 个非数值")
    
    # 检查日期格式
    if 'timestamp' in df.columns:
        try:
            pd.to_datetime(df['timestamp'])
        except Exception as e:
            errors.append(f"日期格式错误：{str(e)}")
    
    # 检查规格限
    if 'usl' in df.columns and 'lsl' in df.columns:
        invalid_spec = df[df['usl'] <= df['lsl']]
        if len(invalid_spec) > 0:
            errors.append(f"USL 必须大于 LSL，发现 {len(invalid_spec)} 条错误记录")
    
    success = len(errors) == 0
    
    return ImportResult(
        success=success,
        total_rows=len(df),
        imported_rows=len(df) if success else 0,
        failed_rows=0 if success else len(df),
        errors=errors,
        warnings=warnings
    )


def import_csv_data(
    file_content: bytes,
    required_columns: List[str]
) -> tuple[ImportResult, Optional[pd.DataFrame]]:
    """导入 CSV 数据"""
    try:
        # 读取 CSV
        df = pd.read_csv(io.BytesIO(file_content))
        
        # 验证数据
        result = validate_measurement_data(df, required_columns)
        
        if result.success:
            return result, df
        else:
            return result, None
            
    except Exception as e:
        return ImportResult(
            success=False,
            total_rows=0,
            imported_rows=0,
            failed_rows=0,
            errors=[f"CSV 解析失败：{str(e)}"],
            warnings=[]
        ), None


def import_excel_data(
    file_content: bytes,
    sheet_name: Optional[str] = None,
    required_columns: List[str] = None
) -> tuple[ImportResult, Optional[pd.DataFrame]]:
    """导入 Excel 数据"""
    try:
        # 读取 Excel
        if sheet_name:
            df = pd.read_excel(io.BytesIO(file_content), sheet_name=sheet_name)
        else:
            # 读取第一个 sheet
            excel_file = pd.ExcelFile(io.BytesIO(file_content))
            df = pd.read_excel(excel_file, sheet_name=excel_file.sheet_names[0])
        
        # 验证数据
        result = validate_measurement_data(df, required_columns or [])
        
        if result.success:
            return result, df
        else:
            return result, None
            
    except Exception as e:
        return ImportResult(
            success=False,
            total_rows=0,
            imported_rows=0,
            failed_rows=0,
            errors=[f"Excel 解析失败：{str(e)}"],
            warnings=[]
        ), None


def parse_measurement_data(
    df: pd.DataFrame,
    product_id: Optional[int] = None,
    process_id: Optional[int] = None,
    characteristic_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    """解析测量数据为数据库格式"""
    measurements = []
    
    for _, row in df.iterrows():
        measurement = {
            'product_id': product_id or row.get('product_id'),
            'process_id': process_id or row.get('process_id'),
            'characteristic_id': characteristic_id or row.get('characteristic_id'),
            'measurement_value': float(row.get('measurement_value', 0)),
            'timestamp': row.get('timestamp', datetime.now()),
            'operator': row.get('operator'),
            'equipment': row.get('equipment'),
            'batch_number': row.get('batch_number'),
            'notes': row.get('notes'),
        }
        
        # 添加规格限（如果有）
        if 'usl' in row:
            measurement['usl'] = float(row['usl'])
        if 'lsl' in row:
            measurement['lsl'] = float(row['lsl'])
        if 'target' in row:
            measurement['target'] = float(row['target'])
        
        measurements.append(measurement)
    
    return measurements


def generate_import_template(template_type: str = 'measurement') -> bytes:
    """生成导入模板"""
    if template_type == 'measurement':
        # 测量数据模板
        data = {
            'product_id': [1, 1, 1],
            'process_id': [1, 1, 1],
            'characteristic_id': [1, 1, 1],
            'measurement_value': [10.02, 10.01, 9.99],
            'timestamp': ['2026-03-27 10:00:00', '2026-03-27 11:00:00', '2026-03-27 12:00:00'],
            'operator': ['张三', '李四', '王五'],
            'equipment': ['卡尺#001', '卡尺#001', '卡尺#001'],
            'batch_number': ['BATCH-001', 'BATCH-001', 'BATCH-001'],
            'notes': ['', '', ''],
        }
        
        df = pd.DataFrame(data)
        
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, sheet_name='测量数据模板')
        buffer.seek(0)
        
        return buffer.read()
    
    elif template_type == 'grr':
        # GR&R 数据模板
        data = {
            'part_id': [1, 1, 1, 2, 2, 2],
            'operator_id': [1, 1, 1, 1, 1, 1],
            'trial_id': [1, 2, 3, 1, 2, 3],
            'measurement_value': [10.02, 10.01, 10.03, 10.05, 10.04, 10.06],
        }
        
        df = pd.DataFrame(data)
        
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, sheet_name='GR&R 数据模板')
        buffer.seek(0)
        
        return buffer.read()
    
    else:
        raise ValueError(f"不支持的模板类型：{template_type}")
