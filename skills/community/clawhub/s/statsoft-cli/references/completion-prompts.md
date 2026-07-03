# 配置完成提示模板 / Configuration Completion Prompts

> 本文档由 SKILL.md 精简时拆出，包含各统计软件配置完成后的提示模板。
> 软件统计完成后，AI 应按以下模板输出提示信息给用户。

---

## SPSS 配置完成提示

> ⚠️ **重要 — 日常使用建议**：
> - **跑复杂语法 → 用方案 1**（`stats.com` + `.spj`，万无一失）
> - **方案 2**（Python 内部驱动）**只能跑纯分析语法**，不能包含：
>   - `OUTPUT SAVE`、`OUTPUT EXPORT`、`OUTPUT DISPLAY`
>   - `HOST COMMAND`、`XDATA`、`XSAVE`（涉及 OUTPUT 对象时）
> - 遇到不确定是否涉及 OUTPUT/SAVE 的命令时 → 统一走方案 1（`.spj`）

详见 SKILL.md 第 8 行"核心权限 / Core Permissions"章节中的 SPSS 调用方式说明。

### English Version

See SKILL.md core permissions section for SPSS invocation details.

---

## SPSS Modeler 配置完成提示

## SPSS Modeler 配置完成提示

- ✅ SPSS Modeler 通过 `clemb.exe` 支持纯 CLI 执行，完全无 GUI，无闪屏
- ⚠️ Windows-only，不支持 macOS 和 Linux
- 💡 适合数据挖掘、预测建模和机器学习流水线

### English Version

- ✅ SPSS Modeler supports pure CLI execution via `clemb.exe`, completely GUI-free, no splash screen
- ⚠️ Windows-only, no macOS/Linux support
- 💡 Suitable for data mining, predictive modeling, ML pipelines

---

## Stata 配置完成提示

```
✅ Stata 关联配置已完成！

⚠️ 重要注意事项：
  1. **⚠️⚠️ Stata 版本与批处理参数（重要）**：
     - **Stata 12 及更早** → Windows: `/e do "script.do"`, Mac/Linux: `-e do "script.do"`
     - **Stata 13 及之后** → Windows: `/b do "script.do"`, Mac/Linux: `-b do "script.do"`
     - ❌ **用错版本参数会导致弹出确认框！**
  2. 路径中含有空格时必须用双引号包裹，否则会报 file not found 错误
  3. **许可证匹配**：调用 Stata 时必须使用与许可证匹配的版本可执行文件
     - 有 MP 许可证 → 使用 StataMP-64.exe（Windows）或 stata-mp（Mac/Linux）
     - 有 SE 许可证 → 使用 StataSE-64.exe（Windows）或 stata-se（Mac/Linux）
     - 有 BE 许可证 → 使用 Stata-64.exe（Windows）或 stata（Mac/Linux）
     - ❌ 如果用错版本（如用 MP 版但没有 MP 许可证），Stata 会启动失败或报错
  4. **版本功能差异**：
     - MP（Multiprocessing）：支持多核并行，适合大数据
     - SE（Special Edition）：单核，适合中等数据
     - BE（Basic Edition）：功能受限，不支持并行
  5. **版本特定变化**：
     - Stata 14/15：可执行文件名为 StataMP、StataSE（无 -64 后缀）
     - Stata 16+：可执行文件名为 StataMP-64、StataSE-64（新增 -64 后缀）
     - Stata 16+：支持 Python 集成（可从 Stata 调用 Python）
     - Stata 17+：引入 PyStata（可从 Python 调用 Stata）
     - Stata 19+：引入 StataNow 快速更新机制
  6. **Windows 安装路径差异**：
     - Stata 14-18: `C:\Program Files\StataNN`（NN为版本号）
     - Stata 19: `C:\Program Files\Stata19` 或 `C:\Program Files\StataNow19`

📋 推荐使用方式：
  # Windows（根据许可证选择正确版本）
  "StataMP-64.exe" /b do "script.do"   # MP 版（Stata 16+）
  "StataSE-64.exe" /b do "script.do"   # SE 版（Stata 16+）
  "Stata-64.exe" /b do "script.do"     # BE 版（Stata 16+）
  "StataMP" /b do "script.do"          # MP 版（Stata 14/15）

  # Mac/Linux（根据许可证选择正确版本）
  stata-mp -b do "script.do"   # MP 版
  stata-se -b do "script.do"   # SE 版
  stata -b do "script.do"      # BE 版
```

---

## R 配置完成提示

```
✅ R 关联配置已完成！

⚠️ 重要注意事项：
  1. 批处理模式使用 Rscript 命令，不要用 R GUI
  2. 安装新 R 包时使用 quiet=TRUE 参数实现静默安装
  3. 中文乱码问题：用 fileEncoding="UTF-8" 参数指定文件编码
  4. 内存不足时：使用 data.table 或 arrow 包处理大数据

📋 推荐使用方式：
  Rscript --vanilla "script.R"

  # 静默安装包
  Rscript -e "install.packages('[PKG]', repos='https://cran.r-project.org', quiet=TRUE)"

  # 读取 SPSS .sav 文件
  Rscript -e "library(haven); df <- read_sav('data.sav'); print(head(df))"

💡 无 R 时的替代方案：
  如果未安装 R 且不愿意安装，可以使用 Anaconda Python 环境作为替代：
  - dplyr / tidyr → pandas
  - ggplot2 → matplotlib / seaborn
  - caret / xgboost → scikit-learn
  - survival → lifelines
  - lme4 / nlme → statsmodels
  - metafor → PyMC
```

### English Version

```
✅ R connection configuration complete!

⚠️ Important notes:
  1. Use Rscript command for batch mode, not R GUI
  2. Use quiet=TRUE parameter for silent package installation
  3. Chinese encoding issues: use fileEncoding="UTF-8" parameter
  4. Insufficient memory: use data.table or arrow packages for large data

📋 Recommended usage:
  Rscript --vanilla "script.R"

  # Silent package installation
  Rscript -e "install.packages('[PKG]', repos='https://cran.r-project.org', quiet=TRUE)"

  # Read SPSS .sav file
  Rscript -e "library(haven); df <- read_sav('data.sav'); print(head(df))"

💡 Alternatives without R:
  If R is not installed, consider using Anaconda Python environment:
  - dplyr / tidyr → pandas
  - ggplot2 → matplotlib / seaborn
  - caret / xgboost → scikit-learn
  - survival → lifelines
  - lme4 / nlme → statsmodels
  - metafor → PyMC
```

---

## SAS 配置完成提示

```
✅ SAS 关联配置已完成！

⚠️ 重要注意事项：
  1. 批处理模式会生成 .log（日志）和 .lst（输出列表）文件，确保输出路径有写权限
  2. 中文乱码问题：在程序开头加 options encoding='utf-8';
  3. SAS 许可证过期会导致 ERROR: License 过期，需更新许可证文件

📋 推荐使用方式：
  # Windows
  "sas.exe" -sysin "prog.sas" -log "out.log" -print "out.lst"

  # Mac/Linux
  sas -sysin "prog.sas" -log "out.log" -print "out.lst"
```

### English Version

```
✅ SAS connection configuration complete!

⚠️ Important notes:
  1. Batch mode generates .log (log) and .lst (output listing) files, ensure write permissions
  2. Chinese encoding: add options encoding='utf-8'; at beginning of program
  3. SAS license expiration will cause ERROR: License expired

📋 Recommended usage:
  # Windows
  "sas.exe" -sysin "prog.sas" -log "out.log" -print "out.lst"

  # Mac/Linux
  sas -sysin "prog.sas" -log "out.log" -print "out.lst"
```

### English Version

```
✅ SAS connection configuration complete!

⚠️ Important notes:
  1. Batch mode generates .log (log) and .lst (output listing) files, ensure write permissions
  2. Chinese encoding: add options encoding='utf-8'; at beginning of program
  3. SAS license expiration will cause ERROR: License expired

📋 Recommended usage:
  # Windows
  "sas.exe" -sysin "prog.sas" -log "out.log" -print "out.lst"

  # Mac/Linux
  sas -sysin "prog.sas" -log "out.log" -print "out.lst"
```

---

## JMP 配置完成提示

- ⚠️ JMP 运行时会有短暂闪屏（1-2秒），无法完全避免
- ⚠️ 脚本末尾必须加 `Exit();`，否则 JMP GUI 会保持打开

> 详细配置信息和注意事项请参考 [ADDITIONAL_SOFTWARE.md → JMP](ADDITIONAL_SOFTWARE.md#jmp)

### English Version

- ⚠️ JMP may display a brief splash screen (1-2 seconds), cannot be fully avoided
- ⚠️ Script must end with `Exit();` or JMP GUI will remain open

> See [ADDITIONAL_SOFTWARE.md → JMP](ADDITIONAL_SOFTWARE.md#jmp) for details


---

## GraphPad Prism 配置完成提示

- ⚠️⚠️⚠️ GraphPad Prism **没有 CLI 模式**，调用时会弹出 GUI 界面（无法避免）
- ⚠️ 使用时会有以下现象：调用时弹出 GUI 界面，用户需手动操作

**替代方案**：
| 方案 | 说明 |
|------|------|
| Python `prismWriter` | 后台操作 .pzfx 文件（无需 GUI） |
| Windows COM/OLE | 通过 pywin32 调用 GraphPad Prism 自动化接口 |

> 详细配置信息和注意事项请参考 [ADDITIONAL_SOFTWARE.md → GraphPad Prism](ADDITIONAL_SOFTWARE.md#graphpad-prism)


---

## Stat/Transfer 配置完成提示

- ✅ Stat/Transfer 是纯 CLI 工具，完全无 GUI，适合自动化
- ⚠️ 转换前请确认目标格式支持所需的数据类型

> 详细配置信息请参考 [ADDITIONAL_SOFTWARE.md → Stat/Transfer](ADDITIONAL_SOFTWARE.md#stattransfer)


---

## Gretl 配置完成提示

- ✅ Gretl 是纯 CLI 工具，完全无 GUI，无闪屏
- ✅ 免费软件，适合计量经济学分析
- 💡 支持 Stata .dta、SAS .sas7bdat、Excel .xlsx 等格式读取

> 详细配置信息请参考 [ADDITIONAL_SOFTWARE.md → Gretl](ADDITIONAL_SOFTWARE.md#gretl)


---

## Minitab 配置完成提示

- ⚠️ Minitab 批处理模式可能有短暂闪屏
- ⚠️ 确保许可证有效
- 💡 适合质量控制和六西格玛项目

> 详细配置信息请参考 [ADDITIONAL_SOFTWARE.md → Minitab](ADDITIONAL_SOFTWARE.md#minitab)


---

## Matlab 配置完成提示

- ✅ 使用 `-batch` 参数时完全无 GUI，无闪屏
- ⚠️ 需要 Statistics and Machine Learning Toolbox 进行统计分析
- 💡 适合工程统计、信号处理和机器学习

> 详细配置信息请参考 [ADDITIONAL_SOFTWARE.md → Matlab](ADDITIONAL_SOFTWARE.md#matlab)

### English Version

- ✅ Completely GUI-free when using `-batch` parameter
- ⚠️ Requires Statistics and Machine Learning Toolbox
- 💡 Suitable for engineering statistics, signal processing, and ML

> See [ADDITIONAL_SOFTWARE.md → Matlab](ADDITIONAL_SOFTWARE.md#matlab) for details

---

## Mathematica 配置完成提示

- ✅ Mathematica 是纯 CLI 工具（`wolframscript`），完全无 GUI，无闪屏
- ✅ 跨平台支持（Win/Mac/Linux）
- 💡 适合符号数学、数值分析、统计建模和可视化
- ⚠️ WolframScript 是商业软件许可证，需要定期激活

> 详细配置信息和注意事项请参考 [ADDITIONAL_SOFTWARE.md → Mathematica](ADDITIONAL_SOFTWARE.md#mathematica)

### English Version

- ✅ Mathematica is a pure CLI tool (`wolframscript`), completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- 💡 Suitable for symbolic mathematics, numerical analysis, statistical modeling, and visualization
- ⚠️ WolframScript requires a commercial license with periodic activation

> See [ADDITIONAL_SOFTWARE.md → Mathematica](ADDITIONAL_SOFTWARE.md#mathematica) for details


---

## Julia 配置完成提示

- ✅ Julia 是纯 CLI 工具，完全无 GUI，无闪屏
- ✅ 高性能，适合大数据和复杂统计计算
- 💡 常用包：`Statistics`、`HypothesisTests`、`GLM`、`Turing`（贝叶斯）

> 详细配置信息请参考 [ADDITIONAL_SOFTWARE.md → Julia](ADDITIONAL_SOFTWARE.md#julia)

### English Version

- ✅ Julia is a pure CLI tool, completely GUI-free, no splash screen
- ✅ High performance, suitable for big data and complex statistical computing
- 💡 Common packages: Statistics, HypothesisTests, GLM, Turing (Bayesian)

> See [ADDITIONAL_SOFTWARE.md → Julia](ADDITIONAL_SOFTWARE.md#julia) for details


---

## EViews 配置完成提示

- ⚠️ EViews 批处理模式可能有闪屏
- ⚠️ Windows-only，不支持 macOS 和 Linux
- 💡 适合时间序列分析、回归和预测

> 详细配置信息请参考 [ADDITIONAL_SOFTWARE.md → EViews](ADDITIONAL_SOFTWARE.md#eviews)


---

## Statistica 配置完成提示

- ⚠️ Statistica 批处理模式可能有闪屏
- ⚠️ Windows-only，不支持 macOS 和 Linux
- 💡 适合数据挖掘、机器学习和统计分析

> 详细配置信息请参考 [ADDITIONAL_SOFTWARE.md → Statistica](ADDITIONAL_SOFTWARE.md#statistica)


## JAGS 配置完成提示

- ✅ JAGS 是纯 CLI 工具，完全无 GUI，无闪屏
- ✅ 跨平台支持（Win/Mac/Linux）
- ⚠️ 如果通过 `rjags` R 包调用，需要先安装 R 和 rjags 包
- 💡 适合贝叶斯层次模型、MCMC 模拟

📋 推荐使用方式：
  jags scriptfile

💡 通过 R 接口调用：
  Rscript -e "library(rjags); jags.model('script.dat', data)"

---

## SHAZAM 配置完成提示

- ✅ SHAZAM 是纯 CLI 工具，完全无 GUI，无闪屏
- ✅ 跨平台支持（Win/Mac/Linux）
- ⚠️ Windows 版需要确保许可证文件有效
- 💡 适合计量经济学、时间序列、假设检验

📋 推荐使用方式：
  shazam commands.txt

---

## OxMetrics 配置完成提示

- ✅ OxMetrics 是纯 CLI 工具，完全无 GUI，无闪屏
- ✅ 跨平台支持（Win/Mac/Linux）
- ⚠️ 需要许可证文件
- 💡 适合计量经济学、时间序列、预测

📋 推荐使用方式：
  oxmetrics --help          # 查看选项
  oxmetrics -b commands.txt # 批处理

---

## TSP 配置完成提示

- ✅ TSP 是纯 CLI 工具，完全无 GUI，无闪屏
- ✅ 跨平台支持（Win/Mac/Linux）
- ⚠️ 需要许可证文件
- 💡 适合时间序列分析、计量经济学、假设检验

📋 推荐使用方式：
  tsp commands.txt

---

## Tanagra 配置完成提示

- ✅ Tanagra 是纯 CLI 工具，完全无 GUI，无闪屏
- ✅ 跨平台支持（Win/Mac/Linux）
- ✅ 开源免费
- 💡 适合聚类、分类、关联规则、特征选择

📋 推荐使用方式：
  tanagra --help          # 查看选项
  tanagra -f script.txt   # 批处理脚本

---

## Orange 配置完成提示

- ⚠️ Orange **没有纯 CLI 模式**，调用时会弹出 GUI 界面（无法避免）
- ✅ 推荐通过 Python 模块后台调用（无需 GUI）
- ✅ 跨平台支持（Win/Mac/Linux）
- ✅ 开源免费

**纯 CLI 替代方案（Python）**：
```python
# 后台运行 Orange 分析脚本，无需 GUI
from Orange.data import Table
from Orange.classification import RandomForestLearner

data = Table("data.csv")
learner = RandomForestLearner()
model = learner(data)
predictions = model(data)
```

📋 推荐使用方式：
  python3 -m Orange.canvas          # GUI 模式
  python3 script.py                 # Python 脚本模式（推荐，无 GUI）

---

## H2O.ai 配置完成提示

- ✅ H2O 可以通过 Python 后台运行，无 GUI 弹窗
- ✅ 跨平台支持（Win/Mac/Linux）
- ✅ 开源免费（AutoML 功能完全免费）
- ⚠️ 需要 Java 环境（JVM）
- ⚠️ 首次启动需下载组件
- 💡 适合大规模机器学习、AutoML、深度学习

📋 推荐使用方式（Python）：
```python
import h2o
h2o.init()                          # 启动 H2O 服务器（后台）
h2o.import_file("data.csv")         # 上传数据
# ... AutoML 训练 ...
h2o.shutdown()                      # 关闭服务器
```

⚠️ 注意事项：
  - 默认端口 54321 被占用时，使用 `h2o.init(port=54322)`
  - 内存不足时设置 `h2o.init(max_mem_size="4G")`

---

## GenStat 配置完成提示

- ✅ GenStat 是纯 CLI 工具，完全无 GUI，无闪屏
- ✅ 跨平台支持（Win/Mac/Linux）
- ⚠️ 需要许可证文件
- 💡 适合混合模型、试验设计、REML、空间分析、Meta 分析

📋 推荐使用方式：
  genstat commands.txt

---

## Rattle 配置完成提示

- ⚠️ Rattle **没有纯 CLI 模式**，调用时会弹出 GUI 界面（无法避免）
- ✅ 推荐通过 R 脚本后台调用 Rattle 函数（无需 GUI）
- ✅ 跨平台支持（Win/Mac/Linux）
- ✅ 开源免费
- 💡 适合数据挖掘、决策树、聚类、关联规则

**纯 CLI 替代方案（R 脚本）**：
```r
library(rattle)
# 加载数据
audit <- read.csv("audit.csv")
# 构建模型
model <- Target ~ Age + Employment + ... 
# 输出结果
summary(model)
```

📋 推荐使用方式：
  rattle --cli    # 尝试 CLI 模式（可能仍弹窗，不保证）
  Rscript script.R  # R 脚本调用 Rattle 函数（推荐，无 GUI）

---

## OpenBUGS 配置完成提示

- ⚠️ OpenBUGS **没有纯 CLI 模式**，调用时会弹出 GUI 界面（无法避免）
- ✅ 可通过 R 包 `R2OpenBUGS` 或 `BRugs` 后台调用（无需 GUI）
- ✅ 跨平台支持（Win/Mac/Linux）
- ✅ 开源免费
- 💡 适合贝叶斯分析、MCMC、层次模型

**纯 CLI 替代方案（R 脚本）**：
```r
library(BRugs)
# 定义模型
modelCheck("model.txt")
modelData("data.txt")
modelCompile()
modelUpdate(1000)
# 提取结果
samplesStats("*")
```

📋 推荐使用方式：
  openbugs --help            # GUI 模式
  Rscript openbugs_script.R  # R 脚本调用（推荐，无 GUI）

---

## LIMDEP 配置完成提示

- ✅ LIMDEP 是纯 CLI 工具，完全无 GUI，无闪屏
- 🔴 仅支持 Windows
- ⚠️ 需要许可证文件
- 💡 适合 Logit、Probit、Tobit、样本选择、Count 模型、Frontier 分析

📋 推荐使用方式（Windows）：
  limdep commands.txt

English Memory Template:
```
- **Version**: LIMDEP 11.0
- **Path**: `[LIMDEP_install_PATH]\limdep.exe`
- **Batch Command Format**:
  ```batch
  limdep commands.txt
  ```
- **Notes**: Windows only, license required
```

---

## NLOGIT 配置完成提示

- ✅ NLOGIT 是纯 CLI 工具，完全无 GUI，无闪屏
- 🔴 仅支持 Windows
- ⚠️ 需要许可证文件（包含在 LIMDEP 许可证中）
- 💡 适合 Multinomial Logit、Nested Logit、Mixed Logit、Probit 模型

📋 推荐使用方式（Windows）：
  nlogit commands.txt

---

## Microfit 配置完成提示

- ✅ Microfit 是纯 CLI 工具，完全无 GUI，无闪屏
- 🔴 仅支持 Windows
- ⚠️ 需要许可证文件
- 💡 适合时间序列、计量经济学、单位根检验、ARDL、面板数据

📋 推荐使用方式（Windows）：
  microfit commands.txt

---

## CmdStan 配置完成提示

- ✅ CmdStan 是纯 CLI 工具，完全无 GUI，无闪屏
- ✅ 跨平台支持（Win/Mac/Linux）
- ✅ 开源免费
- ⚠️ 首次使用需编译模型（耗时较长）
- ⚠️ 需要 C++ 编译器（Windows: Rtools 或 Visual Studio）
- 💡 适合贝叶斯统计、层次模型、消费者行为建模

📋 推荐使用方式：
  # 编译模型
  stanc model.stan
  # 运行采样
  sample num_samples=1000 num_warmup=500 data file=data.json
  # 查看结果
  stansummary output.csv

💡 通过 cmdstanr/cmdstanpy 调用（推荐）：
  Rscript -e "library(cmdstanr); model <- cmdstan_model('model.stan'); fit <- model\$sample(data_file='data.json')"

---

## Weka 配置完成提示

- ✅ Weka 是纯 CLI 工具，完全无 GUI，无闪屏
- ✅ 跨平台支持（Win/Mac/Linux）
- ✅ 开源免费
- ⚠️ 需要 Java 环境（JVM）
- ⚠️ 大数据时需增加 JVM 内存：`java -Xmx4g -jar weka.jar ...`
- 💡 适合聚类、分类、关联规则、特征选择、购物篮分析

📋 推荐使用方式：
  # 命令行分类
  java -cp weka.jar weka.classifiers.trees.RandomForest -t data.arff -T test.arff
  # 聚类
  java -cp weka.jar weka.clusterers.SimpleKMeans -t data.arff -N 3
  # 关联规则
  java -cp weka.jar weka.associations.Apriori -t data.arff

### English Version

- ✅ Weka is a pure CLI tool, completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- ✅ Open source and free
- ⚠️ Requires Java environment (JVM)
- ⚠️ Increase JVM memory for large data: `java -Xmx4g -jar weka.jar ...`
- 💡 Suitable for clustering, classification, association rules, feature selection, market basket analysis

📋 Recommended usage:
  # Command line classification
  java -cp weka.jar weka.classifiers.trees.RandomForest -t data.arff -T test.arff
  # Clustering
  java -cp weka.jar weka.clusterers.SimpleKMeans -t data.arff -N 3
  # Association rules
  java -cp weka.jar weka.associations.Apriori -t data.arff

---

## KNIME 配置完成提示

- ✅ KNIME 支持无头模式（headless），完全无 GUI，无闪屏
- ✅ 跨平台支持（Win/Mac/Linux）
- ✅ 开源免费
- ⚠️ 无头模式需安装 KNIME 无头扩展
- ⚠️ 工作流需预先在 GUI 中设计好
- 💡 适合自动化工作流、ETL、数据挖掘、可视化分析

📋 推荐使用方式：
  # 无头模式执行工作流
  knime -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflowDir="/path/to/workflow"
  # 带参数执行
  knime -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflowDir="/path/to/workflow" -workflow.variable=myVar,value,String

---

## jamovi 配置完成提示

- ⚠️ jamovi **没有纯 CLI 模式**，调用时会弹出 GUI 界面（无法避免）
- ✅ 可通过 `jmv` R 包后台调用 jamovi 分析模块（无需 GUI）
- ✅ 跨平台支持（Win/Mac/Linux）
- ✅ 开源免费
- 💡 适合描述统计、贝叶斯分析、频率分析

**纯 CLI 替代方案（R 脚本）**：
```r
library(jmv)
# 描述统计
descriptives <- jmv::descriptives(data = mydata, vars = c("var1", "var2"))
# 卡方检验
chisq <- jmv::contTables(data = mydata, rows = "group", cols = "outcome")
```

📋 推荐使用方式：
  jamovi --Rj "summary(mtcars)"    # Rj 模式（可能仍弹窗）
  Rscript jmv_script.R              # R 脚本调用 jmv 包（推荐，无 GUI）

---

## JASP 配置完成提示

- ⚠️ JASP **没有纯 CLI 模式**，调用时会弹出 GUI 界面（无法避免）
- ✅ 可通过 `jaspTools` R 包后台调用 JASP 分析模块（无需 GUI）
- ✅ 跨平台支持（Win/Mac/Linux）
- ✅ 开源免费
- 💡 适合描述统计、贝叶斯分析、探索性分析

**纯 CLI 替代方案（R 脚本）**：
```r
library(jaspTools)
# 加载 JASP 数据
data <- jaspTools::readOSR("data.csv")
# 描述统计
desc <- jaspTools::descriptives(data, variables = c("var1", "var2"))
```

📋 推荐使用方式：
  jasp --console data.csv           # 实验性控制台模式（可能仍弹窗）
  Rscript jasp_script.R             # R 脚本调用 jaspTools 包（推荐，无 GUI）

---

## PSPP 配置完成提示

- ✅ PSPP 是纯 CLI 工具，完全无 GUI，无闪屏
- ✅ 跨平台支持（Win/Mac/Linux）
- ✅ 开源免费（SPSS 替代品）
- ⚠️ 语法与 SPSS 兼容，但部分高级功能不支持
- 💡 适合描述统计、回归、列联表、数据清洗

📋 推荐使用方式：
  # 运行 .sps 语法
  pspp -o output.txt analysis.sps
  # 管道模式
  pspp < analysis.sps
  # 直接输出到文件
  pspp analysis.sps -o output.html

---

## Mplus 配置完成提示

- ✅ Mplus 是纯 CLI 工具，完全无 GUI，无闪屏
- ✅ 支持 Windows 和 Mac
- ⚠️ 需要许可证文件
- ⚠️ 语法较独特，学习曲线陡峭
- 💡 适合 SEM、潜类别分析（LCA/LPA）、多水平模型、生存分析

📋 推荐使用方式：
  mplus model.inp
  # 带输出文件
  mplus model.inp output.out

---

## AMOS 配置完成提示

- ⚠️ AMOS **没有纯 CLI 模式**，调用时会弹出 GUI 界面（无法避免）
- ✅ 可通过 IBM SPSS Amos Python 扩展后台调用（无需 GUI）
- 🔴 仅支持 Windows
- ⚠️ 需要 SPSS Statistics 许可证
- 💡 适合 SEM、路径分析、验证性因子分析

**纯 CLI 替代方案（Python 脚本）**：
```python
# 需要 IBM SPSS Amos Python 扩展
import amos
amos.RunAnalysis("model.amw", "output.out")
```

📋 推荐使用方式：
  # GUI 模式（会弹窗）
  amos.exe model.amw
  # Python 脚本调用（推荐，无 GUI）
  python amos_script.py

---

## Q (MRKS) 配置完成提示

- ✅ Q (MRKS) 支持 QScript 批处理模式，完全无 GUI，无闪屏
- 🔴 仅支持 Windows
- ⚠️ 需要 Q (MRKS) 许可证
- 💡 适合市场调研问卷分析、交叉表、统计检验

📋 推荐使用方式（Windows）：
  REM 运行 QScript
  Q.exe /QScript "c:\scripts\analysis.qs"
  REM 带日志
  Q.exe /QScript "c:\scripts\analysis.qs" /Log "c:\logs\output.log"

---

## NCSS 配置完成提示

```
✅ NCSS 关联配置已完成！

📊 配置信息：
  - NCSS 版本: [2024]
  - NCSS 主程序: [NCSS.exe 路径]
  - 平台: Windows

⚠️ 重要注意事项：
  1. NCSS 支持批处理模式，可通过 /B 参数运行分析脚本
  2. Windows-only，不支持 macOS 和 Linux
  3. 适合医疗统计、样本量计算和临床数据分析

📋 推荐使用方式：
  "NCSS.exe" /B "analysis.ncss"
```

### English Version

```
✅ NCSS connection configuration complete!

📊 Configuration Information:
  - NCSS Version: [2024]
  - NCSS Executable: [NCSS.exe path]
  - Platform: Windows

⚠️ Important notes:
  1. NCSS supports batch mode via /B parameter
  2. Windows-only, no macOS/Linux support
  3. Suitable for medical statistics, sample size calculation, clinical data analysis

📋 Recommended usage:
  "NCSS.exe" /B "analysis.ncss"
```

---

## Origin (OriginLab) 配置完成提示

```
✅ Origin 关联配置已完成！

📊 配置信息：
  - Origin 版本: [2025/2024/2023]
  - Origin 主程序: [Origin95.exe 或 Origin97.exe 路径]
  - 平台: Windows

⚠️ 重要注意事项：
  1. Origin 支持 LabTalk 脚本批处理，通过 -h 参数运行 .ogs 脚本
  2. 科学绘图与数据分析软件，全球百万用户
  3. macOS 版本 CLI 支持有限，建议在 Windows 环境下使用
  4. 适合批量数据处理、科学图表生成和统计分析

📋 推荐使用方式：
  "origin97.exe" -h "script.ogs"
```

### English Version

```
✅ Origin connection configuration complete!

📊 Configuration Information:
  - Origin Version: [2025/2024/2023]
  - Origin Executable: [Origin95.exe or Origin97.exe path]
  - Platform: Windows

⚠️ Important notes:
  1. Origin supports LabTalk script batch processing via -h parameter
  2. Scientific graphing and data analysis software, over 1M users worldwide
  3. macOS CLI support is limited, Windows environment recommended
  4. Suitable for batch data processing, scientific figure generation, statistical analysis

📋 Recommended usage:
  "origin97.exe" -h "script.ogs"
```

---

## 通用记忆模板格式

如果软件未在本文档中列出，可使用以下通用模板：

### 中文记忆模板

```
### [软件名] 环境配置 / [Software] Environment

- **版本 / Version**：[版本号]
- **主程序路径 / Executable Path**：`[路径]`
- **批处理命令行格式 / Batch Command Format**：
  ```bash
  [调用命令]
  ```
- **脚本模板 / Script Template**：
  ```[语言]
  [示例代码]
  ```
- **常见错误与解决方案 / Common Errors & Solutions**：
  | 错误 | 原因 | 解决方案 |
  |------|------|---------|
  | [错误1] | [原因] | [方案] |
- **配置完成提示 / Configuration Completion Notes**：
  - ✅ [优点1]
  - ⚠️ [注意事项1]
```

### English Memory Template

```
### [Software] Environment

- **Version**: [version]
- **Executable Path**: `[path]`
- **Batch Command Format**:
  ```bash
  [command]
  ```
- **Script Template**:
  ```[language]
  [code]
  ```
- **Common Errors & Solutions**:
  | Error | Cause | Solution |
  |-------|-------|---------|
  | [error1] | [cause] | [solution] |
- **Configuration Completion Notes**:
  - ✅ [benefit1]
  - ⚠️ [caution1]
```
