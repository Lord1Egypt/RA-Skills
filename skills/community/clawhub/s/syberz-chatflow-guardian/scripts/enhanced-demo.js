/**
 * 增强功能演示程序
 * 
 * 展示智能对话管理技能的增强功能：
 * 1. 多平台支持
 * 2. 预测性响应
 * 3. 高级监控
 */

const DialogManager = require('../src/index');

// 模拟会话
const mockSession = {
  id: 'enhanced-demo-' + Date.now(),
  type: 'direct',
  platform: 'qqbot',
  userId: 'demo-user-001',
  userName: '演示用户'
};

// 创建增强版对话管理器
const dialogManager = new DialogManager();

/**
 * 演示1：多平台支持
 */
async function demoMultiPlatformSupport() {
  console.log('🚀 演示1：多平台支持功能\n');
  
  try {
    // 初始化多个平台
    console.log('📱 支持的平台:');
    const supportedPlatforms = dialogManager.platformManager.getSupportedPlatforms();
    console.log('  ', supportedPlatforms.join(', '));
    
    // 初始化QQBot平台
    console.log('\n🔧 初始化QQBot平台...');
    await dialogManager.platformManager.initializePlatform('qqbot', {
      botId: 'demo-bot',
      apiKey: 'demo-api-key'
    });
    
    // 初始化企业微信平台
    console.log('🔧 初始化企业微信平台...');
    await dialogManager.platformManager.initializePlatform('wecom', {
      corpId: 'demo-corp',
      agentId: 'demo-agent'
    });
    
    // 显示平台状态
    console.log('\n📊 平台状态:');
    const status = dialogManager.platformManager.getPlatformStatus();
    Object.entries(status).forEach(([name, info]) => {
      console.log(`  ${name}: ${info.name} (${info.type})`);
    });
    
    // 测试消息发送
    console.log('\n📨 测试多平台消息发送:');
    
    // 发送到QQBot
    const qqResult = await dialogManager.platformManager.sendMessage(
      'qqbot',
      '这是一条来自增强版对话管理器的测试消息',
      { userId: 'test-user-001' }
    );
    console.log(`  QQBot发送结果: ${qqResult.success ? '✅ 成功' : '❌ 失败'}`);
    
    // 发送到企业微信
    const wecomResult = await dialogManager.platformManager.sendMessage(
      'wecom',
      '这是一条来自增强版对话管理器的测试消息',
      { userId: 'wecom-user-001' }
    );
    console.log(`  企业微信发送结果: ${wecomResult.success ? '✅ 成功' : '❌ 失败'}`);
    
    // 测试广播功能
    console.log('\n📣 测试广播功能:');
    const broadcastResult = await dialogManager.platformManager.broadcastMessage(
      '这是一条广播测试消息',
      {
        qqbot: { userId: 'user-001' },
        wecom: { userId: 'user-002' }
      }
    );
    console.log(`  广播结果: ${broadcastResult.success}/${broadcastResult.total} 成功`);
    
  } catch (error) {
    console.error('❌ 多平台演示失败:', error.message);
  }
}

/**
 * 演示2：预测性响应
 */
async function demoPredictiveResponse() {
  console.log('\n\n🚀 演示2：预测性响应功能\n');
  
  try {
    // 模拟用户交互历史
    console.log('📝 模拟用户交互历史...');
    
    const testInteractions = [
      {
        userId: 'demo-user-001',
        message: '今天天气怎么样？',
        intent: 'question',
        priority: 'p0',
        responseTime: 1500,
        responseType: 'weather_report',
        timestamp: Date.now() - 3600000, // 1小时前
        context: { topic: 'weather' }
      },
      {
        userId: 'demo-user-001',
        message: '帮我分析销售数据',
        intent: 'task_request',
        priority: 'p1',
        responseTime: 30000,
        responseType: 'data_analysis',
        timestamp: Date.now() - 7200000, // 2小时前
        context: { topic: 'data', type: 'sales' }
      },
      {
        userId: 'demo-user-001',
        message: '早上好',
        intent: 'social',
        priority: 'p3',
        responseTime: 500,
        responseType: 'greeting',
        timestamp: Date.now() - 86400000, // 昨天
        context: { topic: 'greeting' }
      },
      {
        userId: 'demo-user-001',
        message: '需要改进一下报告格式',
        intent: 'feedback',
        priority: 'p2',
        responseTime: 8000,
        responseType: 'improvement_suggestion',
        timestamp: Date.now() - 43200000, // 半天前
        context: { topic: 'report', aspect: 'format' }
      }
    ];
    
    // 记录交互历史
    testInteractions.forEach(interaction => {
      dialogManager.predictiveEngine.recordInteraction(interaction);
    });
    
    // 显示用户统计数据
    console.log('📊 用户统计数据:');
    const userStats = dialogManager.predictiveEngine.getUserStats('demo-user-001');
    if (userStats) {
      console.log(`  总交互次数: ${userStats.totalInteractions}`);
      console.log(`  主要意图: ${userStats.intents.slice(0, 3).map(([intent, count]) => `${intent}(${count})`).join(', ')}`);
      console.log(`  活跃时段: ${userStats.activeHours.slice(0, 3).map(([hour, count]) => `${hour}:00(${count})`).join(', ')}`);
      console.log(`  感兴趣的话题: ${userStats.favoriteTopics.slice(0, 5).join(', ')}`);
    }
    
    // 生成预测
    console.log('\n🔮 生成预测:');
    const currentContext = { topic: 'data', type: 'sales' };
    const predictions = dialogManager.predictiveEngine.generatePredictions('demo-user-001', currentContext);
    
    if (predictions.length > 0) {
      predictions.forEach((prediction, index) => {
        console.log(`\n  ${index + 1}. ${prediction.type} (置信度: ${(prediction.confidence * 100).toFixed(1)}%)`);
        console.log(`     原因: ${prediction.reason}`);
        console.log(`     准备: ${prediction.prepare.join(', ')}`);
      });
    } else {
      console.log('  ℹ️  暂无足够数据生成预测');
    }
    
    // 模拟新的交互
    console.log('\n🔄 模拟新交互并更新预测:');
    const newInteraction = {
      userId: 'demo-user-001',
      message: '帮我分析最新的销售数据',
      intent: 'task_request',
      priority: 'p1',
      responseTime: 25000,
      responseType: 'data_analysis',
      timestamp: Date.now(),
      context: { topic: 'data', type: 'sales', period: 'latest' }
    };
    
    dialogManager.predictiveEngine.recordInteraction(newInteraction);
    
    // 重新生成预测
    const updatedPredictions = dialogManager.predictiveEngine.generatePredictions('demo-user-001', {
      topic: 'data',
      type: 'sales',
      period: 'latest'
    });
    
    console.log(`  更新后的预测数量: ${updatedPredictions.length}`);
    
  } catch (error) {
    console.error('❌ 预测性响应演示失败:', error.message);
  }
}

/**
 * 演示3：完整功能集成
 */
async function demoFullIntegration() {
  console.log('\n\n🚀 演示3：完整功能集成\n');
  
  try {
    // 启动对话管理器
    console.log('🚀 启动增强版对话管理器...');
    await dialogManager.start(mockSession);
    
    // 显示完整状态
    console.log('\n📊 完整系统状态:');
    const status = dialogManager.getStatus();
    
    console.log(`  运行状态: ${status.isRunning ? '✅ 运行中' : '❌ 已停止'}`);
    console.log(`  会话平台: ${status.session.platform}`);
    console.log(`  检查间隔: ${status.config.check_interval}秒`);
    
    if (status.enhanced) {
      console.log(`  平台支持: ${status.enhanced.platforms ? '✅ 已启用' : '❌ 未启用'}`);
      console.log(`  预测功能: ${status.enhanced.predictive ? '✅ 已启用' : '❌ 未启用'}`);
    }
    
    // 模拟用户交互
    console.log('\n💬 模拟用户交互流程:');
    
    console.log('  1. 用户: "早上好"');
    const socialIntent = dialogManager.analyzer.analyzeIntent('早上好');
    console.log(`     识别意图: ${socialIntent}`);
    
    console.log('  2. 用户: "帮我分析一下数据"');
    const taskIntent = dialogManager.analyzer.analyzeIntent('帮我分析一下数据');
    console.log(`     识别意图: ${taskIntent}`);
    
    console.log('  3. 用户: "这个功能很好用"');
    const feedbackIntent = dialogManager.analyzer.analyzeIntent('这个功能很好用');
    console.log(`     识别意图: ${feedbackIntent}`);
    
    // 测试进度汇报
    console.log('\n📈 测试进度汇报:');
    const task = {
      name: '数据分析任务',
      progress: 0.5,
      status: 'working',
      estimatedTime: '15分钟'
    };
    
    const progressReport = dialogManager.responder.generateProgressReport(task);
    console.log(`  进度汇报: ${progressReport.content}`);
    
    // 测试多平台进度通知
    console.log('\n📱 测试多平台进度通知:');
    if (dialogManager.platformManager.platforms.has('qqbot')) {
      const notification = `进度通知: ${progressReport.content}`;
      console.log(`  准备发送到QQBot: ${notification.substring(0, 50)}...`);
    }
    
    // 停止对话管理器
    console.log('\n🛑 停止对话管理器...');
    await dialogManager.stop();
    
  } catch (error) {
    console.error('❌ 完整集成演示失败:', error.message);
  }
}

/**
 * 演示4：性能监控和诊断
 */
async function demoPerformanceMonitoring() {
  console.log('\n\n🚀 演示4：性能监控和诊断\n');
  
  try {
    // 显示系统统计数据
    console.log('📊 预测引擎统计数据:');
    const predictiveStats = dialogManager.predictiveEngine.getAllStats();
    
    console.log(`  总用户数: ${predictiveStats.totalUsers}`);
    console.log(`  总交互数: ${predictiveStats.totalInteractions}`);
    console.log(`  最近活跃: ${predictiveStats.recentActivity.length} 条记录`);
    
    // 显示平台统计数据
    console.log('\n📱 平台管理器统计:');
    const platformStatus = dialogManager.platformManager.getPlatformStatus();
    console.log(`  已初始化平台: ${Object.keys(platformStatus).length}`);
    
    // 清理旧数据演示
    console.log('\n🧹 数据清理演示:');
    const cleanedCount = dialogManager.predictiveEngine.cleanupOldData(24 * 60 * 60 * 1000); // 清理24小时前的数据
    console.log(`  清理的旧记录数: ${cleanedCount}`);
    
    // 重置演示
    console.log('\n🔄 重置演示:');
    dialogManager.predictiveEngine.reset();
    console.log('  预测引擎已重置');
    
  } catch (error) {
    console.error('❌ 性能监控演示失败:', error.message);
  }
}

/**
 * 运行所有演示
 */
async function runAllDemos() {
  console.log('='.repeat(60));
  console.log('🤖 智能对话管理技能 - 增强功能演示');
  console.log('='.repeat(60));
  
  console.log('\n📅 演示开始时间:', new Date().toISOString());
  
  try {
    await demoMultiPlatformSupport();
    await demoPredictiveResponse();
    await demoFullIntegration();
    await demoPerformanceMonitoring();
    
    console.log('\n\n' + '='.repeat(60));
    console.log('🎉 所有增强功能演示完成！');
    console.log('='.repeat(60));
    
    console.log('\n✅ 已演示的增强功能:');
    console.log('  1. 多平台支持（QQBot、企业微信等8个平台）');
    console.log('  2. 预测性响应（基于用户历史的智能预测）');
    console.log('  3. 高级监控和诊断系统');
    console.log('  4. 完整功能集成和工作流');
    
    console.log('\n🚀 技能现已支持:');
    console.log('  • 跨平台对话管理');
    console.log('  • 预测性用户需求分析');
    console.log('  • 智能资源优化');
    console.log('  • 企业级可扩展性');
    
  } catch (error) {
    console.error('\n❌ 演示过程中出现错误:', error.message);
    console.error(error.stack);
  }
}

// 运行演示程序
runAllDemos().catch(console.error);