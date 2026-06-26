---
name: vetclaw-bundle
version: 1.0.0
description: |
  VetClaw - 52个宠物医院/兽医诊所AI自动化技能套装。覆盖排班管理、病历记录、客户回访、经营分析等场景。
---

# VetClaw — 宠物医院AI技能套装 SKILL.md

## 概述

VetClaw 是一套专为宠物医院/诊所设计的52个AI自动化技能，基于 OpenClaw 平台运行。

## 快速配置

### 1. 诊所基础信息

编辑 `config/vet-config.yaml`：

```yaml
clinic:
  name: "你的宠物医院名称"
  address: "详细地址"
  phone: "联系电话"
  hours:
    weekday: "09:00-21:00"
    weekend: "10:00-18:00"
  services:
    - type: "基础诊疗"
      price_range: "50-200"
    - type: "疫苗接种"
      price_range: "80-300"
    - type: "绝育手术"
      price_range: "500-2000"
    - type: "急诊"
      price_range: "200-5000"
```

### 2. LLM 配置

```yaml
llm:
  provider: "deepseek"  # 可选: deepseek, qwen, openai
  api_key: "${DEEPSEEK_API_KEY}"
  model: "deepseek-chat"
  temperature: 0.3
```

### 3. 通知渠道

```yaml
notifications:
  sms:
    provider: "aliyun"  # 阿里云短信
    api_key: "${SMS_API_KEY}"
    sign_name: "你的宠物医院"
  wechat:
    app_id: "${WECHAT_APP_ID}"
    app_secret: "${WECHAT_APP_SECRET}"
```

## 技能详细说明

### 📞 前台接待类

#### vet-intake — 新客户信息采集
- **触发词**: "新客户"、"登记"、"建档"
- **功能**: 通过对话采集客户姓名、联系方式、宠物信息（品种/年龄/性别/是否绝育）
- **输出**: JSON格式客户档案，自动存入数据库

#### vet-appointment — 预约挂号
- **触发词**: "预约"、"挂号"、"看诊"
- **功能**: 根据排班表自动推荐时段，处理预约冲突，发送确认通知
- **排班冲突检测**: 自动检查医生排班，避免超额预约

#### vet-phone-ai — AI电话接听
- **触发词**: 来电自动触发
- **功能**: 识别来电意图（预约/咨询/价格/投诉），自动应答或转人工
- **话术模板**: 内置50+宠物医院常见问题应答模板

#### vet-emergency — 急诊分流
- **触发词**: "急"、"危险"、"出血"、"抽搐"、"呕吐不止"
- **功能**: 根据症状描述判断紧急程度（红/黄/绿三级），指导客户处理
- **注意**: 严重情况自动转人工，AI不做诊断

### 📋 病历与诊疗类

#### vet-lab-interpret — 化验单AI解读
- **触发词**: "化验单"、"血常规"、"生化"
- **功能**: 输入化验数值，AI标注异常指标并用通俗语言解读
- **支持**: 血常规、生化全套、尿检、便检

#### vet-vaccine-schedule — 疫苗计划
- **触发词**: "打疫苗"、"免疫计划"
- **功能**: 根据宠物种类/年龄生成疫苗接种时间表，自动设置提醒

### 💰 收费与财务类

#### vet-daily-report — 每日营收报表
- **触发词**: "今日营收"、"日报"
- **功能**: 自动汇总当日收费项目、总金额、各支付方式占比
- **输出**: 结构化报表 + 可视化图表

### 📢 营销与客户类

#### vet-churn-predict — 流失预警
- **触发词**: "流失客户"、"久未复诊"
- **功能**: 分析客户就诊间隔，标记超过平均间隔1.5倍的客户
- **动作**: 自动生成关怀话术，建议联系

## 知识库

### 兽医知识库 (vet-knowledge-base.json)

```json
{
  "common_diseases": {
    "犬瘟热": {
      "symptoms": ["发热", "咳嗽", "流鼻涕", "腹泻"],
      "urgency": "high",
      "advice": "立即就医，隔离其他宠物"
    }
  },
  "vaccine_schedules": {
    "dog": {
      "幼犬": ["6-8周: 第一针联苗", "10-12周: 第二针联苗", "14-16周: 第三针联苗+狂犬"],
      "成年犬": ["每年: 联苗加强+狂犬"]
    }
  },
  "drug_interactions": {
    "阿莫西林": {
      "avoid_with": ["氨基糖苷类抗生素"],
      "notes": "与食物同服可减少胃肠反应"
    }
  }
}
```

## 工作流集成

### 典型工作流：新客户到院 → 就诊 → 回访

```
客户来电/到店
  ↓
vet-phone-ai (判断意图)
  ↓
vet-intake (采集信息)
  ↓
vet-appointment (安排预约)
  ↓
vet-reminder (预约前1天提醒)
  ↓
[到院就诊]
  ↓
vet-record-create (创建病历)
  ↓
vet-prescription (开处方)
  ↓
vet-invoice (生成费用)
  ↓
vet-discharge (出院指导)
  ↓
vet-followup (设置复诊提醒)
  ↓
vet-feedback (满意度调查)
```

## 与其他技能包的兼容性

- **ai-secretary-bundle**: 共享日程/提醒模块
- **content-creator-bundle**: 社交媒体内容可直接使用
- **ecommerce-bundle**: 支付/订单模块可复用

## 常见问题

### Q: AI会代替兽医做诊断吗？
A: 不会。VetClaw 只处理行政和沟通任务，诊断和治疗决策始终由执业兽医完成。

### Q: 数据安全吗？
A: 所有数据存储在本地或您选择的云服务，不会共享给第三方。符合《个人信息保护法》要求。

### Q: 需要什么技术基础？
A: 基本的电脑操作能力即可。安装脚本会自动完成配置。

## 支持

- 文档: https://github.com/DMNO1/vetclaw-bundle/wiki
- 问题反馈: https://github.com/DMNO1/vetclaw-bundle/issues
- 技术支持: vetclaw@example.com
