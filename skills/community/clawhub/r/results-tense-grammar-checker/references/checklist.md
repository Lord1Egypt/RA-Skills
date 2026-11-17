# checklist.md — results-tense-grammar-checker 逐项检查清单

> 用途：诊断时逐项核对，确保输出稳定、可复现、可被汇总 Skill 整合
> 用法：每项回答 是 / 否 / 不适用；出现"否"即需修正后再输出诊断报告

---

## 一、范围检查（诊断前）

- [ ] 输入内容是否属于 Results 部分？（若为 Introduction/Method/Discussion，提示不在本 Skill 范围并停止）
- [ ] 是否已确认研究类型（实验 / 问卷 / 纵向 / 元分析）？（影响时态判断场景）
- [ ] 是否已明确目标格式（默认 APA）？
- [ ] 是否避免做超出本 Skill 范围的判断（统计计算、APA 统计格式、词汇选择、结构诊断）？

## 二、时态检查（Tense）

- [ ] 描述本研究的具体结果是否使用一般过去时（showed, was, were, revealed, indicated）？
- [ ] 描述图表/表格是否使用一般现在时（Figure X shows, Table X presents, As shown in）？
- [ ] 陈述领域共识/前人研究结论是否使用一般现在时（is consistent with, shows）？
- [ ] 同一句内、同一段内时态是否保持一致（无无理由切换）？
- [ ] 是否存在"把本研究结果写成一般现在时"的误用？
- [ ] 是否存在"把图表引用写成过去时"的误用？

## 三、主谓一致检查（Subject-Verb Agreement）

- [ ] data 是否按复数处理（data show / are / were，而非 data shows / is）？
- [ ] 复数主语（analyses, results, scores, ratings, parameters, groups）是否搭配复数谓语？
- [ ] "a series of / a number of + 复数名词"是否搭配复数谓语？
- [ ] 缩写主语（如 ICC 指 correlations）的谓语单复数是否与所指名词一致？
- [ ] 单数主语（analysis, effect, model）是否误配复数谓语？

## 四、冠词检查（Articles）

- [ ] 特指本研究中的变量/效应是否使用 the？
- [ ] 首次引入可数概念是否使用 a/an？
- [ ] 再次提及已引入概念是否使用 the（回指）？
- [ ] 是否存在 "a/an + 复数名词" 错误（如 a situations）？
- [ ] some/many/these + 复数名词处是否误加 the？
- [ ] 数值搭配（a median of, a mean of, a total of）冠词是否正确？

## 五、句子片段检查（Sentence Fragment）

- [ ] 正文中是否存在无主谓结构的独立句（片段）？
- [ ] 是否误把标题式名词短语写进正文？
- [ ] 标题/小节标题/图表注中的名词短语（合法片段）是否未被误判为错误？

## 六、run-on 检查（Run-on Sentence）

- [ ] 是否存在两个独立句仅以逗号连接（comma splice）？
- [ ] 长句是否依赖连接词（although, because, whether, which, when, whereas）组织？
- [ ] 是否需要将 run-on 拆分为两句或用连接词改写？

## 七、平行结构检查（Parallel Structure）

- [ ] neither…nor… / either…or… / both…and… 两侧结构是否对称？
- [ ] 比较结构 than/as 两侧对象范畴与结构是否平行？
- [ ] 并列列举（X or Y, X or Y）各组结构是否一致？
- [ ] 并列修饰语（higher X and higher Y）是否对称？

## 八、问题定位与证据（诊断中）

- [ ] 每个问题是否都有明确的问题定位（引用草稿原句）？
- [ ] 是否区分了"错误"与"可优化"（边缘例不误判为错误）？
- [ ] 是否引用了 examples_memberC.md 中的对应例句作为依据（如 C-T01）？
- [ ] 问题例（Problem Example）是否标注了真实来源，避免误导？

## 九、评分（按 rubric）

- [ ] 是否按 rubric.md 的 1–5 分档位评分？
- [ ] 是否输出分维度评分（Tense / SVA / Articles / Parallel / Fragment / Run-on）？
- [ ] 总分是否按加权规则计算并取整？

## 十、输出（诊断后）

- [ ] 是否按统一 Output Format 输出（Dimension Score / Key Problems / Evidence from Draft / Example-based Comparison / Revision Suggestions / Priority Level）？
- [ ] 是否对每个问题给出 Before / After 示例？
- [ ] 是否说明修改优先级（高 / 中 / 低）？
- [ ] 修改建议是否具体（指出问题 + 给替代表达），而非空泛表述（如"语言不够学术"）？
- [ ] 输出格式是否便于汇总 Skill（results-summary-report-generator）继续整合？
