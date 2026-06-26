---
name: qinglite-platform
version: 1.1.0
description: 模拟登录轻识 (qinglite.cn) 并获取 token，或使用 token 发布作品。
parameters:
  - name: action
    type: string
    description: 执行的操作，可选值为 "login" 或 "publish"
  - name: mobile
    type: string
    description: (仅当 action 为 "login" 时需要) 手机号码
  - name: code
    type: string
    description: (仅当 action 为 "login" 时需要) 验证码
  - name: token
    type: string
    description: (仅当 action 为 "publish" 时需要) 登录后获取的 token
  - name: title
    type: string
    description: (仅当 action 为 "publish" 时需要) 作品标题
  - name: content
    type: string
    description: (仅当 action 为 "publish" 时需要) 作品内容
  - name: type
    type: integer
    description: (仅当 action 为 "publish" 时需要) 作品类型 (1文章, 2文字, 3图片, 4视频)
  - name: media
    type: string
    description: (仅当 action 为 "publish" 时需要) 文件路径，多个英文逗号隔开
---

# 轻识平台操作技能

## 描述
本技能整合了轻识平台的模拟登录和作品发布功能。用户可以选择执行登录操作以获取 token，或使用已有的 token 发布作品。

## 操作步骤
### 登录操作 (action: "login")
1. 接收用户提供的手机号 (`mobile`) 和验证码 (`code`)。
2. 构建请求体，包含 `mobile`, `code`, `prefix` (固定为 "+86"), `act` (固定为 1), `app_type` (固定为 "openclaw"), 和 `post_type` (固定为 "ajax")。
3. 向登录接口 `https://www.qinglite.cn/api/interface/user/user_mobile/login` 发送 POST 请求。
4. 解析返回的 JSON 数据，提取 `token`。
5. 将 `token` 返回给用户。

### 发布作品操作 (action: "publish")
1. 接收用户提供的 `token`, `title`, `content`, `type`, `media`。
2. 构建请求体，包含 `title`, `content`, `type`, `media`, `token`, `app_type` (固定为 "openclaw")。
3. 向发布接口 `https://www.qinglite.cn/api/interface/content/news/create` 发送 POST 请求。
4. 解析返回的 JSON 数据，确认发布结果。
5. 将发布结果返回给用户。

## 接口信息
### 登录接口
- **URL**: `https://www.qinglite.cn/api/interface/user/user_mobile/login`
- **Method**: `POST`
- **Request Body (JSON)**:
  ```json
  {
    "mobile": "用户手机号",
    "code": "用户验证码",
    "prefix": "+86",
    "act": 1,
    "app_type": "openclaw",
    "post_type": "ajax"
  }
  ```
- **Response (JSON)**:
  ```json
  {
    "code": 20000,
    "msg": "success",
    "data": {
      "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
  ```
  (成功时返回示例，`code` 为 20000，`data` 中包含 `token`)

### 发布作品接口
- **URL**: `https://www.qinglite.cn/api/interface/content/news/create`
- **Method**: `POST`
- **Request Body (JSON)**:
  ```json
  {
    "title": "作品标题",
    "content": "作品内容",
    "type": 1, // 1文章, 2文字, 3图片, 4视频
    "media": "文件路径，多个英文逗号隔开",
    "token": "登录返回的token值",
    "app_type": "openclaw"
  }
  ```
- **Response (JSON)**:
  ```json
  {
    "code": 20000,
    "msg": "success"
  }
  ```
  (成功时返回示例，`code` 为 20000)
