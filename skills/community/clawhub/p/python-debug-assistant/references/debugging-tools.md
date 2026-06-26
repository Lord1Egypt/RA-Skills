# Python 调试工具使用指南

## 1. Print 调试法

最简单直接的调试方式，通过打印变量值观察程序状态。

```python
def calculate_sum(numbers):
    result = 0
    for i, num in enumerate(numbers):
        # 打印每一步的中间结果
        print(f"i={i}, num={num}, result={result}")
        result += num
    return result

calculate_sum([1, 2, 3, 4, 5])
```

**输出：**
```
i=0, num=1, result=0
i=1, num=2, result=1
i=2, num=3, result=3
i=3, num=4, result=6
i=4, num=5, result=10
```

---

## 2. pdb 断点调试

Python 内置的交互式调试器。

### 基本命令

| 命令 | 简写 | 说明 |
|------|------|------|
| `n` (next) | `n` | 执行下一行 |
| `s` (step) | `s` | 进入函数内部 |
| `c` (continue) | `c` | 继续执行直到下一个断点 |
| `p` (print) | `p` | 打印变量值 |
| `l` (list) | `l` | 查看当前代码上下文 |
| `q` (quit) | `q` | 退出调试 |

### 使用方式

```python
import pdb

def buggy_function(x, y):
    pdb.set_trace()  # 设置断点
    result = x / y
    return result

buggy_function(10, 0)  # 会触发断点
```

### 启动方式

```bash
# 方式1: 命令行启动
python -m pdb myscript.py

# 方式2: 代码中设置断点
import pdb; pdb.set_trace()

# 方式3: 使用 breakpoint() (Python 3.7+)
breakpoint()
```

---

## 3. logging 日志调试

适合正式项目，可以控制日志级别和输出格式。

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def divide(a, b):
    logger.debug(f"a = {a}, b = {b}")
    if b == 0:
        logger.error("除数不能为零！")
        return None
    result = a / b
    logger.debug(f"result = {result}")
    return result

divide(10, 2)
divide(10, 0)
```

---

## 4. try-except 异常捕获

```python
def read_number(s):
    try:
        value = int(s)
        print(f"成功转换: {value}")
    except ValueError as e:
        print(f"转换失败: {e}")
        print(f"输入内容: '{s}'")
        return None
    return value

read_number("123")
read_number("abc")
```

---

## 5. IDE 调试工具

### VS Code 调试配置

1. 安装 Python 扩展
2. 在代码左侧点击设置断点
3. 按 F5 启动调试

### PyCharm 调试

1. 点击代码行号左侧设置断点
2. 右键选择 "Debug"
3. 使用调试窗口观察变量

---

## 6. 单元测试辅助

```python
import unittest

def add(a, b):
    return a + b

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

if __name__ == '__main__':
    unittest.main()
```

---

## 7. 快速检查变量

```python
# 查看变量类型
print(type(my_variable))

# 查看变量所有属性和方法
print(dir(my_variable))

# 查看对象详细信息
import pprint
pprint.pprint(vars(my_object))
```

---

## 调试流程建议

1. **先看错误信息** — 明确错误类型和位置
2. **缩小范围** — 注释掉部分代码，定位问题区间
3. **打印关键变量** — 在可疑处打印变量值
4. **使用 pdb** — 复杂问题用断点调试
5. **检查数据类型** — 很多错误源于类型不匹配
6. **查看文档** — 确认函数参数和使用方式

---

## 常见调试场景

| 场景 | 推荐方法 |
|------|----------|
| 简单错误 | print 打印 |
| 循环中的错误 | print + 计数器 |
| 函数返回值错误 | pdb 断点 |
| 偶发错误 | logging 记录 |
| 未知异常 | try-except + traceback |