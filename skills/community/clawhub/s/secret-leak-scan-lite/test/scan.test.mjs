import { test } from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promises as fs } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT = fileURLToPath(
  new URL("../scripts/scan.mjs", import.meta.url),
);

const run = (args) =>
  new Promise((resolve) => {
    execFile(
      process.execPath,
      [SCRIPT, ...args],
      (err, stdout, stderr) =>
        resolve({ code: err?.code ?? 0, stdout, stderr }),
    );
  });

const withTempDir = async (fn) => {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "slsl-test-"));
  try {
    return await fn(dir);
  } finally {
    await fs.rm(dir, { recursive: true, force: true });
  }
};

test("directory scan reports masked findings and exits 1", async () =>
  withTempDir(async (dir) => {
    const aws = "REDACTED-SECRET"; // AWS's documented public example key
    const slack = "REDACTED-SECRET";
    await fs.writeFile(
      path.join(dir, "a.js"),
      `const k = "${aws}";\nconst t = "${slack}";\n`,
    );
    await fs.mkdir(path.join(dir, "sub"));
    await fs.writeFile(
      path.join(dir, "sub", "key.pem"),
      "REDACTED-SECRET\n",
    );

    const { code, stdout } = await run([dir]);
    assert.equal(code, 1);
    const report = JSON.parse(stdout);

    assert.equal(report.tool, "secret-leak-scan-lite");
    assert.equal(report.input.kind, "directory");
    assert.equal(report.summary.filesScanned, 2);
    assert.equal(report.summary.findings, 3);

    const types = report.findings.map((f) => f.type).sort();
    assert.deepEqual(types, [
      "aws-access-key-id",
      "private-key-block",
      "slack-token",
    ]);
    const awsFinding = report.findings.find(
      (f) => f.type === "aws-access-key-id",
    );
    assert.equal(awsFinding.file, "a.js");
    assert.equal(awsFinding.line, 1);
    assert.match(
      awsFinding.fingerprint,
      /^AKIA… \(len=20, sha256:[0-9a-f]{8}\)$/,
    );

    // raw secret values must never appear in the report
    assert.equal(stdout.includes(aws), false);
    assert.equal(stdout.includes("1234567890"), false);
  }));

test("clean directory exits 0 with empty findings", async () =>
  withTempDir(async (dir) => {
    await fs.writeFile(path.join(dir, "index.js"), "export const x = 1;\n");
    const { code, stdout } = await run([dir]);
    assert.equal(code, 0);
    const report = JSON.parse(stdout);
    assert.equal(report.findings.length, 0);
    assert.equal(report.summary.findings, 0);
  }));

test("usage error exits 2 and writes no report", async () => {
  const { code, stdout } = await run([]);
  assert.equal(code, 2);
  assert.equal(stdout.trim(), "");
});
