/**
 * Study Buddy - 错题本管理
 * 功能：查看错题、记录错题、复习提醒
 */

const { listRecords, createRecord, updateRecord } = require('./bitable-client.js');

// 错题表配置（待创建）
const WRONG_ANSWERS_TABLE_ID = "tbl_wrong_answers"; // TODO: 创建后替换实际 ID

/**
 * 处理查看错题请求
 * @param {string} userText - 用户输入
 * @param {string} userId - 用户 ID
 * @param {Object} config - 配置信息
 * @returns {Promise<Object>} 回复对象
 */
async function handleWrongQuestions(userText, userId, config) {
  try {
    // TODO: 创建错题表后，从 Bitable 获取真实数据
    // 现在返回提示信息
    
    return {
      text: `📝 **错题本功能说明**

━━━━━━━━━━━━━━━━━━━

🎯 **功能亮点**:
• 自动记录答错的题目
• 智能推送复习提醒
• 标记已掌握的错题
• 按知识点分类统计

📊 **当前状态**:
错题表正在创建中...

预计下一版本上线！

━━━━━━━━━━━━━━━━━━━

💡 **使用方式**（即将支持）:
• "查看我的错题" - 浏览所有错题
• "复习错题" - 随机抽取错题重做
• "统计错题" - 查看错题分布
• "标记掌握" - 标记已掌握的错题

现在先专注于练习吧！
说 **"来一道 N2 语法题"** 开始学习～`
    };
    
  } catch (error) {
    console.error('[Wrong Questions] Error:', error);
    return {
      text: `😅 查看错题时出现错误：${error.message}`
    };
  }
}

/**
 * 记录错题到 Bitable
 * @param {Object} params - 参数对象
 * @returns {Promise<void>}
 */
async function recordWrongAnswer(params) {
  const { userId, questionId, questionText, userAnswer, correctAnswer, config } = params;
  
  try {
    // TODO: 创建错题表后，取消下面代码的注释
    /*
    const now = new Date().toISOString();
    
    await createRecord(
      config.BITABLE_APP_TOKEN,
      WRONG_ANSWERS_TABLE_ID,
      {
        "user_id": userId,
        "question_id": questionId,
        "question_text": questionText,
        "user_answer": userAnswer,
        "correct_answer": correctAnswer,
        "wrong_time": now,
        "review_count": 0,
        "mastered": false,
        "notes": ""
      }
    );
    
    console.log(`[Wrong Answer] Recorded for user ${userId}: ${questionId}`);
    */
    
    // 临时方案：在控制台记录
    console.log(`[Wrong Answer - Mock] User: ${userId}, Question: ${questionId}, Your Answer: ${userAnswer}, Correct: ${correctAnswer}`);
    
    return Promise.resolve();
    
  } catch (error) {
    console.error('[Record Wrong Answer] Error:', error);
    // 不抛出错误，避免影响用户体验
  }
}

/**
 * 获取用户的错题列表
 * @param {string} userId - 用户 ID
 * @param {Object} config - 配置信息
 * @param {Object} options - 选项 {limit, category, mastered}
 * @returns {Promise<Array>} 错题数组
 */
async function getUserWrongQuestions(userId, config, options = {}) {
  try {
    // TODO: 从 Bitable 获取真实数据
    const limit = options.limit || 10;
    const category = options.category;
    const mastered = options.mastered;
    
    // 模拟数据
    const mockWrongQuestions = [
      {
        "question_id": "jp_001",
        "question_text": "彼は約束の時間に遅れた_____、謝りもせず帰ってしまった。",
        "user_answer": "A",
        "correct_answer": "B",
        "wrong_time": "2026-03-26T10:30:00Z",
        "review_count": 0,
        "mastered": false,
        "category": "日语 N2",
        "knowledge_point": "～あげく"
      },
      {
        "question_id": "rk_001",
        "question_text": "在 UML 中，用于描述系统中类的静态结构和类之间关系的图是？",
        "user_answer": "B",
        "correct_answer": "C",
        "wrong_time": "2026-03-26T14:20:00Z",
        "review_count": 1,
        "mastered": false,
        "category": "软考架构师",
        "knowledge_point": "UML 类图"
      }
    ];
    
    // 筛选
    let filtered = mockWrongQuestions;
    
    if (category) {
      filtered = filtered.filter(q => q.category === category);
    }
    
    if (mastered !== undefined) {
      filtered = filtered.filter(q => q.mastered === mastered);
    }
    
    return filtered.slice(0, limit);
    
  } catch (error) {
    console.error('[Get Wrong Questions] Error:', error);
    return [];
  }
}

/**
 * 标记错题为已掌握
 * @param {string} userId - 用户 ID
 * @param {string} questionId - 题目 ID
 * @param {Object} config - 配置信息
 * @returns {Promise<boolean>} 是否成功
 */
async function markQuestionAsMastered(userId, questionId, config) {
  try {
    // TODO: 更新 Bitable 记录
    console.log(`[Mark Mastered] User: ${userId}, Question: ${questionId}`);
    return true;
    
  } catch (error) {
    console.error('[Mark Mastered] Error:', error);
    return false;
  }
}

/**
 * 获取错题统计信息
 * @param {string} userId - 用户 ID
 * @param {Object} config - 配置信息
 * @returns {Promise<Object>} 统计信息
 */
async function getWrongQuestionStats(userId, config) {
  try {
    // TODO: 从 Bitable 计算真实统计数据
    return {
      total: 23,
      byCategory: {
        "日语 N2 语法": 12,
        "日语 N2 词汇": 5,
        "软考架构师 UML": 4,
        "软考架构师 设计模式": 2
      },
      mastered: 8,
      pending: 15,
      recentWrong: [
        {
          "question_id": "jp_001",
          "category": "日语 N2 语法",
          "wrong_time": "3 月 26 日"
        },
        {
          "question_id": "rk_001",
          "category": "软考架构师 UML",
          "wrong_time": "3 月 26 日"
        }
      ]
    };
    
  } catch (error) {
    console.error('[Get Stats] Error:', error);
    return null;
  }
}

/**
 * 格式化错题列表消息
 */
function formatWrongQuestionsList(wrongQuestions, userId) {
  if (wrongQuestions.length === 0) {
    return `🎉 太棒了！你还没有错题哦～\n\n继续保持，争取一直全对！💪`;
  }
  
  let message = `📝 **你的错题本**\n\n`;
  message += `总计错题：**${wrongQuestions.length}** 道\n\n`;
  message += `━━━━━━━━━━━━━━━━━━━\n\n`;
  
  wrongQuestions.forEach((q, index) => {
    message += `${index + 1}. **【${q.category}】** ${q.knowledge_point}\n`;
    message += `   题目：${q.question_text.substring(0, 50)}...\n`;
    message += `   你的答案：${q.user_answer} ❌ | 正确答案：${q.correct_answer} ✅\n`;
    message += `   答错时间：${new Date(q.wrong_time).toLocaleDateString('zh-CN')}\n`;
    message += `   复习次数：${q.review_count} | 掌握状态：${q.mastered ? '✅' : '⏳'}\n\n`;
  });
  
  message += `━━━━━━━━━━━━━━━━━━━\n\n`;
  message += `💡 **操作建议**:\n`;
  message += `• 回复 **"复习错题"** 随机抽取错题重做\n`;
  message += `• 回复 **"统计错题"** 查看错题分布\n`;
  message += `• 回复 **"标记掌握 jp_001"** 标记某道题已掌握\n`;
  
  return message;
}

module.exports = {
  handleWrongQuestions,
  recordWrongAnswer,
  getUserWrongQuestions,
  markQuestionAsMastered,
  getWrongQuestionStats,
  formatWrongQuestionsList
};
