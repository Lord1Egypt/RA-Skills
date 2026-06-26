#!/usr/bin/env python3
"""
印象笔记 -> Obsidian 增量同步脚本

判断逻辑：
- 资源有 fileName+扩展名  → 附件笔记，存入 _attachments/
- 资源无 fileName，有 en-media 内嵌图片  → 内嵌图片笔记，转 Markdown + 附件 section
- 资源无 fileName，div+span≥3 且 < 5KB  → 短网页片段，转 Markdown
- 资源无 fileName，div+span≥3 且 ≥ 5KB 且是纯 HTML（无用户手写内容） → 存 HTML 进 _clips/
- 其余  → 转 Markdown
"""

import sys, os, json, time, hashlib, re, argparse
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from list_notebooks import load_config
import evernote.edam.notestore.NoteStore as NoteStore
import thrift.transport.THttpClient as THttpClient
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import html as html_module
from datetime import datetime
import html2text

# ─── 配置 ────────────────────────────────────────────────
VAULT_PATH = r"C:\Users\adun\Documents\印象笔记同步"
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.sync_state.json')
MAX_SYNC_PER_RUN = 50
TARGET_NOTEBOOK = None  # 只同步此笔记本，None 表示全部同步
API_DELAY = 1.0
CLIP_SIZE_THRESHOLD = 200 * 1024  # 200KB 网页片段阈值
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp', '.ico'}


# ─── 工具函数 ──────────────────────────────────────────────

def safe_filename(name):
    return re.sub(r'[\\/:*?"<>|]', '_', name) or 'untitled'


def resource_has_filename(res):
    """检查资源是否有原始文件名（最关键的判断条件）"""
    if not hasattr(res, 'attributes') or not res.attributes:
        return False
    fname = getattr(res.attributes, 'fileName', None)
    if not fname:
        return False
    # 有文件名且带扩展名 → 是真实附件
    _, ext = os.path.splitext(fname)
    return bool(ext)


def get_resource_filename(res):
    """获取资源的原始文件名，无则返回 None"""
    if not hasattr(res, 'attributes') or not res.attributes:
        return None
    return getattr(res.attributes, 'fileName', None)


def extract_resources(note):
    """提取所有附件，返回 {hash: {filename, data, mime}}"""
    # 已知的 MIME type → 扩展名映射
    MIME_EXT_MAP = {
        'image/png': '.png', 'image/jpeg': '.jpg',
        'image/gif': '.gif', 'image/webp': '.webp',
        'image/svg+xml': '.svg', 'application/pdf': '.pdf',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
        'application/vnd.ms-excel': '.xls',
        'application/msword': '.doc',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    }
    KNOWN_EXTS = set(MIME_EXT_MAP.values())
    
    resources = {}
    if not hasattr(note, 'resources') or not note.resources:
        return resources
    for res in note.resources:
        if not hasattr(res, 'data') or not res.data or not res.data.body:
            continue
        mime = getattr(res, 'mime', 'application/octet-stream')
        data = res.data.body
        h = hashlib.md5(data).hexdigest()

        # 优先用原始文件名，否则用 hash
        orig_name = get_resource_filename(res)
        if orig_name:
            safe_name = safe_filename(orig_name)
            _, ext = os.path.splitext(orig_name)
            # 如果扩展名不是已知类型，根据 MIME 添加正确的扩展名
            if ext.lower() not in KNOWN_EXTS:
                correct_ext = MIME_EXT_MAP.get(mime, '')
                if correct_ext:
                    safe_name += correct_ext
            filename = safe_name
        else:
            # 无文件名 → inline 资源，用 hash 做文件名
            ext = MIME_EXT_MAP.get(mime, '')
            filename = h + ext

        h = hashlib.md5(data).hexdigest()
        resources[h] = {'filename': filename, 'data': data, 'mime': mime, 'hash': h}
    return resources


def save_attachments(resources, attachments_dir):
    """保存附件到目录（按文件名，hash 去重）"""
    saved = {}
    for h, res in resources.items():
        fp = os.path.join(attachments_dir, res['filename'])
        if not os.path.exists(fp):
            with open(fp, 'wb') as f:
                f.write(res['data'])
        saved[h] = res['filename']
    return saved


def make_attachment_link(fname):
    """根据文件类型生成正确的 Markdown 链接格式"""
    ext = os.path.splitext(fname)[1].lower()
    if ext in IMAGE_EXTS:
        return f'![{fname}](_attachments/{fname})'
    else:
        return f'[{fname}](_attachments/{fname})'


def make_attachments_section(hash_to_file):
    """生成附件列表 section"""
    if not hash_to_file:
        return ''
    lines = ['\n---\n', '## 附件\n']
    for fname in hash_to_file.values():
        ext = os.path.splitext(fname)[1].lower()
        if ext in IMAGE_EXTS:
            lines.append(f'![{fname}](_attachments/{fname})')
        else:
            lines.append(f'- [{fname}](_attachments/{fname})')
    return '\n'.join(lines)


def is_enml_clip(content):
    """检查 ENML 内容是否有网页裁剪属性（更可靠的判断）"""
    if not content:
        return False
    return '--en-clipped-content' in content


def is_web_clip_by_content(content):
    """通过内容结构判断是否为网页裁剪（用于无 fileName 的资源）"""
    if not content:
        return False
    return (content.count('<div') + content.count('<span') +
            content.count('<script') + content.count('<style')) >= 3


def has_en_media(content):
    """检查内容是否包含 en-media 标签（内嵌图片等资源）"""
    if not content:
        return False
    return bool(re.search(r'<en-media[^>]*hash="[a-f0-9]{32}"', content))


def enml_to_markdown(enml_content):
    """ENML 纯文本笔记转 Markdown"""
    if not enml_content:
        return ""
    c = enml_content
    c = re.sub(r'<\?xml[^?]*\?>', '', c)
    c = re.sub(r'<!DOCTYPE[^>]*>', '', c)
    c = re.sub(r'<en-note[^>]*>', '', c)
    c = re.sub(r'</en-note>', '', c)
    c = re.sub(r'<br\/?>', '\n', c)
    c = re.sub(r'<p[^>]*>', '', c)
    c = re.sub(r'</p>', '\n\n', c)
    c = re.sub(r'<li[^>]*>', '- ', c)
    c = re.sub(r'</li>', '\n', c)
    for tag in ['b', 'strong', 'i', 'em', 'u']:
        c = re.sub(f'<{tag}[^>]*>(.*?)</{tag}>', r'\1', c, flags=re.DOTALL)
    c = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n', c, flags=re.DOTALL)
    c = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n', c, flags=re.DOTALL)
    c = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n', c, flags=re.DOTALL)
    c = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', c, flags=re.DOTALL)
    c = html_module.unescape(c)
    c = re.sub(r'\n{3,}', '\n\n', c)
    return c.strip()


def html_to_md(content, hash_to_file):
    """ENML 网页裁剪内容转 Markdown（使用 html2text）"""
    if not content:
        return ""

    IMAGE_EXTS_LOCAL = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp'}

    def en_media_to_img(m):
        h = m.group(1)
        if hash_to_file and h in hash_to_file:
            fname = hash_to_file[h]
            ext = os.path.splitext(fname)[1].lower()
            if ext in IMAGE_EXTS_LOCAL:
                return f'<img src="_attachments/{fname}" alt="{fname}">'
            else:
                return f'<a href="_attachments/{fname}">{fname}</a>'
        return f'<img src="_attachments/{h}" alt="{h}">'

    def replace_en_media(c):
        for m in re.finditer(r'<en-media[^>]*hash="([a-f0-9]{32})"', c):
            h = m.group(1)
            img_tag = en_media_to_img(m)
            start = m.start()
            end = c.find('</en-media>', start)
            if end == -1:
                end = c.find('/>', start)
                if end == -1:
                    continue
                end += 2
            else:
                end += len('</en-media>')
            c = c[:start] + img_tag + c[end:]
            break
        return c

    c = content
    c = re.sub(r'<img[^>]*src="data:image/svg\+xml[^"]*"[^>]*/?\s*>', '', c)
    c = re.sub(r'<img[^>]*src="data:image/svg\+xml[^"]*"[^>]*>\s*</img>', '', c)
    for _ in range(100):
        new_c = replace_en_media(c)
        if new_c == c:
            break
        c = new_c
    c = re.sub(r'<\?xml[^?]*\?>', '', c)
    c = re.sub(r'<!DOCTYPE[^>]*>', '', c)
    c = re.sub(r'<en-note[^>]*>', '<div>', c)
    c = re.sub(r'</en-note>', '</div>', c)
    c = re.sub(r'<en-todo[^>]*checked="true"[^>]*>', '[x] ', c)
    c = re.sub(r'<en-todo[^>]*>', '[ ] ', c)
    c = re.sub(r'</en-todo>', '', c)

    h2t = html2text.HTML2Text()
    h2t.body_width = 0
    h2t.ignore_links = False
    h2t.ignore_images = False
    h2t.unescape = True
    md = h2t.handle(c)
    md = re.sub(r'\n{3,}', '\n\n', md)
    md = re.sub(r'(\]\([\s\S]*?\))([^)\n]*)\!\[' , r'\1\2\n\n![' , md)
    md = re.sub(r'(\]\([\s\S]*?\))([^\n])', r'\1\n\n\2', md)
    md = re.sub(r'[ \t]+\n', '\n', md)
    md = re.sub(r'\n[ \t]+', '\n', md)
    return md.strip()


def make_clip_html(enml_content, hash_to_file=None):
    """ENML 内容转纯 HTML 文件（en-media 替换为 <img> 标签）"""
    IMAGE_EXTS_LOCAL = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp'}

    def en_media_to_img_full(m):
        h = m.group(1)
        if hash_to_file and h in hash_to_file:
            fname = hash_to_file[h]
            ext = os.path.splitext(fname)[1].lower()
            if ext in IMAGE_EXTS_LOCAL:
                return f'<img src="../_attachments/{fname}" alt="{fname}">'
            else:
                return f'<a href="../_attachments/{fname}">{fname}</a>'
        return f'<img src="../_attachments/{h}" alt="{h}">'

    def replace_en_media_html(c):
        for m in re.finditer(r'<en-media[^>]*hash="([a-f0-9]{32})"', c):
            h = m.group(1)
            img_tag = en_media_to_img_full(m)
            start = m.start()
            end = c.find('</en-media>', start)
            if end == -1:
                end = c.find('/>', start)
                if end == -1:
                    continue
                end += 2
            else:
                end += len('</en-media>')
            c = c[:start] + img_tag + c[end:]
            break
        return c

    c = enml_content
    for _ in range(100):
        new_c = replace_en_media_html(c)
        if new_c == c:
            break
        c = new_c
    c = re.sub(r'<\?xml[^?]*\?>', '', c)
    c = re.sub(r'<!DOCTYPE[^>]*>', '', c)
    c = re.sub(r'<en-note[^>]*>', '<div>', c)
    c = re.sub(r'</en-note>', '</div>', c)
    return c.strip()


def frontmatter(title, nb_name, guid, created, updated, extra=None):
    fm = f"---\ntitle: {title}\ncreated: {created.strftime('%Y-%m-%d %H:%M:%S')}\nupdated: {updated.strftime('%Y-%m-%d %H:%M:%S')}\nsource: Evernote\nsource_guid: {guid}\nnotebook: {nb_name}\n"
    if extra:
        fm += extra + "\n"
    fm += "---\n\n"
    return fm


# ─── 状态管理 ──────────────────────────────────────────────

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {'last_sync': None, 'synced_guids': {}, 'progress': {'notebook_idx': 0, 'note_idx': 0}}


def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def scan_local_vault():
    guid_map = {}
    for root, dirs, files in os.walk(VAULT_PATH):
        dirs[:] = [d for d in dirs if d != '.obsidian']
        for file in files:
            if not file.endswith('.md'):
                continue
            fp = os.path.join(root, file)
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                mtime_ms = int(os.path.getmtime(fp) * 1000)
                guid = None
                if content.startswith('---'):
                    end = content.find('---', 3)
                    if end > 0:
                        for line in content[3:end].splitlines():
                            if line.startswith('source_guid:'):
                                guid = line.split(':', 1)[1].strip()
                                break
                if guid:
                    guid_map[guid] = {'file': fp, 'local_updated_ms': mtime_ms}
            except Exception:
                continue
    return guid_map


# ─── 主同步 ────────────────────────────────────────────────

def sync_to_obsidian():
    print("=" * 60)
    print("🔄 印象笔记 -> Obsidian 增量同步")
    print("=" * 60)
    print(f"目标: {VAULT_PATH}")
    print(f"本次上限: {MAX_SYNC_PER_RUN} 条 | HTML片段阈值: {CLIP_SIZE_THRESHOLD // 1024} KB")
    print()

    token, note_store_url = load_config()
    if not token:
        print("❌ 错误: 未找到 EVERNOTE_TOKEN")
        return

    transport = THttpClient.THttpClient(note_store_url)
    transport.setCustomHeaders({"Authorization": f"Bearer {token}"})
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    note_store = NoteStore.Client(protocol)

    state = load_state()
    synced_guids = state.get('synced_guids', {})
    progress = state.get('progress', {'notebook_idx': 0, 'note_idx': 0})

    if state.get('last_sync'):
        dt = datetime.fromtimestamp(state['last_sync'] / 1000)
        print(f"上次同步: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"已同步: {len(synced_guids)} 条")
    else:
        print("首次同步：全量")
    print()

    print("🔍 扫描本地 vault...")
    local_guid_map = scan_local_vault()
    print(f"   本地已有笔记: {len(local_guid_map)} 条\n")

    try:
        notebooks = note_store.listNotebooks(token)
    except Exception as e:
        print(f"❌ 获取笔记本列表失败: {e}")
        return

    print(f"📓 印象笔记: {len(notebooks)} 个笔记本\n")
    os.makedirs(os.path.join(VAULT_PATH, '.obsidian'), exist_ok=True)

    new_notes = updated = skipped = errors = sync_count = 0
    total_notebooks = len(notebooks)

    # 过滤到目标笔记本（仅当 TARGET_NOTEBOOK 设置时生效）
    if TARGET_NOTEBOOK:
        notebooks = [nb for nb in notebooks if nb.name == TARGET_NOTEBOOK]
        total_notebooks = len(notebooks)
        if total_notebooks == 0:
            print(f"❌ 未找到笔记本: {TARGET_NOTEBOOK}")
            return
        print(f"🎯 只同步笔记本: {TARGET_NOTEBOOK}\n")

    for nb_idx in range(progress.get('notebook_idx', 0), total_notebooks):
        nb = notebooks[nb_idx]
        progress['notebook_idx'] = nb_idx
        progress['note_idx'] = 0
        save_state(state)

        nb_folder = os.path.join(VAULT_PATH, safe_filename(nb.name))
        if not os.path.exists(nb_folder):
            os.makedirs(nb_folder)
        os.makedirs(os.path.join(nb_folder, '_attachments'), exist_ok=True)
        os.makedirs(os.path.join(nb_folder, '_clips'), exist_ok=True)

        try:
            result = note_store.findNotesMetadata(
                token, NoteStore.NoteFilter(notebookGuid=nb.guid), 0, 1000,
                NoteStore.NotesMetadataResultSpec(
                    includeTitle=True, includeCreated=True, includeUpdated=True
                )
            )
            notes_meta = result.notes if result else []
        except Exception as e:
            print(f"  ⚠️ 获取失败: {nb.name}: {e}")
            continue

        if not notes_meta:
            print(f"  [{nb_idx+1}/{total_notebooks}] 📓 {nb.name}: 0 条")
            continue

        print(f"  [{nb_idx+1}/{total_notebooks}] 📓 {nb.name}: {len(notes_meta)} 条")

        for meta_idx in range(progress.get('note_idx', 0), len(notes_meta)):
            meta = notes_meta[meta_idx]
            progress['note_idx'] = meta_idx
            save_state(state)

            if sync_count >= MAX_SYNC_PER_RUN:
                print(f"\n⚠️  达上限（{MAX_SYNC_PER_RUN} 条），下次继续")
                state['last_sync'] = int(time.time() * 1000)
                save_state(state)
                return

            ev_updated = getattr(meta, 'updated', 0) or 0
            if meta.guid in local_guid_map:
                if ev_updated <= local_guid_map[meta.guid]['local_updated_ms']:
                    skipped += 1
                    continue
                need_sync = 'update'
            else:
                need_sync = 'new'

            try:
                note = note_store.getNote(token, meta.guid, True, True, True, True)
            except Exception as e:
                print(f"     ⚠️ 获取失败: {meta.title[:30]}: {e}")
                errors += 1
                continue

            # ── 提取附件 ──
            resources = extract_resources(note)
            att_dir = os.path.join(nb_folder, '_attachments')
            hash_to_file = save_attachments(resources, att_dir)

            # ── 保存原始 ENML（用于 clip 生成，make_replacer 会修改 note.content） ──
            original_content = note.content

            # ── 替换 en-media 引用 ──
            def make_replacer():
                def replacer(m):
                    h = m.group(1)
                    if h in hash_to_file:
                        return make_attachment_link(hash_to_file[h])
                    return ''
                return replacer

            # 自闭合 en-media
            note.content = re.sub(
                r'<en-media[^>]*hash="([^"]*)"[^>]*/>',
                make_replacer(),
                note.content or ''
            )

            # ── 清理 ENML 结构 ──
            raw = re.sub(r'<\?xml[^?]*\?>', '',
                re.sub(r'<!DOCTYPE[^>]*>', '',
                    re.sub(r'<en-note[^>]*>', '',
                        re.sub(r'</en-note>', '', original_content or ''))))

            # ── 判断笔记类型 ──
            has_named_resource = any(resource_has_filename(r) for r in (note.resources or []))
            raw_content = note.content or ''
            is_clip = is_enml_clip(raw_content) or is_web_clip_by_content(raw_content)
            has_inline_media = has_en_media(raw_content) and not has_named_resource
            size_kb = len(raw) / 1024

            dt_c = datetime.fromtimestamp(note.created / 1000)
            dt_u = datetime.fromtimestamp(note.updated / 1000) if note.updated else dt_c
            safe = safe_filename(note.title)

            # ══════════════════════════════════════════════════════
            # 类型 2：长网页片段 ≥5KB → 纯 HTML（无用户手写内容）存 HTML 进 _clips，否则转 Markdown
            # ══════════════════════════════════════════════════════
            if is_clip and size_kb >= CLIP_SIZE_THRESHOLD / 1024:
                if is_enml_clip(original_content):
                    clip_filename = f"clip_{meta.guid[:8]}.html"
                    clip_dir = os.path.join(nb_folder, '_clips')
                    clip_fp = os.path.join(clip_dir, clip_filename)
                    with open(clip_fp, 'w', encoding='utf-8') as f:
                        f.write(f"<!-- source_guid: {meta.guid} -->\n")
                        f.write(f"<!-- notebook: {nb.name} -->\n")
                        f.write(make_clip_html(original_content or '', hash_to_file))
                    md = frontmatter(note.title, nb.name, note.guid, dt_c, dt_u, 'type: webclip')
                    md += f"# {note.title}\n\n![[_clips/{clip_filename}]]\n"
                    icon = '🔗'
                    clip_target = clip_filename
                else:
                    md_body = html_to_md(original_content or '', hash_to_file)
                    md = frontmatter(note.title, nb.name, note.guid, dt_c, dt_u, 'type: webclip')
                    md += f"# {note.title}\n\n{md_body}\n"
                    icon = '📄'
                    clip_target = None

            # ══════════════════════════════════════════════════════
            # 类型 3：网页裁剪 <5KB → 转 Markdown
            # ══════════════════════════════════════════════════════
            elif is_clip and size_kb < CLIP_SIZE_THRESHOLD / 1024:  # size_kb 是 KB，CLIP_SIZE_THRESHOLD 是 bytes
                md_body = html_to_md(original_content or '', hash_to_file)
                md = frontmatter(note.title, nb.name, note.guid, dt_c, dt_u)
                md += f"# {note.title}\n\n{md_body}\n"
                icon = '📄'
                clip_target = None

            # ══════════════════════════════════════════════════════
            # 类型 1：有原始文件名的附件笔记（非 clip 时）
            # ══════════════════════════════════════════════════════
            elif has_named_resource:
                if has_inline_media:
                    md_body = html_to_md(original_content or '', hash_to_file)
                else:
                    md_body = enml_to_markdown(note.content or '')
                md = frontmatter(note.title, nb.name, note.guid, dt_c, dt_u)
                md += f"# {note.title}\n\n{md_body}\n"
                md += make_attachments_section(hash_to_file)
                icon = '📎'
                clip_target = None

            # ══════════════════════════════════════════════════════
            # 类型 5：内嵌图片笔记（有 en-media 但无 fileName，非 clip）
            # ══════════════════════════════════════════════════════
            elif has_inline_media:
                md_body = html_to_md(original_content or '', hash_to_file)
                md = frontmatter(note.title, nb.name, note.guid, dt_c, dt_u, 'type: inline-images')
                md += f"# {note.title}\n\n{md_body}\n"
                md += make_attachments_section(hash_to_file)
                icon = '🖼️'
                clip_target = None

            # ══════════════════════════════════════════════════════
            # 类型 4：纯文本笔记
            # ══════════════════════════════════════════════════════
            else:
                md_body = enml_to_markdown(note.content or '')
                md = frontmatter(note.title, nb.name, note.guid, dt_c, dt_u)
                md += f"# {note.title}\n\n{md_body}\n"
                icon = '📝'
                clip_target = None

            # ── 写入文件 ──
            md_fp = os.path.join(nb_folder, safe + '.md')
            try:
                with open(md_fp, 'w', encoding='utf-8') as f:
                    f.write(md)
            except Exception as e:
                print(f"     ❌ 写入失败: {meta.title[:30]}: {e}")
                errors += 1
                continue

            if need_sync == 'new':
                new_notes += 1
            else:
                updated += 1

            sync_count += 1
            print(f"     {icon} {meta.title[:45]}")
            if clip_target:
                print(f"        ({size_kb:.0f}KB → _clips/{clip_target})")

            synced_guids[meta.guid] = {
                'file': md_fp, 'ev_updated': ev_updated,
                'notebook': nb.name, 'title': note.title
            }
            time.sleep(API_DELAY)

        progress['note_idx'] = 0
        time.sleep(0.5)

    state['last_sync'] = int(time.time() * 1000)
    state['synced_guids'] = synced_guids
    state['progress'] = {'notebook_idx': 0, 'note_idx': 0}
    save_state(state)

    print()
    print("=" * 60)
    print("🎉 同步完成!")
    print("=" * 60)
    print(f"🆕 新增: {new_notes}  🔄 更新: {updated}  ⏭️  跳过: {skipped}  ❌ 错误: {errors}")
    print()
    print("📝 = 纯文本  📎 = 附件笔记  🖼 = 内嵌图片  📄 = 网页裁剪<200KB转MD  🔗 = 网页裁剪>=200KB存HTML")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='印象笔记 -> Obsidian 增量同步')
    parser.add_argument('--notebook', '-n', type=str, default=None,
                        help='只同步此笔记本（名称匹配）')
    args = parser.parse_args()

    if args.notebook is not None:
        TARGET_NOTEBOOK = args.notebook

    sync_to_obsidian()
