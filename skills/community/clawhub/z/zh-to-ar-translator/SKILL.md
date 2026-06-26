---
name: zh-to-ar-translator
description: 中阿翻译工具。将中文词汇翻译成符合沙特当地使用习惯的阿拉伯语。
---

# 中阿翻译工具

## 功能

将中文词汇翻译成沙特习惯的阿拉伯语。

## 词典

内置常用词词典，可扩展。

## 使用方法

### 命令行

```bash
node ~/.openclaw/workspace/skills/zh-to-ar-translator/index.js "中文词汇"
```

### 示例

```bash
node ~/.openclaw/workspace/skills/zh-to-ar-translator/index.js "无线蓝牙耳机"
# 输出: سماعات بلوتوث لاسلكية
```

### 批量翻译

```bash
node ~/.openclaw/workspace/skills/zh-to-ar-translator/index.js "无线" "蓝牙" "耳机"
```

## 依赖

无（纯 JS 实现）

## 翻译示例

| 中文 | 阿语 |
|------|------|
| 无线蓝牙耳机 | سماعات بلوتوث لاسلكية |
| 蓝牙耳机 | سماعات بلوتوث |
| 无线 | لاسلكي |
| 蓝牙 | بلوتوث |
| 耳机 | سماعات |
| 可折叠拉车 | عربة تسوق قابلة للطي |
| 买菜车 | عربة تسوق |
