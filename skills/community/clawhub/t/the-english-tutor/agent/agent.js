/**
 * 英语助教 · 主 Agent
 *
 * 设计原则：
 *   - 本文件只做文本生成和业务逻辑，无任何 subprocess / exec / spawn 调用
 *   - 所有需要外部进程的操作（TTS/ASR/飞书语音发送）由调用方通过 OpenClaw
 *     工具层执行，或通过 scripts/ 目录下的独立 Python 脚本处理
 *   - 这确保 ClawScan 扫描本文件时不包含任何危险 exec 模式
 *
 * 节点流程: n01 消息解析 → n02 ASR → n03 合并 → n04 单词筛选
 *          → n05 LLM对话 → n06 文本返回（语音由调用方通过 OpenClaw 工具处理）
 */

const config = require('./config');
const { MinimaxTTS, MiniMaxAPI } = require('./minimax');
const BitableMemory = require('./memory');

const TTS = new MinimaxTTS(config);
const memory = new BitableMemory(config);

// ===== n01 · 飞书消息解析 =====
// 注：本文件不处理 ASR（由 scripts/transcribe.py 或调用方处理）
function parseFeishuMessage(event) {
  const { msg_type, content, voice_url, user_id, chat_id } = event;
  return {
    user_id,
    chat_id,
    msg_type: msg_type || 'text',
    raw_content: content,
    voice_url: voice_url || null,
    is_voice: msg_type === 'audio' || msg_type === 'voice',
  };
}

// ===== n02 · ASR 说明 =====
// 语音转文字由 scripts/transcribe.py（纯 Python）或调用方处理。
// 本文件收到的 unifiedInput 应已是转写后的文字（由调用方注入）。
async function asrVoice(voice_url) {
  if (!voice_url) return '';
  // 注意：本函数不实际执行 ASR。调用方需要在调用 run() 之前
  // 先用 scripts/transcribe.py 或其他 ASR 工具将语音转为文字，
  // 然后将文字作为 userInput 参数传入。
  console.warn('[ASR] 请先通过 scripts/transcribe.py 或调用方 ASR 工具转写语音');
  return '';
}

// ===== n03 · 用户输入统一合并 =====
function mergeInput(parsedMsg, asrResult) {
  if (parsedMsg.is_voice) {
    return asrResult || parsedMsg.raw_content || '';
  }
  return parsedMsg.raw_content || '';
}

// ===== n04 · 单词库管理 + 艾宾浩斯筛选 =====
async function getWordPool(user_id, timePeriod) {
  const today = new Date();
  const records = await memory.getReviewRecords(user_id);

  const overdue = records.filter(r => {
    const next = new Date(r.next_review);
    return today >= next;
  });

  const newWords = await memory.getTodayNewWords(user_id, config.DAILY_WORD_MAX);

  const reviewWords = overdue.map(r => r.word);
  const pool = [...newWords, ...reviewWords].slice(0, config.DAILY_WORD_MAX);

  return {
    pool,
    new_count: newWords.length,
    review_count: reviewWords.length,
    time_period: timePeriod,
  };
}

// ===== n05 · LLM 美式场景对话 =====
async function llmChat(userInput, wordPool, timePeriod, chatHistory) {
  const systemPrompt = buildSystemPrompt(wordPool, timePeriod);
  const api = new MiniMaxAPI(config);

  const messages = [
    ...chatHistory.slice(-10),
    { role: 'user', content: userInput },
  ];

  const result = await api.chat(systemPrompt, messages);
  return result;
}

function buildSystemPrompt(wordPool, timePeriod) {
  const scenes = {
    'morning': '通勤场景（早晨出门、上班路上）',
    'noon': '午休场景（餐厅、咖啡厅）',
    'evening': '居家/购物场景（下班后）',
  };
  const scene = scenes[timePeriod] || '日常生活场景';
  const words = wordPool.length > 0 ? wordPool.join('、') : '（无特定单词，进入自由对话）';

  return `你是美式口语陪练，全程使用自然美式短句，结合给定单词融入${scene}。

【当前词汇池】${words}

要求：
1. 对话简洁口语化，适合口语跟读
2. 重点单词自然穿插进对话，不刻意解释
3. 主动提问引导用户开口说英文
4. 用户用英文或中文回复都可适配纠正
5. 复习阶段循环旧单词强化记忆
6. 回复长度控制在50字以内（一条消息适合朗读）
7. 如需发音提示用(pron: xxx)标注`;
}

// ===== n06 · TTS 说明 =====
// 语音合成由调用方通过 OpenClaw tts 工具处理，
// 或通过 scripts/feishu_voice.py（纯 Python）处理。
// 本文件返回文本和 TTS 指令，由调用方决定如何合成语音。

async function ttsVoice(text) {
  // 返回 { text } 表示需要调用方合成语音
  // 如配置了 MiniMax API Key，尝试返回可用的音频 URL
  try {
    const result = await TTS.synthesize(text);
    return { text, voiceUrl: result.url, exhausted: false };
  } catch (e) {
    if (e.message === 'TOKEN_EXHAUSTED') {
      return { text, voiceUrl: '', exhausted: true };
    }
    if (e.message === 'MINIMAX_API_KEY_NOT_CONFIGURED') {
      return { text, voiceUrl: '', exhausted: false, noTts: true };
    }
    throw e;
  }
}

// ===== n07 · 飞书推送文本生成 =====
async function feishuPush(aiText, voiceData, timePeriod) {
  const periodLabel = {
    'morning': '🌅 晨间',
    'noon': '☀️ 午间',
    'evening': '🌙 晚间',
  }[timePeriod] || '📚 英语助教';

  let voiceBlock = '';
  if (voiceData.voiceUrl) {
    voiceBlock = `🔊 [点击播放 AI 示范朗读](${voiceData.voiceUrl})`;
  } else if (voiceData.noTts) {
    voiceBlock = '🔊（TTS 未配置，可尝试配置 MiniMax API Key 或 Piper 本地 TTS）';
  } else if (voiceData.exhausted) {
    voiceBlock = '🔊（今日语音额度已用完）';
  } else {
    voiceBlock = '🔊（语音合成中...）';
  }

  return `${periodLabel} · 单词场景学习\n\n🤖 ${aiText}\n\n${voiceBlock}\n\n💡 试着跟读上面的句子，然后用英文回复我～`;
}

// ===== n08 · 记忆持久化 =====
async function saveLearningRecord(user_id, word, aiText, userInput, voiceUrl) {
  const now = new Date();
  const record = {
    word,
    last_review: now.toISOString(),
    review_count: 1,
    mastery: 0,
    chat_log: [{ role: 'ai', text: aiText }, { role: 'user', text: userInput }],
    voice_url: voiceUrl,
  };

  await memory.upsertWordRecord(user_id, word, record);
  await memory.appendChatLog(user_id, { role: 'ai', text: aiText }, { role: 'user', text: userInput });
}

// ===== 艾宾浩斯 · 计算下次复习时间 =====
function calcNextReview(reviewCount) {
  const intervals = config.EBINGHAUS;
  const interval = intervals[Math.min(reviewCount - 1, intervals.length - 1)];
  const next = new Date();
  next.setDate(next.getDate() + interval);
  return next.toISOString().split('T')[0];
}

// ===== 主流程入口 =====
/**
 * @param {string} userInput - 用户输入文字（如是语音需先转写）
 * @param {object} event - 飞书事件对象
 * @param {string} timePeriod - 时间段：morning / noon / evening
 * @returns {object} { success, aiReply, pushText, voiceData, lessonMode }
 */
async function run(userInput, event, timePeriod) {
  const msg = parseFeishuMessage(event);
  const asrResult = msg.is_voice ? await asrVoice(msg.voice_url) : '';
  const unifiedInput = mergeInput(msg, asrResult);

  // ===== 课程模式（定时任务，无用户输入）=====
  if (!unifiedInput.trim() && !msg.is_voice) {
    return runLessonMode(msg.user_id, timePeriod);
  }

  if (!unifiedInput.trim()) {
    return { success: false, error: '无法解析输入内容，请发文字或语音～' };
  }

  // ===== 交互模式 =====

  // n04 单词池
  const { pool } = await getWordPool(msg.user_id, timePeriod);

  // n05 LLM 对话
  const chatHistory = await memory.getChatHistory(msg.user_id, 10);
  const aiReply = await llmChat(unifiedInput, pool, timePeriod, chatHistory);

  // n06 TTS（返回文本+语音URL，由调用方决定如何处理）
  const voiceData = await ttsVoice(aiReply);

  // n07 生成推送文本
  const pushText = await feishuPush(aiReply, voiceData, timePeriod);

  // n08 记忆
  const STOP_WORDS = new Set([
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'the', 'a', 'an', 'to', 'of', 'in', 'on', 'at', 'for', 'with',
    'it', 'i', 'you', 'he', 'she', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
    'my', 'your', 'his', 'its', 'our', 'their',
    'and', 'or', 'but', 'not', 'no', 'yes', 'so', 'if', 'do', 'does', 'did',
    'can', 'will', 'would', 'could', 'should', 'may', 'has', 'have', 'had',
    'this', 'that', 'these', 'those', 'what', 'when', 'where', 'who', 'how', 'why',
    'just', 'very', 'too', 'all', 'some', 'any', 'more', 'most',
  ]);
  const rawWords = (unifiedInput.match(/[a-zA-Z]{3,}/g) || [])
    .map(w => w.toLowerCase())
    .filter(w => !STOP_WORDS.has(w));
  for (const w of rawWords.slice(0, 3)) {
    await saveLearningRecord(msg.user_id, w.toLowerCase(), aiReply, unifiedInput, voiceData.voiceUrl);
  }

  return {
    success: true,
    aiReply,
    voiceData,        // { text, voiceUrl, exhausted, noTts }
    pushText,
    lessonMode: false,
  };
}

// ===== 课程模式：定时任务，自动生成多段跟读文本发飞书 =====
async function runLessonMode(user_id, timePeriod) {
  const periodLabel = {
    'morning': '🌅 晨间',
    'noon': '☀️ 午间',
    'evening': '🌙 晚间',
  }[timePeriod] || '📚 英语助教';

  // 1. 读取单词池（复用 getWordPool）
  const { pool } = await getWordPool(user_id, timePeriod);

  // 2. 生成场景对话（3段，每段1-2句）
  const api = new MiniMaxAPI(config);
  const sceneMap = {
    'morning': '通勤场景（早晨出门、地铁、公交）',
    'noon': '午休场景（餐厅、咖啡厅）',
    'evening': '居家/购物场景（下班后、超市、网购）',
  };
  const scene = sceneMap[timePeriod] || '日常生活场景';
  const wordsStr = pool.length > 0 ? pool.join('、') : 'travel、subway、commute、delay';

  const lessonPrompt = `你是美式口语陪练。根据以下单词池，生成${periodLabel}的跟读练习内容。
单词池：${wordsStr}
场景：${scene}

要求：生成3段跟读对话，每段1-3句，简洁自然，适合跟读。重点单词要融入对话中。

输出格式（每段用 ||| 分隔）：
|||第1段对话文本（英文，1-3句）|||
|||第2段对话文本（英文，1-3句）|||
|||第3段对话文本（英文，1-3句）|||`;

  let lessonLines = [];
  try {
    const raw = await api.chat(lessonPrompt, []);
    lessonLines = raw.split(/\|{3}/).map(s => s.trim()).filter(s => s.length > 10);
  } catch (e) {
    console.error('[Lesson] LLM 生成失败:', e.message);
    lessonLines = [
      `Today's words are ${wordsStr}. Let's practice them in a natural conversation.`,
      `I'll say a sentence, you repeat after me. Ready? Let's begin!`,
      `Great job! Keep practicing every day and you'll improve fast.`,
    ];
  }

  // 3. 对每段生成 TTS 数据
  const voiceLines = [];
  for (const line of lessonLines) {
    try {
      const v = await ttsVoice(line);
      voiceLines.push({ text: line, voiceUrl: v.voiceUrl, exhausted: v.exhausted });
    } catch (e) {
      console.error('[Lesson] TTS 失败:', e.message);
      voiceLines.push({ text: line, voiceUrl: '', exhausted: false, noTts: true });
    }
  }

  const vocabText = pool.length > 0 ? pool.map(w => `• ${w}`).join('\n') : '';
  const summaryText = `${periodLabel} · 单词跟读练习\n\n🎧 上面发了 ${lessonLines.length} 段跟读内容，试着跟读～\n\n📚 今日词汇：\n${vocabText}\n\n💡 试着跟读，然后在飞书里发语音回复我！`;

  return {
    success: true,
    lessonMode: true,
    voiceLines,     // [{ text, voiceUrl, exhausted, noTts }]
    summaryText,
    pool,
  };
}

module.exports = { run };
