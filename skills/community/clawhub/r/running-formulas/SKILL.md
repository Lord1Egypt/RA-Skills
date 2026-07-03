---
name: 跑步计算服务
description: 一个提供全面的跑步计算工具的MCP服务器，包括VDOT计算、训练配速、比赛时间预测、速度标记、心率区间和配速转换等功能。
version: 1.0.0
---

# 跑步计算服务

一个提供全面的跑步计算工具的MCP服务器，包括VDOT计算、训练配速、比赛时间预测、速度标记、心率区间和配速转换等功能。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Calculate VDOT according to Jack Daniels.

Args:
    distance: Distance in meters.
    time: Time in seconds.

Returns:
    dict:
        vdot (float): The calculated VDOT value, representing the runner's aerobic capacity based on the input distance and time. | `scripts.tools.daniels_calculate_vdot` |
| Get recommended training paces for a given VDOT, based on Jack Daniels' formulas.

Args:
    vdot: VDOT value.

Returns:
    dict:
        easy (dict): Recommended easy pace range with lower and upper bounds.
        marathon (dict): Recommended marathon pace with value and format.
        threshold (dict): Recommended threshold pace with value and format.
        interval (dict): Recommended interval pace with value and format.
        repetition (dict): Recommended repetition pace with value and format. | `scripts.tools.daniels_calculate_training_paces` |
| Predict race time for a target distance based on a current race performance.
Uses Jack Daniels' equivalent performance methodology.

Args:
    current_distance: Distance of known performance in meters.
    current_time: Time of known performance in seconds.
    target_distance: Distance for race time prediction in meters.

Returns:
    dict: Daniels' VDOT method prediction with value, format, and time_seconds. | `scripts.tools.daniels_predict_race_time` |
| Predict race time for a target distance based on a current race performance.
Uses Riegel's formula.

Args:
    current_distance: Distance of known performance in meters.
    current_time: Time of known performance in seconds.
    target_distance: Distance for race time prediction in meters.

Returns:
    dict: Riegel's formula prediction with value, format, and time_seconds. | `scripts.tools.riegel_predict_race_time` |
| Calculate velocity markers (vLT, CV, vVO2) from a race performance using McMillan methodology.

Args:
    distance: Race distance in meters
    time: Race time in seconds

Returns:
    Dictionary containing velocity markers with paces in MM:SS/km format | `scripts.tools.mcmillan_calculate_velocity_markers` |
| Predict race times for standard distances based on a single race performance using McMillan methodology.

Args:
    distance: Race distance in meters
    time: Race time in seconds

Returns:
    Dictionary containing predicted race times in HH:MM:SS format | `scripts.tools.mcmillan_predict_race_times` |
| Calculate training paces for all zones based on a race performance using McMillan methodology.

Args:
    distance: Race distance in meters
    time: Race time in seconds

Returns:
    Dictionary containing training paces organized by zones (endurance, stamina, speed, sprint) | `scripts.tools.mcmillan_calculate_training_paces` |
| Calculate heart rate training zones based on age, resting heart rate, and optional max heart rate.
Uses McMillan methodology with multiple max HR estimation formulas and both HRMAX and HRRESERVE methods.

Args:
    age: Runner's age in years
    resting_heart_rate: Resting heart rate in BPM
    max_heart_rate: Optional maximum heart rate in BPM (if None, will be estimated)

Returns:
    Dictionary containing estimated max HR, effective max HR, and training zones with both HRMAX and HRRESERVE calculations | `scripts.tools.mcmillan_heart_rate_zones` |
| Convert between different pace and speed units.

Args:
    value: The numeric value to convert.
    from_unit: Source unit ("min_km", "min_mile", "kmh", "mph").
    to_unit: Target unit ("min_km", "min_mile", "kmh", "mph").

Returns:
    dict:
        value (float): Converted numeric value.
        formatted (str): Human-readable formatted result.
        unit (str): Target unit descriptor.

Raises:
    ValueError: If from_unit or to_unit are not valid, or if conversion is not supported. | `scripts.tools.convert_pace` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.daniels_calculate_vdot
工具描述：Calculate VDOT according to Jack Daniels.

Args:
    distance: Distance in meters.
    time: Time in seconds.

Returns:
    dict:
        vdot (float): The calculated VDOT value, representing the runner's aerobic capacity based on the input distance and time.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|distance|number|true| |null|
|time|number|true| |null|

---

## scripts.tools.daniels_calculate_training_paces
工具描述：Get recommended training paces for a given VDOT, based on Jack Daniels' formulas.

Args:
    vdot: VDOT value.

Returns:
    dict:
        easy (dict): Recommended easy pace range with lower and upper bounds.
        marathon (dict): Recommended marathon pace with value and format.
        threshold (dict): Recommended threshold pace with value and format.
        interval (dict): Recommended interval pace with value and format.
        repetition (dict): Recommended repetition pace with value and format.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|vdot|number|true| |null|

---

## scripts.tools.daniels_predict_race_time
工具描述：Predict race time for a target distance based on a current race performance.
Uses Jack Daniels' equivalent performance methodology.

Args:
    current_distance: Distance of known performance in meters.
    current_time: Time of known performance in seconds.
    target_distance: Distance for race time prediction in meters.

Returns:
    dict: Daniels' VDOT method prediction with value, format, and time_seconds.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|current_distance|number|true| |null|
|current_time|number|true| |null|
|target_distance|number|true| |null|

---

## scripts.tools.riegel_predict_race_time
工具描述：Predict race time for a target distance based on a current race performance.
Uses Riegel's formula.

Args:
    current_distance: Distance of known performance in meters.
    current_time: Time of known performance in seconds.
    target_distance: Distance for race time prediction in meters.

Returns:
    dict: Riegel's formula prediction with value, format, and time_seconds.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|current_distance|number|true| |null|
|current_time|number|true| |null|
|target_distance|number|true| |null|

---

## scripts.tools.mcmillan_calculate_velocity_markers
工具描述：Calculate velocity markers (vLT, CV, vVO2) from a race performance using McMillan methodology.

Args:
    distance: Race distance in meters
    time: Race time in seconds

Returns:
    Dictionary containing velocity markers with paces in MM:SS/km format
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|distance|number|true| |null|
|time|number|true| |null|

---

## scripts.tools.mcmillan_predict_race_times
工具描述：Predict race times for standard distances based on a single race performance using McMillan methodology.

Args:
    distance: Race distance in meters
    time: Race time in seconds

Returns:
    Dictionary containing predicted race times in HH:MM:SS format
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|distance|number|true| |null|
|time|number|true| |null|

---

## scripts.tools.mcmillan_calculate_training_paces
工具描述：Calculate training paces for all zones based on a race performance using McMillan methodology.

Args:
    distance: Race distance in meters
    time: Race time in seconds

Returns:
    Dictionary containing training paces organized by zones (endurance, stamina, speed, sprint)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|distance|number|true| |null|
|time|number|true| |null|

---

## scripts.tools.mcmillan_heart_rate_zones
工具描述：Calculate heart rate training zones based on age, resting heart rate, and optional max heart rate.
Uses McMillan methodology with multiple max HR estimation formulas and both HRMAX and HRRESERVE methods.

Args:
    age: Runner's age in years
    resting_heart_rate: Resting heart rate in BPM
    max_heart_rate: Optional maximum heart rate in BPM (if None, will be estimated)

Returns:
    Dictionary containing estimated max HR, effective max HR, and training zones with both HRMAX and HRRESERVE calculations
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|age|integer|true| |null|
|resting_heart_rate|integer|true| |null|
|max_heart_rate|integer|false| |null|

---

## scripts.tools.convert_pace
工具描述：Convert between different pace and speed units.

Args:
    value: The numeric value to convert.
    from_unit: Source unit ("min_km", "min_mile", "kmh", "mph").
    to_unit: Target unit ("min_km", "min_mile", "kmh", "mph").

Returns:
    dict:
        value (float): Converted numeric value.
        formatted (str): Human-readable formatted result.
        unit (str): Target unit descriptor.

Raises:
    ValueError: If from_unit or to_unit are not valid, or if conversion is not supported.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |null|
|from_unit|string|true| |null|
|to_unit|string|true| |null|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据