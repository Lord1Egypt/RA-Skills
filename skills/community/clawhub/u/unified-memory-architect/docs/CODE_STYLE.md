# 代码规范

## 概述

本项目遵循 Standard JS 代码风格，并添加了特定于项目的规范。

## 格式化

### 缩进
- 使用 2 空格缩进
- 不要使用 Tab

### 换行
- 每行不超过 100 字符
- 使用 Unix 换行符 (LF)

### 引号
- 字符串使用单引号
- JSX 使用双引号

## 命名

### 变量和函数
```javascript
// ✅ 正确
const userName = 'John';
function getUserById(id) { }

// ❌ 错误
const user_name = 'John';
function get_user_by_id(id) { }
```

### 常量
```javascript
// ✅ 正确
const MAX_RETRIES = 3;
const DEFAULT_LIMIT = 100;

// ❌ 错误
const maxRetries = 3;
const default_limit = 100;
```

### 类
```javascript
class MemoryManager {
  // 首字母大写，驼峰命名
}
```

## 注释

### JSDoc 注释
```javascript
/**
 * 按标签查询记忆
 * @param {string} tag - 标签名称
 * @param {number} limit - 返回数量限制
 * @returns {Array<Memory>} 记忆数组
 */
function queryByTag(tag, limit) {
  // ...
}
```

### 行内注释
```javascript
// ✅ 正确
// 计算总数
const total = user + admin;

// ❌ 错误
/* 计算总数 */
const total = user + admin;
```

## 最佳实践

### 错误处理
```javascript
// ✅ 正确
try {
  const data = JSON.parse(content);
} catch (error) {
  console.error('Parse error:', error.message);
  throw error;
}

// ❌ 错误
try {
  const data = JSON.parse(content);
} catch (e) {
  // 静默失败
}
```

### 异步处理
```javascript
// ✅ 正确
async function fetchData() {
  try {
    const result = await fetch(url);
    return result;
  } catch (error) {
    throw error;
  }
}

// ❌ 错误
function fetchData() {
  fetch(url).then(result => {
    return result;
  });
}
```

### 模块导出
```javascript
// ✅ 正确
module.exports = {
  queryByTag,
  queryByDate,
  searchMemories,
  getStats
};

// ❌ 错误
exports.queryByTag = queryByTag;
exports.queryByDate = queryByDate;
```

## 文件组织

```
scripts/
├── query.cjs           # 主查询模块
├── migrate-simple.cjs   # 迁移脚本
├── enhance-tags.cjs    # 标签增强
└── ...
```

## 脚本要求

每个脚本必须：
1. 包含 shebang (`#!/usr/bin/env node`)
2. 包含 JSDoc 头部注释
3. 导出主要函数
4. 支持 CLI 和编程调用
5. 提供错误处理
