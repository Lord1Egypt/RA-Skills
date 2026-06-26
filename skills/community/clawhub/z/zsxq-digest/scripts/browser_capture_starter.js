() => {
  const visible = (el) => {
    if (!el) return false;
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };

  const textOf = (el) => (el?.innerText || '')
    .replace(/\r\n/g, '\n')
    .replace(/\s+\n/g, '\n')
    .replace(/[ \t]+/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();

  const abs = (href) => {
    try {
      return href ? new URL(href, location.href).href : '';
    } catch {
      return '';
    }
  };

  const circleNameFromTitle = () => {
    const title = (document.title || '').trim();
    return title.replace(/-知识星球$/, '').trim() || '';
  };

  const parseCount = (text, markers) => {
    for (const marker of markers) {
      const re = new RegExp(`${marker}\s*(\d+)`);
      const match = text.match(re);
      if (match) return Number(match[1]) || 0;
    }
    return 0;
  };

  const parseTime = (text) => {
    const m = text.match(/(20\d{2}[-/.]\d{1,2}[-/.]\d{1,2}(?:\s+\d{1,2}:\d{2})?)/);
    return m ? m[1].replace(/\//g, '-') : '';
  };

  const parseAuthor = (lines) => {
    for (const line of lines.slice(0, 4)) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      if (/^20\d{2}[-/.]/.test(trimmed)) continue;
      if (/^(查看详情|全文|展开全文|点赞|评论)/.test(trimmed)) continue;
      if (trimmed.length <= 16 && !/^https?:\/\//.test(trimmed)) {
        return trimmed;
      }
    }
    return '';
  };

  const findCard = (anchor) => {
    let node = anchor;
    for (let i = 0; i < 8 && node; i += 1) {
      const text = textOf(node);
      if (text.length >= 30 && text.length <= 4000) {
        if (/(查看详情|点赞|评论|全文|20\d{2}-\d{1,2}-\d{1,2})/.test(text) || text.length >= 120) {
          return node;
        }
      }
      node = node.parentElement;
    }
    return anchor.parentElement || anchor;
  };

  const collectAnchors = () => {
    const selector = [
      'a[href*="/topic/"]',
      'a[href*="articles.zsxq.com/"]',
      'a[href*="mp.weixin.qq.com/"]',
      'a[href*="ifeng.com/"]',
      'a[href*="163.com/"]',
      'a[href*="caixin.com/"]',
      'a[href^="http"]'
    ].join(',');
    return Array.from(document.querySelectorAll(selector)).filter((el) => visible(el) && abs(el.href));
  };

  const anchors = collectAnchors();
  const items = [];
  const seen = new Set();
  const circleName = circleNameFromTitle();

  for (const anchor of anchors) {
    const url = abs(anchor.href);
    if (!url) continue;
    if (/logout|login|register|download|privacy|agreement/.test(url)) continue;

    const card = findCard(anchor);
    const cardText = textOf(card);
    const anchorText = textOf(anchor);
    const text = cardText || anchorText;
    if (!text || text.length < 12) continue;

    const lines = text.split('\n').map((s) => s.trim()).filter(Boolean);
    const title = (anchorText || lines[0] || text.slice(0, 80)).slice(0, 160);
    const key = `${url}|${title}`;
    if (seen.has(key)) continue;
    seen.add(key);

    const publishedAt = parseTime(text);
    const likes = parseCount(text, ['点赞', '赞']);
    const comments = parseCount(text, ['评论', '回复']);
    const isTruncated = /(查看详情|展开全文|全文|下略)/.test(text) || /(?:\.\.\.|……)$/.test(text);
    const rawText = text.slice(0, 1600);
    const preview = rawText.slice(0, 280);

    items.push({
      item_id: (url.match(/\/topic\/(\d+)/) || [])[1] || null,
      circle_name: circleName,
      author: parseAuthor(lines),
      published_at: publishedAt || '',
      title_or_hook: title,
      content_preview: preview,
      detail_excerpt: rawText,
      raw_text: rawText,
      likes,
      comments,
      is_truncated: isTruncated,
      has_links: /^https?:\/\//.test(url),
      has_images: !!card.querySelector('img'),
      source_confidence: rawText.length >= 180 ? 'medium' : 'low',
      url,
    });

    if (items.length >= 40) break;
  }

  return {
    page_title: document.title,
    page_url: location.href,
    circle_name: circleName,
    item_count: items.length,
    items,
  };
};
