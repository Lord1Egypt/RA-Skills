"""
PSD 文本图层直接修改工具
============================================================
直接修改 PSD 二进制文件中 Txt TEXT 描述符的文本内容。

原理：
  PSD 的文本图层通过 "Txt TEXT" 标记 + 4字节字符数 + UTF-16-BE 编码
  存储文本。本工具定位标记并替换为等长或更短的文本。

用法：
  # 按图层名替换
  python psd_text_editor.py 门票.psd output.psd "名字=张三" "赛区=北京" "学校=清华"

  # 在 Python 中调用
  from psd_text_editor import edit_psd_by_layer_map
  edit_psd_by_layer_map(Path("in.psd"), Path("out.psd"), {"名字": "张三"})

限制：
  - 新文本不能比原文本长（字节数）
  - 如果新文本更短，用 null 填充，不影响渲染
============================================================
"""

import struct
from pathlib import Path
from typing import List, Tuple

from console_utils import configure_stdio

configure_stdio()


# ============================================================
# 查找 PSD 中的 Txt TEXT 字段
# ============================================================

def find_text_markers(data: bytes) -> List[Tuple[int, int, str]]:
    """
    在 PSD 二进制中查找所有 Txt TEXT 描述符。
    
    PSD 描述符格式:
      "Txt TEXT" (8 bytes) + 4 bytes char_count (big-endian)
      + (char_count * 2) bytes UTF-16-BE text (含尾部 null)
    
    返回: [(offset, char_count, text), ...]
    """
    results = []
    marker = b'Txt TEXT'
    pos = 0
    
    while True:
        idx = data.find(marker, pos)
        if idx < 0:
            break
        
        cnt_off = idx + 8
        if cnt_off + 4 > len(data):
            pos = idx + 1; continue
        
        char_count = struct.unpack('>I', data[cnt_off:cnt_off + 4])[0]
        if char_count > 5000 or char_count <= 0:
            pos = idx + 1; continue
        
        text_start = cnt_off + 4
        text_end = text_start + char_count * 2
        if text_end > len(data):
            pos = idx + 1; continue
        
        text_bytes = data[text_start:text_end]
        try:
            text = text_bytes.decode('utf-16-be')
        except UnicodeDecodeError:
            pos = idx + 1; continue
        
        results.append((idx, char_count, text))
        pos = text_end
    
    return results


# ============================================================
# 修改 PSD 文本
# ============================================================

def patch_psd_text(
    input_path: Path,
    output_path: Path,
    replacements: dict,
) -> int:
    """
    修改 PSD 文件中的文本。支持任意长度替换。
    
    策略：保持 Txt TEXT 的字符计数不变，替换文本内容后用 null 填充剩余空间。
    这样后续的 PSD 结构字节完全不受影响。
    
    注意：psd-tools 按 char_count 去读文本，但由于 UTF-16 中 U+0000 是终止符，
    解析时 null 填充部分不会被当作有效文本。
    
    Args:
        input_path: 输入 PSD 路径
        output_path: 输出 PSD 路径
        replacements: {原始文本: 新文本}
    
    Returns:
        成功替换的数量
    """
    with open(input_path, 'rb') as f:
        data = bytearray(f.read())
    
    markers = find_text_markers(bytes(data))
    print(f"[分析] 找到 {len(markers)} 个 Txt TEXT 字段")
    
    replaced = 0
    skipped = 0
    
    for old_text, new_text in replacements.items():
        old_clean = old_text.strip('\x00').strip()
        found = False
        
        for off, char_count, txt in markers:
            txt_clean = txt.strip('\x00').strip()
            if txt_clean != old_clean:
                continue
            
            cnt_off = off + 8
            text_start = cnt_off + 4
            old_byte_len = char_count * 2
            
            # 编码新文本
            new_bytes = new_text.encode('utf-16-be')
            new_byte_len = len(new_bytes)
            
            # 超出时自动截断
            if new_byte_len > old_byte_len:
                # 先尝试缩短到刚好容纳（不含 null 终止符）
                truncated = new_text
                while True:
                    test_bytes = truncated.encode('utf-16-be')
                    if len(test_bytes) <= old_byte_len:
                        break
                    truncated = truncated[:-1]
                    if not truncated:
                        break
                
                if not truncated:
                    print(f"  [跳过] '{old_clean}' -> '{new_text}': 无法截断")
                    found = True; skipped += 1; break
                
                new_bytes = truncated.encode('utf-16-be')
                print(f"  [截断] '{new_text}' -> '{truncated}' (原{len(new_text)}字→{len(truncated)}字, 以适配{old_byte_len}字节限制)")
            else:
                truncated = new_text
            
            new_byte_len = len(new_bytes)
            
            # 写入新文本
            data[text_start:text_start + new_byte_len] = new_bytes
            # null 填充剩余空间（保持 char_count 不变，保护后续结构字节）
            for i in range(text_start + new_byte_len, text_start + old_byte_len):
                data[i] = 0
            
            print(f"  [替换] '{old_clean}' -> '{truncated}' "
                  f"(保持 {char_count}c={old_byte_len}b, 写入{new_byte_len}b+null填充)")
            replaced += 1; found = True; break
        
        if not found:
            print(f"  [未找到] '{old_clean}'")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(data)
    
    skip_msg = f", 跳过 {skipped} 处" if skipped else ""
    print(f"\n[完成] 替换 {replaced} 处{skip_msg} -> {output_path}")
    return replaced


# ============================================================
# 便捷接口：按图层名替换
# ============================================================

def edit_psd_by_layer_map(
    input_psd: Path,
    output_psd: Path,
    layer_replacements: dict,
) -> int:
    """
    按图层名修改 PSD。
    
    Args:
        input_psd: 输入 PSD
        output_psd: 输出 PSD
        layer_replacements: {图层名: 新文本}
    """
    from psd_tools import PSDImage
    
    psd = PSDImage.open(str(input_psd))
    text_map = {}
    
    for layer in psd.descendants():
        if layer.kind == 'type' and layer.name in layer_replacements:
            old = layer.text.strip('\x00').strip()
            new = layer_replacements[layer.name]
            text_map[old] = new
            print(f"[映射] '{layer.name}': '{old}' -> '{new}'")
    
    return patch_psd_text(input_psd, output_psd, text_map)


# ============================================================
# 批量处理：根据 Excel 批量生成 PSD
# ============================================================

def batch_edit_psd_by_excel(
    input_psd: Path,
    output_dir: Path,
    excel_path: Path,
) -> int:
    """
    根据 Excel 批量生成修改后的 PSD。
    
    Args:
        input_psd: PSD 模板
        output_dir: 输出目录
        excel_path: Excel 数据文件
    
    Returns:
        生成的 PSD 数量
    """
    import pandas as pd
    from psd_tools import PSDImage
    
    df = pd.read_excel(excel_path)
    df = df.dropna(how='all')
    
    psd = PSDImage.open(str(input_psd))
    layers = [(l.name, l.text.strip('\x00').strip())
              for l in psd.descendants() if l.kind == 'type']
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    count = 0
    for idx, (_, row) in enumerate(df.iterrows(), start=1):
        version = row.iloc[0] if pd.notna(row.iloc[0]) else idx
        text_map = {}
        skip = False
        
        for col_idx, (layer_name, original) in enumerate(layers, start=1):
            if col_idx >= len(row):
                break
            val = row.iloc[col_idx]
            if pd.isna(val):
                skip = True; break
            text_map[original] = str(val)
        
        if skip or not text_map:
            continue
        
        out = output_dir / f"版本_{version}.psd"
        r = patch_psd_text(input_psd, out, text_map)
        if r > 0:
            print(f"  [{idx}] -> 版本_{version}.psd\n")
            count += 1
    
    return count


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output = Path(sys.argv[2])
    
    replacements = {}
    for arg in sys.argv[3:]:
        if '=' in arg:
            k, v = arg.split('=', 1)
            replacements[k] = v
    
    if replacements:
        edit_psd_by_layer_map(input_file, output, replacements)
    else:
        print("用法: python psd_text_editor.py in.psd out.psd 名字=张三 赛区=北京 ...")
        sys.exit(1)
