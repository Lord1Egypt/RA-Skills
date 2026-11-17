# -*- coding: utf-8 -*-
"""
通用拼接脚本：将各 _draft_*.html 章节片段拼入知乎风 HTML 骨架，
保留外壳（顶栏/问题头/侧栏/页脚），更新侧栏导航、回答数、浏览量。
使用方式：先编辑下方的 CHAPTERS，再运行 python assemble.py
"""
import re, os, sys

# ============================================================
# 每章格式：(显示名, 锚点id, [候补文件名列表，取有效字较大者])
# 使用者根据实际主题编辑此列表，其余代码无需修改
# ============================================================
CHAPTERS = [
    ("第一章标题",   "ch-01",     ["_draft_ch_01.html"]),
    ("第二章标题",   "ch-02",     ["_draft_ch_02.html"]),
    ("第三章标题",   "ch-03",     ["_draft_ch_03.html"]),
    ("第四章标题",   "ch-04",     ["_draft_ch_04.html"]),
    ("第五章标题",   "ch-05",     ["_draft_ch_05.html"]),
    ("第六章标题",   "ch-06",     ["_draft_ch_06.html"]),
    ("第七章标题",   "ch-07",     ["_draft_ch_07.html"]),
    ("第八章标题",   "ch-08",     ["_draft_ch_08.html"]),
    ("第九章标题",   "ch-09",     ["_draft_ch_09.html"]),
    ("第十章标题",   "ch-10",     ["_draft_ch_10.html"]),
]

# 主 HTML 路径（默认当前目录下的 index.html）
MAIN_HTML = "index.html"
# 字数达标阈值（完整版 100000；N% 模式按 floor(100000 × N/100) 调整）
TARGET_WORDS = 100000

# ============================================================
# 以下为通用逻辑，无需修改
# ============================================================

def valid_chars(text):
    """统计有效中文字数：去<script>/<style>/所有标签后的汉字+中文标点"""
    t = re.sub(r'<script.*?</script>', '', text, flags=re.S)
    t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
    t = re.sub(r'<[^>]+>', '', t)
    cn = len(re.findall(r'[\u4e00-\u9fff]', t))
    pn = len(re.findall(r'[\u3000-\u303f\uff00-\uffef]', t))
    return cn + pn

DRAFT_DIR = "./other"   # 章节草稿存放目录

def pick_file(cands):
    """从候选列表中选有效字最多的文件，优先查找 ./other/ 目录"""
    best = None
    for c in cands:
        # 尝试 ./other/ 前缀和裸文件名
        for path in [os.path.join(DRAFT_DIR, c), c]:
            if os.path.exists(path):
                vc = valid_chars(open(path, encoding='utf-8', errors='ignore').read())
                if best is None or vc > valid_chars(open(best, encoding='utf-8', errors='ignore').read()):
                    best = path
                break   # 找到一个就跳出
    return best

# ---- 读主文件 ----
if not os.path.exists(MAIN_HTML):
    print(f"[错误] 未找到主 HTML 文件: {MAIN_HTML}")
    sys.exit(1)
html = open(MAIN_HTML, encoding='utf-8').read()

# ---- 1) 补 h2/h3 标题样式（若不存在） ----
if '.zh-answer__body h3' not in html:
    css = """
.zh-answer__body h2,.zh-answer__body h3{margin:20px 0 10px;color:var(--text-title);font-weight:700;line-height:1.4;}
.zh-answer__body h2{font-size:19px;}
.zh-answer__body h3{font-size:17px;border-left:3px solid var(--zhihu-blue);padding-left:8px;background:var(--bg-page);}
"""
    html = html.replace('</style>', css + '</style>', 1)

# ---- 2) 幂等剥离旧章节（防止重复运行累积） ----
#    使用属性顺序无关的正则 <article[^>]*id="ch-XX"[^>]*>，
#    不依赖 class="zh-card zh-answer" 或 id="ch-NN" 的顺序。
#    核心教训：别用 replace('</main>', …) 做注入点——
#    骨架中若存在含 </main> 的注释（如 <!-- 注入到 </main> -->），
#    章节会被塞进注释里，浏览器直接不渲染。
#    改用独立占位标记 <!-- ASSEMBLE -->，做单次替换。
html = re.sub(r'<article[^>]*id="ch-\d+"[^>]*>.*?</article>', '', html, flags=re.S)

# ---- 3) 注入锚点 + 收集章节片段 ----
all_chapters = []
for name, aid, cands in CHAPTERS:
    fp = pick_file(cands)
    if not fp:
        print(f"[跳过] 未找到文件: {name} ({cands})")
        continue
    frag = open(fp, encoding='utf-8', errors='ignore').read().strip()
    # 注入锚点 id：用宽松正则匹配 <article ...>，不依赖原草稿的属性顺序
    frag = re.sub(r'(<article[^>]*?)(>)', rf'\1 id="{aid}"\2', frag, count=1, flags=re.S)
    vc = valid_chars(frag)
    all_chapters.append((name, aid, frag, vc))
    print(f"[准备] {name:32s} id={aid:14s} 有效中文 {vc:6d} 字  <- {fp}")

# ---- 4) 一次性注入到骨架的 <!-- ASSEMBLE --> 占位标记 ----
if '<!-- ASSEMBLE -->' not in html:
    print("[错误] 骨架中缺少 <!-- ASSEMBLE --> 占位标记，请先在 </main> 前添加该行。")
    sys.exit(1)
chapters_html = '\n\n'.join(frag for _, _, frag, _ in all_chapters)
html = html.replace('<!-- ASSEMBLE -->', chapters_html, 1)
print(f"[注入] 共 {len(all_chapters)} 个章节已写入 <!-- ASSEMBLE --> 标记处")
# 构建兼容旧格式的 inserted 列表（用于后续侧栏/统计）
inserted = [(name, aid, vc) for name, aid, _, vc in all_chapters]

# ---- 5) 去重 <style> 块（各章草稿自带卡片模板，相同模板产生完全重复的 style 块） ----
def dedupe_styles(html):
    """遍历所有 <style>...</style> 块，内容完全相同的只保留首次出现"""
    pattern = re.compile(r'(<style[^>]*>)(.*?)(</style>)', re.S | re.I)
    seen = set()
    dupes = 0
    def replace_unique(m):
        nonlocal dupes
        inner = m.group(2).strip()
        if inner in seen:
            dupes += 1
            return ''          # 重复块删掉
        seen.add(inner)
        return m.group(0)      # 首次出现保留
    result = pattern.sub(replace_unique, html)
    if dupes:
        print(f"[去重] 移除了 {dupes} 个重复的 <style> 块")
    return result

html = dedupe_styles(html)

# ---- 6) 统一硬编码主题蓝为 var(--zhihu-blue) ----
#    卡片模板可能用 #0084ff、#0066ff、#175199 等不同蓝系 hex，
#    与 :root 中定义的 --zhihu-blue:#0084FF 不一致，导致页面出现多种蓝。
#    规则：蓝系 hex（蓝通道显著高于红绿且 >0x80）→ var(--zhihu-blue)；
#    非蓝系（橙 #ff7a45、灰 #333 等）保留。不碰 :root 块和变量定义行。
def normalize_blues(html):
    BLUE_HEX_RE = re.compile(r'(#[0-9a-fA-F]{3,6})\b', re.I)

    def is_blue(h):
        h = h.lstrip('#')
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        if len(h) != 6:
            return False
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return b > 0xC0 and b > max(r, g) * 1.2

    def replace_blue(m):
        return 'var(--zhihu-blue)' if is_blue(m.group(1)) else m.group(0)

    def process_block(m):
        inner = m.group(2)
        lines = inner.split('\n')
        new = []
        for line in lines:
            # 跳过 :root 行、变量定义行、注释行
            if ':root' in line or '--zhihu-blue' in line or line.strip().startswith('/*'):
                new.append(line)
            else:
                new.append(BLUE_HEX_RE.sub(replace_blue, line))
        return m.group(1) + '\n'.join(new) + m.group(3)

    style_pat = re.compile(r'(<style[^>]*>)(.*?)(</style>)', re.S | re.I)
    before = html.count('var(--zhihu-blue)') if 'var(--zhihu-blue)' in html else 0
    html = style_pat.sub(process_block, html)
    after = html.count('var(--zhihu-blue)')
    if after > before:
        print(f"[颜色归一] 将 {after - before} 处硬编码蓝系 hex 替换为 var(--zhihu-blue)")
    return html

html = normalize_blues(html)

# ---- 7) 更新回答数（属性顺序无关的宽松匹配） ----
#    不用严格 match 如 <article class="zh-card zh-answer">，
#    因为草稿自带 id 或 class 顺序可能不一致，用 <article[^>]*> 避免漏算。
n_ans = len(re.findall(r'<article[^>]*id="ch-\d+"[^>]*>', html))
html = re.sub(r'(\d+)\s*个回答', f'{n_ans} 个回答', html, count=1)

# ---- 8) 重建侧栏（自动从 inserted 列表生成） ----
nav_items = "".join(
    f'      <li><a href="#{aid}">{name}</a></li>' for name, aid, _ in inserted)
sidebar = f'''<aside class="zh-sidebar">

  <div class="zh-card zh-sideblock">
    <h3>📑 本页回答</h3>
    <ol>
{nav_items}
    </ol>
  </div>

  <div class="zh-card zh-sideblock">
    <h3>🔗 相关资源</h3>
    <ul>
      <li>可在 HTML 骨架的 <code>zh-sidebar</code> 中自行补充</li>
    </ul>
  </div>

</aside>'''
html = re.sub(r'<aside class="zh-sidebar">.*?</aside>', sidebar, html, count=1, flags=re.S)

# ---- 9) 自动自查（组装后完整性验证） ----
def autocheck(html):
    """在写回磁盘前运行 5 项自动检查，发现问题报错并终止"""
    issues = []
    BLUE_HEX_RE = re.compile(r'(#[0-9a-fA-F]{3,6})')

    def is_blue(h):
        h = h.lstrip('#')
        if len(h) == 3: h = ''.join(c*2 for c in h)
        if len(h) != 6: return False
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return b > 0xC0 and b > max(r, g) * 1.2

    # ① :root 中 --zhihu-blue 定义数和 var(--zhihu-blue) 用法数
    root_block = re.search(r':root\s*\{([^}]+)\}', html, re.S)
    if root_block:
        blue_defs = len(re.findall(r'--zhihu-blue\s*:', root_block.group(1)))
        if blue_defs != 1:
            issues.append(f"  ① :root 中 --zhihu-blue 定义数 = {blue_defs}（期望 1）")
    var_usages = html.count('var(--zhihu-blue)')
    print(f"[自查] ① :root --zhihu-blue 定义数=1, var(--zhihu-blue) 用法数={var_usages}")

    # ② 检测硬编码蓝系 hex（非 :root 行且非 var 值内）
    style_pat = re.compile(r'(<style[^>]*>)(.*?)(</style>)', re.S | re.I)
    for m in style_pat.finditer(html):
        inner = m.group(2)
        for line in inner.split('\n'):
            if ':root' in line or '--zhihu-blue' in line or 'var(--zhihu-blue)' in line:
                continue
            for h in BLUE_HEX_RE.findall(line):
                if is_blue(h):
                    ctx = line.strip()[:80]
                    issues.append(f"  ② 硬编码蓝系 hex {h} → {ctx}")
    if not any('②' in i for i in issues):
        print("[自查] ② 无残留硬编码蓝系 hex [PASS]")

    # ③ 检测 <style> 块完全重复
    seen = {}
    for i, m in enumerate(style_pat.finditer(html), 1):
        key = m.group(2).strip()
        if key in seen:
            issues.append(f"  ③ <style> 块 #{i} 与块 #{seen[key]} 完全重复")
        else:
            seen[key] = i
    if not any('③' in i for i in issues):
        print(f"[自查] ③ 共 {len(seen)} 个 <style> 块，无重复 [PASS]")

    # ④ 校验 .zh-answer__body code 样式与模板一致
    code_styles = re.findall(r'\.zh-answer__body\s+code\s*\{([^}]+)\}', html)
    expected = {'color': '#191b1f', 'background': '#f8f8fa', 'padding': '3px 4px'}
    for cs in code_styles:
        cs_flat = cs.replace(' ', '')  # 压缩空格，兼容 CSS 压缩后和格式化后的两种写法
        for prop, val in expected.items():
            val_compact = val.replace(' ', '')  # 避免 f-string 内嵌转义引号 SyntaxError
            if f'{prop}:{val_compact}' not in cs_flat and f'{prop}:{val}' not in cs:
                issues.append(f"  ④ .zh-answer__body code 缺少 {prop}:{val}，当前：{cs.strip()[:80]}")
                break
    if not any('④' in i for i in issues):
        print("[自查] ④ .zh-answer__body code 样式与模板一致 [PASS]")

    # ⑤ .zh-body 类名在页面元素出现次数（理想为 0）
    body_count = len(re.findall(r'class="[^"]*zh-body[^"]*"', html))
    if body_count > 0:
        issues.append(f"  ⑤ .zh-body 类名在页面出现 {body_count} 次（理想 0，应全部改为 zh-page 或 zh-answer__body）")
    else:
        print("[自查] ⑤ .zh-body 类名出现 0 次 [PASS]")

    if issues:
        print("\n⛔ 组装自查失败，以下问题须修复后再运行 assemble.py：\n")
        for i in issues:
            print(i)
        sys.exit(1)
    else:
        print("[自查] ✅ 全部 5 项检查通过\n")

autocheck(html)

# ---- 10) 写回 ----
open(MAIN_HTML, 'w', encoding='utf-8').write(html)

# ---- 11) 统计 ----
total = valid_chars(html)
print("\n================ 字数核验 ================")
for name, aid, vc in inserted:
    print(f"  {name:32s} {vc:6d} 字")
print(f"  {'[网页总计]':32s} {total:6d} 字")
if total >= TARGET_WORDS:
    print(f"  目标：{TARGET_WORDS:,} 字  |  [PASS] 已达标")
else:
    print(f"  目标：{TARGET_WORDS:,} 字  |  [FAIL] 还差 {TARGET_WORDS-total} 字，需扩写薄弱章节")
print("==========================================")
