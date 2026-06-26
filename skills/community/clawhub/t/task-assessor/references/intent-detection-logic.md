# 意图检测逻辑

## 概述

本模块定义如何将用户原始指令解析为结构化漏洞列表。

## 漏洞类型分类

### 1. 参数缺失 (PARAM_MISSING)

缺少必要参数，无法执行。

```json
{
  "type": "PARAM_MISSING",
  "examples": ["查股价", "分析一下", "帮我整理"]
}
```

**必需字段：**
- `field`: 字段名
- `question`: 提问

### 2. 动词模糊 (VERB_AMBIGUOUS)

动作不明确，可对应多种操作。

```json
{
  "type": "VERB_AMBIGUOUS",
  "examples": ["处理文件", "整理数据", "发出去"]
}
```

**必需字段：**
- `options`: [{"verb": "打开", "action": "open"}, {"verb": "压缩", "action": "compress"}]

### 3. 范围过大 (SCOPE_TOO_LARGE)

范围模糊，需要明确。

```json
{
  "type": "SCOPE_TOO_LARGE",
  "examples": ["整理所有文件", "清理缓存", "分析所有股票"]
}
```

**必需字段：**
- `options`: 数量/类型选项

### 4. 隐含假设 (IMPLIED_ASSUMPTION)

存在未说明的前提假设。

```json
{
  "type": "IMPLIED_ASSUMPTION",
  "examples": ["清空垃圾箱", "关闭后台", "加速一下"]
}
```

**必需字段：**
- `assumption`: 隐含假设
- `options`: 明确后的选项

### 5. 多义名词 (POLYSEMOUS_NOUN)

名词有多种含义。

```json
{
  "type": "POLYSEMOUS_NOUN",
  "examples": ["发出去", "回复", "更新"]
}
```

**必需字段：**
- `options`: 含义选项

## 检测Prompt设计

```
你是一个任务意图分析器。请分析以下用户指令，识别所有信息漏洞。

用户指令：{user_input}

分析要求：
1. 检查是否缺少必要参数
2. 检查动词是否模糊
3. 检查范围是否过大
4. 检查是否有隐含假设
5. 检查是否有歧义名词

输出格式（JSON数组）：
[
  {
    "field": "字段名",
    "type": "PARAM_MISSING|VERB_AMBIGUOUS|SCOPE_TOO_LARGE|IMPLIED_ASSUMPTION|POLYSEMOUS_NOUN",
    "options": ["选项1", "选项2"]（如果适用）,
    "question": "向用户提问的自然语言"
  }
]

如果没有漏洞，返回空数组 []。
```

## 常见任务漏洞清单

### 股票分析类

| 指令示例 | 漏洞 | 补全选项 |
|---------|------|---------|
| "分析茅台" | stock_code | ["600519", "000858"] |
| "查下股价" | stock_code | - |
| "技术分析" | stock_code, time_range | 时间：["1周","1月","3月"] |
| "选股" | criteria | ["低估", "高成长", "低波动"] |

### 文件整理类

| 指令示例 | 漏洞 | 补全选项 |
|---------|------|---------|
| "整理文件" | directory, rule | 规则：["类型", "日期", "大小"] |
| "清理缓存" | target | ["系统缓存", "浏览器缓存", "应用缓存"] |
| "备份一下" | destination, scope | 范围：["全部", "指定文件夹"] |

### 消息发送类

| 指令示例 | 漏洞 | 补全选项 |
|---------|------|---------|
| "发出去" | channel | ["飞书", "邮件", "微信"] |
| "通知他们" | recipients | - |
| "回复" | content, channel | 频道：["当前频道", "原频道"] |

### 数据分析类

| 指令示例 | 漏洞 | 补全选项 |
|---------|------|---------|
| "分析数据" | data_source, analysis_type | 类型：["描述性", "预测性"] |
| "做个报表" | time_range, format | 格式：["Excel", "PDF", "Word"] |
| "对比一下" | targets, metrics | 指标：["收入", "利润", "增长率"] |

## 阈值规则

```javascript
const CLARIFICATION_THRESHOLDS = {
  // 最少几个漏洞才触发澄清
  MIN_VULNERABILITIES: 1,
  
  // 几个以上漏洞启用主动建议模式
  ACTIVE_SUGGESTION_THRESHOLD: 2,
  
  // 缓存有效期（毫秒）
  CACHE_TTL: 10 * 60 * 1000, // 10分钟
  
  // 记忆型澄清连续次数
  MEMORY_CONSECUTIVE_COUNT: 3
};
```

## 不触发情况

以下情况直接放行，不触发澄清：

```javascript
const SKIP_CHANNELS = [
  "heartbeat",      // 心跳检测
  "system",         // 系统消息
  "cron"            // 定时任务触发
];

const SKIP_PATTERNS = [
  /^继续$/,         // 继续执行
  /^取消$/,         // 取消任务
  /^r$/,            // 重置
  /^确认$/          // 确认执行
];
```