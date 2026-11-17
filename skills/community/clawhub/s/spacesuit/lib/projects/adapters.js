const { redactExtensionText } = require("../flavors/redaction");
const STAGES = new Set([
  "inbox",
  "planned",
  "doing",
  "review",
  "done",
  "canceled",
  "unknown",
]);
const ID = /^[a-z][a-z0-9-]{0,63}$/;
const fail = (code) => {
  throw Object.assign(new Error(code), { code: `PROJECT_${code}` });
};
const text = (v, n = 256) =>
  redactExtensionText(typeof v === "string" ? v : "").slice(0, n);
const date = (v) =>
  typeof v === "string" && Number.isFinite(Date.parse(v))
    ? new Date(v).toISOString()
    : null;
function url(v) {
  try {
    const u = new URL(v);
    return u.protocol === "https:" &&
      !u.username &&
      !u.password &&
      !u.search &&
      !u.hash
      ? u.href
      : null;
  } catch {
    return null;
  }
}
function validateSource(source) {
  if (
    !source ||
    typeof source.id !== "string" ||
    !ID.test(source.id) ||
    !["linear", "jira"].includes(source.provider) ||
    typeof source.label !== "string" ||
    source.label.length > 256 ||
    typeof source.enabled !== "boolean"
  )
    fail("INVALID_SOURCE");
  if (source.statusMap !== undefined) {
    if (
      !source.statusMap ||
      typeof source.statusMap !== "object" ||
      Array.isArray(source.statusMap) ||
      Object.keys(source.statusMap).length > 100
    )
      fail("INVALID_MAPPING");
    for (const [key, value] of Object.entries(source.statusMap))
      if (!key || key.length > 128 || !STAGES.has(value))
        fail("INVALID_MAPPING");
  }
  if (
    source.provider === "jira" &&
    (!Array.isArray(source.jiraEpicTypeIds) ||
      !source.jiraEpicTypeIds.length ||
      source.jiraEpicTypeIds.length > 20 ||
      source.jiraEpicTypeIds.some(
        (id) => typeof id !== "string" || !/^\d{1,20}$/.test(id),
      ))
  )
    fail("EPIC_TYPES_REQUIRED");
  if (
    source.links !== undefined &&
    (!source.links ||
      typeof source.links !== "object" ||
      Array.isArray(source.links) ||
      Object.keys(source.links).length > 200)
  )
    fail("INVALID_LINKS");
  return source;
}
function stage(source, id, category) {
  if (source.statusMap && Object.hasOwn(source.statusMap, id))
    return source.statusMap[id];
  const types =
    source.provider === "linear"
      ? {
          backlog: "inbox",
          planned: "planned",
          started: "doing",
          paused: "unknown",
          completed: "done",
          canceled: "canceled",
        }
      : { new: "inbox", indeterminate: "doing", done: "done" };
  return Object.hasOwn(types, category) ? types[category] : "unknown";
}
function associations(source, id) {
  const value =
    source.links && Object.hasOwn(source.links, id) ? source.links[id] : {};
  if (!value || typeof value !== "object") fail("INVALID_LINKS");
  const result = {};
  for (const field of ["agents", "sessionKeys"]) {
    const a = value[field] ?? [];
    if (
      !Array.isArray(a) ||
      a.length > 20 ||
      a.some((v) => typeof v !== "string" || !v || v.length > 256)
    )
      fail("INVALID_LINKS");
    result[field] = a.map((v) => text(v));
  }
  result.dependencies = value.dependencies ?? [];
  if (
    !Array.isArray(result.dependencies) ||
    result.dependencies.length > 20 ||
    result.dependencies.some(
      (d) =>
        !d ||
        typeof d.sourceId !== "string" ||
        !ID.test(d.sourceId) ||
        typeof d.projectId !== "string" ||
        !d.projectId ||
        d.projectId.length > 128,
    )
  )
    fail("INVALID_LINKS");
  result.dependencies = result.dependencies.map((d) => ({
    sourceId: d.sourceId,
    projectId: d.projectId,
  }));
  return result;
}
function project(source, raw) {
  const linear = source.provider === "linear";
  const f = linear ? raw : raw.fields;
  if (
    !raw ||
    !f ||
    typeof raw.id !== "string" ||
    !raw.id ||
    raw.id.length > 128
  )
    fail("INVALID_PROJECT");
  if (!linear && !source.jiraEpicTypeIds.includes(String(f.issuetype?.id)))
    return null;
  const title = linear ? raw.name : f.summary;
  if (typeof title !== "string" || !title.trim()) fail("INVALID_PROJECT");
  const state = linear ? raw.status : f.status;
  const nativeStatus = text(state?.name);
  const statusId = String(state?.id ?? "");
  let href = linear ? url(raw.url) : null;
  if (
    !linear &&
    source.jiraBaseUrl &&
    /^[A-Za-z][A-Za-z0-9_]*-\d+$/.test(raw.key)
  ) {
    const base = url(source.jiraBaseUrl);
    if (base)
      href = new URL(
        `browse/${raw.key}`,
        base.endsWith("/") ? base : `${base}/`,
      ).href;
  }
  const due = linear ? raw.targetDate : f.duedate;
  const targetDate =
    typeof due === "string" &&
    /^\d{4}-\d{2}-\d{2}$/.test(due) &&
    date(due)?.slice(0, 10) === due
      ? due
      : null;
  return {
    id: raw.id,
    title: text(title),
    url: href,
    kind: linear ? "project" : "epic",
    stage: stage(
      source,
      statusId,
      linear ? state?.type : state?.statusCategory?.key,
    ),
    nativeStatus,
    nativeStatusId: statusId && statusId.length <= 128 ? statusId : null,
    health: "unknown",
    owner: text(linear ? raw.lead?.name : f.assignee?.displayName) || null,
    // Jira ADF is intentionally not guessed into a plain-text summary.
    summary: text(linear ? raw.description : f.description, 2048),
    updatedAt: date(linear ? raw.updatedAt : f.updated),
    targetDate,
    counts: { total: null, done: null, blocked: null },
    ...associations(source, raw.id),
  };
}
const LINEAR_QUERY = `query ProjectPortfolio($after: String, $first: Int!) {
  projects(first: $first, after: $after) {
    nodes { id name url description updatedAt targetDate lead { name } status { id name type } }
    pageInfo { hasNextPage endCursor }
  }
}`;
function parsePage(source, response) {
  if (source.provider === "linear") {
    if (response?.errors?.length) fail("PROVIDER_ERROR");
    const connection = response?.data?.projects;
    if (
      !Array.isArray(connection?.nodes) ||
      typeof connection.pageInfo?.hasNextPage !== "boolean"
    )
      fail("INVALID_RESPONSE");
    return {
      nodes: connection.nodes,
      next: connection.pageInfo.hasNextPage
        ? connection.pageInfo.endCursor
        : null,
      more: connection.pageInfo.hasNextPage,
    };
  }
  if (!Array.isArray(response?.issues) || typeof response.isLast !== "boolean")
    fail("INVALID_RESPONSE");
  return {
    nodes: response.issues,
    more: !response.isLast,
    next: response.isLast ? null : response.nextPageToken,
  };
}
async function collect({
  source,
  profile = "",
  agentId = "main",
  request,
  observedAt = new Date().toISOString(),
  maxPages = 10,
  maxProjects = 200,
  timeoutMs = 10000,
}) {
  validateSource(source);
  if (
    typeof profile !== "string" ||
    !/^[a-zA-Z0-9_-]{0,64}$/.test(profile) ||
    typeof agentId !== "string" ||
    !/^[a-zA-Z0-9_-]{1,64}$/.test(agentId) ||
    !source.enabled ||
    typeof request !== "function" ||
    !date(observedAt) ||
    !Number.isInteger(maxPages) ||
    maxPages < 1 ||
    maxPages > 20 ||
    !Number.isInteger(maxProjects) ||
    maxProjects < 1 ||
    maxProjects > 200 ||
    !Number.isInteger(timeoutMs) ||
    timeoutMs < 1 ||
    timeoutMs > 30000
  )
    fail("INVALID_OPTIONS");
  const snapshot = {
    schemaVersion: 1,
    sourceId: source.id,
    provider: source.provider,
    profile,
    agentId,
    observedAt: date(observedAt),
    status: "ready",
    projects: [],
  };
  const seen = new Set(),
    cursors = new Set();
  let cursor = null;
  const controller = new AbortController();
  let timer;
  const expiry = new Promise((_, reject) => {
    timer = setTimeout(() => {
      controller.abort();
      reject(new Error("deadline"));
    }, timeoutMs);
  });
  try {
    for (let page = 0; page < maxPages; page++) {
      const descriptor =
        source.provider === "linear"
          ? {
              provider: "linear",
              method: "POST",
              path: "/graphql",
              query: LINEAR_QUERY,
              variables: { after: cursor, first: 50 },
              signal: controller.signal,
            }
          : {
              provider: "jira",
              method: "GET",
              path: "/rest/api/3/search/jql",
              params: {
                jql:
                  source.jql ||
                  `issuetype in (${source.jiraEpicTypeIds.join(",")}) ORDER BY updated DESC`,
                fields:
                  "summary,status,issuetype,assignee,description,updated,duedate",
                maxResults: 50,
                ...(cursor ? { nextPageToken: cursor } : {}),
              },
              signal: controller.signal,
            };
      const response = await Promise.race([
        Promise.resolve().then(() => request(descriptor)),
        expiry,
      ]);
      if (Buffer.byteLength(JSON.stringify(response)) > 1024 * 1024)
        fail("RESPONSE_LIMIT");
      const parsed = parsePage(source, response);
      if (parsed.nodes.length > 200) fail("RESPONSE_LIMIT");
      for (const raw of parsed.nodes) {
        const p = project(source, raw);
        if (!p) continue;
        if (seen.has(p.id)) fail("DUPLICATE_ID");
        if (snapshot.projects.length >= maxProjects) {
          snapshot.status = "partial";
          return snapshot;
        }
        seen.add(p.id);
        snapshot.projects.push(p);
      }
      if (!parsed.more) return snapshot;
      if (snapshot.projects.length >= maxProjects) {
        snapshot.status = "partial";
        return snapshot;
      }
      if (
        typeof parsed.next !== "string" ||
        !parsed.next ||
        parsed.next.length > 2048 ||
        cursors.has(parsed.next)
      )
        fail("INVALID_CURSOR");
      cursors.add(parsed.next);
      cursor = parsed.next;
    }
    snapshot.status = "partial";
  } catch {
    snapshot.status = snapshot.projects.length ? "partial" : "error";
  } finally {
    clearTimeout(timer);
    controller.abort();
  }
  return snapshot;
}
// Only retain known, bounded contract fields from a previously stored snapshot.
function retainedProjects(value) {
  if (
    !value ||
    value.schemaVersion !== 1 ||
    !date(value.observedAt) ||
    !Array.isArray(value.projects) ||
    value.projects.length > 200
  )
    fail("INVALID_PREVIOUS");
  const ids = new Set();
  return value.projects.map((p) => {
    if (
      !p ||
      typeof p.id !== "string" ||
      !p.id ||
      p.id.length > 128 ||
      ids.has(p.id) ||
      !STAGES.has(p.stage) ||
      !["project", "epic", "milestone"].includes(p.kind) ||
      !["on-track", "at-risk", "blocked", "off-track", "unknown"].includes(
        p.health,
      )
    )
      fail("INVALID_PREVIOUS");
    ids.add(p.id);
    for (const field of ["title", "nativeStatus", "summary"])
      if (
        typeof p[field] !== "string" ||
        p[field].length > (field === "summary" ? 2048 : 256)
      )
        fail("INVALID_PREVIOUS");
    if (
      !p.title ||
      (p.owner !== null &&
        (typeof p.owner !== "string" || p.owner.length > 256)) ||
      (p.nativeStatusId != null &&
        (typeof p.nativeStatusId !== "string" ||
          p.nativeStatusId.length > 128)) ||
      (p.url !== null && !url(p.url)) ||
      (p.updatedAt !== null && !date(p.updatedAt)) ||
      (p.targetDate !== null &&
        (!/^\d{4}-\d{2}-\d{2}$/.test(p.targetDate) ||
          date(p.targetDate)?.slice(0, 10) !== p.targetDate))
    )
      fail("INVALID_PREVIOUS");
    const counts = {};
    for (const key of ["total", "done", "blocked"]) {
      const n = p.counts?.[key];
      if (n !== null && (!Number.isSafeInteger(n) || n < 0))
        fail("INVALID_PREVIOUS");
      counts[key] = n;
    }
    if (
      counts.total !== null &&
      [counts.done, counts.blocked].some((n) => n !== null && n > counts.total)
    )
      fail("INVALID_PREVIOUS");
    return {
      id: p.id,
      title: text(p.title),
      url: p.url,
      kind: p.kind,
      stage: p.stage,
      nativeStatus: text(p.nativeStatus),
      nativeStatusId: p.nativeStatusId ?? null,
      health: p.health,
      owner: p.owner === null ? null : text(p.owner),
      summary: text(p.summary, 2048),
      updatedAt: p.updatedAt,
      targetDate: p.targetDate,
      counts,
      ...associations({ links: { [p.id]: p } }, p.id),
    };
  });
}
module.exports = {
  collect,
  project,
  validateSource,
  retainedProjects,
  fail,
  text,
  date,
};
