import sys
import os

MAX_FILE_SIZE = 10 * 1024 * 1024

def detect_engine():
    try:
        import openpyxl
        return 'openpyxl'
    except ImportError:
        pass
    try:
        import xlrd
        return 'xlrd'
    except ImportError:
        pass
    return None

def normalize_column_name(name):
    name = str(name).strip()
    name = name.replace('　', ' ').replace(' ', '')
    name = name.replace('（', '(').replace('）', ')')
    return name

def validate_file_path(file_path):
    abs_path = os.path.abspath(file_path)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    project_root = os.path.dirname(skill_dir)
    if not abs_path.startswith(project_root):
        raise ValueError("错误：文件路径超出允许范围")
    if not os.path.exists(abs_path):
        raise FileNotFoundError("错误：文件不存在")
    if os.path.isdir(abs_path):
        raise ValueError("错误：路径是目录而非文件")
    file_size = os.path.getsize(abs_path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError("错误：文件大小超过限制")
    return abs_path

def read_excel_to_text(file_path):
    engine = detect_engine()
    if engine is None:
        raise ImportError("错误：缺少必要的依赖库")
    
    import pandas as pd
    
    try:
        df = pd.read_excel(file_path, engine=engine)
    except Exception as e:
        raise RuntimeError("错误：读取文件失败")
    
    df.columns = [normalize_column_name(col) for col in df.columns]
    
    text_output = f"文件名: {os.path.basename(file_path)}\n"
    text_output += f"列数: {len(df.columns)}\n"
    text_output += f"行数: {len(df)}\n"
    text_output += f"列名: {', '.join(df.columns.tolist())}\n\n"
    
    text_output += "数据内容:\n"
    for idx, row in df.iterrows():
        row_text = f"第{idx+1}行: "
        for col in df.columns:
            val = row[col]
            if pd.isna(val):
                val = "空"
            row_text += f"{col}={val}, "
        text_output += row_text.rstrip(', ') + "\n"
    
    return text_output

def read_text_file(file_path):
    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'utf-16']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            text_output = f"文件名: {os.path.basename(file_path)}\n"
            text_output += f"文件大小: {len(content)} 字符\n\n"
            text_output += "文件内容:\n"
            text_output += content
            return text_output
        except UnicodeDecodeError:
            continue
    
    raise ValueError("错误：无法读取文件，请检查文件编码是否正确")

def read_file(file_path):
    abs_path = validate_file_path(file_path)
    ext = os.path.splitext(abs_path)[1].lower()
    
    if ext in ['.xlsx', '.xls']:
        return read_excel_to_text(abs_path)
    elif ext in ['.md', '.txt', '.json', '.csv']:
        return read_text_file(abs_path)
    else:
        raise ValueError("错误：不支持的文件格式")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python read_file.py <文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        result = read_file(file_path)
        print(result)
    except Exception as e:
        print(str(e))
        sys.exit(1)