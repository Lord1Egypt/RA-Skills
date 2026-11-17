#!/usr/bin/env node
// Sync a local skill directory to a GitHub repo via the GitHub Contents API (PAT auth).
// All machine-specific values come from CLI args / environment variables — nothing is hardcoded.
//
// Usage:
//   node sync_skill_to_github.js --owner <github-user> [--repo <name>] [--dir <local-skill-dir>]
//                                [--message <commit-message>] [--branch main]
//                                [--files "SKILL.md,README.md,references/foo.md"]
//
// Environment:
//   GITHUB_TOKEN or GITHUB_PAT — a GitHub personal access token (repo scope). Required.
//   The script exits with an error if neither variable is set. Credentials are
//   consumed from the environment only — nothing credential-related is read from
//   disk, and requests go nowhere except api.github.com.
//
// Behavior notes (disclosed for transparency):
//   - This script ONLY creates or updates files (contents API PUT). It never deletes
//   - Path containment (fail-closed): --files entries must resolve inside LOCAL_DIR. Absolute
//     paths, ".." components, and symlinked path segments are rejected (exit 1) before
//     anything is read or uploaded.
//     remote files: files present on GitHub but absent from the local FILES list are
//     left untouched. If you remove a file from the list, delete it on GitHub manually.

const https = require("https");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

function parseArgs(argv) {
  const out = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith("--")) out[key] = true;
      else { out[key] = next; i++; }
    }
  }
  return out;
}

const args = parseArgs(process.argv);

// --- Resolve configuration (no hardcoded personal values) ---
const TOKEN = process.env.GITHUB_TOKEN || process.env.GITHUB_PAT || null;

const LOCAL_DIR = path.resolve(args.dir || process.cwd());
const REPO = args.repo || path.basename(LOCAL_DIR);
const OWNER = args.owner || process.env.GITHUB_OWNER || null;
const BRANCH = args.branch || "main";
const COMMIT_MSG = args.message || `sync ${REPO} from local`;

if (!OWNER) {
  console.error("ERROR: --owner <github-user> is required (or set GITHUB_OWNER).");
  process.exit(1);
}
if (!TOKEN) {
  console.error("ERROR: no GitHub token. Set the GITHUB_TOKEN or GITHUB_PAT environment variable (credentials are read from the environment only, never from files).");
  process.exit(1);
}
if (!fs.existsSync(path.join(LOCAL_DIR, "SKILL.md")) && !args.files) {
  console.error(`ERROR: ${LOCAL_DIR} does not look like a skill dir (no SKILL.md). Pass --dir or --files.`);
  process.exit(1);
}

// Default whitelist: top-level docs + one references level. Extend via --files (comma-separated).
// Path containment (fail-closed): every entry must resolve inside LOCAL_DIR — absolute paths,
// ".." components, symlinked segments, and escapes are rejected before anything is read.
function assertContained(rel) {
  const deny = (why) => {
    console.error(`ERROR: path containment violation for "${rel}": ${why}. Nothing was read or uploaded.`);
    process.exit(1);
  };
  if (path.isAbsolute(rel)) deny("absolute paths are not allowed");
  if (rel.split(/[\\/]+/).includes("..")) deny("'..' components are not allowed");
  const target = path.resolve(path.join(LOCAL_DIR, rel));
  if (target !== LOCAL_DIR && !target.startsWith(LOCAL_DIR + path.sep)) deny("resolves outside LOCAL_DIR");
  let probe = LOCAL_DIR;
  for (const seg of rel.split(/[\\/]+/)) {
    probe = path.join(probe, seg);
    let st = null;
    try { st = fs.lstatSync(probe); } catch (e) { return; } // absent segment — handled by existsSync filter below
    if (st.isSymbolicLink()) deny("symlinked path segments are not allowed");
  }
}

const RAW_FILES = (args.files
  ? String(args.files).split(",").map((s) => s.trim()).filter(Boolean)
  : [
      "SKILL.md",
      "README.md",
      "README_zh.md",
      "references/publish-rules.md",
    ]
);
RAW_FILES.forEach(assertContained);
const FILES = RAW_FILES.filter((f) => fs.existsSync(path.join(LOCAL_DIR, f)));

function api(method, p, body) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const req = https.request(
      {
        hostname: "api.github.com",
        path: p,
        method,
        headers: {
          "User-Agent": "skill-sync",
          Authorization: `token ${TOKEN}`,
          Accept: "application/vnd.github+json",
          ...(data ? { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(data) } : {}),
        },
      },
      (res) => {
        let buf = "";
        res.on("data", (c) => (buf += c));
        res.on("end", () => {
          try { resolve({ status: res.statusCode, json: JSON.parse(buf || "{}") }); }
          catch (e) { resolve({ status: res.statusCode, json: { raw: buf } }); }
        });
      }
    );
    req.on("error", reject);
    if (data) req.write(data);
    req.end();
  });
}

// Compute the local file's git blob sha (same scheme as the GitHub Contents API).
function gitBlobSha(content) {
  const header = Buffer.from(`blob ${Buffer.byteLength(content)}\0`);
  const store = Buffer.concat([header, Buffer.from(content, "utf8")]);
  return crypto.createHash("sha1").update(store).digest("hex");
}

async function main() {
  console.log(`sync ${LOCAL_DIR} -> github.com/${OWNER}/${REPO} (branch ${BRANCH})`);

  // 1) Fetch remote file shas
  const remote = {};
  for (const f of FILES) {
    const r = await api("GET", `/repos/${OWNER}/${REPO}/contents/${encodeURIComponent(f)}?ref=${BRANCH}`);
    if (r.status === 200) remote[f] = r.json.sha;
  }
  console.log("remote files found:", Object.keys(remote).length, "/", FILES.length);

  // 2) Compare local content shas
  const toPush = [];
  for (const f of FILES) {
    const local = fs.readFileSync(path.join(LOCAL_DIR, f), "utf8");
    const localSha = gitBlobSha(local);
    if (remote[f] === localSha) {
      console.log(`  = ${f} (unchanged)`);
    } else {
      toPush.push({ f, local, sha: remote[f] || null, why: remote[f] ? "modified" : "new" });
      console.log(`  ${remote[f] ? "~" : "+"} ${f} (${remote[f] ? "modified" : "new"})`);
    }
  }
  if (!toPush.length) { console.log("nothing to push."); return; }

  // 3) PUT each changed file (create/update only — no remote deletions)
  for (const { f, local, sha } of toPush) {
    const body = {
      message: `${COMMIT_MSG} [${f}]`,
      content: Buffer.from(local, "utf8").toString("base64"),
      branch: BRANCH,
    };
    if (sha) body.sha = sha;
    const r = await api("PUT", `/repos/${OWNER}/${REPO}/contents/${encodeURIComponent(f)}`, body);
    if (r.status === 200 || r.status === 201) {
      console.log(`  pushed ${f} -> commit ${r.json.commit.sha.slice(0, 8)}`);
    } else {
      console.log(`  FAILED ${f}: HTTP ${r.status}`, JSON.stringify(r.json).slice(0, 300));
      process.exitCode = 1;
    }
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
