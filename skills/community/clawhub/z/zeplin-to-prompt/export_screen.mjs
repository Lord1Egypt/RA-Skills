import "dotenv/config";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";
import { createLogger } from "./lib/logger.mjs";
import { ensureDir, writeJSON, writeJSONMin, writeText, sanitizeFileName } from "./lib/fsHelpers.mjs";
import { buildAssetLookup } from "./lib/assets.mjs";
import { buildLayerTree, computeBounds } from "./lib/layerTree.mjs";
import { renderDesignPreview, makeTreeHTMLDocument } from "./lib/renderHtml.mjs";
import { createStyleContext } from "./lib/styleMapping.mjs";
import { createZeplinClient, fetchLatestScreenVersion } from "./lib/zeplinClient.mjs";
import { minifyLayerTree } from "./lib/minifyLayout.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const argv = process.argv.slice(2);
if (!argv.length) {
  console.error("Usage: node export_screen.mjs <URL | PROJECT_ID> [SCREEN_ID] [--workdir <DIR>] [--quiet] [--verbose]");
  console.error("Example: node export_screen.mjs https://app.zeplin.io/project/xxx/screen/yyy");
  process.exit(1);
}

let inputUrlOrProjectId = argv.shift();
let screenIdCandidate = argv.length ? argv[0] : undefined;
let screenId = undefined;
if (screenIdCandidate && !screenIdCandidate.startsWith("-")) {
  screenId = screenIdCandidate;
  argv.shift();
}

let projectId = inputUrlOrProjectId;
const urlPattern = /\/project\/([^\/]+)\/screen\/([^\/?#]+)/;
const urlMatch = urlPattern.exec(projectId);
if (urlMatch) {
  projectId = urlMatch[1];
  screenId = urlMatch[2];
}

if (!projectId || !screenId) {
  console.error("Usage: node export_screen.mjs <URL | PROJECT_ID> [SCREEN_ID] [--workdir <DIR>] [--platform <c|b>] [--quiet] [--verbose]");
  console.error("Example: node export_screen.mjs https://app.zeplin.io/project/xxx/screen/yyy");
  process.exit(1);
}

let workdir = null;
let QUIET = false;
let VERBOSE = false;
let NO_OPEN = false;
let backUrl = null;
let platformKey = null;
for (let i = 0; i < argv.length; i++) {
  const arg = argv[i];
  if (arg === "--workdir" && argv[i + 1]) { workdir = argv[++i]; continue; }
  if (arg === "--platform" && argv[i + 1]) { platformKey = argv[++i]; continue; }
  if (arg === "--quiet") { QUIET = true; continue; }
  if (arg === "--verbose") { VERBOSE = true; continue; }
  if (arg === "--no-open") { NO_OPEN = true; continue; }
  if (arg === "--back-url" && argv[i + 1]) { backUrl = argv[++i]; continue; }
}

const accessToken = process.env.zeplin_token || process.env.ZEPLIN_TOKEN;
if (!accessToken) {
  console.error("Missing token: please set the ZEPLIN_TOKEN environment variable");
  process.exit(1);
}

const log = createLogger(QUIET);

const buildWorkdir = (latestVersion) => {
  if (workdir) {
    ensureDir(workdir);
    return path.resolve(workdir);
  }
  const buildRoot = path.resolve(__dirname, "build");
  ensureDir(buildRoot);
  const dateStr = new Date().toISOString().slice(0, 16).replace("T", "_").replace(":", "-");
  const screenName = sanitizeFileName(latestVersion?.name || screenId || "screen");
  const auto = path.join(buildRoot, `${screenName}_${dateStr}`);
  ensureDir(auto);
  return auto;
};

const api = createZeplinClient(accessToken);
const phase = (index, message) => log(`${index} ${message}`);
const styleHelpers = createStyleContext(platformKey);

const openInFinder = (targetPath, log) => {
  try {
    execSync(`open "${targetPath.replace(/"/g, '\\"')}"`);
  } catch (err) {
    log(`Warning: failed to open ${targetPath}: ${err?.message || err}`);
  }
};

const normaliseScreenFrame = (latestVersion) => {
  const frame = latestVersion?.frame
    || latestVersion?.rect
    || latestVersion?.bounds
    || latestVersion?.size
    || latestVersion?.content?.frame
    || latestVersion?.content?.rect
    || latestVersion?.content?.bounds
    || latestVersion?.content?.size
    || null;

  const widthCandidate = frame?.width ?? latestVersion?.width ?? latestVersion?.content?.width;
  const heightCandidate = frame?.height ?? latestVersion?.height ?? latestVersion?.content?.height;
  const width = Number.isFinite(widthCandidate) ? widthCandidate : null;
  const height = Number.isFinite(heightCandidate) ? heightCandidate : null;
  if (width === null || height === null) return null;

  const xCandidate = frame?.x;
  const yCandidate = frame?.y;
  return {
    x: Number.isFinite(xCandidate) ? xCandidate : 0,
    y: Number.isFinite(yCandidate) ? yCandidate : 0,
    width,
    height
  };
};

const hasSingleScreenContainer = (layers, screenFrame, epsilon = 0.5) => {
  if (!Array.isArray(layers) || layers.length !== 1 || !screenFrame) return false;
  const root = layers[0];
  const rect = root?.rect;
  if (!rect || !Array.isArray(root?.layers) || !root.layers.length) return false;
  const dx = Math.abs((rect.x ?? 0) - screenFrame.x);
  const dy = Math.abs((rect.y ?? 0) - screenFrame.y);
  const dw = Math.abs((rect.width ?? 0) - screenFrame.width);
  const dh = Math.abs((rect.height ?? 0) - screenFrame.height);
  return dx <= epsilon && dy <= epsilon && dw <= epsilon && dh <= epsilon;
};

const MAX_SYNTHETIC_ROOT_IMAGE_WIDTH = 375;

const buildRenderableLayers = (latestVersion, screenFrame) => {
  const sourceLayers = latestVersion?.layers || latestVersion?.content?.layers || [];
  if (!screenFrame || !Array.isArray(sourceLayers) || !sourceLayers.length) return sourceLayers;
  if (!Number.isFinite(screenFrame.width) || screenFrame.width > MAX_SYNTHETIC_ROOT_IMAGE_WIDTH) {
    return sourceLayers;
  }
  if (hasSingleScreenContainer(sourceLayers, screenFrame)) return sourceLayers;

  return [{
    id: `__screen_root_${latestVersion?.id || screenId || "screen"}`,
    name: latestVersion?.name ? `${latestVersion.name} (Screen)` : "Screen",
    type: "screen",
    visible: true,
    rect: {
      x: screenFrame.x,
      y: screenFrame.y,
      width: screenFrame.width,
      height: screenFrame.height
    },
    layers: sourceLayers
  }];
};

(async () => {
  phase("START", "Starting export");

  try {
    phase("1", `Fetching screen data project=${projectId} screen=${screenId}`);
    const latestVersion = await fetchLatestScreenVersion(api, projectId, screenId);
    phase("2", "Creating export directory and writing raw data");
    const wd = buildWorkdir(latestVersion);
    process.env.ZEPLIN_LOG_FILE = path.join(wd, "export.log");
    if (VERBOSE) log(`→ log file: ${process.env.ZEPLIN_LOG_FILE}`);
    log(`→ workdir: ${wd}`);
    const rawPath = path.join(wd, "raw.json");
    writeJSON(rawPath, latestVersion, VERBOSE ? log : null);

    phase("3", "Downloading assets and building asset lookup");
    const assetsDir = path.join(wd, "assets");
    ensureDir(assetsDir);

    const assetLookup = await buildAssetLookup(latestVersion?.assets || [], {
      assetsDir,
      workdir: wd,
      log,
      verbose: VERBOSE
    });

    const screenFrame = normaliseScreenFrame(latestVersion);
    const renderableLayers = buildRenderableLayers(latestVersion, screenFrame);

    phase("4", "Building layer tree");
    const tree = buildLayerTree(
      renderableLayers,
      {
        debug: VERBOSE && !QUIET,
        verbose: VERBOSE,
        assetLookup,
        rootFrame: screenFrame,
        styleHelpers,
        log
      }
    );
    phase("5", "Computing canvas bounds and writing layout JSON");
    const bounds = computeBounds(tree);
    const layoutOutput = minifyLayerTree(tree, { bounds });
    const treePath = path.join(wd, "layers_tree.json");
    writeJSONMin(treePath, layoutOutput, VERBOSE ? log : null);

    const origin = { x: bounds.minX, y: bounds.minY };
    const screenImageUrl = latestVersion?.imageUrl
      || latestVersion?.content?.imageUrl
      || null;

    phase("6", "Rendering preview and HTML document");
    const preview = renderDesignPreview(
      tree,
      origin,
      bounds,
      {
        backgroundImage: screenImageUrl || undefined,
        backgroundImageFrame: screenFrame || undefined,
        assetLookup,
        styleHelpers,
        useNormalizedTree: true
      }
    );

    const html = makeTreeHTMLDocument(tree, {
      project: projectId,
      screen: latestVersion?.name || screenId,
      screenId,
      exportedAt: new Date().toISOString(),
      backUrl,
      preview
    }, {
      styleHelpers,
      minifiedTree: layoutOutput,
      minifiedRootWrapped: Array.isArray(tree) ? tree.length !== 1 : true
    });
    phase("7", "Writing HTML and opening the result");
    const htmlPath = path.join(wd, "layers_tree.html");
    writeText(htmlPath, html, VERBOSE ? log : null);
    if (!NO_OPEN) {
      openInFinder(wd, log);
      openInFinder(htmlPath, log);
    }
    phase("DONE", "Completed");
  } catch (err) {
    console.error("Request failed:", err?.response?.data || err?.message || err);
    process.exit(1);
  }
})();
