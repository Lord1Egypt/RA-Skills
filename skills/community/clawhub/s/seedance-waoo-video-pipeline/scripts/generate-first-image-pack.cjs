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

function trimSlash(url) {
  return String(url || '').replace(/\/+$/, '');
}

function canonicalVendor(name) {
  const value = String(name || '').trim().toLowerCase();
  if (!value) return '';
  if (value.includes('openai-compatible') || value.includes('openai compatible') || value.includes('openai兼容')) return 'openai-compatible';
  if (value.includes('openai')) return 'openai';
  return value;
}

function ensureDirForFile(filePath) {
  fs.mkdirSync(path.dirname(path.resolve(filePath)), { recursive: true });
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(path.resolve(filePath), 'utf8'));
}

function readConfig(configPath) {
  const full = path.resolve(configPath);
  if (!fs.existsSync(full)) throw new Error(`配置文件不存在: ${full}`);
  const raw = fs.readFileSync(full, 'utf8').trim();
  if (!raw) throw new Error(`配置文件为空: ${full}`);
  return { full, config: JSON.parse(raw) };
}

function validateStage(stage) {
  const missing = [];
  if (!stage?.['厂商']) missing.push('厂商');
  if (!stage?.['接口地址']) missing.push('接口地址');
  if (!stage?.['模型名']) missing.push('模型名');
  if (!stage?.['APIKey']) missing.push('API Key');
  if (missing.length) throw new Error(`Seedance upstream 配置不完整: ${missing.join(' / ')}`);
}

function buildPrompt(bundle, panelIndex, revisionNote) {
  const revision = String(revisionNote || '').trim();
  return [
    '你是 Seedance 首图确认包生成器。',
    '任务：基于已经确认的四件套，为指定 panel 生成首图确认包。',
    '必须输出严格 JSON，不要 markdown 代码块，不要额外解释。',
    '',
    '输出 JSON 结构：',
    '{',
    '  "panelIndex": 1,',
    '  "panelTitle": "",',
    '  "briefMarkdown": "# P01_首图说明\\n...",',
    '  "promptText": "",',
    '  "negativePrompt": "",',
    '  "subtitleCandidate": "",',
    '  "confirmationQuestion": "请确认是否按这张首图方向继续生成。"',
    '}',
    '',
    `项目题材：${bundle.topic}`,
    `集数：${bundle.episode}`,
    `目标 panelIndex：${panelIndex}`,
    '',
    '以下是已确认四件套：',
    '【前置思考】',
    bundle.fullText.intentBrief,
    '【剧本】',
    bundle.fullText.script,
    '【素材清单】',
    bundle.fullText.assets,
    '【分镜】',
    bundle.fullText.storyboard,
    '',
    '要求：',
    '1. 只针对目标 panel 生成首图确认包。',
    '2. brief 要说明画面主体、人物站位、情绪、动作、机位、环境。',
    '3. promptText 要适合实际首图生成，中文为主，可混合必要英文风格词。',
    '4. negativePrompt 要明确避免串人、串景、现代元素、风格跑偏。',
    '5. subtitleCandidate 必须与目标 panel 语义一致。',
    '6. 结果要具体、可生成、可继续确认。',
    revision ? '' : '',
    revision ? '用户修改意见（必须严格吸收并落到首图确认包，不要忽略）：' : '',
    revision ? revision : '',
  ].join('\n');
}

async function callOpenAiCompatible(stage, prompt) {
  const url = `${trimSlash(stage['接口地址'])}/chat/completions`;
  const body = {
    model: stage['模型名'],
    temperature: 0.6,
    response_format: { type: 'json_object' },
    messages: [
      { role: 'system', content: '你是严格输出 JSON 的首图确认包生成模型。' },
      { role: 'user', content: prompt },
    ],
  };
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${stage['APIKey']}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`首图确认包生成失败: ${res.status} ${text}`);
  const data = JSON.parse(text);
  const content = data?.choices?.[0]?.message?.content;
  if (!content) throw new Error(`首图确认包返回缺少 message.content: ${text.slice(0, 500)}`);
  const parsed = JSON.parse(content);
  return { parsed, raw: data };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const configPath = args.config;
  const entryResultPath = args['entry-result'];
  const panelIndex = Number(args['panel-index'] || '1');
  const outDir = args['out-dir'];
  const resultJson = args['result-json'];
  const revisionNote = String(args['revision-note'] || '').trim();
  if (!configPath || !entryResultPath || !outDir) {
    throw new Error('用法: node generate-first-image-pack.cjs --config <json> --entry-result <json> --out-dir <目录> [--panel-index 1] [--result-json <json>]');
  }

  const { config } = readConfig(configPath);
  const stage = config?.upstream?.seedance;
  validateStage(stage);
  const vendor = canonicalVendor(stage['厂商']);
  if (vendor !== 'openai' && vendor !== 'openai-compatible') {
    throw new Error(`当前首图确认包脚本暂只支持 OpenAI-compatible 上游，收到厂商: ${stage['厂商']}`);
  }

  const entry = readJson(entryResultPath);
  const bundle = entry?.confirmationBundle;
  if (!bundle?.fullText?.storyboard) {
    throw new Error('entry.result.json 缺少已确认四件套内容，无法生成首图确认包');
  }

  const prompt = buildPrompt(bundle, panelIndex, revisionNote);
  const { parsed, raw } = await callOpenAiCompatible(stage, prompt);

  const baseDir = path.resolve(outDir);
  fs.mkdirSync(baseDir, { recursive: true });
  const prefix = `P${String(panelIndex).padStart(2, '0')}`;
  const files = {
    brief: path.join(baseDir, `${prefix}_首图说明.md`),
    prompt: path.join(baseDir, `${prefix}_首图prompt.txt`),
    json: path.join(baseDir, `${prefix}_首图确认包.json`),
  };

  fs.writeFileSync(files.brief, String(parsed.briefMarkdown || '').trim() + '\n', 'utf8');
  fs.writeFileSync(files.prompt, String(parsed.promptText || '').trim() + '\n', 'utf8');
  fs.writeFileSync(files.json, JSON.stringify(parsed, null, 2) + '\n', 'utf8');

  const result = {
    ok: true,
    panelIndex,
    panelTitle: parsed.panelTitle || '',
    files,
    briefMarkdown: parsed.briefMarkdown || '',
    promptText: parsed.promptText || '',
    negativePrompt: parsed.negativePrompt || '',
    subtitleCandidate: parsed.subtitleCandidate || '',
    confirmationQuestion: parsed.confirmationQuestion || '请确认是否按这张首图方向继续生成。',
    rawResponsePreview: {
      id: raw?.id || null,
      model: raw?.model || null,
      usage: raw?.usage || null,
    },
  };

  if (resultJson) {
    ensureDirForFile(resultJson);
    fs.writeFileSync(path.resolve(resultJson), JSON.stringify(result, null, 2) + '\n', 'utf8');
  }
  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
