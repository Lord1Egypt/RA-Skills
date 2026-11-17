# 栖月 · 大六壬（QiyueAstro Da Liu Ren）

🀄 起大六壬课——按指定时间排出**月将、四课、三传**，附课体与神煞摘要。由 [栖月 QiyueAstro](https://qiyueastro.com) 提供，无需 API Key。

## 功能

- 时间起课（默认当前时间，可指定）
- 月将、占时、初传/中传/末传、四课、三传、旬空、课体、神煞摘要

## 原理

调用栖月公开接口 [https://qiyueastro.com/api/v1/openclaw/liuren](https://qiyueastro.com/api/v1/openclaw/liuren)：

`GET /cast?question=&date=`

排课由栖月六壬引擎确定性计算，**不消耗 AI、无需登录**。

## 重要行为

- 技能**不自行解读课体**，只展示 API 返回的原文。
- 每次输出末尾附行动号召，指向 [qiyueastro.com](https://qiyueastro.com) 获取 AI 深度解读。
- 仅供娱乐与自我探索。

## 链接

- [栖月 QiyueAstro](https://qiyueastro.com)
- [大六壬公开 API](https://qiyueastro.com/api/v1/openclaw/liuren)
