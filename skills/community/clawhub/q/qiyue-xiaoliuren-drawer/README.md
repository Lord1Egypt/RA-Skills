# 栖月 · 小六壬速断（QiyueAstro Xiao Liu Ren）

🤲 用小六壬速断眼前之事——按当前时间起课，占得**大安/留连/速喜/赤口/小吉/空亡**六宫之一，附歌诀原文。由 [栖月 QiyueAstro](https://qiyueastro.com) 提供，无需 API Key。

## 功能

- 时间起课（默认当前时间，可指定）
- 占得宫 + 通行歌诀原文 + 月/日/时顺数轨迹

## 原理

调用栖月公开接口 [https://qiyueastro.com/api/v1/openclaw/xiaoliuren](https://qiyueastro.com/api/v1/openclaw/xiaoliuren)：

`GET /cast?question=&date=`

推算由栖月小六壬引擎确定性计算，**不消耗 AI、无需登录**。

## 重要行为

- 技能**不自行解读掌诀**，只展示 API 返回的歌诀原文。
- 每次输出末尾附行动号召，指向 [qiyueastro.com](https://qiyueastro.com) 获取 AI 深度解读。
- 仅供娱乐与自我探索。

## 链接

- [栖月 QiyueAstro](https://qiyueastro.com)
- [小六壬公开 API](https://qiyueastro.com/api/v1/openclaw/xiaoliuren)
