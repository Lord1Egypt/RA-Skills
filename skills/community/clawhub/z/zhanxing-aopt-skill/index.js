var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// src/index.ts
var import_child_process = require("child_process");
var path = __toESM(require("path"));
var ID_PATTERN = /^Z\d{2}$/;
function isValidId(id) {
  return ID_PATTERN.test(id);
}
function helperName() {
  return process.platform === "win32" ? "scheduler.exe" : "scheduler";
}
async function runCheck(id, dryRun = false) {
  if (!isValidId(id)) {
    return { id, ok: false, blocked: false, output: "", error: "invalid id (expected Z01..Z20)" };
  }
  const bin = path.join(__dirname, "bin", helperName());
  const args = [id];
  if (dryRun) args.push("--dry-run");
  return new Promise((resolve) => {
    const child = (0, import_child_process.spawn)(bin, args);
    let out = "";
    let err = "";
    child.stdout.on("data", (d) => out += d.toString());
    child.stderr.on("data", (d) => err += d.toString());
    child.on("error", (e) => {
      resolve({ id, ok: false, blocked: false, output: "", error: e.message });
    });
    child.on("close", () => {
      const text = out || err;
      try {
        const r = JSON.parse(text);
        resolve({
          id: r.id || id,
          ok: !!r.ok,
          blocked: !!r.blocked,
          output: String(r.output || ""),
          error: String(r.error || "")
        });
      } catch {
        resolve({ id, ok: false, blocked: false, output: text, error: "" });
      }
    });
  });
}
async function runAllChecks(dryRun = false) {
  const ids = Array.from({ length: 20 }, (_, i) => "Z" + String(i + 1).padStart(2, "0"));
  const results = [];
  for (const id of ids) {
    results.push(await runCheck(id, dryRun));
  }
  return results;
}
function printDiagnostics(results) {
  console.log("\n=== Diagnostics ===\n");
  for (const r of results) {
    const status = r.ok ? "PASS" : r.blocked ? "BLOCK" : "FAIL";
    console.log(`[${status}] ${r.id}`);
    if (r.output) console.log("  output:", r.output.slice(0, 200).replace(/\n/g, " "));
    if (r.error) console.log("  error:", r.error.slice(0, 200).replace(/\n/g, " "));
  }
  const total = results.length;
  const blocked = results.filter((r) => r.blocked).length;
  const passed = results.filter((r) => r.ok).length;
  const failed = total - blocked - passed;
  console.log(`
=== Result: ${passed} pass, ${blocked} block, ${failed} fail / ${total} total ===`);
}
async function main() {
  const argv = process.argv.slice(2);
  const dryRun = argv.includes("--dry-run");
  const all = argv.includes("--all") || argv.length === 0 || argv.length === 1 && dryRun;
  if (all) {
    const results = await runAllChecks(dryRun);
    printDiagnostics(results);
    return;
  }
  const id = argv.find((a) => !a.startsWith("--"));
  if (id) {
    const r = await runCheck(id, dryRun);
    printDiagnostics([r]);
  }
}
if (require.main === module) {
  main().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}
