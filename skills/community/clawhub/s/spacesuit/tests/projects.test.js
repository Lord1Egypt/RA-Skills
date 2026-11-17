const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { execFileSync } = require("node:child_process");
const { collect, project } = require("../lib/projects/adapters");
const { run, read } = require("../lib/projects/runtime");
const fixtures = path.join(__dirname, "fixtures/projects");
const config = require("./fixtures/projects/config.json");
const linear = require("./fixtures/projects/linear.json");
const jira = require("./fixtures/projects/jira.json");
function workspace(t) {
  const root = fs.realpathSync(
    fs.mkdtempSync(path.join(os.tmpdir(), "projects-")),
  );
  for (const name of ["config.json", "linear.json", "jira.json"])
    fs.copyFileSync(path.join(fixtures, name), path.join(root, name));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
}
const args = (root, op = "preview") => [
  op,
  "--workspace",
  root,
  "--config",
  "config.json",
];
test("mixed source import retains equal titles, distinct IDs, null counts and original observation", async (t) => {
  const root = workspace(t),
    out = await run(args(root));
  assert.equal(out.liveSyncConfigured, false);
  assert.equal(out.snapshots.length, 2);
  assert.equal(
    out.snapshots[0].projects[0].title,
    out.snapshots[1].projects[0].title,
  );
  assert.equal(out.snapshots[0].projects[0].stage, "doing");
  assert.equal(out.snapshots[1].projects[0].stage, "review");
  assert.equal(out.snapshots[1].projects[0].nativeStatusId, "10002");
  assert.deepEqual(out.snapshots[1].projects[0].counts, {
    total: null,
    done: null,
    blocked: null,
  });
  assert.equal(
    out.snapshots[0].observedAt,
    linear.observedAt.replace("00Z", "00.000Z"),
  );
  assert.equal(fs.existsSync(path.join(root, "state")), false);
  await run(args(root, "apply"));
  const sel = JSON.parse(
    read(root, "state/command-center/project-sources.json"),
  );
  assert.equal(sel.sources.length, 2);
  assert.equal("input" in sel.sources[0], false);
});
test("semantic categories do not infer review; native IDs override; non-epic excluded", () => {
  const s = { ...config.sources[1], statusMap: {} };
  const raw = structuredClone(jira.pages[0].issues[0]);
  raw.fields.status.name = "In Review";
  raw.fields.status.statusCategory.key = "done";
  assert.equal(project(s, raw).stage, "done");
  raw.fields.status.statusCategory.key = "unrecognized";
  assert.equal(project(s, raw).stage, "unknown");
  raw.fields.issuetype.id = "10009";
  assert.equal(project(s, raw), null);
  const a = structuredClone(linear.pages[0].data.projects.nodes[0]);
  a.status.type = "canceled";
  assert.equal(project(config.sources[0], a).stage, "canceled");
});
test("pagination follows Linear cursors and fixed read-only query; caps are partial", async () => {
  const requests = [];
  const result = await collect({
    source: config.sources[0],
    maxPages: 2,
    request: async (req) => {
      requests.push(req);
      const r = structuredClone(linear.pages[0]);
      r.data.projects.nodes[0].id = `p-${requests.length}`;
      r.data.projects.pageInfo = {
        hasNextPage: true,
        endCursor: `cursor-${requests.length}`,
      };
      return r;
    },
  });
  assert.equal(result.status, "partial");
  assert.equal(result.projects.length, 2);
  assert.equal(requests[1].variables.after, "cursor-1");
  assert.match(requests[0].query, /^query /);
  assert.equal(requests[0].signal.aborted, true);
});
test("Jira token pagination and read-only request with explicit epic types", async () => {
  const seen = [];
  const result = await collect({
    source: config.sources[1],
    request: async (req) => {
      seen.push(req);
      const r = structuredClone(jira.pages[0]);
      r.issues[0].id = String(seen.length);
      if (seen.length === 1) {
        r.isLast = false;
        r.nextPageToken = "next";
      }
      return r;
    },
  });
  assert.equal(result.status, "ready");
  assert.equal(result.projects.length, 2);
  assert.equal(seen[0].method, "GET");
  assert.equal(seen[1].params.nextPageToken, "next");
});
test("deadline resolves even when injected client ignores AbortSignal", async () => {
  const start = Date.now();
  const result = await collect({
    source: config.sources[0],
    timeoutMs: 15,
    request: () => new Promise(() => {}),
  });
  assert.equal(result.status, "error");
  assert.ok(Date.now() - start < 1000);
});
test("repeated cursors, GraphQL errors, malformed pages and duplicate project IDs never report complete", async () => {
  const bad = structuredClone(linear.pages[0]);
  bad.data.projects.nodes = [];
  bad.data.projects.pageInfo = { hasNextPage: true, endCursor: "repeat" };
  assert.equal(
    (await collect({ source: config.sources[0], request: async () => bad }))
      .status,
    "error",
  );
  assert.equal(
    (
      await collect({
        source: config.sources[0],
        request: async () => ({
          errors: [{ message: "private server detail" }],
        }),
      })
    ).status,
    "error",
  );
  const dupe = structuredClone(linear.pages[0]);
  dupe.data.projects.nodes.push(dupe.data.projects.nodes[0]);
  assert.equal(
    (await collect({ source: config.sources[0], request: async () => dupe }))
      .status,
    "partial",
  );
});
test("partial pages and project cap honestly mark partial, never synthesize counts", async () => {
  let call = 0;
  const result = await collect({
    source: config.sources[0],
    request: async () => {
      if (call++) throw new Error("offline");
      const r = structuredClone(linear.pages[0]);
      r.data.projects.pageInfo = { hasNextPage: true, endCursor: "next" };
      return r;
    },
  });
  assert.equal(result.status, "partial");
  assert.equal(result.projects.length, 1);
  const p = structuredClone(linear.pages[0]);
  p.data.projects.nodes.push({ ...p.data.projects.nodes[0], id: "other" });
  assert.equal(
    (
      await collect({
        source: config.sources[0],
        maxProjects: 1,
        request: async () => p,
      })
    ).status,
    "partial",
  );
});
test("disabled source unread, missing source unavailable, malformed isolated", async (t) => {
  const root = workspace(t),
    c = structuredClone(config);
  c.sources[0].enabled = false;
  c.sources[0].input = "../secret";
  fs.writeFileSync(path.join(root, "config.json"), JSON.stringify(c));
  fs.unlinkSync(path.join(root, "jira.json"));
  const out = await run(args(root));
  assert.equal(out.snapshots.length, 1);
  assert.equal(out.snapshots[0].status, "unavailable");
  fs.writeFileSync(path.join(root, "jira.json"), "{");
  assert.equal((await run(args(root))).snapshots[0].status, "error");
});
test("profile isolation refuses overwrite and previous data survives failed refresh with old timestamp", async (t) => {
  const root = workspace(t);
  await run(args(root, "apply"));
  fs.writeFileSync(path.join(root, "linear.json"), "{");
  const out = await run(args(root, "apply"));
  assert.equal(out.snapshots[0].status, "error");
  assert.equal(out.snapshots[0].projects.length, 1);
  assert.equal(
    out.snapshots[0].observedAt,
    linear.observedAt.replace("00Z", "00.000Z"),
  );
  const c = structuredClone(config);
  c.profile = "different";
  fs.writeFileSync(path.join(root, "config.json"), JSON.stringify(c));
  await assert.rejects(run(args(root, "apply")), /IDENTITY_MISMATCH/);
});
test("unsafe input paths, symlinks, FIFOs, oversized files and output symlinks rejected", async (t) => {
  const root = workspace(t);
  assert.throws(() => read(root, "../escape"), /UNSAFE_PATH/);
  fs.symlinkSync(path.join(root, "linear.json"), path.join(root, "alias.json"));
  assert.throws(() => read(root, "alias.json"), /UNSAFE_PATH/);
  execFileSync("mkfifo", [path.join(root, "pipe.json")]);
  assert.throws(() => read(root, "pipe.json"), /INVALID_FILE/);
  fs.writeFileSync(path.join(root, "big.json"), "x".repeat(1024 * 1024 + 1));
  assert.throws(() => read(root, "big.json"), /INPUT_LIMIT/);
  fs.mkdirSync(path.join(root, "state"));
  fs.symlinkSync(root, path.join(root, "state/command-center"));
  await assert.rejects(run(args(root, "apply")), /UNSAFE_PATH/);
});
test("unsafe URLs removed, explicit associations retained without title-based inference", () => {
  const s = structuredClone(config.sources[0]);
  s.links = {
    "project-alpha": {
      agents: ["worker"],
      dependencies: [{ sourceId: "jira-example", projectId: "10001" }],
    },
  };
  const raw = structuredClone(linear.pages[0].data.projects.nodes[0]);
  raw.url = "javascript:alert(1)";
  raw.description = "Authorization: Bearer samplevalue1234";
  const p = project(s, raw);
  assert.equal(p.url, null);
  assert.deepEqual(p.agents, ["worker"]);
  assert.equal(p.dependencies.length, 1);
  assert.ok(!p.summary.includes("samplevalue1234"));
  assert.deepEqual(project(config.sources[0], raw).dependencies, []);
});

test("invalid transport identity and missing source ID fail before request", async () => {
  let called = false;
  const request = async () => {
    called = true;
    return linear.pages[0];
  };
  await assert.rejects(
    collect({ source: { ...config.sources[0], id: undefined }, request }),
    /INVALID_SOURCE/,
  );
  await assert.rejects(
    collect({ source: config.sources[0], profile: 42, request }),
    /INVALID_OPTIONS/,
  );
  assert.equal(called, false);
});

test("retention strips unexpected previous fields and isolates invalid counts", async (t) => {
  const root = workspace(t);
  await run(args(root, "apply"));
  const dest = path.join(
    root,
    "state/command-center/projects/linear-example.json",
  );
  const previous = JSON.parse(fs.readFileSync(dest, "utf8"));
  previous.projects[0].unexpectedPrivateField = "not copied";
  fs.writeFileSync(dest, JSON.stringify(previous));
  fs.writeFileSync(path.join(root, "linear.json"), "{");
  const result = await run(args(root));
  assert.equal(
    "unexpectedPrivateField" in result.snapshots[0].projects[0],
    false,
  );
  previous.projects[0].counts = { total: 1, done: 2, blocked: null };
  fs.writeFileSync(dest, JSON.stringify(previous));
  const invalid = await run(args(root));
  assert.equal(invalid.snapshots[0].status, "error");
  assert.deepEqual(invalid.snapshots[0].projects, []);
  assert.equal(invalid.snapshots[1].status, "ready");
});

test("offline exports beyond 200 projects retain bounded partial instead of error", async (t) => {
  const root = workspace(t);
  const exported = { observedAt: linear.observedAt, pages: [] };
  for (let i = 0; i < 5; i++) {
    const page = structuredClone(linear.pages[0]);
    page.data.projects.nodes = Array.from({ length: 50 }, (_, j) => ({
      ...page.data.projects.nodes[0],
      id: `project-${i}-${j}`,
    }));
    page.data.projects.pageInfo = {
      hasNextPage: i < 4,
      endCursor: i < 4 ? `cursor-${i}` : null,
    };
    exported.pages.push(page);
  }
  fs.writeFileSync(path.join(root, "linear.json"), JSON.stringify(exported));
  const result = await run(args(root, "apply"));
  assert.equal(result.snapshots[0].status, "partial");
  assert.equal(result.snapshots[0].projects.length, 200);
  assert.equal(
    JSON.parse(read(root, "state/command-center/projects/linear-example.json"))
      .projects.length,
    200,
  );
});

test("corrupt previous snapshots isolate source and preserve files; healthy sources still apply", async (t) => {
  const root = workspace(t);
  await run(args(root, "apply"));
  const dest = path.join(
    root,
    "state/command-center/projects/linear-example.json",
  );
  fs.writeFileSync(dest, "{");
  const changed = structuredClone(jira);
  changed.pages[0].issues[0].fields.summary = "Updated delivery";
  fs.writeFileSync(path.join(root, "jira.json"), JSON.stringify(changed));
  const result = await run(args(root, "apply"));
  assert.equal(result.status, "partial");
  assert.equal(result.snapshots[0].status, "error");
  assert.deepEqual(result.snapshots[0].projects, []);
  assert.equal(result.snapshots[1].status, "ready");
  assert.equal(fs.readFileSync(dest, "utf8"), "{");
  assert.equal(
    JSON.parse(read(root, "state/command-center/projects/jira-example.json"))
      .projects[0].title,
    "Updated delivery",
  );
});

test("foreign previous source is not retained or overwritten while healthy source applies", async (t) => {
  const root = workspace(t);
  await run(args(root, "apply"));
  const dest = path.join(
    root,
    "state/command-center/projects/linear-example.json",
  );
  const foreign = JSON.parse(fs.readFileSync(dest, "utf8"));
  foreign.profile = "foreign";
  foreign.projects[0].title = "Private foreign title";
  const original = JSON.stringify(foreign);
  fs.writeFileSync(dest, original);
  const result = await run(args(root, "apply"));
  assert.equal(result.status, "partial");
  assert.deepEqual(result.skippedSources, ["linear-example"]);
  assert.equal(JSON.stringify(result).includes("Private foreign title"), false);
  assert.equal(fs.readFileSync(dest, "utf8"), original);
  assert.equal(result.snapshots[1].status, "ready");
});
