"""每个防护对应一个构造出来的反例。跑 python3 test_zotero_docx.py。

只拿一篇正常论文测是不够的 —— 那篇恰好不触发任何坑，全绿反而给人错觉。
"""
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lxml import etree
from zotero_docx import (Q, Refused, _read_prefs, precheck, process,
                         protected_runs)

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
STRICT = 'http://purl.oclc.org/ooxml/wordprocessingml/main'
CUSTOM = 'http://schemas.openxmlformats.org/officeDocument/2006/custom-properties'
VT = 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'
FMTID = '{D5CDD505-2E9C-101B-9397-08002B2CF9AE}'

CT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
      '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="xml" ContentType="application/xml"/></Types>')

CITE = ('<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r><w:instrText xml:space="preserve"> ADDIN ZOTERO_ITEM CSL_CITATION '
        '{"citationID":"a"} </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        '<w:r><w:t>(Smith, 2020)</w:t></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r>')

_n = [0]
RESULTS = []


def prefs_xml(mode='Field', style='http://www.zotero.org/styles/nature'):
    data = ('<data data-version="3" zotero-version="7"><session id="X"/>'
            '<style id="%s" hasBibliography="1"/>'
            '<prefs><pref name="fieldType" value="%s"/></prefs></data>' % (style, mode))
    chunks = [data[i:i + 255] for i in range(0, len(data), 255)]
    props = ''.join(
        '<property fmtid="%s" pid="%d" name="ZOTERO_PREF_%d"><vt:lpwstr>%s</vt:lpwstr></property>'
        % (FMTID, 2 + i, i + 1,
           c.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
        for i, c in enumerate(chunks))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Properties xmlns="%s" xmlns:vt="%s">%s</Properties>' % (CUSTOM, VT, props))


def make(tmp, body, ns=W, custom=None, extra=None):
    _n[0] += 1
    p = Path(tmp) / ('t%d.docx' % _n[0])
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="%s" xmlns:r="http://schemas.openxmlformats.org/'
           'officeDocument/2006/relationships"><w:body>%s</w:body></w:document>' % (ns, body))
    with zipfile.ZipFile(p, 'w') as z:
        z.writestr('[Content_Types].xml', CT)
        z.writestr('word/document.xml', doc)
        z.writestr('docProps/custom.xml', custom if custom is not None else prefs_xml())
        for k, v in (extra or {}).items():
            z.writestr(k, v)
    return p


def check(name, ok, detail=''):
    RESULTS.append((name, ok))
    print('  %s %s%s' % ('通过' if ok else '失败', name, ('  ' + detail) if detail else ''))


def refuses(name, fn, keyword):
    """fn 应当抛 Refused，且理由里含 keyword。"""
    try:
        fn()
        check(name, False, '居然放行了')
    except Refused as e:
        check(name, keyword in str(e), '理由: %s' % str(e)[:40])


def main():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / 'out.docx'

        print('=== 一 应当拒绝的情况 ===')
        body = '<w:p><w:r><w:t>正文</w:t></w:r>%s</w:p>' % CITE

        f = make(tmp, body, custom=prefs_xml(mode='Bookmark'))
        refuses('Bookmark 模式被拒绝', lambda: precheck(f), 'Bookmark')

        f2 = make(tmp, '<w:p><w:bookmarkStart w:id="1" w:name="ZOTERO_BREF_x"/>'
                       '<w:r><w:t>正文</w:t></w:r>%s</w:p>' % CITE)
        refuses('ZOTERO_ 书签被拒绝', lambda: precheck(f2), '书签')

        f3 = make(tmp, body, ns=STRICT)
        refuses('strict 命名空间被拒绝', lambda: precheck(f3), 'strict')

        f4 = make(tmp, '<w:p><w:r><w:fldChar w:fldCharType="begin"/></w:r>'
                       '<w:r><w:instrText> ADDIN ZOTERO_ITEM CSL_CITATION {} </w:instrText></w:r>'
                       '<w:r><w:t>x</w:t></w:r></w:p>')
        refuses('域未闭合被拒绝', lambda: precheck(f4), '闭合')

        f5 = make(tmp, '<w:p><w:r><w:t>没有任何引用</w:t></w:r></w:p>')
        refuses('零引用被拒绝', lambda: precheck(f5), '拒绝处理')

        # 真实 altChunk：元素在 document.xml 里，关联 part 叫任意名字
        f6 = make(tmp, body + '<w:altChunk r:id="rId9"/>',
                  extra={'word/afchunk.htm': '<html/>'})
        refuses('altChunk 被拒绝（真实形态，关联 part 不叫 altChunk）',
                lambda: precheck(f6), 'altChunk')

        f7 = make(tmp, body)
        refuses('拒绝原地覆盖', lambda: process(f7, f7, fn=lambda t: t), '同一个')
        refuses('非法样式 id 被拒绝', lambda: process(f7, out, new_style='a"b'), '非法字符')

        print()
        print('=== 二 应当保护的情况 ===')
        f8 = make(tmp, '<w:p><w:r><w:t>前 </w:t></w:r>'
                       '<w:fldSimple w:instr=" ADDIN ZOTERO_ITEM CSL_CITATION {} ">'
                       '<w:r><w:t>(Smith, 2020)</w:t></w:r></w:fldSimple>'
                       '<w:r><w:t> 后</w:t></w:r></w:p>')
        rep = precheck(f8)
        with zipfile.ZipFile(f8) as z:
            root = etree.fromstring(z.read('word/document.xml'))
        q = Q(W)
        skip = protected_runs(root, q)
        inner = [r for fs in root.iter(q('fldSimple')) for r in fs.iter(q('r'))]
        check('fldSimple 内 run 受保护', len(inner) == 1 and all(r in skip for r in inner))
        check('fldSimple 被计入引用数', rep['fields'] == 1, '实际 %d' % rep['fields'])

        f9 = make(tmp, '<w:p><w:r><w:t>Smith 的研究</w:t></w:r>%s</w:p>' % CITE)
        process(f9, out, fn=lambda t: t.replace('Smith', 'XXXX'))
        txt = zipfile.ZipFile(out).read('word/document.xml').decode()
        check('域外文字被改写', 'XXXX 的研究' in txt)
        check('域内显示文本没动', '(Smith, 2020)' in txt)
        check('域代码没动', 'ZOTERO_ITEM' in txt)
        out.unlink()

        print()
        print('=== 三 跨 run 改写 ===')
        f10 = make(tmp, '<w:p><w:r><w:t>O</w:t></w:r><w:r><w:t>steoarthritis</w:t></w:r>'
                        '<w:r><w:t> 是常见病</w:t></w:r>%s</w:p>' % CITE)
        seen = []
        process(f10, out, fn=lambda t: (seen.append(t), t)[1], dry_run=True)
        check('碎片被拼成完整文本', any('Osteoarthritis' in s for s in seen), '拿到 %r' % seen)

        process(f10, out, fn=lambda t: t.replace('Osteoarthritis', '骨关节炎'))
        txt = zipfile.ZipFile(out).read('word/document.xml').decode()
        check('跨 run 替换成功', '骨关节炎' in txt)
        out.unlink()

        f11 = make(tmp, '<w:p><w:r><w:t>普通</w:t></w:r>'
                        '<w:r><w:rPr><w:b/></w:rPr><w:t>加粗</w:t></w:r>%s</w:p>' % CITE)
        seen = []
        process(f11, out, fn=lambda t: (seen.append(t), t)[1], dry_run=True)
        check('不同格式不合并', '普通加粗' not in seen and {'普通', '加粗'} <= set(seen),
              '拿到 %r' % seen)

        print()
        print('=== 三点五 codex 指出的边界 ===')

        # 普通书签跨在中间，文本不能被搬过去
        f13 = make(tmp, '<w:p><w:r><w:t>前半</w:t></w:r>'
                        '<w:bookmarkStart w:id="9" w:name="myref"/>'
                        '<w:r><w:t>被书签框住</w:t></w:r>'
                        '<w:bookmarkEnd w:id="9"/>'
                        '<w:r><w:t>后半</w:t></w:r>%s</w:p>' % CITE)
        seen = []
        process(f13, out, fn=lambda t: (seen.append(t), t)[1], dry_run=True)
        check('普通书签是硬边界', '前半被书签框住后半' not in seen, '拿到 %r' % seen)

        # 批注范围同理
        f14 = make(tmp, '<w:p><w:r><w:t>A</w:t></w:r>'
                        '<w:commentRangeStart w:id="1"/><w:r><w:t>B</w:t></w:r>'
                        '<w:commentRangeEnd w:id="1"/>'
                        '<w:r><w:t>C</w:t></w:r>%s</w:p>' % CITE)
        seen = []
        process(f14, out, fn=lambda t: (seen.append(t), t)[1], dry_run=True)
        check('批注范围是硬边界', 'ABC' not in seen, '拿到 %r' % seen)

        # run 内含脚注锚点，文本不能被搬走
        f15 = make(tmp, '<w:p><w:r><w:t>甲</w:t></w:r>'
                        '<w:r><w:t>乙</w:t><w:footnoteReference w:id="2"/></w:r>'
                        '<w:r><w:t>丙</w:t></w:r>%s</w:p>' % CITE)
        seen = []
        process(f15, out, fn=lambda t: (seen.append(t), t)[1], dry_run=True)
        check('含脚注锚点的 run 不与邻居合并', '甲乙丙' not in seen, '拿到 %r' % seen)
        check('但它的文字仍会被送去改写', '乙' in ''.join(seen), '拿到 %r' % seen)

        # 目标文件已存在
        f16 = make(tmp, body)
        out.write_bytes(b'x')
        refuses('目标已存在时拒绝覆盖', lambda: process(f16, out, fn=lambda t: t), '已存在')
        process(f16, out, fn=lambda t: t, overwrite=True)
        check('传 overwrite=True 才覆盖', out.exists())
        out.unlink()

        # protected_runs 单独调用也自校验
        from zotero_docx import protected_runs as _pr
        bad_xml = ('<w:document xmlns:w="%s"><w:body><w:p>'
                   '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
                   '</w:p></w:body></w:document>' % W)
        refuses('protected_runs 自校验畸形域',
                lambda: _pr(etree.fromstring(bad_xml), Q(W)), '畸形')

        # 膨胀率
        f17 = make(tmp, '<w:p><w:r><w:t>%s</w:t></w:r>%s</w:p>' % ('短句。' * 400, CITE))
        refuses('改写膨胀过头被拒绝',
                lambda: process(f17, out, fn=lambda t: t * 10, overwrite=True), '倍')

        # 表格单元格里的段落不能被重复改写
        from zotero_docx import _segments, protected_runs as _pr2
        tbl = ('<w:document xmlns:w="%s"><w:body>'
               '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>单元格</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
               '<w:p><w:r><w:t>正文</w:t></w:r></w:p></w:body></w:document>' % W)
        rt = etree.fromstring(tbl)
        sg = [x.text for x in _segments(rt, Q(W), _pr2(rt, Q(W)))]
        check('表格内段落不重复进入 segment',
              sg.count('单元格') == 1 and sg.count('正文') == 1, '切出 %r' % sg)

        # sdtContent 直接包 run 时不跨界合并
        sdt = ('<w:document xmlns:w="%s"><w:body><w:p>'
               '<w:r><w:t>前</w:t></w:r>'
               '<w:sdt><w:sdtContent><w:r><w:t>控件内</w:t></w:r></w:sdtContent></w:sdt>'
               '<w:r><w:t>后</w:t></w:r></w:p></w:body></w:document>' % W)
        rt2 = etree.fromstring(sdt)
        sg2 = _segments(rt2, Q(W), _pr2(rt2, Q(W)))
        check('内容控件是硬边界', not any('前控件内后' in x.text for x in sg2),
              '切出 %r' % [x.text for x in sg2])

        # P0：含锚点的 run 写回时不能搬移锚点位置（必须真写回，dry_run 盖不住）
        anc = ('<w:document xmlns:w="%s"><w:body><w:p>'
               '<w:r><w:t>甲</w:t><w:softHyphen/><w:t>乙</w:t></w:r>'
               '</w:p></w:body></w:document>' % W)
        rt3 = etree.fromstring(anc)
        for sg3 in _segments(rt3, Q(W), _pr2(rt3, Q(W))):
            sg3.write_back(sg3.text + 'X')
        xml3 = etree.tostring(rt3, encoding='unicode')
        i_sh = xml3.index('softHyphen')
        check('锚点位置不被搬移',
              xml3.index('甲X') < i_sh < xml3.index('乙X'),
              '实际 %s' % xml3[xml3.index('<w:r'):][:120])

        # 锚点只在末尾时，中间的 w:t 仍应合并（否则被 Word 拆开的词再也替换不到）
        tail = ('<w:document xmlns:w="%s"><w:body><w:p>'
                '<w:r><w:t>Osteo</w:t><w:t>arthritis</w:t>'
                '<w:footnoteReference w:id="2"/></w:r></w:p></w:body></w:document>' % W)
        rt5 = etree.fromstring(tail)
        sg5 = [x.text for x in _segments(rt5, Q(W), _pr2(rt5, Q(W)))]
        check('锚点在末尾时中间仍合并', 'Osteoarthritis' in sg5, '切出 %r' % sg5)

        # P0：文本框嵌套段落只处理一次
        tb = ('<w:document xmlns:w="%s"><w:body><w:p><w:r><w:drawing>'
              '<w:txbxContent><w:p><w:r><w:t>框内</w:t></w:r></w:p></w:txbxContent>'
              '</w:drawing></w:r></w:p></w:body></w:document>' % W)
        rt4 = etree.fromstring(tb)
        sg4 = [x.text for x in _segments(rt4, Q(W), _pr2(rt4, Q(W)))]
        # 断言文本出现次数，不用 id() 去重 —— lxml 代理对象 id 不稳定，
        # 拿它做断言恰好踩了这条测试本来要规避的坑
        check('文本框内文字只被处理一次', sg4.count('框内') == 1, '切出 %r' % sg4)

        # P0：白名单之外的非文本元素也必须当边界（lastRenderedPageBreak 不在旧白名单里）
        lrpb = ('<w:document xmlns:w="%s"><w:body><w:p>'
                '<w:r><w:t>甲</w:t><w:lastRenderedPageBreak/><w:t>乙</w:t></w:r>'
                '</w:p></w:body></w:document>' % W)
        rt6 = etree.fromstring(lrpb)
        for x in _segments(rt6, Q(W), _pr2(rt6, Q(W))):
            x.write_back(x.text + 'X')
        s6 = etree.tostring(rt6, encoding='unicode')
        check('未列举的非文本元素也不被搬移',
              '乙X' in s6 and s6.index('甲X') < s6.index('lastRenderedPageBreak') < s6.index('乙X'),
              s6[s6.index('<w:r'):][:110])

        # P1：嵌在中间层里的 wrapper 也要生效（不能只看直接父节点）
        deep = ('<w:document xmlns:w="%s"><w:body><w:p>'
                '<w:r><w:t>外</w:t></w:r>'
                '<w:sdt><w:sdtContent><w:customXml><w:r><w:t>深层</w:t></w:r></w:customXml>'
                '</w:sdtContent></w:sdt>'
                '<w:r><w:t>面</w:t></w:r></w:p></w:body></w:document>' % W)
        rt7 = etree.fromstring(deep)
        sg7 = [x.text for x in _segments(rt7, Q(W), _pr2(rt7, Q(W)))]
        check('多层包装内的 run 仍被隔离', '外深层面' not in sg7, '切出 %r' % sg7)

        # 文本框内套表格：更深一层嵌套
        deep2 = ('<w:document xmlns:w="%s"><w:body><w:p><w:r><w:drawing><w:txbxContent>'
                 '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>框内表格</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
                 '</w:txbxContent></w:drawing></w:r></w:p></w:body></w:document>' % W)
        rt8 = etree.fromstring(deep2)
        sg8 = [x.text for x in _segments(rt8, Q(W), _pr2(rt8, Q(W)))]
        check('文本框套表格只处理一次', sg8.count('框内表格') == 1, '切出 %r' % sg8)

        # 自带的修订 fixture，不依赖外部样本
        f20 = make(tmp, '<w:p><w:ins w:id="1" w:author="a"><w:r><w:t>新增文字</w:t></w:r></w:ins>'
                        '<w:r><w:t>正文</w:t></w:r>%s</w:p>' % CITE)
        refuses('自带修订样本默认被拒绝', lambda: process(f20, out, fn=lambda t: t), '修订')
        rr = process(f20, out, fn=lambda t: t.replace('正文', '改过'),
                     allow_revisions=True, overwrite=True)
        check('显式放行后能改', len(rr['changes']) > 0)
        out.unlink()

        # dry_run 只是预览，不该被修订检查拦住
        f21 = make(tmp, '<w:p><w:ins w:id="1"><w:r><w:t>新增</w:t></w:r></w:ins>'
                        '<w:r><w:t>正文</w:t></w:r>%s</w:p>' % CITE)
        try:
            rr2 = process(f21, out, fn=lambda t: t, dry_run=True)
            check('dry_run 不被修订检查拦住', rr2['written'] is False)
        except Refused as e:
            check('dry_run 不被修订检查拦住', False, str(e)[:40])

        # fn 返回值类型
        f22 = make(tmp, body)
        for bad, label in ((123, '数字'), (b'x', 'bytes'), (['a'], '列表')):
            refuses('改写函数返回%s被拒绝' % label,
                    lambda b=bad: process(f22, out, fn=lambda t: b, overwrite=True),
                    '必须返回 str')

        # 反向判断不能切过头：只有真正的位置元素才断开
        def segtext(inner):
            rr = etree.fromstring('<w:document xmlns:w="%s"><w:body><w:p>%s</w:p>'
                                  '</w:body></w:document>' % (W, inner))
            return [x.text for x in _segments(rr, Q(W), _pr2(rr, Q(W)))]

        check('纯文本多片段仍合并',
              segtext('<w:r><w:t>Osteo</w:t><w:t>arthritis</w:t></w:r>') == ['Osteoarthritis'])
        check('rPr 不算位置边界',
              segtext('<w:r><w:rPr><w:b/></w:rPr><w:t>Osteo</w:t>'
                      '<w:t>arthritis</w:t></w:r>') == ['Osteoarthritis'])
        check('末尾的分页标记不影响合并',
              segtext('<w:r><w:t>Osteo</w:t><w:t>arthritis</w:t>'
                      '<w:lastRenderedPageBreak/></w:r>') == ['Osteoarthritis'])
        check('delText 算位置边界',
              segtext('<w:r><w:t>Osteo</w:t><w:delText>x</w:delText>'
                      '<w:t>arthritis</w:t></w:r>') == ['Osteo', 'arthritis'])

        # 关系校验：带 URL 编码的 Target 不能被误判成断链
        f24 = make(tmp, body, extra={
            'word/_rels/document.xml.rels':
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
                'relationships"><Relationship Id="rId1" Type="http://x" '
                'Target="media/my%20image.png"/></Relationships>',
            'word/media/my image.png': 'x'})
        try:
            process(f24, out, fn=lambda t: t.replace('正文', '改后'), overwrite=True)
            check('关系 Target 的百分号编码被正确解码', True)
            out.unlink()
        except Refused as e:
            check('关系 Target 的百分号编码被正确解码', False, str(e)[:50])

        # 关系真的断了要能查出来
        f25 = make(tmp, body, extra={
            'word/_rels/document.xml.rels':
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
                'relationships"><Relationship Id="rId1" Type="http://x" '
                'Target="media/missing.png"/></Relationships>'})
        refuses('断掉的关系被查出',
                lambda: process(f25, out, fn=lambda t: t.replace('正文', '改后'),
                                overwrite=True), '关系断了')

        # 关系目标的各种 URI 形式都要解析对
        from zotero_docx import _resolve_target
        for base, raw, expect in (
                ('word', 'media/img.png', 'word/media/img.png'),
                ('word', 'media/my%20i.png', 'word/media/my i.png'),
                ('word', '../docProps/core.xml', 'docProps/core.xml'),
                ('', 'docProps/app.xml', 'docProps/app.xml'),
                ('word', '/word/media/abs.png', 'word/media/abs.png'),
                ('word', 'media/x.png#frag', 'word/media/x.png'),
                ('word', 'media/x.png?v=2', 'word/media/x.png'),
                ('word', 'media/a%20b.png?v=1#f', 'word/media/a b.png')):
            got = _resolve_target(base, raw)
            check('Target 解析 %s' % raw, got == expect, '得到 %s' % got)

        # 移动型修订也算未处理的修订
        for rev in ('moveFrom', 'moveTo'):
            f_mv = make(tmp, '<w:p><w:%s w:id="1"><w:r><w:t>挪动的字</w:t></w:r></w:%s>'
                             '<w:r><w:t>正文</w:t></w:r>%s</w:p>' % (rev, rev, CITE))
            r_mv = precheck(f_mv)
            check('%s 被识别为修订' % rev, r_mv['has_revisions'] is True)

        # 已签名文档拒绝处理
        f26 = make(tmp, body, extra={'_xmlsignatures/sig1.xml': '<sig/>'})
        refuses('已签名文档被拒绝（按路径）', lambda: precheck(f26), '签名')

        # 签名部件放在别的位置，靠内容类型识别
        ct_signed = CT.replace('</Types>',
                               '<Override PartName="/sig/s.xml" ContentType='
                               '"application/vnd.openxmlformats-package.'
                               'digital-signature-xmlsignature+xml"/></Types>')
        f27 = make(tmp, body, extra={'sig/s.xml': '<sig/>'})
        with zipfile.ZipFile(f27, 'a') as z:
            pass
        import shutil as _sh
        f27b = Path(tmp) / 'signed2.docx'
        with zipfile.ZipFile(f27) as zi, zipfile.ZipFile(f27b, 'w') as zo:
            for it in zi.namelist():
                zo.writestr(it, ct_signed if it == '[Content_Types].xml' else zi.read(it))
        refuses('已签名文档被拒绝（按内容类型）', lambda: precheck(f27b), '签名')

        # 产出包的结构保真：条目、顺序、压缩方式、关系
        f23 = make(tmp, body)
        process(f23, out, fn=lambda t: t.replace('正文', '改后'), overwrite=True)
        za, zb = zipfile.ZipFile(f23), zipfile.ZipFile(out)
        check('包内条目与顺序不变', za.namelist() == zb.namelist())
        ca = {i.filename: i.compress_type for i in za.infolist()}
        cb = {i.filename: i.compress_type for i in zb.infolist()}
        check('压缩方式不变', ca == cb)
        out.unlink()

        # P1：域缺 separate 要被拒绝
        f18 = make(tmp, '<w:p><w:r><w:fldChar w:fldCharType="begin"/></w:r>'
                        '<w:r><w:instrText> ADDIN ZOTERO_ITEM CSL_CITATION {} </w:instrText></w:r>'
                        '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
        refuses('域缺 separate 被拒绝', lambda: precheck(f18), 'separate')

        # P1：单个片段膨胀不能被别的片段抵消
        long_body = ('<w:p><w:r><w:t>%s</w:t></w:r><w:r><w:rPr><w:b/></w:rPr>'
                     '<w:t>%s</w:t></w:r>%s</w:p>' % ('正常句子。' * 200, '短片段内容' * 5, CITE))
        f19 = make(tmp, long_body)

        def blow_one(t):
            return t * 20 if t.startswith('短片段') else t[:len(t) // 2]

        refuses('单片段膨胀不被整体抵消',
                lambda: process(f19, out, fn=blow_one, overwrite=True,
                                allow_heavy_rewrite=True), '倍')

        print()
        print('=== 四 换样式 ===')
        f12 = make(tmp, body)
        NEW = 'http://www.zotero.org/styles/china-national-standard-gb-t-7714-2015-numeric'
        process(f12, out, new_style=NEW)
        with zipfile.ZipFile(out) as z:
            prefs = _read_prefs(z)
            txt = z.read('word/document.xml').decode()
        check('样式已更换', NEW in prefs)
        check('偏好 XML 仍闭合', prefs.endswith('</data>'))
        check('换样式不动正文域', txt.count('ZOTERO_ITEM') == 1)
        out.unlink()

        print()
        print('=== 五 真实论文回归 ===')
        real = Path('/root/upload/分子分型文章修订/20260714LZY revised-分子分型20260710.docx')
        if real.exists():
            rep = precheck(real)
            check('真实论文体检通过', rep['fields'] == 37 and rep['bibl'] == 1,
                  '域 %d 文献表 %d 有修订 %s' % (rep['fields'], rep['bibl'], rep['has_revisions']))
            # 这篇带修订标记，默认会被拒绝 —— 先验证这个保护有效
            refuses('带修订的文档默认拒绝改写',
                    lambda: process(real, out, fn=lambda t: t), '修订')
            r = process(real, out, fn=lambda t: t.replace('leading cause', 'major cause'),
                        allow_revisions=True)
            rep2 = precheck(out)
            check('改写后域数不变', rep2['fields'] == rep['fields'],
                  '%d -> %d' % (rep['fields'], rep2['fields']))
            check('确实改到了东西', len(r['changes']) > 0, '%d 处' % len(r['changes']))
            out.unlink()
        else:
            check('真实论文回归', True, '样本不在，跳过')

    print()
    bad = [n for n, ok in RESULTS if not ok]
    print('%d 项，通过 %d，失败 %d' % (len(RESULTS), len(RESULTS) - len(bad), len(bad)))
    if bad:
        print('失败项:', bad)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
