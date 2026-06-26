# Chapter 5: Working with Files

Python can read from and write to files using the built-in `open()` function. Always use a `with` block — it closes the file automatically when you're done, even if an error occurs.

## Example 1: Writing to a file

```python
with open("notes.txt", "w") as f:
    f.write("Python is fun.\n")
    f.write("Files are easy.\n")

print("File written.")
```

**Output:**
```
File written.
```

## Example 2: Reading a file line by line

```python
with open("notes.txt", "r") as f:
    for line in f:
        print(line.strip())
```

**Output:**
```
Python is fun.
Files are easy.
```

## Example 3: Appending to an existing file

Opening with `"a"` adds content after whatever is already in the file instead of overwriting it.

```python
with open("notes.txt", "a") as f:
    f.write("Appending is simple.\n")

with open("notes.txt", "r") as f:
    print(f.read())
```

**Output:**
```
Python is fun.
Files are easy.
Appending is simple.
```
