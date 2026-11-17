// SPDX-License-Identifier: MIT-0
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { copyFileSync, cpSync, existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, symlinkSync, truncateSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { deflateSync } from "node:zlib";
import { fileURLToPath } from "node:url";

const argv = process.argv.slice(2);
assert.equal(argv.length, 6, "Supply --engine-root DIRECTORY --fixture external-gen_v5_q.png --mixed-fixture external-mixed-code128-qr.png");
assert.equal(argv[0], "--engine-root");
assert.equal(argv[2], "--fixture");
assert.equal(argv[4], "--mixed-fixture");
const runtime = resolve(argv[1]);
const fixture = resolve(argv[3]);
const mixedFixture = resolve(argv[5]);
const helper = fileURLToPath(new URL("scan.mjs", import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), "qrcode-barcode-scanner-test-"));
const checks = [];
const run = (image, args = [], engine = runtime, env = {}) => spawnSync(process.execPath,
  [helper, "--engine-root", engine, "--budget-ms", "0", ...args, "--", image],
  { cwd: scratch, env: { ...process.env, ...env }, encoding: "utf8", timeout: 30_000, maxBuffer: 8 * 1024 * 1024 });
const parse = (result, status) => {
  assert.equal(result.error, undefined);
  assert.equal(result.status, status, result.stderr);
  return JSON.parse(status === 2 ? result.stderr : result.stdout);
};
const record = (name, fn) => { fn(); checks.push(name); };
function crc32(bytes) {
  let crc = 0xffffffff;
  for (const byte of bytes) {
    crc ^= byte;
    for (let bit = 0; bit < 8; bit++) crc = (crc >>> 1) ^ (0xedb88320 & -(crc & 1));
  }
  return (crc ^ 0xffffffff) >>> 0;
}
function chunk(name, data) {
  const label = Buffer.from(name);
  const length = Buffer.alloc(4); length.writeUInt32BE(data.length);
  const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(Buffer.concat([label, data])));
  return Buffer.concat([length, label, data, crc]);
}
function whitePng(width = 64, height = 64) {
  const header = Buffer.alloc(13); header.writeUInt32BE(width, 0); header.writeUInt32BE(height, 4);
  header[8] = 8; header[9] = 2;
  const rows = Buffer.alloc(height * (1 + width * 3), 255);
  for (let y = 0; y < height; y++) rows[y * (1 + width * 3)] = 0;
  return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]), chunk("IHDR", header), chunk("IDAT", deflateSync(rows)), chunk("IEND", Buffer.alloc(0))]);
}
try {
  record("full-exact-report", () => {
    const report = parse(run(fixture), 0);
    assert.deepEqual(report.versions, { scanner: "0.11.0", pipeline: 5, score_contract: 5 });
    assert.equal(report.trace.budget_exhausted, false);
    assert.equal(report.detections.length, 1);
    assert.equal(report.detections[0].symbology, "qr_code");
    assert.equal(report.detections[0].content.text, "https://qrcode-ai.com/c/v5q");
    assert.equal(Buffer.from(report.detections[0].content.raw, "base64").toString("utf8"), "https://qrcode-ai.com/c/v5q");
    assert.equal(report.score.value, 100);
    assert.equal(report.score.weights_run, 100);
    assert.equal(Object.hasOwn(report, "alpha"), false);
  });
  record("frame-null-score", () => {
    const report = parse(run(fixture, ["--profile", "frame"]), 0);
    assert.equal(report.score, null);
    assert.equal(report.detections[0].content.text, "https://qrcode-ai.com/c/v5q");
  });
  for (const profile of ["fast", "frame", "full"]) record(`mixed-qr-code128-${profile}`, () => {
    const report = parse(run(mixedFixture, ["--profile", profile]), 0);
    assert.deepEqual(report.versions, { scanner: "0.11.0", pipeline: 5, score_contract: 5 });
    assert.equal(report.trace.budget_exhausted, false);
    assert.deepEqual(report.detections.map(({ symbology, content }) => ({ symbology, text: content.text, raw: content.raw })).sort((a, b) => a.symbology.localeCompare(b.symbology)), [
      { symbology: "code128", text: "STOCK-4827", raw: Buffer.from("STOCK-4827").toString("base64") },
      { symbology: "qr_code", text: "https://qrc-ai.com/76xMa", raw: Buffer.from("https://qrc-ai.com/76xMa").toString("base64") },
    ]);
    if (profile === "frame") assert.equal(report.score, null);
  });
  const white = join(scratch, "white.png"); writeFileSync(white, whitePng());
  record("valid-no-detection", () => {
    const report = parse(run(white, ["--profile", "frame"]), 1);
    assert.deepEqual(report.detections, []);
    assert.equal(report.score, null);
    assert.equal(report.trace.budget_exhausted, false);
  });
  const invalid = join(scratch, "invalid.png"); writeFileSync(invalid, "invalid");
  record("invalid-image-is-error", () => assert.match(parse(run(invalid), 2).error.message, /QRS-001/));
  record("missing-file-is-error", () => assert.equal(parse(run(join(scratch, "absent.png")), 2).error.code, "input_file"));
  record("missing-dependency-refuses-ambient", () => assert.equal(parse(run(fixture, [], join(scratch, "missing")), 2).error.code, "dependency_missing"));
  const stale = join(scratch, "stale");
  const packageDir = join(stale, "node_modules", "@qrcode-ai-com", "qrcode-barcode-scanner"); mkdirSync(packageDir, { recursive: true });
  writeFileSync(join(packageDir, "package.json"), JSON.stringify({ name: "@qrcode-ai-com/qrcode-barcode-scanner", version: "0.9.0" }));
  record("stale-dependency-refused", () => assert.equal(parse(run(fixture, [], stale), 2).error.code, "dependency_version"));
  record("native-override-refused", () => assert.equal(parse(run(fixture, [], runtime, { NAPI_RS_NATIVE_LIBRARY_PATH: "/unused" }), 2).error.code, "dependency_override"));
  record("wasi-override-refused", () => assert.equal(parse(run(fixture, [], runtime, { NAPI_RS_FORCE_WASI: "true" }), 2).error.code, "dependency_override"));
  const scope = join(runtime, "node_modules", "@qrcode-ai-com");
  const mainSource = join(scope, "qrcode-barcode-scanner");
  const nativeNames = readdirSync(scope).filter((name) => name.startsWith("qrcode-barcode-scanner-") && readdirSync(join(scope, name)).some((file) => file.endsWith(".node")));
  assert.equal(nativeNames.length, 1, "Use a fresh runtime with its single installed native platform");
  const nativeName = nativeNames[0];
  const nativeSource = join(scope, nativeName);
  const binaryName = readdirSync(nativeSource).find((file) => file.endsWith(".node"));
  const clone = (name, native = true) => {
    const root = join(scratch, name);
    const packages = join(root, "node_modules", "@qrcode-ai-com"); mkdirSync(packages, { recursive: true });
    cpSync(mainSource, join(packages, "qrcode-barcode-scanner"), { recursive: true });
    if (native) cpSync(nativeSource, join(packages, nativeName), { recursive: true });
    return { root, main: join(packages, "qrcode-barcode-scanner"), native: join(packages, nativeName) };
  };
  const sentinel = (main) => {
    const marker = join(scratch, "dependency-entry-was-executed");
    const entry = join(main, "index.js");
    writeFileSync(entry, `require('node:fs').writeFileSync(${JSON.stringify(marker)}, 'loaded');\n${readFileSync(entry, 'utf8')}`);
    return marker;
  };
  record("ancestor-native-refused-before-main-execution", () => {
    const c = clone("ancestor/project-runtime", false);
    const ancestor = join(scratch, "ancestor/node_modules/@qrcode-ai-com", nativeName); mkdirSync(ancestor, { recursive: true });
    cpSync(nativeSource, ancestor, { recursive: true });
    const marker = sentinel(c.main);
    assert.equal(parse(run(fixture, [], c.root), 2).error.code, "dependency_missing");
    assert.equal(existsSync(marker), false);
  });
  record("main-package-symlink-escape-refused", () => {
    const c = clone("main-link"); rmSync(c.main, { recursive: true });
    symlinkSync(mainSource, c.main, "junction");
    assert.equal(parse(run(fixture, [], c.root), 2).error.code, "dependency_boundary");
  });
  record("native-package-symlink-escape-refused-before-main-execution", () => {
    const c = clone("native-link"); rmSync(c.native, { recursive: true }); symlinkSync(nativeSource, c.native, "junction");
    const marker = sentinel(c.main);
    assert.equal(parse(run(fixture, [], c.root), 2).error.code, "dependency_boundary");
    assert.equal(existsSync(marker), false);
  });
  record("native-binary-symlink-escape-refused", () => {
    const c = clone("binary-link"); rmSync(join(c.native, binaryName)); symlinkSync(join(nativeSource, binaryName), join(c.native, binaryName), "file");
    assert.equal(parse(run(fixture, [], c.root), 2).error.code, "dependency_boundary");
  });
  record("native-manifest-symlink-escape-refused", () => {
    const c = clone("native-manifest-link"); rmSync(join(c.native, "package.json")); symlinkSync(join(nativeSource, "package.json"), join(c.native, "package.json"), "file");
    assert.equal(parse(run(fixture, [], c.root), 2).error.code, "dependency_boundary");
  });
  record("main-entry-symlink-escape-refused", () => {
    const c = clone("main-entry-link"); rmSync(join(c.main, "index.js")); symlinkSync(join(mainSource, "index.js"), join(c.main, "index.js"), "file");
    assert.equal(parse(run(fixture, [], c.root), 2).error.code, "dependency_boundary");
  });
  record("native-loader-symlink-escape-refused", () => {
    const c = clone("native-loader-link"); rmSync(join(c.main, "native.js")); symlinkSync(join(mainSource, "native.js"), join(c.main, "native.js"), "file");
    assert.equal(parse(run(fixture, [], c.root), 2).error.code, "dependency_boundary");
  });
  record("input-image-symlink-supported", () => {
    const image = join(scratch, "image-symlink.png"); symlinkSync(fixture, image, "file");
    assert.equal(parse(run(image, ["--profile", "frame"]), 0).detections[0].content.text, "https://qrcode-ai.com/c/v5q");
  });
  const large = join(scratch, "large.png"); writeFileSync(large, ""); truncateSync(large, 10 * 1024 * 1024 + 1);
  record("encoded-input-size-cap", () => assert.equal(parse(run(large), 2).error.code, "input_size"));
  const wide = join(scratch, "wide.png"); writeFileSync(wide, whitePng(4097, 1));
  record("decoded-dimension-cap", () => assert.match(parse(run(wide), 2).error.message, /QRS-002/));
  const pixels = join(scratch, "pixels.png"); writeFileSync(pixels, whitePng(4096, 4096));
  record("decoded-pixel-cap", () => assert.match(parse(run(pixels), 2).error.message, /QRS-003/));
  record("nonregular-input-refused", () => assert.equal(parse(run(scratch), 2).error.code, "input_file"));
  record("invalid-profile-refused", () => assert.equal(parse(run(fixture, ["--profile", "faster"]), 2).error.code, "usage"));
  record("special-filename-is-data", () => {
    const image = join(scratch, "-- image ; $(touch injected) `touch injected2` ' quote.png");
    copyFileSync(fixture, image);
    assert.equal(parse(run(image, ["--profile", "frame"]), 0).detections[0].content.text, "https://qrcode-ai.com/c/v5q");
    assert.equal(existsSync(join(scratch, "injected")), false);
    assert.equal(existsSync(join(scratch, "injected2")), false);
  });
  console.log(JSON.stringify({ helper: "qrcode-barcode-scanner", version: "0.2.0", engine: "0.11.0", node: process.version, checks }));
} finally { rmSync(scratch, { recursive: true, force: true }); }
