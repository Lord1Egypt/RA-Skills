#!/usr/bin/env node
"use strict";

const fs = require("node:fs");

const DEFAULT_PATHS = ["/sitemap.xml", "/sitemaps.xml", "/atom.xml", "/rss.xml"];
const DEFAULT_TIMEOUT_MS = 15000;
const DEFAULT_MAX_DEPTH = 3;

function usage() {
  console.error(`Usage:
  node scripts/preprocess-rss-sitemap.js --site https://example.com [--output result.json]
  node scripts/preprocess-rss-sitemap.js --url https://example.com/sitemap.xml --url https://example.com/rss.xml
  node scripts/preprocess-rss-sitemap.js --file ./sitemap.xml --file ./feed.xml

Options:
  --site <origin>       Probe /sitemap.xml, /sitemaps.xml, /atom.xml, /rss.xml, and robots.txt.
  --url <url>           Process an explicit sitemap, Atom, or RSS URL. Repeatable.
  --file <path>         Process a local sitemap, Atom, or RSS XML file. Repeatable.
  --output <path>       Write JSON to a file instead of stdout.
  --max-depth <n>       Recursive sitemapindex depth. Default: ${DEFAULT_MAX_DEPTH}.
  --timeout-ms <n>      Fetch timeout in milliseconds. Default: ${DEFAULT_TIMEOUT_MS}.
  --no-robots           Skip robots.txt Sitemap directives when --site is used.
  --help                Show this help.
`);
}

function parseArgs(argv) {
  const args = {
    site: null,
    urls: [],
    files: [],
    output: null,
    maxDepth: DEFAULT_MAX_DEPTH,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    robots: true,
  };

  for (let index = 2; index < argv.length; index += 1) {
    const arg = argv[index];
    const next = () => {
      index += 1;
      if (index >= argv.length) {
        throw new Error(`Missing value for ${arg}`);
      }
      return argv[index];
    };

    if (arg === "--help" || arg === "-h") {
      args.help = true;
    } else if (arg === "--site") {
      args.site = normalizeOrigin(next());
    } else if (arg === "--url") {
      args.urls.push(normalizeUrl(next()));
    } else if (arg === "--file") {
      args.files.push(next());
    } else if (arg === "--output") {
      args.output = next();
    } else if (arg === "--max-depth") {
      args.maxDepth = parsePositiveInteger(next(), "--max-depth");
    } else if (arg === "--timeout-ms") {
      args.timeoutMs = parsePositiveInteger(next(), "--timeout-ms");
    } else if (arg === "--no-robots") {
      args.robots = false;
    } else {
      throw new Error(`Unknown option: ${arg}`);
    }
  }

  return args;
}

function parsePositiveInteger(value, flag) {
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed) || parsed < 0) {
    throw new Error(`${flag} must be a non-negative integer`);
  }
  return parsed;
}

function normalizeOrigin(value) {
  const url = new URL(value);
  return url.origin;
}

function normalizeUrl(value, base) {
  let url;
  try {
    url = new URL(value);
  } catch {
    url = new URL(value, base);
  }
  url.hash = "";
  return url.href;
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

async function fetchText(url, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      redirect: "follow",
      signal: controller.signal,
      headers: {
        "accept": "application/xml,text/xml,application/rss+xml,application/atom+xml,text/plain;q=0.8,*/*;q=0.2",
        "user-agent": "rss-sitemap-skill/1.0",
      },
    });
    const body = await response.text();
    return {
      url,
      finalUrl: response.url || url,
      status: response.status,
      ok: response.ok,
      contentType: response.headers.get("content-type") || "",
      body,
    };
  } finally {
    clearTimeout(timer);
  }
}

async function discoverRobotsSitemaps(origin, timeoutMs) {
  const robotsUrl = `${origin}/robots.txt`;
  const response = await fetchText(robotsUrl, timeoutMs);
  if (!response.ok) {
    return { resource: responseSummary(response, "robots"), urls: [] };
  }

  const urls = [];
  for (const line of response.body.split(/\r?\n/)) {
    const match = line.match(/^\s*sitemap\s*:\s*(\S+)\s*$/i);
    if (match) {
      urls.push(normalizeUrl(match[1], origin));
    }
  }

  return { resource: responseSummary(response, "robots"), urls: unique(urls) };
}

function responseSummary(response, role, error) {
  return {
    role,
    url: response.url,
    finalUrl: response.finalUrl,
    status: response.status,
    ok: response.ok,
    contentType: response.contentType,
    error: error ? String(error.message || error) : undefined,
  };
}

function fileResponse(filePath) {
  const body = fs.readFileSync(filePath, "utf8");
  return {
    url: filePath,
    finalUrl: filePath,
    status: 200,
    ok: true,
    contentType: "application/xml",
    body,
  };
}

function looksXmlLike(body) {
  const trimmed = body.trimStart();
  return trimmed.startsWith("<") && (
    /<(?:\w+:)?sitemapindex[\s>]/i.test(trimmed) ||
    /<(?:\w+:)?urlset[\s>]/i.test(trimmed) ||
    /<(?:\w+:)?rss[\s>]/i.test(trimmed) ||
    /<(?:\w+:)?feed[\s>]/i.test(trimmed) ||
    /<(?:\w+:)?rdf\b/i.test(trimmed)
  );
}

function decodeXml(value) {
  return String(value || "")
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, "\"")
    .replace(/&apos;/g, "'")
    .replace(/&amp;/g, "&")
    .trim();
}

function stripXmlNoise(xml) {
  return xml
    .replace(/<\?xml[\s\S]*?\?>/gi, "")
    .replace(/<!--[\s\S]*?-->/g, "");
}

function blocksFor(xml, tag) {
  const pattern = new RegExp(`<([\\w.-]+:)?${tag}\\b[^>]*>[\\s\\S]*?<\\/([\\w.-]+:)?${tag}>`, "gi");
  return xml.match(pattern) || [];
}

function firstText(block, tag) {
  const pattern = new RegExp(`<([\\w.-]+:)?${tag}\\b[^>]*>([\\s\\S]*?)<\\/([\\w.-]+:)?${tag}>`, "i");
  const match = block.match(pattern);
  return match ? decodeXml(match[2]) : null;
}

function allTags(block, tag) {
  const pattern = new RegExp(`<([\\w.-]+:)?${tag}\\b([^>]*)\\/?>(?:[\\s\\S]*?<\\/([\\w.-]+:)?${tag}>)?`, "gi");
  return [...block.matchAll(pattern)].map((match) => ({
    raw: match[0],
    attrs: parseAttributes(match[2] || ""),
  }));
}

function parseAttributes(rawAttrs) {
  const attrs = {};
  const pattern = /([\w:.-]+)\s*=\s*("([^"]*)"|'([^']*)'|([^\s"'=<>`]+))/g;
  for (const match of rawAttrs.matchAll(pattern)) {
    attrs[match[1]] = decodeXml(match[3] || match[4] || match[5] || "");
  }
  return attrs;
}

function toAbsoluteMaybe(value, base) {
  if (!value) {
    return null;
  }
  try {
    return normalizeUrl(value, base);
  } catch {
    return null;
  }
}

function parseXmlResource(xml, sourceUrl) {
  const clean = stripXmlNoise(xml);

  if (/<(?:[\w.-]+:)?sitemapindex\b/i.test(clean)) {
    const entries = blocksFor(clean, "sitemap").map((block) => ({
      type: "sitemap",
      url: toAbsoluteMaybe(firstText(block, "loc"), sourceUrl),
      lastmod: firstText(block, "lastmod"),
      source: sourceUrl,
    })).filter((entry) => entry.url);
    return { kind: "sitemapindex", entries };
  }

  if (/<(?:[\w.-]+:)?urlset\b/i.test(clean)) {
    const entries = blocksFor(clean, "url").map((block) => ({
      type: "url",
      url: toAbsoluteMaybe(firstText(block, "loc"), sourceUrl),
      lastmod: firstText(block, "lastmod"),
      changefreq: firstText(block, "changefreq"),
      priority: firstText(block, "priority"),
      source: sourceUrl,
    })).filter((entry) => entry.url);
    return { kind: "urlset", entries };
  }

  if (/<(?:[\w.-]+:)?feed\b/i.test(clean)) {
    const entries = blocksFor(clean, "entry").map((block) => {
      const links = allTags(block, "link")
        .map((link) => ({
          href: toAbsoluteMaybe(link.attrs.href, sourceUrl),
          rel: link.attrs.rel || "",
          type: link.attrs.type || "",
        }))
        .filter((link) => link.href);
      const preferred = links.find((link) => !link.rel || link.rel === "alternate") || links[0] || {};
      return {
        type: "atom-entry",
        url: preferred.href || null,
        title: firstText(block, "title"),
        id: firstText(block, "id"),
        updated: firstText(block, "updated"),
        published: firstText(block, "published"),
        summary: firstText(block, "summary"),
        source: sourceUrl,
      };
    }).filter((entry) => entry.url || entry.id);
    return { kind: "atom", entries };
  }

  if (/<(?:[\w.-]+:)?rss\b/i.test(clean) || /<(?:[\w.-]+:)?rdf\b/i.test(clean)) {
    const entries = blocksFor(clean, "item").map((block) => {
      const link = toAbsoluteMaybe(firstText(block, "link"), sourceUrl);
      const guid = firstText(block, "guid");
      return {
        type: "rss-item",
        url: link || toAbsoluteMaybe(guid, sourceUrl),
        title: firstText(block, "title"),
        guid,
        pubDate: firstText(block, "pubDate"),
        description: firstText(block, "description"),
        source: sourceUrl,
      };
    }).filter((entry) => entry.url || entry.guid);
    return { kind: "rss", entries };
  }

  return { kind: "unknown", entries: [] };
}

function dedupeEntries(entries) {
  const seen = new Set();
  const result = [];

  for (const entry of entries) {
    const key = entry.url || `${entry.type}:${entry.id || entry.guid || entry.title || ""}`;
    if (!key || seen.has(key)) {
      continue;
    }
    seen.add(key);
    result.push(entry);
  }

  return result;
}

async function processResource(url, state, depth) {
  if (state.visited.has(url)) {
    return;
  }
  state.visited.add(url);

  let response;
  try {
    response = await fetchText(url, state.timeoutMs);
  } catch (error) {
    state.resources.push({
      role: "xml",
      url,
      finalUrl: url,
      status: null,
      ok: false,
      contentType: "",
      error: String(error.message || error),
    });
    return;
  }

  const summary = responseSummary(response, "xml");
  state.resources.push(summary);
  if (!response.ok || !looksXmlLike(response.body)) {
    return;
  }

  const parsed = parseXmlResource(response.body, response.finalUrl || url);
  summary.kind = parsed.kind;
  summary.entryCount = parsed.entries.length;
  state.entries.push(...parsed.entries);

  if (parsed.kind === "sitemapindex" && depth < state.maxDepth) {
    for (const entry of parsed.entries) {
      await processResource(entry.url, state, depth + 1);
    }
  }
}

async function processFile(filePath, state) {
  if (state.visited.has(filePath)) {
    return;
  }
  state.visited.add(filePath);

  let response;
  try {
    response = fileResponse(filePath);
  } catch (error) {
    state.resources.push({
      role: "file",
      url: filePath,
      finalUrl: filePath,
      status: null,
      ok: false,
      contentType: "",
      error: String(error.message || error),
    });
    return;
  }

  const summary = responseSummary(response, "file");
  state.resources.push(summary);
  if (!looksXmlLike(response.body)) {
    return;
  }

  const parsed = parseXmlResource(response.body, response.finalUrl);
  summary.kind = parsed.kind;
  summary.entryCount = parsed.entries.length;
  state.entries.push(...parsed.entries);
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    usage();
    return;
  }

  if (!args.site && args.urls.length === 0 && args.files.length === 0) {
    usage();
    process.exitCode = 2;
    return;
  }

  const seedUrls = [];
  const resources = [];
  if (args.site) {
    seedUrls.push(...DEFAULT_PATHS.map((path) => `${args.site}${path}`));
    if (args.robots) {
      try {
        const robots = await discoverRobotsSitemaps(args.site, args.timeoutMs);
        resources.push(robots.resource);
        seedUrls.push(...robots.urls);
      } catch (error) {
        resources.push({
          role: "robots",
          url: `${args.site}/robots.txt`,
          finalUrl: `${args.site}/robots.txt`,
          status: null,
          ok: false,
          contentType: "",
          error: String(error.message || error),
        });
      }
    }
  }
  seedUrls.push(...args.urls);

  const state = {
    timeoutMs: args.timeoutMs,
    maxDepth: args.maxDepth,
    visited: new Set(),
    resources,
    entries: [],
  };

  for (const url of unique(seedUrls)) {
    await processResource(url, state, 0);
  }

  for (const filePath of unique(args.files)) {
    await processFile(filePath, state);
  }

  const output = {
    generatedAt: new Date().toISOString(),
    input: {
      site: args.site,
      urls: args.urls,
      files: args.files,
      maxDepth: args.maxDepth,
      robots: args.robots,
    },
    resources: state.resources,
    entries: dedupeEntries(state.entries),
  };

  const json = `${JSON.stringify(output, null, 2)}\n`;
  if (args.output) {
    fs.writeFileSync(args.output, json);
  } else {
    process.stdout.write(json);
  }
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exit(1);
});
