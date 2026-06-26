# Python 常见错误速查表

## 语法错误 (SyntaxError)

### 1. 缺少冒号
```python
# ❌ 错误
if x > 0
    print(x)

# ✅ 正确
if x > 0:
    print(x)
```

### 2. 缩进错误
```python
# ❌ 错误
def foo():
print("hello")

# ✅ 正确
def foo():
    print("hello")
```

### 3. 括号不匹配
```python
# ❌ 错误
print("hello"

# ✅ 正确
print("hello")
```

---

## 名称错误 (NameError)

### 1. 变量未定义
```python
# ❌ 错误
print(x)  # x 未定义

# ✅ 正确
x = 10
print(x)
```

### 2. 变量名拼写错误
```python
# ❌ 错误
my_list = [1, 2, 3]
print(mylist)  # 拼写错误

# ✅ 正确
print(my_list)
```

---

## 类型错误 (TypeError)

### 1. 类型不匹配
```python
# ❌ 错误
print("Hello" + 123)

# ✅ 正确
print("Hello" + str(123))
# 或
print("Hello", 123)
```

### 2. 参数数量错误
```python
# ❌ 错误
def greet(name, greeting):
    print(f"{greeting}, {name}!")

greet("Alice")  # 缺少 greeting 参数

# ✅ 正确
greet("Alice", "Hello")
```

---

## 索引错误 (IndexError)

### 列表索引越界
```python
# ❌ 错误
my_list = [1, 2, 3]
print(my_list[5])  # 索引超出范围

# ✅ 正确
print(my_list[2])  # 输出 3
# 或使用循环
for i in range(len(my_list)):
    print(my_list[i])
```

---

## 键错误 (KeyError)

### 字典键不存在
```python
# ❌ 错误
my_dict = {"a": 1, "b": 2}
print(my_dict["c"])  # 键不存在

# ✅ 正确
print(my_dict.get("c", "默认值"))  # 输出默认值
# 或
if "c" in my_dict:
    print(my_dict["c"])
```

---

## 值错误 (ValueError)

### 值不符合函数预期
```python
# ❌ 错误
int("abc")  # 无法将字符串转换为整数

# ✅ 正确
int("123")  # 正常转换
# 或
try:
    result = int("abc")
except ValueError:
    print("转换失败")
```

---

## 文件未找到错误 (FileNotFoundError)

### 文件路径错误
```python
# ❌ 错误
with open("data.txt", "r") as f:
    content = f.read()

# ✅ 正确
# 使用绝对路径
with open(r"C:\path\to\data.txt", "r") as f:
    content = f.read()
# 或检查文件是否存在
import os
if os.path.exists("data.txt"):
    with open("data.txt", "r") as f:
        content = f.read()
```

---

## 属性错误 (AttributeError)

### 对象没有该属性/方法
```python
# ❌ 错误
my_list = [1, 2, 3]
my_list.add(4)  # list 没有 add 方法

# ✅ 正确
my_list.append(4)
```

### 类型错误使用了不存在的方法
```python
# ❌ 错误
text = "hello"
text.append(" world")  # str 没有 append 方法

# ✅ 正确
text += " world"
```

---

## 导入错误 (ImportError)

### 模块不存在
```python
# ❌ 错误
import numpyoo  # 拼写错误

# ✅ 正确
import numpy as np
```

---

## 常见错误快速诊断表

| 错误类型 | 关键词 | 检查点 |
|----------|--------|--------|
| SyntaxError | "invalid syntax" | 括号、冒号、缩进 |
| NameError | "name 'x' is not defined" | 变量是否定义 |
| TypeError | "unsupported operand type" | 数据类型 |
| IndexError | "list index out of range" | 索引范围 |
| KeyError | "KeyError: 'x'" | 字典键是否存在 |
| ValueError | "invalid literal" | 值是否合法 |
| ImportError | "No module named" | 模块是否安装 |
| FileNotFoundError | "No such file" | 文件路径是否正确 |