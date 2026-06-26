#!/usr/bin/env node
/**
 * 通义万相 2.6 视频生成 - Node 实现
 * 用法: node generate_video.js t2v --prompt "描述" [--duration 5] [--resolution 720P]
 *       node generate_video.js i2v --prompt "描述" --image-url "https://..." [--duration 5]
 */

const apiKey = process.env.DASHSCOPE_API_KEY;
if (!apiKey) {
  console.error('请设置 DASHSCOPE_API_KEY 环境变量');
  process.exit(1);
}

const BASE = 'https://dashscope.aliyuncs.com/api/v1';

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { mode: null, prompt: null, imageUrl: null, duration: 5, resolution: '720P' };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === 't2v' || args[i] === 'i2v') opts.mode = args[i];
    else if (args[i] === '--prompt') opts.prompt = args[++i];
    else if (args[i] === '--image-url') opts.imageUrl = args[++i];
    else if (args[i] === '--duration') opts.duration = parseInt(args[++i]) || 5;
    else if (args[i] === '--resolution') opts.resolution = args[++i] === '1080P' ? '1080P' : '720P';
  }
  return opts;
}

async function createTask(opts) {
  const input = { prompt: opts.prompt };
  if (opts.imageUrl) input.image_url = opts.imageUrl;
  const res = await fetch(`${BASE}/services/aigc/video-generation/video-synthesis`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'X-DashScope-Async': 'enable',
    },
    body: JSON.stringify({
      model: 'wan2.6-t2v',
      input,
      parameters: {
        resolution: opts.resolution,
        duration: opts.duration,
        shot_type: 'single',
        watermark: false,
      },
    }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.message || `HTTP ${res.status}`);
  return data.output?.task_id;
}

async function pollTask(taskId, timeout = 600000, interval = 10000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const res = await fetch(`${BASE}/tasks/${taskId}`, {
      headers: { Authorization: `Bearer ${apiKey}` },
    });
    const data = await res.json();
    const status = data?.output?.task_status;
    if (status === 'SUCCEEDED') {
      const out = data.output;
      if (out?.results?.[0]?.url) return out.results[0].url;
      if (out?.result?.url) return out.result.url;
      throw new Error('Unexpected response structure');
    }
    if (status === 'FAILED') throw new Error(data?.message || '任务失败');
    await new Promise((r) => setTimeout(r, interval));
  }
  throw new Error(`任务超时 (${timeout / 1000}秒)`);
}

async function main() {
  const opts = parseArgs();
  if (!opts.mode || !opts.prompt) {
    console.error('用法: node generate_video.js t2v|i2v --prompt "描述" [--image-url URL] [--duration 5] [--resolution 720P]');
    process.exit(1);
  }
  if (opts.mode === 'i2v' && !opts.imageUrl) {
    console.error('i2v 模式需要 --image-url');
    process.exit(1);
  }
  const taskId = await createTask(opts);
  const url = await pollTask(taskId);
  console.log('VIDEO_URL:', url);
}

main().catch((e) => {
  console.error('Error:', e.message);
  process.exit(1);
});
