const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { execFile } = require('node:child_process');
const formidable = require('formidable');

const SKILL_DIR = __dirname;
const CONFIG_PATH = path.join(SKILL_DIR, 'config.json');
const DEFAULT_CONFIG = {
  port: 9002,
  flaskTtsUrl: 'http://127.0.0.1:5002/api/tts/synthesize',
  flaskHealthUrl: 'http://127.0.0.1:5002/api/health',
  cloneModel: 'qwen3_tts_0.6b_base_openvino',
  cloneMode: 'voice_clone_xvector',
  customModel: 'qwen3_tts_0.6b_custom_openvino',
  defaultSpeaker: 'Vivian',
  defaultLanguage: 'Chinese',
  minReferenceDurationSec: 3,
  maxReferenceDurationSec: 5,
  maxCloneOutputSeconds: 20,
  maxCustomOutputSeconds: 30,
  estimatedCharsPerSecond: 4,
  fileRetentionDays: 7,
  outputDir: './outputs',
  referencesDir: './references',
  runtimeDir: './runtime',
  sessionStateFile: './runtime/session_state.json',
  openclawSession: 'default',
};

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    return normalizeConfig({});
  }
  try {
    const raw = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    return normalizeConfig(raw || {});
  } catch (error) {
    console.warn('[xeontts] failed to parse config.json, using defaults:', error.message);
    return normalizeConfig({});
  }
}

function normalizeConfig(input) {
  const config = { ...DEFAULT_CONFIG, ...(input || {}) };
  const retentionDays = Number(config.fileRetentionDays);
  config.fileRetentionDays = Number.isFinite(retentionDays) && retentionDays >= 0 ? retentionDays : DEFAULT_CONFIG.fileRetentionDays;
  config.outputDir = resolveLocalPath(config.outputDir);
  config.referencesDir = resolveLocalPath(config.referencesDir);
  config.runtimeDir = resolveLocalPath(config.runtimeDir);
  config.sessionStateFile = resolveLocalPath(config.sessionStateFile);
  return config;
}

function resolveLocalPath(value) {
  if (!value) {
    return value;
  }
  if (value.startsWith('~/')) {
    return path.join(os.homedir(), value.slice(2));
  }
  if (path.isAbsolute(value)) {
    return value;
  }
  return path.join(SKILL_DIR, value);
}

const config = loadConfig();
ensureRuntimeDirs();
cleanupManagedFiles();

function ensureRuntimeDirs() {
  for (const dirPath of [config.outputDir, config.referencesDir, config.runtimeDir, path.dirname(config.sessionStateFile)]) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
  if (!fs.existsSync(config.sessionStateFile)) {
    fs.writeFileSync(config.sessionStateFile, '{}\n');
  }
}

function getRetentionNotice() {
  if (Number(config.fileRetentionDays) <= 0) {
    return '文件保留期未启用自动清理。';
  }
  return `参考音频和生成结果默认只保留 ${config.fileRetentionDays} 天，之后会自动清理。`;
}

function removeEmptyDirsRecursively(dirPath, stopDir) {
  if (!dirPath || dirPath === stopDir) {
    return;
  }
  try {
    const entries = fs.readdirSync(dirPath);
    if (entries.length > 0) {
      return;
    }
    fs.rmdirSync(dirPath);
    removeEmptyDirsRecursively(path.dirname(dirPath), stopDir);
  } catch {
    // ignore cleanup errors
  }
}

function cleanupExpiredFiles(rootDir) {
  if (Number(config.fileRetentionDays) <= 0) {
    return 0;
  }
  const cutoffMs = Date.now() - Number(config.fileRetentionDays) * 24 * 60 * 60 * 1000;
  let removedCount = 0;

  function walk(currentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath);
        removeEmptyDirsRecursively(fullPath, rootDir);
        continue;
      }
      try {
        const stat = fs.statSync(fullPath);
        if (stat.mtimeMs < cutoffMs) {
          fs.rmSync(fullPath, { force: true });
          removedCount += 1;
        }
      } catch {
        // ignore cleanup errors
      }
    }
  }

  if (fs.existsSync(rootDir)) {
    walk(rootDir);
  }
  return removedCount;
}

function cleanupManagedFiles() {
  const removedReferences = cleanupExpiredFiles(config.referencesDir);
  const removedOutputs = cleanupExpiredFiles(config.outputDir);
  if (removedReferences > 0 || removedOutputs > 0) {
    console.log(`[xeontts] auto-cleaned expired files: references=${removedReferences}, outputs=${removedOutputs}, retentionDays=${config.fileRetentionDays}`);
  }
}

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(config.sessionStateFile, 'utf8')) || {};
  } catch {
    return {};
  }
}

function saveState(state) {
  fs.writeFileSync(config.sessionStateFile, `${JSON.stringify(state, null, 2)}\n`);
}

function firstValue(value) {
  if (Array.isArray(value)) {
    return value[0];
  }
  return value;
}

function buildSessionKey(sessionId, userId) {
  return `${String(sessionId || config.openclawSession || 'default').trim()}::${String(userId || 'anonymous').trim()}`;
}

function getSessionState(sessionId, userId) {
  const state = loadState();
  const key = buildSessionKey(sessionId, userId);
  if (!state[key]) {
    state[key] = {
      stage: 'idle',
      sessionId: sessionId || config.openclawSession || 'default',
      userId: userId || 'anonymous',
      referenceAudioPath: null,
      referenceDurationSec: null,
      lastOutputPath: null,
      updatedAt: new Date().toISOString(),
    };
  }
  return { state, key, session: state[key] };
}

function writeSessionState(sessionId, userId, updater) {
  const current = getSessionState(sessionId, userId);
  updater(current.session);
  current.session.updatedAt = new Date().toISOString();
  saveState(current.state);
  return current.session;
}

function listPendingReferenceSessions(state) {
  return Object.entries(state || {})
    .filter(([, session]) => session?.stage === 'awaiting_reference_audio')
    .map(([key, session]) => ({ key, session }));
}

function resolvePendingReferenceSession(sessionId, userId) {
  const state = loadState();
  const pending = listPendingReferenceSessions(state);
  const normalizedSessionId = String(sessionId || '').trim();
  const normalizedUserId = String(userId || '').trim();

  if (normalizedSessionId && normalizedUserId) {
    const exactKey = buildSessionKey(normalizedSessionId, normalizedUserId);
    const exact = pending.find((item) => item.key === exactKey);
    if (exact) {
      return { matched: true, sessionId: exact.session.sessionId, userId: exact.session.userId, state, key: exact.key, session: exact.session, reason: 'exact_match' };
    }
  }

  if (normalizedSessionId) {
    const sameSession = pending.filter((item) => item.session.sessionId === normalizedSessionId);
    if (sameSession.length === 1) {
      const match = sameSession[0];
      return { matched: true, sessionId: match.session.sessionId, userId: match.session.userId, state, key: match.key, session: match.session, reason: 'session_match' };
    }
    if (sameSession.length > 1) {
      return { matched: false, state, reason: 'ambiguous_session_match', pendingCount: sameSession.length };
    }
  }

  if (normalizedUserId) {
    const sameUser = pending.filter((item) => item.session.userId === normalizedUserId);
    if (sameUser.length === 1) {
      const match = sameUser[0];
      return { matched: true, sessionId: match.session.sessionId, userId: match.session.userId, state, key: match.key, session: match.session, reason: 'user_match' };
    }
    if (sameUser.length > 1) {
      return { matched: false, state, reason: 'ambiguous_user_match', pendingCount: sameUser.length };
    }
  }

  if (pending.length === 1) {
    const match = pending[0];
    return { matched: true, sessionId: match.session.sessionId, userId: match.session.userId, state, key: match.key, session: match.session, reason: 'single_pending_session' };
  }

  if (pending.length > 1) {
    return { matched: false, state, reason: 'ambiguous_pending_sessions', pendingCount: pending.length };
  }

  return { matched: false, state, reason: 'no_pending_clone_session', pendingCount: 0 };
}

function persistReferenceAudioForSession(sessionId, userId, sourcePath, originalFilename, durationSec) {
  const sessionKey = buildSessionKey(sessionId, userId).replace(/[^a-zA-Z0-9_-]+/g, '_');
  const fallbackExt = path.extname(sourcePath || '.wav') || '.wav';
  const targetPath = path.join(config.referencesDir, `${sessionKey}${path.extname(originalFilename || '') || fallbackExt}`);
  fs.mkdirSync(path.dirname(targetPath), { recursive: true });
  fs.copyFileSync(sourcePath, targetPath);
  writeSessionState(sessionId, userId, (session) => {
    session.stage = 'awaiting_clone_text';
    session.referenceAudioPath = targetPath;
    session.referenceDurationSec = durationSec;
  });
  cleanupManagedFiles();
  return targetPath;
}

function sendJson(res, statusCode, payload) {
  res.writeHead(statusCode, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(payload));
}

function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('end', () => {
      try {
        const text = Buffer.concat(chunks).toString('utf8');
        resolve(text ? JSON.parse(text) : {});
      } catch (error) {
        reject(error);
      }
    });
    req.on('error', reject);
  });
}

function detectIntent(text, session) {
  const normalized = String(text || '').trim();
  if (!normalized) {
    return 'unknown';
  }
  const lower = normalized.toLowerCase();
  if (/(asr|转写|识别语音|语音转文字|speech[- ]?to[- ]?text|transcribe)/i.test(normalized)) {
    return 'ignore_asr';
  }
  if (/(克隆音色|克隆声音|复制我的声音|voice clone|clone voice)/i.test(normalized)) {
    return 'clone_start';
  }
  if (session?.stage === 'awaiting_clone_text') {
    return 'clone_text';
  }
  if (/(生成语音|朗读|播报|tts|text to speech|语气|风格|声音说)/i.test(normalized)) {
    return 'custom_speak';
  }
  if (/^用.+(语气|风格).+(说|朗读|播报)/.test(normalized)) {
    return 'custom_speak';
  }
  return 'unknown';
}

function parseStyleAndContent(text) {
  const normalized = String(text || '').trim();
  const styleMatch = normalized.match(/用(.{1,12}?)(?:的)?(?:语气|风格|声音)/);
  const style = styleMatch ? styleMatch[1].trim() : '普通';

  const contentPatterns = [
    /(?:说|朗读|播报|念出|生成)(?:一段话|这段话|下面这段话|以下内容)?[:：]?\s*(.+)$/,
    /(?:请|帮我)?(?:用.{0,12}?(?:语气|风格|声音))[:：]?\s*(.+)$/,
    /(?:生成语音|生成音频)[:：]?\s*(.+)$/,
  ];

  for (const pattern of contentPatterns) {
    const match = normalized.match(pattern);
    if (match && match[1]) {
      return { style, content: match[1].trim() };
    }
  }

  return { style, content: normalized };
}

function extractRequestedDurationSeconds(text) {
  const normalized = String(text || '').trim();
  const minuteMatch = normalized.match(/(\d+(?:\.\d+)?)\s*(分钟|分)/);
  if (minuteMatch) {
    return Number(minuteMatch[1]) * 60;
  }
  const secondMatch = normalized.match(/(\d+(?:\.\d+)?)\s*秒/);
  if (secondMatch) {
    return Number(secondMatch[1]);
  }
  return null;
}

function estimateOutputDurationSeconds(text) {
  const chars = Array.from(String(text || '').replace(/\s+/g, '')).length;
  if (!chars) {
    return 0;
  }
  return chars / Number(config.estimatedCharsPerSecond || 4);
}

function validateRequestedOutput(text, maxSeconds, label) {
  const requested = extractRequestedDurationSeconds(text);
  if (requested && requested > maxSeconds) {
    throw new Error(`${label}请求时长超过上限，当前最大支持约 ${maxSeconds} 秒`);
  }
  const estimated = estimateOutputDurationSeconds(text);
  if (estimated > maxSeconds) {
    throw new Error(`${label}内容预计时长约 ${estimated.toFixed(1)} 秒，超过当前上限 ${maxSeconds} 秒，请拆分后重试`);
  }
  return { requestedSeconds: requested, estimatedSeconds: estimated };
}

function getMimeType(filePath, contentType) {
  if (contentType && String(contentType).startsWith('audio/')) {
    return contentType;
  }
  const ext = path.extname(filePath).toLowerCase();
  switch (ext) {
    case '.wav':
      return 'audio/wav';
    case '.mp3':
      return 'audio/mpeg';
    case '.m4a':
      return 'audio/mp4';
    case '.ogg':
    case '.opus':
      return 'audio/ogg';
    default:
      return 'application/octet-stream';
  }
}

function readWavDurationSec(filePath) {
  const stat = fs.statSync(filePath);
  const fd = fs.openSync(filePath, 'r');
  try {
    const riffHeader = Buffer.alloc(12);
    fs.readSync(fd, riffHeader, 0, 12, 0);
    if (riffHeader.toString('ascii', 0, 4) !== 'RIFF' || riffHeader.toString('ascii', 8, 12) !== 'WAVE') {
      return null;
    }

    let offset = 12;
    let sampleRate = null;
    let channels = null;
    let bitsPerSample = null;
    let dataSize = null;

    while (offset + 8 <= stat.size) {
      const chunkHeader = Buffer.alloc(8);
      const bytesRead = fs.readSync(fd, chunkHeader, 0, 8, offset);
      if (bytesRead < 8) {
        break;
      }

      const chunkId = chunkHeader.toString('ascii', 0, 4);
      const chunkSize = chunkHeader.readUInt32LE(4);
      const chunkDataOffset = offset + 8;

      if (chunkId === 'fmt ') {
        const fmtBuffer = Buffer.alloc(Math.min(chunkSize, 32));
        fs.readSync(fd, fmtBuffer, 0, fmtBuffer.length, chunkDataOffset);
        channels = fmtBuffer.readUInt16LE(2);
        sampleRate = fmtBuffer.readUInt32LE(4);
        bitsPerSample = fmtBuffer.readUInt16LE(14);
      } else if (chunkId === 'data') {
        dataSize = chunkSize;
      }

      if (sampleRate && channels && bitsPerSample && dataSize) {
        break;
      }
      offset = chunkDataOffset + chunkSize + (chunkSize % 2);
    }

    if (!sampleRate || !channels || !bitsPerSample || !dataSize) {
      return null;
    }

    const bytesPerSecond = sampleRate * channels * (bitsPerSample / 8);
    if (!bytesPerSecond) {
      return null;
    }
    return dataSize / bytesPerSecond;
  } finally {
    fs.closeSync(fd);
  }
}

function getAudioDurationSec(filePath) {
  return new Promise((resolve, reject) => {
    execFile(
      'ffprobe',
      ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filePath],
      (error, stdout) => {
        if (error) {
          const wavDuration = readWavDurationSec(filePath);
          if (wavDuration && Number.isFinite(wavDuration) && wavDuration > 0) {
            console.warn('[xeontts] ffprobe 不可用，已回退为 WAV 头时长解析');
            resolve(wavDuration);
            return;
          }
          reject(new Error('未找到 ffprobe，且无法通过 WAV 头解析音频时长，请先安装可用的 ffmpeg/ffprobe'));
          return;
        }
        const duration = Number(String(stdout || '').trim());
        if (!Number.isFinite(duration) || duration <= 0) {
          const wavDuration = readWavDurationSec(filePath);
          if (wavDuration && Number.isFinite(wavDuration) && wavDuration > 0) {
            console.warn('[xeontts] ffprobe 输出无效，已回退为 WAV 头时长解析');
            resolve(wavDuration);
            return;
          }
          reject(new Error('无法读取参考音频时长，请上传常见音频格式'));
          return;
        }
        resolve(duration);
      },
    );
  });
}

function uniqueOutputPath(prefix) {
  const date = new Date().toISOString().slice(0, 10);
  const dirPath = path.join(config.outputDir, date);
  fs.mkdirSync(dirPath, { recursive: true });
  return path.join(dirPath, `${prefix}_${Date.now()}.wav`);
}

async function callFlaskTtsJson(payload) {
  const url = new URL(config.flaskTtsUrl);
  url.searchParams.set('response_format', 'json');
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok || data.success === false) {
    throw new Error(data.error || `TTS 服务请求失败 (${response.status})`);
  }
  return data;
}

async function synthesizeCustomVoice(options) {
  const text = String(options.text || '').trim();
  if (!text) {
    throw new Error('缺少要生成的文本');
  }
  const timing = validateRequestedOutput(text, Number(config.maxCustomOutputSeconds || 30), '自定义音色');
  const style = String(options.style || '普通').trim() || '普通';
  const payload = {
    text,
    model: config.customModel,
    tts_model: config.customModel,
    tts_mode: 'custom_voice',
    language: options.language || config.defaultLanguage,
    speaker_id: options.speakerId || config.defaultSpeaker,
    instruct_text: style === '普通' ? '' : `请用${style}的语气朗读这段话。`,
  };
  const result = await callFlaskTtsJson(payload);
  const outputPath = uniqueOutputPath('custom');
  fs.writeFileSync(outputPath, Buffer.from(result.audio_base64, 'base64'));
  cleanupManagedFiles();
  return {
    mode: 'custom_voice',
    outputPath,
    sampleRate: result.sample_rate,
    estimatedSeconds: timing.estimatedSeconds,
    style,
  };
}

async function synthesizeClonedVoice(options) {
  const text = String(options.text || '').trim();
  if (!text) {
    throw new Error('缺少要生成的文本');
  }
  if (!options.referenceAudioPath || !fs.existsSync(options.referenceAudioPath)) {
    throw new Error('当前会话没有可用的参考音频，请先上传 3 到 5 秒参考音频');
  }
  const timing = validateRequestedOutput(text, Number(config.maxCloneOutputSeconds || 20), '音色克隆');
  const form = new FormData();
  form.append('text', text);
  form.append('model', config.cloneModel);
  form.append('tts_model', config.cloneModel);
  form.append('tts_mode', config.cloneMode);
  form.append('language', options.language || config.defaultLanguage);
  form.append('x_vector_only_mode', String(config.cloneMode === 'voice_clone_xvector'));

  const audioBuffer = fs.readFileSync(options.referenceAudioPath);
  form.append('prompt_audio', new Blob([audioBuffer], { type: getMimeType(options.referenceAudioPath) }), path.basename(options.referenceAudioPath));

  if (config.cloneMode !== 'voice_clone_xvector' && options.referenceText) {
    form.append('ref_text', options.referenceText);
  }

  const url = new URL(config.flaskTtsUrl);
  url.searchParams.set('response_format', 'json');
  const response = await fetch(url, { method: 'POST', body: form });
  const data = await response.json().catch(() => ({}));
  if (!response.ok || data.success === false) {
    throw new Error(data.error || `音色克隆请求失败 (${response.status})`);
  }

  const outputPath = uniqueOutputPath('clone');
  fs.writeFileSync(outputPath, Buffer.from(data.audio_base64, 'base64'));
  cleanupManagedFiles();
  return {
    mode: 'voice_clone',
    outputPath,
    sampleRate: data.sample_rate,
    estimatedSeconds: timing.estimatedSeconds,
  };
}

function parseMultipart(req) {
  const form = new formidable.IncomingForm({
    uploadDir: config.runtimeDir,
    keepExtensions: true,
    multiples: false,
  });
  return new Promise((resolve, reject) => {
    form.parse(req, (error, fields, files) => {
      if (error) {
        reject(error);
        return;
      }
      resolve({ fields, files });
    });
  });
}

function getUploadedFile(files) {
  const candidate = files.file || files.audio || files.prompt_audio || null;
  if (Array.isArray(candidate)) {
    return candidate[0] || null;
  }
  return candidate;
}

async function handleWorkflowMessage(body) {
  const sessionId = body.sessionId || config.openclawSession;
  const userId = body.userId || 'anonymous';
  const text = String(body.text || '').trim();
  const snapshot = getSessionState(sessionId, userId);
  const intent = detectIntent(text, snapshot.session);

  if (intent === 'ignore_asr') {
    return {
      success: true,
      action: 'ignore',
      reason: 'detected_asr_request',
      message: '当前请求是语音识别/转写意图，应交给 xeon_asr，不走 xeon_tts。',
    };
  }

  if (intent === 'clone_start') {
    writeSessionState(sessionId, userId, (session) => {
      session.stage = 'awaiting_reference_audio';
      session.referenceAudioPath = null;
      session.referenceDurationSec = null;
    });
    return {
      success: true,
      action: 'ask_reference_audio',
      message: `请上传一段 ${config.minReferenceDurationSec} 到 ${config.maxReferenceDurationSec} 秒的干净人声参考音频，我会用 Base 模型为你克隆音色。${getRetentionNotice()}`,
    };
  }

  if (snapshot.session.stage === 'awaiting_reference_audio') {
    return {
      success: true,
      action: 'waiting_reference_audio',
      message: `当前正在进行音色克隆，请先上传一段 ${config.minReferenceDurationSec} 到 ${config.maxReferenceDurationSec} 秒参考音频。`,
    };
  }

  if (intent === 'clone_text') {
    const result = await synthesizeClonedVoice({
      text,
      referenceAudioPath: snapshot.session.referenceAudioPath,
      language: body.language || config.defaultLanguage,
      referenceText: body.referenceText || '',
    });
    writeSessionState(sessionId, userId, (session) => {
      session.stage = 'idle';
      session.lastOutputPath = result.outputPath;
    });
    return {
      success: true,
      action: 'synthesized_clone_voice',
      message: `音色克隆完成，音频已落盘: ${result.outputPath}。${getRetentionNotice()}`,
      outputPath: result.outputPath,
      estimatedSeconds: result.estimatedSeconds,
    };
  }

  if (intent === 'custom_speak') {
    const parsed = parseStyleAndContent(text);
    const result = await synthesizeCustomVoice({
      text: body.content || parsed.content,
      style: body.style || parsed.style,
      language: body.language || config.defaultLanguage,
      speakerId: body.speakerId || config.defaultSpeaker,
    });
    writeSessionState(sessionId, userId, (session) => {
      session.stage = 'idle';
      session.lastOutputPath = result.outputPath;
    });
    return {
      success: true,
      action: 'synthesized_custom_voice',
      message: `语音生成完成，音频已落盘: ${result.outputPath}。${getRetentionNotice()}`,
      outputPath: result.outputPath,
      style: result.style,
      estimatedSeconds: result.estimatedSeconds,
    };
  }

  return {
    success: true,
    action: 'noop',
    message: '未识别到 TTS/音色克隆意图。若你要克隆音色，请明确说“我要克隆音色”；若要生成语音，请明确说“用某种语气朗读这段话”。',
  };
}

const server = http.createServer(async (req, res) => {
  try {
    if (req.method === 'GET' && req.url === '/health') {
      return sendJson(res, 200, { status: 'ok', port: config.port });
    }

    if (req.method === 'GET' && req.url.startsWith('/api/session/state')) {
      const url = new URL(req.url, 'http://127.0.0.1');
      const sessionId = url.searchParams.get('sessionId') || config.openclawSession;
      const userId = url.searchParams.get('userId') || 'anonymous';
      const current = getSessionState(sessionId, userId).session;
      return sendJson(res, 200, { success: true, session: current });
    }

    if (req.method === 'POST' && req.url === '/api/workflow/message') {
      const body = await readJsonBody(req);
      const result = await handleWorkflowMessage(body || {});
      return sendJson(res, 200, result);
    }

    if (req.method === 'POST' && req.url === '/api/workflow/reference-audio') {
      const parsed = await parseMultipart(req);
      const file = getUploadedFile(parsed.files);
      const sessionId = firstValue(parsed.fields.sessionId) || config.openclawSession;
      const userId = firstValue(parsed.fields.userId) || 'anonymous';
      if (!file?.filepath) {
        return sendJson(res, 400, { success: false, error: 'missing audio file' });
      }
      const durationSec = await getAudioDurationSec(file.filepath);
      if (durationSec < Number(config.minReferenceDurationSec || 3) || durationSec > Number(config.maxReferenceDurationSec || 5)) {
        fs.rmSync(file.filepath, { force: true });
        return sendJson(res, 400, {
          success: false,
          error: `参考音频时长为 ${durationSec.toFixed(2)} 秒，不在 ${config.minReferenceDurationSec} 到 ${config.maxReferenceDurationSec} 秒范围内`,
        });
      }
      const targetPath = persistReferenceAudioForSession(sessionId, userId, file.filepath, file.originalFilename || file.filepath, durationSec);
      fs.rmSync(file.filepath, { force: true });
      return sendJson(res, 200, {
        success: true,
        action: 'reference_audio_saved',
        durationSec,
        referenceAudioPath: targetPath,
        message: `参考音频已接收，请继续发送你希望用该音色朗读的文本。${getRetentionNotice()}`,
      });
    }

    if (req.method === 'POST' && req.url === '/api/workflow/asr-audio-intake') {
      const parsed = await parseMultipart(req);
      const file = getUploadedFile(parsed.files);
      if (!file?.filepath) {
        return sendJson(res, 400, { success: false, consumed: false, error: 'missing audio file' });
      }

      const sessionId = firstValue(parsed.fields.sessionId) || req.headers['x-openclaw-session'] || req.headers['x-session-id'] || config.openclawSession;
      const userId = firstValue(parsed.fields.userId) || firstValue(parsed.fields.senderId) || req.headers['x-user-id'] || req.headers['x-sender-id'] || '';
      const matched = resolvePendingReferenceSession(sessionId, userId);
      if (!matched.matched) {
        fs.rmSync(file.filepath, { force: true });
        return sendJson(res, 200, {
          success: true,
          consumed: false,
          reason: matched.reason,
          pendingCount: matched.pendingCount || 0,
          message: '当前没有等待参考音频的音色克隆会话。',
        });
      }

      const durationSec = await getAudioDurationSec(file.filepath);
      if (durationSec < Number(config.minReferenceDurationSec || 3) || durationSec > Number(config.maxReferenceDurationSec || 5)) {
        fs.rmSync(file.filepath, { force: true });
        return sendJson(res, 200, {
          success: true,
          consumed: true,
          accepted: false,
          sessionId: matched.sessionId,
          userId: matched.userId,
          reason: 'invalid_reference_duration',
          durationSec,
          message: `参考音频时长为 ${durationSec.toFixed(2)} 秒，不在 ${config.minReferenceDurationSec} 到 ${config.maxReferenceDurationSec} 秒范围内，请重新上传。${getRetentionNotice()}`,
          transcriptText: `【TTS参考音频未接收】参考音频时长为 ${durationSec.toFixed(2)} 秒，不在 ${config.minReferenceDurationSec} 到 ${config.maxReferenceDurationSec} 秒范围内，请提醒用户重新上传 3 到 5 秒的干净人声。`,
        });
      }

      const targetPath = persistReferenceAudioForSession(
        matched.sessionId,
        matched.userId,
        file.filepath,
        file.originalFilename || file.filepath,
        durationSec,
      );
      fs.rmSync(file.filepath, { force: true });
      return sendJson(res, 200, {
        success: true,
        consumed: true,
        accepted: true,
        action: 'reference_audio_saved_via_asr',
        reason: matched.reason,
        sessionId: matched.sessionId,
        userId: matched.userId,
        durationSec,
        referenceAudioPath: targetPath,
        message: `参考音频已接收，请继续发送你希望用该音色朗读的文本。${getRetentionNotice()}`,
        transcriptText: '【TTS参考音频已接收】当前音色克隆会话的参考音频已经保存，请直接让用户继续发送要合成的文本，不要再要求重复上传，也不要说文件已被 ASR 清理。',
      });
    }

    if (req.method === 'POST' && req.url === '/api/tts/custom-speak') {
      const body = await readJsonBody(req);
      const result = await synthesizeCustomVoice({
        text: body.text,
        style: body.style || '普通',
        language: body.language || config.defaultLanguage,
        speakerId: body.speakerId || config.defaultSpeaker,
      });
      return sendJson(res, 200, { success: true, ...result });
    }

    if (req.method === 'POST' && req.url === '/api/tts/clone-speak') {
      const body = await readJsonBody(req);
      const result = await synthesizeClonedVoice({
        text: body.text,
        referenceAudioPath: body.referenceAudioPath,
        language: body.language || config.defaultLanguage,
        referenceText: body.referenceText || '',
      });
      return sendJson(res, 200, { success: true, ...result });
    }

    return sendJson(res, 404, { success: false, error: 'not found' });
  } catch (error) {
    console.error('[xeontts] request failed:', error);
    return sendJson(res, 500, { success: false, error: error.message || String(error) });
  }
});

server.listen(config.port, '0.0.0.0', async () => {
  let ttsHealth = 'unknown';
  try {
    const response = await fetch(config.flaskHealthUrl);
    ttsHealth = response.ok ? 'ok' : `http_${response.status}`;
  } catch (error) {
    ttsHealth = `unreachable: ${error.message}`;
  }
  console.log(`[xeontts] workflow gateway listening on http://0.0.0.0:${config.port}`);
  console.log(`[xeontts] upstream tts health: ${ttsHealth}`);
});
