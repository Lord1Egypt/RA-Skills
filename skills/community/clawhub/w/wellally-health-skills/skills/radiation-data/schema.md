# 辐射剂量计算参考数据 Schema

辐射剂量参考数据的完整定义。

## CT剂量标准值 (ct_doses)

单位：mSv

| 部位 | 剂量 |
|-----|------|
| head | 2 |
| chest | 7 |
| abdomen | 8 |
| pelvis | 6 |
| spine | 6 |
| limbs | 0.1 |
| whole_body | 10 |

## X光剂量标准值 (xray_doses)

单位：mSv

| 部位 | 剂量 |
|-----|------|
| chest | 0.1 |
| abdomen | 0.7 |
| limbs | 0.01 |
| dental | 0.005 |

## 其他检查剂量 (other_doses)

单位：mSv

| 类型 | 剂量 |
|-----|------|
| pet_ct | 14 |
| bone_scan | 6 |
| angiography | 5-15 |
| mammography | 0.4 |

## 安全阈值 (safety_thresholds)

| 类型 | 值 |
|-----|-----|
| natural_background | 2.4 mSv/年 |
| public_limit | 1 mSv/年 |
| occupational_limit | 20 mSv/年 |
| medical_advisory | 10 mSv/年 |

## 衰减模型

```
残留剂量 = 初始剂量 × (0.5)^(经过年数)
```
