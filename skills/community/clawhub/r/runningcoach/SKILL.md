
# Running Coach - 跑步教练助手

基于**全频训练法 (Percentage-based Training)** 为跑者管理训练计划，自动同步到 Intervals.icu。

---

## 目录

1. [首次使用设置](#1-首次使用设置)
2. [Intervals.icu API 配置](#2-intervalsicu-api-配置)
3. [训练计划上传规则](#3-训练计划上传规则)
4. [完整上传示例](#4-完整上传示例)
5. [全频训练法模板](#5-全频训练法模板)
6. [使用流程](#6-使用流程)

---

## 1. 首次使用设置

### 步骤1: 注册 Intervals.icu

1. 访问 [Intervals.icu](https://intervals.icu) 注册账号（网页版）

### 步骤2: 同步手表/运动App

在 Intervals.icu 中连接你的数据源：

1. 进入 **Settings** → **Connected Apps**
2. 启用以下同步：
   - **Coros** - 推荐 (同步最完整)
   - **Garmin** - 或使用Garmin
   - **Strava** - 作为备份

### 步骤3: 获取 API 凭证

1. 进入 **Settings** → 滚动到页面底部
2. 找到 **API Key** 部分
3. 点击 **Show** 查看或 **Regenerate** 重新生成
4. **记录以下信息**：
   - **API Key**: (如 `32iir45obp3qcnhzueze70ngv`)
   - **Athlete ID**: (URL中，如 `i461087`)

### 步骤4: 配置

**方式A: 环境变量** (推荐)
```bash
export INTERVALS_API_KEY="你的API_KEY"
export INTERVALS_ATHLETE_ID="你的ATHLETE_ID"
```

**方式B: 修改配置文件**
编辑 `config.json`：
```json
{
  "API_KEY": "你的API_KEY",
  "ATHLETE_ID": "你的ATHLETE_ID",
  "THRESHOLD_PACE": 217
}
```

---

## 2. Intervals.icu API 配置

### 获取凭证

1. 登录 [Intervals.icu](https://intervals.icu)
2. 进入 **Settings** → 找到 **API Key**
3. 记录 **Athlete ID** (URL中可见，如 `i461087`)

### 认证方式

```bash
# 用户名: API_KEY
# 密码: 实际的API Key
curl -u "API_KEY:你的API密钥" ...
```

**Python示例:**
```python
import base64
auth_string = f"API_KEY:{API_KEY}"
auth_b64 = base64.b64encode(auth_string.encode()).decode()
headers = {"Authorization": f"Basic {auth_b64}"}
```

---

## 2. 训练计划上传规则

### 标题格式 (name)

格式: `类型-详细说明`

| 类型 | 示例 |
|------|------|
| 间歇跑 | `间歇跑-1K x 8 @3:46-3:34` |
| 节奏跑 | `Tempo-15K @3:40` |
| 长距离 | `LSD-30K @4:30-3:34` |
| 轻松跑 | `轻松跑-8K @5:00` |
| 比赛日 | `比赛日：5K测试` |

### 分段描述格式 (description)

#### 绝对配速格式
```
- 距离 配速/km Pace
```

**示例:**
```
- 5km 4:31/km Pace
- 3km 3:34/km Pace
```

#### 关键格式要点
1. ✅ 用 `Pace` 关键字，**不是** `@` 符号
2. ✅ `/km` 单位不能省略
3. ✅ 每行以 `-` 开头
4. ✅ `3min` 写成 `3m`

#### 间歇组数格式
可以用 `4x` 格式，但要**单独一行**并换行：

```
热身:
- 3km 5:00/km Pace

间歇:
4x
- 1km 3:46/km Pace

恢复:
- 3m rest
```

#### 休息阶段格式
**重要:** 用 `3m rest` 不用纯 `rest`

```
- 3m rest
- 5m rest
```

#### 距离单位
**所有距离用km表示**

| 实际距离 | 写作 |
|----------|------|
| 800m | 0.8km |
| 1km | 1km |
| 1000m | 1km |

---

## 3. 配速区间参考

基于 **Threshold = 3:37/km** (5K 17:00目标)

```
配速区间(Threshold=3:37/km):
- Z1: >4:40/km  (Easy/恢复)
- Z2: 4:07-4:39/km  (有氧)
- Z3: 3:50-4:06/km  (Tempo)
- Z4: 3:37-3:49/km  (阈值)
```

### 常用配速速查

| 目标 | 配速区间 |
|------|----------|
| 5K 17:00 | 3:24/km |
| 10K 34:00 | 3:24/km |
| 半马 1:11:30 | 3:24/km |
| 全马 2:31:00 | 3:34/km |
| 全马 2:40:00 | 3:47/km |

---

## 4. 完整上传示例

### 周三 Threshold间歇
```json
{
  "name": "间歇跑-8x1K @3:46",
  "category": "WORKOUT",
  "type": "Run",
  "start_date_local": "2026-03-11T06:30:00",
  "description": "配速区间(Threshold=3:37/km):\n- Z1: >4:40/km\n- Z2: 4:07-4:39/km\n- Z3: 3:50-4:06/km\n- Z4: 3:37-3:49/km\n\n热身:\n- 3km easy\n\n间歇:\n8x\n- 1km 3:46/km Pace\n- 3m rest\n\n放松:\n- 3km easy",
  "distance": 14000,
  "athlete_id": "i461087"
}
```

### 周五 Tempo节奏跑
```json
{
  "name": "Tempo-15K @3:40",
  "category": "WORKOUT",
  "type": "Run",
  "start_date_local": "2026-03-13T06:30:00",
  "description": "热身:\n- 3km easy\n\n主训练:\n- 15km 3:40/km Pace\n\n放松:\n- 2km easy",
  "distance": 20000,
  "athlete_id": "i461087"
}
```

### 周日 LSD渐进
```json
{
  "name": "LSD-35K @4:30-3:34",
  "category": "WORKOUT",
  "type": "Run",
  "start_date_local": "2026-03-15T06:30:00",
  "description": "渐进:\n- 5km 4:30/km Pace\n- 5km 4:15/km Pace\n- 5km 4:00/km Pace\n- 5km 3:50/km Pace\n- 5km 3:40/km Pace\n- 5km 3:34/km Pace\n- 5km 3:30/km Pace",
  "distance": 35000,
  "athlete_id": "i461087"
}
```

---

## 5. API端点

| 操作 | 端点 |
|------|------|
| 创建训练 | `POST /api/v1/athlete/{id}/events?upsertOnUid=true` |
| 批量创建 | `POST /api/v1/athlete/{id}/events/bulk?upsertOnUid=true` |
| 更新训练 | `PUT /api/v1/athlete/{id}/events/{event_id}` |
| 删除训练 | `DELETE /api/v1/athlete/{id}/events/{event_id}` |
| 获取活动 | `GET /api/v1/athlete/{id}/activities?oldest=&newest=` |
| 获取计划 | `GET /api/v1/athlete/{id}/events?oldest=&newest=` |

---

## 6. 全频训练法模板

### 周一 - 轻松跑
- 距离: 8-10km
- 配速: 70-80% (5:00/km)
- 目的: 恢复

### 周二 - 有氧跑
- 距离: 12-15km
- 配速: 75-85% (4:30/km)
- 目的: 有氧基础

### 周三 - ⭐ 间歇跑 (强度日)
- 距离: 12-14km
- 结构: 热身 + 8x1km + 放松
- 配速: 90-95% (3:46-3:34/km)
- 目的: 阈值提升

### 周四 - 休息
- 完全休息或主动恢复

### 周五 - ⭐ Tempo (强度日)
- 距离: 15-20km
- 结构: 热身 + 12-15km Tempo + 放松
- 配速: 90-95% (3:40/km)
- 目的: 节奏耐力

### 周六 - 轻松跑
- 距离: 8-10km
- 配速: 70-80%
- 目的: 恢复

### 周日 - ⭐ LSD (强度日)
- 距离: 25-35km
- 结构: 渐进加速 (每5km提速)
- 配速: 80% → 95%
- 目的: 有氧耐力+心理韧性

---

## 7. 使用流程

### 首次设置
1. 获取 Intervals.icu API Key
2. 配置 ATHLETE_ID
3. 确定训练目标 (5K/10K/半马/全马)
4. 设置Threshold配速

### 每周流程
1. **周初** - 生成周计划 → 上传到 Intervals.icu
2. **训练前** - 评估状态 → 给出 GO/MODIFY/SKIP 建议
3. **训练后** - 数据汇总 → 复盘总结
4. **周复盘** - 分析负荷趋势 → 调整下周计划

---

## 8. 训练负荷目标参考

| 目标比赛 | 周负荷范围 |
|----------|------------|
| 5K/10K | 200-350 |
| 半马 | 300-450 |
| 全马 | 350-550 |

**ATL/CTL/TSB 正常范围:**
- ATL: 40-60 (短期疲劳)
- CTL: 40-60 (长期 fitness)
- TSB: -10 ~ +10 (最佳比赛窗口)

---

## 注意事项

1. **Coros同步**: Intervals.icu → Coros 同步时，绝对配速格式可正确传输
2. **训练负荷**: 必须为每段设置配速才能正确计算负荷
3. **阈值更新**: 比赛成绩提升后需更新Threshold配速
