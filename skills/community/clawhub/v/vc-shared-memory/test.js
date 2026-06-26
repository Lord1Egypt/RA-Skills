#!/usr/bin/env node

/**
 * Shared Memory 测试脚本
 * 
 * 测试覆盖：
 * 1. 基础操作：Write / Read / Update / Delete / Search
 * 2. 公告板 API
 * 3. 项目协作 API
 * 4. 知识库 API
 * 5. 员工状态 API
 * 6. 跨团队链接 API
 * 7. 备份/恢复功能
 * 8. 为员工构建上下文
 */

const { SharedMemory } = require('./shared-memory.js');

// 测试结果统计
let passed = 0;
let failed = 0;
const results = [];

/**
 * 运行单个测试
 */
function test(name, fn) {
  try {
    fn();
    passed++;
    results.push({ name, status: '✅ PASS', error: null });
    console.log(`✅ ${name}`);
  } catch (error) {
    failed++;
    results.push({ name, status: '❌ FAIL', error: error.message });
    console.log(`❌ ${name}: ${error.message}`);
  }
}

/**
 * 断言函数
 */
function assertEqual(actual, expected, message = '') {
  if (actual !== expected) {
    throw new Error(`${message} Expected ${expected}, got ${actual}`);
  }
}

function assertExists(value, message = '') {
  if (!value) {
    throw new Error(`${message} Value should exist`);
  }
}

function assertArrayLength(arr, expectedLength, message = '') {
  if (!Array.isArray(arr)) {
    throw new Error(`${message} Expected array, got ${typeof arr}`);
  }
  if (arr.length !== expectedLength) {
    throw new Error(`${message} Expected length ${expectedLength}, got ${arr.length}`);
  }
}

function assertContains(arr, value, message = '') {
  if (!Array.isArray(arr)) {
    throw new Error(`${message} Expected array`);
  }
  if (!arr.includes(value)) {
    throw new Error(`${message} Array should contain ${value}`);
  }
}

// ============================================================================
// 测试套件
// ============================================================================

console.log('\n🧪 Shared Memory 测试开始\n');
console.log('=' .repeat(60));

// 初始化测试实例
const sm = new SharedMemory();

// ----------------------------------------------------------------------------
// 测试 1: 基础操作 - Write
// ----------------------------------------------------------------------------
test('Write - 创建公告', () => {
  const result = sm.write({
    type: 'announcement',
    data: {
      type: 'decision',
      title: '测试公告标题',
      content: '测试公告内容',
      author: 'CEO马云',
      priority: 'high',
      visibleTo: ['all']
    }
  });
  
  assertExists(result.id, '公告应有 ID');
  assertExists(result.createdAt, '公告应有创建时间');
  assertEqual(result.title, '测试公告标题', '标题应匹配');
});

test('Write - 创建经验教训', () => {
  const result = sm.write({
    type: 'lesson',
    data: {
      category: '技术',
      title: 'Gateway 超时根因',
      content: 'TIME_WAIT 连接堆积导致超时',
      learnedBy: '技术大拿',
      team: '技术中台团队',
      importance: 'high'
    }
  });
  
  assertExists(result.id, '经验应有 ID');
  assertEqual(result.category, '技术', '类别应匹配');
});

test('Write - 创建最佳实践', () => {
  const result = sm.write({
    type: 'bestPractice',
    data: {
      category: '开发',
      title: '代码审查最佳实践',
      content: '每次提交前先审查自己的代码',
      createdBy: '程序员',
      tags: ['代码', '审查']
    }
  });
  
  assertExists(result.id, '最佳实践应有 ID');
  assertContains(result.tags, '代码', '标签应包含"代码"');
});

// ----------------------------------------------------------------------------
// 测试 2: 基础操作 - Read
// ----------------------------------------------------------------------------
test('Read - 读取公告列表', () => {
  const results = sm.read({
    type: 'announcement',
    limit: 10
  });
  
  assertArrayLength(results, 1, '应有1条公告');
  assertEqual(results[0].title, '测试公告标题', '第一条公告标题应匹配');
});

test('Read - 按优先级过滤公告', () => {
  const results = sm.read({
    type: 'announcement',
    filter: { priority: 'high' },
    limit: 10
  });
  
  assertArrayLength(results, 1, '应有1条高优先级公告');
});

test('Read - 读取经验教训列表', () => {
  const results = sm.read({
    type: 'lesson',
    limit: 10
  });
  
  assertArrayLength(results, 1, '应有1条经验教训');
});

// ----------------------------------------------------------------------------
// 测试 3: 基础操作 - Update
// ----------------------------------------------------------------------------
test('Update - 更新公告', () => {
  // 先读取第一条公告的 ID
  const announcements = sm.read({ type: 'announcement', limit: 1 });
  const annId = announcements[0].id;
  
  const result = sm.update({
    type: 'announcement',
    id: annId,
    updates: { priority: 'critical' },
    by: 'CEO马云'
  });
  
  assertEqual(result.priority, 'critical', '优先级应更新为 critical');
  assertExists(result.updatedAt, '应有更新时间');
});

test('Update - 更新最佳实践应用次数', () => {
  const practices = sm.read({ type: 'bestPractice', limit: 1 });
  const bpId = practices[0].id;
  
  const result = sm.update({
    type: 'bestPractice',
    id: bpId,
    updates: { appliedCount: 5 },
    by: '程序员'
  });
  
  assertEqual(result.appliedCount, 5, '应用次数应为5');
});

// ----------------------------------------------------------------------------
// 测试 4: 基础操作 - Search
// ----------------------------------------------------------------------------
test('Search - 搜索公告', () => {
  const results = sm.search({
    query: '测试',
    types: ['announcement'],
    limit: 10
  });
  
  assertArrayLength(results, 1, '应有1条搜索结果');
  assertEqual(results[0]._type, 'announcement', '类型应为 announcement');
});

test('Search - 全类型搜索', () => {
  const results = sm.search({
    query: 'Gateway',
    types: ['lesson', 'announcement'],
    limit: 10
  });
  
  assertArrayLength(results, 1, '应有1条搜索结果');
});

// ----------------------------------------------------------------------------
// 测试 5: 公告板 API
// ----------------------------------------------------------------------------
test('announce() - 发布公告', () => {
  const result = sm.announce({
    title: '新战略方向',
    content: '聚焦 OpenClaw 变现',
    type: 'strategy',
    priority: 'critical',
    author: 'CEO马云'
  });
  
  assertExists(result.id, '公告应有 ID');
  assertEqual(result.type, 'strategy', '类型应为 strategy');
});

test('getAnnouncements() - 获取公告', () => {
  const results = sm.getAnnouncements({ limit: 10 });
  
  assertExists(results.length > 0, '应有公告');
});

test('markRead() - 标记已读', () => {
  const announcements = sm.read({ type: 'announcement', limit: 1 });
  const annId = announcements[0].id;
  
  sm.markRead(annId, '市场猎手');
  
  const updated = sm.read({ type: 'announcement', filter: { id: annId } })[0];
  assertContains(updated.readBy, '市场猎手', 'readBy 应包含"市场猎手"');
});

// ----------------------------------------------------------------------------
// 测试 6: 项目协作 API
// ----------------------------------------------------------------------------
test('createProject() - 创建项目', () => {
  const result = sm.createProject({
    name: 'OpenClaw 变现项目',
    teams: ['搞钱特战队', '软件开发团队'],
    members: [
      { name: '市场猎手', role: '市场分析' },
      { name: '程序员', role: '开发实现' }
    ],
    createdBy: 'CEO马云'
  });
  
  assertExists(result.id, '项目应有 ID');
  assertEqual(result.status, 'active', '状态应为 active');
  assertContains(result.teams, '搞钱特战队', '应包含搞钱特战队');
});

test('updateProject() - 更新项目进展', () => {
  const projects = sm.getProjects({ status: 'active', limit: 1 });
  const projId = projects[0].id;
  
  const result = sm.updateProject(projId, {
    content: '市场分析已完成',
    type: 'progress',
    by: '市场猎手'
  });
  
  assertExists(result.updates, '应有 updates');
  assertArrayLength(result.updates, 1, '应有1条进展记录');
});

test('assignTask() - 分配任务', () => {
  const projects = sm.getProjects({ status: 'active', limit: 1 });
  const projId = projects[0].id;
  
  const result = sm.assignTask(projId, {
    to: '程序员',
    task: {
      description: '开发变现功能',
      deadline: '2026-04-15'
    },
    by: 'CEO马云'
  });
  
  assertArrayLength(result.tasks, 1, '应有1条任务');
  assertEqual(result.tasks[0].assignedTo, '程序员', '任务应分配给程序员');
});

test('getProjects() - 获取项目列表', () => {
  const results = sm.getProjects({ status: 'active' });
  
  assertExists(results.length > 0, '应有活跃项目');
});

// ----------------------------------------------------------------------------
// 测试 7: 知识库 API
// ----------------------------------------------------------------------------
test('recordLesson() - 记录经验教训', () => {
  const result = sm.recordLesson({
    category: '市场',
    title: '抖音获客渠道分析',
    content: '短视频带货转化率高',
    learnedBy: '市场猎手',
    team: '搞钱特战队',
    importance: 'high'
  });
  
  assertExists(result.id, '经验应有 ID');
  assertEqual(result.category, '市场', '类别应为市场');
});

test('addBestPractice() - 添加最佳实践', () => {
  const result = sm.addBestPractice({
    category: '运营',
    title: '定时任务管理最佳实践',
    content: '使用守护进程 + 定时任务双重保障',
    createdBy: '技术老人',
    tags: ['定时任务', '守护进程']
  });
  
  assertExists(result.id, '最佳实践应有 ID');
});

test('searchKnowledge() - 搜索知识库', () => {
  const results = sm.searchKnowledge({
    query: '抖音',
    limit: 10
  });
  
  assertExists(results.length > 0, '应有搜索结果');
});

test('getBestPractices() - 获取最佳实践', () => {
  const results = sm.getBestPractices({ limit: 10 });
  
  assertExists(results.length > 0, '应有最佳实践');
});

// ----------------------------------------------------------------------------
// 测试 8: 员工状态 API
// ----------------------------------------------------------------------------
test('updateEmployeeStatus() - 更新员工状态', () => {
  const result = sm.updateEmployeeStatus({
    name: '市场猎手',
    team: '搞钱特战队',
    task: {
      description: '分析抖音获客渠道',
      project: 'OpenClaw 变现项目'
    },
    availability: 'busy',
    workload: 0.7
  });
  
  assertEqual(result.name, '市场猎手', '员工名应匹配');
  assertEqual(result.availability, 'busy', '状态应为 busy');
});

test('findAvailableEmployees() - 查找可用员工', () => {
  // 先设置一个可用员工
  sm.updateEmployeeStatus({
    name: '程序员',
    team: '软件开发团队',
    availability: 'available',
    workload: 0.2
  });
  
  const results = sm.findAvailableEmployees({ workload: '<0.5' });
  
  assertExists(results.length > 0, '应有可用员工');
  assertContains(results.map(e => e.name), '程序员', '应包含程序员');
});

test('requestCollaboration() - 发送协作请求', () => {
  const result = sm.requestCollaboration({
    from: '市场猎手',
    to: '程序员',
    project: 'OpenClaw 变现项目',
    reason: '需要技术实现市场方案'
  });
  
  assertExists(result.id, '协作请求应有 ID');
  assertEqual(result.status, 'pending', '状态应为 pending');
});

test('getEmployeeStatuses() - 获取员工状态列表', () => {
  const results = sm.getEmployeeStatuses();
  
  assertExists(results.length >= 2, '应有至少2个员工状态');
});

// ----------------------------------------------------------------------------
// 测试 9: 跨团队链接 API
// ----------------------------------------------------------------------------
test('recordTeamSync() - 记录跨团队同步', () => {
  const result = sm.recordTeamSync({
    fromTeam: '搞钱特战队',
    toTeam: '软件开发团队',
    type: '项目启动',
    content: '变现项目已启动，需要开发支持',
    participants: ['市场猎手', '程序员']
  });
  
  assertExists(result.id, '同步记录应有 ID');
  assertEqual(result.fromTeam, '搞钱特战队', '来源团队应匹配');
});

test('recordMeeting() - 记录会议纪要', () => {
  const result = sm.recordMeeting({
    title: 'OpenClaw 变现项目启动会',
    participants: ['CEO马云', '市场猎手', '程序员'],
    summary: '确定变现战略方向',
    decisions: ['聚焦抖音获客'],
    actionItems: ['市场分析', '技术开发']
  });
  
  assertExists(result.id, '会议纪要应有 ID');
  assertArrayLength(result.decisions, 1, '应有1条决策');
});

test('getCrossTeamLinks() - 获取跨团队链接', () => {
  const result = sm.getCrossTeamLinks({ limit: 10 });
  
  assertExists(result.syncs, '应有 syncs');
  assertExists(result.notes, '应有 notes');
});

// ----------------------------------------------------------------------------
// 测试 10: 为员工构建上下文
// ----------------------------------------------------------------------------
test('getContextFor() - 为员工构建上下文', () => {
  const context = sm.getContextFor('市场猎手', { team: '搞钱特战队' });
  
  assertExists(context, '应有上下文');
  assertExists(context.includes('共享记忆上下文'), '应包含标题');
  assertExists(context.includes('公司公告'), '应包含公告部分');
  assertExists(context.includes('相关项目'), '应包含项目部分');
  assertExists(context.includes('市场猎手'), '应包含员工名');
});

test('getContextFor() - 上下文应包含最新公告', () => {
  const context = sm.getContextFor('程序员');
  
  assertExists(context.includes('新战略方向'), '应包含最新公告标题');
});

// ----------------------------------------------------------------------------
// 测试 11: 备份功能
// ----------------------------------------------------------------------------
test('backup() - 创建备份', () => {
  const result = sm.backup();
  
  assertExists(result.timestamp, '备份应有时间戳');
  assertExists(result.filesCount > 0, '应有备份文件');
});

test('listBackups() - 查看备份列表', () => {
  const results = sm.listBackups();
  
  assertExists(results.length >= 1, '应有至少1个备份');
  assertExists(results[0].timestamp, '备份应有时间戳');
});

// ----------------------------------------------------------------------------
// 测试 12: 统计功能
// ----------------------------------------------------------------------------
test('getStats() - 获取统计数据', () => {
  const stats = sm.getStats();
  
  assertExists(stats, '应有统计数据');
  assertExists(stats.announcements >= 2, '应有至少2条公告');
  assertExists(stats.lessons >= 2, '应有至少2条经验');
  assertExists(stats.projects.active >= 1, '应有至少1个活跃项目');
  assertExists(stats.employees.total >= 2, '应有至少2个员工状态');
  assertExists(stats.backups >= 1, '应有至少1个备份');
});

// ----------------------------------------------------------------------------
// 测试 13: Delete 操作（带归档）
// ----------------------------------------------------------------------------
test('Delete - 删除公告（带归档）', () => {
  const announcements = sm.read({ type: 'announcement', limit: 1 });
  const annId = announcements[0].id;
  
  const result = sm.delete({
    type: 'announcement',
    id: annId,
    by: 'CLI',
    archive: true
  });
  
  assertEqual(result.success, true, '删除应成功');
  assertEqual(result.archived, true, '应已归档');
  
  // 验证公告已删除
  const remaining = sm.read({ type: 'announcement', filter: { id: annId } });
  assertArrayLength(remaining, 0, '公告应已删除');
});

// ----------------------------------------------------------------------------
// 清理测试数据
// ----------------------------------------------------------------------------
test('清理测试数据', () => {
  // 删除所有测试数据
  const announcements = sm.read({ type: 'announcement' });
  announcements.forEach(a => {
    sm.delete({ type: 'announcement', id: a.id, by: 'CLI', archive: false });
  });
  
  const lessons = sm.read({ type: 'lesson' });
  lessons.forEach(l => {
    sm.delete({ type: 'lesson', id: l.id, by: 'CLI', archive: false });
  });
  
  const practices = sm.read({ type: 'bestPractice' });
  practices.forEach(p => {
    sm.delete({ type: 'bestPractice', id: p.id, by: 'CLI', archive: false });
  });
  
  const projects = sm.getProjects({ status: 'active' });
  projects.forEach(p => {
    sm.delete({ type: 'project', id: p.id, by: 'CLI', archive: false });
  });
  
  const employees = sm.getEmployeeStatuses();
  employees.forEach(e => {
    sm.delete({ type: 'employeeStatus', id: e.name, by: 'CLI', archive: false });
  });
  
  console.log('  (已清理所有测试数据)');
});

// ============================================================================
// 输出测试结果
// ============================================================================

console.log('\n' + '=' .repeat(60));
console.log(`\n📊 测试结果: ${passed} ✅ PASS | ${failed} ❌ FAIL`);

if (failed > 0) {
  console.log('\n失败的测试:');
  results.filter(r => r.status === '❌ FAIL').forEach(r => {
    console.log(`  - ${r.name}: ${r.error}`);
  });
  process.exit(1);
} else {
  console.log('\n🎉 所有测试通过！');
  process.exit(0);
}