# CI 与质量验证

qa-team-skills 是纯 Prompt 形态的 AI 技能，无 HTTP API 可调。质量验证由六套互补的脚本/方案构成，覆盖从静态结构到人工内容判定的不同层面。

## 验证脚本总览

| 脚本 | 验证层面 | 验证什么 | 耗时 |
|------|---------|---------|------|
| `ci/validate.sh` | 静态结构 | 文件齐全、SKILL.md 字段、prompt 必含章节、无硬编码行业词、版本一致 | < 1s |
| `ci/run-evals.sh` | 动态契约 | 触发评测（规则路由基线）+ prompt↔eval 契约断言 + 归档报告 | ~ 2s |
| `ci/test-memory-e2e.sh` | 行为模拟 | 记忆模块全生命周期：写入/合并/清理/转化/规范沉淀/历史加载（14 项断言） | ~ 1s |
| `ci/test-memory-stress.sh` | 长期压测 | 10 轮迭代：summary.json 体积/延迟不退化、无重复堆积、版本清理生效（6 项断言） | ~ 2s |
| `ci/run_llm_eval.py` | **真·LLM 端到端** | 接 LLM API 真调 skill，LLM-as-judge 按 assertion 判定产出内容质量 | ~ 4-6 分钟（8 条 eval） |
| `evals/human-review/README.md` | **人工双盲** | 2 名测试工程师对 AI 产出打 5 维分，验证内容质量（自动化查不出的） | ~ 4 小时/版本 |

## 使用方式

任何 prompt 或结构改动后，依次跑自动化脚本：

```bash
bash ci/validate.sh            # 1. 静态结构校验
bash ci/run-evals.sh           # 2. 触发评测 + 契约断言
bash ci/test-memory-e2e.sh     # 3. 记忆模块端到端
bash ci/test-memory-stress.sh  # 4. 记忆模块长期压测
python ci/run_llm_eval.py      # 5. 真·LLM 端到端（需 export KIMI_API_KEY）
```

前 5 套全过 = 自动化质量基线达标。发版前再做一次人工双盲评测（第 6 套）。

## 各脚本说明

### ci/validate.sh

检查项目结构完整性，由 `ci/forbidden.txt` 定义禁止硬编码的行业词清单。

**检查项**：
- 必需文件齐全（SKILL.md、7 个 skill 的 SKILL.md、模板、docs、examples）
- 每个 skill 含「防注入声明」「输出前自检」章节 + 双段式 description（何时用/何时不用）
- skills/ 与 SKILL.md 中无硬编码行业词（等保/三权分立/堡垒机等）
- VERSION 文件与 SKILL.md frontmatter 版本一致
- 无旧目录残留（prompts/ 应已删除）

### ci/run-evals.sh

把 `evals/` 下的评测数据集变成可执行的评测。

**两类检查**：

1. **触发评测（规则路由基线）** — 读 `evals/trigger-eval.json`，用 `ci/run-evals.sh` 内置的关键词规则跑路由，对照期望算准确率。这是 LLM 路由的对照下限——**LLM 路由准确率应 ≥ 此规则基线才算合格**。当前基线 51/51 = 100%。

2. **契约断言（skill↔eval）** — 把 `evals/functional-eval.json` 的 assertion 翻译成对 skill 文件的静态检查，捕获"skill 定义与 eval 期望"不一致（如标题写 10 个维度但 eval 要求 11 个）。当前 44/44 全过。

**归档报告**：每次运行输出 `evals/history/report-<version>-<时间戳>.json`，供跨版本对比，发现退化。

**Windows 注意**：脚本自动回退 `python`（`python3` 在 Windows 常是 Store 占位符），并清除 CRLF 换行避免字符串比较失败。

### ci/test-memory-e2e.sh

验证 `memory/README.md` 定义的记忆生命周期规则。用一个 python 模拟器复刻规则，在临时产品目录 `memory/data/products/e2e-test-module/` 上跑完整生命周期（测试完自动清理）。

**14 项断言覆盖**：

| # | 验证的行为 | 对应 README 章节 |
|---|----------|----------------|
| 1 | 首次写入创建目录结构 | 架构 |
| 2 | 增量写入多版本文件 | 增量写入 |
| 3 | 合并去重（同标题保留最早） | 汇总快照 |
| 4 | 重新编号 TC001..TCNNN | 汇总快照 |
| 5 | 复发检测（同类缺陷 ≥2 次） | 历史缺陷→用例转化 |
| 6 | 缺陷→用例转化 | 历史缺陷→用例转化 |
| 7 | 规范沉淀 + title 去重 | 规范库闭环 |
| 8 | 版本清理（>5 删最旧） | 版本清理规则 |
| 9 | latest.json 清理后仍保留 | 版本清理规则 |
| 10 | summary.json 索引字段正确 | 索引文件管理 |
| 11 | summary.recurring_patterns 正确 | 索引文件管理 |
| 12 | 跨会话历史加载记忆简报 | 跨会话历史加载 |
| 13 | latest.json 符合 schema | 数据模型 |
| 14 | summary.json 符合 schema | 数据模型 |

这是"规则契约测试"——确保 prompt 指令描述的记忆行为与 README 规范一致。真·AI 执行时的端到端验证由 `ci/run_llm_eval.py` 覆盖。

### ci/run_llm_eval.py

**真·LLM 端到端评测**——前四套脚本的最高层补充。结构校验查"文件齐不齐"，契约断言查"prompt 定义对不对"，记忆测试查"规则实现对不对"，但都查不出"AI 真跑一遍产出质量好不好"。本脚本接 LLM API 真调 skill，用 LLM-as-judge 判定产出内容质量。

**工作流程**：
1. 解析 `functional-eval.json` 每条 eval 的 prompt（自然语言触发）→ 按 skill 名匹配 `skills/xxx/SKILL.md` 作为 system prompt
2. prompt 剩余部分作为 user message 发给 worker 模型生成产出
3. 用 judge 模型按每条 assertion 判定 pass/fail（输出结构化 JSON）
4. 归档报告到 `evals/history/llm-report-<version>-<时间戳>.json`

**使用方式**：
```bash
export KIMI_API_KEY="sk-..."           # 必填，从环境变量读，绝不写入文件
python ci/run_llm_eval.py                    # 跑全量 functional-eval（8 条）
python ci/run_llm_eval.py --smoke            # 只跑第一条（冒烟，~50s）
python ci/run_llm_eval.py --concurrency 2    # 并发数（默认 2）
python ci/run_llm_eval.py --timeout 150      # 单次 LLM 调用超时（默认 120s）
```

**已验证发现的真实问题**（冒烟测试 prd-001）：
- `kimi-for-coding` 生成 prd 评审报告时**只列了 10 个维度，漏了第 11 个（业务分层）**——这是结构断言查不出、只有真调 LLM 才能发现的内容质量问题，说明 prompt 对"业务分层维度必输出"的约束需加强

**注意事项**：
- `kimi-for-coding` 是 reasoning 模型，`reasoning_content` 占大量 token，worker 的 `max_tokens` 需 ≥ 16k 才能保证 content 不被截断
- 模型仅允许 `temperature=1`
- 单条 eval 约 50s（1 次 worker + N 次 judge），全量 8 条并发 2 约 4-6 分钟
- API key 仅从 `$KIMI_API_KEY` 环境变量读，**脚本和归档报告均不写入 key**
- 退出码：准确率 < 70% 或有 error 视为失败

### ci/test-memory-stress.sh

长期积累压测——模拟 10 轮迭代持续写入，验证 `memory/README.md` 定义的清理/去重规则在长期使用下不退化。用临时产品目录 `memory/data/products/stress-test-module/` 跑完自动清理。

**6 项断言覆盖**：

| # | 验证的行为 | 实测结果 |
|---|----------|---------|
| 1 | summary.json 体积线性增长（比值 ≤ 5x） | 第 1 轮 520B → 第 10 轮 586B，1.1x ✔ |
| 2 | 读取延迟不退化（比值 ≤ 3x） | 0.23ms → 0.12ms，0.5x ✔ |
| 3 | latest.json 去重生效（无重复堆积） | 50 条含 20 重复 → 30 条唯一 ✔ |
| 4 | 版本清理生效（保留最近 5 个） | 10 轮后保留 v1.5–v1.9 ✔ |
| 5 | standards.json 标题 hash 去重 | 10 轮含 2 重复 → 8 条 ✔ |
| 6 | latest.json 清理后保留全部合并数据 | 30 条不因版本删除丢失 ✔ |

**发现并修复的真实缺陷**：原 `merge_latest` 只读磁盘现存版本文件，版本清理删除旧版本后，**早期版本中的唯一用例会丢失**。已修复为"以现有 latest.json 为基线再并入新版本"，回填到 `test-memory-e2e.sh` 保持一致。

**P1 去重硬保护**：`standards.json` 写入时增加 `title_hash`（MD5）字段做硬去重，防止标题大小写/标点差异绕过字符串比较。

### 人工双盲评测（evals/human-review/README.md）

自动化层查不出"维度分析对不对、用例合不合理、根因有没有逻辑"——这些是内容质量，需测试专家人工判定。方案定义：

- **5 维度评分**（完整性/准确性/可执行性/深度/实用性，每维 1-5 分）
- **双盲流程**（2 名评审员独立评分，分歧 ≥1.5 分当面校准）
- **版本门槛**（平均分 ≥3.8 准予发布，3.5–3.8 部分重评，<3.5 不予发布）
- **报告模板**（评分表 CSV + 版本报告 Markdown，归档到 `evals/human-review/`）

详见 `evals/human-review/README.md`。每版本发布前跑一次，约 4 小时（2 人 × 8 条 × 15 分钟）。

## 评测金字塔

六套脚本从底到顶，每层过滤不同问题，最大化人工投入价值：

| 层 | 查什么 | 发现什么 | 自动化 |
|----|--------|---------|--------|
| 结构校验 | 文件/字段 | 缺失、不一致 | ✅ |
| 契约断言 | prompt↔eval 一致性 | 定义与期望不符 | ✅ |
| 记忆端到端 | 规则实现 | 行为偏离 README | ✅ |
| 长期压测 | 持续使用 | 性能退化、重复堆积 | ✅ |
| LLM 端到端 | AI 产出 vs 断言 | 漏维度/字段（结构层） | ✅ |
| **人工双盲** | **内容质量** | **分析对不对、用例合不合理、根因有逻辑** | ⚠️ 人工 |

人工评测在金字塔顶端——前面所有自动化层过滤掉结构/规则问题后，人工只评"内容是否真有用"。

## 仍未覆盖的验证方法

| 方法 | 说明 | 优先级 |
|------|------|--------|
| 安全对抗评测集 | 针提示词注入、越权、数据外泄的对抗用例 | P2 |

## 集成到 CI 流水线

在 PR 合并前自动跑五套自动化脚本，任一失败阻断合并：

```yaml
# .github/workflows/qa-skill-check.yml 示例
- name: 静态结构校验
  run: bash ci/validate.sh
- name: 评测 runner
  run: bash ci/run-evals.sh
- name: 记忆模块端到端
  run: bash ci/test-memory-e2e.sh
- name: 记忆模块长期压测
  run: bash ci/test-memory-stress.sh
- name: LLM 端到端评测
  env:
    KIMI_API_KEY: ${{ secrets.KIMI_API_KEY }}
  run: python ci/run_llm_eval.py
```

`run-evals.sh` 和 `run_llm_eval.py` 产生的 `evals/history/*.json` 可作为 artifact 归档，用于版本间准确率对比。人工双盲评测在发版前离线执行，报告归档到 `evals/human-review/`。
