const fs = require('node:fs');
const path = require('node:path');

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      result[key] = true;
      continue;
    }
    result[key] = next;
    i += 1;
  }
  return result;
}

function ensureDirForFile(filePath) {
  fs.mkdirSync(path.dirname(path.resolve(filePath)), { recursive: true });
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(path.resolve(filePath), 'utf8'));
}

function writeJson(outputPath, data) {
  const text = JSON.stringify(data, null, 2);
  if (outputPath) {
    ensureDirForFile(outputPath);
    fs.writeFileSync(path.resolve(outputPath), text + '\n', 'utf8');
  }
  console.log(text);
}

function canonicalVendor(name) {
  const value = String(name || '').trim().toLowerCase();
  if (!value) return '';
  if (value.includes('minimax') || value.includes('mini max')) return 'minimax';
  if (value.includes('vidu')) return 'vidu';
  if (value.includes('seedance') || value.includes('doubao') || value.includes('ark') || value.includes('volc')) return 'seedance';
  return value;
}

function trimSlash(url) {
  return String(url || '').replace(/\/+$/, '');
}

function resolveV1Base(url) {
  const clean = trimSlash(url);
  if (!clean) return '';
  return /\/v1$/i.test(clean) ? clean : `${clean}/v1`;
}

function looksPlaceholder(value) {
  const text = String(value || '').trim().toLowerCase();
  return !text || text === 'demo' || text.includes('placeholder') || text === 'your_api_key' || text.startsWith('your-');
}

function guessMime(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === '.png') return 'image/png';
  if (ext === '.webp') return 'image/webp';
  if (ext === '.gif') return 'image/gif';
  return 'image/jpeg';
}

function resolveImageInput(input) {
  if (!input) throw new Error('缺少图片输入');
  if (/^data:/i.test(input)) return input;
  if (/^https?:\/\//i.test(input)) return input;
  const full = path.resolve(input);
  if (!fs.existsSync(full)) throw new Error(`图片文件不存在: ${full}`);
  const base64 = fs.readFileSync(full).toString('base64');
  return `data:${guessMime(full)};base64,${base64}`;
}

function parseDataUrl(input) {
  const match = String(input || '').match(/^data:([^;]+);base64,(.+)$/i);
  if (!match) return null;
  return {
    mimeType: match[1],
    buffer: Buffer.from(match[2], 'base64'),
  };
}

async function uploadImageToToApis(stage, imageInput) {
  if (!imageInput) return '';
  if (/^https?:\/\//i.test(imageInput)) return imageInput;

  const data = parseDataUrl(imageInput);
  let buffer = null;
  let mimeType = 'image/jpeg';
  let filename = 'upload.jpg';

  if (data) {
    buffer = data.buffer;
    mimeType = data.mimeType || 'image/jpeg';
    const ext = (mimeType.split('/')[1] || 'jpg').replace(/[^a-z0-9]/ig, '').toLowerCase() || 'jpg';
    filename = `upload.${ext}`;
  } else {
    const full = path.resolve(imageInput);
    if (!fs.existsSync(full)) {
      throw new Error(`图片文件不存在: ${full}`);
    }
    buffer = fs.readFileSync(full);
    mimeType = guessMime(full);
    filename = path.basename(full);
  }

  const form = new FormData();
  const blob = new Blob([buffer], { type: mimeType });
  form.append('file', blob, filename);

  const v1Base = resolveV1Base(stage['接口地址']);
  const url = `${v1Base}/uploads/images`;
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${stage['APIKey']}`,
    },
    body: form,
  });
  const body = await res.json().catch(() => ({}));
  const uploadedUrl = String(body?.data?.url || body?.url || '');
  if (!res.ok || !uploadedUrl) {
    throw new Error(`Vidu 图片上传失败: ${JSON.stringify(body)}`);
  }
  return uploadedUrl;
}

function normalizeViduResolution(input) {
  const text = String(input || '').trim().toLowerCase();
  if (text === '540p' || text === '720p' || text === '1080p') return text;
  const m = text.match(/(540|720|1080)/);
  if (m) return `${m[1]}p`;
  return '720p';
}

function mapViduStatus(value) {
  const status = String(value || '').trim().toLowerCase();
  if (status === 'completed') return 'success';
  if (status === 'failed') return 'fail';
  if (status === 'queued') return 'queued';
  return 'processing';
}

async function submitMinimaxVideo(stage, panel, duration, resolution, isProbe) {
  if (isProbe) {
    return {
      厂商: 'MiniMax',
      模型名: stage['模型名'],
      taskId: `probe-minimax-${Date.now()}`,
      status: 'queued',
      isProbe: true,
      原始响应: { probe: true },
    };
  }

  const url = `${trimSlash(stage['接口地址'])}/video_generation`;
  const payload = {
    model: stage['模型名'],
    prompt: panel.videoPrompt,
    prompt_optimizer: true,
    resolution,
    duration: Number(duration),
  };
  if (panel.imageUrl) {
    payload.first_frame_image = resolveImageInput(panel.imageUrl);
  }

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${stage['APIKey']}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok || data?.base_resp?.status_code !== 0 || !data?.task_id) {
    throw new Error(`MiniMax 视频提交失败: ${JSON.stringify(data)}`);
  }
  return {
    厂商: 'MiniMax',
    模型名: stage['模型名'],
    taskId: String(data.task_id),
    status: 'queued',
    isProbe,
    原始响应: data,
  };
}

async function submitViduVideo(stage, panel, duration, resolution, isProbe) {
  if (isProbe) {
    return {
      厂商: 'Vidu',
      模型名: stage['模型名'],
      taskId: `probe-vidu-${Date.now()}`,
      status: 'queued',
      fileId: '',
      downloadUrl: '',
      isProbe: true,
      原始响应: { probe: true },
    };
  }

  const uploadedImageUrl = panel.imageUrl ? await uploadImageToToApis(stage, panel.imageUrl) : '';
  const v1Base = resolveV1Base(stage['接口地址']);
  const url = `${v1Base}/videos/generations`;

  const payload = {
    model: stage['模型名'],
    duration: Number(duration),
    resolution: normalizeViduResolution(resolution),
  };

  const prompt = String(panel.videoPrompt || panel.subtitleText || '').trim();
  if (prompt) {
    payload.prompt = prompt;
  }
  if (uploadedImageUrl) {
    payload.image_urls = [uploadedImageUrl];
  }
  if (!payload.prompt && !payload.image_urls) {
    throw new Error('Vidu 提交至少需要 prompt 或 image_urls');
  }

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${stage['APIKey']}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const data = await res.json().catch(() => ({}));
  const taskId = String(data?.id || data?.task_id || '');
  if (!res.ok || !taskId) {
    throw new Error(`Vidu 视频提交失败: ${JSON.stringify(data)}`);
  }

  return {
    厂商: 'Vidu',
    模型名: stage['模型名'],
    taskId,
    status: mapViduStatus(data?.status || 'queued'),
    fileId: '',
    downloadUrl: '',
    uploadedImageUrl,
    isProbe,
    原始响应: data,
  };
}

async function submitSeedanceVideo(stage, panel, duration, resolution, isProbe) {
  if (isProbe) {
    return {
      厂商: 'Seedance',
      模型名: stage['模型名'],
      taskId: `probe-seedance-${Date.now()}`,
      status: 'queued',
      fileId: '',
      downloadUrl: '',
      isProbe: true,
      原始响应: { probe: true },
    };
  }

  const base = trimSlash(stage['接口地址']);
  const url = /\/api\/v3\/contents\/generations\/tasks$/i.test(base)
    ? base
    : `${base}/api/v3/contents/generations/tasks`;

  const text = String(panel.videoPrompt || panel.subtitleText || '').trim();
  if (!text) {
    throw new Error('Seedance 提交至少需要 videoPrompt/subtitleText');
  }

  const content = [{ type: 'text', text }];
  if (panel.imageUrl) {
    content.push({
      type: 'image_url',
      role: 'first_frame',
      image_url: { url: resolveImageInput(panel.imageUrl) },
    });
  }

  const payload = {
    model: stage['模型名'],
    content,
    duration: Number(duration),
    resolution: normalizeViduResolution(resolution),
    generate_audio: true,
    camera_fixed: true,
    draft: false,
    seed: Number(stage.seed || 2026033101),
    return_last_frame: true,
  };

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${stage['APIKey']}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const data = await res.json().catch(() => ({}));
  const taskId = String(data?.id || data?.task_id || '');
  if (!res.ok || !taskId) {
    throw new Error(`Seedance 视频提交失败: ${JSON.stringify(data)}`);
  }

  return {
    厂商: 'Seedance',
    模型名: stage['模型名'],
    taskId,
    status: 'queued',
    fileId: '',
    downloadUrl: '',
    isProbe,
    原始响应: data,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const configPath = args.config;
  const panelPath = args.panel;
  const outputPath = args.out;
  const duration = args.duration || '6';
  const resolution = args.resolution || '768P';
  const isProbe = args.probe === true;

  if (!configPath || !panelPath) {
    throw new Error('用法: node submit-official-video.cjs --config <json> --panel <panel-context.json> [--duration 6] [--resolution 768P] [--probe] [--out <json>]');
  }

  const config = readJson(configPath);
  const panel = readJson(panelPath);
  const stage = config?.downstream?.waoo?.video;
  if (!stage?.厂商 || !stage?.接口地址 || !stage?.模型名 || (!isProbe && looksPlaceholder(stage?.APIKey))) {
    throw new Error('视频配置不完整，请先补齐真实 厂商 / 接口地址 / 模型名 / API Key');
  }

  const vendor = canonicalVendor(stage['厂商']);
  let result = null;

  if (vendor === 'minimax') {
    if (!panel?.videoPrompt || !panel?.panelId) {
      throw new Error('MiniMax panel context 不完整，缺少 videoPrompt / panelId');
    }
    result = await submitMinimaxVideo(stage, panel, duration, resolution, isProbe);
  } else if (vendor === 'vidu') {
    if (!panel?.panelId) {
      throw new Error('Vidu panel context 不完整，缺少 panelId');
    }
    result = await submitViduVideo(stage, panel, duration, resolution, isProbe);
  } else if (vendor === 'seedance') {
    if (!panel?.panelId) {
      throw new Error('Seedance panel context 不完整，缺少 panelId');
    }
    result = await submitSeedanceVideo(stage, panel, duration, resolution, isProbe);
  } else {
    throw new Error(`暂不支持的官方视频厂商: ${stage['厂商']}`);
  }

  writeJson(outputPath, result);
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
