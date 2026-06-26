# SPSS 操作指南

常用心理学分析的 SPSS 菜单路径与语法。

## t 检验

### 独立样本 t 检验

**菜单路径：**
分析 → 比较均值 → 独立样本 T 检验
- 检验变量：放入因变量
- 分组变量：放入分组变量 → 定义组（组1、组2）

**输出解读：**
- "组统计"表：每组的 N、平均数、标准差
- "独立样本检验"表：
  - Levene 检验：p > 0.05 则方差齐性假设成立，看第一行；否则看第二行（Welch's t）
  - t 值、自由度、p 值、平均数差值、差异的 95% CI

### 配对样本 t 检验

**菜单路径：**
分析 → 比较均值 → 配对样本 T 检验
- 成对变量：放入两个相关测量变量

**输出解读：**
- "成对样本统计"表：每变量的描述性
- "成对样本检验"表：t 值、自由度、p 值、平均差、95% CI

---

## ANOVA

### 单因素被试间 ANOVA

**菜单路径：**
分析 → 一般线性模型 → 单因素
- 因变量：放入分数变量
- 因子：放入自变量
- 选项：勾选"描述统计"、"效应量"、"方差齐性检验"（Levene）

**输出解读：**
- "描述统计"表：每组 N、平均数、标准误
- "Levene 检验"：p > 0.05 方差齐性成立
- "ANOVA"表：F、df、p、偏 η²

**语法：**
```spss
ONEWAY score BY group (1,3)
  /STATISTICS=DESCRIPTIVES EFFSIZE HOMOGENEITY
  /POSTHOC=TURKEY ALPHA(0.05).
```

### 重复测量 ANOVA

**菜单路径：**
分析 → 一般线性模型 → 重复测量
1. "Within-Subject Factor Name"：输入时间/条件名称（如 time）
2. "Number of Levels"：输入测量次数（如 3）
3. "Measure Name"：输入因变量名称
4. 依次将各水平变量移入 Within-Subject Variables

**选项：**
- 勾选"描述统计"、"效应量"
- 下拉"方差协方差矩阵"选"诊断"检查球形性

**输出解读：**
- Mauchly 球形性检验：p > 0.05 则球形假设成立；否则看 Greenhouse-Geisser 或 Huynh-Feldt校正
- "多变量检验"表（备选）
- "假设检验"表：F、p、偏 η²

### 混合设计 ANOVA（两因素混合）

**菜单路径：**
分析 → 一般线性模型 → 重复测量
- 定义被试内因素（同上）
- 被试间因素：单独放入

**语法：**
```spss
GLM time1 time2 time3 BY group
  /WSFACTOR=time 3
  /MEASURE=score
  /PRINT=DESCRIPTIVES
  /CRITERIA=ALPHA(.05)
  /WSDESIGN=time
  /DESIGN=group.
```

---

## 相关分析

### Pearson / Spearman 相关

**菜单路径：**
分析 → 相关 → 双变量
- 变量：放入两个变量
- 相关系数：Pearson（正态连续）/ Spearman（等级/非正态）
- 显著性：双尾

**输出解读：**
- 相关矩阵：r 值、p 值、N
- 注意：p < 0.05 时 r 标注 *，p < 0.01 标注 **

**语法：**
```spss
CORRELATIONS
  /VARIABLES=var1 var2
  /PRINT=PEARSON SIG TWO-TAIL
  /MISSING=PAIRWISE.
```

---

## 回归分析

### 多元线性回归

**菜单路径：**
分析 → 回归 → 线性
- 因变量：放入 Y
- 自变量：放入 X1 X2 X3...
- 统计：勾选"R 方变化量"、"F 值"、"Descriptives"、"共线性诊断"
- 保存：勾选"预测值"、"残差"

**输出解读：**
- "模型摘要"表：R、R²、调整后 R²
- "ANOVA"表：F、p；检验整体模型显著性
- "系数"表：B（未标准化/标准化）、β、t、p、偏 η²、VIF（< 10 无共线性问题）

**语法：**
```spss
REGRESSION
  /DEPENDENT y
  /METHOD=ENTER x1 x2 x3
  /STATISTICS=R ANOVA COEFF TOL
  /SCATTERPLOT=(*ZRESID, *PRED)
  /RESIDUALS=DURBIN.
```

### 分层回归（调节效应）

**菜单路径：**
同多元回归，逐步加入变量

**步骤：**
1. Model 1：放入控制变量
2. Model 2：加入主效应自变量
3. Model 3：加入交互项（中心化后的乘积）

---

## 中介效应（SPSS + PROCESS 插件）

**安装：** 下载 PROCESS macro（Hayes, 2018），放入 SPSS 安装目录

**菜单路径：**
分析 → 回归 → PROCESS (by Hayes)
- 变量窗口：Y（因变量）、X（自变量）、M（中介变量）
- 模型编号：21（简单中介模型）
- 选项：勾选"显示置信区间"（Bootstrap）

**输出解读：**
- 总效应（c）：X → Y 的总效应
- 直接效应（c'）：X → Y 控制 M 后的效应
- 间接效应（a × b）：Bootstrap CI 不含 0 则显著

**语法（PROCESS 手动）：**
```spss
PROCESS y=y x=x m=m /BOOTSTRAP=5000 /CONF=95.
```

---

## 卡方检验

### 两独立组卡方

**菜单路径：**
分析 → 描述统计 → 交叉表
- 行：放入分组变量
- 列：放入结果变量
- 统计：勾选"卡方"、"Phi 和 Cramér's V"
- 单元格：勾选"期望值"、"行百分比"

**输出解读：**
- "交叉表"：频数与期望频数
- "卡方检验"表：Pearson χ²、df、p、连续性校正（2×2 表时看 Fisher 精确检验）
- "对称度量"表：Cramér's V（效应量）

**语法：**
```spss
CROSSTABS
  /TABLES=group BY outcome
  /STATISTIC=CHISQ
  /CELLS=COUNT EXPECTED ROW
  /FORMAT=NOTABLES.
```

---

## 前提假设检验

### 正态性检验

**菜单路径：**
分析 → 描述统计 → 探索
- 因变量列表：放入检验变量
- 绘制：勾选"带检验的正态图"
- 统计：勾选"描述统计"

**输出解读：**
- "描述统计"表：偏度、峰度
- "正态性检验"表：Kolmogorov-Smirnov 和 Shapiro-Wilk，p > 0.05 则正态

### 方差齐性检验

**菜单路径：**
分析 → 描述统计 → 探索
- 因子列表：放入分组变量
- 绘制 → 箱图：选"按组拆分"
- 选项：勾选"描述统计"

**替代：** ANOVA 的"选项"中 Levene 检验

### 球形性检验

在重复测量 ANOVA 输出中自动包含（"Mauchly's Test of Sphericity"）

---

## 结果报告模板（APA 格式）

### 独立样本 t 检验
```
对 [自变量] 在 [因变量] 上的得分进行独立样本 t 检验。结果表明，实验组（M = [M], SD = [SD]）与对照组（M = [M], SD = [SD]）在 [因变量] 上存在显著差异，t([df]) = [t值], p = [p值], Cohen's d = [d值]。
```

### 重复测量 ANOVA
```
对 [因变量] 进行 3（时间）× 2（组别）的混合设计方差分析。时间主效应显著，F([df1], [df2]) = [F值], p = [p值], η² = [η²]。组别主效应 [不] 显著，交互效应 [不] 显著。
```

### Pearson 相关
```
[变量1] 与 [变量2] 呈显著正/负相关，r([df]) = [r值], p = [p值]。
```
