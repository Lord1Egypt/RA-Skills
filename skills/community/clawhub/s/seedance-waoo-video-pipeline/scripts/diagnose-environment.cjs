const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

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

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(path.resolve(filePath), 'utf8'));
}

function writeJson(outputPath, data) {
  const text = JSON.stringify(data, null, 2);
  if (outputPath) {
    fs.mkdirSync(path.dirname(path.resolve(outputPath)), { recursive: true });
    fs.writeFileSync(path.resolve(outputPath), text + '\n', 'utf8');
  }
  console.log(text);
}

function commandExists(command) {
  const checker = process.platform === 'win32' ? 'where' : 'which';
  const res = spawnSync(checker, [command], { stdio: 'ignore' });
  return res.status === 0;
}

function isPlaceholder(value) {
  const text = String(value || '').trim().toLowerCase();
  if (!text) return true;
  return text.includes('your-') || text.includes('placeholder') || text === 'demo';
}

function getPipelineMode(config) {
  const mode = String(config?.runtime?.pipelineMode || 'minimax_full').trim().toLowerCase();
  return mode || 'minimax_full';
}

function canonicalVendor(name) {
  const value = String(name || '').trim().toLowerCase();
  if (!value) return '';
  if (value.includes('minimax') || value.includes('mini max')) return 'minimax';
  if (value.includes('vidu')) return 'vidu';
  if (value.includes('seedance') || value.includes('doubao') || value.includes('ark') || value.includes('volc')) return 'seedance';
  return value;
}

function checkModelBlock(block, label, findings) {
  if (!block) {
    findings.push({ level: 'error', item: label, message: '配置块缺失' });
    return;
  }
  const required = ['厂商', '接口地址', '模型名', 'APIKey'];
  for (const key of required) {
    const val = block[key];
    if (!val || (key === 'APIKey' && isPlaceholder(val))) {
      findings.push({ level: key === 'APIKey' ? 'warn' : 'error', item: `${label}.${key}`, message: key === 'APIKey' ? '疑似占位符/未填' : '缺失' });
    }
  }
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const configPath = path.resolve(args.config || './config/pipeline.config.json');
  const outputPath = args.out ? path.resolve(args.out) : '';

  const findings = [];
  if (!fs.existsSync(configPath)) {
    findings.push({ level: 'error', item: 'config', message: `配置文件不存在: ${configPath}` });
    writeJson(outputPath, {
      ok: false,
      configPath,
      pipelineMode: 'minimax_full',
      findings,
      tools: {
        ffmpegInPath: commandExists('ffmpeg'),
        ffprobeInPath: commandExists('ffprobe'),
        tsxInPath: commandExists('tsx'),
        npxInPath: commandExists('npx'),
      },
    });
    process.exit(2);
  }

  const config = readJson(configPath);
  const mode = getPipelineMode(config);

  if (['vidu_simple', 'seedance_simple'].includes(mode)) {
    checkModelBlock(config?.downstream?.waoo?.video, 'downstream.waoo.video', findings);
    const vendor = canonicalVendor(config?.downstream?.waoo?.video?.厂商);
    if (vendor && !['minimax', 'vidu', 'seedance'].includes(vendor)) {
      findings.push({ level: 'error', item: 'downstream.waoo.video.厂商', message: `vidu_simple 当前仅支持 minimax/vidu/seedance，收到: ${config?.downstream?.waoo?.video?.厂商}` });
    }
  } else {
    checkModelBlock(config?.upstream?.seedance, 'upstream.seedance', findings);
    checkModelBlock(config?.downstream?.waoo?.image, 'downstream.waoo.image', findings);
    checkModelBlock(config?.downstream?.waoo?.video, 'downstream.waoo.video', findings);
    checkModelBlock(config?.downstream?.waoo?.tts, 'downstream.waoo.tts', findings);
  }

  const ffmpegInPath = commandExists('ffmpeg');
  const ffprobeInPath = commandExists('ffprobe');
  const tsxInPath = commandExists('tsx');
  const npxInPath = commandExists('npx');
  const runtimeFfmpeg = String(config?.runtime?.ffmpeg || '').trim();
  const runtimeFfprobe = String(config?.runtime?.ffprobe || '').trim();

  if (!ffmpegInPath && !runtimeFfmpeg) {
    findings.push({ level: 'warn', item: 'runtime.ffmpeg', message: '系统 PATH 未找到 ffmpeg，且 config.runtime.ffmpeg 为空' });
  }
  if (!ffprobeInPath && !runtimeFfprobe) {
    findings.push({ level: 'warn', item: 'runtime.ffprobe', message: '系统 PATH 未找到 ffprobe，且 config.runtime.ffprobe 为空' });
  }
  if (!tsxInPath && !npxInPath) {
    findings.push({ level: 'warn', item: 'tsx', message: '系统未发现 tsx 且 npx 不可用，TS 脚本可能无法执行。' });
  }

  const hasError = findings.some((f) => f.level === 'error');
  writeJson(outputPath, {
    ok: !hasError,
    configPath,
    pipelineMode: mode,
    findings,
    tools: {
      ffmpegInPath,
      ffprobeInPath,
      tsxInPath,
      npxInPath,
    },
    nextStep: hasError
      ? '先补齐 error 项，再执行正式流水线。'
      : '可进入正式流程；若有 warn，按提示补齐以提升稳定性。',
  });

  if (hasError) {
    process.exit(1);
  }
}

try {
  main();
} catch (error) {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
}
