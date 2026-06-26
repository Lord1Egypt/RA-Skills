# Wand Skill - 使用说明

## 概述

`wand-skill` 是一个帮助开发者在其他项目中快速使用 Wand UI 2.0 组件库的技能包。

## 安装方法

### 方法一：直接复制（推荐）

将 `wand-skill` 文件夹复制到你项目的 `.agent/skills/` 目录下：

```bash
# 假设你的目标项目路径为 /path/to/your-project
cp -r /Users/zane/Code/wand-ui/.agent/skills/wand-skill /path/to/your-project/.agent/skills/
```

### 方法二：使用打包文件

使用 `wand-skill.skill` 文件（这是一个 zip 文件）：

```bash
# 解压到目标项目的 skills 目录
unzip wand-skill.skill -d /path/to/your-project/.agent/skills/
```

## 技能内容

这个技能包含以下内容：

### 📄 SKILL.md
主要技能文档，包含：
- Wand UI 组件库概述
- 快速开始指南
- 组件分类（表单、选择器、反馈、展示、导航等）
- 组件使用工作流
- 常见使用场景和完整示例
- 最佳实践
- TypeScript 支持说明
- 故障排查指南

### 📚 references/components_api.md
完整的组件 API 参考文档，包含所有 36+ 组件的：
- Props（属性）
- Events（事件）  
- Slots（插槽）
- Methods（方法）
- 使用示例

组件包括：
- 表单组件：Button, Input, Textarea, Check, Switch, Form, Rate, Uploader
- 选择器组件：Picker, PopupPicker, Datetime, Cascade
- 反馈组件：Toast, Loading, Dialog, Confirm, Alert, ActionSheet
- 展示组件：List, Swipe, Collapse, NoticeBar, PhotoViewer
- 导航组件：Tab, TabBar, NavBar
- 其他组件：Popup, Popover, Search, SwipeCell, Affix

### 📖 references/quickstart.md
快速入门指南，包含：
- 安装方法
- 完整引入 vs 按需引入
- TypeScript 支持
- 组件命名规则
- 4 个典型使用场景的完整示例代码
- 浏览器支持信息
- SSR 支持说明
- 常见问题解答

## 使用方式

安装后，在其他项目中使用 AI 助手时：

### 自动触发

当你提到以下内容时，技能会自动触发：
- "使用 Wand UI 组件"
- "Wand UI 的 Button 组件怎么用"
- "创建一个表单页面（使用 Wand UI）"
- "需要一个移动端列表"
- 等等...

### 手动查询

你也可以直接询问：
- "Wand UI 的 Input 组件有哪些属性？"
- "如何使用 Wand UI 创建一个登录页面？"
- "Wand UI Toast 组件怎么用？"

AI 助手会根据技能文档提供详细的：
- 组件引入方式
- API 说明
- 完整的代码示例
- 最佳实践建议

## 技能特点

✅ **全面**: 覆盖所有 36+ 个组件的完整 API
✅ **实用**: 包含常见场景的完整示例代码
✅ **渐进式**: 分层的文档结构，按需查看详细信息
✅ **中文友好**: 所有文档均为中文

## 示例查询

以下是一些你可以向 AI 助手提出的问题示例：

```
"使用 Wand UI 创建一个登录表单"
"Wand UI 的 List 组件如何实现上拉加载？"
"如何使用 Wand UI 的 TabBar 创建底部导航？"
"Wand UI Dialog 组件的 API 是什么？"
"创建一个带有日期选择器的表单"
```

## 维护说明

### 更新技能

如果 Wand UI 组件库有更新，你可以：

1. 更新 `SKILL.md` 中的组件信息
2. 更新 `references/components_api.md` 中的 API 文档
3. 添加新的使用示例到 `references/quickstart.md`

### 重新打包

```bash
python3 /path/to/skill-creator/scripts/package_skill.py \
  /path/to/wand-skill \
  /output/directory
```

## 技术细节

- **技能格式**: 符合 skill-creator 规范
- **文件大小**: 约 12KB (打包后)
- **组件数量**: 36+ 个移动端组件
- **文档语言**: 中文
- **目标框架**: Vue 2.0
- **支持平台**: Android 4.0+, iOS 8+

## 许可证

与 Wand UI 2.0 使用相同的许可证。

---

**创建时间**: 2026-02-02
**版本**: 1.0.0
**作者**: 通过 skill-creator 创建
