"""
PSD → PNG 渲染器 v2.3
- 支持预渲染背景缓存（最大性能提升）
- 跨平台字体自动发现
- 精确读取 PSD 原始字体/字号/颜色/位置
"""
import sys, os, argparse
from pathlib import Path
from psd_tools import PSDImage
from PIL import Image, ImageDraw, ImageFont

from console_utils import configure_stdio

configure_stdio()


def psd_color_values_to_rgb(values):
    """Convert Photoshop engine color values to RGB.

    Photoshop text colors commonly arrive as [space, R, G, B], where the first
    item identifies the color space and is not a channel.
    """
    if not values:
        return None
    values = list(values)
    first = float(values[0])
    has_space_marker = len(values) >= 4 and 0 <= first <= 4 and first == round(first)
    channels = values[1:4] if has_space_marker else values[:3]
    if len(channels) < 3:
        return None

    rgb = []
    for value in channels[:3]:
        number = float(value)
        if number <= 1:
            number *= 255
        rgb.append(max(0, min(255, int(round(number)))))
    return tuple(rgb)


# ── 跨平台字体自动发现 ──
def find_fonts():
    # 优先扫描技能包自带字体目录
    skill_fonts_dir = Path(__file__).parent.parent / 'fonts'
    dirs = [str(skill_fonts_dir)]
    
    if sys.platform == 'win32':
        dirs += [os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Fonts'),
                 r'C:\Windows\Fonts']
    elif sys.platform == 'darwin':
        dirs += [os.path.expanduser('~/Library/Fonts'), '/System/Library/Fonts', '/Library/Fonts']
    else:
        dirs += [os.path.expanduser('~/.fonts'), '/usr/share/fonts', '/usr/local/share/fonts']
    
    fonts = []
    for d in dirs:
        if not os.path.isdir(d): continue
        for f in Path(d).rglob('*.ttf'): fonts.append(str(f))
        for f in Path(d).rglob('*.otf'): fonts.append(str(f))
    cn_kw = ['hei','song','ming','kai','yuan','fang','chinese','cjk','noto','alimama','ali','sim','msyh']
    fonts.sort(key=lambda f: min((i for i,k in enumerate(cn_kw) if k in Path(f).name.lower()), default=99))
    return fonts


# ── 智能字体匹配 ──
def match_psd_font(psd_font_name, installed_fonts):
    """
    在已安装字体中找最接近 PSD 字体的匹配。
    返回 (font_path, confidence): confidence: 'exact' | 'family' | 'similar' | None
    """
    if not psd_font_name or not installed_fonts:
        return None, None
    
    # 规范化：去空格、去连字符、小写
    def normalize(s):
        return s.lower().replace(' ', '').replace('-', '').replace('_', '')
    
    psd_norm = normalize(psd_font_name)
    
    # 1. 精确匹配（文件名包含完整字体名）
    for fp in installed_fonts:
        fn = normalize(Path(fp).stem)
        if psd_norm in fn or fn in psd_norm:
            return fp, 'exact'
    
    # 2. 族名匹配（去掉权重后缀后匹配）
    # AlimamaFangYuanTiVF-SemiBoldSquare → AlimamaFangYuanTiVF
    psd_family = psd_norm.split('vf')[0] if 'vf' in psd_norm else psd_norm
    # 去掉常见权重后缀
    for suffix in ['bold', 'regular', 'medium', 'thin', 'light', 'heavy', 'black',
                   'semibold', 'extrabold', 'italic', 'oblique', 'square', 'round']:
        if psd_family.endswith(suffix):
            psd_family = psd_family[:-len(suffix)]
    
    for fp in installed_fonts:
        fn = normalize(Path(fp).stem)
        if psd_family and len(psd_family) > 3 and psd_family in fn:
            return fp, 'family'
    
    # 3. 关键词匹配（提取字体名中的特征词）
    keywords = []
    for part in psd_norm.replace('vf', ' ').split():
        if len(part) > 2 and part not in ('ttf', 'otf', 'ttc'):
            keywords.append(part)
    
    for fp in installed_fonts:
        fn = normalize(Path(fp).stem)
        matches = sum(1 for kw in keywords if kw in fn)
        if matches >= len(keywords) * 0.5 and matches >= 1:
            return fp, 'similar'
    
    return None, None


def get_text_style(layer):
    """读取 PSD 文字层的完整样式"""
    text = layer.text.strip('\x00').strip()
    if not text: return None
    bbox = layer.bbox
    style = {
        'text': text, 'bbox': bbox,
        'w': bbox[2]-bbox[0], 'h': bbox[3]-bbox[1],
        'font_size': None, 'font_family': None,
        'fill_color': None, 'stroke_color': None,
    }
    if layer.font_names: style['font_family'] = layer.font_names[0]
    try:
        ssd = layer.engine_dict['StyleRun']['RunArray'][0]['StyleSheet']['StyleSheetData']
        fs = ssd.get('FontSize')
        if fs is not None: style['font_size'] = int(round(float(fs)))
    except: pass
    try:
        ssd = layer.engine_dict['StyleRun']['RunArray'][0]['StyleSheet']['StyleSheetData']
        fill = ssd.get('FillColor',{}).get('Values',[])
        parsed_fill = psd_color_values_to_rgb(fill)
        if parsed_fill:
            style['fill_color'] = parsed_fill
        stroke = ssd.get('StrokeColor',{}).get('Values',[])
        parsed_stroke = psd_color_values_to_rgb(stroke)
        if parsed_stroke:
            style['stroke_color'] = parsed_stroke
    except: pass
    if style['font_size'] is None: style['font_size'] = max(int(layer.height*0.75),20)
    if style['fill_color'] is None: style['fill_color'] = (255,255,255)
    return style


# ── 预渲染背景（只做一次）──
def prerender_background(psd_path):
    """合成不含文字层的底图，返回 PIL Image"""
    psd = PSDImage.open(str(psd_path))
    bg = None
    for layer in psd.descendants():
        if layer.kind == 'type': continue
        try:
            img = layer.topil().convert('RGBA')
            bg = img if bg is None else (bg.paste(img, layer.bbox[:2], img) or bg)
        except: pass
    if bg is None: bg = psd.topil().convert('RGBA')
    return bg


def render_with_background(bg_image, text_styles, font_paths, color=None,
                            font_size=None, align='center', try_match_fonts=True):
    """在预渲染背景上绘制文字"""
    image = bg_image.copy()
    draw = ImageDraw.Draw(image, 'RGBA')
    
    for s in text_styles:
        fs = font_size or s['font_size']
        
        # 智能字体选择
        font = None
        used_font = 'default'
        
        if try_match_fonts and s.get('font_family'):
            matched, conf = match_psd_font(s['font_family'], font_paths)
            if matched:
                try:
                    font = ImageFont.truetype(matched, fs)
                    used_font = f'{Path(matched).stem} ({conf})'
                except:
                    pass
        
        if font is None:
            for fp in font_paths:
                try:
                    font = ImageFont.truetype(fp, fs); break
                except:
                    continue
        
        if font is None:
            font = ImageFont.load_default()
        
        c = color or s.get('fill_color', (255, 255, 255))
        fill = c + (255,) if len(c) == 3 else c
        
        tb = draw.textbbox((0, 0), s['text'], font=font)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        cx = s['bbox'][0] + (s['w'] - tw) / 2 if align == 'center' else \
             s['bbox'][0] + s['w'] - tw if align == 'right' else s['bbox'][0]
        cy = s['bbox'][1] + (s['h'] - th) / 2
        draw.text((cx, cy), s['text'], font=font, fill=fill)
    
    return image


def render_psd_to_png(psd_path, png_path, font_paths=None, color=None,
                       font_size=None, dpi=(300,300), align='center', bg_cache=None):
    """渲染单张（可选使用缓存的背景）"""
    psd = PSDImage.open(str(psd_path))
    styles = [get_text_style(l) for l in psd.descendants() if l.kind=='type']
    styles = [s for s in styles if s]
    if not styles:
        psd.topil().convert('RGBA').save(str(png_path),'PNG',dpi=dpi)
        return
    
    bg = bg_cache if bg_cache is not None else prerender_background(psd_path)
    if font_paths is None: font_paths = []
    result = render_with_background(bg, styles, font_paths, color, font_size, align)
    png_path.parent.mkdir(parents=True,exist_ok=True)
    result.save(str(png_path),'PNG',dpi=dpi)


def show_psd_styles(psd_path, font_paths=None):
    psd = PSDImage.open(str(psd_path))
    if font_paths is None: font_paths = find_fonts()
    
    print(f'\n  {"Layer":<20} {"PSD Font":<30} {"Size":>5} {"Color":>16} {"Match":<25}')
    print(f'  {"-"*20} {"-"*30} {"-"*5} {"-"*16} {"-"*25}')
    for l in psd.descendants():
        if l.kind != 'type': continue
        s = get_text_style(l)
        if not s: continue
        fn = (s['font_family'] or '?')[:30]
        col = s['fill_color']
        cs = f'RGB({col[0]},{col[1]},{col[2]})' if col else '?'
        
        # 字体匹配结果
        match_str = ''
        if s.get('font_family') and font_paths:
            matched, conf = match_psd_font(s['font_family'], font_paths)
            if matched:
                match_str = f'{Path(matched).name} [{conf}]'
            else:
                match_str = 'NOT FOUND - use --font'
        
        print(f'  {l.name:<20} {fn:<30} {s["font_size"]:>5} {cs:>16} {match_str:<25}')
    print()


def main():
    p = argparse.ArgumentParser(description='PSD → PNG v2.3')
    p.add_argument('src_dir')
    p.add_argument('out_dir')
    p.add_argument('--font')
    p.add_argument('--color',nargs=3,type=int)
    p.add_argument('--size',type=int)
    p.add_argument('--align',choices=['left','center','right'],default='center')
    p.add_argument('--dpi',type=int,default=300)
    p.add_argument('--show-styles',action='store_true')
    a = p.parse_args()
    
    src = Path(a.src_dir)
    if a.show_styles:
        psd_files = list(src.glob('*.psd'))
        if psd_files: show_psd_styles(psd_files[0])
        elif src.is_file() and src.suffix=='.psd': show_psd_styles(src)
        else: print(f'No PSD in {src}')
        return
    
    out = Path(a.out_dir); out.mkdir(parents=True,exist_ok=True)
    psd_files = sorted(src.glob('*.psd'))
    if not psd_files: print(f'No PSD in {src}'); return
    
    fps = [a.font] if a.font else find_fonts()[:3]
    color = tuple(a.color) if a.color else None
    
    # 预渲染背景（一次）
    first = psd_files[0]
    styles = [get_text_style(l) for l in PSDImage.open(str(first)).descendants() if l.kind=='type']
    styles = [s for s in styles if s]
    if styles:
        show_psd_styles(first)
        print(f'Pre-rendering background...')
        bg_cache = prerender_background(first)
        print(f'Background cached ({first.name})')
    else:
        bg_cache = None
    
    t = len(psd_files)
    print(f'{t} PSDs -> {out}')
    for i,f in enumerate(psd_files,1):
        try:
            render_psd_to_png(f, out/f'{f.stem}.png', fps, color, a.size, (a.dpi,a.dpi), a.align, bg_cache)
        except Exception as e:
            print(f'  [{i}] {f.name} ERROR: {e}')
        if i%20==0: print(f'  {i}/{t}')
    print(f'Done!')


if __name__=='__main__':
    main()
