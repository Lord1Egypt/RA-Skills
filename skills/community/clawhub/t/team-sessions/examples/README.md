# 使用场景示例

## 场景一：内容创作团队

### 团队构成
- **策划** — 选题、大纲
- **写手** — 内容创作
- **审核** — 质量检查

### 工作流程

```
主代理：派策划写大纲
  ↓ sessions_spawn → 策划 workspace
策划：产出大纲.md
  ↓ 主代理读取
主代理：派写手扩写正文
  ↓ sessions_spawn → 写手 workspace  
写手：产出正文.md
  ↓ 主代理读取
主代理：派审核检查质量
  ↓ sessions_spawn → 审核 workspace
审核：产出 review.md
  ↓ 主代理读取
主代理：汇总，交付用户
```

### 代码示例

```javascript
// 派策划
sessions_spawn({
  agentId: "planner",
  cwd: "~/.qclaw/workspace-main/planner",
  task: `【任务 P001】写大纲

主题：AI 团队管理最佳实践
交付物：大纲.md（三级标题结构）
禁止：不写正文，只写结构`,
  mode: "run"
})

// 派写手
sessions_spawn({
  agentId: "writer",
  cwd: "~/.qclaw/workspace-main/writer",
  task: `【任务 W001】扩写正文

大纲：${大纲内容}
交付物：正文.md（3000字）
禁止：不使用 Markdown 标题`,
  mode: "run"
})
```

---

## 场景二：数据分析团队

### 团队构成
- **采集** — 数据抓取
- **清洗** — 数据处理
- **分析** — 生成报告

### 工作流程

同上模式，只是角色不同。

---

## 场景三：个人多角色

即使一个人，也可以用多个子代理扮演不同角色：

- 理性分析者
- 创意发散者
- 批判检查者

每个角色独立 workspace，互不干扰。
