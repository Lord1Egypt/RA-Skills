# TCM Diagnosis

## 描述
基于三层架构的中医诊疗智能体，传承《黄帝内经》《伤寒论》等中医经典智慧。
支持四诊采集、八纲辨证、脏腑辨证、经典方剂推荐、食疗养生方案。

⚠️ 所有建议仅供参考学习，不能替代专业医疗诊断和治疗。

## 功能
- **四诊采集**：望闻问切信息采集
- **八纲辨证**：阴阳、表里、寒热、虚实
- **脏腑辨证**：心肝脾肺肾各证型判断
- **方剂推荐**：基于证型推荐经典方剂
- **食疗养生**：体质辨识与食疗方案

## 用法
```bash
# 启动系统
cd ~/tcn-diagnosis
./scripts/startup.sh

# 验证系统
./scripts/verify.sh
```

直接对话使用：
- 说"看病"或"问诊" → 开始四诊采集
- 说"体质" → 九种体质辨识
- 说"食疗"或"养生" → 食疗养生方案

## 架构
```
identity/              # 第一层：身份层
  SOUL.md             # 核心灵魂
  IDENTITY.md         # 角色配置
  USER.md             # 用户画像

operations/            # 第二层：操作层
  AGENTS.md           # 5个诊疗代理
  HEARTBEAT.md        # 安全协议
  ROLE-TCM.md         # 中医师指南

knowledge/             # 第三层：知识层
  symptoms/           # 四诊数据库
  formulas/           # 方剂数据库
  patterns/           # 辨证数据库
  MEMORY.md           # 诊疗经验
```

## 核心知识库
- 100+ 四诊症状条目
- 30+ 经典方剂
- 50+ 辨证模式
- 完整安全警示机制

## 安全声明
⚠️ 本智能体提供的所有中医建议仅供参考学习，不能替代专业医疗诊断和治疗。
- 急重症请立即就医
- 孕妇、婴幼儿特殊人群建议咨询医师
- 用药请咨询执业中医师

## 标签
tcm, traditional-chinese-medicine, diagnosis, herbal-medicine, wellness

## 版本
1.0.0
