# Chapter 1: Variables and Data Types

Variables are named containers that store values. In Python you don't declare a type — the interpreter figures it out from the value you assign.

Python has four basic data types: integers (`int`), decimals (`float`), text (`str`), and true/false values (`bool`).

## Example 1: Assigning variables

```python
name = "Alice"
age = 25
height = 1.68
is_student = True

print(name)
print(age)
print(is_student)
```

**Output:**
```
Alice
25
True
```

## Example 2: Checking the type of a variable

```python
score = 42
price = 9.99
greeting = "hello"

print(type(score))
print(type(price))
print(type(greeting))
```

**Output:**
```
<class 'int'>
<class 'float'>
<class 'str'>
```

## Example 3: Updating a variable

Variables can be reassigned at any time. The old value is simply replaced.

```python
count = 10
print(count)

count = count + 5
print(count)

count += 3
print(count)
```

**Output:**
```
10
15
18
```
