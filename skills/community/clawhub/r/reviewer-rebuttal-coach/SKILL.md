---
name: reviewer-rebuttal-coach
description: 从剪贴板读取审稿意见、导师批注或评审反馈，生成逐条回复、修改计划与优先级建议。
metadata: {"openclaw":{"emoji":"🧾","requires":{"bins":["node","pbpaste"]}}}
---

# Reviewer Rebuttal Coach

这是一个专门处理审稿意见、导师批注、答辩修改意见和项目评审反馈的 skill。

## 主要用途

当用户复制了以下内容之一时：
- 审稿人意见
- 导师批注
- 答辩修改意见
- 开题评审意见
- 项目评审反馈
- 编辑部修改建议

你需要：
1. 读取剪贴板文本
2. 提取意见要点
3. 按问题类型分类
4. 生成逐条回复建议
5. 生成修改任务清单
6. 标出优先级和风险点

## 调用方式

当用户说：
- 帮我回复审稿意见
- 读取剪贴板并生成答复
- 帮我把这些评审意见拆成修改任务
- 用剪贴板内容生成rebuttal

你应运行：

```bash
node {baseDir}/scripts/read_clipboard.mjs