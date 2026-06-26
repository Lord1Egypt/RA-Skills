import os
import re
import sys
from docx import Document
from docx.text.paragraph import Paragraph
from docx.oxml import OxmlElement


# =============================================================================
# Phase 1: Parse summary MD
# =============================================================================
def parse_summary_md(content):
    """Parse news summary MD into structured data dict."""
    data = {}
    lines = content.splitlines()

    blocks = []
    current = []
    blank_count = 0
    for raw_line in content.splitlines(keepends=True):
        stripped = raw_line.strip()
        is_bracket_start = stripped.startswith('\uff08') or stripped.startswith('(')
        if stripped:
            if blank_count >= 1 or (is_bracket_start and current):
                if current:
                    blocks.append(current)
                current = []
            blank_count = 0
            current.append(stripped)
        else:
            blank_count += 1
    if current:
        blocks.append(current)

    for block in blocks:
        for idx, line in enumerate(block):
            if line.startswith('\u62df\u6295\u680f\u76ee\uff1a'):
                data['Category'] = line[len('\u62df\u6295\u680f\u76ee\uff1a'):].strip()
            elif line.startswith('\u4e8b\u4ef6\u65f6\u95f4\uff1a'):
                data['EventDate'] = line[len('\u4e8b\u4ef6\u65f6\u95f4\uff1a'):].strip()
            elif line.startswith('\u4ef7\u503c\u70b9\uff1a'):
                parts = []
                for sub in block[idx:]:
                    parts.append(sub[len('\u4ef7\u503c\u70b9\uff1a'):].strip() if sub.startswith('\u4ef7\u503c\u70b9\uff1a') else sub.strip())
                data['ValuePoint'] = ''.join(parts).strip()
                break

    non_meta_blocks = [
        b for b in blocks
        if b
        and not b[0].startswith('\u62df\u6295\u680f\u76ee')
        and not b[0].startswith('\u4e8b\u4ef6\u65f6\u95f4')
        and not b[0].startswith('\u4ef7\u503c')
    ]

    footer_blocks = []
    while non_meta_blocks:
        last_block = non_meta_blocks[-1]
        last_line = ' '.join(last_block).strip()
        has_phone = bool(re.search(r'\d{11}', last_line))
        keyword_hit = (
            last_line.startswith('\uff08') or last_line.startswith('(')
            or last_line.endswith('\uff09') or last_line.endswith(')')
            or '\u6765\u6e90\uff1a' in last_line or '\u6765\u6e90:' in last_line
            or '\u7814\u7a76\u9662' in last_line or '\u79d1\u5b66\u9662' in last_line
            or '\u5355\u4f4d' in last_line or '\u4f5c\u8005' in last_line
        )
        is_footer = has_phone or (len(last_line) <= 50 and keyword_hit)
        if is_footer:
            footer_blocks.insert(0, last_block)
            non_meta_blocks.pop()
        else:
            break

    main_blocks = non_meta_blocks
    if main_blocks:
        title_block = main_blocks[0]
        title_line = ' '.join(title_block)
        data['MainTitle'] = title_line
        data['SubTitle'] = ''
        body_blocks = main_blocks[1:]
        if body_blocks:
            data['Body'] = '\n'.join(' '.join(b) for b in body_blocks)
        else:
            data['Body'] = ''
    else:
        data['MainTitle'] = 'No title found'
        data['SubTitle'] = ''
        data['Body'] = ''

    data['OrgUnit'] = ''
    data['Author'] = ''
    data['Phone'] = ''
    data['SourceMedia'] = ''
    data['SourceDate'] = ''
    data['ReviewUnit'] = ''
    data['ReviewDate'] = '2026\u5e746\u67083\u65e5'
    data['has_footer'] = False

    if footer_blocks:
        data['has_footer'] = True
        footer_text = ' '.join([' '.join(b) for b in footer_blocks]).strip()
        footer_text = footer_text.replace('(', '\uff08').replace(')', '\uff09').replace(':', '\uff1a').replace(',', '\uff0c')

        segments = [s.strip() for s in re.split(r'\uff08|\uff09', footer_text) if s.strip()]

        for seg in segments:
            if '\u6765\u6e90\uff1a' in seg or '\u6765\u6e90' in seg:
                inner = seg.replace('\u6765\u6e90\uff1a', '').replace('\u6765\u6e90', '').strip()
                parts = inner.split('\uff0c')
                data['SourceMedia'] = parts[0].strip() if len(parts) > 0 else ''
                data['SourceDate'] = parts[1].strip() if len(parts) > 1 else ''
            elif re.search(r'\d{11}', seg):
                parts = seg.split('\uff0c')
                data['OrgUnit'] = parts[0].strip() if len(parts) > 0 else ''
                data['Author'] = parts[1].strip() if len(parts) > 1 else ''
                data['Phone'] = parts[2].strip() if len(parts) > 2 else ''
            elif '\u7814\u7a76\u9662' in seg or '\u79d1\u5b66\u9662' in seg or '\u4e2d\u5fc3' in seg or '\u6240' in seg:
                parts = seg.split('\uff0c')
                if data['OrgUnit']:
                    data['ReviewUnit'] = parts[0].strip() if len(parts) > 0 else ''
                    if len(parts) > 1 and '\u5ba1\u5b9a' in last_line:
                        data['ReviewDate'] = parts[1].strip()
                else:
                    data['OrgUnit'] = parts[0].strip() if len(parts) > 0 else ''
                    if len(parts) > 1:
                        data['Author'] = parts[1].strip()
                    if len(parts) > 2:
                        data['Phone'] = parts[2].strip()

    defaults = {
        'Category': '', 'EventDate': '', 'ValuePoint': '',
        'MainTitle': 'No title found', 'SubTitle': '',
        'Body': '',
    }
    for k, v in defaults.items():
        if k not in data:
            data[k] = v

    data['AuthorLine'] = _build_author_line(data)
    return data


def _build_author_line(data):
    """Assemble the footer author line for summary docs."""
    parts = []
    if data.get('OrgUnit'):
        parts.append(data['OrgUnit'])
    if data.get('Author'):
        parts.append(data['Author'])
    if data.get('Phone'):
        parts.append(data['Phone'])
    if data.get('SourceMedia') or data.get('SourceDate'):
        src_parts = []
        if data.get('SourceMedia'):
            src_parts.append('\u6765\u6e90\uff1a' + data['SourceMedia'])
        if data.get('SourceDate'):
            src_parts.append(data['SourceDate'])
        parts.append('\uff08' + '\uff0c'.join(src_parts) + '\uff09')
    if data.get('ReviewUnit'):
        parts.append('\uff08' + data['ReviewUnit'])
        if data.get('ReviewDate'):
            parts[-1] += '\uff0c' + data['ReviewDate']
        parts[-1] += '\uff09'
    return '\u3001'.join(parts)


# =============================================================================
# Phase 2: Parse original MD
# =============================================================================
def parse_original_md(content):
    """Parse news original-article MD into structured data dict."""
    data = {
        'Title': '',
        'SourceDate': '',
        'SourceMedia': '',
        'Author': '',
        'Body': '',
        'SourceLink': '',
        'SerialHeader': '',
    }

    lines = [line.strip() for line in content.split('\n')]
    if lines and (lines[0].startswith("\u539f\u6587\u7a3f") or lines[0].startswith("\u539f\u6587")):
        colon_pos = lines[0].find('\uff1a')
        if colon_pos > 0:
            data['SerialHeader'] = lines[0][:colon_pos + 1]
            lines[0] = lines[0][colon_pos + 1:]
        else:
            data['SerialHeader'] = lines[0].rstrip('\uff1a')
            lines = lines[1:]
    lines = [l for l in lines if l]

    if not lines:
        return data

    data['Title'] = lines[0]
    body_start_idx = 1
    body_end_idx = len(lines)

    if (len(lines) > 1
            and ("\u3010\u6587/" in lines[1] or re.search(r'\d{4}-\d{2}-\d{2}', lines[1]))):
        line2 = lines[1]
        date_match = re.search(r'(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)', line2)
        if date_match:
            data['SourceDate'] = date_match.group(1)

        ROLE_WORDS = ('\u8bb0\u8005', '\u7f16\u8f91', '\u603b\u53f0', '\u7279\u7ea6',
                      '\u64b0\u7a3f', '\u901a\u8baf\u5458', '\u8bc4\u8bba\u5458',
                      '\u4e3b\u7ba1', '\u7f16\u5ba1')

        def strip_role(text):
            for w in ROLE_WORDS:
                text = re.sub(rf'\s*{re.escape(w)}\s*', '', text)
            return text.strip()

        raw = line2.replace('\u3010\u6587/', '').rstrip('\u3011').strip()
        slash_pos = raw.find('/')
        comma_pos = raw.find('\uff0c')
        if comma_pos >= 0 and (slash_pos < 0 or comma_pos < slash_pos):
            sep_pos = comma_pos
        elif slash_pos >= 0:
            sep_pos = slash_pos
        else:
            sep_pos = -1
        if sep_pos >= 0:
            author_part = raw[:sep_pos].strip()
            media_part = raw[sep_pos + 1:].strip()
            if '/' in media_part:
                media_part = media_part.split('/')[-1].strip()
        else:
            MEDIA_RE = re.compile(r'(\u7f51|\u62a5|\u793e|\u53f0|\u6742\u5fd7|\u5468\u520a|\u6708\u520a)$')
            tokens = re.split(r'[\s\uff0c,\u3001]+', raw)
            for i in range(len(tokens) - 1, -1, -1):
                if MEDIA_RE.search(tokens[i]):
                    media_part = ''.join(tokens[i:]).strip()
                    author_part = ''.join(tokens[:i]).strip()
                    break
            else:
                author_part = raw
                media_part = ''
        data['Author'] = strip_role(author_part)
        data['SourceMedia'] = strip_role(media_part)
        body_start_idx = 2

    if "\u539f\u6587\u94fe\u63a5\uff1a" in lines[-1]:
        data['SourceLink'] = lines[-1].replace("\u539f\u6587\u94fe\u63a5\uff1a", "").strip()
        body_end_idx -= 1

    if body_end_idx > body_start_idx:
        last_line = lines[body_end_idx - 1]
        if (last_line.startswith("\uff08") or last_line.startswith("(")) and (
                last_line.endswith("\uff09") or last_line.endswith(")")):
            footer_text = last_line[1:-1].strip()
            if "\u8bb0\u8005" in footer_text:
                data['Author'] = footer_text
                if "\u603b\u53f0" in footer_text:
                    data['SourceMedia'] = "\u4e2d\u592e\u5e7f\u64ad\u7535\u89c6\u603b\u53f0"
            else:
                data['Author'] = footer_text
            body_end_idx -= 1

    para_lines = content.split('\n')
    body_para_segments = []
    current_para = []
    for pl in para_lines:
        stripped = pl.strip()
        if stripped:
            current_para.append(stripped)
        else:
            if current_para:
                body_para_segments.append(' '.join(current_para))
                current_para = []
    if current_para:
        body_para_segments.append(' '.join(current_para))

    body_raw_lines = lines[body_start_idx:body_end_idx]
    body_raw_set = set(body_raw_lines)
    data['Body'] = '\n'.join(
        seg for seg in body_para_segments
        if any(ln in seg for ln in body_raw_set)
    )

    data['SourceDate'] = _normalize_date(data['SourceDate'])
    if not data['SourceMedia']:
        data['SourceMedia'] = "\u673a\u5668\u4e4b\u5fc3"
    if not data['Author']:
        data['Author'] = "\u7f16\u8f91"

    return data


def _normalize_date(date_str):
    """Normalize date: 2026-06-01 -> 2026\u5e746\u67083\u65e5"""
    if not date_str:
        return date_str
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', date_str)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"{y}\u5e74{mo}\u6708{d}\u65e5"
    return date_str


# =============================================================================
# Phase 3: Replace placeholders in DOCX template
# =============================================================================
def replace_docx_template(template_path, output_path, data):
    """Replace {{FieldName}} placeholders in template and save as output."""
    from lxml import etree

    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    WN = f'{{{W}}}'

    doc = Document(template_path)

    for paragraph in doc.paragraphs:
        p_xml = paragraph._p

        runs = p_xml.findall(f'{WN}r')
        all_text = ''.join(r.text or '' for r in runs)

        while True:
            matches = list(re.finditer(r'\{\{(\w+)\}\}', all_text))
            if not matches:
                break

            m = matches[-1]
            key = m.group(1)
            if key not in data:
                break
            value = str(data[key])
            start, end = m.start(), m.end()

            acc = 0
            sri, eri = -1, -1
            rel_start = rel_end = -1
            for ri, run in enumerate(runs):
                rl = len(run.text or '')
                if start < acc + max(rl, 1) and sri == -1:
                    sri = ri
                    rel_start = start - acc
                if end - 1 < acc + max(rl, 1) and eri == -1:
                    eri = ri
                    rel_end = end - acc - 1
                acc += rl
            if sri == -1 or eri == -1:
                break

            body_key = 'Body'
            if key == body_key and '\n' in value:
                parts = [p.strip() for p in value.split('\n') if p.strip()]

                s_text = runs[sri].text or ''
                if sri == eri:
                    runs[sri].text = s_text[:rel_start] + parts[0] + s_text[rel_end + 1:]
                else:
                    e_text = runs[eri].text or ''
                    runs[sri].text = s_text[:rel_start] + parts[0]
                    runs[eri].text = e_text[rel_end + 1:]
                    for ri in range(sri + 1, eri):
                        runs[ri].text = ''

                current_p = p_xml
                for part in parts[1:]:
                    new_p = OxmlElement('w:p')
                    pPr = p_xml.find(f'{WN}pPr')
                    if pPr is not None:
                        new_p.append(etree.fromstring(etree.tostring(pPr)))
                    new_r = etree.SubElement(new_p, f'{WN}r')
                    rPr = runs[sri].find(f'{WN}rPr')
                    if rPr is not None:
                        new_r.append(etree.fromstring(etree.tostring(rPr)))
                    new_t = etree.SubElement(new_r, f'{WN}t')
                    new_t.text = part
                    new_t.set(f'{WN}space', 'preserve')
                    current_p.addnext(new_p)
                    current_p = new_p
            else:
                if sri == eri:
                    run_text = runs[sri].text or ''
                    runs[sri].text = run_text[:rel_start] + value + run_text[rel_end + 1:]
                else:
                    s_text = runs[sri].text or ''
                    e_text = runs[eri].text or ''
                    runs[sri].text = s_text[:rel_start] + value
                    runs[eri].text = e_text[rel_end + 1:]
                    for ri in range(sri + 1, eri):
                        runs[ri].text = ''

            runs = p_xml.findall(f'{WN}r')
            all_text = ''.join(r.text or '' for r in runs)

    doc.save(output_path)
    print(f"[OK] Saved: {output_path}")


# =============================================================================
# Entry point
# =============================================================================
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if len(sys.argv) > 1:
        md_files = [os.path.abspath(f) for f in sys.argv[1:]]
    else:
        md_files = []
        for f in os.listdir(script_dir):
            if f.endswith('.md') and ('\u79d1\u6280\u65b0\u95fb\u539f\u6587' in f or '\u79d1\u6280\u65b0\u95fb\u6458\u8981' in f):
                md_files.append(os.path.join(script_dir, f))
        md_files.sort()

    if not md_files:
        print("No tech-news MD files found!")
        sys.exit(1)

    for md_file in md_files:
        basename = os.path.basename(md_file)
        if "\u6458\u8981" in basename:
            template_file = os.path.join(script_dir, "template-summary.docx")
            parser = parse_summary_md
        else:
            template_file = os.path.join(script_dir, "template-original.docx")
            parser = parse_original_md

        output_file = md_file.replace(".md", ".docx")

        if not os.path.exists(template_file):
            print(f"[Skip] Template not found: {template_file}")
            continue
        if not os.path.exists(md_file):
            print(f"[Skip] MD file not found: {md_file}")
            continue

        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        payload = parser(md_content)
        replace_docx_template(template_file, output_file, payload)
