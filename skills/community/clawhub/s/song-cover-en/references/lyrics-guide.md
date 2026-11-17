# 英文填词规则与文化处理

## 核心原则

**英文音节数 ≤ 中文汉字数**。这是硬约束，违反必然导致语速加快或旋律错位。

## 押韵

- 优先 couplet（两行一韵）：AA BB CC
- 韵脚放在行尾重读音节
- 不必完美押韵，近韵（如 time/shine, set/late）即可

## 文化处理

| 中文 | 英文 | 说明 |
|------|------|------|
| 江湖 | jianghu | **不译**，保留拼音 |
| 长安 | Chang'an | **保留** |
| 劫/缘 | ruin or fate | 保留佛家业力对仗 |
| 恩怨 | debt | 用"债"意象 |
| 宿敌 | nemesis | 标题词 |
| 门童 | gate boy | 保留古风意象 |
| 灵柩 | coffin | 直译 |

## 节奏处理（英文歌唱的特殊技巧）

1. **Elision（连读省音）**: "I am" → "I'm", "do not" → "don't"
2. **Melisma（一字多音）**: 允许一个音节跨多个音符（note_type=3）
3. **Syncopation（切分）**: 弱拍起唱，与中文原曲对齐
4. **Vowel elongation（元音拉长）**: 长音符用开放元音（ah, oh, oo）
5. **Consonant reduction（辅音弱化）**: 演唱中 t/d/p/b 等爆破音弱化

## 实例（《宿敌》28 句）

```
title_en: "Nemesis"
Where will I find you(5) / Was it written before(6) / Flying through time and space(6) / Caught in the blade's embrace(6)
March blooms wake one by one(6) / Who grows old as years run(6) / Ruin or fate for me(6) / With you no foe can touch me(7)
When the debt is half(5) / How do I hold back(5) / Lanterns glow with hate(5) / Vengeance comes too late(5)
Moonlit gate boy sighs(5) / Peaceful Chang'an lies(5) / When the stars set(4) / My fate is set(4)
Wait till ink dries(4) / Nemesis arrives(5) / I borrowed all your pain(6) / Can't give it back again(6)
Snow haunts the lone isle(6) / Falling, mile by mile(6) / Pluck a star from sea(5) / Stay the night with me(5)
Coffin sleeps in the vale(6) / No secret can prevail(6) / Jianghu ends in pain(5) / No one breaks the chain(5)
```

对应中文 28 句：
会在何处见到你 / 莫非前尘已注定 / 飞过时空的距离 / 却囿于刀剑光影 / 三月春花渐次醒 / 迢迢年华谁老去 / 是劫是缘随我心 / 除了你万敌不侵 / 当恩怨各一半 / 我怎么圈揽 / 看灯笼血红染 / 寻仇已太晚 / 月下门童喟叹 / 昨夜太平长安 / 当天上星河转 / 我命已定盘 / 待绝笔墨痕干 / 宿敌已来犯 / 我借你的孤单 / 今生恐怕难还 / 缠扰孤岛的雪雨 / 飘飘洒洒谁来停 / 摘取一颗海上星 / 陪我终夜不孤寂 / 灵柩长埋深谷底 / 没有永远的秘密 / 染指江湖结悲局 / 无人逃得过宿命

韵脚组：A you/before/space/embrace, B one/run/me/me, C half/back/hate/late, D sighs/lies/set/set, E dries/arrives/pain/again, F isle/mile/sea/me, G vale/prevail/pain/chain
