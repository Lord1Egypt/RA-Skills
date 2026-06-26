# 迁移步骤详解

## 目录

- [1. 分析 package.json](#1-分析-packagejson)
- [2. 提取环境变量](#2-提取环境变量)
- [3. 删除 Webpack 文件](#3-删除-webpack-文件)
- [4. 更新 package.json](#4-更新-packagejson)
- [5. 创建环境变量文件](#5-创建环境变量文件)
- [6. 修改 index.html](#6-修改-indexhtml)
- [7. 修改 main.js](#7-修改-mainjs)
- [8. 全局替换环境变量](#8-全局替换环境变量)
- [9. 处理静态资源](#9-处理静态资源)
- [10. 修改组件导入](#10-修改组件导入)
- [11. 修复样式问题](#11-修复样式问题)

---

## 1. 分析 package.json

读取 package.json，识别依赖类型：

**保留的业务依赖：** axios, element-ui, lodash, qs, echarts, moment 等

**需要删除的 devDependencies：**
- webpack, webpack-*, babel-*
- html-webpack-plugin, extract-text-webpack-plugin
- css-loader, style-loader, sass-loader, vue-loader
- node-sass（替换为 sass）
- vue-template-compiler（Vue 2.7 不需要）

**需要升级的核心依赖：**
- vue → ^2.7.16
- vue-router → ^3.6.5
- vuex → ^3.6.2
- element-ui → ^2.15.14
- axios → 当前 1.x 安全补丁版本（执行迁移当天先核对官方 release/security，不再在 skill 中固定写死具体补丁号）

**axios 迁移检查：**
- 如果项目还在 `0.x` 或早期 `1.x`，先升级到当前 1.x 安全补丁版本，再继续做 Vite 迁移
- 搜索是否存在 `CancelToken`、`axios.all`、`axios.spread`、`headers.post['Content-Type']`
- 搜索是否存在裸 `import axios from 'axios'`；如果这些请求也需要统一 token、401/403、加解密逻辑，应迁回统一 request 封装
- 对 `FormData` 上传优先直接传 `FormData`，不要继续依赖 `delete headers.post['Content-Type']` 这类旧写法
- 重点回归上传、文件导出、401/403 跳转、刷新 token 这几类接口

---

## 2. 提取环境变量

读取 config/dev.env.js、config/prod.env.js 等文件，转换格式：

```javascript
// Webpack 格式
module.exports = { BASE_API: '"https://api.example.com"' }

// Vite 格式 (.env.development)
VITE_BASE_API=https://api.example.com
```

---

## 3. 删除 Webpack 文件

> ⚠️ **执行前确认**：以下命令会永久删除文件。确保已在正确的项目根目录执行，且代码已提交或备份。

**3.1 前置安全检查**

```bash
# 确认在项目根目录
pwd
# 确认 Git 状态干净（无未提交的破坏性变更）
git status --short
# 如果存在未提交的业务代码，先提交或 stash
git stash push -m "before vite migration"
```

**3.2 使用 Git 删除（可撤销）**

优先使用 `git rm` 而非 `rm`，以便通过 `git restore` 恢复：

```bash
# 删除 Webpack 构建目录
git rm -rf build/ config/
# 删除 Babel/PostCSS 配置
git rm -f .babelrc .postcssrc.js babel.config.js
# 删除旧锁文件（pnpm 项目不需要 npm/yarn 锁文件）
git rm -f package-lock.json yarn.lock 2>/dev/null || true
```

如果项目未纳入 Git 版本控制，使用以下命令（**不可撤销，执行前务必确认**）：

```bash
rm -rf build/ config/
rm -f .babelrc .postcssrc.js babel.config.js
rm -f package-lock.json yarn.lock
```

**3.3 删除后验证**

```bash
# 确认目标目录已不存在
ls build config .babelrc .postcssrc.js babel.config.js 2>&1 | grep -q "No such" && echo "清理完成" || echo "警告：部分文件仍存在"
```

---

## 4. 更新 package.json

**关键修改：**

1. 添加 `"type": "module"`

2. 替换 scripts：

```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview",
  "build:stage": "pnpm run build --mode staging",
  "build:prod": "pnpm run build --mode production"
}
```

3. 新的 devDependencies：

```json
"devDependencies": {
  "@vitejs/plugin-vue2": "^2.3.1",
  "sass": "^1.77.0",
  "vite": "^4.5.5",
  "vite-plugin-compression": "^0.5.1"
}
```

4. 如果使用 JSX，添加：`"@vitejs/plugin-vue2-jsx": "^2.1.1"`

5. 如果使用 SVG Sprite，添加：`"vite-plugin-svg-icons": "^2.0.1"`

---

## 5. 创建环境变量文件

创建 .env.development、.env.staging、.env.production：

```bash
VITE_RUN_ENV=development
VITE_BASE_API=https://dev-api.example.com
```

**注意：等号后面不能有空格！**

---

## 6. 修改 index.html

1. 移动 index.html 到项目根目录（如果不在）
2. 修改 script 标签：

```html
<script type="module" src="/src/main.js"></script>
```

---

## 7. 修改 main.js

```javascript
// 修改前
import App from "./App";
new Vue({ template: "<App/>", components: { App } });

// 修改后
import App from "./App.vue";
new Vue({ render: h => h(App) });
```

---

## 8. 全局替换环境变量

搜索并替换：

- `process.env.NODE_ENV` → `import.meta.env.VITE_RUN_ENV`
- `process.env.VUE_APP_*` → `import.meta.env.VITE_*`
- `process.env.BASE_API` → `import.meta.env.VITE_BASE_API`

---

## 9. 处理静态资源

```bash
# 重命名 static 目录为 public
mv static public

# 替换 ~@ 为 @
find src -type f \( -name "*.scss" -o -name "*.vue" \) -exec sed -i '' 's/~@/@/g' {} +

# 替换 global. 为 window.
find src -type f \( -name "*.js" -o -name "*.vue" \) -exec sed -i '' 's/global\./window./g' {} +
```

---

## 10. 修改组件导入

所有 .vue 文件导入必须加扩展名：

```javascript
// 修改前
import LoginView from "@/views/login/index";

// 修改后
import LoginView from "@/views/login/index.vue";
```

---

## 11. 修复样式问题

```bash
# 替换深度选择器
find src -type f -name "*.vue" -exec sed -i '' 's/\/deep\//::v-deep /g' {} +
find src -type f -name "*.vue" -exec sed -i '' 's/>>>/::v-deep /g' {} +
```
