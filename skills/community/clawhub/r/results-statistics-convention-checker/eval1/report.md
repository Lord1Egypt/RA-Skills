# 统计报告规范诊断报告：英文心理学论文 Results 段落（baseline，未加载技能）

## 一、原文

> The results showed that the green view was better than the built view. According to the data analysis, most participants felt more relaxed after viewing the green view. A paired-sample t test was conducted to compare stress scores before and after viewing. The result was significant (t = 3.45, p < 0.05), which means the green view can effectively reduce stress. The stress score decreased from 4.82 ± 1.03 to 3.91 ± 1.12. A one-way ANOVA was performed to examine the effect of view type on attention restoration. There was a significant difference between the three groups (F = 8.76, p = .000). Post-hoc tests showed the green view group (M = 5.12) scored higher than the built view group (M = 4.03) and the mixed view group (M = 4.55, p < 0.05). For heart rate, the green view group showed lower values (62.3 ± 2.1 bpm) than the built view group (71.5 ± 1.8 bpm), and the difference was 12.9%. The correlation between preference and restoration was significant (p < 0.01). The regression analysis showed that preference significantly predicted restoration (p < 0.05), proving that H1 was supported. For skin conductance, there was no significant difference between groups (n.s.). The effect of view type on mood was slightly significant (p < 0.1).

## 二、总体评价

该段落的统计报告存在较多不规范之处。主要问题是统计量信息不完整、p 值写法不规范、缺少效应量，以及部分结论缺乏统计检验支撑。整体需要修改才能达到 APA 的统计报告要求。

## 三、逐句诊断

| # | 句子 | 诊断 |
|---|------|------|
| 1 | The results showed that the green view was better than the built view. | "better" 过于笼统，没有说明是哪个指标、好多少，也没有统计支撑。 |
| 2 | According to the data analysis, most participants felt more relaxed after viewing the green view. | "according to the data analysis" 是模糊表述，没有具体数据；"most participants felt" 没有报告人数、比例或检验。 |
| 3 | A paired-sample t test was conducted to compare stress scores before and after viewing. | 交代了检验方法，可以，但没有说明样本量。 |
| 4 | The result was significant (t = 3.45, p < 0.05)... | t 值后面缺少自由度，应写成 t(df) = 3.45。"which means the green view can effectively reduce stress" 的表述偏强。 |
| 5 | The stress score decreased from 4.82 ± 1.03 to 3.91 ± 1.12. | ± 没有说明是标准差还是标准误，读者无法判断。 |
| 6 | A one-way ANOVA was performed... | 方法交代句，可以接受。 |
| 7 | There was a significant difference between the three groups (F = 8.76, p = .000). | F 缺少自由度；p = .000 写法不对，p 不可能等于 0，一般应写 p < .001。 |
| 8 | Post-hoc tests showed the green view group (M = 5.12) scored higher than... | 只报告了 M，没有报告 SD；也没有说明用的是什么事后检验方法。 |
| 9 | For heart rate, ... the difference was 12.9%. | 直接说差异是 12.9%，但没有做任何统计检验，不知道这个差异是否显著；± 同样没有界定。 |
| 10 | The correlation between preference and restoration was significant (p < 0.01). | 只给了 p 值，没有给相关系数 r，读者不知道相关有多强、方向如何。 |
| 11 | The regression analysis showed that preference significantly predicted restoration (p < 0.05), proving that H1 was supported. | 没有报告回归系数 β 和 R²；"proving" 用词过强，统计结果不能"证明"假设。 |
| 12 | For skin conductance, there was no significant difference between groups (n.s.). | 不显著的结果也要报告具体统计量和 p 值，只写 n.s. 信息不足。 |
| 13 | The effect of view type on mood was slightly significant (p < 0.1). | p < 0.1 不能算显著，"slightly significant" 不是规范说法；如果确实在 0.05 到 0.1 之间，应如实报告精确 p 值。 |

## 四、系统性问题归纳

- **统计量不完整**：t、F 都缺自由度；相关和回归只报 p 值，没有 r、β 等核心统计量。
- **p 值报告不规范**：出现 p = .000；p < 0.1 被当作显著；前导零用法不统一（0.05 和 .000 并存）。
- **描述统计不完整**：多处只有 M 没有 SD；"±" 未界定是 SD 还是 SEM。
- **缺少效应量和置信区间**：全文没有任何 Cohen's d、η² 或置信区间，无法判断差异的实际大小。
- **部分结论缺乏检验支撑**：12.9% 的心率差异、"most participants felt more relaxed" 均无统计检验。
- **阴性结果报告不完整**：皮肤电结果只写 "n.s."。
- **措辞问题**："better""proving" 等表述与统计证据的强度不匹配。

## 五、修改建议

1. 给所有 t、F 补上自由度，写成 t(df)、F(df1, df2) 的形式；
2. 把 p = .000 改成 p < .001，全文统一 p 值写法；
3. 相关分析补 r 值，回归分析补 β 和 R²；
4. 主要结果补充效应量（如 Cohen's d、partial η²），有条件的补 95% 置信区间；
5. 所有 "±" 注明是 SD 还是 SEM，事后比较补上各组 SD；
6. 心率差异需要做 t 检验或方差分析后再下结论；
7. p < 0.1 的结果改为报告精确 p 值，不要写 "slightly significant"；
8. 不显著的结果也报告完整统计量。

## 六、结论

该段 Results 的统计分析思路基本清楚，但统计报告的规范性较差，需要系统补全统计量、自由度、效应量并规范 p 值写法后，才能达到 APA 期刊的报告标准。
