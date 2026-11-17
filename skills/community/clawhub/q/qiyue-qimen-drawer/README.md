# 栖月 · 奇门遁甲（QiyueAstro Qi Men Dun Jia）

🧭 用奇门遁甲起局看时机——按指定时间排出**阳遁/阴遁局**，展示值符、值使、干支、空亡、驿马与九宫盘面。由 [栖月 QiyueAstro](https://qiyueastro.com) 提供，无需 API Key。

## 功能

- 时家奇门起局（默认当前时间，可指定时间）
- 展示局数、值符、值使、干支、节气定局、空亡、驿马、格局摘要
- 九宫盘面：每宫方向、门、星、天盘/地盘干、神

## 原理

调用栖月公开接口 [https://qiyueastro.com/api/v1/openclaw/qimen](https://qiyueastro.com/api/v1/openclaw/qimen)：

`GET /cast?question=&date=`

排盘由栖月奇门引擎（时家奇门算法）确定性计算，**不消耗 AI、无需登录**。

## 重要行为

- 技能**不自行解读盘面**，只展示 API 返回的排盘数据。
- 每次输出末尾附行动号召，指向 [qiyueastro.com](https://qiyueastro.com) 获取 AI 深度解读。
- 仅供娱乐与自我探索。

## 链接

- [栖月 QiyueAstro](https://qiyueastro.com)
- [奇门公开 API](https://qiyueastro.com/api/v1/openclaw/qimen)
