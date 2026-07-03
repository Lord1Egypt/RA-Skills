---
name: 数学计算协议服务
description: 一个高性能的数学计算协议服务器，提供从基础算术到高级微积分和线性代数的全面数学计算功能。
version: 1.0.0
---

# 数学计算协议服务

一个高性能的数学计算协议服务器，提供从基础算术到高级微积分和线性代数的全面数学计算功能。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Evaluate mathematical expressions using SymPy.

Supports:
    - Arithmetic: +, -, *, /, ^
    - Trigonometry: sin, cos, tan, asin, acos, atan
    - Logarithms: log, ln, exp
    - Constants: pi, e
    - Functions: sqrt, abs

Examples:

SIMPLE ARITHMETIC:
    expression="2 + 2"
    Result: 4

TRIGONOMETRY:
    expression="sin(pi/2)"
    Result: 1.0

WITH VARIABLES:
    expression="x^2 + 2*x + 1", variables={"x": 3}
    Result: 16

MULTIPLE VARIABLES:
    expression="x^2 + y^2", variables={"x": 3, "y": 4}
    Result: 25 | `scripts.tools.calculate` |
| Perform percentage calculations: of, increase, decrease, or change.

Examples:

PERCENTAGE OF: 15% of 200
    operation="of", value=200, percentage=15
    Result: 30

INCREASE: 100 increased by 20%
    operation="increase", value=100, percentage=20
    Result: 120

DECREASE: 100 decreased by 20%
    operation="decrease", value=100, percentage=20
    Result: 80

PERCENTAGE CHANGE: from 80 to 100
    operation="change", value=80, percentage=100
    Result: 25 (25% increase) | `scripts.tools.percentage` |
| Advanced rounding operations with multiple methods.

Methods:
    - round: Round to nearest (3.145 → 3.15 at 2dp)
    - floor: Always round down (3.149 → 3.14)
    - ceil: Always round up (3.141 → 3.15)
    - trunc: Truncate towards zero (-3.7 → -3, 3.7 → 3)

Examples:

ROUND TO NEAREST:
    values=3.14159, method="round", decimals=2
    Result: 3.14

FLOOR (DOWN):
    values=3.14159, method="floor", decimals=2
    Result: 3.14

CEIL (UP):
    values=3.14159, method="ceil", decimals=2
    Result: 3.15

MULTIPLE VALUES:
    values=[3.14159, 2.71828], method="round", decimals=2
    Result: [3.14, 2.72] | `scripts.tools.round` |
| Convert between angle units: degrees ↔ radians.

Examples:

DEGREES TO RADIANS:
    value=180, from_unit="degrees", to_unit="radians"
    Result: 3.14159... (π)

RADIANS TO DEGREES:
    value=3.14159, from_unit="radians", to_unit="degrees"
    Result: 180

RIGHT ANGLE:
    value=90, from_unit="degrees", to_unit="radians"
    Result: 1.5708... (π/2) | `scripts.tools.convert_units` |
| Perform element-wise operations on arrays using Polars.

Supports array-array and array-scalar operations.

Examples:

SCALAR MULTIPLICATION:
    operation="multiply", array1=[[1,2],[3,4]], array2=2
    Result: [[2,4],[6,8]]

ARRAY ADDITION:
    operation="add", array1=[[1,2]], array2=[[3,4]]
    Result: [[4,6]]

POWER OPERATION:
    operation="power", array1=[[2,3]], array2=2
    Result: [[4,9]]

ARRAY DIVISION:
    operation="divide", array1=[[10,20],[30,40]], array2=[[2,4],[5,8]]
    Result: [[5,5],[6,5]] | `scripts.tools.array_operations` |
| Calculate statistical measures on arrays using Polars.

Supports computation across entire array, rows, or columns.

Examples:

COLUMN-WISE MEANS:
    data=[[1,2,3],[4,5,6]], operations=["mean"], axis=0
    Result: [2.5, 3.5, 4.5] (average of each column)

ROW-WISE MEANS:
    data=[[1,2,3],[4,5,6]], operations=["mean"], axis=1
    Result: [2.0, 5.0] (average of each row)

OVERALL STATISTICS:
    data=[[1,2,3],[4,5,6]], operations=["mean","std"], axis=None
    Result: {mean: 3.5, std: 1.71}

MULTIPLE STATISTICS:
    data=[[1,2,3],[4,5,6]], operations=["min","max","mean"], axis=0
    Result: {min: [1,2,3], max: [4,5,6], mean: [2.5,3.5,4.5]} | `scripts.tools.array_statistics` |
| Perform aggregation operations on 1D arrays.

Examples:

SUMPRODUCT:
    operation="sumproduct", array1=[1,2,3], array2=[4,5,6]
    Result: 32 (1×4 + 2×5 + 3×6)

WEIGHTED AVERAGE:
    operation="weighted_average", array1=[10,20,30], weights=[1,2,3]
    Result: 23.33... ((10×1 + 20×2 + 30×3) / (1+2+3))

DOT PRODUCT:
    operation="dot_product", array1=[1,2], array2=[3,4]
    Result: 11 (1×3 + 2×4)

GRADE CALCULATION:
    operation="weighted_average", array1=[85,92,78], weights=[0.3,0.5,0.2]
    Result: 86.5 | `scripts.tools.array_aggregate` |
| Transform arrays for ML preprocessing and data normalization.

Transformations:
    - normalize: L2 normalization (unit vector)
    - standardize: Z-score (mean=0, std=1)
    - minmax_scale: Scale to [0,1] range
    - log_transform: Natural log transform

Examples:

L2 NORMALIZATION:
    data=[[3,4]], transform="normalize"
    Result: [[0.6,0.8]] (3²+4²=25, √25=5, 3/5=0.6, 4/5=0.8)

STANDARDIZATION (Z-SCORE):
    data=[[1,2],[3,4]], transform="standardize"
    Result: Values with mean=0, std=1

MIN-MAX SCALING:
    data=[[1,2],[3,4]], transform="minmax_scale"
    Result: [[0,0.33],[0.67,1]] (scaled to [0,1])

LOG TRANSFORM:
    data=[[1,10,100]], transform="log_transform"
    Result: [[0,2.3,4.6]] (natural log) | `scripts.tools.array_transform` |
| Comprehensive statistical analysis using Polars.

Analysis types:
    - describe: Count, mean, std, min, max, median
    - quartiles: Q1, Q2, Q3, IQR
    - outliers: IQR-based detection (values beyond Q1-1.5×IQR or Q3+1.5×IQR)

Examples:

DESCRIPTIVE STATISTICS:
    data=[1,2,3,4,5,100], analyses=["describe"]
    Result: {count:6, mean:19.17, std:39.25, min:1, max:100, median:3.5}

QUARTILES:
    data=[1,2,3,4,5], analyses=["quartiles"]
    Result: {Q1:2, Q2:3, Q3:4, IQR:2}

OUTLIER DETECTION:
    data=[1,2,3,4,5,100], analyses=["outliers"]
    Result: {outlier_values:[100], outlier_count:1, lower_bound:-1, upper_bound:8.5}

FULL ANALYSIS:
    data=[1,2,3,4,5,100], analyses=["describe","quartiles","outliers"]
    Result: All three analyses combined | `scripts.tools.statistics` |
| Create pivot tables from tabular data using Polars.

Like Excel pivot tables: reshape data with row/column dimensions and aggregated values.

Example:

SALES BY REGION AND PRODUCT:
    data=[
        {"region":"North","product":"A","sales":100},
        {"region":"North","product":"B","sales":150},
        {"region":"South","product":"A","sales":80},
        {"region":"South","product":"B","sales":120}
    ],
    index="region", columns="product", values="sales", aggfunc="sum"
    Result:
        product |  A   |  B
        --------|------|------
        North   | 100  | 150
        South   |  80  | 120

COUNT AGGREGATION:
    Same data with aggfunc="count"
    Result: Count of entries per region-product combination

AVERAGE SCORES:
    data=[{"dept":"Sales","role":"Manager","score":85}, ...]
    index="dept", columns="role", values="score", aggfunc="mean"
    Result: Average scores by department and role | `scripts.tools.pivot_table` |
| Calculate correlation matrices between multiple variables using Polars.

Methods:
    - pearson: Linear correlation (-1 to +1, 0 = no linear relationship)
    - spearman: Rank-based correlation (monotonic, robust to outliers)

Examples:

PEARSON CORRELATION:
    data={"x":[1,2,3], "y":[2,4,6], "z":[1,1,1]},
    method="pearson", output_format="matrix"
    Result: {
        "x": {"x":1.0, "y":1.0, "z":NaN},
        "y": {"x":1.0, "y":1.0, "z":NaN},
        "z": {"x":NaN, "y":NaN, "z":NaN}
    }

PAIRWISE FORMAT:
    data={"height":[170,175,168], "weight":[65,78,62]},
    method="pearson", output_format="pairs"
    Result: [{"var1":"height", "var2":"weight", "correlation":0.89}]

SPEARMAN (RANK):
    data={"x":[1,2,100], "y":[2,4,200]},
    method="spearman"
    Result: Perfect correlation (1.0) despite non-linear relationship | `scripts.tools.correlation` |
| Time Value of Money (TVM) calculations: solve for PV, FV, PMT, rate, IRR, or NPV.

The TVM equation has 5 variables - know 4, solve for the 5th:
    PV  = Present Value (lump sum now)
    FV  = Future Value (lump sum at maturity)
    PMT = Payment (regular periodic cash flow)
    N   = Number of periods
    I/Y = Interest rate per period

Sign convention: negative = cash out (you pay), positive = cash in (you receive)

Examples:

ZERO-COUPON BOND: PV of £1000 in 10 years at 5%
    calculation="pv", rate=0.05, periods=10, future_value=1000
    Result: £613.91

COUPON BOND: PV of £30 annual coupons + £1000 face value at 5% yield
    calculation="pv", rate=0.05, periods=10, payment=30, future_value=1000
    Result: £845.57

RETIREMENT SAVINGS: FV with £500/month for 30 years at 7%
    calculation="fv", rate=0.07/12, periods=360, payment=-500, present_value=0
    Result: £566,764

MORTGAGE PAYMENT: Monthly payment on £200k loan, 30 years, 4% APR
    calculation="pmt", rate=0.04/12, periods=360, present_value=-200000, future_value=0
    Result: £954.83

INTEREST RATE: What rate grows £613.81 to £1000 in 10 years?
    calculation="rate", periods=10, present_value=-613.81, future_value=1000
    Result: 0.05 (5%)

GROWING ANNUITY: Salary stream with 3.5% raises, discounted at 12%
    calculation="pv", rate=0.12, periods=25, payment=-45000, growth_rate=0.035
    Result: £402,586 | `scripts.tools.financial_calcs` |
| Calculate compound interest with various compounding frequencies.

Formulas:
    Discrete: A = P(1 + r/n)^(nt)
    Continuous: A = Pe^(rt)

Examples:

ANNUAL COMPOUNDING: £1000 at 5% for 10 years
    principal=1000, rate=0.05, time=10, frequency="annual"
    Result: £1628.89

MONTHLY COMPOUNDING: £1000 at 5% for 10 years
    principal=1000, rate=0.05, time=10, frequency="monthly"
    Result: £1647.01

CONTINUOUS COMPOUNDING: £1000 at 5% for 10 years
    principal=1000, rate=0.05, time=10, frequency="continuous"
    Result: £1648.72 | `scripts.tools.compound_interest` |
| Calculate present value of a perpetuity (infinite series of payments).

A perpetuity is an annuity that continues forever. Common in:
    - Preferred stock dividends
    - Endowment funds
    - Real estate with infinite rental income
    - UK Consol bonds (historically)

Formulas:
    Level Ordinary: PV = C / r
    Level Due: PV = C / r × (1 + r)
    Growing: PV = C / (r - g), where r > g

Examples:

LEVEL PERPETUITY: £1000 annual payment at 5%
    payment=1000, rate=0.05
    Result: PV = £20,000

GROWING PERPETUITY: £1000 payment growing 3% annually at 8% discount
    payment=1000, rate=0.08, growth_rate=0.03
    Result: PV = £20,000

PERPETUITY DUE: £1000 at period start at 5%
    payment=1000, rate=0.05, when='begin'
    Result: PV = £21,000 | `scripts.tools.perpetuity` |
| Core matrix operations using NumPy BLAS.

Examples:

MATRIX MULTIPLICATION:
    operation="multiply", matrix1=[[1,2],[3,4]], matrix2=[[5,6],[7,8]]
    Result: [[19,22],[43,50]]

MATRIX INVERSE:
    operation="inverse", matrix1=[[1,2],[3,4]]
    Result: [[-2,1],[1.5,-0.5]]

TRANSPOSE:
    operation="transpose", matrix1=[[1,2],[3,4]]
    Result: [[1,3],[2,4]]

DETERMINANT:
    operation="determinant", matrix1=[[1,2],[3,4]]
    Result: -2.0

TRACE:
    operation="trace", matrix1=[[1,2],[3,4]]
    Result: 5.0 (1+4) | `scripts.tools.matrix_operations` |
| Solve systems of linear equations (Ax = b) using SciPy's optimised solver.

Examples:

SQUARE SYSTEM (2 equations, 2 unknowns):
    coefficients=[[2,3],[1,1]], constants=[8,3], method="direct"
    Solves: 2x+3y=8, x+y=3
    Result: [x=1, y=2]

OVERDETERMINED SYSTEM (3 equations, 2 unknowns):
    coefficients=[[1,2],[3,4],[5,6]], constants=[5,6,7], method="least_squares"
    Finds best-fit x minimizing ||Ax-b||
    Result: [x≈-6, y≈5.5]

3x3 SYSTEM:
    coefficients=[[2,1,-1],[1,3,2],[-1,2,1]], constants=[8,13,5], method="direct"
    Result: [x=3, y=2, z=1] | `scripts.tools.solve_linear_system` |
| Matrix decompositions: eigenvalues/vectors, SVD, QR, Cholesky, LU.

Examples:

EIGENVALUE DECOMPOSITION:
    matrix=[[4,2],[1,3]], decomposition="eigen"
    Result: {eigenvalues: [5, 2], eigenvectors: [[0.89,0.45],[0.71,-0.71]]}

SINGULAR VALUE DECOMPOSITION (SVD):
    matrix=[[1,2],[3,4],[5,6]], decomposition="svd"
    Result: {U: 3×3, singular_values: [9.5, 0.77], Vt: 2×2}

QR FACTORISATION:
    matrix=[[1,2],[3,4]], decomposition="qr"
    Result: {Q: orthogonal, R: upper triangular}

CHOLESKY (symmetric positive definite):
    matrix=[[4,2],[2,3]], decomposition="cholesky"
    Result: {L: [[2,0],[1,1.41]]} where A=LL^T

LU DECOMPOSITION:
    matrix=[[2,1],[4,3]], decomposition="lu"
    Result: {P: permutation, L: lower, U: upper} where A=PLU | `scripts.tools.matrix_decomposition` |
| Compute symbolic and numerical derivatives with support for higher orders and partial derivatives.

Examples:

FIRST DERIVATIVE:
    expression="x^3 + 2*x^2", variable="x", order=1
    Result: derivative="3*x^2 + 4*x"

SECOND DERIVATIVE (acceleration/concavity):
    expression="x^3", variable="x", order=2
    Result: derivative="6*x"

EVALUATE AT POINT:
    expression="sin(x)", variable="x", order=1, point=0
    Result: derivative="cos(x)", value_at_point=1.0

PRODUCT RULE:
    expression="sin(x)*cos(x)", variable="x", order=1
    Result: derivative="cos(x)^2 - sin(x)^2"

PARTIAL DERIVATIVE:
    expression="x^2*y", variable="y", order=1
    Result: derivative="x^2" (treating x as constant) | `scripts.tools.derivative` |
| Compute symbolic and numerical integrals (definite and indefinite).

Examples:

INDEFINITE INTEGRAL (antiderivative):
    expression="x^2", variable="x"
    Result: "x^3/3"

DEFINITE INTEGRAL (area):
    expression="x^2", variable="x", lower_bound=0, upper_bound=1
    Result: 0.333

TRIGONOMETRIC:
    expression="sin(x)", variable="x", lower_bound=0, upper_bound=3.14159
    Result: 2.0 (area under one period)

NUMERICAL METHOD (non-elementary):
    expression="exp(-x^2)", variable="x", lower_bound=0, upper_bound=1, method="numerical"
    Result: 0.746824 (Gaussian integral approximation)

SYMBOLIC ANTIDERIVATIVE:
    expression="1/x", variable="x"
    Result: "log(x)"  | `scripts.tools.integral` |
| Compute limits and series expansions using SymPy.

Examples:

CLASSIC LIMIT:
    expression="sin(x)/x", variable="x", point=0, operation="limit"
    Result: limit=1

LIMIT AT INFINITY:
    expression="1/x", variable="x", point="oo", operation="limit"
    Result: limit=0

ONE-SIDED LIMIT:
    expression="1/x", variable="x", point=0, operation="limit", direction="+"
    Result: limit=+∞ (approaching from right)

REMOVABLE DISCONTINUITY:
    expression="(x^2-1)/(x-1)", variable="x", point=1, operation="limit"
    Result: limit=2

MACLAURIN SERIES (at 0):
    expression="exp(x)", variable="x", point=0, operation="series", order=4
    Result: "1 + x + x^2/2 + x^3/6 + O(x^4)"

TAYLOR SERIES (at point):
    expression="sin(x)", variable="x", point=3.14159, operation="series", order=4
    Result: expansion around π | `scripts.tools.limits_series` |
| Execute multiple math operations in a single request with automatic dependency chaining.

**USE THIS TOOL when you need 2+ calculations where outputs feed into inputs** (bond pricing, statistical workflows, multi-step formulas). Don't make sequential individual tool calls.

Benefits: 90-95% token reduction, single API call, highly flexible workflows

## Quick Start

Available tools (20):
• Basic: calculate, percentage, round, convert_units
• Arrays: array_operations, array_statistics, array_aggregate, array_transform
• Statistics: statistics, pivot_table, correlation
• Financial: financial_calcs, compound_interest, perpetuity
• Linear Algebra: matrix_operations, solve_linear_system, matrix_decomposition
• Calculus: derivative, integral, limits_series

**Result referencing:**

Pass `$op_id.result` directly in any parameter:
- `$op_id.result` - Use output from prior operation
- `$op_id.result[0]` - Array indexing
- `$op_id.metadata.field` - Nested fields

Example: `"payment": "$coupon.result"` or `"variables": {"x": "$op1.result"}`

**Example - Bond valuation:**
```json
{
  "operations": [
    {"id": "coupon", "tool": "calculate",
     "context": "Calculate annual coupon payment",
     "arguments": {"expression": "principal * 0.04", "variables": {"principal": 8306623.86}}},
    {"id": "fv", "tool": "financial_calcs",
     "context": "Future value of coupon payments",
     "arguments": {"calculation": "fv", "rate": 0.04, "periods": 10,
                   "payment": "$coupon.result", "present_value": 0}},
    {"id": "total", "tool": "calculate",
     "context": "Total bond maturity value",
     "arguments": {"expression": "fv + principal",
                   "variables": {"fv": "$fv.result", "principal": 8306623.86}}}
  ],
  "execution_mode": "auto",
  "output_mode": "minimal",
  "context": "Bond A 10-year valuation"
}
```

## When to Use
✅ Multi-step calculations (financial models, statistics, transformations)
✅ Data pipelines where step N needs output from step N-1
✅ Any workflow requiring 2+ operations from the tools above

❌ Single standalone calculation
❌ Need to inspect/validate intermediate results before proceeding

## Execution Modes
- `auto` (recommended): DAG-based optimization, parallel where possible
- `sequential`: Strict order
- `parallel`: All concurrent (only if truly independent)

## Output Modes
- `full`: Complete metadata (default)
- `compact`: Remove nulls/whitespace
- `minimal`: Basic operation objects with values
- `value`: Flat {id: value} map (~90% smaller) - **use this for most cases**
- `final`: Sequential chains only, returns terminal result (~95% smaller)

## Structure
Each operation:
- `tool`: Tool name (required)
- `arguments`: Tool parameters (required)
- `id`: Unique identifier (auto-generated if omitted)
- `context`: Optional label for this operation

Batch-level `context` parameter labels entire workflow across all output modes.

Response includes: per-operation status, result/error, execution_time_ms, dependency wave, summary stats.
 | `scripts.tools.batch_execute` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.calculate
工具描述：Evaluate mathematical expressions using SymPy.

Supports:
    - Arithmetic: +, -, *, /, ^
    - Trigonometry: sin, cos, tan, asin, acos, atan
    - Logarithms: log, ln, exp
    - Constants: pi, e
    - Functions: sqrt, abs

Examples:

SIMPLE ARITHMETIC:
    expression="2 + 2"
    Result: 4

TRIGONOMETRY:
    expression="sin(pi/2)"
    Result: 1.0

WITH VARIABLES:
    expression="x^2 + 2*x + 1", variables={"x": 3}
    Result: 16

MULTIPLE VARIABLES:
    expression="x^2 + y^2", variables={"x": 3, "y": 4}
    Result: 25
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|expression|string|true| |Mathematical expression (e.g., '2+2', 'sin(pi/2)', 'x^2+1')|
|variables|null|false| |Variable substitutions (e.g., {'x': 5, 'y': 10})|

---

## scripts.tools.percentage
工具描述：Perform percentage calculations: of, increase, decrease, or change.

Examples:

PERCENTAGE OF: 15% of 200
    operation="of", value=200, percentage=15
    Result: 30

INCREASE: 100 increased by 20%
    operation="increase", value=100, percentage=20
    Result: 120

DECREASE: 100 decreased by 20%
    operation="decrease", value=100, percentage=20
    Result: 80

PERCENTAGE CHANGE: from 80 to 100
    operation="change", value=80, percentage=100
    Result: 25 (25% increase)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|operation|string|true| |Type of calculation|
|value|number|true| |Base value|
|percentage|number|true| |Percentage amount (or new value for 'change')|

---

## scripts.tools.round
工具描述：Advanced rounding operations with multiple methods.

Methods:
    - round: Round to nearest (3.145 → 3.15 at 2dp)
    - floor: Always round down (3.149 → 3.14)
    - ceil: Always round up (3.141 → 3.15)
    - trunc: Truncate towards zero (-3.7 → -3, 3.7 → 3)

Examples:

ROUND TO NEAREST:
    values=3.14159, method="round", decimals=2
    Result: 3.14

FLOOR (DOWN):
    values=3.14159, method="floor", decimals=2
    Result: 3.14

CEIL (UP):
    values=3.14159, method="ceil", decimals=2
    Result: 3.15

MULTIPLE VALUES:
    values=[3.14159, 2.71828], method="round", decimals=2
    Result: [3.14, 2.72]
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|values|null|true| |Single value or list (e.g., 3.14159 or [3.14, 2.71])|
|method|string|false|"round"|Rounding method|
|decimals|integer|false|0.0|Number of decimal places|

---

## scripts.tools.convert_units
工具描述：Convert between angle units: degrees ↔ radians.

Examples:

DEGREES TO RADIANS:
    value=180, from_unit="degrees", to_unit="radians"
    Result: 3.14159... (π)

RADIANS TO DEGREES:
    value=3.14159, from_unit="radians", to_unit="degrees"
    Result: 180

RIGHT ANGLE:
    value=90, from_unit="degrees", to_unit="radians"
    Result: 1.5708... (π/2)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|value|number|true| |Value to convert (e.g., 180, 3.14159)|
|from_unit|string|true| |Source unit|
|to_unit|string|true| |Target unit|

---

## scripts.tools.array_operations
工具描述：Perform element-wise operations on arrays using Polars.

Supports array-array and array-scalar operations.

Examples:

SCALAR MULTIPLICATION:
    operation="multiply", array1=[[1,2],[3,4]], array2=2
    Result: [[2,4],[6,8]]

ARRAY ADDITION:
    operation="add", array1=[[1,2]], array2=[[3,4]]
    Result: [[4,6]]

POWER OPERATION:
    operation="power", array1=[[2,3]], array2=2
    Result: [[4,9]]

ARRAY DIVISION:
    operation="divide", array1=[[10,20],[30,40]], array2=[[2,4],[5,8]]
    Result: [[5,5],[6,5]]
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|operation|string|true| |Element-wise operation to perform|
|array1|array|true| |First 2D array (e.g., [[1,2],[3,4]])|
|array2|null|true| |Second array, scalar, or JSON string|

---

## scripts.tools.array_statistics
工具描述：Calculate statistical measures on arrays using Polars.

Supports computation across entire array, rows, or columns.

Examples:

COLUMN-WISE MEANS:
    data=[[1,2,3],[4,5,6]], operations=["mean"], axis=0
    Result: [2.5, 3.5, 4.5] (average of each column)

ROW-WISE MEANS:
    data=[[1,2,3],[4,5,6]], operations=["mean"], axis=1
    Result: [2.0, 5.0] (average of each row)

OVERALL STATISTICS:
    data=[[1,2,3],[4,5,6]], operations=["mean","std"], axis=None
    Result: {mean: 3.5, std: 1.71}

MULTIPLE STATISTICS:
    data=[[1,2,3],[4,5,6]], operations=["min","max","mean"], axis=0
    Result: {min: [1,2,3], max: [4,5,6], mean: [2.5,3.5,4.5]}
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|data|array|true| |2D array (e.g., [[1,2,3],[4,5,6]])|
|operations|array|true| |Statistics to compute (e.g., ['mean','std'])|
|axis|null|false| |Axis: 0=column-wise, 1=row-wise, None=overall|

---

## scripts.tools.array_aggregate
工具描述：Perform aggregation operations on 1D arrays.

Examples:

SUMPRODUCT:
    operation="sumproduct", array1=[1,2,3], array2=[4,5,6]
    Result: 32 (1×4 + 2×5 + 3×6)

WEIGHTED AVERAGE:
    operation="weighted_average", array1=[10,20,30], weights=[1,2,3]
    Result: 23.33... ((10×1 + 20×2 + 30×3) / (1+2+3))

DOT PRODUCT:
    operation="dot_product", array1=[1,2], array2=[3,4]
    Result: 11 (1×3 + 2×4)

GRADE CALCULATION:
    operation="weighted_average", array1=[85,92,78], weights=[0.3,0.5,0.2]
    Result: 86.5
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|operation|string|true| |Aggregation operation|
|array1|array|true| |First 1D array (e.g., [1,2,3])|
|array2|null|false| |Second 1D array for sumproduct/dot_product|
|weights|null|false| |Weights for weighted_average (e.g., [1,2,3])|

---

## scripts.tools.array_transform
工具描述：Transform arrays for ML preprocessing and data normalization.

Transformations:
    - normalize: L2 normalization (unit vector)
    - standardize: Z-score (mean=0, std=1)
    - minmax_scale: Scale to [0,1] range
    - log_transform: Natural log transform

Examples:

L2 NORMALIZATION:
    data=[[3,4]], transform="normalize"
    Result: [[0.6,0.8]] (3²+4²=25, √25=5, 3/5=0.6, 4/5=0.8)

STANDARDIZATION (Z-SCORE):
    data=[[1,2],[3,4]], transform="standardize"
    Result: Values with mean=0, std=1

MIN-MAX SCALING:
    data=[[1,2],[3,4]], transform="minmax_scale"
    Result: [[0,0.33],[0.67,1]] (scaled to [0,1])

LOG TRANSFORM:
    data=[[1,10,100]], transform="log_transform"
    Result: [[0,2.3,4.6]] (natural log)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|data|array|true| |2D array to transform (e.g., [[1,2],[3,4]])|
|transform|string|true| |Transformation type|
|axis|null|false| |Axis: 0=column-wise, 1=row-wise, None=overall|

---

## scripts.tools.statistics
工具描述：Comprehensive statistical analysis using Polars.

Analysis types:
    - describe: Count, mean, std, min, max, median
    - quartiles: Q1, Q2, Q3, IQR
    - outliers: IQR-based detection (values beyond Q1-1.5×IQR or Q3+1.5×IQR)

Examples:

DESCRIPTIVE STATISTICS:
    data=[1,2,3,4,5,100], analyses=["describe"]
    Result: {count:6, mean:19.17, std:39.25, min:1, max:100, median:3.5}

QUARTILES:
    data=[1,2,3,4,5], analyses=["quartiles"]
    Result: {Q1:2, Q2:3, Q3:4, IQR:2}

OUTLIER DETECTION:
    data=[1,2,3,4,5,100], analyses=["outliers"]
    Result: {outlier_values:[100], outlier_count:1, lower_bound:-1, upper_bound:8.5}

FULL ANALYSIS:
    data=[1,2,3,4,5,100], analyses=["describe","quartiles","outliers"]
    Result: All three analyses combined
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|data|array|true| |List of numerical values (e.g., [1,2,3,4,5,100])|
|analyses|array|true| |Types of analysis to perform|

---

## scripts.tools.pivot_table
工具描述：Create pivot tables from tabular data using Polars.

Like Excel pivot tables: reshape data with row/column dimensions and aggregated values.

Example:

SALES BY REGION AND PRODUCT:
    data=[
        {"region":"North","product":"A","sales":100},
        {"region":"North","product":"B","sales":150},
        {"region":"South","product":"A","sales":80},
        {"region":"South","product":"B","sales":120}
    ],
    index="region", columns="product", values="sales", aggfunc="sum"
    Result:
        product |  A   |  B
        --------|------|------
        North   | 100  | 150
        South   |  80  | 120

COUNT AGGREGATION:
    Same data with aggfunc="count"
    Result: Count of entries per region-product combination

AVERAGE SCORES:
    data=[{"dept":"Sales","role":"Manager","score":85}, ...]
    index="dept", columns="role", values="score", aggfunc="mean"
    Result: Average scores by department and role
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|data|array|true| |List of row dictionaries|
|index|string|true| |Column name for row index|
|columns|string|true| |Column name for pivot columns|
|values|string|true| |Column name to aggregate|
|aggfunc|string|false|"sum"|Aggregation function|

---

## scripts.tools.correlation
工具描述：Calculate correlation matrices between multiple variables using Polars.

Methods:
    - pearson: Linear correlation (-1 to +1, 0 = no linear relationship)
    - spearman: Rank-based correlation (monotonic, robust to outliers)

Examples:

PEARSON CORRELATION:
    data={"x":[1,2,3], "y":[2,4,6], "z":[1,1,1]},
    method="pearson", output_format="matrix"
    Result: {
        "x": {"x":1.0, "y":1.0, "z":NaN},
        "y": {"x":1.0, "y":1.0, "z":NaN},
        "z": {"x":NaN, "y":NaN, "z":NaN}
    }

PAIRWISE FORMAT:
    data={"height":[170,175,168], "weight":[65,78,62]},
    method="pearson", output_format="pairs"
    Result: [{"var1":"height", "var2":"weight", "correlation":0.89}]

SPEARMAN (RANK):
    data={"x":[1,2,100], "y":[2,4,200]},
    method="spearman"
    Result: Perfect correlation (1.0) despite non-linear relationship
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|data|object|true| |Dict of variable names to values (e.g., {'x':[1,2,3],'y':[2,4,6]})|
|method|string|false|"pearson"|Correlation method|
|output_format|string|false|"matrix"|Output format: 'matrix' or 'pairs'|

---

## scripts.tools.financial_calcs
工具描述：Time Value of Money (TVM) calculations: solve for PV, FV, PMT, rate, IRR, or NPV.

The TVM equation has 5 variables - know 4, solve for the 5th:
    PV  = Present Value (lump sum now)
    FV  = Future Value (lump sum at maturity)
    PMT = Payment (regular periodic cash flow)
    N   = Number of periods
    I/Y = Interest rate per period

Sign convention: negative = cash out (you pay), positive = cash in (you receive)

Examples:

ZERO-COUPON BOND: PV of £1000 in 10 years at 5%
    calculation="pv", rate=0.05, periods=10, future_value=1000
    Result: £613.91

COUPON BOND: PV of £30 annual coupons + £1000 face value at 5% yield
    calculation="pv", rate=0.05, periods=10, payment=30, future_value=1000
    Result: £845.57

RETIREMENT SAVINGS: FV with £500/month for 30 years at 7%
    calculation="fv", rate=0.07/12, periods=360, payment=-500, present_value=0
    Result: £566,764

MORTGAGE PAYMENT: Monthly payment on £200k loan, 30 years, 4% APR
    calculation="pmt", rate=0.04/12, periods=360, present_value=-200000, future_value=0
    Result: £954.83

INTEREST RATE: What rate grows £613.81 to £1000 in 10 years?
    calculation="rate", periods=10, present_value=-613.81, future_value=1000
    Result: 0.05 (5%)

GROWING ANNUITY: Salary stream with 3.5% raises, discounted at 12%
    calculation="pv", rate=0.12, periods=25, payment=-45000, growth_rate=0.035
    Result: £402,586
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|calculation|string|true| |What to solve for: pv, fv, pmt, rate, irr, or npv|
|rate|null|false| |Interest/discount rate per period (e.g., 0.05 for 5% annual)|
|periods|null|false| |Number of compounding periods|
|payment|null|false| |Regular periodic payment (negative=pay out, positive=receive)|
|present_value|null|false| |Single lump sum at time 0 (negative=pay, positive=receive)|
|future_value|null|false| |Single lump sum at maturity (negative=owe, positive=receive)|
|cash_flows|null|false| |Series of cash flows for IRR/NPV (e.g., [-100, 30, 30, 130])|
|when|string|false|"end"|Payment timing: 'end' (ordinary) or 'begin' (annuity due)|
|growth_rate|number|false|0.0|Payment growth rate per period (0.0 for level annuity)|

---

## scripts.tools.compound_interest
工具描述：Calculate compound interest with various compounding frequencies.

Formulas:
    Discrete: A = P(1 + r/n)^(nt)
    Continuous: A = Pe^(rt)

Examples:

ANNUAL COMPOUNDING: £1000 at 5% for 10 years
    principal=1000, rate=0.05, time=10, frequency="annual"
    Result: £1628.89

MONTHLY COMPOUNDING: £1000 at 5% for 10 years
    principal=1000, rate=0.05, time=10, frequency="monthly"
    Result: £1647.01

CONTINUOUS COMPOUNDING: £1000 at 5% for 10 years
    principal=1000, rate=0.05, time=10, frequency="continuous"
    Result: £1648.72
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|principal|number|true| |Initial principal amount (e.g., 1000)|
|rate|number|true| |Annual interest rate (e.g., 0.05 for 5%)|
|time|number|true| |Time period in years (e.g., 10)|
|frequency|string|false|"annual"|Compounding frequency|

---

## scripts.tools.perpetuity
工具描述：Calculate present value of a perpetuity (infinite series of payments).

A perpetuity is an annuity that continues forever. Common in:
    - Preferred stock dividends
    - Endowment funds
    - Real estate with infinite rental income
    - UK Consol bonds (historically)

Formulas:
    Level Ordinary: PV = C / r
    Level Due: PV = C / r × (1 + r)
    Growing: PV = C / (r - g), where r > g

Examples:

LEVEL PERPETUITY: £1000 annual payment at 5%
    payment=1000, rate=0.05
    Result: PV = £20,000

GROWING PERPETUITY: £1000 payment growing 3% annually at 8% discount
    payment=1000, rate=0.08, growth_rate=0.03
    Result: PV = £20,000

PERPETUITY DUE: £1000 at period start at 5%
    payment=1000, rate=0.05, when='begin'
    Result: PV = £21,000
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|payment|number|true| |Periodic payment amount (e.g., 1000)|
|rate|number|true| |Discount rate per period (e.g., 0.05)|
|growth_rate|null|false| |Payment growth rate (None or 0 for level, e.g., 0.03 for growing)|
|when|string|false|"end"|Payment timing: 'end' or 'begin'|

---

## scripts.tools.matrix_operations
工具描述：Core matrix operations using NumPy BLAS.

Examples:

MATRIX MULTIPLICATION:
    operation="multiply", matrix1=[[1,2],[3,4]], matrix2=[[5,6],[7,8]]
    Result: [[19,22],[43,50]]

MATRIX INVERSE:
    operation="inverse", matrix1=[[1,2],[3,4]]
    Result: [[-2,1],[1.5,-0.5]]

TRANSPOSE:
    operation="transpose", matrix1=[[1,2],[3,4]]
    Result: [[1,3],[2,4]]

DETERMINANT:
    operation="determinant", matrix1=[[1,2],[3,4]]
    Result: -2.0

TRACE:
    operation="trace", matrix1=[[1,2],[3,4]]
    Result: 5.0 (1+4)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|operation|string|true| |Matrix operation|
|matrix1|array|true| |First matrix (e.g., [[1,2],[3,4]])|
|matrix2|null|false| |Second matrix for multiplication|

---

## scripts.tools.solve_linear_system
工具描述：Solve systems of linear equations (Ax = b) using SciPy's optimised solver.

Examples:

SQUARE SYSTEM (2 equations, 2 unknowns):
    coefficients=[[2,3],[1,1]], constants=[8,3], method="direct"
    Solves: 2x+3y=8, x+y=3
    Result: [x=1, y=2]

OVERDETERMINED SYSTEM (3 equations, 2 unknowns):
    coefficients=[[1,2],[3,4],[5,6]], constants=[5,6,7], method="least_squares"
    Finds best-fit x minimizing ||Ax-b||
    Result: [x≈-6, y≈5.5]

3x3 SYSTEM:
    coefficients=[[2,1,-1],[1,3,2],[-1,2,1]], constants=[8,13,5], method="direct"
    Result: [x=3, y=2, z=1]
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|coefficients|array|true| |Coefficient matrix A in Ax=b system (2D list, e.g., [[2,3],[1,1]])|
|constants|array|true| |Constants vector b in Ax=b system (1D list, e.g., [8,3])|
|method|string|false|"direct"|Solution method: direct=exact (square systems), least_squares=overdetermined systems|

---

## scripts.tools.matrix_decomposition
工具描述：Matrix decompositions: eigenvalues/vectors, SVD, QR, Cholesky, LU.

Examples:

EIGENVALUE DECOMPOSITION:
    matrix=[[4,2],[1,3]], decomposition="eigen"
    Result: {eigenvalues: [5, 2], eigenvectors: [[0.89,0.45],[0.71,-0.71]]}

SINGULAR VALUE DECOMPOSITION (SVD):
    matrix=[[1,2],[3,4],[5,6]], decomposition="svd"
    Result: {U: 3×3, singular_values: [9.5, 0.77], Vt: 2×2}

QR FACTORISATION:
    matrix=[[1,2],[3,4]], decomposition="qr"
    Result: {Q: orthogonal, R: upper triangular}

CHOLESKY (symmetric positive definite):
    matrix=[[4,2],[2,3]], decomposition="cholesky"
    Result: {L: [[2,0],[1,1.41]]} where A=LL^T

LU DECOMPOSITION:
    matrix=[[2,1],[4,3]], decomposition="lu"
    Result: {P: permutation, L: lower, U: upper} where A=PLU
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|matrix|array|true| |Matrix to decompose as 2D nested list (e.g., [[4,2],[1,3]])|
|decomposition|string|true| |Decomposition type: eigen=eigenvalues/vectors, svd=singular value, qr=QR, cholesky=symmetric positive definite, lu=LU factorisation|

---

## scripts.tools.derivative
工具描述：Compute symbolic and numerical derivatives with support for higher orders and partial derivatives.

Examples:

FIRST DERIVATIVE:
    expression="x^3 + 2*x^2", variable="x", order=1
    Result: derivative="3*x^2 + 4*x"

SECOND DERIVATIVE (acceleration/concavity):
    expression="x^3", variable="x", order=2
    Result: derivative="6*x"

EVALUATE AT POINT:
    expression="sin(x)", variable="x", order=1, point=0
    Result: derivative="cos(x)", value_at_point=1.0

PRODUCT RULE:
    expression="sin(x)*cos(x)", variable="x", order=1
    Result: derivative="cos(x)^2 - sin(x)^2"

PARTIAL DERIVATIVE:
    expression="x^2*y", variable="y", order=1
    Result: derivative="x^2" (treating x as constant)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|expression|string|true| |Mathematical expression to differentiate (e.g., 'x^3 + 2*x^2', 'sin(x)')|
|variable|string|true| |Variable to differentiate with respect to (e.g., 'x', 't')|
|order|integer|false|1.0|Derivative order (1=first derivative, 2=second, etc.)|
|point|null|false| |Optional point for numerical evaluation of the derivative|

---

## scripts.tools.integral
工具描述：Compute symbolic and numerical integrals (definite and indefinite).

Examples:

INDEFINITE INTEGRAL (antiderivative):
    expression="x^2", variable="x"
    Result: "x^3/3"

DEFINITE INTEGRAL (area):
    expression="x^2", variable="x", lower_bound=0, upper_bound=1
    Result: 0.333

TRIGONOMETRIC:
    expression="sin(x)", variable="x", lower_bound=0, upper_bound=3.14159
    Result: 2.0 (area under one period)

NUMERICAL METHOD (non-elementary):
    expression="exp(-x^2)", variable="x", lower_bound=0, upper_bound=1, method="numerical"
    Result: 0.746824 (Gaussian integral approximation)

SYMBOLIC ANTIDERIVATIVE:
    expression="1/x", variable="x"
    Result: "log(x)" 
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|expression|string|true| |Mathematical expression to integrate (e.g., 'x^2', 'sin(x)')|
|variable|string|true| |Integration variable (e.g., 'x', 't')|
|lower_bound|null|false| |Lower bound for definite integral (omit for indefinite)|
|upper_bound|null|false| |Upper bound for definite integral (omit for indefinite)|
|method|string|false|"symbolic"|Integration method: symbolic=exact/analytical, numerical=approximate (requires bounds)|

---

## scripts.tools.limits_series
工具描述：Compute limits and series expansions using SymPy.

Examples:

CLASSIC LIMIT:
    expression="sin(x)/x", variable="x", point=0, operation="limit"
    Result: limit=1

LIMIT AT INFINITY:
    expression="1/x", variable="x", point="oo", operation="limit"
    Result: limit=0

ONE-SIDED LIMIT:
    expression="1/x", variable="x", point=0, operation="limit", direction="+"
    Result: limit=+∞ (approaching from right)

REMOVABLE DISCONTINUITY:
    expression="(x^2-1)/(x-1)", variable="x", point=1, operation="limit"
    Result: limit=2

MACLAURIN SERIES (at 0):
    expression="exp(x)", variable="x", point=0, operation="series", order=4
    Result: "1 + x + x^2/2 + x^3/6 + O(x^4)"

TAYLOR SERIES (at point):
    expression="sin(x)", variable="x", point=3.14159, operation="series", order=4
    Result: expansion around π
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|expression|string|true| |Mathematical expression to analyse (e.g., 'sin(x)/x', 'exp(x)')|
|variable|string|true| |Variable for limit/expansion (e.g., 'x', 't')|
|point|null|true| |Point for limit/expansion (number, 'oo' for infinity, '-oo' for -infinity)|
|operation|string|false|"limit"|Operation: limit=compute limit, series=Taylor/Maclaurin expansion|
|order|integer|false|6.0|Series expansion order (number of terms)|
|direction|string|false|"+-"|Limit direction: +=from right, -=from left, +-=both sides|

---

## scripts.tools.batch_execute
工具描述：Execute multiple math operations in a single request with automatic dependency chaining.

**USE THIS TOOL when you need 2+ calculations where outputs feed into inputs** (bond pricing, statistical workflows, multi-step formulas). Don't make sequential individual tool calls.

Benefits: 90-95% token reduction, single API call, highly flexible workflows

## Quick Start

Available tools (20):
• Basic: calculate, percentage, round, convert_units
• Arrays: array_operations, array_statistics, array_aggregate, array_transform
• Statistics: statistics, pivot_table, correlation
• Financial: financial_calcs, compound_interest, perpetuity
• Linear Algebra: matrix_operations, solve_linear_system, matrix_decomposition
• Calculus: derivative, integral, limits_series

**Result referencing:**

Pass `$op_id.result` directly in any parameter:
- `$op_id.result` - Use output from prior operation
- `$op_id.result[0]` - Array indexing
- `$op_id.metadata.field` - Nested fields

Example: `"payment": "$coupon.result"` or `"variables": {"x": "$op1.result"}`

**Example - Bond valuation:**
```json
{
  "operations": [
    {"id": "coupon", "tool": "calculate",
     "context": "Calculate annual coupon payment",
     "arguments": {"expression": "principal * 0.04", "variables": {"principal": 8306623.86}}},
    {"id": "fv", "tool": "financial_calcs",
     "context": "Future value of coupon payments",
     "arguments": {"calculation": "fv", "rate": 0.04, "periods": 10,
                   "payment": "$coupon.result", "present_value": 0}},
    {"id": "total", "tool": "calculate",
     "context": "Total bond maturity value",
     "arguments": {"expression": "fv + principal",
                   "variables": {"fv": "$fv.result", "principal": 8306623.86}}}
  ],
  "execution_mode": "auto",
  "output_mode": "minimal",
  "context": "Bond A 10-year valuation"
}
```

## When to Use
✅ Multi-step calculations (financial models, statistics, transformations)
✅ Data pipelines where step N needs output from step N-1
✅ Any workflow requiring 2+ operations from the tools above

❌ Single standalone calculation
❌ Need to inspect/validate intermediate results before proceeding

## Execution Modes
- `auto` (recommended): DAG-based optimization, parallel where possible
- `sequential`: Strict order
- `parallel`: All concurrent (only if truly independent)

## Output Modes
- `full`: Complete metadata (default)
- `compact`: Remove nulls/whitespace
- `minimal`: Basic operation objects with values
- `value`: Flat {id: value} map (~90% smaller) - **use this for most cases**
- `final`: Sequential chains only, returns terminal result (~95% smaller)

## Structure
Each operation:
- `tool`: Tool name (required)
- `arguments`: Tool parameters (required)
- `id`: Unique identifier (auto-generated if omitted)
- `context`: Optional label for this operation

Batch-level `context` parameter labels entire workflow across all output modes.

Response includes: per-operation status, result/error, execution_time_ms, dependency wave, summary stats.

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context|null|false| |Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.|
|output_mode|string|false|"full"|Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.|
|operations|array|true| |List of operations to execute. Each operation MUST include: tool (name), arguments (dict). Optional: id (UUID/string), context, label, timeout_ms (int)|
|execution_mode|string|false|"auto"|Execution strategy: sequential (order), parallel (concurrent), auto (DAG-based)|
|max_concurrent|integer|false|5.0|Maximum concurrent operations (applies to parallel/auto modes)|
|stop_on_error|boolean|false|false|Whether to stop execution on first error. If False, independent operations continue even if others fail.|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据