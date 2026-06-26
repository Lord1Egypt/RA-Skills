/**
 * HITL 支持测试套件
 * 
 * 测试覆盖:
 * - 审批流程
 * - 超时处理
 * - 事件系统
 * - 历史记录
 * - 统计信息
 */

const { HITLManager, HITLHelper } = require('../src/hitl');

// 测试辅助函数
function test(name, fn) {
  return { name, fn };
}

async function runTests() {
  console.log('🧪 HITL 支持测试套件');
  console.log('=' .repeat(50));

  const tests = [
    // ========== 基础功能测试 ==========
    test('HITL 初始化', async () => {
      const hitl = new HITLManager({ verbose: false });
      
      if (!hitl) throw new Error('HITL 初始化失败');
      if (!hitl.options) throw new Error('缺少配置');
      if (hitl.options.enabled !== true) throw new Error('默认应该启用');
      
      console.log('✅ HITL 初始化');
    }),

    test('HITL 禁用模式', async () => {
      const hitl = new HITLManager({ enabled: false, verbose: false });
      
      if (hitl.options.enabled !== false) throw new Error('禁用失败');
      if (hitl.requiresApproval('any-tool')) throw new Error('禁用模式下不应需要审批');
      
      console.log('✅ HITL 禁用模式');
    }),

    test('工具审批检查', async () => {
      const hitl = new HITLManager({
        requireApproval: ['file-write', 'execute-command'],
        verbose: false,
      });
      
      if (!hitl.requiresApproval('file-write')) throw new Error('file-write 应该需要审批');
      if (hitl.requiresApproval('file-read')) throw new Error('file-read 不应该需要审批');
      
      console.log('✅ 工具审批检查');
    }),

    test('白名单自动批准', async () => {
      const hitl = new HITLManager({
        requireApproval: ['file-write', 'execute-command'],
        autoApprove: ['file-read'],
        verbose: false,
      });
      
      if (hitl.requiresApproval('file-read')) throw new Error('白名单工具应该自动批准');
      
      console.log('✅ 白名单自动批准');
    }),

    // ========== 审批流程测试 ==========
    test('创建审批请求', async () => {
      const hitl = new HITLManager({ verbose: false });
      
      const requestPromise = hitl.createApprovalRequest('file-write', {
        path: 'test.txt',
        content: 'Hello'
      }, '测试文件写入');
      
      // 检查待处理请求
      const pending = hitl.getPendingRequests();
      if (pending.length !== 1) throw new Error('应该有 1 个待处理请求');
      
      const request = pending[0];
      if (request.toolName !== 'file-write') throw new Error('工具名称错误');
      if (request.status !== 'pending') throw new Error('状态应该是 pending');
      
      // 清理
      await hitl.approve(request.id);
      await requestPromise;
      
      console.log('✅ 创建审批请求');
    }),

    test('批准请求', async () => {
      const hitl = new HITLManager({ verbose: false });
      
      const requestPromise = hitl.createApprovalRequest('file-write', {}, '测试');
      
      const pending = hitl.getPendingRequests();
      const result = await hitl.approve(pending[0].id, '测试批准');
      
      if (!result.success) throw new Error('批准失败');
      if (!result.approved) throw new Error('应该批准');
      
      const finalResult = await requestPromise;
      if (!finalResult.approved) throw new Error('最终结果应该批准');
      
      console.log('✅ 批准请求');
    }),

    test('拒绝请求', async () => {
      const hitl = new HITLManager({ verbose: false });
      
      const requestPromise = hitl.createApprovalRequest('file-write', {}, '测试');
      
      const pending = hitl.getPendingRequests();
      const result = await hitl.reject(pending[0].id, '测试拒绝');
      
      if (!result.success) throw new Error('拒绝失败');
      if (result.approved) throw new Error('应该拒绝');
      
      const finalResult = await requestPromise;
      if (finalResult.approved) throw new Error('最终结果应该拒绝');
      
      console.log('✅ 拒绝请求');
    }),

    // ========== 超时处理测试 ==========
    test('超时处理', async () => {
      const hitl = new HITLManager({
        timeout: 100, // 100ms 超时
        verbose: false,
      });
      
      const requestPromise = hitl.createApprovalRequest('file-write', {}, '测试');
      
      // 等待超时
      const result = await requestPromise;
      
      if (result.approved) throw new Error('超时应该默认拒绝');
      if (result.request.status !== 'rejected') throw new Error('状态应该是 rejected');
      
      console.log('✅ 超时处理');
    }),

    test('超时回调 - 自动批准', async () => {
      const hitl = new HITLManager({
        timeout: 100,
        onTimeout: async (request) => 'approve',
        verbose: false,
      });
      
      const requestPromise = hitl.createApprovalRequest('file-write', {}, '测试');
      
      const result = await requestPromise;
      
      if (!result.approved) throw new Error('超时回调应该批准');
      if (!result.request.responseReason?.includes('超时')) throw new Error('原因应该包含超时');
      
      console.log('✅ 超时回调 - 自动批准');
    }),

    test('超时回调 - 自动拒绝', async () => {
      const hitl = new HITLManager({
        timeout: 100,
        onTimeout: async (request) => 'reject',
        verbose: false,
      });
      
      const requestPromise = hitl.createApprovalRequest('file-write', {}, '测试');
      
      const result = await requestPromise;
      
      if (result.approved) throw new Error('超时回调应该拒绝');
      
      console.log('✅ 超时回调 - 自动拒绝');
    }),

    // ========== 事件系统测试 ==========
    test('事件监听器 - approval-request', async () => {
      const hitl = new HITLManager({ verbose: false });
      let eventTriggered = false;
      
      hitl.on('approval-request', (request) => {
        eventTriggered = true;
        if (!request.id) throw new Error('缺少请求 ID');
        if (request.toolName !== 'test-tool') throw new Error('工具名称错误');
      });
      
      const requestPromise = hitl.createApprovalRequest('test-tool', {});
      await hitl.approve(hitl.getPendingRequests()[0].id);
      await requestPromise;
      
      if (!eventTriggered) throw new Error('事件未触发');
      
      console.log('✅ 事件监听器 - approval-request');
    }),

    test('事件监听器 - approval-response', async () => {
      const hitl = new HITLManager({ verbose: false });
      let eventTriggered = false;
      
      hitl.on('approval-response', (request) => {
        eventTriggered = true;
        if (request.status !== 'approved') throw new Error('状态错误');
      });
      
      const requestPromise = hitl.createApprovalRequest('test-tool', {});
      const pending = hitl.getPendingRequests();
      await hitl.approve(pending[0].id);
      await requestPromise;
      
      if (!eventTriggered) throw new Error('事件未触发');
      
      console.log('✅ 事件监听器 - approval-response');
    }),

    // ========== 历史记录测试 ==========
    test('审批历史记录', async () => {
      const hitl = new HITLManager({ verbose: false });
      
      // 创建并处理 3 个请求
      for (let i = 0; i < 3; i++) {
        const requestPromise = hitl.createApprovalRequest('file-write', { index: i }, `测试${i}`);
        const pending = hitl.getPendingRequests();
        await hitl.approve(pending[0].id);
        await requestPromise;
      }
      
      const history = hitl.getHistory();
      if (history.length !== 3) throw new Error(`历史记录应该是 3 条，实际${history.length}`);
      
      console.log(`✅ 审批历史记录 (${history.length}条)`);
    }),

    test('统计信息', async () => {
      const hitl = new HITLManager({ verbose: false });
      
      // 创建 2 个批准 + 1 个拒绝
      for (let i = 0; i < 2; i++) {
        const requestPromise = hitl.createApprovalRequest('file-write', {}, `测试${i}`);
        const pending = hitl.getPendingRequests();
        await hitl.approve(pending[0].id);
        await requestPromise;
      }
      
      const rejectPromise = hitl.createApprovalRequest('file-write', {}, '拒绝测试');
      const pending = hitl.getPendingRequests();
      await hitl.reject(pending[0].id);
      await rejectPromise;
      
      const stats = hitl.getStats();
      
      if (stats.total !== 3) throw new Error(`总数应该是 3，实际${stats.total}`);
      if (stats.approved !== 2) throw new Error(`批准数应该是 2，实际${stats.approved}`);
      if (stats.rejected !== 1) throw new Error(`拒绝数应该是 1，实际${stats.rejected}`);
      if (stats.approvalRate !== '66.7') throw new Error(`批准率错误：${stats.approvalRate}`);
      
      console.log(`✅ 统计信息 (总数：${stats.total}, 批准率：${stats.approvalRate}%)`);
    }),

    test('清除历史记录', async () => {
      const hitl = new HITLManager({ verbose: false });
      
      // 创建 1 个请求
      const requestPromise = hitl.createApprovalRequest('file-write', {}, '测试');
      const pending = hitl.getPendingRequests();
      await hitl.approve(pending[0].id);
      await requestPromise;
      
      // 清除（0ms，立即清除）
      const removed = hitl.clearHistory(0);
      if (removed !== 1) throw new Error(`应该清除 1 条，实际${removed}`);
      
      const history = hitl.getHistory();
      if (history.length !== 0) throw new Error('历史记录应该为空');
      
      console.log('✅ 清除历史记录');
    }),

    // ========== 配置管理测试 ==========
    test('更新配置', async () => {
      const hitl = new HITLManager({ verbose: false });
      
      hitl.updateConfig({
        enabled: false,
        timeout: 60000,
      });
      
      if (hitl.options.enabled !== false) throw new Error('配置更新失败');
      if (hitl.options.timeout !== 60000) throw new Error('超时配置更新失败');
      
      console.log('✅ 更新配置');
    }),

    test('导出配置', async () => {
      const hitl = new HITLManager({
        requireApproval: ['file-write'],
        autoApprove: ['file-read'],
        timeout: 60000,
        verbose: false,
      });
      
      const config = hitl.exportConfig();
      
      if (!config.enabled) throw new Error('缺少 enabled');
      if (!config.requireApproval.includes('file-write')) throw new Error('缺少 requireApproval');
      if (!config.autoApprove.includes('file-read')) throw new Error('缺少 autoApprove');
      if (config.timeout !== 60000) throw new Error('timeout 错误');
      
      console.log('✅ 导出配置');
    }),

    test('重置状态', async () => {
      const hitl = new HITLManager({ verbose: false });
      
      // 创建 1 个待处理请求
      hitl.createApprovalRequest('file-write', {}, '测试');
      
      // 重置
      hitl.reset();
      
      const pending = hitl.getPendingRequests();
      if (pending.length !== 0) throw new Error('待处理请求应该被清除');
      
      const history = hitl.getHistory();
      if (history.length !== 0) throw new Error('历史记录应该被清除');
      
      console.log('✅ 重置状态');
    }),

    // ========== 集成测试 ==========
    test('集成测试 - 回调确认', async () => {
      let callbackCalled = false;
      
      const hitl = new HITLManager({
        onApprovalRequired: async (request) => {
          callbackCalled = true;
          // 模拟用户确认
          return request.params.approve || false;
        },
        verbose: false,
      });
      
      // 测试批准
      const result1 = await hitl.createApprovalRequest('file-write', { approve: true });
      if (!result1.approved) throw new Error('应该批准');
      
      // 测试拒绝
      const result2 = await hitl.createApprovalRequest('file-write', { approve: false });
      if (result2.approved) throw new Error('应该拒绝');
      
      if (!callbackCalled) throw new Error('回调未调用');
      
      console.log('✅ 集成测试 - 回调确认');
    }),
  ];

  // 运行测试
  let passed = 0;
  let failed = 0;

  for (const { name, fn } of tests) {
    try {
      await fn();
      passed++;
    } catch (error) {
      console.log(`❌ ${name}`);
      console.log(`   ${error.message}`);
      failed++;
    }
  }

  // 汇总结果
  console.log('=' .repeat(50));
  console.log(`📊 测试结果：${passed} passed, ${failed} failed`);
  console.log(`✅ 通过率：${((passed / tests.length) * 100).toFixed(1)}%`);

  if (failed > 0) {
    process.exit(1);
  }
}

// 运行测试
runTests().catch(error => {
  console.error('测试执行失败:', error);
  process.exit(1);
});
