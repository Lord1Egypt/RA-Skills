# Layout Modes v1.2

筛选阶段必须产出 `layout_plan`：

```json
{
  "mode": "full-family | phrasal-hub | function-word | compact-three",
  "cards": [
    { "slot": "TL|TR|BL|BR|T1|T2|T3", "title": "...", "items": ["IR指针或短文案键"] }
  ],
  "knowledge_chain": ["...真实节点..."],
  "omit": ["不上图的 IR 路径说明"]
}
```

## 怎么选 mode

| 条件 | mode |
|------|------|
| word_family 中 priority≥4 的 adj + adv 至少各 1，且有可用搭配 | `full-family` |
| 高频搭配/多义 ≥3，派生链弱或不适合小学主图 | `phrasal-hub` |
| 词类为限定词/介词/连词等功能词 | `function-word` |
| 上图条目总块 < 4，或强行四卡会空 | `compact-three` |

冲突时：功能词优先 `function-word`；否则多义短语优先 `phrasal-hub`；完整词族才用 `full-family`。

## full-family（完整词族）

- 骨架：中央 Hub + 四象限 + 底链
- 默认象限：TL 短语/基本用法 → TR 形容词 → BL 副词 → BR 名词/其他延伸
- 底链示例：`{word} → 短语 → 形容词 → 副词 → 名词`
- 例：care、success（若形副名齐全）

## phrasal-hub（多义 / 短语中心）

- 骨架：中央 Hub + **3～4 张用法卡**（按义项或搭配簇分组）
- 推荐卡：高频搭配 A、高频搭配 B、另一义项或句型、易混/注意（用 `common_mistakes`，勿造派生）
- 底链示例：`核心义 → 搭配① → 搭配② → 易混点`
- **禁止**为填 TR/BL/BR 而编造 -ful/-less/-ness
- 例：get、run、take

## function-word（虚词）

- 骨架：中央 Hub（词 + 词性标签 + 一句话功能）+ 三或四卡
- 推荐卡：主要用法对比、正例、反例/勿用场景、固定说法或搭配
- 底链示例：`什么时候用 → 怎么用 → 别和谁混`
- **禁止**词族派生象限
- 例：the、a/an、of、to（作小品词时）

## compact-three（三卡紧缩）

- 骨架：中央 + 三卡（T1/T2/T3），可无第四卡
- 用于：真实高 priority 内容不够四块；或用户只要「最短一张」
- 留白可以，假内容不行

## 共同约束

- 卡内条目来自 IR；删 P3 / 低 priority，不缩字到不可读
- 每卡仍要：短标题 + 2～4 点 + ≥1 短例句（英+中）+ ≥1 场景向小插画说明（成图用）
- 对用户不出现 mode 英文名
