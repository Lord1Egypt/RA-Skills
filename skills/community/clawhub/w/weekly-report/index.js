// weekly-report 周报生成器
const fs = require('fs');
const path = require('path');

const SKILL_DIR = __dirname;

// 数据文件路径
const FILES = {
  tasks: path.join(SKILL_DIR, 'tasks.json'),
  reports: path.join(SKILL_DIR, 'reports.json')
};

// 初始化数据文件
function initFiles() {
  for (const [key, filePath] of Object.entries(FILES)) {
    if (!fs.existsSync(filePath)) {
      fs.writeFileSync(filePath, JSON.stringify(key === 'tasks' ? [] : {}, null, 2));
    }
  }
}

// 读取数据
function loadData(type) {
  try {
    const data = fs.readFileSync(FILES[type], 'utf-8');
    return JSON.parse(data);
  } catch {
    return type === 'tasks' ? [] : {};
  }
}

// 保存数据
function saveData(type, data) {
  fs.writeFileSync(FILES[type], JSON.stringify(data, null, 2));
}

// 获取本周开始和结束日期
function getWeekRange() {
  const now = new Date();
  const dayOfWeek = now.getDay();
  const monday = new Date(now);
  monday.setDate(now.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1));
  monday.setHours(0, 0, 0, 0);
  
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  sunday.setHours(23, 59, 59, 999);
  
  return {
    start: monday.toLocaleDateString('zh-CN'),
    end: sunday.toLocaleDateString('zh-CN')
  };
}

// 获取上周开始和结束日期
function getLastWeekRange() {
  const now = new Date();
  const dayOfWeek = now.getDay();
  const monday = new Date(now);
  monday.setDate(now.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1) - 7);
  monday.setHours(0, 0, 0, 0);
  
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  sunday.setHours(23, 59, 59, 999);
  
  return {
    start: monday.toLocaleDateString('zh-CN'),
    end: sunday.toLocaleDateString('zh-CN')
  };
}

module.exports = {
  name: 'weekly-report',
  description: '周报生成器，自动汇总本周工作',
  version: '1.0.0',
  author: '黄豆豆',
  
  // 激活条件
  activate(message) {
    const keywords = ['周报', '总结', '本周', '上周'];
    return keywords.some(k => message.includes(k));
  },
  
  async handle(context) {
    const message = context.message || '';
    const lowerMessage = message.toLowerCase();
    
    initFiles();
    
    // 添加任务
    if (lowerMessage.includes('添加任务') || lowerMessage.includes('完成')) {
      return this.addTask(message);
    }
    
    // 生成周报
    if (lowerMessage.includes('周报') || lowerMessage.includes('总结')) {
      return this.generateReport(message);
    }
    
    // 查看任务
    if (lowerMessage.includes('任务列表') || lowerMessage.includes('查看任务')) {
      return this.listTasks();
    }
    
    // 默认显示帮助
    return this.showHelp();
  },
  
  addTask(message) {
    const tasks = loadData('tasks');
    const taskText = message.replace(/添加任务/i, '').replace(/完成/i, '').trim();
    
    if (!taskText) {
      return { message: '请输入任务内容，例如：添加任务 完成项目设计' };
    }
    
    const task = {
      id: Date.now(),
      text: taskText,
      completed: lowerMessage.includes('完成'),
      created: new Date().toISOString()
    };
    
    tasks.push(task);
    saveData('tasks', tasks);
    
    return {
      success: true,
      message: `✅ 任务已添加：${taskText}`
    };
  },
  
  generateReport(message) {
    const tasks = loadData('tasks');
    const reports = loadData('reports');
    const weekRange = getWeekRange();
    const lastWeekRange = getLastWeekRange();
    
    // 筛选本周任务
    const thisWeekTasks = tasks.filter(t => {
      const created = new Date(t.created);
      const now = new Date();
      const dayOfWeek = now.getDay();
      const monday = new Date(now);
      monday.setDate(now.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1));
      monday.setHours(0, 0, 0, 0);
      return created >= monday;
    });
    
    const completedTasks = thisWeekTasks.filter(t => t.completed);
    const pendingTasks = thisWeekTasks.filter(t => !t.completed);
    
    const report = {
      id: Date.now(),
      week: weekRange,
      completed: completedTasks.length,
      pending: pendingTasks.length,
      generated: new Date().toISOString()
    };
    
    // 保存报告
    const reportKey = `${weekRange.start}-${weekRange.end}`;
    reports[reportKey] = report;
    saveData('reports', reports);
    
    // 生成周报内容
    let reportContent = `# 📊 周报 (${weekRange.start} - ${weekRange.end})

## 📈 数据概览
- ✅ 完成任务：${completedTasks.length} 个
- ⏳ 进行中：${pendingTasks.length} 个
- 📝 总任务数：${thisWeekTasks.length} 个

---

## ✅ 本周完成

${completedTasks.length > 0 ? completedTasks.map((t, i) => `${i + 1}. ${t.text}`).join('\n') : '暂无完成的任务'}

---

## ⏳ 进行中

${pendingTasks.length > 0 ? pendingTasks.map((t, i) => `${i + 1}. ${t.text}`).join('\n') : '暂无进行中的任务'}

---

## 🎯 下周计划

- [待添加]

---

## 💡 备注

- [如有需要添加]

---
*由黄豆豆自动生成 | ${new Date().toLocaleString('zh-CN')}*`;
    
    return { message: reportContent };
  },
  
  listTasks() {
    const tasks = loadData('tasks');
    
    if (tasks.length === 0) {
      return { message: '暂无任务\n\n输入"添加任务 xxx"添加任务\n输入"完成 xxx"标记任务完成' };
    }
    
    let msg = '📝 任务列表：\n\n';
    
    tasks.forEach((t, i) => {
      const status = t.completed ? '✅' : '⏳';
      msg += `${i + 1}. ${status} ${t.text}\n`;
    });
    
    return { message: msg };
  },
  
  showHelp() {
    return {
      message: `📋 周报生成器使用方法：

1. 添加任务：添加任务 [任务内容]
2. 标记完成：完成 [任务内容]  
3. 生成周报：生成周报 / 周报 / 本周总结
4. 查看任务：查看任务 / 任务列表

示例：
- 添加任务 完成项目设计
- 添加任务 编写代码
- 生成周报`
    };
  }
};
