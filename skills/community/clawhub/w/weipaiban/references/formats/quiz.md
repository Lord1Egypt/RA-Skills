# 答题 `quiz`

适用于知识测验、科普答题和学习自测。每题至少两个选项，恰好一个正确项；读者每题只能选择一次，选中即锁定。答对得 1 分、答错或未答得 0 分。不是多选题、性格选项匹配或选项加权评分。

## 体验与设计

```text
作品根 section
├── quiz：计分答题
│   ├── questions：题组画布
│   │   ├── 标题、题干、背景、插图等自由内容
│   │   └── 每题 quizQuestion → 多个 quizOption → before + after
│   ├── before：答题前画布，自由装饰 + 一个 submit 触发区
│   └── after：答题后画布，公共背景 + 多个 result 分档
└── ai-credit
```

- 三画布宽度均为 390，各自明确高度；内部为画布绝对定位。不要求选项等宽、固定数量、列表排布或固定题目节拍，横排、纵排、图文组合均可。
- **题干在 quizQuestion 编组之外**，作为题组画布的普通文本或富文本；quizQuestion 的直接子节点只能是选项。题干在选中前后始终可读。
- before 状态的内容包围盒就是选项点击区域。需要完整按钮面积时，放一块带底色的 rect 配合文字，不要仅用零散小字构成点击区域。各题、各选项的点击区域都不得相交；边缘相接不算重叠。
- 选中后 before 始终保留，after 在其上叠加，**不是替换或隐藏前态**。使用透明填充描边、勾叉、标记、说明或插图；如果后态用不透明底覆盖文字，应有意补齐需要保留的信息。后态包围盒不得覆盖其他选项的点击区域。
- 选定后不能改选、不能取消；显式提示「每题选一次，选定后不能更改」。滑动手势沿用组件原有处理。
- 答题前画布仅 submit 编组的包围盒触发结果展开，其他文字和装饰不是提交按钮。不额外要求全部题目答完，未作答按 0 分处理。
- 答题后公共背景放在 result 编组之外；每个结果可以自由组合图文，各结果可以占据同一位置，因为只显示一个分档。
- 结果的 score 为不重复的非负整数，必须含 0 分。显示 **score ≤ 总分的最高档**：配置 0、2、3，则 0/1 分显示 0 档、2 分显示 2 档、3 分显示 3 档。不是按绝对距离选最近值，也不必为每一个得分配置结果。设计时分档应在可得分范围内。

## 任务数据

沿用 [任务契约](../task-contract.md)，`meta.format="quiz"`。`design.json` 至少记录：

- `format`、`title`、`width=390` 和统一视觉方向。
- `canvases.questions`：高度、题目列表；每题的题干与位置、选项列表；每个选项的稳定 ID、唯一 `correct=true`、before 点击框及内容、after 叠加内容与位置。
- `canvases.before`：高度、submit 点击框与按钮文案，以及装饰内容。
- `canvases.after`：高度、公共背景及 `results`（每项 `score`、文案、图文布局）。
- `scoring`：每题答对 1 分，单次选择锁定；`resultMatching="floor"`。

字段用于记录创作决策，不是额外发布 API。完整数据和可解析 HTML 见 [quiz 示例](../../examples/formats/quiz/)。

## HTML 方言

仍遵守 [共享方言](../dialect.md) 的 300 元素、编组深度 5、512KB 和 CDN 规则。quiz 复用现有 SVG 渲染，无需 JavaScript。

```html
<section data-type="quiz" data-name="生活小测">
  <svg data-role="questions" width="390" height="240">
    <text x="24" y="20" width="342" height="32" font-size="20">
      短途出行怎么选？
    </text>
    <text x="24" y="60" width="342" height="24" font-size="14">
      每题选一次，选定后不能更改
    </text>
    <g data-type="quizQuestion">
      <g data-type="quizOption" data-correct="true">
        <g data-state="before">
          <rect x="24" y="100" width="342" height="48" fill="#d9e4cc" />
          <text x="36" y="112" width="310" height="24">步行或骑行</text>
        </g>
        <g data-state="after">
          <rect
            x="24"
            y="100"
            width="342"
            height="48"
            fill="transparent"
            stroke="#32745b"
            stroke-width="3"
          />
        </g>
      </g>
      <g data-type="quizOption" data-correct="false">
        <g data-state="before">
          <rect x="24" y="170" width="342" height="48" fill="#d9e4cc" />
          <text x="36" y="182" width="310" height="24">独自开车</text>
        </g>
        <g data-state="after">
          <rect
            x="24"
            y="170"
            width="342"
            height="48"
            fill="transparent"
            stroke="#ac523b"
            stroke-width="3"
          />
        </g>
      </g>
    </g>
  </svg>
  <svg data-role="before" width="390" height="90">
    <g data-role="submit">
      <rect x="24" y="16" width="342" height="56" fill="#23483c" />
      <text x="90" y="32" width="210" height="28" fill="#e6eecb">
        点击查看结果
      </text>
    </g>
  </svg>
  <svg data-role="after" width="390" height="120">
    <rect width="390" height="120" fill="#d9e4cc" />
    <g data-role="result" data-score="0">
      <text x="24" y="32" width="342" height="40">从一件小事开始改变</text>
    </g>
    <g data-role="result" data-score="1">
      <text x="24" y="32" width="342" height="40">你答对了！</text>
    </g>
  </svg>
</section>
```

quiz 恰好包含三个带角色的 svg；不使用 auto-expand。问题、选项、状态、提交和结果均为 g，必需编组不能空。普通图文继续使用共享画布语法；本版不在 quiz 画布里嵌入其他交互组件。普通 g 的 translate/scale 沿用共享坐标烘焙流程；优先保持状态组与点击区域静态，避免动效改变可点位置。

解析器自动映射为 `as="quiz"`、`quizMode="score"`、`quizQuestionType="singleSelect"`、`quizEffectType="open"`，并生成 `quizOptionFrame`、`quizQuestion`、`quizOption`、`quizDefaultButton`、`quizActiveButton`、`quizBeforeAnswer`、`quizSubmitButton`、`quizAfterAnswer`、`quizAnswerResult` UID。HTML 无需直接书写 UID。

## 素材与验收

图片按自由布局中的实际占位准备，引用 manifest 的最终 CDN；纯色按钮、描边和简单标记直接写 SVG。需要图片时才读取 [assets.md](../assets.md)，不套用滚动背景规则。

发布前检查：唯一正确项、单次选择提示、题干在选项外、点击区域不重叠、原内容保留且后态可见、触发区准确、0 分兜底及分档含义正确。预览中分别尝试答对、答错、重复选择、未答提交、分档间隙和满分；最终保留 AI 声明。
