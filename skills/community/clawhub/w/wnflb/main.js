const fs = require("fs");
const path = require("path");
const { request, Agent, interceptors } = require("undici");
const cheerio = require("cheerio");
const { decodeRedirectUrlFromJs } = require("./lib/decode-redirect");

// ─── Constants ───────────────────────────────────────────────────────────────

const FID_MAP = {
  2: 2,   // 发现之门
  40: 40, // 综合讨论
  37: 37, // 购物网赚
  67: 67, // 网游分享区
  44: 44, // 交易平台
  39: 39, // 福禄娃之家
};

const SITE_ORIGIN = "https://www.wnflb2023.com";

const MOBILE_UA =
  "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36";

const DESKTOP_UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36";

// ─── HTTP Dispatcher (undici 7 redirect interceptor) ─────────────────────────

const redirectAgent = new Agent().compose(
  interceptors.redirect({ maxRedirections: 5 })
);

// ─── Shared Utility Functions ────────────────────────────────────────────────

function parseCookies(cookieString) {
  const cookies = {};
  if (!cookieString) return cookies;
  cookieString.split(';').forEach(part => {
    const trimmed = part.trim();
    if (!trimmed) return;
    const idx = trimmed.indexOf('=');
    if (idx > 0) {
      const name = trimmed.substring(0, idx).trim();
      const value = trimmed.substring(idx + 1).trim();
      cookies[name] = value;
    }
  });
  return cookies;
}

function parseSetCookieHeader(setCookie) {
  if (!setCookie) return null;
  const idx = setCookie.indexOf(';');
  const cookiePart = idx > 0 ? setCookie.substring(0, idx) : setCookie;
  const eqIdx = cookiePart.indexOf('=');
  if (eqIdx <= 0) return null;
  return {
    name: cookiePart.substring(0, eqIdx).trim(),
    value: cookiePart.substring(eqIdx + 1).trim()
  };
}

function mergeCookies(existingCookie, setCookieHeaders) {
  if (!setCookieHeaders || setCookieHeaders.length === 0) return existingCookie;
  const cookies = parseCookies(existingCookie);
  let updated = false;
  const headers = Array.isArray(setCookieHeaders) ? setCookieHeaders : [setCookieHeaders];
  for (const header of headers) {
    const parsed = parseSetCookieHeader(header);
    if (parsed) {
      cookies[parsed.name] = parsed.value;
      updated = true;
    }
  }
  if (!updated) return existingCookie;
  return Object.entries(cookies)
    .map(([name, value]) => `${name}=${value}`)
    .join('; ');
}

function getCookiePath(cookiePath) {
  return path.isAbsolute(cookiePath)
    ? cookiePath
    : path.resolve(__dirname, cookiePath);
}

function readCookieHeaderValue(cookiePath) {
  const resolvedPath = getCookiePath(cookiePath);
  return fs.readFileSync(resolvedPath, "utf8").trim();
}

function writeCookieFile(cookiePath, cookieString) {
  const resolvedPath = getCookiePath(cookiePath);
  fs.writeFileSync(resolvedPath, cookieString, 'utf8');
}

function absoluteUrl(baseUrl, maybeRelative) {
  try {
    return new URL(maybeRelative, baseUrl).toString();
  } catch {
    return null;
  }
}

function normalizeText(s) {
  return String(s || "")
    .replace(/\s+/g, "")
    .replace(/\u00a0/g, "")
    .trim();
}

// ─── HTTP Fetch ──────────────────────────────────────────────────────────────

async function fetchText(url, cookie, extraHeaders = {}, cookiePath = null) {
  const headers = {
    "user-agent": extraHeaders._ua || MOBILE_UA,
    accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.9",
    ...extraHeaders,
  };
  delete headers._ua;

  if (cookie && cookie.trim() && cookie !== '请在此处填写您的福利吧论坛Cookie') {
    headers.cookie = cookie;
  }

  const followRedirects = !extraHeaders._noRedirect;
  delete headers._noRedirect;

  const reqOpts = {
    method: "GET",
    headers,
  };

  // Use redirect agent for automatic redirect following, default agent for no-redirect
  if (followRedirects) {
    reqOpts.dispatcher = redirectAgent;
  }

  const res = await request(url, reqOpts);

  const body = await res.body.text();

  let updatedCookie = cookie;
  const setCookie = res.headers['set-cookie'];
  if (setCookie) {
    const merged = mergeCookies(cookie, setCookie);
    if (merged !== cookie) {
      updatedCookie = merged;
    }
  }

  return { statusCode: res.statusCode, headers: res.headers, body, updatedCookie };
}

// ─── JS Gate / Redirect Resolution ──────────────────────────────────────────

function extractJsPayloadFromGate(htmlOrJs) {
  const text = String(htmlOrJs || "").trim();
  if (!text) return null;
  if (/location\.href|window\.href/i.test(text) && !/<html/i.test(text)) {
    return text;
  }
  const $ = cheerio.load(text);
  const scripts = $("script")
    .toArray()
    .map((s) => $(s).html() || "")
    .map((s) => s.trim())
    .filter(Boolean);
  if (!scripts.length) return null;
  return scripts.find((s) => /location\.href|window\.href/i.test(s)) || scripts[0];
}

async function fetchTextFollowRedirectsAndJsGate(url, cookie, cookiePath = null, maxHops = 8) {
  let current = url;
  let currentCookie = cookie;
  const seen = new Set();
  for (let hop = 0; hop <= maxHops; hop++) {
    if (seen.has(current)) {
      const res = await fetchText(current, currentCookie, {}, cookiePath);
      return { ...res, finalUrl: current };
    }
    seen.add(current);

    const res = await fetchText(current, currentCookie, { _noRedirect: true }, cookiePath);
    currentCookie = res.updatedCookie;
    const location = res.headers.location;
    if (location) {
      const next = absoluteUrl(current, location) || location;
      if (!next) return { ...res, finalUrl: current };
      current = next;
      continue;
    }

    const jsPayload = extractJsPayloadFromGate(res.body);
    const decoded = jsPayload ? decodeRedirectUrlFromJs(jsPayload) : null;
    if (decoded) {
      const next = absoluteUrl(current, decoded) || decoded;
      if (next && next !== current) {
        current = next;
        continue;
      }
    }

    return { ...res, finalUrl: current };
  }

  const last = await fetchText(current, currentCookie, {}, cookiePath);
  return { ...last, finalUrl: current };
}

// ─── Forum Scrape Functions ─────────────────────────────────────────────────

function buildForumUrl(fid) {
  return `https://www.wnflb2023.com/forum.php?mod=forumdisplay&fid=${fid}&mobile=2`;
}

function extractForumTitle(html) {
  const $ = cheerio.load(html);
  const title = $("title").first().text().trim();
  return title || "论坛";
}

function isStickyAnchor($, a) {
  const $a = $(a);
  const $row =
    $a.closest(".thread-item-bds, tr, li, .threadlist, .list, .bm, div") ||
    $a.closest("div");

  const nearText = normalizeText(($row.text && $row.text()) || $a.closest("li, tr, div").text() || "");
  const selfText = normalizeText($a.text() || "");
  const classText = [
    $a.attr("class") || "",
    ($row.attr && $row.attr("class")) || "",
    $a.closest("[class]").attr("class") || "",
  ]
    .join(" ")
    .toLowerCase();

  const hasTopWord =
    nearText.includes("置顶") ||
    selfText.includes("置顶") ||
    nearText.startsWith("置顶") ||
    selfText.startsWith("置顶");

  const hasStickyClass = classText.includes("stick") || classText.includes("top");

  const hasTopIcon =
    ($row.find && $row.find(".icon_top").length > 0) ||
    ($row.find &&
      $row.find('img[src*="icon_top"],img[src*="top.png"],img[src*="top_"]').length >
        0);

  return hasTopWord || hasStickyClass || hasTopIcon;
}

function normalizeThreadUrl(url) {
  try {
    const urlObj = new URL(url);
    const params = urlObj.searchParams;
    const tid = params.get('tid');
    const dsign = params.get('_dsign');
    if (!tid) return url;
    const baseUrl = `${urlObj.protocol}//${urlObj.host}`;
    let newUrl = `${baseUrl}/thread-${tid}-1-1.html`;
    if (dsign) {
      newUrl += `?_dsign=${dsign}`;
    }
    return newUrl;
  } catch {
    return url;
  }
}

function extractThreadLinksFromList(listHtml, baseForumUrl) {
  const $ = cheerio.load(listHtml);
  const anchors = $('a[href*="mod=viewthread"]')
    .toArray()
    .filter((a) => {
      const text = ($(a).text() || "").trim();
      return text.length >= 3;
    });

  const seen = new Set();
  const threads = [];
  for (const a of anchors) {
    const href = $(a).attr("href");
    const url = absoluteUrl(baseForumUrl, href);
    if (!url) continue;
    if (seen.has(url)) continue;
    seen.add(url);

    const title = ($(a).text() || "").trim();
    const sticky = isStickyAnchor($, a);
    const normalizedUrl = normalizeThreadUrl(url);
    threads.push({ title, url: normalizedUrl, sticky });
  }

  return threads;
}

function extractMainPostContent(realThreadHtml) {
  const $ = cheerio.load(realThreadHtml);

  const firstPostContainer = $('[id^="post_"], .plc, .post').first();
  if (firstPostContainer && firstPostContainer.length) {
    const clone = firstPostContainer.clone();
    clone.find("script, style, form, .share-box, .fastreply, .replybox").remove();
    const msg =
      clone.find('[id^="postmessage_"]').first().text().trim() ||
      clone.find(".postmessage").first().text().trim() ||
      clone.find(".message").first().text().trim();
    if (msg) return msg.replace(/\r/g, "").replace(/\n{3,}/g, "\n\n").trim();
  }

  const candidates = [
    () => $('[id^="postmessage_"]').first().text(),
    () => $(".postmessage").first().text(),
    () => $(".message").first().text(),
    () => $("#postlist .message").first().text(),
    () => $(".plc .message").first().text(),
    () => $(".bm .t_f").first().text(),
    () => $("#thread_subject").closest("div").nextAll().text(),
    () => $("article").first().text(),
  ];

  let content = "";
  for (const pick of candidates) {
    const t = (pick() || "").trim();
    if (t) {
      content = t;
      break;
    }
  }

  if (!content) {
    const msgs = $(".message")
      .toArray()
      .map((el) => $(el).text().trim())
      .filter(Boolean);
    if (msgs.length) {
      msgs.sort((a, b) => b.length - a.length);
      content = msgs[0];
    }
  }

  if (!content) {
    const cloned = $.root().clone();
    cloned.find("script, style").remove();
    cloned.find("header, footer, nav").remove();
    cloned.find("#comment, .comment, #comments, .comments").remove();
    cloned.find('div[id^="post_"], .plc, .pl').slice(1).remove();
    content = cloned.text().replace(/\s+\n/g, "\n").trim();
  }

  content = content.replace(/\r/g, "").replace(/\n{3,}/g, "\n\n").trim();
  return content;
}

async function resolveRealThreadUrl(threadUrl, cookie, cookiePath = null) {
  const first = await fetchText(threadUrl, cookie, { _noRedirect: true }, cookiePath);

  const location = first.headers.location;
  if (location) {
    const abs = absoluteUrl(threadUrl, location);
    return { url: abs || threadUrl, updatedCookie: first.updatedCookie };
  }

  const jsPayload = extractJsPayloadFromGate(first.body);
  if (!jsPayload) return { url: threadUrl, updatedCookie: first.updatedCookie };

  const decoded = decodeRedirectUrlFromJs(jsPayload);
  if (!decoded) return { url: threadUrl, updatedCookie: first.updatedCookie };
  return { url: absoluteUrl(threadUrl, decoded) || decoded, updatedCookie: first.updatedCookie };
}

async function fetchThreadMain(threadUrl, cookie, cookiePath = null) {
  const { url: realUrl, updatedCookie: cookie1 } = await resolveRealThreadUrl(threadUrl, cookie, cookiePath);
  const real = await fetchText(realUrl, cookie1, {}, cookiePath);
  const $ = cheerio.load(real.body);
  const title =
    $(".viewtd_tit h2").first().text().trim() ||
    $("#thread_subject").first().text().trim() ||
    $("title").first().text().trim() ||
    "";
  const content = extractMainPostContent(real.body);
  return { title, url: realUrl, content, updatedCookie: real.updatedCookie };
}

async function scrapeForum(opts) {
  const fid = Object.prototype.hasOwnProperty.call(FID_MAP, opts.fid)
    ? opts.fid
    : null;
  if (fid == null) {
    const allowed = Object.keys(FID_MAP)
      .map((k) => Number(k))
      .sort((a, b) => a - b)
      .join(", ");
    throw new Error(`不支持的 fid=${opts.fid},可用 fid 为:${allowed}(未传则默认 2)`);
  }

  const forumUrl = buildForumUrl(fid);
  const cookie = readCookieHeaderValue(opts.cookie);

  if (!cookie || cookie === '请在此处填写您的福利吧论坛Cookie') {
    console.error(`警告:Cookie文件为空或未配置,部分功能可能无法使用。`);
  }

  const list = await fetchText(forumUrl, cookie, {}, opts.cookie);
  let currentCookie = list.updatedCookie;
  const forumTitle = extractForumTitle(list.body);

  if (forumTitle === '论坛' && list.body.length < 100) {
    console.error(`错误：需要登录才能访问。请在cookie.txt中填写有效cookie。`);
    process.exit(1);
  }

  const threadsAll = extractThreadLinksFromList(list.body, forumUrl);
  const threads = threadsAll.filter((t) => !t.sticky);

  let picked = [];
  if (opts.count != null) {
    picked = threads.slice(0, Math.min(opts.count, threads.length));
  } else {
    const pickCount = Math.min(opts.max, Math.max(opts.min, threads.length));
    picked = threads.slice(0, pickCount);
  }

  const results = [];
  for (const t of picked) {
    const item = await fetchThreadMain(t.url, currentCookie, opts.cookie);
    currentCookie = item.updatedCookie;
    if (!item.title) item.title = t.title;
    delete item.updatedCookie;
    results.push(item);
  }

  const output = {
    forumTitle,
    forumUrl,
    fid,
    count: results.length,
    items: results,
  };

  if (currentCookie && currentCookie !== cookie) {
    writeCookieFile(opts.cookie, currentCookie);
  }

  return output;
}

// ─── Checkin Functions ───────────────────────────────────────────────────────

function extractFormhashFromMobileLikeHtml(html) {
  const raw = String(html || "");

  const showWin = raw.match(
    /showWindow\s*\(\s*['"]fx_checkin['"]\s*,\s*['"]([^'"]+)['"]/i
  );
  if (showWin) {
    const part = showWin[1].replace(/&amp;/gi, "&");
    const m = part.match(/(?:^|[?&])formhash=([^&]+)/i);
    if (m && m[1]) return m[1].trim();
  }

  const logout = raw.match(
    /member\.php\?mod=logging(?:&amp;|&)action=logout(?:&amp;|&)formhash=([a-f0-9]+)/i
  );
  if (logout && logout[1]) return logout[1].trim();

  const $ = cheerio.load(raw);
  const v = ($('input[name="formhash"]').attr("value") || "").trim();
  return v || null;
}

function parseFxCheckinInajaxResponse(body) {
  const text = String(body || "");
  if (!text.trim()) {
    return { ok: false, message: "签到返回为空" };
  }

  const cdata = text.match(/<!\[CDATA\[([\s\S]*?)\]\]>/i);
  const inner = cdata ? cdata[1] : text;
  const compact = normalizeText(inner);

  if (/alert_error|alert_info/.test(inner) && !/alert_right/.test(inner)) {
    const em = inner.match(/<div[^>]*class="[^"]*alert_(?:error|info)[^"]*"[^>]*>([\s\S]*?)<\/div>/i);
    const msg = em
      ? normalizeText(cheerio.load(em[1]).text() || em[1])
      : compact.slice(0, 200);
    return { ok: false, message: msg || "签到失败" };
  }

  if (!/alert_right/.test(inner)) {
    if (compact.includes("请先登录") || inner.includes("请先登录")) {
      return { ok: false, message: "可能未登录（cookie 无效）" };
    }
    return { ok: false, message: "未能解析签到结果（非 inajax 响应）" };
  }

  if (/签到成功[,，]/.test(inner) || compact.includes("签到成功,您今日第")) {
    return { ok: true, message: "签到成功" };
  }
  if (
    compact.includes("已签到") &&
    (compact.includes("无需重复") || compact.includes("无需重复签到"))
  ) {
    return { ok: true, message: "已签到" };
  }
  if (compact.includes("已签到")) {
    return { ok: true, message: "已签到" };
  }

  const right = inner.match(/<div[^>]*class="[^"]*alert_right[^"]*"[^>]*>([\s\S]*?)<\/div>/i);
  const plain = right
    ? normalizeText(cheerio.load(right[1]).text() || right[1])
    : compact;
  return { ok: false, message: plain.slice(0, 200) || "签到结果未知" };
}

async function fetchCheckinPageForFormhash(cookie, cookiePath) {
  const entryUrl = `${SITE_ORIGIN}/plugin.php?id=fx_checkin:checkin&mobile=2`;
  const entry = await fetchTextFollowRedirectsAndJsGate(entryUrl, cookie, cookiePath);
  let formhash = extractFormhashFromMobileLikeHtml(entry.body);
  if (formhash) return { formhash, contextUrl: entry.finalUrl, updatedCookie: entry.updatedCookie };

  const mobile = await fetchTextFollowRedirectsAndJsGate(
    `${SITE_ORIGIN}/misc.php?mod=mobile`,
    entry.updatedCookie,
    cookiePath
  );
  formhash = extractFormhashFromMobileLikeHtml(mobile.body);
  return { formhash, contextUrl: mobile.finalUrl, updatedCookie: mobile.updatedCookie };
}

async function postCheckinViaInajax(cookie, formhash, cookiePath) {
  const url = `${SITE_ORIGIN}/plugin.php?id=fx_checkin:checkin&formhash=${encodeURIComponent(
    formhash
  )}&inajax=1`;
  const res = await fetchText(url, cookie, {
    _ua: DESKTOP_UA,
    accept: "text/xml, application/xml, */*;q=0.8",
    "x-requested-with": "XMLHttpRequest",
    referer: `${SITE_ORIGIN}/misc.php?mod=mobile`,
  }, cookiePath);
  const parsed = parseFxCheckinInajaxResponse(res.body);
  return {
    ...parsed,
    statusCode: res.statusCode,
    checkinUrl: url,
    updatedCookie: res.updatedCookie,
  };
}

async function doCheckin(cookie, cookiePath) {
  const { formhash, contextUrl, updatedCookie } = await fetchCheckinPageForFormhash(cookie, cookiePath);
  if (!formhash) {
    return {
      ok: false,
      entryUrl: contextUrl,
      message: "未找到 formhash（请确认 cookie.txt 有效且页面含签到入口）",
    };
  }

  const ajax = await postCheckinViaInajax(updatedCookie, formhash, cookiePath);
  return {
    ok: ajax.ok,
    entryUrl: contextUrl,
    checkinUrl: ajax.checkinUrl,
    message: ajax.message,
  };
}

async function checkin(opts) {
  const cookie = readCookieHeaderValue(opts.cookie);
  return await doCheckin(cookie, opts.cookie);
}

// ─── CLI Argument Parsing ────────────────────────────────────────────────────

function parseArgs(argv) {
  if (argv.length < 3) {
    printUsage();
    process.exit(1);
  }

  const command = argv[2];
  const validCommands = ["scrape", "checkin"];
  if (!validCommands.includes(command)) {
    console.error(`未知命令: ${command}`);
    printUsage();
    process.exit(1);
  }

  const args = {
    command,
    cookie: "cookie.txt",
    // scrape options
    min: 5,
    max: 10,
    count: null,
    fid: 2,
  };

  const pickNumber = (s) => {
    const n = Number(s);
    return Number.isFinite(n) ? n : null;
  };

  for (let i = 3; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--fid") {
      const n = pickNumber(argv[i + 1]);
      if (n != null) args.fid = Math.floor(n);
      i++;
      continue;
    }
    if (a.startsWith("--fid=")) {
      const n = pickNumber(a.split("=").slice(1).join("="));
      if (n != null) args.fid = Math.floor(n);
      continue;
    }
    if (a === "--count" || a === "-c") {
      const n = pickNumber(argv[i + 1]);
      if (n != null) args.count = Math.max(1, Math.floor(n));
      i++;
      continue;
    }
    if (a.startsWith("--count=")) {
      const n = pickNumber(a.split("=").slice(1).join("="));
      if (n != null) args.count = Math.max(1, Math.floor(n));
      continue;
    }
    if (a === "--min") {
      const n = pickNumber(argv[i + 1]);
      if (n != null) args.min = Math.max(1, Math.floor(n));
      i++;
      continue;
    }
    if (a.startsWith("--min=")) {
      const n = pickNumber(a.split("=").slice(1).join("="));
      if (n != null) args.min = Math.max(1, Math.floor(n));
      continue;
    }
    if (a === "--max") {
      const n = pickNumber(argv[i + 1]);
      if (n != null) args.max = Math.max(1, Math.floor(n));
      i++;
      continue;
    }
    if (a.startsWith("--max=")) {
      const n = pickNumber(a.split("=").slice(1).join("="));
      if (n != null) args.max = Math.max(1, Math.floor(n));
      continue;
    }
    if (a === "--cookie") {
      const c = argv[i + 1];
      if (c) args.cookie = c;
      i++;
      continue;
    }
    if (a.startsWith("--cookie=")) {
      const c = a.split("=").slice(1).join("=");
      if (c) args.cookie = c;
      continue;
    }
  }

  if (args.command === "scrape" && args.count == null) {
    if (args.max < args.min) [args.min, args.max] = [args.max, args.min];
  }

  return args;
}

function printUsage() {
  console.log(`
用法: node main.js <command> [options]

命令:
  scrape    抓取论坛帖子列表及内容
  checkin   论坛签到

scrape 选项:
  --fid <n>       板块ID (默认: 2)
  --count <n>     抓取帖子数量
  --min <n>       最少抓取数 (默认: 5)
  --max <n>       最多抓取数 (默认: 10)
  --cookie <path> Cookie文件路径 (默认: cookie.txt)

checkin 选项:
  --cookie <path> Cookie文件路径 (默认: cookie.txt)
`.trim());
}

// ─── Main Entry ──────────────────────────────────────────────────────────────

async function main() {
  const opts = parseArgs(process.argv);

  let result;
  if (opts.command === "scrape") {
    result = await scrapeForum(opts);
  } else if (opts.command === "checkin") {
    result = await checkin(opts);
  }

  process.stdout.write(JSON.stringify(result, null, 2));
}

main().catch((err) => {
  console.error("执行失败:", err && err.message ? err.message : err);
  process.exit(1);
});
