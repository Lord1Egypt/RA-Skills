# IEEE期刊投稿风格指南

> IEEE Journal Submission Style Guide

---

## 一、期刊定位

IEEE是**工程技术领域**顶级出版机构，旗下期刊涵盖：
- 计算机科学
- 电子工程
- 通信技术
- 自动化控制

**写作原则**：精确、正式、方法导向

---

## 二、文章结构

### 标准结构

| 部分 | 内容 |
|------|------|
| Abstract | ≤150词，非结构化 |
| Introduction | 背景、目的、贡献 |
| Related Work | 文献综述 |
| Proposed Method | 方法描述（核心） |
| Experiments | 实验设计 |
| Results | 实验结果 |
| Discussion | 分析讨论 |
| Conclusion | 总结与展望 |
| References | 参考文献 |

---

## 三、写作风格

### 语言特点

| 特点 | 说明 |
|------|------|
| **被动语态可接受** | The data were collected... |
| **正式** | 避免口语化表达 |
| **精确** | 技术术语准确使用 |
| **方法导向** | 详细描述方法步骤 |

---

### 标题风格

| ❌ 差 | ✅ 好 |
|-------|-------|
| A deep learning approach for X | A Deep Learning-Based Approach for X |
| Study of X | X: Methodology and Applications |

**原则**：
- 技术术语大写
- 不要太长
- 说明方法或应用

---

### 摘要风格

**结构**：
```
[问题背景]. [现有方法局限]. [本文提出的方法]. 
[方法特点]. [实验结果]. [结论].
```

**示例**：
```
Deep learning has achieved remarkable success in image 
classification. However, existing methods often require 
large amounts of labeled data. This paper proposes a 
semi-supervised learning approach that leverages unlabeled 
data. The proposed method combines self-training with 
consistency regularization. Experiments on three benchmark 
datasets demonstrate that our method achieves 95% accuracy 
with only 10% labeled data, outperforming existing 
approaches by 8%. The results validate the effectiveness 
of semi-supervised learning for data-scarce scenarios.
```

---

### 方法部分

**IEEE期刊特别重视方法部分**：
- 详细描述算法步骤
- 提供伪代码
- 说明参数设置
- 分析计算复杂度

**伪代码格式**：
```
Algorithm 1: Proposed Method
Input: Dataset D, Parameters θ
Output: Model M
1: Initialize M with random weights
2: for epoch = 1 to E do
3:     for each batch B in D do
4:         Update M using gradient descent
5:     end for
6: end for
7: return M
```

---

## 四、图表要求

### 图片要求

| 项目 | 要求 |
|------|------|
| 格式 | TIFF, EPS, PS, PDF |
| 分辨率 | ≥300 dpi |
| 宽度 | 单栏3.5英寸，双栏7.16英寸 |
| 字体 | Times New Roman, 8-10pt |

### 表格要求

- 使用罗马数字编号（Table I, Table II）
- 标题在表格上方
- 简洁，避免过多线条

---

## 五、参考文献格式

### 正文引用

使用数字编号：[1], [2], [3] 或 [1]-[3]

### 参考文献列表

```
期刊文章：
[1] A. Author and B. Author, "Title of article," Title of Journal, 
vol. X, no. Y, pp. xx-xx, Year.

会议论文：
[2] A. Author, "Title of paper," in Proc. Conference Name, 
City, Country, Year, pp. xx-xx.

示例：
[1] J. Smith and M. Johnson, "Deep learning for medical diagnosis," 
IEEE Trans. Med. Imaging, vol. 15, no. 3, pp. 234-256, 2020.
```

**特点**：
- 使用标准期刊缩写（如 IEEE Trans. Med. Imaging）
- 作者名只写首字母
- 标题用引号

---

## 六、常见拒稿原因

| 原因 | 解决方案 |
|------|----------|
| 方法描述不清 | 详细描述步骤，提供伪代码 |
| 缺少对比实验 | 与多个基线方法对比 |
| 数据集描述不全 | 说明数据来源、规模、划分 |
| 相关工作不足 | 补充文献综述 |
| 创新点不明确 | 在Introduction中明确贡献 |

---

## 七、投稿检查清单

- [ ] 摘要≤150词
- [ ] 方法部分详细，有伪代码
- [ ] 实验与多个基线对比
- [ ] 图表格式符合要求
- [ ] 参考文献使用IEEE格式
- [ ] 期刊名使用标准缩写
- [ ] 被动语态可接受但不过度

---

## 八、官方资源

- **投稿指南**：https://ieeeauthorcenter.ieee.org/
- **格式模板**：https://www.ieee.org/conferences/publishing/templates.html

---

**更新时间**：2026-04-09
