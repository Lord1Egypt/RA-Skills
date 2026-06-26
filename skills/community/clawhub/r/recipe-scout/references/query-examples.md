# Query Formulation Examples

Use these patterns when constructing search queries for Tier A sources.

## By Dish

**番茄炒蛋:**
- `番茄炒蛋 家常菜 做法`
- `番茄炒蛋 下厨房`
- `番茄炒蛋 美食天下`
- `番茄炒蛋 少油版本`

**红烧牛腩 (with Instant Pot):**
- `红烧牛腩 高压锅 做法`
- `红烧牛腩 Instant Pot 中文`
- `牛腩炖土豆 家常菜谱`

## Constraint Modifiers

Append to base query as needed:

| Constraint | Modifier |
|-----------|---------|
| 川菜 style | `川菜 做法` |
| Low oil | `少油 清淡` |
| Air fryer | `空气炸锅` |
| High protein | `高蛋白` |
| Under 15 min | `15分钟 快手` |
| Ingredient restriction | `不放<食材>` / `素` |

## Recommended Primary Sources

| Source | Strengths | Access pattern |
|--------|-----------|----------------|
| 下厨房 | User-generated, trend sections, wide coverage | Search: `<菜名> site:xiachufang.com` |
| 美食天下 | 菜谱大全 structure, good for broad recall | Search: `<菜名> site:meishichina.com` |
| 豆果美食 | Large recipe app ecosystem | Search: `<菜名> 豆果美食` |
| **HowToCook** | Precise gram-level measurements, programmer-friendly, no ads | Raw fetch: `https://raw.githubusercontent.com/Anduin2017/HowToCook/master/dishes/<category>/<dish>/<dish>.md` |
| The Woks of Life | English, excellent normalization, cross-validation | Direct fetch: `thewoksoflife.com/<dish-slug>/` |
| Omnivore's Cookbook | English, Chinese home-style focus | Direct fetch: `omnivorescookbook.com/<dish-slug>/` |
| China Sichuan Food | English, Sichuan specialist | Direct fetch: `chinasichuanfood.com/<dish-slug>/` |

## HowToCook Category Map

| Category folder | Contents |
|----------------|----------|
| `meat_dish` | 宫保鸡丁, 红烧肉, 回锅肉, 糖醋里脊 … |
| `aquatic` | 清蒸鲈鱼, 红烧鱼, 酸菜鱼 … |
| `vegetable_dish` | 蒜蓉西兰花, 地三鲜, 拍黄瓜 … |
| `staple` | 蛋炒饭, 煮面条 … |
| `soup` | 番茄蛋花汤, 酸辣汤 … |
| `condiment` | 辣椒油, 葱油 … |
