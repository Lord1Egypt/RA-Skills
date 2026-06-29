#!/usr/bin/env python3
import argparse, json as _json, re, sys
from pathlib import Path
from datetime import datetime

# === vendor path: 优先用本 skill vendor 下的 mistune ===
_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT / "vendor"))
sys.path.insert(0, str(_SKILL_ROOT))  # 让 `from themes._loader import ...` 可用

try:
    import mistune as _mistune
    _MD = _mistune.create_markdown(plugins=['table', 'strikethrough', 'url'])
    HAS_MISTUNE = True
except Exception as _e:
    _MD = None
    HAS_MISTUNE = False
    print(f"[WARN] mistune 不可用，退回内置正则渲染: {_e}", file=sys.stderr)

try:
    from themes._loader import load_theme_css, list_themes
except Exception as _e:
    print(f"[ERROR] 主题加载器导入失败: {_e}", file=sys.stderr)
    sys.exit(1)

# Cache file: XDG-compliant under ~/.cache/skill-introduction/
# Override with SKILL_INTRO_CACHE env if needed.
import os as _os
_XDG_CACHE = _os.environ.get("XDG_CACHE_HOME") or str(Path("~/.cache").expanduser())
CACHE_FILE = Path(_os.environ.get("SKILL_INTRO_CACHE") or f"{_XDG_CACHE}/skill-introduction/cache.json").expanduser()
# Optional deploy hook: path to a script that uploads the generated HTML.
# Override with SKILL_INTRO_DEPLOY_CMD env (full path to executable).
DEPLOY_CMD_ENV = "SKILL_INTRO_DEPLOY_CMD"

def load_cache() -> dict:
    try:
        if CACHE_FILE.exists():
            return _json.loads(CACHE_FILE.read_text())
    except Exception:
        pass
    return {}

def save_cache(cache: dict):
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(_json.dumps(cache, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"[WARN] 缓存写入失败: {e}")

def extract_dashboard_id(output: str) -> str:
    m = re.search(r'dashboardId=([A-Fa-f0-9]{32})', output)
    return m.group(1) if m else ""


def get_current_user() -> str:
    """Resolve author name across environments.

    Priority:
      1. SKILL_INTRO_AUTHOR env
      2. git config --global user.name
      3. $USER env
      4. empty
    """
    name = _os.environ.get("SKILL_INTRO_AUTHOR", "").strip()
    if name:
        return name
    try:
        import subprocess as _sp
        r = _sp.run(["git", "config", "--global", "user.name"],
                    capture_output=True, text=True, timeout=3)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:
        pass
    return _os.environ.get("USER", "").strip()


def _pick_source_file(skill_dir: Path, source: str = "") -> tuple:
    """选取源 md 文件。返回 (Path, from_skill_md: bool, used_name: str)。
    优先级: --source 指定 > USAGE.md > SKILL.md(回退)
    """
    if source:
        p = (skill_dir / source) if not Path(source).is_absolute() else Path(source)
        if not p.exists():
            print(f"[ERROR] 找不到指定源文件: {p}", file=sys.stderr); sys.exit(1)
        return p, False, p.name
    usage = skill_dir / "USAGE.md"
    if usage.exists():
        return usage, False, "USAGE.md"
    skill = skill_dir / "SKILL.md"
    if skill.exists():
        return skill, True, "SKILL.md"
    print(f"[ERROR] 找不到源文件（USAGE.md / SKILL.md）: {skill_dir}", file=sys.stderr); sys.exit(1)


def parse_skill(skill_dir: Path, source: str = "") -> dict:
    src_path, from_skill_md, used_name = _pick_source_file(skill_dir, source)
    raw = src_path.read_text(encoding="utf-8")
    fm, body = {}, raw
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if ":" in line and not line.strip().startswith("#"):
                    k, _, v = line.partition(":"); fm[k.strip()] = v.strip()
            body = parts[2].strip()
    # name/description 优先取 frontmatter；SKILL.md 也可能没有 USAGE.md 时回退到目录名
    name = fm.get("name", skill_dir.name)
    description = fm.get("description", "")
    sections = parse_sections(body)
    scripts_dir = skill_dir / "scripts"
    refs_dir = skill_dir / "references"
    assets_dir = skill_dir / "assets"
    test_md = skill_dir / "TEST.md"
    scripts_files = sorted(f.name for f in scripts_dir.iterdir() if f.is_file() and not f.name.startswith(".")) if scripts_dir.exists() else []
    ref_files = sorted(f.name for f in refs_dir.iterdir() if f.is_file()) if refs_dir.exists() else []
    test_content = test_md.read_text(encoding="utf-8") if test_md.exists() else ""
    code_examples = extract_code_examples(skill_dir, scripts_files, sections)
    author   = fm.get("author", fm.get("maintainer", fm.get("author_name", "")))
    updated  = fm.get("updated", fm.get("last_updated", ""))
    if not updated:
        try:
            mtime = src_path.stat().st_mtime
            updated = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        except Exception:
            updated = datetime.now().strftime("%Y-%m-%d")

    return dict(name=name, description=description, body=body, sections=sections,
                has_scripts=scripts_dir.exists(), has_refs=refs_dir.exists(),
                has_assets=assets_dir.exists(), has_test=test_md.exists(),
                scripts_files=scripts_files, ref_files=ref_files,
                test_content=test_content, code_examples=code_examples,
                skill_dir=str(skill_dir), author=author, updated=updated,
                from_skill_md=from_skill_md, source_name=used_name)

def parse_sections(body: str) -> list:
    sections, cur = [], None
    for line in body.splitlines():
        m1 = re.match(r'^(#{1,3})\s+(.+)', line)
        if m1:
            if cur: sections.append(cur)
            cur = {"level": len(m1.group(1)), "title": m1.group(2).strip(), "content": []}
        elif cur is not None:
            cur["content"].append(line)
    if cur: sections.append(cur)
    return sections

def extract_code_examples(skill_dir: Path, scripts_files: list, sections: list) -> list:
    examples = []
    for sec in sections:
        content = "\n".join(sec["content"])
        for block in re.findall(r'```(?:bash|python|sh|cmd)?\n(.*?)```', content, re.DOTALL):
            lines = [l for l in block.strip().splitlines() if l.strip()]
            if lines: examples.append((sec["title"], "\n".join(lines[:8])))
        if len(examples) >= 4: break
    for fname in scripts_files[:2]:
        try:
            content = (skill_dir / "scripts" / fname).read_text(encoding="utf-8", errors="ignore")
            ds = re.search(r'"""(.*?)"""', content, re.DOTALL)
            if ds:
                for block in re.findall(r'```[\w]*\n(.*?)```', ds.group(1), re.DOTALL):
                    lines = [l for l in block.strip().splitlines() if l.strip()]
                    if lines: examples.append((fname, "\n".join(lines[:8])))
        except Exception: pass
    return examples[:4]

def esc(text: str) -> str:
    return text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def md2html(text: str) -> str:
    """行内级 markdown（粗体/斜体/code/link）—— 用于小段文案、列表项标题等。
    完整块级渲染交给 mistune（见 process_content）。
    """
    if not text: return ""
    text = re.sub(r'```[\w]*\n(.*?)```', lambda m: f'<pre class="mini-code">{esc(m.group(1).strip())}</pre>', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
    return text

ICON_MAP = {"快速":"⚡","部署":"🚀","更新":"🔄","回滚":"🔙","数据":"📊","存储":"💾","权限":"🔑","管理":"🛠️","下载":"⬇️","配置":"🔧","参数":"⚙️","命令":"💻","示例":"💡","场景":"🗂️","安装":"📦","开始":"🎯","使用":"📖","生成":"✨","解析":"🔍","格式":"📋","脚本":"📜","参考":"📚","规范":"📐","原则":"🧭","设计":"🎨","注意":"⚠️","说明":"📋","核心":"🔥","基础":"📌","进阶":"🚀"}

def icon_for(title: str) -> str:
    for kw, em in ICON_MAP.items():
        if kw in title: return em
    return "📄"

def extract_list_items(content_lines: list, max_items=4) -> list:
    items = []
    for line in content_lines:
        s = line.strip()
        if not s or s.startswith("|") or s.startswith("---") or s.startswith("```"): continue
        if s.startswith(("- ","* ","· ")):
            text = s[2:].strip()
            clean = re.sub(r'`[^`]+`','',text).strip()
            if clean and len(clean)>2: items.append(md2html(text[:80]))
        elif re.match(r'^\d+\. ', s):
            text = re.sub(r'^\d+\. ','',s).strip()
            clean = re.sub(r'`[^`]+`','',text).strip()
            if clean and len(clean)>2: items.append(md2html(text[:80]))
        if len(items) >= max_items: break
    return items


# === legacy 内置渲染（mistune 缺失时兜底） ===
def _legacy_table_to_html(rows: list) -> str:
    if not rows: return ""
    header = rows[0]; data = rows[1:]
    th = "".join(f"<th>{md2html(h)}</th>" for h in header)
    trs = "".join("<tr>"+"".join(f"<td>{md2html(c)}</td>" for c in row)+"</tr>" for row in data)
    return f'<table class="doc-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def _legacy_process(content_lines: list) -> str:
    processed, in_table, trows = [], False, []
    for line in content_lines:
        s = line.strip()
        if re.match(r'^\|.+\|', s):
            if not in_table: in_table, trows = True, []
            if re.match(r'^\|[-: |]+\|', s): continue
            trows.append([c.strip() for c in s.strip('|').split('|')])
        else:
            if in_table:
                processed.append(_legacy_table_to_html(trows))
                in_table, trows = False, []
            processed.append(line)
    if in_table: processed.append(_legacy_table_to_html(trows))
    rendered = md2html("\n".join(processed).strip())
    if not rendered: return ""
    body_html = ""
    for para in re.split(r'\n{2,}', rendered):
        para = para.strip()
        if not para: continue
        if para.startswith("<pre") or para.startswith("<table"):
            body_html += para
        elif re.match(r'^[-*] ', para):
            items = re.split(r'\n[-*] ', para.lstrip("- *"))
            body_html += "<ul class='doc-ul'>"+"".join(f"<li>{it.strip()}</li>" for it in items if it.strip())+"</ul>"
        elif re.match(r'^\d+\. ', para):
            items = re.split(r'\n\d+\. ', re.sub(r'^\d+\. ','',para))
            body_html += "<ol class='doc-ol'>"+"".join(f"<li>{it.strip()}</li>" for it in items if it.strip())+"</ol>"
        else:
            lines = para.split("\n")
            body_html += "<p class='doc-desc'>"+" ".join(l.strip() for l in lines if l.strip())+"</p>"
    return body_html


def _postprocess_mistune_html(html: str) -> str:
    """把 mistune 输出的裸 ul/ol/table/p 标签加上现有 CSS class。"""
    if not html: return ""
    # 仅给顶层 ul/ol/p 加 class（不影响嵌套 ul/ol 已有内容；嵌套的也加 class 无害）
    html = re.sub(r'<ul>', '<ul class="doc-ul">', html)
    html = re.sub(r'<ol>', '<ol class="doc-ol">', html)
    html = re.sub(r'<p>', '<p class="doc-desc">', html)
    html = re.sub(r'<table>', '<table class="doc-table">', html)
    # 代码块：mistune 输出 <pre><code class="language-xxx">...</code></pre>，转成 mini-code
    def _codeblock(m):
        inner = m.group(1)
        # 已经做过 esc（mistune 默认 escape）
        return f'<pre class="mini-code">{inner}</pre>'
    html = re.sub(r'<pre><code(?:\s+class="[^"]*")?>(.*?)</code></pre>', _codeblock, html, flags=re.DOTALL)
    return html


def process_content(content_lines: list) -> str:
    """主块级渲染：优先 mistune，失败回退 legacy。"""
    text = "\n".join(content_lines).strip()
    if not text: return ""
    if HAS_MISTUNE and _MD is not None:
        try:
            raw = _MD(text)
            return _postprocess_mistune_html(raw)
        except Exception as e:
            print(f"[WARN] mistune 渲染失败，回退 legacy: {e}", file=sys.stderr)
    return _legacy_process(content_lines)


def build_highlight_cards(si: dict) -> str:
    """只用真实 h2 章节生成卡片；最多 6 张；无真实章节返回空。"""
    h2s = [s for s in si["sections"] if s["level"] == 2]
    cards = []
    for sec in h2s[:6]:
        items = extract_list_items(sec["content"], 1)
        if items:
            desc = items[0]
        else:
            joined = " ".join(l.strip() for l in sec["content"] if l.strip() and not l.strip().startswith("|"))[:80]
            desc = joined or sec["title"]
        em_actual = icon_for(sec["title"])
        cards.append(f'      <div class="card"><div class="card-icon">{em_actual}</div><div class="card-title">{sec["title"]}</div><div class="card-desc">{desc}</div></div>')
    return "\n".join(cards)

def build_feature_cards(si: dict) -> str:
    """只用真实 h2 章节生成卡片；最多 6 张；无真实章节返回空。"""
    colors = ["feat-cat-blue","feat-cat-purple","feat-cat-green","feat-cat-cyan","feat-cat-orange","feat-cat-pink"]
    h2s = [s for s in si["sections"] if s["level"] == 2][:6]
    if not h2s:
        return ""
    cards = []
    for i, sec in enumerate(h2s):
        color = colors[i % len(colors)]
        ico = icon_for(sec["title"])
        items = extract_list_items(sec["content"], 4)
        if not items:
            non_table = [l for l in sec["content"] if l.strip() and not l.strip().startswith("|") and not l.strip().startswith("```")]
            joined = " ".join(non_table[:3]).strip()
            if joined:
                sentences = [s.strip() for s in re.split(r'[。.！!？?；;]', joined) if s.strip() and len(s.strip())>3]
                items = [md2html(s[:80]) for s in sentences[:3]]
        items_html = "".join(f"<li>{p}</li>" for p in items)
        list_html = f'<ul class="feat-cat-list">{items_html}</ul>' if items_html else ''
        cards.append(f'      <div class="feat-cat-card {color}"><div class="feat-cat-header"><span class="feat-cat-icon">{ico}</span><span class="feat-cat-title">{sec["title"]}</span></div>{list_html}</div>')
    return "\n".join(cards)

def build_quickstart_user(si: dict) -> str:
    sections = si["sections"]
    name = si["name"]
    desc = si["description"]
    quoted = re.findall(r'[\u300c\u201c\u2018]([^\u300d\u201d\u2019]{4,40})[\u300d\u201d\u2019]', desc)
    trigger_ex = f'&ldquo;{esc(quoted[0])}&rdquo;' if quoted else f'&ldquo;帮我用 {esc(name)} 处理...&rdquo;'
    h3s = [s for s in sections if s["level"]==3][:4]
    if h3s:
        steps = []
        for sec in h3s:
            content = [l for l in sec["content"]
                       if l.strip() and not l.startswith("|")
                       and not l.startswith("```") and not l.startswith("#")]
            d = " ".join(l.strip().lstrip("- *") for l in content[:3]).strip()[:200]
            steps.append((sec["title"], md2html(d) if d else "详见文档"))
    else:
        all_items = []
        for sec in sections:
            for line in sec["content"]:
                s = line.strip()
                if s.startswith(("- ","* ")):
                    text = s[2:].strip()
                    if text and len(text)>5: all_items.append((sec["title"], text[:100]))
        if len(all_items) >= 3:
            steps = [(t, md2html(txt)) for t,txt in all_items[:4]]
        else:
            steps = [("安装 Skill", f'点击右下角「点我安装」，或对 AI 说 <em>"帮我安装 {name} skill"</em>。'),
                     ("告诉 AI 你的需求", f'直接说 <em>{trigger_ex}</em>，AI 自动识别并调用。'),
                     ("查看结果", "AI 处理完毕后直接返回结果，无需记忆任何命令。")]
    html = ""
    for i, (title, d) in enumerate(steps, 1):
        html += f'          <div class="user-step"><div class="step-num">{i}</div><div class="step-body"><div class="step-title">{title}</div><div class="step-desc">{d}</div></div></div>\n'
    return html

def build_code_terminal(si: dict) -> str:
    examples = si["code_examples"]
    name = si["name"]
    if not examples:
        return f'<div class="term-body"><div><span class="c-cmt"># 对 AI 描述你的需求，Skill 自动触发</span></div><div><span class="c-out">→ </span><span class="c-text">{name} 会自动处理并返回结果</span></div></div>'
    lines_html = []
    for label, block in examples[:3]:
        lines_html.append(f'<div><span class="c-cmt">{esc(label)}</span></div>')
        for line in block.splitlines():
            if not line.strip(): continue
            if line.strip().startswith("#"):
                lines_html.append(f'<div><span class="c-cmt">{esc(line)}</span></div>')
            else:
                parts = line.split(" ", 1)
                rest = esc(parts[1]) if len(parts)>1 else ""
                rest = re.sub(r'(--[\w-]+)', r'<span class="c-flag">\1</span>', rest)
                rest = re.sub(r'"([^"]+)"', r'<span class="c-val">"\1"</span>', rest)
                lines_html.append(f'<div><span class="c-cmd">{esc(parts[0])}</span><span class="c-text"> {rest}</span></div>')
        lines_html.append("<br/>")
    return '<div class="term-body">\n' + "\n".join(lines_html) + "\n</div>"

def classify_card_tag(title: str) -> tuple:
    t = title.lower()
    if any(k in t for k in ["即将","规划","未来","todo","待办","coming","soon"]):
        return ("即将上线", "tag-orange")
    if any(k in t for k in ["高级","进阶","深度","api","配置","参数","权限"]):
        return ("进阶", "tag-purple")
    return ("基础", "tag-blue")

def build_doc_card(title: str, body: str, tag_name: str, tag_class: str = "tag-blue") -> str:
    ico = icon_for(title)
    return f'            <div class="doc-card"><div class="doc-card-header" onclick="toggleDoc(this)"><span class="doc-card-icon">{ico}</span><span class="doc-card-name">{title}</span><span class="doc-card-tag {tag_class}">{tag_name}</span><span class="doc-card-arrow">▶</span></div><div class="doc-card-body">{body}</div></div>'

def build_doc_section_user(si: dict) -> str:
    sections = si["sections"]
    doc_sections = [s for s in sections if s["level"] in (2,3)]
    if not doc_sections:
        return '<div class="doc-group"><div class="doc-group-title">📖 使用说明</div>' + build_doc_card("使用指南", "<p class='doc-desc'>详见源文档。</p>", "基础") + '</div>'
    groups = []
    group_icons = ["📤","🎨","⚙️","🔧","📊","🛠️","📝","🔍"]
    h2s = [s for s in sections if s["level"] == 2]
    if h2s:
        for gi, h2 in enumerate(h2s):
            icon = group_icons[gi % len(group_icons)]
            h2_idx = sections.index(h2)
            next_h2_idx = sections.index(h2s[gi+1]) if gi+1 < len(h2s) else len(sections)
            sub_h3s = [s for s in sections[h2_idx+1:next_h2_idx] if s["level"]==3]
            cards_html = ""
            body = process_content(h2["content"])
            if not body and not sub_h3s: body = '<p class="doc-desc">—</p>'
            if body:
                tag_name, tag_class = classify_card_tag(h2["title"])
                cards_html += build_doc_card(h2["title"], body, tag_name, tag_class)
            for sec in sub_h3s:
                body = process_content(sec["content"])
                if not body: body = '<p class="doc-desc">—</p>'
                tag_name, tag_class = classify_card_tag(sec["title"])
                cards_html += build_doc_card(sec["title"], body, tag_name, tag_class)
            if cards_html:
                groups.append(f'          <div class="doc-group"><div class="doc-group-title">{icon} {h2["title"]}</div>\n{cards_html}\n          </div>')
    else:
        group_titles_fallback = ["核心功能", "使用指南", "高级配置", "场景示例"]
        for i in range(0, len(doc_sections), 3):
            group_sec = doc_sections[i:i+3]
            icon = group_icons[i//3 % len(group_icons)]
            gtitle = group_titles_fallback[i//3 % len(group_titles_fallback)]
            cards_html = ""
            for sec in group_sec:
                body = process_content(sec["content"])
                if not body: body = '<p class="doc-desc">—</p>'
                tag_name, tag_class = classify_card_tag(sec["title"])
                cards_html += build_doc_card(sec["title"], body, tag_name, tag_class)
            groups.append(f'          <div class="doc-group"><div class="doc-group-title">{icon} {gtitle}</div>\n{cards_html}\n          </div>')
    if not groups:
        return '<div class="doc-group"><div class="doc-group-title">📖 使用说明</div>' + build_doc_card("使用指南", "<p class='doc-desc'>详见源文档。</p>", "基础") + '</div>'
    return "\n".join(groups)

def build_doc_section_agent(si: dict) -> str:
    sections = si["sections"]
    agent_sections = []
    for sec in sections:
        content = "\n".join(sec["content"])
        if any(k in sec["title"].lower() for k in ["命令","参数","api","代码","cli","脚本"]) or "```" in content:
            agent_sections.append(sec)
    if not agent_sections:
        examples = si["code_examples"]
        if examples:
            body = "<pre class='mini-term'>" + "\n".join(f"# {esc(lbl)}\n{esc(cmd)}" for lbl,cmd in examples[:2]) + "</pre>"
            return f'<div class="doc-group"><div class="doc-group-title">💻 命令示例</div>{build_doc_card("快速命令", body, "基础")}</div>'
        return '<div class="doc-group"><div class="doc-group-title">🤖 Agent 使用</div>' + build_doc_card("调用方式", "<p class='doc-desc'>对 AI 描述需求即可，无需记忆具体命令。</p>", "基础") + '</div>'
    groups = []
    group_icons = ["💻","⚙️","🔧","📡"]
    for i, sec in enumerate(agent_sections[:6]):
        body = process_content(sec["content"])
        if not body: body = '<p class="doc-desc">—</p>'
        tag_name, tag_class = classify_card_tag(sec["title"])
        icon = group_icons[i % len(group_icons)]
        groups.append(f'          <div class="doc-group"><div class="doc-group-title">{icon} {sec["title"]}</div>\n{build_doc_card(sec["title"], body, tag_name, tag_class)}\n          </div>')
    return "\n".join(groups)


_ROADMAP_KW = ("规划", "roadmap", "路线", "未来", "计划", "todo")


def build_roadmap(si: dict) -> str:
    """只从源文档真实章节抽取 roadmap；无则返回空字符串。"""
    candidates = []
    for sec in si["sections"]:
        if sec["level"] not in (2, 3):
            continue
        t_lower = sec["title"].lower()
        if any(kw in t_lower for kw in _ROADMAP_KW):
            candidates.append(sec)
    if not candidates:
        return ""
    cards = []
    icons = ["🔗", "🎨", "🔧", "🧭"]
    for i, sec in enumerate(candidates[:4]):
        ico = icons[i % len(icons)]
        title = sec["title"]
        tag = "规划中"
        items = extract_list_items(sec["content"], 1)
        if items:
            desc = items[0]
        else:
            joined = " ".join(l.strip() for l in sec["content"] if l.strip() and not l.strip().startswith("|"))[:120]
            desc = joined or "—"
        cards.append(f'      <div class="roadmap-card"><div class="roadmap-card-header"><span class="roadmap-icon">{ico}</span><span class="roadmap-title">{title}</span><span class="roadmap-tag">{tag}</span></div><p class="roadmap-desc">{desc}</p></div>')
    return "\n".join(cards)

def build_known_issues(si: dict) -> str:
    sections = si["sections"]
    issues = []
    for sec in sections:
        if any(kw in sec["title"] for kw in ["注意","问题","限制","Issue","Warning","已知"]):
            for line in sec["content"]:
                s = line.strip()
                if s.startswith(("- ","* ")):
                    issues.append(s[2:].strip())
    if not issues:
        issues = ["Skill 的调用质量取决于 SKILL.md 描述的清晰度，描述越具体，AI 识别越准确。",
                  "复杂任务建议分步骤描述需求，避免一次输入过多要求。",
                  "如遇调用失败，请检查 Skill 是否已正确安装，或尝试重新描述需求。"]
    items = "".join(f"<li>{md2html(iss)}</li>" for iss in issues[:6])
    return f'  <div id="known-issues" class="known-issues fade-in"><div class="known-issues-title">⚠️ 已知问题 &amp; 注意事项</div><ul>{items}</ul></div>'


JS = r"""
function switchTab(group,name,btn){
  ['user','agent'].forEach(n=>{
    const el=document.getElementById(group+'-'+n);
    if(el) el.classList.remove('active');
  });
  btn.closest('.tab-nav').querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  const target=document.getElementById(group+'-'+name);
  if(target) target.classList.add('active');
  btn.classList.add('active');
}
function toggleDoc(header){ header.closest('.doc-card').classList.toggle('open'); }
const observer=new IntersectionObserver(
  entries=>entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible');}),
  {threshold:0.06}
);
// 降级兜底：IntersectionObserver 不可用时，直接全部显示，避免全站空白
if(typeof IntersectionObserver==='undefined'){
  document.querySelectorAll('.fade-in').forEach(el=>el.classList.add('visible'));
}else{
  document.querySelectorAll('.fade-in').forEach(el=>observer.observe(el));
}
const heroEl=document.querySelector('#hero');
if(heroEl) heroEl.classList.add('visible');
// 二次兜底：若 1.5s 后仍有 fade-in 未触发（如被滚动捕获遗漏），强制显示
setTimeout(function(){document.querySelectorAll('.fade-in:not(.visible)').forEach(el=>el.classList.add('visible'));},1500);
const secIds=__SEC_IDS__;
const navItems={};
secIds.forEach(id=>{navItems[id]=document.querySelector('.side-nav-item[data-sec="'+id+'"]');});
const scrollSpy=new IntersectionObserver(entries=>{
  entries.forEach(e=>{
    if(e.isIntersecting){
      Object.values(navItems).forEach(n=>n&&n.classList.remove('active'));
      const item=navItems[e.target.id];
      if(item) item.classList.add('active');
    }
  });
},{rootMargin:'-30% 0px -60% 0px'});
secIds.forEach(id=>{const el=document.getElementById(id);if(el)scrollSpy.observe(el);});
"""


def generate_html(si: dict, hub_url: str = "", author: str = "", theme: str = "light", subtitle_override: str = "") -> str:
    name = si["name"]
    description = si["description"]
    today   = datetime.now().strftime("%Y-%m-%d")
    updated = si.get("updated", today)
    if not author:
        author = get_current_user()
    author_html = f'维护者 <strong>{author}</strong> &nbsp;·&nbsp;' if author else ""

    # 副标题：优先用 agent 传入的浓缩宣传语；否则回退到 description 截断
    if subtitle_override:
        subtitle = esc(subtitle_override)
    else:
        subtitle = esc(description[:130]) + ("..." if len(description) > 130 else "")
    safe_name = re.sub(r'-{2,}', '-', re.sub(r'[^a-zA-Z0-9\-]', '-', name.lower())).strip('-')
    install_url = hub_url or f"https://clawhub.com/skill/{safe_name}"
    quoted = re.findall(r'[\u300c\u201c\u2018]([^\u300d\u201d\u2019]{4,40})[\u300d\u201d\u2019]', description)
    triggers = quoted[:5]
    trigger_tags = "".join(f'<span class="trigger-tag">{t}</span>' for t in triggers)

    # ---- 各区块内容（空则隐藏整段） ----
    highlight_html = build_highlight_cards(si)
    feature_html   = build_feature_cards(si)
    qs_user_html   = build_quickstart_user(si)
    qs_code_html   = build_code_terminal(si)
    doc_user_html  = build_doc_section_user(si)
    doc_agent_html = build_doc_section_agent(si)
    roadmap_html   = build_roadmap(si)
    known_html     = build_known_issues(si)

    has_highlights = bool(highlight_html.strip())
    has_features   = bool(feature_html.strip())
    has_roadmap    = bool(roadmap_html.strip())

    # 动态侧导航 + JS secIds
    nav_items = [("hero", "首页")]
    if has_highlights: nav_items.append(("highlights", "核心亮点"))
    if has_features:   nav_items.append(("features",   "功能全览"))
    nav_items.append(("quickstart", "开始使用"))
    nav_items.append(("docs",       "详细说明"))
    if has_roadmap:    nav_items.append(("roadmap", "未来规划"))
    nav_items.append(("known-issues", "已知问题"))

    nav_html = "\n  ".join(
        (f'<a class="side-nav-item active" href="#{sid}" data-sec="{sid}"><span class="side-nav-dot"></span>{label}</a>'
         if i == 0 else
         f'<a class="side-nav-item" href="#{sid}" data-sec="{sid}"><span class="side-nav-dot"></span>{label}</a>')
        for i, (sid, label) in enumerate(nav_items)
    )
    sec_ids_js = "[" + ",".join(f"'{sid}'" for sid, _ in nav_items) + "]"

    # ---- 拼接各 section（含条件隐藏）----
    highlights_section = "" if not has_highlights else f'''  <section id="highlights" class="fade-in">
    <div class="section-header">
      <div class="section-label">核心亮点</div>
      <h2 class="section-title">为什么选 {name}？</h2>
      <p class="section-desc">快速了解这个 Skill 的核心价值。</p>
    </div>
    <div class="cards-grid">
{highlight_html}
    </div>
  </section>
'''

    features_section = "" if not has_features else f'''  <section id="features" class="fade-in">
    <div class="section-header">
      <div class="section-label">功能全览</div>
      <h2 class="section-title">开箱即用的能力</h2>
      <p class="section-desc">覆盖主要场景的功能模块一览。</p>
    </div>
    <div class="feat-cat-grid">
{feature_html}
    </div>
  </section>
'''

    roadmap_section = "" if not has_roadmap else f'''  <section id="roadmap" class="fade-in">
    <div class="section-header">
      <div class="section-label">未来规划</div>
      <h2 class="section-title">即将到来的能力</h2>
      <p class="section-desc">持续迭代，让 {name} 更强大、更易用。</p>
    </div>
    <div class="roadmap-grid">
{roadmap_html}
    </div>
  </section>
'''

    # SKILL.md 回退提示
    src_notice = ""
    if si.get("from_skill_md"):
        src_notice = '<div class="src-notice"><span>⚠️</span><span>本页内容取自 SKILL.md（面向 AI 触发），可能偏技术。建议在 skill 目录补充 USAGE.md 以生成面向用户的说明页。</span></div>'

    css = load_theme_css(theme)
    js = JS.replace("__SEC_IDS__", sec_ids_js)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%E2%9C%A8%3C/text%3E%3C/svg%3E">
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{name} · Skill 使用说明</title>
  <style>{css}</style>
  <noscript><style>.fade-in{{opacity:1 !important;transform:none !important}}</style></noscript>
</head>
<body>
<a class="fab-install" href="{install_url}" target="_blank" rel="noopener">
  <div class="fab-circle">📦</div>
  <span class="fab-label">点我安装</span>
</a>
<nav class="side-nav" id="sideNav">
  {nav_html}
</nav>
<div class="layout"><div class="container">
  <section id="hero" class="fade-in">
    <div class="badge"><span class="badge-dot"></span>OpenClaw Skill · {name}</div>
    <h1><span class="gradient-text">{name}</span></h1>
    <p class="subtitle">{subtitle}</p>
    {f'<div class="trigger-tags">{trigger_tags}</div>' if trigger_tags else ''}
    <div class="cta-row">
      <a class="btn btn-primary" href="{install_url}" target="_blank" rel="noopener">🚀 &nbsp;立即安装</a>
      <a class="btn btn-ghost" href="#quickstart">📖 &nbsp;查看文档</a>
    </div>
    <div class="meta-bar">
      <span class="meta-item">🕒 {today}</span>
    </div>
  </section>
  {src_notice}
{highlights_section}{features_section}  <section id="quickstart" class="fade-in">
    <div class="section-header">
      <div class="section-label">开始使用</div>
      <h2 class="section-title">几分钟上手</h2>
      <p class="section-desc">先安装 Skill，然后选择你的身份开始。</p>
    </div>
    <div class="tab-wrap">
      <div class="tab-nav">
        <button class="tab-btn active" onclick="switchTab('qs','user',this)">👤 &nbsp;面向用户</button>
        <button class="tab-btn" onclick="switchTab('qs','agent',this)">🤖 &nbsp;Agent / 命令行</button>
      </div>
      <div id="qs-user" class="tab-panel active">
        <div class="user-panel">
{qs_user_html}
        </div>
      </div>
      <div id="qs-agent" class="tab-panel">
        <div class="term-bar">
          <div class="term-dot"></div><div class="term-dot"></div><div class="term-dot"></div>
          <span class="term-label">快速上手命令</span>
        </div>
{qs_code_html}
      </div>
    </div>
  </section>
  <section id="docs" class="fade-in">
    <div class="section-header">
      <div class="section-label">详细使用说明</div>
      <h2 class="section-title">所有功能与命令</h2>
      <p class="section-desc">点击展开每个功能的详细说明。</p>
    </div>
    <div class="tab-wrap">
      <div class="tab-nav">
        <button class="tab-btn active" onclick="switchTab('doc','user',this)">👤 &nbsp;面向用户</button>
        <button class="tab-btn" onclick="switchTab('doc','agent',this)">🤖 &nbsp;Agent / 命令行</button>
      </div>
      <div id="doc-user" class="tab-panel active">
        <div class="doc-section">
{doc_user_html}
        </div>
      </div>
      <div id="doc-agent" class="tab-panel">
        <div class="doc-section">
{doc_agent_html}
        </div>
      </div>
    </div>
  </section>
{roadmap_section}{known_html}
  <footer class="fade-in">
    <div class="footer-text">
      {name} &nbsp;·&nbsp;
      {author_html}
      最后更新 {updated}
    </div>
  </footer>
</div></div>
<script>{js}</script>
</body>
</html>'''


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--skill-dir", required=True)
    p.add_argument("--output", default="")
    p.add_argument("--no-deploy", action="store_true")
    p.add_argument("--hub-url", default="")
    p.add_argument("--author", default="", help="作者/维护者姓名（可选）")
    p.add_argument("--update-id", default="", help="强制更新指定 dashboardId（留空则自动从缓存读取）")
    p.add_argument("--source", default="", help="指定源 md 文件（相对 skill-dir 或绝对路径）；默认 USAGE.md > SKILL.md")
    p.add_argument("--theme", default="light", choices=list_themes(), help=f"主题，默认 light；可选: {', '.join(list_themes())}")
    p.add_argument("--subtitle", default="", help="英雄区副标题（一句宣传语）；不传则截断 description")
    args = p.parse_args()
    skill_dir = Path(args.skill_dir).expanduser().resolve()
    if not skill_dir.is_dir():
        print(f"[ERROR] 目录不存在: {skill_dir}", file=sys.stderr); sys.exit(1)
    print(f"[INFO] 读取 skill: {skill_dir}")
    si = parse_skill(skill_dir, source=args.source)
    print(f"[INFO] Skill: {si['name']} (source: {si.get('source_name','')}, theme: {args.theme})")
    if si.get("from_skill_md"):
        print("[WARN] 内容取自 SKILL.md，建议补 USAGE.md（详见页面顶部提示）")
    author = args.author or si.get("author", "") or get_current_user()
    html = generate_html(si, hub_url=args.hub_url, author=author, theme=args.theme, subtitle_override=args.subtitle)
    if args.output:
        out = Path(args.output).expanduser()
    else:
        # Default output: CWD/output/<slug>-intro.html (override with --output)
        out_dir = Path.cwd() / "output"
        out_dir.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r'[^a-zA-Z0-9\-_]', '-', si['name'].lower())
        out = out_dir / f"{safe}-intro.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"[OK] HTML generated: {out}")
    if not args.no_deploy:
        # Pluggable deploy hook. Set SKILL_INTRO_DEPLOY_CMD to a script that
        # accepts the HTML path as $1 and returns a public URL on stdout.
        deploy_cmd = _os.environ.get(DEPLOY_CMD_ENV, "").strip()
        if deploy_cmd:
            import subprocess, shlex
            cache = load_cache()
            cache_key = si["name"]
            existing_id = args.update_id or cache.get(cache_key, "")
            env = _os.environ.copy()
            if existing_id:
                env["SKILL_INTRO_UPDATE_ID"] = existing_id
                print(f"[INFO] Updating existing page ({existing_id}) via deploy hook...")
            else:
                print("[INFO] First deployment via deploy hook...")
            cmd = shlex.split(deploy_cmd) + [str(out)]
            r = subprocess.run(cmd, capture_output=True, text=True, env=env)
            if r.returncode == 0:
                output_text = r.stdout.strip()
                print(output_text)
                new_id = extract_dashboard_id(output_text)
                if new_id:
                    cache[cache_key] = new_id
                    save_cache(cache)
                    print(f"[INFO] Cache updated: {cache_key} -> {new_id}")
            else:
                print(f"[WARN] Deploy hook failed:\n{r.stderr}")
                print(f"[INFO] Local file: {out}")
        else:
            print(f"[INFO] No deploy hook configured (set {DEPLOY_CMD_ENV} env to enable).")
            print(f"[INFO] Local file: {out}")

if __name__ == "__main__":
    main()
