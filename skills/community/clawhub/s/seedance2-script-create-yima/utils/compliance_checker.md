# 广告合规检查工具

这是一个用于检查广告内容是否符合中国广告法规的工具。

## 功能特性

- 违禁词自动检测和替换
- 特殊行业合规检查
- 广告内容安全验证
- 批量处理支持

## 使用方法

### 基本检查

```bash
python compliance_checker.py --input "广告文案内容" --category "产品类别"
```

### 批量检查

```bash
python compliance_checker.py --file input.txt --output checked.txt --category "FMCG"
```

### 参数说明

- `--input`: 直接输入要检查的广告文案
- `--file`: 指定包含广告文案的文件
- `--output`: 输出检查结果的文件
- `--category`: 产品类别 (electronics, fmcg, health, etc.)
- `--strict`: 启用严格检查模式

## 检查规则

### 违禁词列表
- **一级违禁词**：国家级、最高级、最佳、第一、唯一、首个、首选、顶级、极品、终极、独一无二、绝无仅有、史无前例、万能、永久、永远、领袖品牌、世界领先、领导者、王者、全球第一、宇宙级、现象级、爆款、网红、超级、巨无霸、神器、黑科技、革命性、颠覆性
- **二级限制词**：最优、最新、最先进、最大、最小、最强、最全、最便宜、最划算、100%、百分百、零风险、无效退款、保证治愈、根治、药到病除、智能、AI驱动、区块链技术、元宇宙体验、Web3应用、NFT资产、虚拟现实、增强现实
- **医疗承诺用词**：治疗、治愈、根除、预防疾病、药到病除、保证治愈等
- **价格承诺用词**：最低价、跳楼价、清仓、血亏等

### 特殊行业规则
- 健康产品：禁止医疗诊断承诺
- 食品饮料：必须标注食品安全信息
- 房地产：必须标注产权信息
- 母婴产品：必须标注适用年龄范围

## 输出格式

检查结果以JSON格式输出：

```json
{
  "original_text": "原始文案",
  "checked_text": "检查后文案",
  "violations": [
    {
      "word": "违禁词",
      "type": "违禁类型",
      "suggestion": "建议替换"
    }
  ],
  "compliance_score": 85,
  "passed": true
}
```

## 依赖项

- Python 3.8+
- jieba (中文分词)
- opencc (简繁转换)

## 安装

```bash
pip install jieba opencc-python-reimplemented
```

## 示例

```python
from compliance_checker import AdComplianceChecker

checker = AdComplianceChecker()
result = checker.check("这款产品绝对能让你年轻10岁！", category="beauty")

print(result['passed'])  # False
print(result['violations'])  # 违禁词列表
```