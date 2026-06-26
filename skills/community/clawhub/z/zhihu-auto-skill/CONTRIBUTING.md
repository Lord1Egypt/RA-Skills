# 贡献指南

感谢你对知乎自动化 Skill 的关注！我们欢迎任何形式的贡献 —— 新功能、bug 修复、文档改进、使用反馈，通通欢迎。

---

## 开发环境搭建

### 前置要求

- Node.js >= 18（推荐使用 nvm 管理版本，参考 `.nvmrc`）
- npm（随 Node.js 一同安装）

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/liuboacean/zhihu-automation-skill.git
cd zhihu-automation-skill

# 安装依赖
npm install

# 安装 Playwright Chromium 浏览器
npx playwright install chromium
```

### 配置 Cookie 加密密钥

```bash
export ZHIHU_COOKIE_KEY="$(openssl rand -hex 32)"
```

---

## 代码规范

### JavaScript 规范

- **ESM 模块**：项目使用 `"type": "module"`，所有 `.js` 文件使用 `import`/`export` 语法
- **命名风格**：
  - 函数名使用 camelCase
  - 类名使用 PascalCase
  - 常量使用 UPPER_SNAKE_CASE
  - 文件名使用 kebab-case
- **异步处理**：优先使用 `async/await`，避免裸 `.then()` / `.catch()`
- **错误处理**：关键操作必须包裹 try-catch，错误信息应包含上下文

### 提交规范

本项目遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>(<scope>): <description>

[optional body]
```

常用类型：

| 类型       | 用途                 |
| ---------- | -------------------- |
| `feat`     | 新功能               |
| `fix`      | Bug 修复             |
| `docs`     | 文档变更             |
| `refactor` | 代码重构             |
| `perf`     | 性能优化             |
| `test`     | 测试相关             |
| `chore`    | 构建/工具/依赖变更   |
| `security` | 安全相关修复         |

示例：

```
feat(zhihu-publish): 支持 Markdown 表格转知乎格式
fix(zhihu-interact): 修复点赞后未更新状态
docs(readme): 更新 Cookie 导出步骤
```

### Prettier 格式化

建议在编辑器中开启 Prettier 自动格式化，或提交前运行：

```bash
npx prettier --check scripts/**/*.js
```

> 注：项目当前尚未配置 `.prettierrc`，欢迎 PR 添加。

---

## 提交 PR 流程

1. **Fork 本仓库** 到你的 GitHub 账号
2. **创建功能分支**：`git checkout -b feat/your-feature-name`
3. **进行开发**，确保：
   - 代码风格与现有代码一致
   - 为新增功能添加必要的注释和错误处理
   - 如果是新脚本，更新 `package.json` 中的 `"scripts"` 字段
4. **运行测试**：`npm test`
5. **提交**：`git commit -m "feat(xxx): 简洁描述变更"`
6. **推送分支**：`git push origin feat/your-feature-name`
7. **创建 PR** 到 `main` 分支，并在描述中说明：
   - 做了什么、为什么做
   - 测试情况
   - 截图（如涉及 UI 操作）

### PR 审查标准

- 代码无明显安全问题
- 不引入新的外部依赖（或新增依赖有充分理由）
- 新增功能的 CLI 接口风格与现有保持一致
- 浏览器自动化操作包含合适的等待和重试逻辑
- 已考虑知乎反爬限制（频率控制、降级策略等）

---

## 测试

```bash
# 选择器冒烟测试
npm run smoke-test

# Cookie 到期检测
npm run cookie-check

# 端到端测试（沙箱模式）
npm run e2e-test
```

建议在提交 PR 前至少通过 `smoke-test` 和 `cookie-check`。

---

## 注意事项

### Cookie 安全

- Cookie 文件使用 **AES-256-GCM** 加密存储在 `~/.hermes/credentials/zhihu-cookies.enc`
- **切勿**将未加密的 Cookie 提交到 Git
- **切勿**将 `ZHIHU_COOKIE_KEY` 写在代码或提交信息中
- Cookie 有效期约 30 天，过期需重新登录导出

### 知乎反爬限制

- **频率控制**：HTTP 请求间隔 200-500ms，浏览器操作间隔 5-10s
- **限流处理**：遇到限流时自动指数退避（30s → 1min → 3min → 10min）
- **验证码**：浏览器通道可能触发滑块验证，系统会自动等待手动验证
- **选择器失效**：知乎前端经常改版，`config/selectors.json` 可能需更新
- **签名降级**：HTTP 签名通道返回 401 时自动降级到浏览器通道

### 账号安全建议

- 建议先在**小号**上测试所有功能
- 不要在公共机器上长期保存 Cookie 密钥
- 定期轮换 Cookie 加密密钥

---

## 问题反馈

遇到问题请先查阅已有 Issues。如未解决，欢迎提交 Issue，请包含：

- 操作步骤
- 期望结果与实际结果
- 相关日志或错误信息
- 知乎页面是否已改版（可附上截图）

---

再次感谢你的贡献！
