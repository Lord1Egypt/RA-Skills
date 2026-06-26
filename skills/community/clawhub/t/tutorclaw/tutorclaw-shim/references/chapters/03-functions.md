# Chapter 3: Functions

A function is a reusable block of code that performs a specific task. You define it once with `def` and call it as many times as you need. Functions can accept inputs (parameters) and return outputs.

## Example 1: A simple function

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
greet("Bob")
```

**Output:**
```
Hello, Alice!
Hello, Bob!
```

## Example 2: A function that returns a value

```python
def add(a, b):
    return a + b

result = add(3, 7)
print(result)
print(add(10, 20))
```

**Output:**
```
10
30
```

## Example 3: Default parameter values

Parameters can have defaults so callers can omit them.

```python
def power(base, exponent=2):
    return base ** exponent

print(power(3))
print(power(3, 3))
print(power(2, 10))
```

**Output:**
```
9
27
1024
```
