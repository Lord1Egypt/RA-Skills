# Task Brief 模板

> 用于跨 agent 传递任务
> 使用时复制此模板，填写具体内容

---

## 基本信息

**task_id:** TQ-YYYYMMDD-XXX  
**from:** [我的 label]  
**to:** [对方 label]  
**type:** [code_task|spec_scan|code_review|test_request|decision_needed|report_request]  
**priority:** [P0|P1|P2]  
**deadline:** [YYYY-MM-DD HH:MM]

---

## 背景（≤100字，只写本任务必需的）

[最小化背景，只写对方需要知道的]

---

## 任务

[具体可执行的操作，清晰明确]

---

## 输入

- 文件路径: [路径]（只传路径，不贴内容）
- 配置信息: [关键配置]
- 依赖项: [依赖说明]

---

## 期望输出格式

根据 type 选择：

- **code_task** → 产出文件路径 + 编译结果
- **spec_scan** → 违规文件:行号:内容:建议
- **code_review** → ⚠️/❌/✅ + 文件:行号:说明
- **test_request** → 测试报告 + bug 列表
- **decision_needed** → 选项A/B + 我的建议 + 理由
- **report_request** → 结构化 Markdown 报告路径

---

## 完成后

**通知方式:**
```
sessions_send(label="[label]", message="[TASK_RESULT]...")
```

**汇报格式:**
```
[TASK_RESULT]
task_id: [task_id]
status: 完成/部分完成/跳过
结论: [3句话以内]
输出: [文件路径或结论]
下一步: [需要谁做什么，或"无"]
```

---

**创建时间:** [YYYY-MM-DD HH:MM]  
**创建人:** [label]
