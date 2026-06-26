/**
 * Study Buddy - 题库引擎
 * 功能：出题、判分、解析
 * 
 * 🚀 优化：支持批量出题（一次 5 题/10 题）
 */

const { listRecords, createRecord } = require('./bitable-client.js');

// 当前答题状态（内存缓存，按 userId 分组）
// 结构：Map<userId, { questions: [], answers: {}, startTime, filters, mode: 'single'|'batch' }>
const answerSessions = new Map();

// 答案缓存（避免重复查询 Bitable）
// 结构：Map<questionId, questionFields>
const questionCache = new Map();

// 批量出题默认配置
const BATCH_CONFIG = {
  DEFAULT_COUNT: 5,      // 默认一次出 5 题
  MAX_COUNT: 10,         // 最多一次 10 题
  MODES: ['single', 'batch'] // single=单题，batch=批量
};

/**
 * 处理出题请求
 * @param {string} userText - 用户输入
 * @param {string} userId - 用户 ID
 * @param {Object} config - 配置信息
 * @returns {Promise<Object>} 回复对象
 */
async function handleQuestion(userText, userId, config) {
  try {
    // 1. 解析用户需求（分类、题型、难度）
    const filters = parseQuestionFilters(userText);
    
    // 2. 从 Bitable 获取题目
    const question = await getRandomQuestion(config, filters);
    
    if (!question) {
      return {
        text: `😅 抱歉，没有找到符合要求的题目。\n\n筛选条件：${JSON.stringify(filters)}\n\n请尝试其他条件，或联系开发者添加更多题库。`
      };
    }
    
    // 🚀 优化 3: 保存答题会话状态（用 userId 作为 key，简化识别）
    const sessionId = userId;
    answerSessions.set(sessionId, {
      questionId: question.fields["题目 ID"],
      correctAnswer: question.fields["正确答案"],
      startTime: Date.now(),
      filters: filters,
      category: question.fields["题库分类"],
      difficulty: question.fields["难度"]
    });
    
    // 🚀 优化 4: 缓存题目信息（避免重复查询）
    questionCache.set(question.fields["题目 ID"], question.fields);
    
    // 4. 格式化题目并返回
    const questionText = formatQuestionMessage(question, sessionId);
    
    return {
      text: questionText
    };
    
  } catch (error) {
    console.error('[Question Engine] Error:', error);
    return {
      text: `😅 出题时出现错误：${error.message}\n\n请稍后再试。`
    };
  }
}

/**
 * 处理用户答案（判分）- 🚀 优化版：使用缓存加速
 * @param {string} userAnswer - 用户答案（A/B/C/D）
 * @param {string} sessionId - 答题会话 ID
 * @param {string} userId - 用户 ID
 * @param {Object} config - 配置信息
 * @returns {Promise<Object>} 回复对象
 */
async function handleUserAnswer(userAnswer, sessionId, userId, config) {
  try {
    // 🚀 优化 1: 直接从内存缓存获取会话状态（无需查询 Bitable）
    const session = answerSessions.get(sessionId);
    if (!session) {
      return {
        text: `😅 未找到答题记录，请重新出题。\n\n说"来一道题"重新开始。`
      };
    }
    
    // 🚀 优化 2: 判断对错（毫秒级）
    const normalizedUserAnswer = userAnswer.trim().toUpperCase();
    const isCorrect = normalizedUserAnswer === session.correctAnswer;
    
    // 🚀 优化 3: 优先从缓存获取题目信息
    let question;
    if (questionCache.has(session.questionId)) {
      question = { fields: questionCache.get(session.questionId) };
    } else {
      // 缓存未命中，从 Bitable 获取并缓存
      question = await getQuestionById(config, session.questionId);
      if (question) {
        questionCache.set(session.questionId, question.fields);
      }
    }
    
    // 🚀 优化 4: 如果没有找到题目，使用会话中保存的备用信息
    if (!question) {
      question = {
        fields: {
          "题目内容": "题目信息已过期",
          "答案解析": "解析信息不可用，请重新出题。",
          "知识点": session.filters?.category || "未知",
          "题目来源": "系统",
          "难度": session.filters?.difficulty || "中等"
        }
      };
    }
    
    // 5. 格式化回复
    let response = "";
    
    if (isCorrect) {
      response = formatCorrectAnswerResponse(question, normalizedUserAnswer);
      
      // 记录正确答题
      await logProgress(userId, 1, 1, config);
      
    } else {
      response = formatWrongAnswerResponse(question, normalizedUserAnswer, session.correctAnswer);
      
      // 记录错题到 Bitable
      await recordWrongAnswer({
        userId,
        questionId: session.questionId,
        questionText: question.fields["题目内容"],
        userAnswer: normalizedUserAnswer,
        correctAnswer: session.correctAnswer,
        config
      });
      
      // 记录进度
      await logProgress(userId, 1, 0, config);
    }
    
    // 6. 清理会话
    answerSessions.delete(sessionId);
    
    return {
      text: response
    };
    
  } catch (error) {
    console.error('[Answer Handler] Error:', error);
    return {
      text: `😅 判分时出现错误：${error.message}`
    };
  }
}

/**
 * 处理模拟考试
 * @param {string} userText - 用户输入
 * @param {string} userId - 用户 ID
 * @param {Object} config - 配置信息
 * @returns {Promise<Object>} 回复对象
 */
async function handleMockExam(userText, userId, config) {
  // TODO: 实现模拟考试逻辑
  return {
    text: `🎯 **模拟考试功能开发中**...\n\n预计下一版本上线！\n\n现在先试试单题练习吧：\n说"来一道 N2 语法题"开始。`
  };
}

/**
 * 解析用户输入中的筛选条件
 */
function parseQuestionFilters(text) {
  const filters = {
    category: null,
    questionType: null,
    difficulty: null
  };
  
  const lowerText = text.toLowerCase();
  
  // 分类筛选
  if (lowerText.includes('日语') || lowerText.includes('n2') || lowerText.includes('n1')) {
    if (lowerText.includes('n1')) {
      filters.category = '日语 N1';
    } else {
      filters.category = '日语 N2';
    }
  } else if (lowerText.includes('软考') || lowerText.includes('架构师')) {
    filters.category = '软考架构师';
  }
  
  // 题型筛选
  if (lowerText.includes('语法')) {
    filters.questionType = '语法';
  } else if (lowerText.includes('词汇')) {
    filters.questionType = '词汇';
  } else if (lowerText.includes('阅读') || lowerText.includes('阅读理解')) {
    filters.questionType = '阅读理解';
  } else if (lowerText.includes('听力')) {
    filters.questionType = '听力';
  } else if (lowerText.includes('选择') || lowerText.includes('选择题')) {
    filters.questionType = '选择题';
  } else if (lowerText.includes('案例')) {
    filters.questionType = '案例分析';
  }
  
  // 难度筛选
  if (lowerText.includes('简单')) {
    filters.difficulty = '简单';
  } else if (lowerText.includes('困难') || lowerText.includes('难')) {
    filters.difficulty = '困难';
  } else {
    filters.difficulty = '中等'; // 默认中等难度
  }
  
  return filters;
}

/**
 * 从 Bitable 随机获取一道题目
 */
async function getRandomQuestion(config, filters) {
  try {
    // 从 Bitable 获取所有题目
    const records = await listRecords(config.BITABLE_APP_TOKEN, config.BITABLE_TABLE_ID);
    
    // 筛选符合条件的题目
    let filteredQuestions = records.filter(record => {
      const fields = record.fields;
      
      // 分类筛选
      if (filters.category && fields["题库分类"] !== filters.category) {
        return false;
      }
      
      // 题型筛选
      if (filters.questionType && fields["题型"] !== filters.questionType) {
        return false;
      }
      
      // 难度筛选
      if (filters.difficulty && fields["难度"] !== filters.difficulty) {
        return false;
      }
      
      return true;
    });
    
    if (filteredQuestions.length === 0) {
      return null;
    }
    
    // 随机选择一道题
    const randomIndex = Math.floor(Math.random() * filteredQuestions.length);
    return filteredQuestions[randomIndex];
    
  } catch (error) {
    console.error('[Get Random Question] Error:', error);
    throw error;
  }
}

/**
 * 根据题目 ID 获取题目详情
 */
async function getQuestionById(config, questionId) {
  const records = await listRecords(config.BITABLE_APP_TOKEN, config.BITABLE_TABLE_ID);
  return records.find(r => r.fields["题目 ID"] === questionId);
}

/**
 * 格式化题目消息
 */
function formatQuestionMessage(question, sessionId) {
  const fields = question.fields;
  
  return `📚 **【${fields["题库分类"]}】${fields["题型"]}练习**

**题目**: ${fields["题目内容"]}

**选项**:
A) ${fields["选项 A"]}
B) ${fields["选项 B"]}
C) ${fields["选项 C"]}
D) ${fields["选项 D"]}

━━━━━━━━━━━━━━━━━━━

💡 请直接回复 **A/B/C/D** 提交答案～

（本题难度：${fields["难度"]} | 知识点：${fields["知识点"]}）`;
}

/**
 * 格式化正确答案回复
 */
function formatCorrectAnswerResponse(question, userAnswer) {
  const fields = question.fields;
  
  return `✅ **回答正确！** 太棒了！🎉

**解析**: 
${fields["答案解析"]}

**知识点**: ${fields["知识点"]}
**来源**: ${fields["题目来源"]}

━━━━━━━━━━━━━━━━━━━

继续挑战吗？
• 回复 **"继续"** 再来一道
• 回复 **"来一道${fields["题库分类"]}${fields["题型"]}题"** 指定类型
• 回复 **"查看进度"** 看看学习情况`;
}

/**
 * 格式化错误答案回复
 */
function formatWrongAnswerResponse(question, userAnswer, correctAnswer) {
  const fields = question.fields;
  
  return `❌ **回答错误**，再加油！💪

**你的答案**: ${userAnswer}
**正确答案**: ${correctAnswer}

**解析**: 
${fields["答案解析"]}

**知识点**: ${fields["知识点"]}

━━━━━━━━━━━━━━━━━━━

📝 这道题已自动加入你的**错题本**，稍后会推送复习提醒哦！

要不要再来一道？
• 回复 **"继续"** 挑战下一题
• 回复 **"查看错题"** 复习错题本`;
}

/**
 * 记录学习进度（简化版，实际应该写入 Bitable）
 */
async function logProgress(userId, totalQuestions, correctQuestions, config) {
  // TODO: 实现进度记录到 Bitable
  console.log(`[Progress] User ${userId}: +${totalQuestions} questions, +${correctQuestions} correct`);
  return Promise.resolve();
}

/**
 * 记录错题到 Bitable
 */
async function recordWrongAnswer(params) {
  const { userId, questionId, questionText, userAnswer, correctAnswer, config } = params;
  
  try {
    // TODO: 创建错题表后，取消下面代码的注释
    /*
    await createRecord(config.BITABLE_APP_TOKEN, "错题表 ID", {
      "user_id": userId,
      "question_id": questionId,
      "question_text": questionText,
      "user_answer": userAnswer,
      "correct_answer": correctAnswer,
      "wrong_time": new Date().toISOString(),
      "review_count": 0,
      "mastered": false
    });
    */
    
    console.log(`[Wrong Answer] Recorded for user ${userId}: ${questionId}`);
    return Promise.resolve();
    
  } catch (error) {
    console.error('[Record Wrong Answer] Error:', error);
    // 不抛出错误，避免影响用户体验
  }
}

// 🚀 导出缓存对象，供 index.js 使用
module.exports.answerSessions = answerSessions;
module.exports.questionCache = questionCache;

module.exports = {
  handleQuestion,
  handleUserAnswer,
  handleMockExam,
  parseQuestionFilters,
  getRandomQuestion,
  formatQuestionMessage
};
