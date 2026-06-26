# 云展网 API 参考文档

> 所有接口基础域名：`https://www.yunzhan365.com`

---

## 登录获取 Token

**接口**: `POST https://www.yunzhan365.com/api/user/get-token`  
**Content-Type**: `application/json`

### 请求参数

```json
{
  "username": "*****",
  "password": "*****"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | **必填** | 邮箱或手机号 |
| password | string | **必填** | 密码 |

### 返回值

```json
{
  "code": "OK",
  "msg": "成功",
  "data": {
    "token": "************************"
  }
}
```

| 字段 | 说明 |
|------|------|
| code | `OK` 表示成功，其他均为失败 |
| msg | 消息内容 |
| data.token | 用户 Token |

---

## 文件上传

**接口**: `POST https://www.yunzhan365.com/api/common/upload-file`  
**Content-Type**: `multipart/form-data`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | binary | **必填** | 二进制文件 |
| cptoken | string | **必填** | 获取 Token 接口返回的 token |

### 返回值

```json
{
  "msg": "操作成功",
  "code": "OK",
  "data": {
    "fileName": "example.pdf",
    "fileSrc": "//book.yunzhan365.com/upload-control/files/example.pdf"
  }
}
```

| 字段 | 说明 |
|------|------|
| code | `OK` 表示成功，其他均为失败 |
| data.fileName | 文件名 |
| data.fileSrc | 文件访问路径（调用时需拼接 `https:` 前缀） |

---

## 创建电子书

**接口**: `POST https://www.yunzhan365.com/api/book/add-book`  
**Content-Type**: `application/json`

### 请求参数

```json
{
  "cptoken": "*****",
  "title": "*****",
  "description": "*****",
  "keyword": "*****",
  "htmlTemplate": "Mobile",
  "phoneTemplate": "Mobile",
  "filePath": '[{"link": "https://..."}]',
  "bookConfig": "{}",
  "engineType": "2",
  "convertMode": "-1",
  "seo_boost": "10"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cptoken | string | **必填** | Token |
| title | string | **必填** | 电子书标题 |
| description | string | **必填** | 电子书描述 |
| keyword | string | 可选 | 关键字 |
| htmlTemplate | string | 可选 | PC端模版 |
| phoneTemplate | string | 可选 | 移动端模版 |
| filePath | string | **必填** | 电子书源文件 JSON字符串格式|
| bookConfig | string | 可选 | 电子书配置 JSON字符串格式|
| engineType | string | 可选 | 转换引擎 |
| convertMode | string | 可选 | 切割类型 |
| seo_boost | string | 可选 | 允许爬虫 (1是/0否) |

### 模版可选值

**htmlTemplate (PC端)**：
- Mobile, Metro, Classical, Clear, Handy, Active, Lively, Minimalist, Neat, Float

**phoneTemplate (移动端)**：
- Mobile, neat, Classical

**engineType (转换引擎)**：
- `1`: 文字高清
- `2`: 图片高清（默认）
- `3`: 高清-旧版
- `4`: 标清-旧版
- `5`: 全矢量

**convertMode (切割类型)**：
- `0`: 不切割
- `-1`: 自动检查（默认）
- `1`: 强制切割一
- `2`: 强制切割二
- `3`: 强制切割三

### filePath 格式

```json
[
  {"link": "https://example.com/1.pdf"},
  {"link": "https://example.com/2.jpg"}
]
```

本地文件需先上传获取 `fileSrc`，然后传入格式：
```json
[{"link": "https://book.yunzhan365.com/upload-control/files/example.pdf"}]
```

### 返回值

```json
{
  "msg": "操作成功",
  "code": "OK",
  "data": {
    "bookId": 3439934
  }
}
```

| 字段 | 说明 |
|------|------|
| bookId | 电子书编号 |


---

## 获取电子书转换进度

**接口**: `POST https://www.yunzhan365.com/api/book/get-book-progress`  
**Content-Type**: `application/json`

### 请求参数

```json
{
  "cptoken": "*****",
  "bookId": 3439934
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cptoken | string | **必填** | Token |
| bookId | int | **必填** | 电子书编号 |

### 返回值

```json
{
  "msg": "操作成功",
  "code": "OK",
  "convertStatus": 2,
  "convertProgress": 15,
  "errorCode": "2"
}
```

### convertStatus 状态说明

| 值 | 说明 |
|----|------|
| -3 | 正在生成配置文件 |
| -2 | 上传文件失败 |
| -1 | 上传文件中 |
| 0 | 未分配 |
| 1 | 已分配但未确认 |
| 2 | 分配并且确认 |
| 3 | 超时 |
| 4 | 异常 |
| 5 | **转换成功** |
| 6 | 转换失败 |

**注意**：转换进度仅为参考项，最终转换结果以 `convertStatus` 为准。当 `convertStatus` 为 `5` 时表示转换成功。

---

## 获取指定书籍信息

**接口**: `POST https://www.yunzhan365.com/api/book/get-book`  
**Content-Type**: `application/json`

### 请求参数

```json
{
  "cptoken": "*****",
  "bookId": 3439934
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cptoken | string | **必填** | Token |
| bookId | ini | **必填** | 电子书ID |

### 返回值

```json
{
  "msg": "操作成功",
  "code": "OK",
  "data"{
  	"title": "******",
  	"auditStatus":1,
  	"book_url": "https://book.yunzhan365.com/******",
    "domain_url": "******",
    "thumbnailUrl": "https://book.yunzhan365.com/****"
  }
}
```
| 字段 | 说明 |
|------|------|
| title | 书籍标题 |
| auditStatus | 审核状态  0待审核  1审核通过  大于1审核不通过 |
| book_url | 书籍原链接 |
| domain_url | 书籍自定义域名链接 |
| thumbnailUrl | 书籍封面链接 |

---

## 获取用户信息

**接口**: `POST https://www.yunzhan365.com/api/user/get-user`  
**Content-Type**: `application/json`

### 请求参数

```json
{
  "cptoken": "*****"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cptoken | string | **必填** | Token |

### 返回值

```json
{
  "msg": "操作成功",
  "code": "OK",
  "data"{
  	"userId": 1,
    "uName": "******",
    "userImg": "******",
    "uType": 0,
    "add_wechat":1
  }
}
```
| 字段 | 说明 |
|------|------|
| userId | 用户编号 |
| uName | 用户名 |
| userImg | 用户头像 |
| uType | 用户会员等级  0免费 大于0付费 |
| add_wechat | 是否添加客服企业微信   1是 0否 |


---

## 获取客服企业微信二维码

**接口**: `POST https://www.yunzhan365.com/api/scrm/get-qrcode`  
**Content-Type**: `application/json`

### 请求参数

```json
{
  "cptoken": "*****"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cptoken | string | **必填** | Token |

### 返回值

```json
{
  "msg": "操作成功",
  "code": "OK",
  "data"{
    "qr_code": "******",
  }
}
```
| 字段 | 说明 |
|------|------|
| qr_code | 客服企业微信二维码 |

---

## 删除电子书

**接口**: `POST https://www.yunzhan365.com/api/folder/delete-folder-data`  
**Content-Type**: `application/json`

### 请求参数

```json
{
  "cptoken": "*****",
  "folders": "1,2",
  "books": "3439934"
}
```
**注意**：禁止自行删除用户的电子书，需要用户二次确认之后才可以执行删除。


| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cptoken | string | **必填** | Token |
| folders | string | folders 和 books 至少二选一 | 文件夹ID |
| books | string | folders 和 books 至少二选一 | 电子书ID |

### 返回值

```json
{
  "msg": "操作成功",
  "code": "OK"
}
```

---

## 获取电子书列表

**接口**: `POST https://www.yunzhan365.com/api/folder/list-folder-data`  
**Content-Type**: `application/json`

### 请求参数

```json
{
  "cptoken": "*****",
  "operateId": "0",
  "folderId": "0",
  "current": "1",
  "size": "20",
  "keyword": "",
  "orderBy": "newTime",
  "orderSeq": "desc"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cptoken | string | **必填** | Token |
| operateId | string | 选填 | 获取类型：0所有, 1仅文件夹, 2仅电子书 |
| folderId | string | 选填 | 文件夹ID，0表示根目录 |
| current | string | 选填 | 页码，起始页1 |
| size | string | 选填 | 页容量，默认20 |
| keyword | string | 选填 | 搜索关键字 |
| orderBy | string | 选填 | 排序字段：title, newTime, updateTime |
| orderSeq | string | 选填 | 排序规则：asc, desc |

### 返回值

```json
{
  "code": "OK",
  "msg": "操作成功",
  "data": {
    "books": [
      {
        "bookId": 13640914,
        "title": "示例电子书",
        "newTime": 1642488162125,
        "book_url": "https://book.yunzhan365.com/tqql/aaeg/",
        "img": "https://book.yunzhan365.com/tqql/aaeg/files/shot.jpg"
      }
    ],
    "folders": [
      {
        "id": 1,
        "title": "默认文件夹",
        "newTime": "1432190821000"
      }
    ],
    "lastTime": 1642644229759
  }
}
```

| 字段 | 说明 |
|------|------|
| bookId | 书籍编号 |
| title | 书籍标题 |
| newTime | 创建时间 |
| book_url | 书籍原链接 |
| domain_url | 书籍自定义域名链接 |
| img | 书籍封面链接 |

---

## 注册说明

若用户尚未注册云展网账号，引导其访问 [https://www.yunzhan365.com](https://www.yunzhan365.com) 完成注册（支持手机号/邮箱注册）。
