"""
chart_generator.py - 将结构化实验数据转化为 Matplotlib 绘图代码
这是与生图模型完全不同的路径：结果图不用生图，用代码画
"""


def generate_bar_chart_code(extraction_result: str) -> str:
    """生成柱状对比图 Python 代码"""
    prompt = f"""你是一个数据可视化工程师。根据以下实验数据，生成一段完整的、可直接运行的 Python + Matplotlib 代码来绘制柱状对比图。

## 严格规则
1. **输出必须是完整可运行的 Python 代码**，包含所有 import
2. **使用 matplotlib**，不要用 seaborn 或其他库（保持兼容性）
3. **颜色使用学术配色**：蓝色系（#2171B5, #4292C6, #6BAED6）为主本文方法，其他颜色区分基线
4. **Y 轴标签使用英文**，刻度清晰
5. **每个柱子顶部显示数值**（ annotate）
6. **添加图例 (legend)** 和网格线 (grid)
7. **图表标题和轴标签全部使用英文**
8. **保存到文件**：output_bar.png（300 DPI，高分辨率）
9. **绝对不能有任何中文字符**

## 代码模板参考
```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

methods = ['Method A', 'Method B', 'Ours']
scores = [72.3, 75.8, 81.2]
colors = ['#CCCCCC', '#AAAAAA', '#2171B5']

fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
bars = ax.bar(methods, scores, color=colors, width=0.5, edgecolor='black', linewidth=0.8)
for bar, score in zip(bars, scores):
    ax.annotate(f'{{score:.1f}}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 3), textcoords='offset points', ha='center', fontsize=10)
ax.set_ylabel('Accuracy (%)', fontsize=12)
ax.set_title('Performance Comparison on Dataset X', fontsize=13)
ax.set_ylim(0, 100)
ax.grid(axis='y', linestyle='--', alpha=0.7)
ax.legend(['Method A', 'Method B', 'Ours'], loc='lower right')
plt.tight_layout()
plt.savefig('output_bar.png', dpi=300, bbox_inches='tight')
plt.close()
print('[DONE] Bar chart saved.')
```

## 实验数据
{extraction_result}

请直接输出完整的 Python 代码：
"""
    return prompt


def generate_line_chart_code(extraction_result: str) -> str:
    """生成折线对比图 Python 代码"""
    prompt = f"""你是一个数据可视化工程师。根据以下实验数据，生成一段完整的、可直接运行的 Python + Matplotlib 代码来绘制折线对比图。

## 严格规则
1. **输出必须是完整可运行的 Python 代码**
2. **使用 matplotlib**，折线图样式学术规范
3. **每个方法一条线**，用不同颜色和标记区分
4. **X 轴为训练步数/迭代次数或时间**，Y 轴为指标
5. **添加网格线**和**图例**
6. **所有文字使用英文**
7. **保存到文件**：output_line.png（300 DPI）
8. **绝对不能有任何中文字符**

## 实验数据
{extraction_result}

请直接输出完整的 Python 代码：
"""
    return prompt


def generate_ablation_chart_code(extraction_result: str) -> str:
    """生成消融实验图 Python 代码"""
    prompt = f"""你是一个数据可视化工程师。根据以下消融实验数据，生成完整的 Python + Matplotlib 柱状图代码。

## 严格规则
1. **完整可运行的 Python 代码**
2. **用分组柱状图 (grouped bar chart)** 展示不同配置的消融结果
3. **基线方法用灰色**，去掉某组件的用浅色，完整方法用深蓝色
4. **每个柱子顶部显示数值**
5. **所有文字英文**
6. **保存为 ablation.png（300 DPI）**

## 消融实验数据
{extraction_result}

请直接输出完整的 Python 代码：
"""
    return prompt


def convert_to_chart_code(figure_type: str, extraction_result: str) -> str:
    """
    主入口：根据具体子类型返回对应 Matplotlib 代码生成 Prompt
    """
    if "ablation" in extraction_result.lower() or "消融" in extraction_result:
        return generate_ablation_chart_code(extraction_result)
    elif "curve" in extraction_result.lower() or "折线" in extraction_result or "training" in extraction_result.lower():
        return generate_line_chart_code(extraction_result)
    else:
        return generate_bar_chart_code(extraction_result)


def execute_chart_code(code: str) -> tuple:
    """
    执行生成的 Matplotlib 代码，返回 (success, output_path, error)
    """
    import os, sys, tempfile

    try:
        output_dir = os.path.join(os.path.expanduser("~"), ".qclaw", "workspace", "outputs")
        os.makedirs(output_dir, exist_ok=True)

        # 将代码写入临时文件执行
        code_path = os.path.join(output_dir, "_temp_chart.py")
        with open(code_path, "w", encoding="utf-8") as f:
            f.write(code)

        import subprocess
        result = subprocess.run(
            ["python", code_path],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=output_dir
        )

        os.remove(code_path)

        if result.returncode != 0:
            return False, "", result.stderr

        # 找出生成的文件
        for fname in ["output_bar.png", "output_line.png", "ablation.png"]:
            fpath = os.path.join(output_dir, fname)
            if os.path.exists(fpath):
                return True, fpath, ""

        return False, "", "No output file found"

    except Exception as e:
        return False, "", str(e)
