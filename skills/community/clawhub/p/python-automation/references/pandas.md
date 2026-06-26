# Pandas Data Analysis Quick Reference

## Setup
```bash
pip install pandas openpyxl matplotlib
```

## Common Patterns

### Reading data
```python
import pandas as pd

df = pd.read_csv("data.csv")
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
df = pd.read_json("data.json")
df = pd.read_html("https://table-page.com")[0]  # parse HTML tables
```

### Data exploration
```python
df.head(10)
df.info()
df.describe()
df["column"].value_counts()
df.isnull().sum()
```

### Filtering
```python
df[df["age"] > 30]
df[(df["city"] == "KL") & (df["active"] == True)]
df.query("age > 30 and city == 'KL'")
```

### Grouping & aggregation
```python
df.groupby("category")["amount"].sum()
df.groupby(["year", "month"]).agg({"sales": "sum", "orders": "count"})
df.pivot_table(values="amount", index="city", columns="category", aggfunc="sum")
```

### Column operations
```python
df["total"] = df["price"] * df["quantity"]
df["date"] = pd.to_datetime(df["date_str"])
df.rename(columns={"old_name": "new_name"}, inplace=True)
df.drop(columns=["unused"], inplace=True)
```

### Export
```python
df.to_csv("output.csv", index=False)
df.to_excel("output.xlsx", sheet_name="Data", index=False)
df.to_json("output.json", orient="records")
```

### Merge / Join
```python
pd.merge(df1, df2, on="key", how="left")
pd.concat([df1, df2], axis=0)  # row bind
pd.concat([df1, df2], axis=1)  # column bind
```

### Date range filtering
```python
df[df["date"].between("2024-01-01", "2024-12-31")]
df.set_index("date").resample("M")["sales"].sum()
```
