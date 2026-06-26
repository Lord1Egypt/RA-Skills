import "dotenv/config";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import { createLogger } from "./lib/logger.mjs";
import { ensureDir, writeText, sanitizeFileName } from "./lib/fsHelpers.mjs";
import { renderIndexHtml } from "./lib/renderIndex.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Argument parsing

const argv = process.argv.slice(2);
if (!argv.length) {
  console.error("Usage: node export_project.mjs <PROJECT_ID> --sections <S1,S2,...> --platform <ajk|bk> [--workdir <DIR>]");
  process.exit(1);
}

const projectId = argv.shift();
let sectionIds = [];
let sectionNames = [];
let screenNames = [];   // If provided, only export screens whose names are in this list.
let workdir = null;
let QUIET = false;

const parseNameList = (raw) =>
  raw.split(",").map(s => s.trim().replace(/^["']|["']$/g, "")).filter(Boolean);

for (let i = 0; i < argv.length; i++) {
  const arg = argv[i];
  if (arg === "--sections"      && argv[i + 1]) { sectionIds   = argv[++i].split(",").map(s => s.trim()).filter(Boolean); continue; }
  if (arg === "--section-names" && argv[i + 1]) { sectionNames = parseNameList(argv[++i]); continue; }
  if (arg === "--screen-names"  && argv[i + 1]) { screenNames  = parseNameList(argv[++i]); continue; }
  if (arg === "--workdir" && argv[i + 1]) { workdir = argv[++i]; continue; }
  if (arg === "--quiet") { QUIET = true; continue; }
}

// Token loading

const accessToken = process.env.zeplin_token || process.env.ZEPLIN_TOKEN;
if (!accessToken) {
  console.error("Missing token: please set the ZEPLIN_TOKEN environment variable");
  process.exit(1);
}

const log = createLogger(QUIET);
const ZEPLIN_API = "https://api.zeplin.dev/v1";
const apiHeaders = { Authorization: `Bearer ${accessToken}`, "Content-Type": "application/json" };

// Zeplin API helpers

const zeplinGet = async (endpoint) => {
  const res = await fetch(`${ZEPLIN_API}${endpoint}`, { headers: apiHeaders });
  if (!res.ok) throw new Error(`Zeplin API ${res.status}: ${endpoint}`);
  return res.json();
};

const getProjectName = async () => {
  try {
    const data = await zeplinGet(`/projects/${projectId}`);
    return data.name || null;
  } catch { return null; }
};

const getSection = async (sectionId) => {
  return zeplinGet(`/projects/${projectId}/screen_sections/${sectionId}`);
};

const getSectionScreens = async (sectionId) => {
  const data = await zeplinGet(`/projects/${projectId}/screens?section_id=${sectionId}&limit=100`);
  return Array.isArray(data) ? data : (data.screens || []);
};

// Work directory

const buildWorkdir = (projectName) => {
  if (workdir) { ensureDir(workdir); return path.resolve(workdir); }
  const buildRoot = path.resolve(__dirname, "build");
  ensureDir(buildRoot);
  const dateStr = new Date().toISOString().slice(0, 16).replace("T", "_").replace(":", "-");
  const baseName = sanitizeFileName(projectName || projectId);
  const dir = path.join(buildRoot, `${baseName}_${dateStr}`);
  ensureDir(dir);
  return dir;
};

// Export a single screen by calling export_screen.mjs

const exportScreen = (screenId, screenWorkdir, screenName) => {
  const args = [
    "export_screen.mjs",
    projectId, screenId,
    "--workdir", screenWorkdir,
    "--no-open",
    "--quiet",
    "--back-url", "../../index.html",
  ];
  log(`  -> Exporting screen: ${screenName} (${screenId})`);
  execFileSync(process.execPath, args, {
    cwd: __dirname,
    stdio: QUIET ? "pipe" : "inherit"
  });
};

// Main flow

(async () => {
  // Resolve the section list.
  if (!sectionIds.length) {
    log("Fetching section list...");
    const data = await zeplinGet(`/projects/${projectId}/screen_sections`);
    const all = Array.isArray(data) ? data : (data.screen_sections || []);
    if (sectionNames.length) {
      // Filter by name.
      const nameSet = new Set(sectionNames);
      const matched = all.filter(s => nameSet.has(s.name));
      if (!matched.length) {
        console.error(`No matching section found: ${sectionNames.join(", ")}`);
        console.error(`Available: ${all.map(s => s.name).join(", ")}`);
        process.exit(1);
      }
      sectionIds = matched.map(s => s.id);
      log(`-> Matched ${sectionIds.length} section(s) by name`);
    } else {
      sectionIds = all.map(s => s.id);
      log(`-> Exporting all ${sectionIds.length} section(s)`);
    }
  }
  const projectName = await getProjectName();
  log(`START exporting project=${projectName || projectId}, ${sectionIds.length} section(s) total`);
  const wd = buildWorkdir(projectName);
  log(`-> Output directory: ${wd}`);

  const exportedAt = new Date().toISOString();
  const indexSections = [];

  for (const sectionId of sectionIds) {
    let sectionName;
    try {
      const section = await getSection(sectionId);
      sectionName = section.name || sectionId;
    } catch {
      sectionName = sectionId;
    }

    log(`\nSection: ${sectionName}`);
    const safeSectionName = sanitizeFileName(sectionName);
    const sectionDir = path.join(wd, safeSectionName);
    ensureDir(sectionDir);

    let screens;
    try {
      screens = await getSectionScreens(sectionId);
    } catch (err) {
      log(`  Warning: failed to fetch screen list: ${err.message}`);
      continue;
    }

    // Filter by screen name if requested.
    if (screenNames.length) {
      const nameSet = new Set(screenNames);
      screens = screens.filter(s => nameSet.has(s.name));
    }
    log(`  ${screens.length} screen(s)${screenNames.length ? " (filtered)" : ""}`);
    const indexScreens = [];

    for (const screen of screens) {
      const safeScreenName = sanitizeFileName(screen.name || screen.id);
      const screenDir = path.join(sectionDir, safeScreenName);
      ensureDir(screenDir);
      try {
        exportScreen(screen.id, screenDir, screen.name || screen.id);
        indexScreens.push({
          name: screen.name || screen.id,
          htmlPath: `${safeSectionName}/${safeScreenName}/layers_tree.html`,
          thumbnailUrl: screen.image?.thumbnails?.small || null
        });
      } catch (err) {
        log(`  Failed to export screen ${screen.name || screen.id}: ${err.message}`);
      }
    }

    indexSections.push({ name: sectionName, screens: indexScreens });
  }

  // Generate index.html.
  const indexHtml = renderIndexHtml({ projectId, exportedAt, sections: indexSections });
  const indexPath = path.join(wd, "index.html");
  writeText(indexPath, indexHtml);
  log(`\nIndex page: ${indexPath}`);

  // Open index.html.
  try {
    const { execSync } = await import("node:child_process");
    execSync(`open "${indexPath.replace(/"/g, '\\"')}"`);
  } catch {}

  log("DONE");
})().catch(err => {
  console.error("Export failed:", err?.message || err);
  process.exit(1);
});
