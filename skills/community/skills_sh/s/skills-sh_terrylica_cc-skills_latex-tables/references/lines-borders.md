**Skill**: [LaTeX Tables with tabularray](../SKILL.md)

## Lines and Borders

### All Lines

```latex
\begin{tblr}{
  colspec = {ccc},
  hlines,              % All horizontal lines
  vlines               % All vertical lines
}
```

### Selective Lines

```latex
\begin{tblr}{
  colspec = {ccc},
  hline{1,2,Z} = {solid},  % Top, after header, bottom
  vline{2} = {dashed}      % Dashed line after column 1
}
```

### Thick Lines

```latex
\begin{tblr}{
  colspec = {ccc},
  hline{1,Z} = {2pt},     % Thick top/bottom
  hline{2} = {1pt}         % Thinner after header
}
```
