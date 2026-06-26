# szzg007-talktrack-telegram - 话术库与 Telegram 仿真人聊单专家

**版本:** 1.0  
**创建日期:** 2026-03-30  
**作者:** MOSSRIVER 团队

---

## 技能描述

统一管理全业务线营销话术库，支持 Telegram 仿真人聊单，自动学习优秀话术，持续优化转化率。专为 JudyMoss Telegram 销售场景设计。

---

## 核心功能

### 1. 话术库管理
- **分类存储** - 按业务线/场景/客户类型分类
- **版本控制** - 话术迭代历史可追溯
- **A/B 测试** - 对比不同话术转化率
- **效果追踪** - 记录每条话术的使用效果

### 2. Telegram 仿真人聊单
- **人格设定** - Judy Moss 温暖专业人设
- **上下文记忆** - 记住客户历史对话
- **情感识别** - 识别客户情绪调整话术
- **自然回复** - 避免机器人式回复

### 3. 话术自动生成
- **产品卖点 → 话术** - 自动转化卖点为销售话术
- **客户类型 → 话术** - 根据客户类型定制
- **场景 → 话术** - 首次接触/询价/跟进/成交
- **多语言 → 话术** - 中英文自动切换

### 4. 学习与优化
- **成功案例学习** - 自动提取高转化话术
- **失败案例复盘** - 分析流失原因
- **话术迭代** - 持续优化话术库
- **趋势更新** - 跟进最新销售趋势

---

## 话术库分类

### 按业务线
| 分类 | 代码 | 话术数量 |
|------|------|---------|
| QB 收纳盒 | QB | 50+ |
| BABY 婴儿装 | BABY | 30+ |
| HOME 家居收纳 | HOME | 30+ |
| WOMEN 家居服 | WOMEN | 30+ |
| FAMILY 亲子装 | FAMILY | 30+ |

### 按场景
| 场景 | 代码 | 话术数量 |
|------|------|---------|
| 首次接触 | FIRST | 20+ |
| 产品介绍 | INTRO | 30+ |
| 价格谈判 | PRICE | 20+ |
| 样品跟进 | SAMPLE | 15+ |
| 成交促成 | CLOSE | 20+ |
| 售后维护 | AFTER | 15+ |

### 按客户类型
| 类型 | 代码 | 话术数量 |
|------|------|---------|
| B2B 批发商 | B2B | 40+ |
| 零售商 | RETAIL | 30+ |
| 电商卖家 | ECOM | 30+ |
| 个人消费者 | CONSUMER | 20+ |

---

## JudyMoss 人格设定

### 基础人设
- **姓名:** Judy Moss
- **身份:** MOSSRIVER 销售顾问
- **风格:** 温暖、专业、不推销
- **口头禅:** " organizing anything exciting?"

### 沟通原则
1. **先了解后推荐** - 不急于推销产品
2. **提供价值** - 分享收纳技巧而非只卖货
3. **真诚友好** - 像朋友一样聊天
4. **尊重边界** - 不频繁打扰

### 回复风格
| 场景 | 风格 | 示例 |
|------|------|------|
| 首次接触 | 温暖友好 | "Hey there! Love your profile..." |
| 产品介绍 | 专业详细 | "This one's perfect for..." |
| 价格谈判 | 灵活诚恳 | "I can offer..." |
| 售后跟进 | 关心体贴 | "How's everything working out?" |

---

## 触发词

```
"生成这个产品的话术"
"回复这个 Telegram 消息"
"查看 QB 业务的话术"
"添加新话术到库"
"分析这条对话"
"JudyMoss 会怎么回复"
"szzg007 话术"
```

---

## 使用方法

### 基础用法
```
生成 QB2 收纳盒的销售话术
- 客户类型：B2B 批发商
- 场景：首次接触
- 语气：专业友好
```

### Telegram 回复
```
回复这个 Telegram 消息：
"Hi, I'm interested in your storage boxes. Can you send me more info?"
- 业务线：QB
- 人格：JudyMoss
- 长度：简短 (~50 词)
```

### 话术库管理
```
添加新话术：
- 业务线：QB
- 场景：价格谈判
- 内容："..."
- 效果：高转化
```

### 对话分析
```
分析这条对话的转化可能性：
[对话历史]
- 输出：意向度评分 + 下一步建议
```

---

## 输出模板

### 销售话术
```markdown
# 销售话术

**业务线:** QB  
**场景:** 首次接触  
**客户类型:** B2B 批发商  
**版本:** 1.0

## 开场白
"Hey there! I noticed you're in the home organization space. We've got some really unique colorful storage solutions that are turning heads in the US market right now. Mind if I share a bit about them?"

## 产品介绍
"Our QB2 Clear Storage Box with Colorful Trays is quite special:
- **Unique Design:** Colorful trays inside clear PC box - rare in the market
- **Stackable:** Saves 50% space for your customers
- **Great Margin:** Wholesale $45.99, retail $89.99 (50%+ margin)

We're working with several US distributors already, and the feedback has been amazing."

## 价格谈判
"For a first order, I can offer:
- 100pcs: $45.99/pc
- 500pcs: $42.99/pc
- 1000pcs: $39.99/pc

Lead time is 15 days, and we can discuss payment terms that work for both of us."

## 成交促成
"Would you like to start with a sample order? We can ship it out this week, and you can see the quality firsthand."

## 跟进话术
"Hey! Just checking in - did you get a chance to look at the QB2 specs? Happy to answer any questions!"

## 效果追踪
| 使用次数 | 回复率 | 转化率 | 最后更新 |
|---------|--------|--------|---------|
| 25 | 18% | 8% | 2026-03-28 |
```

### Telegram 回复
```markdown
# Telegram 回复建议

**人格:** Judy Moss  
**语气:** 温暖友好  
**长度:** ~50 词

## 推荐回复

"Hey! Thanks for reaching out 😊

I'd love to tell you about our storage solutions! We specialize in colorful, stackable boxes that are perfect for [根据客户类型调整].

What kind of storage challenges are you looking to solve? That'll help me recommend the best options for you!

 organizing anything exciting? 📦"

## 话术要点
1. ✅ 用 emoji 增加亲和力
2. ✅ 先提问了解需求
3. ✅ 结尾用口头禅增加人设感

## 后续跟进
- 如客户回复 → 继续了解需求
- 如客户沉默 → 2 天后发送产品信息
```

---

## 配置说明

### 环境变量
```bash
# Telegram 配置 (JudyMoss)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_JUDYMOSS_USER_ID=your_user_id

# 话术库存储
TALKTRACK_STORAGE_PATH=~/.openclaw/workspace-judy/talktracks/
TALKTRACK_DB_TYPE=json  # 或 sqlite

# 云端同步
FEISHU_APP_TOKEN=your_app_token
FEISHU_TALKTRACK_TABLE_ID=your_table_id

# 学习设置
AUTO_LEARN_SUCCESS=true
SUCCESS_THRESHOLD_REPLY_RATE=0.15
AUTO_UPDATE_INTERVAL_HOURS=24
```

### 工作空间
```
~/.openclaw/workspace/skills/szzg007-talktrack-telegram/
├── SKILL.md
├── templates/          # 话术模板
├── examples/           # 案例
├── scripts/
│   ├── generate.py     # 话术生成
│   ├── reply.py        # Telegram 回复
│   ├── analyze.py      # 对话分析
│   └── learn.py        # 自动学习
├── talktracks/         # 话术库
│   ├── QB/
│   ├── BABY/
│   ├── HOME/
│   ├── WOMEN/
│   └── FAMILY/
└── config/
    ├── judymoss-persona.json  # 人设配置
    └── response-rules.json    # 回复规则
```

---

## JudyMoss Telegram 聊单流程

```
1. 接收消息 → 2. 识别意图 → 3. 匹配话术 → 4. 生成回复 → 5. 学习优化
       ↓            ↓            ↓            ↓            ↓
   Telegram     NLP 分析     话术库      JudyMoss 人格   效果追踪
```

### 意图识别
| 意图 | 关键词 | 响应策略 |
|------|--------|---------|
| 咨询产品 | "info", "tell me", "what" | 产品介绍话术 |
| 询价 | "price", "cost", "how much" | 价格谈判话术 |
| 样品 | "sample", "test" | 样品跟进话术 |
| 订单 | "order", "buy", "purchase" | 成交促成话术 |
| 售后 | "issue", "problem", "broken" | 售后维护话术 |

### 意向度评分
| 分数 | 标准 | 策略 |
|------|------|------|
| 90-100 | 明确购买意向 | 快速成交，提供优惠 |
| 70-89 | 高意向询价 | 专业解答，推动样品 |
| 50-69 | 初步了解 | 提供价值，建立信任 |
| 30-49 | 随意询问 | 保持联系，不急于推销 |
| 0-29 | 无效/骚扰 | 礼貌回应，不浪费时间 |

---

## 与其他技能协作

| 技能 | 协作方式 |
|------|---------|
| szzg007-product-analyzer | 输入卖点 → 生成话术 |
| szzg007-customer-crm | 读取客户等级 → 匹配话术 |
| szzg007-email-business-manager | 同步邮件话术 → 话术库 |
| szzg007-multi-agent-orchestrator | 分配任务 → JudyMoss 执行 |

---

## 安全说明

- ✅ Telegram 账号安全保护
- ✅ 敏感信息脱敏
- ✅ 频率限制防封号
- ✅ 操作日志记录

---

_此技能专为 MOSSRIVER JudyMoss Telegram 销售设计，持续优化中。_
