# Truth (求真) - AI事实核查技能

## 简介

AI Content Authenticity Verification Tool.
事实核查技能，6层深度核查（含区块链存证验证），**元认知置信度输出**，**维度权重可配置**，**支持可选定时核查**，识别AI幻觉、虚假信息，输出可信度评分和问题标注。完美适配2核2G环境，100%隐私保护。可简称truth/qiuzhen使用。

## 功能

- ✅ 识别AI生成幻觉内容
- ✅ 识别虚假信息和夸大宣传
- ✅ 输出0-10可信度评分
- ✅ **v1.5.0新增：元认知置信度输出**，模型告诉你对结论的确定程度（0-100%）
- ✅ **v1.5.0新增：维度权重可配置**，自定义各维度权重，按需开关维度
- ✅ **v1.5.0新增：可选定时核查**，默认关闭，配置后自动定时核查，变化超过阈值告警，适配2核2G资源约束
- ✅ 标注问题句子，给出具体位置和原因
- ✅ 提供改进建议
- ✅ 区块链存证验证，验证公开链上内容哈希
- ✅ 多数据源fallback，自动切换可用源
- ✅ 评分维度明细输出，更透明
- ✅ 适配2核2G环境，最大并发=2，不占用过多资源
- ✅ 合规拦截敏感内容
- ✅ **100%隐私保护**：所有核查本地运行，不上传任何内容到外部服务器

## 隐私保护承诺

> Truth (求真) 严格保护您的隐私：
> 1.  本技能完全运行在您自己的OpenClaw实例中，所有您核查的内容**不会上传到任何外部服务器/开发者服务器**，完全本地处理
> 2.  本技能不收集、不存储、不分享任何您的核查内容、个人数据
> 3.  所有功能均离线可用，不需要联网除了您本身模型需要的API调用（模型服务商按其隐私政策处理，本技能不转发数据
> 4.  开源可审计，代码完全开放，任何人可以验证隐私保护实现

## 安装

```
clawhub install tangtaozhanshen/truth-seeking-fact-check
```

## 使用

### 基础示例

```python
from truth.main import TruthSkill
import json

# 初始化
checker = TruthSkill()

# 单篇文本核查
text = "地球是太阳系第三颗行星，围绕太阳公转。"
result = checker.check_text(text, output_format="json")
result_json = json.loads(result)

print(f"可信度评分: {result_json['credibility_score']}/10")
print(f"模型元认知置信度: {result_json['meta_confidence']}%")
print(f"结论: {result_json['conclusion']}")
print(f"问题句子: {result_json['problematic_sentences']}
```

### 自定义维度权重示例

```python
from truth.main import TruthSkill

# 初始化，可在配置中指定维度权重
config = {
    "dimension_weights": {
        "来源匹配度": 0.5,
        "逻辑一致性": 0.2,
        "常识符合度": 0.2,
        "信息明确性": 0.1
    }
}
checker = TruthSkill(config)

# 或者单次核查指定权重
result = checker.check_text(text, weights={
    "来源匹配度": 0.6,
    "逻辑一致性": 0.2,
    "常识符合度": 0.15,
    "信息明确性": 0.05
})
```

### 开启定时核查示例

```python
from truth.main import TruthSkill

# 初始化配置，开启定时调度
config = {
    "scheduler": {
        "interval_hours": 24,        # 默认每天一次，最小24小时
        "max_tasks": 10,             # 最大10个任务，控制资源
        "alert_threshold": 2,        # 分数变化超过2分才告警
        "max_concurrency": 2         # 最大并发，适配2核2G
    }
}
checker = TruthSkill(config)

# 启动定时调度
checker.start_scheduler()

# 添加定时核查任务
result = checker.add_timed_check("需要定期核查的文本", callback=my_alert_callback)
```

### 批量核查示例

## 安装

```
clawhub install tangtaozhanshen/truth-seeking-fact-check
```

## 使用

### 基础示例

```python
from truth.main import TruthSkill
import json

# 初始化
checker = TruthSkill()

# 单篇文本核查
text = "地球是太阳系第三颗行星，围绕太阳公转。"
result = checker.check_text(text, output_format="json")
result_json = json.loads(result)

print(f"可信度评分: {result_json['credibility_score']}/10")
print(f"结论: {result_json['conclusion']}")
print(f"问题句子: {result_json['problematic_sentences']}")
```

### 批量核查示例

```python
from truth.main import TruthSkill

checker = TruthSkill()
texts = [
    "水的化学式是 H2O",
    "OpenClaw 是 Google 开发的 AI 框架"
]
result = checker.check_batch(texts, output_format="json")
print(result)
```

### 区块链存证验证示例

```python
from truth.main import TruthSkill

checker = TruthSkill()
# 文本包含 #blockchain:URL 格式会自动触发验证
text = "这则消息已上链存证 #blockchain:https://etherscan.io/tx/0x..."
result = checker.check_text(text)
print(result)
```

### OpenClaw 技能调用示例

```json
{
  "skill": "truth-seeking-fact-check",
  "params": {
    "text": "需要核查的文本内容"
  }
}
```

## 作者

tangtaozhanshen

## 许可

MIT-0

## 链接

<https://clawhub.ai/tangtaozhanshen/truth-seeking-fact-check>
