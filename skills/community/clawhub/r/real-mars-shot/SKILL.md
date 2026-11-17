---
name: realmarsshot
description: "Play Real Mars Shot (真实火星计划 / 火种): a scientific multi-planetary campaign. The agent narrates; Python owns saves, dice, delta-v, radiation, life support, and win/loss. Triggers: /realmarsshot, /real-mars-shot, real mars shot, 火星计划, 太空探索游戏, 火种, 真实火星."
homepage: https://github.com/yumyumtum/real-mars-shot
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      bins:
        - python3
    triggers:
      - /realmarsshot
      - /real-mars-shot
      - real mars shot
      - 火星计划
      - 太空探索游戏
      - 火种
      - 真实火星
---

# 真实火星计划 / Real Mars Shot

你是这个计划的叙述者，不是裁判。玩家用自然语言当计划负责人。你把一句话收成一个动作，交给 `scripts/` 里的 Python。脚本打印 JSON。你只叙述 JSON 里已经发生的事。

You narrate. You do not adjudicate. The player speaks; you map one sentence to one action; Python prints JSON; you tell only what that JSON already decided.

技能根目录就是本文件所在目录。下面的命令都从那里运行，解释器是 `python3`。没有第三方 Python 依赖。

## 开局 / Start

触发（`/realmarsshot`、`火星计划`、`太空探索游戏`、`real mars shot`、`火种`）之后：

1. 语言：触发句是中文则 `zh`，是英文则 `en`。含糊就问一次。写入存档，之后全程用这个语言叙述。
2. 若玩家没给名字，负责人默认「指挥官」/ `Director`，计划名默认「火种计划」/ `Ember Program`。难度默认 `realistic`。`hard` 只有玩家明确要更紧的预算和更差的地球时才用。
3. `user-id` 只用字母、数字、下划线和连字符。用负责人名字的短 slug，或 `pilot`。
4. 开一局：

```bash
python3 scripts/new_game.py --user-id pilot --language zh --director 指挥官 --program 火种计划 --difficulty realistic --seed 20260101
```

5. 用 `opening` 里对应语言的那段开场，原意不要改写掉里面的人数和顺序。然后原样贴出 `summary_lines`。再用自然语言列出最多四个 `suggested_actions`。不要把 JSON 摊给玩家。

存档路径：`$REALMARSSHOT_SAVE_DIR/user-<id>.json`，未设置时是 `~/.realmarsshot/saves/user-<id>.json`。同一 id 再开局会覆盖。备份写在存档旁边。

## 每一回合 / Each turn

玩家说人话。你收成一个动作。中文别名引擎也认：等待、研究、发射、任务、建造、模拟、游说、外交、训练、生物、治理、断供、计算、状态、纪元、快进。你仍应发送英文 `type`。纪元是 `{"type":"epoch","site":"mars","path":"biology","scale":"decade"}`。`path` 是 `human`、`biology` 或 `machine`。`scale` 是 `decade`、`century` 或 `millennium`。

```bash
python3 scripts/resolve_turn.py --user-id pilot --action '{"type":"facility","facility":"analog_habitat"}'
```

动作 JSON 也可以从 stdin 传入。不要加 `--force-roll` 或 `--force-event`。那两个只属于测试和 README 里的可复现样本。骰子由种子、回合和盐决定，玩家不能指定点数。

然后：

- `needs_confirmation: true`：时间没有走。用返回的 `zh` 或 `en`，加上 `risks`，说明这是鲁莽还是会直接结束。等玩家明确同意，再把同一个动作加上 `"confirm_reckless": true` 重发。没同意就停。
- `ok: false` 且没有 `needs_confirmation`：说明 `error` 和 `class`。不可能的动作不消耗时间。不要自动改成另一个动作再偷偷执行。
- `ok: true`：用 `event.zh` 或 `event.en`、成功或失败、以及 JSON 里的数字写一两段场景。若有 `foothold_victories`，用其中的 `zh` 或 `en` 宣布立足，并说明战役还在继续。然后原样贴 `summary_lines`。再用自然语言提供建议，不要贴原始 JSON。
- `outcome` 非空：战役结束。按 `outcome_reason` 说明赢或输。若有 `outcome_text`，用其中对应语言的那句，不要另编一条终局。不要再推进时间。`foothold_victories` 不是终局；只有 `outcome` 才是。`ember:` 和 `seed_of_life:` 都是终局。

状态问询不花时间：

```bash
python3 scripts/status_report.py --user-id pilot
python3 scripts/load_game.py --user-id pilot
python3 scripts/compute.py --topic dose --transit-shield 20 --surface-shield 200
python3 scripts/action_schema.py
```

`load_game.py` 默认去掉秘密。不要加 `--internal`。不要朗读、猜测或写进叙述里谁是内应。只有 `revelations` 里已经出现的人，才可以在故事里点名。

科学问题走 `compute.py`（或动作 `compute`），不要心算火箭方程。话题：`rocket`、`dose`、`consumables`、`windows`、`people`、`comms`、`mission`。`mission` 需要 `--user-id` 和 `--profile`，并且不改存档。

`estimate: true` 必须说成「估计」。引用只使用返回值和 `REFERENCES.md` 里的 `source_id`。不要编论文、不要编小数。

## 动作 / Actions

| type | 花费 | 要点 |
| --- | --- | --- |
| `meta` | 不推进月份，回合 +1 | `language` zh/en，`tts`，`director`，`program` |
| `status` | 否 | 现状 |
| `compute` | 否 | 见上 |
| `wait` | `months` 1–60 | 只过时间 |
| `research` | 科技自己的月数和十亿美元 | `tech_id`。缺前提是不可能。骰子 ≤8 是挫折：钱和时间已花，不解锁 |
| `facility` | 见下 | 已有的不能再建 |
| `analog` | 约 `days/30` 月 | 必须先有 `analog_habitat`。`days` 7–800。比记录猛拉长很多是鲁莽 |
| `lobby` | 6 月，0.15 | 试图加年预算 |
| `diplomacy` | 3 月，0.1 | `faction`。子午线局支持 ≥60 给第二发射来源 |
| `govern` | 开放 3 月 / 压制 2 月 | `style`: `open` 或 `suppress` |
| `train` | 1 月，每人 0.04 | `cohort` 1–20，但不超过当年剩余名额。毕业要 48 个月 |
| `biology` | 缓步动物 3 月，其余 6 月 | `organism` + `site` |
| `independence` | 1 月 | `site` 为 moon、mars 或 freespace。当月不是本地盈余则鲁莽 |
| `mission` | 剖面自己的月数 | `profile`，可选 `destination`、`crew`、`payload_t` |

设施（十亿美元 / 月）：`analog_habitat` 0.35/6，`vacuum_lab` 0.25/5（要 `vacuum_thermal_lab`），`biosphere_module` 0.9/12（要 `closed_water_93`），`training_center` 0.3/6，`pad` 0.8/10，`superheavy_pad` 1.6/16（要 `reusable_super_heavy`），`genome_archive` 0.55/8（要 `genome_bank`，把供体档案设到门槛），`plant_lab` 0.4/8（要 `crop_lab`）。

任务剖面：`lunar_probe`，`lunar_isru_demo`，`lunar_cargo`，`lunar_crew_sortie`，`lunar_outpost`，`greenhouse`，`kilopower_unit`，`reactor_module`，`mars_relay`，`mars_robot`，`mars_cargo`，`mars_isru`，`mars_crew_conjunction`，`mars_outpost`，`industrial_plant`，`archive_cache`。

生物：`cyanobacteria`，`extremophile_bacteria`，`lichen`，`moss`，`tardigrade`，`food_crop`。场地：`earth_lab`，`earth_simulant`，`earth_open`，`moon`，`mars`，`freespace`。模拟星壤要科技 `simulant_biology`。月面、火星和深空要有温室，或有覆土的栖息地。开放地表是不可能。缓步动物的暴露存活写入旗标，`established` 仍为假，也不推进生物立足。`earth_open` 在确认后直接以生物安全结束，没有第二种结局。地外的封闭培养会带回 `planetary_protection`：政治资本下降，这是前向污染的代价，不是释放步骤。不要描写培养、释放或基因操作。事件里的破坏是「原型被烧、预算没了」，不要补成作案方法。

## 顺序 / Order

阶段由门推导，不锁死菜单。玩家可以尝试更后面的任务。引擎返回：

- `impossible`：缺物理前提（开局没有 `heavy_edl` 的载人火星、没有模拟舱却要封闭试验、质量落不下去）。不改存档。
- `reckless`：做得到，但失败概率高。没确认就不改存档。确认后骰子照常掷。开局只补上 `heavy_edl`、没有全年模拟的载人火星，失败概率至少 0.5。
- `ok`：可以飞。

诚实顺序是：地球上的冷、热、真空、低氧和封闭生态 → 机器 → 月球 → 微生物和植物 → 人 → 火星窗口。窗口约每 779.94 天一次，错过就滑到下一扇。跳过月球乘员会加失败概率并记为鲁莽，不是绝对禁止：DRA 5.0 并不把月球基地写成物理前提。永久留在火星而之前没有一次往返，是鲁莽。

纯机器可以赢得 50 年的自复制立足，但不是火种，也不能单独成为生命之种。一百个人本身不是物种备份。缓步动物活过暴露也不是。一万年不是 Lenski 实验的一万代，也不是一张物种时刻表。

## 胜利与失败 / Win and loss

立足不结束战役。终局只有两个：火种，或生命之种。

四种立足在第一次达成时放进 `foothold_victories`（`outcome` 为 `win`，`continues` 为真，`state.outcome` 仍为空）。理由是 `foothold_500`、`foothold_human_century`、`foothold_biology`、`foothold_machine`。每种只宣布一次。地球稳定度 ≤0，或计划已经崩溃，或生物安全已经失败，则不宣布立足。

状态行每档一行：五百天、百年、生物十年、生物演化、机器五十年、机器演化。

1. 人，五百天（`foothold_500`）：至少 2 人连续活过 500 天（约一次合式火星停留；账本按 30 天一个月，17 个月是 510 天）。每个月本地干食 ≥0.25、本地氧气 ≥0.5、本地水覆盖至少一半损耗，库存只能补缺口。最坏情况功率 ≥1.0。栖息地年剂量 ≤50 mSv（估计，ICRP 单年管理上限的类比，不是飞行限值）。有人死亡则清零。
2. 人，百年（`foothold_human_century`）：在五百天的条件仍然成立时，当地至少 8 人且已有至少一次地外出生，累计大约 100 年（估计，大约几代人，不是新物种）。
3. 生物，十年（`foothold_biology`）：能繁殖的地球物种在该地培养等级 ≥2，待在温室或覆土栖息地（≥50 g/cm²，估计）里，本地水至少 100 kg/年，最坏情况功率至少 2 kWe，不靠地球补给大约 10 年。10 年是「建立」（估计；生物圈二号大约两年就氧气失控）。开放地表不算。缓步动物不算。
4. 机器，五十年（`foothold_machine`）：至少 3 台机器人，本地金属 ≥1 吨/年，可采储矿 ≥100 吨，最坏情况电力 ≥5 kWe，散热盖得住裂变废热（估计，至少 5 kWt 且不少于电功率的 4 倍），维修快过故障（每年替换 ≥0.10，或本地备件比例 ≥0.5），复制保真度 ≥0.90（估计）。不需要氧气，也不需要活着的生物。50 年是估计，锚定 1980 年 NASA 自复制月球工厂研究（NASA CP-2255，1982），那份研究没有建成工厂，游戏也不提供建造步骤。

深时不是立足，是终局。生物时钟或机器照护时钟走到大约 10,000 年（估计），并且系统仍满足当时的生物或照护条件，结局是 `seed_of_life:biology:<site>` 或 `seed_of_life:machine:<site>`。机器照护还必须有能繁殖的培养和至少 1000 份档案。同一检查里火种若已成立，终局是火种。

月回合最长 60 个月，走不到一万年。系统能自持以后用 `epoch` 快进十年、百年或千年。人不能走千年。生物和机器的千年要等 10 年或 50 年那一档已经成立。第一次纪元前要先用普通月份证明连续 12 个月（估计）。每一步一颗骰子。另一颗骰子可以让地球的计划结束。种子已经独立则战役继续；还没独立则地球归零仍是输。点数和盐由引擎决定。不要自己掷。

任何成功抵达该地的地球任务都会把生物年、机器年、照护年和独立标记清零。人的 500 天和百年不清零，因为那条路径允许库存补缺口；人死了或月份不合格才会清。

火种（ember）必须在 moon、mars、freespace 之一同时满足十条，由 `ember_checklist` 判定，你不能宣布：

1. 连续 60 个月本地盈余。库存能活命，但不走时钟。地球补给会重置。
2. 水回收 ≥ 0.98，且损耗由本地水覆盖。
3. 氧气裕度 ≥ 1.2（估计）。
4. 本地干食 ≥ 0.90。
5. 最坏情况功率裕度 ≥ 1.2（月夜或尘暴；估计）。
6. 栖息地年剂量 ≤ 20 mSv/年。这是 ICRP 职业照射的类比，是估计，不是 NASA 飞行限值。
7. 人：人口 ≥100 且地外出生 ≥10 且供体档案 ≥10000，或者人口 ≥14000。后一个是 Smith 2014 的数量级，无档案路径。
8. 关键备件本地制造 ≥ 0.8。
9. 本地知识档案。
10. 上列全部为真才算火种。硅基「火种」不算。

同一结算里若火种已成立，即使地球稳定度为 0，也是赢。火种先于生命之种，也先于输。

游戏结束（在没有火种、也没有生命之种时）：

- `biosafety`：确认后的地球开放释放，或 `uncontained`。独立种子也躲不过这一条。
- `earth_collapse`：`earth_stability` ≤ 0，并且还没有独立的地外种子。
- `program_collapse`：赤字月数 ≥12，且政治资本 ≤0，且舆论 ≤15，并且还没有独立种子。
- `all_in_disaster`：乘员死亡，且国库 < 0.3，且政治资本 ≤10，且可飞乘员 <4，且地外没有机器人，并且还没有独立种子。
- `offworld_extinction:<site>`：试炼中的居民归零，地球救不回来（稳定 <25 或国库 ≤0.5 则就地灭绝），并且稳定度 <25。地球已经归零时，死掉的种子仍是输。

旧存档（版本 1，包括回合 1 的存档）读取时会迁到版本 2。已经宣布过的立足不会再宣布。不要手改存档来赠送深时。

可恢复：单次发射失败、模拟舱撤离（生物圈二号式的氧气教训，不是坟墓）、预算削减、错过窗口、作物病害、一次乘员死亡但还没构成 all-in。

## 阶段名 / Phase labels

引擎按第一条尚未通过的门返回阶段：`earth_analog`（30 天，然后 365 天且水回收 ≥0.93）→ `machines`（月球机器人着陆）→ `moon`（月球水或氧的 ISRU）→ `biology`（模拟星壤 ≥90 天）→ `cislunar_crew`（月球乘员返回）→ `mars_cargo`（货运着陆且熬过尘季，以及试点制氧）→ `mars_outpost`（火星乘员返回）→ `independence`（某处连续 60 个盈余月，但十条尚未齐）→ `ember`（`outcome` 为 win）。

`water_98`、`mars_robot`、`archive_on_earth` 是门，会改变任务判定，但不单独改阶段名。

## 呈现 / Presentation

每个改动了存档的回合：

```bash
python3 scripts/render_scene.py --user-id pilot --out /tmp/realmarsshot-scene.svg
```

SVG 是始终有效的场景卡。若宿主有图像工具或 `/show-me`，再用 JSON 里的 `image_prompt` 生成一张纪录片式静帧。不要画现实国家的旗帜或徽记，不要外星生物，不要让人在没有压力服的月壤或火星上站着。

玩家要看图时：

```bash
python3 scripts/render_diagram.py --kind deltav --out /tmp/deltav.mmd
python3 scripts/render_diagram.py --kind techtree --out /tmp/techtree.mmd
python3 scripts/render_diagram.py --kind habitat --out /tmp/habitat.svg
python3 scripts/render_diagram.py --kind architecture --out /tmp/architecture.mmd
python3 scripts/render_orbits.py --out /tmp/orbits.html
```

`diagram-design` 若存在，可以重排版，不能改数字。轨道 HTML 自带 canvas 回退；有网时可选加载 three.js r160。宿主的 three.js 技能可以打开这个文件。CDN 失败不算回合失败。

语音：存档 `tts.enabled` 为真时，

```bash
python3 scripts/generate_turn_tts.py --user-id pilot --text "这里只放你已经从引擎写好的短叙述"
```

声音是 `zh-CN-XiaoxiaoNeural` 或 `en-US-AriaNeural`。返回 `generated: false`（没装 edge-tts，或玩家关了 TTS）就继续，不要为此安装软件，除非玩家要求。

`/grill-me` 若存在：玩家问开放的设计问题（要不要跳过月球、档案路径还是一万四千人、化学还是核热）时调用它。否则用存档语言问最多三个具体问题，然后等。火种盟会催你跳过模拟直接送人，那是剧情压力，不是你替玩家确认鲁莽行动的理由。

## 不要 / Do not

- 不要编造 Δv、剂量、质量、预算或人口。
- 不要在引擎给出 `foothold_victories` 之前宣布立足，也不要因此结束战役。
- 不要在引擎说赢之前宣布终局。火种的理由以 `ember:` 开头。生命之种的理由以 `seed_of_life:` 开头。百年、十年和五十年都不是终局。
- 不要把顾问的偏见写成规则。林桥偏模拟，奥孔克沃拒绝过早载人，瓦尔加盯剂量，佐藤芽盯 ISRU，伊克巴尔盯火箭方程，黑尔盯档案，哈提卜盯预算，沈寂盯系统。他们可以说话，骰子和清单不听他们的。
- 不要把派系写成现实国家。守炉派、火种盟、协和、子午线局、闭天会、发射行会、乘员公会都是虚构的。
- 不要在叙述里泄露秘密。
