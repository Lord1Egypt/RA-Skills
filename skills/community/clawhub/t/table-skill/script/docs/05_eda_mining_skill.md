# 📊 深度探索与可视化规范 (EDA & Mining)

> **致 Agent 的系统指令**: 
> 当你阅读到本文件时，意味着前置的表格预处理（拆分、清洗、表头合并）已经完成。请读取生成的 `*_description.json` 了解数据结构，并严格按照以下 **5 个核心阶段** 编写 Python 代码来执行深度分析、可视化与 Web 报告生成。

---

## 🛡️ 1. 数据质量与校验规则 (QA)

在生成任何图表之前，必须先对提取的数据进行严格的代码分析与验证。请在你的 Python 脚本中实现以下逻辑：

* **完整性与准确性 (Completeness & Accuracy)**: 检查缺失值 (`isnull().sum()`)、重复项，以及数据类型的一致性。如有必要，进行类型转换（如字符串转数值）。
* **异常值检测 (Outlier Detection)**: 使用 IQR、Z-scores 或 Isolation Forests 等统计方法检测异常情况。
* **可操作的 QA 记录 (Actionable QA)**: 在脚本的控制台输出（或 Logger）中，明确记录被丢弃、插补或调整了哪些数据。

---

## 🔍 2. 探索性数据分析 (EDA)

基于清洗后的数据，编写代码进行深度的统计计算：

* **单变量/双变量分析**: 计算核心指标的均值、中位数、标准差、偏度等。
* **相关性发现**: 生成相关性矩阵 (Pearson/Spearman)，找出强相关的业务指标。
* **模式挖掘**: 识别时间序列的周期性趋势、数据聚类特征以及分类变量的频率分布。

---

## 💡 3. 业务假设生成 (Hypothesis Generation)

基于 EDA 阶段发现的模式，你必须在回复我的对话中（或者在分析报告中）提出具备落地价值的假设：

* **结构化陈述**: 提供清晰的原假设 ($H_0$) 和备择假设 ($H_1$)。
* **商业/科学影响**: 解释 **为什么** 这个假设对业务很重要（例如：它如何影响营收、欠费率或客户流失）。
* **实验设计**: 简要建议未来应如何测试该假设（例如：A/B 测试方案、回归建模）。

---

## 💻 4. 代码生成与可视化规则 (Python Visualization)

你编写的数据分析和绘图代码必须达到**生产级别**，并严格遵守以下规范：

### 代码质量与结构
* **模块化设计**: 使用类 (OOP) 或定义良好的函数。绝对避免面条式 (Spaghetti) 脚本。
* **错误处理**: 必须使用 `try-except` 块和 `logging` 模块来处理潜在的数据解析错误。

### 可视化美学 (Aesthetics)
* **审美底线**: **严禁**使用 Matplotlib 的默认丑陋样式。必须使用 `seaborn` 并搭配现代主题。
* **图表存储**: 必须将生成的图表保存到工作区的 `./charts/` 目录下，要求 `dpi=300` 且 `bbox_inches='tight'`。
* **强制代码模板**: 请务必参考并使用以下模板结构（已包含中文防乱码配置）：

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_aesthetic_chart(df: pd.DataFrame, output_name: str, title: str) -> None:
    """基于 DataFrame 生成高颜值图表并保存"""
    try:
        # 1. 设置高级审美主题 (必须先设置主题)
        sns.set_theme(style="whitegrid", font_scale=1.1)
        sns.set_palette("crest") # 建议使用 'crest', 'husl', 或 'Set2'
        
        # 2. 字体与防乱码配置 (必须放在 set_theme 之后，否则会被覆盖！)
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'PingFang SC'] 
        plt.rcParams['axes.unicode_minus'] = False
        
        # 3. 创建画布并绘图
        plt.figure(figsize=(12, 6))
        
        # TODO: Agent 在此填入具体的 seaborn 绘图逻辑
        
        plt.title(title, pad=15, fontweight='bold')
        
        # 4. 规范化保存路径
        output_path = Path(f"./charts/{output_name}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Successfully saved chart to {output_path}")
    except Exception as e:
        logger.error(f"Failed to generate chart {output_name}: {e}")

if __name__ == "__main__":
    # Agent 需在此编写读取 CSV/JSON，调用 QA/EDA 逻辑，并执行绘图的代码
    pass
```

---

## 📄 5. 现代化 Web 报告生成 (HTML/React)

在完成数据探索和图表绘制后，Agent 必须将 QA 结果、EDA 洞察、业务假设以及生成的图表，综合编译成一个精美的单文件 HTML 报告。

* **输出路径**: 必须保存为 `./reports/index.html`。
* **UI 主题选择 (Agent 根据数据类型选择)**:
  * *Theme 1: 清爽商务风 (Business/Sales)* - 使用 `bg-white` 或 `bg-gray-50`，留白多，避免沉重边框。
  * *Theme 2: 极客暗黑风 (IT/Anomalies)* - 使用 `bg-slate-900`，明亮文字色，突出异常值。
  * *Theme 3: 严谨学术风 (Research)* - 单色调，使用上下粗边框的表格，无圆角。
* **基础代码骨架 (Agent 需动态填充内容，注意 script 标签保持原样)**:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>深度数据分析与业务探索报告</title>
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <script src="[https://unpkg.com/react@18/umd/react.production.min.js](https://unpkg.com/react@18/umd/react.production.min.js)"></script>
    <script src="[https://unpkg.com/react-dom@18/umd/react-dom.production.min.js](https://unpkg.com/react-dom@18/umd/react-dom.production.min.js)"></script>
    <script src="[https://unpkg.com/babel-standalone@6/babel.min.js](https://unpkg.com/babel-standalone@6/babel.min.js)"></script>
</head>
<body class="bg-gray-50 text-gray-900 font-sans antialiased">
    <div id="root"></div>
    <script type="text/babel">
        function Report() {
            return (
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                    {/* 页头 */}
                    <header className="mb-16">
                        <h1 className="text-4xl font-extrabold tracking-tight mb-4">业务数据深度分析报告</h1>
                        <p className="text-xl text-gray-500">由 OpenClaw Agent 自动生成 • 数据质量已校验 ✓</p>
                    </header>

                    {/* Section 1: 数据质量 (QA) 摘要 */}
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-16 pb-8 border-b border-gray-200">
                        <div className="flex flex-col">
                            <span className="text-sm font-semibold uppercase tracking-wider text-gray-500 mb-1">数据完整度</span>
                            <span className="text-4xl font-light text-green-600">100%</span>
                        </div>
                        {/* 动态添加：总行数、异常值数量等 */}
                    </div>

                    {/* Section 2: 可视化与 EDA 洞察 */}
                    <section className="mb-20">
                        <h2 className="text-2xl font-bold mb-8">探索性数据分析 (EDA)</h2>
                        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start mb-12">
                            <div className="lg:col-span-8 bg-white p-4 rounded-lg shadow-sm">
                                {/* 注意相对路径 */}
                                <img src="../charts/your_generated_chart.png" alt="数据分析图表" className="w-full h-auto rounded" />
                            </div>
                            <div className="lg:col-span-4 space-y-6">
                                <div className="p-6 bg-white rounded-lg shadow-sm border-l-4 border-blue-500">
                                    <h3 className="font-bold text-lg mb-2">💡 核心业务洞察</h3>
                                    <p className="text-gray-700 leading-relaxed">[动态生成的统计发现]</p>
                                </div>
                            </div>
                        </div>
                    </section>

                    {/* Section 3: 业务假设与验证 */}
                    <section className="mb-20 bg-blue-50 p-10 rounded-xl border border-blue-100">
                        <h2 className="text-2xl font-bold mb-6 text-blue-900">🔬 业务假设 ($H_0$ / $H_1$)</h2>
                        <div className="space-y-6">
                            <div>
                                <h4 className="text-xl font-semibold text-blue-800">假设 1: [在此输入假设名称]</h4>
                                <p className="text-blue-900 mt-2"><strong>原假设 (H₀):</strong> [在此输入原假设]</p>
                                <p className="text-blue-900 mt-1"><strong>备择假设 (H₁):</strong> [在此输入备择假设]</p>
                                <p className="text-blue-800 mt-4 leading-relaxed"><strong>建议验证方案:</strong> [在此输入实验设计]</p>
                            </div>
                        </div>
                    </section>
                </div>
            );
        }
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<Report />);
    </script>
</body>
</html>
```

---

## 🛠️ 标准执行工作流 (Agent Workflow)

为确保分析流程的顺畅，Agent 必须严格按照以下顺序操作：

1. **环境准备**: 确保输出目录存在 (`mkdir -p ./charts ./reports ./scripts`)。
2. **理解数据**: 读取 `output` 目录中最新的 `*_description.json`，了解数据的列名和结构。
3. **QA 与 EDA**: 编写 Python 脚本清洗和分析数据，在控制台打印统计发现。
4. **生成假设**: 基于 EDA 结果，在对话中或脚本注释里生成 1-3 个可测试的业务假设。
5. **绘制图表**: 编写最终版 Python 脚本，生成图表并保存至 `./charts/`。
6. **编译报告**: 编写 Python 脚本或直接通过文本生成，将以上所有内容注入 HTML 模板，生成最终的 `./reports/index.html`。