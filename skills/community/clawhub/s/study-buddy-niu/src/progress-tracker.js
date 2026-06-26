/**
 * Study Buddy - 学习进度追踪
 * 功能：统计答题数量、正确率、学习时长
 */

const { listRecords, createRecord } = require('./bitable-client.js');

// 进度表配置（待创建）
const PROGRESS_TABLE_ID = "tbl_progress"; // TODO: 创建后替换实际 ID

// 内存缓存（简化版，生产环境应该用数据库）
const userProgressCache = new Map();

/**
 * 处理查看进度请求
 * @param {string} userText - 用户输入
 * @param {string} userId - 用户 ID
 * @param {Object} config - 配置信息
 * @returns {Promise<Object>} 回复对象
 */
async function handleProgress(userText, userId, config) {
  try {
    // 获取用户进度统计
    const stats = await getUserProgressStats(userId, config);
    
    // 格式化并返回
    return {
      text: formatProgressMessage(stats, userId)
    };
    
  } catch (error) {
    console.error('[Progress Tracker] Error:', error);
    return {
      text: `😅 查看进度时出现错误：${error.message}`
    };
  }
}

/**
 * 记录学习进度
 * @param {string} userId - 用户 ID
 * @param {number} totalQuestions - 今日答题总数
 * @param {number} correctQuestions - 今日答对数量
 * @param {Object} config - 配置信息
 * @returns {Promise<void>}
 */
async function logProgress(userId, totalQuestions, correctQuestions, config) {
  try {
    const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
    
    // 更新缓存
    if (!userProgressCache.has(userId)) {
      userProgressCache.set(userId, {
        totalQuestions: 0,
        correctQuestions: 0,
        lastStudyDate: today,
        studyStreak: 0
      });
    }
    
    const userStats = userProgressCache.get(userId);
    userStats.totalQuestions += totalQuestions;
    userStats.correctQuestions += correctQuestions;
    userStats.lastStudyDate = today;
    
    // TODO: 写入 Bitable 进度表
    /*
    await createRecord(
      config.BITABLE_APP_TOKEN,
      PROGRESS_TABLE_ID,
      {
        "user_id": userId,
        "date": today,
        "total_questions": totalQuestions,
        "correct_questions": correctQuestions,
        "accuracy_rate": Math.round((correctQuestions / totalQuestions) * 100) || 0,
        "study_duration": 0, // TODO: 记录实际学习时长
        "jp_category": "",
        "rk_category": "",
        "notes": ""
      }
    );
    */
    
    console.log(`[Progress] User ${userId}: Total=${userStats.totalQuestions}, Correct=${userStats.correctQuestions}`);
    
  } catch (error) {
    console.error('[Log Progress] Error:', error);
    // 不抛出错误
  }
}

/**
 * 获取用户进度统计
 * @param {string} userId - 用户 ID
 * @param {Object} config - 配置信息
 * @returns {Promise<Object>} 统计信息
 */
async function getUserProgressStats(userId, config) {
  try {
    // 从缓存或数据库获取数据
    const cachedStats = userProgressCache.get(userId) || {
      totalQuestions: 4,
      correctQuestions: 3,
      lastStudyDate: new Date().toISOString().split('T')[0],
      studyStreak: 1
    };
    
    // 计算正确率
    const accuracyRate = cachedStats.totalQuestions > 0 
      ? Math.round((cachedStats.correctQuestions / cachedStats.totalQuestions) * 100) 
      : 0;
    
    // 按分类统计（模拟数据）
    const byCategory = {
      "日语 N2 语法": { total: 2, correct: 2 },
      "日语 N2 词汇": { total: 0, correct: 0 },
      "软考架构师 UML": { total: 1, correct: 1 },
      "软考架构师 设计模式": { total: 1, correct: 0 }
    };
    
    // 最近学习记录（模拟数据）
    const recentDays = [
      {
        date: "2026-03-27",
        totalQuestions: 4,
        correctQuestions: 3,
        accuracyRate: 75
      }
    ];
    
    return {
      ...cachedStats,
      accuracyRate,
      byCategory,
      recentDays
    };
    
  } catch (error) {
    console.error('[Get Progress Stats] Error:', error);
    return null;
  }
}

/**
 * 获取连续学习天数
 */
function calculateStudyStreak(userId, studyDates) {
  // TODO: 实现连续学习天数计算逻辑
  return 1; // 简化版返回 1
}

/**
 * 格式化进度消息
 */
function formatProgressMessage(stats, userId) {
  if (!stats) {
    return `😅 暂时无法获取进度数据，请稍后再试。`;
  }
  
  let message = `📊 **你的学习进度**\n\n`;
  message += `━━━━━━━━━━━━━━━━━━━\n\n`;
  
  message += `🎯 **总体统计**:\n`;
  message += `• 总答题数：**${stats.totalQuestions}** 道\n`;
  message += `• 答对数量：**${stats.correctQuestions}** 道\n`;
  message += `• 正确率：**${stats.accuracyRate}%** ${getAccuracyEmoji(stats.accuracyRate)}\n`;
  message += `• 连续学习：**${stats.studyStreak}** 天 🔥\n`;
  message += `• 最后学习：${stats.lastStudyDate}\n\n`;
  
  message += `━━━━━━━━━━━━━━━━━━━\n\n`;
  
  message += `📚 **按分类统计**:\n`;
  for (const [category, data] of Object.entries(stats.byCategory)) {
    const rate = data.total > 0 ? Math.round((data.correct / data.total) * 100) : 0;
    message += `• ${category}: ${data.correct}/${data.total} (${rate}%)\n`;
  }
  
  message += `\n━━━━━━━━━━━━━━━━━━━\n\n`;
  
  message += `📈 **最近学习记录**:\n`;
  stats.recentDays.forEach(day => {
    message += `• ${day.date}: ${day.totalQuestions}题，正确率 ${day.accuracyRate}%\n`;
  });
  
  message += `\n━━━━━━━━━━━━━━━━━━━\n\n`;
  
  message += `${getProgressEncouragement(stats.accuracyRate, stats.studyStreak)}\n\n`;
  
  message += `💡 **下一步建议**:\n`;
  if (stats.accuracyRate < 60) {
    message += `• 基础还不够牢固，建议多刷基础题\n`;
    message += `• 重点复习错题本中的题目\n`;
  } else if (stats.accuracyRate < 80) {
    message += `• 表现不错！继续保持～\n`;
    message += `• 可以尝试增加难度，挑战困难题\n`;
  } else {
    message += `• 太棒了！你已经掌握得很好了！🎉\n`;
    message += `• 建议进行模拟考试，适应考试节奏\n`;
  }
  
  message += `\n继续加油！回复 **"来一道题"** 开始下一轮练习吧！💪`;
  
  return message;
}

/**
 * 根据正确率返回表情符号
 */
function getAccuracyEmoji(rate) {
  if (rate >= 90) return '🏆';
  if (rate >= 80) return '🌟';
  if (rate >= 70) return '👍';
  if (rate >= 60) return '😊';
  return '💪';
}

/**
 * 获取鼓励话语
 */
function getProgressEncouragement(accuracyRate, streak) {
  if (streak >= 7) {
    return `🔥 已经连续学习 ${streak} 天了！坚持就是胜利！`;
  }
  
  if (accuracyRate >= 80) {
    return `🎉 正确率很高！继续保持这个状态！`;
  } else if (accuracyRate >= 60) {
    return `👍 表现不错！每天进步一点点！`;
  } else {
    return `💪 别灰心！每道错题都是进步的机会！`;
  }
}

module.exports = {
  handleProgress,
  logProgress,
  getUserProgressStats,
  calculateStudyStreak,
  formatProgressMessage,
  getAccuracyEmoji,
  getProgressEncouragement
};
