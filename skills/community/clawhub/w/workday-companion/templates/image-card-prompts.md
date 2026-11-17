# 图卡提示词模板

先完成文字判断，再生成图。默认 9:16 工作日桌面票据；中文文字采用确定性 overlay，底图提示词不要求模型绘制可读文字。

## 通用底图

```text
Create a clean 9:16 editorial ticket card for Workday Companion. Quiet workday desk atmosphere, tactile paper, restrained mixed-color palette, clear empty zones for title, reason, action and 2-4 short tags. No readable text, no fake letters, no logo, no face, no private workplace details. Keep generous margins and strong contrast for later Chinese text overlay.
```

## 四模块视觉变量

| 模块 | 视觉线索 | 避免 |
| --- | --- | --- |
| 今日工作签 | 便签、日历撕页、铅笔痕、晨光 | 算命、庙宇、星盘 |
| 午饭判官 | 午餐小票、餐盘轮廓、热气、品类图标 | 虚构店名、医疗饮食图标 |
| 精神天气台 | 天气窗、电量格、云层、雨点 | 病历、诊断标签、灾难画面 |
| 下班放行单 | 通行票、回家箭头、傍晚街灯、短绕路线 | 真实地图、危险逃跑、消费诱导 |

## Overlay 文案

每张图只放：

```text
模块名 · 时间
主标题：12-18 字
依据：40 字内
现在做：40 字内
标签：2-4 个，每个 8 字内
页脚：今天先这么过。
alt_text：120 字内
```

## 分阶段提示词

### 今日工作签

```text
Use the general ticket prompt. Add a narrow morning sign strip, one folded sticky note and subtle task marks. Leave empty text zones. Mood: practical opening ritual, light luck, grounded action.
```

### 午饭判官

```text
Use the general ticket prompt. Add a lunch receipt edge, warm bowl silhouette and three abstract category marks for main, backup and avoid. No restaurant name, menu price or health claim.
```

### 精神天气台

```text
Use the general ticket prompt. Add a small weather window, cloud layer and simple battery indicator. Keep the scene calm and observational, without clinical or therapeutic imagery.
```

### 下班放行单

```text
Use the general ticket prompt. Add a perforated evening pass, one homeward line and one optional short detour. No real map, address, event name or unsafe escape imagery.
```

## 全套

用户说 `每阶段出图` 时生成四张独立卡，保持同一纸张、网格和页脚；颜色与图形按模块变化。不要把四张挤进一张长海报，除非用户明确要求总览图。

## 能力降级

图像工具不可用时返回三块：

1. `能力状态`：未检测到可调用图像能力或调用失败。
2. `Image prompt`：通用底图 + 当前模块变量。
3. `Overlay text`：来自已经完成的文字判断。

不得把 prompt 写成已生成图片。

