# 留学助理 — Agent 生成模式样例（方案 A 存档）

> 日期：2026-08-12  
> 模式：引擎提供确定性上下文（画像/选校/教授/计划），**生成类产出由对话模型（agent）完成**  
> 申请人上下文（引擎实跑）：
>
> - 211 CS · GPA 3.5 · TOEFL 105 · GRE 320 · 科研（分布式共识，无论文）· 大厂后端实习
> - 目标：MS · systems/distributed
> - 引擎画像：54/100，短板 = research(40)/intern(45)/reco(40)
> - 引擎选校：reach MIT/Stanford · match Duke/USC · safety Florida/Northeastern
> - 引擎教授短名单：MIT / Stanford / CMU 的 systems 方向（占位，待核实实名）

---

## 1. 文书逐段反馈（agent 生成）

> 输入段（SOP 首段）："I have always been passionate about computer science. I did a distributed project and it went well."

**逐条批注：**

- 🔴 **开头空泛（high）**：`passionate about computer science` + `since I was young` 是招生官阅卷疲劳区，第一句决定阅读期待。  
  → **改写**：从具体事件切入，直接建立"你是个做系统的人"的印象：
  > "In my senior capstone, I built a replicated key-value store that kept serving reads through a two-node outage. Debugging that split-brain case is when I stopped wanting to be a computer scientist in general — and started wanting to build correct distributed systems."
- 🟡 **缺量化（mid）**：`went well` 是零证据描述。系统方向申请尤其看重数字。  
  → 补：吞吐、延迟、故障恢复时间、规模（节点数/数据量）、对比基线。
  > 示例：`after sharding, throughput went from 2k to 12k ops/s; leader failover recovered in <1.5s`
- 🟡 **缺方向匹配论证（mid）**：没有回答"为什么是 distributed systems + 为什么是这个项目"。  
  → 下一段结构：经历 → 提炼出的开放问题 → 该问题与目标项目的课程/教授/实验室的接点。
  > 例如落在：MIT 的 6.824 / Stanford 的 CS 244B 体系，或某教授关于一致性协议的论文。
- 🟢 **可保留**：分布式项目选题对口，是好素材；问题在**呈现密度**，不在题材。

---

## 2. 套磁邮件（agent 生成 · 首封）

> 对象：CMU systems/distributed 方向教授（占位 Prof. X，待实名后替换）  
> 特点：点名研究方向交集、亮出可度量经历、问题具体（RA/方向而非泛泛求建议）

```
Subject: Inquiry on building availability in distributed systems — Li Ming, [Univ] CS applicant (Fall 2027)

Dear Prof. [Last Name],

I'm Li Ming, a final-year CS student at [University] (GPA 3.5/4.0), applying for MS programs
in Fall 2027 focused on distributed systems.

In my capstone I built a replicated key-value store and spent most of my debugging time on
split-brain — reads stayed available but writes silently diverged. Your work on
[paper title / technique] addresses exactly the trade-off I struggled with: [one concrete
observation about the paper].

Two questions, if you have a moment:
1) Do you plan to take MS students as research assistants for Fall 2027?
2) What background (systems coursework / projects / math) would you recommend I strengthen
   before applying, given my interests?

I'd be glad to share my project write-up if useful.

Best,
Li Ming | [email] | [CV link]
```

**发送前检查**（agent 提示）：① 替换为实名教授 + 真读其近 2 年 1-2 篇论文并点到方法 ② 句子里的 `[paper title]` 必须写具体内容 ③ 不在申请截止前 1 个月群发 ④ 10 天无回复用跟进版（不重发全文）。

---

## 3. 30 天执行清单（agent 生成 · 融合引擎计划与画像短板）

> 依据：引擎计划 p0/p1/p2 阶段 + 画像短板（research 最低）。按周排，可执行、可打勾。

**Week 1（定位与科研启动）**

- [ ] 确定 1 个具体研究问题（基于分布式共识项目延伸：如"部分同步模型下的可用性-一致性权衡"）
- [ ] 联系本校 1 位做系统的老师，表达进组意愿（带 1 页 project write-up）
- [ ] 阅读 2 篇目标方向论文，每篇写 3 行"方法 + 局限 + 我的想法"

**Week 2-3（产出科研）**

- [ ] 在项目基础上做一个实验扩展（如引入分区故障，量化可用性指标）
- [ ] 目标：产出 1 份技术报告（可投 workshop 的水平），解决 research 短板
- [ ] 若在校内无合适导师，改远程 RA 或开源社区项目贡献（选一个能出可引用产出的）

**Week 4（标化与选校定稿）**

- [ ] 预约 TOEFL/GRE 考位（选校已出，反向确认考试时间线）
- [ ] 按引擎选校清单定 6-12 所，把 deadline 录入 `scripts/guide.py apps add`
- [ ] 向 2 位推荐人（科研导师 + 实习主管）发推荐信请求（附提纲，提前 1.5 个月）

> 逻辑：**科研短板是唯一红区** → 前 3 周全部资源砸科研产出；标化保持（已有 105/320），选校进入记录阶段。

---

## 4. 与 mock 的差异对照

| 维度   | 引擎 mock（规则模板）      | Agent 生成（本档）              |
| ---- | ------------------ | ------------------------- |
| 文书反馈 | 命中预设规则（空泛/缺量化/缺匹配） | 针对申请人真实经历给**改写示例**与结构建议   |
| 套磁   | 模板填空               | 点名研究方向交集 + 具体论文接点 + 双问题结构 |
| 执行清单 | 无（引擎只给计划阶段）        | 按短板归因生成周级可打勾动作            |
| 成本   | 0（规则）              | 对话模型推理                    |

**分工结论**：引擎负责确定性（画像/选校/教授/计划/倒计时），agent 负责生成性（反馈/套磁/清单）——二者通过 `SKILL.md` 的 Agent guide 串起来，即"方案 A"的完整形态。
