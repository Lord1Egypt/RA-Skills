# 点击展开 `details`

`<details>` 映射为点击展开组件。`<summary>` 是点前状态，后续每个直接子节点依次成为展开后的状态；可以嵌套另一组 details。

## 写法

```html
<details data-name="夜巡须知" data-duration="0.8">
  <summary>
    <svg width="390" height="56" data-name="展开前">
      <rect x="20" y="8" width="350" height="40" fill="#F7F7F7" rx="20" />
      <text x="36" y="18" width="318" height="20" fill="#333333" font-size="14">
        19:30 集合 · 点击看路线 ›
      </text>
    </svg>
  </summary>
  <svg width="390" height="120" data-name="展开后">
    <foreignObject x="36" y="20" width="318" height="84">
      <section style="font-size:15px;line-height:1.7;color:#333333;">
        绕塔一周，再沿窗棂巷返回。
      </section>
    </foreignObject>
  </svg>
</details>
```

## 规则

- 必须有且只有一个直接子 `<summary>`，并至少有一个展开后子节点。
- `summary` 和展开后内容可以是 SVG、普通 section 或合法交互子树。
- 点前必须有可见 hint，并让读者先看到核心结论；展开内容用于补充，不用于藏住必须信息。
- `data-duration` 单位为秒；建议 0.4–0.8。
- 可多层展开，也可在展开后嵌套 details，但流式嵌套总深度不超过 5。
- `layered-scroll` 与 `parallax-scroll` 的组件白名单都不含 details，不得在这两个 format 中使用。

不要把 details 做成大量 FAQ 列表；它在交互作品中应承担场景翻页、局部揭示或叙事转折。
