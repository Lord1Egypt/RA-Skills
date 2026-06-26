---
name: vue2-vite-upgrade
description: 将 Vue 2 + Webpack 项目升级到 Vite 构建工具。当用户需要将 Vue 2 项目从 Webpack 迁移到 Vite、优化构建速度、解决 Webpack 配置问题，或处理 Vue CLI/Webpack 与 Vite 环境变量兼容时使用此技能。触发场景包括：(1) 用户提到"升级到 Vite"、"迁移到 Vite"、"Webpack 转 Vite"；(2) 用户抱怨 Webpack 构建慢、热更新慢；(3) 用户想要现代化 Vue 2 项目的构建工具；(4) 用户遇到 Webpack 配置复杂难以维护的问题；(5) 用户询问如何提升 Vue 2 项目的开发体验；(6) 用户提到 process.env、VUE_APP_*、import.meta.env、VITE_* 等环境变量兼容。
---

# Vue 2 项目升级到 Vite 构建工具

## 重要提示

⚠️ **在开始之前，必须确认用户已经备份了代码或使用了 Git 版本控制！**

### 前置安全检查

阶段 2 包含删除操作（`rm -rf` / `git rm`），执行前必须确认：

1. 当前在项目根目录（`ls package.json` 存在）
2. Git 状态干净或业务代码已提交/stash（`git status`）
3. 用户已明确确认可以执行删除
4. 删除操作优先使用 `git rm`（可通过 `git restore` 恢复），非 Git 项目才使用 `rm`

## 执行原则

1. **使用 TodoWrite 工具**：创建完整的任务列表，实时更新进度
2. **分阶段执行**：按照阶段顺序执行，每个阶段完成后标记为完成
3. **遇到问题及时沟通**：使用 AskUserQuestion 询问用户
4. **保留业务依赖**：只删除 Webpack/Babel 相关依赖

## 执行流程概览

| 阶段 | 内容 |
|------|------|
| 阶段 1 | 项目分析 - 分析现有项目结构、依赖和配置 |
| 阶段 2 | 文件清理与配置 - 删除 Webpack 配置，创建 Vite 配置 |
| 阶段 3 | 代码迁移 - 修改代码以适配 Vite |
| 阶段 4 | 测试与验证 - 安装依赖并测试运行 |
| 阶段 5 | 部署配置（可选）- 配置自动化部署脚本 |

## 参考文档

- **Vite 配置模板**：见 [references/vite-config.md](references/vite-config.md)
- **常见问题处理**：见 [references/common-issues.md](references/common-issues.md)
- **部署配置**：见 [references/deploy-config.md](references/deploy-config.md)

---

## 阶段 1：项目分析

使用 TodoWrite 创建任务列表，然后依次执行：

1. 分析 package.json（识别业务依赖、Webpack 依赖、需升级依赖）
2. 提取环境变量（从 config/*.env.js 转换为 .env.* 格式）
3. 检查代理配置（记录 proxyTable）
4. 检查特殊功能（SVG Sprite、JSX、动态路由）
5. 单独审计 `axios`：核对官方 release/security 公告，避免继续保留已披露漏洞版本；同时排查上传、导出、401/403 拦截和裸 `axios` 调用

详细步骤见 [references/migration-steps.md](references/migration-steps.md)

---

## 阶段 2：文件清理与配置

1. 删除 Webpack 相关文件（build/、config/、.babelrc 等）
2. 更新 package.json（添加 type: module，替换 scripts，更新依赖）
3. 创建 vite.config.js（使用 [references/vite-config.md](references/vite-config.md) 模板）
4. 创建环境变量文件（.env.development、.env.staging、.env.production）

详细步骤见 [references/migration-steps.md](references/migration-steps.md)

---

## 阶段 3：代码迁移

1. 修改 index.html（移动到根目录，添加 `<script type="module">`）
2. 修改 main.js（使用 render 函数，导入加 .vue 扩展名）
3. 迁移环境变量：优先使用 import.meta.env；如项目存在并行上线或老分支合并，需要保留 process.env.VUE_APP_* 静态写法兼容层
4. 处理静态资源（static → public，~@ → @，global → window）
5. 修改组件导入（所有 .vue 导入加扩展名）
6. 修复样式（/deep/ 和 >>> → ::v-deep）

详细步骤见 [references/migration-steps.md](references/migration-steps.md)

---

## 环境变量兼容约定

迁移期如果可能有 Webpack/Vue CLI 写法的需求先合入生产，不要只做 `process.env -> import.meta.env` 的单向替换。

1. `.env.*` 中新增变量优先使用 `VITE_` 前缀。
2. Vite 代码推荐使用 `import.meta.env.VITE_*`。
3. Webpack/Vue CLI 历史代码允许继续使用 `process.env.VUE_APP_*`。
4. 在 `vite.config.js` 中用 `loadEnv(mode, process.cwd(), '')` 读取变量，并自动把 `VITE_XXX` 映射为 `process.env.VUE_APP_XXX`。
5. 如果 `.env.*` 已存在 `VUE_APP_XXX`，也要原样注入为 `process.env.VUE_APP_XXX`。
6. `define` 使用精确 key，不整体替换 `process.env`，减少对第三方库和动态访问的影响。
7. 兼容层只保证静态写法，如 `process.env.VUE_APP_BASE_API`；不承诺兼容 `process.env[key]`。

具体配置示例见 [references/vite-config.md](references/vite-config.md)。

---

## 阶段 4：测试与验证

1. 安装依赖：先执行 `pnpm install`；如遇 peer dependency 冲突，优先手动排查并解决版本冲突，确认无法解决后再使用 `pnpm install --force`（`--force` 会忽略 lockfile，需检查 `pnpm-lock.yaml` 变更）
2. 启动开发服务器：`pnpm run dev`
3. 验证功能：页面显示、样式、图标、路由、API 请求
4. 构建测试：`pnpm run build:stage && pnpm run preview`

**遇到问题查看 [references/common-issues.md](references/common-issues.md)**

---

## 阶段 5：部署配置（可选）

如需自动化部署，参考 [references/deploy-config.md](references/deploy-config.md)：

1. 创建压缩脚本（export-zip.cjs）
2. 创建 FTP 部署脚本（ftp-deploy.js）—— **部署凭证通过环境变量传入，禁止硬编码**
3. 添加部署 NPM 脚本
4. 安装依赖：`pnpm add -D archiver ftp-deploy rimraf`
5. 执行生产部署前需显式确认

---

## 升级要点速查

| 类别 | 修改内容 |
|------|----------|
| 依赖管理 | 保留业务依赖，删除 Webpack/Babel，升级 Vue 到 2.7.x；`axios` 使用当前 1.x 安全补丁版本，不保留已披露漏洞版本 |
| 配置文件 | 创建 vite.config.js 和 .env.* 文件 |
| 代码修改 | .vue 导入加扩展名，环境变量优先迁移到 import.meta.env，必要时兼容 process.env.VUE_APP_* |
| 语法替换 | require → import，global → window，~@ → @ |
| axios 改造 | 排查 `CancelToken`、`headers.post['Content-Type']`、裸 `axios` 调用、上传下载与登录态拦截 |
