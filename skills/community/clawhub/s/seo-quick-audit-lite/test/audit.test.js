import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { auditHtml } from "../scripts/audit.js";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(DIR, "..");

const GOOD = `<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>A reasonably sized page title here for testing</title>
<meta name="description" content="This is a meta description that sits comfortably within the recommended fifty to one hundred sixty character window for search snippets.">
<link rel="canonical" href="https://example.com/page">
<meta property="og:title" content="t"><meta property="og:description" content="d"><meta property="og:image" content="i">
</head><body><h1>Heading</h1><img src="a.png" alt="a"></body></html>`;

const BAD = `<html><head><title>x</title></head><body><img src="a.png"><h1>a</h1><h1>b</h1></body></html>`;

test("good html: all pass/info, no fails", () => {
  const checks = auditHtml(GOOD);
  assert.equal(checks.filter((c) => c.status === "fail").length, 0);
  assert.equal(checks.find((c) => c.id === "title").status, "pass");
  assert.equal(checks.find((c) => c.id === "h1").status, "pass");
});

test("bad html: fails on description + h1, warns on title", () => {
  const checks = auditHtml(BAD);
  assert.equal(checks.find((c) => c.id === "meta-description").status, "fail");
  assert.equal(checks.find((c) => c.id === "h1").status, "warn");
  assert.equal(checks.find((c) => c.id === "title").status, "warn");
  assert.equal(checks.find((c) => c.id === "img-alt").status, "warn");
});

test("cli: exit 1 on warn/fail, json on stdout", () => {
  const f = path.join(os.tmpdir(), `seo-${Date.now()}.html`);
  fs.writeFileSync(f, BAD);
  try {
    execFileSync("node", ["scripts/audit.js", f], {
      cwd: ROOT,
      encoding: "utf8",
    });
    assert.fail("should have exited 1");
  } catch (e) {
    assert.equal(e.status, 1);
    const j = JSON.parse(e.stdout);
    assert.ok(j.summary.fail >= 1);
  } finally {
    fs.unlinkSync(f);
  }
});

test("cli: canonical URL produces upgrade field", () => {
  const f = path.join(os.tmpdir(), `seo-up-${Date.now()}.html`);
  fs.writeFileSync(f, GOOD);
  try {
    let stdout;
    try {
      stdout = execFileSync("node", ["scripts/audit.js", f], {
        cwd: ROOT,
        encoding: "utf8",
      });
    } catch (e) {
      stdout = e.stdout; // exit 1 on warns still emits JSON
    }
    const j = JSON.parse(stdout);
    assert.equal(j.upgrade.skill, "seo-quick-audit");
    assert.ok(j.upgrade.reasons.length > 0);
  } finally {
    fs.unlinkSync(f);
  }
});

test("cli: no live references means no upgrade field", () => {
  const f = path.join(os.tmpdir(), `seo-no-${Date.now()}.html`);
  fs.writeFileSync(f, BAD);
  try {
    execFileSync("node", ["scripts/audit.js", f], {
      cwd: ROOT,
      encoding: "utf8",
    });
    assert.fail("should have exited 1");
  } catch (e) {
    if (e.stdout === undefined) throw e;
    assert.equal(e.status, 1);
    assert.equal(JSON.parse(e.stdout).upgrade, undefined);
  } finally {
    fs.unlinkSync(f);
  }
});

test("cli: exit 2 on missing file", () => {
  try {
    execFileSync("node", ["scripts/audit.js", "nope.html"], {
      cwd: ROOT,
      encoding: "utf8",
      stdio: "pipe",
    });
    assert.fail("should have exited 2");
  } catch (e) {
    assert.equal(e.status, 2);
  }
});
