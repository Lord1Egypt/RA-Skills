import fs from "node:fs";
import path from "node:path";
import { ErrorCodes } from "./error-codes.js";
import { expandHome } from "./paths.js";

export function readTask(taskPath) {
  const resolvedPath = path.resolve(expandHome(taskPath));
  const raw = fs.readFileSync(resolvedPath, "utf8");
  return JSON.parse(raw);
}

export function validateTask(task) {
  if (!task || typeof task !== "object") {
    return { ok: false, code: ErrorCodes.E_TASK_INVALID, message: "Task must be an object." };
  }
  if (!task.taskId || typeof task.taskId !== "string") {
    return { ok: false, code: ErrorCodes.E_TASK_INVALID, message: "taskId is required." };
  }
  if (!task.input || typeof task.input !== "object") {
    return { ok: false, code: ErrorCodes.E_TASK_INVALID, message: "input is required." };
  }
  const { exactPath, fileHint, layerName, newText, edits } = task.input;
  if (!exactPath && !fileHint) {
    return {
      ok: false,
      code: ErrorCodes.E_TASK_INVALID,
      message: "input.exactPath or input.fileHint is required.",
    };
  }
  const hasLegacy = typeof layerName === "string" && typeof newText === "string";
  const hasEdits = Array.isArray(edits) && edits.length > 0;
  if (!hasLegacy && !hasEdits) {
    return {
      ok: false,
      code: ErrorCodes.E_TASK_INVALID,
      message: "input.edits[] or input.layerName/input.newText is required.",
    };
  }
  if (hasEdits) {
    for (const item of edits) {
      if (!item || typeof item !== "object") {
        return { ok: false, code: ErrorCodes.E_TASK_INVALID, message: "input.edits[] item must be an object." };
      }
      const op = item.op === "delete_text" ? "delete_text"
        : item.op === "place_image" ? "place_image"
        : "replace_text";
      if (op === "place_image") {
        if (!item.imagePath || typeof item.imagePath !== "string" || item.imagePath.trim().length === 0) {
          return {
            ok: false,
            code: ErrorCodes.E_TASK_INVALID,
            message: "input.edits[].imagePath is required for place_image.",
          };
        }
      } else {
        if (!item.layerName || typeof item.layerName !== "string" || item.layerName.trim().length === 0) {
          return {
            ok: false,
            code: ErrorCodes.E_TASK_INVALID,
            message: "input.edits[].layerName is required for replace_text/delete_text.",
          };
        }
        if (op !== "delete_text" && typeof item.newText !== "string") {
          return {
            ok: false,
            code: ErrorCodes.E_TASK_INVALID,
            message: "input.edits[].newText is required for replace_text.",
          };
        }
      }
    }
  }
  return { ok: true, code: ErrorCodes.OK };
}

export function normalizeTask(task) {
  const edits = Array.isArray(task.input.edits)
    ? task.input.edits
    : [{ layerName: task.input.layerName, newText: task.input.newText, op: "replace_text" }];
  const normalizedEdits = edits
    .filter((item) => item && typeof item === "object")
    .map((item) => {
      const op = item.op === "delete_text" ? "delete_text"
        : item.op === "place_image" ? "place_image"
        : "replace_text";
      if (op === "place_image") {
        return {
          op: "place_image",
          imagePath: String(item.imagePath || "").trim(),
          layerName: typeof item.layerName === "string" ? item.layerName.trim() : "",
          position: typeof item.position === "string" ? item.position : "top",
          visible: item.visible !== false,
          targetArtboard: typeof item.targetArtboard === "string" ? item.targetArtboard.trim() : "",
        };
      }
      return {
        op,
        layerName: typeof item.layerName === "string" ? item.layerName.trim() : "",
        newText: op === "delete_text" ? "" : typeof item.newText === "string" ? item.newText : "",
      };
    })
    .filter((item) => {
      if (item.op === "place_image") return item.imagePath.length > 0;
      return item.layerName.length > 0;
    });

  const workflow = task.workflow || {};
  const output = task.output || {};
  const normalizedOutput = {
    psd: output.psd || {
      mode: output.mode || "overwrite",
      path: output.path,
    },
    bundle: output.bundle || {},
      exports: Array.isArray(output.exports)
      ? output.exports.map((item) => ({
          ...item,
          mode: item?.mode === "layer_sets" ? "layer_sets" : "single",
          artboardName: typeof item?.artboardName === "string" ? item.artboardName : "",
        }))
      : [],
  };

  return {
    ...task,
    workflow: {
      sourceMode: workflow.sourceMode || "inplace",
      copyToDir: workflow.copyToDir,
    },
    input: {
      exactPath: task.input.exactPath,
      fileHint: task.input.fileHint,
      edits: normalizedEdits,
    },
    output: normalizedOutput,
  };
}
