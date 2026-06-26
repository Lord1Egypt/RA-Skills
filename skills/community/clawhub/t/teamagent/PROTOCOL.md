# TeamAgent 任务拆解与执行协议 v2.0

> 核心协议：定义任务如何被拆解、分配、执行和审核。
> v2.0 新增：主Agent自主拆解（Solo）、并行组（parallelGroup）、审批控制（requiresApproval）

---

## 一、任务模式

| mode | 含义 | 拆解方式 |
|------|------|----------|
| `solo` | 内部任务，用户+自己的AI团队 | **主Agent拆解**（isMainAgent=true）|
| `team` | 多人协作 | 千问API拆解 |

---

## 二、步骤格式（v2.0）

```json
{
  "title": "步骤标题",
  "description": "详细描述",
  "assignee": "Agent名字（单个，匹配团队成员）",
  "requiresApproval": true,
  "parallelGroup": null,
  "inputs": ["输入依赖"],
  "outputs": ["产出物，文件写文件名如 报告.md"],
  "skills": ["需要的技能"],
  "stepType": "task"
}
```

### 字段说明

**requiresApproval**（bool）
- `true` = 步骤完成后需人类审批才能继续（关键决策、最终产出）
- `false` = 完成后自动流转（常规执行步骤）

**parallelGroup**（string | null）
- `null` = 顺序执行
- 相同字符串（如 `"调研"`）= 同组步骤可以**同时并行执行**

**stepType**
- `task` = 普通执行步骤
- `meeting` = 会议步骤（需填 participants + agenda）
- `decompose` = 主Agent拆解步骤（系统内部使用）

---

## 三、Solo 模式主Agent拆解流程

```
用户点「主Agent拆解」
    ↓
服务器检测 task.mode === 'solo' + 有 isMainAgent=true 的 Agent
    ↓ 是
创建 stepType='decompose' 步骤，分配给主Agent
SSE 通知主Agent（step:ready, stepType=decompose）
    ↓
主Agent 收到通知
→ 认领步骤（POST /api/steps/{id}/claim）
→ 获取团队成员能力（GET /api/agents/team）
→ 调用 LLM 生成步骤 JSON
→ 提交（POST /api/steps/{id}/submit，result = JSON数组）
    ↓
服务器检测 stepType=decompose 提交
→ 解析 JSON → 批量创建 TaskStep
→ parallelGroup 相同的步骤同时设为 pending
→ 通知各 assignee Agent（step:ready）
→ decompose 步骤自动标为 done
    ↓ 无主Agent
提示用户「请先配对并绑定主Agent」
```

## 四、Team 模式千问拆解流程

```
用户点「AI 拆解」（task.mode === 'team'）
    ↓
服务器调用千问 API（QWEN_API_KEY）
→ 输入：任务描述
→ 输出：JSON步骤数组（含 parallelGroup + requiresApproval）
    ↓
批量创建步骤，通知可立刻开始的 Agent（各并行组第一步）
```

---

## 五、主Agent拆解输出示例

```json
[
  {
    "title": "文献调研",
    "description": "调研相关领域已发表论文",
    "assignee": "Galileo",
    "requiresApproval": false,
    "parallelGroup": "调研",
    "outputs": ["文献报告.md"],
    "skills": ["文献检索"]
  },
  {
    "title": "可行性分析",
    "description": "分析数据质量和发表可行性",
    "assignee": "Compass",
    "requiresApproval": false,
    "parallelGroup": "调研",
    "outputs": ["可行性分析.md"],
    "skills": ["数据分析"]
  },
  {
    "title": "综合评估报告",
    "description": "综合以上输出，给出结论",
    "assignee": "Quill",
    "requiresApproval": true,
    "parallelGroup": null,
    "inputs": ["文献报告.md", "可行性分析.md"],
    "outputs": ["评估报告.md"]
  }
]
```

---

## 六、Skill 命令（agent-worker.js）

```bash
node agent-worker.js check       # 检查待执行步骤
node agent-worker.js decompose   # 执行所有待拆解任务（主Agent专用）
node agent-worker.js run         # 执行一个步骤（decompose 优先）
node agent-worker.js watch       # 持续监控（30秒，自动处理 decompose）
node agent-worker.js suggest     # 为完成的任务建议下一步
```

---

## 七、步骤提交格式

```bash
POST /api/steps/{id}/submit
Authorization: Bearer ta_xxx

{
  "result": "步骤结果描述（decompose步骤时为JSON数组）",
  "summary": "AI生成摘要（可选）",
  "attachments": [
    { "name": "文件名.pdf", "url": "/uploads/tasks/xxx/文件名.pdf", "type": "application/pdf" }
  ]
}
```

---

*深海无声，代码不停 🌊*
