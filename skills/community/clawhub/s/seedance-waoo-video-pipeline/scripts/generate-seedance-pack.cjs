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

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
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
  if (String(stage['模型名']).toLowerCase().includes('placeholder')) throw new Error('Seedance upstream 模型名仍是 placeholder');
  if (String(stage['APIKey']).toLowerCase() === 'demo') throw new Error('Seedance upstream APIKey 仍是 demo');
}

function buildPrompt(topic, episode, clipCount, style, aspectRatio, revisionNote) {
  const revision = String(revisionNote || '').trim();
  return [
    '你是 Seedance 上游预制作引擎。',
    '任务：根据用户给定的单句题材，直接产出用于短视频生产的标准化 story pack。',
    '必须输出严格 JSON，不要输出 markdown 代码块，不要输出额外解释。',
    '',
    '输出 JSON 结构：',
    '{',
    '  "title": "",',
    '  "intentBriefMarkdown": "# E01_前置思考\\n...",',
    '  "scriptMarkdown": "# E01_剧本\\n...",',
    '  "assetListMarkdown": "# E01_素材清单\\n...",',
    '  "storyboardMarkdown": "# E01_分镜\\n..."',
    '}',
    '',
    '硬性要求：',
    `1. 项目题材：${topic}`,
    `2. 集数：${episode}`,
    `3. 默认拆条数：${clipCount}`,
    `4. 风格：${style}`,
    `5. 画幅：${aspectRatio}`,
    '6. 必须先有 E01_前置思考，再有 E01_剧本、E01_素材清单、E01_分镜。',
    '7. 内容要具体、可拍、可继续生成，不要写空泛文学评论。',
    '8. 分镜至少给出与默认拆条数一致的 panel 条目。',
    '9. 主体语言使用中文。',
    '10. 不要引用现代元素。',
    '',
    '质量目标：',
    '- 剧本要有本集边界、核心冲突、人物意图与节奏推进。',
    '- 素材清单要包含人物、场景、道具、天气时间、连续性约束。',
    '- 分镜要包含 shot id / scene id / panel index / shot type / action / camera / continuity / subtitle / tail-frame handoff。',
    revision ? '' : '',
    revision ? '用户修改意见（必须严格吸收并落到四件套，不要忽略）：' : '',
    revision ? revision : '',
  ].join('\n');
}

async function callOpenAiCompatible(stage, prompt) {
  const url = `${trimSlash(stage['接口地址'])}/chat/completions`;
  const body = {
    model: stage['模型名'],
    temperature: 0.7,
    response_format: { type: 'json_object' },
    messages: [
      { role: 'system', content: '你是严格输出 JSON 的 Seedance 预制作模型。' },
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
  if (!res.ok) throw new Error(`Seedance upstream 调用失败: ${res.status} ${text}`);

  let data;
  try {
    data = JSON.parse(text);
  } catch (error) {
    throw new Error(`Seedance upstream 返回非 JSON: ${text.slice(0, 500)}`);
  }

  const content = data?.choices?.[0]?.message?.content;
  if (!content) throw new Error(`Seedance upstream 未返回 message.content: ${text.slice(0, 500)}`);

  let parsed;
  try {
    parsed = JSON.parse(content);
  } catch (error) {
    throw new Error(`Seedance upstream content 不是合法 JSON: ${String(content).slice(0, 500)}`);
  }

  return { parsed, raw: data };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const configPath = args.config || './config/pipeline.config.json';
  const topic = args.topic;
  const episode = args.episode || 'E01';
  const outDir = args['out-dir'];
  const resultJson = args['result-json'];
  const clipCount = Number(args['clip-count'] || '8');
  const style = args.style || '古装短剧写实风';
  const aspectRatio = args['aspect-ratio'] || '9:16';
  const revisionNote = String(args['revision-note'] || '').trim();

  if (!topic || !outDir) {
    throw new Error('用法: node generate-seedance-pack.cjs --config <json> --topic <题材> --episode E01 --out-dir <目录> [--result-json <json>] [--clip-count 8] [--style 古装短剧写实风] [--aspect-ratio 9:16]');
  }

  const { full: resolvedConfigPath, config } = readConfig(configPath);
  const stage = config?.upstream?.seedance;
  validateStage(stage);

  const vendor = canonicalVendor(stage['厂商']);
  if (vendor !== 'openai' && vendor !== 'openai-compatible') {
    throw new Error(`当前独立 Seedance 文本脚本暂只支持 OpenAI-compatible 上游，收到厂商: ${stage['厂商']}`);
  }

  const prompt = buildPrompt(topic, episode, clipCount, style, aspectRatio, revisionNote);
  const { parsed, raw } = await callOpenAiCompatible(stage, prompt);

  const title = parsed.title || topic;
  const baseDir = path.resolve(outDir);
  ensureDir(baseDir);

  const files = {
    intentBrief: path.join(baseDir, `${episode}_前置思考.md`),
    script: path.join(baseDir, `${episode}_剧本.md`),
    assets: path.join(baseDir, `${episode}_素材清单.md`),
    storyboard: path.join(baseDir, `${episode}_分镜.md`),
  };

  const mappings = [
    ['intentBriefMarkdown', files.intentBrief],
    ['scriptMarkdown', files.script],
    ['assetListMarkdown', files.assets],
    ['storyboardMarkdown', files.storyboard],
  ];

  for (const [key, filePath] of mappings) {
    const value = parsed[key];
    if (!value || typeof value !== 'string') {
      throw new Error(`Seedance upstream 输出缺少 ${key}`);
    }
    fs.writeFileSync(filePath, value.trim() + '\n', 'utf8');
  }

  const result = {
    ok: true,
    title,
    topic,
    episode,
    vendor: stage['厂商'],
    model: stage['模型名'],
    configPath: resolvedConfigPath,
    outputDir: baseDir,
    files,
    rawResponsePreview: {
      id: raw?.id || null,
      model: raw?.model || null,
      usage: raw?.usage || null,
    },
  };

  const resultText = JSON.stringify(result, null, 2);
  if (resultJson) {
    fs.writeFileSync(path.resolve(resultJson), resultText + '\n', 'utf8');
  }
  console.log(resultText);
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
