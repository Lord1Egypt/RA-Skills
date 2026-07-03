from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def add(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    执行两个数字的加法运算
    
    Args:
        a: 第一个数字
        b: 第二个数字
    
    Returns:
        
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777316659204099", "add", arguments)

def subtract(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    执行两个数字的减法运算
    
    Args:
        a: 被减数
        b: 减数
    
    Returns:
        
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777316659204099", "subtract", arguments)

def multiply(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    执行两个数字的乘法运算
    
    Args:
        a: 第一个数字
        b: 第二个数字
    
    Returns:
        
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777316659204099", "multiply", arguments)

def divide(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    执行两个数字的除法运算
    
    Args:
        a: 被除数
        b: 除数
    
    Returns:
        
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777316659204099", "divide", arguments)

def modulo(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    计算两个数的余数
    
    Args:
        a: 被除数
        b: 除数
    
    Returns:
        
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777316659204099", "modulo", arguments)

def power(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    计算a的b次方
    
    Args:
        a: 底数
        b: 指数
    
    Returns:
        
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777316659204099", "power", arguments)

def sqrt(
    a: float
) -> Dict[str, Any]:
    """
    计算数字的平方根
    
    Args:
        a: 被开方数
    
    Returns:
        
    """
    arguments = {
        "a": a
    }
    
    return call_api("1777316659204099", "sqrt", arguments)

def cbrt(
    a: float
) -> Dict[str, Any]:
    """
    计算数字的立方根
    
    Args:
        a: 被开方数
    
    Returns:
        
    """
    arguments = {
        "a": a
    }
    
    return call_api("1777316659204099", "cbrt", arguments)

def nthRoot(
    a: float,
    n: float
) -> Dict[str, Any]:
    """
    计算数字的n次方根
    
    Args:
        a: 被开方数
        n: 开方次数
    
    Returns:
        
    """
    arguments = {
        "a": a,
        "n": n
    }
    
    return call_api("1777316659204099", "nthRoot", arguments)

def abs(
    a: float
) -> Dict[str, Any]:
    """
    计算数字的绝对值
    
    Args:
        a: 数字
    
    Returns:
        
    """
    arguments = {
        "a": a
    }
    
    return call_api("1777316659204099", "abs", arguments)

def sin(
    angle: float
) -> Dict[str, Any]:
    """
    计算角度的正弦值（输入为弧度）
    
    Args:
        angle: 角度（弧度）
    
    Returns:
        
    """
    arguments = {
        "angle": angle
    }
    
    return call_api("1777316659204099", "sin", arguments)

def cos(
    angle: float
) -> Dict[str, Any]:
    """
    计算角度的余弦值（输入为弧度）
    
    Args:
        angle: 角度（弧度）
    
    Returns:
        
    """
    arguments = {
        "angle": angle
    }
    
    return call_api("1777316659204099", "cos", arguments)

def tan(
    angle: float
) -> Dict[str, Any]:
    """
    计算角度的正切值（输入为弧度）
    
    Args:
        angle: 角度（弧度）
    
    Returns:
        
    """
    arguments = {
        "angle": angle
    }
    
    return call_api("1777316659204099", "tan", arguments)

def asin(
    value: float
) -> Dict[str, Any]:
    """
    计算反正弦值（返回弧度）
    
    Args:
        value: 输入值（-1到1之间）
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777316659204099", "asin", arguments)

def acos(
    value: float
) -> Dict[str, Any]:
    """
    计算反余弦值（返回弧度）
    
    Args:
        value: 输入值（-1到1之间）
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777316659204099", "acos", arguments)

def atan(
    value: float
) -> Dict[str, Any]:
    """
    计算反正切值（返回弧度）
    
    Args:
        value: 输入值
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777316659204099", "atan", arguments)

def atan2(
    y: float,
    x: float
) -> Dict[str, Any]:
    """
    计算从x轴到点(x,y)的角度（返回弧度）
    
    Args:
        y: y坐标
        x: x坐标
    
    Returns:
        
    """
    arguments = {
        "y": y,
        "x": x
    }
    
    return call_api("1777316659204099", "atan2", arguments)

def sinh(
    value: float
) -> Dict[str, Any]:
    """
    计算双曲正弦值
    
    Args:
        value: 输入值
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777316659204099", "sinh", arguments)

def cosh(
    value: float
) -> Dict[str, Any]:
    """
    计算双曲余弦值
    
    Args:
        value: 输入值
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777316659204099", "cosh", arguments)

def tanh(
    value: float
) -> Dict[str, Any]:
    """
    计算双曲正切值
    
    Args:
        value: 输入值
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777316659204099", "tanh", arguments)

def asinh(
    value: float
) -> Dict[str, Any]:
    """
    计算反双曲正弦值
    
    Args:
        value: 输入值
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777316659204099", "asinh", arguments)

def acosh(
    value: float
) -> Dict[str, Any]:
    """
    计算反双曲余弦值（输入值必须≥1）
    
    Args:
        value: 输入值（≥1）
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777316659204099", "acosh", arguments)

def atanh(
    value: float
) -> Dict[str, Any]:
    """
    计算反双曲正切值（输入值必须在-1到1之间）
    
    Args:
        value: 输入值（-1到1之间）
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777316659204099", "atanh", arguments)

def sec(
    angle: float
) -> Dict[str, Any]:
    """
    计算正割值（1/cos）
    
    Args:
        angle: 角度（弧度）
    
    Returns:
        
    """
    arguments = {
        "angle": angle
    }
    
    return call_api("1777316659204099", "sec", arguments)

def csc(
    angle: float
) -> Dict[str, Any]:
    """
    计算余割值（1/sin）
    
    Args:
        angle: 角度（弧度）
    
    Returns:
        
    """
    arguments = {
        "angle": angle
    }
    
    return call_api("1777316659204099", "csc", arguments)

def cot(
    angle: float
) -> Dict[str, Any]:
    """
    计算余切值（1/tan）
    
    Args:
        angle: 角度（弧度）
    
    Returns:
        
    """
    arguments = {
        "angle": angle
    }
    
    return call_api("1777316659204099", "cot", arguments)

def degToRad(
    degrees: float
) -> Dict[str, Any]:
    """
    将角度转换为弧度
    
    Args:
        degrees: 角度值
    
    Returns:
        
    """
    arguments = {
        "degrees": degrees
    }
    
    return call_api("1777316659204099", "degToRad", arguments)

def radToDeg(
    radians: float
) -> Dict[str, Any]:
    """
    将弧度转换为角度
    
    Args:
        radians: 弧度值
    
    Returns:
        
    """
    arguments = {
        "radians": radians
    }
    
    return call_api("1777316659204099", "radToDeg", arguments)

def ln(
    value: float
) -> Dict[str, Any]:
    """
    计算自然对数（以e为底）
    
    Args:
        value: 输入值（必须大于0）
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777316659204099", "ln", arguments)

def log10(
    value: float
) -> Dict[str, Any]:
    """
    计算以10为底的对数
    
    Args:
        value: 输入值（必须大于0）
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777316659204099", "log10", arguments)

def log(
    value: float,
    base: float
) -> Dict[str, Any]:
    """
    计算以指定底数的对数
    
    Args:
        value: 输入值（必须大于0）
        base: 底数（必须大于0且不等于1）
    
    Returns:
        
    """
    arguments = {
        "value": value,
        "base": base
    }
    
    return call_api("1777316659204099", "log", arguments)

def mean(
    numbers: null
) -> Dict[str, Any]:
    """
    计算数组的算术平均值
    
    Args:
        numbers: 数字数组
    
    Returns:
        
    """
    arguments = {
        "numbers": numbers
    }
    
    return call_api("1777316659204099", "mean", arguments)

def median(
    numbers: null
) -> Dict[str, Any]:
    """
    计算数组的中位数
    
    Args:
        numbers: 数字数组
    
    Returns:
        
    """
    arguments = {
        "numbers": numbers
    }
    
    return call_api("1777316659204099", "median", arguments)

def mode(
    numbers: null
) -> Dict[str, Any]:
    """
    计算数组的众数（出现频率最高的数）
    
    Args:
        numbers: 数字数组
    
    Returns:
        
    """
    arguments = {
        "numbers": numbers
    }
    
    return call_api("1777316659204099", "mode", arguments)

def stdDev(
    numbers: null,
    sample: Optional[bool] = None
) -> Dict[str, Any]:
    """
    计算数组的标准差
    
    Args:
        numbers: 数字数组
        sample: 是否为样本标准差（默认为总体标准差）
    
    Returns:
        
    """
    arguments = {
        "numbers": numbers,
        "sample": sample
    }
    
    return call_api("1777316659204099", "stdDev", arguments)

def variance(
    numbers: null,
    sample: Optional[bool] = None
) -> Dict[str, Any]:
    """
    计算数组的方差
    
    Args:
        numbers: 数字数组
        sample: 是否为样本方差（默认为总体方差）
    
    Returns:
        
    """
    arguments = {
        "numbers": numbers,
        "sample": sample
    }
    
    return call_api("1777316659204099", "variance", arguments)

def max(
    numbers: null
) -> Dict[str, Any]:
    """
    找出数组中的最大值
    
    Args:
        numbers: 数字数组
    
    Returns:
        
    """
    arguments = {
        "numbers": numbers
    }
    
    return call_api("1777316659204099", "max", arguments)

def min(
    numbers: null
) -> Dict[str, Any]:
    """
    找出数组中的最小值
    
    Args:
        numbers: 数字数组
    
    Returns:
        
    """
    arguments = {
        "numbers": numbers
    }
    
    return call_api("1777316659204099", "min", arguments)

def sum(
    numbers: null
) -> Dict[str, Any]:
    """
    计算数组所有元素的和
    
    Args:
        numbers: 数字数组
    
    Returns:
        
    """
    arguments = {
        "numbers": numbers
    }
    
    return call_api("1777316659204099", "sum", arguments)

def product(
    numbers: null
) -> Dict[str, Any]:
    """
    计算数组所有元素的乘积
    
    Args:
        numbers: 数字数组
    
    Returns:
        
    """
    arguments = {
        "numbers": numbers
    }
    
    return call_api("1777316659204099", "product", arguments)

def range(
    numbers: null
) -> Dict[str, Any]:
    """
    计算数组的范围（最大值-最小值）
    
    Args:
        numbers: 数字数组
    
    Returns:
        
    """
    arguments = {
        "numbers": numbers
    }
    
    return call_api("1777316659204099", "range", arguments)

def factorial(
    n: int
) -> Dict[str, Any]:
    """
    计算非负整数的阶乘
    
    Args:
        n: 非负整数
    
    Returns:
        
    """
    arguments = {
        "n": n
    }
    
    return call_api("1777316659204099", "factorial", arguments)

def permutation(
    n: int,
    r: int
) -> Dict[str, Any]:
    """
    计算从n个元素中选择r个元素的排列数 P(n,r)
    
    Args:
        n: 总元素数
        r: 选择元素数
    
    Returns:
        
    """
    arguments = {
        "n": n,
        "r": r
    }
    
    return call_api("1777316659204099", "permutation", arguments)

def combination(
    n: int,
    r: int
) -> Dict[str, Any]:
    """
    计算从n个元素中选择r个元素的组合数 C(n,r)
    
    Args:
        n: 总元素数
        r: 选择元素数
    
    Returns:
        
    """
    arguments = {
        "n": n,
        "r": r
    }
    
    return call_api("1777316659204099", "combination", arguments)

def fibonacci(
    n: int
) -> Dict[str, Any]:
    """
    计算斐波那契数列的第n项
    
    Args:
        n: 项数（从0开始）
    
    Returns:
        
    """
    arguments = {
        "n": n
    }
    
    return call_api("1777316659204099", "fibonacci", arguments)

def fibonacciSequence(
    n: int
) -> Dict[str, Any]:
    """
    生成斐波那契数列的前n项
    
    Args:
        n: 生成项数（1-100）
    
    Returns:
        
    """
    arguments = {
        "n": n
    }
    
    return call_api("1777316659204099", "fibonacciSequence", arguments)

def catalan(
    n: int
) -> Dict[str, Any]:
    """
    计算第n个卡塔兰数
    
    Args:
        n: 项数（0-35）
    
    Returns:
        
    """
    arguments = {
        "n": n
    }
    
    return call_api("1777316659204099", "catalan", arguments)

def bellNumber(
    n: int
) -> Dict[str, Any]:
    """
    计算第n个贝尔数（集合划分数）
    
    Args:
        n: 项数（0-15）
    
    Returns:
        
    """
    arguments = {
        "n": n
    }
    
    return call_api("1777316659204099", "bellNumber", arguments)

def binomialCoefficient(
    n: int,
    k: int
) -> Dict[str, Any]:
    """
    计算二项式系数 (n choose k)
    
    Args:
        n: 上标
        k: 下标
    
    Returns:
        
    """
    arguments = {
        "n": n,
        "k": k
    }
    
    return call_api("1777316659204099", "binomialCoefficient", arguments)

def gcd(
    numbers: null
) -> Dict[str, Any]:
    """
    计算两个或多个整数的最大公约数
    
    Args:
        numbers: 整数数组（至少2个数）
    
    Returns:
        
    """
    arguments = {
        "numbers": numbers
    }
    
    return call_api("1777316659204099", "gcd", arguments)

def lcm(
    numbers: null
) -> Dict[str, Any]:
    """
    计算两个或多个整数的最小公倍数
    
    Args:
        numbers: 整数数组（至少2个数）
    
    Returns:
        
    """
    arguments = {
        "numbers": numbers
    }
    
    return call_api("1777316659204099", "lcm", arguments)

def isPrime(
    n: int
) -> Dict[str, Any]:
    """
    判断一个正整数是否为素数
    
    Args:
        n: 正整数
    
    Returns:
        
    """
    arguments = {
        "n": n
    }
    
    return call_api("1777316659204099", "isPrime", arguments)

def primeFactorization(
    n: int
) -> Dict[str, Any]:
    """
    将正整数分解为素因数的乘积
    
    Args:
        n: 大于1的正整数
    
    Returns:
        
    """
    arguments = {
        "n": n
    }
    
    return call_api("1777316659204099", "primeFactorization", arguments)

def eulerPhi(
    n: int
) -> Dict[str, Any]:
    """
    计算欧拉函数φ(n)，即小于等于n且与n互质的正整数个数
    
    Args:
        n: 正整数
    
    Returns:
        
    """
    arguments = {
        "n": n
    }
    
    return call_api("1777316659204099", "eulerPhi", arguments)

def isPerfectNumber(
    n: int
) -> Dict[str, Any]:
    """
    判断一个正整数是否为完全数（等于其所有真因子之和）
    
    Args:
        n: 正整数
    
    Returns:
        
    """
    arguments = {
        "n": n
    }
    
    return call_api("1777316659204099", "isPerfectNumber", arguments)

def divisorCount(
    n: int
) -> Dict[str, Any]:
    """
    计算正整数的因子个数
    
    Args:
        n: 正整数
    
    Returns:
        
    """
    arguments = {
        "n": n
    }
    
    return call_api("1777316659204099", "divisorCount", arguments)

def divisorList(
    n: int
) -> Dict[str, Any]:
    """
    列出正整数的所有因子
    
    Args:
        n: 正整数（1-10000）
    
    Returns:
        
    """
    arguments = {
        "n": n
    }
    
    return call_api("1777316659204099", "divisorList", arguments)

def complex_add(
    a_real: float,
    a_imag: float,
    b_real: float,
    b_imag: float
) -> Dict[str, Any]:
    """
    计算两个复数的和
    
    Args:
        a_real: 第一个复数的实部
        a_imag: 第一个复数的虚部
        b_real: 第二个复数的实部
        b_imag: 第二个复数的虚部
    
    Returns:
        
    """
    arguments = {
        "a_real": a_real,
        "a_imag": a_imag,
        "b_real": b_real,
        "b_imag": b_imag
    }
    
    return call_api("1777316659204099", "complex_add", arguments)

def complex_subtract(
    a_real: float,
    a_imag: float,
    b_real: float,
    b_imag: float
) -> Dict[str, Any]:
    """
    计算两个复数的差
    
    Args:
        a_real: 第一个复数的实部
        a_imag: 第一个复数的虚部
        b_real: 第二个复数的实部
        b_imag: 第二个复数的虚部
    
    Returns:
        
    """
    arguments = {
        "a_real": a_real,
        "a_imag": a_imag,
        "b_real": b_real,
        "b_imag": b_imag
    }
    
    return call_api("1777316659204099", "complex_subtract", arguments)

def complex_multiply(
    a_real: float,
    a_imag: float,
    b_real: float,
    b_imag: float
) -> Dict[str, Any]:
    """
    计算两个复数的乘积
    
    Args:
        a_real: 第一个复数的实部
        a_imag: 第一个复数的虚部
        b_real: 第二个复数的实部
        b_imag: 第二个复数的虚部
    
    Returns:
        
    """
    arguments = {
        "a_real": a_real,
        "a_imag": a_imag,
        "b_real": b_real,
        "b_imag": b_imag
    }
    
    return call_api("1777316659204099", "complex_multiply", arguments)

def complex_divide(
    a_real: float,
    a_imag: float,
    b_real: float,
    b_imag: float
) -> Dict[str, Any]:
    """
    计算两个复数的商
    
    Args:
        a_real: 被除数的实部
        a_imag: 被除数的虚部
        b_real: 除数的实部
        b_imag: 除数的虚部
    
    Returns:
        
    """
    arguments = {
        "a_real": a_real,
        "a_imag": a_imag,
        "b_real": b_real,
        "b_imag": b_imag
    }
    
    return call_api("1777316659204099", "complex_divide", arguments)

def complex_magnitude(
    real: float,
    imag: float
) -> Dict[str, Any]:
    """
    计算复数的模长（绝对值）
    
    Args:
        real: 复数的实部
        imag: 复数的虚部
    
    Returns:
        
    """
    arguments = {
        "real": real,
        "imag": imag
    }
    
    return call_api("1777316659204099", "complex_magnitude", arguments)

def complex_conjugate(
    real: float,
    imag: float
) -> Dict[str, Any]:
    """
    计算复数的共轭
    
    Args:
        real: 复数的实部
        imag: 复数的虚部
    
    Returns:
        
    """
    arguments = {
        "real": real,
        "imag": imag
    }
    
    return call_api("1777316659204099", "complex_conjugate", arguments)

def complex_argument(
    real: float,
    imag: float
) -> Dict[str, Any]:
    """
    计算复数的幅角（以弧度为单位）
    
    Args:
        real: 复数的实部
        imag: 复数的虚部
    
    Returns:
        
    """
    arguments = {
        "real": real,
        "imag": imag
    }
    
    return call_api("1777316659204099", "complex_argument", arguments)

def complex_polar(
    real: float,
    imag: float
) -> Dict[str, Any]:
    """
    将复数转换为极坐标形式 r∠θ
    
    Args:
        real: 复数的实部
        imag: 复数的虚部
    
    Returns:
        
    """
    arguments = {
        "real": real,
        "imag": imag
    }
    
    return call_api("1777316659204099", "complex_polar", arguments)

def matrix_add(
    matrix_a: null,
    matrix_b: null
) -> Dict[str, Any]:
    """
    计算两个矩阵的和
    
    Args:
        matrix_a: 第一个矩阵（二维数组）
        matrix_b: 第二个矩阵（二维数组）
    
    Returns:
        
    """
    arguments = {
        "matrix_a": matrix_a,
        "matrix_b": matrix_b
    }
    
    return call_api("1777316659204099", "matrix_add", arguments)

def matrix_subtract(
    matrix_a: null,
    matrix_b: null
) -> Dict[str, Any]:
    """
    计算两个矩阵的差
    
    Args:
        matrix_a: 被减矩阵（二维数组）
        matrix_b: 减数矩阵（二维数组）
    
    Returns:
        
    """
    arguments = {
        "matrix_a": matrix_a,
        "matrix_b": matrix_b
    }
    
    return call_api("1777316659204099", "matrix_subtract", arguments)

def matrix_multiply(
    matrix_a: null,
    matrix_b: null
) -> Dict[str, Any]:
    """
    计算两个矩阵的乘积
    
    Args:
        matrix_a: 第一个矩阵（二维数组）
        matrix_b: 第二个矩阵（二维数组）
    
    Returns:
        
    """
    arguments = {
        "matrix_a": matrix_a,
        "matrix_b": matrix_b
    }
    
    return call_api("1777316659204099", "matrix_multiply", arguments)

def matrix_transpose(
    matrix: null
) -> Dict[str, Any]:
    """
    计算矩阵的转置
    
    Args:
        matrix: 输入矩阵（二维数组）
    
    Returns:
        
    """
    arguments = {
        "matrix": matrix
    }
    
    return call_api("1777316659204099", "matrix_transpose", arguments)

def matrix_determinant(
    matrix: null
) -> Dict[str, Any]:
    """
    计算方阵的行列式
    
    Args:
        matrix: 输入方阵（二维数组）
    
    Returns:
        
    """
    arguments = {
        "matrix": matrix
    }
    
    return call_api("1777316659204099", "matrix_determinant", arguments)

def matrix_inverse(
    matrix: null
) -> Dict[str, Any]:
    """
    计算方阵的逆矩阵
    
    Args:
        matrix: 输入方阵（二维数组）
    
    Returns:
        
    """
    arguments = {
        "matrix": matrix
    }
    
    return call_api("1777316659204099", "matrix_inverse", arguments)

def matrix_trace(
    matrix: null
) -> Dict[str, Any]:
    """
    计算方阵的迹（对角线元素之和）
    
    Args:
        matrix: 输入方阵（二维数组）
    
    Returns:
        
    """
    arguments = {
        "matrix": matrix
    }
    
    return call_api("1777316659204099", "matrix_trace", arguments)

def numerical_integration(
    function_type: str,
    coefficients: null,
    lower_bound: float,
    upper_bound: float,
    intervals: Optional[int] = 1000.0
) -> Dict[str, Any]:
    """
    使用梯形法则计算函数的定积分
    
    Args:
        function_type: 函数类型
        coefficients: 函数系数或参数
        lower_bound: 积分下限
        upper_bound: 积分上限
        intervals: 分割区间数
    
    Returns:
        
    """
    arguments = {
        "function_type": function_type,
        "coefficients": coefficients,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "intervals": intervals
    }
    
    return call_api("1777316659204099", "numerical_integration", arguments)

def numerical_derivative(
    function_type: str,
    coefficients: null,
    point: float,
    step_size: Optional[float] = 1.0E-4
) -> Dict[str, Any]:
    """
    使用中心差分法计算函数在某点的导数
    
    Args:
        function_type: 函数类型
        coefficients: 函数系数或参数
        point: 求导点
        step_size: 步长
    
    Returns:
        
    """
    arguments = {
        "function_type": function_type,
        "coefficients": coefficients,
        "point": point,
        "step_size": step_size
    }
    
    return call_api("1777316659204099", "numerical_derivative", arguments)

def newton_method(
    function_type: str,
    coefficients: null,
    initial_guess: float,
    tolerance: Optional[float] = 1.0E-6,
    max_iterations: Optional[int] = 100.0
) -> Dict[str, Any]:
    """
    使用牛顿法求解方程的根
    
    Args:
        function_type: 函数类型
        coefficients: 函数系数或参数
        initial_guess: 初始猜测值
        tolerance: 容差
        max_iterations: 最大迭代次数
    
    Returns:
        
    """
    arguments = {
        "function_type": function_type,
        "coefficients": coefficients,
        "initial_guess": initial_guess,
        "tolerance": tolerance,
        "max_iterations": max_iterations
    }
    
    return call_api("1777316659204099", "newton_method", arguments)

def bisection_method(
    function_type: str,
    coefficients: null,
    left_bound: float,
    right_bound: float,
    tolerance: Optional[float] = 1.0E-6,
    max_iterations: Optional[int] = 100.0
) -> Dict[str, Any]:
    """
    使用二分法求解方程在区间内的根
    
    Args:
        function_type: 函数类型
        coefficients: 函数系数或参数
        left_bound: 区间左端点
        right_bound: 区间右端点
        tolerance: 容差
        max_iterations: 最大迭代次数
    
    Returns:
        
    """
    arguments = {
        "function_type": function_type,
        "coefficients": coefficients,
        "left_bound": left_bound,
        "right_bound": right_bound,
        "tolerance": tolerance,
        "max_iterations": max_iterations
    }
    
    return call_api("1777316659204099", "bisection_method", arguments)

def lagrange_interpolation(
    x_points: null,
    y_points: null,
    interpolation_point: float
) -> Dict[str, Any]:
    """
    使用拉格朗日插值法计算插值点的函数值
    
    Args:
        x_points: 已知点的x坐标
        y_points: 已知点的y坐标
        interpolation_point: 插值点的x坐标
    
    Returns:
        
    """
    arguments = {
        "x_points": x_points,
        "y_points": y_points,
        "interpolation_point": interpolation_point
    }
    
    return call_api("1777316659204099", "lagrange_interpolation", arguments)

def compound_interest(
    principal: float,
    annual_rate: float,
    periods: float,
    compounding_frequency: Optional[int] = 1.0
) -> Dict[str, Any]:
    """
    计算复利投资的未来价值
    
    Args:
        principal: 本金
        annual_rate: 年利率（小数形式，如0.05表示5%）
        periods: 投资期数
        compounding_frequency: 每年复利次数（1=年复利，4=季复利，12=月复利）
    
    Returns:
        
    """
    arguments = {
        "principal": principal,
        "annual_rate": annual_rate,
        "periods": periods,
        "compounding_frequency": compounding_frequency
    }
    
    return call_api("1777316659204099", "compound_interest", arguments)

def present_value_annuity(
    payment: float,
    periods: int,
    interest_rate: float
) -> Dict[str, Any]:
    """
    计算普通年金的现值
    
    Args:
        payment: 每期支付金额
        periods: 支付期数
        interest_rate: 每期利率（小数形式）
    
    Returns:
        
    """
    arguments = {
        "payment": payment,
        "periods": periods,
        "interest_rate": interest_rate
    }
    
    return call_api("1777316659204099", "present_value_annuity", arguments)

def future_value_annuity(
    payment: float,
    periods: int,
    interest_rate: float
) -> Dict[str, Any]:
    """
    计算普通年金的未来值
    
    Args:
        payment: 每期支付金额
        periods: 支付期数
        interest_rate: 每期利率（小数形式）
    
    Returns:
        
    """
    arguments = {
        "payment": payment,
        "periods": periods,
        "interest_rate": interest_rate
    }
    
    return call_api("1777316659204099", "future_value_annuity", arguments)

def loan_payment(
    loan_amount: float,
    annual_rate: float,
    years: float
) -> Dict[str, Any]:
    """
    计算等额本息贷款的月供金额
    
    Args:
        loan_amount: 贷款本金
        annual_rate: 年利率（小数形式）
        years: 贷款年限
    
    Returns:
        
    """
    arguments = {
        "loan_amount": loan_amount,
        "annual_rate": annual_rate,
        "years": years
    }
    
    return call_api("1777316659204099", "loan_payment", arguments)

def net_present_value(
    initial_investment: float,
    cash_flows: null,
    discount_rate: float
) -> Dict[str, Any]:
    """
    计算投资项目的净现值（NPV）
    
    Args:
        initial_investment: 初始投资额
        cash_flows: 各期现金流
        discount_rate: 折现率（小数形式）
    
    Returns:
        
    """
    arguments = {
        "initial_investment": initial_investment,
        "cash_flows": cash_flows,
        "discount_rate": discount_rate
    }
    
    return call_api("1777316659204099", "net_present_value", arguments)

def internal_rate_of_return(
    initial_investment: float,
    cash_flows: null,
    initial_guess: Optional[float] = 0.1,
    tolerance: Optional[float] = 1.0E-6,
    max_iterations: Optional[int] = 100.0
) -> Dict[str, Any]:
    """
    计算投资项目的内部收益率（IRR）
    
    Args:
        initial_investment: 初始投资额
        cash_flows: 各期现金流
        initial_guess: 初始猜测值
        tolerance: 容差
        max_iterations: 最大迭代次数
    
    Returns:
        
    """
    arguments = {
        "initial_investment": initial_investment,
        "cash_flows": cash_flows,
        "initial_guess": initial_guess,
        "tolerance": tolerance,
        "max_iterations": max_iterations
    }
    
    return call_api("1777316659204099", "internal_rate_of_return", arguments)

def bond_price(
    face_value: float,
    coupon_rate: float,
    market_rate: float,
    years_to_maturity: float,
    payments_per_year: Optional[int] = 1.0
) -> Dict[str, Any]:
    """
    计算债券的理论价格
    
    Args:
        face_value: 面值
        coupon_rate: 票面利率（小数形式）
        market_rate: 市场利率（小数形式）
        years_to_maturity: 到期年限
        payments_per_year: 每年付息次数
    
    Returns:
        
    """
    arguments = {
        "face_value": face_value,
        "coupon_rate": coupon_rate,
        "market_rate": market_rate,
        "years_to_maturity": years_to_maturity,
        "payments_per_year": payments_per_year
    }
    
    return call_api("1777316659204099", "bond_price", arguments)

def length_conversion(
    value: float,
    from_unit: str,
    to_unit: str
) -> Dict[str, Any]:
    """
    在不同长度单位之间进行转换
    
    Args:
        value: 要转换的数值
        from_unit: 源单位
        to_unit: 目标单位
    
    Returns:
        
    """
    arguments = {
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit
    }
    
    return call_api("1777316659204099", "length_conversion", arguments)

def weight_conversion(
    value: float,
    from_unit: str,
    to_unit: str
) -> Dict[str, Any]:
    """
    在不同重量单位之间进行转换
    
    Args:
        value: 要转换的数值
        from_unit: 源单位
        to_unit: 目标单位
    
    Returns:
        
    """
    arguments = {
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit
    }
    
    return call_api("1777316659204099", "weight_conversion", arguments)

def temperature_conversion(
    value: float,
    from_unit: str,
    to_unit: str
) -> Dict[str, Any]:
    """
    在摄氏度、华氏度和开尔文之间进行转换
    
    Args:
        value: 要转换的温度值
        from_unit: 源单位
        to_unit: 目标单位
    
    Returns:
        
    """
    arguments = {
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit
    }
    
    return call_api("1777316659204099", "temperature_conversion", arguments)

def area_conversion(
    value: float,
    from_unit: str,
    to_unit: str
) -> Dict[str, Any]:
    """
    在不同面积单位之间进行转换
    
    Args:
        value: 要转换的数值
        from_unit: 源单位
        to_unit: 目标单位
    
    Returns:
        
    """
    arguments = {
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit
    }
    
    return call_api("1777316659204099", "area_conversion", arguments)

def volume_conversion(
    value: float,
    from_unit: str,
    to_unit: str
) -> Dict[str, Any]:
    """
    在不同体积单位之间进行转换
    
    Args:
        value: 要转换的数值
        from_unit: 源单位
        to_unit: 目标单位
    
    Returns:
        
    """
    arguments = {
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit
    }
    
    return call_api("1777316659204099", "volume_conversion", arguments)

def time_conversion(
    value: float,
    from_unit: str,
    to_unit: str
) -> Dict[str, Any]:
    """
    在不同时间单位之间进行转换
    
    Args:
        value: 要转换的数值
        from_unit: 源单位
        to_unit: 目标单位
    
    Returns:
        
    """
    arguments = {
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit
    }
    
    return call_api("1777316659204099", "time_conversion", arguments)

def speed_conversion(
    value: float,
    from_unit: str,
    to_unit: str
) -> Dict[str, Any]:
    """
    在不同速度单位之间进行转换
    
    Args:
        value: 要转换的数值
        from_unit: 源单位
        to_unit: 目标单位
    
    Returns:
        
    """
    arguments = {
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit
    }
    
    return call_api("1777316659204099", "speed_conversion", arguments)

def circle_calculation(
    radius: float
) -> Dict[str, Any]:
    """
    计算圆的面积、周长等属性
    
    Args:
        radius: 半径
    
    Returns:
        
    """
    arguments = {
        "radius": radius
    }
    
    return call_api("1777316659204099", "circle_calculation", arguments)

def rectangle_calculation(
    length: float,
    width: float
) -> Dict[str, Any]:
    """
    计算矩形的面积、周长等属性
    
    Args:
        length: 长度
        width: 宽度
    
    Returns:
        
    """
    arguments = {
        "length": length,
        "width": width
    }
    
    return call_api("1777316659204099", "rectangle_calculation", arguments)

def triangle_calculation(
    side_a: float,
    side_b: float,
    side_c: float
) -> Dict[str, Any]:
    """
    根据三边长计算三角形的面积、周长等属性
    
    Args:
        side_a: 边长a
        side_b: 边长b
        side_c: 边长c
    
    Returns:
        
    """
    arguments = {
        "side_a": side_a,
        "side_b": side_b,
        "side_c": side_c
    }
    
    return call_api("1777316659204099", "triangle_calculation", arguments)

def trapezoid_calculation(
    top_base: float,
    bottom_base: float,
    height: float
) -> Dict[str, Any]:
    """
    计算梯形的面积
    
    Args:
        top_base: 上底
        bottom_base: 下底
        height: 高
    
    Returns:
        
    """
    arguments = {
        "top_base": top_base,
        "bottom_base": bottom_base,
        "height": height
    }
    
    return call_api("1777316659204099", "trapezoid_calculation", arguments)

def ellipse_calculation(
    semi_major_axis: float,
    semi_minor_axis: float
) -> Dict[str, Any]:
    """
    计算椭圆的面积和周长（近似）
    
    Args:
        semi_major_axis: 长半轴
        semi_minor_axis: 短半轴
    
    Returns:
        
    """
    arguments = {
        "semi_major_axis": semi_major_axis,
        "semi_minor_axis": semi_minor_axis
    }
    
    return call_api("1777316659204099", "ellipse_calculation", arguments)

def sphere_calculation(
    radius: float
) -> Dict[str, Any]:
    """
    计算球体的体积和表面积
    
    Args:
        radius: 半径
    
    Returns:
        
    """
    arguments = {
        "radius": radius
    }
    
    return call_api("1777316659204099", "sphere_calculation", arguments)

def cylinder_calculation(
    radius: float,
    height: float
) -> Dict[str, Any]:
    """
    计算圆柱体的体积和表面积
    
    Args:
        radius: 底面半径
        height: 高度
    
    Returns:
        
    """
    arguments = {
        "radius": radius,
        "height": height
    }
    
    return call_api("1777316659204099", "cylinder_calculation", arguments)

def cone_calculation(
    radius: float,
    height: float
) -> Dict[str, Any]:
    """
    计算圆锥体的体积和表面积
    
    Args:
        radius: 底面半径
        height: 高度
    
    Returns:
        
    """
    arguments = {
        "radius": radius,
        "height": height
    }
    
    return call_api("1777316659204099", "cone_calculation", arguments)

def cuboid_calculation(
    length: float,
    width: float,
    height: float
) -> Dict[str, Any]:
    """
    计算长方体的体积和表面积
    
    Args:
        length: 长度
        width: 宽度
        height: 高度
    
    Returns:
        
    """
    arguments = {
        "length": length,
        "width": width,
        "height": height
    }
    
    return call_api("1777316659204099", "cuboid_calculation", arguments)

def regular_polygon(
    sides: int,
    side_length: float
) -> Dict[str, Any]:
    """
    计算正多边形的面积和周长
    
    Args:
        sides: 边数
        side_length: 边长
    
    Returns:
        
    """
    arguments = {
        "sides": sides,
        "side_length": side_length
    }
    
    return call_api("1777316659204099", "regular_polygon", arguments)

