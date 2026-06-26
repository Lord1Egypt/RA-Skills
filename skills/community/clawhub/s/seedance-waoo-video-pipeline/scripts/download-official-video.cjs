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

async function fetchBinaryToFile(url, outputPath) {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`下载失败: HTTP ${res.status} ${res.statusText}`);
  }
  const arr = new Uint8Array(await res.arrayBuffer());
  ensureDirForFile(outputPath);
  fs.writeFileSync(path.resolve(outputPath), arr);
  return {
    outputPath: path.resolve(outputPath),
    bytes: arr.byteLength,
  };
}

async function downloadMinimaxVideo(baseUrl, apiKey, taskId, fileId, outputPath, isProbe) {
  if (!fileId) throw new Error('缺少 fileId');

  if (isProbe) {
    ensureDirForFile(outputPath);
    fs.writeFileSync(path.resolve(outputPath), Buffer.from('probe-video'));
    return {
      taskId,
      fileId,
      status: 'success',
      downloadUrl: 'probe://minimax',
      outputFile: path.resolve(outputPath),
      bytes: 10,
      isProbe: true,
      原始响应: { probe: true },
    };
  }

  const url = `${trimSlash(baseUrl)}/files/retrieve?file_id=${encodeURIComponent(fileId)}`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${apiKey}` },
  });
  const data = await res.json();
  const downloadUrl = String(data?.file?.download_url || data?.download_url || '');
  if (!res.ok || data?.base_resp?.status_code !== 0 || !downloadUrl) {
    throw new Error(`MiniMax 文件获取失败: ${JSON.stringify(data)}`);
  }
  const saved = await fetchBinaryToFile(downloadUrl, outputPath);
  return {
    taskId,
    fileId,
    status: 'success',
    downloadUrl,
    outputFile: saved.outputPath,
    bytes: saved.bytes,
    isProbe,
    原始响应: data,
  };
}

async function downloadViduVideo(taskId, fileId, outputPath, isProbe) {
  const direct = String(fileId || '').startsWith('url:') ? String(fileId || '').slice(4) : String(fileId || '');
  if (!direct) {
    throw new Error('Vidu 下载缺少可用 URL（预期 fileId=url:...）。');
  }

  if (isProbe) {
    ensureDirForFile(outputPath);
    fs.writeFileSync(path.resolve(outputPath), Buffer.from('probe-video'));
    return {
      taskId,
      fileId,
      status: 'success',
      downloadUrl: direct,
      outputFile: path.resolve(outputPath),
      bytes: 10,
      isProbe: true,
      原始响应: { probe: true },
    };
  }

  const saved = await fetchBinaryToFile(direct, outputPath);
  return {
    taskId,
    fileId,
    status: 'success',
    downloadUrl: direct,
    outputFile: saved.outputPath,
    bytes: saved.bytes,
    isProbe,
    原始响应: { provider: 'vidu', directDownload: true },
  };
}

async function downloadSeedanceVideo(taskId, fileId, outputPath, isProbe) {
  const direct = String(fileId || '').startsWith('url:') ? String(fileId || '').slice(4) : String(fileId || '');
  if (!direct) {
    throw new Error('Seedance 下载缺少可用 URL（预期 fileId=url:...）。');
  }

  if (isProbe) {
    ensureDirForFile(outputPath);
    fs.writeFileSync(path.resolve(outputPath), Buffer.from('probe-video'));
    return {
      taskId,
      fileId,
      status: 'success',
      downloadUrl: direct,
      outputFile: path.resolve(outputPath),
      bytes: 10,
      isProbe: true,
      原始响应: { probe: true },
    };
  }

  const saved = await fetchBinaryToFile(direct, outputPath);
  return {
    taskId,
    fileId,
    status: 'success',
    downloadUrl: direct,
    outputFile: saved.outputPath,
    bytes: saved.bytes,
    isProbe,
    原始响应: { provider: 'seedance', directDownload: true },
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const configPath = args.config;
  const taskId = args['task-id'];
  const fileId = args['file-id'];
  const outputPath = args.out;
  const resultJsonPath = args['result-json'];
  const isProbe = args.probe === true;

  if (!configPath || !taskId || !fileId || !outputPath) {
    throw new Error('用法: node download-official-video.cjs --config <json> --task-id <id> --file-id <fileId> --out <mp4路径> [--result-json <json>] [--probe]');
  }

  const config = readJson(configPath);
  const stage = config?.downstream?.waoo?.video;
  if (!stage?.厂商 || !stage?.接口地址 || !stage?.模型名 || !stage?.APIKey) {
    throw new Error('视频配置不完整，请先补齐 厂商 / 接口地址 / 模型名 / API Key');
  }

  const vendor = canonicalVendor(stage.厂商);
  let result = null;

  if (vendor === 'minimax') {
    result = await downloadMinimaxVideo(stage.接口地址, stage.APIKey, taskId, fileId, outputPath, isProbe);
  } else if (vendor === 'vidu') {
    result = await downloadViduVideo(taskId, fileId, outputPath, isProbe);
  } else if (vendor === 'seedance') {
    result = await downloadSeedanceVideo(taskId, fileId, outputPath, isProbe);
  } else {
    throw new Error(`暂不支持的官方视频厂商: ${stage.厂商}`);
  }

  writeJson(resultJsonPath, result);
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
