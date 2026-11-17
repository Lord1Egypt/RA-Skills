# LLM 反向提取 rubrics → OR 归因管道

完整执行记录(含首次结果表)见 REDoc `b61d031b113084e5690ded518dc9369b`。本文件为可复现操作手册。

## 目录

- [管道总览](#管道总览)
- [模型与调用配置](#模型与调用配置)
- [阶段一: 分层抽样](#阶段一-分层抽样)
- [阶段二: 归纳候选 rubrics](#阶段二-归纳候选-rubrics)
- [阶段三: 合并去重](#阶段三-合并去重)
- [阶段四: 逐会话判定](#阶段四-逐会话判定)
- [阶段五: OR + FDR](#阶段五-or--fdr)
- [质检清单](#质检清单)

## 管道总览

```
正负样本(留资/未留资 × exp/ctrl 分层抽样)
  → LLM 对比归纳候选 rubrics(8 批, 79 条)
  → LLM 单次合并去重(→18 条, 见 rubrics_final.json)
  → LLM 逐会话判定命中(600 会话 × 18 条)
  → 2×2 列联表 OR + Haldane-Anscombe + BH-FDR(scripts/or_fdr.py)
  → 质检(同义反复/halo)→ 有效因子表
```

rubric 定义纪律(三条硬约束, 写进归纳 prompt):
1. 必须可对单条会话客观判定命中/未命中;
2. 只描述 AI 侧动作/话术(不描述用户或结局);
3. 禁止与留资判定同义的特征。

复用捷径: 18 条 rubrics 起点库已在 references/rubrics_final.json——同域复跑直接跳过阶段二三, 从判定开始; 换域或数据形态大变才重新归纳。

## 模型与调用配置

- 端点: `https://maas.devops.xiaohongshu.com/customerserviceinference-glm-5/v1/chat/completions`
- 模型: `GLM-5.2-FP8`, header `api-key: <你的 MaaS api-key, 可向 @周浩 索取或在 QS 平台自行申请>`
- reasoning 走独立 reasoning_content 字段, content 干净无需剥离; **max_tokens 必须给足**(reasoning 吃限额)
- 参数: 归纳 temperature=0.3/max_tokens=6000; 合并 0.1/8000; 判定 **temperature=0/max_tokens=4000**
- 工程: urllib 直连(不依赖 openai SDK), ThreadPoolExecutor 并发(归纳 8/判定 12), 判定每条 3 次重试 + **jsonl 追加落盘断点续跑**(重跑前读已完成 id 集合跳过)
- 首次实绩: 判定 600/600 零失败, 全程约 8 分钟

## 阶段一: 分层抽样

留资/未留资 × exp/ctrl 四格各 150 条(共 600), 固定随机种子, **抽样池先剔除 L0**。样本携带: session key、分组、行业、宽口径标、压缩对话文本(规格见 data-schema.md 会话重建节)。

## 阶段二: 归纳候选 rubrics

批次设计: exp 正负对比 6 批 + ctrl 对比 2 批, 每批正负各 6 条(含行业标注)。

Prompt 模板:

```
你是私信客服对话分析专家。下面是小红书商家私信AI的会话样本: {npos} 条「留资成功」
(用户留下联系方式/点击留资组件) 和 {nneg} 条「未留资」。

请对比两组, 归纳出最能区分留资成败的 **AI侧动作/话术特征(rubric)**。要求:
1. 每条 rubric 必须是可对单条会话客观判定"命中/未命中"的行为描述(描述AI做了什么, 不是描述用户或结果)
2. 关注: 推进时机与方式、报价/信息交付策略、对用户问题的回应质量、话术风格、对拒绝/犹豫的处理、卡片使用方式等
3. 不要输出与留资判定同义的特征(如"用户留下了手机号")
4. 输出 8-10 条, 严格 JSON 数组: [{"rubric":"...", "direction":"利于留资|不利于留资"}]

【留资成功组】
{正样本×6, 含行业标注}

【未留资组】
{负样本×6, 含行业标注}

只输出 JSON 数组。
```

## 阶段三: 合并去重

单次 LLM 调用: 输入全部候选(带 direction), 要求合并同义项、保留最可判定表述、每条产出 `{id, rubric, criteria}`(criteria=一句话判定标准)。目标 15-20 条。

## 阶段四: 逐会话判定

每会话一次调用判定全部条目, 严格 JSON 输出。

Prompt 模板:

```
判定下面这条商家私信会话中, AI客服的行为是否命中每条 rubric。
注意: {易歧义条目的命中方向澄清, 如 R14 命中=顺势引导; R9 命中=出现无回复中断}。
仅依据会话中"AI"和"人工客服"角色的消息判定 AI 侧行为(以AI为主)。

【Rubrics】
{全部条目: id + rubric + criteria}

【会话】
{压缩对话文本}

严格输出 JSON(不要解释): {"R1":true/false, ..., "R18":true/false}
```

落盘 rubric_judgments.jsonl, 每行 `{"key":..., "group":..., "lead":..., "hits":{"R1":bool,...}}`。

## 阶段五: OR + FDR

用 `scripts/or_fdr.py`(输入 judgments jsonl, 输出每 rubric×每组的 OR/95%CI/p/BH-q):
- 每 rubric、每组分别建 2×2 列联表(命中×留资), OR=(a·d)/(b·c)
- Haldane-Anscombe +0.5 校正(任一格为 0 时全表+0.5)
- log-OR 正态近似 95%CI 与双侧 p
- 组内全部 rubrics 做 Benjamini-Hochberg FDR

解读纪律: **读因果只读 exp 列**(动作全量化近自然实验); ctrl 列仅交叉验证; 两组命中率差单独报作"执行差距"。

## 质检清单

判定结果出来后逐项过:
1. **同义反复**: 命中定义以结局为前提的条目(如"留资后跟进确认")OR 无归因意义, 剔除;
2. **halo 交叉验证**: LLM 版异常高 OR 的软性条目(如情绪价值)与规则版硬特征(emoji 正则)对比, 矛盾则标"疑 halo 待盲判";
3. **结局泄漏**: 会话文本含留资事件字样, 严格版应截断到首个留资事件前重判(首次未做, 已在局限声明);
4. **判定相关性**: 单次判全部条目导致条目间相关, FDR 偏保守, 引用效应量时声明;
5. 报告必须含"方法论局限"小节(相关非因果/结局泄漏/判定相关性三点)。
