import * as cheerio from "cheerio";

const USER_AGENT =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36";

const SOGOU_WEIXIN = "https://weixin.sogou.com/weixin";

export async function searchWechat(query, limit = 5) {
  const searchUrl = `${SOGOU_WEIXIN}?type=2&query=${encodeURIComponent(query)}&ie=utf8`;

  const res = await fetch(searchUrl, {
    headers: {
      "User-Agent": USER_AGENT,
      Accept: "text/html,application/xhtml+xml",
      "Accept-Language": "zh-CN,zh;q=0.9",
      Referer: "https://weixin.sogou.com/",
    },
    signal: AbortSignal.timeout(10000),
  });

  if (!res.ok) {
    throw new Error(`Sogou WeChat returned HTTP ${res.status}`);
  }

  const html = await res.text();
  const $ = cheerio.load(html);
  const results = [];

  $(".news-list li, .news-box .news-list ul li, .txt-box").each((_, el) => {
    if (results.length >= limit) return;
    const $el = $(el);

    const titleEl = $el.find("h3 a, .tit a").first();
    const title = titleEl.text().trim();
    const href = titleEl.attr("href") || "";
    const snippet = $el.find("p.txt-info, .txt-info").first().text().trim();
    const account = $el.find(".s-p a, .account").first().text().trim();
    const date = $el.find(".s-p .s2, .date").first().text().trim();

    if (title) {
      results.push({
        title,
        snippet,
        url: href.startsWith("http") ? href : `https://weixin.sogou.com${href}`,
        account: account || undefined,
        date: date || undefined,
        source: "wechat",
      });
    }
  });

  if (results.length === 0) {
    return searchWechatFallback(query, limit);
  }

  return results;
}

async function searchWechatFallback(query, limit) {
  const url = `https://www.sogou.com/sogou?query=${encodeURIComponent(query + " site:mp.weixin.qq.com")}&ie=utf8`;
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

    $(".vrwrap, .rb").each((_, el) => {
      if (results.length >= limit) return;
      const $el = $(el);
      const titleEl = $el.find("h3 a, .vr-title a").first();
      const title = titleEl.text().trim();
      const href = titleEl.attr("href") || "";
      const snippet = $el.find(".str_info, .str-info, .space-txt").first().text().trim();

      if (title) {
        results.push({
          title,
          snippet,
          url: href.startsWith("http") ? href : `https://www.sogou.com${href}`,
          source: "wechat",
        });
      }
    });

    return results;
  } catch {
    return [];
  }
}
