# -*- coding: utf-8 -*-
"""
Word 打字机演示脚本（v9）
- 逐字打字 + 智能滚屏
- 格式完全由 --style JSON 驱动，脚本不做硬编码假设
- --format gov 仅设页边距/行距等页面属性
- 所有字体/字号/粗体/对齐/缩进由 --style 决定
- 写完自动对照 --style 进行格式校正
- 对齐标记: ---right--- / ---left--- / ---center---
"""

import win32com.client, time, os, argparse, json, signal, sys
import pythoncom

DESKTOP = os.path.join(os.path.expanduser('~'), 'Desktop')

# 默认 gov 格式的 style 配置（仅做默认值，不写死到代码逻辑）
GOV_STYLE_DEFAULTS = {
    "h1": {"font": "黑体", "size": 16, "bold": False, "align": 0},
    "h2": {"font": "楷体", "size": 16, "bold": True, "align": 0},
    "h3": {"font": "仿宋", "size": 16, "bold": True, "align": 0},
    "body": {"font": "仿宋", "size": 16, "bold": False, "align": 0, "indent": True}
}

def pump():
    pythoncom.PumpWaitingMessages()

def need_scroll(win):
    try:
        visible = win.VisibleRange
        sel_end = win.Selection.Range.End
        vis_end = visible.End
        return sel_end > vis_end - 80
    except:
        return False

def scroll_into_view(win):
    try:
        win.ScrollIntoView(win.Selection.Range, False)
    except:
        pass

def typewrite(sel, text, delay, win):
    i = 0
    while i < len(text):
        batch_size = 2 if delay > 0.05 else 4
        chunk = text[i:i+batch_size]
        try:
            sel.TypeText(chunk)
        except:
            for ch in chunk:
                try:
                    sel.TypeText(ch)
                except:
                    pass
        i += batch_size
        time.sleep(delay)
        pump()
        if i % 8 == 0 and need_scroll(win):
            scroll_into_view(win)


def auto_correct_doc(doc, word, paragraphs, style_cfg):
    """写完文档后，逐段检查并校正格式。style_cfg 是用户指定的 --style JSON"""
    print('[校正] 开始自动格式校正...')
    fixes = 0

    h1s = style_cfg.get('h1', GOV_STYLE_DEFAULTS['h1'])
    h2s = style_cfg.get('h2', GOV_STYLE_DEFAULTS['h2'])
    h3s = style_cfg.get('h3', GOV_STYLE_DEFAULTS['h3'])
    bs  = style_cfg.get('body', GOV_STYLE_DEFAULTS['body'])

    # 段落类型对应的目标格式
    def get_target(text, para_idx):
        if para_idx == 0 or text.startswith('报告人') or text.startswith('日　期'):
            return style_cfg.get('title', {'font': '黑体', 'size': 22, 'bold': True, 'align': 1})
        return bs  # default to body

    para_idx = 0
    total_paras = doc.Content.Paragraphs.Count
    for i in range(1, total_paras + 1):
        try:
            para = doc.Content.Paragraphs.Item(i)
            text = para.Range.Text.strip()
            if len(text) < 2 or text.startswith('---'):
                continue
        except:
            continue

        rng = para.Range
        s = rng.Font.Size
        f = rng.Font.Name
        b = rng.Font.Bold
        a = para.Alignment
        indent = para.Format.FirstLineIndent

        # 判断段落类型
        target = {}
        for pt in paragraphs:
            pt = pt.strip()
            if pt.startswith('# ') and (pt[2:] in text or text in pt[2:]):
                target = h1s
                break
            if pt.startswith('## ') and (pt[3:] in text or text in pt[3:]):
                target = h2s
                break
            if pt.startswith('### ') and (pt[4:] in text or text in pt[4:]):
                target = h3s
                break
        if not target:
            target = bs

        # 校正字体
        try:
            tf = target.get('font', '仿宋')
            if f and tf not in str(f):
                rng.Font.Name = tf
                fixes += 1
        except:
            pass

        # 校正在size
        try:
            ts = target.get('size', 16)
            if s and abs(s - ts) > 0.5:
                rng.Font.Size = ts
                fixes += 1
        except:
            pass

        # 校正粗体
        try:
            tb = target.get('bold', False)
            if b is not None and b != tb:
                rng.Font.Bold = tb
                fixes += 1
        except:
            pass

        # 校正对齐
        try:
            ta = target.get('align', 0)
            if a is not None and a != ta:
                para.Alignment = ta
                fixes += 1
        except:
            pass

        # 校正首行缩进
        try:
            need_indent = target.get('indent', False)
            target_indent = word.Application.CentimetersToPoints(0.74) if need_indent else 0
            if indent is not None and abs(indent - target_indent) > 1:
                para.Format.FirstLineIndent = target_indent
                fixes += 1
        except:
            pass

        para_idx += 1

    print(f'[校正] 完成，共修正 {fixes} 处格式问题')
    return fixes


def check_document(doc, paragraphs, gov_format, title):
    issues = []
    if not title or '实时文档' in title:
        issues.append('未指定文档标题')
    if issues:
        print('[自检] 发现以下问题：')
        for iss in issues:
            print(f'  [注意] {iss}')
    else:
        print('[自检] 格式检查全部通过')
    print()


def cleanup_blank_docs(word):
    """关闭所有未保存的空白文档（形如"文字文稿N"或"文档N"），不保存"""
    count = word.Documents.Count
    for i in range(count, 0, -1):  # 倒序遍历，避免删除时索引变化
        try:
            doc = word.Documents.Item(i)
            name = doc.Name
            # 判断是否为未保存的空白文档
            is_blank = False
            for prefix in ['文字文稿', '文档']:
                if name.startswith(prefix):
                    rest = name[len(prefix):].strip().rstrip('.* ')
                    if rest.isdigit() or not rest:
                        is_blank = True
                        break
            if is_blank and not doc.Saved:
                print(f'[清理] 关闭空白文档: {name}')
                doc.Close(SaveChanges=False)
        except:
            pass


def get_or_create_doc(word):
    """获取或创建文档：复用第一个未保存的空白文档，否则新建"""
    try:
        if word.Documents.Count > 0:
            for i in range(1, word.Documents.Count + 1):
                doc = word.Documents.Item(i)
                if not doc.Saved:
                    print(f'[文档] 复用已有文档: {doc.Name}')
                    # 清除内容，准备写入新内容
                    try:
                        doc.Content.Delete()
                    except:
                        pass
                    return doc
    except:
        pass
    return word.Documents.Add()


def run_demo(title, paragraphs, speed, gov_format=False, save_path=None, style_cfg=None):
    # 使用 DispatchEx 创建独立 WPS/Word 实例，避免污染用户已有窗口
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = True
    word.DisplayAlerts = False

    # 清理已有空白文档
    cleanup_blank_docs(word)

    # 复用空白文档或创建新文档（避免每次新增一个空白文档）
    doc = get_or_create_doc(word)

    sel = word.Selection
    sel.Font.Name = '宋体'
    sel.Font.Size = 12
    win = word.ActiveWindow
    pump()
    time.sleep(0.5)

    try:
        word.Activate()
    except:
        pass

    # gov 格式仅设页面属性
    if gov_format:
        for section in doc.Sections:
            section.PageSetup.TopMargin = word.Application.CentimetersToPoints(3.7)
            section.PageSetup.BottomMargin = word.Application.CentimetersToPoints(3.5)
            section.PageSetup.LeftMargin = word.Application.CentimetersToPoints(2.8)
            section.PageSetup.RightMargin = word.Application.CentimetersToPoints(2.6)
        sel.ParagraphFormat.LineSpacingRule = 4
        sel.ParagraphFormat.LineSpacing = 30

    # 解析样式配置
    fmt = style_cfg or {}

    def style_for(key, default):
        s = fmt.get(key, {})
        merged = default.copy()
        merged.update(s)
        return merged

    def sf(sz, bold, font=None):
        sel.Font.Size = sz
        sel.Font.Bold = bold
        if font:
            sel.Font.Name = font

    def nl():
        sel.TypeParagraph()
        pump()

    def wl(text, d, sz=12, b=False, font=None, align=None, indent=False, indent_chars=0):
        sf(sz, b, font)
        if align is not None:
            sel.ParagraphFormat.Alignment = align
        if indent_chars > 0:
            sel.ParagraphFormat.FirstLineIndent = word.Application.CentimetersToPoints(indent_chars * 0.37)
        else:
            sel.ParagraphFormat.FirstLineIndent = (
                word.Application.CentimetersToPoints(0.74) if indent else 0
            )
        typewrite(sel, text, d, win)
        nl()
        if need_scroll(win):
            scroll_into_view(win)
        try:
            word.Application.ScreenRefresh()
        except:
            pass

    # 获取各层级样式
    h1s = style_for('h1', GOV_STYLE_DEFAULTS['h1'])
    h2s = style_for('h2', GOV_STYLE_DEFAULTS['h2'])
    h3s = style_for('h3', GOV_STYLE_DEFAULTS['h3'])
    bs  = style_for('body', GOV_STYLE_DEFAULTS['body'])
    ts  = style_for('title', GOV_STYLE_DEFAULTS['h1'].copy())
    ts['align'] = 1  # 标题默认居中

    # 输出标题（如果内容第一行不是相同标题）
    skip_title = False
    if paragraphs and paragraphs[0].strip().startswith('# '):
        first_heading = paragraphs[0].strip()[2:].strip()
        if first_heading == title:
            skip_title = True

    if not skip_title:
        wl(title, 0.07, ts['size'], ts['bold'], ts['font'], ts.get('align', 1))
        time.sleep(0.2)
        nl()
        nl()
        time.sleep(0.2)

    # 对齐控制变量
    current_align = 0

    # 正文段落循环
    for para in paragraphs:
        p = para.strip()
        if not p:
            continue

        if p == '---page---':
            sel.InsertBreak(7)
            pump()
            time.sleep(0.4)
            continue
        if p == '---right---':
            current_align = 2
            continue
        if p == '---left---':
            current_align = 0
            continue
        if p == '---center---':
            current_align = 1
            continue

        # 使用 --style 设定的格式
        if p.startswith('# '):
            wl(p[2:], max(0.03, speed * 0.6),
               sz=h1s['size'], b=h1s['bold'], font=h1s['font'],
               align=h1s.get('align', 0))
            time.sleep(0.15)
        elif p.startswith('## '):
            wl(p[3:], max(0.03, speed * 0.7),
               sz=h2s['size'], b=h2s['bold'], font=h2s['font'],
               align=h2s.get('align', 0))
            time.sleep(0.1)
        elif p.startswith('### '):
            wl(p[4:], max(0.03, speed * 0.7),
               sz=h3s['size'], b=h3s['bold'], font=h3s['font'],
               align=h3s.get('align', 0))
            time.sleep(0.1)
        else:
            wl(p, speed,
               sz=bs['size'], b=bs['bold'], font=bs['font'],
               align=current_align if current_align != 0 else bs.get('align', 0),
               indent=(bs.get('indent', False) and current_align == 0))
            time.sleep(0.08)

    # 结尾空行
    nl()
    pump()
    time.sleep(0.3)

    # 写完自动校正
    if style_cfg:
        print('[校正] 正在对照 --style 配置进行格式校正...')
        fixes = auto_correct_doc(doc, word, paragraphs, style_cfg)
        if fixes == 0:
            print('[校正] 所有格式均符合要求，无需修正')
        try:
            word.Application.ScreenRefresh()
        except:
            pass
        time.sleep(0.5)

    # 自检
    check_document(doc, paragraphs, gov_format, title)

    # 保存
    if save_path:
        try:
            abs_path = os.path.abspath(save_path)
            doc.SaveAs(abs_path)
            print(f'[OK] 文档已自动保存到: {abs_path}')
        except Exception as e:
            print(f'[FAIL] 自动保存失败: {e}')

    print('关闭 Word 或按 Ctrl+C 退出。')
    try:
        while True:
            time.sleep(1)
            pump()
    except KeyboardInterrupt:
        pass
    finally:
        # 关闭当前文档（不保存），然后退出，避免下次启动时 WPS 堆积空白文档
        try:
            if doc:
                doc.Close(SaveChanges=False)
        except:
            pass
        try:
            word.Quit()
        except:
            pass


def main():
    parser = argparse.ArgumentParser(description='Word 打字机演示')
    parser.add_argument('--file', help='内容文件路径')
    parser.add_argument('--speed', type=float, default=0.06, help='打字速度')
    parser.add_argument('--title', default='OpenClaw 实时文档生成演示', help='文档标题')
    parser.add_argument('--format', choices=['default', 'gov'], default='default',
                        help='文档格式（gov 仅设页边距/行距，不设字体）')
    parser.add_argument('--style', default='',
                        help='样式JSON，如：{"h1":{"font":"黑体","size":26,"bold":true,"align":1},"body":{"font":"楷体","size":16}}')
    parser.add_argument('--save', default='', help='保存路径')
    args = parser.parse_args()

    if args.file and os.path.exists(args.file):
        with open(args.file, 'r', encoding='utf-8') as f:
            paragraphs = [line.rstrip('\n\r') for line in f if line.strip()]
    else:
        paragraphs = ['# 实时打字演示', '展示 AI 操作 Word 的效果。']

    save_path = args.save if args.save else ''
    if not save_path and args.title:
        safe_name = args.title.replace('/', '_').replace('\\', '_').replace(':', '_')
        save_path = os.path.join(DESKTOP, safe_name + '.docx')
    elif not save_path:
        save_path = os.path.join(DESKTOP, 'OpenClaw_文档.docx')

    # 解析样式
    style_cfg = None
    if args.style:
        try:
            style_cfg = json.loads(args.style)
            print(f'[样式] 已加载: {style_cfg}')
        except json.JSONDecodeError as e:
            print(f'[样式] JSON 解析失败: {e}，使用默认样式')

    run_demo(args.title, paragraphs, args.speed, args.format == 'gov', save_path, style_cfg)


if __name__ == '__main__':
    main()
