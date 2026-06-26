# 测试指南

## 测试框架

项目使用 Node.js 内置的测试功能或 Jest 进行单元测试。

## 测试类型

### 1. 单元测试

测试独立函数和模块：

```bash
# 运行所有单元测试
npm test

# 运行特定模块测试
npm test -- --grep "query"
```

### 2. 集成测试

测试脚本间的协作：

```bash
# 运行集成测试
npm run test:integration
```

### 3. 系统测试

验证整个系统：

```bash
# 运行系统验证
node memory/scripts/verify-system.cjs
```

## 测试覆盖

### 必须覆盖

- [ ] queryByTag 函数
- [ ] queryByDate 函数
- [ ] searchMemories 函数
- [ ] getStats 函数
- [ ] 数据格式验证
- [ ] 错误处理

### 建议覆盖

- [ ] 边界条件
- [ ] 性能基准
- [ ] 并发测试
- [ ] 内存使用

## 测试数据

使用 `memory/import/` 目录中的测试数据：

```javascript
const testData = require('./memory/import/2026-04-13.jsonl');
```

## 持续集成

每次 PR 必须通过：
1. `npm test` - 单元测试
2. `npm run lint` - 代码检查
3. `node verify-system.cjs` - 系统验证

## 报告

运行测试覆盖率：

```bash
npm run test:coverage
```
