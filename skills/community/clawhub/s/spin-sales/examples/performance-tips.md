# 🚀 Spin-Sales 技能性能优化指南

**最后更新**: 2026-05-18  
**适用版本**: v2.0+  

---

## 📋 目录

- [缓存机制配置](#-缓存机制配置)
- [异步处理优化](#-异步处理优化)
- [错误处理增强](#-错误处理增强)
- [文件加载策略](#-文件加载策略)
- [监控与调试](#-监控与调试)

---

## 📦 缓存机制配置

### 当前配置 (cache.js)

```javascript
class CacheManager {
  constructor() {
    this.cache = new Map();
    this.cacheTimeout = 300000; // 5 分钟缓存
  }
}
```

### ⚠️ 潜在问题

1. **缓存刷新策略单一**：仅基于时间戳，未考虑数据变更
2. **无内存限制**：Map 无限增长可能导致内存溢出
3. **缺少强制刷新机制**：无法手动清除缓存以更新内容

### ✅ 优化建议

#### 添加智能刷新策略

```javascript
class CacheManager {
  constructor() {
    this.cache = new Map();
    this.cacheTimeout = 300000; // 5 分钟基础缓存
    this.maxMemoryUsage = 10 * 1024 * 1024; // 最大内存限制：10MB
  }

  get(key) {
    const item = this.cache.get(key);
    if (!item) return null;
    
    // 检查时间过期
    if (Date.now() - item.timestamp > this.cacheTimeout) {
      this.cache.delete(key);
      return null;
    }
    
    // 内存检查
    if (this.checkMemoryUsage()) {
      // 内存充足，直接返回
      return item.value;
    } else {
      // 内存紧张，刷新缓存
      return this.refresh(key);
    }
  }

  set(key, value) {
    // 检查内存容量
    if (!this.checkMemoryUsage()) {
      console.warn('⚠️ 缓存内存接近上限，考虑立即清除旧缓存');
      this.clearOldCache();
    }
    
    this.cache.set(key, {
      value,
      timestamp: Date.now()
    });
  }

  // 检查内存使用
  checkMemoryUsage() {
    let totalSize = 0;
    for (const item of this.cache.values()) {
      totalSize += JSON.stringify(item.value).length;
    }
    return totalSize < this.maxMemoryUsage;
  }

  // 清除旧缓存（保留最近使用的）
  clearOldCache() {
    // 简单的 LRU 实现：按时间排序，删除最旧的 30%
    const keys = Array.from(this.cache.keys());
    const sortedKeys = keys.sort((a, b) => {
      return this.cache.get(b).timestamp - this.cache.get(a).timestamp;
    });
    
    const removeCount = Math.floor(sortedKeys.length * 0.3); // 删除最旧的 30%
    for (let i = 0; i < removeCount; i++) {
      this.cache.delete(sortedKeys[i]);
    }
  }

  // 强制刷新缓存
  refresh(key) {
    const cachedContent = this.get(key);
    if (cachedContent) return cachedContent;
    
    const filePath = key.replace(/^file:/, '');
    try {
      const content = fs.promises.readFile(filePath, 'utf8');
      this.set(key, content);
      return content;
    } catch (error) {
      throw new Error(`无法读取文件 ${filePath}: ${error.message}`);
    }
  }

  clear() {
    this.cache.clear();
  }
}
```

---

## ⚡ 异步处理优化

### 当前实现分析

检查 `index.js` 中的主要方法是否使用了正确的 async/await：

```javascript
async initialize() { ... }      // ✅ 正确
async executeOpening() { ... }   // ✅ 正确  
async executeStage(stage) { ... } // ✅ 正确
```

### ✅ 进一步优化建议

#### 1. 批量文件读取优化

```javascript
// ❌ 串行读取（慢）
for (const file of files) {
  const content = await cacheManager.getFileContent(file);
}

// ✅ 并行读取（快）
const promises = files.map(file => 
  cacheManager.getFileContent(file).catch(err => ({ error: err.message }))
);
const results = await Promise.all(promises);
```

#### 2. 设置合理的超时时间

```javascript
async getFileContentWithTimeout(filePath, timeoutMs = 5000) {
  try {
    return await Promise.race([
      this.getFileContent(filePath),
      new Promise((_, reject) => 
        setTimeout(() => reject(new Error(`文件读取超时 (${filePath})`)), timeoutMs)
      )
    ]);
  } catch (error) {
    if (error.message.includes('超时')) throw error;
    throw new Error(`无法读取文件 ${filePath}: ${error.message}`);
  }
}
```

#### 3. 优雅的错误处理

```javascript
async executeStageWithRetry(stage, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await this.executeStage(stage);
      return { success: true, data: result };
    } catch (error) {
      if (attempt === maxRetries) {
        throw error; // 最后尝试失败，抛出异常
      }
      console.warn(`⚠️ 阶段 "${stage}" 执行第${attempt}次失败：${error.message}`);
      
      // 指数退避等待
      await this.sleep(Math.pow(2, attempt) * 1000);
    }
  }
}

sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

---

## 🛡️ 错误处理增强

### 当前实现

检查 `index.js` 中的错误捕获：

```javascript
try {
  // 执行逻辑
} catch (error) {
  console.error(error);
  return { success: false, error: error.message };
}
```

### ✅ 优化建议

#### 分类错误处理

```javascript
// 定义错误类型
const ERROR_TYPES = {
  FILE_NOT_FOUND: 'FILE_NOT_FOUND',
  INVALID_DATA: 'INVALID_DATA',
  TIMEOUT: 'TIMEOUT',
  UNEXPECTED: 'UNEXPECTED'
};

// 在 catch 块中使用
catch (error) {
  let errorType = ERROR_TYPES.UNEXPECTED;
  let errorMessage = error.message;
  
  // 识别错误类型
  if (error.code === 'ENOENT') {
    errorType = ERROR_TYPES.FILE_NOT_FOUND;
    errorMessage = `文件未找到：${error.path}`;
  } else if (error.name === 'TimeoutError') {
    errorType = ERROR_TYPES.TIMEOUT;
    errorMessage = `操作超时`;
  } else if (typeof error.data === 'object') {
    try {
      const code = JSON.parse(error.message)?.code;
      if (code === 'INVALID_INPUT') {
        errorType = ERROR_TYPES.INVALID_DATA;
        errorMessage = error.data.message || '输入数据无效';
      }
    } catch {}
  }
  
  // 记录日志
  console.error(`[${errorType}] ${errorMessage}`);
  
  // 返回结构化错误信息
  return {
    success: false,
    errorType,
    errorMessage,
    timestamp: new Date().toISOString()
  };
}
```

---

## 📁 文件加载策略

### 当前缓存行为分析

- ✅ 使用 Map 存储已读文件内容
- ✅ 支持时间戳过期检查
- ⚠️ 无懒加载机制，所有文件在初始化时可能被一次性读取

### ✅ 优化建议

#### 1. 按需加载策略

```javascript
// ❌ 同步加载所有内容（内存占用大）
const sQuestions = await cacheManager.getJsonContent('references/s-questions.md');
const pQuestions = await cacheManager.getJsonContent('references/p-questions.md');
// ...

// ✅ 懒加载（按需读取）
class LazyLoader {
  constructor(cacheManager) {
    this.cache = cacheManager;
  }
  
  async loadIfNotCached(filePath) {
    if (!this.cache.get(filePath)) {
      const content = await this.cache.getFileContent(filePath);
      console.log(`✅ 加载文件：${filePath}`);
    }
    return this.cache.get(filePath);
  }
}
```

#### 2. 优先加载核心文件

```javascript
const CORE_FILES = [
  'references/s-questions.md',
  'references/p-questions.md',
  'config.json'
];

async initializeCore() {
  for (const file of CORE_FILES) {
    await cacheManager.getFileContent(file);
  }
}

// 在 index.js 的 initialize 方法中调用
await this.initialize();
await this.initializeCore(); // 优先加载核心文件
```

---

## 🔍 监控与调试

### 创建性能监控工具

创建 `scripts/perf-monitor.js`:

```javascript
#!/usr/bin/env node

/**
 * Spin-Sales 性能监控工具
 */

import fs from 'fs';
import path from 'path';

const __filename = path.dirname(fileURLToPath(import.meta.url));

class PerfMonitor {
  constructor() {
    this.startTime = Date.now();
    this.fileReads = [];
    this.errors = [];
  }

  recordFileRead(filePath, duration) {
    this.fileReads.push({
      path: filePath,
      duration,
      timestamp: new Date().toISOString()
    });
  }

  recordError(error) {
    this.errors.push({
      message: error.message,
      stack: error.stack,
      timestamp: new Date().toISOString()
    });
  }

  generateReport() {
    const totalDuration = Date.now() - this.startTime;
    
    return `
=== Spin-Sales 性能报告 ===
生成时间：${new Date().toISOString()}

📊 文件读取统计
----------------
总读取次数：${this.fileReads.length}
平均每次读取耗时：${(this.fileReads.reduce((sum, r) => sum + r.duration, 0) / this.fileReads.length).toFixed(2)}ms
最慢文件：${Math.max(...this.fileReads.map(r => r.path), 'N/A')} (${Math.max(...this.fileReads.map(r => r.duration))}ms)

🔴 错误统计
----------------
总错误数：${this.errors.length}
最近一次错误: ${this.errors[this.errors.length - 1]?.message || '无'}
    `;
  }
}

// 使用示例
const monitor = new PerfMonitor();
// 在初始化时记录文件读取时间
await cacheManager.getFileContent(file).then(content => {
  monitor.recordFileRead(file, performance.now() - startTime);
});
```

---

## 📈 性能基准测试建议

### 创建 benchmark 测试脚本

```javascript
/**
 * 性能基准测试
 */

import CacheManager from '../cache.js';

async function runBenchmarks() {
  console.log('🧪 Spin-Sales 性能基准测试开始\n');
  
  const cache = new CacheManager();
  let totalReads = 0;
  let totalDuration = 0;
  
  // 测试文件列表
  const files = [
    'references/s-questions.md',
    'references/p-questions.md',
    'references/i-questions.md',
    'references/n-questions.md',
    'references/objections.md',
    'references/opening_scripts.md'
  ];
  
  // 重复读取 10 次（第二次及以后应为缓存）
  for (let round = 1; round <= 10; round++) {
    const start = performance.now();
    
    for (const file of files) {
      await cache.getFileContent(`file:${file}`);
    }
    
    const duration = performance.now() - start;
    totalDuration += duration;
    totalReads += files.length;
    
    console.log(`Round ${round}: ${duration.toFixed(2)}ms (${totalReads}次读取)`);
  }
  
  const avgDuration = totalDuration / 10;
  const perReadAvg = avgDuration / totalReads;
  
  console.log('\n📊 结果汇总');
  console.log('='.repeat(50));
  console.log(`总读取次数：${totalReads}`);
  console.log(`平均每次读取耗时：${perReadAvg.toFixed(2)}ms`);
  console.log(`缓存命中率：${((9 * files.length) / totalReads * 100).toFixed(1)}%`);
  console.log('='.repeat(50));
}

runBenchmarks();
```

---

## 📋 检查清单

在使用 `Spin-Sales` 技能前，请确认：

- [ ] TAVILY_API_KEY 已配置（用于 I 阶段数据支持）
- [ ] 缓存文件未被意外修改或删除
- [ ] Node.js 版本 >= v18.0.0
- [ ] 所有 references 文件存在且为 `.md` 格式
- [ ] package.json 依赖已安装 (`npm install`)

---

*此文档帮助优化 Spin-Sales 技能的性能和稳定性。*
*版本：1.0 | 创建时间：2026-05-18*
