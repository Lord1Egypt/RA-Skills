# 栖月 · 紫微斗数排盘（QiyueAstro Zi Wei Dou Shu）

⭐ 排紫微斗数命盘——输入**出生年月日时与性别**，输出五行局与十二宫主星。由 [栖月 QiyueAstro](https://qiyueastro.com) 提供，无需 API Key。

## 功能

- 五行局（金四局、水二局等）
- 十二宫主星分布（命宫、兄弟、夫妻、子女、财帛、疾厄、迁移、仆役、官禄、田宅、福德、父母）
- 主星亮度（庙/旺/利等）与四化

## 原理

调用栖月公开接口 [https://qiyueastro.com/api/v1/openclaw/ziwei](https://qiyueastro.com/api/v1/openclaw/ziwei)：

`GET /chart?year=&month=&day=&hour=&gender=&question=`

排盘由栖月紫微引擎（iztro）确定性计算，**不消耗 AI、无需登录**。

## 重要行为

- 技能**不自行解读命盘**，只展示 API 返回的排盘数据。
- 每次输出末尾附行动号召，指向 [qiyueastro.com](https://qiyueastro.com) 获取 AI 深度解读。
- 仅供娱乐与自我探索。

## 链接

- [栖月 QiyueAstro](https://qiyueastro.com)
- [紫微公开 API](https://qiyueastro.com/api/v1/openclaw/ziwei)
