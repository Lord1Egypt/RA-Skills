/**
 * 英语助教 · 配置文件
 *
 * 全部模块选填设计：
 *   - 填了环境变量 → 启用对应模块
 *   - 没填 → 静默跳过，不报错
 *   - 无任何硬编码默认值 (避免误以为"已配置")
 *
 * 生产环境：cron job 的 env 字段注入
 * 本地开发：.env 文件（不提交到仓库）
 */

const path = require('path');
const fs = require('fs');

// ===== 加载 .env（仅用于本地开发，生产靠 cron env 注入）=====
const envPath = path.join(__dirname, '.env');
if (fs.existsSync(envPath)) {
  fs.readFileSync(envPath, 'utf8').split('\n').forEach(line => {
    const t = line.trim();
    if (!t || t.startsWith('#')) return;
    const ei = t.indexOf('=');
    if (ei < 0) return;
    const k = t.slice(0, ei).trim();
    const rawV = t.slice(ei + 1).trim();
    // Strip surrounding quotes (supports KEY="value with = inside")
    const v = ((rawV.startsWith('"') && rawV.endsWith('"')) || (rawV.startsWith("'") && rawV.endsWith("'")))
      ? rawV.slice(1, -1) : rawV;
    if (k && !process.env[k]) process.env[k] = v;
  });
}

// ===== 配置项（全部选填，无硬编码默认值）=====

module.exports = {
  // ===== MiniMax（全部选填）=====
  // 有 MINIMAX_API_KEY → Token Plan 用户，推荐 speech-2.8-hd；无 Key 则静默跳过
  MINIMAX_API_KEY:  process.env.MINIMAX_API_KEY  || null,
  MINIMAX_GROUP_ID: process.env.MINIMAX_GROUP_ID || '',
  // TTS 优先云端（需 API Key），无 Key 时静默跳过，由 Piper 本地兜底
  TTS_MODEL:        process.env.MINIMAX_TTS_MODEL     || null,   // 有 Key 时推荐 speech-2.8-hd
  TTS_SPEED:        parseFloat(process.env.MINIMAX_TTS_SPEED || '1.05'),
  TTS_ACCENT:      process.env.MINIMAX_TTS_ACCENT    || 'English',
  TTS_VOICE_ID:    process.env.MINIMAX_TTS_VOICE_ID  || null,   // 有 Key 时推荐 male-qn-qingse

  // ===== Piper 本地 TTS（无云端 Key 时的兜底方案）=====
  // 均不填 → 跳过本地 TTS
  PIPER_BIN:   process.env.PIPER_BIN   || null,
  PIPER_MODEL: process.env.PIPER_MODEL || null,

  // ===== 飞书（全部选填）=====
  // 有完整飞书配置 → 启用飞书语音推送；不填 → 静默跳过
  FEISHU_APP_ID:       process.env.FEISHU_APP_ID       || null,
  FEISHU_APP_SECRET:   process.env.FEISHU_APP_SECRET   || null,
  FEISHU_USER_OPEN_ID: process.env.FEISHU_USER_OPEN_ID || null,
  FEISHU_WEBHOOK:      process.env.FEISHU_WEBHOOK      || '',

  // ===== 本地 ASR（可选）=====
  SENSE_VOICE_MODEL_DIR: process.env.SENSE_VOICE_MODEL_DIR || null,

  // ===== 多维表格（全部选填，不填则无记忆功能）=====
  BITABLE_APP_TOKEN:      process.env.BITABLE_APP_TOKEN      || null,
  BITABLE_WORDS_TABLE_ID: process.env.BITABLE_WORDS_TABLE_ID || null,
  BITABLE_CHAT_TABLE_ID:  process.env.BITABLE_CHAT_TABLE_ID  || null,

  // ===== 艾宾浩斯复习 =====
  EBINGHAUS:    [1, 3, 7, 15],
  DAILY_WORD_MAX: parseInt(process.env.DAILY_WORD_MAX || '15'),
};