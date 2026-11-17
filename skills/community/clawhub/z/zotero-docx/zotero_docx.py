"""带 Zotero 引用的 docx 安全改写。

设计原则是不确定就拒绝。体检不通过一律不产出文件，宁可不干活也不悄悄改坏。
每条防护背后的实测数据和源码依据见 references/findings.md。
"""
import hashlib
import os
import posixpath
import re
from urllib.parse import unquote
import shutil
import tempfile
import zipfile
from pathlib import Path

from lxml import etree

# transitional 是常见形态；strict 用另一套 URI，两者都认，别的一律拒绝
NS_TRANSITIONAL = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS_STRICT = 'http://purl.oclc.org/ooxml/wordprocessingml/main'
# 只支持 transitional。strict 变体没有实测样本, Zotero 在里面长什么样未知,
# 放行等于拿用户的论文赌, 所以识别出来就明确拒绝。

CP_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'
CUSTOM_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/custom-properties'
VT_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'
FMTID = '{D5CDD505-2E9C-101B-9397-08002B2CF9AE}'
XML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'

# 只处理这些 part。范围写死，宁可漏也不误伤图表、OLE 子文档这些不归本模块管的东西。
STORY_PARTS = re.compile(r'^word/(document|footnotes|endnotes|comments|header\d*|footer\d*)\.xml$')

PREF_CHUNK = 255          # Word 单个自定义属性上限
MAX_CHANGE_RATIO = 0.5    # 改动字符数超过正文一半就当成失控
MIN_CHARS_FOR_RATIO = 2000  # 太短的文档不做覆盖率判断, 否则改一句就超标
MAX_EXPANSION = 3.0       # 输出/原文 长度比上限, 抓改写函数跑飞


class Refused(Exception):
    """体检没过。message 会直接给用户看，要说清为什么不能处理。"""


class Q:
    """按文档实际命名空间生成限定名，不写死。"""

    def __init__(self, ns):
        self.ns = ns

    def __call__(self, tag):
        return '{%s}%s' % (self.ns, tag)


def _detect_ns(root):
    ns = etree.QName(root).namespace
    if ns == NS_STRICT:
        raise Refused('这是 strict OOXML 格式的文档，本工具只在 transitional 格式上验证过，'
                      '未经验证就处理有风险，拒绝。可以用 Word 另存为常规 .docx 后重试。')
    if ns != NS_TRANSITIONAL:
        raise Refused('文档的命名空间不认识：%s。不是 Word 生成的常规 docx，拒绝处理。' % ns)
    return ns


# ---------- 体检 ----------

def _read_prefs(zf):
    """把 ZOTERO_PREF_n 拼回完整字符串。用 XML 解析，不用正则。"""
    try:
        blob = zf.read('docProps/custom.xml')
    except KeyError:
        return None
    root = etree.fromstring(blob)
    parts = {}
    for prop in root.findall('{%s}property' % CUSTOM_NS):
        name = prop.get('name') or ''
        m = re.fullmatch(r'ZOTERO_PREF_(\d+)', name)
        if not m:
            continue
        node = prop.find('{%s}lpwstr' % VT_NS)
        parts[int(m.group(1))] = node.text or '' if node is not None else ''
    if not parts:
        return None
    idx = sorted(parts)
    if idx != list(range(1, len(idx) + 1)):
        raise Refused('ZOTERO_PREF 分片编号不连续（实际 %s），文件可能已损坏。' % idx)
    return ''.join(parts[i] for i in idx)


def _storage_mode(prefs):
    """Field 还是 Bookmark。依据见 findings.md。"""
    if not prefs:
        return None
    try:
        node = etree.fromstring(prefs.encode())
    except etree.XMLSyntaxError:
        raise Refused('Zotero 文档偏好不是合法 XML，无法判断存储模式。')
    for pref in node.iter('pref'):
        if pref.get('name') == 'fieldType':
            return pref.get('value')
    return None


def precheck(path):
    """体检。返回一份报告，任何一项不满足直接 Refused。"""
    rep = {'path': str(path), 'parts': [], 'fields': 0, 'bibl': 0, 'ns': None,
           'storage_mode': None, 'style': None, 'has_revisions': False}
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()

        prefs = _read_prefs(zf)
        mode = _storage_mode(prefs)
        rep['storage_mode'] = mode
        if mode and mode.lower() != 'field':
            raise Refused('这份文档的 Zotero 引用存成了 %s 模式，不是 Field 模式。'
                          '本工具只认 Field，处理 %s 模式会把引用当普通文字改掉。'
                          '请在 Word 的 Zotero 文档首选项里切成 Fields 后重试。' % (mode, mode))
        if prefs:
            try:
                node = etree.fromstring(prefs.encode())
                styles = node.findall('.//style')
                rep['style'] = styles[0].get('id') if len(styles) == 1 else None
            except etree.XMLSyntaxError:
                raise Refused('Zotero 文档偏好不是合法 XML，拒绝处理。')

        signed = any(n.startswith('_xmlsignatures/') for n in names)
        if not signed and '[Content_Types].xml' in names:
            # 签名部件不一定放在 _xmlsignatures/ 下，按内容类型查更可靠
            ct = zf.read('[Content_Types].xml').decode('utf-8', 'replace')
            signed = 'digital-signature' in ct
        if signed:
            raise Refused('文档带数字签名。重写包会让签名失效，且无法重新签名，'
                          '拒绝处理。请先移除签名再试。')

        story = [n for n in names if STORY_PARTS.match(n)]
        if 'word/document.xml' not in story:
            raise Refused('包里找不到 word/document.xml，这不像一个 docx。')
        # 命名空间必须最先确认。放在后面的话，strict 文档会因为找不到任何
        # transitional 元素而被当成「0 个域」，看起来像安全文件。
        rep['ns'] = _detect_ns(etree.fromstring(zf.read('word/document.xml')))

        # altChunk 必须查元素，不能查文件名。真实的 <w:altChunk r:id="rId9"/>
        # 关联的 part 可以叫任意名字（Word 常用 afchunk.htm），查文件名等于没查。
        q0 = Q(rep['ns'])
        for name in [n for n in names if STORY_PARTS.match(n)]:
            if etree.fromstring(zf.read(name)).find('.//' + q0('altChunk')) is not None:
                raise Refused('%s 里含 altChunk（嵌入了其它格式的内容），'
                              '本工具扫不到那部分，拒绝处理。' % name)

        for name in story:
            root = etree.fromstring(zf.read(name))
            ns = _detect_ns(root)
            if rep['ns'] and rep['ns'] != ns:
                raise Refused('同一文档里出现两种命名空间，拒绝处理。')
            rep['ns'] = ns
            q = Q(ns)
            _walk_fields(root, q, name, rep)
            if any(root.find('.//' + q(t)) is not None
                   for t in ('ins', 'del', 'moveFrom', 'moveTo')):
                rep['has_revisions'] = True
            rep['parts'].append(name)

        # Bookmark 模式的另一个特征：书签名带 ZOTERO_ / CSL_ 前缀
        for name in story:
            root = etree.fromstring(zf.read(name))
            q = Q(rep['ns'])
            for bm in root.iter(q('bookmarkStart')):
                bn = bm.get(q('name')) or ''
                if bn.startswith(('ZOTERO_', 'CSL_')):
                    raise Refused('检测到 Zotero 书签 %s，说明引用存成了 Bookmark 模式，拒绝处理。' % bn)

    if rep['fields'] == 0:
        raise Refused('没有发现任何 Zotero 引用域。可能这份文档本来就没有引用，'
                      '也可能引用用了本工具不认识的形式。为免误判成安全，拒绝处理。')
    return rep


def _tally(s, rep):
    if 'ZOTERO_ITEM' in s or 'ZOTERO_TEMP' in s:
        rep['fields'] += 1
    if 'ZOTERO_BIBL' in s:
        rep['bibl'] += 1


def _walk_fields(root, q, part, rep):
    """扫一遍域，顺便校验 begin/separate/end 配对。不配对直接拒绝。"""
    depth = 0
    seen_separate = []
    instr = []                      # 每层域累积的域代码分片
    for el in root.iter(q('fldChar'), q('instrText'), q('delInstrText'), q('fldSimple')):
        tag = etree.QName(el).localname
        if tag == 'fldChar':
            t = el.get(q('fldCharType'))
            if t == 'begin':
                depth += 1
                seen_separate.append(False)
                instr.append([])
            elif t == 'separate':
                if depth == 0:
                    raise Refused('%s 里出现没有 begin 的 separate，域结构损坏。' % part)
                if seen_separate[-1]:
                    raise Refused('%s 里同一个域出现两次 separate，域结构损坏。' % part)
                seen_separate[-1] = True
            elif t == 'end':
                if depth == 0:
                    raise Refused('%s 里出现没有 begin 的 end，域结构损坏。' % part)
                depth -= 1
                if not seen_separate.pop():
                    raise Refused('%s 里有域从 begin 直接到 end，缺 separate 标记，'
                                  '域结构损坏。' % part)
                _tally(''.join(instr.pop()), rep)
            else:
                # ST_FldCharType 只有 begin/separate/end 三个取值。别的一律当损坏：
                # 否则一个伪造的 fldCharType 就能让扫描漏掉真实的域边界，
                # 而这个模块的前提是「不确定就拒绝」。
                raise Refused('%s 里出现未知的 fldCharType=%r，域结构损坏。' % (part, t))
        elif tag in ('instrText', 'delInstrText'):
            s = el.text or ''
            if instr:
                # 域代码会被 Word 拆成多个 instrText——实测真实论文里一个域拆到
                # 17 段，切点落在中西文交界处。必须按域拼起来再判断，
                # 逐节点看会把「ZOTERO_ITEM 正好跨段」的域整个漏掉。
                instr[-1].append(s)
            else:
                _tally(s, rep)      # 域外的孤立域代码，按原样单独算
        elif tag == 'fldSimple':
            _tally(el.get(q('instr')) or '', rep)
    if depth != 0:
        raise Refused('%s 里有 %d 个域没有闭合，域结构损坏。' % (part, depth))


# ---------- 保护范围 ----------

def protected_runs(root, q):
    """域内 run 的集合。complex field 的 begin..end 闭区间，加上 fldSimple 内部所有 run。"""
    marked = set()
    for fs in root.iter(q('fldSimple')):
        for r in fs.iter(q('r')):
            marked.add(r)
    depth = 0
    for r in root.iter(q('r')):
        fc = r.find(q('fldChar'))
        t = fc.get(q('fldCharType')) if fc is not None else None
        if t == 'begin':
            depth += 1
        if depth > 0 or fc is not None \
                or r.find(q('instrText')) is not None \
                or r.find(q('delInstrText')) is not None:
            marked.add(r)
        if t == 'end':
            depth -= 1
            # 不做 max(0,...) 兜底。这个函数是公开的，别人可能不经 precheck
            # 直接调用；域结构畸形时静默容错会让显示文本失去保护。
            if depth < 0:
                raise Refused('域结构畸形：出现没有 begin 的 end。')
    if depth != 0:
        raise Refused('域结构畸形：有 %d 个域没有闭合。' % depth)
    return marked


# ---------- 跨 run 改写 ----------

class _Segment:
    """一段连续可改写文本，记住它由哪些 w:t 拼成，改完按原比例写回。"""

    __slots__ = ('nodes', 'text')

    def __init__(self):
        self.nodes = []
        self.text = ''

    def add(self, node):
        self.nodes.append(node)
        self.text += node.text or ''

    def write_back(self, new_text):
        """把新文本写回原来那批节点。策略是全部塞进第一个节点，其余清空。

        这样做的理由：跨 run 改写之后，新文本跟原来的格式区间不再有对应关系，
        硬按长度切分会把格式切错位置。塞进第一个节点意味着这段文字统一采用
        第一个 run 的格式。所以只对格式一致的相邻 run 合并成 segment（见 _segments）。
        """
        if not self.nodes:
            return 0
        if new_text == self.text:
            return 0
        first = self.nodes[0]
        first.text = new_text
        if new_text != new_text.strip():
            first.set(XML_SPACE, 'preserve')
        for n in self.nodes[1:]:
            n.text = ''
        return 1


def _rpr_key(run, q):
    """run 的格式指纹。格式不同的 run 不能合并，否则改完格式会串。"""
    rpr = run.find(q('rPr'))
    if rpr is None:
        return b''
    return etree.tostring(rpr, method='c14n')


# run 之间夹着的独立标记。文本被搬走会让这些标记框住空区间，
# 书签失效、批注范围错位、交叉引用指向空处。
MARKER_TAGS = ('bookmarkStart', 'bookmarkEnd', 'commentRangeStart', 'commentRangeEnd',
               'proofErr', 'permStart', 'permEnd', 'moveFromRangeStart', 'moveFromRangeEnd',
               'moveToRangeStart', 'moveToRangeEnd',
               'customXmlInsRangeStart', 'customXmlInsRangeEnd',
               'customXmlDelRangeStart', 'customXmlDelRangeEnd',
               'customXmlMoveFromRangeStart', 'customXmlMoveFromRangeEnd',
               'customXmlMoveToRangeStart', 'customXmlMoveToRangeEnd')

# run 里除了这两个之外的任何直接子元素，都当成位置边界。
# 不用白名单列「哪些算锚点」—— 列表漏一个就错一个，实测 lastRenderedPageBreak
# 不在白名单里时，两侧文字会被合并、标记被搬到末尾。反过来判断才穷尽。
RUN_TEXTUAL = ('rPr', 't')

# 把 run 包起来的结构。跨过它们合并等于把文字挪进挪出。
WRAPPER_TAGS = ('hyperlink', 'ins', 'del', 'sdtContent', 'smartTag', 'moveFrom', 'moveTo',
                'customXml', 'dir', 'bdo')


def _has_anchor(run, q):
    """run 里有没有非文本子元素（rPr 和 t 之外的都算）。"""
    textual = {q(t) for t in RUN_TEXTUAL}
    return any(c.tag not in textual for c in run)


def _split_by_anchor(run, q):
    """把一个 run 里的 w:t 按非文本元素的位置分组。

    按文档顺序走 run 的直接子元素，遇到非文本元素就断开。
    只有真被隔开的 w:t 才分到不同组，连续的 w:t 仍然合并
    （所以 Word 拆出的 Osteo/arthritis 还是能拼回去改）。
    """
    groups, cur = [], []
    tt, rprt = q('t'), q('rPr')
    for child in run:
        if child.tag == tt:
            cur.append(child)
        elif child.tag == rprt:
            continue          # 格式定义不是位置标记
        else:
            if cur:
                groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def _segments(root, q, skip):
    """把可改写的 w:t 按「同段落 + 同格式 + 中间没有硬边界」分组。

    硬边界分三类，见上面三个常量。任何一类出现都断开分组，
    宁可多分几段（改写函数拿到的文本短一点），也不把文字搬过这些结构。
    """
    segs = []
    # 文本框（w:drawing > w:txbxContent > w:p）会让内层段落的 run 被外层段落
    # 和它自己各遍历一次，同一段文字被改两次。只让最内层那次处理。
    for p in root.iter(q('p')):
        # 外层段落里如果嵌着别的段落，那部分由内层那次遍历负责
        pt = q('p')
        cur = _Segment()
        cur_key = None
        cur_parent = None

        def flush():
            if cur.nodes:
                segs.append(cur)

        # 按文档顺序遍历段落的所有后代，遇到标记节点就断开
        for el in p.iter():
            tag = etree.QName(el).localname
            if tag in MARKER_TAGS:
                flush()
                cur = _Segment()
                cur_key = cur_parent = None
                continue
            if tag != 'r':
                continue
            r = el
            # 一次向上遍历同时拿两件事：这个 run 归哪个段落管（文本框会让内层
            # 段落的 run 被外层也遍历到），以及路径上有没有经过包装结构。
            # 只看直接父节点的话，嵌在「wrapper > 中间层 > run」里的 run 会漏掉保护。
            # 注意不能用 id() 建集合判断 —— lxml 代理对象按需生成，id 不稳定。
            node, wrapped = r.getparent(), False
            while node is not None and node.tag != pt:
                if etree.QName(node).localname in WRAPPER_TAGS:
                    wrapped = True
                node = node.getparent()
            if node is not None and node is not p:
                continue
            parent = r.getparent()
            protected = r in skip
            # 含锚点的 run 或被包住的 run：不能跟邻居合并，但它自己的文字
            # 仍然可以改（单独成一段）。整体跳过等于静默漏改。
            isolated = wrapped or _has_anchor(r, q)
            key = _rpr_key(r, q)
            if protected:
                flush()
                cur = _Segment()
                cur_key = cur_parent = None
                continue
            if isolated:
                # 含锚点的 run 不跟邻居合并。内部怎么切要看锚点在哪：
                # 锚点夹在两个 w:t 中间时必须逐个切开（否则写回把文本挤进第一个
                # 节点，锚点相对位置就变了）；锚点只在首尾时中间那段可以合并，
                # 不然像 Osteo|arthritis 这种被 Word 拆开的词就再也替换不到了。
                flush()
                for grp in _split_by_anchor(r, q):
                    seg = _Segment()
                    for t in grp:
                        seg.add(t)
                    if seg.text:
                        segs.append(seg)
                cur = _Segment()
                cur_key = cur_parent = None
                continue
            if key != cur_key or parent is not cur_parent:
                flush()
                cur = _Segment()
                cur_key = key
                cur_parent = parent
            for t in r.findall(q('t')):
                cur.add(t)
        flush()
    return [s for s in segs if s.text]


# ---------- 审计 ----------

def _sha(*parts):
    return hashlib.sha256('\x00'.join(parts).encode()).hexdigest()


REVISION_WRAPPERS = ('ins', 'del', 'moveFrom', 'moveTo')


def _revision_path(el):
    """域外面套着的修订标记链，从外到内。

    两个域内容可以逐字节相同，但一个裸着、一个被 w:moveFrom 包着：
    接受修订后前者留下、后者连引用一起消失。只比对域内部查不出这种调包，
    所以把包装链一起算进指纹。
    """
    out = []
    p = el.getparent()
    while p is not None:
        ln = etree.QName(p).localname
        if ln in REVISION_WRAPPERS:
            out.append(ln)
        p = p.getparent()
    return '/'.join(reversed(out))


def _field_inventory(zf, ns):
    """逐个域建清单，改写前后必须完全一致。

    记四样：完整指令代码、separate 之后的显示文本、有没有 separate 标记、
    外层的修订包装链。只记指令代码是不够的 —— 显示文本被改、separate 被去掉、
    整个域被塞进 w:moveFrom，都查不出来。
    """
    q = Q(ns)
    inv = []
    for name in sorted(n for n in zf.namelist() if STORY_PARTS.match(n)):
        root = etree.fromstring(zf.read(name))
        stack = []          # 每层: [指令片段, 显示文本片段, 见过 separate, 修订链]
        for el in root.iter(q('fldChar'), q('instrText'), q('delInstrText'),
                            q('fldSimple'), q('t')):
            tag = etree.QName(el).localname
            if tag == 'fldChar':
                t = el.get(q('fldCharType'))
                if t == 'begin':
                    stack.append([[], [], False, _revision_path(el)])
                elif t == 'separate' and stack:
                    stack[-1][2] = True
                elif t == 'end' and stack:
                    code, shown, sep, rev = stack.pop()
                    inv.append((name, 'complex',
                                _sha(''.join(code), ''.join(shown),
                                     '1' if sep else '0', rev)))
            elif tag in ('instrText', 'delInstrText') and stack:
                stack[-1][0].append(el.text or '')
            elif tag == 't' and stack and stack[-1][2]:
                stack[-1][1].append(el.text or '')   # separate 之后才算显示文本
            elif tag == 'fldSimple':
                shown = ''.join(x.text or '' for x in el.iter(q('t')))
                inv.append((name, 'simple',
                            _sha(el.get(q('instr')) or '', shown, '1',
                                 _revision_path(el))))
    return inv


REL_TAG = '{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'


def _resolve_target(base, raw):
    """把关系里的 Target 解析成包内路径。

    Target 是 URI 不是文件名：空格写成 %20，可能带 # 片段，也可能是
    以 / 开头的绝对路径。直接当字符串比对会把正常文件误判成断链 ——
    实测「文件名 my image.png / Target 写 my%20image.png」就会被误拦。
    """
    raw = raw.split('#', 1)[0].split('?', 1)[0]
    return posixpath.normpath(posixpath.join(base, unquote(raw))).lstrip('/')


def _check_relationships(zf, names):
    """每条内部关系的目标都得真实存在，否则 Word 会报文件损坏。"""
    pool = set(names)
    for name in names:
        if not name.endswith('.rels'):
            continue
        # word/_rels/document.xml.rels -> base 是 word/ ；_rels/.rels -> 顶层
        base = '/'.join(name.split('/')[:-2])
        for rel in etree.fromstring(zf.read(name)).iter(REL_TAG):
            if rel.get('TargetMode') == 'External':
                continue
            tgt = _resolve_target(base, rel.get('Target') or '')
            if tgt == '..' or tgt.startswith('../'):
                # normpath 之后仍带 ../ 说明目标逃出了包根。lstrip('/') 去不掉它，
                # 而 zip 条目名本身可以是 ../x.xml，两边一撞校验就成了摆设。
                raise Refused('产出文件里的关系逃出了包根：%s 指向 %s，已丢弃。'
                              % (name, tgt))
            if tgt not in pool:
                raise Refused('产出文件里的关系断了：%s 指向不存在的 %s，已丢弃。'
                              % (name, tgt))


def _prefs_of(zf):
    try:
        return _read_prefs(zf)
    except Refused:
        return None


# ---------- 样式 ----------

def _set_style(items, new_style):
    """改参考文献样式。全程 XML 节点操作，不做字符串插值。"""
    if not re.fullmatch(r'[A-Za-z0-9:/._%-]+', new_style or ''):
        raise Refused('样式 id 含非法字符：%r。只接受 URL 安全字符。' % new_style)
    if 'docProps/custom.xml' not in items:
        raise Refused('文档里没有 docProps/custom.xml，无法设置样式。')

    root = etree.fromstring(items['docProps/custom.xml'])
    props = root.findall('{%s}property' % CUSTOM_NS)
    zot = [p for p in props if re.fullmatch(r'ZOTERO_PREF_\d+', p.get('name') or '')]
    if not zot:
        raise Refused('文档里没有 Zotero 偏好属性，无法设置样式。')

    def _order(p):
        return int(re.fullmatch(r'ZOTERO_PREF_(\d+)', p.get('name')).group(1))

    full = ''
    for p in sorted(zot, key=_order):
        node = p.find('{%s}lpwstr' % VT_NS)
        full += (node.text or '') if node is not None else ''

    data = etree.fromstring(full.encode())
    styles = data.findall('.//style')
    if len(styles) != 1:
        raise Refused('偏好里有 %d 个 style 节点，应为 1 个。' % len(styles))
    styles[0].set('id', new_style)
    new_full = etree.tostring(data, encoding='unicode')

    for p in zot:
        root.remove(p)
    # 不能用 isdigit()：XML Schema 的整数词法允许带符号，pid="+2" 会被漏掉，
    # 接着又生成一个 pid="2"，产出一份 pid 逻辑重复的 custom-properties。
    used = set()
    for p in root.findall('{%s}property' % CUSTOM_NS):
        try:
            used.add(int((p.get('pid') or '').strip()))
        except ValueError:
            pass
    pid = max(used) + 1 if used else 2
    for i in range(0, len(new_full), PREF_CHUNK):
        prop = etree.SubElement(root, '{%s}property' % CUSTOM_NS)
        prop.set('fmtid', FMTID)
        prop.set('pid', str(pid))
        prop.set('name', 'ZOTERO_PREF_%d' % (i // PREF_CHUNK + 1))
        val = etree.SubElement(prop, '{%s}lpwstr' % VT_NS)
        val.text = new_full[i:i + PREF_CHUNK]
        pid += 1
    items['docProps/custom.xml'] = etree.tostring(root, xml_declaration=True,
                                                  encoding='UTF-8', standalone=True)


# ---------- 主流程 ----------

def process(src, dst, fn=None, new_style=None, dry_run=False, overwrite=False,
            allow_heavy_rewrite=False, allow_revisions=False):
    """改正文 and/or 换样式。

    fn 收到的是跨 run 拼好的完整文本，返回改写后的文本。
    体检不过、改写幅度异常、或改写后域清单对不上，都不产出文件。
    dry_run=True 只报告会改什么，不写文件。
    """
    src, dst = Path(src), Path(dst)
    if src.resolve() == dst.resolve():
        raise Refused('源文件和目标文件是同一个，拒绝原地覆盖。')
    if dst.exists() and not overwrite:
        raise Refused('目标文件 %s 已存在。传 overwrite=True 才会覆盖。' % dst)

    rep = precheck(src)
    if rep['has_revisions'] and fn is not None and not allow_revisions and not dry_run:
        raise Refused('文档带未处理的修订标记。改写会动到 w:ins 里的文字但不生成新的'
                      '修订记录，等于无痕篡改别人的修改。请先在 Word 里接受或拒绝'
                      '所有修订；确实要这样改就传 allow_revisions=True。')
    ns = rep['ns']
    q = Q(ns)

    with zipfile.ZipFile(src) as zf:
        infos = zf.infolist()
        items = {i.filename: zf.read(i.filename) for i in infos}
        before_inv = _field_inventory(zf, ns)
        before_prefs = _prefs_of(zf)

    seen = set()
    for i in infos:
        if i.filename in seen:
            raise Refused('包里有重名条目 %s，拒绝处理。' % i.filename)
        seen.add(i.filename)

    changes = []
    total_t = 0
    if fn is not None:
        for name in list(items):
            if not STORY_PARTS.match(name):
                continue
            root = etree.fromstring(items[name])
            skip = protected_runs(root, q)
            segs = _segments(root, q, skip)
            total_t += sum(len(s.text) for s in segs)
            hit = 0
            for s in segs:
                new = fn(s.text)
                if new is None or new == s.text:
                    continue
                if not isinstance(new, str):
                    raise Refused('改写函数返回了 %s，必须返回 str 或 None。'
                                  '原文开头：%r' % (type(new).__name__, s.text[:40]))
                changes.append((name, s.text, new))
                if not dry_run:
                    hit += s.write_back(new)
            if hit and not dry_run:
                items[name] = etree.tostring(root, xml_declaration=True,
                                             encoding='UTF-8', standalone=True)

    changed_chars = sum(len(a) for _, a, _ in changes)
    out_chars = sum(len(b) for _, _, b in changes)
    if not allow_heavy_rewrite and total_t >= MIN_CHARS_FOR_RATIO:
        # 覆盖率：改了正文的多大比例。降 AI 味这类场景本来就会大面积改，
        # 所以给了 allow_heavy_rewrite 开关，而不是把阈值调松。
        if changed_chars > total_t * MAX_CHANGE_RATIO:
            raise Refused('改写触及 %d 字符，占可改正文 %d 字符的 %d%%，超过 %d%% 上限。'
                          '确认是有意为之就传 allow_heavy_rewrite=True。'
                          % (changed_chars, total_t, int(100 * changed_chars / total_t),
                             int(MAX_CHANGE_RATIO * 100)))
    # 膨胀率逐片段判断，不能汇总。汇总的话一段疯狂膨胀会被另一段收缩抵消掉。
    for part, old, new in changes:
        if len(old) >= 20 and len(new) > len(old) * MAX_EXPANSION:
            raise Refused('有片段改写后 %d 字符，是原文 %d 字符的 %.1f 倍，超过 %d 倍上限，'
                          '疑似改写函数失控，已拒绝产出。原文开头：%r'
                          % (len(new), len(old), len(new) / len(old), MAX_EXPANSION, old[:40]))

    if dry_run:
        return {'refused': False, 'precheck': rep, 'changes': changes, 'written': False}

    if new_style:
        _set_style(items, new_style)

    # mkstemp 返回 (fd, path)，fd 必须显式关掉。只取 [1] 会每次调用泄漏一个
    # 文件描述符，批量处理几百个文档就会 EMFILE。
    _fd, _tmp_path = tempfile.mkstemp(suffix='.docx', dir=str(dst.parent))
    os.close(_fd)
    tmp = Path(_tmp_path)
    try:
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
            for i in infos:                       # 保持原顺序和压缩方式
                zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
                zi.compress_type = i.compress_type
                zi.external_attr = i.external_attr
                z.writestr(zi, items[i.filename])

        bad = zipfile.ZipFile(tmp).testzip()
        if bad:
            raise Refused('产出的文件 zip 校验失败：%s' % bad)
        with zipfile.ZipFile(tmp) as zf:
            out_names = zf.namelist()
            for name in out_names:
                if name.endswith('.xml') or name.endswith('.rels'):
                    etree.fromstring(zf.read(name))   # 解析不过就是坏的
            _check_relationships(zf, out_names)
            after_inv = _field_inventory(zf, ns)
            after_prefs = _prefs_of(zf)

        if before_inv != after_inv:
            raise Refused('改写后引用域清单跟改写前对不上（改前 %d 个，改后 %d 个），已丢弃产出。'
                          % (len(before_inv), len(after_inv)))
        if new_style is None and before_prefs != after_prefs:
            raise Refused('没要求换样式，但样式偏好被改动了，已丢弃产出。')

        shutil.move(str(tmp), str(dst))
    finally:
        if tmp.exists():
            tmp.unlink()

    return {'refused': False, 'precheck': rep, 'changes': changes, 'written': True,
            # citations 只数 Zotero 引用；all_fields 是文档里所有 Word 域，
            # 含参考文献表和非 Zotero 的域。两个口径不同，别混用。
            'citations': rep['fields'], 'bibliographies': rep['bibl'],
            'all_fields': len(before_inv),
            'style': rep['style'], 'new_style': new_style}
