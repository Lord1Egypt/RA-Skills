/**
 * Study Buddy - 双轨学习助手
 * 主入口文件
 * 
 * 功能：日语 N2 + 软考架构师备考助手
 * 比赛：OPC 极限挑战赛（上海站）
 */

// 配置信息
const CONFIG = {
  BITABLE_APP_TOKEN: "SoZ5bkTBOa3LQisZHO1cAQuknDh",
  BITABLE_TABLE_ID: "tbl0TEk3P0GCqR2p",
  VERSION: "1.0.0"
};

// 导入子模块 - 🚀 使用 v2.0 批量出题引擎
const questionEngine = require('./question-engine-v2.js');
const { handleQuestion, handleUserAnswer } = questionEngine;
const { handleSchedule, generatePlan } = require('./schedule-gen.js');
const { handleWrongQuestions, recordWrongAnswer } = require('./wrong-answers.js');
const { handleProgress, logProgress } = require('./progress-tracker.js');

// 🚀 全局缓存对象（用于答案识别）
global.answerSessions = questionEngine.answerSessions || new Map();
global.questionCache = questionEngine.questionCache || new Map();

/**
 * 处理用户消息的主函数
 * @param {Object} message - 消息对象 {text, userId, timestamp, replyToId}
 * @param {Object} context - 上下文对象 {channel, sessionId, etc.}
 * @returns {Promise<Object>} 回复对象 {text, type, etc.}
 */
export async function handleMessage(message, context) {
  try {
    const text = (message.text || "").trim();
    const lowerText = text.toLowerCase();
    
    // 记录用户 ID（用于错题本和进度追踪）
    const userId = context.userId || message.userId || "default_user";
    
    // 🚀 优化 1: 优先检查是否是答案（A/B/C/D）
    // 如果用户正在答题中，且输入是单个字母 A/B/C/D，则判定为答案
    if (isAnswerInput(text, userId)) {
      const sessionId = userId; // 简化：用 userId 作为 sessionId
      return await handleUserAnswer(text, sessionId, userId, CONFIG);
    }
    
    // 2. 帮助菜单
    if (lowerText.includes('帮助') || lowerText.includes('怎么用') || lowerText.includes('你能做什么')) {
      return showHelpMenu();
    }
    
    // 3. 出题请求
    if (lowerText.includes('来一道') || lowerText.includes('来一题') || 
        lowerText.includes('练习题') || lowerText.includes('做题') ||
        lowerText.includes('刷题') || lowerText.includes('语法题') ||
        lowerText.includes('词汇题') || lowerText.includes('选择题')) {
      
      return await handleQuestion(text, userId, CONFIG);
    }
    
    // 4. 模拟考试
    if (lowerText.includes('模拟考') || lowerText.includes('模拟考试') || lowerText.includes('测试')) {
      return await handleMockExam(text, userId, CONFIG);
    }
    
    // 5. 学习计划
    if (lowerText.includes('计划') || lowerText.includes('今日学什么') || 
        lowerText.includes('复习计划') || lowerText.includes('备考计划') ||
        lowerText.includes('距离考试')) {
      
      return await handleSchedule(text, userId, CONFIG);
    }
    
    // 6. 错题本
    if (lowerText.includes('错题') || lowerText.includes('我错的题')) {
      return await handleWrongQuestions(text, userId, CONFIG);
    }
    
    // 7. 进度统计
    if (lowerText.includes('进度') || lowerText.includes('统计') || 
        lowerText.includes('正确率')) {
      
      return await handleProgress(text, userId, CONFIG);
    }
    
    // 8. 默认回复（引导用户使用）
    return {
      text: `👋 你好！我是 **Study Buddy**，你的双轨学习助手！📚

我可以帮你：
📖 **出题练习** - 说"来一道 N2 语法题"或"来一道软考题"
📝 **模拟考试** - 说"开始模拟考"
📅 **学习计划** - 说"生成今日学习计划"
📊 **查看错题** - 说"查看我的错题本"
📈 **学习进度** - 说"查看我的进度"

💡 试试对我说："来一道 N2 语法题" 吧！

---
*Study Buddy v${CONFIG.VERSION} | OPC 极限挑战赛作品*`
    };
    
  } catch (error) {
    console.error('[Study Buddy] Error:', error);
    return {
      text: `😅 抱歉，出现了一些问题：${error.message}\n\n请稍后再试，或联系开发者。`
    };
  }
}

/**
 * 🚀 优化 2: 判断输入是否是答案（A/B/C/D）
 * @param {string} text - 用户输入
 * @param {string} userId - 用户 ID
 * @returns {boolean} 是否是答案
 */
function isAnswerInput(text, userId) {
  const trimmed = text.trim().toUpperCase();
  
  // 🚀 优化 A: 必须是单个字母 A/B/C/D（排除"继续"、"来一道"等指令）
  if (!/^[ABCD]$/.test(trimmed)) {
    return false;
  }
  
  // 🚀 优化 B: 检查该用户是否正在答题中
  const sessions = global.answerSessions;
  if (!sessions) {
    return false;
  }
  
  const hasActiveSession = sessions.has(userId);
  
  // 调试日志
  if (hasActiveSession) {
    console.log(`[Answer Detection] User ${userId} is answering, session exists.`);
  } else {
    console.log(`[Answer Detection] User ${userId} sent "${text}" but no active session.`);
  }
  
  return hasActiveSession;
}

/**
 * 显示帮助菜单
 */
function showHelpMenu() {
  return {
    text: `📖 **Study Buddy 使用指南**

━━━━━━━━━━━━━━━━━━━

🎯 **核心功能**

1️⃣ **智能出题**
   • "来一道 N2 语法题"
   • "来一道软考架构师的 UML 题目"
   • "来一道 N2 词汇题，难度困难"

2️⃣ **模拟考试**
   • "开始 N2 模拟考"
   • "软考模拟考，15 道题"

3️⃣ **学习计划**
   • "生成今日学习计划"
   • "距离考试还有 90 天，帮我制定计划"

4️⃣ **错题本**
   • "查看我的错题"
   • "我错了几道题了？"

5️⃣ **进度统计**
   • "查看我的学习进度"
   • "我的正确率是多少？"

━━━━━━━━━━━━━━━━━━━

📊 **当前配置**
• 题库：日语 N2 + 软考架构师
• 存储：飞书 Bitable
• 版本：v${CONFIG.VERSION}

━━━━━━━━━━━━━━━━━━━

💡 **小贴士**
• 答错的题会自动记录到错题本
• 每天坚持学习，进步看得见！
• 可以随时查看进度调整学习计划

准备好了吗？试试说 **"来一道 N2 语法题"** 开始学习吧！💪

---
*Study Buddy - 让备考更高效！*`
  };
}

// 导出其他需要暴露的函数
module.exports = {
  handleMessage,
  showHelpMenu,
  CONFIG
};
