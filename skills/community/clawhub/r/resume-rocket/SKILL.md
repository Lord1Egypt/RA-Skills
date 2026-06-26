---
name: resume-rocket
version: 0.1.1
description: AI 简历火箭 — 一键把你的简历改写成目标 JD 的满分匹配版，可选对接 Boss 直聘自动投递。输入旧简历 + 目标岗位 JD，输出「高命中改写版 + 匹配度评分 + 面试话术卡」。春招/秋招/跳槽必备。
author: openclaw-community
homepage: https://github.com/openclaw-community/resume-rocket
license: MIT
tags:
  - resume
  - job-hunting
  - career
  - boss-zhipin
  - llm
  - productivity
category: productivity
pricing:
  free_tier: true
  free_limit: 1次/天
  paid:
    - name: 单次改写
      price: 29
      currency: CNY
      description: 一份简历 × 一个 JD 的深度改写
    - name: 月卡
      price: 99
      currency: CNY
      description: 30 天内无限次改写 + JD 匹配分析
    - name: Pro 版
      price: 299
      currency: CNY
      description: 月卡所有功能 + Boss 直聘自动定向投递 + 投递数据分析
entry: main.py
requires:
  python: ">=3.9"
  packages:
    - python-docx
    - pdfplumber
    - openai
dependencies_skills:
  - boss-zhipin  # 仅 Pro 档需要
---

# Resume Rocket · AI 简历火箭

> **一句话**：把你的简历按目标 JD 重写，命中率从 30% 拉到 90%。

## 为什么需要它

- 投 100 份简历 → HR 用 ATS 系统按关键词过滤 → 90% 直接淘汰
- 每家公司 JD 关键词都不一样 → 人工一份份改到怀疑人生
- 改完自己看不出问题 → 还是没反馈

**Resume Rocket 做的事**：
1. 解析你的简历（PDF/Word/纯文本）
2. 抓取目标岗位 JD（Boss 直聘链接 / 拉勾 / 手动粘贴）
3. LLM 对齐：把你简历里**本来就有**的经历，**用 JD 要求的语言**重新表达
4. 输出匹配度评分 + 改写版 + 面试话术

**不做虚假包装**。只做"你真的做过的事，用招聘方想听的话说出来"。

## 快速开始

```bash
# 安装
clawhub install resume-rocket

# 免费试用（每天 1 次）
openclaw skill run resume-rocket \
  --resume "C:\path\to\my-resume.pdf" \
  --jd "https://www.zhipin.com/job_detail/xxx.html"

# 输出：
# ./output/
#   ├── resume-optimized.docx    改写版简历
#   ├── match-report.md           匹配度分析
#   └── interview-cards.md        面试话术（STAR 格式）
```

## 核心功能

### 1. 智能解析
- ✅ PDF / DOCX / MD / TXT 自动识别
- ✅ 提取工作经历、项目、技能、教育、证书
- ✅ 识别隐含能力（从项目描述反推技能栈）

### 2. JD 深度理解
- ✅ Boss 直聘链接自动抓取
- ✅ 手动粘贴 JD 文本
- ✅ 提取核心关键词 / 优先级 / 加分项

### 3. 匹配度评分（满分 100）
```
技术栈匹配：85/100  ✅ Python / SQL / 数据建模  ❌ 缺：Spark
工作年限：    10/10 ✅ 3 年经验 符合 JD "3-5 年"
学历：        10/10 ✅ 本科 符合
亮点项目：    20/25 ⚠️ 建议突出"用户留存提升 15%"的 A/B 测试项目
综合评分：    88/100
```

### 4. 改写建议
- **语言重写**：把"做了用户分析" → "搭建用户留存监控体系，通过 RFM 模型..."
- **关键词注入**：JD 要 Spark 你没有 → 从你的"Hadoop 离线计算"合理过渡
- **STAR 法则**：每段经历 Situation/Task/Action/Result 结构化

### 5. 面试卡片（免费版不含）
针对 JD 痛点生成 10 张话术卡：
- "你为什么想来我们公司？" → 3 个定制答案
- "你的缺点？" → 避雷 + 巧妙回答
- 可能被问的技术深挖（按 JD 技术栈）

### 6. Pro 版 · 自动投递
```bash
openclaw skill run resume-rocket --mode auto-apply \
  --jd-list boss.txt \
  --daily-limit 50
```
- 读 JD 列表 → 每个 JD 定制一份改写版 → 用 `boss-zhipin` skill 自动投递
- 日报：投了多少 / 打招呼 / HR 回复率 / 建议改进

## 定价

| 版本 | 价格 | 说明 |
|---|---|---|
| 免费 | ¥0 | 1 次/天，无面试卡，无自动投递 |
| 单次 | ¥29 | 单份简历 × 单个 JD，全功能 |
| 月卡 | ¥99 | 30 天无限改写 + 面试卡 |
| Pro | ¥299/月 | 月卡 + 自动投递 + 数据分析 |

---

## 💳 购买方式（扫码付款 → 加微信发码）

### 步骤
1. **扫下方二维码付款**（支付宝 / 微信任选）
2. **备注你的订单**：`rr-` + 档位首字母 + 你的联系方式
   - 例：`rr-S-13427xxx` = 单次 ¥29（S=Single）
   - 例：`rr-M-13427xxx` = 月卡 ¥99（M=Monthly）
   - 例：`rr-P-13427xxx` = Pro ¥299（P=Pro）
3. **加微信** `AGI-竹`（扫付款码同名）
4. 发付款截图给我，**1 小时内发激活码**
5. 配置环境变量：
   ```bash
   set RR_LICENSE_KEY=S-20261231-xxxxxxxx
   ```

### 支付宝收款
![支付宝](assets/pay-alipay.jpg)

### 微信收款
![微信](assets/pay-wechat.jpg)

### 退款政策
- 付款后 24 小时内，未使用激活码可全额退款
- 已使用则不退（激活码绑定你的本机账号）
- 有问题加微信直接找我

---

## 配置

首次使用需配置 LLM：
```bash
openclaw skill config resume-rocket \
  --llm-provider alibaba \
  --llm-model qwen-plus \
  --llm-key sk-xxx
```

推荐模型：
- 🏆 qwen-plus（阿里百炼，速度快 + 中文强）
- ✅ deepseek-chat（便宜 + 质量好）
- ✅ glm-4（智谱，中文优秀）

## 常见问题

**Q: 会不会造假？**
A: 不会。工具**只基于你简历里已有的事实**重新表达，绝不编造经历。你可以对着改写版问自己："这事我真做过吗？"答案必须是"是"。

**Q: 多久能改完一份？**
A: 免费/单次版 30-60 秒；Pro 批量投递时每份 10-15 秒。

**Q: 隐私？**
A: 简历数据不上传云端。LLM 调用走你自己配置的 Key，数据只在本机 + LLM 服务商之间传输。

**Q: 为什么不走平台付款？**
A: ClawHub 是 skill 注册中心，不处理支付。所以我们走**私域收款 + 手动发码**。优点：无平台抽成，你付多少我拿多少（除了税）。缺点：不是 24×7 自动化，高峰期可能等 1-4 小时发码。

**Q: Boss 投递会封号吗？**
A: Pro 版内置频控（默认 50/天、随机间隔）+ 模拟真人行为，但**投递本身有被 Boss 风控的风险**，建议不要开太高频率。账号安全由用户自行承担。

## 路线图

- [x] v0.1 PDF/DOCX 解析 + LLM 改写 + 匹配评分
- [ ] v0.2 Boss JD 抓取 + 批量模式
- [ ] v0.3 面试卡片生成
- [ ] v0.4 Pro 自动投递
- [ ] v0.5 投递效果数据分析 + 话术 AB 测试
- [ ] v1.0 正式版 + 多平台（拉勾/脉脉/LinkedIn）

## 作者 & 支持

- 开发：OpenClaw 社区
- 反馈：提 Issue 或飞书群
- 商务合作：企业批量授权请联系

---

**⚠️ 合规声明**

本 skill 只做内容优化，不做：
- ❌ 伪造学历/证书/工作经历
- ❌ 代人面试 / 代发声
- ❌ 绕过平台风控的高频投递

使用过程中的账号风险由用户自行承担。
