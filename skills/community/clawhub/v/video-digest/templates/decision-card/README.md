# Decision Card 模板使用说明

1 图 = 1 视频 = 4 区块：讲了什么 / 解决什么问题 / 适用范围 / 漏洞与偏见。

## 数据准备

在模板同目录创建 `struct-data.js`（必需）与 `meta.js`（可选）：

```js
// struct-data.js
const STRUCT = {
  "VIDEO_ID": {
    title: "中文标题（可选，缺省用 meta 的原题）",
    what: "视频核心内容 2-3 句，基于字幕提炼，不编造",
    problem: "这个视频补的是哪个认知/行动缺口",
    scope: "谁该看、什么场景用得上",
    caveat: "真实的局限：样本量、立场冲突、时效性、幸存者偏差等"
  }
};
```

```js
// meta.js（可选，补头部元信息）
const META = { "VIDEO_ID": { owner:"频道名", views:"12万播放", dur:"45 分钟", title:"原题" } };
```

## 内容红线

- `caveat` 必须是该视频**真实存在的局限**（基于内容核实），禁止模板化套话（如"仅供参考"）。
- `what` 只能来自字幕/已核实内容，与 Content Integrity 规则一致。
- 立场类视频（观点节目）必须在 caveat 中标注立场偏向。

## 渲染与截图

```bash
# 1. 目录下起本地服务
cd templates/decision-card && python3 -m http.server 8765 --bind 127.0.0.1

# 2. 用 WebKit headless（playwright-cli）逐张截图：
#    打开 http://127.0.0.1:8765/card.html?v=<videoId>
#    等待 .card 渲染 → 取 boundingBox → viewport 设为宽760、高=卡高+60 → clip 截图
#    注意：WebKit 下 element.screenshot 可能超时，用 boundingBox+clip 更稳
#    注意：避免在 run-code 中途 setViewportSize 后继续用旧引用（会触发 context 关闭），
#    先设 viewport 再取 box，或每张卡单独 goto。

# 3. 输出：<videoId>.png，680px 宽浅色卡片，杂志风（赤陶 #c4552f 强调色）
```

## 已验证实战

builders-tube 项目（48 视频站）用此模式批量出 38 张卡，全部通过视觉校验：
参考 `历史参考实现 builders-tube`（cards.html + structured.js + cards/*.png）。
