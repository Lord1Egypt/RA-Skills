/**
 * 智能对话管理技能演示程序
 * 
 * 展示技能的核心功能：
 * 1. 对话状态监控
 * 2. 智能响应生成
 * 3. 进度汇报
 * 4. Token优化
 */

const DialogManager = require('../src/index');

// 模拟会话
const mockSession = {
  id: 'demo-session-' + Date.now(),
  type: 'direct',
  platform: 'qqbot',
  userId: 'demo-user',
  userName: '演示用户'
};

// 创建对话管理器实例
const dialogManager = new DialogManager();

/**
 * 演示1：基础监控功能
 */
async function demoBasicMonitoring() {
  console.log('🚀 演示1：基础监控功能\n');
  
  try {
    // 启动对话管理器
    await dialogManager.start(mockSession);
    console.log('✅ 对话管理器启动成功');
    
    // 显示当前状态
    const status = dialogManager.getStatus();
    console.log('📊 当前状态：', JSON.stringify(status, null, 2));
    
    // 等待3秒，模拟对话检查
    console.log('\n⏳ 等待3秒，模拟对话检查...');
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // 手动触发进度汇报
    console.log('\n📋 手动触发进度汇报：');
    await dialogManager.reportProgress({
      name: '数据分析任务',
      progress: 0.3,
      estimatedTime: '10分钟',
      status: 'working'
    });
    
  } catch (error) {
    console.error('❌ 演示失败：', error.message);
  }
}

/**
 * 演示2：意图识别和响应（使用修复后的Analyzer类）
 */
async function demoIntentRecognition() {
  console.log('\n\n🚀 演示2：意图识别和响应（修复后）\n');
  
  // 使用修复后的Analyzer类
  const Analyzer = require('../src/analyzer');
  
  // 模拟日志
  class MockLogger {
    debug() {}
    info() {}
    error() {}
  }
  
  // 创建分析器实例
  const config = {
    response_priority: {
      intent_mapping: {
        question: "p0",
        task_request: "p1",
        feedback: "p2",
        social: "p3"
      }
    }
  };
  
  const analyzer = new Analyzer(config.response_priority, new MockLogger());
  
  const testMessages = [
    { content: '你好，最近怎么样？', expectedIntent: 'social' },
    { content: '什么是人工智能？', expectedIntent: 'question' },
    { content: '帮我分析一下数据', expectedIntent: 'task_request' },
    { content: '谢谢你的帮助', expectedIntent: 'feedback' },
    { content: '这个功能很好用', expectedIntent: 'feedback' }
  ];
  
  let correctCount = 0;
  
  for (const test of testMessages) {
    console.log(`\n📝 测试消息：${test.content}`);
    
    // 使用修复后的Analyzer类
    const intent = analyzer.analyzeIntent(test.content);
    console.log(`🎯 识别意图：${intent} (预期：${test.expectedIntent})`);
    
    if (intent === test.expectedIntent) {
      console.log('✅ 意图识别正确');
      correctCount++;
    } else {
      console.log('⚠️  意图识别有偏差');
    }
  }
  
  console.log(`\n📊 意图识别准确率：${correctCount}/${testMessages.length} (${(correctCount/testMessages.length*100).toFixed(0)}%)`);
}

/**
 * 演示3：对话完整性检查
 */
async function demoCompletenessCheck() {
  console.log('\n\n🚀 演示3：对话完整性检查\n');
  
  const testMessages = [
    { 
      content: '这个问题的解决方案包括：', 
      shouldComplete: true,
      reason: '列表未完成'
    },
    { 
      content: '首先，我们需要分析需求；其次，', 
      shouldComplete: true,
      reason: '句子未完成'
    },
    { 
      content: '答案是42。这是一个完整的回答。', 
      shouldComplete: false,
      reason: '完整句子'
    },
    { 
      content: '例如，', 
      shouldComplete: true,
      reason: '示例未给出'
    }
  ];
  
  for (const test of testMessages) {
    console.log(`\n📝 测试消息：${test.content}`);
    console.log(`🔍 预期补全：${test.shouldComplete ? '是' : '否'} (原因：${test.reason})`);
    
    // 这里应该调用实际的完整性检查
    // 暂时使用简单模拟
    const needsCompletion = test.content.endsWith('：') || test.content.endsWith('，') || test.content.endsWith('；');
    console.log(`🎯 检查结果：${needsCompletion ? '需要补全' : '不需要补全'}`);
    
    if (needsCompletion === test.shouldComplete) {
      console.log('✅ 检查正确');
    } else {
      console.log('⚠️  检查有偏差');
    }
  }
}

/**
 * 演示4：进度汇报系统
 */
async function demoProgressReporting() {
  console.log('\n\n🚀 演示4：进度汇报系统\n');
  
  const tasks = [
    {
      name: '数据抓取任务',
      progress: 0.1,
      status: 'started',
      description: '开始抓取阿拉丁指数数据'
    },
    {
      name: '竞品分析任务',
      progress: 0.5,
      status: 'working',
      estimatedTime: '15分钟',
      description: '分析主要竞品功能'
    },
    {
      name: '报告生成任务',
      progress: 0.9,
      status: 'working',
      estimatedTime: '5分钟',
      description: '生成最终分析报告'
    },
    {
      name: '系统部署任务',
      progress: 1.0,
      status: 'completed',
      summary: '系统已成功部署到生产环境',
      description: '部署完成'
    }
  ];
  
  for (const task of tasks) {
    console.log(`\n📊 任务：${task.name}`);
    console.log(`📈 进度：${Math.round(task.progress * 100)}%`);
    console.log(`🏷️  状态：${task.status}`);
    console.log(`📝 描述：${task.description}`);
    
    // 生成进度汇报
    await dialogManager.reportProgress(task);
    
    // 等待1秒，模拟时间间隔
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
}

/**
 * 演示5：性能优化展示
 */
async function demoPerformanceOptimization() {
  console.log('\n\n🚀 演示5：性能优化展示\n');
  
  console.log('📊 Token优化策略：');
  console.log('1. 缓存常用响应，减少模型调用');
  console.log('2. 智能判断思考需求，避免不必要的深度思考');
  console.log('3. 限制每次检查的token使用量');
  console.log('4. 根据优先级调整响应深度');
  
  console.log('\n🎯 优化效果模拟：');
  
  const scenarios = [
    { type: '简单社交问候', tokensWithoutOpt: 500, tokensWithOpt: 50, saving: '90%' },
    { type: '常规问题回答', tokensWithoutOpt: 1000, tokensWithOpt: 300, saving: '70%' },
    { type: '复杂任务处理', tokensWithoutOpt: 2000, tokensWithOpt: 1500, saving: '25%' },
    { type: '进度汇报', tokensWithoutOpt: 300, tokensWithOpt: 100, saving: '67%' }
  ];
  
  for (const scenario of scenarios) {
    console.log(`\n📋 ${scenario.type}:`);
    console.log(`   无优化：${scenario.tokensWithoutOpt} tokens`);
    console.log(`   有优化：${scenario.tokensWithOpt} tokens`);
    console.log(`   节省：${scenario.saving}`);
  }
}

/**
 * 运行所有演示
 */
async function runAllDemos() {
  console.log('='.repeat(60));
  console.log('🤖 智能对话管理技能演示程序');
  console.log('='.repeat(60));
  
  try {
    await demoBasicMonitoring();
    await demoIntentRecognition();
    await demoCompletenessCheck();
    await demoProgressReporting();
    await demoPerformanceOptimization();
    
    console.log('\n\n' + '='.repeat(60));
    console.log('🎉 所有演示完成！');
    console.log('='.repeat(60));
    
    // 显示最终状态
    const finalStatus = dialogManager.getStatus();
    console.log('\n📈 最终统计数据：');
    console.log(JSON.stringify(finalStatus, null, 2));
    
    // 停止对话管理器
    await dialogManager.stop();
    console.log('\n🛑 对话管理器已停止');
    
  } catch (error) {
    console.error('\n❌ 演示过程中出现错误：', error.message);
  }
}

// 运行演示程序
runAllDemos().catch(console.error);