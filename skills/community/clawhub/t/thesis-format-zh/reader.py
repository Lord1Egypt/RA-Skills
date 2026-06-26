#!/usr/bin/env python3
"""
模板格式提取器 — 从参考模板 docx 提取精确格式化规范

与 reader.py --classify 的区别:
  reader.py:   通用分类器，对任意docx做统计归并（Counter.most_common）
  template_reader: 模板专用，区分「范例段落」「占位空段」「格式说明文字」
                 从多种来源提取规则 → 输出可执行规范JSON

用法:
  python3 template_reader.py 模板.docx [-o rules.json] [--verbose]

输出 JSON 结构:
{
  "meta": { "template": "...", "school": "自动检测", ... },
  "theme": { "major_ea": "", "major_latin": "", ... },
  "doc_defaults": { "pPr": {}, "rPr": {} },
  "page": { "margins": {...}, "columns": ... },
  "rules": [
    {
      "id": "body",
      "label": "正文",
      "description": "...",
      "selector": { "role": "body", "style": null, "pattern": "..." },
      "pPr": { ... },
      "rPr": { ... },
      "source_trace": { ... },
      "confidence": 0.95,
      "exemplar_count": 3,
      "instruction_text": "..."
    },
    ...
  ]
}
"""
import zipfile, json, sys, os, re
from collections import defaultdict, Counter
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

# ── 复用 reader.py 的 StyleResolver ──
# （直接嵌入，避免循环依赖）

class StyleResolver:
    """解析样式继承链 + 文档默认值 + 主题字体 + source_trace"""

    def __init__(self, zipfile_obj):
        self.z = zipfile_obj
        self.p_styles = {}
        self.c_styles = {}
        self.doc_defaults_pPr = {}
        self.doc_defaults_rPr = {}
        self.theme_major_ea = ''
        self.theme_major_latin = ''
        self.theme_minor_ea = ''
        self.theme_minor_latin = ''
        self._load_styles()
        self._load_theme()

    def _load_styles(self):
        if 'word/styles.xml' not in self.z.namelist():
            return
        root = etree.fromstring(self.z.read('word/styles.xml'))
        defaults = root.find(f'{{{W}}}docDefaults')
        if defaults is not None:
            rPrDefault = defaults.find(f'{{{W}}}rPrDefault')
            if rPrDefault is not None:
                self.doc_defaults_rPr = self._extract_rPr_attrs(rPrDefault.find(f'{{{W}}}rPr'))
            pPrDefault = defaults.find(f'{{{W}}}pPrDefault')
            if pPrDefault is not None:
                self.doc_defaults_pPr = self._extract_pPr_attrs(pPrDefault.find(f'{{{W}}}pPr'))

        for style in root.findall(f'{{{W}}}style'):
            sid = style.get(f'{{{W}}}styleId', '')
            name_el = style.find(f'{{{W}}}name')
            name = name_el.get(f'{{{W}}}val', '') if name_el is not None else ''
            basedOn = style.find(f'{{{W}}}basedOn')
            basedOn_val = basedOn.get(f'{{{W}}}val', '') if basedOn is not None else ''
            stype = style.get(f'{{{W}}}type', 'paragraph')
            pPr = style.find(f'{{{W}}}pPr')
            rPr = style.find(f'{{{W}}}rPr')

            if stype == 'paragraph':
                self.p_styles[sid] = {
                    'name': name, 'basedOn': basedOn_val,
                    'pPr': self._extract_pPr_attrs(pPr),
                    'rPr': self._extract_rPr_attrs(rPr)
                }
            elif stype == 'character':
                self.c_styles[sid] = {
                    'name': name, 'basedOn': basedOn_val,
                    'rPr': self._extract_rPr_attrs(rPr)
                }

    def _load_theme(self):
        for entry in ['word/theme/theme1.xml', 'word/theme/theme.xml']:
            if entry in self.z.namelist():
                root = etree.fromstring(self.z.read(entry))
                tf = root.find(f'{{{W}}}themeElements/{{{W}}}fontScheme')
                if tf is not None:
                    self.theme_major_ea = self._get_theme_font(tf, 'majorFont', 'ea')
                    self.theme_major_latin = self._get_theme_font(tf, 'majorFont', 'latin')
                    self.theme_minor_ea = self._get_theme_font(tf, 'minorFont', 'ea')
                    self.theme_minor_latin = self._get_theme_font(tf, 'minorFont', 'latin')
                break

    def _get_theme_font(self, fontScheme, which, script):
        f = fontScheme.find(f'{{{W}}}{which}')
        if f is None: return ''
        if script == 'ea':
            ea = f.find(f'{{{W}}}ea')
            return ea.get(f'{{{W}}}typeface', '') if ea is not None else ''
        lat = f.find(f'{{{W}}}latin')
        return lat.get(f'{{{W}}}typeface', '') if lat is not None else ''

    def _extract_pPr_attrs(self, pPr):
        if pPr is None: return {}
        attrs = {}
        _TAG_MAP = {'jc': 'alignment', 'outlineLvl': 'outlineLvl'}
        for child in pPr:
            tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
            if tag == 'spacing':
                for attr in ['before', 'after', 'line', 'lineRule', 'beforeLines', 'afterLines', 'beforeAutospacing', 'afterAutospacing']:
                    v = child.get(f'{{{W}}}{attr}')
                    if v is not None:
                        attrs[f'spacing_{attr}'] = v
                # 源头归一：before↔beforeLines 双写，消除全管线别名问题
                for a, b in [('before', 'beforeLines'), ('after', 'afterLines')]:
                    ka, kb = f'spacing_{a}', f'spacing_{b}'
                    if ka in attrs: attrs[kb] = attrs[ka]
                    elif kb in attrs: attrs[ka] = attrs[kb]
            elif tag == 'ind':
                for attr in ['left', 'right', 'firstLine', 'hanging', 'firstLineChars']:
                    v = child.get(f'{{{W}}}{attr}')
                    if v is not None:
                        attrs[f'indent_{attr}'] = v
            else:
                val = child.get(f'{{{W}}}val')
                if val is not None:
                    attrs[_TAG_MAP.get(tag, tag)] = val
        return attrs

    def _extract_rPr_attrs(self, rPr):
        if rPr is None: return {}
        attrs = {}
        _TAG_MAP = {'sz': 'font_size', 'szCs': 'font_size_cs',
                    'b': 'bold', 'bCs': 'bold_cs',
                    'i': 'italic', 'iCs': 'italic_cs',
                    'u': 'underline', 'strike': 'strike',
                    'vertAlign': 'vertAlign'}
        for child in rPr:
            tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
            if tag in ('rFonts', 'rPr'):
                for attr in ['eastAsia', 'ascii', 'hAnsi', 'cs']:
                    v = child.get(f'{{{W}}}{attr}')
                    if v is not None:
                        attrs[f'font_{attr}'] = v
                continue
            val = child.get(f'{{{W}}}val')
            if val is not None:
                attrs[_TAG_MAP.get(tag, tag)] = val
        return attrs

    def resolve_paragraph(self, pPr, pStyle_id, trace=True):
        """解析段落属性继承链"""
        resolved = {}
        trace_map = {}

        # docDefaults
        for k, v in self.doc_defaults_pPr.items():
            resolved[k] = v
            if trace: trace_map[k] = 'docDefaults'

        # pStyle chain
        visited = set()
        sid = pStyle_id
        while sid and sid not in visited:
            visited.add(sid)
            if sid in self.p_styles:
                ps = self.p_styles[sid]
                for k, v in ps['pPr'].items():
                    resolved[k] = v
                    if trace: trace_map[k] = f'pStyle.{sid}'
                sid = ps.get('basedOn', '')
            else:
                break

        # direct pPr
        direct = self._extract_pPr_attrs(pPr)
        for k, v in direct.items():
            resolved[k] = v
            if trace: trace_map[k] = 'direct'

        result = dict(resolved)
        if trace:
            result['_source_trace'] = trace_map
        return result

    def resolve_run(self, rPr, rStyle_id, pStyle_id, trace=True):
        """解析文字属性继承链"""
        resolved = {}
        trace_map = {}

        # docDefaults
        for k, v in self.doc_defaults_rPr.items():
            resolved[k] = v
            if trace: trace_map[k] = 'docDefaults'

        # pStyle chain (rPr)
        visited = set()
        sid = pStyle_id
        while sid and sid not in visited:
            visited.add(sid)
            if sid in self.p_styles:
                ps = self.p_styles[sid]
                for k, v in ps['rPr'].items():
                    resolved[k] = v
                    if trace: trace_map[k] = f'pStyle.{sid}'
                sid = ps.get('basedOn', '')
            else:
                break

        # cStyle chain
        visited = set()
        sid = rStyle_id
        while sid and sid not in visited:
            visited.add(sid)
            if sid in self.c_styles:
                cs = self.c_styles[sid]
                for k, v in cs['rPr'].items():
                    resolved[k] = v
                    if trace: trace_map[k] = f'cStyle.{sid}'
                sid = cs.get('basedOn', '')
            else:
                break

        # direct rPr
        direct = self._extract_rPr_attrs(rPr)
        for k, v in direct.items():
            resolved[k] = v
            if trace: trace_map[k] = 'direct'

        # theme fallback
        for font_key in ['font_eastAsia', 'font_ascii', 'font_hAnsi', 'font_cs']:
            if font_key not in resolved:
                if font_key == 'font_eastAsia':
                    resolved[font_key] = self.theme_major_ea
                    if trace: trace_map[font_key] = 'theme.majorEA'
                elif font_key in ('font_ascii', 'font_hAnsi', 'font_cs'):
                    resolved[font_key] = self.theme_major_latin
                    if trace: trace_map[font_key] = 'theme.majorLatin'

        result = dict(resolved)
        if trace:
            result['_source_trace'] = trace_map
        return result


# ── 模板特有：段落角色识别 ──

# 正则模式：识别模板段落中的「格式说明文字」
INSTRUCTION_PATTERNS = [
    (re.compile(r'(?:采用|用|字体采用|使用)([^，。,\.]+?体)'), 'font'),
    (re.compile(r'([一二三四五六七八九小大]+)号[字]?'), 'font_size_chinese'),
    (re.compile(r'(\d+)\s*pt'), 'font_size_pt'),
    (re.compile(r'([\d.]+)倍行距'), 'line_spacing_multiple'),
    (re.compile(r'固定值?\s*(\d+)\s*pt'), 'line_spacing_fixed'),
    (re.compile(r'(?:居中|居左|居右|两端对齐)'), 'alignment'),
    (re.compile(r'(?:首行|段落首行)(?:左缩进|缩进)\s*(\d+)\s*[个]?汉?字[符]?'), 'indent_chars'),
    (re.compile(r'(?:段前|行前)\s*(?:空\s*)?(\d+)\s*pt'), 'space_before'),
    (re.compile(r'(?:段后|行后)\s*(?:空\s*)?(\d+)\s*pt'), 'space_after'),
    (re.compile(r'(?:段前|行前)\s*(?:空\s*)?(\d+)\s*磅'), 'space_before_lb'),
    (re.compile(r'(?:段后|行后)\s*(?:空\s*)?(\d+)\s*磅'), 'space_after_lb'),
    (re.compile(r'(加黑|加粗|粗体)'), 'bold'),
    (re.compile(r'(不上标|非上标|上标)'), 'superscript'),
    (re.compile(r'单倍行距'), 'line_single'),
    (re.compile(r'行距\s*(?:为|用|采用)?\s*(?:固定值?\s*)?(\d+)\s*pt'), 'line_spacing_pt'),
    (re.compile(r'(黑体|宋体|仿宋|楷体|Times New Roman|Calibri|Arial)'), 'font_name'),
]

# 模板段落类型
TEMPLATE_ROLES = {
    'cover_title': {'keywords': ['论文题目', '题目'], 'label': '封面标题', 'priority': 12},
    'cover_subtitle': {'keywords': ['Research on', 'Study on', 'Based on', 'Analysis of'], 'label': '封面英文副标题', 'priority': 11},
    'cover_info': {'keywords': ['学号', '姓名', '院系', '专业', '指导教师', '学院', '班级'], 'label': '封面信息', 'priority': 9},
    'cover_date': {'keywords': ['二〇', '年  月', '年  月  日'], 'label': '封面日期', 'priority': 8},
    'cover_signature': {'keywords': ['论文作者签名', '作者签名', '指导教师签名'], 'label': '封面签名', 'priority': 8},
    'statement_title': {'keywords': ['原创性声明', '版权使用授权'], 'label': '声明标题', 'priority': 10},
    'abstract_title': {'label': '摘要标题', 'priority': 7,
        'keywords_chinese': ['摘要'], 'keywords_english': ['ABSTRACT', 'Abstract']},
    'abstract_title_cn': {'keywords': ['摘要'], 'label': '中文摘要标题', 'exclude': ['ABSTRACT', 'Abstract'], 'priority': 8},
    'abstract_title_en': {'keywords': ['ABSTRACT', 'Abstract'], 'label': '英文摘要标题', 'exclude': ['摘要', '关键词', 'Key words'], 'priority': 8},
    'abstract_body': {'label': '摘要正文', 'priority': 3},
    'abstract_keywords': {'keywords': ['关键词', 'Key words', 'Keywords'], 'label': '关键词', 'priority': 8},
    'toc_title': {'keywords': ['目录', '目  录'], 'label': '目录标题', 'exclude': ['章', '参考文献', '附录', '结论', '致谢', '…'], 'priority': 8},
    'toc_entry': {'label': '目录条目', 'priority': 2},
    'chapter_title': {'label': '章标题(一级)', 'priority': 6},
    'section_title': {'label': '节标题(二级)', 'priority': 6},
    'subsection_title': {'label': '小节标题(三级)', 'priority': 6},
    'body': {'label': '正文', 'priority': 1},
    'table_caption': {'keywords': ['表题', '表 '], 'label': '表题', 'exclude': ['发表', '代表', '注', '示例'], 'priority': 7},
    'table_note': {'keywords': ['表注', '注'], 'label': '表注', 'priority': 5},
    'figure_caption': {'keywords': ['图题', '图 '], 'label': '图题', 'exclude': ['试图', '意图', '如图'], 'priority': 7},
    'refs_title': {'keywords': ['参考文献'], 'label': '参考文献标题', 'exclude': ['章', '…'], 'priority': 9},
    'refs_body': {'label': '参考文献条目', 'priority': 4,
        'keywords': ['参考文献'], 'exclude': ['章', '…', '标题']},
    'ack_title': {'keywords': ['致谢'], 'label': '致谢标题', 'exclude': ['章', '…'], 'priority': 8},
    'ack_body': {'label': '致谢正文', 'priority': 3},
    'declaration_body': {'label': '声明/授权正文', 'priority': 3,
        'keywords': ['声明', '独创', '授权', '学位论文', '保密', '知识产权'], 'exclude': ['章', '标题']},
    'conclusion_title': {'keywords': ['结论'], 'label': '结论标题', 'exclude': ['章', '…'], 'priority': 7},
    'appendix_title': {'keywords': ['附录'], 'label': '附录标题', 'exclude': ['章', '…', '详见', '见'], 'priority': 7},
    'header': {'keywords': ['页眉'], 'label': '页眉', 'priority': 7},
    'footer': {'keywords': ['页脚'], 'label': '页脚', 'priority': 7},
    'instruction': {'keywords': [
        '采用', '字体', '字号', '格式', '注意', '模板',
        '黑体', '宋体', '仿宋', '楷体', 'Times New Roman', 'Calibri', 'Arial',
        '小四', '三号', '四号', '五号', '小二', '小三', '小初', '一号', '二号', '小一', '初号',
        '行距', '缩进', '居中', '加粗', '加黑', '粗体', '首行', '段前', '段后',
        '磅', 'pt', '倍行距', '字符', '汉字', '页边距', '上空', '下空',
        '标题格式', '正文格式', '表题格式', '图题格式',
    ], 'label': '格式说明', 'priority': 99},
}


def extract_instructions_from_text(text):
    """从模板说明文字中提取格式指令"""
    instructions = []
    for pattern, itype in INSTRUCTION_PATTERNS:
        for m in pattern.finditer(text):
            instructions.append({'type': itype, 'value': m.group(1) if m.lastindex else m.group(0), 'span': m.span()})
    return instructions


# ── 文本内容兜底规则（不依赖样式名，纯文本特征）──
# 用于样式名不可靠（style injection 污染）或 classify_template_role 返回 None 时的二次判定
_TEXT_FALLBACK_RULES = [
    # (pattern, role, priority)
    # 优先匹配长/精确模式
    (re.compile(r'^图\s*\d+'), 'figure_caption', 10),
    (re.compile(r'^图\s*\d+[-.]\d+'), 'figure_caption', 11),
    (re.compile(r'^表\s*\d+'), 'table_caption', 10),
    (re.compile(r'^表\s*\d+[-.]\d+'), 'table_caption', 11),
    (re.compile(r'^\[\d+[\d,\-]*\]'), 'refs_body', 10),
    (re.compile(r'^\[\d+[\d,\-]*\]\s*\S'), 'refs_body', 10),
    # 圆点序号参考文献: 1. 王建国... / 14.Juhani...
    (re.compile(r'^\d+\.\s*[A-Z一-鿿]'), 'refs_body', 9),
    # TOC dots beat chapter number (目录条目 "第1章 绪论………1" 不应被判为 chapter_title)
    (re.compile(r'…{4,}'), 'toc_entry', 10),
    # Cover elements: high-priority patterns for front matter
    (re.compile(r'学\s*院\s*[：:]|专\s*业\s*[：:]|姓\s*名\s*[：:]|学\s*号\s*[：:]|指导教师'), 'cover_info', 11),
    (re.compile(r'论文作者签名|作者签名|指导教师签名'), 'cover_signature', 11),
    (re.compile(r'^[A-Z][a-z].*(?:Jurisdiction|Study|Research|Analysis|Based on)'), 'cover_subtitle', 9),
    (re.compile(r'第\s*[一二三四五六七八九十\d]+\s*章'), 'chapter_title', 9),
    # 中文章节标题紧跟汉字，没有空格：1.3.2研究方法、1.1研究背景
    (re.compile(r'^\d+\.\d+\.\d+'), 'subsection_title', 9),
    (re.compile(r'^\d+\.\d+'), 'section_title', 9),
    (re.compile(r'独创性声明|原创性声明|学位论文版权|使用授权|保密|知识产权'), 'declaration_body', 8),
    (re.compile(r'声明$|授权书$|声明书$'), 'statement_title', 8),
    (re.compile(r'参考文献$|REFERENCES$'), 'refs_title', 8),
    (re.compile(r'致谢$|致  谢$'), 'ack_title', 8),
    (re.compile(r'目录$|目  录$'), 'toc_title', 8),
    (re.compile(r'摘要$|ABSTRACT$'), 'abstract_title', 8),
    (re.compile(r'关键词|Keywords|Key words'), 'abstract_keywords', 7),
    (re.compile(r'结论$|结  论$'), 'conclusion_title', 7),
    (re.compile(r'^附录\w'), 'appendix_title', 7),
]


def _disambiguate_by_text(text, idx=0, total=0, current_role=None):
    """纯文本内容二次判定——当样式名分类失效或过于泛化时使用。

    返回更具体的 role，或原 role（无法进一步判定时）。
    专治 style injection 污染：同一样式 ID 覆盖多个语义区段。
    """
    t = text.strip()
    if not t:
        return current_role

    best_role = current_role
    best_priority = -1

    for pattern, role, priority in _TEXT_FALLBACK_RULES:
        if pattern.search(t):
            if priority > best_priority:
                best_role = role
                best_priority = priority

    # 长文本非标题 = 正文/声明/致谢体
    if best_role is None and len(t) > 50:
        # 在正文大类中二次细分
        if any(kw in t for kw in ['声明', '独创', '授权', '保密', '知识产权']):
            best_role = 'declaration_body'
        elif '致谢' in t[:20]:
            best_role = 'ack_body'

    return best_role if best_role else current_role


def classify_template_role(paragraph_text, index, total_paras, pStyle_id=None, pStyle_name='', outline_lvl=None):
    """判断模板段落的结构角色。

    优先级: outline level > style name > text keywords > number patterns > heuristics > text fallback
    大纲级别（outlineLvl）来自样式继承链，是最可靠的标题判断依据。
    """
    t = paragraph_text.strip()

    if not t:
        return None

    # ── 第零优先级：大纲级别（样式继承链提供，最可靠）──
    if outline_lvl is not None:
        try:
            ol = int(outline_lvl)
            if ol == 0:
                return 'chapter_title'
            elif ol == 1:
                return 'section_title'
            elif ol == 2:
                return 'subsection_title'
        except ValueError:
            pass

    # ── 第一优先级：样式名推断（精确，不需文本匹配）──
    if pStyle_name:
        inferred = _infer_role_from_style_name_strict(pStyle_name)
        if inferred:
            # 样式名匹配成功，但若是泛化角色(body)则做文本兜底
            if inferred == 'body':
                refined = _disambiguate_by_text(t, index, total_paras, inferred)
                if refined != 'body':
                    return refined
            # 样式推断为章标题时，需文本二次验证
            # Heading 1 样式可能被滥用：短文本、"参考文献""致谢"等非章标题需要纠正
            if inferred == 'chapter_title':
                # 先跑关键词匹配，防止 "参考文献""致谢""结论""附录" 被误判为章
                for role, info in TEMPLATE_ROLES.items():
                    if role == 'chapter_title':
                        continue
                    for kw in info.get('keywords', []):
                        if kw in t:
                            if not info.get('exclude') or all(e not in t for e in info['exclude']):
                                return role
                # 不匹配"第X章" / "Chapter N" 且短文本 → 降级为小节标题
                if not re.match(r'^第\s*[一二三四五六七八九十\d]+\s*章', t) \
                   and not re.match(r'^Chapter\s+\d+', t, re.I) \
                   and len(t) < 15:
                    return 'section_title'
            return inferred

    # ── 第二优先级：文本关键词匹配 ──
    candidates = []
    for role, info in TEMPLATE_ROLES.items():
        priority = info.get('priority', 0)
        keywords = info.get('keywords', [])
        exclude = info.get('exclude', [])

        if exclude and any(e in t for e in exclude):
            continue

        for kw in keywords:
            if kw in t:
                candidates.append((priority, role))
                break

    if candidates:
        candidates.sort(key=lambda x: -x[0])
        return candidates[0][1]

    # ── 第三优先级：目录条目 ──
    if re.search(r'…{4,}', t) or re.search(r'\.{6,}', t):
        return 'toc_entry'

    # ── 第四优先级：编号模式匹配（统一使用 heading_patterns）──
    from heading_patterns import match_heading
    h = match_heading(t)
    if h:
        return h['role']

    if re.match(r'\[\d+\]', t):
        return 'refs_body'

    # ── 第四优先级：文本内容兜底 ──
    fallback = _disambiguate_by_text(t, index, total_paras)
    if fallback:
        return fallback

    # ── 第五优先级：启发式 ──
    # 长文本：区分正文还是格式说明。正文模板段落通常有实质性论述内容，
    # 而格式说明段落布满字体/字号/行距等排版术语。
    _INSTRUCTION_KEYWORDS = [
        '采用', '字体', '字号', '格式', '注意', '模板仅供参考', '具体格式以', '模板',
        '黑体', '宋体', '仿宋', '楷体', 'Times New Roman', 'Calibri', 'Arial',
        '小四', '三号', '四号', '五号', '小二', '小三', '小初', '一号', '二号', '小一', '初号',
        '行距', '缩进', '居中', '加粗', '加黑', '粗体', '首行', '段前', '段后',
        '磅', 'pt', '倍行距', '字符', '汉字', '页边距', '上空', '下空',
        '标题格式', '正文格式', '表题格式', '图题格式', '参考文献格式',
    ]
    if len(t) > 15:
        is_instruction = any(kw in t for kw in _INSTRUCTION_KEYWORDS)
        if is_instruction:
            return 'instruction'
        if len(t) > 30:
            return 'body'

    return None


def _infer_role_from_style_name_strict(name):
    """从 Word 样式名精确推断段落角色（用于有完整样式定义的模板）"""
    name_lower = name.lower().replace(' ', '')
    
    # Heading levels (含中文别名，兼容 rebuild.py 生成的中文样式名)
    if name_lower in ('heading1', 'heading 1', '标题1', '标题1', '章标题', '一级章节'):
        return 'chapter_title'
    if name_lower in ('heading2', 'heading 2', '标题2', '标题2', '节标题', '二级章节'):
        return 'section_title'
    if name_lower in ('heading3', 'heading 3', '标题3', '标题3', '小节标题', '三级章节'):
        return 'subsection_title'
    # 其他中文别名
    if name_lower in ('正文', 'normal', 'body text', 'bodytext'):
        return 'body'

    # rebuild.py 生成的中文样式名
    _REBUILD_NAMES = {
        '中文摘要标题': 'abstract_title_cn', '英文摘要标题': 'abstract_title_en',
        '摘要正文': 'abstract_body', '英文摘要正文': 'abstract_body_en',
        '中文关键词': 'abstract_keywords', '英文关键词': 'abstract_keywords_en',
        '致谢标题': 'ack_title', '致谢正文': 'ack_body',
        '参考文献标题': 'refs_title', '参考文献条目': 'refs_body',
        '目录标题': 'toc_title', '目录条目': 'toc_entry',
        '图题': 'figure_caption', '表题': 'table_caption', '表注': 'table_note',
        '结论标题': 'conclusion_title', '附录标题': 'appendix_title',
    }
    if name_lower in _REBUILD_NAMES:
        return _REBUILD_NAMES[name_lower]

    # 各学校自定义样式名（按语义精确匹配）
    _STYLE_TO_ROLE = {
        '摘要正文': 'abstract_body',
        '关键词正文': 'abstract_keywords',
        '英文摘要正文': 'abstract_body_en',
        '英文关键词正文': 'abstract_keywords_en',
        '摘要标题': 'abstract_title_cn',
        '英文摘要标题': 'abstract_title_en',
        '关键词': 'abstract_keywords',
        '英文关键词': 'abstract_keywords_en',
        '目录标题': 'toc_title',
        '章前标题': 'statement_title',
        '声明正文': 'declaration_body',
        '授权书正文': 'declaration_body',
        '致谢标题': 'ack_title',
        '致谢正文': 'ack_body',
        '附录标题': 'appendix_title',
        '参考文献标题': 'refs_title',
        '参考文献条目': 'refs_body',
        'bodytext': 'body',
        'body text': 'body',
        'bodytextindent': 'body',
        'toc1': 'toc_entry',
        'toc2': 'toc_entry',
        'toc3': 'toc_entry',
        'toc 1': 'toc_entry',
        'toc 2': 'toc_entry',
        'toc 3': 'toc_entry',
        'subtitle': 'section_heading',
        'title': 'cover_title',
        'header': 'header',
        'footer': 'footer',
    }
    
    # Exact match
    if name in _STYLE_TO_ROLE:
        return _STYLE_TO_ROLE[name]
    # Case-insensitive
    for key, role in _STYLE_TO_ROLE.items():
        if name_lower == key.lower().replace(' ', ''):
            return role
    
    return None


def normalize_font_size(val):
    """将中文字号/磅值统一为半磅单位（1pt=2半磅）"""
    if not val:
        return None
    val = val.strip()

    # 已经是数字
    try:
        n = int(val)
        return str(n)  # 已经是半磅
    except ValueError:
        pass

    # 中文字号 → 半磅
    zh_sizes = {
        '初号': '84', '小初': '72',
        '一号': '52', '小一': '48',
        '二号': '44', '小二': '36',
        '三号': '32', '小三': '30',
        '四号': '28', '小四': '24',
        '五号': '21', '小五': '18',
        '六号': '15', '小六': '13',
    }
    for zh, half_pt in zh_sizes.items():
        if zh in val:
            return half_pt

    # pt值 → 半磅
    m = re.search(r'(\d+)\s*pt', val)
    if m:
        return str(int(m.group(1)) * 2)

    return val


class TemplateReader:
    """模板格式读取器"""

    def __init__(self, docx_path):
        self.docx_path = docx_path
        self.z = zipfile.ZipFile(docx_path, 'r')
        self.resolver = StyleResolver(self.z)
        self.paragraphs = []
        self._parse()

    def _parse(self):
        """解析所有段落"""
        doc_root = etree.fromstring(self.z.read('word/document.xml'))
        body = doc_root.find(f'{{{W}}}body')

        for i, child in enumerate(body):
            if child.tag != f'{{{W}}}p':
                continue

            texts = [t.text or '' for t in child.findall(f'.//{{{W}}}t')]
            text = ''.join(texts)

            pPr = child.find(f'{{{W}}}pPr')
            pStyle_id = None
            if pPr is not None:
                ps = pPr.find(f'{{{W}}}pStyle')
                if ps is not None:
                    pStyle_id = ps.get(f'{{{W}}}val')

            eff_pPr = self.resolver.resolve_paragraph(pPr, pStyle_id, trace=True)
            eff_rPr = {}
            first_run = child.find(f'{{{W}}}r')
            if first_run is not None:
                rPr = first_run.find(f'{{{W}}}rPr')
                rStyle_id = None
                if rPr is not None:
                    rs = rPr.find(f'{{{W}}}rStyle')
                    if rs is not None:
                        rStyle_id = rs.get(f'{{{W}}}val')
                eff_rPr = self.resolver.resolve_run(rPr, rStyle_id, pStyle_id, trace=True)

            # Get style name for style-first classification
            pStyle_name = ''
            if pStyle_id and pStyle_id in self.resolver.p_styles:
                pStyle_name = self.resolver.p_styles[pStyle_id].get('name', '')
            role = classify_template_role(text, i, 999, pStyle_id, pStyle_name)
            instructions = extract_instructions_from_text(text)

            self.paragraphs.append({
                'index': i,
                'text': text.strip(),
                'pStyle': pStyle_id,
                'role': role,
                'final_pPr': {k: v for k, v in eff_pPr.items() if k != '_source_trace'},
                'pPr_trace': eff_pPr.get('_source_trace', {}),
                'final_rPr': {k: v for k, v in eff_rPr.items() if k != '_source_trace'},
                'rPr_trace': eff_rPr.get('_source_trace', {}),
                'instructions': instructions,
                'is_empty': len(text.strip()) == 0,
                'is_instruction': len(instructions) > 0,
            })

    def extract_rules(self):
        """提取格式化规则 — 仅从有实质文本的段落提取"""
        rules = []

        # 1. 按已分类角色分组（排除空段落和格式说明）
        by_role = defaultdict(list)
        for p in self.paragraphs:
            if p['role'] and not p['is_empty'] and not p['is_instruction']:
                by_role[p['role']].append(p)

        # 2. 对每个角色提取规则
        for role, paras in sorted(by_role.items()):
            if role == 'instruction':
                continue
            if not paras:
                continue
            rule = self._build_rule(role, paras)
            if rule:
                rules.append(rule)

        # 3. 样式库独立输出，不混入 rules
        style_library = self._extract_style_rules()
        return rules, style_library

    def _build_rule(self, role, exemplars):
        """从范例段落构建单条规则"""
        role_info = TEMPLATE_ROLES.get(role, {'label': role})

        # 聚合格式化属性（取众数）
        # ⚠️ 字段名必须与 orchestrator diff_against_rules 的 pPr_keys 完全对齐
        pPr_keys = ['alignment',
                     'spacing_beforeLines', 'spacing_afterLines',
                     'spacing_line', 'spacing_lineRule',
                     'indent_firstLine', 'indent_firstLineChars',
                     'indent_left', 'indent_right', 'indent_hanging']
        rPr_keys = ['font_eastAsia', 'font_ascii', 'font_hAnsi',
                     'font_size', 'bold', 'italic', 'underline', 'vertAlign']

        pPr_spec = {}
        rPr_spec = {}
        merged_trace = {}
        all_instructions = []

        for p in exemplars:
            for k in pPr_keys:
                v = p['final_pPr'].get(k, '')
                if v:
                    pPr_spec.setdefault(k, []).append(v)
            for k in rPr_keys:
                v = p['final_rPr'].get(k, '')
                if v:
                    rPr_spec.setdefault(k, []).append(v)
            for k, v in p['pPr_trace'].items():
                merged_trace.setdefault(k, []).append(v)
            for k, v in p['rPr_trace'].items():
                merged_trace.setdefault(k, []).append(v)
            all_instructions.extend(p['instructions'])

        # 取众数（带共识阈值：少于 30% 或 <2 票的值不采纳，防止少数离群值污染规则）
        total_exemplars = len(exemplars)
        consensus_threshold = max(2, int(total_exemplars * 0.3))

        final_pPr = {}
        for k, vals in pPr_spec.items():
            winner, count = Counter(vals).most_common(1)[0]
            if count >= consensus_threshold:
                final_pPr[k] = winner
            else:
                final_pPr[k] = None  # 标记为不可靠，阻止 style fallback 回填
        final_rPr = {}
        for k, vals in rPr_spec.items():
            winner, count = Counter(vals).most_common(1)[0]
            if count >= consensus_threshold:
                final_rPr[k] = winner
            else:
                final_rPr[k] = None
        final_trace = {}
        for k, vals in merged_trace.items():
            winner, count = Counter(vals).most_common(1)[0]
            if count >= consensus_threshold:
                final_trace[k] = winner
            else:
                final_trace[k] = None

        # 从嵌入指令中提取额外规则
        inst_rules = self._parse_instruction_rules(all_instructions)
        # 指令规则覆盖自动检测的规则（指令更权威）
        for k, v in inst_rules.get('pPr', {}).items():
            final_pPr[k] = v
        for k, v in inst_rules.get('rPr', {}).items():
            final_rPr[k] = v

        # 规范化字号
        if 'font_size' in final_rPr:
            final_rPr['font_size'] = normalize_font_size(final_rPr['font_size'])

        # 检测样式ID
        style_counter = Counter(p.get('pStyle', '') for p in exemplars if p.get('pStyle'))
        dominant_style = style_counter.most_common(1)[0][0] if style_counter else None

        # ── 样式定义层补充：缺失/单例属性从 style definition 取 ──
        if dominant_style and dominant_style in self.resolver.p_styles:
            sd = self.resolver.p_styles[dominant_style]
            # pPr 补充（不覆盖已有值）
            for k, v in sd.get('pPr', {}).items():
                if k not in final_pPr:
                    final_pPr[k] = v
                    final_trace[k] = f'styleDef.{dominant_style}'
            # rPr 补充
            for k, v in sd.get('rPr', {}).items():
                if k not in final_rPr:
                    final_rPr[k] = v
                    final_trace[k] = f'styleDef.{dominant_style}'

        # 根据 role 构建选择器
        selector = self._build_selector(role, dominant_style, exemplars)

        # 从示例段落中提取描述文字
        description = self._build_description(role, all_instructions[:5])

        rule = {
            'id': role,
            'label': role_info.get('label', role),
            'description': description,
            'selector': selector,
            'pPr': final_pPr,
            'rPr': final_rPr,
            'source_trace': final_trace,
            'confidence': min(1.0, len(exemplars) / 3.0),
            'exemplar_count': len(exemplars),
            'sample_texts': [p['text'][:80] for p in exemplars[:3]],
            'style_id': dominant_style,
            'has_instruction': bool(all_instructions),
        }

        return rule

    def _parse_instruction_rules(self, instructions):
        """从格式化说明文字中解析精确规则"""
        result = {'pPr': {}, 'rPr': {}}
        font_size_values = []
        line_spacing_values = []

        for inst in instructions:
            itype = inst['type']
            val = inst['value']

            if itype == 'font_name':
                if val in ('黑体', '宋体', '仿宋', '楷体'):
                    result['rPr']['font_eastAsia'] = val
                elif val in ('Times New Roman', 'Calibri', 'Arial', 'Calibri Light'):
                    result['rPr']['font_ascii'] = val
                    result['rPr']['font_hAnsi'] = val

            elif itype == 'font_size_pt':
                font_size_values.append(int(val) * 2)

            elif itype == 'font_size_chinese':
                zh_map = {
                    '初号': 84, '小初': 72,
                    '一号': 52, '小一': 48,
                    '二号': 44, '小二': 36,
                    '三号': 32, '小三': 30,
                    '四号': 28, '小四': 24,
                    '五号': 21, '小五': 18,
                }
                if val in zh_map:
                    font_size_values.append(zh_map[val])

            elif itype == 'alignment':
                a = val.strip()
                if '居中' in a:
                    result['pPr']['alignment'] = 'center'
                elif '居左' in a:
                    result['pPr']['alignment'] = 'left'
                elif '居右' in a:
                    result['pPr']['alignment'] = 'right'
                elif '两端' in a:
                    result['pPr']['alignment'] = 'both'

            elif itype == 'line_spacing_fixed':
                result['pPr']['spacing_line'] = str(int(val) * 20)
                result['pPr']['spacing_lineRule'] = 'exact'

            elif itype == 'line_spacing_pt':
                result['pPr']['spacing_line'] = str(int(val) * 20)
                result['pPr']['spacing_lineRule'] = 'exact'

            elif itype == 'line_spacing_multiple':
                mult = float(val)
                result['pPr']['spacing_line'] = str(int(mult * 240))
                result['pPr']['spacing_lineRule'] = 'auto'

            elif itype == 'line_single':
                result['pPr']['spacing_line'] = '240'
                result['pPr']['spacing_lineRule'] = 'auto'

            elif itype == 'indent_chars':
                chars = int(val)
                result['pPr']['indent_firstLineChars'] = str(chars * 100)

            elif itype in ('space_before', 'space_before_lb'):
                result['pPr']['spacing_before'] = str(int(val) * 20)

            elif itype in ('space_after', 'space_after_lb'):
                result['pPr']['spacing_after'] = str(int(val) * 20)

            elif itype == 'bold':
                result['rPr']['bold'] = '1'

            elif itype == 'superscript':
                result['rPr']['vertAlign'] = 'baseline' if val in ('不上标', '非上标') else 'superscript'

            elif itype == 'font':
                # 通用字体检测
                fval = val
                if '黑体' in fval:
                    result['rPr']['font_eastAsia'] = '黑体'
                elif '宋体' in fval:
                    result['rPr']['font_eastAsia'] = '宋体'
                elif '仿宋' in fval:
                    result['rPr']['font_eastAsia'] = '仿宋'
                elif 'Times New Roman' in fval:
                    result['rPr']['font_ascii'] = 'Times New Roman'
                    result['rPr']['font_hAnsi'] = 'Times New Roman'

        if font_size_values:
            result['rPr']['font_size'] = str(max(set(font_size_values), key=font_size_values.count))

        return result

    def _build_selector(self, role, style_id, exemplars):
        """根据角色构建段落选择器"""
        selector = {'role': role}

        if style_id:
            selector['style'] = style_id

        # 从示例文本中提取匹配模式
        patterns = []
        for p in exemplars:
            text = p['text']
            if role == 'chapter_title':
                m = re.match(r'第(\d+)章', text)
                if m:
                    patterns.append(r'^第\d+章\s')
            elif role == 'section_title':
                m = re.match(r'(\d+\.\d+)', text)
                if m:
                    patterns.append(r'^\d+\.\d+\s')
            elif role == 'subsection_title':
                m = re.match(r'(\d+\.\d+\.\d+)', text)
                if m:
                    patterns.append(r'^\d+\.\d+\.\d+\s')
            elif role == 'refs_body':
                m = re.match(r'\[\d+\]', text)
                if m:
                    patterns.append(r'^\[\d+\]')
            elif role == 'toc_entry':
                if '…' in text or '..' in text:
                    patterns.append(r'\.{4,}')

        if patterns:
            selector['pattern'] = Counter(patterns).most_common(1)[0][0]

        # 示例关键词
        if role in TEMPLATE_ROLES and 'keywords' in TEMPLATE_ROLES[role]:
            selector['keywords'] = TEMPLATE_ROLES[role]['keywords']

        return selector

    def _build_description(self, role, instructions):
        """从指令文本构建人类可读描述"""
        if not instructions:
            role_info = TEMPLATE_ROLES.get(role, {})
            return role_info.get('label', role)

        # 取前5条指令的原始值作为描述
        texts = []
        for inst in instructions[:5]:
            if inst['value'] not in texts:
                texts.append(inst['value'])
        return '；'.join(texts)

    def _extract_style_rules(self):
        """从已定义但未被使用的样式中提取规则"""
        rules = []
        used_styles = set()
        for p in self.paragraphs:
            if p['pStyle']:
                used_styles.add(p['pStyle'])

        for sid, info in self.resolver.p_styles.items():
            if sid in used_styles or sid == 'Normal':
                continue
            if not info['name']:
                continue

            # 尝试从样式名推断角色
            role = self._infer_role_from_style_name(info['name'])

            rule = {
                'id': f'style_{sid}',
                'label': info['name'],
                'description': f'样式定义（未在模板中使用）: {info["name"]}',
                'selector': {'style': sid},
                'pPr': info['pPr'],
                'rPr': info['rPr'],
                'source_trace': {k: f'pStyle.{sid}' for k in list(info['pPr'].keys()) + list(info['rPr'].keys())},
                'confidence': 0.3,
                'exemplar_count': 0,
                'sample_texts': [],
                'style_id': sid,
                'has_instruction': False,
                'inferred_role': role,
            }
            rules.append(rule)

        return rules

    def _infer_role_from_style_name(self, name):
        """从样式名推断段落角色"""
        name_lower = name.lower()
        if 'heading 1' in name_lower or '标题 1' in name_lower or '标题1' in name_lower:
            return 'chapter_title'
        if 'heading 2' in name_lower or '标题 2' in name_lower or '标题2' in name_lower:
            return 'section_title'
        if 'heading 3' in name_lower or '标题 3' in name_lower or '标题3' in name_lower:
            return 'subsection_title'
        if '正文' in name_lower or 'body' in name_lower:
            return 'body'
        if 'caption' in name_lower or '题注' in name_lower:
            return 'caption'
        if 'toc' in name_lower or '目录' in name_lower:
            return 'toc_entry'
        return None

    def extract_meta(self):
        """提取文档元信息"""
        doc_root = etree.fromstring(self.z.read('word/document.xml'))
        body = doc_root.find(f'{{{W}}}body')

        # 页面设置
        sectPr = body.find(f'{{{W}}}sectPr')
        page = {}
        if sectPr is not None:
            pgSz = sectPr.find(f'{{{W}}}pgSz')
            if pgSz is not None:
                w = pgSz.get(f'{{{W}}}w')
                h = pgSz.get(f'{{{W}}}h')
                if w and h:
                    page['page_size'] = f'{int(w)//20}mm × {int(h)//20}mm'

            pgMar = sectPr.find(f'{{{W}}}pgMar')
            if pgMar is not None:
                for attr in ['top', 'bottom', 'left', 'right', 'header', 'footer']:
                    v = pgMar.get(f'{{{W}}}{attr}')
                    if v:
                        page[f'margin_{attr}'] = f'{int(v)//20}mm'

        # 学校检测 - 从模板文字中推断
        all_text = ' '.join(p['text'] for p in self.paragraphs)
        school = None
        school_patterns = [
            (r'河北科技大学', '河北科技大学'),
            (r'河北工程技术学院', '河北工程技术学院'),
            (r'河北经贸大学', '河北经贸大学'),
            (r'北京林业大学', '北京林业大学'),
            (r'苏州科技大学', '苏州科技大学'),
        ]
        for pattern, name in school_patterns:
            if re.search(pattern, all_text):
                school = name
                break

        return {
            'template': os.path.basename(self.docx_path),
            'school': school,
            'paragraphs_total': len(self.paragraphs),
            'page': page,
            'theme': {
                'major_ea': self.resolver.theme_major_ea,
                'major_latin': self.resolver.theme_major_latin,
                'minor_ea': self.resolver.theme_minor_ea,
                'minor_latin': self.resolver.theme_minor_latin,
            },
            'doc_defaults': {
                'pPr': self.resolver.doc_defaults_pPr,
                'rPr': self.resolver.doc_defaults_rPr,
            },
            'styles_defined': {
                'paragraph': len(self.resolver.p_styles),
                'character': len(self.resolver.c_styles),
            },
        }

    def to_dict(self):
        """完整输出"""
        rules, style_library = self.extract_rules()
        return {
            'meta': self.extract_meta(),
            'rules': rules,
            'style_library': style_library,
        }

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def close(self):
        self.z.close()


# ── CLI ──

def main():
    import argparse
    parser = argparse.ArgumentParser(description='模板格式提取器 — 从参考模板提取精确格式化规范')
    parser.add_argument('template', help='参考模板 docx 路径')
    parser.add_argument('-o', '--output', help='输出 JSON 路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    args = parser.parse_args()

    reader = TemplateReader(args.template)

    if args.verbose or not args.output:
        output = reader.to_dict()
        meta = output['meta']

        print(f"\n{'='*60}")
        print(f"  📐 模板格式提取: {meta['template']}")
        print(f"  🏫 检测学校: {meta.get('school', '未识别')}")
        print(f"  📄 段落总数: {meta['paragraphs_total']}")
        print(f"{'='*60}\n")

        # 主题字体
        theme = meta['theme']
        if theme['major_ea'] or theme['major_latin']:
            print(f"  🎨 主题字体:")
            print(f"     标题: {theme['major_ea'] or '(无)'} / {theme['major_latin'] or '(无)'}")
            print(f"     正文: {theme['minor_ea'] or '(无)'} / {theme['minor_latin'] or '(无)'}\n")

        # 文档默认
        dd = meta['doc_defaults']
        if dd.get('rPr') or dd.get('pPr'):
            print(f"  📋 文档默认值:")
            rPr = dd.get('rPr', {})
            if rPr:
                font_info = []
                if rPr.get('font_eastAsia'): font_info.append(rPr['font_eastAsia'])
                if rPr.get('font_ascii'): font_info.append(rPr['font_ascii'])
                print(f"     字体: {'/'.join(font_info) if font_info else '(未设)'}")
                if rPr.get('font_size'):
                    print(f"     字号: {rPr['font_size']} (半磅)")
            pPr = dd.get('pPr', {})
            if not pPr and not rPr:
                print(f"     (继承默认)")
            print()

        # 规则
        rules = output['rules']
        print(f"  📏 提取规则 ({len(rules)} 条):\n")

        for rule in rules:
            label = rule['label']
            role_id = rule['id']
            count = rule['exemplar_count']
            conf = rule['confidence']
            has_inst = '📝' if rule['has_instruction'] else '  '
            style = rule.get('style_id') or '(无样式)'

            print(f"  [{role_id}] {label} {has_inst} ×{count} conf={conf:.2f}")
            print(f"    style_id: {style}")

            pPr = rule.get('pPr', {})
            if pPr:
                parts = []
                for k, v in pPr.items():
                    if v:
                        # 人类可读格式
                        if k == 'spacing_line':
                            lr = pPr.get('spacing_lineRule', '')
                            if lr == 'exact':
                                parts.append(f"行距=固定{int(v)//20}pt")
                            elif lr == 'auto':
                                parts.append(f"行距={int(v)/240:.1f}倍")
                            else:
                                parts.append(f"{k}={v}")
                        elif k == 'spacing_beforeLines':
                            if v != '0':
                                parts.append(f"段前={int(v)//100}行")
                        elif k == 'spacing_afterLines':
                            if v != '0':
                                parts.append(f"段后={int(v)//100}行")
                        elif k == 'indent_firstLineChars':
                            parts.append(f"首行缩进={int(v)//100}字符")
                        elif k not in ('spacing_lineRule',):
                            parts.append(f"{k}={v}")
                    elif k == 'spacing_lineRule':
                        pass
                if parts:
                    print(f"    段落: {', '.join(parts)}")

            rPr = rule.get('rPr', {})
            if rPr:
                parts = []
                for k, v in rPr.items():
                    if v:
                        if k == 'font_size':
                            parts.append(f"字号={int(v)//2}pt({v}半磅)")
                        elif k == 'bold' and v == '1':
                            parts.append('加粗')
                        elif k == 'vertAlign':
                            parts.append('是否上标=是' if v == 'superscript' else '是否上标=否')
                        else:
                            parts.append(f"{k}={v}")
                if parts:
                    print(f"    文字: {', '.join(parts)}")

            if args.verbose:
                trace = rule.get('source_trace', {})
                if trace:
                    trace_str = ', '.join(f'{k}←{v}' for k, v in sorted(trace.items()))
                    print(f"    trace: {trace_str}")

            desc = rule.get('description', '')
            if desc:
                print(f"    描述: {desc}")

            print()

        # 样式库
        sl = output.get('style_library', [])
        if sl:
            print(f"  📚 样式库 ({len(sl)} 条未使用样式):")
            for s in sl[:8]:
                inferred = s.get('inferred_role', '')
                role_tag = f' → {inferred}' if inferred else ''
                based = f' (basedOn: {s["basedOn"]})' if s.get('basedOn') else ''
                print(f"    {s['id']}: {s['label']}{role_tag}{based}")
            if len(sl) > 8:
                print(f"    ... 还有 {len(sl)-8} 条 (用 --json 看完整)")
            print()

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(reader.to_json())
        print(f'✅ 规则已保存至: {args.output}')

    reader.close()


if __name__ == '__main__':
    main()

# ════════════════════════════════════════════════════════
# 兼容层：提供旧 reader.py 的公开接口
# 供 differ.py / orchestrator.py / fix_registry.py 使用
# ════════════════════════════════════════════════════════

def classify_and_dump(docx_path):
    """兼容旧接口：用 TemplateReader 提取规则，返回 (rules, meta)"""
    tr = TemplateReader(str(docx_path))
    data = tr.to_dict()
    tr.close()

    # 角色ID → 统一类型名（与 extract_document 的 _ROLE_TYPE_MAP 保持一致）
    _ROLE_TO_TYPE = {
        'chapter_title': 'h1', 'section_title': 'h2', 'subsection_title': 'h3',
        'abstract_title_cn': 'abstract_title', 'abstract_title_en': 'abstract_title_en',
        'abstract_body': 'abstract_body', 'abstract_body_en': 'abstract_body_en',
        'abstract_keywords': 'abstract_keywords_cn', 'abstract_keywords_en': 'abstract_keywords_en',
        'ack_title': 'ack_title', 'ack_body': 'ack_body',
        'refs_title': 'refs_title', 'refs_body': 'refs_body',
        'toc_title': 'toc_title', 'toc_entry': 'toc_entry',
        'figure_caption': 'fig_caption', 'table_caption': 'table_caption',
        'declaration_body': 'declaration_body', 'statement_title': 'statement_title',
        'appendix_title': 'appendix_title',
        'cover_title': 'cover_title', 'cover_info': 'cover_info',
        'cover_date': 'cover_date', 'cover_signature': 'cover_signature',
        'cover_subtitle': 'cover_subtitle',
    }
    rules = data['rules']
    rules_out = []
    for r in rules:
        rid = r['id']
        ptype = _ROLE_TO_TYPE.get(rid, rid)
        rules_out.append({
            'type': ptype,
            'label': r['label'],
            'count': r.get('exemplar_count', 0),
            'classifier': r.get('confidence', 'template'),
            'style_id': r.get('style_id'),
            'display_name': f"{r['label']} [{r.get('style_id', '')}]",
            'final_pPr': {k: v for k, v in r.get('pPr', {}).items() if v is not None},
            'final_rPr': {k: v for k, v in r.get('rPr', {}).items() if v is not None},
            'source_trace': r.get('source_trace', {}),
            'readable': r.get('description', ''),
        })

    meta = {
        'source': str(docx_path),
        'theme': data.get('theme', {}),
        'doc_defaults_pPr': data.get('doc_defaults', {}).get('pPr', {}),
        'doc_defaults_rPr': data.get('doc_defaults', {}).get('rPr', {}),
    }
    return rules_out, meta


def classify_paragraph(text, pstyle_id='', font_size='', alignment='', in_table=False):
    """兼容旧接口：段落类型分类（含样式名推断）"""
    # 尝试从已知样式 ID 推断名称（用于有样式文档的分类）
    # StyleResolver 在函数内不可用，但 _infer_role_from_style_name_strict 可匹配
    # 调用方可传入 style name 通过 classify_template_role 的新签名
    role = classify_template_role(text, 0, 999, pstyle_id, '')
    if role is None:
        role = 'unknown'

    type_map = {
        'chapter_title': 'h1',
        'section_title': 'h2',
        'subsection_title': 'h3',
        'subsubsection_title': 'h4',
        'abstract_title': 'abstract_title',
        'abstract_body': 'abstract_body',
        'abstract_keywords_cn': 'abstract_keywords_cn',
        'abstract_keywords_en': 'abstract_keywords_en',
        'ack_title': 'ack_title',
        'ack_body': 'ack_body',
        'declaration_body': 'declaration_body',
        'statement_title': 'statement_title',
        'refs_title': 'refs_title',
        'refs_body': 'refs_body',
        'toc_title': 'toc_title',
        'toc_entry': 'toc_entry',
        'table_caption': 'table_caption',
        'fig_caption': 'fig_caption',
    }
    label = type_map.get(role, role)
    return {
        'type': label,
        'label': label,
        'classifier': 'template_role',
    }


def extract_document(docx_path):
    """提取文档段落数据 — 含 effective_pPr / effective_firstRun_rPr + 样式优先分类"""
    import zipfile
    from lxml import etree
    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    with zipfile.ZipFile(docx_path, 'r') as z:
        resolver = StyleResolver(z)
        doc = etree.fromstring(z.read('word/document.xml'))
        for child in doc:
            if child.tag.endswith('body'):
                body = child
                break

    # 角色 → 类型映射（对齐 orchestrator 的 type 命名）
    _ROLE_TYPE_MAP = {
        'chapter_title': 'h1', 'section_title': 'h2', 'subsection_title': 'h3',
        'abstract_title_cn': 'abstract_title', 'abstract_title_en': 'abstract_title_en',
        'abstract_body': 'abstract_body', 'abstract_body_en': 'abstract_body_en',
        'abstract_keywords': 'abstract_keywords_cn', 'abstract_keywords_en': 'abstract_keywords_en',
        'ack_title': 'ack_title', 'ack_body': 'ack_body',
        'refs_title': 'refs_title', 'refs_body': 'refs_body',
        'toc_title': 'toc_title', 'toc_entry': 'toc_entry',
        'figure_caption': 'fig_caption', 'table_caption': 'table_caption',
        'declaration_body': 'declaration_body', 'statement_title': 'statement_title',
        'appendix_title': 'appendix_title',
        # Front matter — excluded from body formatting
        'cover_title': 'cover_title', 'cover_info': 'cover_info',
        'cover_date': 'cover_date', 'cover_signature': 'cover_signature',
        'cover_subtitle': 'cover_subtitle',
    }

    paras = []
    total = len(body.findall(f'{{{W}}}p'))
    for idx, p in enumerate(body.findall(f'{{{W}}}p')):
        texts = [t.text or '' for t in p.findall(f'.//{{{W}}}t')]
        text = ''.join(texts)
        
        pPr = p.find(f'{{{W}}}pPr')
        pStyle_id = None
        if pPr is not None:
            ps = pPr.find(f'{{{W}}}pStyle')
            if ps is not None:
                pStyle_id = ps.get(f'{{{W}}}val')
        
        eff_pPr = resolver.resolve_paragraph(pPr, pStyle_id, trace=False)
        if pStyle_id:
            eff_pPr['pStyle'] = pStyle_id
        eff_rPr = {}
        # 智能选择 run：若首 run 为标签（摘要/Abstract/关键词等），取第二 run 的 rPr
        # 避免标签 run 的黑体字体污染整个段落的 effective rPr
        LABEL_PREFIXES = ('摘要', 'Abstract', '关键词', 'Keywords', 'Key words')
        runs = p.findall(f'{{{W}}}r')
        target_run = None
        if runs:
            first_text = ''.join(t.text or '' for t in runs[0].findall(f'.//{{{W}}}t')).strip()
            if any(first_text.startswith(lt) for lt in LABEL_PREFIXES) and len(runs) > 1:
                target_run = runs[1]  # 取第二 run（正文部分）
            else:
                target_run = runs[0]
        if target_run is not None:
            rPr = target_run.find(f'{{{W}}}rPr')
            rStyle_id = None
            if rPr is not None:
                rs = rPr.find(f'{{{W}}}rStyle')
                if rs is not None:
                    rStyle_id = rs.get(f'{{{W}}}val')
            eff_rPr = resolver.resolve_run(rPr, rStyle_id, pStyle_id, trace=False)
        
        # ── 样式优先分类 + 文本兜底 ──
        pStyle_name = ''
        if pStyle_id and pStyle_id in resolver.p_styles:
            pStyle_name = resolver.p_styles[pStyle_id].get('name', '')
        outline_lvl = eff_pPr.get('outlineLvl', None)
        role = classify_template_role(text, idx, total, pStyle_id, pStyle_name, outline_lvl)
        # 文本兜底：若样式分类返回 None 或泛化 body，用文本特征二次判定
        if role is None or role == 'body':
            refined = _disambiguate_by_text(text, idx, total, role)
            if refined and refined != 'body':
                role = refined
        # 前端页面二次判定：前 30 段中未匹配具体角色 → 大概率是封面元素
        if (role is None or role == 'body') and idx < 30 and len(text.strip()) > 5:
            if not any(kw in text for kw in ['摘要', '关键词', '目', '引言', '绪论', '第', '参考文献', '致谢']):
                # 中英文长标题 → cover_title / cover_subtitle
                if idx <= 5 and len(text.strip()) > 10 and not any(k in text for k in ['：', ':', '指导教师', '签名', '日期']):
                    if re.match(r'^[A-Za-z]', text):
                        role = 'cover_subtitle'
                    else:
                        role = 'cover_title'
                elif any(k in text for k in ['签名', '日期']):
                    role = 'cover_signature' if '签名' in text else 'cover_date'
                else:
                    role = 'cover_info'
        ptype = _ROLE_TYPE_MAP.get(role, role) if role else 'body'
        
        paras.append({
            'index': idx,
            'text_preview': text[:120],
            'text': text,
            'pStyle_id': pStyle_id,
            'type': ptype,
            'classification': role,
            'effective_pPr': eff_pPr,
            'effective_firstRun_rPr': eff_rPr,
        })
    return {'paragraphs': paras}

