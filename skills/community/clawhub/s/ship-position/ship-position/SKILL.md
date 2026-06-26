---
name: ship-position
description: >-
  获取（岸基+卫星+移动）船舶最新位置信息。需配置 usertoken 后调用 HiFleet 位置 API。Use when user asks for vessel/ship position, latest position by MMSI, or 船位/位置/报位.
---

# 船位 / Ship Position

获取（岸基+卫星+移动）船舶最新位置信息。**使用前必须配置授权 token。**

## Token 配置 / Token Configuration

调用本技能前必须提供有效的 `usertoken`，任选其一方式：

1. **环境变量**：`HIFLEET_USER_TOKEN` 或 `HIFLEET_USERTOKEN`
2. **项目配置**：在项目根目录或 ClawHub 配置中设置 `usertoken` / `userToken`
3. **请求时传入**：若调用方支持，在请求参数中传入 `usertoken`

未配置 token 时，应提示用户：「请先配置 HiFleet 授权 token（如环境变量 HIFLEET_USER_TOKEN）后再使用船位查询。」

---

## API 规范 / API Spec

| 项目 | 值 |
|------|-----|
| **简要描述** | 获取（岸基+卫星+移动）船舶最新位置信息 |
| **请求 URL** | `https://api.hifleet.com/position/position/get/token` |
| **请求方式** | `GET` |

### 请求 Query 参数

| 参数名 | 示例值 | 必选 | 类型 | 说明 |
|--------|--------|------|------|------|
| mmsi | 413829443 | 是 | string | MMSI 号码 |
| usertoken | (从配置读取) | 是 | string | 授权 token |

### 成功响应示例

```json
{
    "result": "ok",
    "num": 1,
    "list": {
        "m": "413829443",
        "n": "ZHENRONG16",
        "sp": "0",
        "co": "0",
        "ti": "2022-04-25 10:31:53",
        "la": "1874.115",
        "lo": "7088.285598",
        "h": "0",
        "draught": "2.3",
        "eta": "-",
        "destination": "NANTONG",
        "destinationIdentified": "",
        "imonumber": "0",
        "callsign": "0",
        "type": "未知类型干货船",
        "buildyear": "NULL",
        "dwt": "-1",
        "fn": "China (Republic of)",
        "dn": "中国",
        "an": "CN",
        "l": "132",
        "w": "22",
        "rot": "0",
        "status": "未知"
    }
}
```

### 响应字段说明（list）

| 参数名 | 类型 | 说明 |
|--------|------|------|
| m | string | MMSI |
| n | string | 船名 |
| sp | string | 航速（节） |
| co | string | 航向（度） |
| ti | string | 最后更新时间（UTC+8） |
| la | string | 纬度（**分**，除以 60 后为度） |
| lo | string | 经度（**分**，除以 60 后为度） |
| h | string | 航艏向（度） |
| draught | string | 吃水（米） |
| eta | string | 预计抵港时间（UTC） |
| destination | string | AIS 填写的目的港 |
| destinationIdentified | string | 目的港（识别） |
| imonumber | string | IMO 号 |
| callsign | string | 呼号 |
| type | string | 船舶类型 |
| buildyear | string | 建造年份 |
| dwt | string | 载重吨 |
| fn | string | 船籍国（英文） |
| dn | string | 船籍国（中文） |
| an | string | 船籍国简称 |
| l | string | 船长（米） |
| w | string | 船宽（米） |
| rot | string | 转向率 |
| status | string | 状态 |

### 纬度经度换算

- **纬度（度）** = `parseFloat(list.la) / 60`
- **经度（度）** = `parseFloat(list.lo) / 60`

---

## 调用流程 / Call Flow

1. **检查 token**：若未配置 `usertoken`，返回提示并终止。
2. **校验 MMSI**：请求必须包含有效 `mmsi`（9 位数字字符串）。
3. **发起请求**：`GET https://api.hifleet.com/position/position/get/token?mmsi={mmsi}&usertoken={usertoken}`
4. **解析结果**：根据 `result === "ok"` 与 `list` 解析位置与船舶信息；若 `result !== "ok"`，按错误处理并提示用户。

---

## 调用示例（伪代码）/ Example

```text
# 获取 MMSI 413829443 的最新船位
GET https://api.hifleet.com/position/position/get/token?mmsi=413829443&usertoken=${HIFLEET_USER_TOKEN}
```

解析后向用户展示时，建议包含：船名、MMSI、最后更新时间、经纬度（度）、航速、航向、目的港、状态。
