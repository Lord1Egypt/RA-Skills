import * as cheerio from "cheerio";

const USER_AGENT =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36";

const FREE_API = "https://v.api.aa1.cn/api/baidu-search/";

async function searchViaFreeApi(query, limit) {
  try {
    const url = `${FREE_API}?msg=${encodeURIComponent(query)}&type=json`;
    const res = await fetch(url, {
      headers: { "User-Agent": USER_AGENT },
      signal: AbortSignal.timeout(8000),
    });
    if (!res.ok) return null;
    const data = await res.json();
    if (!Array.isArray(data)) return null;
    return data.slice(0, limit).map((item) => ({
      title: item.title || "",
      snippet: item.desc || item.description || "",
      url: item.url || item.link || "",
      source: "baidu",
    }));
  } catch {
    return null;
  }
}

async function searchViaScrape(query, limit) {
  const searchUrl = `https://www.baidu.com/s?wd=${encodeURIComponent(query)}&rn=${limit}`;
  const res = await fetch(searchUrl, {
    headers: {
      "User-Agent": USER_AGENT,
      Accept: "text/html,application/xhtml+xml",
      "Accept-Language": "zh-CN,zh;q=0.9",
    },
    signal: AbortSignal.timeout(10000),
  });

  if (!res.ok) {
    throw new Error(`Baidu returned HTTP ${res.status}`);
  }

  const html = await res.text();
  const $ = cheerio.load(html);
  const results = [];

  $(".result, .c-container").each((_, el) => {
    if (results.length >= limit) return;
    const $el = $(el);
    const titleEl = $el.find("h3 a, .t a").first();
    const title = titleEl.text().trim();
    const href = titleEl.attr("href") || "";
    const snippet =
      $el.find(".c-abstract, .content-right_2s-H4, .c-span-last").first().text().trim() ||
      $el.find("span.content-right_2s-H4").text().trim() ||
      $el.find(".c-row .text").text().trim();

    if (title) {
      results.push({ title, snippet, url: href, source: "baidu" });
    }
  });

  return results;
}

export async function searchBaidu(query, limit = 5) {
  const apiResults = await searchViaFreeApi(query, limit);
  if (apiResults && apiResults.length > 0) {
    return apiResults;
  }
  return searchViaScrape(query, limit);
}
