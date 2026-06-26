# 会员查询管理模块

> 通用说明：所有接口响应均包含 `error` 字段（int），`0` = 成功，非 `0` = 失败（此时 `message` 包含错误描述）。下表不再重复列出
`error`。

| 接口     | 方法  | 路由                             | 用途                   |
|--------|-----|--------------------------------|----------------------|
| 会员列表   | GET | /member/list/get               | 按昵称/姓名/手机号/ID搜索会员    |
| 会员详情   | GET | /member/list/get               | 按会员ID获取详情（传 `id` 参数） |
| 手机号查ID | GET | /member/index/get-id-by-mobile | 通过手机号获取会员ID          |

---

## 获取会员列表

`GET /member/list/get`

根据会员昵称、真实姓名、手机号、会员ID搜索会员信息。

**请求参数：**

| 字段        | 类型     | 必传 | 说明                         |
|-----------|--------|----|----------------------------|
| keywords  | string | 否  | 搜索关键字（可匹配昵称、真实姓名、手机号、会员ID） |
| page      | int    | 否  | 页码（默认 1）                   |
| page_size | int    | 否  | 每页数量（默认 6）                 |

**响应字段：**

| 字段                   | 类型     | 说明                   |
|----------------------|--------|----------------------|
| total                | int    | 当前条件下的总数量            |
| page                 | int    | 当前页                  |
| page_size            | int    | 每页数量                 |
| list[].id            | int    | 会员ID                 |
| list[].avatar        | string | 头像地址                 |
| list[].nickname      | string | 昵称                   |
| list[].realname      | string | 真实姓名                 |
| list[].mobile        | string | 手机号                  |
| list[].credit        | int    | 积分                   |
| list[].balance       | float  | 余额                   |
| list[].is_black      | int    | 是否是黑名单：`0` 否 / `1` 是 |
| list[].level_id      | int    | 等级ID                 |
| list[].source        | int    | 来源                   |
| list[].create_time   | string | 创建时间                 |
| list[].remark        | string | 备注                   |
| list[].order_count   | int    | 订单数量                 |
| list[].money_count   | float  | 订单金额                 |
| list[].last_pay_time | string | 最后支付时间               |
| list[].is_black_name | string | 是否黑名单                |
| list[].level_name    | string | 等级名称                 |
| list[].group_name    | string | 标签名                  |
| list[].source_name   | string | 来源渠道                 |

```json
{
    "error": 0,
    "total": 1,
    "list": [
        {
            "id": "317",
            "avatar": "https://xxx.jpg",
            "nickname": "An",
            "realname": "李可鑫",
            "mobile": "15888888888",
            "credit": "9981290",
            "balance": "935276.97",
            "is_black": 0,
            "level_id": "447",
            "source": "40",
            "create_time": "2021-12-13 10:10:35",
            "remark": "",
            "order_count": "104",
            "money_count": "65030.82",
            "last_pay_time": "2026-03-04 21:01:02",
            "is_black_name": "否",
            "level_name": "市长",
            "group_name": "简单明了,复杂繁琐",
            "source_name": "APP"
        }
    ],
    "page": 1,
    "page_size": 20
}
```

---

## 获取会员详情

`GET /member/detail/get`

根据会员ID获取会员详情（传 `id` 参数时返回单个会员详细信息）。

**请求参数：**

| 字段 | 类型  | 必传 | 说明   |
|----|-----|----|------|
| id | int | 是  | 会员ID |

**响应字段：**

| 字段                    | 类型     | 说明                    |
|-----------------------|--------|-----------------------|
| member.id             | int    | 会员ID                  |
| member.avatar         | string | 头像地址                  |
| member.nickname       | string | 昵称                    |
| member.realname       | string | 真实姓名                  |
| member.mobile         | string | 手机号                   |
| member.credit         | int    | 积分                    |
| member.balance        | float  | 余额                    |
| member.level_id       | int    | 等级ID                  |
| member.source         | int    | 来源                    |
| member.last_time      | string | 最后登录时间                |
| member.is_deleted     | int    | 是否删除：`0` 否 / `1` 是    |
| member.create_time    | string | 注册时间                  |
| member.is_black       | int    | 是否黑名单：`0` 否 / `1` 是   |
| member.remark         | string | 备注                    |
| member.is_bind_mobile | int    | 是否绑定手机号：`0` 否 / `1` 是 |
| member.birthday       | string | 生日                    |
| member.level_name     | string | 等级名称                  |
| member.password_set   | int    | 是否设置密码：`0` 否 / `1` 是  |
| member.group_name     | string | 标签名                   |
| member.is_black_name  | string | 是否黑名单（文字）             |
| member.member_code    | string | 会员码                   |
| member.source_name    | string | 来源渠道                  |

```json
{
    "error": 0,
    "member": {
        "id": "317",
        "avatar": "https://xxx.jpg",
        "nickname": "An",
        "realname": "李可鑫",
        "level_id": "447",
        "mobile": "15888888888",
        "credit": "9981290",
        "balance": "935276.97",
        "source": "40",
        "last_time": "2026-03-05 17:28:12",
        "is_deleted": "0",
        "create_time": "2021-12-13 10:10:35",
        "is_black": 0,
        "remark": "-",
        "is_bind_mobile": "0",
        "birthday": "0000-00-00 00:00:00",
        "level_name": "市长",
        "password_set": 1,
        "group_name": "简单明了,复杂繁琐",
        "is_black_name": "否",
        "member_code": "000000000000000317",
        "source_name": "APP"
    }
}
```

---

## 通过手机号获取会员ID

`GET /member/index/get-id-by-mobile`

**请求参数：**

| 字段     | 类型     | 必传 | 说明  |
|--------|--------|----|-----|
| mobile | string | 是  | 手机号 |

**响应字段：**

| 字段        | 类型  | 说明   |
|-----------|-----|------|
| member_id | int | 会员ID |

```json
{
    "error": 0,
    "member_id": "317"
}
```
