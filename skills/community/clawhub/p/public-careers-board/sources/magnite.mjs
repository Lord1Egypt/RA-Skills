// Declared Magnite source. The pinned normalizeWorkday function stays in
// recipe/boards.mjs and is passed in by the caller. This module does not widen
// that file's host gate and does not accept a caller-supplied origin.

export const USER_AGENT = "SameDayDesk-careers-trial (https://samedaydesk.com)";

const ORIGIN = "https://osv-rubicon.wd5.myworkdayjobs.com";

export const MAGNITE = {
  id: "magnite",
  company: "Magnite",
  careersPage: "https://www.magnite.com/careers/",
  robotsUrl: "https://www.magnite.com/robots.txt",
  handoffLabel: "Search Jobs",
  boardUrl: `${ORIGIN}/MagniteCareers`,
  host: "osv-rubicon.wd5.myworkdayjobs.com",
  hostnameLabel: "osv-rubicon",
  tenant: "osv_rubicon",
  siteId: "MagniteCareers",
  endpoint: `${ORIGIN}/wday/cxs/osv_rubicon/MagniteCareers/jobs`,
  method: "POST",
  forbiddenPathPrefix: "/refreshFacet/",
  limit: 20,
  maxPages: 4,
  staleSuppliedSource: "https://api.smartrecruiters.com/v1/companies/Magnite/postings",
};

const ALLOWED_URLS = new Set([
  new URL(MAGNITE.robotsUrl).href,
  new URL(MAGNITE.careersPage).href,
  new URL(MAGNITE.boardUrl).href,
  new URL(MAGNITE.endpoint).href,
]);

export function endpointUsingHostnameLabel(source = MAGNITE) {
  const board = new URL(source.boardUrl);
  const label = board.host.split(".")[0];
  return `${board.origin}/wday/cxs/${label}/${source.siteId}/jobs`;
}

export function assertSourceIdentity(source = MAGNITE) {
  const board = new URL(source.boardUrl);
  const endpoint = new URL(source.endpoint);
  if (source.tenant === source.hostnameLabel) {
    throw Object.assign(new Error("tenant_matches_hostname_label"), { code: "tampered_source" });
  }
  if (board.host !== source.host || endpoint.host !== source.host) {
    throw Object.assign(new Error("host_drift"), { code: "tampered_source" });
  }
  const built = `${board.origin}/wday/cxs/${source.tenant}/${source.siteId}/jobs`;
  if (built !== source.endpoint || endpointUsingHostnameLabel(source) === source.endpoint) {
    throw Object.assign(new Error("endpoint_drift"), { code: "tampered_source" });
  }
  if (source.endpoint.includes(`/${source.hostnameLabel}/`)) {
    throw Object.assign(new Error("hostname_label_in_endpoint"), { code: "tampered_source" });
  }
  return true;
}

assertSourceIdentity(MAGNITE);

export function gateMagnite(url) {
  let parsed;
  try {
    parsed = new URL(url);
  } catch {
    return { ok: false, status: "invalid_url", host: null };
  }
  if (parsed.protocol !== "https:" || parsed.username || parsed.password) {
    return { ok: false, status: "rejected_url", host: parsed.host };
  }
  if (parsed.pathname.startsWith(MAGNITE.forbiddenPathPrefix)) {
    return { ok: false, status: "forbidden_path", host: parsed.host };
  }
  if (!ALLOWED_URLS.has(parsed.href)) return { ok: false, status: "unknown_origin", host: parsed.host };
  return { ok: true, status: "allowed", host: parsed.host };
}

export function classifyStaleSuppliedList(body) {
  if (!body || typeof body !== "object" || !Array.isArray(body.content) || typeof body.totalFound !== "number") {
    return { status: "wrong_schema", emptyBoard: false, companyBoardEmpty: false };
  }
  const empty = body.totalFound === 0 && body.content.length === 0;
  return {
    status: empty ? "empty_for_this_source" : "rows_for_this_source",
    emptyBoard: false,
    companyBoardEmpty: false,
    totalFound: body.totalFound,
  };
}

export function parseRobots(text) {
  const groups = [];
  let current = null;
  let fileCrawlDelay = null;
  for (const raw of String(text ?? "").split(/\r?\n/)) {
    const line = raw.replace(/#.*$/, "").trim();
    if (!line) continue;
    const idx = line.indexOf(":");
    if (idx < 0) continue;
    const field = line.slice(0, idx).trim().toLowerCase();
    const value = line.slice(idx + 1).trim();
    if (!current && field === "crawl-delay") {
      const n = Number(value);
      if (Number.isFinite(n) && n >= 0) fileCrawlDelay = Math.max(fileCrawlDelay ?? 0, n);
      continue;
    }
    if (field === "user-agent") {
      if (!current || current.rules.length > 0 || current.crawlDelay != null) {
        current = { agents: [], rules: [], crawlDelay: null };
        groups.push(current);
      }
      current.agents.push(value.toLowerCase());
      continue;
    }
    if (!current) continue;
    if (field === "allow" || field === "disallow") current.rules.push({ field, value });
    if (field === "crawl-delay") {
      const n = Number(value);
      if (Number.isFinite(n) && n >= 0) current.crawlDelay = n;
    }
  }
  return { groups, fileCrawlDelay };
}

function applicableGroups(parsed) {
  return parsed.groups.filter((group) => group.agents.includes("*"));
}

export function robotsDecision(parsed, path) {
  const groups = applicableGroups(parsed);
  let match = null;
  let crawlDelaySec = parsed.fileCrawlDelay ?? 0;
  for (const group of groups) {
    if (group.crawlDelay != null) crawlDelaySec = Math.max(crawlDelaySec, group.crawlDelay);
    for (const rule of group.rules) {
      if (!rule.value) continue;
      if (path.startsWith(rule.value) && (!match || rule.value.length > match.value.length)) match = rule;
    }
  }
  return {
    allowed: match ? match.field === "allow" : true,
    crawlDelaySec,
    match,
  };
}

function decodeEntities(value) {
  return value
    .replace(/&#x([0-9a-f]+);/gi, (_, hex) => String.fromCodePoint(Number.parseInt(hex, 16)))
    .replace(/&#(\d+);/g, (_, dec) => String.fromCodePoint(Number(dec)))
    .replace(/&quot;/g, "\"")
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&");
}

export function canonicalBoardHref(value) {
  const url = new URL(value);
  url.hash = "";
  url.search = "";
  if (url.pathname.length > 1 && url.pathname.endsWith("/")) url.pathname = url.pathname.slice(0, -1);
  return url.href;
}

export function parseSearchJobsLinks(html, baseUrl) {
  const links = [];
  const re = /<a\b([^>]*)>([\s\S]*?)<\/a>/gi;
  for (const match of String(html ?? "").matchAll(re)) {
    const hrefMatch = match[1].match(/\bhref\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/i);
    if (!hrefMatch) continue;
    const text = decodeEntities(match[2].replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim());
    if (text.toLowerCase() !== "search jobs") continue;
    const hrefRaw = decodeEntities(hrefMatch[1] ?? hrefMatch[2] ?? hrefMatch[3] ?? "");
    let href = null;
    try {
      href = new URL(hrefRaw, baseUrl).href;
    } catch {
      href = null;
    }
    links.push({ text, href });
  }
  return links;
}

export function agreeBoard(links, expectedHref) {
  let expected;
  try {
    expected = canonicalBoardHref(expectedHref);
  } catch {
    return { status: "invalid_expected_board", hrefs: [] };
  }
  const hrefs = [];
  for (const link of links) {
    if (!link.href) continue;
    try {
      hrefs.push(canonicalBoardHref(link.href));
    } catch {
      hrefs.push(link.href);
    }
  }
  const unique = [...new Set(hrefs)];
  if (links.length === 0) return { status: "missing_search_jobs_link", hrefs: unique, expected };
  if (unique.length !== 1) return { status: "ambiguous_handoff", hrefs: unique, expected };
  if (unique[0] !== expected) return { status: "unconfigured_handoff_target", hrefs: unique, expected };
  return { status: "confirmed", href: unique[0], hrefs: unique, expected };
}

function jsString(html, key) {
  const match = String(html ?? "").match(new RegExp(`\\b${key}:\\s*"([^"]*)"`));
  return match ? match[1] : null;
}

function jsBoolOrNull(html, key) {
  const match = String(html ?? "").match(new RegExp(`\\b${key}:\\s*(true|false|null)\\b`));
  if (!match) return { present: false, value: null };
  return { present: true, value: match[1] === "null" ? null : match[1] === "true" };
}

const SAFE_ID = /^[A-Za-z0-9_-]+$/;

export function parseShell(html) {
  const source = String(html ?? "");
  const tokenPresent = /\btoken:\s*"([^"]*)"/.test(source);
  const tenant = jsString(source, "tenant");
  const siteId = jsString(source, "siteId");
  const appName = jsString(source, "appName");
  const isExternal = jsBoolOrNull(source, "isExternal");
  const idsOk = SAFE_ID.test(tenant ?? "") && SAFE_ID.test(siteId ?? "");
  let status = "ok";
  if (!tenant || !siteId || !appName) status = "shell_missing_config";
  else if (!idsOk) status = "shell_unsafe_identifier";
  else if (appName !== "cxs") status = "unexpected_app";
  else if (!isExternal.present || isExternal.value !== true) status = "not_external";
  return {
    status,
    tenant: idsOk ? tenant : null,
    siteId: idsOk ? siteId : null,
    appName,
    isExternal: isExternal.value,
    anonymousShellTokenPresent: tokenPresent,
  };
}

export function identityDecision(shell, source = MAGNITE) {
  if (!shell || shell.status !== "ok") {
    return { ok: false, reason: shell?.status || "shell_missing_config" };
  }
  if (shell.tenant === source.hostnameLabel) return { ok: false, reason: "hostname_used_as_tenant" };
  if (shell.tenant !== source.tenant || shell.siteId !== source.siteId) {
    return { ok: false, reason: "tenant_or_site_mismatch" };
  }
  const built = `${new URL(source.boardUrl).origin}/wday/cxs/${shell.tenant}/${shell.siteId}/jobs`;
  if (built !== source.endpoint) return { ok: false, reason: "declared_endpoint_mismatch" };
  return { ok: true, reason: "ok" };
}

export async function collectWorkdayPages({ load, maxPages }) {
  const pages = [];
  const loaded = await load(0);
  let probe = null;
  let stopReason = loaded.skipped ? loaded.stopReason : null;
  if (loaded.skipped) return { pages, probe, stopReason };
  pages.push(loaded);
  const declared = loaded.body?.total;
  const firstOk = loaded.httpStatus === 200
    && loaded.error == null
    && Number.isInteger(declared)
    && declared > 0
    && Array.isArray(loaded.body?.jobPostings);
  if (!firstOk) return { pages, probe, stopReason };
  let offset = loaded.body.jobPostings.length;
  const seen = new Set(loaded.body.jobPostings.map((job) => job?.externalPath).filter(Boolean));
  while (offset > 0 && offset < declared && pages.length < maxPages) {
    const page = await load(offset);
    if (page.skipped) {
      stopReason = page.stopReason;
      break;
    }
    const postings = page.body?.jobPostings;
    if (page.httpStatus !== 200 || page.error || !Array.isArray(postings) || postings.length === 0) {
      pages.push(page);
      break;
    }
    const paths = postings.map((job) => job?.externalPath).filter(Boolean);
    if (paths.length > 0 && paths.every((path) => seen.has(path))) {
      probe = page;
      break;
    }
    for (const path of paths) seen.add(path);
    pages.push(page);
    offset += postings.length;
  }
  if (!probe && !stopReason && pages.length < maxPages && offset >= declared) {
    const past = await load(declared);
    if (past.skipped) stopReason = past.stopReason;
    else probe = past;
  } else if (!probe && !stopReason && offset < declared && pages.length >= maxPages) {
    stopReason = "page_budget";
  }
  return { pages, probe, stopReason };
}

const TRANSPORT_ERRORS = new Set([
  "response_too_large",
  "timeout",
  "network",
  "deadline",
  "wrong_host",
  "forbidden_path",
]);

function defaultSleep(ms, signal) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      signal?.removeEventListener("abort", onAbort);
      resolve();
    }, ms);
    const onAbort = () => {
      clearTimeout(timer);
      reject(Object.assign(new Error("deadline"), { code: "deadline" }));
    };
    if (signal?.aborted) onAbort();
    else signal?.addEventListener("abort", onAbort, { once: true });
  });
}

function publicLog(entry) {
  return {
    purpose: entry.purpose,
    method: entry.method,
    url: entry.url,
    httpStatus: entry.httpStatus,
    elapsedMs: entry.elapsedMs,
    bytes: entry.bytes,
    error: entry.error,
    offset: entry.offset ?? null,
  };
}

async function readBounded(response, cap, controller) {
  const reader = response.body?.getReader();
  if (!reader) return { bytes: 0, text: "", error: null };
  const chunks = [];
  let bytes = 0;
  let onAbort;
  const aborted = new Promise((_, reject) => {
    onAbort = () => {
      reject(Object.assign(new Error("aborted"), { name: "AbortError" }));
      void reader.cancel("request aborted").catch(() => {});
    };
    controller.signal.addEventListener("abort", onAbort, { once: true });
  });
  try {
    if (controller.signal.aborted) onAbort();
    while (true) {
      const { done, value } = await Promise.race([reader.read(), aborted]);
      if (done) break;
      bytes += value.byteLength;
      if (bytes > cap) {
        controller.abort();
        await reader.cancel("response_too_large").catch(() => {});
        return { bytes, text: null, error: "response_too_large" };
      }
      chunks.push(value);
    }
  } catch (error) {
    if (error?.name === "AbortError") return { bytes, text: null, error: "timeout" };
    return { bytes, text: null, error: "network" };
  } finally {
    if (onAbort) controller.signal.removeEventListener("abort", onAbort);
    try { reader.releaseLock(); } catch { /* already cancelled */ }
  }
  const raw = new Uint8Array(bytes);
  let offset = 0;
  for (const chunk of chunks) {
    raw.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return { bytes, text: new TextDecoder().decode(raw), error: null };
}

async function requestPublic(url, options) {
  const method = options.method || "GET";
  const started = Date.now();
  const gate = gateMagnite(url);
  if (!gate.ok) {
    return {
      purpose: options.purpose,
      url,
      method,
      httpStatus: 0,
      body: null,
      text: null,
      elapsedMs: 0,
      bytes: 0,
      error: "wrong_host",
      offset: options.offset ?? null,
      fetched: false,
    };
  }
  const timeoutMs = options.timeoutMs;
  const cap = Number.isInteger(options.maxBytes) && options.maxBytes > 0 ? options.maxBytes : 1_000_000;
  const fetchFn = typeof options.fetchImpl === "function" ? options.fetchImpl : fetch;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  const signals = [controller.signal, options.signal].filter(Boolean);
  const signal = signals.length > 1 ? AbortSignal.any(signals) : signals[0];
  const onParent = () => controller.abort();
  if (options.signal) options.signal.addEventListener("abort", onParent, { once: true });
  let readerController = controller;
  try {
    const headers = { accept: options.accept, "user-agent": USER_AGENT };
    if (options.payload !== undefined) headers["content-type"] = "application/json";
    const response = await fetchFn(url, {
      method,
      redirect: "manual",
      headers,
      body: options.payload === undefined ? undefined : JSON.stringify(options.payload),
      signal,
    });
    const readController = new AbortController();
    const onEither = () => readController.abort();
    signal.addEventListener("abort", onEither, { once: true });
    readerController = readController;
    const read = await readBounded(response, cap, readController);
    signal.removeEventListener("abort", onEither);
    if (read.error) {
      return {
        purpose: options.purpose,
        url,
        method,
        httpStatus: response.status,
        body: null,
        text: null,
        elapsedMs: Date.now() - started,
        bytes: read.bytes,
        error: read.error,
        offset: options.offset ?? null,
        fetched: true,
      };
    }
    let body = null;
    let error = null;
    if (options.parseJson) {
      try {
        body = JSON.parse(read.text);
      } catch {
        body = null;
        error = "invalid_json";
      }
    }
    return {
      purpose: options.purpose,
      url,
      method,
      httpStatus: response.status,
      body,
      text: options.parseJson ? null : read.text,
      elapsedMs: Date.now() - started,
      bytes: read.bytes,
      error,
      offset: options.offset ?? null,
      fetched: true,
    };
  } catch (error) {
    return {
      purpose: options.purpose,
      url,
      method,
      httpStatus: 0,
      body: null,
      text: null,
      elapsedMs: Date.now() - started,
      bytes: 0,
      error: error?.name === "AbortError" || error?.code === "deadline" ? "timeout" : "network",
      offset: options.offset ?? null,
      fetched: true,
    };
  } finally {
    clearTimeout(timer);
    if (options.signal) options.signal.removeEventListener("abort", onParent);
    void readerController;
  }
}

function isRedirect(status) {
  return Number.isInteger(status) && status >= 300 && status < 400;
}

function redirectRefusal(requests) {
  return classified(
    requests,
    "not_fetched",
    "unexpected_redirect",
    "A declared Magnite URL returned a redirect. The redirect was not followed. This is not an empty board.",
  );
}

async function waitForCrawlDelay(delayMs, remaining, sleep, signal) {
  if (delayMs >= remaining()) return false;
  if (delayMs <= 0) return remaining() > 0;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), Math.max(remaining(), 0));
  const onParent = () => controller.abort();
  if (signal) signal.addEventListener("abort", onParent, { once: true });
  try {
    await sleep(delayMs, controller.signal);
  } catch (error) {
    if (error?.code === "deadline" || error?.name === "AbortError") return false;
    throw error;
  } finally {
    clearTimeout(timer);
    if (signal) signal.removeEventListener("abort", onParent);
  }
  return remaining() > 0;
}

function classified(requests, result, reason, nextAction, extra = {}) {
  return {
    kind: "classified",
    result,
    reason,
    nextAction,
    requests,
    emptyBoard: false,
    handoff: extra.handoff ?? null,
    identity: extra.identity ?? null,
  };
}

function failureObservation(requests, error, httpStatus = 0) {
  return {
    kind: "observation",
    rows: [],
    coverage: {
      status: "source_failure",
      emptyBoard: false,
      httpStatus,
      declaredTotal: null,
      remaining: null,
      roleFilter: null,
      error: error ?? "source_failure",
      searchText: "",
      requests,
    },
  };
}

function handoffView(agreement) {
  return {
    status: agreement.status,
    href: agreement.href ?? null,
    hrefs: agreement.hrefs,
    expected: agreement.expected,
  };
}

function identityView(shell, reason) {
  return {
    status: reason === "ok" ? "ok" : "mismatch",
    reason,
    tenant: shell?.tenant ?? null,
    siteId: shell?.siteId ?? null,
    hostnameLabel: MAGNITE.hostnameLabel,
    endpoint: MAGNITE.endpoint,
  };
}

export async function fetchMagnite(options = {}) {
  const normalizeWorkday = options.normalizeWorkday;
  if (typeof normalizeWorkday !== "function") {
    throw Object.assign(new Error("missing_normalizer"), { code: "tampered_source" });
  }
  assertSourceIdentity(MAGNITE);
  const timeoutMs = Number.isFinite(options.timeoutMs) ? options.timeoutMs : 15000;
  const deadline = Date.now() + timeoutMs;
  const remaining = () => deadline - Date.now();
  const sleep = typeof options.sleep === "function" ? options.sleep : defaultSleep;
  const requests = [];
  const common = {
    maxBytes: options.maxBytes,
    fetchImpl: options.fetchImpl,
    signal: options.signal,
  };

  const robots = await requestPublic(MAGNITE.robotsUrl, {
    ...common,
    method: "GET",
    timeoutMs: Math.max(remaining(), 0),
    accept: "text/plain",
    purpose: "robots",
    parseJson: false,
  });
  requests.push(publicLog(robots));
  if (TRANSPORT_ERRORS.has(robots.error)) return failureObservation(requests, robots.error, robots.httpStatus);
  if (isRedirect(robots.httpStatus)) return redirectRefusal(requests);
  if (robots.httpStatus !== 200 || robots.error) {
    return classified(
      requests,
      "not_fetched",
      "robots_unreadable",
      "The careers host robots file was not readable, so the handoff was not checked. This is not an empty board.",
    );
  }
  const robotsParsed = parseRobots(robots.text);
  const careersRule = robotsDecision(robotsParsed, new URL(MAGNITE.careersPage).pathname);
  if (!careersRule.allowed) {
    return classified(
      requests,
      "not_fetched",
      "robots_disallow",
      "The careers host robots file disallows the careers page. The handoff was not checked. This is not an empty board.",
    );
  }
  const delayMs = Math.round(careersRule.crawlDelaySec * 1000);
  const delayFits = await waitForCrawlDelay(delayMs, remaining, sleep, options.signal);
  if (!delayFits) {
    return classified(
      requests,
      "not_fetched",
      "crawl_delay_exceeds_deadline",
      "The careers host crawl delay does not fit the deadline. The handoff was not skipped and the jobs endpoint was not called. This is not an empty board.",
    );
  }

  const careers = await requestPublic(MAGNITE.careersPage, {
    ...common,
    method: "GET",
    timeoutMs: Math.max(remaining(), 0),
    accept: "text/html",
    purpose: "careers",
    parseJson: false,
  });
  requests.push(publicLog(careers));
  if (TRANSPORT_ERRORS.has(careers.error)) return failureObservation(requests, careers.error, careers.httpStatus);
  if (isRedirect(careers.httpStatus)) return redirectRefusal(requests);
  if (careers.httpStatus !== 200 || careers.error) {
    return failureObservation(requests, careers.error || "careers_http", careers.httpStatus);
  }
  const agreement = agreeBoard(parseSearchJobsLinks(careers.text, MAGNITE.careersPage), MAGNITE.boardUrl);
  if (agreement.status !== "confirmed") {
    return classified(
      requests,
      "source_moved",
      agreement.status,
      "The official Search Jobs link does not match the declared Magnite Workday board. No jobs request was sent. This is not an empty board.",
      { handoff: handoffView(agreement) },
    );
  }

  const shellEntry = await requestPublic(MAGNITE.boardUrl, {
    ...common,
    method: "GET",
    timeoutMs: Math.max(remaining(), 0),
    accept: "text/html",
    purpose: "shell",
    parseJson: false,
  });
  requests.push(publicLog(shellEntry));
  if (TRANSPORT_ERRORS.has(shellEntry.error)) return failureObservation(requests, shellEntry.error, shellEntry.httpStatus);
  if (isRedirect(shellEntry.httpStatus)) return redirectRefusal(requests);
  if (shellEntry.httpStatus !== 200 || shellEntry.error) {
    return failureObservation(requests, shellEntry.error || "shell_http", shellEntry.httpStatus);
  }
  const shell = parseShell(shellEntry.text);
  const identity = identityDecision(shell);
  if (!identity.ok) {
    return classified(
      requests,
      "identity_mismatch",
      identity.reason,
      "The Workday shell tenant or site does not match the declared Magnite source. The hostname label is not the tenant. No jobs request was sent. This is not an empty board.",
      { handoff: handoffView(agreement), identity: identityView(shell, identity.reason) },
    );
  }

  const rowFetchedAt = new Date().toISOString();
  const load = async (offset) => {
    const left = remaining();
    if (left <= 0) {
      const entry = {
        purpose: "jobs",
        url: MAGNITE.endpoint,
        method: "POST",
        httpStatus: 0,
        elapsedMs: 0,
        bytes: 0,
        error: "timeout",
        offset,
      };
      requests.push(entry);
      return { offset, httpStatus: 0, error: "timeout", body: null, skipped: true, stopReason: "deadline" };
    }
    const entry = await requestPublic(MAGNITE.endpoint, {
      ...common,
      method: "POST",
      payload: { appliedFacets: {}, limit: MAGNITE.limit, offset, searchText: "" },
      timeoutMs: left,
      accept: "application/json",
      purpose: "jobs",
      parseJson: true,
      offset,
    });
    requests.push(publicLog(entry));
    return {
      offset,
      httpStatus: entry.httpStatus,
      error: entry.error,
      body: entry.error ? null : entry.body,
      skipped: false,
    };
  };

  const collected = await collectWorkdayPages({ load, maxPages: MAGNITE.maxPages });
  const first = collected.pages[0];
  if (!first || TRANSPORT_ERRORS.has(first.error)) {
    return failureObservation(requests, first?.error || collected.stopReason || "not_fetched", first?.httpStatus ?? 0);
  }
  if (isRedirect(first.httpStatus)) return redirectRefusal(requests);
  const normalized = normalizeWorkday({
    pages: collected.pages.map((page) => ({
      offset: page.offset,
      httpStatus: page.httpStatus,
      body: page.error ? null : page.body,
    })),
    probe: collected.probe
      ? {
        offset: collected.probe.offset,
        httpStatus: collected.probe.httpStatus,
        body: collected.probe.error ? null : collected.probe.body,
      }
      : null,
  }, {
    boardUrl: MAGNITE.boardUrl,
    source: MAGNITE.endpoint,
    fetchedAt: rowFetchedAt,
  });
  normalized.coverage.requests = requests;
  normalized.coverage.limit = MAGNITE.limit;
  normalized.coverage.maxPages = MAGNITE.maxPages;
  normalized.coverage.searchText = "";
  normalized.coverage.handoff = "confirmed";
  normalized.coverage.tenant = MAGNITE.tenant;
  normalized.coverage.siteId = MAGNITE.siteId;
  normalized.coverage.hostnameLabel = MAGNITE.hostnameLabel;
  normalized.coverage.stopReason = collected.stopReason;
  return { kind: "observation", rows: normalized.rows, coverage: normalized.coverage };
}
