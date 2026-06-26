---
name: remotion-bozo
description: 快速创建 Remotion 视频项目的技能。提供完整的项目模板、动画工具函数、渲染脚本和最佳实践。一键创建专业视频项目。
metadata:
  tags: remotion, video, react, animation, template
---

# Remotion Bozo - 快速视频创作技能

一个完整的 Remotion 视频项目模板和创作工具集，让你快速创建专业视频。需要先安装好`remotion-best-practices`与`remotion-video-toolkit`这两个skill。并且有安装`playwright`。

## 🎯 适用场景

当你需要以下任务时使用此技能：

- 创建新的 Remotion 视频项目
- 快速搭建视频开发环境
- 使用预定义的动画工具函数
- 一键渲染 MP4 视频
- 复用 chrome-headless-shell（避免重复下载）

## 📋 核心功能

### 1. 项目模板
- 完整的 TypeScript + Remotion 配置
- 预配置的 package.json 脚本
- 优化的项目结构

### 2. 动画工具集
- Spring 动画配置
- Easing 缓动函数
- 场景进度计算
- 贝塞尔曲线预设

### 3. 快速渲染
- CLI 渲染命令
- Lambda 云端渲染支持
- 多种输出格式

### 4. Chrome 复用
- 自动检测现有 chrome-headless-shell
- 避免重复下载

## 🚀 快速开始

### 创建新项目

```bash
# 使用技能创建项目
remotion-bozo create my-video

# 进入项目目录
cd my-video

# 预览视频
npm start

# 渲染视频
npm run render
```

## 📁 项目结构

```
my-video/
├── src/
│   ├── index.tsx              # 入口文件
│   └── VideoTemplate.tsx      # 视频组件模板
├── out/                       # 输出目录
├── package.json
├── tsconfig.json
└── README.md
```

## 🎨 动画工具函数

### Spring 动画
```typescript
import {spring} from 'remotion';

const scale = spring({
  frame: progress * 30,
  fps: 30,
  config: {
    damping: 12,
    stiffness: 80,
    mass: 1
  }
});
```

### Easing 缓动
```typescript
import {interpolate, Easing} from 'remotion';

const opacity = interpolate(progress, [0, 0.3], [0, 1], {
  easing: Easing.inOut(Easing.cubic)
});
```

### 贝塞尔曲线
```typescript
const bouncy = Easing.bezier(0.68, -0.55, 0.265, 1.55);
```

## 🔧 Chrome Headless Shell 复用

技能会自动检测并复用现有的 chrome-headless-shell：

1. **Playwright 版本**: `~/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-arm64`
2. **Remotion 版本**: `node_modules/.remotion/chrome-headless-shell/`

设置环境变量强制使用指定版本：

```bash
# 在 .zshrc 中添加
export REMOTION_BROWSER_EXECUTABLE="/path/to/chrome-headless-shell"
```

## 📦 可用命令

| 命令 | 说明 |
|------|------|
| `create <project-name>` | 创建新项目 |
| `render` | 渲染当前项目 |
| `preview` | 预览视频 |
| `lambda` | 配置 Lambda 渲染 |

## 🎬 视频参数

- 默认分辨率: 1920 x 1080 (Full HD)
- 默认帧率: 30 fps
- 默认编码: H.264
- 支持格式: MP4, WebM, GIF

## 📚 相关规则

- [rules/project-template.md](rules/project-template.md) - 项目模板说明
- [rules/animation-tools.md](rules/animation-tools.md) - 动画工具函数
- [rules/rendering.md](rules/rendering.md) - 渲染配置
- [rules/chrome-reuse.md](rules/chrome-reuse.md) - Chrome 复用配置

## 🌟 最佳实践

1. 使用 Sequence 组件管理场景
2. 预计算场景进度避免重复计算
3. 使用 clamp 防止插值超出范围
4. Spring 动画适合缩放和位移
5. Easing 适合淡入淡出效果

## 🔗 相关资源

- [Remotion 官方文档](https://www.remotion.dev/docs)
- [remotion-best-practices](../remotion-best-practices)
- [remotion-video-toolkit](../remotion-video-toolkit)
