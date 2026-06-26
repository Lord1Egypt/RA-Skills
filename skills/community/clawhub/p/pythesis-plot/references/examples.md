# 代码示例集

本文件提供 PyThesisPlot 的完整代码示例，涵盖常见科研图表场景。

## 目录

- [基础示例](#基础示例)
- [进阶示例](#进阶示例)
- [论文场景示例](#论文场景示例)
- [完整模板](#完整模板)

---

## 基础示例

### 示例1：最简单的科研图表

```python
import matplotlib.pyplot as plt
import numpy as np

# 设置科研样式
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 绘图
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, linewidth=2, color='#2E5AAC')
ax.set_xlabel('X轴', fontsize=12)
ax.set_ylabel('Y轴', fontsize=12)
ax.set_title('正弦波', fontsize=14)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simple.pdf', bbox_inches='tight', dpi=300)
```

### 示例2：多子图布局

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

x = np.linspace(0, 10, 100)

# 子图1
axes[0, 0].plot(x, np.sin(x), color='#2E5AAC')
axes[0, 0].set_title('正弦波')
axes[0, 0].grid(True, alpha=0.3)

# 子图2
axes[0, 1].plot(x, np.cos(x), color='#5CB85C')
axes[0, 1].set_title('余弦波')
axes[0, 1].grid(True, alpha=0.3)

# 子图3
axes[1, 0].plot(x, np.tan(x), color='#F0AD4E')
axes[1, 0].set_title('正切波')
axes[1, 0].set_ylim(-5, 5)
axes[1, 0].grid(True, alpha=0.3)

# 子图4
axes[1, 1].plot(x, np.exp(-x/5), color='#D9534F')
axes[1, 1].set_title('指数衰减')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('subplots.pdf', bbox_inches='tight', dpi=300)
```

---

## 进阶示例

### 示例3：带误差线的图表

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

x = np.arange(1, 6)
y = [10, 15, 13, 18, 16]
error = [1, 2, 1.5, 2.5, 1.8]

fig, ax = plt.subplots(figsize=(7, 5))
ax.errorbar(x, y, yerr=error, fmt='o-', linewidth=2, 
            markersize=8, capsize=5, color='#2E5AAC',
            ecolor='#D9534F', capthick=2)

ax.set_xlabel('实验组', fontsize=12)
ax.set_ylabel('测量值', fontsize=12)
ax.set_title('带误差线的实验结果', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('errorbar.pdf', bbox_inches='tight', dpi=300)
```

### 示例4：双Y轴图表

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

x = np.arange(1, 11)
y1 = np.random.randint(50, 100, 10)
y2 = np.random.randint(1000, 5000, 10)

fig, ax1 = plt.subplots(figsize=(8, 5))

color1 = '#2E5AAC'
ax1.bar(x, y1, color=color1, alpha=0.7, label='数量')
ax1.set_xlabel('时间 (月)', fontsize=12)
ax1.set_ylabel('数量', fontsize=12, color=color1)
ax1.tick_params(axis='y', labelcolor=color1)

ax2 = ax1.twinx()
color2 = '#D9534F'
ax2.plot(x, y2, color=color2, marker='o', linewidth=2, label='金额')
ax2.set_ylabel('金额 (元)', fontsize=12, color=color2)
ax2.tick_params(axis='y', labelcolor=color2)

fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.95))
ax1.set_title('双Y轴示例', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('twinx.pdf', bbox_inches='tight', dpi=300)
```

### 示例5：带标注的图表

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, linewidth=2, color='#2E5AAC')

# 标注最大值
max_idx = np.argmax(y)
ax.annotate(f'最大值: ({x[max_idx]:.2f}, {y[max_idx]:.2f})',
            xy=(x[max_idx], y[max_idx]),
            xytext=(x[max_idx]+1, y[max_idx]+0.3),
            arrowprops=dict(arrowstyle='->', color='#D9534F'),
            fontsize=10, color='#D9534F')

# 标注最小值
min_idx = np.argmin(y)
ax.annotate(f'最小值: ({x[min_idx]:.2f}, {y[min_idx]:.2f})',
            xy=(x[min_idx], y[min_idx]),
            xytext=(x[min_idx]+1, y[min_idx]-0.3),
            arrowprops=dict(arrowstyle='->', color='#5CB85C'),
            fontsize=10, color='#5CB85C')

ax.set_xlabel('X轴', fontsize=12)
ax.set_ylabel('Y轴', fontsize=12)
ax.set_title('带标注的图表', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('annotation.pdf', bbox_inches='tight', dpi=300)
```

---

## 论文场景示例

### 示例6：实验结果对比图

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

methods = ['方法A', '方法B', '方法C', '方法D', '方法E']
accuracy = [0.85, 0.88, 0.92, 0.90, 0.87]
precision = [0.83, 0.86, 0.91, 0.89, 0.85]
recall = [0.87, 0.89, 0.93, 0.91, 0.88]

x = np.arange(len(methods))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width, accuracy, width, label='准确率', color='#2E5AAC')
bars2 = ax.bar(x, precision, width, label='精确率', color='#5CB85C')
bars3 = ax.bar(x + width, recall, width, label='召回率', color='#F0AD4E')

ax.set_xlabel('方法', fontsize=12)
ax.set_ylabel('分数', fontsize=12)
ax.set_title('不同方法的性能对比', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(methods)
ax.legend(loc='best')
ax.set_ylim(0, 1.0)
ax.yaxis.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('comparison.pdf', bbox_inches='tight', dpi=300)
```

### 示例7：学习曲线

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

epochs = np.arange(1, 101)
train_loss = 1 / (epochs * 0.05) + 0.1 + np.random.randn(100) * 0.02
val_loss = 1 / (epochs * 0.04) + 0.15 + np.random.randn(100) * 0.02

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(epochs, train_loss, label='训练损失', linewidth=2, color='#2E5AAC')
ax.plot(epochs, val_loss, label='验证损失', linewidth=2, color='#D9534F')

# 标记最佳epoch
best_epoch = np.argmin(val_loss)
ax.axvline(x=best_epoch, color='#5CB85C', linestyle='--', alpha=0.7)
ax.scatter([best_epoch], [val_loss[best_epoch]], color='#5CB85C', s=100, zorder=5)
ax.annotate(f'最佳: Epoch {best_epoch}', 
            xy=(best_epoch, val_loss[best_epoch]),
            xytext=(best_epoch+10, val_loss[best_epoch]+0.1),
            fontsize=10, color='#5CB85C')

ax.set_xlabel('训练轮次', fontsize=12)
ax.set_ylabel('损失', fontsize=12)
ax.set_title('模型训练学习曲线', fontsize=14, fontweight='bold')
ax.legend(loc='best')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('learning_curve.pdf', bbox_inches='tight', dpi=300)
```

### 示例8：混淆矩阵

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 混淆矩阵数据
confusion = np.array([[85, 5, 3, 2],
                      [4, 88, 4, 4],
                      [2, 3, 90, 5],
                      [3, 4, 5, 88]])

classes = ['类别A', '类别B', '类别C', '类别D']

fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(confusion, cmap='Blues')

# 添加颜色条
cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label('样本数', fontsize=11)

# 设置刻度
ax.set_xticks(np.arange(len(classes)))
ax.set_yticks(np.arange(len(classes)))
ax.set_xticklabels(classes)
ax.set_yticklabels(classes)
ax.set_xlabel('预测标签', fontsize=12)
ax.set_ylabel('真实标签', fontsize=12)
ax.set_title('混淆矩阵', fontsize=14, fontweight='bold')

# 在每个格子中显示数值
for i in range(len(classes)):
    for j in range(len(classes)):
        text = ax.text(j, i, confusion[i, j],
                      ha="center", va="center", 
                      color="white" if confusion[i, j] > 50 else "black",
                      fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('confusion_matrix.pdf', bbox_inches='tight', dpi=300)
```

### 示例9：ROC曲线

```python
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 生成模拟数据
np.random.seed(42)
n_samples = 1000
y_true = np.random.randint(0, 2, n_samples)
y_scores = np.random.rand(n_samples)

# 计算ROC曲线
fpr, tpr, _ = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)

fig, ax = plt.subplots(figsize=(7, 6))
ax.plot(fpr, tpr, linewidth=2, color='#2E5AAC', 
        label=f'ROC曲线 (AUC = {roc_auc:.3f})')
ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='随机猜测')

ax.set_xlabel('假正率 (False Positive Rate)', fontsize=12)
ax.set_ylabel('真正率 (True Positive Rate)', fontsize=12)
ax.set_title('ROC曲线', fontsize=14, fontweight='bold')
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3)
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])

plt.tight_layout()
plt.savefig('roc_curve.pdf', bbox_inches='tight', dpi=300)
```

---

## 完整模板

### 论文图表完整模板

```python
#!/usr/bin/env python3
"""
论文图表完整模板
包含：样式设置、数据绘图、图例、导出
"""

import matplotlib.pyplot as plt
import numpy as np

# ==================== 配置 ====================
# 中文字体设置
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 全局样式设置
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 6

# ==================== 数据 ====================
np.random.seed(42)
x = np.linspace(0, 10, 100)
y1 = np.sin(x) + np.random.randn(100) * 0.1
y2 = np.cos(x) + np.random.randn(100) * 0.1

# ==================== 绘图 ====================
# 创建图形
fig, ax = plt.subplots(figsize=(7, 5))

# 配色方案
colors = ['#2E5AAC', '#D9534F']

# 绘制数据
ax.plot(x, y1, color=colors[0], linewidth=2, 
        label='方法A', marker='o', markevery=10)
ax.plot(x, y2, color=colors[1], linewidth=2, 
        label='方法B', marker='s', markevery=10, linestyle='--')

# 设置标签
ax.set_xlabel('时间 (s)', fontsize=12)
ax.set_ylabel('信号强度', fontsize=12)
ax.set_title('实验结果对比', fontsize=14, fontweight='bold')

# 图例
ax.legend(loc='best', frameon=True, fancybox=True, shadow=False)

# 网格
ax.grid(True, linestyle='--', alpha=0.3)

# 调整布局
plt.tight_layout()

# ==================== 导出 ====================
# 矢量图（LaTeX）
plt.savefig('figure.pdf', bbox_inches='tight', dpi=300)

# 位图（Word）
plt.savefig('figure.png', bbox_inches='tight', dpi=300, 
            facecolor='white', edgecolor='none')

print("✓ 图表已导出: figure.pdf, figure.png")
```

### LaTeX 集成模板

```python
#!/usr/bin/env python3
"""
LaTeX 论文图表模板
使用 pgf 后端直接生成 LaTeX 可用的图表
"""

import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt
import numpy as np

# LaTeX 配置
matplotlib.rcParams.update({
    'pgf.texsystem': 'pdflatex',
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

# 数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 绘图
fig, ax = plt.subplots(figsize=(3.5, 2.5))
ax.plot(x, y, linewidth=1.5)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
ax.set_title('Sine Wave')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figure.pgf')
```

LaTeX 中使用：

```latex
\begin{figure}
    \centering
    \input{figure.pgf}
    \caption{示例图表}
    \label{fig:example}
\end{figure}
```
