/**
 * Study Buddy - 学习计划生成器
 * 功能：根据考试日期生成每日学习任务
 */

/**
 * 处理学习计划请求
 * @param {string} userText - 用户输入
 * @param {string} userId - 用户 ID
 * @param {Object} config - 配置信息
 * @returns {Promise<Object>} 回复对象
 */
async function handleSchedule(userText, userId, config) {
  try {
    // 1. 解析用户输入的考试日期或剩余天数
    const examInfo = parseExamDate(userText);
    
    // 2. 生成学习计划
    const plan = generateDailyPlan(examInfo);
    
    // 3. 格式化并返回计划
    return {
      text: formatPlanMessage(plan, examInfo)
    };
    
  } catch (error) {
    console.error('[Schedule Generator] Error:', error);
    return {
      text: `😅 生成计划时出现错误：${error.message}\n\n请告诉我考试日期，例如："距离考试还有 90 天"`
    };
  }
}

/**
 * 生成详细的学习计划
 * @param {Object} examInfo - 考试信息 {daysRemaining, examDate}
 * @returns {Object} 学习计划对象
 */
function generatePlan(examInfo) {
  const daysRemaining = examInfo.daysRemaining || 90; // 默认 90 天
  
  // 计算总学习量分配
  const totalStudyDays = daysRemaining;
  const japaneseRatio = 0.5; // 日语占 50%
  const softwareArchRatio = 0.5; // 软考占 50%
  
  // 生成今日计划
  const todayPlan = {
    date: new Date().toLocaleDateString('zh-CN'),
    japanese: {
      duration: 45, // 分钟
      tasks: [
        "语法练习：10 道题",
        "单词复习：20 个"
      ],
      focus: "N2 语法重点：～あげく、～とはいえ"
    },
    softwareArch: {
      duration: 60, // 分钟
      tasks: [
        "真题练习：15 道选择题",
        "知识点复习：UML 图"
      ],
      focus: "UML 类图、序列图、用例图"
    },
    review: {
      duration: 15,
      tasks: [
        "复习昨日错题",
        "总结今日学习"
      ]
    }
  };
  
  // 生成阶段规划
  const phases = generateStudyPhases(daysRemaining);
  
  return {
    today: todayPlan,
    phases: phases,
    tips: getStudyTips(daysRemaining)
  };
}

/**
 * 解析用户输入的考试日期
 */
function parseExamDate(text) {
  const lowerText = text.toLowerCase();
  
  // 尝试提取"距离考试还有 X 天"
  const daysMatch = text.match(/还[有|剩](\d+)[天|日]/);
  if (daysMatch) {
    const days = parseInt(daysMatch[1]);
    const examDate = new Date();
    examDate.setDate(examDate.getDate() + days);
    
    return {
      daysRemaining: days,
      examDate: examDate,
      examDateStr: examDate.toLocaleDateString('zh-CN')
    };
  }
  
  // 尝试提取具体日期（如"2026 年 7 月 1 日"）
  const dateMatch = text.match(/(\d{4})[年\-/](\d{1,2})[月\-/](\d{1,2})[日]?/);
  if (dateMatch) {
    const year = parseInt(dateMatch[1]);
    const month = parseInt(dateMatch[2]) - 1; // JS 月份从 0 开始
    const day = parseInt(dateMatch[3]);
    const examDate = new Date(year, month, day);
    
    const now = new Date();
    const diffTime = examDate - now;
    const daysRemaining = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    return {
      daysRemaining: daysRemaining > 0 ? daysRemaining : 0,
      examDate: examDate,
      examDateStr: examDate.toLocaleDateString('zh-CN')
    };
  }
  
  // 默认返回 90 天
  const examDate = new Date();
  examDate.setDate(examDate.getDate() + 90);
  
  return {
    daysRemaining: 90,
    examDate: examDate,
    examDateStr: examDate.toLocaleDateString('zh-CN')
  };
}

/**
 * 生成每日学习计划
 */
function generateDailyPlan(examInfo) {
  return {
    date: new Date().toLocaleDateString('zh-CN'),
    totalDuration: 120, // 总计 120 分钟
    japanese: {
      duration: 45,
      tasks: [
        "语法练习：10 道题（重点：～あげく、～とはいえ）",
        "单词复习：20 个（List 15-16）"
      ]
    },
    softwareArch: {
      duration: 60,
      tasks: [
        "真题练习：15 道选择题（知识点：UML、设计模式）",
        "案例分析：1 道（2024 年真题）"
      ]
    },
    review: {
      duration: 15,
      tasks: [
        "整理今日错题",
        "回顾薄弱环节"
      ]
    }
  };
}

/**
 * 生成阶段性学习规划
 */
function generateStudyPhases(totalDays) {
  const phase1Days = Math.floor(totalDays * 0.4); // 40% 基础阶段
  const phase2Days = Math.floor(totalDays * 0.4); // 40% 强化阶段
  const phase3Days = totalDays - phase1Days - phase2Days; // 20% 冲刺阶段
  
  return [
    {
      name: "基础阶段",
      days: `第 1-${phase1Days}天`,
      focus: "系统学习基础知识，建立知识框架",
      japanese: "完成 N2 所有语法点学习，掌握核心词汇",
      softwareArch: "熟悉 UML、设计模式、软件架构基础"
    },
    {
      name: "强化阶段",
      days: `第${phase1Days + 1}-${phase1Days + phase2Days}天`,
      focus: "大量刷题，巩固知识点",
      japanese: "每日 20 道语法题 + 20 个单词，重点突破薄弱环节",
      softwareArch: "每日 20 道选择题 + 1 道案例分析，查漏补缺"
    },
    {
      name: "冲刺阶段",
      days: `最后${phase3Days}天`,
      focus: "模拟考试，调整状态",
      japanese: "全套模拟题训练，控制答题时间",
      softwareArch: "历年真题模拟，适应考试节奏"
    }
  ];
}

/**
 * 获取学习建议
 */
function getStudyTips(daysRemaining) {
  if (daysRemaining > 180) {
    return "⏰ 时间充裕，建议稳扎稳打，不要急于求成。每天坚持学习，积少成多！";
  } else if (daysRemaining > 90) {
    return "⏰ 时间适中，按计划推进，注意劳逸结合。每周可以休息半天调整状态。";
  } else if (daysRemaining > 30) {
    return "⚠️ 进入关键期！加大学习强度，重点突破薄弱环节。减少娱乐时间，全力备考！";
  } else {
    return "🔥 冲刺阶段！保持状态，调整作息，保证睡眠。相信自己，一定可以的！💪";
  }
}

/**
 * 格式化学习计划消息
 */
function formatPlanMessage(plan, examInfo) {
  const today = plan.today;
  
  let message = `📅 **今日学习计划**（${today.date}）\n\n`;
  
  message += `━━━━━━━━━━━━━━━━━━━\n\n`;
  
  if (examInfo.examDateStr) {
    message += `🎯 **距离考试**: ${examInfo.daysRemaining}天（${examInfo.examDateStr}）\n\n`;
  }
  
  message += `【日语 N2】⏰ 预计 ${today.japanese.duration} 分钟\n`;
  today.japanese.tasks.forEach(task => {
    message += `• ${task}\n`;
  });
  message += `重点：${today.japanese.focus}\n\n`;
  
  message += `【软考架构师】⏰ 预计 ${today.softwareArch.duration} 分钟\n`;
  today.softwareArch.tasks.forEach(task => {
    message += `• ${task}\n`;
  });
  message += `重点：${today.softwareArch.focus}\n\n`;
  
  message += `【复习总结】⏰ 预计 ${today.review.duration} 分钟\n`;
  today.review.tasks.forEach(task => {
    message += `• ${task}\n`;
  });
  
  message += `\n━━━━━━━━━━━━━━━━━━━\n\n`;
  
  message += `💡 **今日目标**:\n`;
  message += `• 完成上述所有任务\n`;
  message += `• 正确率达到 75% 以上\n`;
  message += `• 错题整理到错题本\n\n`;
  
  message += `${plan.tips}\n\n`;
  
  message += `━━━━━━━━━━━━━━━━━━━\n\n`;
  message += `准备好了吗？\n`;
  message += `• 回复 **"开始学习"** 进入第一题\n`;
  message += `• 回复 **"来一道 N2 语法题"** 开始日语练习\n`;
  message += `• 回复 **"来一道软考题"** 开始软考练习\n`;
  
  return message;
}

module.exports = {
  handleSchedule,
  generatePlan,
  generateDailyPlan,
  parseExamDate,
  formatPlanMessage
};
