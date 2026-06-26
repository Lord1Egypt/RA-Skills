---
name: safe-guardian
description: "A safe security layer plugin for OpenClaw that intercepts dangerous tool calls (exec, write, edit) through multi-layer blacklist/whitelist filtering and intent validation with comprehensive audit logs."
version: 1.1.0
---

# Safe Guardian

## 📖 功能描述

Safe Guardian 是一个安全的 OpenClaw 安全层插件，通过多层次的过滤机制拦截危险的工具调用（`exec`、`write`、`edit`），确保 AI 代理操作的安全性。

**核心价值**：防止 AI 代理执行危险操作，提供透明的安全审计和灵活的配置。

---

## ✨ 核心功能

### 1. **黑名单过滤** 🚫
- **两级正则表达式黑名单**：第一级（严格模式）和第二级（宽松模式）
- **默认包含常见危险命令**：如 `rm -rf`、`dd if`、格式化命令等
- **自定义规则**：支持添加自定义危险模式

### 2. **意图验证** 🧠
- 基于 LLM 的安全意图分析
- 验证工具调用的语义安全性
- 检测潜在的恶意意图

### 3. **审计日志** 📝
- 完整的操作审计日志
- 记录所有被阻止和允许的操作
- 支持日志导出和查询

### 4. **策略配置** ⚙️
- **安全模式**：严格模式，只允许白名单操作
- **宽松模式**：宽松模式，黑名单过滤
- **混合模式**：黑名单 + 意图验证
- **自定义规则**：支持 JSON 配置

---

## 🚀 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install safe-guardian

# 或本地安装
npm install safe-guardian
```

### 基本使用

```javascript
const SafeGuardian = require('safe-guardian');
const guardian = new SafeGuardian({
  mode: 'strict' // 'strict' | 'loose' | 'hybrid'
});

// 检查工具调用安全性
const result = guardian.checkToolCall('exec', {
  command: 'rm -rf /var/log'
});

if (!result.allowed) {
  console.log('❌ 操作被阻止:', result.reason);
} else {
  console.log('✅ 操作允许:', result.details);
}
```

---

## 📚 详细使用方法

### 1. 初始化配置

#### 基础配置
```javascript
const guardian = new SafeGuardian({
  // 模式选择
  mode: 'strict',  // 'strict' | 'loose' | 'hybrid'

  // 日志配置
  logPath: './logs/guardian.log',

  // 是否启用审计日志
  enableAudit: true,

  // 安全级别
  safetyLevel: 'high'  // 'low' | 'medium' | 'high'
});
```

#### 高级配置
```javascript
const guardian = new SafeGuardian({
  mode: 'hybrid',

  // 黑名单配置
  blacklist: {
    enabled: true,
    patterns: [
      /rm\s+-rf\s+\/?/,
      /dd\s+if=.*of=.*status=noerror/,
      /mkfs\.\w+\s+\/\w+/
    ]
  },

  // 白名单配置
  whitelist: {
    enabled: false,  // 严格模式下推荐启用白名单
    patterns: [
      /ls\s+-la/,
      /cat\s+\//path/to/file/
    ]
  },

  // LLM 配置（意图验证）
  llm: {
    enabled: true,
    model: 'qwen2.5:3b',
    apiKey: 'your-api-key'
  },

  // 审计配置
  audit: {
    includeToolCalls: true,
    includeReasons: true,
    includeTimestamps: true
  }
});
```

### 2. 工具调用检查

#### 检查 exec 命令
```javascript
// 危险命令（会被阻止）
const result1 = guardian.checkToolCall('exec', {
  command: 'rm -rf /var/log',
  args: ['*.log']
});
// 结果: { allowed: false, reason: '安全检查失败：命令包含危险模式' }

// 安全命令（会被允许）
const result2 = guardian.checkToolCall('exec', {
  command: 'ls -la /var/log',
  args: []
});
// 结果: { allowed: true, details: '命令通过安全检查' }
```

#### 检查 write 操作
```javascript
// 危险写操作
const result = guardian.checkToolCall('write', {
  path: '/etc/shadow',
  content: 'root:$1$...'
});
// 结果: { allowed: false, reason: '尝试写入系统核心文件' }
```

#### 检查 edit 操作
```javascript
// 危险编辑
const result = guardian.checkToolCall('edit', {
  path: '/etc/passwd',
  changes: [
    { field: 'root', value: 'admin' }
  ]
});
// 结果: { allowed: false, reason: '修改系统配置文件风险高' }
```

### 3. 获取安全报告

```javascript
// 获取整体安全报告
const report = guardian.getSecurityReport();

console.log(report);

// 输出示例:
/*
{
  totalChecks: 150,
  allowed: 145,
  blocked: 5,
  blockedReasons: {
    '危险命令': 3,
    '系统文件访问': 2
  },
  safetyScore: 0.967,
  lastCheck: '2026-04-06T22:00:00Z',
  recommendations: [
    '建议检查更多 rm 命令的使用',
    '可以考虑启用白名单模式'
  ]
}
*/
```

### 4. 添加自定义规则

#### 添加黑名单规则
```javascript
// 方式1: 使用字符串模式
guardian.addBlacklistPattern(/pkill.*all/);

// 方式2: 使用正则对象
guardian.addBlacklistPattern({
  pattern: /reboot/,
  description: '防止意外重启',
  severity: 'high'
});

// 方式3: 批量添加
guardian.addBlacklistPatterns([
  /shutdown/,
  /halt/,
  /reboot/,
  /poweroff/
]);
```

#### 添加白名单规则
```javascript
guardian.addWhitelistPattern(/cat\s+\/etc\/hosts/);
guardian.addWhitelistPattern(/ls\s+\/var\/log/);
```

### 5. 审计日志

```javascript
// 获取审计日志
const logs = guardian.getAuditLogs({
  limit: 50,
  filter: { action: 'blocked' }
});

console.log(logs);

// 导出审计日志
guardian.exportAuditLog('./audit-report.json');

// 清空审计日志
guardian.clearAuditLogs();
```

---

## 🎯 使用场景

### 场景 1: Web 应用的脚本执行安全

```javascript
const guardian = new SafeGuardian({
  mode: 'loose'
});

// 用户提交的脚本
const userInput = document.getElementById('script').value;

// 检查脚本安全性
const result = guardian.checkToolCall('exec', {
  command: userInput
});

if (!result.allowed) {
  alert('脚本不安全，已被阻止: ' + result.reason);
} else {
  executeScript(userInput);
}
```

### 场景 2: AI 代理自动化运维

```javascript
const guardian = new SafeGuardian({
  mode: 'hybrid',
  safetyLevel: 'high'
});

// AI 代理要执行的操作
const aiOperation = {
  type: 'exec',
  command: 'tail -f /var/log/app.log',
  context: '查看应用日志'
};

// 安全检查
const result = guardian.checkToolCall(aiOperation.type, aiOperation);

if (!result.allowed) {
  // 回退到安全方案
  return {
    allowed: false,
    alternative: '使用 `cat /var/log/app.log | tail -n 100` 替代'
  };
}
```

### 场景 3: 自动化文件管理

```javascript
const guardian = new SafeGuardian({
  mode: 'strict',
  whitelist: {
    enabled: true,
    patterns: [
      /cp\s+.*\s+\/backup\//,
      /mv\s+.*\s+\/archive\//,
      /ls\s+/home\/user\//
    ]
  }
});

// 文件操作
const result = guardian.checkToolCall('write', {
  path: '/home/user/documents/new.txt',
  content: 'Hello World'
});

if (result.allowed) {
  fs.writeFileSync(result.path, result.content);
}
```

---

## ⚙️ 配置文件

Safe Guardian 支持通过配置文件进行初始化。

### 配置文件格式 (config.json)

```json
{
  "mode": "hybrid",
  "safetyLevel": "high",
  "blacklist": {
    "enabled": true,
    "patterns": [
      "rm -rf /",
      "dd if=/dev/zero",
      "mkfs.*"
    ]
  },
  "whitelist": {
    "enabled": false,
    "patterns": []
  },
  "llm": {
    "enabled": true,
    "model": "qwen2.5:3b"
  },
  "audit": {
    "enabled": true,
    "logPath": "./logs/guardian.log"
  }
}
```

### 使用配置文件初始化

```javascript
const guardian = new SafeGuardian('./config.json');
```

---

## 🔒 安全特性

| 特性 | 说明 |
|------|------|
| **多层过滤** | 黑名单 + 意图验证 + 白名单 |
| **灵活配置** | 支持多种安全模式 |
| **审计追踪** | 完整的操作日志 |
| **自定义规则** | 支持添加自定义规则 |
| **向后兼容** | 默认配置安全且实用 |
| **性能优化** | 高效的规则匹配算法 |

---

## 📊 安全评分

Guardian 会计算**安全评分**（0-1）：

```
安全评分 = (允许操作数 / 总操作数) * 100%
```

**评分等级**：
- ✅ **优秀** (90-100): 安全操作占比高
- ✅ **良好** (70-89): 基本安全，可接受
- ⚠️ **警告** (50-69): 需要关注
- ❌ **危险** (0-49): 存在安全隐患

---

## 🛠️ 开发与测试

### 运行测试

```bash
# 安装依赖
npm install

# 运行测试套件
npm test
```

### 测试示例

```javascript
// test.js
const guardian = new SafeGuardian();

// 测试 1: 危险命令
console.log(guardian.checkToolCall('exec', { command: 'rm -rf /' }));

// 测试 2: 安全命令
console.log(guardian.checkToolCall('exec', { command: 'ls -la' }));

// 测试 3: 白名单
guardian.addWhitelistPattern(/ls\s+-la/);
console.log(guardian.checkToolCall('exec', { command: 'ls -la' }));

// 测试 4: 获取报告
console.log(guardian.getSecurityReport());
```

---

## 📝 API 参考

### 构造函数
```javascript
new SafeGuardian(config?)
```

**参数**:
- `config` (Object): 配置对象

### 方法

| 方法 | 返回 | 说明 |
|------|------|------|
| `checkToolCall(type, data)` | Object | 检查工具调用安全性 |
| `addBlacklistPattern(pattern)` | void | 添加黑名单规则 |
| `removeBlacklistPattern(pattern)` | void | 移除黑名单规则 |
| `addWhitelistPattern(pattern)` | void | 添加白名单规则 |
| `getSecurityReport()` | Object | 获取安全报告 |
| `getAuditLogs(filter?)` | Array | 获取审计日志 |
| `exportAuditLog(path)` | void | 导出审计日志 |
| `clearAuditLogs()` | void | 清空审计日志 |

### checkToolCall 返回值

```typescript
{
  allowed: boolean,      // 是否允许
  reason: string,        // 阻止原因
  details: Object,       // 详细信息
  timestamp: string     // 时间戳
}
```

---

## 📖 使用示例

### 完整示例：AI 代理安全执行

```javascript
const SafeGuardian = require('safe-guardian');
const { exec } = require('child_process');

// 初始化安全守护者
const guardian = new SafeGuardian({
  mode: 'hybrid',
  safetyLevel: 'high'
});

// 安全执行函数
async function safeExec(command) {
  const result = guardian.checkToolCall('exec', { command });

  if (!result.allowed) {
    console.error('❌ 拒绝执行:', command);
    console.error('原因:', result.reason);
    return null;
  }

  console.log('✅ 允许执行:', command);
  return new Promise((resolve, reject) => {
    exec(command, (error, stdout, stderr) => {
      if (error) reject(error);
      else resolve(stdout);
    });
  });
}

// 使用
safeExec('ls -la')
  .then(output => console.log('输出:', output))
  .catch(error => console.error('错误:', error));
```

---

## 🐛 常见问题

### Q1: 为什么某些命令被阻止？

**A**: 可能是以下原因：
1. 匹配黑名单中的危险模式
2. 尝试访问系统核心文件
3. 修改关键系统配置

解决方案：
- 检查配置文件中的规则
- 将需要的安全命令添加到白名单
- 在意图验证中添加自定义规则

### Q2: 如何禁用某个特定检查？

**A**: 使用白名单配置：

```javascript
const guardian = new SafeGuardian({
  whitelist: {
    enabled: true,
    patterns: [
      /特定的安全命令/
    ]
  }
});
```

### Q3: 日志太大怎么办？

**A**: 定期清理和导出日志：

```javascript
// 导出并清理
guardian.exportAuditLog('./backup/audit-' + Date.now() + '.json');
guardian.clearAuditLogs();
```

---

## 📄 许可证

MIT-0 License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📞 联系方式

- Issue: https://github.com/your-repo/safe-guardian/issues
- 文档: https://docs.your-repo.com/safe-guardian

---

## 🎉 更新日志

### v1.1.0 (2026-04-06)
- ✨ 添加详细的中文文档和使用示例
- ✨ 改进安全评分算法
- ✨ 优化审计日志功能
- 🐛 修复某些正则匹配问题

### v1.0.0 (2026-04-05)
- 🎉 初始版本发布
