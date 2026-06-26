# Prompt 发送前自检 Checklist

> ⚠️ 每次 prompt 写完、发送给 Lovart 之前，必须逐项过一遍。
> 这是防止"生成后才发现问题"的最后一道关卡。

---

## 8 项必检

| # | 检查维度 | 检查内容 | 不通过怎么办 |
|---|---------|---------|-------------|
| 1 | **联想路径检查** | 核心创意是不是"最直线的联想"？（论文→大脑、AI→机器人、编程→代码）如果是，换一条路 | 回到阶段 1 重新想创意 |
| 2 | **文图一致性** | 标题/正文提到的人物、品牌、产品，画面中是否都有对应视觉？ | 补充缺失的视觉元素 |
| 3 | **情绪检查** | 封面传递的情绪是否和帖子一致？是否有引发不适的可能？ | 调整视觉元素或风格 |
| 4 | **文字逐字指定** | prompt 中的标题文字是否逐字写清楚？（不能只说"写标题"） | 补全文字内容 |
| 5 | **禁止项检查** | 是否包含以下禁忌内容？↓ | 删除违规元素 |
| 6 | **AI 生图缺陷预防** | 是否加入了必要的质量约束？↓ | 补充负面提示 |
| 7 | **Logo/品牌精确性** | 品牌 logo 是基于搜索/截图精确描述的？还是凭想象猜的？ | 去搜索确认后再写 |
| 8 | **比例和尺寸** | 是否指定了图片比例？（3:4 竖图 / 1:1 方图） | 补充比例要求 |

---

## 第 5 项：禁止项完整清单

| 禁忌类别 | 具体内容 | 原因 |
|---------|---------|------|
| 裸露器官 | 大脑、心脏、眼球、骨骼、神经网络可视化 | 信息流中引发生理不适 |
| 恐怖/惊悚元素 | 骷髅、血液、裂缝、腐烂、暗黑风格 | 小红书用户群体不接受 |
| 过度写实机械/赛博朋克 | 布满管线的机械脑、赛博眼 | "恐怖谷"效果 |
| 争议性符号 | 特定旗帜、宗教符号、政治元素 | 违规风险 |
| 暴力/武器 | 枪械、刀具、爆炸场景 | 平台违规 |
| 色情/低俗 | 暴露着装、挑逗姿态 | 平台违规 |
| 未经验证的品牌 logo | 凭想象描述的 logo | AI 会胡编 |

---

## 第 6 项：AI 生图常见缺陷预防

在 prompt 末尾加入负面提示（按需选用）：

```
Negative: deformed hands, extra fingers, mutated fingers, bad anatomy,
blurry text, illegible text, misspelled text, garbled characters,
uncanny valley face, plastic skin, cross-eyed, asymmetric eyes,
watermark, signature, low quality, pixelated, oversaturated colors,
generic AI stock photo look, left-right comparison layout
```

---

## Logo/品牌元素精确描述规则

> 这是第3轮的血泪教训。

**禁止凭想象描述 logo！必须：**

1. `web_search "<品牌名> logo icon"` 搜索
2. 在品牌官网截图找到 logo
3. 如果都找不到 → **直接问用户要截图**
4. 用精确的视觉语言描述：形状、颜色、线条、构成元素

**正确示例**：
- ✅ `"a dark circle icon with two white dots arranged like eyes (cute mascot face)"`
- ✅ `"a black circle with white concentric arc lines like sound waves"`

**错误示例**：
- ❌ `"NotebookLM logo"`（AI 不知道长什么样）
- ❌ `"Kimi logo"`（AI 会胡编一个不存在的图形）

---

## 文字逐字指定规则

Lovart 有文字设计能力，但必须明确告诉它每一个字：

**正确**：
```
The exact title text must be: 马斯克点赞的AI论文
Subtitle text: Kimi注意力残差
```

**错误**：
```
Include a title about the paper  ← Lovart 会自由发挥，可能翻译错误
Add Chinese text for the topic   ← 太模糊
```

> 教训：Lovart 曾自行将"Attention Residuals"翻译为"专注力残差"（不准确）。
