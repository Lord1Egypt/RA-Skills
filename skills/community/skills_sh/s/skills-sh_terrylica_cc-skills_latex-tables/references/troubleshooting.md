**Skill**: [LaTeX Tables with tabularray](../SKILL.md)

## Common Issues

### Issue: Table Too Wide

**Solution 1: Fixed-width columns**

```latex
% Instead of:
colspec = {ccc}

% Use fixed widths that fit:
colspec = {Q[2cm] Q[3cm] Q[2cm]}
```

**Solution 2: Flexible columns**

```latex
colspec = {XXX}  % All columns expand equally
```

**Solution 3: Scale table**

```latex
\usepackage{graphicx}

\begin{table}[h]
  \resizebox{\textwidth}{!}{%
    \begin{tblr}{...}
      % table content
    \end{tblr}
  }
\end{table}
```

### Issue: Text Not Wrapping

**Problem:** Using `c` or `l` or `r` doesn't wrap

**Solution:** Use `Q[width]` for wrapping

```latex
% ❌ Won't wrap:
colspec = {ccc}

% ✅ Will wrap:
colspec = {Q[3cm] Q[4cm] Q[3cm]}
```

### Issue: Alignment in Fixed-Width Column

```latex
% Left-aligned in fixed width
Q[3cm, l]

% Centered in fixed width
Q[3cm, c]

% Right-aligned in fixed width
Q[3cm, r]
```

