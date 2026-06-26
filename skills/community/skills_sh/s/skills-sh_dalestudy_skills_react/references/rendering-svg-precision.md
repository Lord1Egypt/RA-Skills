---
title: Optimize SVG Coordinate Precision
impact: LOW
impactDescription: reduces SVG file size
tags: rendering, svg, optimization, svgo, file-size
---

## SVG 좌표 정밀도 축소

SVG 좌표 소수점을 줄여 파일 크기 감소. viewBox 크기에 따라 적절한 정밀도 선택.

**Incorrect (과도한 정밀도):**

```svg
<path d="M 10.293847 20.847362 L 30.938472 40.192837" />
```

**Correct (소수점 1자리):**

```svg
<path d="M 10.3 20.8 L 30.9 40.2" />
```

**SVGO로 자동화:**

```bash
npx svgo --precision=1 --multipass icon.svg
```

**일괄 처리:**

```bash
npx svgo --precision=1 --multipass -f ./src/icons/ -o ./src/icons/
```

**SVGO 설정 파일 (`svgo.config.js`):**

```js
module.exports = {
  multipass: true,
  plugins: [
    {
      name: "preset-default",
      params: {
        overrides: {
          cleanupNumericValues: { floatPrecision: 1 },
          convertPathData: { floatPrecision: 1 },
        },
      },
    },
  ],
};
```

> 원본: [vercel-react-best-practices: rendering-svg-precision](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rendering-svg-precision.md)
