import { extractLinksFromHtml, extractReadableText } from "./html-text.mjs";
import { requestText } from "./http-client.mjs";
import { assertSafeRemoteUrl } from "./url-safety.mjs";

const USER_AGENT = "web-search-pro/1.1 (+https://github.com/Zjianru/web-search-pro)";

function isRedirect(status) {
  return status >= 300 && status < 400;
}

function isHtmlContentType(contentType = "") {
  return (
    contentType.includes("text/html") || contentType.includes("application/xhtml+xml")
  );
}

function isTextLikeContentType(contentType = "") {
  return (
    contentType === "" ||
    isHtmlContentType(contentType) ||
    contentType.startsWith("text/") ||
    contentType.includes("application/json") ||
    contentType.includes("application/xml")
  );
}

async function fetchWithRedirects(inputUrl, options, depth = 0) {
  const maxRedirects = options.maxRedirects ?? 4;
  if (depth > maxRedirects) {
    throw new Error("Too many redirects");
  }

  const safe = await assertSafeRemoteUrl(inputUrl, options);
  const requestTextFn = options.requestTextFn ?? requestText;
  const response = await requestTextFn(safe.url.toString(), {
    method: "GET",
    headers: {
      "user-agent": USER_AGENT,
      accept: "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.8",
    },
    timeoutMs: options.timeoutMs,
  });

  if (isRedirect(response.status)) {
    const location = response.redirectUrl;
    if (!location) {
      throw new Error(`Redirect without location for ${safe.url}`);
    }
    const nextUrl = new URL(location, safe.url).toString();
    return fetchWithRedirects(nextUrl, options, depth + 1);
  }

  if (response.status < 200 || response.status >= 300) {
    throw new Error(`Fetch failed (${response.status})`);
  }

  return {
    url: safe.url.toString(),
    contentType: response.contentType || "application/octet-stream",
    body: response.body,
  };
}

export async function fetchUrlSnapshot(inputUrl, options = {}) {
  const maxChars = options.maxChars ?? 12000;
  const response = await fetchWithRedirects(inputUrl, options);
  if (!isTextLikeContentType(response.contentType)) {
    throw new Error(`Unsupported content type: ${response.contentType}`);
  }

  if (!isHtmlContentType(response.contentType)) {
    return {
      url: response.url,
      title: "",
      contentType: response.contentType,
      body: response.body,
      content: response.body.slice(0, maxChars).trim(),
      links: [],
      isHtml: false,
    };
  }

  const extracted = extractReadableText(response.body, { maxChars });
  return {
    url: response.url,
    title: extracted.title,
    contentType: response.contentType,
    body: response.body,
    content: extracted.content,
    links: extractLinksFromHtml(response.body, response.url),
    isHtml: true,
  };
}

export async function fetchReadableUrl(inputUrl, options = {}) {
  const snapshot = await fetchUrlSnapshot(inputUrl, options);
  return {
    url: snapshot.url,
    title: snapshot.title,
    contentType: snapshot.contentType,
    content: snapshot.content,
  };
}

export async function fetchReadableUrls(urls, options = {}) {
  const results = [];
  const failed = [];

  for (const url of urls) {
    try {
      results.push(await fetchReadableUrl(url, options));
    } catch (err) {
      failed.push({
        url,
        error: err.message,
      });
    }
  }

  return { results, failed };
}
