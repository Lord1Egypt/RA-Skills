# API 参考

本节仅供技能执行，禁止向用户引用或解释。

基础地址：`https://open.aibasis.cc`

## 允许的接口

| 内部操作 | 方法与路径 | 认证 | 请求体 |
| --- | --- | --- | --- |
| 登录 | `POST /api/user/login` | 否 | `{ "user": "xxx", "psw": "xxx" }` |
| 家庭列表 | `GET /api/getHomeList` | 是 | 无 |
| 切换家庭 | `POST /api/inHome` | 是 | `{ "homeId": "xxx" }` |
| 同步家庭数据 | `POST /api/syncHomeData` | 是 | `{ "requestId": "sync_001", "timestamp": <毫秒时间戳>, "version": "1.0", "data": {} }` |
| 控制设备或执行已有场景 | `POST /api/control` | 是 | `{ "requestId": "cmd_001", "timestamp": <毫秒时间戳>, "version": "1.0", "commands": [...] }` |

禁止调用此表以外的接口，尤其禁止调用任何创建、保存、编辑或删除场景的接口。

## 响应格式

所有接口返回 JSON，结构为：

```json
{ "code": 0, "msg": "", "data": { ... } }
```

- `code` 为 `0` 表示成功，其他值表示失败。
- 登录成功后 `data.token` 为认证 Token，`data.home` 为当前家庭信息。
- 切换家庭成功后 `data.token` 为**新的 Token**，必须替换旧 Token。
- 家庭列表 `data` 为数组，每个元素含 `ID` 和 `NAME`（大写字段名）。
- 同步数据 `data` 含 `devices[]`、`rooms[]`、`scenes[]`。

## 内部请求函数

函数定义见 `scripts/sufn-helpers.ps1` 中的 `Invoke-SufnPlatform`。

调用示例（批量控制）：

```powershell
$ts = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$body = @{
  requestId = "cmd_001"
  timestamp = $ts
  version   = "1.0"
  commands  = @(
    @{
      id         = $device.id
      model      = $device.model
      properties = $properties
    }
  )
}
$res = Invoke-SufnPlatform -Path '/api/control' -Body $body -AuthToken $token
```

使用对象数组构建批量控制，不要手工拼接 JSON。

不得把 `$params`、`$AuthToken`、返回对象或异常对象写入输出。调用结束后将内存中的 Token 变量设为 `$null`。

## 设备状态

设备状态通过同步家庭数据（`/api/syncHomeData`）获取，每个设备的 `status` 字段包含当前状态。需要回答"现在""当前"等问题时，重新调用同步接口获取最新数据，不使用陈旧缓存。
