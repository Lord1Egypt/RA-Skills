/**
 * 学分查询技能 - OpenClaw Skill
 * 用于查询学生各科目成绩
 */

const fs = require('fs');
const path = require('path');

// 数据库路径
const DB_PATH = path.join(__dirname, 'database', 'scores.json');

// 加载数据库
function loadDatabase() {
  try {
    const data = fs.readFileSync(DB_PATH, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error('加载数据库失败:', error);
    return { students: [] };
  }
}

// 解析用户查询，提取姓名和科目
function parseQuery(query) {
  const result = {
    name: null,
    subject: null
  };
  
  const db = loadDatabase();
  const students = db.students;
  
  // 提取姓名 - 在数据库中查找匹配的学生名
  for (const student of students) {
    if (query.includes(student.name)) {
      result.name = student.name;
      break;
    }
  }
  
  // 科目映射 (口语化表达 -> 标准科目)
  const subjectMapping = {
    '语言': '语文',
    '国文': '语文',
    '中文': '语文',
    '代数': '数学',
    '几何': '数学',
    '英文': '英语',
    '美语': '英语',
    '物理': '物理',
    '化学': '化学',
    '生物': '生物',
    '历史': '历史',
    '地理': '地理',
    '政治': '政治'
  };
  
  // 提取科目
  for (const [colloquial, standard] of Object.entries(subjectMapping)) {
    if (query.includes(colloquial)) {
      result.subject = standard;
      break;
    }
  }
  
  // 如果没找到口语化科目，尝试直接匹配标准科目
  if (!result.subject) {
    const standardSubjects = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治'];
    for (const subject of standardSubjects) {
      if (query.includes(subject)) {
        result.subject = subject;
        break;
      }
    }
  }
  
  return result;
}

// 查询单科成绩
function queryScore(name, subject) {
  const db = loadDatabase();
  const student = db.students.find(s => s.name === name);
  
  if (!student) {
    return null;
  }
  
  if (subject) {
    const score = student.scores[subject];
    return score !== undefined ? score : null;
  }
  
  return student.scores;
}

// 处理查询请求
function handleQuery(query) {
  console.log('收到查询:', query);
  
  const { name, subject } = parseQuery(query);
  
  // 检查是否找到姓名
  if (!name) {
    return {
      success: false,
      message: '抱歉，我没有找到您的信息。请检查姓名是否正确。',
      type: 'error'
    };
  }
  
  // 查询成绩
  const scores = queryScore(name, subject);
  
  if (scores === null) {
    return {
      success: false,
      message: `抱歉，${name}的${subject}成绩暂未记录。`,
      type: 'error'
    };
  }
  
  // 返回单科成绩
  if (subject) {
    return {
      success: true,
      message: `${name}的${subject}成绩是：${scores}分`,
      data: { name, subject, score: scores }
    };
  }
  
  // 返回全部成绩
  const scoreList = Object.entries(scores)
    .map(([sub, score]) => `${sub}: ${score}分`)
    .join('，');
  
  return {
    success: true,
    message: `${name}的全部成绩如下：${scoreList}`,
    data: { name, scores }
  };
}

// OpenClaw Skill 导出格式
module.exports = {
  // 技能元数据
  metadata: {
    name: '学分查询',
    version: '1.0.0',
    description: '查询学生各科目成绩'
  },
  
  /**
   * 处理用户查询 - 主入口函数
   * @param {Object} params - 参数对象
   * @param {string} params.query - 用户输入的查询
   * @param {Object} params.entities - 解析出的实体（可选）
   * @returns {Object} 查询结果
   */
  handler: function(params) {
    const query = params.query || '';
    
    // 如果传入了预解析的实体，优先使用
    if (params.entities && params.entities.name) {
      const { name, subject } = params.entities;
      const scores = queryScore(name, subject);
      
      if (scores === null) {
        return {
          success: false,
          message: `抱歉，${name}的${subject || '该科目'}成绩暂未记录。`
        };
      }
      
      if (subject) {
        return {
          success: true,
          message: `${name}的${subject}成绩是：${scores}分`,
          data: { name, subject, score: scores }
        };
      }
      
      const scoreList = Object.entries(scores)
        .map(([sub, score]) => `${sub}: ${score}分`)
        .join('，');
      
      return {
        success: true,
        message: `${name}的全部成绩如下：${scoreList}`,
        data: { name, scores }
      };
    }
    
    // 否则解析查询
    return handleQuery(query);
  },
  
  /**
   * 意图识别函数
   * @param {string} query - 用户输入
   * @returns {Object} 意图和实体
   */
  recognize: function(query) {
    const { name, subject } = parseQuery(query);
    
    if (!name) {
      return {
        intent: null,
        confidence: 0
      };
    }
    
    const intent = subject ? '查询成绩' : '查询全部成绩';
    
    return {
      intent: intent,
      confidence: 0.9,
      entities: { name, subject }
    };
  },
  
  // 技能配置
  config: {
    fuzzyMatch: true,
    caseSensitive: false
  }
};

// 如果直接运行此文件，进行测试
if (require.main === module) {
  console.log('=== 学分查询技能测试 ===\n');
  
  const testQueries = [
    '张三语言考了多少',
    '李四数学成绩是多少',
    '王五英语多少分',
    '张三全部成绩',
    '李四各科成绩'
  ];
  
  for (const q of testQueries) {
    console.log(`查询: ${q}`);
    const result = handleQuery(q);
    console.log(`结果: ${result.message}\n`);
  }
}
