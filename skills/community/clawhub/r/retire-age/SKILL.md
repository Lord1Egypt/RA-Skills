---
name: retirement_age
description: 根据用户的职位信息、性别、出生年月计算该用户的退休时间
metadata:
  {
    "openclaw":
      {
        "emoji": "🎂",
        "requires": { "bins": ["uv"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      }
  }
---

# Retirement Age Calculator

根据中国渐进式延迟退休政策，计算用户的退休时间和退休年龄。

## 使用示例

```bash
uv run {baseDir}/scripts/calculate_age.py \
  --birth-year 1970 \
  --birth-month 5 \
  --role "男性"
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--birth-year` | 出生年份（如 1970） |
| `--birth-month` | 出生月份（1-12） |
| `--role` | 职位类型：`男性`、`女职工`、`女干部` |

## 退休政策说明

根据 2024 年 9 月发布的渐进式延迟退休政策：

- **男性**：从 60 岁逐步延迟到 63 岁（1965-1976 年出生为过渡期）
- **女职工**：从 50 岁逐步延迟到 55 岁（1975-1984 年出生为过渡期）
- **女干部**：从 55 岁逐步延迟到 58 岁（1970-1981 年出生为过渡期）

## 输出示例

```json
{
  "retirement_time": "2031年10月",
  "retirement_age": "61岁5个月"
}
```