// Gist a8f74ed84b4ece624209be1dab745a30
// revision 7d01bfb09c530430933dec1f07c5c0b8517cffa8
// Local delta: requestJson accepts optional fetchImpl and maxBytes (default 1000000).
import { writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));

export const USER_AGENT = "SameDayDesk-careers-trial (https://samedaydesk.com)";

const ALLOWED_HOSTS = new Set([
  "acxiomllc.wd5.myworkdayjobs.com",
  "api.ashbyhq.com",
  "liveramp.wd5.myworkdayjobs.com",
]);

export const BOARDS = {
  acxiom: {
    company: "Acxiom",
    careersPage: "https://www.acxiom.com/careers/",
    boardUrl: "https://acxiomllc.wd5.myworkdayjobs.com/en-US/AcxiomUSA",
    endpoint: "https://acxiomllc.wd5.myworkdayjobs.com/wday/cxs/acxiomllc/AcxiomUSA/jobs",
    method: "POST",
  },
  liverampAshby: {
    company: "LiveRamp",
    careersPage: "https://liveramp.com/careers",
    boardUrl: "https://jobs.ashbyhq.com/liveramp-inc",
    endpoint: "https://api.ashbyhq.com/posting-api/job-board/liveramp-inc",
    method: "GET",
  },
  liverampWorkday: {
    company: "LiveRamp",
    boardUrl: "https://liveramp.wd5.myworkdayjobs.com/en-US/LiveRampCareers",
    endpoint: "https://liveramp.wd5.myworkdayjobs.com/wday/cxs/liveramp/LiveRampCareers/jobs",
    method: "POST",
  },
};

export function gateRequest(url) {
  let host = null;
  try {
    const parsed = new URL(url);
    host = parsed.host;
    if (parsed.protocol !== "https:" || parsed.username || parsed.password) {
      return { ok: false, status: "wrong_host", host };
    }
  } catch {
    return { ok: false, status: "wrong_host", host };
  }
  if (!ALLOWED_HOSTS.has(host)) return { ok: false, status: "wrong_host", host };
  return { ok: true, status: "allowed", host };
}

export function assessCompletenessClaim(claim) {
  if (!claim || typeof claim !== "object") {
    return { accepted: false, reason: "claim is not an object" };
  }
  if ("paidMarginalValue" in claim || "willingToPay" in claim || "marketVerdict" in claim) {
    return { accepted: false, reason: "a pricing flag is not an output check" };
  }
  if (claim.claim === "source_failure_is_an_empty_board") {
    return { accepted: false, reason: "a source failure is not an empty board" };
  }
  if (claim.claim === "page_one_is_the_full_board") {
    const { pageLength, declaredTotal, uniqueRows } = claim;
    if (typeof declaredTotal !== "number" || typeof pageLength !== "number") {
      return { accepted: false, reason: "completeness claim is missing counts" };
    }
    if (declaredTotal > pageLength) {
      return { accepted: false, reason: "first page is shorter than the declared total" };
    }
    if (typeof uniqueRows === "number" && uniqueRows < declaredTotal) {
      return { accepted: false, reason: "unique rows are below the declared total" };
    }
    if (pageLength === declaredTotal && uniqueRows === declaredTotal) {
      return { accepted: true, reason: "the single page matches the declared total" };
    }
    return { accepted: false, reason: "completeness is not shown" };
  }
  return { accepted: false, reason: "unrecognized claim" };
}

function sourceFailure(httpStatus, body) {
  return {
    rows: [],
    coverage: {
      status: "source_failure",
      emptyBoard: false,
      httpStatus: httpStatus ?? 0,
      errorCode: body && typeof body.errorCode === "string" ? body.errorCode : null,
      message: body && typeof body.message === "string" ? body.message : null,
      declaredTotal: null,
      remaining: null,
      roleFilter: null,
    },
  };
}

function wrongSchema(httpStatus) {
  return {
    rows: [],
    coverage: {
      status: "wrong_schema",
      emptyBoard: false,
      httpStatus,
      declaredTotal: null,
      remaining: null,
      roleFilter: null,
    },
  };
}

function workdayUrl(boardUrl, externalPath) {
  return `${boardUrl.replace(/\/$/, "")}${externalPath}`;
}

function readWorkdayJob(job) {
  const title = typeof job?.title === "string" ? job.title.trim() : "";
  const externalPath = typeof job?.externalPath === "string" ? job.externalPath.trim() : "";
  const locationRaw = typeof job?.locationsText === "string" ? job.locationsText.trim() : "";
  if (!title || !externalPath.startsWith("/job/")) {
    let reason = "missing_externalPath";
    if (!title && !externalPath) reason = "missing_title_and_externalPath";
    else if (!title) reason = "missing_title";
    return {
      ok: false,
      missing: {
        title: title || null,
        externalPath: externalPath || null,
        bulletFields: Array.isArray(job?.bulletFields) ? job.bulletFields : null,
        reason,
      },
    };
  }
  return { ok: true, title, externalPath, location: locationRaw || null };
}

// Later Workday pages in this study returned total 0 while still listing jobs.
// An offset at or past the first-page total repeated page 1, so an empty page
// is not the end signal. Only the offset-0 total is the declared count.
export function normalizeWorkday(input, ctx) {
  const pages = Array.isArray(input?.pages) ? input.pages : [];
  const first = pages[0];
  if (!first) return sourceFailure(0, null);
  if (first.httpStatus !== 200) return sourceFailure(first.httpStatus, first.body);
  if (!first.body || !Array.isArray(first.body.jobPostings) || !Number.isInteger(first.body.total) || first.body.total < 0 || first.offset !== 0) {
    return wrongSchema(first.httpStatus);
  }

  const declaredTotal = first.body.total;
  const seen = new Set();
  const rows = [];
  const missing = [];
  let duplicateCount = 0;
  let locationMissing = 0;
  let laterPageTotalUnreliable = false;
  let stoppedOnRepeat = false;

  const take = (postings, offset, { countDuplicates }) => {
    let added = 0;
    for (const job of postings) {
      const parsed = readWorkdayJob(job);
      if (!parsed.ok) {
        missing.push({ offset, ...parsed.missing });
        continue;
      }
      const url = workdayUrl(ctx.boardUrl, parsed.externalPath);
      if (seen.has(url)) {
        if (countDuplicates) duplicateCount += 1;
        continue;
      }
      seen.add(url);
      if (parsed.location === null) locationMissing += 1;
      rows.push({
        title: parsed.title,
        location: parsed.location,
        url,
        source: ctx.source,
        fetchedAt: ctx.fetchedAt,
      });
      added += 1;
    }
    return added;
  };

  for (const page of pages) {
    if (page !== first && page.httpStatus !== 200) {
      return {
        rows,
        coverage: {
          status: "partial",
          emptyBoard: false,
          httpStatus: page.httpStatus,
          declaredTotal,
          firstPageCount: first.body.jobPostings.length,
          uniqueRows: rows.length,
          remaining: declaredTotal > rows.length ? declaredTotal - rows.length : null,
          duplicateCount,
          missing,
          locationMissing,
          laterPageTotalUnreliable,
          roleFilter: null,
          note: "a later page failed and the rows above are only what was read",
        },
      };
    }
    if (!page.body || !Array.isArray(page.body.jobPostings)) {
      return {
        rows,
        coverage: {
          status: "partial", emptyBoard: false, httpStatus: page.httpStatus,
          declaredTotal, firstPageCount: first.body.jobPostings.length,
          uniqueRows: rows.length,
          remaining: declaredTotal > rows.length ? declaredTotal - rows.length : null,
          duplicateCount, missing, locationMissing, laterPageTotalUnreliable,
          roleFilter: null, note: "a later page has the wrong schema; prior rows are retained",
        },
      };
    }
    if (page.offset > 0 && page.body.total === 0 && page.body.jobPostings.length > 0) {
      laterPageTotalUnreliable = true;
    }
    const freshUrls = [];
    for (const job of page.body.jobPostings) {
      const parsed = readWorkdayJob(job);
      if (!parsed.ok) continue;
      freshUrls.push(workdayUrl(ctx.boardUrl, parsed.externalPath));
    }
    if (page.offset > 0 && freshUrls.length > 0 && freshUrls.every((url) => seen.has(url))) {
      stoppedOnRepeat = true;
      break;
    }
    take(page.body.jobPostings, page.offset, { countDuplicates: true });
  }

  let status;
  if (declaredTotal === 0 && rows.length === 0 && missing.length === 0) status = "empty_board";
  else if (declaredTotal === 0) status = "partial_inconsistent_total";
  else if (rows.length === declaredTotal && missing.length === 0) status = "complete_for_declared_total";
  else status = "partial";

  const coverage = {
    status,
    emptyBoard: status === "empty_board",
    httpStatus: 200,
    declaredTotal,
    firstPageCount: first.body.jobPostings.length,
    uniqueRows: rows.length,
    remaining: status === "complete_for_declared_total"
      ? 0
      : (declaredTotal > rows.length ? declaredTotal - rows.length : null),
    duplicateCount,
    missing,
    locationMissing,
    laterPageTotalUnreliable,
    stoppedOnRepeat,
    pagesRead: pages.length,
    roleFilter: null,
    pastEnd: null,
  };

  const probe = input?.probe;
  if (probe) {
    if (probe.httpStatus !== 200 || !probe.body || !Array.isArray(probe.body.jobPostings)) {
      coverage.pastEnd = { confirmed: false, httpStatus: probe.httpStatus ?? 0 };
    } else if (probe.body.jobPostings.length === 0) {
      coverage.pastEnd = { confirmed: true, behavior: "empty", rowsAdded: 0 };
    } else {
      const missingBeforeProbe = missing.length;
      const added = take(probe.body.jobPostings, probe.offset ?? declaredTotal, { countDuplicates: false });
      const unreadable = missing.length - missingBeforeProbe;
      if (added === 0 && unreadable > 0) {
        coverage.status = "partial_past_end_incomplete";
        coverage.emptyBoard = false;
        coverage.remaining = null;
        coverage.pastEnd = { confirmed: false, behavior: "unreadable_rows", rowsAdded: 0, unreadableRows: unreadable };
      } else if (added === 0) {
        coverage.pastEnd = { confirmed: true, behavior: "repeated_prior_paths", rowsAdded: 0 };
      } else {
        coverage.status = "partial_past_end_grew";
        coverage.emptyBoard = false;
        coverage.uniqueRows = rows.length;
        coverage.remaining = null;
        coverage.pastEnd = { confirmed: false, behavior: "new_rows", rowsAdded: added };
      }
    }
  }

  return { rows, coverage };
}

export function normalizeAshby(input, ctx) {
  if (!input || input.httpStatus !== 200) return sourceFailure(input?.httpStatus, input?.body);
  if (!input.body || !Array.isArray(input.body.jobs)) return wrongSchema(input.httpStatus);

  const seen = new Set();
  const rows = [];
  const missing = [];
  let duplicateCount = 0;
  let unlistedWithheld = 0;
  let locationMissing = 0;

  for (const job of input.body.jobs) {
    if (typeof job?.isListed !== "boolean") {
      missing.push({ reason: "missing_isListed" });
      continue;
    }
    if (job?.isListed === false) {
      unlistedWithheld += 1;
      continue;
    }
    const title = typeof job?.title === "string" ? job.title.trim() : "";
    const jobUrl = typeof job?.jobUrl === "string" ? job.jobUrl.trim() : "";
    const applyUrl = typeof job?.applyUrl === "string" ? job.applyUrl.trim() : "";
    const board = new URL(ctx.boardUrl || BOARDS.liverampAshby.boardUrl);
    const safePosting = (value) => {
      try {
        const parsed = new URL(value);
        return parsed.protocol === "https:" && !parsed.username && !parsed.password
          && parsed.origin === board.origin
          && parsed.pathname.startsWith(`${board.pathname.replace(/\/$/, "")}/`)
          ? parsed.href : "";
      } catch { return ""; }
    };
    const url = safePosting(jobUrl) || safePosting(applyUrl);
    const locationRaw = typeof job?.location === "string" ? job.location.trim() : "";
    if (!title || !url) {
      missing.push({ title: title || null, reason: !title ? "missing_title" : "missing_url" });
      continue;
    }
    if (seen.has(url)) {
      duplicateCount += 1;
      continue;
    }
    seen.add(url);
    if (!locationRaw) locationMissing += 1;
    rows.push({
      title,
      location: locationRaw || null,
      url,
      source: ctx.source,
      fetchedAt: ctx.fetchedAt,
    });
  }

  const returned = input.body.jobs.length;
  let status = "complete_for_returned_listed_set";
  if (missing.length > 0) status = "partial";
  const listedSetEmpty = rows.length === 0;
  return {
    rows,
    coverage: {
      status,
      emptyBoard: returned === 0,
      listedSetEmpty,
      httpStatus: 200,
      separateTotalField: false,
      returned,
      uniqueRows: rows.length,
      unlistedWithheld,
      duplicateCount,
      missing,
      locationMissing,
      remaining: null,
      remainingMeaning: "This API returns one jobs array and no separate total. The rows are that response after the listed-row rules. They are not a count of every role on another system.",
      roleFilter: null,
    },
  };
}

async function requestJson(url, { method, payload, timeoutMs, fetchImpl, maxBytes } = {}) {
  const gate = gateRequest(url);
  const started = Date.now();
  if (!gate.ok) {
    return { url, method, httpStatus: 0, body: null, elapsedMs: 0, bytes: 0, error: "wrong_host" };
  }
  const cap = Number.isInteger(maxBytes) && maxBytes > 0 ? maxBytes : 1_000_000;
  const fetchFn = typeof fetchImpl === "function" ? fetchImpl : fetch;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  let reader;
  let onAbort;
  try {
    const headers = { accept: "application/json", "user-agent": USER_AGENT };
    if (payload !== undefined) headers["content-type"] = "application/json";
    const response = await fetchFn(url, {
      method,
      redirect: "manual",
      headers,
      body: payload === undefined ? undefined : JSON.stringify(payload),
      signal: controller.signal,
    });
    // Bound raw bytes before decoding or parsing, including a stalled body.
    // Never fall back to response.text(), which buffers the entire response.
    reader = response.body?.getReader();
    const chunks = [];
    let bytes = 0;
    if (reader) {
      const aborted = new Promise((resolve, reject) => {
        onAbort = () => {
          reject(new DOMException("request timed out", "AbortError"));
          void reader.cancel("request aborted").catch(() => {});
        };
        controller.signal.addEventListener("abort", onAbort, { once: true });
      });
      if (controller.signal.aborted) onAbort();
      while (true) {
        const { done, value } = await Promise.race([reader.read(), aborted]);
        if (done) break;
        bytes += value.byteLength;
        if (bytes > cap) {
          controller.abort();
          return {
            url, method, httpStatus: response.status, body: null,
            elapsedMs: Date.now() - started, bytes, error: "response_too_large",
          };
        }
        chunks.push(value);
      }
    }
    const raw = new Uint8Array(bytes);
    let offset = 0;
    for (const chunk of chunks) {
      raw.set(chunk, offset);
      offset += chunk.byteLength;
    }
    const text = new TextDecoder().decode(raw);
    let body = null;
    try {
      body = JSON.parse(text);
    } catch {
      body = null;
    }
    return {
      url,
      method,
      httpStatus: response.status,
      body,
      elapsedMs: Date.now() - started,
      bytes,
      error: null,
    };
  } catch (error) {
    return {
      url,
      method,
      httpStatus: 0,
      body: null,
      elapsedMs: Date.now() - started,
      bytes: 0,
      error: error?.name === "AbortError" ? "timeout" : "network",
    };
  } finally {
    clearTimeout(timer);
    if (onAbort) controller.signal.removeEventListener("abort", onAbort);
    if (reader) reader.releaseLock();
  }
}

function requestLog(entry, extra = {}) {
  return {
    method: entry.method,
    url: entry.url,
    httpStatus: entry.httpStatus,
    elapsedMs: entry.elapsedMs,
    bytes: entry.bytes,
    error: entry.error,
    ...extra,
  };
}

export async function fetchAcxiom(ctx, options = {}) {
  const timeoutMs = options.timeoutMs ?? 15000;
  const deadline = Date.now() + timeoutMs;
  const limit = 20;
  const maxPages = options.maxPages ?? 4;
  const endpoint = BOARDS.acxiom.endpoint;
  const pages = [];
  const requests = [];

  const load = async (offset) => {
    const remainingMs = deadline - Date.now();
    const entry = remainingMs <= 0 ? {
      url: endpoint, method: "POST", httpStatus: 0, body: null,
      elapsedMs: 0, bytes: 0, error: "timeout",
    } : await requestJson(endpoint, {
      method: "POST",
      payload: { appliedFacets: {}, limit, offset, searchText: "" },
      timeoutMs: remainingMs,
      fetchImpl: options.fetchImpl,
      maxBytes: options.maxBytes,
    });
    requests.push(requestLog(entry, { offset }));
    return { offset, httpStatus: entry.httpStatus, body: entry.body, error: entry.error };
  };

  const first = await load(0);
  pages.push(first);
  let probe = null;
  const declared = first.body?.total;
  if (first.httpStatus === 200 && Number.isInteger(declared) && declared > 0 && Array.isArray(first.body?.jobPostings)) {
    let offset = first.body.jobPostings.length;
    const seen = new Set(first.body.jobPostings.map((job) => job?.externalPath).filter(Boolean));
    while (offset > 0 && offset < declared && pages.length < maxPages) {
      const page = await load(offset);
      const postings = page.body?.jobPostings;
      if (page.httpStatus !== 200 || !Array.isArray(postings) || postings.length === 0) {
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
    if (!probe && pages.length < maxPages && offset >= declared) {
      probe = await load(declared);
    }
  }

  const normalized = normalizeWorkday({ pages, probe }, ctx);
  normalized.coverage.requests = requests;
  normalized.coverage.limit = limit;
  normalized.coverage.maxPages = maxPages;
  return normalized;
}

export async function fetchAshby(ctx, options = {}) {
  const entry = await requestJson(BOARDS.liverampAshby.endpoint, {
    method: "GET",
    timeoutMs: options.timeoutMs ?? 15000,
    fetchImpl: options.fetchImpl,
    maxBytes: options.maxBytes,
  });
  const normalized = normalizeAshby(entry, ctx);
  normalized.coverage.requests = [requestLog(entry)];
  return normalized;
}

export async function fetchLiveRampWorkday(ctx, options = {}) {
  const entry = await requestJson(BOARDS.liverampWorkday.endpoint, {
    method: "POST",
    payload: { appliedFacets: {}, limit: 20, offset: 0, searchText: "" },
    timeoutMs: options.timeoutMs ?? 15000,
    fetchImpl: options.fetchImpl,
    maxBytes: options.maxBytes,
  });
  const normalized = normalizeWorkday({
    pages: [{ offset: 0, httpStatus: entry.httpStatus, body: entry.body }],
  }, ctx);
  normalized.coverage.requests = [requestLog(entry, { offset: 0 })];
  return normalized;
}

export async function buildLiveEvidence() {
  const fetchedAt = new Date().toISOString();
  const acxiomCtx = {
    boardUrl: BOARDS.acxiom.boardUrl,
    source: BOARDS.acxiom.endpoint,
    fetchedAt,
  };
  const ashbyCtx = {
    boardUrl: BOARDS.liverampAshby.boardUrl,
    source: BOARDS.liverampAshby.endpoint,
    fetchedAt,
  };
  const workdayCtx = {
    boardUrl: BOARDS.liverampWorkday.boardUrl,
    source: BOARDS.liverampWorkday.endpoint,
    fetchedAt,
  };
  const [acxiom, liverampAshby, liverampWorkday] = await Promise.all([
    fetchAcxiom(acxiomCtx),
    fetchAshby(ashbyCtx),
    fetchLiveRampWorkday(workdayCtx),
  ]);
  return {
    task: "https://github.com/firecrawl/firecrawl/issues/3552",
    roleFilter: null,
    cashSpent: 0,
    fetchedAt,
    inputs: {
      acxiomCareersPage: BOARDS.acxiom.careersPage,
      acxiomBoard: BOARDS.acxiom.boardUrl,
      liverampCareersPage: BOARDS.liverampAshby.careersPage,
      liverampPrimaryJobsPage: BOARDS.liverampAshby.boardUrl,
      liverampWorkdayBoard: BOARDS.liverampWorkday.boardUrl,
    },
    acxiom,
    liverampAshby,
    liverampWorkday,
  };
}

export function summarizeEvidence(evidence) {
  const brief = (part) => ({
    status: part.coverage.status,
    emptyBoard: part.coverage.emptyBoard,
    uniqueRows: part.coverage.uniqueRows ?? part.rows.length,
    declaredTotal: part.coverage.declaredTotal ?? null,
    remaining: part.coverage.remaining ?? null,
    httpStatus: part.coverage.httpStatus ?? null,
    sample: part.rows[0] ?? null,
  });
  return {
    fetchedAt: evidence.fetchedAt,
    cashSpent: evidence.cashSpent,
    roleFilter: evidence.roleFilter,
    acxiom: brief(evidence.acxiom),
    liverampAshby: brief(evidence.liverampAshby),
    liverampWorkday: brief(evidence.liverampWorkday),
  };
}

async function cli() {
  const evidence = await buildLiveEvidence();
  if (process.argv.includes("--stdout")) {
    console.log(JSON.stringify(evidence));
    return;
  }
  const out = resolve(root, "evidence/boards-live.json");
  writeFileSync(out, `${JSON.stringify(evidence, null, 2)}\n`);
  console.log(JSON.stringify(summarizeEvidence(evidence)));
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  cli().catch((error) => {
    console.error(error?.name || "live-fetch-failed");
    process.exit(1);
  });
}
