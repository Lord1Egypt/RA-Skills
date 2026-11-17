# 小红书赛道深度分析引擎（XHS Track Analysis）

> 品牌进入品类、推出新品或重做内容策略之前，通过公开内容（笔记、达人主页、评论）看清五件事：**用户在问什么、平台内容怎样回答、谁在讲且谁更可信、用户到底信不信、赛道供给是否饱和**，最终形成带证据边界的品牌建议与 GO/NO-GO 决策结论。

## 一句话定位

不是市场规模估算，也不是平台算法逆向，而是把内容、达人和评论放在同一张桌面看的赛道判断方法。产出可执行的投决结论，而非一份"最近什么火"的报告。

## 架构

```
xhs-track-analysis/
├── SKILL.md                       # 入口（工作流 + 输出契约 + 诚实边界 + 原创性声明）
├── references/
│   ├── methodology.md             # 完整方法论（四分组、意图标注、四排序、长尾、达人生态位、四行为、供给结构、风险扫描）
│   ├── case-study.md              # 匿名化演示案例与数据（不含真实个人/品牌）
│   ├── table-template.md          # 赛道分析主表字段定义与样例
│   ├── data-sources.md            # 真实数据获取路径、采集字段模板与质检清单
│   └── collection-playbook.md     # 浏览器自动化采集 → 结构化整理的执行协议（v3.0 新增）
├── scripts/
│   ├── scaffold_table.py          # 一键生成空主表骨架（Markdown，含参数校验）
│   ├── finalize_report.py         # 主表自检 + 一键生成决策简报（交付门禁）
│   ├── collector/                 # 受监督有界采集器（T4 公开页主粮）
│   └── integrations/              # 官方/第三方数据源接入骨架（A 方案）
├── evals/
│   └── trigger_cases.json         # 回归测试集（触发词回归 + 防晒霜分析逻辑回归）
├── trace-schema.json              # 执行轨迹契约
└── README.md
```

## 工作流（Pass-by-Pass）

| Step | 动作 | 产出 |
|------|------|------|
| 0 | 定义问题：最想看懂什么 / 品牌要做什么选择 / 结论交给谁 | 三问 |
| 1 | 关键词四分组 + 意图标注（发现/了解/比较/决策） | 关键词表 |
| 2 | 多排序采集（最新/赞/藏/评）+ 长尾检查 | 采集记录 |
| 3 | 多轮合并去重：同一笔记只留一份，保留全部出处 | 去重后笔记 |
| 4 | 内容 + 达人分析：角色生态位（种草/测评/专家/官方） | 达人可信边界 |
| 5 | 评论分析：四行为 + 评论者类型 + 自来水 + 购买意图分层 | 评论归类 |
| 6 | 品牌建议 + 供给结构 + 风险扫描 + 决策收敛 | 决策结论 |
| 7 | 交付决策简报：`finalize_report.py` 自检 + 一键生成简报 | 决策简报 |

## 快速开始

```bash
# 1. 生成空主表骨架
python3 scripts/scaffold_table.py "熟龄抗老" 赛道分析主表.md

# 2. （可选）用 mock 数据源跑通采集管线演示
cd scripts/integrations && python3 run_pipeline.py config.example.json && cd ../..

# 3. 采集公开数据（受监督，需本人扫码）：
#    复制 scripts/collector/config.example.json → config.json 并填关键词
#    python3 scripts/collector/collect.py config.json --debug

# 4. 填写主表后自检 + 一键生成决策简报（交付门禁）
python3 scripts/finalize_report.py 赛道分析主表.md
```

```text
# 发起分析
做一份小红书赛道分析：熟龄抗老
分析XX品类在小红书的内容生态，我们要进这个赛道
```

## 数据获取（真实数据从哪来）

本 Skill 是「分析方法 + 输出框架」。真实数据通过以下路径注入：

- **浏览器自动化采集**（主粮，详见 `references/collection-playbook.md`）：`scripts/collector/collect.py` 受监督采集「关键词 × 排序」笔记与评论
- **浏览器插件 / 人工**：网页端按关键词 + 排序边看边采（仅公开页面、控频）
- **第三方数据平台**：千瓜 / 新红 / 蝉妈妈 / 灰豚 —— 补量级与趋势
- **官方商业平台**：蒲公英（达人 / 笔记 / 报价）、聚光（搜索词 / 行业大盘）

## 输出契约

最终交付 = 《赛道分析主表》（字段定义见 `references/table-template.md`）+ 品牌建议（含证据边界）+ **《决策简报》**（`finalize_report.py` 一键生成，作为投决摘要）。采集产物经 `finalize_report.py --focus` 可生成《重点笔记候选》。

## 诚实边界与原创性

- 基于公开内容**抽样**，不代表全量用户；样本量与关键词覆盖决定结论上限
- 排序/重合观察**不能反推平台算法**
- 工具与流程**不替代品牌策略判断**；真实商业结果仍需品牌自有曝光/点击/成交数据验证
- **原创性声明**：方法论、流程、脚本均为原创；`references/case-study.md` 为**匿名化演示数据**，人物/品牌/笔记均为虚构代号，不指向任何真实个人或商业主体
- **重投放品类须打折解读**：商业化浓度高的内容其"用户问题/评论"信号要打折
- **赛道分析有保质期**：采集时间距分析 > 90 天的内容须标"需复核"

## 品牌归属

- 擎漫网络 | Qomob.AI

---

## License

MIT License

Copyright (c) 2026 擎漫网络 | Qomob.AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

# 加入群聊

<div align="center">
  <img src="https://qomob.ai/xskill.jpg" width="600" alt="XSkill">
</div>
