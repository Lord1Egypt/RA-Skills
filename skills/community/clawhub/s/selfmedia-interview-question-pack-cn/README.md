# 采访问题与追问清单

![推广图：采访问题与追问清单](assets/promo-1600x900.png)

把受访者公开资料变成一份可直接录制的中文采访提纲：问题按主线排列，每题附条件式追问与素材核对点。它只处理你提供的材料，不会编造受访者的观点、经历或数据。

输入：受访者公开资料摘录、采访主题、时长（可加受众与避谈边界）。结果：按时间段组织的问题流程、追问、已知事实与录制前待确认事项；必需资料缺失时会先列出缺项和补充模板。

## 安装

```bash
npx skills add xxjrq/selfmedia-interview-question-pack-cn
```

## 适用场景

- 人物、品牌与专题采访的录制前准备
- 把简介、演讲摘要或已发布内容整理为提问顺序
- 需要避免预设受访者立场的中性追问

## 最小输入

```text
受访者公开资料：
采访主题：
时长：
```

完整工作方式与输出格式见 [SKILL.md](SKILL.md)。可复制的[成功交付样例](fixtures/success.md)与[缺料处理样例](fixtures/failure-missing-input.md)也已附在仓库中。

## 自检

```bash
python3 scripts/self_test.py
```

## 来源与许可证

本 Skill 的说明、流程与样例均为原创；仅核对了 [marketingskills customer-research](https://github.com/coreyhaines31/marketingskills/tree/main/skills/customer-research) 的公开业务用途，未复制其文本或代码。仓库采用 [MIT-0](LICENSE)。

真实前向参考：[成功](fixtures/forward-success.md) · [缺资料](fixtures/forward-failure.md)。问题允许活动与复购无关联的回答，输入资料保持原有来源归属。
