/**
 * 超能力 CN - 示例：待办事项工作流
 * 
 * 演示如何使用超能力CN框架完成一个项目
 */

import { generateClarifyQuestions } from './clarify.js';
import { generatePlan, breakIntoTasks } from './plan.js';
import { executePlan } from './execute.js';
import { generateReviewReport } from './review.js';

/**
 * 示例：开发一个待办事项CLI工具
 */
async function demoTodoApp() {
  console.log('=== 超能力 CN 工作流演示 ===\n');
  
  // 阶段1: 澄清
  console.log('【阶段1: 澄清】');
  const userRequest = '做一个待办事项CLI工具';
  const questions = generateClarifyQuestions(userRequest);
  console.log(questions);
  
  // 模拟用户回答后的需求
  const requirement = {
    goal: '命令行待办事项管理工具',
    scope: ['添加任务', '查看任务列表', '完成任务', '删除任务'],
    constraints: ['Node.js环境', '简单易用', '数据存储在本地JSON文件']
  };
  
  // 阶段2: 设计
  console.log('\n【阶段2: 设计】');
  const plan = generatePlan(requirement);
  console.log(plan);
  
  // 模拟用户确认
  console.log('\n> 用户确认方案，开始执行...\n');
  
  // 阶段3: 执行
  console.log('【阶段3: 执行】');
  const tasks = breakIntoTasks(plan);
  const result = await executePlan(tasks, async (task) => {
    // 模拟执行和验证
    await new Promise(r => setTimeout(r, 100));
    return { success: true };
  });
  
  // 阶段4: 审核
  console.log('\n【阶段4: 审核】');
  const report = generateReviewReport(result, requirement);
  console.log(report);
}

// 运行演示
demoTodoApp().catch(console.error);
