/**
 * tcm-exam-assistant.js - 中医执业医师考试备考助手
 * 
 * 功能：
 * 1. 生成每日复习计划（结合文档内容）
 * 2. 评估真题答案
 * 3. 管理错题集
 * 4. 追踪学习进度
 * 
 * 用法：
 *   node assistant.js "generate-plan" "{{用户反馈}}"
 *   node assistant.js "evaluate-answers" "{{题目}}" "{{用户答案}}" "{{正确答案}}"
 *   node assistant.js "export-wrong-questions"
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 注意：文档读取由 OpenClaw 主程序/AI 处理，本 skill 专注于复习计划生成

// ============================================================
// 配置
// ============================================================
const SKILL_DIR = path.join(__dirname);
const MEMORY_DIR = path.join(SKILL_DIR, 'memory');

// 考试日期（发布版：留空，用户首次运行时自动初始化）
const SKILL_EXAM_DATE = null; // 由用户在首次使用 时配置
const WRITTEN_EXAM_DATE = null;

// 记忆文件路径
const STAGE_FILE = path.join(MEMORY_DIR, 'stage.json');
const PROGRESS_FILE = path.join(MEMORY_DIR, 'progress.json');
const WRONG_QUESTIONS_FILE = path.join(MEMORY_DIR, 'wrong-questions.json');
const REVIEW_SCHEDULE_FILE = path.join(MEMORY_DIR, 'review-schedule.json');
const USER_PROFILE_FILE = path.join(MEMORY_DIR, 'user-profile.json');
const DOC_CACHE_FILE = path.join(MEMORY_DIR, 'doc-cache.json');

// ============================================================
// 工具函数
// ============================================================

function ensureDirExists(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

function initMemoryFiles() {
  ensureDirExists(MEMORY_DIR);
  ensureDirExists(OUTPUT_DIR);

  if (!fs.existsSync(STAGE_FILE)) {
    fs.writeFileSync(STAGE_FILE, JSON.stringify({
      currentStage: 'skill-exam-prep',
      stageStartDate: new Date().toISOString().split('T')[0],
      skillExamDate: null,
      writtenExamDate: null,
      daysToSkillExam: null,
      daysToWrittenExam: null
    }, null, 2));
  }

  if (!fs.existsSync(PROGRESS_FILE)) {
    fs.writeFileSync(PROGRESS_FILE, JSON.stringify({
      subjects: {
        'skill-station-1': { name: '技能第一站（病例分析）', progress: 0, lastReviewDate: null, chapters: [] },
        'skill-station-2': { name: '技能第二站（操作）', progress: 0, lastReviewDate: null, chapters: [] },
        'skill-station-3': { name: '技能第三站（答辩）', progress: 0, lastReviewDate: null, chapters: [] },
        'tcm-herbs': { name: '中药学', progress: 0, lastReviewDate: null, chapters: [] },
        'tcm-formulas': { name: '方剂学', progress: 0, lastReviewDate: null, chapters: [] },
        'tcm-internal': { name: '中医内科学', progress: 0, lastReviewDate: null, chapters: [] },
        'acupuncture': { name: '针灸学', progress: 0, lastReviewDate: null, chapters: [] },
        'tcm-basic': { name: '中医基础理论', progress: 0, lastReviewDate: null, chapters: [] },
        'tcm-diagnosis': { name: '中医诊断学', progress: 0, lastReviewDate: null, chapters: [] },
        'western-medicine': { name: '西医综合', progress: 0, lastReviewDate: null, chapters: [] }
      },
      lastStudyDate: null
    }, null, 2));
  }

  if (!fs.existsSync(WRONG_QUESTIONS_FILE)) {
    fs.writeFileSync(WRONG_QUESTIONS_FILE, JSON.stringify({
      questions: [],
      totalCount: 0,
      bySubject: {},
      lastExportDate: null
    }, null, 2));
  }

  if (!fs.existsSync(REVIEW_SCHEDULE_FILE)) {
    fs.writeFileSync(REVIEW_SCHEDULE_FILE, JSON.stringify({
      pendingReviews: [],
      ebbinghausIntervals: [1, 3, 7, 15, 30]
    }, null, 2));
  }

  if (!fs.existsSync(USER_PROFILE_FILE)) {
    fs.writeFileSync(USER_PROFILE_FILE, JSON.stringify({
      studyTimeSlots: {
        morning: { start: null, duration: null, type: 'memory' },
        evening: { start: null, duration: null, type: 'deep' }
      },
      preferences: {
        outputFormat: 'discord',
        planDetailLevel: 'detailed',
        aggressionMode: 'aggressive' // conservative / standard / aggressive / crazy
      },
      weakPoints: []
    }, null, 2));
  }

  if (!fs.existsSync(DOC_CACHE_FILE)) {
    fs.writeFileSync(DOC_CACHE_FILE, JSON.stringify({
      docs: [],
      lastUpdated: null,
      examInfo: {
        skillExamDate: null,
        writtenExamDate: null,
        skillStations: ['第一站（病例分析）', '第二站（操作）', '第三站（答辩）']
      }
    }, null, 2));
  }
}

function getDaysToSkillExam() {
  const today = new Date();
  if (!SKILL_EXAM_DATE) return null;
  const diff = SKILL_EXAM_DATE - today;
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

function getDaysToWrittenExam() {
  const today = new Date();
  if (!WRITTEN_EXAM_DATE) return null;
  const diff = WRITTEN_EXAM_DATE - today;
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

function readMemoryFile(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }
    return null;
  } catch (error) {
    console.error(`[ERROR] 读取记忆文件失败：${error.message}`);
    return null;
  }
}

function writeMemoryFile(filePath, data) {
  try {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
    return true;
  } catch (error) {
    console.error(`[ERROR] 写入记忆文件失败：${error.message}`);
    return false;
  }
}

/**
 * 同步桌面文档到 OpenClaw 记忆目录
 * 自动将桌面"中医备考系统"文件夹中的 docx/txt 文件复制到 memory 目录
 * 注意：发布版不包含具体文件名，用户需自行配置
 */
function syncDocsFromDesktop() {
  console.log('[INFO] 文档同步功能需用户配置路径');
  return { syncedCount: 0, syncedDir: null };
}

/**
 * 使用 OpenClaw 读取文档
 */
function readDocWithOpenClaw() {
  console.log('[INFO] 调用 OpenClaw 读取文档...');
  
  const docCache = readMemoryFile(DOC_CACHE_FILE);
  
  // 先同步文档
  syncDocsFromDesktop();
  
  const instruction = {
    action: 'read-docs',
    docDir: path.join(MEMORY_DIR, 'synced-docs'),
    files: docCache.docs
  };
  
  // 返回指令，让 OpenClaw 主程序处理
  return instruction;
}

/**
 * 解析用户反馈
 */
function parseFeedback(feedback) {
  const result = {
    studiedChapters: [],
    wrongQuestions: [],
    studiedContent: [],
    notes: ''
  };

  // 检测技能考试相关
  if (feedback.includes('技能') || feedback.includes('第一站') || feedback.includes('第二站') || feedback.includes('第三站')) {
    if (feedback.includes('第一站')) {
      result.studiedChapters.push({ subject: 'skill-station-1', name: '第一站复习' });
    }
    if (feedback.includes('第二站')) {
      result.studiedChapters.push({ subject: 'skill-station-2', name: '第二站复习' });
    }
    if (feedback.includes('第三站')) {
      result.studiedChapters.push({ subject: 'skill-station-3', name: '第三站复习' });
    }
  }

  // 检测笔试相关
  if (feedback.includes('肺系') || feedback.includes('感冒') || feedback.includes('咳嗽')) {
    result.studiedChapters.push({ subject: 'tcm-internal', name: '肺系病证' });
  }
  if (feedback.includes('麻黄') || feedback.includes('桂枝') || feedback.includes('解表药')) {
    result.studiedChapters.push({ subject: 'tcm-herbs', name: '解表药' });
  }

  // 检测错题
  const wrongPattern = /错了？?(\d+)[道]?题/g;
  const wrongMatch = wrongPattern.exec(feedback);
  if (wrongMatch) {
    result.wrongQuestions.push({
      count: parseInt(wrongMatch[1]),
      date: new Date().toISOString().split('T')[0]
    });
  }

  result.notes = feedback;
  return result;
}

/**
 * 计算每日应学量（激进模式）
 */
function calculateDailyLoad(progress, userProfile, daysRemaining) {
  const mode = userProfile?.preferences?.aggressionMode || 'aggressive';
  const aggressionMultiplier = {
    conservative: 1.0,
    standard: 1.2,
    aggressive: 1.5,
    crazy: 2.0
  }[mode];

  // 计算剩余章节
  let totalChapters = 50; // 假设总共 50 章
  let studiedChapters = 0;
  for (const key in progress.subjects) {
    studiedChapters += progress.subjects[key].chapters.length;
  }
  const remainingChapters = totalChapters - studiedChapters;

  // 每日应学 = 剩余章节 ÷ 剩余天数 × 激进系数
  const dailyChapters = Math.ceil(remainingChapters / daysRemaining * aggressionMultiplier);

  return {
    dailyChapters,
    aggressionMode: mode,
    remainingChapters,
    studiedChapters
  };
}

/**
 * 生成每日复习计划
 */
async function generatePlan(feedback) {
  console.log('[INFO] ════════════════════════════════════════════');
  console.log('[INFO] 📅 生成每日复习计划');
  console.log('[INFO] ════════════════════════════════════════════');
  console.log(`[INFO] 用户反馈：${feedback}`);

  // 初始化记忆文件
  initMemoryFiles();

  const stage = readMemoryFile(STAGE_FILE);
  const progress = readMemoryFile(PROGRESS_FILE);
  const wrongQuestions = readMemoryFile(WRONG_QUESTIONS_FILE);
  const reviewSchedule = readMemoryFile(REVIEW_SCHEDULE_FILE);
  const userProfile = readMemoryFile(USER_PROFILE_FILE);

  // 更新考试天数
  stage.daysToSkillExam = getDaysToSkillExam();
  stage.daysToWrittenExam = getDaysToWrittenExam();
  writeMemoryFile(STAGE_FILE, stage);

  // 判断当前阶段
  const daysToSkillExam = stage.daysToSkillExam;
  const isSkillExamPhase = daysToSkillExam <= 90; // 90 天内以技能考试为主

  // 解析用户反馈
  const parsedFeedback = parseFeedback(feedback);

  // 更新进度
  if (parsedFeedback.studiedChapters.length > 0) {
    for (const chapter of parsedFeedback.studiedChapters) {
      if (progress.subjects[chapter.subject]) {
        if (!progress.subjects[chapter.subject].chapters.includes(chapter.name)) {
          progress.subjects[chapter.subject].chapters.push(chapter.name);
          progress.subjects[chapter.subject].progress += 10;
        }
      }
    }
    progress.lastStudyDate = new Date().toISOString().split('T')[0];
    writeMemoryFile(PROGRESS_FILE, progress);
  }

  // 计算每日应学量
  const daysRemaining = isSkillExamPhase ? daysToSkillExam : stage.daysToWrittenExam;
  const dailyLoad = calculateDailyLoad(progress, userProfile, daysRemaining);

  // 生成计划
  const plan = buildPlan(stage, progress, reviewSchedule, userProfile, parsedFeedback, dailyLoad, isSkillExamPhase);

  console.log('[INFO] ════════════════════════════════════════════');
  console.log('[INFO] ✅ 计划生成完成');
  console.log('[INFO] ════════════════════════════════════════════');

  return plan;
}

/**
 * 构建复习计划
 */
function buildPlan(stage, progress, reviewSchedule, userProfile, parsedFeedback, dailyLoad, isSkillExamPhase) {
  const today = new Date();
  const dateStr = today.toISOString().split('T')[0];
  const daysToSkillExam = stage.daysToSkillExam;
  const daysToWrittenExam = stage.daysToWrittenExam;

  // 构建计划文本
  let plan = `📅 明日复习计划（${dateStr}）\n`;
  plan += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;

  if (isSkillExamPhase) {
    plan += `【备考阶段】技能考试备考 - ${dailyLoad.aggressionMode}模式\n`;
    plan += `【距离技能考试】还有 ${daysToSkillExam} 天\n`;
    plan += `【距离笔试】还有 ${daysToWrittenExam} 天\n`;
  } else {
    plan += `【备考阶段】笔试备考 - ${dailyLoad.aggressionMode}模式\n`;
    plan += `【距离技能考试】已过\n`;
    plan += `【距离笔试】还有 ${daysToWrittenExam} 天\n`;
  }

  plan += `【每日应学】${dailyLoad.dailyChapters} 章（${dailyLoad.aggressionMode}模式）\n`;
  plan += `【已学内容】${dailyLoad.studiedChapters} 章\n`;
  plan += `【剩余内容】${dailyLoad.remainingChapters} 章\n\n`;

  // 中午任务
  const morningSlot = userProfile?.studyTimeSlots?.morning;
  const morningStr = morningSlot?.start ? `（${morningSlot.start}，${morningSlot.duration || 30} 分钟）` : '';
  plan += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
  plan += `☀️ 中午任务${morningStr}\n`;
  plan += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
  plan += `【背诵内容】\n`;

  if (isSkillExamPhase) {
    // 技能考试阶段：背诵技能相关内容
    plan += `- 技能考试要点：\n`;
    plan += `  · 第一站：病例分析模板\n`;
    plan += `  · 第二站：操作流程口诀\n`;
    plan += `  · 第三站：答辩要点\n`;
  } else {
    // 笔试阶段：背诵中药方剂
    const herbsChapters = progress.subjects['tcm-herbs'].chapters;
    if (herbsChapters.length > 0) {
      const lastChapter = herbsChapters[herbsChapters.length - 1];
      plan += `- 复习昨日中药：${lastChapter}\n`;
    } else {
      plan += `- 新学：解表药（麻黄、桂枝、细辛）\n`;
      plan += `  · 共同点：辛温解表\n`;
      plan += `  · 不同点：麻黄发汗最强，桂枝温通经脉，细辛祛风止痛\n`;
    }
  }

  plan += `\n`;

  // 晚上任务
  const eveningSlot = userProfile?.studyTimeSlots?.evening;
  const eveningStr = eveningSlot?.start ? `（${eveningSlot.start}，${eveningSlot.duration || 180} 分钟）` : '';
  plan += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
  plan += `🌙 晚上任务${eveningStr}\n`;
  plan += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
  plan += `【学习内容】\n`;

  if (isSkillExamPhase) {
    // 技能考试阶段
    plan += `- 技能考试专项训练：\n`;
    plan += `  · 第一站：完成 2 个病例分析练习\n`;
    plan += `  · 第二站：练习 1 个操作项目\n`;
    plan += `  · 第三站：模拟答辩 5 题\n`;
    plan += `\n`;
    plan += `【提示】请让 OpenClaw 读取技能考试文档，获取具体内容\n`;
  } else {
    // 笔试阶段
    const internalChapters = progress.subjects['tcm-internal'].chapters;
    if (internalChapters.length > 0) {
      const lastChapter = internalChapters[internalChapters.length - 1];
      plan += `- 复习昨日中内：${lastChapter}\n`;
    } else {
      plan += `- 新学：中医内科学 - 肺系病证\n`;
    }
  }

  plan += `\n`;
  plan += `【真题任务】\n`;
  plan += `- 完成 ${dailyLoad.dailyChapters * 5} 道相关真题\n`;
  plan += `- 完成后回复答案格式：答案：1.A 2.B 3.C...\n`;

  plan += `\n`;
  plan += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
  plan += `📝 复习提醒\n`;
  plan += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
  plan += `- 睡前请反馈今日学习情况，以便生成后日计划\n`;
  plan += `- 让 OpenClaw 读取你的备考文档，获取更详细的内容\n`;

  return plan;
}

/**
 * 评估答案
 */
function evaluateAnswers(questions, userAnswers, correctAnswers) {
  console.log('[INFO] ════════════════════════════════════════════');
  console.log('[INFO] ✅ 评估答案');
  console.log('[INFO] ════════════════════════════════════════════');

  const result = {
    totalQuestions: 0,
    correctCount: 0,
    wrongCount: 0,
    wrongDetails: []
  };

  const userAnsList = parseAnswers(userAnswers);
  const correctAnsList = parseAnswers(correctAnswers);

  result.totalQuestions = userAnsList.length;

  for (let i = 0; i < userAnsList.length; i++) {
    if (userAnsList[i] === correctAnsList[i]) {
      result.correctCount++;
    } else {
      result.wrongCount++;
      result.wrongDetails.push({
        questionIndex: i + 1,
        userAnswer: userAnsList[i],
        correctAnswer: correctAnsList[i],
        date: new Date().toISOString().split('T')[0]
      });
    }
  }

  if (result.wrongCount > 0) {
    recordWrongQuestions(result.wrongDetails);
  }

  const report = buildEvaluationReport(result);
  return report;
}

function parseAnswers(answerStr) {
  const answers = [];
  const matches = answerStr.match(/[A-D]/gi);
  if (matches) {
    for (const m of matches) {
      answers.push(m.toUpperCase());
    }
  }
  return answers;
}

function recordWrongQuestions(wrongDetails) {
  const wrongQuestions = readMemoryFile(WRONG_QUESTIONS_FILE);

  for (const detail of wrongDetails) {
    wrongQuestions.questions.push({
      id: wrongQuestions.totalCount + 1,
      questionIndex: detail.questionIndex,
      userAnswer: detail.userAnswer,
      correctAnswer: detail.correctAnswer,
      date: detail.date,
      reviewCount: 0,
      nextReviewDate: getFutureDate(1)
    });
    wrongQuestions.totalCount++;
  }

  writeMemoryFile(WRONG_QUESTIONS_FILE, wrongQuestions);
  console.log(`[INFO] ✅ 已记录 ${wrongDetails.length} 道错题`);
}

function buildEvaluationReport(result) {
  let report = `✅ 答案评估报告\n`;
  report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
  report += `【正确率】${result.correctCount}/${result.totalQuestions} (${Math.round(result.correctCount / result.totalQuestions * 100)}%)\n`;
  report += `【正确】${result.correctCount} 道\n`;
  report += `【错误】${result.wrongCount} 道\n\n`;

  if (result.wrongCount > 0) {
    report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
    report += `❌ 错题分析\n`;
    report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;

    for (const detail of result.wrongDetails) {
      report += `第 ${detail.questionIndex} 题\n`;
      report += `  你的答案：${detail.userAnswer}\n`;
      report += `  正确答案：${detail.correctAnswer}\n`;
      report += `  已记录到错题集，将在第 1、3、7 天复习\n\n`;
    }
  }

  report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
  report += `📝 已记录 ${result.wrongCount} 道错题到错题集\n`;

  return report;
}

/**
 * 导出错题集
 */
function exportWrongQuestions() {
  console.log('[INFO] ════════════════════════════════════════════');
  console.log('[INFO] 📤 导出错题集');
  console.log('[INFO] ════════════════════════════════════════════');

  const wrongQuestions = readMemoryFile(WRONG_QUESTIONS_FILE);

  if (wrongQuestions.questions.length === 0) {
    console.log('[INFO] 错题集为空，暂无可导出内容');
    return '错题集为空，暂无可导出内容';
  }

  let content = `中医执业医师考试 - 错题集\n`;
  content += `导出日期：${new Date().toLocaleDateString('zh-CN')}\n`;
  content += `错题总数：${wrongQuestions.totalCount}\n\n`;
  content += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;

  for (const q of wrongQuestions.questions) {
    content += `第${q.id}题（${q.date}）\n`;
    content += `  题目序号：${q.questionIndex}\n`;
    content += `  你的答案：${q.userAnswer}\n`;
    content += `  正确答案：${q.correctAnswer}\n`;
    content += `  复习次数：${q.reviewCount}\n`;
    content += `  下次复习：${q.nextReviewDate}\n\n`;
  }

  const filename = `错题集_${new Date().toISOString().split('T')[0]}`;
  const outputPath = path.join(OUTPUT_DIR, `${filename}.txt`);

  try {
    fs.writeFileSync(outputPath, content, 'utf8');
    console.log(`[INFO] ✅ 错题集已导出：${outputPath}`);
    return `错题集已导出：${outputPath}`;
  } catch (error) {
    console.error(`[ERROR] 导出失败：${error.message}`);
    return `导出失败：${error.message}`;
  }
}

function getFutureDate(days) {
  const date = new Date();
  date.setDate(date.getDate() + days);
  return date.toISOString().split('T')[0];
}

async function main() {
  initMemoryFiles();

  const args = process.argv.slice(2);

  console.log('[INFO] ════════════════════════════════════════════');
  console.log('[INFO] 📚 tcm-exam-assistant 技能 v2.0（技能考试优先）');
  console.log('[INFO] ════════════════════════════════════════════');
  console.log(`[INFO] 收到参数数量：${args.length}`);

  if (args.length < 1) {
    console.error('[ERROR] 用法：node assistant.js "action" [params...]');
    console.error('[ERROR] action: generate-plan / evaluate-answers / export-wrong-questions');
    process.exit(1);
  }

  const action = args[0];

  try {
    switch (action) {
      case 'generate-plan':
        if (args.length < 2) {
          console.error('[ERROR] generate-plan 需要用户反馈参数');
          process.exit(1);
        }
        const plan = await generatePlan(args[1]);
        console.log('\n' + plan);
        break;

      case 'evaluate-answers':
        if (args.length < 4) {
          console.error('[ERROR] evaluate-answers 需要题目、用户答案、正确答案参数');
          process.exit(1);
        }
        const report = evaluateAnswers(args[1], args[2], args[3]);
        console.log('\n' + report);
        break;

      case 'export-wrong-questions':
        const result = exportWrongQuestions();
        console.log('\n' + result);
        break;

      case 'sync-docs':
        const syncResult = syncDocsFromDesktop();
        console.log('\n✅ 文档同步完成：' + syncResult.syncedCount + ' 个文件');
        console.log('同步目录：' + syncResult.syncedDir);
        break;

      default:
        console.error(`[ERROR] 未知操作：${action}`);
        console.error('[ERROR] 支持的操作：generate-plan / evaluate-answers / export-wrong-questions / sync-docs');
        process.exit(1);
    }
  } catch (error) {
    console.error(`[ERROR] 执行失败：${error.message}`);
    console.error(error.stack);
    process.exit(1);
  }
}

main();
