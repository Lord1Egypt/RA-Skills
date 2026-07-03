---
name: 计算器服务
description: 一个功能完整的基于 Model Context Protocol (MCP) 的计算器服务器，提供丰富的数学运算功能，包括基础算术、根式运算、三角函数、对数运算、统计学、组合数学、数论、复数运算、矩阵运算、数值分析、金融计算、单位转换和几何计算等 13 个专业数学模块。
version: 1.0.0
---

# 计算器服务

一个功能完整的基于 Model Context Protocol (MCP) 的计算器服务器，提供丰富的数学运算功能，包括基础算术、根式运算、三角函数、对数运算、统计学、组合数学、数论、复数运算、矩阵运算、数值分析、金融计算、单位转换和几何计算等 13 个专业数学模块。

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
| 执行两个数字的加法运算 | `scripts.tools.add` |
| 执行两个数字的减法运算 | `scripts.tools.subtract` |
| 执行两个数字的乘法运算 | `scripts.tools.multiply` |
| 执行两个数字的除法运算 | `scripts.tools.divide` |
| 计算两个数的余数 | `scripts.tools.modulo` |
| 计算a的b次方 | `scripts.tools.power` |
| 计算数字的平方根 | `scripts.tools.sqrt` |
| 计算数字的立方根 | `scripts.tools.cbrt` |
| 计算数字的n次方根 | `scripts.tools.nthRoot` |
| 计算数字的绝对值 | `scripts.tools.abs` |
| 计算角度的正弦值（输入为弧度） | `scripts.tools.sin` |
| 计算角度的余弦值（输入为弧度） | `scripts.tools.cos` |
| 计算角度的正切值（输入为弧度） | `scripts.tools.tan` |
| 计算反正弦值（返回弧度） | `scripts.tools.asin` |
| 计算反余弦值（返回弧度） | `scripts.tools.acos` |
| 计算反正切值（返回弧度） | `scripts.tools.atan` |
| 计算从x轴到点(x,y)的角度（返回弧度） | `scripts.tools.atan2` |
| 计算双曲正弦值 | `scripts.tools.sinh` |
| 计算双曲余弦值 | `scripts.tools.cosh` |
| 计算双曲正切值 | `scripts.tools.tanh` |
| 计算反双曲正弦值 | `scripts.tools.asinh` |
| 计算反双曲余弦值（输入值必须≥1） | `scripts.tools.acosh` |
| 计算反双曲正切值（输入值必须在-1到1之间） | `scripts.tools.atanh` |
| 计算正割值（1/cos） | `scripts.tools.sec` |
| 计算余割值（1/sin） | `scripts.tools.csc` |
| 计算余切值（1/tan） | `scripts.tools.cot` |
| 将角度转换为弧度 | `scripts.tools.degToRad` |
| 将弧度转换为角度 | `scripts.tools.radToDeg` |
| 计算自然对数（以e为底） | `scripts.tools.ln` |
| 计算以10为底的对数 | `scripts.tools.log10` |
| 计算以指定底数的对数 | `scripts.tools.log` |
| 计算数组的算术平均值 | `scripts.tools.mean` |
| 计算数组的中位数 | `scripts.tools.median` |
| 计算数组的众数（出现频率最高的数） | `scripts.tools.mode` |
| 计算数组的标准差 | `scripts.tools.stdDev` |
| 计算数组的方差 | `scripts.tools.variance` |
| 找出数组中的最大值 | `scripts.tools.max` |
| 找出数组中的最小值 | `scripts.tools.min` |
| 计算数组所有元素的和 | `scripts.tools.sum` |
| 计算数组所有元素的乘积 | `scripts.tools.product` |
| 计算数组的范围（最大值-最小值） | `scripts.tools.range` |
| 计算非负整数的阶乘 | `scripts.tools.factorial` |
| 计算从n个元素中选择r个元素的排列数 P(n,r) | `scripts.tools.permutation` |
| 计算从n个元素中选择r个元素的组合数 C(n,r) | `scripts.tools.combination` |
| 计算斐波那契数列的第n项 | `scripts.tools.fibonacci` |
| 生成斐波那契数列的前n项 | `scripts.tools.fibonacciSequence` |
| 计算第n个卡塔兰数 | `scripts.tools.catalan` |
| 计算第n个贝尔数（集合划分数） | `scripts.tools.bellNumber` |
| 计算二项式系数 (n choose k) | `scripts.tools.binomialCoefficient` |
| 计算两个或多个整数的最大公约数 | `scripts.tools.gcd` |
| 计算两个或多个整数的最小公倍数 | `scripts.tools.lcm` |
| 判断一个正整数是否为素数 | `scripts.tools.isPrime` |
| 将正整数分解为素因数的乘积 | `scripts.tools.primeFactorization` |
| 计算欧拉函数φ(n)，即小于等于n且与n互质的正整数个数 | `scripts.tools.eulerPhi` |
| 判断一个正整数是否为完全数（等于其所有真因子之和） | `scripts.tools.isPerfectNumber` |
| 计算正整数的因子个数 | `scripts.tools.divisorCount` |
| 列出正整数的所有因子 | `scripts.tools.divisorList` |
| 计算两个复数的和 | `scripts.tools.complex_add` |
| 计算两个复数的差 | `scripts.tools.complex_subtract` |
| 计算两个复数的乘积 | `scripts.tools.complex_multiply` |
| 计算两个复数的商 | `scripts.tools.complex_divide` |
| 计算复数的模长（绝对值） | `scripts.tools.complex_magnitude` |
| 计算复数的共轭 | `scripts.tools.complex_conjugate` |
| 计算复数的幅角（以弧度为单位） | `scripts.tools.complex_argument` |
| 将复数转换为极坐标形式 r∠θ | `scripts.tools.complex_polar` |
| 计算两个矩阵的和 | `scripts.tools.matrix_add` |
| 计算两个矩阵的差 | `scripts.tools.matrix_subtract` |
| 计算两个矩阵的乘积 | `scripts.tools.matrix_multiply` |
| 计算矩阵的转置 | `scripts.tools.matrix_transpose` |
| 计算方阵的行列式 | `scripts.tools.matrix_determinant` |
| 计算方阵的逆矩阵 | `scripts.tools.matrix_inverse` |
| 计算方阵的迹（对角线元素之和） | `scripts.tools.matrix_trace` |
| 使用梯形法则计算函数的定积分 | `scripts.tools.numerical_integration` |
| 使用中心差分法计算函数在某点的导数 | `scripts.tools.numerical_derivative` |
| 使用牛顿法求解方程的根 | `scripts.tools.newton_method` |
| 使用二分法求解方程在区间内的根 | `scripts.tools.bisection_method` |
| 使用拉格朗日插值法计算插值点的函数值 | `scripts.tools.lagrange_interpolation` |
| 计算复利投资的未来价值 | `scripts.tools.compound_interest` |
| 计算普通年金的现值 | `scripts.tools.present_value_annuity` |
| 计算普通年金的未来值 | `scripts.tools.future_value_annuity` |
| 计算等额本息贷款的月供金额 | `scripts.tools.loan_payment` |
| 计算投资项目的净现值（NPV） | `scripts.tools.net_present_value` |
| 计算投资项目的内部收益率（IRR） | `scripts.tools.internal_rate_of_return` |
| 计算债券的理论价格 | `scripts.tools.bond_price` |
| 在不同长度单位之间进行转换 | `scripts.tools.length_conversion` |
| 在不同重量单位之间进行转换 | `scripts.tools.weight_conversion` |
| 在摄氏度、华氏度和开尔文之间进行转换 | `scripts.tools.temperature_conversion` |
| 在不同面积单位之间进行转换 | `scripts.tools.area_conversion` |
| 在不同体积单位之间进行转换 | `scripts.tools.volume_conversion` |
| 在不同时间单位之间进行转换 | `scripts.tools.time_conversion` |
| 在不同速度单位之间进行转换 | `scripts.tools.speed_conversion` |
| 计算圆的面积、周长等属性 | `scripts.tools.circle_calculation` |
| 计算矩形的面积、周长等属性 | `scripts.tools.rectangle_calculation` |
| 根据三边长计算三角形的面积、周长等属性 | `scripts.tools.triangle_calculation` |
| 计算梯形的面积 | `scripts.tools.trapezoid_calculation` |
| 计算椭圆的面积和周长（近似） | `scripts.tools.ellipse_calculation` |
| 计算球体的体积和表面积 | `scripts.tools.sphere_calculation` |
| 计算圆柱体的体积和表面积 | `scripts.tools.cylinder_calculation` |
| 计算圆锥体的体积和表面积 | `scripts.tools.cone_calculation` |
| 计算长方体的体积和表面积 | `scripts.tools.cuboid_calculation` |
| 计算正多边形的面积和周长 | `scripts.tools.regular_polygon` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.add
工具描述：执行两个数字的加法运算
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |第一个数字|
|b|number|true| |第二个数字|

---

## scripts.tools.subtract
工具描述：执行两个数字的减法运算
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |被减数|
|b|number|true| |减数|

---

## scripts.tools.multiply
工具描述：执行两个数字的乘法运算
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |第一个数字|
|b|number|true| |第二个数字|

---

## scripts.tools.divide
工具描述：执行两个数字的除法运算
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |被除数|
|b|number|true| |除数|

---

## scripts.tools.modulo
工具描述：计算两个数的余数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |被除数|
|b|number|true| |除数|

---

## scripts.tools.power
工具描述：计算a的b次方
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |底数|
|b|number|true| |指数|

---

## scripts.tools.sqrt
工具描述：计算数字的平方根
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |被开方数|

---

## scripts.tools.cbrt
工具描述：计算数字的立方根
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |被开方数|

---

## scripts.tools.nthRoot
工具描述：计算数字的n次方根
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |被开方数|
|n|number|true| |开方次数|

---

## scripts.tools.abs
工具描述：计算数字的绝对值
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |数字|

---

## scripts.tools.sin
工具描述：计算角度的正弦值（输入为弧度）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|angle|number|true| |角度（弧度）|

---

## scripts.tools.cos
工具描述：计算角度的余弦值（输入为弧度）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|angle|number|true| |角度（弧度）|

---

## scripts.tools.tan
工具描述：计算角度的正切值（输入为弧度）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|angle|number|true| |角度（弧度）|

---

## scripts.tools.asin
工具描述：计算反正弦值（返回弧度）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |输入值（-1到1之间）|

---

## scripts.tools.acos
工具描述：计算反余弦值（返回弧度）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |输入值（-1到1之间）|

---

## scripts.tools.atan
工具描述：计算反正切值（返回弧度）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |输入值|

---

## scripts.tools.atan2
工具描述：计算从x轴到点(x,y)的角度（返回弧度）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|y|number|true| |y坐标|
|x|number|true| |x坐标|

---

## scripts.tools.sinh
工具描述：计算双曲正弦值
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |输入值|

---

## scripts.tools.cosh
工具描述：计算双曲余弦值
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |输入值|

---

## scripts.tools.tanh
工具描述：计算双曲正切值
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |输入值|

---

## scripts.tools.asinh
工具描述：计算反双曲正弦值
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |输入值|

---

## scripts.tools.acosh
工具描述：计算反双曲余弦值（输入值必须≥1）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |输入值（≥1）|

---

## scripts.tools.atanh
工具描述：计算反双曲正切值（输入值必须在-1到1之间）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |输入值（-1到1之间）|

---

## scripts.tools.sec
工具描述：计算正割值（1/cos）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|angle|number|true| |角度（弧度）|

---

## scripts.tools.csc
工具描述：计算余割值（1/sin）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|angle|number|true| |角度（弧度）|

---

## scripts.tools.cot
工具描述：计算余切值（1/tan）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|angle|number|true| |角度（弧度）|

---

## scripts.tools.degToRad
工具描述：将角度转换为弧度
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|degrees|number|true| |角度值|

---

## scripts.tools.radToDeg
工具描述：将弧度转换为角度
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|radians|number|true| |弧度值|

---

## scripts.tools.ln
工具描述：计算自然对数（以e为底）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |输入值（必须大于0）|

---

## scripts.tools.log10
工具描述：计算以10为底的对数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |输入值（必须大于0）|

---

## scripts.tools.log
工具描述：计算以指定底数的对数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |输入值（必须大于0）|
|base|number|true| |底数（必须大于0且不等于1）|

---

## scripts.tools.mean
工具描述：计算数组的算术平均值
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|numbers|array|true| |数字数组|

---

## scripts.tools.median
工具描述：计算数组的中位数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|numbers|array|true| |数字数组|

---

## scripts.tools.mode
工具描述：计算数组的众数（出现频率最高的数）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|numbers|array|true| |数字数组|

---

## scripts.tools.stdDev
工具描述：计算数组的标准差
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|numbers|array|true| |数字数组|
|sample|boolean|false| |是否为样本标准差（默认为总体标准差）|

---

## scripts.tools.variance
工具描述：计算数组的方差
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|numbers|array|true| |数字数组|
|sample|boolean|false| |是否为样本方差（默认为总体方差）|

---

## scripts.tools.max
工具描述：找出数组中的最大值
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|numbers|array|true| |数字数组|

---

## scripts.tools.min
工具描述：找出数组中的最小值
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|numbers|array|true| |数字数组|

---

## scripts.tools.sum
工具描述：计算数组所有元素的和
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|numbers|array|true| |数字数组|

---

## scripts.tools.product
工具描述：计算数组所有元素的乘积
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|numbers|array|true| |数字数组|

---

## scripts.tools.range
工具描述：计算数组的范围（最大值-最小值）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|numbers|array|true| |数字数组|

---

## scripts.tools.factorial
工具描述：计算非负整数的阶乘
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |非负整数|

---

## scripts.tools.permutation
工具描述：计算从n个元素中选择r个元素的排列数 P(n,r)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |总元素数|
|r|integer|true| |选择元素数|

---

## scripts.tools.combination
工具描述：计算从n个元素中选择r个元素的组合数 C(n,r)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |总元素数|
|r|integer|true| |选择元素数|

---

## scripts.tools.fibonacci
工具描述：计算斐波那契数列的第n项
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |项数（从0开始）|

---

## scripts.tools.fibonacciSequence
工具描述：生成斐波那契数列的前n项
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |生成项数（1-100）|

---

## scripts.tools.catalan
工具描述：计算第n个卡塔兰数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |项数（0-35）|

---

## scripts.tools.bellNumber
工具描述：计算第n个贝尔数（集合划分数）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |项数（0-15）|

---

## scripts.tools.binomialCoefficient
工具描述：计算二项式系数 (n choose k)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |上标|
|k|integer|true| |下标|

---

## scripts.tools.gcd
工具描述：计算两个或多个整数的最大公约数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|numbers|array|true| |整数数组（至少2个数）|

---

## scripts.tools.lcm
工具描述：计算两个或多个整数的最小公倍数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|numbers|array|true| |整数数组（至少2个数）|

---

## scripts.tools.isPrime
工具描述：判断一个正整数是否为素数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |正整数|

---

## scripts.tools.primeFactorization
工具描述：将正整数分解为素因数的乘积
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |大于1的正整数|

---

## scripts.tools.eulerPhi
工具描述：计算欧拉函数φ(n)，即小于等于n且与n互质的正整数个数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |正整数|

---

## scripts.tools.isPerfectNumber
工具描述：判断一个正整数是否为完全数（等于其所有真因子之和）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |正整数|

---

## scripts.tools.divisorCount
工具描述：计算正整数的因子个数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |正整数|

---

## scripts.tools.divisorList
工具描述：列出正整数的所有因子
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |正整数（1-10000）|

---

## scripts.tools.complex_add
工具描述：计算两个复数的和
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a_real|number|true| |第一个复数的实部|
|a_imag|number|true| |第一个复数的虚部|
|b_real|number|true| |第二个复数的实部|
|b_imag|number|true| |第二个复数的虚部|

---

## scripts.tools.complex_subtract
工具描述：计算两个复数的差
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a_real|number|true| |第一个复数的实部|
|a_imag|number|true| |第一个复数的虚部|
|b_real|number|true| |第二个复数的实部|
|b_imag|number|true| |第二个复数的虚部|

---

## scripts.tools.complex_multiply
工具描述：计算两个复数的乘积
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a_real|number|true| |第一个复数的实部|
|a_imag|number|true| |第一个复数的虚部|
|b_real|number|true| |第二个复数的实部|
|b_imag|number|true| |第二个复数的虚部|

---

## scripts.tools.complex_divide
工具描述：计算两个复数的商
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a_real|number|true| |被除数的实部|
|a_imag|number|true| |被除数的虚部|
|b_real|number|true| |除数的实部|
|b_imag|number|true| |除数的虚部|

---

## scripts.tools.complex_magnitude
工具描述：计算复数的模长（绝对值）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|real|number|true| |复数的实部|
|imag|number|true| |复数的虚部|

---

## scripts.tools.complex_conjugate
工具描述：计算复数的共轭
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|real|number|true| |复数的实部|
|imag|number|true| |复数的虚部|

---

## scripts.tools.complex_argument
工具描述：计算复数的幅角（以弧度为单位）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|real|number|true| |复数的实部|
|imag|number|true| |复数的虚部|

---

## scripts.tools.complex_polar
工具描述：将复数转换为极坐标形式 r∠θ
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|real|number|true| |复数的实部|
|imag|number|true| |复数的虚部|

---

## scripts.tools.matrix_add
工具描述：计算两个矩阵的和
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|matrix_a|array|true| |第一个矩阵（二维数组）|
|matrix_b|array|true| |第二个矩阵（二维数组）|

---

## scripts.tools.matrix_subtract
工具描述：计算两个矩阵的差
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|matrix_a|array|true| |被减矩阵（二维数组）|
|matrix_b|array|true| |减数矩阵（二维数组）|

---

## scripts.tools.matrix_multiply
工具描述：计算两个矩阵的乘积
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|matrix_a|array|true| |第一个矩阵（二维数组）|
|matrix_b|array|true| |第二个矩阵（二维数组）|

---

## scripts.tools.matrix_transpose
工具描述：计算矩阵的转置
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|matrix|array|true| |输入矩阵（二维数组）|

---

## scripts.tools.matrix_determinant
工具描述：计算方阵的行列式
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|matrix|array|true| |输入方阵（二维数组）|

---

## scripts.tools.matrix_inverse
工具描述：计算方阵的逆矩阵
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|matrix|array|true| |输入方阵（二维数组）|

---

## scripts.tools.matrix_trace
工具描述：计算方阵的迹（对角线元素之和）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|matrix|array|true| |输入方阵（二维数组）|

---

## scripts.tools.numerical_integration
工具描述：使用梯形法则计算函数的定积分
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|function_type|string|true| |函数类型|
|coefficients|array|true| |函数系数或参数|
|lower_bound|number|true| |积分下限|
|upper_bound|number|true| |积分上限|
|intervals|integer|false|1000.0|分割区间数|

---

## scripts.tools.numerical_derivative
工具描述：使用中心差分法计算函数在某点的导数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|function_type|string|true| |函数类型|
|coefficients|array|true| |函数系数或参数|
|point|number|true| |求导点|
|step_size|number|false|1.0E-4|步长|

---

## scripts.tools.newton_method
工具描述：使用牛顿法求解方程的根
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|function_type|string|true| |函数类型|
|coefficients|array|true| |函数系数或参数|
|initial_guess|number|true| |初始猜测值|
|tolerance|number|false|1.0E-6|容差|
|max_iterations|integer|false|100.0|最大迭代次数|

---

## scripts.tools.bisection_method
工具描述：使用二分法求解方程在区间内的根
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|function_type|string|true| |函数类型|
|coefficients|array|true| |函数系数或参数|
|left_bound|number|true| |区间左端点|
|right_bound|number|true| |区间右端点|
|tolerance|number|false|1.0E-6|容差|
|max_iterations|integer|false|100.0|最大迭代次数|

---

## scripts.tools.lagrange_interpolation
工具描述：使用拉格朗日插值法计算插值点的函数值
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|x_points|array|true| |已知点的x坐标|
|y_points|array|true| |已知点的y坐标|
|interpolation_point|number|true| |插值点的x坐标|

---

## scripts.tools.compound_interest
工具描述：计算复利投资的未来价值
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|principal|number|true| |本金|
|annual_rate|number|true| |年利率（小数形式，如0.05表示5%）|
|periods|number|true| |投资期数|
|compounding_frequency|integer|false|1.0|每年复利次数（1=年复利，4=季复利，12=月复利）|

---

## scripts.tools.present_value_annuity
工具描述：计算普通年金的现值
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|payment|number|true| |每期支付金额|
|periods|integer|true| |支付期数|
|interest_rate|number|true| |每期利率（小数形式）|

---

## scripts.tools.future_value_annuity
工具描述：计算普通年金的未来值
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|payment|number|true| |每期支付金额|
|periods|integer|true| |支付期数|
|interest_rate|number|true| |每期利率（小数形式）|

---

## scripts.tools.loan_payment
工具描述：计算等额本息贷款的月供金额
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|loan_amount|number|true| |贷款本金|
|annual_rate|number|true| |年利率（小数形式）|
|years|number|true| |贷款年限|

---

## scripts.tools.net_present_value
工具描述：计算投资项目的净现值（NPV）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|initial_investment|number|true| |初始投资额|
|cash_flows|array|true| |各期现金流|
|discount_rate|number|true| |折现率（小数形式）|

---

## scripts.tools.internal_rate_of_return
工具描述：计算投资项目的内部收益率（IRR）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|initial_investment|number|true| |初始投资额|
|cash_flows|array|true| |各期现金流|
|initial_guess|number|false|0.1|初始猜测值|
|tolerance|number|false|1.0E-6|容差|
|max_iterations|integer|false|100.0|最大迭代次数|

---

## scripts.tools.bond_price
工具描述：计算债券的理论价格
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|face_value|number|true| |面值|
|coupon_rate|number|true| |票面利率（小数形式）|
|market_rate|number|true| |市场利率（小数形式）|
|years_to_maturity|number|true| |到期年限|
|payments_per_year|integer|false|1.0|每年付息次数|

---

## scripts.tools.length_conversion
工具描述：在不同长度单位之间进行转换
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |要转换的数值|
|from_unit|string|true| |源单位|
|to_unit|string|true| |目标单位|

---

## scripts.tools.weight_conversion
工具描述：在不同重量单位之间进行转换
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |要转换的数值|
|from_unit|string|true| |源单位|
|to_unit|string|true| |目标单位|

---

## scripts.tools.temperature_conversion
工具描述：在摄氏度、华氏度和开尔文之间进行转换
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |要转换的温度值|
|from_unit|string|true| |源单位|
|to_unit|string|true| |目标单位|

---

## scripts.tools.area_conversion
工具描述：在不同面积单位之间进行转换
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |要转换的数值|
|from_unit|string|true| |源单位|
|to_unit|string|true| |目标单位|

---

## scripts.tools.volume_conversion
工具描述：在不同体积单位之间进行转换
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |要转换的数值|
|from_unit|string|true| |源单位|
|to_unit|string|true| |目标单位|

---

## scripts.tools.time_conversion
工具描述：在不同时间单位之间进行转换
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |要转换的数值|
|from_unit|string|true| |源单位|
|to_unit|string|true| |目标单位|

---

## scripts.tools.speed_conversion
工具描述：在不同速度单位之间进行转换
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |要转换的数值|
|from_unit|string|true| |源单位|
|to_unit|string|true| |目标单位|

---

## scripts.tools.circle_calculation
工具描述：计算圆的面积、周长等属性
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|radius|number|true| |半径|

---

## scripts.tools.rectangle_calculation
工具描述：计算矩形的面积、周长等属性
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|length|number|true| |长度|
|width|number|true| |宽度|

---

## scripts.tools.triangle_calculation
工具描述：根据三边长计算三角形的面积、周长等属性
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|side_a|number|true| |边长a|
|side_b|number|true| |边长b|
|side_c|number|true| |边长c|

---

## scripts.tools.trapezoid_calculation
工具描述：计算梯形的面积
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|top_base|number|true| |上底|
|bottom_base|number|true| |下底|
|height|number|true| |高|

---

## scripts.tools.ellipse_calculation
工具描述：计算椭圆的面积和周长（近似）
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|semi_major_axis|number|true| |长半轴|
|semi_minor_axis|number|true| |短半轴|

---

## scripts.tools.sphere_calculation
工具描述：计算球体的体积和表面积
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|radius|number|true| |半径|

---

## scripts.tools.cylinder_calculation
工具描述：计算圆柱体的体积和表面积
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|radius|number|true| |底面半径|
|height|number|true| |高度|

---

## scripts.tools.cone_calculation
工具描述：计算圆锥体的体积和表面积
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|radius|number|true| |底面半径|
|height|number|true| |高度|

---

## scripts.tools.cuboid_calculation
工具描述：计算长方体的体积和表面积
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|length|number|true| |长度|
|width|number|true| |宽度|
|height|number|true| |高度|

---

## scripts.tools.regular_polygon
工具描述：计算正多边形的面积和周长
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|sides|integer|true| |边数|
|side_length|number|true| |边长|

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