// workled core: shared MCP client + adapters for every supported client.
//
// Exports (named only - opencode auto-loads EVERY exported function as a
// plugin, so keep this file free of unrelated function exports; per-client
// entry files re-export the single adapter they need). All adapters share the
// same entry shape {id,name,description,register}:
//   opencodeEntry   - opencode adapter (register(ctx) returns hooks)
//   openclawEntry   - openclaw adapter (register(api) hooks api.on events)
//   piEntry         - pi adapter (register(pi) hooks pi.on events)
//
// CLI hook mode for hermes (short-lived, stdin JSON):
//   node index.js hook [--event <name>]
// Reads the hook payload from stdin, maps the event to a state, sends it over
// MCP (awaiting completion so the process stays alive), and prints `{}`.
// The event->state mapping is unified across all hook-based clients.
//
// Works with the workled MCP server over streamable HTTP. Discovery order:
//   WORKLED_MCP_URL env -> opencode config (mcp.*.url).

import { homedir } from "os";
import { join, resolve, dirname } from "path";
import { readFileSync, existsSync } from "fs";
import { fileURLToPath } from "url";
import { execFile } from "child_process";
import { promisify } from "util";
import {
  WRITE_ERROR_REASONS,
  checkWriteAccess,
  stripJsonc,
  hermesHome,
  sleep,
  dshHome,
  traeCnUserDir,
  traeCnHooksHome,
  toPosix,
  persistentEnvVarNames,
} from "./utils.js";

const HOME = homedir();

const execFileAsync = promisify(execFile);

// Per-client install targets — the single source of truth for where each
// client's workled integration lives. skill-install.mjs derives both the
// `--help` text and the plugin-file install logic from it, so a client's
// paths are maintained exactly once. `default` is the fallback used by --help.
//
// Each real client entry carries:
//   mcpPath    - MCP config file path (lazy, so env-derived dirs are fresh)
//   mcpKey     - top-level key holding the server map (mcp / mcpServers / mcp_servers)
//   mcpFormat  - "json" (JSONC tolerated) | "yaml" | "dsh-patch"
//   mcpType    - default `type` for a fresh entry; only for clients requiring
//                explicit transport declaration (opencode/kilo/workbuddy)
//   existMcp   - probe: config file exists AND mentions "workled"
//   pluginPath - where the plugin/hooks artifact lives
//   existPlugin- probe: artifact is actually installed
//   sigDir     - signature dir for detectClient() fallback
//   skillPath  - where SKILL.md lives for this client
//   existSkill - probe: SKILL.md exists in skillPath
//   label/help - for --help rendering
export const CLIENT_TARGETS = {
  opencode: {
    label: "plugin",
    mcpPath: () => join(HOME, ".config", "opencode", "opencode.json"),
    mcpKey: "mcp",
    mcpFormat: "json",
    mcpType: "remote",
    mcpTimeoutMs: 10000,
    procVars: ["OPENCODE_CONFIG", "OPENCODE_HOME"],
    existMcp: (p) => existsSync(p) && fileContains(p, "workled"),
    pluginPath: () => join(HOME, ".config", "opencode", "plugins", "workled.js"),
    existPlugin: (p) => existsSync(p),
    sigDir: () => join(HOME, ".config", "opencode"),
    skillPath: () => join(HOME, ".config", "opencode", "skills", "workled"),
    existSkill: (p) => existsSync(join(p, "SKILL.md")),
  },
  kilo: {
    label: "plugin",
    mcpPath: () => join(HOME, ".config", "kilo", "kilo.json"),
    mcpKey: "mcp",
    mcpFormat: "json",
    mcpType: "remote",
    mcpTimeoutMs: 10000,
    procVars: ["KILO_CONFIG", "KILO_HOME"],
    existMcp: (p) => existsSync(p) && fileContains(p, "workled"),
    pluginPath: () => join(HOME, ".config", "kilo", "plugin", "workled.js"),
    existPlugin: (p) => existsSync(p),
    sigDir: () => join(HOME, ".config", "kilo"),
    skillPath: () => join(HOME, ".config", "kilo", "skills", "workled"),
    existSkill: (p) => existsSync(join(p, "SKILL.md")),
  },
  openclaw: {
    label: "plugin",
    mcpPath: () => join(HOME, ".openclaw", "openclaw.json"),
    // OpenClaw nests its OpenClaw-managed MCP servers under mcp.servers (not
    // directly under `mcp`), and a remote server declares `transport` rather
    // than `type`. mcpNestedPath marks the container the workled server map
    // lives in so write/read/remove all target mcp.servers.<name>.
    mcpNestedPath: ["mcp", "servers"],
    mcpTransport: "streamable-http",
    // openclaw bundle-mcp defaults tool-listing timeout to 1500ms when
    // requestTimeoutMs is absent; a network MCP server (mDNS + HTTP) can
    // take >1s just for DNS. Set 10s so the initial tools/list doesn't
    // race the deadline.
    mcpRequestTimeoutMs: 10000,
    mcpFormat: "json",
    procVars: ["OPENCLAW_HOME"],
    existMcp: (p) => existsSync(p) && fileContains(p, "workled"),
    pluginPath: () => join(HOME, ".openclaw", "plugins", "workled", "index.js"),
    existPlugin: (p) => existsSync(p) && existsSync(join(dirname(p), "openclaw.plugin.json")),
    sigDir: () => join(HOME, ".openclaw"),
    skillPath: () => join(HOME, ".openclaw", "workspace", "skills", "workled"),
    existSkill: (p) => existsSync(join(p, "SKILL.md")),
  },
  hermes: {
    help: "hooks  -> <hermes-home>/config.yaml (~/.hermes on unix, %LOCALAPPDATA%\\hermes on Windows)",
    mcpPath: () => join(hermesHome(), "config.yaml"),
    mcpKey: "mcp_servers",
    mcpFormat: "yaml",
    mcpConnectTimeoutSeconds: 10,
    mcpTimeoutSeconds: 10,
    // HERMES_HOME is filtered out by the persistent-env guard when hermes is
    // installed into the OS env, so it only fires when hermes actually injects
    // it into this process's environment at spawn.
    procVars: ["HERMES_HOME"],
    existMcp: (p) => existsSync(p) && fileContains(p, "workled"),
    pluginPath: () => join(hermesHome(), "config.yaml"),
    existPlugin: (p) => fileContains(p, "workled"),
    sigDir: () => hermesHome(),
    skillPath: () => join(hermesHome(), "skills", "workled"),
    existSkill: (p) => existsSync(join(p, "SKILL.md")),
  },
  pi: {
    label: "extension",
    mcpPath: () => join(HOME, ".pi", "mcp.json"),
    mcpKey: "mcp",
    mcpFormat: "json",
    procVars: ["PI_HOME"],
    existMcp: (p) => existsSync(p) && fileContains(p, "workled"),
    pluginPath: () => join(HOME, ".pi", "agent", "extensions", "workled", "index.ts"),
    existPlugin: (p) => existsSync(p),
    sigDir: () => join(HOME, ".pi"),
    skillPath: () => join(HOME, ".pi", "skills", "workled"),
    existSkill: (p) => existsSync(join(p, "SKILL.md")),
  },
  workbuddy: {
    help: "mcp    -> ~/.workbuddy/mcp.json (mcpServers.workled)   + SKILL.md (protocol already loaded)",
    mcpPath: () => join(HOME, ".workbuddy", "mcp.json"),
    mcpKey: "mcpServers",
    mcpFormat: "json",
    mcpType: "remote",
    // No mcpTimeoutMs here: WorkBuddy's remote MCP client resolves a configured
    // timeout as Math.max(60000, configured) and caps the connect handshake at
    // 60s, so any value <= 60000 is a no-op and shorter values are unreachable.
    // Emitting `timeout` would only advertise a knob that does not exist.
    // (Read out of the client bundle 2026-09-05.)
    procVars: ["WORKBUDDY_HOME"],
    existMcp: (p) => existsSync(p) && fileContains(p, "workled"),
    pluginPath: () => join(HOME, ".workbuddy", "settings.json"),
    existPlugin: (p) => fileContains(p, "workled"),
    sigDir: () => join(HOME, ".workbuddy"),
    skillPath: () => join(HOME, ".workbuddy", "skills", "workled"),
    existSkill: (p) => existsSync(join(p, "SKILL.md")),
  },
  dsh: {
    // Plan B (2026-09-05): the bundle is self-configuring — installDsh copies
    // dsh-plugin/ to <dsh-home>/profiles/web/node_modules/workled and writes the
    // real device url into that copy's patch.yml. Nothing is written to the
    // profile's cordis.patch.yml any more, so both the MCP/config probe and the
    // plugin probe must look at the bundle (the old Plan A path,
    // <dsh-home>/plugins/workled, is dead and no longer installed anywhere).
    help: "bundle -> <dsh-home>/profiles/web/node_modules/workled (patch.yml carries url/config) + registered in <dsh-home>/profiles/web/package.json",
    mcpPath: () => join(dshHome(), "profiles", "web", "node_modules", "workled", "patch.yml"),
    mcpKey: "mcp",
    mcpFormat: "dsh-patch",
    procVars: ["DSH_HOME"],
    existMcp: (p) => existsSync(p) && fileContains(p, "workled"),
    pluginPath: () => join(dshHome(), "profiles", "web", "node_modules", "workled"),
    existPlugin: (p) => existsSync(p) && existsSync(join(p, "patch.yml")),
    sigDir: () => dshHome(),
    skillPath: () => join(dshHome(), "skills", "workled"),
    existSkill: (p) => existsSync(join(p, "SKILL.md")),
  },
  "trae-cn": {
    help: "mcp    -> <user-data>/User/mcp.json (global mcpServers.workled) + hooks -> ~/.trae-cn/hooks.json",
    mcpPath: () => join(traeCnUserDir(), "User", "mcp.json"),
    mcpKey: "mcpServers",
    mcpFormat: "json",
    mcpHeaderTimeoutMs: 10000,
    // trae-cn is a VSCode fork; its IDE process injects TRAE_* brand vars and a
    // VSCODE_IPC_HOOK handle. TRAE_BRAND_NAME / TRAE_JWT_TOKEN_PATH are Trae CN
    // specific (vs. VSCODE_IPC_HOOK which every VSCode fork sets). None of these
    // are ever written to the OS persistent env, so the process-env guard keeps
    // them usable.
    procVars: ["TRAE_BRAND_NAME", "TRAE_JWT_TOKEN_PATH"],
    existMcp: (p) => existsSync(p) && fileContains(p, "workled"),
    pluginPath: () => join(traeCnHooksHome(), "hooks.json"),
    existPlugin: (p) => fileContains(p, "workled"),
    sigDir: () => join(HOME, ".trae-cn"),
    skillPath: () => join(HOME, ".trae-cn", "skills", "workled"),
    existSkill: (p) => existsSync(join(p, "SKILL.md")),
  },
  default: {
    help: "installed (targets: see SKILL.md)",
  },
};

// Normalise every path a CLIENT_TARGETS accessor returns to POSIX ("/") so
// install/status echoes stay uniform on Windows, matching the installer's
// joinP. Only string responses containing a backslash are rewritten; booleans,
// labels, and relative config strings pass through untouched.
for (const clientName of Object.keys(CLIENT_TARGETS)) {
  const target = CLIENT_TARGETS[clientName];
  for (const k of Object.keys(target)) {
    if (typeof target[k] !== "function") continue;
    const fn = target[k];
    target[k] = (...args) => {
      const v = fn(...args);
      return typeof v === "string" && v.includes("\\") ? toPosix(v) : v;
    };
  }
}

// Every client the skill installs to, derived from CLIENT_TARGETS keys.
// `status` accepts an optional `--client <name>` filter that must be one of
// these. To add a client, add a new key to CLIENT_TARGETS above and the matching
// install/uninstall branch in skill-install.mjs + SKILL.md.
export const CLIENTS = Object.keys(CLIENT_TARGETS).filter((k) => k !== "default");

// Helper: does any of this client's `procVars` exist as a live process env
// var AND is absent from the OS persistent env? The persistent-env filter is
// what separates a genuine process injection (spawned by that client) from a
// stale system-level var that lingers in every unrelated terminal.
function hasProcessInjectedSignal(client, persistent) {
  const vars = CLIENT_TARGETS[client]?.procVars;
  if (!vars || !vars.length) return false;
  return vars.some((v) => process.env[v] && !persistent.has(v));
}

// Best-effort detection of the client running this agent, used when no
// explicit `--client` is passed to the installer or `status`. Layered so a
// single-client dev box resolves cleanly, while a box with many stale client
// configs falls back to an explicit `--client` (the reliable cross-client
// path). Returns a CLIENTS member, or null when ambiguous.
//
// Layer 1 reasons from PROCESS environment vars only — and only those that
// are NOT persisted in the OS user/machine env. A var sitting in the registry
// (e.g. a hermes installer writing HERMES_HOME) is inherited by every process
// and carries no signal, so it is ignored. A var present in this process but
// absent from the persistent env can only have come from the agent runtime
// that spawned us, and identifies the client. This keeps detection valid for
// EVERY client (each listed via its `procVars`) without ever trusting a
// system-level leftover.
//
// NOTE: on a machine where several clients have all been installed, every
// client's signature dir / workled MCP entry is present, so detection is
// necessarily ambiguous — callers must then require `--client` (the agent
// already knows its own client name from its system prompt, so it simply
// passes `--client <its-name>`).
export function detectClient() {
  // 1. Process-injected env vars, filtered against the OS persistent env.
  const persistent = persistentEnvVarNames();
  const hits = CLIENTS.filter((c) => hasProcessInjectedSignal(c, persistent));
  if (hits.length === 1) return hits[0];
  if (hits.length > 1) return null; // ambiguous → require --client

  // 2. Existing MCP config (only if exactly ONE client has workled configured).
  const configured = [...new Set(loadMcpServers()
    .filter(s => s.name === "workled")
    .map(s => s.client))];
  if (configured.length === 1) return configured[0];

  // 3. Signature directories (only if exactly ONE client's sigDir exists).
  const byDir = CLIENTS.filter(c => {
    const d = CLIENT_TARGETS[c]?.sigDir?.();
    return d && existsSync(d);
  });
  if (byDir.length === 1) return byDir[0];

  // 4. Detection failed — return null (NO default fallback).
  return null;
}

// Cheap substring probe used by CLIENT_TARGETS.*.pluginPath(); never throws.
function fileContains(path, needle) {
  try {
    return readFileSync(path, "utf8").includes(needle);
  } catch {
    return false;
  }
}

// Per-attempt RPC ceiling in ms, and the single budget the whole send path is
// built on: rpc(), probeReachable() and probeBluetooth() all default to it, and
// the hook's asyncTimeout is derived from it (+2000, see declareAsync).
//
// Deliberately NOT env-tunable — and the reason is measured, not aesthetic:
//   * A hung CONNECT is capped by undici's own connect timeout (~10s), not by
//     this value. Against a black-holed peer the hook process lives ~12.8s
//     whether this is 10000, 20000 or 60000, so raising it buys nothing there.
//   * The one regime it does govern is a peer that accepted the TCP connection
//     and then went silent, which undici lets hang for 300s by default. For a
//     best-effort LED state sync, waiting past this is pointless anyway: the
//     state is already stale and the next hook event supersedes it.
// One hardcoded value keeps the hook's exit bound honest and removes a config
// surface whose failure modes users cannot observe.
const WORKLED_TIMEOUT_MS = 10000;

// Monotonic counter for JSON-RPC request ids. JSON-RPC 2.0 requires a valid
// id on every request (the server echoes it back and rejects a missing or
// null id with -32600), and the firmware rejects duplicate ids within a
// session, so keep ids unique per process even though requests are currently
// single-flight and stateless.
let nextRpcId = 1;

// Fixed patterns treated as "waiting for user input" by the openclaw/pi
// adapters. Covers the common naming conventions used by agent toolkits
// (AskUserQuestion, AskUserConfirm, choose_option, select_choice,
// prompt_input, permission_approval etc.) so input detection fires on
// every interactive tool regardless of client spelling.
export function getInputTools() {
  return ["question", "confirm", "ask", "choose", "select", "prompt", "input", "approval", "questionnaire"];
}

// Input-tool detection for the openclaw/pi adapters. Matches by substring
// (case-insensitive) so tools like "AskUserQuestion" or "ask_question" hit
// the fixed "question" pattern — an exact `includes(name)` would never fire
// for those names and the waiting state would stay dark.
export function isInputTool(name) {
  if (!name || typeof name !== "string") return false;
  return getInputTools().some((t) => name.toLowerCase().includes(t.toLowerCase()));
}

// Decide the effective MCP URL when (re)writing a workled server entry.
// Never downgrade a working URL to the `<device-name>` placeholder: if the
// incoming URL is the placeholder but an existing real URL is present, keep
// the real one. Pure helper shared by skill-install.mjs and the test suite.
export function resolveMergedUrl(existingUrl, incomingUrl) {
  const isPlaceholder = (u) => typeof u === "string" && u.includes("<device-name>");
  return isPlaceholder(incomingUrl) && existingUrl && !isPlaceholder(existingUrl)
    ? existingUrl
    : incomingUrl;
}

// Decide the `type` field for a workled MCP entry when (re)writing config.
// An existing `type` wins (a client may use a different transport spelling or
// the user customized it); otherwise the source's default `type` is applied.
// Returns null when neither exists, so the caller omits the field entirely
// rather than writing an empty `type`. Pure helper shared by skill-install.mjs
// and the test suite.
export function resolveMcpType(existingType, defaultType) {
  if (existingType) return existingType;
  if (defaultType) return defaultType;
  return null;
}

// Pure decision for the status hint. The trae-cn install writes the workled
// server into the GLOBAL MCP config (<user-data>/User/mcp.json), so MCP needs
// only a reload — unless the URL is the <device-name> placeholder, which the
// user must still replace. The lifecycle hooks are written to
// <home>/.trae-cn/hooks.json but must also be enabled manually in
// Settings → Hooks to fire. Returns the reminder text when the trae-cn client
// is in scope (the user filtered to it, or a trae-cn entry is present),
// otherwise "". Accepts an optional list of scanned client entries so a
// trae-cn entry can also trigger the reminder.
export function traeCnReminderText({ clientPrefix = null, clients = [] } = {}) {
  const traeCnFilter = !clientPrefix || String(clientPrefix).startsWith("trae-cn");
  const hasTraeCnEntry =
    Array.isArray(clients) &&
    clients.some((c) => c && c.client && String(c.client).startsWith("trae-cn"));
  if (!(traeCnFilter || hasTraeCnEntry)) return "";
  return "trae-cn: verify the device-name in Settings → MCP (reload to pick up the config) and enable the workled hooks in Settings → Hooks for agent-state tracking.";
}

// Run a child command, retrying once on failure (transient errors, sandbox
// flakiness, or a briefly-blocked powershell). Returns the execFileAsync result
// and only throws after all attempts are exhausted.
async function execWithRetry(cmd, args, opts, maxAttempts = 2) {
  let lastErr;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      return await execFileAsync(cmd, args, opts);
    } catch (err) {
      lastErr = err;
      if (attempt < maxAttempts - 1) {
        await sleep(300);
      }
    }
  }
  throw lastErr;
}

let hookClientPrefix = null;
const seenUserMessages = new Set();
let seenMessagesCleanedAt = Date.now();
const SEEN_MESSAGES_CLEANUP_INTERVAL_MS = 5 * 60 * 1000; // 5 minutes

// Minimal YAML reader for the `mcp_servers:` block in hermes config.yaml.
// Top-level `mcp_servers:` then `  <name>:` then `    key: value` scalars;
// nested lists/objects beyond that are left out (not needed for MCP servers).
function mcpServersFromYaml(text) {
  const lines = text.split("\n");
  const root = {};
  let section = null; // "mcp_servers" when inside the block
  let serverName = null;
  for (const raw of lines) {
    const line = raw.replace(/\r$/, ""); // tolerate CRLF files
    const m = line.match(/^(\s*)(.*)$/);
    if (!m) continue;
    const indent = m[1].length;
    const content = m[2].trim();
    if (content === "" || content.startsWith("#")) continue;
    if (indent === 0) {
      const topKey = content.replace(/:.*$/, "").trim();
      section = topKey === "mcp_servers" ? topKey : null;
      serverName = null;
      continue;
    }
    if (!section) continue;
    if (indent === 2) {
      const name = content.replace(/:\s*$/, "").trim();
      const inline = content.match(/^([^:]+):\s*(.+)$/);
      if (inline) {
        if (!root[name]) root[name] = {};
        root[name][inline[1].trim()] = stripValue(inline[2].trim());
      } else if (content.endsWith(":")) {
        serverName = name;
        if (!root[serverName]) root[serverName] = {};
      }
      continue;
    }
    if (indent >= 4 && serverName) {
      const kv = content.match(/^([^:]+):\s*(.+)$/);
      if (kv && !content.startsWith("-")) {
        root[serverName][kv[1].trim()] = stripValue(kv[2].trim());
      }
    }
  }
  return root;
}

function stripValue(v) {
  if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
    try {
      return JSON.parse(v);
    } catch {
      return v.slice(1, -1);
    }
  }
  if (v === "true") return true;
  if (v === "false") return false;
  if (/^-?\d+(\.\d+)?$/.test(v)) return Number(v);
  return v;
}

// Scan every client's MCP config (via CLIENT_TARGETS) and return the MCP
// servers it declares, each tagged with its source (client + path).
function loadMcpServers() {
  const servers = [];
  for (const client of CLIENTS) {
    const t = CLIENT_TARGETS[client];
    if (!t?.mcpPath) continue;
    const srcPath = t.mcpPath();
    const format = t.mcpFormat;
    const key = t.mcpKey;
    if (format === "dsh-patch") {
      // Same Plan B bundle dir as CLIENT_TARGETS.dsh.pluginPath(); the old
      // <dsh-home>/plugins/workled location belongs to the retired Plan A
      // layout and is never written by installDsh.
      const pluginDir = join(dshHome(), "profiles", "web", "node_modules", "workled");
      const pluginInstalled = existsSync(join(pluginDir, "patch.yml")) && existsSync(join(pluginDir, "src", "index.js"));
      // dsh's MCP file lives inside the bundle (Plan B) and is preserved across
      // uninstall — installDsh rewrites its workled row to nothing rather than
      // deleting it. Mirror pi/opencode semantics: skip the entry entirely
      // when the bundle is missing OR the bundle has no `workled` row. The
      // earlier "push a phantom {url:null, enabled:false}" behavior made status
      // show "dsh is configured but disabled" on a clean machine, which was a
      // false positive that misled diagnosis.
      if (!existsSync(srcPath)) continue;
      let parsed = null;
      try {
        parsed = dshWorkledPluginFromPatch(readFileSync(srcPath, "utf8"));
      } catch {
        // unreadable patch file: skip
        continue;
      }
      if (!parsed) continue;
      servers.push({
        name: "workled",
        client,
        path: srcPath,
        server: {
          url: parsed.url,
          enabled: parsed.enabled !== false,
          type: "remote",
          _dshPluginInstalled: pluginInstalled,
          _dshPatchExists: true,
        },
      });
      continue;
    }
    if (!existsSync(srcPath)) continue;
    try {
      const text = readFileSync(srcPath, "utf8");
      const parsed = format === "yaml" ? mcpServersFromYaml(text) : JSON.parse(stripJsonc(text));
      // JSON server map location: default is the client's top-level mcpKey;
      // a client with mcpNestedPath (e.g. openclaw: mcp.servers) walks down
      // that container path first, then treats the last segment as the map.
      let m;
      if (format !== "yaml" && parsed && typeof parsed === "object" && t.mcpNestedPath) {
        let node = parsed;
        for (const seg of t.mcpNestedPath) node = node && typeof node === "object" ? node[seg] : undefined;
        m = node;
      } else {
        m = format === "yaml" || !parsed || typeof parsed !== "object" ? parsed : parsed[key];
      }
      if (m && typeof m === "object") {
        for (const [name, server] of Object.entries(m)) {
          if (server && typeof server === "object") {
            servers.push({ name, client, path: srcPath, server });
          }
        }
      }
    } catch {
      // unreadable config file: skip
    }
  }
  return servers;
}

// Parse a dsh `cordis.patch.yml` (top-level YAML array of `- insert:` rows)
// and extract the {url, enabled} config from the row whose inserted id is
// `workled` (the native Cordis plugin). Returns null when no such row is
// present. Scalar values use stripValue() for consistency with the hermes parser.
function dshWorkledPluginFromPatch(yamlText) {
  const lines = yamlText.split(/\r?\n/);
  // Accept both indent styles: 4-space "    - id: X" and 6-space "      - id: X".
  const ID_RE = new RegExp(`^\\s{4,6}-\\s*id:\\s*workled\\s*$`);
  let i = 0;
  while (i < lines.length) {
    if (!/^-\s*insert:\s*$/.test(lines[i])) { i++; continue; }
    const start = i + 1;
    let end = start;
    while (end < lines.length && !/^-\s/.test(lines[end])) end++;
    for (let k = start; k < end; k++) {
      if (!ID_RE.test(lines[k])) continue;
      const idIndentMatch = lines[k].match(/^(\s*)/);
      const idIndent = idIndentMatch ? idIndentMatch[1].length : 6;
      let url = null;
      let enabled = undefined;
      let row = k + 1;
      while (row < end) {
        const r = lines[row];
        const lead = r.match(/^(\s*)/);
        if (!lead || r.trim() === "") { row++; continue; }
        if (lead[1].length <= idIndent) break; // next sibling "- id: ..."
        const cfgUrl = r.match(/^\s*url:\s*(.+?)\s*$/);
        if (cfgUrl) url = stripValue(cfgUrl[1].trim());
        const cfgEnabled = r.match(/^\s*enabled:\s*(.+?)\s*$/);
        if (cfgEnabled) enabled = stripValue(cfgEnabled[1].trim());
        row++;
      }
      return { url, enabled };
    }
    i = end;
  }
  return null;
}

// dsh has no user-editable `mcp` map: the workled server is declared inside the
// L1 bundle (<dsh-home>/profiles/web/node_modules/workled/patch.yml) and
// registered in <dsh-home>/profiles/web/package.json. When dsh is targeted but
// no workled entry is found, diagnose that L1 path instead of telling the user
// to edit an `mcp` section this client does not have.
function dshL1Hint() {
  const home = dshHome();
  const bundle = join(home, "profiles", "web", "node_modules", "workled");
  const patch = join(bundle, "patch.yml");
  const skill = join(home, "skills", "workled");
  const scriptDir = dirname(fileURLToPath(import.meta.url));
  const cmd = `node ${JSON.stringify(toPosix(join(scriptDir, "skill-install.mjs")))} install --client dsh`;

  let state;
  if (!existsSync(bundle)) {
    state = `no workled bundle on the dsh L1 standard path (${toPosix(bundle)})`;
  } else if (!existsSync(patch)) {
    state = `bundle dir ${toPosix(bundle)} exists but has no patch.yml`;
  } else {
    state = `bundle at ${toPosix(bundle)} carries no workled row (or is missing src/index.js)`;
  }

  const check = checkWriteAccess([patch, bundle, skill]);
  const perm = check.ok
    ? ""
    : `; L1 path not writable: ${check.path} (${WRITE_ERROR_REASONS[check.code] || check.code})` +
      " - the install will request elevated permission";

  return `dsh: ${state}${perm}. dsh is configured on the L1 standard path only - run: ${cmd}`;
}

// Read every client's MCP config and keep the `workled` rows. Uncached on
// purpose: in hook mode every event is a fresh process, so a cache would never
// be reused, and re-reading is cheap (measured ~40ms across all clients).
function getWorkledCandidates(clientPrefix) {
  const candidates = [];
  for (const s of loadMcpServers()) {
    if (s.name !== "workled") continue;
    if (!s.server || typeof s.server !== "object") continue;
    if (s.server.enabled === false) continue;
    if (s.server.url) candidates.push({ url: s.server.url, client: s.client });
  }
  if (!clientPrefix) return candidates;
  return candidates.filter((c) => c.client.startsWith(clientPrefix));
}

// Best-effort host-side Bluetooth diagnostic. Returns { available, powered,
// devicePaired, deviceNames, error }. On unsupported platforms or missing
// adapters the fields degrade gracefully so the caller never throws.
//
// `available` is tri-state:
//   true  - a Bluetooth adapter was found
//   false - the probe ran and definitively found no adapter
//   null  - the probe could not be executed (powershell missing/blocked, a
//           sandbox restriction, or a command failure after retries). We report
//           "unknown" instead of falsely claiming "no adapter", so a blocked
//           probe never masquerades as a missing adapter.
//
// `devicePaired` / `deviceNames` are workled-specific: they report ONLY the
// workled device(s) (name matches HomeAnt-* or workled-* prefix) so the
// macro-readiness hint is accurate. A non-workled device never masquerades as
// paired (fixes #1 — Linux fallback path previously promoted the first
// arbitrary BT device to "paired"). When several workled devices are paired,
// `deviceNames` lists them all (deduplicated).
export async function probeBluetooth(timeoutMs = WORKLED_TIMEOUT_MS) {
  const result = {
    available: null,
    powered: false,
    devicePaired: false,
    deviceNames: [],
    error: null,
  };

  // Regex shared by every platform probe. Device broadcasts use names like
  // "HomeAnt-A919" or "workled-1234"; OS-level paired lists often carry the
  // same name, optionally with HID suffixes. Match anywhere (not just ^)
  // because some hosts prepend "BLE " or append " (Keyboard)" to the name.
  const WORKLED_NAME_RE = /(?:HomeAnt|workled)[-_]?[A-Za-z0-9]*/i;

  try {
    if (process.platform === "win32") {
      // Windows: three-tier probe with progressive fallback.
      //
      //  Tier 1 (preferred): Get-CimInstance Win32_PnPEntity — gives us
      //    HardwareID strings that carry the raw Bluetooth device name in
      //    the format `BTHENUM\{UUID}_<device-mac>#`, plus a ConfigManager
      //    status code where 0 == device present and working. This is the
      //    most reliable source of the workled device name on Windows
      //    because FriendlyName is often localised ("Bluetooth HID Device").
      //  Tier 2 (powered): check the BTHPORT service AND the radio state
      //    via the registry. PnP Status == "OK" only means the driver is
      //    loaded (fixes #3 — previously it was conflated with "radio on").
      //  Tier 3 (FriendlyName last-resort name match): keep the
      //    FriendlyName regex probe as a final fallback so an older Windows
      //    version that happens to set FriendlyName correctly is still
      //    covered (fixes #2 — now it's one probe among many, not the
      //    only way to detect a paired workled).

      try {
        // --- Tier 1: CIM PnP entities (adapter + device name) ------------
        const cimCmd =
          "@(Get-CimInstance Win32_PnPEntity -ErrorAction SilentlyContinue | " +
          "Where-Object { $_.PNPClass -in @('Bluetooth','BluetoothLE') -or $_.Service -eq 'BTHLE' -or $_.Service -eq 'BTHPORT' } | " +
          "Select-Object Name,FriendlyName,HardwareID,PNPClass,Status,ConfigManagerErrorCode | ConvertTo-Json -Compress)";
        let parsed = [];
        try {
          const { stdout: cimOut } = await execWithRetry(
            "powershell",
            ["-NoProfile", "-Command", cimCmd],
            { timeout: timeoutMs }
          );
          const trimmed = cimOut.trim();
          if (trimmed) parsed = JSON.parse(trimmed);
        } catch {
          parsed = [];
        }
        if (!Array.isArray(parsed)) parsed = parsed ? [parsed] : [];

        // Adapter present = any Bluetooth class entry (regardless of status)
        // that isn't just a virtual enumerator.
        const adapterEntries = parsed.filter((e) =>
          /^Bluetooth/i.test(String(e.PNPClass || ""))
        );
        result.available = adapterEntries.length > 0;

        // Adapter working = at least one entry with CM error code 0 (OK).
        const adapterWorking = adapterEntries.some((e) => {
          const cmErr = Number(e.ConfigManagerErrorCode);
          const statusOk = String(e.Status || "").toLowerCase() === "ok";
          return cmErr === 0 || statusOk;
        });

        // --- Tier 2: powered — BTHPORT service + radio registry hint -----
        // Query the Bluetooth Windows Service state; "Running" means the
        // radio stack is up. Without this the PnP driver status can be
        // "OK" even when the user turned the radio off in Action Center.
        let serviceRunning = false;
        try {
          const { stdout: svcOut } = await execWithRetry(
            "powershell",
            [
              "-NoProfile",
              "-Command",
              "(Get-Service -Name BTHPORT -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Status) -as [string]",
            ],
            { timeout: timeoutMs }
          );
          serviceRunning = svcOut.trim().toLowerCase() === "running";
        } catch {
          // service probe blocked — infer powered only from adapter working
        }
        result.powered = serviceRunning || adapterWorking;

        // --- Tier 3: workled device name (HardwareID > Name > FriendlyName)
        // HardwareID entries look like:
        //   BTHENUM\{00001812-0000-1000-8000-00805f9b34fb}_LOCALMFG&0000
        //   BTHENUM\\Dev_<6-hex-byte-mac>...
        // But more importantly, the raw device enumeration name for HID
        // over BLE sometimes embeds the advertised name. When it doesn't,
        // we fall back to checking the Name and FriendlyName fields with
        // the prefix regex so manually-assigned FriendlyNames still work.
        // Additionally, scan *all* PnP entities, not just Bluetooth class —
        // the HID side of a paired BLE keyboard often shows up under class
        // "HIDClass" / "Keyboard" / "Mouse" with the real device name in
        // FriendlyName and a BTHENUM HardwareID parent. Collect every match
        // (a single device can match via Name AND FriendlyName, so dedupe).
        const matchedDevices = new Set();
        for (const e of parsed) {
          const haystack = [
            e.Name,
            e.FriendlyName,
            ...(Array.isArray(e.HardwareID) ? e.HardwareID : []),
          ]
            .filter(Boolean)
            .map(String)
            .join(" | ");
          const m = haystack.match(WORKLED_NAME_RE);
          if (m) matchedDevices.add(m[0]);
        }
        // Last-resort FriendlyName sweep across ALL classes (covers the
        // case where the CIM query accidentally filtered the HID side out,
        // but a non-Bluetooth class entry still has a friendly name like
        // "HomeAnt-A919 Keyboard"). Only run when Tier 1 found nothing.
        if (matchedDevices.size === 0) {
          try {
            const { stdout: hidOut } = await execWithRetry(
              "powershell",
              [
                "-NoProfile",
                "-Command",
                "Get-PnpDevice -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FriendlyName",
              ],
              { timeout: timeoutMs }
            );
            const names = hidOut.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
            for (const n of names) {
              const m = n.match(WORKLED_NAME_RE);
              if (m) matchedDevices.add(m[0]);
            }
          } catch {
            // ignored — last resort only
          }
        }
        if (matchedDevices.size > 0) {
          result.devicePaired = true;
          result.deviceNames = [...matchedDevices];
        }
      } catch {
        result.available = null;
        result.error =
          "Bluetooth probe could not run (powershell unavailable or blocked)";
      }
    } else if (process.platform === "darwin") {
      try {
        const { stdout } = await execFileAsync("blueutil", ["--power"], { timeout: timeoutMs });
        result.powered = stdout.trim() === "1";
        result.available = true;

        try {
          const { stdout: pairedOut } = await execFileAsync("blueutil", ["--paired"], {
            timeout: timeoutMs,
          });
          const lines = pairedOut.trim().split(/\r?\n/).filter(Boolean);
          const matched = new Set();
          for (const l of lines) {
            if (!WORKLED_NAME_RE.test(l)) continue;
            const m = l.match(/address:\s*([^\s,]+)/i);
            const nameMatch = l.match(WORKLED_NAME_RE);
            matched.add(nameMatch ? nameMatch[0] : (m ? m[1] : l.split(",")[0]?.trim() || null));
          }
          if (matched.size > 0) {
            result.devicePaired = true;
            result.deviceNames = [...matched];
          }
        } catch {
          // no paired devices
        }
      } catch {
        try {
          const { stdout } = await execFileAsync(
            "system_profiler",
            ["SPBluetoothDataType", "-json"],
            { timeout: timeoutMs }
          );
          const data = JSON.parse(stdout);
          result.available = true;
          result.powered = true;

          const devices =
            data.SPBluetoothDataType?.[0]?.device_connected ||
            data.SPBluetoothDataType?.[0]?.device_paired ||
            [];
          const matched = new Set();
          for (const d of devices) {
            if (
              !WORKLED_NAME_RE.test(d.device_name || "") &&
              !WORKLED_NAME_RE.test(d.device_type || "")
            ) {
              continue;
            }
            const nm = String(d.device_name || "").match(WORKLED_NAME_RE);
            matched.add(nm ? nm[0] : (d.device_name || null));
          }
          if (matched.size > 0) {
            result.devicePaired = true;
            result.deviceNames = [...matched];
          }
        } catch {
          result.available = null;
          result.error =
            "Bluetooth not available (install blueutil or enable system_profiler)";
        }
      }
    } else if (process.platform === "linux") {
      try {
        const { stdout } = await execFileAsync("bluetoothctl", ["show"], { timeout: timeoutMs });
        result.available = stdout.includes("Controller");
        result.powered = stdout.includes("Powered: yes");

        try {
          // `bluetoothctl devices` lines: "AA:BB:CC:DD:EE:FF DeviceName"
          // Only accept a device whose name matches the workled prefix.
          // Fixes #1: the previous else-if branch promoted ANY paired
          // device (earbuds, mouse) to "workled paired" when no match
          // was found — that branch is now removed entirely.
          const { stdout: devOut } = await execFileAsync("bluetoothctl", ["devices"], {
            timeout: timeoutMs,
          });
          const lines = devOut.trim().split(/\r?\n/).filter(Boolean);
          const matched = new Set();
          for (const l of lines) {
            if (!WORKLED_NAME_RE.test(l)) continue;
            const m = l.match(WORKLED_NAME_RE);
            matched.add(m ? m[0] : (l.split(/\s+/).slice(2).join(" ") || null));
          }
          if (matched.size > 0) {
            result.devicePaired = true;
            result.deviceNames = [...matched];
          }
        } catch {
          // no paired devices
        }
      } catch {
        result.available = null;
        result.error = "bluetoothctl not available";
      }
    } else {
      result.error = `Unsupported platform: ${process.platform}`;
    }
  } catch {
    result.available = null;
    result.error = "Bluetooth probe failed";
  }

  return result;
}

// Parse a JSON-RPC response body. Accepts a plain JSON object/array (stateless
// JSON transport) or an SSE stream (`data:` lines). On failure it throws with
// the offending snippet so rpc()/probeReachable surface a diagnosable error
// instead of a raw JSON.parse exception.
function extractJson(text) {
  const trimmed = (text || "").trim();
  // Direct JSON object/array
  if (trimmed.startsWith("{") || trimmed.startsWith("[")) {
    try {
      return JSON.parse(trimmed);
    } catch {
      throw new Error(`Invalid JSON: ${trimmed.substring(0, 100)}`);
    }
  }
  // SSE data lines
  const data = trimmed
    .split("\n")
    .filter((l) => l.startsWith("data:"))
    .map((l) => l.slice(5).trim())
    .join("");
  if (!data) throw new Error("No JSON data found in response");
  try {
    return JSON.parse(data);
  } catch {
    throw new Error(`Invalid JSON: ${data.substring(0, 100)}`);
  }
}

// POST a single JSON-RPC request without any session header.
async function postJson(url, method, params, controller, extraHeaders = {}) {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      ...extraHeaders,
    },
    signal: controller.signal,
    body: JSON.stringify({ jsonrpc: "2.0", id: nextRpcId++, method, params }),
  });
  return { status: res.status, headers: res.headers, text: await res.text() };
}

// Send a JSON-RPC request, stateless-only. The device server runs with
// stateless support (MCP 2026-07-28+ / bare requests without a version header
// are served without a session), so there is no session fallback: a JSON-RPC
// error in the response is surfaced as an exception for the caller's retry
// logic. The error message carries the firmware's `data.reason` (e.g.
// "initialize must be first interaction") so status output is self-explanatory.
async function rpc(url, method, params, timeoutMs = WORKLED_TIMEOUT_MS) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const { status, text } = await postJson(url, method, params, controller);
    const out = extractJson(text);
    if (out && out.error) {
      const detail = out.error.data && (out.error.data.reason || out.error.data.method);
      throw new Error(
        `workled rpc: JSON-RPC error ${out.error.code}: ${out.error.message}${detail ? ` (${detail})` : ""} (HTTP ${status})`
      );
    }
    return out;
  } finally {
    clearTimeout(timer);
  }
}

// Resolve the MCP URL to talk to. Deliberately uncached: the answer is a pure
// function of process.env plus the config files, both read cheaply, and in hook
// mode each event is a fresh process where a cache could never be reused.
//
// The env override is taken at face value — it is explicit user intent, and
// probing it is pure loss in hook mode: a stale WORKLED_MCP_URL made each event
// burn a full WORKLED_TIMEOUT_MS before the config fallback even got a chance
// (measured: 3.2s per event against a reachable device, because the probe
// doubled the round trips). Reachability probing is `status`'s job; it reports
// exactly what it finds. The one input still refused is the documented
// `<device-name>` placeholder, which is a template rather than an address —
// accepting it would shadow a working config with something unroutable.
function discoverWorkledUrl(clientPrefix) {
  const envUrl = process.env.WORKLED_MCP_URL;
  if (envUrl && !envUrl.includes("<device-name>")) {
    return envUrl;
  }
  const candidates = getWorkledCandidates(clientPrefix);
  if (candidates.length === 0) {
    return null;
  }
  // First configured URL wins (the server is stateless, so there is nothing to
  // probe or rank); the read above happens again on the next call by design.
  return candidates[0].url;
}

let pendingState = null;
let senderRunning = false;
// Handle on the in-flight sendLoop, so hook mode can await delivery inline.
// The async declaration releases the HOST immediately, but the device send
// still has to finish before this process exits — a detached child would be
// killed by the host's job object the moment the hook parent returns.
let senderDone = Promise.resolve();
// Track flush promises for CLI hook mode. Each queued flush is tagged with
// the state that was pending at enqueue time so sendLoop can settle only the
// promises whose target state has actually been processed (fixes #6:
// previously a single completed state settled every queued flush regardless
// of which state each caller was waiting for).
const flushPromises = [];
// { state, resolve, reject }[]
//
// The last state actually delivered via MCP (set only on a successful send)
// AND the monotonic timestamp of that send. Dedup only fires when the
// incoming state matches lastSentState AND the last send was within the
// recent dedup window — otherwise an identical state across turns is sent
// so the device can reset animations (fixes #7).
let lastSentState = null;
let lastSentStateAtMs = 0;
const SAME_STATE_DEDUP_WINDOW_MS = 200;

// Pure, side-effect-free predicate that decides whether an incoming state
// should be deduplicated against the last successfully delivered state.
// Exposed for unit tests (and re-used by setAgentState below) so the 200 ms
// short-window rule of #7 is locked down: a repeat state is only suppressed
// when it matches the last sent state, the queue is empty, AND the previous
// send happened within the dedup window. Any repeat state after the window
// is delivered so the device can restart breath/pulse animations.
export function shouldDedupState(state, ctx) {
  const dedup = ctx.dedupWindowMs ?? SAME_STATE_DEDUP_WINDOW_MS;
  if (state !== ctx.lastSentState) return false;
  if (ctx.pendingState !== null && ctx.pendingState !== undefined) return false;
  if (typeof ctx.lastSentStateAtMs !== "number") return false;
  if (typeof ctx.nowMs !== "number") return false;
  return ctx.nowMs - ctx.lastSentStateAtMs < dedup;
}

// Pure version of resolveFlushPromisesForState (fixes #6). Given an array of
// flush entries `{ state: string|null, resolve, reject }` and a just-processed
// `state`, removes and resolves every entry whose target state matches — an
// entry with state=null means "wait for queue drain" so it only matches
// state=null. Returns the count of settled entries so tests can assert that
// entries tagged with a DIFFERENT state remain in-flight for a later settle.
export function drainFlushPromisesForState(list, state, result) {
  let settled = 0;
  for (let i = list.length - 1; i >= 0; i--) {
    const entry = list[i];
    if (entry.state === null || entry.state === state) {
      list.splice(i, 1);
      entry.resolve(result);
      settled++;
    }
  }
  return settled;
}

// Settle flush promises whose target state matches the just-processed one.
// Thin wrapper over the pure helper above — see that helper for the #6 note.
function resolveFlushPromisesForState(state, result) {
  drainFlushPromisesForState(flushPromises, state, result);
}
// Reject every remaining flush promise (sender-loop teardown path).
function rejectAllFlushPromises(err) {
  while (flushPromises.length > 0) {
    const entry = flushPromises.shift();
    entry.reject(err);
  }
}

async function sendLoop() {
  try {
    while (pendingState !== null) {
      const state = pendingState;
      pendingState = null;
      let lastErr = null;
      let sent = false;
      let superseded = false;

      // Fast-fail when no MCP URL is configured/discoverable: no point retrying.
      const url = await discoverWorkledUrl(hookClientPrefix);
      if (!url) {
        lastErr = new Error("MCP URL not configured or not discovered");
        const result = { state, sent, error: lastErr, superseded: false };
        resolveFlushPromisesForState(state, result);
        console.warn(`[workled] setAgentState(${state}) skipped: no MCP URL available`);
        continue;
      }

      for (let attempt = 0; attempt < 2; attempt++) { // maxAttempts
        if (pendingState !== null) {
          // a newer state superseded this one; drop it and send the latest next
          superseded = true;
          lastErr = null;
          break;
        }
        try {
          await rpc(url, "tools/call", { name: "set_agent_state", arguments: { state_name: state } });
          lastErr = null;
          sent = true;
          lastSentState = state;
          lastSentStateAtMs = Date.now();
          break;
        } catch (err) {
          lastErr = err;
          // Retry only for errors the LOCAL stack can judge instantly (DNS/mDNS
          // resolution failure, refused/reset socket). Everything else is final:
          //   timeout/abort   the per-attempt ceiling already elapsed
          //   HTTP / JSON-RPC the peer answered; a retry is moot
          //   config errors   deterministic; a retry is identical
          // Bailing out here keeps the worst case bounded (one attempt) instead
          // of spending a second full timeout on a doomed send.
          if (!isRetryableNetworkError(err)) break;
          // Only the first attempt may retry (attempt 0 is the send, attempt 1
          // is the retry), and a newer state already queued behind this one
          // cancels it — that retry would be stale before it left.
          if (attempt === 0 && pendingState === null) {
            await sleep(500);
          }
        }
      }
      // Resolve only flush promises waiting for THIS state
      const result = { state, sent, error: lastErr, superseded };
      resolveFlushPromisesForState(state, result);
      // Nothing to invalidate here: discovery re-reads the config on every
      // call, so a device that went offline — or a config that changed — is
      // picked up on its own. The failed state is still never resent: the next
      // state supersedes it.
      // console.warn(`[workled] setAgentState(${state}) failed after attempts: ${lastErr.message || lastErr}`);
    }
    // After the outer while-loop exits (pendingState became null) we know the
    // queue is fully drained. Flush any remaining "wait for drain" entries
    // (state === null) that weren't settled by a specific state match.
    const drainResult = { state: null, sent: true, error: null, superseded: false };
    resolveFlushPromisesForState(null, drainResult);
  } finally {
    senderRunning = false;
    // Reject any stragglers if sender exits unexpectedly (shouldn't happen)
    rejectAllFlushPromises(new Error("Sender loop exited unexpectedly"));
  }
}

function setAgentState(state) {
  // Short-window dedup: only skip when the same state was successfully sent
  // VERY recently AND no other state is queued. This lets legitimate repeat
  // requests (new turn, animation reset, question → answered → back to
  // thinking all resolve to "thinking" but separated by "waiting") reach the
  // device so it can restart breath / pulse effects. A tight 200 ms window
  // still collapses accidental double-fires from clients that emit duplicate
  // lifecycle events in quick succession.
  const now = Date.now();
  if (shouldDedupState(state, { lastSentState, lastSentStateAtMs, nowMs: now, pendingState })) {
    return;
  }
  pendingState = state;
  if (!senderRunning) {
    senderRunning = true;
    senderDone = sendLoop().catch((err) => {
      console.warn(`[workled] sender loop error: ${err && err.message}`);
    });
  }
}

function getUserMessage(event) {
  if (event.type !== "message.updated") return null;
  const props = event.properties || {};
  const msg = props.info || {};
  if (msg.role !== "user") return null;
  return msg;
}

// Register a seen user-message id and opportunistically clear the dedup set
// when it grows too large or goes stale. Shared by the opencode and openclaw
// adapters so per-turn "thinking" is only triggered once per message.
function markSeenMessage(id) {
  seenUserMessages.add(id);
  if (seenUserMessages.size > 200 || Date.now() - seenMessagesCleanedAt > SEEN_MESSAGES_CLEANUP_INTERVAL_MS) {
    seenUserMessages.clear();
    seenMessagesCleanedAt = Date.now();
  }
}

// ---- opencode adapter --------------------------------------------------------
//
// opencode plugins are exported as FUNCTIONS (async (ctx) => ({ hooks })), so
// the core keeps the same entry shape as openclawEntry and the generated entry
// file adapts it:
//   import { opencodeEntry as core } from ".../index.js";
//   export const workled = async (ctx) => await core.register(ctx);
//
// kilo (Anomaly) is an opencode fork: its Event/Hooks types are identical, so
// this adapter is reused verbatim. kilo only differs in the module shape:
//   import { opencodeEntry as core } from ".../index.js";
//   export default { id: "workled", server: async (ctx) => await core.register(ctx) }

export const opencodeEntry = {
  id: "workled",
  name: "workled",
  description:
    "Maps opencode agent lifecycle events (thinking/idle/waiting/error) to the workled MCP set_agent_state tool driving the LED strip.",
  async register(ctx) {
    try {
      await discoverWorkledUrl("opencode");
    } catch {
      // discovery retried lazily on first user message
    }
    return {
      event: async ({ event }) => {
        try {
          if (event.type === "session.idle") {
            setAgentState("idle");
            return;
          }
          if (event.type === "session.error") {
            setAgentState("error");
            return;
          }
          // session.status: busy/retry means work is in progress (covers new
          // user input, question reply, and permission approval resuming the
          // turn); idle means finished.
          if (event.type === "session.status") {
            const status = event.properties && event.properties.status;
            if (status && (status.type === "busy" || status.type === "retry")) {
              setAgentState("thinking");
            } else if (status && status.type === "idle") {
              setAgentState("idle");
            }
            return;
          }
          // permission.asked -> waiting (tool approval popup shown);
          // permission.replied -> thinking (resolved).
          if (event.type === "permission.asked" || event.type === "question.asked") {
            setAgentState("waiting");
            return;
          }
          if (event.type === "permission.replied" || event.type === "question.replied" || event.type === "question.rejected") {
            setAgentState("thinking");
            return;
          }
          const msg = getUserMessage(event);
          if (!msg) return;
          const id = msg.id || JSON.stringify(msg);
          if (seenUserMessages.has(id)) return;
          markSeenMessage(id);
          setAgentState("thinking");
        } catch (err) {
          // Never block the user workflow; device unreachable is skipped gracefully.
          console.warn(`[workled] event handler error: ${err && err.message}`);
        }
      },
      "tool.execute.before": async (input) => {
        try {
          // Substring, case-insensitive match (isInputTool) so renamed tool
          // variants (ask_question vs AskUserQuestion) still light up `waiting`.
          const toolName = input && input.tool ? String(input.tool) : "";
          if (toolName && isInputTool(toolName)) {
            setAgentState("waiting");
          }
        } catch (err) {
          // Never block the tool pipeline; device unreachable is skipped gracefully.
          console.warn(`[workled] tool hook error: ${err && err.message}`);
        }
      },
    };
  },
};

// ---- openclaw adapter (best-effort) -----------------------------------------
//
// OpenClaw plugins are loaded by the Gateway via `plugins.load.paths`; the
// entry is usually `export default definePluginEntry(...)`. The SDK wrapper
// lives in openclaw's node_modules, which the unified file must NOT import at
// top level (opencode auto-loads every function export and would fail on an
// unresolvable import). Installers therefore wrap this shape:
//   import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
//   import { openclawEntry } from ".../index.js";
//   export default definePluginEntry(openclawEntry);
// Event names/fields follow the OpenClaw plugin-hook docs and are best-effort.

export const openclawEntry = {
  id: "workled",
  name: "workled controller",
  description:
    "Maps OpenClaw agent lifecycle events (thinking/idle/waiting/error) to the workled MCP set_agent_state tool driving the LED strip.",
  register(api) {
    // True while an input tool (AskUserQuestion / confirm / ...) is awaiting
    // the user's answer, so we can recover to "thinking" once it replies.
    let lastWasInput = false;

    // Inbound user message starts a turn -> thinking.
    api.on("before_agent_run", async (event, ctx) => {
      try {
        const id = event.messageId || JSON.stringify(event);
        if (seenUserMessages.has(id)) return;
        markSeenMessage(id);
        setAgentState("thinking");
      } catch (err) {
        console.warn(`[workled] before_agent_run hook error: ${err && err.message}`);
      }
    });

    // Tool call that needs a user decision -> waiting
    api.on("before_tool_call", async (event) => {
      try {
        const name =
          (event && (event.toolName || event.tool || event.name)) || "";
        if (isInputTool(name)) {
          setAgentState("waiting");
          lastWasInput = true;
        } else if (lastWasInput) {
          // A previous input tool (waiting) has been answered and a regular
          // tool now runs -> thinking (defensive recovery for ordered flows).
          setAgentState("thinking");
          lastWasInput = false;
        }
      } catch (err) {
        console.warn(`[workled] before_tool_call hook error: ${err && err.message}`);
      }
    });

    // An input tool (AskUserQuestion) returned -> the user answered, resume
    // thinking. OpenClaw fires this after the tool resolves (before the next
    // agent step), which is the reliable recovery point out of "waiting".
    api.on("after_tool_call", async (event) => {
      try {
        if (lastWasInput) {
          setAgentState("thinking");
          lastWasInput = false;
        }
      } catch (err) {
        console.warn(`[workled] after_tool_call hook error: ${err && err.message}`);
      }
    });

    // Turn finished -> idle (or error when the run reports failure).
    // Note: if event is missing/falsy, default to idle (best-effort).
    // Only explicitly flag "error" when success === false or outcome === "error".
    api.on("agent_end", async (event) => {
      try {
        let failed = false;
        if (event) {
          if (event.success === false) failed = true;
          else if (event.outcome === "error") failed = true;
          else if (event.error) failed = true;
        }
        setAgentState(failed ? "error" : "idle");
      } catch (err) {
        console.warn(`[workled] agent_end hook error: ${err && err.message}`);
      }
    });

    // Session torn down -> idle fallback so the LED is not stuck in a busy state.
    api.on("session_end", async (event) => {
      try {
        setAgentState("idle");
      } catch (err) {
        console.warn(`[workled] session_end hook error: ${err && err.message}`);
      }
    });
  },
};

// ---- pi adapter ---------------------------------------------------------------
//
// pi loads `~/.pi/agent/extensions/*.ts` (or *.js) and takes the module's
// DEFAULT export as `(pi: ExtensionAPI) => void`. Like the other adapters the
// core exposes an entry object, and the generated extension file adapts it:
//   import { piEntry } from ".../index.js";
//   export default (pi) => piEntry.register(pi);

export const piEntry = {
  id: "workled",
  name: "workled controller",
  description:
    "Maps pi agent lifecycle events (thinking/idle/waiting/error) to the workled MCP set_agent_state tool driving the LED strip.",
  register(pi) {
    console.log("[workled] extension loaded");

    pi.on("agent_start", async () => {
      setAgentState("thinking");
    });

    pi.on("agent_end", async (event) => {
      // agent_end fires for each low-level run; use agent_settled for final idle.
      // Note: pi's agent_end may fire multiple times per turn; we ignore it
      // here to avoid premature idle. agent_settled is the reliable final state.
    });

    pi.on("agent_settled", async () => {
      setAgentState("idle");
    });

    pi.on("session_shutdown", async () => {
      setAgentState("idle");
    });

    let lastWasWaiting = false;

    pi.on("tool_call", async (event) => {
      // Best-effort input detection: pi has no built-in question tool, but
      // extensions may register interactive tools. Match by tool name.
      const name =
        (event && (event.toolName || event.tool || event.name)) || "";
      const isInput = isInputTool(name);

      if (isInput) {
        setAgentState("waiting");
        lastWasWaiting = true;
      } else if (lastWasWaiting) {
        // Previous tool was an input tool (waiting), now a regular tool runs -> thinking
        setAgentState("thinking");
        lastWasWaiting = false;
      }
    });

    // Note: pi's "input" event fires when USER submits input, not when agent asks.
    // It does NOT map to waiting state. The waiting state is triggered by
    // the agent calling input tools (question, ask, confirm, questionnaire, etc.).
    //
    // Pi has NO built-in permission prompts (docs: "No permission popups.").
    // Custom permission flows must be built via extensions (see confirm-destructive.ts).

    pi.on("session_start", async (_event, ctx) => {
      try {
        const url = await discoverWorkledUrl("pi");
        if (url && ctx && ctx.ui) {
          ctx.ui.notify(`workled connected: ${url}`, "info");
        }
      } catch {
        // device unreachable: skip gracefully
      }
    });
  },
};

// ---- default export for OpenClaw ------------------------------------------
// OpenClaw expects a module with `register` or `activate` as the default export.
// We wrap the openclawEntry adapter so the gateway can load the plugin directly.
export default { register: openclawEntry.register, activate: openclawEntry.register };

// ---- CLI hook mode (hermes) -------------------------------------------

// Event name -> state, unified across every hook-based client (hermes).
// Event names are unique per client so no conflicts arise; the same mapping
// serves all of them.
//
// PreToolUse maps to "tool": it resolves to "waiting" only when the payload
// references an input tool (AskUserQuestion etc., checked by extractToolName),
// otherwise it is a no-op. PostToolUse maps to "thinking" — after any tool
// returns the agent resumes working, so the LED returns to the working state.
//
// NOTE (trae-cn & WorkBuddy, both verified effective): PreToolUse AND
// PostToolUse for AskUserQuestion fire as expected in BOTH engines. The
// earlier "only-on-answer" behavior seen in trae-cn no longer reproduces.
// The installer therefore wires PreToolUse(matcher: AskUserQuestion) so a plain
// question lights "waiting" automatically as it is shown, and the matching
// PostToolUse returns the LED to "thinking" once the user answers — no
// agent-side set_agent_state call is needed. Notification remains the signal
// for approval dialogs (resolved via payload.notification_type, see
// "notification" below).
const HOOK_MAP = {
  // WorkBuddy (Claude Code-compatible hooks in ~/.workbuddy/settings.json)
  UserPromptSubmit: "thinking",
  // Notification fires when a dialog is SHOWN (render time), not after the
  // user answers. Resolved via payload.notification_type:
  //   permission_prompt -> waiting (tool approval dialog displayed)
  //   idle_prompt       -> idle   (session idle >60s, fallback for Stop)
  //   auth_success/...  -> no-op
  Notification: "notification",
  // hermes (camelCase)
  Stop: "idle",
  PreInvocation: "thinking",
  PostInvocation: "thinking",
  PreToolUse: "tool",
  PostToolUse: "thinking",
  // hermes shell-hook events (snake_case)
  pre_llm_call: "thinking",
  post_llm_call: "idle",
  pre_tool_call: "tool",
  post_tool_call: "thinking",
  pre_approval_request: "waiting",
  post_approval_response: "thinking",
  on_session_start: "thinking",
  on_session_end: "idle",
  subagent_start: "thinking",
  subagent_stop: "thinking",
  // dsh native Cordis events (bridge-source-validated; see
  // packages/core/agent-loop + packages/core/tools in deepseek-harness).
  // Default install path: a native dsh Cordis plugin (dsh-plugin/src) calls
  // workled DIRECTLY over HTTP (no shell hook hop). These entries remain so
  // a user who prefers the shell-hook bridge can also route raw Cordis
  // event names through the hook CLI path.
  "agent/session-start": "thinking",
  "agent/pre-step": "thinking",
  "tools/pre-execute": "tool",
  "tools/post-execute": "thinking",
  "agent/turn-stopping": "idle",
  "subagent/start": "thinking",
  "subagent/end": "thinking",
  // Additional Claude Code hook events that dsh's @deepseek-ai/dsh-hooks-claude-code
  // bridge supports (dsh runs CC hook config verbatim — see its packages/hooks).
  // Harmless for other clients, which never emit these events.
  SessionStart: "thinking",
  SubagentStart: "thinking",
  SubagentStop: "thinking",
};

function extractToolName(payload) {
  const p = payload || {};
  return (
    p.tool_name ||
    p.toolName ||
    p.tool ||
    (p.input && (p.input.tool || p.input.toolName)) ||
    (p.toolCall && (p.toolCall.name || p.toolCall.tool)) ||
    ""
  );
}

function toolIsInput(toolName) {
  const lowered = (toolName || "").toLowerCase();
  if (!lowered) return false;
  return getInputTools().some((t) => {
    const needle = t.toLowerCase();
    // Match on exact name OR substring: a default token like "question" should
    // also catch "AskUserQuestion", while explicit exact names still work.
    return needle === lowered || lowered.includes(needle);
  });
}

function resolveHookState(event, payload) {
  const target = HOOK_MAP[event];
  if (!target) return null;
  if (target === "tool") {
    const toolName = extractToolName(payload);
    if (!toolIsInput(toolName)) return null;
    return "waiting";
  }
  if (target === "notification") {
    // CodeBuddy/workbuddy Notification hook input carries notification_type.
    // Only the dialog-shown types map to a state; auth_success and anything
    // unknown are no-ops so the LED is not disturbed by incidental notices.
    const ntype = (payload && (payload.notification_type || payload.notificationType)) || "";
    if (ntype === "permission_prompt") return "waiting";
    if (ntype === "idle_prompt") return "idle";
    return null;
  }
  return target;
}

// Hook events that run as blocking hooks instead of async ones.
//
// The host recycles the worker around turn teardown (measured: killWorker lands
// 139-365ms after TURN_COMPLETED), and on Windows every hook is contained in a
// Job Object that owns its children too — so a hook still sending when the
// worker goes away is killed mid-flight and the device write dies with it.
// Stop is the exposed one: it is spawned ~20ms before the turn completes, i.e.
// right inside that window (measured 161ms of life, while one send needs ~2.1s
// over mDNS). Declaring no `async` makes the host wait for this process to
// exit, which is the only way to survive the recycle — a detached child cannot
// escape the job. Cost: teardown waits for the send, so settings.json needs a
// wider `timeout` for this event.
const SYNC_EVENTS = new Set(["Stop"]);

async function runHookMode() {
  // Set once the declaration line reaches stdout. It both guards the finally
  // block (never emit a second JSON line once declared) and tells the send path
  // that the host has already been released.
  let asyncDeclared = false;
  const declareAsync = (event) => {
    if (asyncDeclared) return Promise.resolve();
    asyncDeclared = true;
    // Sync event: stay a plain blocking hook. stdout still has to carry one
    // well-formed object, so emit the same no-op as the historical `{}`.
    if (SYNC_EVENTS.has(event)) {
      return new Promise((resolve) => process.stdout.write("{}\n", () => resolve()));
    }
    // Everything else declares async: the host reads this first stdout line,
    // drops its synchronous budget for this hook and resolves immediately, so
    // the LLM is never blocked on the device link. Clients that do not know the
    // `async` key still get a well-formed object carrying no decision fields,
    // i.e. the same no-op as `{}`. asyncTimeout is derived from the send budget
    // so the host keeps us alive exactly as long as the send can possibly take.
    // Resolve on the write callback, not on write() returning, so the line has
    // really left the process before hook mode is allowed to exit explicitly
    // (hook mode ends in process.exit — see the dispatcher).
    const line = JSON.stringify({ async: true, asyncTimeout: WORKLED_TIMEOUT_MS + 2000 }) + "\n";
    return new Promise((resolve) => process.stdout.write(line, () => resolve()));
  };
  try {
    const argv = process.argv.slice(2);
    const eventIdx = argv.indexOf("--event");
    const eventArg = eventIdx >= 0 ? argv[eventIdx + 1] : null;
    const clientIdx = argv.indexOf("--client");
    const clientArg = clientIdx >= 0 ? argv[clientIdx + 1] : null;
    if (clientArg) hookClientPrefix = clientArg;

    // Read the hook JSON payload from stdin (hermes may pass the event name via
    // --event instead). Never block on stdin: if the host never closes it
    // (e.g. a hook event with no payload), proceed after a short grace period
    // so this short-lived process always exits and never stalls the host's
    // tool call / turn.
    const chunks = [];
    const stdinDone = (async () => {
      for await (const chunk of process.stdin) chunks.push(chunk);
    })();
    await Promise.race([stdinDone, sleep(500)]);
    const raw = Buffer.concat(chunks).toString("utf8").trim();
    let payload = {};
    if (raw) {
      try {
        payload = JSON.parse(stripJsonc(raw));
      } catch {
        payload = {};
      }
    }

    const event = eventArg || payload.hook_event_name || payload.event || null;
    if (!event) {
      return;
    }
    const state = resolveHookState(event, payload);
    if (state) {
      // Declare async FIRST, then await the send inline. The host is released
      // the moment the declaration line lands, so the LLM is never blocked on
      // the device link; but this process stays alive until the send settles,
      // which is the whole point — a detached child is killed by the host's job
      // object the instant the hook parent returns, so the send would never
      // complete. Delivery reuses the plugin-style send loop, so hooks and
      // plugin clients share one logic path and one timeout budget.
      await declareAsync(event);
      setAgentState(state);
      await senderDone;
    }
  } catch (err) {
    // Never propagate: the hook process must always exit cleanly (stdout {}
    // + status 0) so the host's tool call is never denied or delayed.
    console.warn(`[workled] hook error: ${err && err.message}`);
  } finally {
    // Sync path only (no state to send, or an early error): keep the historical
    // no-op object. Once the async declaration is out, stdout must stay exactly
    // as it is — a second JSON line would corrupt the host's parse.
    // Awaited for the same reason as the declaration: hook mode exits with
    // process.exit, which must not outrun this write.
    if (!asyncDeclared) {
      await new Promise((resolve) => process.stdout.write("{}\n", () => resolve()));
    }
  }
}

// ---- status mode (diagnostics) ---------------------------------------------

// Errors worth exactly ONE extra attempt, decided immediately by the local
// stack rather than by a peer going quiet — so the second attempt costs almost
// no extra wall-clock and often succeeds (warm mDNS cache, device mid-reboot).
//
// Deliberately NOT retryable:
//   ABORT_ERR / UND_ERR_CONNECT_TIMEOUT  the per-attempt ceiling already
//                                        elapsed; retrying doubles the wait
//   EHOSTUNREACH / ENETUNREACH           "instant" in theory, but Windows waits
//                                        out ARP first (~1-3s) — not instant
//   ERR_INVALID_URL / ERR_SOCKET_BAD_PORT  deterministic; retry is identical
//   HTTP non-2xx / JSON-RPC error        the peer answered; retrying is moot
function isRetryableNetworkError(err) {
  if (!err) return false;
  const code = String((err.cause && err.cause.code) || err.code || "").toUpperCase();
  const retryable = [
    // DNS / mDNS resolution
    "ENOTFOUND",
    "EAI_AGAIN",
    "EAI_NONAME",
    "EAI_NODATA",
    // TCP refused / reset — device restarting, or a stale pooled socket
    "ECONNREFUSED",
    "ECONNRESET",
  ];
  if (retryable.includes(code)) return true;
  // Some platforms surface the resolver failure only in the message text.
  const msg = (err.message || String(err)).toLowerCase();
  return /\beai_again\b|\beai_noname\b|enotfound|econnrefused|econnreset/.test(msg);
}

// Reachability probe: a bare stateless tools/call to get_agent_state. No
// initialize handshake or session needed (the server serves stateless
// requests), and it also verifies the endpoint is really a workled server:
// only workled knows the get_agent_state tool. Reuses rpc() so error handling
// stays in one place; any throw (HTTP/JSON-RPC/network) means unreachable.
// Retries under the same rule as sendLoop:
// only an instantly-judgable network error (see
// isRetryableNetworkError) earns the second one, so a dead host does not double
// the wait. Reports which attempt succeeded so `status` can distinguish a
// flaky-but-working link from a dead one.
async function probeReachable(url, timeoutMs = WORKLED_TIMEOUT_MS) {
  if (!url || typeof url !== "string" || url.includes("<device-name>")) {
    return { reachable: false, error: "placeholder URL", attempt: 0 };
  }
  let lastErr = null;
  let attemptsMade = 0;
  for (let attempt = 1; attempt <= 2; attempt++) { // maxAttempts
    attemptsMade = attempt;
    try {
      await rpc(url, "tools/call", { name: "get_agent_state", arguments: {} }, timeoutMs);
      return { reachable: true, error: null, attempt };
    } catch (err) {
      lastErr = err;
      // Same rule as sendLoop: retry only when the local stack can decide
      // instantly that the failure is transient. A timeout/abort or a peer
      // that answered with an error is final — retrying only wastes time.
      if (!isRetryableNetworkError(err)) {
        break;
      }
      if (attempt < 2) { // maxAttempts
        await sleep(500);
      }
    }
  }
  return {
    reachable: false,
    error: (lastErr && lastErr.message) || String(lastErr),
    attempt: attemptsMade,
  };
}

// status: scan every client config source, keep only sources declaring a
// `workled` server, and probe each unique URL with a bare stateless
// tools/call.
// `clients` is omitted entirely when no workled server is configured.
async function runStatusMode() {
  const out = { hint: "", ok: false, exitCode: 1 };
  const startedAt = Date.now();
  // Progress goes to stderr so stdout stays a clean JSON for the install flow
  // to parse; the step-by-step log also proves the process is alive while the
  // Bluetooth/network probes (which can take seconds) are running.
  const log = (msg) => console.error(`[workled] status: ${msg}`);

  log("scanning agent configs...");

  // Optional per-client filter: `--client <name>` restricts the scan to
  // matching sources; omitted means all clients. Env override is always shown.
  const clientIdx = process.argv.indexOf("--client");
  const clientPrefix = clientIdx >= 0 ? process.argv[clientIdx + 1] : null;
  if (clientPrefix && !CLIENTS.some((c) => c.startsWith(clientPrefix))) {
    console.error(`Unknown client: ${clientPrefix}\nSupported clients: ${CLIENTS.join(", ")}`);
    process.exitCode = 1;
    return;
  }

  // Hoisted: needed both by the "nothing configured" early return below and by
  // the unwired-client hint. Pure (env + filesystem only), so hoisting is safe.
  const detectedClient = detectClient();
  // True when dsh is the client under diagnosis: named explicitly via --client,
  // or the only client this process can identify itself as.
  const dshTargeted = clientPrefix
    ? "dsh".startsWith(clientPrefix)
    : detectedClient === "dsh";

  const entries = [];
  const envUrl = process.env.WORKLED_MCP_URL;
  for (const s of loadMcpServers()) {
    if (s.name !== "workled") continue;
    if (clientPrefix && !s.client.startsWith(clientPrefix)) continue;
    const entry = {
      client: s.client,
      path: toPosix(s.path),
      enabled: s.server.enabled !== false,
      url: s.server.url || null,
    };
    // dsh-only install flags: allow the final status report to distinguish
    // "patch present but URL placeholder" from "plugin vendored" from "both
    // missing" without a second filesystem probe.
    for (const k of ["_dshPluginInstalled", "_dshPatchExists"]) {
      if (k in s.server) entry[k] = s.server[k];
    }
    entries.push(entry);
  }
  log(`found ${entries.length} workled entry(ies)`);

  // A lone WORKLED_MCP_URL still gets the full probe (its verdict lands in the
  // hint) — only "nothing configured anywhere" is a dead end.
  if (entries.length === 0 && !envUrl) {
    if (dshTargeted) {
      out.hint = dshL1Hint();
    } else {
      out.hint = clientPrefix
        ? `No \`workled\` server configured for client "${clientPrefix}". Add it under \`mcp\` in that client's config or set WORKLED_MCP_URL.`
        : "No `workled` server configured. Add it under `mcp` in your agent config or set WORKLED_MCP_URL.";
    }
    out.duration_ms = Date.now() - startedAt;
    log(`done in ${out.duration_ms}ms (no workled server configured)`);
    console.log(JSON.stringify(out, null, 2));
    process.exitCode = out.exitCode;
    return;
  }

  log("probing Bluetooth...");
  const bluetooth = await probeBluetooth().catch(() => ({
    available: false,
    powered: false,
    devicePaired: false,
    deviceNames: [],
    error: "Bluetooth probe failed",
  }));
  out.bluetooth = bluetooth;
  const btDeviceNames = bluetooth.deviceNames && bluetooth.deviceNames.length
    ? bluetooth.deviceNames
    : [];
  log(
    `Bluetooth ${bluetooth.available === true ? "available" : "unavailable"}` +
      (btDeviceNames.length > 0
        ? `, paired device(s): ${btDeviceNames.map((n) => `'${n}'`).join(", ")}`
        : "")
  );

  // Probe each unique URL once, in parallel. Distinct URLs can be checked
  // concurrently; per-URL retries (up to 3 with backoff) stay inside
  // probeReachable. Keeps `status` fast when many clients share configs.
  const urls = [
    ...new Set([
      // The override is probed too: it wins over config URLs, so a broken
      // override is exactly the thing worth reporting.
      ...(envUrl ? [envUrl] : []),
      ...entries.filter((e) => e.url && e.enabled !== false).map((e) => e.url),
    ]),
  ];
  log(`probing ${urls.length} unique URL(s)...`);
  const results = new Map(
    await Promise.all(urls.map(async (u) => [u, await probeReachable(u)]))
  );
  log("URL probes finished");

  // WORKLED_MCP_URL override: hoisted to a top-level field, with its probe
  // verdict folded into the hint (there is no clients[] entry left to carry
  // `mcpUrlReachable`). `envReachable` keeps the override equivalent to a
  // configured client for the ok / exitCode decision below.
  const envProbe = envUrl ? results.get(envUrl) : null;
  const envReachable = !!(envProbe && envProbe.reachable);
  if (envUrl) out.WORKLED_MCP_URL = envUrl;

  out.clients = entries.map((e) => {
    const enabled = e.enabled !== false;
    const probe = e.url && enabled ? results.get(e.url) : null;
    const entry = {
      client: e.client,
      mcpUrlReachable: !!(probe && probe.reachable),
      mcpPath: toPosix(e.path),
      mcpUrl: e.url,
    };
    if (e.enabled !== undefined) entry.mcpEnable = e.enabled;
    if (probe && probe.error) entry.error = probe.error;
    // dsh-only install metadata: plugin vendored / patch file exists / workled
    // row is present. Plain entries (JSON/YAML) omit these.
    for (const k of ["_dshPluginInstalled", "_dshPatchExists"]) {
      if (k in e) entry[k] = e[k];
    }
    return entry;
  });

  // ---- per-client install status: merge skill / plugin into clients -------
  // A functional client must have a workled MCP server configured — that is
  // how the agent calls the device (the generated plugin/hooks only add
  // lifecycle lighting). `out.clients` therefore already holds only MCP-
  // configured clients (from loadMcpServers). Here we enrich each with the
  // actual installed artifact paths: its plugin/hooks (plugin) and the workled
  // skill dir (skill). Pure filesystem probe — does not touch the device.
  for (const entry of out.clients) {
    entry.mcpEnable = entry.mcpEnable !== false;
    // An entry reaches out.clients only because loadMcpServers found a workled
    // server declared in that client's config, so "configured" is simply
    // "present here". Deriving it from mcpEnable/mcpUrl made the two
    // diagnostics below (configured-but-disabled / missing-url) unreachable:
    // both describe exactly the states that the old expression required to be
    // absent, so those hints could never fire and the user got the generic
    // "Device unreachable" text instead of the actionable one.
    entry.mcpConfig = true;
    // plugin / skill: pure path + separate existence probe. Symmetric.
    const t = CLIENT_TARGETS[entry.client];
    const pPath = t?.pluginPath?.();
    entry.plugin = pPath && t.existPlugin(pPath) ? toPosix(pPath) : null;
    const sPath = t?.skillPath?.();
    entry.skill = sPath && t.existSkill(sPath) ? toPosix(sPath) : null;
  }

  // `hint` reports failures only — a healthy link leaves it empty, so the
  // report does not carry a paragraph nobody acts on. Sentences are joined
  // through this helper: the first failure starts the string, and a later one
  // is separated from a hint that does not already end in punctuation (not
  // every sentence does — the wiring advice ends with a command).
  const appendHint = (sentence) => {
    if (!out.hint) {
      out.hint = sentence;
      return;
    }
    out.hint += /[.!?]$/.test(out.hint) ? ` ${sentence}` : `. ${sentence}`;
  };

  // A reachable WORKLED_MCP_URL override counts exactly like a reachable
  // client: it is the URL the hook actually uses.
  if (envReachable || out.clients.some((c) => c.mcpUrlReachable)) {
    out.ok = true;
    out.exitCode = 0;
    // Healthy state: The one exception is Bluetooth, whose
    // missing BLE pairing breaks the touch-pad macros even though the MCP link
    // itself is fine.
    if (bluetooth && bluetooth.available === true && !bluetooth.devicePaired) {
      let hint = "Macro requires Bluetooth. Pair the device as a BLE HID keyboard.";
      if (btDeviceNames.length > 0) {
        hint += ` Found: ${btDeviceNames.join(", ")}.`;
      } else {
        hint += " Device not found — scan for devices whose name starts with 'HomeAnt' or 'workled' in your OS Bluetooth settings.";
      }
      hint += " Ensure it is connected.";
      out.hint = hint;
    } else {
      out.hint =
        "If something looks off, check in this order: " +
        "LED — if the light stays off, set_brightness(128) or use the device switch; " +
        "MCP — if it was just configured, restart the agent/session so the new config loads; " +
        "trust — some agents require manually trusting the MCP connection before they use it; " +
        "hooks — some agents need to manually enable hooks (e.g. Settings -> Hooks); " +
        "DNS — on Windows mDNS is unstable, so in the MCP config prefer a static IP over the .local hostname to avoid intermittent -32001 timeouts.";
    }
  } else if (out.clients.some((c) => c.mcpConfig && c.mcpEnable === false)) {
    out.hint = "workled is configured but disabled. Set enabled=true or set WORKLED_MCP_URL.";
  } else if (out.clients.some((c) => c.mcpConfig && !c.mcpUrl)) {
    out.hint = "workled server has no `url`. Add `url` in your agent config or set WORKLED_MCP_URL.";
  } else {
    if (bluetooth && bluetooth.available === false) {
      out.hint = `Device unreachable: verify power and Wi-Fi, or use the IP address instead of the .local name. Bluetooth is also unavailable: ${bluetooth.error || "no Bluetooth adapter detected"}.`;
    } else {
      let hint = "Device unreachable: verify power and Wi-Fi, or use the IP address instead of the .local name.";
      if (btDeviceNames.length > 0) {
        hint += ` Paired device(s): ${btDeviceNames.join(", ")}.`;
      }
      out.hint = hint;
    }
  }

  // dsh has no editable `mcp` map, so the generic advice above does not apply
  // to it. When dsh is the diagnosis target but nothing is installed on its L1
  // path, replace the hint with a diagnosis of that path (which carries the
  // install command itself).
  const dshMissing = dshTargeted && !out.clients.some((c) => c.client === "dsh");
  if (dshMissing) out.hint = dshL1Hint();

  // Clients that should be wired but aren't: configured clients missing their
  // plugin, plus the running client if it has no MCP config at all (it can't
  // call the device until a full install runs).
  // Only installable clients reach out.clients at all (the WORKLED_MCP_URL
  // override is a top-level field), so a plain "has no plugin" test suffices.
  const unwired = out.clients.filter((e) => !e.plugin && CLIENTS.includes(e.client));
  // Skip dsh here when its L1 hint already replaced the hint above — that
  // message names the missing path and the install command, so a second
  // "wiring not installed for: dsh" line would just repeat it.
  if (!dshMissing && detectedClient && !out.clients.some((c) => c.client === detectedClient)) {
    unwired.push({ client: detectedClient, plugin: null });
  }
  if (unwired.length > 0) {
    const target = detectedClient && unwired.some((e) => e.client === detectedClient)
      ? detectedClient
      : unwired[0].client;
    const scriptDir = dirname(fileURLToPath(import.meta.url));
    const cmd = `node ${JSON.stringify(toPosix(join(scriptDir, "skill-install.mjs")))} install --client ${target}`;
    const list = unwired.map((e) => e.client).join(", ");
    // Its own sentence: follows an existing hint, or becomes the whole hint
    // when everything else is healthy.
    appendHint(`Wiring not installed for: ${list}; run: ${cmd}`);
  }

  out.duration_ms = Date.now() - startedAt;
  log(`done in ${out.duration_ms}ms (ok=${out.ok})`);
  console.log(JSON.stringify(out, null, 2));
  process.exitCode = out.exitCode;
}

if (process.argv[1]) {
  const selfPath = fileURLToPath(import.meta.url);
  // The installed (global) copy is invoked via a different absolute path than
  // the source/workspace copy (e.g. C:\Users\<u>\.agents\skills\workled vs the
  // workspace .agents\skills\workled), so a strict full-path comparison wrongly
  // yields isMain=no and silently skips the hook/status dispatch. Fall back to
  // the resolved basename so the entry file boots regardless of install path.
  const isMain =
    (process.argv[1] && resolve(process.argv[1]) === resolve(selfPath)) ||
    (process.argv[1] && resolve(process.argv[1]).toLowerCase().replace(/\\/g, "/").split("/").filter(Boolean).at(-1) ===
      resolve(selfPath).toLowerCase().replace(/\\/g, "/").split("/").filter(Boolean).at(-1));
  if (isMain) {
    const sub = process.argv[2];
    if (sub === "hook") {
      // Exit explicitly the moment the hook work is done. An aborted CONNECT
      // leaves undici holding a half-open socket that keeps the event loop alive
      // for another ~8s even though every byte of work has finished (measured:
      // work 3.0s, process 11.4s). Without this, hook lifetime is governed by
      // undici rather than by WORKLED_TIMEOUT_MS, and the host's asyncTimeout
      // ends up cutting the process off mid-exit.
      // Both stdout writes in runHookMode are awaited, so exiting here cannot
      // truncate the output the host reads. runHookMode never rejects (internal
      // try/catch/finally); the catch below is a safety net that still exits 0
      // so the host never denies the tool call.
      runHookMode()
        .then(() => process.exit(0))
        .catch((err) => {
          console.warn(`[workled] hook error: ${err && err.message}`);
          process.exit(0);
        });
    } else if (sub === "status") {
      runStatusMode().catch((err) => {
        console.warn(`[workled] status error: ${err && err.message}`);
        process.exitCode = 1;
      });
    } else {
      console.error(`[workled] unknown subcommand: "${sub}".`);
      process.exitCode = 2;
    }
  }
}
