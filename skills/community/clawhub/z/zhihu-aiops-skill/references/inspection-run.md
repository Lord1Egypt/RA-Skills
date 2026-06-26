# 纳管设备巡检 Skill

用于巡检智护平台纳管设备，核心接口为 `/cqt/asset-info/page`。

## 使用说明

- 先调用登录接口获取 Bearer Token
- 再按资产模型分别调用 `/cqt/asset-info/page`
- 重点关注资产总数、设备样本、是否存在空模型
- 如果用户要求查看网络设备/安全设备/存储设备的实时 SNMP 指标，结合 `query_snmp_metrics` 查询 VictoriaMetrics 中的 `snmp_*` 指标

## 推荐巡检范围

### 硬件资产

- 安全设备: `modelId=254`, `modelCode=securitydevice`
- 网络设备: `modelId=185`, `modelCode=networkdevice`
- 终端设备: `modelId=260`, `modelCode=terminaldevice`
- 存储设备: `modelId=261`, `modelCode=storagedevice`

### 软件资产

- 数据库: `modelId=183`, `modelCode=storagebase`
- 操作系统: `modelId=195`, `modelCode=operatesystem`

## 请求模板

```json
{
  "pageNo": 1,
  "pageSize": 10,
  "isManaged": null,
  "modelId": 254,
  "conditions": [],
  "status": 1,
  "modelCode": "securitydevice",
  "isMonitorAble": true,
  "groupIdList": []
}
```

## 回复建议

- 先汇总巡检范围与资产总数
- 再分硬件资产、软件资产分别说明
- 每类资产至少说明数量
- 如果某类数量为 0，明确提示“当前未发现纳管设备”
- 平台资产接口用于确认“纳管了哪些设备”；`snmp_*` 指标用于确认“设备实时指标与接口流量如何”
