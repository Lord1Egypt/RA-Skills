---
name: radiation
description: Record and track medical radiation exposure from imaging tests with automatic dose calculation based on body surface area and cumulative dose tracking.
argument-hint: <操作类型(添加/状态/历史/清空) 检查类型 检查部位 [检查日期]>
allowed-tools: Read, Write
schema: radiation/schema.json
---

# 医学辐射暴露管理技能

记录、追踪和查询医学影像检查的辐射暴露情况，帮助管理累积辐射剂量。

## 核心流程

```
用户输入 -> 解析操作类型 -> [add] 解析检查信息 -> 计算辐射剂量 -> 保存 -> 显示累积
                              -> [status] 计算累积剂量 -> 输出报告
                              -> [history] 显示历史记录
                              -> [clear] 确认清空
```

## 步骤 1: 解析操作类型

| Input Keywords | Operation |
|---------------|-----------|
| add | add |
| status | status |
| history | history |
| clear | clear |

## 步骤 2: 添加辐射记录 (add)

### 检查信息解析

- **检查类型**：CT、X光、PET-CT、骨扫描、血管造影等
- **检查部位**：头部、胸部、腹部、盆腔、脊柱、四肢等
- **检查日期**：格式 YYYY-MM-DD，默认为今天

### 辐射剂量参考表

**CT检查（标准剂量）：**
| 部位 | 剂量 |
|------|------|
| 头部 | 2 mSv |
| 胸部 | 7 mSv |
| 腹部 | 8 mSv |
| 盆腔 | 6 mSv |
| 脊柱 | 6 mSv |
| 全身 | 10 mSv |

**X光检查（标准剂量）：**
| 部位 | 剂量 |
|------|------|
| 胸部 | 0.1 mSv |
| 腹部 | 0.7 mSv |
| 四肢 | 0.01 mSv |
| 牙齿 | 0.005 mSv |

**其他检查：**
| 类型 | 剂量 |
|------|------|
| PET-CT | 14 mSv |
| 骨扫描 | 6 mSv |
| 血管造影 | 5-15 mSv |
| 乳腺钼靶 | 0.4 mSv |

### 剂量计算

```
调整系数 = 实际体表面积 / 1.73
实际剂量 = 标准剂量 × 调整系数
```

体表面积从 `data/profile.json` 读取。

### 辐射衰减计算

```
残留剂量 = 初始剂量 × (0.5)^(经过年数)
```

## 步骤 3: 生成 JSON

```json
{
  "id": "20251231123456789",
  "exam_type": "CT",
  "body_part": "胸部",
  "exam_date": "2025-12-31",
  "standard_dose": 7.0,
  "body_surface_area": 1.85,
  "adjustment_factor": 1.07,
  "actual_dose": 7.5,
  "dose_unit": "mSv"
}
```

## 步骤 4: 保存数据

文件路径：`data/radiation-records.json`

## 步骤 5: 查看累积状态 (status)

### 计算累积剂量

```
1. 按年份分组统计
2. 计算往年剂量残留（指数衰减）
3. 计算本年累积剂量
4. 计算总有效剂量
```

### 安全阈值

| 状态 | 剂量范围 |
|-----|---------|
| 安全 | < 1 mSv/年 |
| 关注 | 1-10 mSv/年 |
| 警告 | 10-50 mSv/年 |
| 危险 | > 50 mSv/年 |

## 执行指令

```
1. 解析操作类型
2. [add] 解析检查信息 -> 计算剂量 -> 保存 -> 显示累积
3. [status] 读取记录 -> 计算累积 -> 显示报告
4. [history] 读取记录 -> 格式化显示
5. [clear] 确认 -> 删除所有记录
```

## 示例交互

### 添加CT检查
```
用户: 添加CT 胸部

输出:
✅ 辐射记录已添加
检查项目：胸部 CT
辐射剂量：7.5 mSv
本年度累积：15.3 mSv
⚠️ 超过建议安全范围
```

### 查看累积状态
```
用户: 查看辐射累积

输出:
📊 辐射暴露累积报告
本年剂量：15.3 mSv
往年残留：3.2 mSv
总有效剂量：18.5 mSv
```

### 查看历史
```
用户: 查看辐射历史

输出:
📋 辐射暴露历史
2025年12月 (共3次，12.5 mSv)
12-31  胸部CT        7.5 mSv
...
```
