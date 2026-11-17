const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const {
  collect,
  validateSource,
  retainedProjects,
  fail,
  text,
  date,
} = require("./adapters");
const LIMIT = 1024 * 1024;
const BASE = "state/command-center";
const SELECTION = `${BASE}/project-sources.json`;
function guarded(root, relative, mkdir = false) {
  if (
    typeof relative !== "string" ||
    !relative ||
    path.isAbsolute(relative) ||
    relative.includes("\\") ||
    relative.split("/").some((p) => !p || p === "." || p === "..")
  )
    fail("UNSAFE_PATH");
  let current = root;
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
      if (i === parts.length - 1 && !stat.isFile() && !stat.isDirectory())
        fail("INVALID_FILE");
    } catch (e) {
      if (e.code !== "ENOENT") throw e;
      if (mkdir && i < parts.length - 1) fs.mkdirSync(current, { mode: 0o700 });
    }
  }
  return current;
}
function read(root, relative, limit = LIMIT) {
  const file = guarded(root, relative);
  let fd;
  try {
    if (!fs.lstatSync(file).isFile()) fail("INVALID_FILE");
    fd = fs.openSync(
      file,
      fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW | fs.constants.O_NONBLOCK,
    );
    const st = fs.fstatSync(fd);
    if (!st.isFile() || st.size > limit) fail("INPUT_LIMIT");
    const buffer = Buffer.alloc(limit + 1);
    let count = 0,
      n;
    while (
      (n = fs.readSync(fd, buffer, count, buffer.length - count, null)) > 0
    ) {
      count += n;
      if (count > limit) fail("INPUT_LIMIT");
    }
    return buffer.toString("utf8", 0, count);
  } catch (e) {
    if (e.code === "ENOENT") return null;
    throw e;
  } finally {
    if (fd !== undefined) fs.closeSync(fd);
  }
}
function atomic(root, relative, value) {
  const encoded = JSON.stringify(value, null, 2) + "\n";
  if (Buffer.byteLength(encoded) > LIMIT) fail("OUTPUT_LIMIT");
  const dest = guarded(root, relative, true);
  const tmp = `${dest}.${crypto.randomUUID()}.tmp`;
  try {
    fs.writeFileSync(tmp, encoded, { flag: "wx", mode: 0o600 });
    guarded(root, relative);
    fs.renameSync(tmp, dest);
  } finally {
    if (fs.existsSync(tmp)) fs.unlinkSync(tmp);
  }
}
function identity(value, config) {
  if (value.profile !== config.profile || value.agentId !== config.agentId)
    fail("IDENTITY_MISMATCH");
}
function validateConfig(config) {
  if (
    !config ||
    config.schemaVersion !== 1 ||
    typeof config.agentId !== "string" ||
    !/^[a-zA-Z0-9_-]{0,64}$/.test(config.profile) ||
    typeof config.profile !== "string" ||
    !/^[a-zA-Z0-9_-]{1,64}$/.test(config.agentId) ||
    !Array.isArray(config.sources) ||
    config.sources.length > 8
  )
    fail("INVALID_CONFIG");
  const ids = new Set();
  for (const s of config.sources) {
    validateSource(s);
    if (ids.has(s.id)) fail("DUPLICATE_SOURCE");
    ids.add(s.id);
    if (s.enabled && typeof s.input !== "string") fail("INPUT_REQUIRED");
  }
}
function previousSnapshot(root, source, config) {
  const previous = read(root, `${BASE}/projects/${source.id}.json`);
  if (!previous) return null;
  const parsed = JSON.parse(previous);
  identity(parsed, config);
  if (parsed.sourceId !== source.id || parsed.provider !== source.provider)
    fail("SOURCE_MISMATCH");
  if (!["ready", "partial", "error", "unavailable"].includes(parsed.status))
    fail("INVALID_PREVIOUS");
  return { ...parsed, projects: retainedProjects(parsed) };
}
function sourceError(snapshot) {
  snapshot.status = "error";
  snapshot.projects = [];
}
async function run(args) {
  const command = args[0];
  const opts = {};
  if (!["preview", "apply"].includes(command)) fail("USAGE");
  for (let i = 1; i < args.length; i += 2) {
    const key = { "--workspace": "workspace", "--config": "config" }[args[i]];
    if (!key || opts[key] || !args[i + 1]) fail("USAGE");
    opts[key] = args[i + 1];
  }
  if (!opts.workspace || !opts.config) fail("USAGE");
  const root = path.resolve(opts.workspace);
  if (fs.realpathSync(root) !== root || !fs.lstatSync(root).isDirectory())
    fail("UNSAFE_WORKSPACE");
  const config = JSON.parse(read(root, opts.config, 64 * 1024));
  validateConfig(config);
  const old = read(root, SELECTION, 64 * 1024);
  if (old) identity(JSON.parse(old), config);
  const selection = {
    schemaVersion: 1,
    profile: config.profile,
    agentId: config.agentId,
    sources: config.sources.map((s) => ({
      id: s.id,
      provider: s.provider,
      label: text(s.label),
      enabled: s.enabled,
    })),
  };
  const snapshots = [];
  const skipWrites = new Set();
  for (const source of config.sources) {
    if (!source.enabled) continue;
    let snapshot;
    let missing = false;
    try {
      const input = read(root, source.input);
      missing = input === null;
      if (missing) fail("MISSING_EXPORT");
      const exported = JSON.parse(input);
      if (
        !exported ||
        !date(exported.observedAt) ||
        Date.parse(exported.observedAt) > Date.now() + 60000 ||
        !Array.isArray(exported.pages) ||
        !exported.pages.length ||
        exported.pages.length > 10
      )
        fail("INVALID_EXPORT");
      let page = 0;
      snapshot = await collect({
        source,
        profile: config.profile,
        agentId: config.agentId,
        observedAt: exported.observedAt,
        request: async () => {
          if (page >= exported.pages.length) fail("INCOMPLETE_EXPORT");
          return exported.pages[page++];
        },
      });
      if (snapshot.status === "ready" && page < exported.pages.length)
        fail("UNEXPECTED_EXPORT_PAGES");
    } catch {
      snapshot = {
        schemaVersion: 1,
        sourceId: source.id,
        provider: source.provider,
        profile: config.profile,
        agentId: config.agentId,
        observedAt: new Date().toISOString(),
        status: missing ? "unavailable" : "error",
        projects: [],
      };
    }
    try {
      const previous = previousSnapshot(root, source, config);
      if (previous && ["error", "unavailable"].includes(snapshot.status)) {
        snapshot.projects = previous.projects;
        snapshot.observedAt = previous.observedAt;
      }
    } catch {
      // Never retain or overwrite corrupt/foreign data; only this source fails.
      skipWrites.add(source.id);
      sourceError(snapshot);
    }
    snapshots.push(snapshot);
  }
  const result = {
    mode: "offline-import",
    liveSyncConfigured: false,
    selection,
    snapshots,
  };
  if (command === "preview") return result;
  const lock = guarded(root, `${BASE}/.project-import-lock`, true);
  try {
    fs.mkdirSync(lock, { mode: 0o700 });
  } catch (e) {
    if (e.code === "EEXIST") fail("BUSY");
    throw e;
  }
  try {
    if (read(root, SELECTION, 64 * 1024) !== old) fail("SELECTION_CHANGED");
    for (const snapshot of snapshots) {
      try {
        previousSnapshot(
          root,
          { id: snapshot.sourceId, provider: snapshot.provider },
          config,
        );
        if (Buffer.byteLength(JSON.stringify(snapshot, null, 2) + "\n") > LIMIT)
          fail("OUTPUT_LIMIT");
      } catch {
        skipWrites.add(snapshot.sourceId);
        sourceError(snapshot);
      }
    }
    for (const snapshot of snapshots) {
      if (skipWrites.has(snapshot.sourceId)) continue;
      try {
        atomic(root, `${BASE}/projects/${snapshot.sourceId}.json`, snapshot);
      } catch {
        skipWrites.add(snapshot.sourceId);
        sourceError(snapshot);
      }
    }
    // Publish selection last. Atomicity is per file, not across all sources.
    atomic(root, SELECTION, selection);
    return {
      ...result,
      status: skipWrites.size ? "partial" : "applied",
      skippedSources: [...skipWrites],
    };
  } finally {
    fs.rmdirSync(lock);
  }
}
module.exports = { run, read, guarded, validateConfig };
