# 如何使用 Thinking 技能

## 启用方式

`skills/thinking/` 技能包随 OpenClaw 启动自动加载，无需额外配置。

## 工作原理

1. OpenClaw 在会话启动时加载所有 skills
2. `skills/thinking/SKILL.md` 的内容被注入到 system prompt
3. AI 在每次推理时遵循 thinking protocol
4. 思考过程用 `thinking` 代码块包裹
5. 最终回复前进行 response preparation 检查

## 配置建议

### 在 AGENTS.md 中附加说明

```markdown
## Thinking Protocol

我已内建 Thinking-Claude 风格的全面思考流程：
- Inner monolog（内心独白）
- Progressive understanding（渐进理解）
- Error recognition & correction（错误识别与修正）
- Pattern recognition（模式识别）

思考格式：```thinking ... ```
```

### 在 TOOLS.md 中添加使用建议

```markdown
### 思考技巧

1. **保持自然** - 不要机械地列出步骤
2. **自我质疑** - 经常问 "Am I missing something?"
3. **逐步深入** - 从表面现象到深层原理
4. **及时修正** - 发现错误立即承认并解释
```

## 典型用例

### 案例 1: 技术问题
```
用户：解释 Transformer 架构
→ AI 使用 thinking block 分析注意力机制、位置编码、多头注意力
→ 最终给出清晰的技术解释
```

### 案例 2: 复杂推理
```
用户：分析 XXX 项目的可行性
→ AI 使用 multiple hypotheses 方法生成多个解读
→ 通过 error recognition 修正初步结论
→ 给出平衡的分析
```

### 案例 3: 代码调试
```
用户：为什么这段代码报错？
→ AI 首先复现问题场景
→ 然后分析错误堆栈
→ 识别根本原因
→ 提供修复方案
```

## 注意事项

1. **不要担忧 token usage** - thorough thinking 通常值得额外的 token
2. **保持流畅** - 思考应该是自然的对话，不是机械列表
3. **尊重用户** - 所有思考最终服务于高质量回复
4. **持续优化** - 根据反馈调整思考策略

## 性能影响

- **+% Tokens**：约 20-30%（取决于问题复杂度）
- **延迟**：几乎无感知（模型在流式输出时生成 thinking）
- **质量提升**：显著（深思熟虑的回复）

## 与 OpenClaw 的集成

| OpenClaw 组件 | 与 Thinking 的交互 |
|--------------|------------------|
| Session | in-memory, no persistence needed |
| Cron | 适合 background jobs（无需 thinking） |
| Sub-Agent | 可嵌套使用（子 agent 也遵循 protocol） |
| Skills | 作为独立 skill，可替换或禁用 |