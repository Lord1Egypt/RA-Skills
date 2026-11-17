const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const collectors = require("./collectors");
const ROOT = path.resolve(__dirname, "../..");
const BASE = "state/command-center";
const SELECTION = `${BASE}/extensions.json`;
const LIMIT = 256 * 1024;
const SELECTION_LIMIT = 16 * 1024;
const fail = (code) => {
  throw Object.assign(new Error(code), { code: `FLAVOR_${code}` });
};
function guarded(workspace, relative, mkdir = false) {
  if (
    path.isAbsolute(relative) ||
    relative.split(/[\\/]/).some((p) => p === ".." || p === ".")
  )
    fail("UNSAFE_PATH");
  let current = workspace;
  const parts = relative.split("/");
  for (let i = 0; i < parts.length; i++) {
    current = path.join(current, parts[i]);
    try {
      const stat = fs.lstatSync(current);
      if (
        stat.isSymbolicLink() ||
        (i < parts.length - 1 && !stat.isDirectory())
      )
        fail("UNSAFE_PATH");
    } catch (e) {
      if (e.code !== "ENOENT") throw e;
      if (mkdir && i < parts.length - 1) fs.mkdirSync(current, { mode: 0o700 });
    }
  }
  return current;
}
function read(workspace, relative, limit = LIMIT) {
  const file = guarded(workspace, relative);
  let fd;
  try {
    if (!fs.lstatSync(file).isFile()) fail("INVALID_INPUT_TYPE");
    fd = fs.openSync(
      file,
      fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW | fs.constants.O_NONBLOCK,
    );
    const stat = fs.fstatSync(fd);
    if (!stat.isFile() || stat.size > limit) fail("INPUT_LIMIT");
    const data = Buffer.alloc(limit + 1);
    let total = 0,
      n;
    while ((n = fs.readSync(fd, data, total, data.length - total, null)) > 0) {
      total += n;
      if (total > limit) fail("INPUT_LIMIT");
    }
    return { text: data.toString("utf8", 0, total), stat };
  } catch (e) {
    if (e.code === "ENOENT") return null;
    throw e;
  } finally {
    if (fd !== undefined) fs.closeSync(fd);
  }
}
function atomic(workspace, relative, text) {
  if (Buffer.byteLength(text) > LIMIT) fail("OUTPUT_LIMIT");
  const dest = guarded(workspace, relative, true);
  const temp = `${dest}.${crypto.randomUUID()}.tmp`;
  try {
    fs.writeFileSync(temp, text, { flag: "wx", mode: 0o600 });
    fs.renameSync(temp, dest);
  } finally {
    if (fs.existsSync(temp)) fs.unlinkSync(temp);
  }
}
const encode = (value) => JSON.stringify(value, null, 2) + "\n";
function identity(value, opts) {
  if (value.profile !== opts.profile || value.agentId !== opts.agentId)
    fail("IDENTITY_MISMATCH");
}
function validateSelection(value, opts, ids) {
  if (
    !value ||
    value.schemaVersion !== 1 ||
    !["legacy", "core", "extensions"].includes(value.mode) ||
    !Array.isArray(value.enabled)
  )
    fail("INVALID_SELECTION");
  identity(value, opts);
  if (
    value.enabled.length > ids.length ||
    new Set(value.enabled.map((x) => x.id)).size !== value.enabled.length
  )
    fail("INVALID_SELECTION");
  for (const item of value.enabled)
    if (!ids.includes(item.id) || item.version !== "1.0.0")
      fail("INCOMPATIBLE_PACKAGE");
}
function validateManifest(m, id) {
  const expectedInput =
    id === "spacesuit.monetization"
      ? ["intel/MONETIZATION-TRACKER.md"]
      : id === "spacesuit.pipeline"
        ? ["intel/*PIPELINE*.md", "intel/*QUEUE*.md"]
        : ["intel/*.md"];
  if (
    !m ||
    m.schemaVersion !== 1 ||
    m.id !== id ||
    m.version !== "1.0.0" ||
    m.contractVersion !== 1 ||
    !Array.isArray(m.locales) ||
    m.locales.length !== 2 ||
    new Set(m.locales).size !== 2 ||
    !m.locales.includes("en") ||
    !m.locales.includes("zh-CN") ||
    JSON.stringify(m.inputs) !== JSON.stringify(expectedInput) ||
    m.collection !== "explicit-reviewed-cli" ||
    "command" in m ||
    "script" in m
  )
    fail("INVALID_PACKAGE");
}
function packageInfo() {
  const flavor = JSON.parse(
    fs.readFileSync(
      path.join(ROOT, "flavors/business-operations/manifest.json"),
      "utf8",
    ),
  );
  const ids = [
    "spacesuit.intel",
    "spacesuit.pipeline",
    "spacesuit.monetization",
  ];
  if (
    flavor.schemaVersion !== 1 ||
    flavor.id !== "business-operations" ||
    flavor.version !== "1.0.0" ||
    JSON.stringify(flavor.extensions) !==
      JSON.stringify(ids.map((id) => ({ id, version: "1.0.0" })))
  )
    fail("INVALID_PACKAGE");
  for (const id of ids) {
    const m = JSON.parse(
      fs.readFileSync(
        path.join(ROOT, "extensions", id, "manifest.json"),
        "utf8",
      ),
    );
    validateManifest(m, id);
  }
  return { flavor, ids };
}
function inputs(workspace, extension) {
  // Exact-file collectors must not inspect unrelated directory entries or contents.
  if (extension === "monetization") {
    const name = "MONETIZATION-TRACKER.md";
    const data = read(workspace, `intel/${name}`);
    return data
      ? [{ name, content: data.text, mtimeMs: data.stat.mtimeMs }]
      : null;
  }
  const directory = guarded(workspace, "intel");
  let dir;
  try {
    dir = fs.opendirSync(directory);
  } catch (e) {
    if (e.code === "ENOENT") return null;
    throw e;
  }
  const files = [];
  let count = 0;
  let bytes = 0;
  try {
    let entry;
    while ((entry = dir.readSync())) {
      if (++count > 200) fail("INPUT_LIMIT");
      if (!entry.name.endsWith(".md")) continue;
      if (extension === "pipeline" && !/PIPELINE|QUEUE/i.test(entry.name))
        continue;
      if (entry.isSymbolicLink()) fail("UNSAFE_PATH");
      if (!entry.isFile()) fail("INVALID_INPUT_TYPE");
      const data = read(workspace, `intel/${entry.name}`);
      if (!data) fail("INPUT_CHANGED");
      bytes += Buffer.byteLength(data.text);
      if (bytes > 1024 * 1024 || files.length >= 100) fail("INPUT_LIMIT");
      files.push({
        name: entry.name,
        content: data.text,
        mtimeMs: data.stat.mtimeMs,
      });
    }
  } finally {
    dir.closeSync();
  }
  return files.sort((a, b) => b.mtimeMs - a.mtimeMs);
}
function parseArgs(args) {
  const command = args[0];
  if (!["preview", "apply", "disable", "restore", "collect"].includes(command))
    fail("USAGE");
  const opts = {
    command,
    profile: "",
    agentId: "main",
    flavor: "business-operations",
  };
  const keys = {
    "--workspace": "workspace",
    "--profile": "profile",
    "--agent": "agentId",
    "--flavor": "flavor",
    "--backup": "backup",
  };
  const seen = new Set();
  for (let i = 1; i < args.length; i += 2) {
    const key = keys[args[i]];
    if (!key || args[i + 1] === undefined || seen.has(key)) fail("USAGE");
    seen.add(key);
    opts[key] = args[i + 1];
  }
  if (
    !opts.workspace ||
    opts.flavor !== "business-operations" ||
    !/^[a-zA-Z0-9_-]{0,64}$/.test(opts.profile) ||
    !/^[a-zA-Z0-9_-]{1,64}$/.test(opts.agentId)
  )
    fail("USAGE");
  if (opts.backup && !/^[a-f0-9-]{36}\.json$/.test(opts.backup))
    fail("INVALID_BACKUP");
  if ((command === "restore") !== !!opts.backup) fail("USAGE");
  opts.workspace = path.resolve(opts.workspace);
  if (
    fs.lstatSync(opts.workspace).isSymbolicLink() ||
    !fs.statSync(opts.workspace).isDirectory() ||
    fs.realpathSync(opts.workspace) !== opts.workspace
  )
    fail("UNSAFE_WORKSPACE");
  return opts;
}
function run(args) {
  const opts = parseArgs(args);
  const { ids, flavor } = packageInfo();
  const w = opts.workspace;
  const old = read(w, SELECTION, SELECTION_LIMIT);
  let current = null;
  if (old) {
    try {
      current = JSON.parse(old.text);
    } catch (error) {
      if (opts.command !== "restore") throw error;
    }
    if (opts.command === "restore") {
      // Recovery may replace corrupt selection bytes, but not another identified instance.
      if (
        current &&
        typeof current.profile === "string" &&
        typeof current.agentId === "string"
      )
        identity(current, opts);
    } else validateSelection(current, opts, ids);
  }
  const next = {
    ...(current && typeof current === "object" && !Array.isArray(current)
      ? current
      : {}),
    schemaVersion: 1,
    profile: opts.profile,
    agentId: opts.agentId,
    mode: opts.command === "disable" ? "core" : "extensions",
    enabled: opts.command === "disable" ? [] : flavor.extensions,
  };
  if (opts.command === "preview")
    return {
      changes: !current || encode(current) !== encode(next),
      before: current,
      after: next,
      collection: "explicit-only",
    };
  if (opts.command === "collect" && (!current || current.mode !== "extensions"))
    fail("COLLECTION_DISABLED");
  if (
    opts.command !== "restore" &&
    Buffer.byteLength(encode(next)) > SELECTION_LIMIT
  )
    fail("OUTPUT_LIMIT");
  const lock = guarded(w, `${BASE}/.flavor-lock`, true);
  try {
    fs.mkdirSync(lock, { mode: 0o700 });
  } catch (e) {
    if (e.code === "EEXIST") fail("BUSY");
    throw e;
  }
  try {
    // Refuse stale read-modify-write even if another invocation finished before lock acquisition.
    if (read(w, SELECTION, SELECTION_LIMIT)?.text !== old?.text)
      fail("SELECTION_CHANGED");
    if (opts.command === "collect") {
      if (!current || current.mode !== "extensions")
        fail("COLLECTION_DISABLED");
      const observedAt = new Date().toISOString();
      const snapshots = [];
      for (const item of current.enabled) {
        const short = item.id.split(".")[1];
        let panels = null;
        let inputError = false;
        try {
          const files = inputs(w, short);
          panels = files ? collectors[short](files, Date.now()) : null;
        } catch {
          inputError = true;
        }
        const snapshot = {
          schemaVersion: 1,
          ...item,
          profile: opts.profile,
          agentId: opts.agentId,
          observedAt,
          status: inputError ? "error" : panels ? "ready" : "unavailable",
          panels: panels || [],
        };
        const target = `${BASE}/extensions/${item.id}.json`;
        const previous = read(w, target);
        if (previous) identity(JSON.parse(previous.text), opts);
        snapshots.push({ target, snapshot, text: encode(snapshot) });
      }
      if (snapshots.some((s) => Buffer.byteLength(s.text) > LIMIT))
        fail("OUTPUT_LIMIT");
      for (const s of snapshots) atomic(w, s.target, s.text);
      return {
        status: snapshots.some((s) => s.snapshot.status === "error")
          ? "error"
          : "collected",
        items: snapshots.map((s) => ({
          id: s.snapshot.id,
          status: s.snapshot.status,
        })),
      };
    }
    let restored;
    if (opts.command === "restore") {
      const backup = read(w, `${BASE}/backups/${opts.backup}`);
      if (!backup) fail("INVALID_BACKUP");
      restored = JSON.parse(backup.text);
      identity(restored, opts);
      if (
        restored.schemaVersion !== 1 ||
        !(restored.selection === null || typeof restored.selection === "string")
      )
        fail("INVALID_BACKUP");
      if (restored.selection !== null) {
        if (Buffer.byteLength(restored.selection) > SELECTION_LIMIT)
          fail("INVALID_BACKUP");
        validateSelection(JSON.parse(restored.selection), opts, ids);
      }
    }
    const destination =
      opts.command === "restore" ? restored.selection : encode(next);
    if ((old?.text ?? null) === destination) return { status: "unchanged" };
    const backupId = `${crypto.randomUUID()}.json`;
    atomic(
      w,
      `${BASE}/backups/${backupId}`,
      encode({
        schemaVersion: 1,
        profile: opts.profile,
        agentId: opts.agentId,
        selection: old?.text ?? null,
      }),
    );
    if (destination === null) {
      if (old) fs.unlinkSync(guarded(w, SELECTION));
    } else atomic(w, SELECTION, destination);
    return {
      status: opts.command === "restore" ? "restored" : "applied",
      mode:
        destination === null ? "legacy-default" : JSON.parse(destination).mode,
      backup: backupId,
    };
  } finally {
    fs.rmdirSync(lock);
  }
}
module.exports = {
  run,
  parseArgs,
  validateManifest,
  parseTables: collectors.parseTables,
  hasPositiveRevenue: collectors.hasPositiveRevenue,
};
