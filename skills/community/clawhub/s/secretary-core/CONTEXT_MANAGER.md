# 🧠 语境管理模块

**版本：** 1.0.0  
**功能：** 对话历史/用户偏好/场景识别

---

## 📚 对话历史管理

### 短期记忆（工作记忆）
```python
class ShortTermMemory:
    capacity = 10  # 最近 10 轮对话
    ttl = 3600     # 1 小时过期
    
    def add(self, turn):
        self.buffer.append(turn)
        if len(self.buffer) > self.capacity:
            self.buffer.popleft()
    
    def get_recent(self, n=5):
        return list(self.buffer)[-n:]
```

### 长期记忆（永久存储）
```python
class LongTermMemory:
    storage = "SQLite"
    
    def store(self, memory):
        # 重要信息永久存储
        db.execute(
            "INSERT INTO memories VALUES (?, ?, ?)",
            (memory.content, memory.timestamp, memory.tags)
        )
    
    def retrieve(self, query):
        # 语义搜索
        return db.search(query)
```

---

## 👤 用户偏好学习

### 偏好类型
| 类型 | 示例 | 学习方式 |
|------|------|---------|
| **沟通风格** | 简洁/详细 | 观察响应反馈 |
| **工作时间** | 9:00-18:00 | 行为模式分析 |
| **优先级习惯** | 邮件优先/电话优先 | 行为统计 |
| **表达习惯** | 正式/随意 | 语言分析 |
| **常用功能** | 会议/邮件/提醒 | 使用频率统计 |

### 偏好更新
```python
class PreferenceLearner:
    def update(self, user_action, feedback):
        if feedback == "positive":
            self.preferences[user_action] += 0.1
        elif feedback == "negative":
            self.preferences[user_action] -= 0.1
        
        # 归一化
        self.normalize()
```

---

## 🎭 场景识别

### 工作场景
**特征：** 工作词汇、正式语气、工作时间
**响应策略：** 专业、高效、简洁
**示例功能：**
- 会议安排
- 邮件处理
- 报告生成
- 日程管理

### 生活场景
**特征：** 生活词汇、随意语气、非工作时间
**响应策略：** 亲切、贴心、主动
**示例功能：**
- 日常提醒
- 购物清单
- 健康管理
- 旅行规划

### 社交场景
**特征：** 社交词汇、情感表达、人际关系
**响应策略：** 情商高、会来事、有温度
**示例功能：**
- 消息回复建议
- 礼物推荐
- 活动安排
- 关系维护

---

## 🔗 关系感知

### 关系类型
| 关系 | 特征 | 响应策略 |
|------|------|---------|
| **上级** | 命令语气、工作安排 | 尊重、执行、汇报 |
| **同事** | 商量语气、协作 | 平等、配合、支持 |
| **客户** | 询问语气、需求 | 专业、耐心、服务 |
| **朋友** | 随意语气、情感 | 轻松、真诚、关心 |
| **家人** | 亲密语气、日常 | 温暖、体贴、照顾 |

### 关系识别
```python
def recognize_relationship(text, user_history):
    cues = {
        "superior": ["安排", "去", "立即", "任务"],
        "colleague": ["一起", "帮忙", "协作", "我们"],
        "client": ["咨询", "需求", "服务", "贵司"],
        "friend": ["哈", "啦", "～", "嘿嘿"],
        "family": ["记得", "别忘", "关心", "爱"]
    }
    
    for relation, keywords in cues.items():
        if any(kw in text for kw in keywords):
            return relation
    
    return "unknown"
```

---

## 💡 应用示例

### 场景切换
```
[工作场景 15:00]
用户：下午有什么安排？
秘书：您下午 14:00 有项目评审会📍，16:00 与客户会议📍。

[生活场景 20:00]
用户：晚上有什么安排？
秘书：今晚没有安排哦～ 可以好好休息，或者看个电影🎬？
```

### 关系感知
```
[对上级]
用户：立即准备会议材料
秘书：好的，马上准备📋。请问需要哪些内容？

[对同事]
用户：帮我看看这个方案
秘书：没问题👌。我觉得这里可以优化一下...

[对客户]
用户：这个功能怎么实现
秘书：您好😊。这个功能可以通过...实现。
```

---

**状态：** ✅ 设计完成  
**实现：** 迭代 2 完成
