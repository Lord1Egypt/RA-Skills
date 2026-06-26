#!/usr/bin/env node
/**
 * 文生图 - 使用阿里云通义万相 (DashScope) API
 * 用法: node generate_image.js --prompt "描述" [--size 1664*928] [--api-key KEY]
 * 输出: MEDIA_URL: <url> 或 MEDIA: <本地路径>
 *
 * 环境变量: DASHSCOPE_API_KEY
 * 或 openclaw.json: skills.entries.tianshu-image.api_key
 */

const fs = require('fs');
const path = require('path');

const DEFAULT_NEGATIVE =
  '低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。';

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    prompt: null,
    model: 'qwen-image-max',
    size: '1664*928',
    negativePrompt: DEFAULT_NEGATIVE,
    promptExtend: true,
    watermark: false,
    apiKey: process.env.DASHSCOPE_API_KEY || null,
    filename: null,
  };
  const sizes = ['1664*928', '1024*1024', '720*1280', '1280*720'];
  const models = ['qwen-image-max', 'qwen-image-turbo', 'qwen-image-plus-2026-01-09'];

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--prompt' || args[i] === '-p') {
      opts.prompt = args[++i];
    } else if (args[i] === '--model' || args[i] === '-m') {
      opts.model = models.includes(args[i + 1]) ? args[++i] : opts.model;
    } else if (args[i] === '--size' || args[i] === '-s') {
      opts.size = sizes.includes(args[i + 1]) ? args[++i] : opts.size;
    } else if (args[i] === '--negative-prompt' || args[i] === '-n') {
      opts.negativePrompt = args[++i];
    } else if (args[i] === '--no-prompt-extend') {
      opts.promptExtend = false;
    } else if (args[i] === '--watermark') {
      opts.watermark = true;
    } else if (args[i] === '--api-key' || args[i] === '-k') {
      opts.apiKey = args[++i];
    } else if (args[i] === '--filename' || args[i] === '-f') {
      opts.filename = args[++i];
    }
  }
  return opts;
}

async function main() {
  const opts = parseArgs();
  if (!opts.prompt) {
    console.error('用法: node generate_image.js --prompt "描述" [--size 1664*928] [--api-key KEY]');
    process.exit(1);
  }
  if (!opts.apiKey) {
    console.error('请设置 DASHSCOPE_API_KEY 或传入 --api-key');
    process.exit(1);
  }

  const payload = {
    model: opts.model,
    input: {
      messages: [{ role: 'user', content: [{ text: opts.prompt }] }],
    },
    parameters: {
      negative_prompt: opts.negativePrompt,
      prompt_extend: opts.promptExtend,
      watermark: opts.watermark,
      size: opts.size,
    },
  };

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 120000);

  try {
    const res = await fetch(
      'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${opts.apiKey}`,
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      }
    );

    clearTimeout(timeout);
    const result = await res.json();

    if (result.code) {
      console.error('API Error:', result.message || 'Unknown error');
      process.exit(1);
    }

    const choices = result?.output?.choices ?? [];
    if (!choices.length) {
      console.error('No choices in response');
      process.exit(1);
    }
    const content = choices[0]?.message?.content ?? [];
    const imageUrl = content[0]?.image;
    if (!imageUrl) {
      console.error('No image URL in response');
      process.exit(1);
    }

    if (opts.filename) {
      const dir = path.dirname(opts.filename);
      if (dir && !fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      const imgRes = await fetch(imageUrl);
      const buf = Buffer.from(await imgRes.arrayBuffer());
      fs.writeFileSync(opts.filename, buf);
      const fullPath = path.resolve(opts.filename);
      console.log(`MEDIA: ${fullPath}`);
    } else {
      console.log(`MEDIA_URL: ${imageUrl}`);
    }
  } catch (e) {
    clearTimeout(timeout);
    console.error(e.message || e);
    process.exit(1);
  }
}

main();
