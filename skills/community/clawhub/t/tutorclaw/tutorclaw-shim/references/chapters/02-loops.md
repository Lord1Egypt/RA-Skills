# Chapter 2: Loops

Loops let you repeat a block of code. Python has two kinds: `for` loops (repeat over a sequence) and `while` loops (repeat while a condition is true).

## Example 1: for loop over a range

`range(n)` produces the numbers 0 through n-1.

```python
for i in range(5):
    print(i)
```

**Output:**
```
0
1
2
3
4
```

## Example 2: for loop over a list

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
```

**Output:**
```
apple
banana
cherry
```

## Example 3: while loop

A `while` loop runs as long as its condition remains `True`. Always make sure something inside the loop moves toward the condition becoming `False`, or the loop will run forever.

```python
count = 1

while count <= 5:
    print(count)
    count += 1
```

**Output:**
```
1
2
3
4
5
```
