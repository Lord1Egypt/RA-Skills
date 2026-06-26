function decodeNamedEntities(text) {
  return text
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'");
}

function decodeNumericEntities(text) {
  return text
    .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number.parseInt(code, 10)))
    .replace(/&#x([0-9a-f]+);/gi, (_, code) => String.fromCodePoint(Number.parseInt(code, 16)));
}

export function decodeHtmlEntities(text) {
  return decodeNumericEntities(decodeNamedEntities(text));
}

export function stripHtmlTags(text) {
  return decodeHtmlEntities(text.replace(/<[^>]+>/g, " "));
}

export function collapseWhitespace(text) {
  return text
    .replace(/\r/g, "")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n[ \t]+/g, "\n")
    .replace(/[ \t]{2,}/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

export function extractTitleFromHtml(html) {
  const titleMatch = html.match(/<title[^>]*>(.*?)<\/title>/is);
  if (!titleMatch) {
    return "";
  }
  return collapseWhitespace(stripHtmlTags(titleMatch[1]));
}

export function extractReadableText(html, options = {}) {
  const maxChars = options.maxChars ?? 12000;
  const title = extractTitleFromHtml(html);
  const text = html
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, "\n")
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, "\n")
    .replace(/<noscript\b[^>]*>[\s\S]*?<\/noscript>/gi, "\n")
    .replace(/<svg\b[^>]*>[\s\S]*?<\/svg>/gi, "\n")
    .replace(/<(br|\/p|\/div|\/li|\/section|\/article|\/h[1-6])>/gi, "\n")
    .replace(/<li\b[^>]*>/gi, "\n- ")
    .replace(/<p\b[^>]*>|<div\b[^>]*>|<section\b[^>]*>|<article\b[^>]*>/gi, "\n")
    .replace(/<h[1-6]\b[^>]*>/gi, "\n\n")
    .replace(/<[^>]+>/g, " ");

  return {
    title,
    content: collapseWhitespace(decodeHtmlEntities(text)).slice(0, maxChars),
  };
}

export function extractLinksFromHtml(html, baseUrl) {
  const links = [];
  const matcher = /<a\b[^>]*href\s*=\s*(['"])(.*?)\1/gi;

  for (const match of html.matchAll(matcher)) {
    const href = decodeHtmlEntities(match[2] ?? "").trim();
    if (!href || href.startsWith("#")) {
      continue;
    }

    try {
      const url = new URL(href, baseUrl);
      url.hash = "";
      links.push(url.toString());
    } catch {
      // Ignore malformed URLs.
    }
  }

  return Array.from(new Set(links));
}
