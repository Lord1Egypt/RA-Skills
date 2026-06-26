/**
 * 超能力 CN - 计划阶段
 * 
 * 制定详细执行计划，等待确认后执行
 */

/**
 * 生成设计方案
 * @param {object} requirement - 经过澄清的需求
 * @returns {string} 设计方案文档
 */
export function generatePlan(requirement) {
  const { goal, constraints, scope } = requirement;
  
  return `
## 📋 设计方案

### 目标
${goal}

### 文件结构
\`\`\`
项目目录/
├── src/
│   └── ...
├── tests/
├── README.md
└── package.json
\`\`\`

### 核心模块
${scope.map((s, i) => `${i + 1}. ${s}`).join('\n')}

### 实现步骤
1. 初始化项目结构
2. 实现核心功能
3. 编写测试
4. 文档编写

### 限制条件
${constraints.map((c, i) => `- ${c}`).join('\n')}

### 风险点
- 需要确认的风险项

---

**请确认设计方案，我可以开始执行吗？**
  `.trim();
}

/**
 * 分解任务为小步骤
 * @param {string} plan - 确认的设计方案
 * @returns {array} 任务步骤列表
 */
export function breakIntoTasks(plan) {
  return [
    { step: 1, task: '初始化项目结构', status: 'pending' },
    { step: 2, task: '实现核心功能', status: 'pending' },
    { step: 3, task: '编写测试', status: 'pending' },
    { step: 4, task: '完成文档', status: 'pending' }
  ];
}
