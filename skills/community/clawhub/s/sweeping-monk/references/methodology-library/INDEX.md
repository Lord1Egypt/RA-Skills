# 方法论卡库索引 INDEX

> 自动生成（八卦炉 `scripts/build_index.py`）。共 **33** 张卡（深卡 7 + 方法卡 26）/ **82** 个方法块，归并为 **21** 个 pattern 聚类。

> 取招路径：按「症状或根因」定位 pattern 聚类 → 聚类内按 trigger 挑最贴的方法 → 打开对应卡读全文。

> `原名` 为该方法的原始模式词（卡内 `pattern_raw` 字段），便于追溯归并前语义。


## 一、按 pattern 聚类（扫地僧「博览」入口）


### pattern: assumption-surfacing  （1 个方法）

- 卡：`deep_圣吉__悬挂假设左手栏.md` ｜ 方法：— ｜ 原名：— ｜ trigger："会上大家都点头，执行全走样"；"同样事实，两个人结论完全相反"；"沟通卡住，说不清到底卡在哪" ｜ root_cause：hidden-assumptions；unstated-models ｜ surface_domain：团队；复盘；评审；沟通 ｜ confidence：高 ｜ source_fidelity：一手

### pattern: black-box  （1 个方法）

- 卡：`deep_温伯格__黑箱系统边界.md` ｜ 方法：— ｜ 原名：— ｜ trigger："这模块内部看不了，怎么判断它坏了没"；"一改就全崩，边界到底在哪"；"怎么在不懂内部时仍能推断行为" ｜ root_cause：no-boundary；internal-invisible ｜ surface_domain：调试；评测；对手分析；系统分析 ｜ confidence：高 ｜ source_fidelity：一手

### pattern: convexity  （1 个方法）

- 卡：`deep_反脆弱__凸性杠铃.md` ｜ 方法：— ｜ 原名：— ｜ trigger："波动一大我就亏，平稳时也不怎么赚"；"想设计一种越折腾越强的策略"；"怎么用小成本博大上行、又不怕黑天鹅" ｜ root_cause：risk-asymmetry；fragility-to-volatility ｜ surface_domain：投资；研发；个人成长；组织 ｜ confidence：高 ｜ source_fidelity：一手

### pattern: dual-process  （1 个方法）

- 卡：`deep_思考快与慢__双系统.md` ｜ 方法：— ｜ 原名：— ｜ trigger："我凭直觉拍板了，事后看错了"；"第一反应很强烈，但说不清为什么"；"面对复杂判断，怎么避免被直觉带偏" ｜ root_cause：system1-override；low-effort-default ｜ surface_domain：判断；谈判；风险；日常 ｜ confidence：高 ｜ source_fidelity：一手

### pattern: extreme-tail  （1 个方法）

- 卡：`deep_黑天鹅__极端斯坦未然历史.md` ｜ 方法：— ｜ 原名：— ｜ trigger："历史很平稳，能照这个预测未来吗"；"小概率事件会不会把我整个干掉"；"复盘时总觉得'本来就该发生'" ｜ root_cause：thin-tails；silent-evidence；hindsight-bias ｜ surface_domain：风险；预测；安全；投资 ｜ confidence：高 ｜ source_fidelity：一手

### pattern: feedback-regulation  （1 个方法）

- 卡：`deep_维纳__负反馈稳态.md` ｜ 方法：— ｜ 原名：— ｜ trigger："系统一跑就飘，指标慢慢失真"；"怎么让服务/习惯长期稳定在目标附近"；"为什么加了'自动调节'反而振荡" ｜ root_cause：no-closing-loop；drift-without-correction ｜ surface_domain：控制；运维；习惯；算法；管理 ｜ confidence：高 ｜ source_fidelity：一手

### pattern: loss-aversion  （1 个方法）

- 卡：`deep_思考快与慢__前景损失厌恶.md` ｜ 方法：— ｜ 原名：— ｜ trigger："亏一点就死扛，赚一点就跑"；"同样数额，丢钱比得钱疼得多"；"为什么大家对损失比收益敏感" ｜ root_cause：asymmetric-valence；risk-attitude-reversal ｜ surface_domain：投资；谈判；行为；产品 ｜ confidence：高 ｜ source_fidelity：一手

### pattern: 价值权衡  （1 个方法）

- 卡：`harbor_韦伯社会科学方法论.md` ｜ 方法：价值关联与价值分析——用价值选出对象，用价值无涉守住结论 ｜ 原名：价值关联与价值分析 ｜ trigger：研究对象选不定、"这个结论客观吗"被反复质疑，或研讨中事实陈述与价值评判纠缠不清 ｜ root_cause：未把"选题由价值关联决定"与"结论须价值无涉"分开，把价值判断混进了经验认识 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

### pattern: 信息设计  （7 个方法）

- 卡：`harbor_社会性动物.md` ｜ 方法：首因效应与稀释效应——安排和散发信息的方式决定别人怎样解释它 ｜ 原名：呈现顺序决定判断 ｜ trigger：同样的内容换个顺序讲、换个参照物摆，听者的结论就完全变了 ｜ root_cause：判断都是相关的，我们如何解释后续信息取决于先到信息与背景参照 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_粘住.md` ｜ 方法：找出核心问题——一次只说一件事，并把它压成一句谚语 ｜ 原名：找出核心问题 ｜ trigger：要传达的东西太多，听众听完什么也没记住；或者自己因为选择过多而迟迟定不下来 ｜ root_cause：同时说三件事等于什么都没说，复杂性本身会诱发决策的麻痹 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_粘住.md` ｜ 方法：先破坏别人的推测机器，再把它修好——指出他们知识中的缺口 ｜ 原名：知识的缺口 ｜ trigger：你要讲的东西很重要，但听众根本不觉得跟自己有关，注意力起不来 ｜ root_cause：人对自以为已经知道的东西不再投入注意力，好奇心只来自知识的缺口 ｜ surface_domain：沟通说服 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_粘住.md` ｜ 方法：可验证的凭据——把可信度交给受众，让他自己试出结果 ｜ 原名：可验证的凭据 ｜ trigger：你说得头头是道、数据也齐全，对方却就是不买账、不行动 ｜ root_cause：外部权威与内部数据都不构成对方的亲身体验，可信度没有交到受众手里 ｜ surface_domain：偏误解毒 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_粘住——为什么我们记住了这些，忘掉了那些 (扫描版).md` ｜ 方法：打破推测机器——先破坏，再修好 ｜ 原名：打破推测机器 ｜ trigger：你要传达的信息正确且重要，但听众凭既有经验就能预测你下一句，注意力当场流失 ｜ root_cause：大脑天生对变化敏感，平淡无奇的信息根本进不了注意 ｜ surface_domain：沟通说服 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_粘住——为什么我们记住了这些，忘掉了那些 (扫描版).md` ｜ 方法：知识缺口而非知识深渊——先填背景，再指出缺口 ｜ 原名：知识缺口与知识深渊 ｜ trigger：想让对方对一个主题产生兴趣，却发现他连基础背景都没有，提问和悬念都激不起好奇心 ｜ root_cause：缺口会引发执着的痛苦，深渊只会让人放弃 ｜ surface_domain：沟通说服 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_粘住——为什么我们记住了这些，忘掉了那些 (扫描版).md` ｜ 方法：找到创意的核心——用指挥官意图剔除多余 ｜ 原名：找到创意的核心 ｜ trigger：材料太多、优先级难分，自己或团队被复杂性麻痹，说不清到底要传达哪一条 ｜ root_cause：无法区分何为"至关重要"、何为"有用" ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

### pattern: 偏误解毒  （10 个方法）

- 卡：`harbor_思考快与慢.md` ｜ 方法：锚定效应——先发锚定与"为对方着想"的解药 ｜ 原名：锚定效应 ｜ trigger：谈判、报价或数值估测时，先进入视野的那个数字悄悄左右了你的判断，事后却坚称自己没受影响 ｜ root_cause：锚定效应是由联想激发引起的，与锚定值是否真实、是否可信一点都不重要 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_思考快与慢.md` ｜ 方法：回归平均值——最保守、最接近平均值的预测才是最准确的 ｜ 原名：回归平均值 ｜ trigger：一次超常的好成绩或坏成绩之后，紧接着出现了"回落"，于是急于为这次回落找一个因果解释 ｜ root_cause：只要两个数值之间的相关度不高，就会出现回归平均值的情况 ｜ surface_domain：偏误解毒 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_思考快与慢.md` ｜ 方法：框架效应——在获得时偏向确定的事，在损失时偏向赌一把 ｜ 原名：框架效应 ｜ trigger：同一个方案换个说法，人们的偏好就整体翻转，而你以为大家在做同一个决定 ｜ root_cause：不同的框架会触发不同的心理账户，且损失的严重性如何要看其指向的账户 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_无从选择.md` ｜ 方法：尽取者与满足者——只寻求"够好"而不必执意"最好" ｜ 原名：尽取者与满足者 ｜ trigger：选项越多越挑不动，选完还在反复后悔，明明已经买到不错的东西却高兴不起来 ｜ root_cause：尽取者要的是最好的，而确定"最好"必须比较完所有选项，这个成本被忽略了 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_无从选择.md` ｜ 方法：高峰与结尾——改变收尾就能改变整段体验的记忆 ｜ 原名：高峰与结尾决定记忆效用 ｜ trigger：一段体验过程其实差不多，不同的人事后评价却相差很大；或者明明整体不错，回忆起来只记得糟糕 ｜ root_cause：对过往体验的愉快记忆几乎完全取决于高峰时的感觉和结束时的感觉，与时长和总量关系不大 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_无从选择.md` ｜ 方法：损失厌恶与框架效应——中心点的位置决定你算作获利还是损失 ｜ 原名：损失厌恶与中心点 ｜ trigger：同一笔钱、同一个条件，换个说法就让人做出相反选择，而你自己也拿不准到底哪个更划算 ｜ root_cause：不同的框架会触发不同的心理账户，中心点的位置决定这笔交易被算作获利还是损失 ｜ surface_domain：偏误解毒 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_清醒思考的艺术.md` ｜ 方法：干掉你最心爱的理论——与确认偏误作斗争 ｜ 原名：确认偏误 ｜ trigger：新信息进来后，你总觉得它恰好印证了你原来的判断 ｜ root_cause：确认偏误是所有思维错误之父——它倾向于这样诠释新信息，让它们与我们现有的理论、世界观和信念相兼容 ｜ surface_domain：偏误解毒 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_清醒思考的艺术.md` ｜ 方法：拆解故事——望着里程碑，而不是望着天空 ｜ 原名：故事偏误 ｜ trigger：一个解释听起来特别顺、特别有说服力，重要细节恰好都被串起来了 ｜ root_cause：故事偏误是指：用故事扭曲和简化现实，它们排斥不合适编进故事的一切 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_清醒思考的艺术.md` ｜ 方法：行动偏误与不作为偏误——不明情形下的两头陷阱 ｜ 原名：行动偏误 ｜ trigger：情况不明、拿不准，却有一种必须做点什么的冲动 ｜ root_cause：我们全都是这些迅速反应者的后代，他们宁可不必要地多逃跑一次 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_社会性动物.md` ｜ 方法：决策后不协调——把思想调整到与行动相一致 ｜ 原名：决策后不协调 ｜ trigger：已经投入一大笔资源或作出了公开承诺，此后所有新信息都被自动解读成"我们当初是对的" ｜ root_cause：思想与行动不符时，人会把思想调整到与行动一致，以消除不协调 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

### pattern: 反思与自律  （6 个方法）

- 卡：`harbor_圣吉第五项修炼.md` ｜ 方法：悬挂假设——把自己的假设挂在面前接受询问与观察 ｜ 原名：悬挂假设 ｜ trigger：一场会议里各说各话、谁也说服不了谁，散会后才发现双方争的压根不是同一件事 ｜ root_cause：各自的假设都藏在心里没有摆到桌面上，因而从未被询问与观察 ｜ surface_domain：沟通说服 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_少有人走的路.md` ｜ 方法：自律四原则——推迟满足感、承担责任、尊重事实、保持平衡 ｜ 原名：自律 ｜ trigger：问题一堆、痛苦绕不开，想找个不痛的办法绕过去 ｜ root_cause：规避问题和逃避痛苦的趋向，是人类心理疾病的根源 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_少有人走的路.md` ｜ 方法：批评他人之前，先进行自我反省 ｜ 原名：自我反省 ｜ trigger：想指出别人的问题、说服对方改变，或刚与人起了冲突 ｜ root_cause：冲突的实质是告诉对方"你是错的，我是对的" ｜ surface_domain：沟通说服 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_少有人走的路.md` ｜ 方法：真正的爱——促进心智成熟的自我完善意愿，靠实际行动证明 ｜ 原名：自我完善 ｜ trigger：分不清"心动、上头"与真正的爱，或一段关系里只有感觉没有行动 ｜ root_cause：把精神贯注当成了爱 ｜ surface_domain：偏误解毒 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_笛卡尔谈谈方法.md` ｜ 方法：临时行为规范——在判断上犹疑时，如何做到在行动上不犹疑 ｜ 原名：临时行为规范 ｜ trigger：理性告诉你说证据还不够、判断该悬着，但事情不能等着，必须现在就动 ｜ root_cause：判断的犹疑不该传导成行动的瘫痪，行动需要一套暂行的、可替换的规则 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_笛卡尔：第一哲学沉思集.md` ｜ 方法：在领会得清楚、分明之前不下判断——让同意的强度对齐领会的强度 ｜ 原名：清楚、分明地领会之前不下判断 ｜ trigger：一个必须表态的问题摆在面前，心里其实只有模糊印象，却已经被催着给结论 ｜ root_cause：错误不是外来的，而是人在理智尚未给出清楚、明白的认识时就动用了下判断的自由 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

### pattern: 因果推断  （9 个方法）

- 卡：`harbor_休谟人类理解研究.md` ｜ 方法：恒常会合与习惯——因果推断只建立在经验的会合上 ｜ 原名：恒常会合 ｜ trigger：需要断言 A 就是 B 的原因，却发现除了"两者总是一起出现"，拿不出任何可说明的联系机制 ｜ root_cause：物象之间没有可以发现出的联系，因果推断只建立在经验的恒常会合上 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_休谟人类理解研究.md` ｜ 方法：使信念和证据适成比例——平衡相反的实验 ｜ 原名：信念与证据适成比例 ｜ trigger：面对一份证人证言或一份异常报告，要么全盘接受、要么一口回绝，拿不准该信到几分 ｜ root_cause：证言的明验会跟着事实反常的程度按比例减低其力量 ｜ surface_domain：偏误解毒 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_休谟人类理解研究.md` ｜ 方法：观念的关系与实际的事情——先给命题分类，再决定要什么等级的证据 ｜ 原名：观念的关系与实际的事情 ｜ trigger：一个命题吵了很久没有结论，双方却在一方要求"严格证明"、另一方只肯给"经验归纳"上互相指责 ｜ root_cause：两类对象被混为一谈——观念的关系凭直觉或解证确定，实际的事情只能由经验得到或然性 ｜ surface_domain：研究设计 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_对伪心理学说不.md` ｜ 方法：警惕虚假相关——第三变量与选择性偏差 ｜ 原名：相关并不意味着因果关系 ｜ trigger：看到两个变量一起变动，就想据此动手干预 ｜ root_cause：第三变量与选择性偏差制造虚假相关 ｜ surface_domain：偏误解毒 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_戴蒙德枪炮病菌与钢铁.md` ｜ 方法：自然实验——用自然形成的对照替代无法实施的干预 ｜ 原名：自然实验 ｜ trigger：想验证一个关于长期、大尺度现象的因果判断，却既不能做实验也找不到足够样本 ｜ root_cause：历史系统的变数极多且互相反馈，事前预测困难，只能靠自然实验做事后解释 ｜ surface_domain：研究设计 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_戴蒙德枪炮病菌与钢铁.md` ｜ 方法：是独立发明还是思想传播——用"非同一般的巧合"做归因检验 ｜ 原名：思想传播还是独立发明 ｜ trigger：多个地方几乎同时出现了同一个新事物，需要判断它究竟是各自独立发明的，还是从一个源头传播开的 ｜ root_cause：差异来自民族环境的差异，而不是民族自身在生物学上的差异；同时许多看似独立发明的成果实为思想传播 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_统计数字会撒谎.md` ｜ 方法：相关关系的四种替代解释——先排除，再谈因果 ｜ 原名：相关不等于因果 ｜ trigger：有人用一条"A 上升、B 也上升"的曲线，推出"做了 A 就能得到 B" ｜ root_cause：相关可能来自第三因素、偶然、因果倒置，或根本超出了数据范围 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_韦伯社会学基本概念.md` ｜ 方法：动机——意义妥当与因果妥当双重校验，再以结果控制 ｜ 原名：意义妥当与因果妥当 ｜ trigger：一个关于动机的解释听起来很通顺，却既拿不出经验规则的佐证，也没有结果来验证 ｜ root_cause：把主观上妥当的意义关联直接当成了因果上妥当的诠释 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_韦伯社会科学方法论.md` ｜ 方法：因果归源——只取无限实在中具有文化意义的有限部分 ｜ 原名：因果归源 ｜ trigger：一个案例的原因越列越长、越追溯越接近无限，研究陷在"详尽无遗"里出不来 ｜ root_cause：试图从整个实在出发做详尽无遗的因果追溯，而实在本身并没有指明该选哪一部分的现成标志 ｜ surface_domain：偏误解毒 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

### pattern: 学习与通讯  （3 个方法）

- 卡：`harbor_戴蒙德枪炮病菌与钢铁.md` ｜ 方法：影响接受新技术的四个考虑——相对经济利益、社会价值和声望、既得利益、优点的可见性 ｜ 原名：影响接受新技术的因素 ｜ trigger：一项明显更好的技术、工具或做法推不动，用户就是不换 ｜ root_cause：是否被接受取决于相对经济利益、社会价值和声望、既得利益、优点是否容易看到这四项，而不取决于技术本身有多先进 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_维纳：人有人的用处.md` ｜ 方法：学习——用过去演绩改变操作的一般方法 ｜ 原名：学习 ｜ trigger：系统或人反复犯同一类错，却只在单次动作上打补丁，从不修改做事的一般方法 ｜ root_cause：演绩信息送回后只用于调节特定动作，没有用来改变操作的一般方法和演绩的模式 ｜ surface_domain：研究设计 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_维纳：人有人的用处.md` ｜ 方法：通讯——讲者和听者联合起来反对混乱的博奕 ｜ 原名：通讯 ｜ trigger：消息越传越失真、组织里充斥没有信息量的通报，或系统看似在运转实则在滑向混乱 ｜ root_cause：把通讯量当成了通讯价值，而通讯本是讲者和听者联合起来对抗混乱的博弈 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

### pattern: 概念建模  （8 个方法）

- 卡：`harbor_学会提问.md` ｜ 方法：用"如果……"句得出多个结论，远离二元思维 ｜ 原名：如果……句 ｜ trigger：一场讨论逼你在"是/否"、"干/不干"之间二选一 ｜ root_cause：二元思维把一组理由只能导向一个结论 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_波普尔历史决定论的贫困.md` ｜ 方法：方法论唯名主义——描述事物如何活动，而非追问它真正是什么 ｜ 原名：方法论唯名主义 ｜ trigger：讨论卡在"这个词到底是什么意思"、或争论某事物的"真正本质"是什么 ｜ root_cause：方法论本质主义要求把本质和现象区别开来，要求获得本质的知识 ｜ surface_domain：研究设计 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_笛卡尔谈谈方法.md` ｜ 方法：普遍怀疑与分解——怀疑到底，再把对象分成尽可能小的部分 ｜ 原名：普遍怀疑 ｜ trigger：面对一个众说纷纭的问题，满脑子是先入之见，却分不清哪些是事实哪些是偏见 ｜ root_cause：成长期在充分运用理性之前形成的判断留下了先入的偏见，阻碍认识真理 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_笛卡尔谈谈方法.md` ｜ 方法：从最简单、最一般的问题开始——让发现的每一个真理成为发现其他真理的规则 ｜ 原名：从最简单、最一般的问题开始 ｜ trigger：面对一个陌生领域或一堆杂乱材料，不知道先啃哪一块才能越做越顺 ｜ root_cause：真理不是平列的堆积，而是有主有从的有机体系，必须先找到能当统帅的核心 ｜ surface_domain：研究设计 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_笛卡尔：第一哲学沉思集.md` ｜ 方法：分析法——展示发现的过程，而不只是给出证明 ｜ 原名：分析法 ｜ trigger：你拿出了严丝合缝的论证，读者却说"看懂了、但不信，也学不会" ｜ root_cause：综合法只证明结论，不告诉读者结论是怎样被发现的，而困难恰恰在清楚分明地领会第一概念 ｜ surface_domain：研究设计 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_笛卡尔：第一哲学沉思集.md` ｜ 方法：先给反驳分类——查它建筑在误解了的词句上，还是错误的假定上 ｜ 原名：误解了的词句或错误的假定 ｜ trigger：一堆反对意见涌来，看着条条有理，却越辩越乱、越澄清越糊 ｜ root_cause：反驳多半不指向论证本身，而是建筑在误解了的词句或者错误的假定上 ｜ surface_domain：偏误解毒 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_韦伯社会学基本概念.md` ｜ 方法：理念型——愈尖锐而明确便愈远离真实世界，也愈能善尽其责 ｜ 原名：理念型 ｜ trigger：面对杂多的现实无从下手，或者手里有一堆"平均类型"却解释不了任何一个具体行动 ｜ root_cause：缺少一个尽可能展现完备之意义妥当性的概念单位，作为衡量现实与设想解释的准绳 ｜ surface_domain：研究设计 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_韦伯社会科学方法论.md` ｜ 方法：理想类型——纯粹理想的界限概念，用来衡量和比较实在 ｜ 原名：理想类型 ｜ trigger：建出来的概念被当成历史实在本身，或者理论与历史被相互换用乃至完全混起来 ｜ root_cause：把作为衡量手段的纯粹理想界限概念误当作规律、当作实在应该被分门别类放进去的图式 ｜ surface_domain：研究设计 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

### pattern: 渐进试错  （3 个方法）

- 卡：`harbor_反脆弱.md` ｜ 方法：置于"喜欢错误"的位置——乐于犯众多的小错，承受小的伤害 ｜ 原名：喜欢错误 ｜ trigger：一处组织或流程长期追求零差错，一切平稳，直到某天出一次谁都没想到的大事故 ｜ root_cause：错误被压制而非分散，一旦发生就极其严重且不可逆 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_波普尔历史决定论的贫困.md` ｜ 方法：渐进的修补与批判性分析——渐进工程取代乌托邦工程 ｜ 原名：渐进的修补 ｜ trigger：面对复杂社会或组织问题，想一次性拿出整体改造的蓝图并按图施工 ｜ root_cause：乌托邦工程事先就一口咬定彻底改造是可能的和必然的 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_波普尔猜想与反驳.md` ｜ 方法：试探和清除错误——用试错法替代辩证三段式 ｜ 原名：试探和清除错误 ｜ trigger：观点僵持，想靠"正题—反题—合题"把两边综合掉 ｜ root_cause：辩证法的模糊性——把辩证解释强加于各种发展以及全然不同的事物太容易了 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

### pattern: 理解采纳  （6 个方法）

- 卡：`harbor_乌合之众.md` ｜ 方法：断言、重复和传染——说服群体的三件套 ｜ 原名：断言重复传染 ｜ trigger：需要让群体接受一个主张或人选，却拿不出能被逐条核验的严密论证 ｜ root_cause：群体不受推理影响，只能理解拼凑起来的观念 ｜ surface_domain：沟通说服 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_乌合之众.md` ｜ 方法：用形象而非论证触动群众的想像力 ｜ 原名：形象胜于论证 ｜ trigger：需要让一件事真正进入公众记忆并驱动行动，却发现数据和道理都推不动 ｜ root_cause：群体只受形象支配，不被推理打动 ｜ surface_domain：影响群众 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_乌合之众.md` ｜ 方法：词语和套话——唤醒形象而不诉诸含义 ｜ 原名：词语套话的威力 ｜ trigger：需要用语言撬动群体情绪，却发现讲道理完全无效 ｜ root_cause：词语的威力来自它唤醒的形象，与它的真实含义无关 ｜ surface_domain：沟通说服 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_引爆点.md` ｜ 方法：个别人物法则——联系员、内行和推销员 ｜ 原名：个别人物法则 ｜ trigger：想让一个观念、产品或行为方式流行起来，却发现按人群平均发力迟迟不见起色 ｜ root_cause：流行的兴起系于关键的少数人身上，而不是均匀分布在大多数人身上 ｜ surface_domain：沟通说服 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_引爆点.md` ｜ 方法：附着力因素法则——稍稍改变一下呈现的形式就能改变一切 ｜ 原名：附着力因素 ｜ trigger：信息、产品或口号已经铺出去了，人们看过就忘，留不下任何印象 ｜ root_cause：流行物本身缺少能让人过目不忘的附着力 ｜ surface_domain：沟通说服 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_社会性动物.md` ｜ 方法：接种预防效应——先接触一个能马上反驳的简短攻击以获得免疫力 ｜ 原名：接种预防效应 ｜ trigger：想让一个人或一群人抵抗即将到来的说服、洗脑或同伴压力，却发现提前讲道理没用 ｜ root_cause：抵抗力来自自己动手反驳的练习，而不是来自别人替他堆好的论证 ｜ surface_domain：偏误解毒 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

### pattern: 系统观  （4 个方法）

- 卡：`harbor_圣吉第五项修炼.md` ｜ 方法：高杠杆解——以一个小小的改变，去引起持续而重大的改善 ｜ 原名：高杠杆解 ｜ trigger：问题反复出现，每次都在最明显的地方用力，短期见效、长期更糟 ｜ root_cause：抓住的是症状解而非高杠杆解，而症状解反应愈来愈快、根本解反应愈来愈慢 ｜ surface_domain：系统观 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_圣吉第五项修炼.md` ｜ 方法：看动环，而非线段——真实世界是由许多因果环组成的 ｜ 原名：看动环而非线段 ｜ trigger：一出事就先找责任人，换了人问题照旧，甚至更严重 ｜ root_cause：只看到线段式的因果关系，看不见真实世界由许多因果环组成 ｜ surface_domain：系统观 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_引爆点.md` ｜ 方法：环境威力法则——人对自己周围环境的敏感程度比他们所表现出来的更为强烈 ｜ 原名：环境威力法则 ｜ trigger：内容没变、人没变，换个场合效果却天差地别；或者明明问题摆在眼前，在场的人却都无动于衷 ｜ root_cause：人对自己周围环境的敏感程度比他们所表现出来的更为强烈 ｜ surface_domain：系统观 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_维纳：人有人的用处.md` ｜ 方法：反馈——以实际演绩而非预期演绩为依据的控制 ｜ 原名：反馈 ｜ trigger：系统或行动一直在跑偏却迟迟纠不回来，因为你始终在按预期方案而非实际表现做调整 ｜ root_cause：控制依据的是预期演绩而非实际演绩，缺少把偏差送回输入端的回路 ｜ surface_domain：系统观 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

### pattern: 规则与结构  （1 个方法）

- 卡：`harbor_韦伯社会学基本概念.md` ｜ 方法：社会行动——以"有意义地指向他人"为判准 ｜ 原名：社会行动 ｜ trigger：把一群人同时做出的相同举动当成了"社会现象"，据此给出的解释全盘落空 ｜ root_cause：未检验行动者是否主观上有意义地把自己的行动指向他人，把单纯的相似反应误判为社会行动 ｜ surface_domain：偏误解毒 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

### pattern: 证伪检验  （9 个方法）

- 卡：`harbor_学会提问.md` ｜ 方法：找出描述性假设——填补缺失的空白来重构推理 ｜ 原名：描述性假设 ｜ trigger：一套论证的理由看着都成立，结论却让你隐隐觉得不对劲 ｜ root_cause：从理由到结论之间缺了一环，而这一环没有被清楚陈述 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_对伪心理学说不.md` ｜ 方法：可证伪性——理论必须指出哪些事情不会发生 ｜ 原名：可证伪性 ｜ trigger：遇到一套怎么解释都通、永远正确的说法 ｜ root_cause：理论只说会发生什么，不说不会发生什么 ｜ surface_domain：研究设计 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_波普尔历史决定论的贫困.md` ｜ 方法：淘汰假理论——凡检验都解释为证伪而非证实 ｜ 原名：淘汰假理论 ｜ trigger：做检验、评审或复盘时，默认在找支持自己方案的证据 ｜ root_cause：缺乏批判的态度时，我们总会寻求和找寻证实，忽视那些危及心爱理论的情况 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_波普尔猜想与反驳.md` ｜ 方法：可反驳性划界——一切真正的检验都是有意的反驳 ｜ 原名：可反驳性 ｜ trigger：要判断一个说法、模型或理论值不值得认真对待，而它听起来怎么都说得通 ｜ root_cause：用"可证实性"作划界标准，反而放进了伪科学、排除了最重要的科学陈述 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_波普尔猜想与反驳.md` ｜ 方法：猜想和反驳两大环节——简单性、可独立检验性与新预言 ｜ 原名：猜想和反驳 ｜ trigger：要提出或挑选一个新理论、新方案、新假说，却只顾着让它自洽 ｜ root_cause：科学发现包含猜想和反驳两大环节，只做前一半会停滞、只做后一半会枯竭 ｜ surface_domain：研究设计 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_波普尔科学发现的逻辑.html.md` ｜ 方法：反约定主义的对抗手段——拆掉特设性假说的免疫策略 ｜ 原名：反约定主义的对抗手段 ｜ trigger：一个说法被推翻之后，靠补一条"这只是特殊情况"又活了过来 ｜ root_cause：特设性地引入辅助假说，对一个定义特设性地加以修改 ｜ surface_domain：偏误解毒 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_波普尔科学发现的逻辑.html.md` ｜ 方法：验证度由检验的严格程度决定，不由验证实例的数目决定 ｜ 原名：验证度 ｜ trigger：用"我有很多案例支持"来给一个说法加分 ｜ root_cause：把验证度等同于验证事例的数目，而不是检验的严格程度 ｜ surface_domain：研究设计 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_波普尔科学发现的逻辑.html.md` ｜ 方法：先划出潜在证伪者类——理论只对自己的禁令负责 ｜ 原名：潜在证伪者类 ｜ trigger：说出一个判断或目标之后，说不清"出现什么情况就算它失败" ｜ root_cause：不满足可证伪性条件的陈述，不能在所有可能的经验的基础陈述的总体中区分任何两个陈述 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_黑天鹅.md` ｜ 方法：证伪——通过负面例子而不是正面证据接近真相 ｜ 原名：证伪 ｜ trigger：手上已经攒了一大批支持自己判断的案例，正准备据此下结论或下注 ｜ root_cause：无知经验主义——天生习惯于寻找能够证明我们的理论的例子，这些例子总是很容易找到 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

### pattern: 证据评估  （4 个方法）

- 卡：`harbor_学会提问.md` ｜ 方法：对事实性声明先问"我为什么要相信它" ｜ 原名：我为什么要相信它 ｜ trigger：遇到一项斩钉截铁的事实性声明，或被要求据此下判断 ｜ root_cause：需要证据却没给证据的声明，仅仅是一个断言 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_对伪心理学说不.md` ｜ 方法：聚合性证据原则——把结论建立在大量有些许差异的实验之上 ｜ 原名：聚合性证据原则 ｜ trigger：一批研究结论互相打架，或整个结论被某个单一研究的缺陷一票否决 ｜ root_cause：科学上没有哪个实验被设计得完美无缺，结论不靠单一决定性证明 ｜ surface_domain：研究设计 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_统计数字会撒谎.md` ｜ 方法：内在有偏的样本——结论不会好于样本本身 ｜ 原名：内在有偏的样本 ｜ trigger：看到一份"调查显示"的结论，需要判断它到底能不能信 ｜ root_cause：结论不会好于样本本身，有偏样本几乎能产生任何人需要的任何结果 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_统计数字会撒谎.md` ｜ 方法：没有透露的数据——追问全距与偏离水平 ｜ 原名：没有透露的数据 ｜ trigger：一个结论只给你一个平均数，不给你范围和偏离 ｜ root_cause：平均数过于简单而无用，而没说出口的数据人们根本不会察觉它缺席 ｜ surface_domain：批判思维 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

### pattern: 风险与不确定性  （4 个方法）

- 卡：`harbor_反脆弱.md` ｜ 方法：凸性效应——从波动中赚到的比你失去的多 ｜ 原名：凸性效应 ｜ trigger：用平均值做决策时一切正常，一遇到波动就亏损，而波动在平均值里根本看不见 ｜ root_cause：反应是非线性的，平均数的概念对在变化面前脆弱的事物没有意义 ｜ surface_domain：系统观 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_反脆弱.md` ｜ 方法：在游戏中投注——谁提意见，谁下注 ｜ 原名：在游戏中投注 ｜ trigger：有人给出预测、建议或评级，话说得很满，判断错了却完全不用付出任何代价 ｜ root_cause：提意见的人未在游戏里投注，风险被转嫁给了依赖其信息的人 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_黑天鹅.md` ｜ 方法：平均斯坦与极端斯坦——别把钟形曲线用在极端斯坦 ｜ 原名：平均斯坦与极端斯坦 ｜ trigger：要用标准差、相关性、R平方、夏普比率这类指标去描述一个可能出现极端值的领域 ｜ root_cause：传统的高斯方法只关注平均水平，把意外当做附属问题；将钟形曲线用在一切地方的严重错误 ｜ surface_domain：偏误解毒 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯
- 卡：`harbor_黑天鹅.md` ｜ 方法：杠铃策略——极度保守加极度冒险，不碰中等风险 ｜ 原名：杠铃策略 ｜ trigger：无法预测、也无法计算极端事件的概率，却又必须对未来下注 ｜ root_cause：在可能性不可计算时，你只需要减轻事件的影响 ｜ surface_domain：决策卡点 ｜ confidence：板上钉钉 ｜ source_fidelity：一手·原文可溯

## 二、无路由头的卡（未入聚类，待补 v2 路由头）

- harbor_影响力.md


## 三、统计

- 卡：33 张（深卡 7 ＋ 方法卡 26）

- 方法块：82 个 ｜ pattern 聚类：21 个 ｜ 无路由头：1 张
