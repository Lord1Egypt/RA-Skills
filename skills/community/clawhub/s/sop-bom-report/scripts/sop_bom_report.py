#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOP-BOM 校对报告生成器 v1.3.0 (混合解析版本)
- XML 解析物料编码和名称规格
- openpyxl 解析数值类型数据（数量）
- 跨平台兼容（Linux/Mac/Windows）
- 支持多种 SOP 格式
"""

import sys
import os
import re
import zipfile
import xml.etree.ElementTree as ET
import shutil
import logging
import tempfile
import platform
from typing import Dict, List, Any, Optional
from collections import Counter
import html

# 尝试导入 openpyxl（用于读取数值类型数据）
try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

# Python 版本检查
if sys.version_info < (3, 8):
    print("错误: 需要 Python 3.8 或更高版本")
    sys.exit(1)

# 跨平台临时目录
TEMP_DIR = tempfile.gettempdir()

# 平台检测
IS_WINDOWS = platform.system() == 'Windows'
IS_MACOS = platform.system() == 'Darwin'
IS_LINUX = platform.system() == 'Linux'

# 配置日志
def setup_logging(verbose=False):
    """配置日志（跨平台兼容）"""
    level = logging.DEBUG if verbose else logging.INFO
    
    # Windows 控制台编码处理
    if IS_WINDOWS:
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except:
            pass
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()


def safe_rmtree(path: str) -> bool:
    """安全删除目录（跨平台兼容）"""
    try:
        if os.path.exists(path):
            # Windows 上可能需要先修改权限
            if IS_WINDOWS:
                import stat
                def on_rm_error(func, p, exc_info):
                    os.chmod(p, stat.S_IWRITE)
                    func(p)
                shutil.rmtree(path, onerror=on_rm_error)
            else:
                shutil.rmtree(path, ignore_errors=True)
        return True
    except Exception as e:
        logger.warning(f"删除目录失败: {path} - {e}")
        return False


def get_dir_size(path: str) -> int:
    """计算目录大小（跨平台兼容）"""
    total_size = 0
    try:
        for root, dirs, files in os.walk(path):
            for f in files:
                try:
                    fp = os.path.join(root, f)
                    total_size += os.path.getsize(fp)
                except:
                    pass
    except:
        pass
    return total_size


def print_environment_info():
    """打印环境信息"""
    logger.info(f"Python 版本: {sys.version.split()[0]}")
    logger.info(f"平台: {platform.system()} {platform.release()}")
    logger.info(f"临时目录: {TEMP_DIR}")
    logger.info(f"工作目录: {os.getcwd()}")

NS = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

# 物料编码格式
MATERIAL_CODE_PATTERN = re.compile(r'^\d{5}-\d{3}-\d{3}$')


def safe_str(s: Any, max_len: int = 200) -> str:
    """安全转换为字符串"""
    if s is None:
        return ''
    s = str(s).strip()
    if len(s) > max_len:
        s = s[:max_len] + '...'
    return s


def escape_xml(s: str) -> str:
    """转义 XML 特殊字符"""
    if not s:
        return ''
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def normalize_for_compare(text: str) -> str:
    """规范化文本用于对比"""
    if not text:
        return ''
    
    text = text.translate(str.maketrans(
        '０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ',
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ))
    
    text = re.sub(r'[，。！？；：""\'\'【】（）、—…《》,.!?;:"\'\[\]\(\)\-…<>:：|｜/\\、\s\n\r\t]+', '', text)
    
    return text.lower()


def normalize_position_for_compare(text: str) -> str:
    """规范化位号用于对比"""
    if not text:
        return ''
    
    text = text.translate(str.maketrans(
        '０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ',
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ))
    
    text = re.sub(r'[（\(][^）\)]*[）\)]', '', text)
    positions = re.split(r'[,，\s\n\r]+', text)
    
    normalized = []
    for pos in positions:
        pos = pos.strip().upper()
        if pos:
            normalized.append(pos)
    
    return ''.join(sorted(set(normalized)))


def extract_page_number(text: str) -> int:
    """从页码文本中提取页号"""
    if not text:
        return 0
    match = re.search(r'第(\d+)页', str(text))
    return int(match.group(1)) if match else 0


def parse_shared_strings(extract_dir: str) -> List[str]:
    """解析共享字符串"""
    ss_path = os.path.join(extract_dir, 'xl', 'sharedStrings.xml')
    shared_strings = []
    
    if not os.path.exists(ss_path):
        return shared_strings
    
    with open(ss_path, 'r', encoding='utf-8') as f:
        ss_content = f.read()
    
    # 检查是否为空
    if 'count="0"' in ss_content or not ss_content.strip():
        return shared_strings
    
    try:
        ss_root = ET.fromstring(ss_content)
        for si in ss_root.findall('main:si', NS):
            text_parts = []
            for t in si.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'):
                if t.text:
                    text_parts.append(t.text)
            shared_strings.append(''.join(text_parts))
    except Exception as e:
        logger.warning(f"解析共享字符串失败: {e}")
    
    return shared_strings


def get_cell_value(row_content: str, col: str, shared_strings: List[str]) -> str:
    """提取指定列的单元格值"""
    # 匹配单元格 <c r="XX..." ...>...</c>
    pattern = rf'<c r="{col}\d+"([^>]*)>(.*?)</c>'
    match = re.search(pattern, row_content, re.DOTALL)
    
    if not match:
        return ''
    
    attrs = match.group(1)
    cell_content = match.group(2)
    
    # 检查是否是 inlineStr 格式 (t="inlineStr")
    if 't="inlineStr"' in attrs or 't="inlineStr"' in cell_content:
        # 提取 <is><t>...</t></is> 中的值
        is_match = re.search(r'<is><t[^>]*>([^<]*)</t></is>', cell_content)
        if is_match:
            return html.unescape(is_match.group(1))
        return ''
    
    # 提取值 <v>...</v>
    v_match = re.search(r'<v>([^<]*)</v>', cell_content)
    if not v_match:
        return ''
    
    value = v_match.group(1)
    
    # 检查是否是共享字符串 (t="s")
    if 't="s"' in attrs:
        try:
            idx = int(value)
            if 0 <= idx < len(shared_strings):
                return shared_strings[idx]
        except:
            pass
    
    return value


def col_name_to_num(col: str) -> int:
    """将列名转换为列号（A=1, B=2, ..., Z=26, AA=27, ...）"""
    num = 0
    for c in col:
        num = num * 26 + (ord(c.upper()) - ord('A') + 1)
    return num


def read_numeric_values_for_rows(sop_path: str, row_nums: List[int], columns: List[str] = None) -> Dict[int, Dict[str, Any]]:
    """使用 openpyxl 读取指定行的数值类型数据（优化版本，只读取需要的行）
    
    Args:
        sop_path: SOP 文件路径
        row_nums: 要读取的行号列表
        columns: 要读取的列名列表（如 ['BO', 'BP', 'BQ']）
    
    Returns:
        {行号: {列名: 值}} 的字典
    """
    if not HAS_OPENPYXL:
        logger.warning("openpyxl 未安装，无法读取数值类型数据")
        return {}
    
    if not row_nums:
        return {}
    
    result = {}
    
    try:
        # 使用 data_only=True 读取实际显示值
        wb = openpyxl.load_workbook(sop_path, data_only=True, read_only=True)
        ws = wb.active
        
        if columns is None:
            columns = ['BO', 'BP', 'BQ', 'BN']
        
        # 将列名转换为列号
        col_nums = {col: col_name_to_num(col) for col in columns}
        
        # 只读取指定行
        row_set = set(row_nums)
        max_row = max(row_nums) if row_nums else 0
        
        for row in ws.iter_rows(max_row=max_row):
            row_num = row[0].row if row else 0
            if row_num not in row_set:
                continue
            
            row_data = {}
            for col, col_num in col_nums.items():
                try:
                    # 从当前行获取单元格
                    if col_num <= len(row):
                        cell = row[col_num - 1]  # 0-indexed
                        val = cell.value
                        if val is not None:
                            # 只保留数值类型
                            if isinstance(val, (int, float)) and not isinstance(val, bool):
                                row_data[col] = int(val) if isinstance(val, int) or val == int(val) else val
                except:
                    pass
            
            if row_data:
                result[row_num] = row_data
        
        wb.close()
        logger.info(f"openpyxl 读取到 {len(result)} 行数值数据（共 {len(row_nums)} 个目标行）")
        
    except Exception as e:
        logger.warning(f"openpyxl 读取失败: {e}")
    
    return result


def parse_sop_file(sop_path: str) -> List[Dict]:
    """解析 SOP 文件 - 优先使用标准格式，兼容多列提取"""
    items = []
    
    extract_dir = os.path.join(TEMP_DIR, f'sop_extract_{os.getpid()}')
    safe_rmtree(extract_dir)
    
    with zipfile.ZipFile(sop_path, 'r') as zf:
        zf.extractall(extract_dir)
    
    # 查找工作表（优先选择包含 AQ 或 AR 列数据的表）
    worksheets_dir = os.path.join(extract_dir, 'xl', 'worksheets')
    best_sheet = None
    best_aq_count = 0
    best_total_count = 0
    
    for sheet_file in sorted(os.listdir(worksheets_dir)):
        if not sheet_file.endswith('.xml') or not sheet_file.startswith('sheet'):
            continue
        candidate = os.path.join(worksheets_dir, sheet_file)
        if os.path.isdir(candidate):
            continue
        try:
            with open(candidate, 'r', encoding='utf-8') as f:
                content = f.read()
            aq_count = len(re.findall(r'<c r="AQ\d+"', content))
            ar_count = len(re.findall(r'<c r="AR\d+"', content))
            total_count = len(re.findall(r'<c r="[A-Z]+\d+"', content))
            # 优先选择有 AQ 或 AR 列的表，其次选择数据最多的表
            target_count = aq_count + ar_count
            if target_count > best_aq_count or (target_count == best_aq_count and total_count > best_total_count):
                best_aq_count = target_count
                best_total_count = total_count
                best_sheet = candidate
        except:
            continue
    
    if not best_sheet:
        logger.error("SOP 文件中未找到工作表")
        safe_rmtree(extract_dir)
        return items
    
    logger.info(f"选择工作表: {os.path.basename(best_sheet)}, 数据量: {best_total_count}")
    
    # 解析共享字符串
    shared_strings = parse_shared_strings(extract_dir)
    logger.info(f"共享字符串数量: {len(shared_strings)}")
    
    # 解析工作表
    with open(best_sheet, 'r', encoding='utf-8') as f:
        sheet_content = f.read()
    
    current_page = 0
    
    # ========== 标准格式提取 ==========
    # AQ列物料编码 + AN列序号(1-20)
    standard_items = []
    material_rows = []  # 收集物料编码所在的行号
    
    for row_match in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', sheet_content, re.DOTALL):
        row_num = int(row_match.group(1))
        row_content = row_match.group(2)
        
        bf_val = get_cell_value(row_content, 'BF', shared_strings)
        an_val = get_cell_value(row_content, 'AN', shared_strings)
        aq_val = get_cell_value(row_content, 'AQ', shared_strings)
        ax_val = get_cell_value(row_content, 'AX', shared_strings)
        bi_val = get_cell_value(row_content, 'BI', shared_strings)
        bo_val = get_cell_value(row_content, 'BO', shared_strings)
        
        # 更新页码
        if bf_val and '第' in str(bf_val) and '页' in str(bf_val):
            new_page = extract_page_number(bf_val)
            if new_page > 0:
                current_page = new_page
        
        # 标准格式：AQ列物料编码
        if not aq_val:
            continue
        
        code = str(aq_val).strip()
        if not MATERIAL_CODE_PATTERN.match(code):
            continue
        
        # 标准格式：AN列序号(1-20)
        if not an_val:
            continue
        
        seq_str = str(an_val).strip()
        if not seq_str.isdigit():
            continue
        
        seq = int(seq_str)
        if seq < 1 or seq > 20:
            continue
        
        material_rows.append(row_num)
        
        standard_items.append({
            'page': current_page,
            'seq': seq,
            'code': code,
            'name_spec': ax_val,
            'position': bi_val,
            'qty': bo_val,  # 先用 XML 解析的值
            'row': row_num
        })
    
    # 如果标准格式提取到物料，用 openpyxl 补充数值数量
    if standard_items:
        logger.info(f"标准格式提取到 {len(standard_items)} 项物料")
        
        # 用 openpyxl 读取指定行的数值
        if HAS_OPENPYXL and material_rows:
            numeric_values = read_numeric_values_for_rows(sop_path, material_rows, columns=['BO', 'BP', 'BN', 'BQ'])
            
            # 合并数值数量
            for item in standard_items:
                row_num = item['row']
                if row_num in numeric_values:
                    for col in ['BO', 'BP', 'BN', 'BQ']:
                        if col in numeric_values[row_num]:
                            item['qty'] = numeric_values[row_num][col]
                            break
        
        items = standard_items
    else:
        # ========== 兼容模式：多列提取 ==========
        logger.info("标准格式未提取到物料，启用多列兼容模式")
        
        # 可能包含物料编码的列（按优先级排序）
        CODE_COLUMNS = ['AQ', 'AR', 'AX', 'AN', 'BU', 'BF', 'A', 'I']
        # 可能包含名称规格的列
        NAME_COLUMNS = ['AX', 'AQ', 'AR', 'AN', 'BU', 'BF']
        # 可能包含位号的列
        POSITION_COLUMNS = ['BI', 'BJ', 'BK']
        # 可能包含数量的列
        QTY_COLUMNS = ['BO', 'BP', 'BN', 'BQ']
        
        current_page = 0
        material_rows = []  # 收集物料编码所在的行号
        
        for row_match in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', sheet_content, re.DOTALL):
            row_num = int(row_match.group(1))
            row_content = row_match.group(2)
            
            # 提取所有相关列的值
            col_values = {}
            all_cols = set(CODE_COLUMNS + NAME_COLUMNS + POSITION_COLUMNS + QTY_COLUMNS + ['BF'])
            for col in all_cols:
                col_values[col] = get_cell_value(row_content, col, shared_strings)
            
            # 更新页码
            bf_val = col_values.get('BF', '')
            if bf_val and '第' in str(bf_val) and '页' in str(bf_val):
                new_page = extract_page_number(bf_val)
                if new_page > 0:
                    current_page = new_page
            
            # 在多个列中查找物料编码
            code = None
            code_index = None  # 记录物料编码在共享字符串中的索引
            for col in CODE_COLUMNS:
                val = col_values.get(col, '')
                if val:
                    # 检查是否是物料编码格式
                    if MATERIAL_CODE_PATTERN.match(str(val).strip()):
                        code = str(val).strip()
                        # 在共享字符串中查找索引
                        try:
                            code_index = shared_strings.index(code)
                        except:
                            pass
                        break
                    # 检查是否是数字索引（指向共享字符串）
                    try:
                        idx = int(val)
                        if idx < len(shared_strings) and MATERIAL_CODE_PATTERN.match(shared_strings[idx].strip()):
                            code = shared_strings[idx].strip()
                            code_index = idx
                            break
                    except:
                        pass
            
            if not code:
                continue
            
            material_rows.append(row_num)
            
            # 查找名称规格
            # 优先：从共享字符串中物料编码索引+1的位置获取
            name_spec = ''
            if code_index is not None and code_index + 1 < len(shared_strings):
                next_val = shared_strings[code_index + 1]
                if not MATERIAL_CODE_PATTERN.match(next_val.strip()):
                    name_spec = next_val
            # 后备：从名称规格列查找
            if not name_spec:
                for col in NAME_COLUMNS:
                    val = col_values.get(col, '')
                    if val and not MATERIAL_CODE_PATTERN.match(str(val).strip()):
                        # 检查是否是数字索引
                        try:
                            idx = int(val)
                            if idx < len(shared_strings):
                                actual_val = shared_strings[idx]
                                if not MATERIAL_CODE_PATTERN.match(actual_val.strip()):
                                    name_spec = actual_val
                                    break
                        except:
                            name_spec = str(val)
                            break
            
            # 查找位号
            position = ''
            for col in POSITION_COLUMNS:
                val = col_values.get(col, '')
                if val:
                    # 检查是否是数字索引
                    try:
                        idx = int(val)
                        if idx < len(shared_strings):
                            position = shared_strings[idx]
                            break
                    except:
                        position = str(val)
                        break
            
            # 查找数量（先用 XML 解析的值）
            qty = ''
            for col in QTY_COLUMNS:
                val = col_values.get(col, '')
                if val:
                    # 检查是否是数字索引
                    try:
                        idx = int(val)
                        if idx < len(shared_strings):
                            qty = shared_strings[idx]
                            break
                    except:
                        qty = str(val)
                        break
            
            # 序号：尝试从 AN 列获取
            an_val = col_values.get('AN', '')
            seq = 0
            if an_val and str(an_val).strip().isdigit():
                seq = int(str(an_val).strip())
            
            items.append({
                'page': current_page,
                'seq': seq,
                'code': code,
                'name_spec': name_spec,
                'position': position,
                'qty': qty,
                'row': row_num
            })
        
        # 用 openpyxl 补充数值数量
        if HAS_OPENPYXL and material_rows:
            numeric_values = read_numeric_values_for_rows(sop_path, material_rows, columns=QTY_COLUMNS)
            
            # 合并数值数量
            for item in items:
                row_num = item['row']
                if row_num in numeric_values:
                    for col in QTY_COLUMNS:
                        if col in numeric_values[row_num]:
                            item['qty'] = numeric_values[row_num][col]
                            break
    
    # 如果兼容模式仍然没有提取到物料，使用共享字符串直接提取
    if not items:
        logger.info("兼容模式未提取到物料，启用共享字符串直接提取模式")
        for i, s in enumerate(shared_strings):
            code = s.strip()
            if MATERIAL_CODE_PATTERN.match(code):
                # 获取相邻的名称规格
                name_spec = ''
                if i + 1 < len(shared_strings):
                    next_val = shared_strings[i + 1]
                    if not MATERIAL_CODE_PATTERN.match(next_val.strip()):
                        name_spec = next_val
                
                items.append({
                    'page': 0,
                    'seq': 0,
                    'code': code,
                    'name_spec': name_spec,
                    'position': '',
                    'qty': '',
                    'row': 0
                })
    
    safe_rmtree(extract_dir)
    logger.info(f"SOP 解析完成，共 {len(items)} 项物料")
    
    return items


def parse_bom_file(bom_path: str) -> List[Dict]:
    """解析 BOM 文件"""
    items = []
    
    extract_dir = os.path.join(TEMP_DIR, f'bom_extract_{os.getpid()}')
    if os.path.exists(extract_dir):
        safe_rmtree(extract_dir)
    
    with zipfile.ZipFile(bom_path, 'r') as zf:
        zf.extractall(extract_dir)
    
    # 查找工作表
    worksheets_dir = os.path.join(extract_dir, 'xl', 'worksheets')
    sheet_path = None
    for sheet_file in sorted(os.listdir(worksheets_dir)):
        candidate = os.path.join(worksheets_dir, sheet_file)
        if os.path.exists(candidate) and not os.path.isdir(candidate):
            sheet_path = candidate
            break
    
    if not sheet_path:
        logger.error("BOM 文件中未找到工作表")
        safe_rmtree(extract_dir)
        return items
    
    # 解析共享字符串（可能为空）
    shared_strings = parse_shared_strings(extract_dir)
    logger.info(f"BOM 共享字符串数量: {len(shared_strings)}")
    
    # 解析工作表
    with open(sheet_path, 'r', encoding='utf-8') as f:
        sheet_content = f.read()
    
    # 解析每一行
    for row_match in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', sheet_content, re.DOTALL):
        row_num = int(row_match.group(1))
        if row_num < 2:  # 跳过表头
            continue
        
        row_content = row_match.group(2)
        
        # 提取各列值
        # 新格式: F=项次, G=物料编码, H=名称, I=规格, K=用量分子, L=用量分母, M=备注
        # 旧格式: H=项次, I=物料编码, J=名称, K=规格, N=用量分子, O=用量分母, P=备注
        f_val = get_cell_value(row_content, 'F', shared_strings)
        g_val = get_cell_value(row_content, 'G', shared_strings)
        h_val = get_cell_value(row_content, 'H', shared_strings)
        i_val = get_cell_value(row_content, 'I', shared_strings)
        j_val = get_cell_value(row_content, 'J', shared_strings)
        k_val = get_cell_value(row_content, 'K', shared_strings)
        l_val = get_cell_value(row_content, 'L', shared_strings)
        m_val = get_cell_value(row_content, 'M', shared_strings)
        n_val = get_cell_value(row_content, 'N', shared_strings)
        o_val = get_cell_value(row_content, 'O', shared_strings)
        p_val = get_cell_value(row_content, 'P', shared_strings)
        
        # 智能检测列格式：优先检测新格式（G列有物料编码）
        # 新格式: F=项次, G=物料编码, H=名称, I=规格, K=用量分子, L=用量分母, M=备注
        # 旧格式: H=项次, I=物料编码, J=名称, K=规格, N=用量分子, O=用量分母, P=备注
        if g_val and MATERIAL_CODE_PATTERN.match(str(g_val).strip()):
            # 新格式
            code = str(g_val).strip()
            seq = f_val
            name = h_val
            spec = i_val
            num_val = k_val
            den_val = l_val
            position = m_val
        elif i_val and MATERIAL_CODE_PATTERN.match(str(i_val).strip()):
            # 旧格式
            code = str(i_val).strip()
            seq = h_val
            name = j_val
            spec = k_val
            num_val = n_val
            den_val = o_val
            position = p_val
        else:
            # 无有效物料编码，跳过
            continue
        
        if not MATERIAL_CODE_PATTERN.match(code):
            continue
        
        # 计算数量
        try:
            num = float(num_val) if num_val else 1
            den = float(den_val) if den_val else 1
            qty = num / den if den > 0 else num
            qty = int(qty) if qty == int(qty) else round(qty, 2)
        except:
            qty = num_val or '1'
        
        items.append({
            'seq': seq,
            'code': code,
            'name': name,
            'spec': spec,
            'position': position,
            'qty': str(qty),
            'row': row_num
        })
    
    safe_rmtree(extract_dir)
    logger.info(f"BOM 解析完成，共 {len(items)} 项物料")
    
    return items


def compare_bom_sop(sop_items: List[Dict], bom_items: List[Dict]) -> Dict:
    """对比 BOM 和 SOP"""
    result = {
        'diffs': [],
        'only_sop': [],
        'only_bom': [],
        'duplicate_codes': set()
    }
    
    code_counts = Counter(item['code'] for item in sop_items)
    result['duplicate_codes'] = {code for code, count in code_counts.items() if count > 1}
    
    logger.info(f"SOP 中重复物料编码: {len(result['duplicate_codes'])} 个")
    
    bom_index = {}
    for item in bom_items:
        code = item['code']
        if code not in bom_index:
            bom_index[code] = []
        bom_index[code].append(item)
    
    sop_index = {}
    for item in sop_items:
        code = item['code']
        if code not in sop_index:
            sop_index[code] = []
        sop_index[code].append(item)
    
    sop_codes = set(sop_index.keys())
    bom_codes = set(bom_index.keys())
    
    for code in bom_codes - sop_codes:
        for item in bom_index[code]:
            result['only_bom'].append(item)
    
    for code in sop_codes - bom_codes:
        for item in sop_index[code]:
            result['only_sop'].append(item)
    
    for code in sop_codes & bom_codes:
        sop_list = sop_index[code]
        bom_list = bom_index[code]
        
        for sop_item in sop_list:
            bom_item = bom_list[0] if bom_list else None
            
            if not bom_item:
                result['only_sop'].append(sop_item)
                continue
            
            diff_types = []
            diff_details = {}
            
            bom_name_spec = f"{bom_item.get('name', '')}|{bom_item.get('spec', '')}"
            sop_name_spec = sop_item.get('name_spec', '')
            if bom_name_spec and sop_name_spec:
                if normalize_for_compare(bom_name_spec) != normalize_for_compare(sop_name_spec):
                    diff_types.append('名称规格')
            
            bom_pos = bom_item.get('position', '')
            sop_pos = sop_item.get('position', '')
            if bom_pos and sop_pos:
                if normalize_position_for_compare(bom_pos) != normalize_position_for_compare(sop_pos):
                    diff_types.append('位号')
            
            bom_qty = bom_item.get('qty', '')
            sop_qty = sop_item.get('qty', '')
            if bom_qty and sop_qty:
                try:
                    if abs(float(bom_qty) - float(sop_qty)) > 0.001:
                        diff_types.append('数量')
                except:
                    if bom_qty != sop_qty:
                        diff_types.append('数量')
            
            if diff_types:
                result['diffs'].append({
                    'sop_item': sop_item,
                    'bom_item': bom_item,
                    'diff_types': diff_types,
                    'is_duplicate': code in result['duplicate_codes']
                })
    
    return result


def create_report_xlsx(result: Dict, output_path: str, sop_items: List[Dict] = None) -> str:
    """生成校对报告 xlsx 文件（纯 XML 方式，自动检测列，自适应列宽）
    
    Args:
        result: 对比结果
        output_path: 输出路径
        sop_items: SOP物料列表（用于检测是否有位号/数量）
    """
    
    # 检测 SOP 是否有位号和数量
    # 位号格式：字母+数字，如 R1, C10, U3A, JP1, CN2 等
    POSITION_PATTERN = re.compile(r'^[A-Z]{1,3}\d+[A-Z]?$', re.IGNORECASE)
    
    has_position = False
    has_qty = False
    if sop_items:
        for item in sop_items:
            pos = item.get('position', '')
            if pos and POSITION_PATTERN.match(str(pos).strip()):
                has_position = True
            if item.get('qty'):
                has_qty = True
            if has_position and has_qty:
                break
    
    # 构建动态表头
    # SOP 侧
    sop_headers = ['页码', '序号', '物料编码', '名称规格']
    if has_position:
        sop_headers.append('位号')
    if has_qty:
        sop_headers.append('数量')
    
    # BOM 侧
    bom_headers = ['项次', '物料编码', '名称', '规格']
    if has_position:
        bom_headers.append('位号')
    if has_qty:
        bom_headers.append('数量')
    
    logger.info(f"报告列配置: SOP{sop_headers}, BOM{bom_headers}")
    
    # 计算每列最大宽度（自适应）
    col_widths = {}  # {列索引: 最大宽度}
    
    def update_col_width(col_idx: int, text: str):
        """更新列宽（中文字符算2个宽度）"""
        if not text:
            return
        # 计算显示宽度（中文2，英文1）
        width = 0
        for c in str(text):
            if '\u4e00' <= c <= '\u9fff':  # 中文字符
                width += 2
            else:
                width += 1
        if col_idx not in col_widths or width > col_widths[col_idx]:
            col_widths[col_idx] = width
    
    temp_dir = os.path.join(TEMP_DIR, f'report_{os.getpid()}')
    safe_rmtree(temp_dir)
    
    # 创建目录结构
    os.makedirs(os.path.join(temp_dir, 'xl', 'worksheets'), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, 'xl', '_rels'), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, '_rels'), exist_ok=True)
    
    # 收集所有字符串
    all_strings = []
    string_index = {}
    
    def add_string(s):
        s = safe_str(s, 200)  # 增加最大长度
        if not s:
            return -1
        if s not in string_index:
            string_index[s] = len(all_strings)
            all_strings.append(s)
        return string_index[s]
    
    # 构建行数据
    rows_xml = []
    row_num = 1
    
    # 表格1标题（加高）
    title1_idx = add_string("【有差异的物料】")
    update_col_width(0, "【有差异的物料】")
    rows_xml.append(f'<row r="{row_num}" ht="25" customHeight="1"><c r="A{row_num}" t="s"><v>{title1_idx}</v></c></row>')
    row_num += 1
    
    # 表头（SOP列 + 分隔列 + BOM列）- 加粗加高
    all_headers = sop_headers + [''] + bom_headers
    total_cols = len(all_headers)
    header_cells = []
    for i, h in enumerate(all_headers):
        col = chr(ord('A') + i) if i < 26 else chr(ord('A') + i // 26 - 1) + chr(ord('A') + i % 26)
        update_col_width(i, h)  # 记录表头宽度
        if h:  # 非空表头
            idx = add_string(h)
            header_cells.append(f'<c r="{col}{row_num}" t="s"><v>{idx}</v></c>')
        else:  # 空分隔列
            header_cells.append(f'<c r="{col}{row_num}"/>')
    rows_xml.append(f'<row r="{row_num}" ht="22" customHeight="1">{"".join(header_cells)}</row>')
    row_num += 1
    
    # 差异数据
    for diff in result['diffs']:
        sop = diff['sop_item']
        bom = diff['bom_item']
        is_duplicate = diff.get('is_duplicate', False)
        diff_types = diff.get('diff_types', [])
        
        # SOP 数据（动态列）
        sop_vals = [str(sop.get('page', '')), str(sop.get('seq', '')), sop.get('code', ''), sop.get('name_spec', '')]
        if has_position:
            sop_vals.append(sop.get('position', ''))
        if has_qty:
            sop_vals.append(sop.get('qty', ''))
        
        # BOM 数据（动态列）
        bom_vals = [bom.get('seq', ''), bom.get('code', ''), bom.get('name', ''), bom.get('spec', '')]
        if has_position:
            bom_vals.append(bom.get('position', ''))
        if has_qty:
            bom_vals.append(bom.get('qty', ''))
        
        # 构建单元格
        cells = []
        col_idx = 0
        
        # SOP 数据
        for val in sop_vals:
            col = chr(ord('A') + col_idx) if col_idx < 26 else chr(ord('A') + col_idx // 26 - 1) + chr(ord('A') + col_idx % 26)
            update_col_width(col_idx, val)  # 更新列宽
            if val:
                idx = add_string(val)
                # 添加样式属性
                style = ''
                if col_idx == 2 and is_duplicate:  # 物料编码列，重复物料
                    style = ' s="2"'  # 黄色样式
                elif col_idx == 3 and '名称规格' in diff_types:
                    style = ' s="1"'  # 红色样式
                elif has_position and col_idx == 4 and '位号' in diff_types:
                    style = ' s="1"'
                elif has_qty and ((has_position and col_idx == 5) or (not has_position and col_idx == 4)) and '数量' in diff_types:
                    style = ' s="1"'
                cells.append(f'<c r="{col}{row_num}"{style} t="s"><v>{idx}</v></c>')
            else:
                cells.append(f'<c r="{col}{row_num}"/>')
            col_idx += 1
        
        # 分隔列
        col = chr(ord('A') + col_idx) if col_idx < 26 else chr(ord('A') + col_idx // 26 - 1) + chr(ord('A') + col_idx % 26)
        cells.append(f'<c r="{col}{row_num}"/>')
        col_idx += 1
        
        # BOM 数据
        for val in bom_vals:
            col = chr(ord('A') + col_idx) if col_idx < 26 else chr(ord('A') + col_idx // 26 - 1) + chr(ord('A') + col_idx % 26)
            update_col_width(col_idx, val)  # 更新列宽
            if val:
                idx = add_string(val)
                cells.append(f'<c r="{col}{row_num}" t="s"><v>{idx}</v></c>')
            else:
                cells.append(f'<c r="{col}{row_num}"/>')
            col_idx += 1
        
        rows_xml.append(f'<row r="{row_num}" ht="20" customHeight="1">{"".join(cells)}</row>')
        row_num += 1
    
    row_num += 1
    
    # 表格2：SOP 独有（加高标题）
    title2_idx = add_string("【SOP 独有物料】（SOP中有但BOM中没有）")
    update_col_width(0, "【SOP 独有物料】（SOP中有但BOM中没有）")
    rows_xml.append(f'<row r="{row_num}" ht="25" customHeight="1"><c r="A{row_num}" t="s"><v>{title2_idx}</v></c></row>')
    row_num += 1
    
    # 表头（加高）
    header_cells = []
    for i, h in enumerate(sop_headers):
        col = chr(ord('A') + i) if i < 26 else chr(ord('A') + i // 26 - 1) + chr(ord('A') + i % 26)
        update_col_width(i, h)
        idx = add_string(h)
        header_cells.append(f'<c r="{col}{row_num}" t="s"><v>{idx}</v></c>')
    rows_xml.append(f'<row r="{row_num}" ht="22" customHeight="1">{"".join(header_cells)}</row>')
    row_num += 1
    
    for item in result['only_sop']:
        cells = []
        vals = [str(item.get('page', '')), str(item.get('seq', '')), item.get('code', ''), item.get('name_spec', '')]
        if has_position:
            vals.append(item.get('position', ''))
        if has_qty:
            vals.append(item.get('qty', ''))
        
        for i, val in enumerate(vals):
            col = chr(ord('A') + i) if i < 26 else chr(ord('A') + i // 26 - 1) + chr(ord('A') + i % 26)
            update_col_width(i, val)
            if val:
                idx = add_string(val)
                cells.append(f'<c r="{col}{row_num}" t="s"><v>{idx}</v></c>')
            else:
                cells.append(f'<c r="{col}{row_num}"/>')
        rows_xml.append(f'<row r="{row_num}" ht="20" customHeight="1">{"".join(cells)}</row>')
        row_num += 1
    
    row_num += 1
    
    # 表格3：BOM 独有（加高标题）
    title3_idx = add_string("【BOM 独有物料】（BOM中有但SOP中没有）")
    update_col_width(0, "【BOM 独有物料】（BOM中有但SOP中没有）")
    rows_xml.append(f'<row r="{row_num}" ht="25" customHeight="1"><c r="A{row_num}" t="s"><v>{title3_idx}</v></c></row>')
    row_num += 1
    
    # 表头（加高）
    header_cells = []
    for i, h in enumerate(bom_headers):
        col = chr(ord('A') + i) if i < 26 else chr(ord('A') + i // 26 - 1) + chr(ord('A') + i % 26)
        update_col_width(i, h)
        idx = add_string(h)
        header_cells.append(f'<c r="{col}{row_num}" t="s"><v>{idx}</v></c>')
    rows_xml.append(f'<row r="{row_num}" ht="22" customHeight="1">{"".join(header_cells)}</row>')
    row_num += 1
    
    for item in result['only_bom']:
        cells = []
        vals = [item.get('seq', ''), item.get('code', ''), item.get('name', ''), item.get('spec', '')]
        if has_position:
            vals.append(item.get('position', ''))
        if has_qty:
            vals.append(item.get('qty', ''))
        
        for i, val in enumerate(vals):
            col = chr(ord('A') + i) if i < 26 else chr(ord('A') + i // 26 - 1) + chr(ord('A') + i % 26)
            update_col_width(i, val)
            if val:
                idx = add_string(val)
                cells.append(f'<c r="{col}{row_num}" t="s"><v>{idx}</v></c>')
            else:
                cells.append(f'<c r="{col}{row_num}"/>')
        rows_xml.append(f'<row r="{row_num}" ht="20" customHeight="1">{"".join(cells)}</row>')
        row_num += 1
    
    max_row = row_num - 1
    
    # 生成列宽配置（自适应）
    col_defs = []
    for i in range(total_cols):
        width = max(col_widths.get(i, 8) + 2, 8)  # 最小8，加2个字符的padding
        col_defs.append(f'<col min="{i+1}" max="{i+1}" width="{width}" customWidth="1"/>')
    cols_xml = ''.join(col_defs)
    
    # 生成共享字符串 XML
    ss_items = ''.join(f'<si><t>{escape_xml(s)}</t></si>' for s in all_strings)
    shared_strings_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(all_strings)}" uniqueCount="{len(all_strings)}">{ss_items}</sst>'''
    
    # 生成工作表 XML（自适应列宽）
    sheet_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<dimension ref="A1:{chr(ord('A') + total_cols - 1) if total_cols <= 26 else 'A' + chr(ord('A') + total_cols - 27)}{max_row}"/>
<sheetViews><sheetView workbookViewId="0"/></sheetViews>
<sheetFormatPr defaultColWidth="15" defaultRowHeight="20"/>
<cols>
{cols_xml}
</cols>
<sheetData>{"".join(rows_xml)}</sheetData>
</worksheet>'''
    
    # 生成样式 XML（包含红色和黄色填充）
    styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fills count="3">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFFF0000"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFFFFF00"/></patternFill></fill>
</fills>
<cellXfs count="3">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
<xf numFmtId="0" fontId="0" fillId="1" borderId="0"/>
<xf numFmtId="0" fontId="0" fillId="2" borderId="0"/>
</cellXfs>
</styleSheet>'''
    
    # 生成其他必要文件
    workbook_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="校对报告" sheetId="1" r:id="rId1"/></sheets>
</workbook>'''
    
    workbook_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''
    
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>'''
    
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''
    
    # 写入文件
    with open(os.path.join(temp_dir, '[Content_Types].xml'), 'w', encoding='utf-8') as f:
        f.write(content_types)
    
    with open(os.path.join(temp_dir, '_rels', '.rels'), 'w', encoding='utf-8') as f:
        f.write(rels)
    
    with open(os.path.join(temp_dir, 'xl', 'workbook.xml'), 'w', encoding='utf-8') as f:
        f.write(workbook_xml)
    
    with open(os.path.join(temp_dir, 'xl', '_rels', 'workbook.xml.rels'), 'w', encoding='utf-8') as f:
        f.write(workbook_rels)
    
    with open(os.path.join(temp_dir, 'xl', 'worksheets', 'sheet1.xml'), 'w', encoding='utf-8') as f:
        f.write(sheet_xml)
    
    with open(os.path.join(temp_dir, 'xl', 'sharedStrings.xml'), 'w', encoding='utf-8') as f:
        f.write(shared_strings_xml)
    
    with open(os.path.join(temp_dir, 'xl', 'styles.xml'), 'w', encoding='utf-8') as f:
        f.write(styles_xml)
    
    # 打包成 xlsx
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, temp_dir)
                zf.write(file_path, arc_name)
    
    # 清理
    safe_rmtree(temp_dir)
    
    return output_path


def extract_order_number(filename: str) -> str:
    """从文件名中提取订单编号"""
    match = re.match(r'^(\d{5}-\d{3}-\d{3})', filename)
    if match:
        return match.group(1)
    return "校对报告"


def cleanup_cache(output_dir: str, max_reports: int = 20, max_age_days: int = 7):
    """清理缓存
    
    Args:
        output_dir: 输出目录
        max_reports: 保留的最大报告数量
        max_age_days: 报告最大保留天数
    """
    import time
    from datetime import datetime, timedelta
    
    cleaned = {
        'temp_dirs': 0,
        'old_reports': 0,
        'freed_mb': 0
    }
    
    # 1. 清理临时目录
    temp_patterns = [
        os.path.join(TEMP_DIR, 'sop_extract_*'),
        os.path.join(TEMP_DIR, 'bom_extract_*'),
        os.path.join(TEMP_DIR, 'report_*')
    ]
    
    import glob
    for pattern in temp_patterns:
        try:
            for path in glob.glob(pattern):
                if os.path.isdir(path):
                    size = get_dir_size(path)
                    if safe_rmtree(path):
                        cleaned['temp_dirs'] += 1
                        cleaned['freed_mb'] += size / (1024 * 1024)
        except Exception as e:
            logger.warning(f"清理临时目录失败: {e}")
    
    # 2. 清理旧报告
    if os.path.exists(output_dir):
        now = time.time()
        cutoff = now - (max_age_days * 24 * 60 * 60)
        
        reports = []
        for f in os.listdir(output_dir):
            # 匹配校对报告文件
            if '校对报告' in f and f.endswith('.xlsx'):
                path = os.path.join(output_dir, f)
                try:
                    mtime = os.path.getmtime(path)
                    size = os.path.getsize(path)
                    reports.append((path, mtime, size))
                except:
                    pass
        
        # 按修改时间排序（新到旧）
        reports.sort(key=lambda x: x[1], reverse=True)
        
        # 删除超过数量限制或过期的报告
        for i, (path, mtime, size) in enumerate(reports):
            if i >= max_reports or mtime < cutoff:
                try:
                    os.remove(path)
                    cleaned['old_reports'] += 1
                    cleaned['freed_mb'] += size / (1024 * 1024)
                except:
                    pass
    
    if cleaned['temp_dirs'] > 0 or cleaned['old_reports'] > 0:
        logger.info(f"缓存清理: 临时目录 {cleaned['temp_dirs']} 个, 旧报告 {cleaned['old_reports']} 个, 释放 {cleaned['freed_mb']:.1f}MB")
    
    return cleaned


def main():
    import argparse
    parser = argparse.ArgumentParser(description='SOP-BOM 校对报告生成器 v1.4.0 (智能列检测版本)')
    parser.add_argument('bom', nargs='+', help='BOM 文件路径')
    parser.add_argument('--sop', '-s', required=True, help='SOP 文件路径')
    parser.add_argument('--output-dir', '-d', default='./output', help='输出目录')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 重新配置日志级别
    global logger
    logger = setup_logging(args.verbose)
    
    # 显示环境信息
    if args.verbose:
        print_environment_info()
    
    bom_paths = args.bom if isinstance(args.bom, list) else [args.bom]
    sop_path = args.sop
    
    # 检查文件是否存在
    for bom_path in bom_paths:
        if not os.path.exists(bom_path):
            print(f"❌ 错误: BOM 文件不存在: {bom_path}")
            return 1
    
    if not os.path.exists(sop_path):
        print(f"❌ 错误: SOP 文件不存在: {sop_path}")
        return 1
    
    try:
        all_bom_items = []
        for bom_path in bom_paths:
            print(f"解析 BOM 文件: {os.path.basename(bom_path)}")
            items = parse_bom_file(bom_path)
            all_bom_items.extend(items)
        print(f"BOM 共有 {len(all_bom_items)} 项物料")
        
        print(f"\n解析 SOP 文件: {os.path.basename(sop_path)}")
        sop_items = parse_sop_file(sop_path)
        print(f"SOP 共有 {len(sop_items)} 项物料")
        
        code_counts = Counter(item['code'] for item in sop_items)
        duplicate_count = sum(1 for code, count in code_counts.items() if count > 1)
        if duplicate_count > 0:
            print(f"SOP 中有 {duplicate_count} 个重复物料编码")
        
        result = compare_bom_sop(sop_items, all_bom_items)
        
        print("\n" + "=" * 60)
        print("## 校对结果统计\n")
        print(f"- 有差异的物料: {len(result['diffs'])} 项")
        print(f"- SOP 独有物料: {len(result['only_sop'])} 项")
        print(f"- BOM 独有物料: {len(result['only_bom'])} 项")
        print(f"- 重复物料编码: {len(result['duplicate_codes'])} 个")
        
        os.makedirs(args.output_dir, exist_ok=True)
        order_num = extract_order_number(os.path.basename(sop_path))
        output_path = os.path.join(args.output_dir, f"{order_num}_校对报告.xlsx")
        
        create_report_xlsx(result, output_path, sop_items)
        print(f"\n✅ 校对报告已生成: {output_path}")
        
        # 清理缓存
        cleanup_cache(args.output_dir, max_reports=20, max_age_days=7)
        
        return 0
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
