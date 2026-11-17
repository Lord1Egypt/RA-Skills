# 两周内容日历

![两周内容日历推广图](assets/promo-1600x900.png)

把已有素材和创作时间排成一份能落地的 14 天内容制作日历，减少临时想选题和超排。适合中文小店经营者、小说作者与自媒体创作者。

提供账号定位、素材清单、每周产能和必须排入的主题，即可得到连续14天的选题顺序、内容形式、素材需求和制作时间建议。缺少关键字段时会明确要求补充，不会编造。

这是纯 Markdown Skill，不需要登录、浏览器或第三方 API。它只规划制作安排，不包含热点采集、发布执行和发布后数据回流。

## 使用

将以下内容发给 Skill：

```json
{"账号定位":"…","素材清单":["…"],"产能":"…","已确定主题":["…"]}
```

输出为含“已知事实、14天安排、建议与待确认、边界”的 Markdown 日历。完整规则见 [SKILL.md](SKILL.md)，可运行校验：

```bash
bash scripts/self-test.sh
```

## 来源与许可

实现为原创说明与样例。仅参考 [social-media-skills/skills](https://github.com/social-media-skills/skills) 及其 [batch-content-plan](https://github.com/social-media-skills/skills/blob/main/skills/batch-content-plan/SKILL.md) 的用途定位，未复制源码或文案。采用 [MIT-0](LICENSE)。

## Install / 安装

```bash
npx skills add xxjrq/selfmedia-content-calendar-cn
```

[成功输入](fixtures/success-input.json) · [实际参考交付](fixtures/forward-success.md) · [缺料分支](fixtures/forward-failure.md)。样例为离线材料上的 Markdown 执行参考，自检仅检查包结构和样例约束。
