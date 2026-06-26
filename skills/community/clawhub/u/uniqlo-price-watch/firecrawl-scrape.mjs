#!/usr/bin/env node

const DEFAULT_ENDPOINT = "https://api.firecrawl.dev/v2/scrape";
const DEFAULT_TIMEOUT_MS = 30_000;

function printHelp() {
  process.stdout.write(
    [
      "Usage:",
      "  node .skills/uniqlo-price-watch/firecrawl-scrape.mjs <uniqlo-search-url>",
      "",
      "Environment variables:",
      "  FIRECRAWL_API_KEY   FireCrawl API key",
      '  FIRECRAWL-API-KEY   Compatibility alias for the skill readme',
      "  FIRECRAWL_API_URL   Optional override for the scrape endpoint",
      "  FIRECRAWL_TIMEOUT_MS  Optional request timeout in milliseconds",
      "",
      "Output:",
      '  { "markdown": "...", "url": "..." }',
      "",
    ].join("\n"),
  );
}

function fail(message, details) {
  process.stderr.write(`Error: ${message}\n`);

  if (details) {
    process.stderr.write(`${details}\n`);
  }

  process.exit(1);
}

const args = process.argv.slice(2);

if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
  printHelp();
  process.exit(args.length === 0 ? 1 : 0);
}

if (args.length !== 1) {
  fail("expected exactly one URL argument");
}

const inputUrl = args[0];
let parsedUrl;

try {
  parsedUrl = new URL(inputUrl);
} catch {
  fail("invalid URL argument", inputUrl);
}

if (!/^https?:$/.test(parsedUrl.protocol)) {
  fail("URL must use http or https", inputUrl);
}

const apiKey =
  process.env.FIRECRAWL_API_KEY ?? process.env["FIRECRAWL-API-KEY"];

if (!apiKey) {
  fail("missing FIRECRAWL_API_KEY environment variable");
}

const endpoint = process.env.FIRECRAWL_API_URL ?? DEFAULT_ENDPOINT;
const timeoutMs = Number.parseInt(
  process.env.FIRECRAWL_TIMEOUT_MS ?? `${DEFAULT_TIMEOUT_MS}`,
  10,
);

const controller = new AbortController();
const timeout = Number.isFinite(timeoutMs)
  ? setTimeout(() => controller.abort(), timeoutMs)
  : null;

try {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url: parsedUrl.toString(),
      formats: ["markdown"],
    }),
    signal: controller.signal,
  });

  const responseText = await response.text();
  let payload;

  try {
    payload = JSON.parse(responseText);
  } catch {
    fail("FireCrawl returned non-JSON content", responseText);
  }

  if (!response.ok) {
    fail(
      `FireCrawl request failed with status ${response.status}`,
      JSON.stringify(payload, null, 2),
    );
  }

  if (!payload?.success) {
    fail("FireCrawl reported success=false", JSON.stringify(payload, null, 2));
  }

  const markdown = payload?.data?.markdown;
  const url =
    payload?.data?.metadata?.sourceURL ??
    payload?.data?.metadata?.url ??
    parsedUrl.toString();

  if (typeof markdown !== "string") {
    fail("FireCrawl response does not contain data.markdown");
  }

  process.stdout.write(`${JSON.stringify({ markdown, url }, null, 2)}\n`);
} catch (error) {
  if (error?.name === "AbortError") {
    fail(`FireCrawl request timed out after ${timeoutMs}ms`);
  }

  fail("FireCrawl request failed", error instanceof Error ? error.message : String(error));
} finally {
  if (timeout) {
    clearTimeout(timeout);
  }
}
