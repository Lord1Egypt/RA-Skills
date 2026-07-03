from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def calculate(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    expression: str,
    variables: Optional[null] = None
) -> Dict[str, Any]:
    """
    Evaluate mathematical expressions using SymPy.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        expression: Mathematical expression (e.g., '2+2', 'sin(pi/2)', 'x^2+1')
        variables: Variable substitutions (e.g., {'x': 5, 'y': 10})
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "expression": expression,
        "variables": variables
    }
    
    return call_api("1777419075074051", "calculate", arguments)

def percentage(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    operation: str,
    value: float,
    percentage: float
) -> Dict[str, Any]:
    """
    Perform percentage calculations: of, increase, decrease, or change.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        operation: Type of calculation
        value: Base value
        percentage: Percentage amount (or new value for 'change')
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "operation": operation,
        "value": value,
        "percentage": percentage
    }
    
    return call_api("1777419075074051", "percentage", arguments)

def round(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    values: null,
    method: Optional[str] = "round",
    decimals: Optional[int] = 0.0
) -> Dict[str, Any]:
    """
    Advanced rounding operations with multiple methods.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        values: Single value or list (e.g., 3.14159 or [3.14, 2.71])
        method: Rounding method
        decimals: Number of decimal places
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "values": values,
        "method": method,
        "decimals": decimals
    }
    
    return call_api("1777419075074051", "round", arguments)

def convert_units(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    value: float,
    from_unit: str,
    to_unit: str
) -> Dict[str, Any]:
    """
    Convert between angle units: degrees ↔ radians.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        value: Value to convert (e.g., 180, 3.14159)
        from_unit: Source unit
        to_unit: Target unit
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit
    }
    
    return call_api("1777419075074051", "convert_units", arguments)

def array_operations(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    operation: str,
    array1: null,
    array2: null
) -> Dict[str, Any]:
    """
    Perform element-wise operations on arrays using Polars.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        operation: Element-wise operation to perform
        array1: First 2D array (e.g., [[1,2],[3,4]])
        array2: Second array, scalar, or JSON string
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "operation": operation,
        "array1": array1,
        "array2": array2
    }
    
    return call_api("1777419075074051", "array_operations", arguments)

def array_statistics(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    data: null,
    operations: null,
    axis: Optional[null] = None
) -> Dict[str, Any]:
    """
    Calculate statistical measures on arrays using Polars.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        data: 2D array (e.g., [[1,2,3],[4,5,6]])
        operations: Statistics to compute (e.g., ['mean','std'])
        axis: Axis: 0=column-wise, 1=row-wise, None=overall
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "data": data,
        "operations": operations,
        "axis": axis
    }
    
    return call_api("1777419075074051", "array_statistics", arguments)

def array_aggregate(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    operation: str,
    array1: null,
    array2: Optional[null] = None,
    weights: Optional[null] = None
) -> Dict[str, Any]:
    """
    Perform aggregation operations on 1D arrays.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        operation: Aggregation operation
        array1: First 1D array (e.g., [1,2,3])
        array2: Second 1D array for sumproduct/dot_product
        weights: Weights for weighted_average (e.g., [1,2,3])
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "operation": operation,
        "array1": array1,
        "array2": array2,
        "weights": weights
    }
    
    return call_api("1777419075074051", "array_aggregate", arguments)

def array_transform(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    data: null,
    transform: str,
    axis: Optional[null] = None
) -> Dict[str, Any]:
    """
    Transform arrays for ML preprocessing and data normalization.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        data: 2D array to transform (e.g., [[1,2],[3,4]])
        transform: Transformation type
        axis: Axis: 0=column-wise, 1=row-wise, None=overall
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "data": data,
        "transform": transform,
        "axis": axis
    }
    
    return call_api("1777419075074051", "array_transform", arguments)

def statistics(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    data: null,
    analyses: null
) -> Dict[str, Any]:
    """
    Comprehensive statistical analysis using Polars.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        data: List of numerical values (e.g., [1,2,3,4,5,100])
        analyses: Types of analysis to perform
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "data": data,
        "analyses": analyses
    }
    
    return call_api("1777419075074051", "statistics", arguments)

def pivot_table(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    data: null,
    index: str,
    columns: str,
    values: str,
    aggfunc: Optional[str] = "sum"
) -> Dict[str, Any]:
    """
    Create pivot tables from tabular data using Polars.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        data: List of row dictionaries
        index: Column name for row index
        columns: Column name for pivot columns
        values: Column name to aggregate
        aggfunc: Aggregation function
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "data": data,
        "index": index,
        "columns": columns,
        "values": values,
        "aggfunc": aggfunc
    }
    
    return call_api("1777419075074051", "pivot_table", arguments)

def correlation(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    data: null,
    method: Optional[str] = "pearson",
    output_format: Optional[str] = "matrix"
) -> Dict[str, Any]:
    """
    Calculate correlation matrices between multiple variables using Polars.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        data: Dict of variable names to values (e.g., {'x':[1,2,3],'y':[2,4,6]})
        method: Correlation method
        output_format: Output format: 'matrix' or 'pairs'
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "data": data,
        "method": method,
        "output_format": output_format
    }
    
    return call_api("1777419075074051", "correlation", arguments)

def financial_calcs(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    calculation: str,
    rate: Optional[null] = None,
    periods: Optional[null] = None,
    payment: Optional[null] = None,
    present_value: Optional[null] = None,
    future_value: Optional[null] = None,
    cash_flows: Optional[null] = None,
    when: Optional[str] = "end",
    growth_rate: Optional[float] = 0.0
) -> Dict[str, Any]:
    """
    Time Value of Money (TVM) calculations: solve for PV, FV, PMT, rate, IRR, or NPV.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        calculation: What to solve for: pv, fv, pmt, rate, irr, or npv
        rate: Interest/discount rate per period (e.g., 0.05 for 5% annual)
        periods: Number of compounding periods
        payment: Regular periodic payment (negative=pay out, positive=receive)
        present_value: Single lump sum at time 0 (negative=pay, positive=receive)
        future_value: Single lump sum at maturity (negative=owe, positive=receive)
        cash_flows: Series of cash flows for IRR/NPV (e.g., [-100, 30, 30, 130])
        when: Payment timing: 'end' (ordinary) or 'begin' (annuity due)
        growth_rate: Payment growth rate per period (0.0 for level annuity)
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "calculation": calculation,
        "rate": rate,
        "periods": periods,
        "payment": payment,
        "present_value": present_value,
        "future_value": future_value,
        "cash_flows": cash_flows,
        "when": when,
        "growth_rate": growth_rate
    }
    
    return call_api("1777419075074051", "financial_calcs", arguments)

def compound_interest(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    principal: float,
    rate: float,
    time: float,
    frequency: Optional[str] = "annual"
) -> Dict[str, Any]:
    """
    Calculate compound interest with various compounding frequencies.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        principal: Initial principal amount (e.g., 1000)
        rate: Annual interest rate (e.g., 0.05 for 5%)
        time: Time period in years (e.g., 10)
        frequency: Compounding frequency
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "principal": principal,
        "rate": rate,
        "time": time,
        "frequency": frequency
    }
    
    return call_api("1777419075074051", "compound_interest", arguments)

def perpetuity(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    payment: float,
    rate: float,
    growth_rate: Optional[null] = None,
    when: Optional[str] = "end"
) -> Dict[str, Any]:
    """
    Calculate present value of a perpetuity (infinite series of payments).

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        payment: Periodic payment amount (e.g., 1000)
        rate: Discount rate per period (e.g., 0.05)
        growth_rate: Payment growth rate (None or 0 for level, e.g., 0.03 for growing)
        when: Payment timing: 'end' or 'begin'
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "payment": payment,
        "rate": rate,
        "growth_rate": growth_rate,
        "when": when
    }
    
    return call_api("1777419075074051", "perpetuity", arguments)

def matrix_operations(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    operation: str,
    matrix1: null,
    matrix2: Optional[null] = None
) -> Dict[str, Any]:
    """
    Core matrix operations using NumPy BLAS.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        operation: Matrix operation
        matrix1: First matrix (e.g., [[1,2],[3,4]])
        matrix2: Second matrix for multiplication
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "operation": operation,
        "matrix1": matrix1,
        "matrix2": matrix2
    }
    
    return call_api("1777419075074051", "matrix_operations", arguments)

def solve_linear_system(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    coefficients: null,
    constants: null,
    method: Optional[str] = "direct"
) -> Dict[str, Any]:
    """
    Solve systems of linear equations (Ax = b) using SciPy's optimised solver.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        coefficients: Coefficient matrix A in Ax=b system (2D list, e.g., [[2,3],[1,1]])
        constants: Constants vector b in Ax=b system (1D list, e.g., [8,3])
        method: Solution method: direct=exact (square systems), least_squares=overdetermined systems
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "coefficients": coefficients,
        "constants": constants,
        "method": method
    }
    
    return call_api("1777419075074051", "solve_linear_system", arguments)

def matrix_decomposition(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    matrix: null,
    decomposition: str
) -> Dict[str, Any]:
    """
    Matrix decompositions: eigenvalues/vectors, SVD, QR, Cholesky, LU.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        matrix: Matrix to decompose as 2D nested list (e.g., [[4,2],[1,3]])
        decomposition: Decomposition type: eigen=eigenvalues/vectors, svd=singular value, qr=QR, cholesky=symmetric positive definite, lu=LU factorisation
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "matrix": matrix,
        "decomposition": decomposition
    }
    
    return call_api("1777419075074051", "matrix_decomposition", arguments)

def derivative(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    expression: str,
    variable: str,
    order: Optional[int] = 1.0,
    point: Optional[null] = None
) -> Dict[str, Any]:
    """
    Compute symbolic and numerical derivatives with support for higher orders and partial derivatives.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        expression: Mathematical expression to differentiate (e.g., 'x^3 + 2*x^2', 'sin(x)')
        variable: Variable to differentiate with respect to (e.g., 'x', 't')
        order: Derivative order (1=first derivative, 2=second, etc.)
        point: Optional point for numerical evaluation of the derivative
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "expression": expression,
        "variable": variable,
        "order": order,
        "point": point
    }
    
    return call_api("1777419075074051", "derivative", arguments)

def integral(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    expression: str,
    variable: str,
    lower_bound: Optional[null] = None,
    upper_bound: Optional[null] = None,
    method: Optional[str] = "symbolic"
) -> Dict[str, Any]:
    """
    Compute symbolic and numerical integrals (definite and indefinite).

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        expression: Mathematical expression to integrate (e.g., 'x^2', 'sin(x)')
        variable: Integration variable (e.g., 'x', 't')
        lower_bound: Lower bound for definite integral (omit for indefinite)
        upper_bound: Upper bound for definite integral (omit for indefinite)
        method: Integration method: symbolic=exact/analytical, numerical=approximate (requires bounds)
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "expression": expression,
        "variable": variable,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "method": method
    }
    
    return call_api("1777419075074051", "integral", arguments)

def limits_series(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    expression: str,
    variable: str,
    point: null,
    operation: Optional[str] = "limit",
    order: Optional[int] = 6.0,
    direction: Optional[str] = "+-"
) -> Dict[str, Any]:
    """
    Compute limits and series expansions using SymPy.

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
    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        expression: Mathematical expression to analyse (e.g., 'sin(x)/x', 'exp(x)')
        variable: Variable for limit/expansion (e.g., 'x', 't')
        point: Point for limit/expansion (number, 'oo' for infinity, '-oo' for -infinity)
        operation: Operation: limit=compute limit, series=Taylor/Maclaurin expansion
        order: Series expansion order (number of terms)
        direction: Limit direction: +=from right, -=from left, +-=both sides
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "expression": expression,
        "variable": variable,
        "point": point,
        "operation": operation,
        "order": order,
        "direction": direction
    }
    
    return call_api("1777419075074051", "limits_series", arguments)

def batch_execute(
    context: Optional[null] = None,
    output_mode: Optional[str] = "full",
    operations: null,
    execution_mode: Optional[str] = "auto",
    max_concurrent: Optional[int] = 5.0,
    stop_on_error: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Execute multiple math operations in a single request with automatic dependency chaining.

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

    
    Args:
        context: Optional annotation to label this calculation (e.g., 'Bond A PV', 'Q2 revenue'). Appears in results for easy identification.
        output_mode: Output format: full (default), compact, minimal, value, or final. See batch_execute tool for details.
        operations: List of operations to execute. Each operation MUST include: tool (name), arguments (dict). Optional: id (UUID/string), context, label, timeout_ms (int)
        execution_mode: Execution strategy: sequential (order), parallel (concurrent), auto (DAG-based)
        max_concurrent: Maximum concurrent operations (applies to parallel/auto modes)
        stop_on_error: Whether to stop execution on first error. If False, independent operations continue even if others fail.
    
    Returns:
        null
    """
    arguments = {
        "context": context,
        "output_mode": output_mode,
        "operations": operations,
        "execution_mode": execution_mode,
        "max_concurrent": max_concurrent,
        "stop_on_error": stop_on_error
    }
    
    return call_api("1777419075074051", "batch_execute", arguments)

