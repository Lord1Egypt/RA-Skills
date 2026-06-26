---
when: 想看完整前后对照走查,或某段不确定该归哪类
topics: walkthrough, marketing-strategy-pmm, before-after, classification
---

# 走查 1:marketing-strategy-pmm(论文 Appendix A)

## 原始(12,019 tok)

**description(87 tok)**:
> "Product marketing, positioning, GTM strategy, competitive intelligence... Use when developing positioning, planning product launches, creating messaging, analyzing competitors, entering new markets, enabling sales, or when user mentions product marketing, positioning, GTM, go-to-market..."

**body(2,543 tok)**:KPI、方法论步骤、决策标准、workflow 解释、persona 消息示范、HubSpot 配置片段,全混在一个文件。

**4 个 reference 文件(9,476 tok)**

## Stage 1:description 压到 32 tok(-63%)

> "Product marketing, positioning, GTM strategy, competitive intelligence. Tools: ICP definition, April Dunford methodology, launch playbooks, battlecards, market entry guides"

DDMIN 发现"Use when..."那一长串触发词是冗余的——router 从特征关键词(ICP / Dunford / battlecards)就能推断触发条件。

## Stage 2:body 分类 + 压缩

| 原段落 | 分类 | 处理 |
|--------|------|------|
| KPI、方法论步骤、决策标准 | `core_rule` | 合并为 bullet,压到 540 tok(-79%) |
| workflow 解释 | `background` | 拆 `background.md`(602 tok) |
| persona 消息示范 | `example` | 拆 `examples.md`(684 tok) |
| HubSpot 配置片段 | `template` | 拆 `templates.md`(327 tok) |

## Stage 2:references 跨文件去重(9,476 → 6,691 tok, -29%)

每个 ref 加 when / topics metadata。

## 端到端成本

- core-only 调用(不触发 read_file):12,019 → 540 tok(**-96%**)
- 全量加载(所有 ref 都被 read):12,019 → 7,231 tok(-40%)
- Gate 2:score_C = 1.0 vs score_A = 0.93 → less-is-more

## 关键教训

1. **触发词枚举通常可删**。关键词本身就是触发词
2. **HubSpot 配置**看起来像"背景说明",其实是 template(可复用模板),必须单独拆
3. **Persona 消息示范**是 example 不是 core_rule。rule 本身是"按 X 风格写",风格**示范**是 example,应按需加载

---

# 走查 2:常见误分类

## examples-as-specification 陷阱

原文:
> "You should respond like this:
> Q: How do I deploy?
> A: Run `make deploy` in the staging/ directory, then check logs at /var/log/app.log"

**错分**:整段 → `example`
**问题**:`make deploy`、`staging/`、`/var/log/app.log` 这些操作项会在 Faithfulness 丢失
**正确**:
- core_rule:"部署命令 `make deploy`,工作目录 `staging/`,日志 `/var/log/app.log`"
- example:保留 Q&A 对话形式作为风格示范

## redundant 误判

原文 body 的最后一段:
> "See references/api-spec.md for the full API specification."

**错分**:`core_rule`(看起来是指令)
**正确**:`redundant`。这是 progressive disclosure 的路由提示,在 Stage 2 应由自动生成的 `when:` metadata 替代,原段丢弃。

## background 中藏阈值

原文:
> "Our pipeline was designed for low latency, which is why we use a 500ms timeout instead of the default 30s."

**错分**:整段 → `background`
**问题**:"500ms timeout" 是操作阈值,丢了就错
**正确**:
- core_rule:"timeout 500ms(不是默认 30s)"
- background(可选):"为什么 500ms"的解释移到 background.md

---

# 走查 3:该退休的 skill

Stage 1 validation:无论原 desc 还是压缩 desc,在所有测试查询上 router 都不触发。
Condition D(无 skill)的任务评分 = Condition A(原 skill)≈ Condition C(压缩版)。

→ 标"候选退休",不强制删除,让用户决定。
