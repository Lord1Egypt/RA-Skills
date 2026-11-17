// SPDX-License-Identifier: MIT-0
import { closeSync, constants, fstatSync, openSync, readFileSync, readSync, realpathSync, statSync } from "node:fs";
import { createRequire } from "node:module";
import { isAbsolute, join, relative, resolve } from "node:path";

const ENGINE = "@qrcode-ai-com/qrcode-barcode-scanner";
const VERSION = "0.11.0";
const MAX_BYTES = 10 * 1024 * 1024;

class InputError extends Error {
  constructor(code, message) { super(message); this.code = code; }
}

function options(args) {
  const values = { profile: "full", budgetMs: 2000 };
  let index = 0;
  for (; index < args.length && args[index] !== "--"; index += 2) {
    const key = args[index];
    const value = args[index + 1];
    if (!value || value === "--") throw new InputError("usage", `Missing value for ${key}`);
    if (key === "--engine-root") values.engineRoot = resolve(value);
    else if (key === "--profile" && ["full", "fast", "frame"].includes(value)) values.profile = value;
    else if (key === "--budget-ms" && /^(0|[1-9][0-9]*)$/.test(value) && Number(value) <= 10000) values.budgetMs = Number(value);
    else throw new InputError("usage", "Expected --engine-root, --profile full|fast|frame, or --budget-ms 0..10000");
  }
  if (!values.engineRoot || args[index] !== "--" || args.length !== index + 2) {
    throw new InputError("usage", "Usage: node scan.mjs --engine-root DIRECTORY [--profile full|fast|frame] [--budget-ms 0..10000] -- IMAGE");
  }
  values.image = resolve(args[index + 1]);
  return values;
}

function contained(root, path, label, regular = false) {
  let canonical;
  try { canonical = realpathSync(path); }
  catch { throw new InputError("dependency_missing", `Missing ${label} in the explicit engine runtime directory`); }
  const tail = relative(root, canonical);
  if (tail === ".." || tail.startsWith(`..${process.platform === "win32" ? "\\" : "/"}`) || isAbsolute(tail)) {
    throw new InputError("dependency_boundary", `${label} resolves outside the explicit engine runtime directory`);
  }
  if (regular && !statSync(canonical).isFile()) throw new InputError("dependency_boundary", `${label} must be a regular file`);
  return canonical;
}

function nativeTarget() {
  if (process.platform === "darwin" && ["arm64", "x64"].includes(process.arch)) return `darwin-${process.arch}`;
  if (process.platform === "win32" && process.arch === "x64" && process.config.variables.shlib_suffix !== "dll.a" && process.config.variables.node_target_type !== "shared_library") return "win32-x64-msvc";
  if (process.platform === "linux" && ["arm64", "x64"].includes(process.arch)) {
    if (process.report) process.report.excludeNetwork = true;
    const libc = process.report?.getReport()?.header?.glibcVersionRuntime ? "gnu" : "musl";
    if (process.arch === "arm64" && libc === "musl") throw new InputError("dependency_platform", "Linux ARM64 musl is not a published engine 0.11.0 target");
    return `linux-${process.arch}-${libc}`;
  }
  throw new InputError("dependency_platform", "This Node runtime is not one of the six published engine 0.11.0 native targets");
}

function manifest(path, name) {
  let value;
  try { value = JSON.parse(readFileSync(path, "utf8")); }
  catch { throw new InputError("dependency_load", `Cannot read ${name} package metadata`); }
  if (value.name !== name || value.version !== VERSION) {
    throw new InputError("dependency_version", `Expected ${name}@${VERSION}; found ${String(value.name)}@${String(value.version)}`);
  }
  return value;
}

function loadEngine(root) {
  let canonicalRoot;
  try { canonicalRoot = realpathSync(root); }
  catch { throw new InputError("dependency_missing", `Install ${ENGINE}@${VERSION} in the explicit engine runtime directory`); }
  const directory = contained(canonicalRoot, join(canonicalRoot, "node_modules", "@qrcode-ai-com", "qrcode-barcode-scanner"), "main engine package");
  const mainManifest = contained(canonicalRoot, join(directory, "package.json"), "main engine manifest", true);
  const mainPackage = manifest(mainManifest, ENGINE);
  if (mainPackage.main !== "index.js") throw new InputError("dependency_load", "Unexpected main engine entry");
  const entry = contained(canonicalRoot, join(directory, "index.js"), "main engine entry", true);
  contained(canonicalRoot, join(directory, "native.js"), "main engine native loader", true);
  if (process.env.NAPI_RS_NATIVE_LIBRARY_PATH || process.env.NAPI_RS_FORCE_WASI) {
    throw new InputError("dependency_override", "Native library and WASI overrides are not supported");
  }
  const target = nativeTarget();
  const name = `${ENGINE}-${target}`;
  const nativeDirectory = contained(canonicalRoot, join(canonicalRoot, "node_modules", "@qrcode-ai-com", `qrcode-barcode-scanner-${target}`), "native engine package");
  const nativeManifest = manifest(contained(canonicalRoot, join(nativeDirectory, "package.json"), "native engine manifest", true), name);
  const binaryName = `qrcode-barcode-scanner.${target}.node`;
  if (nativeManifest.main !== binaryName) throw new InputError("dependency_load", "Unexpected native engine entry");
  const binary = contained(canonicalRoot, join(nativeDirectory, binaryName), "native engine binary", true);
  const require = createRequire(mainManifest);
  let native;
  try { native = require(binary); }
  catch { throw new InputError("dependency_load", "The pinned native engine cannot load on this runtime/platform; reinstall its exact dependency"); }
  if (native.version() !== VERSION) throw new InputError("dependency_version", `Loaded engine must be ${VERSION}`);
  // Prove the validated binary loads before invoking the public JS wrapper.
  // Its controlled override then cannot silently choose an ancestor/universal
  // package. These environment changes affect only this helper process.
  process.env.NAPI_RS_NATIVE_LIBRARY_PATH = binary;
  process.env.NAPI_RS_ENFORCE_VERSION_CHECK = "1";
  let engine;
  try { engine = require(entry); }
  catch { throw new InputError("dependency_load", "The pinned public engine wrapper cannot load"); }
  if (engine.version() !== VERSION || require.cache[binary]?.exports !== native || Object.keys(require.cache).some((path) => path.endsWith(".node") && path !== binary)) {
    throw new InputError("dependency_boundary", "The public engine wrapper loaded an unexpected native dependency");
  }
  return engine;
}

function readImage(path) {
  let fd;
  try {
    fd = openSync(path, constants.O_RDONLY | (constants.O_NONBLOCK ?? 0));
    const stat = fstatSync(fd);
    if (!stat.isFile()) throw new InputError("input_file", "The image must be a regular local file");
    if (stat.size > MAX_BYTES) throw new InputError("input_size", "The image exceeds the 10 MiB input limit");
    // Read at most limit+1 even if a file grows after fstat, rather than trusting
    // its initial size or letting readFile allocate an unbounded buffer.
    const buffer = Buffer.alloc(Math.min(stat.size + 1, MAX_BYTES + 1));
    let length = 0;
    while (length < buffer.length) {
      const count = readSync(fd, buffer, length, buffer.length - length, null);
      if (count === 0) return buffer.subarray(0, length);
      length += count;
    }
    if (length > MAX_BYTES) throw new InputError("input_size", "The image exceeds the 10 MiB input limit");
    const probe = Buffer.alloc(1);
    if (readSync(fd, probe, 0, 1, null) !== 0) throw new InputError("input_changed", "The image grew during reading; retry from a stable local file");
    return buffer.subarray(0, length);
  } catch (error) {
    if (error instanceof InputError) throw error;
    throw new InputError("input_file", `Cannot read local image (${error.code ?? "unknown"})`);
  } finally { if (fd !== undefined) closeSync(fd); }
}

try {
  if (Number(process.versions.node.split(".")[0]) < 22) throw new InputError("runtime", "Node.js 22 or later is required");
  const args = options(process.argv.slice(2));
  const engine = loadEngine(args.engineRoot);
  const report = await engine.scan(readImage(args.image), {
    profile: args.profile, budgetMs: args.budgetMs, maxDimension: 4096, maxPixels: 16_000_000,
  });
  if (report.versions?.scanner !== VERSION || report.versions.pipeline !== 5 || report.versions.score_contract !== 5) {
    throw new InputError("report_version", "Unexpected scanner report contract; no result emitted");
  }
  process.stdout.write(`${JSON.stringify(report)}\n`);
  process.exitCode = report.detections.length > 0 ? 0 : 1;
} catch (error) {
  process.stderr.write(`${JSON.stringify({ error: { code: error.code ?? "scan", message: error.message } })}\n`);
  process.exitCode = 2;
}
