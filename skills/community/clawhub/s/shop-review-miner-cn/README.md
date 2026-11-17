# 商品评价需求提炼

![商品评价需求提炼推广图](assets/promo-1600x900.png)

把你合法拥有的真实商品评价，整理成产品改进与详情页优化可直接使用的 Markdown：常见诉求、正负反馈主题、详情页补充点和待验证问题。适用于中文小店经营者，也适用于复盘读者反馈的小说作者和自媒体创作者。

## 输入与结果

输入商品/作品名、品类、评价原文（均必需），以及可用的评分、时间、使用场景、版本等原始字段。按 [SKILL.md](SKILL.md) 工作流可得到一份清楚区分“已知事实”和“建议”的需求提炼 Markdown。

缺少商品/作品名、品类或评价原文任一项时，Skill 会列出缺失信息及影响并停止分析，不会编造结论。它不抓取平台评论，不做公开同款价格比较，也不替代抖音评论洞察。

## 快速使用

```text
使用 $shop-review-miner-cn 分析以下真实商品评价。请保留原始字段值，输出常见诉求、正负反馈主题和详情页补充点；资料不足时说明缺口。
```

输入形状可参考 [成功样例](fixtures/success.json)；[失败样例](fixtures/failure-missing-reviews.json) 展示缺少评价原文时应指出的关键缺失。

## 自测

在仓库根目录运行 `python3 scripts/self_test.py`。它校验打包结构、字段、图像尺寸，以及成功/失败样例的明确预期（单次信号不算常见诉求、事实与建议分栏、缺少评价原文时停止）；不运行或假装运行定性分析，真实效果需以已授权评价人工复核。

## 来源与许可

用途参考 [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) 的 customer-research Skill。未复制其源码或文案；本仓库说明、流程和样例均为原创。参考仓库采用 MIT License；本 ClawHub 分发包采用 [MIT-0](LICENSE)。
