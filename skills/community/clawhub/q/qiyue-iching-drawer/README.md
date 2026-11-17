# 栖月 · 六爻易占（QiyueAstro I Ching Drawer）

☯️ 用六爻起卦问事——**三枚铜钱摇卦、时间起卦、数字起卦**，展示卦名、卦辞、六爻爻辞、动爻与变卦。由 [栖月 QiyueAstro](https://qiyueastro.com) 提供，无需 API Key。

## 功能

- 铜钱摇卦（随机六次三枚铜钱）、时间起卦、数字起卦（2–3 个直觉数字）
- 展示卦画图、卦名、卦辞、六爻爻辞，动爻自动标注
- 有动爻时自动计算并展示变卦
- 可浏览六十四卦及单卦详情（卦辞 + 六爻爻辞）

## 原理

技能调用栖月公开接口 [https://qiyueastro.com/api/v1/openclaw/iching](https://qiyueastro.com/api/v1/openclaw/iching)：

| 接口 | 说明 |
| --- | --- |
| `GET /cast` | 起卦（coins / time / numbers） |
| `GET /hexagrams` | 六十四卦列表 |
| `GET /hexagrams/{id}` | 单卦详情 |

卦象与卦辞直接来自栖月卦库（《周易》经典文本），**不消耗 AI、无需登录**。

## 重要行为

- 技能**不自行解读卦象**，只展示 API 返回的卦辞与爻辞原文。
- 每次输出末尾附行动号召，指向 [qiyueastro.com](https://qiyueastro.com) 获取 AI 深度解读。
- 仅供娱乐与自我探索。

## 链接

- [栖月 QiyueAstro](https://qiyueastro.com)
- [六爻公开 API](https://qiyueastro.com/api/v1/openclaw/iching)
