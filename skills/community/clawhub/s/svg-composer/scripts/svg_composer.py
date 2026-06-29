"""
SVG 拼接工具
支持横向/纵向拼接多个 SVG 符号
支持两套字符集：
  1. @fortawesome/fontawesome-free（默认）：0-9, A-Z
  2. @tscircuit/alphabet：0-9, A-Z, a-z

功能特点：
- 黑白双色支持：仅支持黑色(#000000)和白色(#FFFFFF)
- 横向/纵向拼接
- 四种拼接模式：仅顺序、全排列、笛卡尔积、限制长度

用法：
  from svg_composer import compose_text
  # 默认使用 FA 字符集，黑色
  svg = compose_text("A10", fill='black')
  # 白色
  svg = compose_text("HELLO", fill='white')

  # 四种拼接模式
  from svg_composer import compose_permutations, compose_combinations
  # 全排列（ABC -> ABC, ACB, BAC, BCA, CAB, CBA）
  svg_list = compose_permutations("ABC")
  # 笛卡尔积（重复组合，AAA, AAB...）
  svg_list = compose_combinations("AB", length=3)
"""

import os
import re
import math
import itertools
from svgpathtools import parse_path

# 导入内置字符集
from charset import SVG_ALPHABET, GLYPH_WIDTH_RATIO, ALL_SUPPORTED
from charset_fa import FA_ALPHABET, FA_ALL_SUPPORTED


# ==================== 常量定义 ====================

# 支持的颜色列表
SUPPORTED_COLORS = {
    'black': '#000000',
    'white': '#FFFFFF',
}

# 默认颜色
DEFAULT_FILL = 'black'


# ==================== 基础工具函数 ====================

def extract_path_from_svg(filepath):
    """从 SVG 文件中提取第一个 <path> 的 d 属性值"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'<path\s+[^>]*d="([^"]+)"', content)
    if not match:
        raise ValueError(f"未找到路径: {filepath}")
    return match.group(1)


def get_path_bbox(d_str):
    """计算路径的包围盒 (xmin, xmax, ymin, ymax)"""
    path = parse_path(d_str)
    bbox = path.bbox()
    return bbox


def load_symbols(symbol_dir):
    """
    从文件夹加载所有符号，返回 {symbol_char: {'d': path_d, 'bbox': bbox}}

    Args:
        symbol_dir: 符号文件夹路径（包含 .svg 文件）

    Returns:
        dict: {symbol_name: {'d': path_d, 'bbox': (xmin,xmax,ymin,ymax)}}
    """
    symbols = {}
    if not os.path.isdir(symbol_dir):
        raise ValueError(f"符号文件夹不存在: {symbol_dir}")

    for filename in os.listdir(symbol_dir):
        if filename.endswith(".svg"):
            symbol = filename[:-4]  # 去掉 .svg 扩展名
            filepath = os.path.join(symbol_dir, filename)
            try:
                d = extract_path_from_svg(filepath)
                bbox = get_path_bbox(d)
                symbols[symbol] = {'d': d, 'bbox': bbox}
            except Exception as e:
                print(f"警告：加载 {filename} 失败: {e}")

    if not symbols:
        raise ValueError(f"符号文件夹中没有找到有效的 .svg 文件: {symbol_dir}")

    return symbols


def element_transform(d, bbox, target_scale, target_pos, canvas_height=None):
    """
    根据原始路径 d 和包围盒 bbox，生成缩放平移后的 path 元素字符串。

    适用于两种字符集：
    - @tscircuit/alphabet：坐标 [0,1]，Y=0 在底部
    - Font Awesome：坐标为 viewBox（Y=0 在顶部，标准 SVG）

    Args:
        d: 原始 path 的 d 属性值
        bbox: 包围盒 (xmin, xmax, ymin, ymax)
        target_scale: 最终缩放系数
        target_pos: (tx, ty) 将原始包围盒的 (xmin, ymin) 映射到的目标点

    Returns:
        str: SVG <path> 元素字符串
    """
    xmin, xmax, ymin, ymax = bbox
    s = target_scale
    tx = target_pos[0] - xmin * s
    ty = target_pos[1] - ymin * s
    transform = f"matrix({s},0,0,{s},{tx},{ty})"
    return f'<path d="{d}" transform="{transform}"/>'


# ==================== 内置字符集支持 ====================

# 缓存：避免每次调用都重新计算 bbox
_CHARSET_CACHE = None

def get_charset():
    """
    获取内置字符集，使用 svgpathtools 计算每个字符的真实 bbox。

    @tscircuit/alphabet 字符路径并不填满整个 [0,1]x[0,1] 方框，
    必须计算真实包围盒才能正确缩放和对齐。

    Returns:
        dict: {char: {'d': path_d, 'bbox': (xmin, xmax, ymin, ymax)}}
    """
    global _CHARSET_CACHE
    if _CHARSET_CACHE is not None:
        return _CHARSET_CACHE

    charset = {}
    for char, d in SVG_ALPHABET.items():
        if char == " " or not d.strip():
            # 空格给一个合理宽度
            charset[char] = {'d': d, 'bbox': (0, 0.5, 0, 1)}
        else:
            try:
                path = parse_path(d)
                xmin, xmax, ymin, ymax = path.bbox()
                charset[char] = {'d': d, 'bbox': (xmin, xmax, ymin, ymax)}
            except Exception:
                # 解析失败时跳过
                pass

    _CHARSET_CACHE = charset
    return charset


def check_chars_supported(text, charset='fa'):
    """
    检查字符串中的所有字符是否被支持。

    Args:
        text: 要检查的字符串
        charset: 'fa'（默认）或 'tscircuit'

    Returns:
        tuple: (全部支持, 不支持的字符列表)
    """
    if charset == 'fa':
        alphabet = FA_ALPHABET
        all_supported = FA_ALL_SUPPORTED
    else:
        alphabet = SVG_ALPHABET
        all_supported = ALL_SUPPORTED

    unsupported = []
    for ch in text:
        if ch not in alphabet:
            unsupported.append(ch)
    return (len(unsupported) == 0, unsupported, all_supported)


def normalize_text(text, charset='fa'):
    """
    规范化输入文本：小写自动转大写（仅 FA 字符集）

    Args:
        text: 输入文本
        charset: 'fa' 或 'tscircuit'

    Returns:
        str: 规范化后的文本
    """
    if charset == 'fa':
        # FA 只支持大写，小写自动转大写
        return text.upper()
    return text


def normalize_fill(fill):
    """
    规范化颜色值：仅支持黑色和白色

    Args:
        fill: 颜色名称或十六进制值

    Returns:
        str: 规范化后的十六进制颜色值

    Raises:
        ValueError: 不支持的颜色
    """
    if fill is None:
        return SUPPORTED_COLORS[DEFAULT_FILL]

    fill_lower = str(fill).lower().strip()

    # 直接是支持的名称
    if fill_lower in SUPPORTED_COLORS:
        return SUPPORTED_COLORS[fill_lower]

    # 十六进制格式
    if fill_lower.startswith('#'):
        hex_val = fill_lower.upper()
        if hex_val == '#000000':
            return '#000000'
        elif hex_val == '#FFFFFF':
            return '#FFFFFF'
        elif hex_val == '#000' or hex_val == '#FFF':
            return '#000000' if hex_val == '#000' else '#FFFFFF'

    raise ValueError(f"不支持的颜色 '{fill}'。仅支持: black(#000000), white(#FFFFFF)")


# ==================== 布局拼接（横向/纵向）====================

# @tscircuit/alphabet 标准参数（来自官方 JS）
GLYPH_ADVANCE_RATIO = 0.692052   # 每个字符的固定 advance 宽度（相对于字形高度）
STROKE_WIDTH_RATIO = 0.09         # 笔画粗细 = 字高 × 9%


def layout_elements(elements, direction='horizontal', canvas_size=(640, 640),
                   margin=0, align='center', fill="black",
                   font_height_ratio=0.8):
    """
    将多个 SVG 路径元素横向或纵向拼接成一个 SVG。
    
    宽度计算逻辑参考用户示例代码：用 bbox 宽度直接计算。

    Args:
        elements: 列表，每个元素为 {'d': path_d, 'bbox': (xmin,xmax,ymin,ymax)}
        direction: 'horizontal'（横向）或 'vertical'（纵向）
        canvas_size: (width, height) 画布尺寸
        margin: 元素间距（像素）
        align: 'center', 'start', 'end'（仅横向有效）
        fill: 填充颜色，仅支持 'black' 或 'white'
        font_height_ratio: 字体高度占画布的比例

    Returns:
        str: SVG 字符串
    """
    # 参数校验
    direction = direction.lower()
    if direction not in ('horizontal', 'vertical'):
        raise ValueError(f"direction 必须是 'horizontal' 或 'vertical'，实际: {direction}")

    # 规范化颜色
    fill_color = normalize_fill(fill)

    n = len(elements)
    if n == 0:
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_size[0]} {canvas_size[1]}"></svg>'

    canvas_w, canvas_h = canvas_size

    if direction == 'horizontal':
        # ===== 横向拼接（参考用户示例代码） =====
        target_h = canvas_h * font_height_ratio

        # 第一遍：计算每个元素的 scale 和宽度
        scales = []
        widths = []
        for elem in elements:
            xmin, xmax, ymin, ymax = elem['bbox']
            h = ymax - ymin
            if h == 0:
                raise ValueError("元素高度为 0，无法缩放")
            scale = target_h / h
            scales.append(scale)
            w = (xmax - xmin) * scale  # 直接用 bbox 宽度
            widths.append(w)

        total_width = sum(widths) + margin * (n - 1)

        # 整体缩放（防止溢出）
        if total_width > canvas_w:
            scale_total = canvas_w / total_width
        else:
            scale_total = 1

        # 计算最终高度和偏移
        final_height = target_h * scale_total
        y_offset = (canvas_h - final_height) / 2

        # 计算起始位置
        if total_width * scale_total < canvas_w:
            if align == 'center':
                x_start = (canvas_w - total_width * scale_total) / 2
            elif align == 'end':
                x_start = canvas_w - total_width * scale_total
            else:
                x_start = 0
        else:
            x_start = 0

        # 计算每个符号的最终左边界
        L = []
        current_L = x_start
        for i in range(n):
            L.append(current_L)
            current_L += widths[i] * scale_total + margin * scale_total

        # 生成 path 元素
        path_elems = []
        for i, elem in enumerate(elements):
            xmin, xmax, ymin, ymax = elem['bbox']
            s = scales[i] * scale_total
            tx = L[i] - xmin * s
            ty = y_offset - ymin * s
            path_elems.append(f'<path fill="{fill_color}" d="{elem["d"]}" transform="matrix({s},0,0,{s},{tx},{ty})"/>')

    else:
        # ===== 纵向拼接 =====
        # 与横向逻辑一致：统一高度，按高度缩放，字符上下排列
        target_h = canvas_h * font_height_ratio

        # 第一遍：计算每个元素的 scale 和宽度（按统一高度缩放）
        # 注意：这里与横向逻辑完全一致
        scales = []
        widths = []
        for elem in elements:
            xmin, xmax, ymin, ymax = elem['bbox']
            h = ymax - ymin
            if h == 0:
                raise ValueError("元素高度为 0，无法缩放")
            scale = target_h / h
            scales.append(scale)
            w = (xmax - xmin) * scale
            widths.append(w)

        # 找最大宽度（用于横向居中）
        max_width = max(widths) if widths else 0

        # 总高度 = 各元素高度之和（统一高度，所以都是 target_h）
        total_height = target_h * n + margin * (n - 1)

        # 整体缩放（防止溢出）- 与横向一致
        # 纵向拼接时，缩放后字符会变小，这是纵向排列的正常特性
        if total_height > canvas_h:
            scale_total = canvas_h / total_height
        else:
            scale_total = 1

        # 计算最终宽度和横向偏移（居中）
        final_width = max_width * scale_total
        x_offset = (canvas_w - final_width) / 2

        # 计算最终高度
        final_height = target_h * scale_total

        # 计算起始位置（居中）
        if total_height * scale_total < canvas_h:
            y_start = (canvas_h - total_height * scale_total) / 2
        else:
            y_start = 0

        # 计算每个符号的最终上边界（纵向排列的关键！）
        T = []
        current_T = y_start
        for i in range(n):
            T.append(current_T)
            current_T += final_height + margin * scale_total

        # 生成 path 元素
        path_elems = []
        for i, elem in enumerate(elements):
            xmin, xmax, ymin, ymax = elem['bbox']
            s = scales[i] * scale_total
            # x位置：居中（所有字符 x 相同）
            tx = x_offset - xmin * s
            # y位置：纵向排列（每个字符在不同 Y）
            ty = T[i] - ymin * s
            path_elems.append(f'<path fill="{fill_color}" d="{elem["d"]}" transform="matrix({s},0,0,{s},{tx},{ty})"/>')

    # 许可证注释（Font Awesome Free 使用 CC BY 4.0）
    license_comment = '<!-- Icons provided by Font Awesome Free (CC BY 4.0) https://fontawesome.com/license/free -->'

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}">\n' + \
          license_comment + '\n' + \
          '\n'.join(path_elems) + '\n</svg>'
    return svg


def compose_text(text, direction='horizontal', canvas_size=(640, 640),
                margin=0, align='center', fill="black",
                font_height_ratio=0.8, charset='fa'):
    """
    使用内置字符集拼接文本为 SVG。

    Args:
        text: 要拼接的文本，如 "AB12" 或 "HELLO"
        direction: 'horizontal'（横向）或 'vertical'（纵向）
        canvas_size: (width, height) 画布尺寸
        margin: 字符间距（像素）
        align: 'center', 'start', 'end' 整体对齐方式
        fill: 填充颜色，仅支持 'black'(#000000) 和 'white'(#FFFFFF)
        font_height_ratio: 字体高度占画布的比例（默认 0.8）
        charset: 'fa'（默认，0-9/A-Z）或 'tscircuit'（0-9/A-Z/a-z）

    Returns:
        str: SVG 字符串

    Raises:
        ValueError: 如果文本包含不支持的字符或颜色
    """
    # 规范化输入
    text = normalize_text(text, charset)
    fill_color = normalize_fill(fill)

    # 检查字符支持
    supported, unsupported, all_supported = check_chars_supported(text, charset)
    if not supported:
        raise ValueError(f"不支持的字符: {set(unsupported)}。仅支持: {all_supported}")

    if charset == 'fa':
        charset_data = FA_ALPHABET
        elements = []
        for ch in text:
            c = charset_data[ch]
            elements.append({
                'd': c['d'],
                'bbox': (0, c['vb_w'], 0, c['vb_h']),
                'advance_ratio': c['advance_ratio'],
                'vb_w': c['vb_w'],
                'vb_h': c['vb_h'],
            })
    else:
        charset_data = get_charset()
        elements = [{'d': charset_data[ch]['d'], 'bbox': charset_data[ch]['bbox'],
                     'advance_ratio': GLYPH_ADVANCE_RATIO}
                    for ch in text]

    return layout_elements(elements, direction, canvas_size, margin, align, fill_color,
                          font_height_ratio=font_height_ratio)


# ==================== 四种拼接模式 ====================

def compose_sequence(text, direction='horizontal', canvas_size=(640, 640),
                    margin=0, align='center', fill="black",
                    font_height_ratio=0.8, charset='fa'):
    """
    【模式1】仅拼接输入顺序文字
    输入 "ABC" -> 输出 SVG("ABC")

    Args:
        text: 输入字符（如 "ABC"）
        其他参数同 compose_text

    Returns:
        str: SVG 字符串
    """
    return compose_text(text, direction, canvas_size, margin, align, fill,
                       font_height_ratio, charset)


def compose_permutations(text, direction='horizontal', canvas_size=(640, 640),
                         margin=0, align='center', fill="black",
                         font_height_ratio=0.8, charset='fa'):
    """
    【模式2】全排列（不重复组合）
    输入 "ABC" -> 输出 SVG("ABC"), SVG("ACB"), SVG("BAC"), SVG("BCA"), SVG("CAB"), SVG("CBA")

    Args:
        text: 输入字符（如 "ABC"）
        其他参数同 compose_text

    Returns:
        list: SVG 字符串列表
    """
    # 规范化输入
    text = normalize_text(text, charset)

    # 去重并保持顺序
    unique_chars = []
    seen = set()
    for ch in text:
        if ch not in seen:
            seen.add(ch)
            unique_chars.append(ch)

    if len(unique_chars) == 0:
        return []
    if len(unique_chars) == 1:
        return [compose_text(text, direction, canvas_size, margin, align, fill,
                             font_height_ratio, charset)]

    # 全排列
    result = []
    for perm in itertools.permutations(unique_chars):
        perm_str = ''.join(perm)
        svg = compose_text(perm_str, direction, canvas_size, margin, align, fill,
                          font_height_ratio, charset)
        result.append(svg)

    return result


def compose_combinations(text, length=None, direction='horizontal', canvas_size=(640, 640),
                         margin=0, align='center', fill="black",
                         font_height_ratio=0.8, charset='fa'):
    """
    【模式3】笛卡尔积（可重复组合/密码本模式）
    输入 "AB", length=3 -> 输出 AAA, AAB, ABA, ABB, BAA, BAB, BBA, BBB

    Args:
        text: 输入字符（如 "AB"）
        length: 输出字符串长度（默认使用输入字符数）
        其他参数同 compose_text

    Returns:
        list: SVG 字符串列表
    """
    # 规范化输入
    text = normalize_text(text, charset)

    # 去重并保持顺序
    unique_chars = []
    seen = set()
    for ch in text:
        if ch not in seen:
            seen.add(ch)
            unique_chars.append(ch)

    if len(unique_chars) == 0:
        return []

    # 默认长度
    if length is None:
        length = len(unique_chars)

    if length <= 0:
        return []

    # 笛卡尔积
    result = []
    for combo in itertools.product(unique_chars, repeat=length):
        combo_str = ''.join(combo)
        svg = compose_text(combo_str, direction, canvas_size, margin, align, fill,
                          font_height_ratio, charset)
        result.append(svg)

    return result


def compose_limited(text, limit=2, direction='horizontal', canvas_size=(640, 640),
                    margin=0, align='center', fill="black",
                    font_height_ratio=0.8, charset='fa'):
    """
    【模式4】限制长度的全排列
    输入 "ABC", limit=2 -> 输出 AB, AC, BA, BC, CA, CB

    Args:
        text: 输入字符（如 "ABC"）
        limit: 每个组合的长度（默认 2）
        其他参数同 compose_text

    Returns:
        list: SVG 字符串列表
    """
    # 规范化输入
    text = normalize_text(text, charset)

    # 去重并保持顺序
    unique_chars = []
    seen = set()
    for ch in text:
        if ch not in seen:
            seen.add(ch)
            unique_chars.append(ch)

    if len(unique_chars) == 0:
        return []

    if limit <= 0:
        return []

    # 限制长度不能超过唯一字符数
    actual_limit = min(limit, len(unique_chars))

    # 生成所有长度的排列
    result = []
    for length in range(1, actual_limit + 1):
        for perm in itertools.permutations(unique_chars, length):
            perm_str = ''.join(perm)
            svg = compose_text(perm_str, direction, canvas_size, margin, align, fill,
                              font_height_ratio, charset)
            result.append(svg)

    return result


# ==================== 批量生成 ====================

def batch_compose(symbol_dir, output_dir, n=2, allow_repeat=True, margin=0, fill="black"):
    """
    批量生成符号组合的 SVG 文件。

    Args:
        symbol_dir: 符号文件夹路径
        output_dir: 输出文件夹路径
        n: 组合长度
        allow_repeat: 是否允许重复符号
        margin: 符号间距
        fill: 填充颜色，仅支持 'black' 或 'white'
    """
    os.makedirs(output_dir, exist_ok=True)

    symbols_dict = load_symbols(symbol_dir)
    if not symbols_dict:
        raise ValueError("符号文件夹中没有找到任何 .svg 文件")

    symbols = list(symbols_dict.keys())
    print(f"找到符号: {symbols}")

    if allow_repeat:
        comb_iter = itertools.product(symbols, repeat=n)
    else:
        comb_iter = itertools.permutations(symbols, n)

    combinations = [''.join(combo) for combo in comb_iter]
    if not combinations:
        print(f"警告：当 n={n} 且不允许重复时，没有有效组合。")
        return

    print(f"将生成 {len(combinations)} 个组合: {combinations}")

    fill_color = normalize_fill(fill)

    for target in combinations:
        print(f"生成 {target}.svg")
        elements = [symbols_dict[ch] for ch in target]
        svg = layout_elements(elements, direction='horizontal', canvas_size=(640, 640),
                              margin=margin, align='center', fill=fill_color)
        with open(os.path.join(output_dir, f"{target}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)

    print("所有文件生成完毕。")


def batch_text_compose(output_dir, chars=None, direction='horizontal',
                       canvas_size=(640, 640), margin=20, fill="black",
                       font_height_ratio=0.8, charset='fa'):
    """
    使用内置字符集批量生成文本 SVG。

    Args:
        output_dir: 输出文件夹路径
        chars: 要生成的字符列表
        direction: 'horizontal' 或 'vertical'
        canvas_size: (width, height) 画布尺寸
        margin: 字符间距
        fill: 填充颜色，仅支持 'black' 或 'white'
        font_height_ratio: 字体高度比例
        charset: 'fa' 或 'tscircuit'
    """
    os.makedirs(output_dir, exist_ok=True)

    if chars is None:
        if charset == 'fa':
            chars = list(FA_ALL_SUPPORTED)
        else:
            chars = list(ALL_SUPPORTED)

    fill_color = normalize_fill(fill)

    print(f"将生成 {len(chars)} 个字符 SVG (charset={charset})")

    for ch in chars:
        supported, _, _ = check_chars_supported(ch, charset)
        if not supported:
            print(f"跳过不支持的字符: {ch}")
            continue

        print(f"生成 {ch}.svg")
        svg = compose_text(ch, direction=direction, canvas_size=canvas_size,
                          margin=margin, fill=fill_color, font_height_ratio=font_height_ratio,
                          charset=charset)

        safe_name = ch.replace('/', '_slash').replace('\\', '_backslash')
        safe_name = safe_name.replace('"', '_quote').replace("'", '_apos')
        safe_name = safe_name.replace('*', '_star').replace('?', '_question')
        safe_name = safe_name.replace('[', '_bracket').replace(']', '_bracket_r')
        safe_name = safe_name.replace(':', '_colon')

        with open(os.path.join(output_dir, f"{safe_name}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)

    print("所有文件生成完毕。")


def batch_mode_compose(output_dir, text, mode='permutations', limit=2,
                       direction='horizontal', canvas_size=(640, 640),
                       margin=0, align='center', fill='black',
                       font_height_ratio=0.8, charset='fa'):
    """
    批量生成模式组合 SVG 文件。

    Args:
        output_dir: 输出文件夹路径
        text: 输入字符（如 "ABC"）
        mode: 模式
            - 'sequence': 仅顺序（模式1）
            - 'permutations': 全排列（模式2，默认）
            - 'combinations': 笛卡尔积（模式3）
            - 'limited': 限制长度（模式4）
        limit: 模式3的长度或模式4的限制（默认2）
        其他参数同 compose_text

    Returns:
        list: 生成的 (文件名, SVG内容) 元组列表
    """
    os.makedirs(output_dir, exist_ok=True)

    fill_color = normalize_fill(fill)

    if mode == 'sequence':
        svg_list = [compose_text(text, direction, canvas_size, margin, align, fill_color,
                                  font_height_ratio, charset)]
    elif mode == 'permutations':
        svg_list = compose_permutations(text, direction, canvas_size, margin, align,
                                        fill_color, font_height_ratio, charset)
    elif mode == 'combinations':
        svg_list = compose_combinations(text, length=limit, direction=direction,
                                        canvas_size=canvas_size, margin=margin, align=align,
                                        fill=fill_color, font_height_ratio=font_height_ratio,
                                        charset=charset)
    elif mode == 'limited':
        svg_list = compose_limited(text, limit=limit, direction=direction,
                                   canvas_size=canvas_size, margin=margin, align=align,
                                   fill=fill_color, font_height_ratio=font_height_ratio,
                                   charset=charset)
    else:
        raise ValueError(f"不支持的模式 '{mode}'。支持的模式: sequence, permutations, combinations, limited")

    result = []
    for i, svg in enumerate(svg_list):
        if mode == 'sequence':
            filename = f"{normalize_text(text, charset)}.svg"
        else:
            # 从 SVG 中提取文本（简化方式）
            chars_found = []
            for ch in normalize_text(text, charset):
                if ch not in chars_found:
                    chars_found.append(ch)
            # 尝试从 SVG 内容提取实际拼接的字符
            # 默认使用索引命名
            filename = f"combo_{i+1:04d}.svg"

        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg)
        result.append((filename, svg))

    print(f"已生成 {len(svg_list)} 个 SVG 文件到 {output_dir}")
    return result


# ==================== 导出公共 API ====================

__all__ = [
    # 工具函数
    'extract_path_from_svg',
    'get_path_bbox',
    'load_symbols',
    'element_transform',
    'get_charset',
    'normalize_text',
    'normalize_fill',
    # 核心函数
    'compose_text',
    'layout_elements',
    'check_chars_supported',
    # 四种拼接模式
    'compose_sequence',       # 模式1：仅顺序
    'compose_permutations',   # 模式2：全排列
    'compose_combinations',    # 模式3：笛卡尔积
    'compose_limited',        # 模式4：限制长度
    # 批量生成
    'batch_compose',
    'batch_text_compose',
    'batch_mode_compose',
    'batch_mode_compose_with_preview',  # 带预览的批量生成
    # 预览生成
    'generate_preview_html',
    # 兼容别名
    'compose_number',   # 兼容函数，与 compose_text 等效
    # 字符集常量
    'SVG_ALPHABET',
    'FA_ALPHABET',
    'ALL_SUPPORTED',
    'FA_ALL_SUPPORTED',
    # 颜色常量
    'SUPPORTED_COLORS',
    'DEFAULT_FILL',
    # @tscircuit/alphabet 标准参数
    'GLYPH_ADVANCE_RATIO',
    'STROKE_WIDTH_RATIO',
]


def generate_preview_html(output_dir, svg_list=None, text=None, direction='horizontal',
                          fill='black', font_height_ratio=0.8):
    """
    生成预览 HTML 页面，包含可点击超链接。

    Args:
        output_dir: 输出文件夹路径（SVG 文件存放位置）
        svg_list: SVG 内容列表（每个元素为 (名称, svg字符串)）
        text: 文本内容（用于标题）
        direction: 'horizontal' 或 'vertical'
        fill: 填充颜色
        font_height_ratio: 字体高度比例

    Returns:
        str: 预览 HTML 文件路径
    """
    os.makedirs(output_dir, exist_ok=True)

    # 如果没有提供 svg_list，从 text 和 direction 生成
    if svg_list is None and text:
        svg_h = compose_text(text, direction='horizontal', fill=fill,
                            font_height_ratio=font_height_ratio)
        svg_v = compose_text(text, direction='vertical', fill=fill,
                            font_height_ratio=font_height_ratio)
        svg_list = [
            ('horizontal', f"{text}_horizontal.svg", svg_h),
            ('vertical', f"{text}_vertical.svg", svg_v),
        ]
    elif svg_list is None:
        svg_list = []

    # 保存 SVG 文件
    saved_files = []
    for label, filename, svg_content in svg_list:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        saved_files.append((label, filename, filepath))

    # 获取文件夹路径
    folder_path = output_dir.replace('\\', '/')

    # 生成 HTML
    title = f"{text} SVG 预览" if text else "SVG 预览"
    direction_label = "横向" if direction == 'horizontal' else "纵向"

    # 构建 SVG 预览项 HTML
    preview_items_html = ""
    for label, filename, _ in saved_files:
        svg_path = os.path.join(output_dir, filename)
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        preview_items_html += f'''
        <div class="preview-item">
            <h3>{'横向' if label == 'horizontal' else '纵向'}</h3>
            <div class="svg-wrapper">
                {svg_content}
            </div>
        </div>
        '''

    # 构建下载和链接 HTML
    links_html = ""
    for label, filename, filepath in saved_files:
        file_url = filepath.replace('\\', '/')
        links_html += f'''
        <div class="link-item">
            <a href="{filename}" download="{filename}">下载 {filename}</a>
        </div>
        '''
        links_html += f'''
        <div class="link-item">
            <a href="file:///{file_url}" target="_blank">打开文件: {filename}</a>
        </div>
        '''

    html_content = f'''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            color: white;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .links-section {{
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }}
        .links-section h3 {{
            margin-top: 0;
            color: #4fc3f7;
        }}
        .link-item {{
            margin: 10px 0;
            word-break: break-all;
        }}
        .link-item a {{
            color: #81d4fa;
            text-decoration: none;
            padding: 8px 16px;
            background: rgba(79, 195, 247, 0.2);
            border-radius: 6px;
            display: inline-block;
            transition: background 0.3s;
        }}
        .link-item a:hover {{
            background: rgba(79, 195, 247, 0.4);
        }}
        .preview-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 40px;
            justify-content: center;
        }}
        .preview-item {{
            background: rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
        }}
        .preview-item h3 {{
            margin: 0 0 15px 0;
            color: #fff;
        }}
        .svg-wrapper {{
            background: repeating-conic-gradient(#808080 0% 25%, #606060 0% 50%) 50% / 20px 20px;
            border-radius: 8px;
            padding: 10px;
            display: inline-block;
        }}
        .svg-wrapper svg {{
            display: block;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>

    <div class="links-section">
        <h3>📎 文件下载链接</h3>
        {links_html}
        <hr style="border-color: rgba(255,255,255,0.2); margin: 20px 0;">
        <h3>📁 文件夹路径（可直接打开）</h3>
        <div class="link-item">
            <a href="file:///{folder_path}/" target="_blank">打开文件夹</a>
        </div>
    </div>

    <div class="preview-container">
        {preview_items_html}
    </div>
</body>
</html>'''

    # 保存 HTML
    html_filename = f"{text}_preview.html" if text else "preview.html"
    html_filename = html_filename.replace(' ', '_')
    html_filepath = os.path.join(output_dir, html_filename)
    with open(html_filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return html_filepath


def batch_mode_compose_with_preview(output_dir, text, mode='permutations', limit=2,
                                    direction='horizontal', canvas_size=(640, 640),
                                    margin=0, align='center', fill='black',
                                    font_height_ratio=0.8, charset='fa',
                                    generate_preview=True):
    """
    批量生成模式组合 SVG 文件，并生成预览 HTML。

    Args:
        output_dir: 输出文件夹路径
        text: 输入字符（如 "ABC"）
        mode: 模式（同 batch_mode_compose）
        limit: 长度限制（同 batch_mode_compose）
        其他参数同 compose_text
        generate_preview: 是否生成预览 HTML（默认 True）

    Returns:
        tuple: (生成的SVG列表, 预览HTML路径)
    """
    svg_list = batch_mode_compose(output_dir, text, mode, limit, direction,
                                  canvas_size, margin, align, fill,
                                  font_height_ratio, charset)

    preview_path = None
    if generate_preview and svg_list:
        preview_path = generate_preview_html(output_dir, svg_list, text, direction,
                                           fill, font_height_ratio)

    return svg_list, preview_path


# ==================== 兼容别名 ====================

def compose_number(target, symbol_files, fill="black", margin=0):
    """
    兼容函数别名：使用外部 SVG 符号文件组合字符串。

    等效于:
        symbols = load_symbols(symbol_dir)
        elements = [symbols[ch] for ch in target]
        layout_elements(elements, margin=margin, fill=fill)

    Args:
        target: 目标字符串，如 "A10"
        symbol_files: 字典，{字符: SVG文件路径}
        fill: 填充颜色，仅支持 'black' 或 'white'
        margin: 符号间间距（像素）

    Returns:
        str: SVG 字符串
    """
    fill_color = normalize_fill(fill)
    elements = []
    for ch in target:
        svg_file = symbol_files[ch]
        d = extract_path_from_svg(svg_file)
        bbox = get_path_bbox(d)
        elements.append({'d': d, 'bbox': bbox})
    return layout_elements(elements, direction='horizontal', canvas_size=(640, 640),
                          margin=margin, align='center', fill=fill_color)


if __name__ == "__main__":
    # 示例用法
    import sys

    if len(sys.argv) > 1:
        # 命令行模式
        text = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else "output.svg"
        fill = sys.argv[3] if len(sys.argv) > 3 else "black"

        svg = compose_text(text, fill=fill, font_height_ratio=0.85)
        with open(output, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"已生成: {output}")
    else:
        # 默认示例
        print("SVG Composer - 内置字符集版本")
        print(f"支持字符: {FA_ALL_SUPPORTED}")
        print(f"支持颜色: {list(SUPPORTED_COLORS.keys())}")
        print()
        print("四种拼接模式示例：")
        print("1. compose_sequence('ABC') - 仅拼接顺序")
        print("2. compose_permutations('ABC') - 全排列")
        print("3. compose_combinations('AB', length=3) - 笛卡尔积")
        print("4. compose_limited('ABC', limit=2) - 限制长度")
        print()

        # 示例 1: 直接拼接文本（黑色）
        text = "HELLO2026"
        svg = compose_text(text, fill="black", font_height_ratio=0.85)
        with open("hello2026_black.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"示例1: 生成 {text} (黑色).svg")

        # 示例 2: 白色
        svg2 = compose_text(text, fill="white", font_height_ratio=0.85)
        with open("hello2026_white.svg", "w", encoding="utf-8") as f:
            f.write(svg2)
        print(f"示例2: 生成 {text} (白色).svg")

        # 示例 3: 模式2全排列
        print("\n示例3: 全排列 ABC")
        perm_svgs = compose_permutations("ABC", fill="black")
        print(f"  生成 {len(perm_svgs)} 个排列")
        for i, svg in enumerate(perm_svgs):
            with open(f"perm_{i+1}.svg", "w", encoding="utf-8") as f:
                f.write(svg)
            print(f"    排列{i+1}.svg")
