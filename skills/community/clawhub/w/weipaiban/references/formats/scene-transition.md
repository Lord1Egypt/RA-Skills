# 场景转场 `scene-transition`

在一个固定高度的展示区域里逐幕推进同一主题。点击当前场景的热区后播放本幕动画，时间轴结束时将本幕画布高度归零，后面的等高画布自然顶上来。最后一幕静态收场。

适合连续故事、空间穿行、阶段变化；每次点击都应推动同一个故事。独立图片切换用 clickSwitch；滑动浏览长内容用其它 scroll format。

制作时同时读取 [方言](../dialect.md)、[SVG 画布](../components/svg.md) 和 [动画组](../components/animation-group.md)。本格式仅组合已有语法，不新增服务端 `data-type`。

## 层级与高度

```text
作品根 section：overflow hidden
├── 场景层：overlay 前层，高度 0、允许内部溢出
│   ├── 场景 1：390 × H，播放后高度归零
│   ├── 场景 2：390 × H，播放后高度归零
│   └── 场景 N：390 × H，静态结尾
└── 占位画布：390 × H，透明、不接事件、不添加动效
```

- 至少两幕。所有场景宽 390、高 `H`，占位画布同高；`H` 是设计值，示例取 600。
- 场景按叙事顺序作为同一个 overlay 的直接 SVG 子节点，无间距；不要每幕单独套一个 overlay。
- 场景层 `data-elevated="true"`，不占文档流；它后面的占位画布唯一负责整件作品的高度。根层裁剪到该高度，防止提前看到、点到后面的场景。
- 场景画布写 `data-overflow="hidden"`、`pointer-events="none"`，不自动撑高；高度归零后旧内容不能继续溢出遮挡下一幕。
- 不用 scroller、不用页面滚动模拟换幕，不通过缩小占位画布或 scaleY 模拟高度归零。

## 连续场景设计

先做逐幕分镜，再准备素材。每幕写清：初始画面、点击动作、动画过程、结束画面、下一幕如何接住这个结束画面。

相邻两幕至少有一项明确承接：同一人物或道具的位置、同一地平线、同一门框/轮廓，或上一幕动作带出的下一幕结果。保持统一主题、主角外观、画面比例、材质、光线逻辑；不要把无关海报顺序排列当成转场。

上一幕动画终态与下一幕初态应尽量匹配。可复用背景或道具；文字、按钮和背景的变化要服从故事。每幕点前能看懂操作结果，例如“推开门，走进晨光”，不写空泛的“点击查看”。结尾回收前面的动作或意象，留下完整可读的静态画面。

## 点击与时间轴

### 非末幕

每幕只有一个主触发热区。画布、底图、文字、普通组和动画内容均不接受事件；只有热区 `pointer-events="visible"`。一次点击同时触发本幕内容动画和祖先画布的归零计时。

优先用一个 `animationGroup` 组织本幕需要播放的元素：

- 使用 `appear` 或 `disappear`，触发统一为 `pointerUp`；子动效也显式写 `data-trigger="pointerUp"`。
- 动画组导出时自动生成一次性热区；热区点击后移走，事件沿嵌套组冒泡至场景画布，同步启动内容和画布动效。不要再叠一块独立热区阻断这条链路。
- 当前 HTML 动画组热区覆盖整组范围。示例使用整幕大小的组，让整幕都可点击，并在组外放可见提示；不要虚构局部热区属性。若需要精确局部按钮，须先确认导入器支持该热区配置。
- 底图、提示等静态元素放在组外，并明确 `pointer-events="none"`。不要在画布上开 `visible` 来扩大点击面。
- 同一幕有多个动画组时，独立组的热区不会自动联动。优先合成一个主时间轴，不把各自等待点击的组误算成一次点击播放。
- 不用 `load`、无限循环或需要二次点击才播放的分支；下一幕到达前不得自行播放。

从**本幕点击时刻**计时，全部参与动画结束的最晚时间为：

`T = max(delay_i + duration_i × repeat_i)`

这里的 delay 是各动画相对本次点击的起播时刻，repeat 必须为有限正数。顺序播放也先排成这条绝对时间轴；不能只取最后写的元素时长，也不能把并行动画时长累加。一次性热区移走属于操作机制，不计入叙事时长。

画布的归零动效延迟必须等于 `T`，不是从整篇加载起算，也不是所有前幕累计时间。归零自身使用短时长 `0.001s` 并保持终态；修改本幕任何动画后都要重算 `T`。

### 高度归零写法

作品 API 支持“高度归零” preset。作为场景 SVG 的**直接子节点**：

```html
<animate
  data-preset="高度归零"
  data-trigger="pointerUp"
  data-delay="1.5"
  data-duration="0.001"
  data-repeat="1"
  fill="freeze"
  restart="never"
/>
```

`1.5` 替换为本幕 `T`。预设自动取画布实际高度作为起点，默认持续 1s；本格式显式指定 0.001s 实现瞬时换幕。不要把 height 动效放入动画组，因为套组 wrapper 的尺寸不是场景画布的占位尺寸。

旧发布服务尚未部署该预设时，兼容写法是把 `data-preset="高度归零"` 换成 `attributeName="height" values="600;0"`（600 换为 H），其它时序属性保持不变。

### 最后一幕

末幕不添加任何动画：无动画组、无高度归零、无自动入场或循环效果。静态展示收口内容。保留独立热区矩形作为场景结构的一部分，但不绑定转场或动画，也不显示“下一幕”提示；没有明确的结尾操作时不要虚构可点击的功能。其它元素仍不接收事件。

AI 声明作为末幕底部的静态内容，文案为“文章部分内容由AI辅助设计和制作”；不额外加一块改变作品高度的声明画布。这是本格式对共享“最后一块 ai-credit”的具体实现。

## `design.json` 契约

- `format`: `scene-transition`。
- `shell`: `width=390`、`sceneHeight=H`、`overflow="hidden"`；`sceneLayer` 标识 overlay，`spacer` 标识唯一占位画布。
- `scenes[]`: 按叙事顺序排列，包含 `id`、`name`、`height`、`initialState`、`endState`、`handoff`、`hint`、`hotspot`、`timeline`、`collapse`、`layout`。
- `hotspot`: 写明 `source`（`animationGroup` 或末幕的 `static`）、矩形范围及事件行为。
- `timeline[]`: 每项有稳定元素 `id`、`trigger`、`delay`、`duration`、`repeat`、所用动效；与 HTML 的时间轴一致。
- 非末幕 `collapse={"delay":T,"duration":0.001}`。末幕 `timeline=[]`、`collapse=null`、`hint=null`，不得假设仍需一次点击才能看到结局。
- `layout`: 可执行的坐标与尺寸；图片使用稳定 `assetId`。声明记为末幕内 `ai-credit`。

完整数据见 [design.json](../../examples/formats/scene-transition/design.json)，HTML 见 [work.html](../../examples/formats/scene-transition/work.html)。示例是语法与结构参考，不固定创作主题、幕数或视觉风格。

## HTML 壳

```html
<section data-name="作品标题" data-overflow="hidden">
  <section data-type="overlay" data-elevated="true" data-name="场景层">
    <svg
      width="390"
      height="600"
      data-overflow="hidden"
      pointer-events="none"
      data-name="场景1"
    >
      <animate
        data-preset="高度归零"
        data-trigger="pointerUp"
        data-delay="1.5"
        data-duration="0.001"
        data-repeat="1"
        fill="freeze"
        restart="never"
      />
      <!-- 静态底图、点前可见提示：pointer-events="none" -->
      <g
        data-type="animationGroup"
        data-mode="disappear"
        data-trigger="pointerUp"
        data-order="up"
        width="390"
        height="600"
        data-name="本幕时间轴"
      >
        <!-- 内容使用 pointerUp 动效，时间轴最晚结束在 1.5s；热区由动画组生成 -->
      </g>
    </svg>
    <!-- 更多等高场景；末幕只保留静态内容与独立热区，没有 animate -->
  </section>
  <svg
    width="390"
    height="600"
    pointer-events="none"
    data-name="占位画布"
  ></svg>
</section>
```

## 素材策略

场景与道具按 [assets.md](../assets.md) 从当前 tag 素材池分配，不使用循环背景。相邻幕优先复用同一张场景图或同一件透明道具。透明道具只用池里 `transparent=true` 的图。底色、按钮、简单几何直接用 SVG。

先确认各幕初态与终态；不要把需要分别运动的元素全部放进一张背景。纯 SVG 示例允许 `asset-request.assets=[]`。

## 发布前质量闸门

- 一个前层 overlay + 一个静态占位画布；根层裁剪。场景层高度为 0，场景画布和占位画布均为 `390 × H`。
- 所有非末幕都有一次点击启动的主时间轴，只有热区接事件；背景、文字和画布均为 none。
- 非末幕恰有一条画布高度归零动效，delay 等于本幕时间轴终点，结束保持高度 0；不是隐藏透明度后仍占空间。
- 等待任意时长不点击，当前幕与后续幕都不播放；点击后本幕完整播完才换幕；快速重复点击不重播、不跳过下一幕。
- 后续幕在到达前被根层裁剪且不能点击；归零后旧幕也不能溢出或拦截点击；外层作品高度始终不变。
- 相邻幕终态与初态衔接可解释，无坐标跳变或无关主题插入；结尾无任何动画，无假的下一步提示。
- AI 声明在末幕内静态可见；manifest URL 原样使用；总元素 ≤300、HTML ≤512KB。
- 解析校验后仍需在作品预览检查一次完整点击流程；仅检查 HTML 可以解析不能证明运行时换幕正确。
