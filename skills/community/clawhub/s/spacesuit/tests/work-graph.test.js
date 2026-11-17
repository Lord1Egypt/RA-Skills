const test = require("node:test");
const assert = require("node:assert/strict");
const { compile } = require("../lib/work-graph");
const input = () =>
  structuredClone(require("./fixtures/work-graph/input.json"));
test("Linear projects and Jira epics normalize without conflating native IDs", () => {
  const g = compile(input());
  assert.equal(g.nodes.filter((n) => n.kind === "outcome").length, 2);
  assert.equal(g.nodes.filter((n) => n.kind === "task").length, 5);
  assert.equal(g.sources[1].complete, false);
  assert.ok(g.nodes.some((n) => n.id === "demo-linear:task:1"));
  assert.ok(g.nodes.some((n) => n.id === "demo-jira:task:1"));
  assert.ok(
    g.edges.some(
      (e) =>
        e.from === "demo-jira:task:1" &&
        e.to === "demo-jira:task:2" &&
        e.relation === "blocks",
    ),
  );
});
test("explicit labels and bindings remain distinguishable from inference", () => {
  const g = compile(input());
  const inferred = g.edges.filter((e) => e.basis === "inferred");
  assert.equal(inferred.length, 2);
  assert.ok(inferred.some((e) => e.relation === "works-on"));
  assert.ok(inferred.some((e) => e.relation === "role"));
  assert.ok(!g.nodes.some((n) => "brief" in n));
});
test("exact reference matching never crosses sources or matches a larger identifier", () => {
  for (const brief of ["DEMO-20", "XDEMO-2", "OPS-1", "no ticket"]) {
    const x = input();
    x.runs.at(-1).brief = brief;
    assert.ok(
      !compile(x).edges.some(
        (e) => e.basis === "inferred" && e.relation === "works-on",
      ),
    );
  }
});
test("unmapped statuses stay unknown; explicit native ID mapping supports review", () => {
  const g = compile(input());
  assert.equal(
    g.nodes.find((n) => n.id === "demo-linear:task:3").state,
    "review",
  );
  assert.equal(
    g.nodes.find((n) => n.id === "demo-jira:task:2").state,
    "unknown",
  );
});
test("missing references warn without inventing entities", () => {
  const x = input();
  x.runs[0].taskId = "missing";
  const g = compile(x);
  assert.ok(g.warnings.includes("missing_reference"));
  assert.ok(!g.nodes.some((n) => n.nativeId === "missing"));
});
test("cycles, duplicate sources and future runtime observations fail safely", () => {
  for (const mutate of [
    (x) => x.sources.push(x.sources[0]),
    (x) => (x.runs[0].observedAt = "2027-01-01T00:00:00Z"),
    (x) => {
      x.sources[0].issues[0].parent = { id: "2" };
      x.sources[0].issues[1].parent = { id: "1" };
    },
    (x) => (x.sources[1].epicTypeIds = []),
  ]) {
    const x = input();
    mutate(x);
    assert.throws(() => compile(x), /^Error: WORK_GRAPH_INVALID_INPUT$/);
  }
});
test("CLI rejects malformed input without echoing payload", () => {
  const { spawnSync } = require("node:child_process");
  const r = spawnSync(process.execPath, ["scripts/work-graph.js"], {
    input: "private-payload",
    encoding: "utf8",
  });
  assert.notEqual(r.status, 0);
  assert.ok(!r.stderr.includes("private-payload"));
  assert.equal(r.stdout, "");
});
test("prototype property names are not valid status categories", () => {
  const x = input();
  x.sources[0].issues[0].state.type = "constructor";
  assert.equal(
    compile(x).nodes.find((n) => n.id === "demo-linear:task:1").state,
    "unknown",
  );
});
