// 测试 Safe Guardian
const SafeGuardian = require('./index.js');

const guardian = new SafeGuardian();

console.log('🧪 测试 Safe Guardian...\n');

// 测试1: 安全的工具调用
console.log('1. 测试安全的工具调用:');
const safeCall = 'cat /var/log/syslog';
const result1 = guardian.checkToolCall(safeCall);
console.log('   工具调用:', safeCall);
console.log('   结果:', result1);
console.log('');

// 测试2: 危险的工具调用 (rm -rf)
console.log('2. 测试危险的工具调用 (rm -rf):');
const dangerousCall = 'rm -rf /var/log';
const result2 = guardian.checkToolCall(dangerousCall);
console.log('   工具调用:', dangerousCall);
console.log('   结果:', result2);
console.log('');

// 测试3: 危险的工具调用 (dd if=/dev)
console.log('3. 测试危险的工具调用 (dd if=/dev):');
const dangerousCall2 = 'dd if=/dev/zero of=/dev/sda';
const result3 = guardian.checkToolCall(dangerousCall2);
console.log('   工具调用:', dangerousCall2);
console.log('   结果:', result3);
console.log('');

// 测试4: 危险的工具调用 (mkfs)
console.log('4. 测试危险的工具调用 (mkfs):');
const dangerousCall3 = 'mkfs.ext4 /dev/sda1';
const result4 = guardian.checkToolCall(dangerousCall3);
console.log('   工具调用:', dangerousCall3);
console.log('   结果:', result4);
console.log('');

// 测试5: 系统修改操作
console.log('5. 测试系统修改操作 (useradd):');
const dangerousCall4 = 'useradd -m newuser';
const result5 = guardian.checkToolCall(dangerousCall4);
console.log('   工具调用:', dangerousCall4);
console.log('   结果:', result5);
console.log('');

// 测试6: 白名单功能
console.log('6. 测试白名单功能:');
guardian.addToWhitelist({
  command: 'cat /etc/passwd',
  reason: 'Admin monitoring'
});
const whitelistResult = guardian.checkToolCall('cat /etc/passwd');
console.log('   工具调用: cat /etc/passwd (白名单)');
console.log('   结果:', whitelistResult);
console.log('');

// 记录操作
console.log('7. 记录操作:');
const logResult1 = guardian.logOperation(result1, safeCall);
console.log('   已记录操作:', logResult1.timestamp);
const logResult2 = guardian.logOperation(result2, dangerousCall);
console.log('   已记录操作:', logResult2.timestamp);

// 获取安全报告
console.log('\n8. 安全报告:');
const report = guardian.getSecurityReport();
console.log('   总检查次数:', report.totalChecks);
console.log('   被阻止:', report.blocked);
console.log('   允许:', report.allowed);
console.log('   阻止率:', report.blockRate + '%');
console.log('   黑名单规则数:', report.blacklistRules);
console.log('   白名单条目数:', report.whitelistEntries);

// 获取审计日志
console.log('\n9. 审计日志:');
const logs = guardian.getAuditLog();
console.log('   日志条数:', logs.length);
if (logs.length > 0) {
  console.log('   最后一条日志:', logs[logs.length - 1].timestamp);
}

console.log('\n✅ Safe Guardian 测试完成!');
