#!/usr/bin/env node
import { parseArgs } from "node:util";
import path from "node:path";
import fs from "node:fs/promises";
import { execFile } from "node:child_process";

const DASHSCOPE_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation";

const VALID_VOICE_IDS = [
  "Cherry",
  "Serena",
  "Ethan",
  "Chelsie",
  "Momo",
  "Vivian",
  "Moon",
  "Maia",
  "Kai",
  "Nofish",
  "Bella",
  "Eldric Sage",
  "Mia",
  "Mochi",
  "Bellona",
  "Vincent",
  "Bunny",
  "Neil",
  "Elias",
  "Arthur",
  "Nini",
  "Ebona",
  "Seren",
  "Pip",
  "Stella"
];

class CliError extends Error {
  constructor(message, options = {}) {
    super(message);
    this.name = "CliError";
    this.code = options.code || "CLI_ERROR";
    this.details = options.details;
  }
}

function parseCliArgs(argv = process.argv.slice(2)) {
  const { values } = parseArgs({
    args: argv,
    options: {
      text: { type: "string" },
      voice: { type: "string" },
      instructions: { type: "string" },
      "optimize-instructions": { type: "boolean", default: true },
      "output-dir": { type: "string" },
      "temp-id": { type: "string" },
      help: { type: "boolean", short: "h" }
    },
    allowPositionals: false
  });

  if (values.help) {
    return { help: true };
  }

  if (!values.text || !values.text.trim()) {
    throw new CliError("参数 --text 为必填", {
      code: "MISSING_TEXT",
      details: "示例: clibase.js --text \"你好\" --voice Cherry --instructions \"语气平稳\" --output-dir ./output"
    });
  }

  if (!values["output-dir"] || !values["output-dir"].trim()) {
    throw new CliError("参数 --output-dir 为必填", {
      code: "MISSING_OUTPUT_DIR",
      details: "示例: clibase.js --text \"你好\" --voice Cherry --instructions \"语气平稳\" --output-dir ./output"
    });
  }

  const voice = values.voice ? values.voice.trim() : undefined;
  if (voice && !VALID_VOICE_IDS.includes(voice)) {
    throw new CliError(
      `无效的音色 ID: "${voice}"`,
      {
        code: "INVALID_VOICE_ID",
        details: `可选音色列表: ${VALID_VOICE_IDS.join(", ")}`
      }
    );
  }

  return {
    text: values.text.trim(),
    voice,
    instructions: values.instructions ? values.instructions.trim() : undefined,
    optimizeInstructions: values["optimize-instructions"],
    outputDir: values["output-dir"].trim(),
    tempId: values["temp-id"] ? values["temp-id"].trim() : undefined
  };
}

function helpText() {
  return [
    " TTS CLI Base",
    "",
    "用法:",
    "  clibase.js --text <文本> --voice <音色> --instructions <指令> --output-dir <输出目录> [--temp-id <临时ID>] [--optimize-instructions]",
    "",
    "参数:",
    "  --text                   必填，待合成文本",
    "  --voice                  必填，音色名称",
    "  --instructions           必填，指令内容",
    "  --output-dir             必填，输出目录路径",
    "  --optimize-instructions  可选，是否优化指令（默认 true）",
    "  --temp-id                可选，临时文件夹名称（用于批量测试）",
    "  -h, --help               显示帮助"
  ].join("\n");
}

function getApiKey(env = process.env) {
  const key = env.DASHSCOPE_API_KEY;
  if (!key) {
    throw new CliError("缺少 DASHSCOPE_API_KEY 环境变量", {
      code: "MISSING_API_KEY",
      details: "请先执行: export DASHSCOPE_API_KEY=<your_api_key>"
    });
  }
  return key;
}

function createPayload({ text, voice, instructions, optimizeInstructions }) {
  const input = { text };

  if (voice) {
    input.voice = voice;
  }
  if (instructions) {
    input.instructions = instructions;
    input.optimize_instructions = optimizeInstructions ? "True" : "False";
  }

  return {
    model: "qwen3-tts-instruct-flash",
    input
  };
}

function parseAudioUrl(responseJson) {
  return responseJson && responseJson.output && responseJson.output.audio && responseJson.output.audio.url
    ? responseJson.output.audio.url
    : undefined;
}

async function synthesizeSpeech({ apiKey, text, voice, instructions, optimizeInstructions, fetchImpl = fetch }) {
  const payload = createPayload({ text, voice, instructions, optimizeInstructions });
  const response = await fetchImpl(DASHSCOPE_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  let json;
  try {
    json = await response.json();
  } catch (error) {
    throw new CliError("TTS 响应不是合法 JSON", {
      code: "INVALID_JSON_RESPONSE"
    });
  }

  if (!response.ok) {
    const message = json.message || json.code || "未知错误";
    throw new CliError(`TTS 请求失败: ${response.status} ${message}`, {
      code: "TTS_REQUEST_FAILED",
      details: JSON.stringify(json)
    });
  }

  const audioUrl = parseAudioUrl(json);
  if (!audioUrl) {
    throw new CliError("响应缺少 output.audio.url", {
      code: "MISSING_AUDIO_URL",
      details: JSON.stringify(json)
    });
  }

  return {
    audioUrl,
    payload,
    raw: json
  };
}

function buildOutputPaths({ outputDir, tempId }) {
  const folderName = tempId ? `tmp-${tempId}` : `tmp-${Date.now()}`;
  const folderPath = path.resolve(outputDir, folderName);

  return {
    folderPath,
    sourcePath: path.join(folderPath, "source.mp3"),
    opusPath: path.join(folderPath, "audio.opus"),
    requestPath: path.join(folderPath, "request.json"),
    responsePath: path.join(folderPath, "response.json")
  };
}

function runFfmpeg({ inputPath, outputPath, execFileImpl = execFile }) {
  return new Promise((resolve, reject) => {
    execFileImpl(
      "ffmpeg",
      ["-y", "-i", inputPath, "-vn", "-c:a", "libopus", outputPath],
      (error, stdout, stderr) => {
        if (error) {
          reject(
            new CliError(`ffmpeg 转码失败: ${error.message}`, {
              code: "FFMPEG_CONVERT_FAILED",
              details: stderr || stdout
            })
          );
          return;
        }
        resolve();
      }
    );
  });
}

async function downloadAudio({
  audioUrl,
  fetchImpl = fetch,
  fsImpl = fs,
  execFileImpl = execFile
}) {
  const response = await fetchImpl(audioUrl);
  if (!response.ok) {
    throw new CliError(`音频下载失败: ${response.status} ${response.statusText}`, {
      code: "AUDIO_DOWNLOAD_FAILED"
    });
  }

  const arrayBuffer = await response.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);

  return buffer;
}

async function run(argv = process.argv.slice(2), deps = {}) {
  const stdout = deps.stdout || process.stdout;
  const stderr = deps.stderr || process.stderr;
  const env = deps.env || process.env;
  const fetchImpl = deps.fetchImpl || fetch;
  const fsImpl = deps.fsImpl || fs;
  const execFileImpl = deps.execFileImpl || execFile;

  try {
    const args = parseCliArgs(argv);
    if (args.help) {
      stdout.write(`${helpText()}\n`);
      return 0;
    }

    const apiKey = getApiKey(env);
    const ttsResult = await synthesizeSpeech({
      apiKey,
      text: args.text,
      voice: args.voice,
      instructions: args.instructions,
      optimizeInstructions: args.optimizeInstructions,
      fetchImpl
    });

    const paths = buildOutputPaths({
      outputDir: args.outputDir,
      tempId: args.tempId
    });

    await fsImpl.mkdir(paths.folderPath, { recursive: true });

    await fsImpl.writeFile(
      paths.requestPath,
      JSON.stringify(
        {
          text: args.text,
          voice: args.voice,
          instructions: args.instructions
        },
        null,
        2
      ),
      "utf8"
    );

    await fsImpl.writeFile(
      paths.responsePath,
      JSON.stringify(
        {
          audio_url: ttsResult.audioUrl
        },
        null,
        2
      ),
      "utf8"
    );

    const audioBuffer = await downloadAudio({
      audioUrl: ttsResult.audioUrl,
      fetchImpl,
      fsImpl
    });

    await fsImpl.writeFile(paths.sourcePath, audioBuffer);

    await runFfmpeg({
      inputPath: paths.sourcePath,
      outputPath: paths.opusPath,
      execFileImpl
    });

    try {
      await fsImpl.unlink(paths.sourcePath);
    } catch (error) {
    }

    stdout.write(`合成成功\n`);
    stdout.write(`输出目录: ${paths.folderPath}\n`);
    stdout.write(`音频文件: ${paths.opusPath}\n`);
    return 0;
  } catch (error) {
    if (error instanceof CliError) {
      stderr.write(`错误[${error.code}]: ${error.message}\n`);
      if (error.details) {
        stderr.write(`诊断: ${error.details}\n`);
      }
      return 1;
    }
    stderr.write(`错误[UNEXPECTED]: ${error.message}\n`);
    return 1;
  }
}

if (import.meta.main) {
  run().then((code) => {
    process.exitCode = code;
  });
}

export { run };