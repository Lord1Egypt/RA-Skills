import type { Article } from "../rss/parse";

export const SKIP_DOMAINS = new Set([
  "twitter.com",
  "x.com",
  "reddit.com",
  "github.com",
  "youtube.com",
  "nytimes.com",
  "bloomberg.com",
  "wsj.com",
  "ft.com",
]);

export interface EnrichedArticle extends Article {
  fullText?: string;
  fullTextMethod?: "cf-markdown" | "html-extract" | "skipped";
  fullTextTokens?: number;
}

export function getDomain(url: string): string {
  try {
    const parsed = new URL(url);
    return parsed.hostname.replace(/^www\./, "").toLowerCase();
  } catch {
    return "";
  }
}

function stripTags(html: string): string {
  return html
    .replace(/<(script|style|nav|footer|header|aside)[^>]*>[\s\S]*?<\/\1>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, "\"")
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function extractMainContent(html: string): string {
  const articleMatch = html.match(/<article[^>]*>([\s\S]*?)<\/article>/i);
  if (articleMatch) return stripTags(articleMatch[1]!);

  const mainMatch = html.match(/<main[^>]*>([\s\S]*?)<\/main>/i);
  if (mainMatch) return stripTags(mainMatch[1]!);

  const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
  if (bodyMatch) return stripTags(bodyMatch[1]!);

  return stripTags(html);
}

export async function fetchFullText(
  url: string,
  options?: {
    fetcher?: typeof fetch;
    maxChars?: number;
    timeoutMs?: number;
  },
): Promise<{ text: string; method: "cf-markdown" | "html-extract" | "skipped"; tokens: number; error?: string }> {
  const domain = getDomain(url);
  if (SKIP_DOMAINS.has(domain)) {
    return { text: "", method: "skipped", tokens: 0 };
  }

  const fetcher = options?.fetcher ?? fetch;
  const maxChars = options?.maxChars ?? 2000;
  const timeoutMs = options?.timeoutMs ?? 10_000;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetcher(url, {
      signal: controller.signal,
      headers: { Accept: "text/markdown, text/html;q=0.9" },
    });
    clearTimeout(timeout);

    if (!response.ok) {
      return { text: "", method: "skipped", tokens: 0, error: `HTTP ${response.status}` };
    }

    const contentType = response.headers.get("content-type") ?? "";
    const body = await response.text();

    if (contentType.includes("text/markdown")) {
      const text = body.slice(0, maxChars);
      return { text, method: "cf-markdown", tokens: Math.ceil(text.length / 4) };
    }

    const text = extractMainContent(body).slice(0, maxChars);
    return { text, method: "html-extract", tokens: Math.ceil(text.length / 4) };
  } catch (error) {
    clearTimeout(timeout);
    const message = error instanceof Error ? error.message : String(error);
    return { text: "", method: "skipped", tokens: 0, error: message };
  }
}

export async function enrichArticles(
  articles: Article[],
  options?: {
    fetcher?: typeof fetch;
    concurrency?: number;
    maxChars?: number;
  },
): Promise<EnrichedArticle[]> {
  const concurrency = options?.concurrency ?? 5;
  const results: EnrichedArticle[] = [];

  for (let i = 0; i < articles.length; i += concurrency) {
    const batch = articles.slice(i, i + concurrency);
    const batchResults = await Promise.all(
      batch.map(async (article): Promise<EnrichedArticle> => {
        const { text, method, tokens } = await fetchFullText(article.link, {
          fetcher: options?.fetcher,
          maxChars: options?.maxChars,
        });
        return {
          ...article,
          fullText: text || undefined,
          fullTextMethod: method,
          fullTextTokens: tokens || undefined,
        };
      }),
    );
    results.push(...batchResults);
  }

  return results;
}
