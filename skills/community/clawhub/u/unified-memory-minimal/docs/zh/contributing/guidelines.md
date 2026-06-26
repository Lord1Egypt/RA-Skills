# 贡献指南

> 欢迎为 Unified Memory 项目做出贡献！

## 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发环境](#开发环境)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [测试规范](#测试规范)
- [文档规范](#文档规范)
- [发布流程](#发布流程)
- [社区角色](#社区角色)
- [获取帮助](#获取帮助)

## 行为准则

### 我们的承诺

为了营造开放、友好的环境，我们作为贡献者和维护者承诺：无论年龄、体型、身体健全与否、民族、性征、性别认同与表达、经验水平、教育程度、社会地位、国籍、相貌、种族、信仰、性取向，我们项目和社区的参与者都免于骚扰。

### 我们的准则

有助于创造积极环境的行为包括但不限于：

- 使用友好和包容性语言
- 尊重不同的观点和经历
- 耐心接受有益批评
- 关注对社区最有利的事情
- 友善对待其他社区成员

不可接受的行为包括但不限于：

- 使用与性有关的言语或图像，以及不受欢迎的性关注
- 捣乱、侮辱或贬损的评论，以及人身或政治攻击
- 公开或私下的骚扰
- 未经明确许可，发布他人的私人信息
- 其他有理由认定为违反职业操守的不当行为

### 我们的责任

项目维护者有责任诠释何谓“不可接受的行为”，并妥善、公平地纠正一切不可接受的行为。

项目维护者有权利和责任去删除、编辑、拒绝违背本行为准则的评论、提交、代码、wiki编辑、问题等，以及暂时或永久地封禁任何他们认为行为不当、威胁、冒犯、有害的贡献者。

### 适用范围

本行为准则适用于本项目所有平台，以及当个人代表本项目或本社区出席的公共场合。代表本项目或本社区的场合包括但不限于：使用官方电子邮件地址、通过官方社交媒体账号发布消息、作为指定代表参与在线或线下活动。

### 执行

如遇滥用、骚扰或其他不可接受的行为，请通过 [team@openclaw.ai](mailto:team@openclaw.ai) 联系项目团队。所有投诉都将得到及时、公正的处理。

项目团队有义务保密举报者信息。

## 如何贡献

### 贡献类型

#### 1. 报告错误
- 使用 GitHub Issues 报告错误
- 提供详细的重现步骤
- 包括环境信息
- 如果可能，提供修复建议

#### 2. 功能建议
- 使用 GitHub Issues 提出功能建议
- 描述功能的使用场景
- 如果可能，提供实现思路
- 讨论功能优先级

#### 3. 代码贡献
- Fork 仓库
- 创建功能分支
- 编写代码和测试
- 提交 Pull Request
- 参与代码审查

#### 4. 文档改进
- 修复拼写错误
- 改进文档结构
- 添加使用示例
- 翻译文档

#### 5. 社区帮助
- 回答 Issues 中的问题
- 帮助审查 Pull Requests
- 参与社区讨论
- 分享使用经验

### 贡献流程

1. **寻找任务**
   - 查看 [Good First Issues](https://github.com/mouxangithub/unified-memory/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
   - 查看 [Help Wanted](https://github.com/mouxangithub/unified-memory/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
   - 查看项目路线图

2. **讨论方案**
   - 在 Issue 中讨论实现方案
   - 确认技术细节
   - 获取维护者反馈

3. **开始开发**
   - Fork 仓库
   - 创建功能分支
   - 设置开发环境

4. **编写代码**
   - 遵循代码规范
   - 编写测试用例
   - 更新文档

5. **提交更改**
   - 遵循提交规范
   - 确保测试通过
   - 更新相关文档

6. **创建 Pull Request**
   - 描述更改内容
   - 链接相关 Issue
   - 等待代码审查

7. **代码审查**
   - 根据反馈修改
   - 保持积极沟通
   - 感谢审查者

8. **合并发布**
   - 维护者合并代码
   - 更新版本号
   - 发布新版本

## 开发环境

### 环境要求

- Node.js >= 18.0.0
- npm >= 8.0.0
- Git
- 文本编辑器（推荐 VS Code）

### 设置步骤

1. **Fork 仓库**
   ```bash
   # 访问 https://github.com/mouxangithub/unified-memory
   # 点击 "Fork" 按钮
   ```

2. **克隆仓库**
   ```bash
   git clone https://github.com/YOUR_USERNAME/unified-memory.git
   cd unified-memory
   ```

3. **添加上游仓库**
   ```bash
   git remote add upstream https://github.com/mouxangithub/unified-memory.git
   ```

4. **安装依赖**
   ```bash
   npm install
   ```

5. **设置开发环境**
   ```bash
   npm run setup:dev
   ```

6. **启动开发服务器**
   ```bash
   npm run dev
   ```

### 开发脚本

```bash
# 开发
npm run dev          # 启动开发服务器
npm run watch        # 监视模式

# 测试
npm test             # 运行所有测试
npm run test:unit    # 运行单元测试
npm run test:integration # 运行集成测试
npm run test:watch   # 监视测试模式

# 代码质量
npm run lint         # 代码检查
npm run format       # 代码格式化
npm run type-check   # 类型检查

# 构建
npm run build        # 生产构建
npm run clean        # 清理构建产物

# 文档
npm run docs:build   # 构建文档
npm run docs:serve   # 本地文档服务器
```

## 代码规范

### 语言规范

- **JavaScript**: 使用 ES6+ 语法
- **TypeScript**: 推荐使用 TypeScript
- **JSON**: 使用 2 空格缩进
- **Markdown**: 遵循 CommonMark 规范

### 命名规范

#### 变量和函数
```javascript
// 正确
const userName = '张三';
function calculateTotalPrice() { }

// 错误
const UserName = '张三';
function CalculateTotalPrice() { }
```

#### 类和构造函数
```javascript
// 正确
class UserService { }
function DatabaseConnection() { }

// 错误
class userService { }
function databaseConnection() { }
```

#### 常量和枚举
```javascript
// 正确
const MAX_RETRY_COUNT = 3;
const API_ENDPOINTS = {
  USERS: '/api/users',
  POSTS: '/api/posts'
};

// 错误
const maxRetryCount = 3;
const apiEndpoints = { ... };
```

### 代码风格

#### 缩进和空格
```javascript
// 正确：2 空格缩进
function example() {
  if (condition) {
    doSomething();
  }
}

// 错误：4 空格或制表符
function example() {
    if (condition) {
        doSomething();
    }
}
```

#### 分号
```javascript
// 正确：使用分号
const name = '张三';
function sayHello() {
  console.log('你好');
}

// 错误：省略分号
const name = '张三'
function sayHello() {
  console.log('你好')
}
```

#### 引号
```javascript
// 正确：使用单引号
const message = 'Hello World';
const template = `Hello ${name}`;

// 错误：使用双引号
const message = "Hello World";
```

### 注释规范

#### 文件头注释
```javascript
/**
 * @fileoverview 用户服务模块
 * @module services/user
 * @author 张三 <zhangsan@example.com>
 * @version 1.0.0
 * @license MIT
 */
```

#### 函数注释
```javascript
/**
 * 计算用户年龄
 * @param {Date} birthDate - 出生日期
 * @param {Date} [referenceDate=new Date()] - 参考日期，默认为当前日期
 * @returns {number} 年龄（整数）
 * @throws {Error} 如果出生日期无效
 * @example
 * const age = calculateAge(new Date('1990-01-01'));
 * console.log(age); // 34
 */
function calculateAge(birthDate, referenceDate = new Date()) {
  // 实现代码
}
```

#### 行内注释
```javascript
// 正确：解释复杂逻辑
const result = data.filter(item => {
  // 过滤掉已删除的项目
  return !item.deleted;
});

// 错误：重复明显信息
const name = '张三'; // 设置姓名为张三
```

## 提交规范

### 提交消息格式

```
<类型>(<范围>): <主题>

<正文>

<页脚>
```

#### 类型
- `feat`: 新功能
- `fix`: 修复错误
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变更

#### 范围
- `api`: API 相关
- `ui`: 用户界面
- `db`: 数据库
- `auth`: 认证授权
- `search`: 搜索功能
- `cache`: 缓存系统
- `docs`: 文档

#### 示例
```
feat(search): 添加混合搜索功能

- 实现 BM25 搜索算法
- 集成向量搜索
- 添加 RRF 结果融合
- 更新搜索 API 文档

Closes #123
```

### 提交频率

- 每个提交应该是一个完整的功能单元
- 避免提交未完成的代码
- 及时提交，避免大量更改一次性提交
- 使用 `git rebase` 整理提交历史

### 分支管理

#### 分支命名
```
# 功能分支
feat/user-authentication
feat/search-optimization

# 修复分支
fix/login-bug
fix/memory-leak

# 发布分支
release/v1.2.0
hotfix/v1.2.1
```

#### 分支策略
```bash
# 从主分支创建功能分支
git checkout main
git pull upstream main
git checkout -b feat/your-feature

# 开发完成后
git add .
git commit -m "feat(your-feature): 描述功能"
git push origin feat/your-feature

# 创建 Pull Request
```

## 测试规范

### 测试类型

#### 单元测试
```javascript
// 测试单个函数或模块
describe('calculateAge', () => {
  it('应该正确计算年龄', () => {
    const birthDate = new Date('1990-01-01');
    const referenceDate = new Date('2024-01-01');
    const age = calculateAge(birthDate, referenceDate);
    expect(age).toBe(34);
  });
});
```

#### 集成测试
```javascript
// 测试模块间集成
describe('UserService', () => {
  it('应该创建用户并保存到数据库', async () => {
    const user = await userService.createUser({ name: '张三' });
    const savedUser = await database.findUser(user.id);
    expect(savedUser.name).toBe('张三');
  });
});
```

#### 端到端测试
```javascript
// 测试完整流程
describe('用户注册流程', () => {
  it('应该完成用户注册', async () => {
    await page.goto('/register');
    await page.fill('#name', '张三');
    await page.fill('#email', 'zhangsan@example.com');
    await page.click('#submit');
    await expect(page).toHaveURL('/dashboard');
  });
});
```

### 测试覆盖率

- 目标覆盖率：80% 以上
- 关键功能：100% 覆盖率
- 使用 `npm run test:coverage` 生成报告

### 测试最佳实践

1. **测试独立性**: 每个测试应该独立运行
2. **确定性测试**: 测试结果应该可预测
3. **快速反馈**: 测试应该快速运行
4. **清晰断言**: 断言应该清晰表达预期
5. **模拟外部依赖**: 使用模拟对象测试外部依赖

## 文档规范

### 文档结构

```
docs/
├── en/                    # 英文文档
│   ├── getting-started/  # 入门指南
│   ├── guides/           # 使用指南
│   ├── api/              # API 参考
│   ├── architecture/     # 架构文档
│   └── contributing/     # 贡献指南
├── zh/                    # 中文文档
│   └── ...               # 相同结构
└── shared/               # 共享资源
```

### 文档格式

#### Markdown 规范
```markdown
# 一级标题

## 二级标题

### 三级标题

正文内容...

- 列表项1
- 列表项2

1. 有序列表1
2. 有序列表2

**粗体文本**
*斜体文本*

`代码片段`

```javascript
// 代码块
const example = '代码示例';
```

[链接文本](https://example.com)

![图片描述](image.png)
```

#### 中文文档规范
- 使用简体中文
- 专业术语保持英文
- 代码示例使用英文注释
- 保持中英文文档同步更新

### 文档更新

1. **代码变更时更新文档**
2. **API 变更时更新 API 文档**
3. **新功能时添加使用指南**
4. **定期检查文档准确性**

## 发布流程

### 版本规范

遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- **主版本号**: 不兼容的 API 修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

### 发布步骤

1. **准备发布**
   ```bash
   # 更新版本号
   npm version patch  # 或 minor, major
   
   # 更新 CHANGELOG.md
   # 更新文档
   ```

2. **创建发布分支**
   ```bash
   git checkout -b release/v1.2.0
   git push origin release/v1.2.0
   ```

3. **测试发布版本**
   ```bash
   npm run build
   npm test
   npm run integration-test
   ```

4. **创建 Pull Request**
   - 描述发布内容
   - 链接相关 Issues
   - 等待代码审查

5. **合并发布**
   ```bash
   git checkout main
   git merge release/v1.2.0
   git tag v1.2.0
   git push origin main --tags
   ```

6. **发布到 npm**
   ```bash
   npm publish
   ```

7. **更新文档网站**
   ```bash
   npm run docs:deploy
   ```

### 发布检查清单

- [ ] 所有测试通过
- [ ] 代码审查完成
- [ ] 文档更新完成
- [ ] CHANGELOG 更新
- [ ] 版本号更新
- [ ] 构建产物检查
- [ ] 发布公告准备

## 社区角色

### 贡献者级别

#### 1. 首次贡献者
- 修复拼写错误
- 添加测试用例
- 报告错误
- 参与讨论

#### 2. 常规贡献者
- 实现小型功能
- 修复中等复杂度错误
- 改进文档
- 帮助审查代码

#### 3. 核心贡献者
- 实现主要功能
- 架构改进
- 指导新贡献者
- 参与路线图规划

#### 4. 维护者
- 代码审查
- 版本发布
- 社区管理
- 项目决策

### 权限和责任

| 角色 | 权限 | 责任 |
|------|------|------|
| 首次贡献者 | 提交 Issues, 参与讨论 | 遵守行为准则 |
| 常规贡献者 | 提交 Pull Requests | 代码质量, 测试覆盖 |
| 核心贡献者 | 合并 Pull Requests | 架构设计, 代码审查 |
| 维护者 | 发布版本, 管理仓库 | 项目方向, 社区管理 |

## 获取帮助

### 沟通渠道

#### GitHub Issues
- **功能建议**: 使用 `enhancement` 标签
- **错误报告**: 使用 `bug` 标签
- **问题咨询**: 使用 `question` 标签

#### GitHub Discussions
- **使用问题**: 在 Q&A 板块提问
- **功能讨论**: 在 Ideas 板块讨论
- **社区交流**: 在 General 板块交流

#### 电子邮件
- **安全问题**: security@openclaw.ai
- **合作咨询**: partnership@openclaw.ai
- **一般问题**: team@openclaw.ai

### 学习资源

#### 官方文档
- [入门指南](../getting-started/quickstart.md)
- [API 参考](../api/overview.md)
- [架构文档](../architecture/overview.md)

#### 外部资源
- [OpenClaw 文档](https://docs.openclaw.ai)
- [Node.js 文档](https://nodejs.org/docs)
- [GitHub 指南](https://docs.github.com)

### 社区活动

#### 定期会议
- **社区会议**: 每月第一个周二
- **技术分享**: 每月第三个周四
- **代码审查**: 每周三下午

#### 线上交流
- **Discord**: [OpenClaw Community](https://discord.gg/openclaw)
- **Twitter**: [@OpenClawAI](https://twitter.com/OpenClawAI)
- **博客**: [OpenClaw Blog](https://blog.openclaw.ai)

## 致谢

感谢所有为 Unified Memory 项目做出贡献的开发者！您的贡献让这个项目变得更好。

特别感谢：

- **OpenClaw 团队**: 提供平台和支持
- **核心贡献者**: 持续的代码贡献
- **文档贡献者**: 完善的中英文文档
- **测试贡献者**: 确保代码质量
- **社区成员**: 反馈和建议

让我们共同努力，打造更好的记忆管理系统！