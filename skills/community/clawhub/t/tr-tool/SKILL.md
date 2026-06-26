---
name: tr-tool
description: Translate or delete characters from input streams. Use for character substitution, deletion, and squeezing repeated characters.
---
# Tr - Character Translation Utility

Translate, squeeze, or delete characters from standard input. Replaces specified characters with alternatives or removes them entirely.

## Usage
```bash
tr-tool [options] <set1> [set2]
```

## Common Uses

- `'a-z' 'A-Z'`: Convert lowercase to uppercase
- `'\n' ' '`: Replace newlines with spaces
- `-d 'aeiou'`: Delete all vowels
- `-s ' '`: Squeeze repeated spaces

## Examples

```bash
echo "hello" | tr-tool 'a-z' 'A-Z'
echo "foo bar" | tr-tool -d ' '
echo "hello   world" | tr-tool -s ' '
```