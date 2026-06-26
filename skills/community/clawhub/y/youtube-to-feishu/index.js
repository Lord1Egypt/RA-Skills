/**
 * OpenClaw Skill Tool Registration — youtube-to-feishu
 *
 * Registers tool:
 *   - youtube_upload: download YouTube audio and upload to Feishu
 */

const { execFile } = require("child_process");
const path = require("path");
const fs = require("fs");

const PYTHON = process.platform === "win32" ? "python" : "python3";
const SCRIPT_PATH = path.join(__dirname, "youtube_upload.py");
const TEMP_DIR = path.join(__dirname, "..", "..", "temp");

/**
 * Run Python script and return structured result.
 */
function _runPython(args, config) {
  return new Promise((resolve) => {
    const child = execFile(PYTHON, [SCRIPT_PATH, ...args], {
      maxBuffer: 50 * 1024 * 1024,
      env: { ...process.env, ...config?.env },
      cwd: TEMP_DIR,
    }, (error, stdout, stderr) => {
      if (error) {
        resolve({
          status: "error",
          message: `Execution failed: ${error.message}`,
          stderr: stderr?.slice(-2000),
        });
        return;
      }

      const lines = stdout.trim().split("\n");
      let result;
      try {
        const jsonStart = lines.findIndex((l) => l.trim().startsWith("{"));
        if (jsonStart >= 0) {
          result = JSON.parse(lines.slice(jsonStart).join("\n"));
        }
      } catch {
        result = null;
      }

      resolve({
        status: "success",
        progress_log: lines.filter((l) => l.startsWith("[")).join("\n"),
        result: result || { raw_output: stdout.slice(-3000) },
      });
    });

    child.stdout?.on("data", (chunk) => {
      process.stdout.write(chunk);
    });
  });
}

/**
 * youtube_upload — Download YouTube audio and upload to Feishu.
 *
 * @param {object} params
 * @param {string} params.url     - YouTube video URL
 * @param {string} [params.title] - Optional custom title
 * @param {object} config         - OpenClaw skill config
 */
async function youtube_upload(params, config) {
  const url = params.url;
  if (!url || !url.includes("youtube.com") && !url.includes("youtu.be")) {
    return { error: "Please provide a valid YouTube URL, e.g.: https://www.youtube.com/watch?v=..." };
  }

  return _runPython([
    "--url", url,
    ...(params.title ? ["--title", params.title] : []),
  ], config);
}

module.exports = { youtube_upload };
