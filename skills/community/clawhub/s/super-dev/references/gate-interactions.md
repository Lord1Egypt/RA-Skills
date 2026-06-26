# 门禁交互详细指南

## DOC_CONFIRM_GATE（文档确认门禁）

### 触发条件
三份核心文档（PRD + Architecture + UIUX）全部生成完毕。

### Agent 必须做的
1. 停止一切后续动作
2. 列出三份文档的完整路径
3. 请用户查看并确认
4. 等待用户明确说"确认"或执行确认命令

### 确认方式
```bash
# 用户在终端执行
super-dev review docs --status confirmed --comment "三文档已确认"
super-dev run --resume

# 或在对话中告诉 Agent "确认"/"可以继续"
# Agent 代为执行上述命令
```

### 状态文件
`.super-dev/.review-state/docs-confirmation.json`
```json
{
  "status": "confirmed",
  "updated_at": "2026-03-25T10:00:00Z",
  "actor": "user",
  "comment": "三文档已确认"
}
```

### 如果用户要求修改
1. 根据用户反馈修改对应文档
2. 重新展示修改后的文件路径
3. 再次请求确认

---

## PREVIEW_CONFIRM_GATE（预览确认门禁）

### 触发条件
前端实现完成，前端运行验证通过。

### Agent 必须做的
1. 展示前端预览路径或截图
2. 请用户查看效果
3. 等待用户确认满意

### 三种可能的用户反馈

**满意 -> 继续后端**
```
Agent: 你对前端效果满意吗？
User: 满意，继续
Agent: 好的，进入后端实现阶段...
```

**不满意 -> UI 返工**
```
Agent: 你对前端效果满意吗？
User: 不满意，配色太沉闷
Agent: 收到，我会：
  1. 更新 output/*-uiux.md 中的配色方案
  2. 重做前端
  3. 重新运行 UI 审查
  修改中...
```

**架构问题 -> 架构返工**
```
User: 这个页面结构不对，应该用 SPA 而不是 MPA
Agent: 收到，这涉及架构变更，我会：
  1. 更新 output/*-architecture.md
  2. 同步调整 Spec 和任务清单
  3. 重新实现
  修改中...
```

---

## 质量门禁（Quality Gate）

### 触发条件
红队审查 + 质量检查完成后。

### 通过（score >= threshold）
继续交付阶段。

### 未通过（score < threshold）
```
质量门禁未通过（{score}/{threshold}）

未通过项:
  - 类型覆盖率: {actual}% (要求 80%)
  - 安全问题: {count} 个高风险

修复步骤:
  1. 修复上述问题
  2. 重新运行: super-dev quality
  3. 确认: super-dev review quality --status confirmed
  4. 恢复: super-dev run --resume
```

---

## 状态机

```
                  +---> waiting_confirmation --+
                  |          (docs gate)        |
                  |                             v
started ---> running ---> waiting_ui_revision --+---> running ---> success
                  |     (preview gate: UI)      |
                  |                             |
                  +---> waiting_arch_revision --+
                  |     (preview gate: arch)     |
                  |                             |
                  +---> waiting_quality_rev ----+
                  |     (quality gate)          |
                  |                             v
                  +---> failed ---------> (resume) ---> running
```
