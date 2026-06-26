# Recipes: Seaborn snippets (one-off, not in JSON spec)

These are quick scripts when you want richer statistical plots.

All snippets assume:

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")
df = pd.read_csv("data.csv")
```

## Distribution: histogram + KDE

```python
plt.figure(figsize=(10,6), dpi=250)
sns.histplot(df["col"], bins=50, kde=True)
plt.title("col distribution (hist + KDE)")
plt.xlabel("col"); plt.ylabel("count")
plt.tight_layout(); plt.savefig("out/plots/dist_kde.png", bbox_inches="tight", facecolor="white")
```

## Distribution by group: KDE curves

```python
plt.figure(figsize=(10,6), dpi=250)
sns.kdeplot(data=df, x="value", hue="group", common_norm=False)
plt.title("value distribution by group (KDE)")
plt.tight_layout(); plt.savefig("out/plots/kde_by_group.png", bbox_inches="tight", facecolor="white")
```

## Box / violin by group

```python
plt.figure(figsize=(10,6), dpi=250)
sns.violinplot(data=df, x="group", y="value", inner="quartile")
# or: sns.boxplot(data=df, x="group", y="value")
plt.title("value by group")
plt.xticks(rotation=30, ha="right")
plt.tight_layout(); plt.savefig("out/plots/violin.png", bbox_inches="tight", facecolor="white")
```

## Correlation heatmap

```python
sns.set_theme(style="white")
num = df.select_dtypes(include=["number"]).corr()
plt.figure(figsize=(9,7), dpi=250)
sns.heatmap(num, cmap="vlag", center=0, square=True)
plt.title("correlation")
plt.tight_layout(); plt.savefig("out/plots/corr.png", bbox_inches="tight", facecolor="white")
```

## Pairplot (quick overview)

```python
# Beware: can be slow on big tables
pp = sns.pairplot(df.select_dtypes(include=["number"]).sample(min(len(df), 500)))
pp.fig.suptitle("pairplot", y=1.02)
pp.savefig("out/plots/pairplot.png", dpi=200)
```
