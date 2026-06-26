/**
 * 超能力 CN - 执行阶段
 * 
 * 按计划逐步执行任务
 */

/**
 * 执行单个任务步骤
 * @param {object} task - 任务对象
 * @param {function} verifyFn - 验证函数
 */
export async function executeStep(task, verifyFn) {
  console.log(`[执行] 步骤 ${task.step}: ${task.task}`);
  
  try {
    // 执行任务
    await task.execute();
    
    // 验证结果
    const result = await verifyFn(task);
    
    if (result.success) {
      task.status = 'completed';
      console.log(`[完成] 步骤 ${task.step}: ✓`);
    } else {
      task.status = 'failed';
      console.log(`[失败] 步骤 ${task.step}: ${result.error}`);
    }
    
    return result;
  } catch (error) {
    task.status = 'failed';
    console.error(`[错误] 步骤 ${task.step}:`, error.message);
    return { success: false, error: error.message };
  }
}

/**
 * 执行完整计划
 * @param {array} tasks - 任务列表
 * @param {function} verifyFn - 验证函数
 */
export async function executePlan(tasks, verifyFn) {
  const results = [];
  
  for (const task of tasks) {
    const result = await executeStep(task, verifyFn);
    results.push(result);
    
    if (!result.success) {
      console.log('[警告] 任务失败，停止执行');
      break;
    }
  }
  
  return {
    completed: tasks.filter(t => t.status === 'completed').length,
    failed: tasks.filter(t => t.status === 'failed').length,
    results
  };
}
