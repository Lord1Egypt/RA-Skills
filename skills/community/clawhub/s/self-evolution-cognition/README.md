# self-evolution-cognition

> 核心自进化认知框架 —— 让 Agent 拥有 KingOfZhao 的思考操作系统

**作者**: KingOfZhao  
**版本**: 1.1.0  
**发布日期**: 2026-03-31  
**许可证**: MIT

---

## 这个 Skill 解决什么问题？

普通 Agent 每次对话都从零开始，没有记忆，没有自我进化能力。  
`self-evolution-cognition` 将 **SOUL 五律**固化为可调用的认知模块，使 Agent 能够：

- 每次推理前强制分离已知/未知，避免幻觉
- 将所有思考过程写入文件，实现跨 session 记忆
- 用四向碰撞推理代替线性思考，挖掘隐藏洞见
- 接受人类反馈后真正更新内部世界模型
- 对所有输出标注置信度，不确定时主动暂停

## 快速安装

```bash
clawhub install self-evolution-cognition
```

## 核心 API

```python
from skills.self_evolution_cognition import SelfEvolutionCognition

cog = SelfEvolutionCognition(workspace=".")
result = cog.evolve(
    task="分析这段代码的潜在风险",
    known=["代码结构", "依赖关系"],
    unknown=["运行时行为", "并发场景"]
)

# result.output        — 四向碰撞后的最终结论
# result.confidence    — 置信度 (0.0 ~ 1.0)
# result.collision_log — 四向推理详情
# result.file_written  — 写入的记忆文件路径

cog.inject_human_feedback("我在生产环境发现了一个并发 bug，复现步骤是...")
```

## SOUL 五律速查

| 律 | 核心思想 | 实现方式 |
|----|---------|---------|
| 已知/未知 | 推理从已知出发 | `known/unknown` 强制参数 |
| 文件即记忆 | 思考写入文件 | 自动写 `VERIFICATION_LOG.md` |
| 四向碰撞 | 禁止过早收敛 | 4个视角并行推理 |
| 人机闭环 | 人类证伪注入 | `inject_human_feedback()` |
| 置信度+红线 | 不确定时暂停 | `confidence` 字段 + 红线守护 |

## 与其他 Skill 配合

```bash
clawhub install self-evolution-cognition
clawhub install human-ai-closed-loop      # 人机闭环增强
clawhub install arxiv-collision-cognition  # 文献碰撞推理
clawhub install diepre-vision-cognition    # 视觉认知扩展
```

## 变更日志

### v1.1.0 (2026-03-31)
- 新增学术参考文献（6篇精选arXiv论文）
- SAGE四Agent闭环与四向碰撞推理的理论对应关系
- 具身智能自进化路径引入
- Agent记忆体系学术支撑

### v1.0.0 (2026-03-31)
- 初始发布
- 实现 SOUL 五律全覆盖
- 通过自验证置信度: 97%

---

*开源认知 Skill by KingOfZhao*
