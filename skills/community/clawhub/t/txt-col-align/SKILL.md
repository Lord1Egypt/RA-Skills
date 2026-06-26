# Text Column Aligner

Aligns columns in plain text tables using custom or auto-detected delimiters, making messy logs or CSV-like data human-readable with clean spacing.

## Usage

```bash
# Align columns in a CSV file
txt_col_align data.csv

# Use a custom delimiter (semicolon)
txt_col_align -d ';' logs.txt

# Pipe data directly
echo -e "name;score;rank\nAlice;95;1\nBob;87;2" | txt_col_align -d ';'

# Increase padding between columns
txt_col_align --padding 4 data.txt
```

## Price

$2.00
