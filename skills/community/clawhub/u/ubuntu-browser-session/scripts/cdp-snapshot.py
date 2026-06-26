#!/usr/bin/env python3
"""Capture a structured snapshot of a browser page via CDP.

Reuses the low-level CDP helpers from cdp-eval.py (same directory) so
there is no duplicated websocket code.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys

# Import shared CDP helpers from the sibling module (hyphenated filename).
_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("cdp_eval", os.path.join(_here, "cdp-eval.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
CdpError = _mod.CdpError
evaluate = _mod.evaluate

# ---------------------------------------------------------------------------
# JavaScript extraction snippets
# ---------------------------------------------------------------------------

_JS_MARKDOWN = r"""(() => {
  const lines = [];
  const title = document.title || '';
  if (title) lines.push('# ' + title, '');
  const url = location.href || '';
  if (url) lines.push('URL: ' + url, '');

  function walkNode(node, depth) {
    if (node.nodeType === Node.TEXT_NODE) {
      const t = node.textContent.trim();
      if (t) lines.push(t);
      return;
    }
    if (node.nodeType !== Node.ELEMENT_NODE) return;
    const tag = node.tagName;
    if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'SVG'].includes(tag)) return;

    if (tag === 'H1') lines.push('', '# ' + (node.innerText || '').trim(), '');
    else if (tag === 'H2') lines.push('', '## ' + (node.innerText || '').trim(), '');
    else if (tag === 'H3') lines.push('', '### ' + (node.innerText || '').trim(), '');
    else if (tag === 'H4') lines.push('', '#### ' + (node.innerText || '').trim(), '');
    else if (tag === 'H5') lines.push('', '##### ' + (node.innerText || '').trim(), '');
    else if (tag === 'H6') lines.push('', '###### ' + (node.innerText || '').trim(), '');
    else if (tag === 'A') {
      const href = node.getAttribute('href') || '';
      const text = (node.innerText || '').trim();
      if (text && href) lines.push('[' + text + '](' + href + ')');
      else if (text) lines.push(text);
      return;  // don't recurse into links
    }
    else if (tag === 'LI') {
      lines.push('- ' + (node.innerText || '').trim());
      return;
    }
    else if (tag === 'P' || tag === 'DIV' || tag === 'SECTION' || tag === 'ARTICLE') {
      // recurse into block elements
      for (const child of node.childNodes) walkNode(child, depth + 1);
      lines.push('');
      return;
    }
    else if (tag === 'BR') { lines.push(''); return; }
    else if (tag === 'IMG') {
      const alt = node.getAttribute('alt') || '';
      if (alt) lines.push('[image: ' + alt + ']');
      return;
    }
    else {
      for (const child of node.childNodes) walkNode(child, depth + 1);
      return;
    }
  }

  if (document.body) walkNode(document.body, 0);

  // collapse multiple blank lines
  const collapsed = [];
  let lastBlank = false;
  for (const line of lines) {
    if (line === '') {
      if (!lastBlank) collapsed.push('');
      lastBlank = true;
    } else {
      collapsed.push(line);
      lastBlank = false;
    }
  }
  return { title, url, content: collapsed.join('\n') };
})()"""

_JS_TEXT = r"""(() => {
  const title = document.title || '';
  const url = location.href || '';
  const text = document.body ? (document.body.innerText || '') : '';
  return { title, url, content: text };
})()"""

_JS_LINKS = r"""(() => {
  const title = document.title || '';
  const url = location.href || '';
  const anchors = Array.from(document.querySelectorAll('a[href]'));
  const links = anchors.map(a => ({
    text: (a.innerText || '').trim(),
    href: a.href
  })).filter(l => l.text && l.href);
  return { title, url, content: JSON.stringify(links) };
})()"""

_JS_TOPIC_LINKS = r"""(() => {
  const title = document.title || '';
  const url = location.href || '';
  const normalizeText = (value) => (value || '').replace(/\s+/g, ' ').trim();
  const toAbsoluteHref = (href) => {
    if (!href) return '';
    try {
      const u = new URL(href, location.href);
      if (!['http:', 'https:', 'file:'].includes(u.protocol)) return '';
      return u.href;
    } catch {
      return '';
    }
  };
  const isPreferredTopicHref = (href) => {
    const absolute = toAbsoluteHref(href);
    if (!absolute) return false;
    try {
      const u = new URL(absolute);
      return (
        /^\/t\//.test(u.pathname) ||
        /\/(topic|thread|discussion|comment|comments|question|questions|item)s?(\/|$)/i.test(u.pathname) ||
        (/viewtopic\.php$/i.test(u.pathname) && u.searchParams.has('t'))
      );
    } catch {
      return false;
    }
  };
  const topicRoots = Array.from(new Set([
    document.querySelector('main'),
    document.querySelector('article'),
    document.querySelector('[role=main]')
  ].filter(Boolean)));
  const chooseAnchor = (anchors) => {
    const ranked = anchors.map((anchor, index) => {
      const text = normalizeText(anchor.innerText || anchor.textContent);
      const href = toAbsoluteHref(anchor.getAttribute('href') || anchor.href || '');
      if (!text || !href) return null;
      let score = 0;
      if (isPreferredTopicHref(href)) score += 4;
      if (anchor.closest('h1, h2, h3, h4')) score += 2;
      const className = normalizeText([
        anchor.className || '',
        anchor.parentElement ? anchor.parentElement.className || '' : ''
      ].join(' ')).toLowerCase();
      if (/(^| )(title|topic|question|result|headline|subject)( |$)/.test(className)) score += 1;
      score += Math.min(text.length, 120) / 120;
      return { anchor, href, index, score, text };
    }).filter(Boolean);
    ranked.sort((a, b) => b.score - a.score || b.text.length - a.text.length || a.index - b.index);
    return ranked[0] || null;
  };

  const seen = new Set();
  const results = [];
  const collectFromContainer = (container) => {
    const chosen = chooseAnchor(Array.from(container.querySelectorAll('a[href]')));
    if (!chosen || seen.has(chosen.href)) return;
    seen.add(chosen.href);

    const item = {
      text: chosen.text,
      href: chosen.href,
    };

    const meta = normalizeText(container.innerText || '');
    if (meta) item.meta = meta.slice(0, 400);
    const topicId = container.getAttribute('data-topic-id');
    if (topicId) item.topicId = topicId;
    results.push(item);
  };

  const containers = Array.from(document.querySelectorAll([
    '.search-results .fps-result',
    '.topic-list-item',
    '.latest-topic-list-item',
    '.category-topic-link',
    'tr.topic-list-item',
    '[data-topic-id]'
  ].join(',')));

  for (const container of containers) {
    collectFromContainer(container);
  }

  if (!results.length) {
    const repeatedContainers = [];
    for (const root of topicRoots) {
      for (const child of Array.from(root.children || [])) {
        if (child.querySelector('a[href]')) repeatedContainers.push(child);
      }
    }
    if (repeatedContainers.length >= 2) {
      for (const container of repeatedContainers) {
        collectFromContainer(container);
      }
    }
  }

  if (!results.length) {
    const roots = topicRoots.length ? topicRoots : [document.body].filter(Boolean);
    for (const root of roots) {
      for (const anchor of Array.from(root.querySelectorAll('a[href]'))) {
        const text = normalizeText(anchor.innerText || anchor.textContent);
        const href = toAbsoluteHref(anchor.getAttribute('href') || anchor.href || '');
        if (!text || !href || seen.has(href)) continue;
        seen.add(href);
        results.push({ text, href });
      }
    }
  }

  return { title, url, content: JSON.stringify(results) };
})()"""

_FORMAT_JS = {
    "markdown": _JS_MARKDOWN,
    "text": _JS_TEXT,
    "links": _JS_LINKS,
    "topic-links": _JS_TOPIC_LINKS,
}


def snapshot(port: int, target_id: str | None, fmt: str, max_chars: int) -> dict[str, str]:
    js = _FORMAT_JS[fmt]
    value = evaluate(port, target_id, js)
    if not isinstance(value, dict):
        raise CdpError("snapshot did not return an object")
    content = str(value.get("content", ""))
    if max_chars and len(content) > max_chars:
        content = content[:max_chars] + "\n[truncated]"
    return {
        "title": str(value.get("title", "")),
        "url": str(value.get("url", "")),
        "content": content,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="cdp-snapshot",
        description="Capture a structured page snapshot via CDP.",
    )
    parser.add_argument("--port", type=int, required=True, help="CDP HTTP/WebSocket port")
    parser.add_argument("--target-id", help="Specific target id from /json/list")
    parser.add_argument(
        "--format",
        choices=["markdown", "text", "links", "topic-links"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=8000,
        help="Truncate content to N chars (default: 8000, 0=unlimited)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = snapshot(args.port, args.target_id, args.format, args.max_chars)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, CdpError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
