# 工具服务 API

## 坐标转换

将其他坐标系批量转换到腾讯地图坐标系（GCJ-02）。

> **注意**：此接口**仅支持将其他坐标系转换到腾讯地图坐标系**，不支持反向转换。`locations` 参数字符总长度不超过2048个。

**接口**: `GET /ws/coord/v1/translate`

**请求参数**:
- `key` (必填): 开发密钥
- `locations` (必填): 坐标串，格式 `lat1,lng1;lat2,lng2`（经纬度小数点后不超过16位）
- `type` (必填): 输入坐标的坐标系类型
  - `1` — GPS 坐标（WGS-84）→ GCJ-02（**最常用**）
  - `2` — 搜狗经纬度 → GCJ-02
  - `3` — 百度经纬度（BD-09）→ GCJ-02（**常用**）
  - `4` — MapBar 经纬度 → GCJ-02
  - `6` — 搜狗墨卡托 → GCJ-02
- `output` (可选): 返回格式，`json`（默认）/ `jsonp`

**请求示例**:

GPS 坐标转腾讯地图坐标:
```
GET /ws/coord/v1/translate?key=YOUR_KEY&locations=39.984154,116.307490&type=1
```

百度坐标转腾讯地图坐标（批量）:
```
GET /ws/coord/v1/translate?key=YOUR_KEY&locations=39.984154,116.307490;30.21,115.43&type=3
```

**响应格式**:
```json
{
  "status": 0,
  "message": "Success",
  "locations": [
    {
      "lat": 39.985704,
      "lng": 116.313548
    }
  ]
}
```

> 转换后坐标数组的顺序与输入顺序一致。

---

## 公共错误码

完整错误码参考：https://lbs.qq.com/service/webService/webServiceGuide/status

### 常见错误码

| 状态码 | 含义 | 处理建议 |
|--------|------|----------|
| `0` | 成功 | — |
| `110` | 请求来源未被授权 | 检查 Key 的域名白名单或 IP 白名单配置 |
| `111` | 签名验证失败 | 检查签名算法和 Secret Key |
| `112` | IP 未被授权 | 在控制台添加服务器 IP 白名单 |
| `113` | 此功能未被授权 | 在控制台开通对应 API 权限 |
| `120` | 此 Key 每秒请求量已达到上限（QPS 限制） | 等待 1-2 秒后重试 |
| `121` | 此 Key 每日调用量已达到上限 | 升级配额或更换 Key |
| `190` | 无效的 Key | 确认 Key 是否已被删除或禁用 |
| `199` | 此 Key 未开启 WebService 功能 | 在控制台为 Key 启用 WebService |
| `300` | 缺少必要字段 | 检查必填参数是否齐全 |
| `301` | 缺少 key 参数 | 添加 `key` 参数 |
| `306` | 缺少参数 | 检查接口所需的必填参数 |
| `310` | 请求参数信息有误 | 检查请求参数格式和必填项 |
| `311` | Key 格式错误 | 检查 Key 是否正确 |
| `320` | 参数数据类型错误 | 检查参数值类型 |
| `347` | 查询无结果 | 尝试放宽搜索条件 |
| `365` | 纬度不能超过 ±90 | 检查坐标值范围 |
| `366` | 经度不能超过 ±180 | 检查坐标值范围 |
| `396` | 距离矩阵坐标点超限 | 最多 200 个坐标点，起终点数乘积最多 625 |
| `500` | 后端超时 | 稍后重试 |

**错误响应示例**:
```json
{
  "status": 311,
  "message": "key格式错误"
}
```

**QPS 限制处理建议**:
- 收到 `120` 错误时，等待 1-2 秒后重试
- 合理使用批量接口（如距离矩阵替代多次路线规划）
- 对频繁查询的结果做本地缓存

---

## 参考资源

- **官方文档**: https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview
- **Key 管理**: https://lbs.qq.com/dev/console/key/manage
- **配额说明**: https://lbs.qq.com/dev/console/quotaImprove
- **常见问题**: https://lbs.qq.com/faq/serverFaq/webServiceKey
- **状态码说明**: https://lbs.qq.com/service/webService/webServiceGuide/status
- **天气接口文档**: https://lbs.qq.com/service/webService/webServiceGuide/webServiceWeather
- **POI 分类表**: https://lbs.qq.com/service/webService/webServiceGuide/webServiceAppendix
