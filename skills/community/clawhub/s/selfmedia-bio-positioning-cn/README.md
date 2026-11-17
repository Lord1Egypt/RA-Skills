# 账号主页定位文案

![账号主页定位文案推广图](assets/promo-1600x900.png)

把真实经历变成用户一眼看懂的账号主页：得到可直接使用的简介、可持续的栏目定位，以及 3 条有明确分工的置顶内容建议。适合中文小店经营者、小说作者和自媒体创作者。

## 输入与结果

输入真实资历、内容方向和目标受众；可补充平台、语气与不宜提及的信息。Skill 会保留本地资料字段的原值，并把“已知事实”与“文案建议”分开。

输出为 Markdown，包含：

- 3 个主页简介版本；
- 3–5 个栏目定位建议；
- 3 条置顶内容建议。

缺少任一必填项时，它会先指出缺失项并索取补充，不会编造资历、成果或受众洞察。此 Skill 只为本人主页写文案，不做他人抖音账号的公开诊断。

## 示例

完整输入及三类交付的预期结果见 [fixtures/success.json](fixtures/success.json)。缺少字段时应列出的缺失项、补充问题和不得生成的交付项见 [fixtures/failure-missing-fields.json](fixtures/failure-missing-fields.json)；其中“想开始做自媒体”不是有效的真实资历。

## 验证

在本目录执行：

```bash
python3 scripts/self_test.py
```

该测试验证发布结构、元数据、素材尺寸以及 fixtures 中成功/失败的预期结果结构；它不运行虚构的文案生成引擎，也不把文案质量、事实准确性或 Skill 的真实行为伪装成自动验证。

## 来源与许可

用途参考 [social-media-skills/skills](https://github.com/social-media-skills/skills) 及 [profile-optimization](https://github.com/social-media-skills/skills/blob/main/skills/profile-optimization/SKILL.md)。中文说明、流程和样例为原创，未复制其源码或文案。采用 [MIT-0](LICENSE)。

## 实际输出示例

查看 [成功输出](fixtures/forward-success.md) 和 [缺资料响应](fixtures/forward-failure.md)，与原始输入逐项对照。

## 安装

```bash
npx skills add xxjrq/selfmedia-bio-positioning-cn
```
