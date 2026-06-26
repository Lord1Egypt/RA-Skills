/**
 * Enhanced Memory System - 统一初始化脚本
 * 确保所有优化组件正确集成
 */

import { logger } from './logger.js';
import { getEnhancedMemorySystem } from './enhanced_memory_system.js';
import { ENHANCED_CONFIG, getEnhancedConfig } from './config/enhanced_config.js';

/**
 * 初始化增强版记忆系统
 */
export async function initializeEnhancedMemorySystem(customConfig = {}) {
  logger.info('[Init] 开始初始化增强版记忆系统...');
  
  // 合并配置
  const config = {
    ...ENHANCED_CONFIG,
    ...customConfig,
    enabled: {
      ...ENHANCED_CONFIG.enabled,
      ...(customConfig.enabled || {})
    }
  };
  
  // 创建系统实例
  const system = getEnhancedMemorySystem({
    // 核心开关
    enableTypeSystem: config.enabled.typeSystem,
    enableQueue: config.enabled.queue,
    enableDedup: config.enabled.dedup,
    enableRecallOptimization: config.enabled.recallOptimization,
    enableCompression: config.enabled.compression,
    enableLifecycle: config.enabled.lifecycle,
    enablePipeline: config.enabled.pipeline,
    
    // 子系统配置
    typeSystemOptions: config.typeSystem,
    queueOptions: config.queue,
    dedupOptions: config.dedup,
    recallOptions: config.recall,
    compressionOptions: config.compression,
    lifecycleOptions: config.lifecycle,
    pipelineOptions: config.pipeline,
    
    asyncProcessing: config.pipeline.asyncProcessing
  });
  
  // 初始化系统
  await system.initialize();
  
  logger.info('[Init] 增强版记忆系统初始化完成');
  
  return system;
}

/**
 * 获取系统状态报告
 */
export function getSystemReport(system) {
  const status = system.getStatus();
  const health = system.healthCheck();
  
  const report = {
    timestamp: new Date().toISOString(),
    status: health.status,
    initialized: status.initialized,
    
    components: {
      typeSystem: {
        enabled: !!status.components.typeRegistry,
        typesCount: status.components.typeRegistry?.typesCount || 0
      },
      
      queue: {
        enabled: !!status.components.queue,
        status: status.components.queue?.status || 'disabled',
        activeTasks: status.components.queue?.activeTasks || 0
      },
      
      dedup: {
        enabled: !!status.components.deduplicator,
        totalChecked: status.components.deduplicator?.totalChecked || 0,
        duplicatesFound: status.components.deduplicator?.duplicatesFound || 0
      },
      
      recallOptimizer: {
        enabled: !!status.components.recallOptimizer,
        totalRecalls: status.components.recallOptimizer?.totalRecalls || 0,
        avgRecallTime: status.components.recallOptimizer?.avgRecallTime || 0
      },
      
      compressor: {
        enabled: !!status.components.compressor,
        totalCompressions: status.components.compressor?.totalCompressions || 0,
        avgCompressionRatio: status.components.compressor?.avgCompressionRatio || 0
      },
      
      lifecycleManager: {
        enabled: !!status.components.lifecycleManager,
        totalArchived: status.components.lifecycleManager?.totalArchived || 0,
        totalCleaned: status.components.lifecycleManager?.totalCleaned || 0
      },
      
      pipeline: {
        enabled: !!status.components.pipeline,
        isProcessing: status.components.pipeline?.isProcessing || false
      }
    },
    
    health: health
  };
  
  return report;
}

/**
 * 打印系统状态
 */
export function printSystemStatus(system) {
  const report = getSystemReport(system);
  
  console.log('\n' + '='.repeat(60));
  console.log('📊 Enhanced Memory System Status');
  console.log('='.repeat(60));
  console.log(`Timestamp: ${report.timestamp}`);
  console.log(`Status: ${report.status.toUpperCase()}`);
  console.log(`Initialized: ${report.initialized ? '✅' : '❌'}`);
  console.log('\n📦 Components:');
  
  for (const [name, info] of Object.entries(report.components)) {
    const statusIcon = info.enabled ? '✅' : '❌';
    console.log(`  ${statusIcon} ${name}: ${JSON.stringify(info)}`);
  }
  
  console.log('\n' + '='.repeat(60) + '\n');
}

/**
 * 快速测试系统功能
 */
export async function quickTest(system) {
  logger.info('[Test] 开始快速测试...');
  
  const results = {
    store: false,
    recall: false,
    typeDetection: false,
    dedup: false,
    compression: false
  };
  
  try {
    // 测试存储
    const storeResult = await system.remember('测试记忆：张三擅长JavaScript编程', {
      userId: 'test_user',
      source: 'quick_test'
    });
    results.store = storeResult.status === 'success';
    logger.info(`[Test] 存储: ${results.store ? '✅' : '❌'}`);
    
    // 测试召回
    const recallResult = await system.recall('编程技能', {
      userId: 'test_user',
      optimizeRecall: true,
      compress: true
    });
    results.recall = recallResult.status === 'success';
    logger.info(`[Test] 召回: ${results.recall ? '✅' : '❌'}`);
    
    // 测试类型检测
    if (system.typeRegistry) {
      const detected = await system.typeRegistry.detectMemoryType('张三每天早上7点起床');
      results.typeDetection = detected.type !== 'general';
      logger.info(`[Test] 类型检测: ${results.typeDetection ? '✅' : '❌'} (类型: ${detected.type})`);
    }
    
    // 测试去重
    if (system.deduplicator) {
      const dupResult = await system.remember('测试记忆：张三擅长JavaScript编程', {
        userId: 'test_user',
        source: 'quick_test'
      });
      results.dedup = dupResult.status === 'duplicate_skipped';
      logger.info(`[Test] 去重: ${results.dedup ? '✅' : '❌'}`);
    }
    
    // 测试压缩
    if (system.compressor && recallResult.compressedText) {
      results.compression = recallResult.compressedText.length > 0;
      logger.info(`[Test] 压缩: ${results.compression ? '✅' : '❌'}`);
    }
    
    const allPassed = Object.values(results).every(v => v);
    logger.info(`[Test] 测试完成: ${allPassed ? '✅ 全部通过' : '⚠️ 部分失败'}`);
    
    return {
      success: allPassed,
      results: results
    };
    
  } catch (error) {
    logger.error('[Test] 测试失败:', error);
    return {
      success: false,
      results: results,
      error: error.message
    };
  }
}

/**
 * 关闭系统
 */
export async function shutdownEnhancedMemorySystem(system) {
  logger.info('[Shutdown] 关闭增强版记忆系统...');
  
  await system.shutdown();
  
  logger.info('[Shutdown] 系统已关闭');
}

// 导出所有组件
export {
  getEnhancedMemorySystem,
  getEnhancedConfig,
  ENHANCED_CONFIG
};

export default {
  initializeEnhancedMemorySystem,
  getSystemReport,
  printSystemStatus,
  quickTest,
  shutdownEnhancedMemorySystem
};
