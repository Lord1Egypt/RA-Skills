# Paper Reader Skill 使用示例

## 使用方式

### 方式1：斜杠命令（推荐，最快）

```
/readpaper                              # 启动交互式流程
/readpaper D:\\papers\\paper.pdf              # 直接分析本地PDF
/readpaper https://arxiv.org/abs/xxx    # 直接分析在线论文
```

### 方式2：自然语言

```
"帮我读这篇论文"
"总结这篇文献"
"分析这篇论文"
```

## 示例对话

### 示例 1：斜杠命令 + 本地文件（最快）

**用户**：`/readpaper D:\\papers\\attention_is_all_you_need.pdf`

**助手**：
1. 立即读取并分析论文
2. 提取标题：`Attention Is All You Need`
3. 生成文件名：`Attention Is All You Need_阅读报告.md`
4. 保存报告到工作区目录
5. 向用户确认：

```
✓ 论文阅读报告已生成
📄 文件名：Attention Is All You Need_阅读报告.md
📁 保存位置：D:\papers\
```

---

### 示例 2：斜杠命令 + 在线论文

**用户**：`/readpaper https://arxiv.org/abs/1706.03762`

**助手**：立即获取并分析论文，直接生成报告...

---

### 示例 3：仅斜杠命令（交互式）

**用户**：`/readpaper`

**助手**：请提供论文路径或链接：

**用户**：`D:\\papers\\paper.pdf`

**助手**：开始分析...

---

### 示例 4：自然语言 + 本地PDF

**用户**：帮我读这篇论文，文件在 `D:\\papers\\attention_is_all_you_need.pdf`

**助手**：
1. 读取PDF文件内容
2. 提取论文信息
3. 生成结构化报告...

---

### 示例 5：直接上传

**用户**：帮我总结这篇论文 [上传PDF文件]

**助手**：
1. 接收上传的文件
2. 分析论文内容
3. 生成完整报告

## 报告输出示例

```markdown
# 论文阅读报告

## 基本信息
- **标题**：Attention Is All You Need
- **作者**：Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin
- **单位**：Google Brain, Google Research
- **发表**：NIPS 2017
- **DOI**：-

## 摘要总结
本文提出了Transformer模型，完全基于注意力机制，摒弃了RNN和CNN。在机器翻译任务上取得了SOTA效果，同时训练速度大幅提升。

## 背景介绍
### 研究领域
自然语言处理 - 机器翻译

### 研究动机
RNN序列模型计算效率低，难以并行化。LSTM和GRU虽然缓解了梯度消失，但长距离依赖仍是问题。

### 本文贡献
提出纯注意力架构，实现全局依赖建模和高效并行计算。

## 图表分析

### Figure 1: The Transformer - model architecture
- **类型**：架构图
- **内容**：展示Transformer的编码器-解码器结构
- **关键信息**：
  - 左侧：N层编码器，每层包含多头注意力和前馈网络
  - 右侧：N层解码器，额外包含编码器-解码器注意力
  - 使用残差连接和层归一化
- **支撑论点**：说明Transformer的整体架构设计

### Figure 2: (left) Scaled Dot-Product Attention. (right) Multi-Head Attention
- **类型**：机制示意图
- **内容**：注意力机制的计算过程
- **关键信息**：
  - 左图：Q、K、V的计算，缩放因子√d_k
  - 右图：多头注意力的并行计算和拼接
- **支撑论点**：解释核心注意力机制的实现细节

## 论文总结

### 论文逻辑
引言指出现有序列模型的局限性→提出注意力机制解决方案→详细介绍Transformer架构→实验验证→结论

### 核心创新点
1. 完全基于注意力，无需RNN/CNN
2. 多头注意力机制捕获不同子空间信息
3. 位置编码引入序列顺序信息

### 分析方法
#### 研究方法
基于自注意力的编码器-解码器架构

#### 实验设计
在WMT英德和英法翻译任务上验证

#### 评估指标
BLEU分数

### 主要结论
Transformer在翻译任务上达到SOTA，训练速度显著快于RNN模型。

### 局限性与展望
- 对长文档处理可能需要优化
- 未来可应用于其他NLP任务
```
