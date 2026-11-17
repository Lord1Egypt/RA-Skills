# 暗黑霓虹 · 赛博

有彩色深底 + 单色荧光点缀，高对比未来感。建议语法：卡片流。

## Token

```
主色 primary     #00E5FF
辅色 accent      #FF2D95
正文 text        #B8E8EC
次要 muted       #7EB8C0
线   line        rgba(0,229,255,0.28)
浅底 wash        rgba(0,229,255,0.08)
作品底 canvas    #141A2E
```

作品底必须是**有彩色深底** `#141A2E`（近黑蓝），禁止灰阶深底——微信深色模式会反转无彩色。正文用浅青灰 `#B8E8EC`，不用近白灰。主色电光青、辅色霓虹粉只点缀。长段正文放在深靛卡片上，每段控制在 3–5 行。根 `data-background` 用 `#141A2E`。

## 形态（一篇一套）

- **标题**：左对齐、字距 1px、主色小标。主标题 22–28px、字重 700，色用正文浅青灰；二级 18px，主色，带 `>` 前缀。无竖条。不要 `font-family`、不要 `text-shadow`。
- **分割**：全宽 1px 渐变线 `background:linear-gradient(90deg,transparent,#00E5FF,transparent)`。
- **卡片**：圆角 8px，背景 `#1E2A4A`，描边 `1px solid rgba(0,229,255,0.28)`，无重阴影。
- **图注**：左齐，次要色小字。

## 写法参考

版首：

```html
<section style="padding:28px 14px 20px;background:#141A2E;">
  <span style="display:inline-block;font-size:11px;letter-spacing:3px;color:#00E5FF;">// SYS.LOG 001</span>
  <p style="margin:14px 0 0;font-size:26px;font-weight:700;color:#B8E8EC;letter-spacing:1px;line-height:1.3;">主标题三到八字</p>
</section>
```

二级标题：

```html
<section style="margin:24px 10px 12px;">
  <p style="margin:0;font-size:18px;font-weight:700;color:#00E5FF;letter-spacing:0.5px;line-height:1.4;">&gt; 02 小标题</p>
</section>
```

卡片小结：

```html
<section style="margin:12px 10px 0;padding:20px;background:#1E2A4A;border:1px solid rgba(0,229,255,0.28);border-radius:8px;">
  <p style="margin:0;font-size:16px;line-height:1.8;color:#B8E8EC;">一句话带走。</p>
</section>
```

## 适配场景

科技数码、AI/大模型、游戏电竞、加密货币、科幻文化、潮流街头、音乐节、先锋设计品牌。产品发布、美妆轻卡片请用 `glassmorphism`；商务科技请用 `graphite-minimal`。

## 挑图气质

- styleAnchor：赛博深靛空间，电光青与霓虹粉点缀，冷金属与屏幕高光
- lightingHint：边缘轮廓光，暗部干净，荧光只点不铺
