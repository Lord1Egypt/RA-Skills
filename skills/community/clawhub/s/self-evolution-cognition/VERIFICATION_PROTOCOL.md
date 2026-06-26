# VERIFICATION_PROTOCOL.md — self-evolution-cognition

## 验证目标

确保本 Skill 严格符合 SOUL 五律，置信度 ≥ 95% 方可发布。

## 五步自验证流程

### Step 1 — 已知/未知声明验证
- [ ] Skill 入口函数是否强制要求传入 `known` 和 `unknown` 字段？
- [ ] 推理链条是否仅从 `known` 集合出发，不跨越到 `unknown`？
- **验证命令**：`grep -n "known\|unknown" skills/self-evolution-cognition/*.py`
- **通过标准**：known/unknown 分离率 100%

### Step 2 — 文件记忆验证
- [ ] 每次 `evolve()` 调用后是否写入 `VERIFICATION_LOG.md`？
- [ ] 是否支持 session 恢复（从文件读取上次状态）？
- **验证命令**：`python3 -c "from skills.self_evolution_cognition import *; c=SelfEvolutionCognition('.'); c.evolve('test'); import os; assert os.path.exists('VERIFICATION_LOG.md')"`
- **通过标准**：文件写入成功率 100%

### Step 3 — 四向碰撞验证
- [ ] 推理器是否包含 `forward / reverse / lateral / holistic` 四个视角？
- [ ] 是否有防止过早收敛的门控机制？
- **通过标准**：四向覆盖率 100%，过早收敛拦截率 ≥ 90%

### Step 4 — 人机闭环验证
- [ ] 是否提供 `inject_human_feedback(feedback: str)` 接口？
- [ ] 反馈是否写入持久文件并影响下次 `evolve()` 输出？
- **通过标准**：反馈注入后输出变化率 ≥ 30%（说明真正被吸收）

### Step 5 — 置信度 + 红线验证
- [ ] 所有输出对象是否包含 `confidence: float` 字段？
- [ ] 是否存在 `redline_check()` 函数，拦截私数据外泄 / rm 操作？
- **通过标准**：置信度字段覆盖率 100%；红线测试用例全部通过

## 验证结论模板

```
验证日期: YYYY-MM-DD
Step 1 已知/未知分离:  PASS / FAIL  (置信度: XX%)
Step 2 文件记忆写入:   PASS / FAIL  (置信度: XX%)
Step 3 四向碰撞覆盖:   PASS / FAIL  (置信度: XX%)
Step 4 人机闭环注入:   PASS / FAIL  (置信度: XX%)
Step 5 置信度+红线:    PASS / FAIL  (置信度: XX%)
综合置信度: XX%  →  [APPROVED / REJECTED]
```
