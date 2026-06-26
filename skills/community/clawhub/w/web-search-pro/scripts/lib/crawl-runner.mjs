import { fetchUrlSnapshot } from "./web-fetch.mjs";

function normalizePathPrefixes(prefixes = []) {
  return Array.from(
    new Set(
      prefixes
        .map((prefix) => String(prefix).trim())
        .filter(Boolean)
        .map((prefix) => (prefix.startsWith("/") ? prefix : `/${prefix}`)),
    ),
  );
}

function normalizeAbsoluteUrl(input) {
  const url = new URL(input);
  url.hash = "";
  if ((url.protocol === "http:" && url.port === "80") || (url.protocol === "https:" && url.port === "443")) {
    url.port = "";
  }
  return url.toString();
}

function shouldIncludePath(url, options = {}) {
  const includePathPrefixes = normalizePathPrefixes(options.includePathPrefixes);
  const excludePathPrefixes = normalizePathPrefixes(options.excludePathPrefixes);
  const pathname = url.pathname || "/";

  if (excludePathPrefixes.some((prefix) => pathname.startsWith(prefix))) {
    return false;
  }
  if (includePathPrefixes.length === 0) {
    return true;
  }
  return includePathPrefixes.some((prefix) => pathname.startsWith(prefix));
}

function parseRobotsTxt(body) {
  const lines = String(body ?? "").split(/\r?\n/);
  const disallowed = [];
  let applies = false;

  for (const rawLine of lines) {
    const line = rawLine.replace(/#.*$/, "").trim();
    if (!line) {
      continue;
    }
    const [rawKey, ...rest] = line.split(":");
    const key = rawKey.trim().toLowerCase();
    const value = rest.join(":").trim();

    if (key === "user-agent") {
      applies = value === "*" ? true : false;
      continue;
    }
    if (applies && key === "disallow" && value) {
      disallowed.push(value);
    }
  }

  return disallowed;
}

async function loadRobotsRules(origin, options, cache) {
  if (!options.respectRobotsTxt) {
    return [];
  }
  if (cache.has(origin)) {
    return cache.get(origin);
  }

  try {
    const snapshot = await fetchUrlSnapshot(new URL("/robots.txt", origin).toString(), {
      lookupAll: options.lookupAll,
      requestTextFn: options.requestTextFn,
      timeoutMs: options.timeoutMs,
      maxRedirects: options.maxRedirects,
      maxChars: 64_000,
    });
    const rules = parseRobotsTxt(snapshot.body);
    cache.set(origin, rules);
    return rules;
  } catch {
    cache.set(origin, []);
    return [];
  }
}

async function isAllowedByRobots(url, options, cache) {
  if (!options.respectRobotsTxt) {
    return true;
  }
  const rules = await loadRobotsRules(url.origin, options, cache);
  return !rules.some((prefix) => url.pathname.startsWith(prefix));
}

export async function discoverSite(entryUrls, options = {}) {
  const normalizedEntries = Array.from(
    new Set(entryUrls.map((entryUrl) => normalizeAbsoluteUrl(entryUrl))),
  );
  const allowedOrigins = new Set(normalizedEntries.map((entryUrl) => new URL(entryUrl).origin));
  const sameOrigin = options.sameOrigin ?? true;
  const depthLimit = options.depth ?? 1;
  const maxPages = options.maxPages ?? 10;
  const visited = [];
  const failures = [];
  const queue = normalizedEntries.map((url) => ({
    url,
    depth: 0,
    discoveredFrom: null,
  }));
  const seen = new Set(normalizedEntries);
  const robotsCache = new Map();

  while (queue.length > 0 && visited.length < maxPages) {
    const current = queue.shift();

    try {
      const currentUrl = new URL(current.url);
      const isEntry = current.depth === 0 && current.discoveredFrom === null;

      if (!isEntry && !shouldIncludePath(currentUrl, options)) {
        continue;
      }
      if (!(await isAllowedByRobots(currentUrl, options, robotsCache))) {
        throw new Error(`Blocked by robots.txt: ${current.url}`);
      }

      const snapshot = await fetchUrlSnapshot(current.url, {
        lookupAll: options.lookupAll,
        requestTextFn: options.requestTextFn,
        timeoutMs: options.timeoutMs,
        maxRedirects: options.maxRedirects,
        maxChars: options.maxChars,
      });

      const page = {
        url: snapshot.url,
        title: snapshot.title,
        contentType: snapshot.contentType,
        content: snapshot.content,
        depth: current.depth,
        discoveredFrom: current.discoveredFrom,
        links: snapshot.links,
        isHtml: snapshot.isHtml,
      };
      visited.push(page);
      await options.onVisit?.({
        current,
        page,
      });

      if (!snapshot.isHtml || current.depth >= depthLimit) {
        continue;
      }

      for (const href of snapshot.links) {
        let normalizedLink;
        try {
          normalizedLink = normalizeAbsoluteUrl(href);
        } catch {
          continue;
        }

        if (seen.has(normalizedLink)) {
          continue;
        }

        const nextUrl = new URL(normalizedLink);
        if (sameOrigin && !allowedOrigins.has(nextUrl.origin)) {
          continue;
        }
        if (!shouldIncludePath(nextUrl, options)) {
          continue;
        }
        if (!(await isAllowedByRobots(nextUrl, options, robotsCache))) {
          continue;
        }

        seen.add(normalizedLink);
        queue.push({
          url: normalizedLink,
          depth: current.depth + 1,
          discoveredFrom: snapshot.url,
        });

        await options.onDiscover?.({
          from: snapshot.url,
          to: normalizedLink,
          depth: current.depth + 1,
        });
      }
    } catch (error) {
      failures.push({
        url: current.url,
        depth: current.depth,
        discoveredFrom: current.discoveredFrom,
        error: error.message,
      });
      await options.onFailure?.({
        current,
        error,
      });
    }
  }

  return {
    entryUrls: normalizedEntries,
    visited,
    failed: failures,
    maxPagesReached: visited.length >= maxPages && queue.length > 0,
  };
}

export async function crawlSite(entryUrls, options = {}) {
  const discovery = await discoverSite(entryUrls, options);

  return {
    pages: discovery.visited.map((page) => ({
      url: page.url,
      title: page.title,
      contentType: page.contentType,
      content: page.content,
      depth: page.depth,
      discoveredFrom: page.discoveredFrom,
    })),
    failed: discovery.failed,
    summary: {
      entryUrls: discovery.entryUrls,
      visitedPages: discovery.visited.length,
      maxPagesReached: discovery.maxPagesReached,
    },
  };
}
