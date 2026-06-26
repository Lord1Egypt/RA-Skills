# 常用地址文件 `~/.config/tms-takecar/addr.json`

用于保存快捷叫车和地址记忆流程依赖的常用地址数据。

## 1. 文件结构

顶层必须是 JSON object：

```json
{
  "家": {
    "name": "万科翡翠滨江",
    "address": "深圳市南山区沙河西路3088号",
    "poiid": "B0FFXXXX01",
    "citycode": "440300",
    "point_name": "万科翡翠滨江北门",
    "point_longitude": 113.934528,
    "point_latitude": 22.521867
  },
  "公司": {
    "name": "腾讯滨海大厦",
    "address": "深圳市南山区滨海大道33号",
    "poiid": "B0FFXXXX02",
    "citycode": "440300",
    "point_name": "腾讯滨海大厦北门",
    "point_longitude": 113.941245,
    "point_latitude": 22.520031
  }
}
```

## 2. 字段约束

- key：地址别名，只允许使用语义键，例如 `家`、`公司`、`小宝学校`。
- value：必须是用户最终确认后的 `poi_search` 单条返回结果对象。
- 禁止手填、猜测、裁剪字段，必须原样保留 `poi_search` 返回中用于下游流程的地址与推荐点字段。

## 3. 必需字段

每个地址对象至少包含以下字段：

| 字段 | 含义 |
| --- | --- |
| `name` | POI 名称 |
| `address` | POI 地址 |
| `poiid` | POI 唯一标识 |
| `citycode` | 城市编码 |
| `point_name` | 推荐上下车点名称 |
| `point_longitude` | 推荐点经度 |
| `point_latitude` | 推荐点纬度 |

## 4. 读写规则

1. 读取快捷场景前，必须先加载本文件并按别名取值。
2. 若别名不存在、字段缺失或对象损坏，必须回退到地址检索流程，重新调用 `poi_search`。
3. 写入时仅允许整条地址对象新增或整条覆盖，禁止字段级部分更新。
4. 下游写入 `state.json` 时，`pickup` / `dropoff` 的字段值必须直接来自本文件对应对象。
