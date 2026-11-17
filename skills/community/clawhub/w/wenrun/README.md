# 文润 (WenRun) — 中文AI文本自然度检测工具

检测并消除中文AI文本的模板化痕迹，让文字更像人写的。

## 快速开始

```bash
# 分析文本
python3 scripts/wenrun.py analyze --text "要检测的文章内容..."

# 分析文件
python3 scripts/wenrun.py analyze --file article.txt

# 详细模式
python3 scripts/wenrun.py analyze --file article.txt --verbose

# 指定文体模式
python3 scripts/wenrun.py analyze --file article.txt --style academic

# JSON 输出
python3 scripts/wenrun.py analyze --file article.txt --json

# 查看特征库状态
python3 scripts/wenrun.py check
```

## 文体模式

| 模式 | 适用场景 | 说明 |
|------|---------|------|
| auto | 自动检测 | 根据文本特征自动判断文体（默认） |
| academic | 学术/正式写作 | 论文、研究报告、教材等，结构化表达不视为AI特征 |
| casual | 日常/自媒体 | 公众号、博客、日常对话，模板化套话会扣分 |
| marketing | 营销/推广 | 广告文案、产品介绍，套话是强烈AI信号 |

## 输出示例

```
═══════════════════════════════════════════════
  文润 (WenRun) v1.0.1 — AI文本自然度检测
  输入长度: 1520 字
═══════════════════════════════════════════════

  文体模式: casual
  结论: 疑似AI — 有多处AI文本特征

  ── 维度评分 ──
  ⚠ AI高频套话     65/100 ██████░ (4项)
  ⚠ 模板化结构     72/100 ███████░ (3项)
  ⚠ 生硬过渡词     78/100 ███████░ (2项)
  ✓ 段落结构异常   85/100 ████████░ (1项)
  ✓ 句式单一化     90/100 █████████░ (1项)

  ── 发现问题 (11 处) ──
  [高] 在这个日新月异的时代
       → AI开篇金句，人类几乎不这样写
  [高] 随着科技的不断发展
       → AI万能开场白
  [中] 首先 ... 其次 ... 最后
       → 三段式AI模板
  ...

═══════════════════════════════════════════════
  免责声明: 本工具分析仅供参考，不构成对AI检测结果的保证。
```

## 效果案例

### 案例 1：AI 范文（含大量套话）

输入：一篇典型的 AI 生成文章，包含"在这个日新月异的时代"、"随着科技的不断发展"、"首先/其次/最后"三段式结构。

输出：**评分 ~61/100，结论：疑似AI**

### 案例 2：日常对话

输入：一段真实的朋友圈日常分享。

输出：**评分 ~99/100，结论：非常自然**

### 案例 3：学术论文（7万字）

输入：智本论卷一（7万字学术文本）。

输出：**评分 ~87/100，结论：基本自然**（学术模式下结构化表达不扣分）

## 特征库

当前版本内置 **8 大类 60+ 条** 中文 AI 文本特征规则：

| 类别 | 权重 | 说明 |
|------|------|------|
| TEMPLATE_STRUCTURE | 18 | 模板化结构（首先/其次/最后等） |
| TRANSITION | 15 | 生硬过渡词（综上所述/毋庸置疑等） |
| BUZZWORD | 28 | AI高频套话（在这个日新月异的时代等） |
| EXCESSIVE_POLITE | 10 | 过度礼貌（非常荣幸/竭诚为您等） |
| PARAGRAPH_STRUCTURE | 15 | 段落结构异常（长度趋同） |
| SYNTAX | 10 | 句式单一化（的密度/这字句等） |
| MOOD | 10 | 语气与情感缺陷（缺少反问/口语） |
| DATA_DESCRIPTION | 10 | 数据化表达机械（从数据可以看出等） |
| ENGLISH_MIX | 5 | 英文表达中式化（作为之一/被...所等） |

详见 [features/ai-patterns.json](features/ai-patterns.json)。

## 依赖

- Python 3.8+
- 纯标准库，无外部依赖

## 法律声明

**重要声明：**
1. **仅供参考**：本工具的分析结果和建议仅供参考，不构成对 AI 检测结果的保证。
2. **非保证**：本工具无法保证 100% 准确识别 AI 生成文本，存在误报和漏报的可能。
3. **用户责任**：最终内容质量和使用责任由用户自行承担。
4. **持续迭代**：AI 文本特征不断变化，本工具的特征库将持续更新。

**Disclaimer (English):**
1. **For Reference Only**: Analysis results and suggestions are for reference only and do not guarantee AI detection accuracy.
2. **No Guarantee**: This tool cannot guarantee 100% accuracy in identifying AI-generated text.
3. **User Responsibility**: The ultimate responsibility for content quality and use rests with the user.
4. **Continuous Updates**: AI text patterns evolve; this tool's feature library will be updated accordingly.
