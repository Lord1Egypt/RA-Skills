---
name: vibe-coding-checker
displayName: Vibe Coding 可行性评估
version: 1.0.0
description: >
  描述一个功能或项目，AI 快速评估用 Cursor/Windsurf/Bolt 等 AI 编程工具能否独立实现，
  给出可行性判断、推荐工具、拆解路径和风险提示。
author: antonia-sz
tags: [vibe-coding, ai-coding, cursor, windsurf, developer, evaluation]
---

# Vibe Coding 可行性评估 ⚡

## 你能做什么

描述你想做的功能或项目，我帮你评估：

- **能不能**用 Cursor / Windsurf / Bolt 等 AI 工具独立完成？
- **哪个工具**最适合这个任务？
- **怎么拆解**成 AI 能处理的子任务？
- **哪里最容易卡住**，需要提前知道？

---

## 使用方式

### 快速问答

```
做一个小红书评论分析的 Chrome 插件，能 vibe coding 实现吗？
```

### 详细描述

```
我想做：
- 一个网页工具，用户上传 Excel，自动清洗数据（去重、格式化、填充缺失值），生成预览并下载
- 技术栈不限
- 我有基础 Python 知识
能 vibe coding 搞定吗？
```

---

## 评估维度

| 维度 | 说明 |
|------|------|
| 技术复杂度 | 逻辑是否清晰，还是需要深度领域知识 |
| Context 长度 | 单次能装进 AI 上下文窗口吗 |
| 外部依赖 | 第三方 API/SDK 是否有完整文档 |
| 调试难度 | 出错时 AI 能自我修复吗 |
| 前/后端难度 | 哪一层更适合 vibe coding |

---

## 输出格式

```
## 评估结论

✅ 可以独立 vibe coding 实现
（或 ⚠️ 需要部分人工介入 / ❌ 不建议纯 vibe coding）

## 推荐工具
- 主力：Cursor（复杂逻辑）
- 辅助：v0.dev（UI 原型）

## 拆解路径
1. 第一步：用 v0 生成 UI 框架（1小时）
2. 第二步：用 Cursor 实现 Excel 解析逻辑（2小时）
3. 第三步：...

## ⚠️ 风险提示
- Excel 格式多样，边界情况多，AI 可能漏掉某些格式
- 大文件性能优化需要人工介入

## 💡 实战建议
[具体的提示词策略或注意事项]
```

---

## 工具调用

```python
exec: python3 SKILL_DIR/scripts/evaluate_vibe.py --idea "功能描述"
```

---

## Vibe Coding 工具参考

| 工具 | 最适合 | 局限 |
|------|--------|------|
| Cursor | 复杂全栈项目、有大量代码的项目 | 需要懂一点代码才能 review |
| Windsurf | 全自动从零到一 | 超长项目容易失控 |
| Bolt / StackBlitz | 纯前端、原型演示 | 不适合复杂后端 |
| v0.dev | React UI 生成 | 仅限 UI，无业务逻辑 |
| Replit AI | 快速 demo、脚本 | 不适合大型项目 |
| Claude Code | 复杂重构、需要理解整个代码库 | 需要 terminal 环境 |
