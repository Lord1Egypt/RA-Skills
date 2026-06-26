#!/usr/bin/env python3
"""
CS Browser CLI：给 AI agent 使用的一行式浏览器控制工具。

用法：
    python browser.py exec <javascript>            执行 JS 并返回结构化结果
    python browser.py scan                         获取简化后的页面 HTML
    python browser.py evidence <selector>          导出渲染后的组件证据
    python browser.py tabs                         列出所有浏览器 tab
    python browser.py navigate <url>               打开 URL
    python browser.py back                         后退
    python browser.py forward                      前进
    python browser.py reload                       重新加载当前页
    python browser.py newtab [url]                 打开新 tab
    python browser.py close [tab_id]               关闭 tab
    python browser.py switch <url-pattern>         切换到匹配的 tab
    python browser.py screenshot [filepath]        截图

示例：
    python browser.py exec "document.title"
    python browser.py exec "document.querySelector('.btn').click()"
    python browser.py scan --text-only
    python browser.py scan --tabs-only
    python browser.py scan --size-only
    python browser.py tabs
    python browser.py navigate "https://example.com"
    python browser.py switch "github"
    python browser.py screenshot
    python browser.py screenshot page.png
"""

import sys, os, json, argparse, io, base64, time

# ── Windows 上强制使用 UTF-8 ──────────────────────────────────────────
# Windows 控制台默认常是 GBK，遇到 © 等字符会失败
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

_skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _skill_dir not in sys.path:
    sys.path.insert(0, _skill_dir)


def main():
    parser = argparse.ArgumentParser(prog='browser', description='CS 浏览器控制 CLI')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_exec = sub.add_parser('exec', help='在浏览器中执行 JavaScript')
    p_exec.add_argument('script', help='要执行的 JavaScript 代码')
    p_exec.add_argument('--tab', help='目标 tab ID')
    p_exec.add_argument('--no-monitor', action='store_true', help='跳过 DOM diff 监控')
    p_exec.add_argument('--wait', help='执行前等待出现的 CSS selector')
    p_exec.add_argument('--wait-ms', type=int, default=10000, help='最长等待毫秒数（默认：10000）')
    p_exec.add_argument('--timeout', type=int, default=15, help='执行超时秒数（默认：15）')

    p_scan = sub.add_parser('scan', help='获取简化后的页面内容')
    p_scan.add_argument('--tabs-only', action='store_true', help='只返回 tab 列表')
    p_scan.add_argument('--text-only', action='store_true', help='只返回文本，减少 token')
    p_scan.add_argument('--size-only', action='store_true', help='只返回内容大小，不返回内容本身')
    p_scan.add_argument('--tab', help='要扫描的 tab ID')
    p_scan.add_argument('--wait', help='扫描前等待出现的 CSS selector，适合 SPA')
    p_scan.add_argument('--wait-ms', type=int, default=10000, help='最长等待毫秒数（默认：10000）')

    p_evidence = sub.add_parser('evidence', help='导出组件的渲染 DOM、样式、结构和截图证据')
    p_evidence.add_argument('selector', help='组件根节点的 CSS selector')
    p_evidence.add_argument('--name', default='component', help='组件名，用于 metadata 和输出目录')
    p_evidence.add_argument('--out', help='输出目录（默认：component-evidence/<name>）')
    p_evidence.add_argument('--index', type=int, default=0, help='selector 匹配多个元素时使用的序号')
    p_evidence.add_argument('--depth', type=int, default=4, help='后代结构深度')
    p_evidence.add_argument('--tab', help='目标 tab ID')
    p_evidence.add_argument('--wait', help='抽取前等待出现的 CSS selector')
    p_evidence.add_argument('--wait-ms', type=int, default=10000, help='最长等待毫秒数（默认：10000）')
    p_evidence.add_argument('--all-styles', action='store_true', help='捕获全部 computed styles，而不只重要 UI 样式')

    sub.add_parser('tabs', help='列出所有浏览器 tab')

    p_nav = sub.add_parser('navigate', help='打开 URL')
    p_nav.add_argument('url', help='要打开的 URL')
    p_nav.add_argument('--no-wait', action='store_true', help='不等待页面加载')

    sub.add_parser('back', help='浏览器历史后退')
    sub.add_parser('forward', help='浏览器历史前进')
    sub.add_parser('reload', help='重新加载当前页面')

    p_newtab = sub.add_parser('newtab', help='打开新 tab')
    p_newtab.add_argument('url', nargs='?', help='可选 URL')

    p_close = sub.add_parser('close', help='关闭 tab')
    p_close.add_argument('tab_id', nargs='?', help='要关闭的 tab ID，默认当前 tab')

    p_switch = sub.add_parser('switch', help='切换到匹配的 tab')
    p_switch.add_argument('pattern', help='要匹配的 URL 片段')

    p_screenshot = sub.add_parser('screenshot', help='截取当前 tab')
    p_screenshot.add_argument('filepath', nargs='?', help='保存 PNG 的路径，默认自动放到临时目录')

    args = parser.parse_args()

    # ── 把模块日志重定向到 stderr ─────────────────────────────────────
    # TMWebDriver 和 simphtml 会把连接日志、执行进度打印到 stdout。
    # 这里转到 stderr，确保 stdout 只输出干净的 JSON 结果。
    _real_stdout = sys.stdout
    sys.stdout = sys.stderr
    try:
        from tmwd_bridge import (
            init_browser, web_execute_js, web_scan,
            list_tabs, web_navigate, web_back, web_forward, web_reload,
            web_newtab, web_close, web_screenshot, switch_tab, get_driver
        )
        init_browser()

        if args.cmd == 'exec':
            result = web_execute_js(args.script, switch_tab_id=args.tab, no_monitor=args.no_monitor,
                                    wait_selector=args.wait, wait_ms=args.wait_ms, timeout=args.timeout)
        elif args.cmd == 'scan':
            result = web_scan(tabs_only=args.tabs_only, switch_tab_id=args.tab,
                              text_only=args.text_only, size_only=args.size_only,
                              wait_selector=args.wait, wait_ms=args.wait_ms)
        elif args.cmd == 'evidence':
            result = export_component_evidence(args, web_execute_js, web_screenshot, get_driver)
        elif args.cmd == 'tabs':
            result = {'status': 'success', 'sessions': list_tabs()}
        elif args.cmd == 'navigate':
            result = web_navigate(args.url, wait_load=not args.no_wait)
        elif args.cmd == 'back':
            result = web_back()
        elif args.cmd == 'forward':
            result = web_forward()
        elif args.cmd == 'reload':
            result = web_reload()
        elif args.cmd == 'newtab':
            result = web_newtab(args.url)
        elif args.cmd == 'close':
            result = web_close(args.tab_id)
        elif args.cmd == 'switch':
            sid = switch_tab(args.pattern)
            result = {'status': 'success' if sid else 'error', 'session_id': sid}
        elif args.cmd == 'screenshot':
            result = web_screenshot(args.filepath)
    except Exception as e:
        result = {'status': 'error', 'msg': str(e)}
    finally:
        sys.stdout = _real_stdout

    # ── stdout 只输出一行干净 JSON ───────────────────────────────────
    print(json.dumps(result, ensure_ascii=False, default=str))


STYLE_PROPS = [
    'display', 'position', 'box-sizing',
    'width', 'height', 'min-width', 'min-height', 'max-width', 'max-height',
    'margin', 'margin-top', 'margin-right', 'margin-bottom', 'margin-left',
    'padding', 'padding-top', 'padding-right', 'padding-bottom', 'padding-left',
    'border', 'border-width', 'border-style', 'border-color', 'border-radius',
    'background', 'background-color', 'color',
    'font-family', 'font-size', 'font-weight', 'font-style', 'line-height', 'letter-spacing',
    'text-align', 'text-transform', 'white-space', 'overflow', 'overflow-x', 'overflow-y', 'text-overflow',
    'opacity', 'transform', 'translate', 'scale', 'rotate', 'transform-origin', 'transition', 'animation',
    'inset', 'top', 'right', 'bottom', 'left',
    'box-shadow', 'outline', 'outline-color', 'outline-width', 'outline-style',
    'cursor', 'pointer-events', 'appearance', 'accent-color',
    'align-items', 'justify-content', 'justify-items', 'gap', 'row-gap', 'column-gap',
    'flex-direction', 'flex-shrink', 'flex-grow',
    'grid-template-columns', 'grid-template-rows', 'z-index',
]


def _safe_name(value):
    import re
    value = re.sub(r'[^a-zA-Z0-9_-]+', '-', str(value or 'component').strip()).strip('-').lower()
    return value or 'component'


def _write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        f.write('\n')


def _decode_js_return(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return value
    return value


def _extract_script(selector, index, depth, all_styles):
    return f"""
return (() => {{
  const selector = {json.dumps(selector)};
  const index = {int(index)};
  const depth = {int(depth)};
  const allStyles = {str(bool(all_styles)).lower()};
  const styleProps = {json.dumps(STYLE_PROPS)};
  const matches = Array.from(document.querySelectorAll(selector));
  const element = matches[index];
  if (!element) {{
    return {{ status: 'error', msg: `No element matched selector ${{selector}} at index ${{index}}`, matchedCount: matches.length }};
  }}

  function attrs(node) {{
    return Object.fromEntries(Array.from(node.attributes || []).map(attr => [attr.name, attr.value]));
  }}

  function rect(node) {{
    const r = node.getBoundingClientRect();
    return {{ x: r.x, y: r.y, width: r.width, height: r.height, top: r.top, right: r.right, bottom: r.bottom, left: r.left }};
  }}

  function computed(node, pseudo) {{
    const styles = getComputedStyle(node, pseudo || undefined);
    const props = allStyles ? Array.from(styles) : styleProps;
    const result = {{}};
    for (const prop of props) result[prop] = styles.getPropertyValue(prop);
    return result;
  }}

  function pseudo(node, name) {{
    const styles = computed(node, name);
    const content = styles.content;
    if (!content || content === 'none' || content === 'normal') return null;
    return styles;
  }}

  function summarize(node, remainingDepth) {{
    if (node.nodeType !== Node.ELEMENT_NODE) {{
      return {{ nodeType: node.nodeType, text: (node.textContent || '').replace(/\\s+/g, ' ').trim() }};
    }}
    const children = remainingDepth > 0
      ? Array.from(node.childNodes)
          .filter(child => child.nodeType === Node.ELEMENT_NODE || (child.textContent || '').trim())
          .map(child => summarize(child, remainingDepth - 1))
      : [];
    return {{
      tag: node.tagName.toLowerCase(),
      attributes: attrs(node),
      dataset: {{ ...node.dataset }},
      classList: Array.from(node.classList || []),
      role: node.getAttribute('role'),
      aria: Object.fromEntries(Array.from(node.attributes || []).filter(attr => attr.name.startsWith('aria-')).map(attr => [attr.name, attr.value])),
      text: (node.textContent || '').replace(/\\s+/g, ' ').trim(),
      box: rect(node),
      computed: computed(node),
      pseudo: {{ before: pseudo(node, '::before'), after: pseudo(node, '::after') }},
      children
    }};
  }}

  element.scrollIntoView({{ block: 'center', inline: 'center' }});

  return {{
    status: 'success',
    url: location.href,
    title: document.title,
    selector,
    index,
    matchedCount: matches.length,
    outerHTML: element.outerHTML,
    attributes: attrs(element),
    dataset: {{ ...element.dataset }},
    classList: Array.from(element.classList || []),
    role: element.getAttribute('role'),
    aria: Object.fromEntries(Array.from(element.attributes || []).filter(attr => attr.name.startsWith('aria-')).map(attr => [attr.name, attr.value])),
    text: (element.textContent || '').replace(/\\s+/g, ' ').trim(),
    box: {{
      rect: rect(element),
      offsetWidth: element.offsetWidth,
      offsetHeight: element.offsetHeight,
      clientWidth: element.clientWidth,
      clientHeight: element.clientHeight,
      scrollWidth: element.scrollWidth,
      scrollHeight: element.scrollHeight
    }},
    computed: computed(element),
    pseudo: {{ before: pseudo(element, '::before'), after: pseudo(element, '::after') }},
    anatomy: summarize(element, depth)
  }};
}})()
"""


def _capture_clip(driver, filepath, rect):
    x = max(0, float(rect.get('x', 0)))
    y = max(0, float(rect.get('y', 0)))
    width = max(1, float(rect.get('width', 1)))
    height = max(1, float(rect.get('height', 1)))
    payload = {
        "cmd": "cdp",
        "method": "Page.captureScreenshot",
        "params": {
            "format": "png",
            "clip": {"x": x, "y": y, "width": width, "height": height, "scale": 1}
        }
    }
    response = driver.execute_js(json.dumps(payload))
    data = response.get('data', {}) if isinstance(response, dict) else {}
    b64 = data.get('data') if isinstance(data, dict) else None
    if not b64:
        return {'status': 'error', 'msg': 'Element screenshot returned no image data'}
    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(b64))
    return {'status': 'success', 'filepath': filepath}


def export_component_evidence(args, web_execute_js, web_screenshot, get_driver):
    name = args.name or 'component'
    out_dir = os.path.abspath(args.out or os.path.join('component-evidence', _safe_name(name)))
    os.makedirs(out_dir, exist_ok=True)

    script = _extract_script(args.selector, args.index, args.depth, args.all_styles)
    exec_result = web_execute_js(
        script,
        switch_tab_id=args.tab,
        no_monitor=True,
        wait_selector=args.wait or args.selector,
        wait_ms=args.wait_ms,
        timeout=20
    )
    evidence = _decode_js_return(exec_result.get('js_return'))

    if not isinstance(evidence, dict) or evidence.get('status') != 'success':
        return {'status': 'error', 'msg': 'Evidence extraction failed', 'exec_result': exec_result, 'evidence': evidence}

    with open(os.path.join(out_dir, 'dom.html'), 'w', encoding='utf-8') as f:
        f.write(evidence.get('outerHTML', '') + '\n')
    with open(os.path.join(out_dir, 'class-list.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(evidence.get('classList', [])) + '\n')

    _write_json(os.path.join(out_dir, 'attributes.json'), {
        'attributes': evidence.get('attributes', {}),
        'dataset': evidence.get('dataset', {}),
        'role': evidence.get('role'),
        'aria': evidence.get('aria', {}),
    })
    _write_json(os.path.join(out_dir, 'box-model.json'), evidence.get('box', {}))
    _write_json(os.path.join(out_dir, 'computed-styles.json'), evidence.get('computed', {}))
    _write_json(os.path.join(out_dir, 'anatomy.json'), evidence.get('anatomy', {}))
    _write_json(os.path.join(out_dir, 'metadata.json'), {
        'component': name,
        'selector': args.selector,
        'index': args.index,
        'matchedCount': evidence.get('matchedCount'),
        'url': evidence.get('url'),
        'title': evidence.get('title'),
        'tab_id': exec_result.get('tab_id'),
        'capturedAt': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    })

    page_path = os.path.join(out_dir, 'page.png')
    page_shot = web_screenshot(page_path)

    element_path = os.path.join(out_dir, 'screenshot.png')
    clip_shot = _capture_clip(get_driver(), element_path, evidence.get('box', {}).get('rect', {}))

    readme = f"""# Component Evidence: {name}

Captured from: {evidence.get('url')}

Selector: `{args.selector}`

Matched elements: {evidence.get('matchedCount')}; captured index: {args.index}

## Files

- `dom.html`: rendered outerHTML for the selected element.
- `attributes.json`: role, aria, data attributes, and all element attributes.
- `class-list.txt`: class names, one per line.
- `box-model.json`: bounding/client/scroll dimensions.
- `computed-styles.json`: important computed styles.
- `anatomy.json`: recursive element anatomy with attributes, boxes, styles, and children.
- `screenshot.png`: screenshot of the selected element.
- `page.png`: full page screenshot for composition context.

Use this evidence as canonical component anatomy before approximating from screenshots.
"""
    with open(os.path.join(out_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme)

    return {
        'status': 'success',
        'out_dir': out_dir,
        'files': sorted(os.listdir(out_dir)),
        'page_screenshot': page_shot,
        'element_screenshot': clip_shot,
        'metadata': {
            'component': name,
            'selector': args.selector,
            'matchedCount': evidence.get('matchedCount'),
            'url': evidence.get('url'),
        }
    }


if __name__ == '__main__':
    main()
