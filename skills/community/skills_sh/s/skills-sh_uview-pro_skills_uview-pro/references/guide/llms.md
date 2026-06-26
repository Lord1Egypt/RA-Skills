---
name: "llms"
description: "uView Pro 为大型语言模型（LLMs）提供了完善的上下文支持，帮助 AI 更好地理解和使用组件库。. Invoke when user needs guidance on llms."
url: "https://uviewpro.cn/zh/guide/llms.html"
triggers: ["llms","LLMs说明"]
---

# LLMs 支持

uView Pro 为大型语言模型（LLMs）提供了完善的上下文支持，帮助 AI 更好地理解和使用组件库。

## llms.txt 文件

我们为 LLMs 提供了两种格式的上下文文件：

### 标准版（llms.txt）

**地址：** <https://uviewpro.cn/llms.txt>

标准版文件包含：
- 组件库概述和特性介绍
- 所有组件的链接和简介
- 工具函数的列表
- 快速导航索引

适用于：快速了解 uView Pro 的整体结构和可用资源

### 完整版（llms-full.txt）

**地址：** <https://uviewpro.cn/llms-full.txt>

完整版文件包含：
- 所有组件的详细文档内容
- 完整的 API 说明和属性列表
- 详细的使用示例和代码片段
- 事件、插槽、方法等完整参考

适用于：深度理解和精确使用具体组件

## 如何使用

### 在 AI 助手/IDE 中使用

将以下 URL 提供给支持的 AI 助手或 IDE：

```
https://uviewpro.cn/llms.txt
```

或完整版本：

```
https://uviewpro.cn/llms-full.txt
```

### 在 Cursor 中使用

在 Cursor 的设置中，可以将 llms.txt 添加为项目的上下文参考：

1. 打开 Cursor 设置
2. 找到 "Context" 或 "Documents" 设置
3. 添加 URL：`https://uviewpro.cn/llms.txt`

### 在其他 AI 工具中使用

大多数支持 URL 上下文的 AI 工具（如 Claude、ChatGPT、GitHub Copilot 等）都可以通过提供上述 URL 来获取 uView Pro 的组件库信息。

## 内容覆盖

llms.txt 和 llms-full.txt 文件涵盖了 uView Pro 的全部内容：

### 基础组件
- Button、Icon、Image、Cell、Badge 等基础 UI 组件
- Layout、Grid、Gap 等布局组件
- Card、Divider、Line 等展示组件

### 表单组件
- Input、Field、Textarea 等输入组件
- Radio、Checkbox、Switch 等选择组件
- Form、Picker、Select 等表单容器组件

### 反馈组件
- Toast、Modal、Loading、Message 等提示组件
- ActionSheet、Popup、Notify 等弹层组件
- Progress、Skeleton、Empty 等状态组件

### 导航组件
- Navbar、Tabbar、Tabs、Steps 等导航组件
- BackTop、IndexList、TreeSelect 等辅助导航

### 工具函数
- 颜色处理（color、colorSwitch）
- 数据操作（deepClone、deepMerge、random）
- 格式化工具（timeFormat、priceFormat）
- 设备信息（systemInfo、getRect）
- 其他实用工具（guid、queryParams、test）

## 更新频率

llms.txt 文件会随着 uView Pro 的版本更新而自动更新，确保 AI 始终获取到最新的组件文档和 API 信息。

## 结合 Skills 使用

为了获得最佳的 AI 辅助开发体验，建议同时使用：

1. **llms.txt** - 为 AI 提供组件库的完整上下文
2. **[Skills](./skills.md)** - 提供标准化的代码生成能力

两者结合，可以让 AI 更准确地理解你的需求并生成高质量的 uView Pro 代码。

## 问题反馈

如果在使用 llms.txt 过程中发现内容有误或缺失，欢迎通过以下方式反馈：

- [GitHub Issues](https://github.com/anyup/uview-pro/issues)
- [Gitee Issues](https://gitee.com/anyup/uview-pro/issues)
