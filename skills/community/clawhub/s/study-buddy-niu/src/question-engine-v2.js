/**
 * Study Buddy - 题库引擎 v2.0
 * 功能：出题、判分、解析
 * 
 * 🚀 新增：支持批量出题（一次 5 题/10 题）
 */

const { listRecords, createRecord } = require('./bitable-client.js');

// 当前答题状态（内存缓存，按 userId 分组）
const answerSessions = new Map();

// 答案缓存（避免重复查询 Bitable）
const questionCache = new Map();

// 批量出题配置
const BATCH_CONFIG = {
  DEFAULT_COUNT: 5,   // 默认一次出 5 题
  MAX_COUNT: 10       // 最多一次 10 题
};

/**
 * 处理出题请求 - 支持批量
 */
async function handleQuestion(userText, userId, config) {
  try {
    // 1. 解析用户需求
    const filters = parseQuestionFilters(userText);
    const count = parseQuestionCount(userText);
    
    // 2. 获取多道题目
    const questions = await getRandomQuestions(config, filters, count);
    
    if (!questions || questions.length === 0) {
      return { text: `😅 抱歉，没有找到符合要求的题目。` };
    }
    
    // 3. 保存会话状态（批量模式）
    answerSessions.set(userId, {
      questions: questions.map(q => ({
        id: q.fields["题目 ID"],
        answer: q.fields["正确答案"],
        fields: q.fields
      })),
      answers: {},
      startTime: Date.now(),
      mode: 'batch',
      total: questions.length
    });
    
    // 4. 缓存题目
    questions.forEach(q => questionCache.set(q.fields["题目 ID"], q.fields));
    
    // 5. 返回批量题目
    return { text: formatBatchQuestionsMessage(questions, userId) };
    
  } catch (error) {
    console.error('[Question] Error:', error);
    return { text: `😅 出题错误：${error.message}` };
  }
}

/**
 * 处理用户答案 - 批量判分
 */
async function handleUserAnswer(userAnswer, sessionId, userId, config) {
  try {
    const session = answerSessions.get(sessionId);
    if (!session) {
      return { text: `😅 未找到答题记录。\n\n说"来一道题"重新开始。` };
    }
    
    // 批量模式：收集答案
    if (session.mode === 'batch') {
      // 解析用户答案（如 "1.A 2.B 3.C 4.D 5.A"）
      const userAnswers = parseBatchAnswers(userAnswer);
      
      // 保存答案
      Object.entries(userAnswers).forEach(([qIndex, answer]) => {
        const question = session.questions[qIndex];
        if (question) {
          session.answers[question.id] = answer;
        }
      });
      
      // 检查是否所有题都答完了
      const answeredCount = Object.keys(session.answers).length;
      
      if (answeredCount < session.total) {
        return { 
          text: `✅ 已记录 ${answeredCount}/${session.total} 题\n\n继续回答剩余题目，或直接说"提交"交卷！` 
        };
      }
      
      // 全部答完，统一判分
      return await gradeBatchAnswers(session, userId, config);
    }
    
    // 单题模式（兼容旧版）
    return await gradeSingleAnswer(session, userId, config);
    
  } catch (error) {
    console.error('[Answer] Error:', error);
    return { text: `😅 判分错误：${error.message}` };
  }
}

/**
 * 批量判分
 */
async function gradeBatchAnswers(session, userId, config) {
  let correctCount = 0;
  let wrongQuestions = [];
  
  // 逐题判分
  session.questions.forEach(q => {
    const userAnswer = session.answers[q.id];
    if (userAnswer === q.answer) {
      correctCount++;
    } else {
      wrongQuestions.push({
        question: q,
        userAnswer: userAnswer
      });
    }
  });
  
  // 计算正确率
  const accuracy = Math.round((correctCount / session.total) * 100);
  
  // 记录错题
  for (const wrong of wrongQuestions) {
    await recordWrongAnswer({
      userId,
      questionId: wrong.question.id,
      questionText: wrong.question.fields["题目内容"],
      userAnswer: wrong.userAnswer,
      correctAnswer: wrong.question.answer,
      config
    });
  }
  
  // 记录进度
  await logProgress(userId, session.total, correctCount, config);
  
  // 清理会话
  answerSessions.delete(session.userId);
  
  // 返回成绩报告
  return {
    text: formatBatchResultMessage(session, correctCount, accuracy, wrongQuestions)
  };
}

/**
 * 单题判分（兼容旧版）
 */
async function gradeSingleAnswer(session, userId, config) {
  // ... 保持原有逻辑
  return { text: "单题模式兼容代码..." };
}

/**
 * 解析题目数量
 */
function parseQuestionCount(text) {
  const match = text.match(/(\d+)\s*道/);
  if (match) {
    const count = parseInt(match[1]);
    return Math.min(count, BATCH_CONFIG.MAX_COUNT);
  }
  
  // 关键词匹配
  if (text.includes('五道') || text.includes('5 道')) return 5;
  if (text.includes('十道') || text.includes('10 道')) return 10;
  
  return BATCH_CONFIG.DEFAULT_COUNT; // 默认 5 道
}

/**
 * 解析批量答案
 */
function parseBatchAnswers(text) {
  const answers = {};
  
  // 支持格式："1.A 2.B 3.C" 或 "A,B,C,D,A" 或 "1A 2B 3C"
  const patterns = [
    /(\d+)\.?([ABCD])/gi,  // 1.A 2.B
    /^([ABCD])(?:\s*,\s*([ABCD]))*$/i,  // A,B,C,D
    /(\d+)([ABCD])/gi  // 1A 2B
  ];
  
  for (const pattern of patterns) {
    const matches = text.matchAll(pattern);
    for (const match of matches) {
      if (match[1] && match[2]) {
        // 数字 + 答案格式
        const index = parseInt(match[1]) - 1; // 转 0-based
        answers[index] = match[2].toUpperCase();
      } else if (match[0]) {
        // 纯字母格式 A,B,C,D
        const letters = match[0].split(/[\s,]+/);
        letters.forEach((letter, i) => {
          if (/^[ABCD]$/.test(letter)) {
            answers[i] = letter.toUpperCase();
          }
        });
      }
    }
  }
  
  return answers;
}

/**
 * 格式化批量题目消息
 */
function formatBatchQuestionsMessage(questions, userId) {
  const count = questions.length;
  
  let msg = `📚 **批量练习**（共${count}题）\n\n`;
  msg += `━━━━━━━━━━━━━━━━━━━\n\n`;
  
  questions.forEach((q, i) => {
    const f = q.fields;
    msg += `**第${i+1}题**【${f["题库分类"]}】${f["题型"]}\n`;
    msg += `${f["题目内容"]}\n\n`;
    msg += `A) ${f["选项 A"]}\n`;
    msg += `B) ${f["选项 B"]}\n`;
    msg += `C) ${f["选项 C"]}\n`;
    msg += `D) ${f["选项 D"]}\n`;
    msg += `\n---\n\n`;
  });
  
  msg += `━━━━━━━━━━━━━━━━━━━\n\n`;
  msg += `💡 **答题方式**:\n`;
  msg += `• 格式 1: \`1.A 2.B 3.C 4.D 5.A\`\n`;
  msg += `• 格式 2: \`A,B,C,D,A\`\n`;
  msg += `• 格式 3: \`1A 2B 3C 4D 5A\`\n\n`;
  msg += `回复答案后说 **"提交"** 或直接发送即可！\n\n`;
  msg += `*Study Buddy v2.0 | OPC 极限挑战赛*`;
  
  return msg;
}

/**
 * 格式化批量结果消息
 */
function formatBatchResultMessage(session, correctCount, accuracy, wrongQuestions) {
  let msg = `🎯 **批量练习成绩单**\n\n`;
  msg += `━━━━━━━━━━━━━━━━━━━\n\n`;
  
  msg += `📊 **总体统计**:\n`;
  msg += `• 总题数：**${session.total}** 道\n`;
  msg += `• 答对：**${correctCount}** 道\n`;
  msg += `• 答错：**${session.total - correctCount}** 道\n`;
  msg += `• 正确率：**${accuracy}%** ${getAccuracyEmoji(accuracy)}\n\n`;
  
  msg += `━━━━━━━━━━━━━━━━━━━\n\n`;
  
  if (wrongQuestions.length > 0) {
    msg += `❌ **错题解析**:\n\n`;
    wrongQuestions.forEach((w, i) => {
      const f = w.question.fields;
      msg += `${i+1}. 【${f["知识点"]}】\n`;
      msg += `   你的答案：${w.userAnswer} ❌ | 正确：${f["正确答案"]} ✅\n`;
      msg += `   解析：${f["答案解析"]}\n\n`;
    });
  } else {
    msg += `🎉 **全对！** 太棒了！继续保持！\n\n`;
  }
  
  msg += `━━━━━━━━━━━━━━━━━━━\n\n`;
  msg += `💡 **下一步**:\n`;
  msg += `• 回复 **"继续"** 再来一组\n`;
  msg += `• 回复 **"查看错题"** 复习错题本\n`;
  msg += `• 回复 **"查看进度"** 看学习情况\n`;
  
  return msg;
}

/**
 * 获取多道随机题目
 */
async function getRandomQuestions(config, filters, count) {
  const records = await listRecords(config.BITABLE_APP_TOKEN, config.BITABLE_TABLE_ID);
  
  // 筛选
  let filtered = records.filter(r => {
    const f = r.fields;
    if (filters.category && f["题库分类"] !== filters.category) return false;
    if (filters.questionType && f["题型"] !== filters.questionType) return false;
    if (filters.difficulty && f["难度"] !== filters.difficulty) return false;
    return true;
  });
  
  if (filtered.length === 0) return [];
  
  // 随机抽取 count 道
  const result = [];
  const used = new Set();
  
  while (result.length < Math.min(count, filtered.length)) {
    const idx = Math.floor(Math.random() * filtered.length);
    if (!used.has(idx)) {
      used.add(idx);
      result.push(filtered[idx]);
    }
  }
  
  return result;
}

/**
 * 解析筛选条件
 */
function parseQuestionFilters(text) {
  const filters = { category: null, questionType: null, difficulty: '中等' };
  const lower = text.toLowerCase();
  
  if (lower.includes('日语') || lower.includes('n2')) filters.category = '日语 N2';
  else if (lower.includes('软考') || lower.includes('架构师')) filters.category = '软考架构师';
  
  if (lower.includes('语法')) filters.questionType = '语法';
  else if (lower.includes('词汇')) filters.questionType = '词汇';
  
  if (lower.includes('简单')) filters.difficulty = '简单';
  else if (lower.includes('困难')) filters.difficulty = '困难';
  
  return filters;
}

/**
 * 记录错题
 */
async function recordWrongAnswer(params) {
  console.log(`[Wrong] ${params.userId}: ${params.questionId}`);
}

/**
 * 记录进度
 */
async function logProgress(userId, total, correct, config) {
  console.log(`[Progress] ${userId}: ${correct}/${total}`);
}

/**
 * 表情符号
 */
function getAccuracyEmoji(rate) {
  if (rate >= 90) return '🏆';
  if (rate >= 80) return '🌟';
  if (rate >= 70) return '👍';
  return '💪';
}

module.exports = {
  handleQuestion,
  handleUserAnswer,
  parseQuestionCount,
  parseBatchAnswers,
  formatBatchQuestionsMessage,
  formatBatchResultMessage
};
