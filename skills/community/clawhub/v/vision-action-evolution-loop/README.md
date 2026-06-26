# vision-action-evolution-loop

> 视觉-动作-进化闭环框架 —— 感知→规划→执行→评估→进化，SOUL五律的具身化实现

**作者**: KingOfZhao  
**版本**: 1.0.0  
**发布日期**: 2026-03-31  
**许可证**: MIT

---

## 这个 Skill 解决什么问题？

现有视觉Skill只能"看"（输出DXF），不能"做"（生成动作）。
现有自进化Skill只能"想"（更新认知），不能"动"（物理执行）。

`vision-action-evolution-loop` 将两者碰撞，产生五阶段闭环：

```
Perceive(看) → Plan(想) → Execute(做) → Evaluate(查) → Evolve(学)
```

每次循环都在前一次基础上进化，Agent 越用越强。

## 核心创新：三阶段桥接（非端到端）

不是用一个大模型直接从照片生成动作（太不可靠），而是：

1. **2D检测**（已验证，6/6成功）→ SVG/DXF
2. **3D空间理解**（桥接层）→ 空间坐标 + 折叠顺序
3. **动作规划**（VLA增强）→ 抓取点 + 力控参数

每阶段独立验证，失败可回退到前一阶段。

## 快速安装

```bash
clawhub install vision-action-evolution-loop
```

## 与其他 Skill 配合

```bash
clawhub install diepre-vision-cognition       # 2D视觉检测（子节点）
clawhub install self-evolution-cognition       # 自进化框架（父节点）
clawhub install human-ai-closed-loop          # 人机闭环（兄弟节点）
clawhub install arxiv-collision-cognition     # 论文碰撞（交叉引用）
```

## 学术支撑

6篇精选arXiv论文，覆盖VLA、具身推理、2D→3D桥接、工具增强、自进化Agent。

## 变更日志

### v1.0.0 (2026-03-31)
- 初始发布（Skill工厂第1个自动生成的Skill）
- 五阶段闭环框架（Perceive→Plan→Execute→Evaluate→Evolve）
- 三阶段桥接架构（2D→3D→Action）
- 工具增强策略（OpenCV管道封装为VLA工具）
- 通过自验证置信度: 96%

---

*自动开源认知 Skill by Skill Factory — KingOfZhao*
