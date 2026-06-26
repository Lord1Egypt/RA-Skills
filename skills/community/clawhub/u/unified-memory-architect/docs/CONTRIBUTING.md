# 贡献指南

## 欢迎贡献

感谢您有兴趣为 Unified Memory 文档整理与发布系统做出贡献！

## 如何贡献

### 1. 报告问题

- 使用 GitHub Issues 报告 Bug
- 提供复现步骤
- 包含环境信息（Node.js 版本等）

### 2. 提交代码

#### 开发流程

1. **Fork 仓库**
2. **创建分支**: `git checkout -b feature/your-feature`
3. **编写代码**
4. **添加测试**
5. **提交**: `git commit -m 'Add: your feature'`
6. **推送**: `git push origin feature/your-feature`
7. **创建 Pull Request**

#### 提交信息规范

```
类型: 简短描述

详细说明（可选）

Fixes #issue-number
```

**类型**:
- `Add`: 新功能
- `Fix`: Bug 修复
- `Update`: 更新现有功能
- `Docs`: 文档更新
- `Refactor`: 代码重构
- `Test`: 测试相关
- `Chore`: 维护任务

### 3. 代码审查

- 响应代码审查意见
- 保持提交历史整洁
- 确保所有测试通过

## 开发设置

### 环境要求

- Node.js >= 14.0.0
- npm 或 yarn

### 本地开发

```bash
# 克隆你的 Fork
git clone https://github.com/your-username/unified-memory-architect.git
cd unified-memory-architect

# 安装依赖
npm install

# 创建功能分支
git checkout -b feature/your-feature

# 运行测试
npm test

# 运行特定脚本
node memory/scripts/verify-system.cjs
```

### 代码规范

- 使用 ESLint 进行代码检查
- 遵循 Standard JS 风格
- 添加 JSDoc 注释

## 测试

### 运行测试

```bash
# 运行所有测试
npm test

# 运行特定测试
npm test -- --grep "query"
```

### 编写测试

```javascript
describe('Query Module', () => {
  it('should query by tag', () => {
    const results = queryByTag('reflection', 10);
    expect(results).toHaveLength(10);
  });
});
```

## 文档贡献

- 更新相关文档
- 添加使用示例
- 翻译文档（如果需要）

## 行为准则

- 保持友好和尊重
- 接受建设性批评
- 关注社区利益
