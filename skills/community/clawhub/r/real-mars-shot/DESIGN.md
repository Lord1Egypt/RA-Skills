# 火种计划设计 / Real Mars Shot design

叙述由智能体完成，判定由 `scripts/rms` 完成。玩家看到的每一笔钱、每一毫希沃特、每一次窗口，都来自脚本读到的 `data/science.json`。本文解释这些规则为什么这样写。数字的出处在 `REFERENCES.md`。

The agent narrates. `scripts/rms` decides. Every dollar, millisievert, and launch window the player is told comes from `data/science.json` as the scripts read it. This document is why the rules are shaped this way. Citations live in `REFERENCES.md`.

## 1. 命题 / Premises

地球文明若只住在地球上，就会随地球一起结束。计划的目标不是插旗，而是在另一个世界上留下一颗火种：能够不靠地球补给，自己开始下一轮文明。标题里的 “real mars shot” 是那条被质疑的捷径，不是默认打法。

人极脆弱，依赖水、电、空气、营养、温度、压力和辐射屏蔽。地衣、苔藓、缓步动物、极端细菌、蓝细菌和可食用作物都比人容易送到远处，但「暴露后还活着」不等于「在那里建立了」。缓步动物的暴露试验会留下旗标，永远不算建立。机器比人更能先抵达，也比人更能在没有闭环生态时工作；纯机器定居不能赢。碳基生命要水、能量和屏蔽才能生长。机器要能量、备件和还能从地球发出去的质量。

顺序从易到难：地球上的模拟（冷、热、真空、低氧、封闭舱）→ 机器 → 月球 → 微生物和植物 → 人 → 火星及更远。走错顺序会失败，失败的方式分成「不可能」和「鲁莽」。不可能不改存档。鲁莽必须玩家确认后才掷骰。

每一回合都过预算、运力、消耗品、乘员剂量与心理、能量、原位资源、转移窗口和通信延迟，也过政治：虚构派系、舆论、预算削减、内部异议、安静的破坏。骰子是确定性的 d100，由种子、回合和盐的 SHA-256 决定。

A civilization that lives only on Earth ends when Earth does. The goal is not a flag. It is an ember on another world that can start the next round without Earth. The title names the shortcut the game refuses to take blindly.

Humans need water, power, air, food, temperature, pressure, and shielding. Lichens, mosses, tardigrades, extremophile bacteria, cyanobacteria, and food crops are easier to send, and survival of an exposure is not establishment. A tardigrade test sets a flag and never counts. Machines arrive sooner and work without a closed ecology. A machine-only settlement cannot win.

The honest order is Earth analogs, then machines, then the Moon, then microbes and plants, then humans, then Mars. Wrong order is either impossible (no mutation) or reckless (no mutation until the player confirms).

## 2. 谁在算数 / Who owns the numbers

| 层 | 职责 |
| --- | --- |
| `SKILL.md` | 智能体怎么把人话收成一个动作，怎么叙述，什么不能编 |
| `scripts/*.py` | 命令行。存档、回合、计算、图、可选 TTS |
| `scripts/rms/` | 火箭方程、剂量、消耗、窗口、任务分级、事件、火种清单 |
| `data/*.json` | 科学叶子、科技树、派系、顾问、生物、事件 |
| 存档 | `$REALMARSSHOT_SAVE_DIR` 或 `~/.realmarsshot/saves/user-<id>.json` |

科学叶子的形状是 `{value, estimate, source_id}`。`estimate: true` 在叙述里必须叫估计。`game_calibration` 是本游戏的设计规则，不是测量。

## 3. 开局世界 / Starting world

时钟从 2026 年 1 月起。默认语言中文。难度 `realistic`：国库 1.5（十亿美元），年预算 6.0，舆论 50，政治资本 55，地球稳定 82，异议 12，安全文化 62，36 名虚构乘员，剂量为 0。运力是每年 8 次中型 × 18 吨近地轨道，加 2 次重型 × 45 吨，合计约 234 吨/年。`hard`：年预算 4，稳定和舆论更低，闭天会敌意 +15，重型箭略差，可靠性略低。

若把这支舰队未来十年全部拿去飞化学推进、六人、合式的火星战役，地球大约能送出 **10 人**。约束是质量与窗口，不是训练管线（管线在同样假设下大约还能培养上百人）。这是估计，而且是「什么别的都不发射」的上限。开场白必须把这个数字说出来。

顾问八人，全部虚构：林桥（封闭生态）、阿德瓦莱·奥孔克沃（乘员安全）、叶莲娜·瓦尔加（辐射）、佐藤芽（原位资源）、拉斐尔·伊克巴尔（推进）、索伦·黑尔（档案）、努尔·哈提卜（外交）、沈寂（系统工程）。约 45% 的种子会在秘密字段里指定一名内应。公开读档和回合结果都剥掉 `secrets`。仓库里的 `examples/save-example.json` 把内应写成 null，避免剧透种子 7。

## 4. 阶段与门 / Phases and gates

阶段不是菜单锁。它是「下一条还没通过的诚实步骤」，用来生成建议。玩家仍可尝试更后面的任务。

| 顺序 | 阶段 id | 通过条件 |
| --- | --- | --- |
| 1 | `earth_analog` | 封闭舱记录 ≥30 天；然后 ≥365 天且演示水回收 ≥0.93 |
| 2 | `machines` | 月球至少一次成功着陆 |
| 3 | `moon` | 月球水或氧的 ISRU 年产量 > 0 |
| 4 | `biology` | 模拟星壤试验 ≥90 天 |
| 5 | `cislunar_crew` | 至少一次月球乘员返回 |
| 6 | `mars_cargo` | 火星货运着陆且机器人熬过一个尘季；并且火星制氧试点 ≥ 数据文件里的年产量门槛 |
| 7 | `mars_outpost` | 至少一次火星乘员往返。先留驻、没有往返，是鲁莽 |
| 8 | `independence` | 某处连续 60 个本地盈余月，但十条火种尚未齐 |
| 9 | `ember` | `outcome == win` |

另外三条门不改阶段名，但会改任务判定：水回收演示到 0.98 且持续 ≥180 天；火星机器人着陆；地球上的基因组档案达到门槛。

科技树二十二项，写在 `data/tech_tree.json`。主干是：真空热循环与模拟规程 → 水循环 93% 然后 98% → 萨巴蒂尔与植物舱 → 模拟星壤 → 发射逃逸与精确机器人 → 月球 ISRU、粒子风暴掩体、千瓦裂变、覆土 → 重型火星进入减速着陆与 MOXIE 放大 → 工业级推进剂、核热上面级 → 地外产科、种质库、本地制造 → 可重复超重型与非窗口高能转移。研究骰子 ≤8 时钱和时间已经花掉，科技不解锁。

## 5. 质量、窗口、人 / Mass, windows, people

齐奥尔科夫斯基公式：Δv = Isp · g0 · ln(m0/mf)，g0 = 9.80665 m/s²。

游戏用的规划比冲（估计，除非叶子另有说明）：氢氧约 450 秒，可储存推进剂约 320 秒，核热约 905 秒。核热把战役级初始近地轨道质量乘上 0.62，这是估计。

DRA 5.0 的锚：会合周期约 26 个月（779.94 天）；地火双向通信约 6–44 分钟；核热架构的战役级 IMLEO 约 800–1200 吨；月球从近地轨道到表面再回来合计约 9.5 km/s；火星约 12–14 km/s。窗口中心从 2026-11-15 起，间隔约 780 天，半宽 ±45 天。错过的发射滑到下一扇，不消失。

本游戏的化学六人战役（预置 + 每人化学上面级 + 消耗品）落在 1200 吨以上。参考点：6 人 × 860 天，水回收 0.98，食物开环，氧气走萨巴蒂尔，运上去的生命保障约 15.55 吨，化学战役 IMLEO 约 **1375.6 吨**。同一消耗下核热约 **853 吨**，落进 800–1200 吨。这两个拆分都标了估计，锚是 DRA 5.0，不是一份飞行清单。

货运：月球单向货物 IMLEO 系数约 4–10；火星货物约 5–20，含 1.4 的防热壳和 2.0 的进入减速着陆开销（估计）。遗产级火星着陆质量约 1 吨。更重的火星货物或乘员在没有科技 `heavy_edl` 时是不可能。

生命保障按 BVAD 2022 表 3-31 的量级：氧气 0.895 kg/人·日，二氧化碳 1.085，食物干重 0.80，食物能量 12.778 MJ，饮用水 3.217，废水 0.101+2.946+1.42 = 4.467 kg/人·日。国际空间站食物后勤若含包装更高；游戏用干重加包装系数时会在叶子里标明。水回收 98% 以后，补水相对运上去的食物很小。由二氧化碳回收氧气，当前萨巴蒂尔约 47%（氢受限），目标高于 75%。

辐射：额外屏蔽为 0 时，巡航复现 MSL/RAD 的 1.84 mSv/日（飞船里，不是裸舱外活动），火星表面 0.64 mSv/日（巡视器甲板，近太阳活动高年）。短往返 360×1.84 = 662.4 mSv = 0.662 Sv，落在 Zeitlin 0.66±0.12 Sv 里面。参考合式（180+500+180 天）无额外屏蔽约 **982.4 mSv**，超过游戏里的 600 mSv 规划帽。这顶帽子是估计，不是 NASA-STD-3001 里按年龄和性别计算的 REID。额外屏蔽透射用 `1/(1+extra_g_cm2/50)`，这是估计，不是 HZETRN。+20 g/cm² 的转移掩体和 +200 g/cm² 的表面覆土可以把参考合式压到 600 mSv 以下。栖息地年剂量目标 20 mSv/年是 ICRP 职业照射的类比，同样是估计。

太阳粒子事件在载人火星任务上的出现概率写成 0.10。这是戏剧压缩，不是物理发生率。骰子 100 即使有这个检查也成功；骰子 1 失败，并且可以杀死乘员。

## 6. 定居月账 / Settlement month

`evaluate_month` 看一个世界这个月能不能本地盈余。盈余才把 `independent_months` 加一。库存可以让人活着，时钟不动。地球补给重置试炼时钟。

食物照明是功率的大头（约 0.4 kWe/m²，估计；可食用干重约 0.015 kg/m²·日，估计；每人大约几十平方米）。Kilopower 一级是 +10 kWe，喂不饱农场。`reactor_module` 的 +500 kWe 是估计，并且要本地制造科技。电解氧气大约每千克 8 kWh（估计），比灯小。

水回收在游戏里封顶到已经演示过的 0.98，所以补水不会变成零。本地 ISRU 必须盖住损耗，火种清单才承认水这一条。

断供试炼里，若功率或食物垮掉，人口下降。试炼居民归零时：地球稳定 ≥25 且国库 >0.5，则花 0.4 撤离；否则该地灭绝。灭绝再加上稳定 <25，才是 `offworld_extinction` 的游戏结束。

出生发生在某些正月，要求当地还有人口、食物比例和剂量没垮、乘员心理不太差，并且当月骰子 ≥40。这是游戏规则，不是人口学模型。

## 7. 火种 / The ember

十条都要真，地点是月球、火星或自由空间之一。清单见 `scripts/rms/win.py`。

| id | 门槛 | 性质 |
| --- | --- | --- |
| `independence_months` | 60 | 设计规则：五年本地盈余，不是库存 |
| `water_recovery` | ≥0.98 | ISS 卤水处理器之后的演示水平 |
| `water_isru` | 损耗由本地水覆盖 | 设计规则 |
| `oxygen_margin` | ≥1.2 | 估计 |
| `food` | 本地干食 ≥0.90 | 设计规则 |
| `power` | 最坏情况 ≥1.2 | 估计。月夜或尘暴 |
| `dose` | ≤20 mSv/年 | 估计。ICRP 类比，不是飞行限值 |
| `people` | 100 人 + 10 次地外出生 + 1 万供体，或约 14000 人 | 估计。Smith 2014 的数量级。100 人单独不够 |
| `industry` | 关键备件本地比例 ≥0.8 | 设计规则 |
| `knowledge` | 当地有制造与农业的冗余档案 | 设计规则 |

14000 是 Smith 发表的普查区间的下沿量级，他的情景是世界船，不是火星。游戏把这一点标成估计。档案路径是「小定居点加上种质」，不是假装 100 人已经是一个物种备份。

同一结算先查火种。火种成立则赢，即使地球稳定度在同一次检查里已经是 0。

## 立足与终局 / Footholds and endings

时间分四档立足，两条终局。

立足不结束战役。每一种第一次跨过门槛时写入 `footholds`，放进当回合的 `foothold_victories`，`continues` 为真，`state.outcome` 仍为空。同一种不宣布第二次。宣布时地球必须还活着：稳定度 > 0，计划没有崩溃，也没有无约束释放。

终局才写 `state.outcome = win` 并停表。两条终局：

1. **火种** `ember:<site>`。十条人类文明清单在月球、火星或自由空间之一同时成立。同一检查里若生命之种也成立，记下的是火种。地球稳定度同时为 0 仍然算赢。
2. **生命之种** `seed_of_life:biology:<site>` 或 `seed_of_life:machine:<site>`。地球生命在另一个世界上走到深时。生物路径优先于同一地点的机器照护路径；火星优先于月球和自由空间。地球的计划可以已经结束，但种子必须已经独立（进入过纪元，而且那颗世界上还有东西活着）。一万年是估计，不是新物种的时刻表。

### 人 / Humans

`foothold_500`：至少两人，有栖息地，连续 500 天。500 来自 DRA 5.0 的合式停留（约 500–540 天，一个算例是 539），游戏取 500，标成估计。账本一个月 30 天，17 个月是 510 天。每个这样的月：本地干食 ≥25%（估计；火种要 90%），本地氧气 ≥50%（估计，卡在已演示的约 47% 萨巴蒂尔回收之上），本地水至少盖住一半损耗（估计），库存只补缺口。最坏情况功率 ≥1.0（估计）。年剂量 ≤50 mSv，借用 ICRP 103 的单年管理上限，是估计，不是飞行限值。有人死亡或人数掉到 2 以下，天数归零。地球货运不归零这只钟。只有库存不算。

`foothold_human_century`：大约 100 年，估计，大约四代人如果一代按 25 年粗算。25 不是实测的定居寿命。这一档还要求当地至少 8 人、至少一次地外出生。两个人变老不是下一代。100 年不是火种，也不是新物种。

### 生物 / Biology

不必是人。蓝细菌、极端微生物、地衣、苔藓或作物，在那颗世界上培养等级 ≥2。缓步动物永远不算。生态位是温室，或覆土栖息地（≥50 g/cm²，估计，针对紫外和干渴）。开放的火星地表不行：约 6 mbar、没有稳定液态水、有高氯酸盐、紫外线直接打下来。本地水 ≥100 kg/年（估计）。最坏情况功率 ≥2 kWe（估计）。

`foothold_biology`：这样自持大约 **10 年**。这是「建立」。生物圈二号在大约两年里氧气失控（Severinghaus 等，1994）。十年是设计规则，比那次失败长一个量级，仍然不是物种形成。估计。

`seed_of_life:biology`：同一只生物时钟走到 **10,000 年**。Hendry、Nosil 与 Rieseberg（2007）说明生态物种形成没有单一时钟：有的例子是几百代，许多动物更接近一百万年级。一万年取的是「几千到几万年」的低端，是估计。它不是蓝细菌变成新物种的日程。

不要把它和 Lenski 与 Travisano（1994）的一万代大肠杆菌混在一起。那次实验里细菌一天分裂数次，一万代是几年培养，不是一万年。`ltee_generations` 把这个数单独存着，就是为了分开。

任何成功的地球抵达都会把生物年、照护年和独立标记清零。封闭培养仍是前向污染：扣一笔政治资本（估计）。游戏不写释放步骤。

### 机器 / Machines

机器不需要氧气。它们的生命保障是矿石、能量、散热和维修。

`foothold_machine`：大约 **50 年**自主维持、更新和复制。估计。1980 年 NASA/ASEE 夏季研究（1982 年出版为 NASA CP-2255，Freitas 与 Gilbreath 编）讨论过一座能用当地材料维持并长大的月球工厂。那座工厂没有建成。游戏不提供建造步骤。50 年不是那份报告里的实测寿命。

门槛，全部是估计，除非另注：至少 3 台机器人；本地金属 ≥1 吨/年；可采储矿 ≥100 吨；最坏情况电力 ≥5 kWe（Kilopower 的 1–10 kWe 这一级，不是说 KRUSTY 已经飞过）；散热至少 5 kWt，并且不少于裂变电功率的 4 倍（4 是估计，不是某座反应堆的散热曲线）；每年替换比例 ≥0.10，或不低于 0.08 的年故障比例，也可以改由本地备件比例 ≥0.5 顶上；复制保真度 ≥0.90。0.90 借用的是冯·诺依曼《自复制自动机理论》（1966，Burks 编）里「副本必须够真」的想法，不是测得的误码率，也不是探测器图纸。

没有生命的机器可以赢得这 50 年。它们赢不了火种，也赢不了生命之种。

`seed_of_life:machine`：同一套复制器再照看一条活着的、能繁殖的培养（不是缓步动物），当地有至少 1000 份可重播的微生物或种子档案（估计，不是释放步骤），这样走到 10,000 年。演化的是生物。机器是园丁。

稳定纪元的骰子 ≥96（估计）时，复制品可以好过上一代。这不是 50 年门槛的条件。受压、挫折和崩溃会扣保真度。掉到 0.90 以下，下一次机器纪元会被拒绝。

`replicator_seed` 任务在研究门 `self_replicating_factory` 之后，把一座种子工厂送下去：金属速率、储矿、散热、维修比例和初始保真度。质量按 0.9 吨估计，以便落在已证实的约 1 吨火星着陆量级之内。它不是 NASA 那份研究的施工图。

### 纪元 / Epochs

普通 `wait` 最长 60 个月。深时走 `epoch`：`site` 是 moon、mars 或 freespace，`path` 是 human、biology 或 machine，`scale` 是 decade（10 年）、century（100 年）或 millennium（1000 年）。一步一掷。一千年不能一次叠成一万年。

第一次快进之前，要用普通月份证明它转过一年（12 个月，估计）。生物圈二号没能干净地走完两年，所以游戏不让第一天就跳地质时间。人的纪元还要求 500 天已经在账上，并且眼下仍是多代定居。人不能走千年。生物或机器的千年，要等 10 年或 50 年那一档已经成立。

骰子是 `sha256(seed:turn:salt)` 的 d100，和别的判定一样。盐是 `epoch:<path>:<site>:<scale>`。另一颗骰子 `epoch-earth:...` 决定地球的计划还在不在。

| 点数 | 结果 | 估计 |
| --- | --- | --- |
| ≥70 | 整段年数加上 | 设计规则 |
| ≥40 | 加上一半 | 设计规则 |
| ≥15 | 不加，这一档的纪元年数减半 | 设计规则 |
| 低于 15 | 这一档的纪元年数归零 | 设计规则 |
| ≤5 的崩溃 | 再伤到种子本身：死一个人，或培养等级下降，或少一台机器人 | 设计规则 |

风险只是名字：小行星撞击、太阳粒子、设备熵、突变负荷、生态崩溃、复制漂移、散热故障。游戏不写这些事怎么做。

地球骰子 ≤5 / ≤25 / ≤55 分别对应十年、百年、千年（估计）。命中则地球稳定度归零，计划结束。种子若在这一步开始时已经独立，战役继续，直到生命之种或种子自己死光。种子若还没独立，地球归零仍是 `earth_collapse`。

生物安全的无约束释放仍然直接结束，独立与否不论。试炼人口死光且地球救不了，仍是灭绝。

机器纪元按金属速率消耗储矿。矿不够，这一步只活得了矿还能喂的那些年。一次地球飞船抵达会清掉生物年、机器年、照护年和独立标记。已经宣布过的立足不收回。人的天数和百年不因货运清零；人死了或月份不合格才会清。

版本 1 的存档在读取时迁到版本 2。缺的场地字段补 0。已经宣布过的立足保持已宣布，`just_announced` 清掉，不会再宣布一次。旧的生物或机器立足会把对应的短时钟抬到新的 10 年或 50 年，以免同一条胜利再响一次。不赠送一万年。

Four footholds do not end the campaign. Each is recorded once, while Earth is alive, and play continues. Two endings do end it. The ember (`ember:<site>`) is the ten-item human civilization. If the Seed of Life is also true in that same check, the recorded win is the ember. The Seed of Life (`seed_of_life:biology:<site>` or `seed_of_life:machine:<site>`) is Earth life reaching deep time on another world. On one world the biological path is reported before the machine-tended path. Mars is checked before the Moon and free space. Earth may already have stopped paying for the program. The seed has to be independent: an epoch has started, and something there is still alive. Ten thousand years is an estimate, not a speciation schedule.

Humans: 500 days with a real local share of food, oxygen, and water, dose at or below 50 mSv/year (an ICRP single-year analogy, an estimate), then about 100 years once at least eight people and one off-world birth are in place. A hundred years is a few generations, not the ember.

Biology: a reproducing sheltered culture, not a tardigrade and not open regolith, for about 10 years (established; Biosphere 2 lost oxygen control in about two years) and then 10,000 years. Hendry, Nosil, and Rieseberg (2007) is the citation that speciation has no single clock. Lenski and Travisano (1994) is cited so their 10,000 bacterial generations are not mistaken for 10,000 years.

Machines do not need oxygen. Fifty years (an estimate anchored to the 1980 NASA self-replicating lunar factory study, NASA CP-2255, 1982, which was not built) requires ore, a metal rate, electric power, radiators, repair at least as fast as the failure rate, and copy fidelity at or above 0.90. That floor is an estimate in the spirit of von Neumann's 1966 theory, not a measured error rate and not a blueprint. Machines alone can win those 50 years. They cannot win the ember or the Seed of Life. The machine ending is 10,000 years of a replicator tending a living culture it can re-seed.

An epoch is one decade, one century, or one millennium, and one risk roll. Humans cannot take a millennium. A millennium of life or machines waits until the 10-year or 50-year tier is already real. A separate roll can end Earth's program. An independent seed continues. A seed that has not entered an epoch does not. Version-1 saves migrate on load. An announcement that already happened does not fire again. Deep time is not granted by the migration.

## 8. 失败 / Losses

致命：

- 确认之后把试验生物在地球上无约束释放（`biosafety`）。确认前会停下来问。游戏不提供培养或释放步骤。
- 地球稳定度 ≤0（气候、政治、灾害把地球自己打垮）。已经独立的地外种子不因此结束：地球计划记为结束，种子继续，直到生命之种或种子自己死掉。
- 计划崩溃：连续赤字 ≥12 个月，且政治资本 ≤0，且舆论 ≤15。独立种子同样不因此结束。
- 孤注一掷：一次载人死亡，同时国库 <0.3、政治资本 ≤10、可飞乘员 <4、地外没有机器人。独立种子不因此结束。
- 地外灭绝且地球已救不了（稳定 <25）。地球已经归零时，死掉的种子仍是输。

可恢复：单次火箭失败、模拟舱撤离、预算削减、错过窗口、作物病害、还没构成孤注一掷的乘员死亡。模拟失败增加知识，记一次生物圈二号式的氧气教训，人撤出来。

载人任务的剂量帽 600 mSv 用来计算「还能飞的人」。这是规划帽，是估计。

## 9. 任务分级 / Mission class

`plan_mission` 返回 `ok`、`reckless` 或 `impossible`，并给出失败概率、IMLEO、费用、月数、是否滑窗口、剂量。

开局直接选 `mars_crew_conjunction` 是不可能：没有 `heavy_edl`。只补上 `heavy_edl`、没有全年封闭模拟，是鲁莽，失败概率 ≥0.5。确认后若骰子落在失败侧，乘员可以死，这不是胜利。

其他鲁莽理由包括：月球乘员但连 30 天模拟都没有；载人火星但水回收还没到 98%；没有粒子风暴掩体；返回氧还停在克级而不是吨级试点；跳过月球乘员经验；火星留驻发生在第一次往返之前；没做过模拟星壤就把温室送去火星。缺员、缺钱、缺窗口里的运力，按情况变成不可能或滑到下一扇窗口。

失败概率有上限 0.95。成功条件是 `roll/100 > failure_p`。

## 10. 政治 / Politics

派系是原创的，不是现实国家的化名，也不是《三体》的角色。闭天会只借用「有人会反对暴露」这一个想法。

| id | 中文 | 角色 |
| --- | --- | --- |
| `hearthbound` | 守炉派 | 认为离开地球是背叛。争预算，堵试验场的路 |
| `ember_covenant` | 火种盟 | 盟友。会逼你跳过模拟和机器人，直接送人 |
| `concord` | 协和 | 多边框架。第二来源的外交延迟也来自这里 |
| `meridian` | 子午线局 | 另一个空间工业集团。支持 ≥60 时成为第二发射来源 |
| `closed_sky` | 闭天会 | 安静拆计划。敌意高时才抽得到破坏事件 |
| `launch_guild` | 发射行会 | 掌握班次。没有第二来源时可以涨价 |
| `crew_guild` | 乘员公会 | 安全文化低时停飞 |

事件二十三种，加权，带前提。效果是预算、信任、舆论、一座烧掉的原型、一次尘暴。`sabotage` 的文本是夜间电气故障，不写做法。`mole_exposed` 才把秘密里的人放进 `revelations`。叙述在那之前不能点名。

治理：`open` 降低异议、略花政治资本、略升安全文化。`suppress` 压下声音的同时降低安全文化，并打开与压制有关的事件前提。

## 11. 语言、图、声音 / Language, pictures, voice

`language` 存在档里，`zh` 或 `en`。状态行、阶段名、事件文本和开场白都有两套。科学术语可以保留英文缩写（ISRU、IMLEO、Δv），句子跟存档语言走。

每回合可以写一张 SVG 场景卡。宿主若有图像工具或 `/show-me`，用引擎给的 `image_prompt`：纪录片、合理的硬件、没有外星生物、没有现实国家的旗帜、人在压力容器或模拟舱里。

结构图是脚本产物：Δv 的 Mermaid、科技树 Mermaid、栖息地剖面 SVG、任务架构 Mermaid。`diagram-design` 可以重排版，不能改数。

轨道可视化是单个 HTML：canvas 二维始终在，three.js r160 从 unpkg 可选加载。没有网也能看回退图。

TTS 走 `edge-tts` 命令行。没安装时脚本成功退出并说明 `edge_tts_missing`。声音：`zh-CN-XiaoxiaoNeural`、`en-US-AriaNeural`。

玩家提出开放设计问题时，若宿主有 `/grill-me`，用它来问清。否则最多问三个具体问题。不要替玩家选定教条。

## 12. 样本 / Sample

种子 7，负责人顾长川，计划名火种计划。为了让样本可复现，第一次建造使用 `quiet_quarter`，第二次 30 天模拟使用骰子 99 且没有事件。真实对局不要传这两个强制参数。样本结果：2026 年 8 月，回合 2，国库 4.56，舆论 52，政治资本 55，稳定 82，异议 12，封闭记录 30 天，阶段仍是地球模拟，下一窗口 2026-10，月球火种 0/10，十年送人上限 10。详见 README。
