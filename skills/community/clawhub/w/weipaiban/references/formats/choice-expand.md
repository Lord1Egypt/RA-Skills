# 选择其一 `choice-expand`

适用于从一组封面里点一个展开看完再回来选的作品。数量只有三种：二选一、四选一、六选一。不是答题计分，也不是长页滑动。

底层是现有的二选一节点。二选一是 1 个节点，四选一是 2 个竖向叠放，六选一是 3 个。不要做成一个带 4 个或 6 个槽位的新节点。

## 体验与设计

```text
作品根 section
├── 开场画布：标题，以及「选一个展开」
├── choiceExpand × 1 / 2 / 3
└── 收束画布 + ai-credit
```

- 选定 format 后若没说数量，先问 2 / 4 / 6。用户说「你定」时用二选一。
- 同一行是一对可对比的选择。四选一、六选一按行成对，不要把互不相关的条目硬拆进左右。
- **同一行左右封面高度必须相同**，并且等于这一行的 `data-init-height`。**同一行左右展开高度必须相同**，且不小于封面高度。左右不一样高时并排会错位；展开高度不一致时，导出会被拉成较高的一侧。
- 四选一、六选一各行的封面高度也建议相同，避免叠起来高低不齐。各行的展开高度可以不同，但同一行的左右两侧仍然必须相同。
- 一行内部左右互斥：点左侧则右侧封面让开，展开左侧；点返回恢复并排。行与行独立。展开一行会把下面的内容往下推，不会收起其它行。文案写「看完返回，再选下一个」，不要承诺全篇同时只展开一项。
- 封面在未点击时就能看懂选项，并有可见的展开按钮。展开稿底部有返回按钮。到达所选内容只需点一次。热区矩形盖住对应按钮，不要只盖住一行小字。
- 六选一把封面压矮一些，避免三行收起态过长。仍受 300 元素和 512KB 约束。
- 这是会员功能：未订阅可预览，导出需订阅。成品摘要要标明。

## 任务数据

沿用 [任务契约](../task-contract.md)，`meta.format="choice-expand"`。`design.json` 至少记录：

- `format`、`title`、`width=390`、`optionCount`（只允许 `2`、`4`、`6`）。
- `pairs`：长度必须是 `optionCount / 2`。每对有 `name`、`initHeight`、`expandHeight`、`duration`、`easing`，以及左右两项。
- 每一项有稳定侧别 `left` 或 `right`、封面文案、展开文案、颜色，以及 `expandTrigger` / `collapseTrigger` 热区。同一对的两项封面高度都等于该对 `initHeight`，展开高度都等于该对 `expandHeight`。

字段用于记录创作决策，不是额外发布 API。完整数据和可解析 HTML 见 [四选一示例](../../examples/formats/choice-expand/)。

## HTML 方言

仍遵守 [共享方言](../dialect.md) 的 300 元素、编组深度 5、512KB 和 CDN 规则。选择块复用现有二选一导出，无需 JavaScript。

二选一是下面这一块。四选一把两块按顺序放进根 section，六选一放三块。开场和收束是普通 390 宽 `<svg>`。

```html
<section
  data-type="choiceExpand"
  data-name="山与海"
  data-init-height="220"
  data-duration="0.5"
  data-easing="ease-in-out"
>
  <svg data-role="leftCover" width="195" height="220">
    <rect width="195" height="220" fill="#e5f0e4" />
    <text x="16" y="52" width="163" height="32" font-size="22" fill="#2f6a4f">
      去看山
    </text>
    <rect x="16" y="168" width="163" height="34" rx="17" fill="#2f6a4f" />
    <text
      x="16"
      y="176"
      width="163"
      height="20"
      font-size="13"
      fill="#f4efe4"
      data-align="center"
    >
      点击展开
    </text>
    <rect data-role="expandTrigger" x="16" y="168" width="163" height="34" />
  </svg>
  <svg data-role="rightCover" width="195" height="220">...</svg>
  <svg data-role="leftExpand" width="390" height="420">
    <rect data-role="collapseTrigger" x="105" y="348" width="180" height="44" />
  </svg>
  <svg data-role="rightExpand" width="390" height="420">...</svg>
</section>
```

解析规则：

- 恰好四块画布，角色为 `leftCover`、`rightCover`、`leftExpand`、`rightExpand` 各一。组顺序固定，多个选择块可以重复同一套 uid。
- 封面宽 195、高都等于 `data-init-height`。省略 `data-init-height` 时用封面高度，但左右封面高度仍然必须相同。展开宽 390，左右展开高度必须相同，且不小于初始高度。
- 每张封面恰好一个直接子节点 `<rect data-role="expandTrigger">`，每张展开稿恰好一个 `<rect data-role="collapseTrigger">`。热区从画面里摘掉，写入画布热区；可见按钮另写 `rect` + `text`，热区与按钮重合，且落在画布内。
- `data-duration` 缺省 0.5，必须为正。`data-easing` 缺省 `ease-in-out`，只接受现有缓动预设。
- 四块画布里只用普通画布标签。禁止再嵌 `choiceExpand`、`quiz`、`scroller`、`parallax`、`overlay`、`details`、`clickPopup`、`slideshow`、`richText`、`clickSwitch`、`animationGroup`。不要写 `data-auto-expand`。

## 素材与验收

按钮、底色和分割直接写 SVG。需要插画时才读取 [assets.md](../assets.md)。封面和展开可以共用一张图。

发布前检查：数量是 2、4 或 6；每一行左右封面同高、左右展开同高；热区盖住按钮；封面未点就能看懂；展开稿有返回；文案不承诺跨行互斥。预览里分别点每一侧、返回，再点另一行，确认上一行不会被自动收起，下面的收束画布会被推下去。最终保留 AI 声明。
