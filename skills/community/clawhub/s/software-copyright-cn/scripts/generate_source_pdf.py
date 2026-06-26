#!/usr/bin/env python3
"""
程序鉴别材料PDF生成器
从源代码目录生成符合软著申请要求的PDF文件。
- 连续的前30页 + 连续的后30页（不足60页则全部）
- 每页不少于50行
- 页眉包含软件名称和版本号
- 代码语法高亮（Syntax Highlighting）
- 中文支持（自动查找系统中文字体）
"""

import argparse
import os
import sys
import re
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm, cm
    from reportlab.lib.colors import HexColor, black, white, Color
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.enums import TA_LEFT
except ImportError:
    print("错误：需要安装 reportlab 库")
    print("请运行：pip install reportlab")
    sys.exit(1)

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_for_filename, get_lexer_by_name, TextLexer
    from pygments.token import Token
    from pygments.lexers import guess_lexer
except ImportError:
    print("错误：需要安装 pygments 库（用于语法高亮）")
    print("请运行：pip install pygments")
    sys.exit(1)

# ============================================================
# 配置
# ============================================================
LINES_PER_PAGE = 50
PAGE_WIDTH, PAGE_HEIGHT = A4  # 595.27, 841.89 points
MARGIN_LEFT = 20 * mm
MARGIN_RIGHT = 15 * mm
MARGIN_TOP = 25 * mm
MARGIN_BOTTOM = 20 * mm
HEADER_HEIGHT = 10 * mm
LINE_HEIGHT = 12  # points
CODE_FONT_SIZE = 8
HEADER_FONT_SIZE = 9
LINE_NUM_WIDTH = 35  # points for line number column
MAX_PAGES = 60
PAGES_EACH_SIDE = 30

# 常见源代码文件扩展名
SOURCE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.cc',
    '.h', '.hpp', '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt',
    '.kts', '.scala', '.m', '.mm', '.r', '.R', '.pl', '.pm', '.sh',
    '.bash', '.zsh', '.sql', '.html', '.htm', '.css', '.scss', '.sass',
    '.less', '.xml', '.json', '.yaml', '.yml', '.toml', '.vue', '.svelte',
    '.dart', '.lua', '.ex', '.exs', '.erl', '.hs', '.ml', '.mli',
    '.f90', '.f95', '.f03', '.asm', '.s', '.vb', '.vbs', '.pas',
    '.dpr', '.mat', '.clj', '.cljs', '.groovy', '.gradle',
}

# Pygments token 到颜色的映射
TOKEN_COLORS = {
    Token.Keyword:                HexColor('#0000FF'),      # 蓝色 - 关键字
    Token.Keyword.Constant:       HexColor('#0000FF'),
    Token.Keyword.Declaration:    HexColor('#0000FF'),
    Token.Keyword.Namespace:      HexColor('#0000FF'),
    Token.Keyword.Pseudo:         HexColor('#0000FF'),
    Token.Keyword.Reserved:       HexColor('#0000FF'),
    Token.Keyword.Type:           HexColor('#2B91AF'),      # 青蓝 - 类型关键字
    Token.Name.Builtin:           HexColor('#2B91AF'),
    Token.Name.Class:             HexColor('#2B91AF'),
    Token.Name.Decorator:         HexColor('#795E26'),
    Token.Name.Function:          HexColor('#795E26'),      # 棕色 - 函数名
    Token.Name.Function.Magic:    HexColor('#795E26'),
    Token.Literal.String:         HexColor('#A31515'),      # 红棕 - 字符串
    Token.Literal.String.Affix:   HexColor('#A31515'),
    Token.Literal.String.Backtick:HexColor('#A31515'),
    Token.Literal.String.Char:    HexColor('#A31515'),
    Token.Literal.String.Doc:     HexColor('#A31515'),
    Token.Literal.String.Double:  HexColor('#A31515'),
    Token.Literal.String.Escape:  HexColor('#A31515'),
    Token.Literal.String.Heredoc: HexColor('#A31515'),
    Token.Literal.String.Interpol:HexColor('#A31515'),
    Token.Literal.String.Other:   HexColor('#A31515'),
    Token.Literal.String.Regex:   HexColor('#A31515'),
    Token.Literal.String.Single:  HexColor('#A31515'),
    Token.Literal.String.Symbol:  HexColor('#A31515'),
    Token.Literal.Number:         HexColor('#098658'),      # 绿色 - 数字
    Token.Literal.Number.Bin:     HexColor('#098658'),
    Token.Literal.Number.Float:   HexColor('#098658'),
    Token.Literal.Number.Hex:     HexColor('#098658'),
    Token.Literal.Number.Integer: HexColor('#098658'),
    Token.Literal.Number.Oct:     HexColor('#098658'),
    Token.Comment:                HexColor('#008000'),      # 绿色 - 注释
    Token.Comment.Hashbang:       HexColor('#008000'),
    Token.Comment.Multiline:      HexColor('#008000'),
    Token.Comment.Single:         HexColor('#008000'),
    Token.Comment.Special:        HexColor('#008000'),
    Token.Comment.Preproc:        HexColor('#808080'),
    Token.Operator:               HexColor('#000000'),
    Token.Punctuation:            HexColor('#000000'),
}

# ============================================================
# 中文字体查找
# ============================================================
CHINESE_FONT_PATHS = [
    # macOS
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    # Linux
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    # Windows
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/simhei.ttf",
]

MONOSPACE_FONT_PATHS = [
    # macOS
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/SFMono-Regular.otf",
    "/System/Library/Fonts/Monaco.ttf",
    # Linux
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
    # Windows
    "C:/Windows/Fonts/consola.ttf",
    "C:/Windows/Fonts/cour.ttf",
]


def find_font(font_paths, font_name):
    """查找并注册字体，返回注册的字体名称。"""
    for path in font_paths:
        if os.path.exists(path):
            try:
                if path.endswith('.ttc'):
                    from reportlab.pdfbase.ttfonts import TTFont
                    pdfmetrics.registerFont(TTFont(font_name, path, subfontIndex=0))
                else:
                    pdfmetrics.registerFont(TTFont(font_name, path))
                return font_name
            except Exception:
                continue
    return None


def setup_fonts():
    """初始化字体，返回 (中文字体名, 等宽字体名)。"""
    cn_font = find_font(CHINESE_FONT_PATHS, "ChineseFont")
    mono_font = find_font(MONOSPACE_FONT_PATHS, "MonoFont")

    if not cn_font:
        print("警告：未找到中文字体，中文可能无法正常显示")
        cn_font = "Helvetica"
    if not mono_font:
        print("警告：未找到等宽字体，使用 Courier")
        mono_font = "Courier"

    return cn_font, mono_font


# ============================================================
# 源代码收集
# ============================================================
def collect_source_files(src_dir, extensions=None):
    """递归收集源代码文件，按路径排序。"""
    if extensions is None:
        extensions = SOURCE_EXTENSIONS
    files = []
    src_path = Path(src_dir)
    for f in sorted(src_path.rglob('*')):
        if f.is_file() and f.suffix.lower() in extensions:
            # 跳过常见的非源代码目录
            parts = f.parts
            skip_dirs = {'node_modules', '.git', '__pycache__', '.venv', 'venv',
                         'dist', 'build', '.next', '.nuxt', 'vendor', '.idea',
                         '.vscode', 'target', 'bin', 'obj', '.gradle',
                         'scripts', '软著申请', '软著申请材料', '.agents'}
            if not any(d in parts for d in skip_dirs):
                files.append(f)
    return files


def read_file_safe(filepath):
    """安全读取文件，尝试多种编码。"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'latin-1']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    return None


def get_lexer_for_file(filepath):
    """获取文件对应的 Pygments lexer。"""
    try:
        return get_lexer_for_filename(str(filepath), stripall=False)
    except Exception:
        return TextLexer()


def tokenize_line(line, lexer):
    """将一行代码进行语法分析，返回 [(color, text), ...] 列表。"""
    tokens = []
    try:
        from pygments import lex
        for token_type, token_value in lex(line, lexer):
            color = black
            # 查找匹配的颜色，支持 token 类型的父类匹配
            t = token_type
            while t:
                if t in TOKEN_COLORS:
                    color = TOKEN_COLORS[t]
                    break
                t = t.parent
            tokens.append((color, token_value))
    except Exception:
        tokens.append((black, line))
    return tokens


# ============================================================
# PDF 生成
# ============================================================
def draw_header(c, page_num, total_pages, software_name, version, cn_font):
    """绘制页眉。"""
    y = PAGE_HEIGHT - MARGIN_TOP + 3 * mm
    c.setFont(cn_font, HEADER_FONT_SIZE)
    c.setFillColor(HexColor('#333333'))

    # 左侧：软件名称 + 版本
    header_text = f"{software_name} {version}"
    c.drawString(MARGIN_LEFT, y, header_text)

    # 右侧：页码
    page_text = f"第 {page_num} 页 / 共 {total_pages} 页"
    c.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, y, page_text)

    # 分隔线
    c.setStrokeColor(HexColor('#CCCCCC'))
    c.setLineWidth(0.5)
    line_y = y - 3 * mm
    c.line(MARGIN_LEFT, line_y, PAGE_WIDTH - MARGIN_RIGHT, line_y)


def draw_code_line(c, x, y, line_num, line_text, lexer, mono_font, cn_font):
    """绘制一行带行号和语法高亮的代码。"""
    # 行号
    c.setFont(mono_font, CODE_FONT_SIZE)
    c.setFillColor(HexColor('#999999'))
    c.drawRightString(x + LINE_NUM_WIDTH - 5, y, str(line_num))

    # 分隔符
    c.setStrokeColor(HexColor('#DDDDDD'))
    c.setLineWidth(0.3)
    c.line(x + LINE_NUM_WIDTH, y + LINE_HEIGHT - 2, x + LINE_NUM_WIDTH, y - 2)

    # 代码内容（语法高亮）
    code_x = x + LINE_NUM_WIDTH + 5
    max_width = PAGE_WIDTH - MARGIN_RIGHT - code_x

    tokens = tokenize_line(line_text, lexer)
    current_x = code_x

    for color, text in tokens:
        if text == '\n':
            continue
        # 将 tab 转为 4 空格
        text = text.replace('\t', '    ')
        if not text:
            continue

        c.setFillColor(color)
        # 判断是否包含中文字符来选择字体
        has_cjk = any('\u4e00' <= ch <= '\u9fff' or
                      '\u3000' <= ch <= '\u303f' or
                      '\uff00' <= ch <= '\uffef' for ch in text)
        if has_cjk:
            c.setFont(cn_font, CODE_FONT_SIZE)
        else:
            c.setFont(mono_font, CODE_FONT_SIZE)

        text_width = c.stringWidth(text)
        if current_x + text_width > PAGE_WIDTH - MARGIN_RIGHT:
            # 超出右边界，截断
            remaining_width = PAGE_WIDTH - MARGIN_RIGHT - current_x
            if remaining_width > 10:
                c.drawString(current_x, y, text)
            break
        c.drawString(current_x, y, text)
        current_x += text_width


def generate_pdf(all_lines, file_markers, output_path, software_name, version,
                 cn_font, mono_font, lexers, lines_per_page=LINES_PER_PAGE):
    """
    生成最终 PDF。
    all_lines: [(global_line_num, text, file_index), ...]
    file_markers: [(file_index, filepath), ...]
    lexers: {file_index: lexer}
    """
    total_lines = len(all_lines)
    total_pages_all = (total_lines + lines_per_page - 1) // lines_per_page

    # 确定要输出的页面
    if total_pages_all <= MAX_PAGES:
        pages_to_render = list(range(total_pages_all))
    else:
        first_pages = list(range(PAGES_EACH_SIDE))
        last_pages = list(range(total_pages_all - PAGES_EACH_SIDE, total_pages_all))
        pages_to_render = first_pages + last_pages

    total_output_pages = len(pages_to_render)

    c = canvas.Canvas(str(output_path), pagesize=A4)
    c.setTitle(f"{software_name} {version} 程序鉴别材料")
    c.setAuthor(software_name)

    output_page_num = 0
    for page_idx in pages_to_render:
        output_page_num += 1
        start_line = page_idx * lines_per_page
        end_line = min(start_line + lines_per_page, total_lines)
        page_lines = all_lines[start_line:end_line]

        # 页眉
        draw_header(c, output_page_num, total_output_pages, software_name, version, cn_font)

        # 代码区域起始 Y
        content_top = PAGE_HEIGHT - MARGIN_TOP - HEADER_HEIGHT
        y = content_top

        for i, (global_num, text, file_idx) in enumerate(page_lines):
            # 如果是文件的第一行，显示文件路径标记
            draw_code_line(c, MARGIN_LEFT, y, global_num, text,
                           lexers.get(file_idx, TextLexer()), mono_font, cn_font)
            y -= LINE_HEIGHT

        c.showPage()

    c.save()
    return total_pages_all, total_output_pages


def main():
    parser = argparse.ArgumentParser(
        description='软著程序鉴别材料PDF生成器（带语法高亮）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python generate_source_pdf.py /path/to/src --name "智慧管理系统" --version "V1.0"
  python generate_source_pdf.py ./src --name "数据平台" --version "V2.0" -o 程序鉴别材料.pdf
  python generate_source_pdf.py ./src --name "测试软件" --version "V1.0" --ext .py .js .ts
        """
    )
    parser.add_argument('source_dir', help='源代码目录路径')
    parser.add_argument('--name', '-n', required=True, help='软件全称')
    parser.add_argument('--version', '-v', required=True, help='版本号（如 V1.0）')
    parser.add_argument('--output', '-o', default=None,
                        help='输出PDF路径（默认：<软件名>_程序鉴别材料.pdf）')
    parser.add_argument('--ext', nargs='+', default=None,
                        help='额外的源代码文件扩展名（如 .vue .svelte）')
    parser.add_argument('--lines-per-page', type=int, default=LINES_PER_PAGE,
                        help=f'每页行数（默认 {LINES_PER_PAGE}，不少于50）')

    args = parser.parse_args()

    if not os.path.isdir(args.source_dir):
        print(f"错误：源代码目录不存在: {args.source_dir}")
        sys.exit(1)

    lines_per_page = max(args.lines_per_page, 50)

    # 设置字体
    cn_font, mono_font = setup_fonts()

    # 收集文件
    extensions = SOURCE_EXTENSIONS.copy()
    if args.ext:
        for ext in args.ext:
            if not ext.startswith('.'):
                ext = '.' + ext
            extensions.add(ext)

    files = collect_source_files(args.source_dir, extensions)
    if not files:
        print(f"错误：在 {args.source_dir} 中未找到源代码文件")
        print(f"支持的扩展名: {', '.join(sorted(extensions))}")
        sys.exit(1)

    print(f"找到 {len(files)} 个源代码文件")

    # 读取所有文件并构建行数据
    all_lines = []  # (global_line_num, text, file_index)
    lexers = {}
    global_line = 0

    for file_idx, filepath in enumerate(files):
        content = read_file_safe(filepath)
        if content is None:
            print(f"  跳过（无法读取）: {filepath}")
            continue

        lexer = get_lexer_for_file(filepath)
        lexers[file_idx] = lexer

        rel_path = filepath.relative_to(Path(args.source_dir))
        lines = content.splitlines()

        for line in lines:
            global_line += 1
            all_lines.append((global_line, line, file_idx))

        # 文件之间加空行
        global_line += 1
        all_lines.append((global_line, "", file_idx))

    total_lines = len(all_lines)
    total_pages = (total_lines + lines_per_page - 1) // lines_per_page

    print(f"总行数: {total_lines}")
    print(f"总页数: {total_pages}")

    if total_pages <= MAX_PAGES:
        print(f"源程序不足{MAX_PAGES}页，将提交全部 {total_pages} 页")
    else:
        print(f"源程序超过{MAX_PAGES}页，将提交前{PAGES_EACH_SIDE}页 + 后{PAGES_EACH_SIDE}页")

    # 输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        safe_name = re.sub(r'[^\w\u4e00-\u9fff]', '_', args.name)
        output_path = Path(f"{safe_name}_程序鉴别材料.pdf")

    # 生成 PDF
    print(f"正在生成 PDF: {output_path}")
    total_all, total_out = generate_pdf(
        all_lines, [(i, f) for i, f in enumerate(files)],
        output_path, args.name, args.version,
        cn_font, mono_font, lexers, lines_per_page
    )

    print(f"生成完成！")
    print(f"  输出文件: {output_path}")
    print(f"  源程序总页数: {total_all}")
    print(f"  PDF实际页数: {total_out}")


if __name__ == '__main__':
    main()
