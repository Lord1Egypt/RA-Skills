/**
 * 模块3: 本地去重 + 模块4: LLM信息提取
 */

const fs = require('fs');
const path = require('path');

// 历史记录文件
const HISTORY_FILE = path.join(__dirname, '../data/history.csv');

// 读取历史记录
const loadHistory = () => {
  try {
    if (fs.existsSync(HISTORY_FILE)) {
      const content = fs.readFileSync(HISTORY_FILE, 'utf-8');
      const lines = content.split('\n').filter(l => l.trim());
      // 返回第一列（noteId）集合
      return new Set(lines.slice(1).map(l => l.split(',')[0]));
    }
  } catch (e) {
    console.log('读取历史记录失败:', e.message);
  }
  return new Set();
};

// 保存到历史记录
const saveToHistory = (notes) => {
  const timestamp = new Date().toISOString();
  let content = '';
  
  if (fs.existsSync(HISTORY_FILE)) {
    content = fs.readFileSync(HISTORY_FILE, 'utf-8');
  } else {
    content = 'noteId,accountName,fetchTime,title\n';
  }
  
  notes.forEach(n => {
    content += `${n.noteId},${n.accountName},${timestamp},"${n.text.split('\n')[0]}"\n`;
  });
  
  fs.writeFileSync(HISTORY_FILE, content);
};

// 去重
const deduplicate = (notes, history) => {
  const newNotes = [];
  const duplicateNotes = [];
  
  notes.forEach(n => {
    if (history.has(n.noteId)) {
      duplicateNotes.push(n);
    } else {
      newNotes.push(n);
    }
  });
  
  return { newNotes, duplicateNotes };
};

module.exports = { loadHistory, saveToHistory, deduplicate };
