**Skill**: [LaTeX Tables with tabularray](../SKILL.md)

## Common Table Patterns

### 1. Simple Table with Lines

```latex
\begin{table}[h]
  \centering
  \begin{tblr}{
    colspec = {ccc},    % 3 centered columns
    hlines,              % Horizontal lines
    vlines               % Vertical lines
  }
    Header 1 & Header 2 & Header 3 \\
    Data 1   & Data 2   & Data 3   \\
    More 1   & More 2   & More 3   \\
  \end{tblr}
  \caption{My table}
\end{table}
```

### 2. Fixed-Width Columns

```latex
\begin{table}[h]
  \centering
  \begin{tblr}{
    colspec = {Q[2cm] Q[4cm] Q[2cm]},  % Fixed widths: 2cm, 4cm, 2cm
    hlines, vlines
  }
    Short & This is longer text that wraps & Data \\
    A     & More wrapping content here     & B    \\
  \end{tblr}
\end{table}
```

### 3. Mixed Column Types

```latex
\begin{tblr}{
  colspec = {l Q[3cm,c] r},  % Left, centered fixed-width, right
  hlines
}
  Left-aligned & Centered in 3cm & Right-aligned \\
  Text         & More text       & 123           \\
\end{tblr}
```

### 4. No Lines (Minimal Style)

```latex
\begin{tblr}{
  colspec = {lcc},
  row{1} = {font=\bfseries}  % Bold first row (header)
}
  Name     & Age & City    \\
  Alice    & 25  & Boston  \\
  Bob      & 30  & Seattle \\
\end{tblr}
```

### 5. Colored Rows/Columns

```latex
\usepackage{xcolor}

\begin{tblr}{
  colspec = {ccc},
  row{1} = {bg=blue!20},      % Light blue header
  row{even} = {bg=gray!10}    % Alternate row colors
}
  Header 1 & Header 2 & Header 3 \\
  Data 1   & Data 2   & Data 3   \\
  Data 4   & Data 5   & Data 6   \\
\end{tblr}
```

