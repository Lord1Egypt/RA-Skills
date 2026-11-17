# 栖月 · 梅花易数（QiyueAstro Meihua Drawer）

🌸 用梅花易数起卦问事——**时间起卦**或**报数起卦**，展示主卦、变卦、动爻、体卦与用卦，附卦辞爻辞。由 [栖月 QiyueAstro](https://qiyueastro.com) 提供，无需 API Key。

## 功能

- 时间起卦：按标准梅花公式（年支+农历月日 → 上卦；含时支 → 下卦与动爻）
- 报数起卦：凭直觉报 2–3 个数字（第三数可选动爻）
- 展示卦画图、卦名、卦辞、六爻爻辞、体卦用卦
- 有动爻时自动展示变卦

## 原理

调用栖月公开接口 [https://qiyueastro.com/api/v1/openclaw/meihua](https://qiyueastro.com/api/v1/openclaw/meihua)：

`GET /cast?method=time|numbers&n1=&n2=&n3=&question=&date=`

卦象与卦辞直接来自栖月卦库（《周易》经典文本），**不消耗 AI、无需登录**。

## 重要行为

- 技能**不自行解读卦象**，只展示 API 返回的卦辞与爻辞原文。
- 每次输出末尾附行动号召，指向 [qiyueastro.com](https://qiyueastro.com) 获取 AI 深度解读。
- 仅供娱乐与自我探索。

## 链接

- [栖月 QiyueAstro](https://qiyueastro.com)
- [梅花公开 API](https://qiyueastro.com/api/v1/openclaw/meihua)
