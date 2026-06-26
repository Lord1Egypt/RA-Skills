# Code Refactor Skill

智能代码重构助手，用于分析代码质量问题并自动应用重构建议。

## 功能特性

### 1. 代码分析 (CodeAnalyzer)
- 检测代码异味 (Code Smells)
- 计算复杂度指标（圈复杂度、认知复杂度）
- 识别重复代码
- 检查代码规范

### 2. 重构引擎 (RefactoringEngine)
- 提取函数/方法
- 重命名变量/函数
- 简化条件表达式
- 消除重复代码
- 优化导入/依赖

### 3. 变更应用 (ChangeApplier)
- 应用重构变更
- 生成 diff 预览
- 支持 dry-run 模式
- 回滚功能

### 4. 测试验证 (TestValidator)
- 运行测试确保重构后功能正常
- 检查测试覆盖率

## 检测的代码异味

1. **长函数** (>50行)
2. **过多参数** (>4个)
3. **重复代码**
4. **深层嵌套** (>3层)
5. **魔法数字**
6. **未使用变量/导入**
7. **复杂条件表达式**

## 使用方法

```javascript
const { CodeRefactor } = require('./src/index');

const refactor = new CodeRefactor();

// 分析代码
const analysis = refactor.analyze('path/to/file.js');

// 查看问题
console.log(analysis.issues);

// 自动重构
const result = refactor.refactor('path/to/file.js', {
  dryRun: true  // 预览模式
});

// 应用变更
if (result.canApply) {
  refactor.applyChanges(result.changes);
}
```

## CLI 使用

```bash
# 分析代码
node src/index.js analyze file.js

# 重构代码（dry-run）
node src/index.js refactor file.js --dry-run

# 应用重构
node src/index.js refactor file.js --apply
```

## 配置选项

```javascript
{
  maxFunctionLength: 50,      // 函数最大行数
  maxParameters: 4,           // 参数最大数量
  maxNestingDepth: 3,         // 最大嵌套深度
  minDuplicateLines: 5,       // 最小重复行数
  complexityThreshold: 10     // 复杂度阈值
}
```

## 测试

```bash
npm test
```
