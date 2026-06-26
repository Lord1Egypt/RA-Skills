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

function trimSlash(url) {
  return String(url || '').replace(/\/+$/, '');
}

function canonicalVendor(name) {
  const value = String(name || '').trim().toLowerCase();
  if (!value) return '';
  if (value.includes('minimax') || value.includes('mini max')) return 'minimax';
  if (value.includes('openai-compatible') || value.includes('openai compatible') || value.includes('openai兼容')) return 'openai-compatible';
  if (value.includes('openai')) return 'openai';
  return value;
}

function looksPlaceholder(value) {
  const text = String(value || '').trim().toLowerCase();
  return !text || text === 'demo' || text.includes('placeholder') || text === 'your_api_key';
}

function readConfig(configPath) {
  const full = path.resolve(configPath);
  if (!fs.existsSync(full)) throw new Error(`配置文件不存在: ${full}`);
  const raw = fs.readFileSync(full, 'utf8').trim();
  if (!raw) throw new Error(`配置文件为空: ${full}`);
  return { full, config: JSON.parse(raw) };
}

function buildImagePrompt(firstImage) {
  const parts = [String(firstImage.promptText || '').trim()];
  if (String(firstImage.negativePrompt || '').trim()) {
    parts.push(`Avoid: ${String(firstImage.negativePrompt).trim()}`);
  }
  return parts.filter(Boolean).join('\n\n');
}

async function downloadUrlToFile(url, outputPath) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`下载首图失败: ${res.status} ${await res.text()}`);
  const arrayBuffer = await res.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);
  ensureDirForFile(outputPath);
  fs.writeFileSync(path.resolve(outputPath), buffer);
  return { outputPath: path.resolve(outputPath), bytes: buffer.length };
}

async function generateOpenAiCompatibleImage(stage, prompt, size) {
  const endpoint = `${trimSlash(stage['接口地址'])}/images/generations`;
  const body = {
    model: stage['模型名'],
    prompt,
    size,
    response_format: 'b64_json',
  };

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${stage['APIKey']}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  const text = await res.text();
  if (!res.ok) throw new Error(`首图生成失败: ${res.status} ${text}`);
  return JSON.parse(text);
}

async function generateMiniMaxImage(stage, prompt, aspectRatio) {
  const endpoint = `${trimSlash(stage['接口地址'])}/image_generation`;
  const body = {
    model: stage['模型名'],
    prompt,
    aspect_ratio: aspectRatio,
    response_format: 'base64',
  };

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${stage['APIKey']}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  const text = await res.text();
  if (!res.ok) throw new Error(`首图生成失败: ${res.status} ${text}`);
  return JSON.parse(text);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const configPath = args.config;
  const firstImageResultPath = args['first-image-result'];
  const outputPath = args['result-json'];
  const outDir = args['out-dir'];
  const size = args.size || '1536x1024';
  const aspectRatio = args['aspect-ratio'] || '16:9';

  if (!configPath || !firstImageResultPath || !outDir) {
    throw new Error('用法: node generate-first-image-asset.cjs --config <json> --first-image-result <json> --out-dir <dir> [--size 1536x1024] [--result-json <json>]');
  }

  const { config, full } = readConfig(configPath);
  const stage = config?.downstream?.waoo?.image;
  if (!stage?.厂商 || !stage?.接口地址 || !stage?.模型名 || looksPlaceholder(stage?.APIKey)) {
    throw new Error(`首图图片配置不完整: ${full}`);
  }

  const vendor = canonicalVendor(stage['厂商']);
  if (vendor !== 'openai' && vendor !== 'openai-compatible' && vendor !== 'minimax') {
    throw new Error(`当前首图图片脚本暂只支持 MiniMax 或 OpenAI-compatible 厂商，收到: ${stage['厂商']}`);
  }

  const firstImage = readJson(firstImageResultPath);
  const prompt = buildImagePrompt(firstImage);
  const raw = vendor === 'minimax'
    ? await generateMiniMaxImage(stage, prompt, aspectRatio)
    : await generateOpenAiCompatibleImage(stage, prompt, size);
  const item = vendor === 'minimax'
    ? { b64_json: raw?.data?.image_base64?.[0] || '', url: '' }
    : raw?.data?.[0];
  if (!item || (!item.b64_json && !item.url)) throw new Error(`首图图片返回缺少可用图片数据: ${JSON.stringify(raw).slice(0, 500)}`);

  const baseDir = path.resolve(outDir);
  fs.mkdirSync(baseDir, { recursive: true });
  const prefix = `P${String(firstImage.panelIndex || 1).padStart(2, '0')}`;
  const imagePath = path.join(baseDir, `${prefix}_首图.png`);

  let imageUrl = '';
  if (item.b64_json) {
    ensureDirForFile(imagePath);
    fs.writeFileSync(imagePath, Buffer.from(String(item.b64_json), 'base64'));
  } else if (item.url) {
    imageUrl = String(item.url);
    await downloadUrlToFile(imageUrl, imagePath);
  } else {
    throw new Error(`首图图片返回既没有 b64_json，也没有 url: ${JSON.stringify(item).slice(0, 500)}`);
  }

  const result = {
    ok: true,
    panelIndex: Number(firstImage.panelIndex || 1),
    panelTitle: String(firstImage.panelTitle || ''),
    imageFile: path.resolve(imagePath),
    imageUrl,
    caption: `【Panel ${firstImage.panelIndex}${firstImage.panelTitle ? `｜${firstImage.panelTitle}` : ''}】正式首图已生成，请确认这张图是否通过。`,
    stateLabel: 'image-approved-candidate',
    promptText: String(firstImage.promptText || ''),
    negativePrompt: String(firstImage.negativePrompt || ''),
    subtitleCandidate: String(firstImage.subtitleCandidate || ''),
    rawResponsePreview: {
      created: raw?.created || null,
      model: stage['模型名'],
      vendor: stage['厂商'],
    },
  };

  writeJson(outputPath, result);
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
