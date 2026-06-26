---
name: jz-vin-cartype
description: 使用积智数据 VIN 车型解析 API，通过 17 位 VIN 车架号查询车辆的车型信息：如品牌、车型、车系、年款、销售类型、发动机、变速箱等信息。
metadata: { "openclaw": {  "requires": { "bins": ["python3"], "env": ["JZ_API_KEY"] }, "primaryEnv": "JZ_API_KEY" } }
---

# 积智数据 VIN 车型解析（ VIN）

基于 [VIN 车型解析 API] 的 OpenClaw 技能，支持：

- **VIN 查询**：通过 17 位 VIN 车架号查询车型信息：如品牌、车型、车系、年款、销售类型、发动机、变速箱等信息；


使用技能前需要申请数据，请联系【积智数据】 15821282326获取。

## 后端服务
本技能依赖积智数据 VIN 解析服务，接口地址：https://erp.qipeidao.com/jzOpenClaw/getVinCarType

## 环境变量配置

```bash
# Linux / macOS
export JZ_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JZ_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/vincartype/get_vin_cartype.py`

## 使用方式

### 1. 按 VIN 车架号查询车辆信息

```bash
python3 skills/vincartype/get_vin_cartype.py LSVAL41Z882104202
```

```
## VIN 车型查询请求参数

| 字段名  | 类型   | 必填 | 说明                                           |
|--------|--------|------|------------------------------------------------|
| vin    | string | 是   | 17 位 VIN 车架号                               |

示例：

```
LSVAL41Z882104202
```

## VIN 查询返回结果示例

脚本直接输出接口 `model` 字段，结构与示例一致（示例简化）：

```json
 {
    "id": 516,
    "lyId": "PAACJ00236",
    "carType": "Wrangler [牧马人]",
    "manufacturers": "克莱斯勒",
    "lyBrand": "Jeep",
    "lySubBrand": "克莱斯勒",
    "carSystem": "Wrangler [牧马人]",
    "salesName": "2.0T 手自一体 Rubicon 四门版",
    "productTime": "2019",
    "engineType": "N",
    "displacement": "2.0",
    "oilDrive": "汽油",
    "driveType": "前置四驱",
    "chassis": "JL",
    "transmissionDesc": "手自一体变速器(AT)",
    "state": 0,
    "createTime": 1710500382000,
    "updateTime": 1710500382000
  }
```

当出现错误（如 VIN 不正确或无数据），脚本会输出：

```json
{
  "error": "api_error",
  "state": 202,
  "msg": "VIN不正确"
}
```


## 常见错误码


| 代号   | 说明      |
|------|---------|
| 10001 | 参数错误    |
| 10004 | VIN 不正确或无数据 |


## 在 OpenClaw 中的推荐用法

1. 用户给出车架号：「帮我查一下 VIN  `LSVAL41Z882104202` 是什么车」。  
2. 调用：  
   `python3 skills/vincartype/get_vin_cartype.py LSVAL41Z882104202 `  
3. 从返回中选取 `lyBrand/carType/carSystem/productTime/salesName/engineType/displacement/oilDrive/driveType/chassis/transmissionDesc` 等字段，给出自然语言总结；

