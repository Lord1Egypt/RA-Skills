#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import JSZip from "jszip";
import { appendAudit } from "../lib/audit-log.js";
import { ErrorCodes } from "../lib/error-codes.js";
import { resolvePsdPath, DEFAULT_INDEX } from "../lib/index-resolver.js";
import { expandHome } from "../lib/paths.js";
import { normalizeTask, readTask, validateTask } from "../lib/task.js";
import {
  rankImagesByVisualSimilarity,
  snapshotDirectoryHashes,
  findChangedFiles,
} from "../lib/visual-match.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--task") {
      args.task = argv[i + 1];
      i += 1;
    } else if (arg === "--index") {
      args.index = argv[i + 1];
      i += 1;
    } else if (arg === "--dry-run") {
      args.dryRun = true;
    } else if (arg === "--timeout-ms") {
      args.timeoutMs = Number(argv[i + 1] || 60_000);
      i += 1;
    } else if (arg === "--help" || arg === "-h") {
      args.help = true;
    }
  }
  return args;
}

function printResultAndExit(result, code = 0) {
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  process.exit(code);
}

function createBackup(filePath) {
  const stamp = new Date()
    .toISOString()
    .replace(/[-:TZ.]/g, "")
    .slice(0, 14);
  const backupPath = `${filePath}.bak.${stamp}`;
  fs.copyFileSync(filePath, backupPath);
  return backupPath;
}

function waitMs(ms) {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
}

function looksLockedError(message) {
  const lower = String(message || "").toLowerCase();
  return (
    lower.includes("e_file_locked") ||
    lower.includes("is locked") ||
    lower.includes("being used by another process") ||
    lower.includes("permission denied")
  );
}

function mapErrorCode(message) {
  if (looksLockedError(message)) return ErrorCodes.E_FILE_LOCKED;
  if (String(message).includes("E_LAYER_NOT_FOUND")) return ErrorCodes.E_LAYER_NOT_FOUND;
  if (String(message).includes("E_STYLE_MISMATCH")) return ErrorCodes.E_STYLE_MISMATCH;
  if (String(message).includes("E_PHOTOSHOP_UNAVAILABLE"))
    return ErrorCodes.E_PHOTOSHOP_UNAVAILABLE;
  if (String(message).includes("E_EXPORT_FAILED")) return ErrorCodes.E_EXPORT_FAILED;
  if (String(message).includes("E_FILE_AMBIGUOUS")) return ErrorCodes.E_FILE_AMBIGUOUS;
  if (String(message).includes("E_IMAGE_NOT_FOUND")) return ErrorCodes.E_FILE_NOT_FOUND;
  return ErrorCodes.E_EXEC_FAILED;
}

function parseAvailableLayers(message) {
  const text = String(message || "");
  const marker = "AVAILABLE_LAYERS:";
  const idx = text.indexOf(marker);
  if (idx === -1) return [];
  const tail = text.slice(idx + marker.length);
  const raw = tail.split(/\r?\n/)[0].split(/\.\s*(?:\r?直线:|line:)/)[0] || "";
  return raw
    .split(",")
    .map((x) => x.replace(/\r?\n/g, ""))
    .filter((x) => x.trim().length > 0);
}

function buildFuzzyLayerSuggestions(target, layers) {
  const t = String(target || "").toLowerCase();
  if (!t || layers.length === 0) return [];
  const scored = layers
    .map((layer) => {
      const l = layer.toLowerCase();
      let score = 0;
      if (l === t) score += 100;
      if (l.includes(t) || t.includes(l)) score += 50;
      if (l.startsWith(t) || t.startsWith(l)) score += 20;
      return { layer, score };
    })
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score);
  const picked = scored.slice(0, 5).map((x) => x.layer);
  if (picked.length > 0) return picked;
  return layers.slice(0, 5);
}

function hasNonAscii(input) {
  return /[^\x00-\x7F]/.test(String(input || ""));
}

function prepareMacPathBridgeIfNeeded(task, workingPath) {
  const bridgeMode = task.options?.pathBridgeMode || "auto";
  const BRIDGE_AUTO_MAX_BYTES = 1.5 * 1024 * 1024 * 1024; // 1.5GB
  if (bridgeMode === "off") {
    return { executionPath: workingPath, syncBack: () => {} };
  }
  const ext = path.extname(workingPath).toLowerCase();
  const stat = fs.existsSync(workingPath) ? fs.statSync(workingPath) : null;
  const fileSize = stat?.size || 0;
  const shouldSkipAutoBridge =
    bridgeMode === "auto" &&
    (ext === ".psb" || fileSize > BRIDGE_AUTO_MAX_BYTES);
  if (shouldSkipAutoBridge) {
    return { executionPath: workingPath, syncBack: () => {} };
  }
  if (bridgeMode === "always" || (bridgeMode === "auto" && hasNonAscii(workingPath))) {
    const tmpDir = path.join(os.tmpdir(), "openclaw-psd-bridge");
    fs.mkdirSync(tmpDir, { recursive: true });
    const bridgedPath = path.join(tmpDir, `${Date.now()}-${path.basename(workingPath)}`);
    fs.copyFileSync(workingPath, bridgedPath);
    return {
      executionPath: bridgedPath,
      syncBack: () => {
        fs.copyFileSync(bridgedPath, workingPath);
      },
    };
  }
  return { executionPath: workingPath, syncBack: () => {} };
}

function runMacModify(inputPath, layerName, newText, outputPath, timeoutMs, styleLock = true) {
  const script = path.resolve(__dirname, "psd-modify-mac.applescript");
  return spawnSync(
    "osascript",
    [script, inputPath, layerName, newText, outputPath, styleLock ? "true" : "false"],
    {
      encoding: "utf8",
      timeout: timeoutMs,
    },
  );
}

function runMacPlaceImage(inputPath, imagePath, layerLabel, position, visible, outputPath, timeoutMs, targetArtboard = "") {
  const script = path.resolve(__dirname, "psd-place-image-mac.applescript");
  return spawnSync(
    "osascript",
    [script, inputPath, imagePath, layerLabel || "", position || "top", visible ? "true" : "false", outputPath, targetArtboard || ""],
    {
      encoding: "utf8",
      timeout: timeoutMs,
    },
  );
}

function runWinModify(inputPath, layerName, newText, outputPath, timeoutMs, styleLock = true) {
  const script = path.resolve(__dirname, "psd-modify-win.ps1");
  return spawnSync(
    "powershell.exe",
    [
      "-ExecutionPolicy",
      "Bypass",
      "-File",
      script,
      inputPath,
      layerName,
      newText,
      outputPath,
      String(styleLock),
    ],
    { encoding: "utf8", timeout: timeoutMs },
  );
}

function runMacExportPng(inputPath, pngPath, timeoutMs, exportMode = "single", pngDir = "", artboardName = "") {
  const script = path.resolve(__dirname, "psd-export-png-mac.applescript");
  return spawnSync("osascript", [script, inputPath, pngPath, exportMode, pngDir, artboardName], {
    encoding: "utf8",
    timeout: timeoutMs,
  });
}

function runWinExportPng(inputPath, pngPath, timeoutMs) {
  const script = path.resolve(__dirname, "psd-export-png-win.ps1");
  return spawnSync(
    "powershell.exe",
    ["-ExecutionPolicy", "Bypass", "-File", script, inputPath, pngPath],
    { encoding: "utf8", timeout: timeoutMs },
  );
}

function ensureParentDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function resolveDesktopDir() {
  return path.join(os.homedir(), "Desktop");
}

function resolveWorkingPsdPath(task, sourcePath) {
  const sourceMode = task.workflow?.sourceMode || "inplace";
  if (sourceMode !== "copy_then_edit") {
    return { sourceMode, workingPath: sourcePath, copiedFrom: undefined };
  }
  const copyToDir = path.resolve(expandHome(task.workflow?.copyToDir || resolveDesktopDir()));
  const fileName = path.basename(sourcePath);
  const workingPath = path.join(copyToDir, fileName);
  ensureParentDir(workingPath);
  fs.copyFileSync(sourcePath, workingPath);
  return { sourceMode, workingPath, copiedFrom: sourcePath };
}

function resolveFinalPsdPath(task, workingPath) {
  const psdOutput = task.output?.psd || {};
  const mode = psdOutput.mode || "overwrite";
  if (mode === "copy" && psdOutput.path) {
    const target = path.resolve(expandHome(psdOutput.path));
    ensureParentDir(target);
    fs.copyFileSync(workingPath, target);
    return target;
  }
  return workingPath;
}

function resolvePngOutputPath(item, psdPath) {
  const dir = item.dir ? path.resolve(expandHome(item.dir)) : path.dirname(psdPath);
  const fileName = item.fileName || `${path.basename(psdPath, path.extname(psdPath))}.png`;
  return path.join(dir, fileName);
}

function resolvePngOutputDir(item, psdPath) {
  const dir = item.dir ? path.resolve(expandHome(item.dir)) : path.dirname(psdPath);
  const folderName = item.folderName || `${path.basename(psdPath, path.extname(psdPath))}_web`;
  return path.join(dir, folderName);
}

function listExportedImagesInDir(dirPath) {
  if (!fs.existsSync(dirPath)) return [];
  // Check the given dir and the "images/" subdirectory (Photoshop SFW convention)
  const dirsToScan = [dirPath];
  const imagesSub = path.join(dirPath, "images");
  if (fs.existsSync(imagesSub) && fs.statSync(imagesSub).isDirectory()) {
    dirsToScan.push(imagesSub);
  }
  const result = [];
  for (const dir of dirsToScan) {
    const names = fs
      .readdirSync(dir)
      .filter((name) => /\.(png|jpg|jpeg|gif|webp)$/i.test(name))
      .sort((a, b) => a.localeCompare(b, "en"));
    result.push(...names.map((name) => path.join(dir, name)));
  }
  return result;
}

async function buildZipFromDirectory(dirPath, outPath) {
  const zip = new JSZip();
  const files = listExportedImagesInDir(dirPath);
  for (const filePath of files) {
    const base = path.basename(filePath);
    const data = fs.readFileSync(filePath);
    zip.file(base, data);
  }
  const buffer = await zip.generateAsync({
    type: "nodebuffer",
    compression: "DEFLATE",
    compressionOptions: { level: 6 },
  });
  ensureParentDir(outPath);
  fs.writeFileSync(outPath, buffer);
  return outPath;
}

function resolveBundleZipPath(task, outputDir, psdPath) {
  const zipName =
    task.output?.bundle?.zipName || `${path.basename(psdPath, path.extname(psdPath))}_web.zip`;
  return path.join(outputDir, zipName);
}

function executeWithRetry(params) {
  let result;
  for (let attempt = 0; attempt <= params.maxRetries; attempt += 1) {
    result = params.execute();
    if (!result) break;
    if (result.status === 0) break;
    const message = `${result.stderr || ""}\n${result.stdout || ""}`;
    if (!(params.retryEnabled && looksLockedError(message) && attempt < params.maxRetries)) break;
    waitMs(500 * (attempt + 1));
  }
  return result;
}

async function main() {
  const start = Date.now();
  const args = parseArgs(process.argv);
  if (args.help || !args.task) {
    process.stdout.write(
      "Usage: run-task.js --task <task.json> [--index <path>] [--dry-run] [--timeout-ms <n>]\n",
    );
    process.exit(args.help ? 0 : 1);
  }

  let task;
  try {
    task = readTask(args.task);
  } catch (error) {
    printResultAndExit(
      {
        status: "error",
        code: ErrorCodes.E_TASK_INVALID,
        message: `Cannot read task: ${error.message}`,
      },
      1,
    );
  }

  const validation = validateTask(task);
  if (!validation.ok) {
    printResultAndExit(
      {
        taskId: task && task.taskId,
        status: "error",
        code: validation.code,
        message: validation.message,
      },
      1,
    );
  }

  const normalizedTask = normalizeTask(task);
  const indexPath = path.resolve(expandHome(args.index || DEFAULT_INDEX));
  const resolved = resolvePsdPath({
    exactPath: normalizedTask.input.exactPath,
    fileHint: normalizedTask.input.fileHint,
    indexPath,
  });
  if (!resolved.ok) {
    const payload = {
      taskId: normalizedTask.taskId,
      status: "error",
      code: resolved.code || ErrorCodes.E_FILE_NOT_FOUND,
      message: resolved.message,
      candidates: resolved.candidates || [],
      suggestion: resolved.suggestion,
    };
    payload.auditLogPath = appendAudit(payload);
    printResultAndExit(payload, 1);
  }

  const platform = os.platform();
  const dryRun = Boolean(args.dryRun || (normalizedTask.options && normalizedTask.options.dryRun));
  const workingInfo = resolveWorkingPsdPath(normalizedTask, resolved.path);
  const pathBridge =
    platform === "darwin"
      ? prepareMacPathBridgeIfNeeded(normalizedTask, workingInfo.workingPath)
      : { executionPath: workingInfo.workingPath, syncBack: () => {} };
  const edits = normalizedTask.input.edits || [];
  const plannedExports = Array.isArray(normalizedTask.output?.exports)
    ? normalizedTask.output.exports
    : [];
  const matchImagePath = normalizedTask.options?.matchImagePath
    ? path.resolve(expandHome(normalizedTask.options.matchImagePath))
    : "";
  const enableBundleZip = normalizedTask.options?.bundleZip === true;
  const plannedPngPaths = plannedExports
    .filter((item) => item.format === "png")
    .map((item) =>
      item.mode === "layer_sets"
        ? resolvePngOutputDir(item, workingInfo.workingPath)
        : resolvePngOutputPath(item, workingInfo.workingPath),
    );
  if (dryRun) {
    const firstLayerSetExport = plannedExports.find(
      (item) => item.format === "png" && item.mode === "layer_sets",
    );
    const firstLayerSetDir = firstLayerSetExport
      ? resolvePngOutputDir(firstLayerSetExport, workingInfo.workingPath)
      : "";
    const plannedBundleZipPath =
      enableBundleZip && firstLayerSetDir
        ? resolveBundleZipPath(normalizedTask, firstLayerSetDir, workingInfo.workingPath)
        : "";
    const preview = {
      taskId: normalizedTask.taskId,
      status: "dry-run",
      code: ErrorCodes.OK,
      resolvedPath: resolved.path,
      workingPath: workingInfo.workingPath,
      executionPath: pathBridge.executionPath,
      via: resolved.via,
      candidates: resolved.candidates || [],
      edits,
      plannedPngPaths,
      selectedPngPath: "",
      bundleZipPath: plannedBundleZipPath,
      confidence: 0,
      candidates: [],
      matchImagePath,
      bundleZipEnabled: enableBundleZip,
      platform,
    };
    const auditPath = appendAudit(preview);
    preview.auditLogPath = auditPath;
    printResultAndExit(preview, 0);
  }

  let backupPath;
  try {
    if (!normalizedTask.options || normalizedTask.options.createBackup !== false) {
      backupPath = createBackup(resolved.path);
    }
  } catch (error) {
    const payload = {
      taskId: normalizedTask.taskId,
      status: "error",
      code: ErrorCodes.E_BACKUP_FAILED,
      message: error.message,
    };
    payload.auditLogPath = appendAudit(payload);
    printResultAndExit(payload, 1);
  }

  let result;
  let styleLockFallbackUsed = false;
  const styleLockEnabled = normalizedTask.options?.styleLock !== false;
  const styleLockSoftRetryEnabled =
    styleLockEnabled && normalizedTask.options?.styleLockSoftRetry !== false;
  const retryEnabled = Boolean(normalizedTask.options && normalizedTask.options.retryOnLockedFile);
  const maxRetries = Math.max(
    0,
    Math.min(5, (normalizedTask.options && normalizedTask.options.maxRetries) || 2),
  );
  const timeoutMs = args.timeoutMs || 90_000;

  if (platform === "darwin" || platform === "win32") {
    for (const edit of edits) {
      if (edit.op === "place_image") {
        // Image placement op: call the dedicated place-image script.
        const execPath = platform === "darwin" ? pathBridge.executionPath : workingInfo.workingPath;
        result = executeWithRetry({
          maxRetries,
          retryEnabled,
          execute: () => {
            if (platform === "darwin") {
              return runMacPlaceImage(
                execPath,
                edit.imagePath,
                edit.layerName || "",
                edit.position || "top",
                edit.visible !== false,
                execPath,
                timeoutMs,
                edit.targetArtboard || "",
              );
            }
            // Windows: not yet implemented; fall through to error.
            return { status: 1, stderr: "E_PLATFORM_UNSUPPORTED: place_image not supported on Windows yet.", stdout: "" };
          },
        });
      } else {
        // Text edit op (replace_text / delete_text).
        result = executeWithRetry({
          maxRetries,
          retryEnabled,
          execute: () => {
            if (platform === "darwin") {
              return runMacModify(
                pathBridge.executionPath,
                edit.layerName,
                edit.newText,
                pathBridge.executionPath,
                timeoutMs,
                styleLockEnabled,
              );
            }
            return runWinModify(
              workingInfo.workingPath,
              edit.layerName,
              edit.newText,
              workingInfo.workingPath,
              timeoutMs,
              styleLockEnabled,
            );
          },
        });
        if (!result || result.status !== 0) {
          const message = `${result?.stderr || ""}\n${result?.stdout || ""}`;
          if (styleLockSoftRetryEnabled && message.includes("E_STYLE_MISMATCH")) {
            const relaxedResult = executeWithRetry({
              maxRetries,
              retryEnabled,
              execute: () => {
                if (platform === "darwin") {
                  return runMacModify(
                    pathBridge.executionPath,
                    edit.layerName,
                    edit.newText,
                    pathBridge.executionPath,
                    timeoutMs,
                    false,
                  );
                }
                return runWinModify(
                  workingInfo.workingPath,
                  edit.layerName,
                  edit.newText,
                  workingInfo.workingPath,
                  timeoutMs,
                  false,
                );
              },
            });
            if (relaxedResult && relaxedResult.status === 0) {
              styleLockFallbackUsed = true;
              result = relaxedResult;
            }
          }
        }
      }
      if (!result || result.status !== 0) {
        break;
      }
    }
    if (platform === "darwin") {
      pathBridge.syncBack();
    }
  } else {
    printResultAndExit(
      {
        taskId: normalizedTask.taskId,
        status: "error",
        code: ErrorCodes.E_PLATFORM_UNSUPPORTED,
        message: `Unsupported platform: ${platform}`,
      },
      1,
    );
  }

  if (result?.error && result.error.code === "ETIMEDOUT") {
    printResultAndExit(
      {
        taskId: normalizedTask.taskId,
        status: "error",
        code: ErrorCodes.E_EXEC_TIMEOUT,
        message: "Photoshop execution timed out.",
      },
      1,
    );
  }

  if (!result || result.status !== 0) {
    const stderr = ((result && result.stderr) || "").trim();
    const stdout = ((result && result.stdout) || "").trim();
    const message = stderr || stdout || "Unknown execution failure.";
    const payload = {
      taskId: normalizedTask.taskId,
      status: "error",
      code: mapErrorCode(message),
      message,
      backupPath,
    };
    const availableLayers = parseAvailableLayers(message);
    if (availableLayers.length > 0) {
      payload.availableLayers = availableLayers;
      const failedEdit = edits.find((item) =>
        message.includes(`E_LAYER_NOT_FOUND: ${item.layerName}`),
      );
      const targetLayer = failedEdit ? failedEdit.layerName : "";
      payload.suggestedLayers = buildFuzzyLayerSuggestions(targetLayer, availableLayers);
      payload.suggestion =
        payload.suggestedLayers.length > 0
          ? `Try one of: ${payload.suggestedLayers.join(", ")}`
          : "Pick a layer from availableLayers.";
    }
    payload.auditLogPath = appendAudit(payload);
    printResultAndExit(payload, 1);
  }

  let finalPsdPath = workingInfo.workingPath;
  try {
    finalPsdPath = resolveFinalPsdPath(normalizedTask, workingInfo.workingPath);
  } catch (error) {
    const payload = {
      taskId: normalizedTask.taskId,
      status: "error",
      code: ErrorCodes.E_OUTPUT_WRITE_FAILED,
      message: error.message,
    };
    payload.auditLogPath = appendAudit(payload);
    printResultAndExit(payload, 1);
  }

  const pngOutputs = [];
  const layerSetOutputDirs = [];
  // Snapshot pixel hashes of existing slice files BEFORE re-export, so we can
  // identify which slices changed content (= contain the modified text layer).
  const preExportHashesByDir = new Map();
  for (const item of plannedExports) {
    if (item.format !== "png") {
      continue;
    }
    const artboardTarget = item.artboardName || "";
    const exportMode = artboardTarget ? "artboard" : (item.mode === "layer_sets" ? "layer_sets" : "single");
    const pngPath = resolvePngOutputPath(item, finalPsdPath);
    const pngDir = (exportMode === "layer_sets" || exportMode === "artboard") ? resolvePngOutputDir(item, finalPsdPath) : "";
    if (exportMode === "layer_sets" || exportMode === "artboard") {
      fs.mkdirSync(pngDir, { recursive: true });
      if (!preExportHashesByDir.has(pngDir)) {
        preExportHashesByDir.set(pngDir, await snapshotDirectoryHashes(pngDir));
      }
    } else {
      ensureParentDir(pngPath);
    }
    const artboardName = artboardTarget;
    const exportResult =
      platform === "darwin"
        ? runMacExportPng(finalPsdPath, pngPath, timeoutMs, exportMode, pngDir, artboardName)
        : runWinExportPng(finalPsdPath, pngPath, timeoutMs);
    if (exportResult.status !== 0) {
      const payload = {
        taskId: normalizedTask.taskId,
        status: "error",
        code: ErrorCodes.E_EXPORT_FAILED,
        message: (exportResult.stderr || exportResult.stdout || "").trim() || "PNG export failed",
        psdOutputPath: finalPsdPath,
      };
      payload.auditLogPath = appendAudit(payload);
      printResultAndExit(payload, 1);
    }
    if (exportMode === "layer_sets" || exportMode === "artboard") {
      const exported = listExportedImagesInDir(pngDir);
      if (exported.length === 0) {
        const payload = {
          taskId: normalizedTask.taskId,
          status: "error",
          code: ErrorCodes.E_EXPORT_FAILED,
          message: `No image files (PNG/JPG/GIF/WebP) exported in directory: ${pngDir}`,
          psdOutputPath: finalPsdPath,
        };
        payload.auditLogPath = appendAudit(payload);
        printResultAndExit(payload, 1);
      }
      layerSetOutputDirs.push(pngDir);
      pngOutputs.push(...exported);
    } else {
      pngOutputs.push(pngPath);
    }
  }

  // --- Slice selection: find the slice that contains the modified text ---
  // Priority 1: before-after pixel hash diff (most reliable — identifies the
  //   slice whose content actually changed after the text edit).
  // Priority 2: visual similarity against the user's screenshot (fallback for
  //   first-run scenarios where no previous exports exist).
  let selectedPngPath = "";
  let confidence = 0;
  let candidates = [];
  let selectionMethod = "";

  if (layerSetOutputDirs.length > 0 && pngOutputs.length > 0) {
    try {
      const changedSlices = [];
      for (const dir of layerSetOutputDirs) {
        const before = preExportHashesByDir.get(dir);
        if (!before || before.size === 0) continue;
        const after = await snapshotDirectoryHashes(dir);
        const changed = findChangedFiles(before, after);
        changedSlices.push(...changed);
      }
      if (changedSlices.length > 0) {
        selectedPngPath = changedSlices[0];
        confidence = 1.0;
        selectionMethod = "before_after_diff";
        candidates = changedSlices.map((p) => ({
          path: p,
          score: 1.0,
          reason: "Content changed after text edit (before/after diff).",
        }));
      }
    } catch (_err) {
      // Fall through to visual matching.
    }
  }

  if (!selectedPngPath && matchImagePath && pngOutputs.length > 0) {
    try {
      const ranked = await rankImagesByVisualSimilarity({
        referenceImagePath: matchImagePath,
        candidatePaths: pngOutputs,
      });
      candidates = ranked.map((item) => ({
        path: item.path,
        score: Number(item.score.toFixed(4)),
        reason: item.reason,
      }));
      if (ranked.length > 0) {
        selectedPngPath = ranked[0].path;
        confidence = Number(ranked[0].score.toFixed(4));
        selectionMethod = "visual_similarity";
      }
    } catch (_err) {
      // Keep success path; selection is an optional addon for dual delivery.
    }
  }

  let bundleZipPath = "";
  if (enableBundleZip && layerSetOutputDirs.length > 0) {
    try {
      const outputDir = layerSetOutputDirs[0];
      const zipPath = resolveBundleZipPath(normalizedTask, outputDir, finalPsdPath);
      bundleZipPath = await buildZipFromDirectory(outputDir, zipPath);
    } catch (error) {
      const payload = {
        taskId: normalizedTask.taskId,
        status: "error",
        code: ErrorCodes.E_EXPORT_FAILED,
        message: `ZIP bundle failed: ${error.message}`,
        psdOutputPath: finalPsdPath,
      };
      payload.auditLogPath = appendAudit(payload);
      printResultAndExit(payload, 1);
    }
  }

  const success = {
    taskId: normalizedTask.taskId,
    status: "success",
    code: ErrorCodes.OK,
    resolvedPath: resolved.path,
    psdOutputPath: finalPsdPath,
    pngOutputPath: pngOutputs[0],
    pngOutputPaths: pngOutputs,
    selectedPngPath,
    bundleZipPath,
    confidence,
    candidates,
    selectionMethod: selectionMethod || "none",
    matchImagePath: matchImagePath || "",
    editsApplied: edits.map((item) =>
      item.op === "place_image" ? `[place_image] ${item.imagePath}` : item.layerName
    ),
    styleLockFallbackUsed,
    backupPath,
    via: resolved.via,
    sourceMode: workingInfo.sourceMode,
    durationMs: Date.now() - start,
    runnerStdout: (result.stdout || "").trim(),
  };
  success.auditLogPath = appendAudit(success);
  printResultAndExit(success, 0);
}

main().catch((error) => {
  printResultAndExit(
    {
      status: "error",
      code: ErrorCodes.E_EXEC_FAILED,
      message: error instanceof Error ? error.message : String(error),
    },
    1,
  );
});
