import * as cheerio from "cheerio";

const USER_AGENT =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36";

const SOGOU_ZHIHU = "https://www.sogou.com/sogou";

export async function searchZhihu(query, limit = 5) {
  const searchUrl = `${SOGOU_ZHIHU}?query=${encodeURIComponent(query + " site:zhihu.com")}&ie=utf8`;
  const res = await fetch(searchUrl, {
    headers: {
      "User-Agent": USER_AGENT,
      Accept: "text/html,application/xhtml+xml",
      "Accept-Language": "zh-CN,zh;q=0.9",
    },
    signal: AbortSignal.timeout(10000),
  });

  if (!res.ok) {
    throw new Error(`Sogou/Zhihu returned HTTP ${res.status}`);
  }

  const html = await res.text();
  const $ = cheerio.load(html);
  const results = [];

  $(".vrwrap, .rb, .results .vrwrap").each((_, el) => {
    if (results.length >= limit) return;
    const $el = $(el);
    const titleEl = $el.find("h3 a, .vr-title a, .pt a").first();
    const title = titleEl.text().trim();
    const href = titleEl.attr("href") || "";
    const snippet = $el.find(".str_info, .str-info, .space-txt, .ft").first().text().trim();

    if (title && (href.includes("zhihu.com") || title.includes("知乎"))) {
      results.push({
        title: title.replace(/ - 知乎$/, ""),
        snippet,
        url: href.startsWith("http") ? href : `https://www.sogou.com${href}`,
        source: "zhihu",
      });
    }
  });

  if (results.length === 0) {
    return searchZhihuDirect(query, limit);
  }

  return results;
}

async function searchZhihuDirect(query, limit) {
  const url = `https://www.zhihu.com/search?type=content&q=${encodeURIComponent(query)}`;
  try {
    const res = await fetch(url, {
      headers: {
        "User-Agent": USER_AGENT,
        Accept: "text/html,application/xhtml+xml",
        "Accept-Language": "zh-CN,zh;q=0.9",
      },
      signal: AbortSignal.timeout(10000),
    });

    if (!res.ok) return [];

    const html = await res.text();
    const $ = cheerio.load(html);
    const results = [];

    $(".SearchResult-Card, .List-item").each((_, el) => {
      if (results.length >= limit) return;
      const $el = $(el);
      const title =
        $el.find(".ContentItem-title a").text().trim() ||
        $el.find("h2").text().trim();
      const snippet = $el.find(".RichContent-inner, .content").first().text().trim().slice(0, 300);
      const link = $el.find(".ContentItem-title a").attr("href") || "";
      const fullUrl = link.startsWith("http") ? link : `https://www.zhihu.com${link}`;

      if (title) {
        results.push({ title, snippet, url: fullUrl, source: "zhihu" });
      }
    });

    return results;
  } catch {
    return [];
  }
}
