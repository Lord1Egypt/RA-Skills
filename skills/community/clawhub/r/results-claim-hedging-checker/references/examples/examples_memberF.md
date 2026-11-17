# Examples for results-claim-hedging-checker

This file contains curated examples extracted from 8 classic psychology papers.
These examples are used by the Skill to diagnose issues related to claim strength,
hedging, causal language, and interpretation in the Results section.

---

## Example ID：F-01

Source：Milgram (1963), Journal of Abnormal and Social Psychology

Dimension：Hedging

Type：Positive Example

Original Sentence：
"Many subjects showed signs of nervousness in the experimental situation, and especially upon administering the more powerful shocks."

Why it is useful：
该句使用 "showed signs of" 谨慎描述观察到的行为，没有断言因果关系，也没有使用绝对化词语，是描述被试反应时规范使用 hedging 的典范。

Reusable Rule：
描述被试行为或情绪时，优先使用 "showed signs of""displayed""appeared to" 等表达，避免 "proved""caused" 等强动词。

Possible Application：
诊断时若发现用户使用 "proved that subjects were nervous" 或 "caused anxiety"，可引用此例建议替换为 "showed signs of nervousness"。

---

## Example ID：F-02

Source：Milgram (1963), Journal of Abnormal and Social Psychology

Dimension：Claim Strength / Interpretation

Type：Problem Example

Original Sentence：
"It is instructive to reprint their remarks at the point of defiance, as transcribed from the tape recordings:"

Why it is useful：
作者在 Results 部分使用 "instructive" 这一主观评价词，不属于纯结果报告，容易让读者感到作者在引导解释而非客观呈现数据。

Reusable Rule：
Results 中避免使用 "It is instructive to...""Interestingly,""Importantly," 等主观引导语，直接呈现结果即可。

Possible Application：
当用户草稿中出现类似主观引导语时，Skill 可指出该问题，并建议删除或改为中性过渡，如 "The transcribed remarks were as follows:"。

---

## Example ID：F-03

Source：Festinger & Carlsmith (1959), Journal of Abnormal and Social Psychology

Dimension：Claim Strength / Statistics

Type：Positive Example

Original Sentence：
"In this condition, the average rating was +1.35, considerably on the positive side and significantly different from the Control condition at the .02 level (t = 2.48)."

Why it is useful：
准确报告了均值、方向、显著性水平和 t 值，没有夸大或遗漏统计信息，claim strength 与数据完全匹配。

Reusable Rule：
报告组间差异时，应包含均值、方向、显著性水平和统计量（如 t 值），避免只给出 "显著" 或 "不显著" 的笼统结论。

Possible Application：
当用户只写 "the difference was significant" 而未报告具体数值时，可引用此例建议补充完整统计信息。

---

## Example ID：F-04

Source：Festinger & Carlsmith (1959), Journal of Abnormal and Social Psychology

Dimension：Interpretation in Results

Type：Problem Example

Original Sentence：
"In the One Dollar condition, since the magnitude of dissonance was high, the pressure to reduce this dissonance would also be high."

Why it is useful：
作者在 Results 部分用理论机制解释数据趋势，属于对原因的推测，应放在 Discussion。该句是"在结果部分提前解释原因"的典型问题。

Reusable Rule：
Results 中避免用理论机制解释数据，应直接报告统计比较结果；解释原因应留到 Discussion。

Possible Application：
当用户草稿中出现类似 "since X was high, Y should be high" 的推理句时，Skill 应提示将其移到 Discussion 或删除。

---

## Example ID：F-05

Source：Loftus & Palmer (1974), Journal of Verbal Learning and Verbal Behavior

Dimension：Hedging

Type：Positive Example

Original Sentence：
"It appears to be the case that the effect of the verb is mediated at least in part by the speed estimate."

Why it is useful：
使用 "It appears to be the case" 和 "at least in part" 进行双重限定，避免过度声称，体现了对间接证据的谨慎态度。

Reusable Rule：
提出中介或机制时，使用 "It appears that" "may be mediated by" "at least in part" 等 hedging 表达。

Possible Application：
当用户直接断言 "the verb caused higher speed estimates" 时，可引用此例建议改为更谨慎的表述。

---

## Example ID：F-06

Source：Loftus & Palmer (1974), Journal of Verbal Learning and Verbal Behavior

Dimension：Causal Language

Type：Problem Example

Original Sentence：
"Thus smashed leads both to more 'yes' responses and to higher speed estimates."

Why it is useful：
使用 "leads to" 暗示强因果关系。虽然实验操纵可支持因果，但 Results 中宜用更中性的 "was associated with" 或 "resulted in"，以避免过度声称。

Reusable Rule：
避免使用 "leads to" "causes" "determines" 等强因果动词，改用 "was associated with" "was related to" 或 "showed more... responses"。

Possible Application：
当用户草稿中出现 "X leads to Y" 时，Skill 应建议替换为 "X was associated with Y" 并说明理由。

---

## Example ID：F-07

Source：Elkin et al. (1989), Archives of General Psychiatry

Dimension：Hedging / Claim Strength

Type：Positive Example

Original Sentence：
"In the completer sample, there was evidence of significant superiority of imipramine-CM over PLA-CM (P=.006) on the HSCL-90 T."

Why it is useful：
使用 "there was evidence of" 进行适度 hedging，同时报告具体 p 值，既谨慎又具体，避免了 "proved superior" 的强断言。

Reusable Rule：
报告显著优势时，使用 "there was evidence of significant superiority" 而非 "proved superior" "was definitely better"。

Possible Application：
当用户写 "the treatment was significantly better" 时，可建议改为 "there was evidence of significant superiority" 并补充 p 值。

---

## Example ID：F-08

Source：Elkin et al. (1989), Archives of General Psychiatry

Dimension：Interpretation in Results

Type：Problem Example

Original Sentence：
"Because systematic or differential dropout can introduce bias in the results and affect the interpretation of findings, we compared those patients who completed treatment with those who did not on the major demographic and clinical variables obtained before treatment."

Why it is useful：
作者在 Results 中用 "Because..." 解释进行后续比较的原因，属于研究方法或讨论逻辑，不应出现在结果部分。

Reusable Rule：
Results 中避免用 "Because..." 解释分析动机，直接报告比较结果即可；理由应放在 Method 或 Introduction。

Possible Application：
当用户草稿中在报告结果前解释为什么做某个分析时，Skill 应提示将该解释移到 Method 或删除。

---

## Example ID：F-09

Source：Costa & McCrae (1988), Journal of Personality and Social Psychology

Dimension：Hedging / Claim Strength

Type：Positive Example

Original Sentence：
"It thus appears that aging, attrition, the passage of time, and the addition of a second sample together have relatively little effect on mean levels of any of the personality traits measured."

Why it is useful：
使用 "It thus appears" 和 "relatively little effect" 进行双重限定，结论与前面的数据展示一致，没有过度声称。

Reusable Rule：
总结多个因素的综合影响时，使用 "It appears that... have relatively little effect" 等表达，避免绝对化。

Possible Application：
当用户总结结果时写出 "these factors had no effect" 时，可引用此例建议改为 "appear to have relatively little effect"。

---

## Example ID：F-10

Source：Costa & McCrae (1988), Journal of Personality and Social Psychology

Dimension：Claim Strength / Effect Size

Type：Positive Example

Original Sentence：
"Although most of the correlations are statistically significant in these large samples, the majority are small in magnitude."

Why it is useful：
在报告显著性的同时强调效应量小，避免读者因显著性而高估实际意义，是 claim strength 与证据匹配的典范。

Reusable Rule：
报告显著结果时，如效应量小，应同时说明 "small in magnitude"，避免夸大实际意义。

Possible Application：
当用户只报告 "p < .05" 而未提及效应量大小时，Skill 可引用此例建议补充效应量信息。

---

## Example ID：F-11

Source：Cohen et al. (1983), Journal of Health and Social Behavior

Dimension：Causal Language / Interpretation

Type：Positive Example

Original Sentence：
"Since these are cross-sectional correlations, no causal inferences are implied. For example, it is possible that increased symptomatology caused increased stress, rather than that the stress caused the symptomatology."

Why it is useful：
主动说明数据性质，排除因果推断，并提供替代解释，是避免过度声称的典范。

Reusable Rule：
当数据为横断面相关时，应明确说明 "no causal inferences are implied"，并列出可能的反向因果或第三变量解释。

Possible Application：
当用户草稿基于相关结果做出因果结论时，Skill 应引用此例提醒添加类似限制声明。

---

## Example ID：F-12

Source：Cohen et al. (1983), Journal of Health and Social Behavior

Dimension：Interpretation in Results

Type：Problem Example

Original Sentence：
"Since perceived stress should generally increase with increases in objective cumulative stress levels, the PSS should be related to the number of life events. Moreover, these correlations should be higher when the life-event scores are based on the self-rated impact of the events, since impact scores reflect some of the same stressor appraisal measured by the PSS."

Why it is useful：
作者在 Results 中陈述理论预期（"should be related""should be higher"），属于假设或讨论内容，不应出现在结果部分。

Reusable Rule：
Results 中避免重述理论预期或假设，直接报告数据；预期应放在 Introduction 或 Discussion。

Possible Application：
当用户草稿在结果部分出现 "we expected that..." 或 "X should be related to Y" 时，Skill 应提示删除或移到其他部分。

---

## Example ID：F-13

Source：Asch (1956), Psychological Monographs: General and Applied

Dimension：Causal Language / Claim Strength

Type：Problem Example

Original Sentence：
"From the preceding analysis we draw the following conclusions: 1. The unanimously wrong majority produced a marked and significant distortion in the reported estimates."

Why it is useful：
使用 "produced" 暗示强因果关系，且 "draw the following conclusions" 属于 Discussion 内容，不应在 Results 中列出。

Reusable Rule：
Results 中避免 "produced" "caused" 等强因果词，改用 "was associated with" "showed significant differences"；结论性总结放到 Discussion。

Possible Application：
当用户草稿在结果部分写 "the manipulation produced a significant effect" 时，Skill 可建议改为 "the manipulation was associated with a significant difference"。

---

## Example ID：F-14

Source：Asch (1956), Psychological Monographs: General and Applied

Dimension：Interpretation / Subjective Language

Type：Problem Example

Original Sentence：
"It is helpful to consider that the area included between the two curves represents the majority effect, while the area below the experimental curve represents the resistance to the majority."

Why it is useful：
"It is helpful to consider" 是主观引导，且该句在结果部分解释图表的理论含义，超出纯报告范围。

Reusable Rule：
直接说明图表构成，删除 "It is helpful to consider" 等主观引导；图表含义可在 Discussion 中讨论。

Possible Application：
当用户草稿在结果部分出现 "It is helpful to note that..." 或 "This figure shows the effect of..." 时，Skill 可建议删除主观引导，直接描述数据。

---

## Example ID：F-15

Source：Asch (1956), Psychological Monographs: General and Applied

Dimension：Claim Strength

Type：Problem Example

Original Sentence：
"The results leave no room for doubt about the constancy of the effect produced by identical trials."

Why it is useful：
"leave no room for doubt" 过于绝对，即使数据一致，也应为未来研究留有余地，属于过度声称。

Reusable Rule：
避免 "leave no room for doubt" "prove" "definitely" 等绝对化表达，改用 "provide strong evidence" 并提及例外情况。

Possible Application：
当用户草稿中出现类似绝对化断言时，Skill 应建议改为 "provide strong evidence" 或 "strongly support"。

---

## Example ID：F-16

Source：Ainsworth & Bell (1970), Child Development

Dimension：Hedging / Interpretation

Type：Positive Example

Original Sentence：
"Although this might suggest that search behavior is especially activated by being left alone and reduced in the presence of the stranger, this interpretation is not advanced because of the contingencies of the stranger's behavior and her location near the door."

Why it is useful：
作者明确说明虽然数据可能提示某种解释，但因混淆因素而不采纳，体现了谨慎态度，是避免过度推断的典范。

Reusable Rule：
当存在混淆变量时，应主动说明 "this interpretation is not advanced because..." 避免误导读者。

Possible Application：
当用户草稿基于有混淆因素的数据提出解释时，Skill 可引用此例建议添加类似限制说明。

---

## Example ID：F-17

Source：Ainsworth & Bell (1970), Child Development

Dimension：Subjective Language / Claim Strength

Type：Problem Example

Original Sentence：
"Individual differences were conspicuous, instructive, and significantly correlated with other variables."

Why it is useful：
使用 "conspicuous""instructive" 等主观评价形容词，不符合 Results 客观报告的要求，且与统计结果混合，削弱了客观性。

Reusable Rule：
Results 中避免使用 "conspicuous""instructive""remarkable" 等评价性词语，改为客观描述差异范围或统计结果。

Possible Application：
当用户草稿中出现类似主观形容词时，Skill 应建议删除或替换为客观描述，如 "Individual differences varied widely and were significantly correlated with..."。

---

## Example ID：F-18

Source：Ainsworth & Bell (1970), Child Development

Dimension：Interpretation in Results

Type：Problem Example

Original Sentence：
"Contact-resisting behavior directed toward the mother occurred very rarely in the preseparation episodes because the mother had been instructed not to intervene except in response to the baby's demands, and therefore episodes 2 and 3 are omitted from the table."

Why it is useful：
作者在结果部分解释数据缺失的原因，属于方法学信息，不应出现在 Results，会导致结果部分结构混乱。

Reusable Rule：
数据缺失或未收集的原因应在 Method 中说明，Results 只需报告已分析的数据。

Possible Application：
当用户草稿在结果部分解释为什么某些数据未纳入分析时，Skill 应提示将该解释移到 Method 或脚注。

---

# Summary of Coverage

- **Positive Examples**: 10 条（F-01, F-03, F-05, F-07, F-09, F-10, F-11, F-16 等）
- **Problem Examples**: 8 条（F-02, F-04, F-06, F-08, F-12, F-13, F-14, F-15, F-17, F-18）
- **覆盖维度**：
  - 相关关系写成因果关系（F-06, F-13）
  - 使用过强动词（F-06, F-13）
  - 缺少 hedging 表达（F-02, F-14, F-15, F-17）
  - claim strength 与统计证据不匹配（F-10, F-15）
  - 在 Results 中提前解释原因（F-04, F-08, F-12, F-18）
  - 超出数据支持范围的推论（F-05, F-11, F-16）
