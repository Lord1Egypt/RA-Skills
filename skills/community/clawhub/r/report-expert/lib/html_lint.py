"""HTML 结构检查修复管线 — 可扩展的 lint + fix 框架

设计理念：
- 每个规则同时具备 check() 和 fix() — 发现问题就修，不只报错
- LintPipeline 按 stage 分组运行：检查→修复→确认（最多 3 轮）
- 新增检查项只需定义 LintRule 子类并注册到 default_pipeline()
- produce 模块用 body-stage 管线
- page 模块用 page-stage 管线
- verify 模块从管线生成线上验证清单

三个 stage：
  body   — 对 extract_body 输出的纯内容做检查修复
  page   — 对 generate_page_html 输出的完整页面做检查修复
  online — 不修改 HTML，只产出线上验证标准
"""

import re
from html.parser import HTMLParser
from pathlib import Path


# ── 规则基类 ──

class LintRule:
    """Lint 规则基类。子类必须同时实现 check() 和 fix()。

    设计原则：发现问题就必须有修复手段。
    如果确实无法自动修复（如内容为空），fix() 返回原 HTML，
    但这类规则应该很少，且 severity 应为 error 以阻断部署。

    Attributes:
        name: 规则名称（用于日志和标识）
        stage: 适用阶段 ('body' | 'page' | 'online')
        severity: 严重度 ('error' | 'warning' | 'info')
        description: 规则描述
    """
    name = "base"
    stage = "body"
    severity = "error"
    description = ""

    def check(self, html):
        """检查 HTML 是否满足规则。

        Returns:
            LintResult — passed=True 表示通过, passed=False 表示有问题
        """
        return LintResult(rule=self, passed=True)

    def fix(self, html):
        """自动修复 HTML 中的问题。

        Returns:
            (fixed_html, fix_log) — 修复后的 HTML 和修复日志
        """
        return html, ""

    def online_checks(self):
        """返回线上验证标准"""
        return []


class LintResult:
    """Lint 检查结果"""

    def __init__(self, rule, passed, details="", fixable=False):
        self.rule = rule
        self.passed = passed
        self.details = details
        self.fixable = fixable

    def __repr__(self):
        status = "✅" if self.passed else ("🔧" if self.fixable else "❌")
        return f"{status} [{self.rule.name}] {self.details or ('passed' if self.passed else 'failed')}"


# ── 管线 ──

class LintPipeline:
    """Lint 管线 — 按 stage 运行一组规则，检查→修复→确认。

    run() 流程：
        1. 运行所有 check()，收集 LintResult
        2. 对 failed 且 fixable 的规则，运行 fix()
        3. 修复后再运行 check() 确认（最多 3 轮）
        4. 返回最终 HTML 和最终轮检查结果
    """

    MAX_FIX_ROUNDS = 3

    def __init__(self, rules=None):
        self.rules = rules or []

    def register(self, rule):
        self.rules.append(rule)
        return self

    def check_only(self, html, stage):
        results = []
        for rule in self.rules:
            if rule.stage != stage:
                continue
            result = rule.check(html)
            results.append(result)
        return results

    def run(self, html, stage, label=""):
        current_html = html
        final_results = []

        for round_num in range(self.MAX_FIX_ROUNDS + 1):
            round_results = self.check_only(current_html, stage)

            if round_num == 0:
                for r in round_results:
                    if not r.passed:
                        print(f"  {r}")

            fixable = [r for r in round_results if not r.passed and r.fixable]
            if not fixable or round_num >= self.MAX_FIX_ROUNDS:
                final_results = round_results
                if fixable and round_num >= self.MAX_FIX_ROUNDS:
                    print(f"  ⚠️ {label} — 修复轮次已达上限，以下问题未能自动修复:")
                    for r in fixable:
                        print(f"    {r}")
                break

            for result in fixable:
                rule = result.rule
                current_html, log = rule.fix(current_html)
                if log:
                    print(f"  🔧 {label} — {rule.name}: {log}")

        return current_html, final_results

    def get_online_checks(self):
        checks = []
        for rule in self.rules:
            if rule.stage == "online":
                for item in rule.online_checks():
                    checks.append({"rule": rule.name, "check": item, "severity": rule.severity})
        return checks

    def get_failed(self, results):
        return [r for r in results if not r.passed]


# ── 辅助类 ──

class _DivCounter(HTMLParser):
    """HTMLParser 级的 div 计数器，排除 script/style 内内容"""
    def __init__(self):
        super().__init__()
        self.opens = 0
        self.closes = 0
        self._in_raw = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self._in_raw = True
        if tag == 'div' and not self._in_raw: self.opens += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self._in_raw = False
        if tag == 'div' and not self._in_raw: self.closes += 1


class _TagCounter(HTMLParser):
    """HTMLParser 级的通用标签计数器，用于找未闭合标签"""
    def __init__(self):
        super().__init__()
        self.open_tags = {}   # tag → count
        self.close_tags = {}  # tag → count
        self._in_raw = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self._in_raw = True
        if not self._in_raw:
            self.open_tags[tag] = self.open_tags.get(tag, 0) + 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self._in_raw = False
        if not self._in_raw:
            self.close_tags[tag] = self.close_tags.get(tag, 0) + 1


# ── 具体规则（全部具备 check + fix） ──


class BodyNotEmpty(LintRule):
    """检查 body 内容不为空。

    无法自动修复（空内容无法凭空生成），severity=error 阻断部署。
    """
    name = "body_not_empty"
    stage = "body"
    severity = "error"
    description = "body 必须有可见内容或结构标签"

    def check(self, html):
        text_only = re.sub(r'<[^>]+>', '', html).strip()
        has_tags = bool(re.search(r'<(?:img|table|svg|iframe|video|audio|canvas|div|p|ul|ol|h[2-6])', html))
        if not text_only and not has_tags:
            return LintResult(self, False, "内容为空（无可见文本也无结构标签）", fixable=False)
        return LintResult(self, True)


class DivBalance(LintRule):
    """检查并修复 div 开闭标签不平衡"""
    name = "div_balance"
    stage = "body"
    severity = "error"
    description = "div 开闭标签数量必须相等（排除 script/style 内内容）"

    def check(self, html):
        counter = _DivCounter()
        counter.feed(html)
        diff = counter.opens - counter.closes
        if diff != 0:
            direction = "多余" if diff < 0 else "缺失"
            count = abs(diff)
            return LintResult(self, False,
                              f"div 不平衡: {direction} {count} 个 </div> (opens={counter.opens} closes={counter.closes})",
                              fixable=True)
        return LintResult(self, True)

    def fix(self, html):
        counter = _DivCounter()
        counter.feed(html)
        diff = counter.opens - counter.closes

        if diff < 0:
            removed = 0
            for _ in range(abs(diff)):
                new_html = re.sub(r'\s*</div>(\s*)$', r'\1', html, count=1)
                if new_html != html:
                    html = new_html
                    removed += 1
            return html, f"移除尾部 {removed} 个多余 </div>"
        elif diff > 0:
            html += '</div>' * diff
            return html, f"补充 {diff} 个缺失 </div>"
        return html, ""


class NoDuplicateWrapper(LintRule):
    """检查并剥离多余的 report-wrap / page-body wrapper"""
    name = "no_duplicate_wrapper"
    stage = "body"
    severity = "error"
    description = "不允许重复的 report-wrap 或 page-body，自动剥离多余的 wrapper"

    WRAPPER_CLASSES = ['report-wrap', 'page-body', 'wrap']

    def check(self, html):
        issues = []
        for cls in self.WRAPPER_CLASSES:
            count = html.count(f'class="{cls}"')
            if count > 1:
                issues.append((cls, count))
        if issues:
            return LintResult(self, False,
                              f"重复 wrapper: {', '.join(f'{c}({n}个)' for c,n in issues)}",
                              fixable=True)
        return LintResult(self, True)

    def fix(self, html):
        """剥离多余的 wrapper div（保留第一个）"""
        total_unwrapped = 0
        for cls in self.WRAPPER_CLASSES:
            count = html.count(f'class="{cls}"')
            if count <= 1:
                continue
            # Iteratively unwrap: find the Nth occurrence and strip its open+close tags
            # Strategy: keep first, unwrap rest by removing <div class="cls"...> and its matching </div>
            for _ in range(count - 1):
                # Find first occurrence after the one we're keeping
                first_pos = html.find(f'class="{cls}"')
                # Find next occurrence
                next_pos = html.find(f'class="{cls}"', first_pos + 1)
                if next_pos == -1:
                    break
                # Find the <div that contains this class
                div_start = html.rfind('<div', 0, next_pos)
                # Find matching </div> by tracking depth from the opening tag
                depth = 1
                pos = html.find('>', div_start) + 1
                while pos < len(html) and depth > 0:
                    next_open = re.search(r'<div[\s>]', html[pos:])
                    next_close = re.search(r'</div>', html[pos:])
                    if not next_close:
                        break
                    if next_open and next_open.start() < next_close.start():
                        depth += 1
                        pos += next_open.end()
                    else:
                        depth -= 1
                        if depth == 0:
                            close_start = pos + next_close.start()
                            close_end = pos + next_close.end()
                            html = html[:div_start] + html[html.find('>', div_start) + 1:close_start] + html[close_end:]
                            total_unwrapped += 1
                            break
                        pos += next_close.end()

        return html, f"剥离 {total_unwrapped} 个多余 wrapper"


class NoFrameworkChrome(LintRule):
    """检查并移除 body 中的模板 chrome 元素"""
    name = "no_framework_chrome"
    stage = "body"
    severity = "warning"
    description = "提取后的 body 不应包含模板 chrome，自动移除"

    CHROME_REMOVALS = [
        # (regex pattern, label, flags)
        (r'<header[^>]*class="report-header"[^>]*>.*?</header>', 'report-header', re.DOTALL),
        (r'<footer[^>]*class="page-footer"[^>]*>.*?</footer>', 'page-footer', re.DOTALL),
        (r'<button[^>]*class="back-to-top"[^>]*>.*?</button>', 'back-to-top', re.DOTALL),
        (r'<aside[^>]*class="toc-sidebar"[^>]*>.*?</aside>', 'toc-sidebar', re.DOTALL),
        (r'<button[^>]*class="toc-toggle"[^>]*>.*?</button>', 'toc-toggle', re.DOTALL),
        (r'<div[^>]*class="scroll-progress"[^>]*></div>', 'scroll-progress', 0),
        (r'<script[^>]*src="[^"]*main\.js[^"]*"[^>]*></script>', 'main.js script', 0),
        (r'<script[^>]*src="[^"]*echarts[^"]*"[^>]*></script>', 'echarts script', 0),
        (r'<script[^>]*src="[^"]*mermaid[^"]*"[^>]*></script>', 'mermaid script', 0),
        (r'<script[^>]*src="[^"]*chart\.js[^"]*"[^>]*></script>', 'chart.js script', 0),
        (r'<script>\s*(?:new\s+ECharts|var\s+chart\s*=|echarts\.init|//\s*echarts).*?</script>', 'echarts init', re.DOTALL),
        (r'<script>\s*mermaid\.initialize.*?</script>', 'mermaid init', re.DOTALL),
    ]

    def check(self, html):
        found = []
        for pattern, label, flags in self.CHROME_REMOVALS:
            if re.search(pattern, html, flags):
                found.append(label)
        if found:
            return LintResult(self, False, f"发现模板 chrome: {', '.join(found)}", fixable=True)
        return LintResult(self, True)

    def fix(self, html):
        removed = []
        for pattern, label, flags in self.CHROME_REMOVALS:
            new_html = re.sub(pattern, '', html, flags=flags)
            if new_html != html:
                html = new_html
                removed.append(label)
        log = f"移除 chrome: {', '.join(removed)}" if removed else ""
        return html.strip(), log


class ImgPathAbsolute(LintRule):
    """检查并修复图片路径为绝对路径"""
    name = "img_path_absolute"
    stage = "body"
    severity = "error"
    description = "图片 src 必须使用绝对路径 /images/xxx"

    def check(self, html):
        # Only match src inside <img> tags (not in prose/code blocks)
        relative_imgs = re.findall(r'<img[^>]*\ssrc="((?:\.\./)?images/[^"]+)"[^>]*>', html)
        if not relative_imgs:
            relative_imgs = re.findall(r'<img[^>]*\ssrc=\'((?:\.\./)?images/[^\']+)\'[^>]*>', html)
        if relative_imgs:
            return LintResult(self, False,
                              f"图片使用相对路径: {', '.join(relative_imgs[:3])}",
                              fixable=True)
        return LintResult(self, True)

    def fix(self, html):
        # Only fix src inside <img> tags
        html = re.sub(r'<img([^>]*\s)src="(\.\./)?images/', r'<img\1src="/images/', html)
        html = re.sub(r'<img([^>]*\s)src=\'(\.\./)?images/', r'<img\1src=\'/images/', html)
        return html, "图片路径改为绝对 /images/"


class ScriptSafety(LintRule):
    """检查并移除危险 script 内容"""
    name = "script_safety"
    stage = "body"
    severity = "warning"
    description = "内联 script 不应包含敏感 API 调用，自动移除危险 script 标签"

    DANGEROUS_PATTERNS = [
        (r'document\.cookie', 'document.cookie'),
        (r'localStorage', 'localStorage'),
        (r'sessionStorage', 'sessionStorage'),
        (r'eval\(', 'eval()'),
        (r'new\s+Function\(', 'new Function()'),
    ]

    def check(self, html):
        # Only check inside <script> tags, not in code blocks or prose
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
        found = []
        for script_content in scripts:
            for pattern, label in self.DANGEROUS_PATTERNS:
                if re.search(pattern, script_content):
                    found.append(label)
        # Also check inline event handlers (onclick/onerror containing dangerous patterns)
        inline_handlers = re.findall(r'on(?:click|error|load|mouseover|focus|blur)\s*=\s*["\'](.*?)["\']', html, re.IGNORECASE)
        for handler in inline_handlers:
            for pattern, label in self.DANGEROUS_PATTERNS:
                if re.search(pattern, handler):
                    found.append(label)
        if found:
            found = list(set(found))  # deduplicate
            return LintResult(self, False, f"发现危险 script: {', '.join(found)}", fixable=True)
        return LintResult(self, True)

    def fix(self, html):
        """移除包含危险内容的 inline script 标签"""
        removed = 0
        # Remove <script>...</script> blocks that contain dangerous patterns
        for pattern, _ in self.DANGEROUS_PATTERNS:
            def should_remove(m):
                return '' if re.search(pattern, m.group(0)) else m.group(0)
            new_html = re.sub(r'<script[^>]*>.*?</script>', should_remove, html, flags=re.DOTALL)
            if new_html != html:
                html = new_html
                removed += 1
        return html, f"移除 {removed} 个危险 script"


class TagBalance(LintRule):
    """检查并修复非 div 标签的闭合平衡"""
    name = "tag_balance"
    stage = "body"
    severity = "warning"
    description = "非 div 标签也应闭合平衡（p/span/a/ul 等），自动补充缺失闭合标签"

    # 只检查需要闭合的关键语义标签（排除自闭合标签和允许不闭合的标签）
    CHECK_TAGS = ['p', 'span', 'a', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
                   'h2', 'h3', 'h4', 'h5', 'h6', 'section', 'article', 'aside', 'details', 'summary']

    def check(self, html):
        counter = _TagCounter()
        counter.feed(html)
        issues = []
        for tag in self.CHECK_TAGS:
            opens = counter.open_tags.get(tag, 0)
            closes = counter.close_tags.get(tag, 0)
            if opens != closes:
                issues.append(f'{tag}: opens={opens} closes={closes}')
        if issues:
            return LintResult(self, False, f"标签不平衡: {', '.join(issues)}", fixable=True)
        return LintResult(self, True)

    def fix(self, html):
        """补充缺失的闭合标签到末尾"""
        counter = _TagCounter()
        counter.feed(html)
        additions = []
        for tag in self.CHECK_TAGS:
            opens = counter.open_tags.get(tag, 0)
            closes = counter.close_tags.get(tag, 0)
            diff = opens - closes
            if diff > 0:
                additions.append(f'</{tag}>' * diff)
        if additions:
            html += '\n'.join(additions)
            return html, f"补充闭合标签: {', '.join(additions)}"
        return html, ""


class StyleConflict(LintRule):
    """检查并修复 style 冲突：body 中不应有全局样式覆盖模板"""
    name = "style_conflict"
    stage = "body"
    severity = "warning"
    description = "body 中的 <style> 标签不应覆盖模板全局样式，自动隔离为 scoped"

    # 检查会覆盖模板核心样式的全局选择器
    CONFLICT_SELECTORS = [
        r'^body\s*\{',       # only top-level body selector (not .page-body body)
        r'^\.report-wrap\s*\{',
        r'^\.page-body\s*\{',
        r'^\.page-footer\s*\{',
    ]

    def check(self, html):
        styles = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
        conflicts = []
        for css in styles:
            for pattern in self.CONFLICT_SELECTORS:
                if re.search(pattern, css, re.MULTILINE):
                    conflicts.append(pattern.replace(r'^', '').replace(r'\s*\{', '').replace(r'\.', '').strip())
        if conflicts:
            return LintResult(self, False, f"发现样式冲突: {', '.join(conflicts)}", fixable=True)
        return LintResult(self, True)

    def fix(self, html):
        """将冲突的全局选择器加 .page-body 前缀隔离"""
        def scope_style(m):
            tag_attrs = m.group(1)
            css = m.group(2)
            # Direct string replacements for each conflict selector
            css = re.sub(r'^body\s*\{', '.page-body body {', css, flags=re.MULTILINE)
            css = re.sub(r'^\.report-wrap\s*\{', '.page-body .report-wrap {', css, flags=re.MULTILINE)
            css = re.sub(r'^\.page-body\s*\{', '.page-body .page-body {', css, flags=re.MULTILINE)
            css = re.sub(r'^\.page-footer\s*\{', '.page-body .page-footer {', css, flags=re.MULTILINE)
            return f'<style{tag_attrs}>{css}</style>'

        html = re.sub(r'<style([^>]*)>(.*?)</style>', scope_style, html, flags=re.DOTALL)
        return html, "样式冲突选择器已添加 .page-body 前缀隔离"


class PageStructure(LintRule):
    """检查完整页面结构，自动修复缺失的必要元素"""
    name = "page_structure"
    stage = "page"
    severity = "error"
    description = "完整页面必须包含必要结构元素，无法自动修复则阻断部署"

    REQUIRED = {
        'class="report-wrap"': 'report-wrap',
        'class="page-body"': 'page-body',
        'class="page-footer"': 'page-footer',
        '/styles/base.css': 'base.css',
        '/scripts/main.js': 'main.js',
        '<html': 'html 标签',
        '</html>': 'html 闭合',
        '<head': 'head 标签',
        '</head>': 'head 闭合',
        '<body': 'body 标签',
        '</body>': 'body 闭合',
    }

    def check(self, html):
        issues = []
        for marker, label in self.REQUIRED.items():
            if marker not in html:
                issues.append(f"缺少 {label}")
        if issues:
            # page 结构问题通常是 generate_page_html 出错，无法自动修复
            return LintResult(self, False, "; ".join(issues), fixable=False)
        return LintResult(self, True)


class PageDivBalance(LintRule):
    """检查并修复完整页面的 div 平衡"""
    name = "page_div_balance"
    stage = "page"
    severity = "error"
    description = "完整页面的 div 开闭标签必须平衡，自动修复"

    def check(self, html):
        counter = _DivCounter()
        counter.feed(html)
        diff = counter.opens - counter.closes
        if diff != 0:
            return LintResult(self, False,
                              f"页面 div 不平衡: diff={diff} (opens={counter.opens} closes={counter.closes})",
                              fixable=True)
        return LintResult(self, True)

    def fix(self, html):
        counter = _DivCounter()
        counter.feed(html)
        diff = counter.opens - counter.closes

        if diff < 0:
            removed = 0
            for _ in range(abs(diff)):
                new_html = re.sub(r'\s*</div>(\s*)$', r'\1', html, count=1)
                if new_html != html:
                    html = new_html
                    removed += 1
            return html, f"移除尾部 {removed} 个多余 </div>"
        elif diff > 0:
            # 补充在 </body> 之前
            html = html.replace('</body>', '</div>' * diff + '</body>')
            return html, f"补充 {diff} 个缺失 </div>"
        return html, ""


class PageImgIntegrity(LintRule):
    """检查页面中所有图片 src 有对应文件在 dist/images/，并修复缺失引用"""
    name = "page_img_integrity"
    stage = "page"
    severity = "warning"
    description = "图片 src 对应的文件应存在于 dist，缺失的自动标记为 broken"

    def __init__(self, dist_dir=None):
        super().__init__()
        self.dist_dir = dist_dir

    def check(self, html):
        if not self.dist_dir:
            return LintResult(self, True)
        img_srcs = re.findall(r'<img[^>]*\ssrc="/images/([^"]+)"[^>]*>', html)
        missing = []
        for name in img_srcs:
            img_path = self.dist_dir / "images" / name
            if not img_path.exists():
                missing.append(name)
        if missing:
            return LintResult(self, False,
                              f"缺失图片文件: {', '.join(missing[:5])}",
                              fixable=True)
        return LintResult(self, True)

    def fix(self, html):
        """将缺失图片的 src 替换为占位图"""
        if not self.dist_dir:
            return html, ""
        img_srcs = re.findall(r'<img[^>]*\ssrc="/images/([^"]+)"[^>]*>', html)
        replaced = 0
        for name in img_srcs:
            img_path = self.dist_dir / "images" / name
            if not img_path.exists():
                # Replace with a placeholder SVG (inline, no external dependency)
                placeholder = f'src="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'200\' height=\'150\'><rect fill=\'%23f0f0f0\' width=\'200\' height=\'150\'/><text x=\'50%25\' y=\'50%25\' text-anchor=\'middle\' fill=\'%23999\' font-size=\'14\'>图片缺失</text></svg>"'
                html = html.replace(f'src="/images/{name}"', placeholder)
                replaced += 1
        return html, f"替换 {replaced} 个缺失图片为占位图"


class OnlineReportChecks(LintRule):
    name = "online_report"
    stage = "online"
    severity = "error"
    description = "线上报告页面的验证标准"

    def online_checks(self):
        return [
            "HTTP 可达（非 404/5xx）",
            "包含 report-wrap 容器",
            "包含 page-body 内容区",
            "引用 /styles/base.css",
            "引用 /scripts/main.js",
            "div 标签闭合平衡",
            "图片 src 使用绝对路径 /images/",
            "无模板 chrome 遗留",
        ]


class OnlineAssetChecks(LintRule):
    name = "online_assets"
    stage = "online"
    severity = "error"
    description = "线上静态资源的验证标准"

    def online_checks(self):
        return [
            "CSS/JS HTTP 可达且内容非空",
            "index.json 可解析且 pages 数量与 dist 文件一致",
            "images/ 目录中图片为真实图片文件（非 HTML fallback）",
        ]


class OnlineImageChecks(LintRule):
    name = "online_images"
    stage = "online"
    severity = "warning"
    description = "线上图片资源的验证标准"

    def online_checks(self):
        return [
            "所有 <img> src 返回真实图片（Content-Type 为 image/*）",
            "图片不是 HTML fallback（SPA 路由导致的 index.html 伪装）",
            "图片文件大小 > 0",
        ]


# ── 默认管线 ──

def default_pipeline(dist_dir=None):
    """创建默认 lint 管线"""
    return LintPipeline([
        # body stage — 检查提取后的纯内容
        BodyNotEmpty(),
        DivBalance(),
        NoDuplicateWrapper(),
        NoFrameworkChrome(),
        ImgPathAbsolute(),
        ScriptSafety(),
        TagBalance(),
        StyleConflict(),
        # page stage — 检查注入模板后的完整页面
        PageStructure(),
        PageDivBalance(),
        PageImgIntegrity(dist_dir=dist_dir),
        # online stage — 线上验证标准
        OnlineReportChecks(),
        OnlineAssetChecks(),
        OnlineImageChecks(),
    ])


# ── 便捷函数 ──

def lint_body(body, label="", dist_dir=None):
    pipeline = default_pipeline(dist_dir=dist_dir)
    fixed, results = pipeline.run(body, "body", label)
    failed = pipeline.get_failed(results)
    return fixed, failed


def lint_page(page_html, label="", dist_dir=None):
    pipeline = default_pipeline(dist_dir=dist_dir)
    fixed, results = pipeline.run(page_html, "page", label)
    failed = pipeline.get_failed(results)
    return fixed, failed


def lint_online_checks():
    pipeline = default_pipeline()
    return pipeline.get_online_checks()


def check_body(body, label=""):
    pipeline = default_pipeline()
    return pipeline.check_only(body, "body")


def check_page(page_html, label=""):
    pipeline = default_pipeline()
    return pipeline.check_only(page_html, "page")