import { fetchReadableUrls } from "../lib/web-fetch.mjs";

export function isAvailable() {
  return true;
}

export function name() {
  return "fetch";
}

export async function search(_query, _opts = {}) {
  throw new Error("fetch engine does not support search. Use ddg or a provider API instead.");
}

export async function extract(urls, opts = {}) {
  const result = await fetchReadableUrls(urls, {
    maxChars: opts.maxChars ?? 12000,
  });

  return {
    engine: "fetch",
    results: result.results.map((entry) => ({
      url: entry.url,
      title: entry.title,
      content: entry.content,
      contentType: entry.contentType,
    })),
    failed: result.failed,
  };
}
