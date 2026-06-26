---
name: rn-bundle-to-github
description: React Native bundle 发布到 GitHub 的完整工作流。当需要为 React Native 项目打包并发布到 GitHub Release 时激活。包括：(1) 初始化 RN 项目发布配置，(2) 使用 publish.sh 自动发布 release/debug 版本，(3) 生成包含 Android/iOS bundle 的 GitHub Release，(4) 版本号自动递增管理，(5) CHANGELOG 自动生成。
---

# React Native Bundle 发布到 GitHub

本 skill 用于将 React Native 项目的 JavaScript 代码打包成 bundle 并发布到 GitHub Release。

## 核心概念

### 什么是 Bundle？

Bundle 是 React Native 应用编译后的 JavaScript 代码包，包含了应用的所有业务逻辑。移动端加载 bundle 即可运行应用，无需连接开发服务器。

### 为什么发布到 GitHub？

- **热更新**: App 可以从 GitHub 下载最新 bundle 实现热更新，无需重新发布应用市场
- **版本管理**: GitHub Release 提供版本化管理，支持回滚
- **独立性**: Bundle 独立于应用本身，可以独立更新

### Release vs Debug 版本

| 类型 | 格式 | 示例 | prerelease | 用途 |
|------|------|------|------------|------|
| Release | `vx.x.x` | v1.0.3 | `false` | 正式版本 |
| Debug | `vx.x.x.x` | v1.0.1.5 | `true` | 开发/测试版本 |

Debug 版本通过 GitHub API 的 `prerelease: true` 标记，可以在 App 端过滤区分。

## 快速开始

### 前提条件

1. Node.js >= 18
2. GitHub 账号和仓库
3. GitHub Personal Access Token

### Step 1: 配置 GitHub Token

```bash
# 创建 token 文件（只读权限即可）
echo "ghp_xxxxxxxxxxxx" > ~/.github_token
chmod 600 ~/.github_token
```

Token 需要 `repo` 权限才能创建 Release 和上传 assets。

### Step 2: 初始化项目

在 RN 项目根目录执行：

```bash
# 下载发布脚本
curl -o publish.sh https://raw.githubusercontent.com/lvtong199881/MyRNApp/refs/heads/main/publish.sh
chmod +x publish.sh

# 添加 npm scripts（可选）
npm pkg set scripts.release="bash publish.sh"
npm pkg set scripts.debug="bash publish.sh debug"
```

### Step 3: 发布版本

```bash
# 发布正式版本
npm run release
# 或直接执行
./publish.sh

# 发布调试版本
npm run debug
# 或直接执行
./publish.sh debug
```

## 发布流程详解

### 完整步骤

```
1. [检查] 验证未提交的 Git 改动
2. [版本] 计算新版本号并更新 package.json
3. [依赖] 执行 npm install 更新 lock 文件
4. [打包] 生成 Android 和 iOS bundle
5. [日志] 获取上一个版本的 commit SHA
6. [日志] 生成 changelog 内容
7. [文档] 更新 CHANGELOG.md
8. [Git] 提交改动并推送到远程
9. [Git] 创建 tag 并推送
10. [GitHub] 创建 Release
11. [GitHub] 上传 bundle 到 Release
12. [完成] 打印发布信息
```

### 版本号计算规则

**Release 版本 (vx.x.x)**:
- 基于最新 Release tag 的 patch 版本 +1
- 示例: v1.0.2 → v1.0.3

**Debug 版本 (vx.x.x.x)**:
- 首次: 基于最新 Release 添加 .0 → v1.0.1.0
- 后续: 自增末位 → v1.0.1.1, v1.0.1.2
- 如果存在 Debug tag，基于最新 Debug tag 自增

### Bundle 生成

```bash
# Android bundle
node node_modules/@react-native-community/cli/build/bin.js bundle \
  --platform android \
  --dev false \
  --entry-file index.js \
  --bundle-output ./dist/index.android.bundle

# iOS bundle
node node_modules/@react-native-community/cli/build/bin.js bundle \
  --platform ios \
  --dev false \
  --entry-file index.js \
  --bundle-output ./dist/index.ios.bundle
```

`--dev false` 表示生产模式，会进行代码压缩和优化。

### GitHub Release 创建

通过 GitHub API 创建：

```bash
POST https://api.github.com/repos/{owner}/{repo}/releases
```

Release 包含:
- tag_name: 版本标签
- name: 显示名称
- body: 发布说明（包含 commit 列表）
- prerelease: 是否预发布

### Bundle 下载链接

发布后，bundle 可以通过以下格式访问：

```
# 直接 raw 链接
https://github.com/{owner}/{repo}/raw/{tag}/dist/index.android.bundle

# jsDelivr CDN（可选）
https://cdn.jsdelivr.net/gh/{owner}/{repo}@{tag}/dist/index.android.bundle
```

## App 端集成

### 获取最新 Release 版本

```bash
# 获取最新 release
GET https://api.github.com/repos/{owner}/{repo}/releases/latest

# 获取最新 debug 版本（prerelease: true）
GET https://api.github.com/repos/{owner}/{repo}/releases?per_page=100
# 然后过滤 prerelease === true 的最新一个
```

### 下载并使用 Bundle

```kotlin
// Android 示例
val bundleUrl = "https://github.com/lvtong199881/MyRNApp/raw/v1.0.1/dist/index.android.bundle"
// 使用 React Native 的 BundleLoader 加载
```

## 项目配置要求

| 配置项 | 说明 | 来源 |
|--------|------|------|
| GitHub Token | 用于 API 认证 | `~/.github_token` 文件 |
| repo owner | GitHub 用户名 | 从 git remote 获取 |
| repo name | GitHub 仓库名 | `package.json` 的 `name` 字段 |
| Git remote | 必须指向 GitHub | 本地 git 配置 |

## 目录结构

发布脚本会创建以下文件:

```
{project}/
├── publish.sh          # 发布脚本
├── dist/
│   ├── index.android.bundle
│   └── index.ios.bundle
├── CHANGELOG.md        # 自动生成/更新
└── package.json        # 版本号自动更新
```

## 常见问题

### Q: 发布失败 "存在未提交的改动"

需要先提交或 stash：
```bash
git stash && ./publish.sh debug && git stash pop
```

### Q: 想指定版本号发布

手动修改 `package.json` 的 `version` 字段后再执行脚本。

### Q: 如何发布到私有仓库

同样适用，确保 Token 有该仓库的 `repo` 权限。

### Q: Bundle 太大怎么办

1. 启用 Hermes 引擎（需要重建 android/）可减少 30-50%
2. 删除不需要的 npm 依赖
3. 避免引入大型第三方库

### Q: 如何查看发布了哪些版本

```bash
git tag -l --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+'
```

或访问 https://github.com/{owner}/{repo}/releases

## 手动干预场景

### 只打包不发布

修改 publish.sh，注释掉最后 GitHub API 相关行。

### 重新发布某个版本

```bash
# 查看历史 tag
git tag -l

# 基于某个 tag 重新打包
git checkout v1.0.1
# 修改代码...
./publish.sh
```

### 回滚到上一个版本

在 GitHub Release 页面下载上一个版本的 bundle，然后在 App 端配置使用该版本的下载链接。

## 优化建议

1. **减少依赖**: 删除不用的 npm 包，减少安装和打包时间
2. **启用 Hermes**: 需要重建 android/ 文件夹
3. **懒加载**: 将部分代码拆分成多个 chunk，按需加载（需要修改 App 加载逻辑）
4. **压缩**: Metro 已经默认使用 terser 压缩，无需额外配置