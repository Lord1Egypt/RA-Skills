const { redactExtensionText } = require("../flavors/redaction");
const fail = () => {
  throw new Error("WORK_GRAPH_INVALID_INPUT");
};
const arr = (v, n) => {
  if (!Array.isArray(v) || v.length > n) fail();
  return v;
};
const id = (v) => {
  if (
    typeof v !== "string" ||
    !v ||
    v.length > 256 ||
    /[\x00-\x1f]/.test(v) ||
    redactExtensionText(v) !== v
  )
    fail();
  return v;
};
const text = (v, n = 256) =>
  redactExtensionText(typeof v === "string" ? v : "").slice(0, n);
const instant = (v) => {
  if (
    typeof v !== "string" ||
    !/^\d{4}-\d\d-\d\dT/.test(v) ||
    !Number.isFinite(Date.parse(v)) ||
    new Date(v).toISOString().slice(0, 10) !== v.slice(0, 10)
  )
    fail();
  return new Date(v).toISOString();
};
const key = (source, kind, native) =>
  [id(source), kind, id(native)].map(encodeURIComponent).join(":");
const roles = [
  "frontend",
  "backend",
  "infra",
  "qa",
  "architecture",
  "copywriting",
  "legal",
];
const cues = {
  frontend: /\b(frontend|css|component|layout)\b/i,
  backend: /\b(backend|endpoint|database|migration)\b/i,
  infra: /\b(infrastructure|terraform|kubernetes|deploy)\b/i,
  qa: /\b(qa|regression|verification|testing)\b/i,
  architecture: /\b(architecture|system design|adr)\b/i,
  copywriting: /\b(copywriting|copy|wording)\b/i,
  legal: /\b(legal|contract|licensing)\b/i,
};
const stage = (source, raw) => {
  const native = String(raw?.id ?? "");
  const mapped = source.statusMap?.[native];
  if (
    mapped &&
    ["planned", "doing", "review", "done", "canceled", "unknown"].includes(
      mapped,
    )
  )
    return mapped;
  const category =
    source.provider === "linear" ? raw?.type : raw?.statusCategory?.key;
  const stages =
    source.provider === "linear"
      ? {
          backlog: "planned",
          unstarted: "planned",
          started: "doing",
          completed: "done",
          canceled: "canceled",
        }
      : { new: "planned", indeterminate: "doing", done: "done" };
  return Object.hasOwn(stages, category) ? stages[category] : "unknown";
};
/** Compile reviewed exports and runtime records; no provider calls or execution authority. */
function compile(input) {
  if (
    !input ||
    input.schemaVersion !== 1 ||
    typeof input.profile !== "string" ||
    !/^[\w-]{0,64}$/.test(input.profile)
  )
    fail();
  const agentId = id(input.agentId),
    observedAt = instant(input.observedAt);
  const sources = arr(input.sources, 8),
    nodes = new Map(),
    edges = [],
    edgeIds = new Set(),
    warnings = [];
  const sourceIds = new Set(),
    issueRecords = [],
    runRecords = [];
  function node(n) {
    if (nodes.has(n.id)) fail();
    nodes.set(n.id, n);
    return n.id;
  }
  function auxiliary(kind, name, sourceId = "shared") {
    const k = key(sourceId, kind, name);
    if (!nodes.has(k))
      node({
        id: k,
        sourceId,
        kind,
        title: text(name),
        state: "unknown",
        nativeStatus: "",
        observedAt,
      });
    return k;
  }
  function edge(from, to, relation, basis, evidence) {
    if (!nodes.has(from) || !nodes.has(to)) {
      warnings.push("missing_reference");
      return;
    }
    if (from === to) {
      warnings.push("self_reference");
      return;
    }
    const identity = JSON.stringify([from, to, relation, basis]);
    if (edgeIds.has(identity)) return;
    edgeIds.add(identity);
    edges.push({ from, to, relation, basis, evidence: text(evidence, 512) });
  }
  const declarations = [];
  for (const source of sources) {
    const sid = id(source.id);
    if (sourceIds.has(sid) || !["linear", "jira"].includes(source.provider))
      fail();
    sourceIds.add(sid);
    const when = instant(source.observedAt);
    if (Date.parse(when) > Date.parse(observedAt) + 60000) fail();
    declarations.push({
      id: sid,
      provider: source.provider,
      observedAt: when,
      complete: source.complete === true,
    });
    if (
      source.provider === "jira" &&
      (!Array.isArray(source.epicTypeIds) || !source.epicTypeIds.length)
    )
      fail();
    for (const project of arr(source.projects || [], 100)) {
      if (source.provider !== "linear") fail();
      node({
        id: key(sid, "outcome", project.id),
        sourceId: sid,
        kind: "outcome",
        title: text(project.name) || "Untitled",
        state: stage(source, project.status),
        nativeStatus: text(project.status?.name),
        observedAt: when,
        nativeId: id(project.id),
      });
    }
    for (const raw of arr(source.issues, 500)) {
      const f = source.provider === "linear" ? raw : raw.fields;
      if (!f) fail();
      const kind =
        source.provider === "jira" &&
        source.epicTypeIds.includes(String(f.issuetype?.id))
          ? "outcome"
          : "task";
      const nid = node({
        id: key(sid, kind, raw.id),
        sourceId: sid,
        kind,
        title:
          text(source.provider === "linear" ? f.title : f.summary) ||
          "Untitled",
        state: stage(source, source.provider === "linear" ? f.state : f.status),
        nativeStatus: text(
          (source.provider === "linear" ? f.state : f.status)?.name,
        ),
        observedAt: when,
        nativeId: id(raw.id),
        identifier: text(
          source.provider === "linear" ? raw.identifier : raw.key,
        ),
      });
      issueRecords.push({ source, raw, f, kind, nid });
    }
  }
  for (const { source, raw, f, kind, nid } of issueRecords) {
    const sid = source.id;
    const parent = source.provider === "linear" ? raw.parent : f.parent;
    if (kind === "task" && parent?.id) {
      const parentTask = key(sid, "task", parent.id),
        parentOutcome = key(sid, "outcome", parent.id);
      edge(
        nodes.has(parentTask) ? parentTask : parentOutcome,
        nid,
        "contains",
        "observed",
        "Provider parent reference",
      );
    } else if (
      kind === "task" &&
      source.provider === "linear" &&
      raw.project?.id
    )
      edge(
        key(sid, "outcome", raw.project.id),
        nid,
        "contains",
        "observed",
        "Provider project reference",
      );
    if (kind !== "task") continue;
    const labels =
      source.provider === "linear"
        ? (raw.labels?.nodes || []).map((x) => x.name)
        : f.labels || [];
    for (const value of arr(labels, 30)) {
      const label = text(value);
      if (!label) continue;
      const role = label.match(
        /^role:(frontend|backend|infra|qa|architecture|copywriting|legal)$/i,
      );
      if (role)
        edge(
          nid,
          auxiliary("role", role[1].toLowerCase()),
          "role",
          "observed",
          "Explicit role label",
        );
      const topic = label.match(/^topic:(.+)$/i);
      if (topic)
        edge(
          nid,
          auxiliary("topic", topic[1].trim(), sid),
          "topic",
          "observed",
          "Explicit topic label",
        );
    }
    const existingRole = edges.some(
      (e) => e.from === nid && e.relation === "role",
    );
    if (!existingRole)
      for (const [role, pattern] of Object.entries(cues))
        if (pattern.test(nodes.get(nid).title))
          edge(
            nid,
            auxiliary("role", role),
            "role",
            "inferred",
            `Role cue in title: ${nodes.get(nid).title}`,
          );
    if (source.provider === "jira")
      for (const link of arr(f.issuelinks || [], 100)) {
        if (!(source.blocksTypeIds || []).includes(String(link.type?.id)))
          continue;
        if (link.outwardIssue?.id)
          edge(
            nid,
            key(sid, "task", link.outwardIssue.id),
            "blocks",
            "observed",
            "Configured provider blocking-link type",
          );
        if (link.inwardIssue?.id)
          edge(
            key(sid, "task", link.inwardIssue.id),
            nid,
            "blocks",
            "observed",
            "Configured provider blocking-link type",
          );
      }
  }
  for (const run of arr(input.runs || [], 500)) {
    const sid = id(run.sourceId);
    if (!sourceIds.has(sid)) fail();
    if (Date.parse(instant(run.observedAt)) > Date.parse(observedAt) + 60000)
      fail();
    const rid = node({
      id: key(sid, "run", run.id),
      sourceId: sid,
      kind: "run",
      title: text(run.title) || "Agent run",
      state: ["active", "waiting", "finished", "unknown"].includes(run.state)
        ? run.state
        : "unknown",
      nativeStatus: "",
      observedAt: instant(run.observedAt),
      sessionKey: id(run.sessionKey),
      agent: id(run.agentId),
    });
    edge(
      auxiliary("agent", run.agentId),
      rid,
      "runs",
      "observed",
      "Runtime agent identity",
    );
    if (run.taskId)
      edge(
        key(sid, "task", run.taskId),
        rid,
        "works-on",
        "observed",
        "Explicit runtime task binding",
      );
    if (run.role) {
      if (!roles.includes(run.role)) fail();
      edge(
        rid,
        auxiliary("role", run.role),
        "role",
        "observed",
        "Explicit run role",
      );
    }
    runRecords.push({ run, rid });
  }
  // Missing task bindings may be suggested by exact tracker references, never titles alone.
  for (const { run, rid } of runRecords) {
    if (run.taskId) continue;
    const brief = text(run.brief, 4096);
    for (const task of nodes.values()) {
      if (
        task.kind !== "task" ||
        task.sourceId !== run.sourceId ||
        !task.identifier
      )
        continue;
      const escaped = task.identifier.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      if (
        new RegExp(`(^|[^A-Za-z0-9_-])${escaped}($|[^A-Za-z0-9_-])`, "i").test(
          brief,
        )
      )
        edge(
          task.id,
          rid,
          "works-on",
          "inferred",
          `Tracker reference ${task.identifier} occurs in run brief; mention does not prove assignment`,
        );
    }
  }
  if (nodes.size > 2000 || edges.length > 5000) fail();
  // Parent cycles invalidate the graph instead of producing recursive or inflated progress.
  const children = new Map();
  for (const e of edges)
    if (e.relation === "contains") {
      if (!children.has(e.from)) children.set(e.from, []);
      children.get(e.from).push(e.to);
    }
  const seen = new Set(),
    stack = new Set();
  function visit(k) {
    if (stack.has(k)) fail();
    if (seen.has(k)) return;
    stack.add(k);
    for (const c of children.get(k) || []) visit(c);
    stack.delete(k);
    seen.add(k);
  }
  for (const k of nodes.keys()) visit(k);
  return {
    schemaVersion: 1,
    profile: input.profile,
    agentId,
    observedAt,
    sources: declarations,
    nodes: [...nodes.values()],
    edges,
    warnings: [...new Set(warnings)],
  };
}
module.exports = { compile };
