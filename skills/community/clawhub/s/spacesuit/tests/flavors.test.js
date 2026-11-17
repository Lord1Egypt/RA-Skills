const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const {
  run,
  parseTables,
  hasPositiveRevenue,
  validateManifest,
} = require("../lib/flavors/runtime");
function fixture(t) {
  const w = fs.mkdtempSync(
    path.join(fs.realpathSync(os.tmpdir()), "spacesuit-flavor-"),
  );
  t.after(() => fs.rmSync(w, { recursive: true, force: true }));
  return {
    w,
    cli: (command, ...rest) => run([command, "--workspace", w, ...rest]),
    selection: () =>
      JSON.parse(
        fs.readFileSync(path.join(w, "state/command-center/extensions.json")),
      ),
    snapshot: (id) =>
      JSON.parse(
        fs.readFileSync(
          path.join(w, `state/command-center/extensions/spacesuit.${id}.json`),
        ),
      ),
  };
}
function intel(w, files) {
  fs.mkdirSync(path.join(w, "intel"));
  for (const [name, data] of Object.entries(files))
    fs.writeFileSync(path.join(w, "intel", name), data);
}
test("preview never writes; apply/select/core disable/restore are reversible and preserve overrides and data", (t) => {
  const f = fixture(t);
  const preview = f.cli("preview");
  assert.equal(preview.after.enabled.length, 3);
  assert.deepEqual(fs.readdirSync(f.w), []);
  const applied = f.cli("apply");
  assert.equal(f.selection().mode, "extensions");
  assert.equal(f.cli("apply").status, "unchanged");
  const sel = f.selection();
  sel.privateOverride = { custom: true };
  const selectionPath = path.join(f.w, "state/command-center/extensions.json");
  fs.writeFileSync(selectionPath, JSON.stringify(sel));
  const original = fs.readFileSync(selectionPath, "utf8");
  const disable = f.cli("disable");
  assert.equal(f.selection().mode, "core");
  assert.deepEqual(f.selection().privateOverride, sel.privateOverride);
  assert.throws(() => f.cli("collect"), /COLLECTION_DISABLED/);
  f.cli("restore", "--backup", disable.backup);
  assert.equal(fs.readFileSync(selectionPath, "utf8"), original);
  f.cli("restore", "--backup", applied.backup);
  assert.equal(fs.existsSync(selectionPath), false);
});
test("collect missing inputs yields unavailable not zero, and does not create inputs", (t) => {
  const f = fixture(t);
  f.cli("apply");
  f.cli("collect");
  for (const id of ["intel", "pipeline", "monetization"]) {
    const s = f.snapshot(id);
    assert.equal(s.status, "unavailable");
    assert.deepEqual(s.panels, []);
    assert.ok(Number.isFinite(Date.parse(s.observedAt)));
  }
  assert.equal(fs.existsSync(path.join(f.w, "intel")), false);
});
test("empty table cells, escaped pipes, status aliases and explicit revenue retain corrected legacy behavior", (t) => {
  const f = fixture(t);
  intel(f.w, {
    "DEMO-PIPELINE.md":
      "| Item | Status | Note |\n| --- | --- | --- |\n| Alpha | **READY** | A \\| B |\n| Beta | | last |\n",
    "MONETIZATION-TRACKER.md":
      "| Company | Revenue | Milestone | Blocker | Priority |\n| --- | --- | --- | --- | --- |\n| Example | | ready | | HIGH |\n| Sample | $1,200/mo | | | LOW |\n| Pending | 100 prospects | | | |\n",
  });
  f.cli("apply");
  f.cli("collect");
  const mon = f.snapshot("monetization");
  assert.equal(mon.status, "ready");
  assert.deepEqual(
    mon.panels[0].metrics.map((m) => m.value),
    [3, 1, 1],
  );
  assert.equal(mon.panels[1].rows[0].revenue, "");
  assert.equal(mon.panels[1].rows[0].milestone, "ready");
  const pipeline = f.snapshot("pipeline").panels[0].rows[0];
  assert.equal(pipeline.statuses, "READY: 1");
  assert.equal(pipeline.items, "2");
  assert.equal(
    parseTables("| A | B |\n| --- | --- |\n| | x \\| y |")[0].rows[0].b,
    "x | y",
  );
  for (const value of ["pending", "0", "$0.00", "100 prospects", "-5"])
    assert.equal(hasPositiveRevenue(value), false);
});
test("malicious headers and HTML values remain inert JSON strings, no execution metadata", (t) => {
  const f = fixture(t);
  const payload = "<img src=x onerror=alert(1)>";
  intel(f.w, {
    "MONETIZATION-TRACKER.md": `| Company | Revenue | Priority | __proto__ |\n| --- | --- | --- | --- |\n| ${payload} | 5 | "><script>x</script> | poison |`,
  });
  f.cli("apply");
  f.cli("collect");
  const s = f.snapshot("monetization");
  assert.equal(s.panels[1].rows[0].name, payload);
  assert.equal({}.poison, undefined);
  assert.equal(s.schemaVersion, 1);
  assert.equal(s.version, "1.0.0");
  assert.equal(s.profile, "");
  assert.equal(s.agentId, "main");
  for (const p of s.panels) {
    assert.deepEqual(Object.keys(p.title).sort(), ["en", "zh-CN"]);
    assert.ok(p.id);
    assert.ok(!("html" in p));
    assert.ok(!("script" in p));
  }
});
test("profile and agent isolation reject foreign selections, snapshots and backups", (t) => {
  const f = fixture(t);
  const applied = f.cli("apply", "--profile", "work");
  assert.throws(() => f.cli("collect"), /IDENTITY_MISMATCH/);
  assert.throws(
    () => f.cli("apply", "--profile", "work", "--agent", "other"),
    /IDENTITY_MISMATCH/,
  );
  f.cli("collect", "--profile", "work");
  const s = f.snapshot("intel");
  s.profile = "foreign";
  fs.writeFileSync(
    path.join(f.w, "state/command-center/extensions/spacesuit.intel.json"),
    JSON.stringify(s),
  );
  assert.throws(
    () => f.cli("collect", "--profile", "work"),
    /IDENTITY_MISMATCH/,
  );
  assert.throws(
    () => f.cli("restore", "--backup", applied.backup),
    /IDENTITY_MISMATCH/,
  );
});
test("reject path traversal, symlink source/destination/root, oversized inputs and duplicate IDs", (t) => {
  const f = fixture(t);
  f.cli("apply");
  assert.throws(
    () => f.cli("restore", "--backup", "../other"),
    /INVALID_BACKUP/,
  );
  fs.symlinkSync(os.tmpdir(), path.join(f.w, "intel"));
  assert.equal(f.cli("collect").status, "error");
  assert.equal(f.snapshot("intel").status, "error");
  fs.unlinkSync(path.join(f.w, "intel"));
  intel(f.w, { "large.md": "x".repeat(256 * 1024 + 1) });
  assert.equal(f.cli("collect").status, "error");
  const snapshotPath = path.join(
    f.w,
    "state/command-center/extensions/spacesuit.intel.json",
  );
  fs.unlinkSync(snapshotPath);
  fs.symlinkSync(path.join(f.w, "intel/large.md"), snapshotPath);
  assert.throws(() => f.cli("collect"), /UNSAFE_PATH/);
  const sel = f.selection();
  sel.enabled.push(sel.enabled[0]);
  fs.writeFileSync(
    path.join(f.w, "state/command-center/extensions.json"),
    JSON.stringify(sel),
  );
  assert.throws(() => f.cli("preview"), /INVALID_SELECTION/);
});
test("unsupported package version rejected, missing optional tracker isolated, snapshots replaced without temp debris", (t) => {
  const f = fixture(t);
  intel(f.w, { "notes.md": "Agent: Helper\nSynthetic note" });
  f.cli("apply");
  f.cli("collect");
  assert.equal(f.snapshot("intel").status, "ready");
  assert.equal(f.snapshot("pipeline").status, "ready");
  assert.equal(f.snapshot("monetization").status, "unavailable");
  const selectionFile = path.join(f.w, "state/command-center/extensions.json");
  const sel = f.selection();
  sel.enabled[0].version = "2.0.0";
  fs.writeFileSync(selectionFile, JSON.stringify(sel));
  assert.throws(() => f.cli("collect"), /INCOMPATIBLE_PACKAGE/);
  assert.ok(
    fs
      .readdirSync(path.join(f.w, "state/command-center/extensions"))
      .every((n) => n.endsWith(".json")),
  );
});
test("collect requires explicit selection; invalid options do not mutate workspace", (t) => {
  const f = fixture(t);
  assert.throws(() => f.cli("collect"), /COLLECTION_DISABLED/);
  assert.throws(() => f.cli("apply", "--flavor", "../unreviewed"), /USAGE/);
  assert.throws(() => f.cli("apply", "--command", "touch"), /USAGE/);
});
test("restore recovers corrupt current selection while backing up exact damaged bytes", (t) => {
  const f = fixture(t);
  f.cli("apply");
  const disabled = f.cli("disable");
  const target = path.join(f.w, "state/command-center/extensions.json");
  const corrupt = "{ broken JSON";
  fs.writeFileSync(target, corrupt);
  const restored = f.cli("restore", "--backup", disabled.backup);
  assert.equal(f.selection().mode, "extensions");
  const backup = JSON.parse(
    fs.readFileSync(
      path.join(f.w, "state/command-center/backups", restored.backup),
    ),
  );
  assert.equal(backup.selection, corrupt);
});
test("selected FIFO rejected before open; source FIFO does not stall collection", (t) => {
  if (process.platform === "win32") return t.skip("POSIX FIFO test");
  const { execFileSync } = require("node:child_process");
  const f = fixture(t);
  f.cli("apply");
  const target = path.join(f.w, "state/command-center/extensions.json");
  fs.unlinkSync(target);
  execFileSync("mkfifo", [target]);
  assert.throws(() => f.cli("preview"), /INVALID_INPUT_TYPE/);
  fs.unlinkSync(target);
  f.cli("apply");
  fs.mkdirSync(path.join(f.w, "intel"));
  execFileSync("mkfifo", [path.join(f.w, "intel", "source.md")]);
  assert.equal(f.cli("collect").status, "error");
});
test("snapshot display cells redact common credentials without altering input files", (t) => {
  const f = fixture(t);
  const fake = "Bearer " + "x".repeat(24);
  const content = `| Company | Revenue | Blocker |\n| --- | --- | --- |\n| Example | 5 | ${fake} |\n| Other | 1 | password=synthetic |`;
  intel(f.w, { "MONETIZATION-TRACKER.md": content });
  f.cli("apply");
  f.cli("collect");
  const rows = f.snapshot("monetization").panels[1].rows;
  assert.equal(rows[0].blocker, "Bearer [REDACTED]");
  assert.equal(rows[1].blocker, "password=[REDACTED]");
  assert.equal(
    fs.readFileSync(path.join(f.w, "intel/MONETIZATION-TRACKER.md"), "utf8"),
    content,
  );
});
test("package locale integrity and incompatible or executable declarations are rejected", () => {
  const manifest = require("../extensions/spacesuit.intel/manifest.json");
  assert.doesNotThrow(() => validateManifest(manifest, "spacesuit.intel"));
  for (const mutation of [
    { locales: ["en", "en"] },
    { locales: ["en"] },
    { contractVersion: 2 },
    { command: "unreviewed" },
    { inputs: ["../outside"] },
  ]) {
    assert.throws(
      () => validateManifest({ ...manifest, ...mutation }, "spacesuit.intel"),
      /INVALID_PACKAGE/,
    );
  }
});

test("credential defense includes full Basic authentication values", () => {
  const { redactExtensionText } = require("../lib/flavors/redaction");
  assert.equal(
    redactExtensionText("Authorization: Basic " + "X".repeat(32)),
    "Authorization: [REDACTED] [REDACTED]",
  );
});
test("all generated panel IDs/column keys and translated labels follow host v1", (t) => {
  const f = fixture(t);
  intel(f.w, {
    "SAMPLE-PIPELINE.md":
      "| Item | Status |\n| --- | --- |\n| Sample | Ready |",
    "MONETIZATION-TRACKER.md":
      "| Company | Revenue |\n| --- | --- |\n| Example | 5 |",
  });
  f.cli("apply");
  f.cli("collect");
  for (const id of ["intel", "pipeline", "monetization"]) {
    const s = f.snapshot(id);
    assert.equal(s.status, "ready");
    assert.equal(new Set(s.panels.map((p) => p.id)).size, s.panels.length);
    for (const p of s.panels) {
      assert.match(p.id, /^[a-z][a-z0-9_-]*$/);
      const labels = [p.title];
      for (const column of p.columns || []) {
        assert.match(column.key, /^[a-z][a-z0-9_-]*$/);
        labels.push(column.label);
      }
      for (const m of p.metrics || []) labels.push(m.label);
      for (const l of labels)
        for (const locale of ["en", "zh-CN"])
          assert.ok(
            typeof l[locale] === "string" &&
              l[locale].length > 0 &&
              l[locale].length <= 256,
          );
    }
  }
});

test("input errors are isolated to extensions whose declared inputs include the file", (t) => {
  const f = fixture(t);
  intel(f.w, {
    "MONETIZATION-TRACKER.md":
      "| Company | Revenue |\n| --- | --- |\n| Example | $5 |",
    "sample-queue.md": "| Item | Status |\n| --- | --- |\n| Sample | Ready |",
    "unrelated.md": "x".repeat(256 * 1024 + 1),
  });
  f.cli("apply");
  f.cli("collect");
  assert.equal(f.snapshot("intel").status, "error");
  assert.equal(f.snapshot("pipeline").status, "ready");
  assert.equal(f.snapshot("monetization").status, "ready");
  if (process.platform !== "win32") {
    require("node:child_process").execFileSync("mkfifo", [
      path.join(f.w, "intel", "unrelated-fifo.md"),
    ]);
    f.cli("collect");
    assert.equal(f.snapshot("intel").status, "error");
    assert.equal(f.snapshot("pipeline").status, "ready");
    assert.equal(f.snapshot("monetization").status, "ready");
  }
});

test("monetization-only selection reads exact tracker even when unrelated inputs fail", (t) => {
  const f = fixture(t);
  intel(f.w, {
    "MONETIZATION-TRACKER.md":
      "| Company | Revenue |\n| --- | --- |\n| Example | $5 |",
    "unrelated.md": "x".repeat(256 * 1024 + 1),
  });
  f.cli("apply");
  const selection = f.selection();
  selection.enabled = selection.enabled.filter(
    (x) => x.id === "spacesuit.monetization",
  );
  fs.writeFileSync(
    path.join(f.w, "state/command-center/extensions.json"),
    JSON.stringify(selection),
  );
  assert.equal(f.cli("collect").status, "collected");
  assert.equal(f.snapshot("monetization").status, "ready");
  assert.equal(
    fs.existsSync(
      path.join(f.w, "state/command-center/extensions/spacesuit.intel.json"),
    ),
    false,
  );
});
