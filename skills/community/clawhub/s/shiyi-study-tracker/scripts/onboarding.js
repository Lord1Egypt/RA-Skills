/**
 * onboarding.js
 * 首次加载：问一次考试类型，存入 config.json，之后不再打扰。
 */

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const { resolveExam, listSupportedExams } = require('../assets/exam_prompts');

const CONFIG_PATH = path.join(os.homedir(), '.openclaw/skills/shiyi/config.json');

function loadConfig() {
  try { return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8')); }
  catch (_) { return {}; }
}

function saveConfig(cfg) {
  const dir = path.dirname(CONFIG_PATH);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(cfg, null, 2), 'utf-8');
}

function isSetupDone() { return !!loadConfig().setup_done; }
function getExamKey()  { return loadConfig().exam_key || '_generic'; }
function getExamName() { return loadConfig().exam_name || ''; }

// ─── 消息模板 ─────────────────────────────────────────────────

function buildWelcome() {
  const supported = listSupportedExams();
  return `拾遗已安装。

你在备考什么考试？发名字过来就行，比如：
  ${supported.slice(0, 6).join('、')}……
  或者高数期末、驾照理论、某省特岗——不在列表里也没关系。

告诉我考试名称，我来配置识别逻辑。`;
}

// ─── 主处理函数 ───────────────────────────────────────────────

async function handleOnboarding(userMessage, sendMessage) {
  if (isSetupDone()) return false;

  const text = (userMessage || '').trim();
  const cfg  = loadConfig();

  // 第一次加载，还没发过欢迎消息
  if (!text || !cfg._waiting_exam) {
    await sendMessage(buildWelcome());
    saveConfig({ _waiting_exam: true });
    return true;
  }

  // 用户发来考试名称
  const { key, prompt } = resolveExam(text);
  const isGeneric = key === '_generic';

  saveConfig({
    setup_done: true,
    exam_key:   key,
    exam_name:  text,
  });

  const msg = isGeneric
    ? `好，用「${text}」作为考试名称，按通用模式识别截图。\n\n直接发错题截图就行，或者发文字描述也可以。`
    : `好，已配置「${key}」的识别逻辑。\n\n直接发错题截图就行，或者发文字描述也可以。\n\n如果之后换考试，发「换考试」即可重新配置。`;

  await sendMessage(msg);
  return true;
}

/**
 * 处理"换考试"指令。
 */
async function handleChangeExam(sendMessage) {
  saveConfig({ _waiting_exam: true });
  await sendMessage(buildWelcome());
}

async function initOnboarding(sendMessage) {
  if (isSetupDone()) return;
  await sendMessage(buildWelcome());
  saveConfig({ _waiting_exam: true });
}

module.exports = { initOnboarding, handleOnboarding, isSetupDone, getExamKey, getExamName, handleChangeExam };
