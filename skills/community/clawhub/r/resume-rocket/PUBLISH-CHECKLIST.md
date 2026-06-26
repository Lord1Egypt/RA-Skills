# ClawHub 发布 Checklist

## 发布前必备（Day 5 当天）

### 代码层
- [x] SKILL.md 完整
- [x] skill.json schema 规范
- [x] main.py 入口能跑
- [x] requirements.txt
- [x] examples/sample-resume.md
- [x] examples/before-after-demo.md
- [ ] LICENSE 文件（MIT）
- [ ] .gitignore（排 output/ __pycache__/ *.key）
- [ ] 一份英文 README-EN.md（国际化用户）
- [ ] 集成测试：`openclaw skill install ./` 能成功加载

### 商品页素材
- [x] 产品描述（SKILL.md）
- [x] 推广文案（MARKETING.md）
- [ ] 封面图（1200×630）
- [ ] Demo 动图 / 视频（30-60s 演示 match-score + rewrite）
- [ ] 3 张功能截图（评分报告 / 改写对比 / 面试卡）

### 账号与收款（只能你做）
- [ ] ClawHub 开发者账号：https://clawhub.com/publisher/register
- [ ] 实名认证（身份证 + 人脸）
- [ ] 绑支付宝收款
- [ ] 填分成信息（默认 ClawHub 抽 15%，你拿 85%）
- [ ] 拿到 publisher_id 告诉我

### 定价页后端
- [ ] 激活码生成规则（已在 license.py）
- [ ] 付款回调：ClawHub 付款成功 → 生成激活码 → 发邮箱
  - 方案 A：用 ClawHub 官方支付（简单，但抽成）
  - 方案 B：自建 Stripe/支付宝接入（灵活，但慢）
  - **推荐 A，MVP 用官方通道**

---

## 发布流程（上线日）

```bash
# 1. 本地打包
cd C:\Users\qq\.openclaw\workspace\skills\resume-rocket
clawhub lint .                 # 检查格式
clawhub pack . -o dist/        # 打包

# 2. 上传（需 publisher_id 登录）
clawhub login
clawhub publish dist/resume-rocket-0.1.0.tgz \
  --price-tiers "free:0,single:29,monthly:99,pro:299" \
  --category productivity \
  --tags "resume,job,career"

# 3. 等审核（一般 24h）

# 4. 上架后监控
clawhub stats resume-rocket --daily
```

---

## 上架后前 7 天每日任务

### 我自动做
- 每日数据抓取 → 飞书推送（下载 / 付费转化 / 差评）
- 用户反馈分类（bug / feature / 吐槽 / 好评）
- prompt 优化（如果改写质量有反馈问题）

### 你配合
- 看飞书日报（2 分钟）
- 重要差评我会 @你确认怎么回
- 提现时自己点 ClawHub → 提现 → 支付宝到账

---

## 风险 & 预案

| 风险 | 概率 | 预案 |
|---|---|---|
| 审核被拒（内容违规） | 低 | 立刻读审核反馈针对性修复 |
| 没人下载 | 中 | 加大推广，小红书/抖音投免费流 |
| 有人投诉"造假" | 低 | SKILL.md 已写明"不造假原则"，引导看声明 |
| 激活码被破解 | 低 | 本地 HMAC，短期内不影响；后期上服务端 |
| LLM 调用失败率高 | 中 | 已有 fallback 降级 + 多 provider 切换 |

---

## 成功指标（MVP 目标）

- D7：下载 100+，付费 5+
- D30：下载 1000+，付费 30+，月流水 ¥500-3000
- D90：月流水 ¥3000-10000，复购率 > 30%

达标就加开 `xhs-factory`（小红书工厂，第二个付费 skill）继续扩矩阵。
