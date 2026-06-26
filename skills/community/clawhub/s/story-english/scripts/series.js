#!/usr/bin/env node
/**
 * story-english series — browse available story series and how to start
 */

const lang = process.argv.includes('--lang')
  ? process.argv[process.argv.indexOf('--lang') + 1]
  : 'zh';
const isZh = lang === 'zh';

console.log(`
${isZh ? '📚 故事英语 — 系列介绍' : '📚 Story English — Series Guide'}
${'═'.repeat(54)}

${isZh ? '通过追剧的方式学英语。每集都是真实小说，不是教材。' : 'Learn English by following a story you actually want to read.'}

${'─'.repeat(54)}
🕵️  ${isZh ? '悬疑侦探' : 'Mystery'}  ·  The Shanghai Files
${'─'.repeat(54)}
${isZh
? '上海，雨夜，一名菜鸟侦探接手了一个不该碰的案子。\n    每集都是真正的悬疑小说体验，带你追凶同时学英语。'
: 'Shanghai. Rain. A rookie detective. A case she should have refused.\n    Atmospheric noir fiction — learn English while solving the mystery.'}

    ${isZh ? '推荐等级' : 'Level'}: B1–B2
    ${isZh ? '风格' : 'Style'}:    ${isZh ? '短句、对话、紧张气氛' : 'Short punchy sentences, dialogue-heavy, tense'}
    ${isZh ? '开始' : 'Start'}:    node episode.js --series shanghai --level B1 --chapter 1

${'─'.repeat(54)}
🏙️  ${isZh ? '都市生活' : 'Slice of Life'}  ·  City of Dreamers
${'─'.repeat(54)}
${isZh
? '四个朋友，一座新城市，关于工作、友情和迷失的故事。\n    最贴近日常英语表达，适合想学口语的学习者。'
: 'Four friends. A new city. The messy, funny, real story of growing up.\n    Closest to everyday spoken English — perfect for conversational learners.'}

    ${isZh ? '推荐等级' : 'Level'}: A2–B1
    ${isZh ? '风格' : 'Style'}:    ${isZh ? '温暖轻松、口语化、贴近生活' : 'Warm, relatable, conversational, workplace + personal'}
    ${isZh ? '开始' : 'Start'}:    node episode.js --series city --level A2 --chapter 1

${'─'.repeat(54)}
🚀  ${isZh ? '科幻冒险' : 'Sci-fi'}  ·  Starfall
${'─'.repeat(54)}
${isZh
? '2157年，深空探索飞船"子午线号"，六名船员，一个错误的目的地。\n    词汇量最丰富，适合想冲击高分的进阶学习者。'
: 'Year 2157. The research vessel Meridian. Six crew. One wrong destination.\n    Rich descriptive vocabulary — ideal for learners targeting IELTS/TOEFL.'}

    ${isZh ? '推荐等级' : 'Level'}: B1–B2
    ${isZh ? '风格' : 'Style'}:    ${isZh ? '画面感强、动作节奏、科技词汇' : 'Vivid descriptions, action pacing, technical vocabulary'}
    ${isZh ? '开始' : 'Start'}:    node episode.js --series starfall --level B1 --chapter 1

${'═'.repeat(54)}
${isZh ? '📖 等级说明' : '📖 Level Guide'}
${'─'.repeat(54)}
  A2  ${isZh ? '初级' : 'Elementary'}         — ${isZh ? '基础词汇，简单句型，每集5个新词' : 'Basic vocab, simple sentences, 5 new words/ep'}
  B1  ${isZh ? '中级（推荐）' : 'Intermediate (rec)'}  — ${isZh ? '日常词汇+习语，每集6个新词' : 'Everyday vocab + idioms, 6 new words/ep'}
  B2  ${isZh ? '中高级' : 'Upper-Intermediate'}  — ${isZh ? '高级词汇，复杂句式，每集8个新词' : 'Advanced vocab, complex grammar, 8 new words/ep'}

${'═'.repeat(54)}
${isZh ? '💡 学习建议' : '💡 Study Tips'}
${'─'.repeat(54)}
  1. ${isZh ? '先读故事，遇到生词先猜意思' : 'Read the story first — guess unknown words from context'}
  2. ${isZh ? '再看词汇板块，验证猜测是否正确' : 'Then check the Vocabulary section to verify'}
  3. ${isZh ? '完成章末测验（3题）' : 'Complete the 3-question quick check'}
  4. ${isZh ? '第二天用词汇复习模式巩固' : 'Next day, use vocab review mode to consolidate'}
  5. ${isZh ? '每集约10分钟，养成每日习惯' : '~10 min per episode — build a daily habit'}

  ${isZh ? '复习模式' : 'Review'}:  node vocab.js --mode review
  ${isZh ? '测验模式' : 'Quiz'}:    node vocab.js --mode quiz
`);
