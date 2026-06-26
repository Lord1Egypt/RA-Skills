/**
 * Unified Diagnostics — merged PipelineTrace + MetricsCollector
 * Phase tracing, memory profiling, counters, JSON/JSONL output.
 * Local copy for qwen-orchestrator so it does not depend on ai-orchestrator.
 */

const fs = require('fs');
const os = require('os');

const PHASES = {
  INIT:             { id: 'init',             label: 'Инициализация',         color: '\x1b[36m' },
  BROWSER_LAUNCH:   { id: 'browser_launch',   label: 'Запуск браузера',       color: '\x1b[35m' },
  DAEMON_CONNECT:   { id: 'daemon_connect',   label: 'Подключение к демону',  color: '\x1b[34m' },
  SESSION_RESTORE:  { id: 'session_restore',  label: 'Восстановление сессии', color: '\x1b[33m' },
  PAGE_NAVIGATE:    { id: 'page_navigate',    label: 'Навигация',             color: '\x1b[35m' },
  AUTH_CHECK:       { id: 'auth_check',       label: 'Проверка авторизации',  color: '\x1b[31m' },
  COMPOSER_WAIT:    { id: 'composer_wait',    label: 'Ожидание composer',     color: '\x1b[34m' },
  PROMPT_SEND:      { id: 'prompt_send',      label: 'Отправка промпта',      color: '\x1b[32m' },
  ANSWER_WAIT:      { id: 'answer_wait',      label: 'Ожидание ответа',       color: '\x1b[36m' },
  ANSWER_EXTRACT:   { id: 'answer_extract',   label: 'Извлечение ответа',     color: '\x1b[32m' },
  CONTINUE:         { id: 'continue',         label: 'Продолжение',           color: '\x1b[33m' },
  DRY_RUN:          { id: 'dry_run',          label: 'Dry run',               color: '\x1b[33m' },
};

const RESET = '\x1b[0m';

class Diagnostics {
  constructor(opts = {}) {
    this.traceId = opts.traceId || `tr-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`;
    this.sessionName = opts.sessionName || null;
    this.promptPreview = (opts.promptPreview || '').substring(0, 80);
    this.phases = {};
    this.events = [];
    this.error = null;
    this.startTime = Date.now();
    this.memorySnapshots = [];
    this.retryCount = 0;
    this.extractionAttempts = 0;
    this.continueRounds = 0;
    this.charactersExtracted = 0;
    this.apiRequests = 0;
    this.answerComplete = false;
    this.incompleteReason = null;
    this.logDir = opts.logDir || null;
    if (this.logDir) {
      try { fs.mkdirSync(this.logDir, { recursive: true }); } catch (e) {}
    }
  }

  start(phaseId, meta) {
    const ph = PHASES[phaseId];
    if (!ph) return;
    this.phases[phaseId] = { phaseId, label: ph.label, status: 'running', start: Date.now(), end: null, duration_ms: null, metadata: meta || {} };
    this._emit(phaseId, 'started');
    console.log(`${ph.color}⏳ [${ph.label}]${RESET} Начат: ${ph.label}`);
  }

  succeed(phaseId, meta) {
    const rec = this.phases[phaseId];
    if (!rec) return;
    rec.status = 'succeeded';
    rec.end = Date.now();
    rec.duration_ms = rec.end - rec.start;
    if (meta) Object.assign(rec.metadata, meta);
    this._emit(phaseId, 'succeeded');
    const ph = PHASES[phaseId];
    const m = meta && Object.keys(meta).length > 0 ? ` ${JSON.stringify(meta)}` : '';
    console.log(`${ph.color}✅ [${ph.label}]${RESET} Завершён: ${ph.label} (${this._fmt(rec.duration_ms)})${m}`);
  }

  fail(phaseId, err, meta) {
    const rec = this.phases[phaseId];
    const ph = PHASES[phaseId];
    const msg = err instanceof Error ? err.message : String(err);
    if (rec) {
      rec.status = 'failed';
      rec.end = Date.now();
      rec.duration_ms = rec.end - rec.start;
      rec.error = msg;
      if (meta) Object.assign(rec.metadata, meta);
    }
    if (!this.error) this.error = { phaseId, phaseLabel: ph?.label, message: msg };
    console.log(`\x1b[31m❌ [${ph?.label}]${RESET} ОШИБКА [${ph?.label}]: ${msg}`);
  }

  skip(phaseId, reason) {
    const rec = this.phases[phaseId];
    const ph = PHASES[phaseId];
    if (rec) {
      rec.status = 'skipped';
      rec.end = Date.now();
      rec.duration_ms = rec.end - rec.start;
    }
    console.log(`\x1b[33m⏭ [${ph?.label}]${RESET} Пропущен: ${ph?.label}${reason ? ` (${reason})` : ''}`);
  }

  snapMemory(label) {
    const m = process.memoryUsage();
    this.memorySnapshots.push({ label: label || 'snap', rssMB: Math.round(m.rss / 1024 / 1024) });
  }

  phaseStart(name) {
    if (!this.phases[name]) {
      this.phases[name] = { phaseId: name, label: name, status: 'running', start: Date.now(), end: null, duration_ms: null, metadata: {}, auxiliary: true };
    }
  }

  phaseEnd(name, meta) {
    const rec = this.phases[name];
    if (rec) {
      rec.end = Date.now();
      rec.duration_ms = rec.end - rec.start;
      rec.status = rec.status === 'running' ? 'succeeded' : rec.status;
      if (meta) Object.assign(rec.metadata, meta);
    }
  }

  increment(key, by) { this[key] = (this[key] || 0) + (by || 1); }

  _emit(phaseId, status) {
    const e = { traceId: this.traceId, timestamp: new Date().toISOString(), phaseId, status, duration_ms: this.phases[phaseId] ? Date.now() - this.phases[phaseId].start : null };
    this.events.push(e);
    if (this.logDir) {
      try { fs.appendFileSync(this.logDir + `/trace-${this.traceId}.jsonl`, JSON.stringify(e) + '\n'); } catch (e2) {}
    }
  }

  _fmt(ms) {
    if (ms < 1000) return ms + 'ms';
    if (ms < 60000) return (ms / 1000).toFixed(1) + 's';
    return Math.floor(ms / 60000) + 'm' + ((ms % 60000) / 1000).toFixed(0) + 's';
  }

  printSummary(answerLength) {
    const totalMs = Date.now() - this.startTime;
    const peakMB = this.memorySnapshots.length > 0 ? Math.max(...this.memorySnapshots.map(s => s.rssMB)) : null;
    console.log('\n📊 Метрики:');
    console.log('   ⏱  Общее время:    ' + Math.round(totalMs / 1000) + 's');
    if (peakMB) console.log('   💾 Пик памяти:    ' + peakMB + 'MB (Node)');
    console.log('   📝 Промпт:        ' + this.promptPreview.length + ' символов');
    console.log('   📦 Ответ:         ' + (answerLength || 0) + ' символов');
    console.log('   🔄 Продолжений:   ' + this.continueRounds);
    console.log('   🔁 Ретраев:       ' + this.retryCount);
    console.log('   📥 Попыток экстракта: ' + this.extractionAttempts);
    for (const [, p] of Object.entries(this.phases)) {
      if (p.auxiliary) continue;
      if (p.duration_ms != null) console.log('      ' + p.phaseId.padEnd(18) + ' ' + this._fmt(p.duration_ms));
    }
    console.log('   ✅ Статус ответа: ' + (this.answerComplete ? 'полный' : this.incompleteReason || 'не полный'));
  }

  save() {
    if (!this.logDir) return null;
    const data = {
      traceId: this.traceId,
      phases: this.phases,
      memory: { peakMB: this.memorySnapshots.length > 0 ? Math.max(...this.memorySnapshots.map(s => s.rssMB)) : null },
      counts: { retries: this.retryCount, continueRounds: this.continueRounds, apiRequests: this.apiRequests },
      answerLength: this.charactersExtracted,
      answerComplete: this.answerComplete,
      incompleteReason: this.incompleteReason,
      error: this.error,
      totalMs: Date.now() - this.startTime,
      platform: os.platform(),
      nodeVersion: process.version,
    };
    const file = this.logDir + '/metrics-' + this.traceId + '.json';
    try {
      fs.writeFileSync(file, JSON.stringify(data, null, 2));
      return file;
    } catch (e) {
      return null;
    }
  }

  summary() {
    const totalMs = Date.now() - this.startTime;
    console.log('\n' + '='.repeat(65));
    console.log('📊 TRACER REPORT [' + this.traceId + ']');
    console.log('═'.repeat(65));
    console.log('⏱  Общее время:     ' + this._fmt(totalMs));
    if (this.sessionName) console.log('Сессия: ' + this.sessionName);
    console.log('');
    for (const [id, rec] of Object.entries(this.phases)) {
      if (rec.auxiliary) continue;
      const icon = rec.status === 'succeeded' ? '✅' : rec.status === 'failed' ? '❌' : rec.status === 'skipped' ? '⏭' : '⏳';
      const c = rec.status === 'succeeded' ? '\x1b[32m' : rec.status === 'failed' ? '\x1b[31m' : '\x1b[33m';
      const ph = PHASES[id] || { label: id };
      console.log('  ' + icon + ' ' + ph.label.padEnd(22) + ' ' + c + this._fmt(rec.duration_ms || 0).padEnd(10) + RESET + ' ' + rec.status);
    }
    console.log('═'.repeat(65));
    return { traceId: this.traceId, totalMs, error: this.error, phases: this.phases };
  }

  finish() {}
}

module.exports = { Diagnostics, PHASES };
