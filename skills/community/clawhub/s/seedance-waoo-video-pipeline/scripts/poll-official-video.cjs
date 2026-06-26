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

function mapMinimaxStatus(value) {
  const status = String(value || '').toLowerCase();
  if (status === 'success') return 'success';
  if (status === 'fail' || status === 'failed') return 'fail';
  if (status === 'preparing' || status === 'queue' || status === 'queued') return 'queued';
  return 'processing';
}

function mapViduStatus(value) {
  const status = String(value || '').trim().toLowerCase();
  if (status === 'completed') return 'success';
  if (status === 'failed') return 'fail';
  if (status === 'queued') return 'queued';
  return 'processing';
}

async function pollMinimaxVideo(baseUrl, apiKey, taskId, isProbe) {
  if (isProbe) {
    return {
      taskId,
      status: 'success',
      fileId: 'probe-file-id',
      downloadUrl: '',
      progress: 100,
      isProbe: true,
      原始响应: { probe: true },
    };
  }

  const url = `${trimSlash(baseUrl)}/query/video_generation?task_id=${encodeURIComponent(taskId)}`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${apiKey}` },
  });
  const data = await res.json();
  if (!res.ok || data?.base_resp?.status_code !== 0) {
    throw new Error(`MiniMax 视频查询失败: ${JSON.stringify(data)}`);
  }
  return {
    taskId,
    status: mapMinimaxStatus(data?.status),
    fileId: String(data?.file_id || ''),
    downloadUrl: '',
    progress: typeof data?.progress === 'number' ? data.progress : null,
    isProbe,
    原始响应: data,
  };
}

async function pollViduVideo(baseUrl, apiKey, taskId, isProbe) {
  if (isProbe) {
    return {
      taskId,
      status: 'success',
      fileId: 'url:https://example.com/probe.mp4',
      downloadUrl: 'https://example.com/probe.mp4',
      progress: 100,
      isProbe: true,
      原始响应: { probe: true },
    };
  }

  const url = `${resolveV1Base(baseUrl)}/videos/generations/${encodeURIComponent(taskId)}`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${apiKey}` },
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(`Vidu 视频查询失败: ${JSON.stringify(data)}`);
  }

  let status = mapViduStatus(data?.status);
  const firstResult = Array.isArray(data?.result?.data) ? data.result.data[0] : null;
  const downloadUrl = String(firstResult?.url || data?.url || '');
  if (status === 'success' && !downloadUrl) {
    status = 'processing';
  }

  return {
    taskId: String(data?.id || taskId),
    status,
    fileId: downloadUrl ? `url:${downloadUrl}` : '',
    downloadUrl,
    progress: typeof data?.progress === 'number' ? data.progress : null,
    isProbe,
    原始响应: data,
  };
}

async function pollSeedanceVideo(baseUrl, apiKey, taskId, isProbe) {
  if (isProbe) {
    return {
      taskId,
      status: 'success',
      fileId: 'url:https://example.com/probe.mp4',
      downloadUrl: 'https://example.com/probe.mp4',
      progress: 100,
      isProbe: true,
      原始响应: { probe: true },
    };
  }

  const base = trimSlash(baseUrl);
  const url = /\/api\/v3\/contents\/generations\/tasks$/i.test(base)
    ? `${base}/${encodeURIComponent(taskId)}`
    : `${base}/api/v3/contents/generations/tasks/${encodeURIComponent(taskId)}`;

  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${apiKey}` },
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(`Seedance 视频查询失败: ${JSON.stringify(data)}`);
  }

  const rawStatus = String(data?.status || '').toLowerCase();
  const status = rawStatus === 'succeeded' ? 'success' : rawStatus === 'failed' ? 'fail' : 'processing';
  const downloadUrl = String(data?.content?.video_url || '');

  return {
    taskId: String(data?.id || taskId),
    status,
    fileId: downloadUrl ? `url:${downloadUrl}` : '',
    downloadUrl,
    progress: null,
    isProbe,
    原始响应: data,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const configPath = args.config;
  const taskId = args['task-id'];
  const outputPath = args.out;
  const isProbe = args.probe === true;

  if (!configPath || !taskId) {
    throw new Error('用法: node poll-official-video.cjs --config <json> --task-id <id> [--probe] [--out <json>]');
  }

  const config = readJson(configPath);
  const stage = config?.downstream?.waoo?.video;
  if (!stage?.厂商 || !stage?.接口地址 || !stage?.模型名 || !stage?.APIKey) {
    throw new Error('视频配置不完整，请先补齐 厂商 / 接口地址 / 模型名 / API Key');
  }

  const vendor = canonicalVendor(stage.厂商);
  let result = null;

  if (vendor === 'minimax') {
    result = await pollMinimaxVideo(stage.接口地址, stage.APIKey, taskId, isProbe);
  } else if (vendor === 'vidu') {
    result = await pollViduVideo(stage.接口地址, stage.APIKey, taskId, isProbe);
  } else if (vendor === 'seedance') {
    result = await pollSeedanceVideo(stage.接口地址, stage.APIKey, taskId, isProbe);
  } else {
    throw new Error(`暂不支持的官方视频厂商: ${stage.厂商}`);
  }

  writeJson(outputPath, result);
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
