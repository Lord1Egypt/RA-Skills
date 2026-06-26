const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function commandExists(cmd) {
  const checker = process.platform === 'win32' ? 'where' : 'which';
  const result = spawnSync(checker, [cmd], { encoding: 'utf8', shell: false });
  return result.status === 0 && result.stdout && result.stdout.trim();
}

function resolvePython() {
  const preferred = String(process.env.RAPIDOCR_PYTHON || '').trim();
  if (preferred) {
    if (preferred.includes(path.sep)) {
      if (fs.existsSync(preferred)) return preferred;
    } else if (commandExists(preferred)) {
      return preferred;
    }
  }
  const candidates = process.platform === 'win32' ? ['python', 'py'] : ['python3', 'python'];
  for (const name of candidates) {
    const found = commandExists(name);
    if (found) return name;
  }
  return null;
}

function cleanToken(s) {
  return String(s || '').trim().replace(/^['"]+|['"]+$/g, '');
}

function isImagePathCandidate(s) {
  return /\.(png|jpg|jpeg|webp|bmp|tif|tiff)$/i.test(cleanToken(s));
}

function tryExistingPath(s) {
  const v = cleanToken(s);
  if (!v || !isImagePathCandidate(v) || !fs.existsSync(v)) return null;
  return v;
}

function extractWindowsPaths(text) {
  const s = String(text || '');
  return s.match(/[A-Za-z]:\\[^\r\n"'<>|?*]+?\.(?:png|jpg|jpeg|webp|bmp|tif|tiff)/gi) || [];
}

function extractPosixPaths(text) {
  const s = String(text || '');
  return s.match(/\/(?:[^\s"'<>|?*]+\/)*[^\s"'<>|?*]+\.(?:png|jpg|jpeg|webp|bmp|tif|tiff)/gi) || [];
}

function parseOptions(text) {
  const s = String(text || '');
  return {
    json: /(^|\s)--json(\s|$)|\bjson输出\b|\b返回json\b|\bjson格式\b|\b结构化\b/i.test(s),
  };
}

function extractImagePathFromText(text) {
  if (!text) return null;
  if (typeof text !== 'string') {
    try {
      text = JSON.stringify(text);
    } catch {
      text = String(text);
    }
  }

  try {
    const obj = JSON.parse(text);
    if (obj && typeof obj === 'object') {
      const candidates = [obj.img_path, obj.image_path, obj.path, obj.file, obj.file_path, obj.image];
      for (const candidate of candidates) {
        const p = tryExistingPath(candidate);
        if (p) return p;
      }
      if (obj.args && typeof obj.args === 'object') {
        const nested = [obj.args.img_path, obj.args.image_path, obj.args.path, obj.args.file, obj.args.file_path, obj.args.image];
        for (const candidate of nested) {
          const p = tryExistingPath(candidate);
          if (p) return p;
        }
      }
    }
  } catch {}

  const explicitPatterns = [
    /img_path\s*[=:]\s*([^\r\n]+)/i,
    /image_path\s*[=:]\s*([^\r\n]+)/i,
    /file_path\s*[=:]\s*([^\r\n]+)/i,
    /图片路径[是为：:]\s*([^\r\n]+)/i,
  ];

  for (const re of explicitPatterns) {
    const m = text.match(re);
    if (!m || !m[1]) continue;
    const segment = cleanToken(m[1]);
    const direct = tryExistingPath(segment);
    if (direct) return direct;
    for (const candidate of [...extractWindowsPaths(segment), ...extractPosixPaths(segment)]) {
      const p = tryExistingPath(candidate);
      if (p) return p;
    }
  }

  for (const candidate of [...extractWindowsPaths(text), ...extractPosixPaths(text)]) {
    const p = tryExistingPath(candidate);
    if (p) return p;
  }

  const tokens = text.split(/\s+/).map(cleanToken).filter(Boolean);
  for (const token of tokens) {
    const p = tryExistingPath(token);
    if (p) return p;
  }

  return null;
}

function resolveInput(argv) {
  const positional = (argv || []).slice(2);
  const rawText = positional.join(' ');
  const envCandidates = [
    process.env.SKILL_ARGS,
    process.env.SKILL_INPUT,
    process.env.SKILL_USER_PROMPT,
    process.env.INPUT,
    process.env.USER_PROMPT,
    process.env.ARGS,
    process.env.ARGUMENTS,
    process.env.PROMPT,
  ].filter(Boolean);

  let source = null;

  for (const arg of positional) {
    const direct = tryExistingPath(arg);
    if (direct) {
      source = direct;
      break;
    }
  }

  if (!source) {
    for (const arg of positional) {
      if (arg === '<用户原话>' || arg === '{input}' || arg === '{{input}}' || arg === '{user_prompt}' || arg === '{{user_prompt}}') {
        continue;
      }
      const found = extractImagePathFromText(arg);
      if (found) {
        source = found;
        break;
      }
    }
  }

  if (!source) {
    for (const text of envCandidates) {
      const found = extractImagePathFromText(text);
      if (found) {
        source = found;
        break;
      }
    }
  }

  return { source, options: parseOptions(rawText || envCandidates.join(' ')) };
}

function main() {
  const { source, options } = resolveInput(process.argv);
  if (!source) {
    console.error('Missing local image path.');
    process.exit(2);
  }

  const python = resolvePython();
  if (!python) {
    console.error('Python executable not found.');
    process.exit(127);
  }

  const scriptPath = path.join(__dirname, 'run_rapidocr.py');
  const args = python === 'py'
    ? ['-3', scriptPath, source]
    : [scriptPath, source];

  if (options.json) {
    args.push('--json');
  }

  const result = spawnSync(python, args, {
    encoding: 'utf8',
    shell: false,
    env: {
      ...process.env,
      PYTHONWARNINGS: 'ignore',
      LOG_LEVEL: 'CRITICAL',
      RAPIDOCR_LOG_LEVEL: 'CRITICAL',
    },
  });

  if (result.stdout) process.stdout.write(result.stdout);
  if ((result.status ?? 1) !== 0) {
    const stderr = String(result.stderr || '').trim();
    console.error(stderr || 'RapidOCR execution failed.');
    process.exit(result.status ?? 1);
  }
}

main();
