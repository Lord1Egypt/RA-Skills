**Skill**: [LaTeX Tables with tabularray](../SKILL.md)

## Migration from Old Packages

### From tabular

```latex
% Old:
\begin{tabular}{|c|c|c|}
  \hline
  A & B & C \\
  \hline
\end{tabular}

% New:
\begin{tblr}{
  colspec = {ccc},
  hlines, vlines
}
  A & B & C \\
\end{tblr}
```

### From tabularx

```latex
% Old:
\begin{tabularx}{\textwidth}{|l|X|r|}
  \hline
  Left & Middle & Right \\
  \hline
\end{tabularx}

% New:
\begin{tblr}{
  width = \textwidth,
  colspec = {lXr},
  hlines
}
  Left & Middle & Right \\
\end{tblr}
```
