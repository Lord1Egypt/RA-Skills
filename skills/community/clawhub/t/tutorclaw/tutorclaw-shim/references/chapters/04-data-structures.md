# Chapter 4: Data Structures

Python has four built-in collection types. Lists store ordered, changeable sequences. Tuples are ordered but immutable. Sets store unique unordered values. Dictionaries map keys to values.

## Example 1: Lists

```python
scores = [85, 92, 78, 95, 60]

print(scores[0])
print(scores[-1])

scores.append(88)
print(len(scores))
print(sorted(scores))
```

**Output:**
```
85
60
6
[60, 78, 85, 88, 92, 95]
```

## Example 2: Dictionaries

```python
student = {
    "name": "Alice",
    "age": 21,
    "grade": "A"
}

print(student["name"])
student["age"] = 22
print(student)
print(list(student.keys()))
```

**Output:**
```
Alice
{'name': 'Alice', 'age': 22, 'grade': 'A'}
['name', 'age', 'grade']
```

## Example 3: Sets

Sets automatically remove duplicates and support fast membership checks.

```python
tags = {"python", "coding", "python", "beginner", "coding"}
print(tags)
print("python" in tags)

tags.add("loops")
print(len(tags))
```

**Output:**
```
{'beginner', 'coding', 'python'}
True
4
```
