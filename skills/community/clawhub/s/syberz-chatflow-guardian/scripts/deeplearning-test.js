/**
 * 深度学习优化模块测试程序
 * 
 * 测试深度学习增强功能：
 * 1. 意图识别增强
 * 2. 用户行为预测
 * 3. 对话质量分析
 */

const DeepLearningOptimizer = require('../src/deeplearning');

// 创建深度学习优化器
const dlOptimizer = new DeepLearningOptimizer({
  enabled: true,
  trainingEnabled: true,
  modelType: 'hybrid',
  usePretrained: true
}, console);

/**
 * 测试1：意图识别增强
 */
async function testIntentEnhancement() {
  console.log('🧠 测试1：意图识别增强\n');
  
  const testCases = [
    { message: '今天天气怎么样？', baselineIntent: 'question', context: { topic: 'weather' } },
    { message: '帮我分析一下数据', baselineIntent: 'task_request', context: { topic: 'data' } },
    { message: '谢谢你的帮助', baselineIntent: 'feedback', context: { topic: 'general' } },
    { message: '早上好', baselineIntent: 'social', context: { topic: 'greeting' } },
    { message: '这个功能很好用', baselineIntent: 'feedback', context: { topic: 'feature' } },
    { message: '最近工作忙吗？', baselineIntent: 'social', context: { topic: 'work' } },
    { message: '需要改进一下界面', baselineIntent: 'feedback', context: { topic: 'ui' } },
    { message: '什么是人工智能？', baselineIntent: 'question', context: { topic: 'ai' } }
  ];
  
  let correctCount = 0;
  let enhancedCount = 0;
  
  for (const testCase of testCases) {
    const result = dlOptimizer.enhanceIntentRecognition(
      testCase.message,
      testCase.context,
      testCase.baselineIntent
    );
    
    console.log(`📝 测试消息: ${testCase.message}`);
    console.log(`  基线意图: ${testCase.baselineIntent}`);
    console.log(`  增强意图: ${result.intent} (置信度: ${result.confidence.toFixed(2)})`);
    console.log(`  是否增强: ${result.enhanced ? '✅ 是' : '❌ 否'}`);
    
    if (result.enhanced) {
      enhancedCount++;
    }
    
    if (result.intent === testCase.baselineIntent) {
      correctCount++;
      console.log('  ✅ 意图识别正确');
    } else {
      console.log('  ⚠️  意图识别有偏差');
    }
    
    console.log('');
    
    // 收集训练数据
    dlOptimizer.collectTrainingData({
      userId: 'test-user',
      message: testCase.message,
      intent: testCase.baselineIntent,
      predictedIntent: result.intent,
      confidence: result.confidence,
      responseTime: Math.random() * 5000,
      context: testCase.context
    });
  }
  
  console.log('📊 测试结果统计:');
  console.log(`  总测试用例: ${testCases.length}`);
  console.log(`  正确识别: ${correctCount}/${testCases.length} (${(correctCount/testCases.length*100).toFixed(1)}%)`);
  console.log(`  增强功能使用: ${enhancedCount}/${testCases.length} (${(enhancedCount/testCases.length*100).toFixed(1)}%)`);
  
  return { correctCount, total: testCases.length, enhancedCount };
}

/**
 * 测试2：用户行为预测
 */
async function testUserBehaviorPrediction() {
  console.log('\n\n🧠 测试2：用户行为预测\n');
  
  // 模拟用户交互历史
  const userHistory = [
    { userId: 'user-001', intent: 'social', message: '早上好', timestamp: Date.now() - 3600000 },
    { userId: 'user-001', intent: 'question', message: '今天有什么安排？', timestamp: Date.now() - 1800000 },
    { userId: 'user-001', intent: 'task_request', message: '帮我查一下数据', timestamp: Date.now() - 900000 },
    { userId: 'user-001', intent: 'feedback', message: '谢谢，很好用', timestamp: Date.now() - 300000 }
  ];
  
  console.log('📝 用户交互历史:');
  userHistory.forEach((interaction, index) => {
    console.log(`  ${index + 1}. [${interaction.intent}] ${interaction.message}`);
  });
  
  // 预测下一个动作
  const prediction = dlOptimizer.predictNextAction('user-001', userHistory);
  
  console.log('\n🔮 预测结果:');
  if (prediction) {
    console.log(`  预测下一个意图: ${prediction.nextIntent}`);
    console.log(`  置信度: ${prediction.confidence.toFixed(2)}`);
    console.log(`  识别模式: ${prediction.pattern || 'N/A'}`);
    console.log(`  使用模型: ${prediction.model || 'N/A'}`);
  } else {
    console.log('  ℹ️  无法生成预测（数据不足）');
  }
  
  // 测试多个用户
  console.log('\n👥 多用户测试:');
  const users = ['user-002', 'user-003', 'user-004'];
  
  users.forEach(userId => {
    const randomPrediction = dlOptimizer.predictNextAction(userId, [
      { intent: 'social', message: '你好' },
      { intent: 'question', message: '问个问题' }
    ]);
    
    console.log(`  ${userId}: ${randomPrediction ? randomPrediction.nextIntent : '无预测'}`);
  });
  
  return prediction;
}

/**
 * 测试3：对话质量分析
 */
async function testConversationQualityAnalysis() {
  console.log('\n\n🧠 测试3：对话质量分析\n');
  
  // 模拟对话记录
  const conversation = [
    { role: 'user', message: '你好', intent: 'social', responseTime: 1200, confidence: 0.9 },
    { role: 'assistant', message: '你好！有什么可以帮助您的？', responseTime: 800, confidence: 0.95 },
    { role: 'user', message: '今天天气怎么样？', intent: 'question', responseTime: 1500, confidence: 0.85 },
    { role: 'assistant', message: '今天天气晴朗，温度25度，适合外出。', responseTime: 1200, confidence: 0.92 },
    { role: 'user', message: '谢谢', intent: 'feedback', responseTime: 900, confidence: 0.88 },
    { role: 'assistant', message: '不客气！有其他问题随时问我。', responseTime: 700, confidence: 0.96 }
  ];
  
  console.log('💬 对话记录:');
  conversation.forEach((turn, index) => {
    console.log(`  ${turn.role}: ${turn.message} [${turn.intent || 'N/A'}]`);
  });
  
  // 分析对话质量
  const qualityAnalysis = dlOptimizer.analyzeConversationQuality(conversation);
  
  console.log('\n📊 质量分析结果:');
  console.log(`  质量得分: ${qualityAnalysis.score.toFixed(2)}/1.0`);
  
  if (qualityAnalysis.metrics) {
    console.log('  详细指标:');
    console.log(`    总消息数: ${qualityAnalysis.metrics.totalMessages || 0}`);
    console.log(`    用户消息: ${qualityAnalysis.metrics.userMessages || 0}`);
    console.log(`    助手消息: ${qualityAnalysis.metrics.assistantMessages || 0}`);
    console.log(`    平均响应时间: ${(qualityAnalysis.metrics.avgResponseTime || 0).toFixed(0)}ms`);
    console.log(`    意图准确率: ${(qualityAnalysis.metrics.intentAccuracy || 0).toFixed(2)}`);
  }
  
  console.log(`  使用模型: ${qualityAnalysis.model || 'N/A'}`);
  console.log(`  模型已训练: ${qualityAnalysis.trained ? '✅ 是' : '❌ 否'}`);
  
  return qualityAnalysis;
}

/**
 * 测试4：模型训练和性能
 */
async function testModelTraining() {
  console.log('\n\n🧠 测试4：模型训练和性能\n');
  
  // 获取初始模型状态
  console.log('📊 初始模型状态:');
  const initialStatus = dlOptimizer.getModelStatus();
  console.log(`  深度学习启用: ${initialStatus.enabled ? '✅ 是' : '❌ 否'}`);
  console.log(`  训练启用: ${initialStatus.trainingEnabled ? '✅ 是' : '❌ 否'}`);
  console.log(`  模型数量: ${initialStatus.modelCount}`);
  console.log(`  训练数据量: ${initialStatus.trainingDataSize}`);
  
  // 手动触发训练
  console.log('\n🔄 触发模型训练...');
  
  // 添加更多训练数据
  for (let i = 0; i < 50; i++) {
    const intents = ['question', 'task_request', 'feedback', 'social'];
    const randomIntent = intents[Math.floor(Math.random() * intents.length)];
    
    dlOptimizer.collectTrainingData({
      userId: `train-user-${i % 5}`,
      message: `测试消息 ${i} - ${randomIntent}`,
      intent: randomIntent,
      predictedIntent: randomIntent,
      confidence: 0.7 + Math.random() * 0.3,
      responseTime: 1000 + Math.random() * 4000,
      context: { topic: 'test', iteration: i }
    });
  }
  
  // 检查是否需要训练
  if (initialStatus.trainingDataSize >= 32) { // batch size
    console.log('🎯 训练数据足够，开始训练...');
    
    // 模拟训练过程
    dlOptimizer.trainModels();
    
    // 获取训练后状态
    console.log('\n📈 训练后状态:');
    const trainedStatus = dlOptimizer.getModelStatus();
    
    if (trainedStatus.models) {
      console.log('  模型准确率:');
      for (const [modelName, modelInfo] of Object.entries(trainedStatus.models)) {
        if (modelInfo.trained) {
          console.log(`    ${modelName}: ${modelInfo.accuracy.toFixed(3)} (${modelInfo.trainingSamples} 样本)`);
        }
      }
    }
    
    // 显示性能指标
    if (trainedStatus.performanceMetrics && trainedStatus.performanceMetrics.length > 0) {
      const latestMetrics = trainedStatus.performanceMetrics[trainedStatus.performanceMetrics.length - 1];
      console.log(`  最近训练时间: ${new Date(latestMetrics[0]).toLocaleTimeString()}`);
      console.log(`  训练耗时: ${latestMetrics[1].trainingTime}ms`);
    }
  } else {
    console.log('ℹ️  训练数据不足，跳过训练');
  }
  
  return initialStatus;
}

/**
 * 测试5：综合性能对比
 */
async function testPerformanceComparison() {
  console.log('\n\n🧠 测试5：综合性能对比\n');
  
  console.log('⚡ 性能对比测试:');
  console.log('  基线算法 vs 深度学习增强\n');
  
  const testMessages = [
    '你好，最近怎么样？',
    '帮我处理这个文件',
    '这个功能需要改进',
    '什么是机器学习？',
    '早上好，今天有什么计划？'
  ];
  
  const results = [];
  
  for (const message of testMessages) {
    // 基线算法（简单规则）
    const baselineIntent = guessIntentBaseline(message);
    
    // 深度学习增强
    const enhancedResult = dlOptimizer.enhanceIntentRecognition(
      message,
      { topic: 'test' },
      baselineIntent
    );
    
    results.push({
      message,
      baselineIntent,
      enhancedIntent: enhancedResult.intent,
      confidence: enhancedResult.confidence,
      enhanced: enhancedResult.enhanced
    });
    
    console.log(`📝 "${message}"`);
    console.log(`  基线: ${baselineIntent}`);
    console.log(`  增强: ${enhancedResult.intent} (${enhancedResult.confidence.toFixed(2)})`);
    console.log(`  是否改变: ${baselineIntent !== enhancedResult.intent ? '✅ 是' : '❌ 否'}`);
    console.log('');
  }
  
  // 统计
  const changedCount = results.filter(r => r.baselineIntent !== r.enhancedIntent).length;
  const enhancedCount = results.filter(r => r.enhanced).length;
  
  console.log('📊 对比统计:');
  console.log(`  总测试消息: ${results.length}`);
  console.log(`  意图改变: ${changedCount} (${(changedCount/results.length*100).toFixed(1)}%)`);
  console.log(`  增强功能使用: ${enhancedCount} (${(enhancedCount/results.length*100).toFixed(1)}%)`);
  console.log(`  平均置信度: ${(results.reduce((sum, r) => sum + r.confidence, 0) / results.length).toFixed(2)}`);
  
  return results;
}

/**
 * 基线意图识别（简单规则）
 */
function guessIntentBaseline(message) {
  const lower = message.toLowerCase();
  
  if (lower.includes('？') || lower.includes('?') || 
      lower.includes('什么') || lower.includes('怎么') || lower.includes('如何')) {
    return 'question';
  }
  
  if (lower.includes('帮') || lower.includes('请') || lower.includes('需要') || 
      lower.includes('处理') || lower.includes('分析')) {
    return 'task_request';
  }
  
  if (lower.includes('谢谢') || lower.includes('感谢') || 
      lower.includes('好') || lower.includes('改进')) {
    return 'feedback';
  }
  
  if (lower.includes('你好') || lower.includes('早上好') || 
      lower.includes('晚上好') || lower.includes('最近')) {
    return 'social';
  }
  
  return 'unknown';
}

/**
 * 运行所有测试
 */
async function runAllTests() {
  console.log('='.repeat(60));
  console.log('🧠 深度学习优化模块 - 综合测试');
  console.log('='.repeat(60));
  
  console.log('\n📅 测试开始时间:', new Date().toISOString());
  
  try {
    const test1Results = await testIntentEnhancement();
    const test2Results = await testUserBehaviorPrediction();
    const test3Results = await testConversationQualityAnalysis();
    const test4Results = await testModelTraining();
    const test5Results = await testPerformanceComparison();
    
    console.log('\n\n' + '='.repeat(60));
    console.log('🎉 所有测试完成！');
    console.log('='.repeat(60));
    
    console.log('\n✅ 测试总结:');
    console.log(`  1. 意图识别增强: ${test1Results.correctCount}/${test1Results.total} 正确`);
    console.log(`  2. 用户行为预测: ${test2Results ? '✅ 成功' : '❌ 失败'}`);
    console.log(`  3. 对话质量分析: ${test3Results.score ? '得分 ' + test3Results.score.toFixed(2) : '❌ 失败'}`);
    console.log(`  4. 模型训练: ${test4Results.enabled ? '✅ 启用' : '❌ 禁用'}`);
    console.log(`  5. 性能对比: ${test5Results.length} 条消息测试`);
    
    console.log('\n🚀 深度学习优化功能:');
    console.log('  • 意图识别准确率提升');
    console.log('  • 用户行为智能预测');
    console.log('  • 对话质量深度学习评估');
    console.log('  • 自适应训练和优化');
    
    console.log('\n📈 性能指标:');
    const modelStatus = dlOptimizer.getModelStatus();
    if (modelStatus.models) {
      for (const [name, info] of Object.entries(modelStatus.models)) {
        if (info.trained) {
          console.log(`  ${name}: ${(info.accuracy * 100).toFixed(1)}% 准确率`);
        }
      }
    }
    
  } catch (error) {
    console.error('\n❌ 测试过程中出现错误:', error.message);
    console.error(error.stack);
  }
}

// 运行所有测试
runAllTests().catch(console.error);