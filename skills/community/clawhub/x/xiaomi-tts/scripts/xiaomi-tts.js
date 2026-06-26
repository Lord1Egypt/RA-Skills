#!/usr/bin/env node
/**
 * MiMo TTS 语音合成脚本
 * 用法: node xiaomi-tts.js "要合成的文本" [--voice default_zh] [--style 夹子音] [--output out.wav]
 */

import { writeFileSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { parseArgs } from "node:util";
import { homedir } from "node:os";

const API_URL = "https://api.xiaomimimo.com/v1/chat/completions";
const MODEL = "mimo-v2-tts";
const DEFAULT_VOICE = "default_zh";

function resolveApiKey(override) {
  if (override) return override;
  if (process.env.MIMO_API_KEY) return process.env.MIMO_API_KEY;

  const configPath = join(homedir(), ".openclaw", "config.json");
  if (existsSync(configPath)) {
    try {
      const cfg = JSON.parse(readFileSync(configPath, "utf-8"));
      if (cfg.mimo_api_key || cfg.MIMO_API_KEY) return cfg.mimo_api_key || cfg.MIMO_API_KEY;
    } catch { /* ignore */ }
  }

  console.error("错误: 未找到 MIMO_API_KEY，请通过环境变量或 --api-key 参数提供");
  process.exit(1);
}

function buildContent(text, style) {
  return style ? `<style>${style}</style>${text}` : text;
}

async function tts(text, { voice = DEFAULT_VOICE, style = "", apiKey }) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: MODEL,
      messages: [
        { role: "user", content: "你好" },
        { role: "assistant", content: buildContent(text, style) },
      ],
      audio: { format: "wav", voice },
    }),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`API 错误 ${res.status}: ${body || res.statusText}`);
  }

  const data = await res.json();
  const audioData = data?.choices?.[0]?.message?.audio?.data;
  if (!audioData) {
    throw new Error("API 返回数据中未包含音频内容");
  }

  return Buffer.from(audioData, "base64");
}

async function main() {
  const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
      voice:     { type: "string", short: "v", default: DEFAULT_VOICE },
      style:     { type: "string", short: "s", default: "" },
      output:    { type: "string", short: "o" },
      "api-key": { type: "string", short: "k" },
    },
  });

  const text = positionals[0];
  if (!text) {
    console.error("用法: node xiaomi-tts.js \"要合成的文本\" [--voice default_zh] [--style 夹子音] [--output out.wav]");
    process.exit(1);
  }

  const apiKey = resolveApiKey(values["api-key"]);

  try {
    const audio = await tts(text, { voice: values.voice, style: values.style, apiKey });

    if (values.output) {
      writeFileSync(values.output, audio);
      console.log(`音频已保存: ${values.output}`);
    } else {
      process.stdout.write(audio);
    }
  } catch (e) {
    console.error(`合成失败: ${e.message}`);
    process.exit(1);
  }
}

main();
