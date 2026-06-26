# Day 1 完成报告 · resume-rocket skill 骨架

## 已产出

```
C:\Users\qq\.openclaw\workspace\skills\resume-rocket\
├── SKILL.md         3.5 KB  商业化就绪的产品说明 + 定价 + FAQ + 合规声明
├── skill.json       1.0 KB  OpenClaw CLI schema（3 个子命令）
├── main.py          3.0 KB  入口 + 命令路由 + 档位鉴权流程
├── lib/             (待填充各模块)
│   ├── parser.py        简历解析（PDF/DOCX/MD/TXT）
│   ├── jd_fetcher.py    JD 抓取（Boss URL / 纯文本）
│   ├── matcher.py       匹配度评分
│   ├── rewriter.py      LLM 改写
│   ├── interview.py     面试卡片生成
│   ├── auto_apply.py    Pro 批量投递（对接 boss-zhipin）
│   ├── license.py       档位鉴权
│   └── exporter.py      输出 DOCX/MD
├── templates/       (LLM prompt 模板)
└── examples/        (测试数据)
```

## 产品定位敲定

- **免费**：每天 1 次改写，吸引流量
- **单次 ¥29**：单份简历 × 单 JD 深度改写 + 面试卡
- **月卡 ¥99**：30 天无限次
- **Pro ¥299/月**：自动投递

## 商业化关键点

1. **合规性**：已在 SKILL.md 写明"不伪造、不代面试、不高频投递"三不原则
2. **护城河**：依赖 `boss-zhipin` skill 的投递能力是我们独有的
3. **流量池**：免费档 1 次/天 → 用户被口味后付费转化
4. **价格梯度**：29/99/299 = 一杯奶茶 / 一顿饭 / 一张电影卡对应的心理锚点

## Day 2 我要做的（不打扰你）

- [ ] `lib/parser.py` PDF/DOCX 解析
- [ ] `lib/jd_fetcher.py` Boss 抓取（用现有 `boss-zhipin`）
- [ ] `lib/matcher.py` 规则评分 + LLM 评分
- [ ] `lib/rewriter.py` LLM 改写 prompt 工程
- [ ] `templates/` 的 prompt 模板调优
- [ ] 本地跑通一份测试简历

## Day 3 需要你做的事（只 1 件）

**给我一份你的旧简历（脱敏或真实都行）** 当测试样本。
- 脱敏：把姓名/电话/邮箱/身份证/真实公司名改成 ***
- 格式：PDF / Word / 纯文本都行
- 放到：`C:\Users\qq\.openclaw\workspace\skills\resume-rocket\examples\`
- 或飞书直接发我

没有的话我用网上公开的模板简历顶上，但测真实简历改写效果会更好。

## Day 5 需要你做的事（阻塞项）

**ClawHub 开发者账号注册 + 绑收款**

```
1. 访问 https://clawhub.com/publisher/register
2. 手机号/邮箱注册
3. 实名认证（身份证 + 人脸）
4. 绑支付宝收款
5. 告诉我开发者 ID
```

这步无论如何都必须你做，AI 做不了。

---

## 现在的进度

- ✅ Day 1 骨架 + 产品设计（30% 完成）
- 🔄 继续 Day 2：开始写 `lib/parser.py`，要不要我继续？

**你只需回复**：
- **"继续"** → 我开工 Day 2
- **"SKILL.md 要改 X"** → 告诉我改什么
- **"暂停，我要审"** → 我停，等你看完文档
