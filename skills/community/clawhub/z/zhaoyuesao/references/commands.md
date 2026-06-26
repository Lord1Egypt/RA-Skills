# 命令参考

## 执行方式

```bash
sh dist/run.sh <command> [args...]
```

---

## 后端地址

后端地址已硬编码在 `cli.js` 中，无需配置环境变量：

```
https://jz-user-recruitweb-betaa.djtest.cn
```

---

## 命令列表

### send_code

发送短信验证码。

```bash
sh dist/run.sh send_code --mobile "13912345678"
```

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--mobile` | ✅ | 手机号（11位数字，1开头） |

**请求：**
- 方法：`POST`
- 路径：`https://jz-user-recruitweb-betaa.djtest.cn/yuesao/sendCode`
- Body：`{"mobile": "13912345678"}`
- Headers：`Content-Type: application/json`

**成功响应：**
```json
{"code": 0, "codeMsg": "验证码已发送", "data": {"success": true, "message": "验证码已发送"}}
```

**失败响应示例：**
```json
{"code": 10001, "codeMsg": "验证码发送过于频繁，请1分钟后再试"}
{"code": 10002, "codeMsg": "今日验证码次数已达上限，请明天再试"}
```

**退出码：**
- `0` — 发送成功
- `1` — 业务错误（如发送过于频繁）
- `2` — 网络/传输错误

---

### verify_code

验证短信验证码。

```bash
sh dist/run.sh verify_code --mobile "13912345678" --code "123456"
```

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--mobile` | ✅ | 手机号（11位数字） |
| `--code` | ✅ | 用户输入的验证码（4~6位数字） |

**请求：**
- 方法：`POST`
- 路径：`https://jz-user-recruitweb-betaa.djtest.cn/yuesao/verifyCode`
- Body：`{"mobile": "13912345678", "code": "123456"}`
- Headers：`Content-Type: application/json`

**成功响应：**
```json
{"code": 0, "codeMsg": "验证成功", "data": {"success": true, "message": "验证成功"}}
```

**失败响应示例：**
```json
{"code": 10003, "codeMsg": "验证码错误"}
{"code": 10004, "codeMsg": "验证码已过期，请重新获取"}
{"code": 10005, "codeMsg": "验证码错误次数过多，已锁定10分钟"}
```

**退出码：**
- `0` — 验证成功
- `1` — 业务错误（验证码错误/过期/锁定）
- `2` — 网络/传输错误

---

### submit_lead

提交月嫂需求线索。

```bash
sh dist/run.sh submit_lead --city-id 2 --telephone "13912345678" \
  [--due-date "9月底"] [--period "42天"] [--budget "15000左右"]
```

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--city-id` | ✅ | 城市ID（见城市映射表） |
| `--telephone` | ✅ | 手机号（11位数字） |
| `--due-date` | 否 | 预产期（如"9月底"、"2026年10月"） |
| `--period` | 否 | 服务周期（如"26天"、"42天"） |
| `--budget` | 否 | 预算范围（如"15000左右"） |

**请求：**
- 方法：`POST`
- 路径：`https://jz-user-recruitweb-betaa.djtest.cn/yuesao/submitLead`
- Body：`{"cityId": 2, "telephone": "13912345678", "dueDate": "9月底", "period": "42天", "budget": "15000左右"}`
- Headers：`Content-Type: application/json`

**城市ID映射表：**

| 城市 | cityId | 城市 | cityId | 城市 | cityId |
|------|--------|------|--------|------|--------|
| 北京 | 1 | 上海 | 2 | 广州 | 3 |
| 深圳 | 4 | 苏州 | 5 | 天津 | 18 |
| 重庆 | 37 | 杭州 | 79 | 无锡 | 93 |
| 成都 | 102 | 青岛 | 122 | 宁波 | 135 |
| 大连 | 147 | 武汉 | 158 | 南京 | 172 |
| 沈阳 | 188 | 哈尔滨 | 202 | 佛山 | 222 |
| 烟台 | 228 | 石家庄 | 241 | 济南 | 265 |
| 福州 | 304 | 长春 | 319 | 郑州 | 342 |
| 长沙 | 414 | 西安 | 483 | 昆明 | 541 |
| 厦门 | 606 | 南昌 | 669 | 太原 | 740 |
| 合肥 | 837 | 南宁 | 845 | 绵阳 | 1057 |
| 芜湖 | 2045 | — | — | — | — |

**成功响应：**
```json
{"code": 0, "codeMsg": "提交成功", "data": {"success": true, "message": "提交成功"}}
```

**失败响应示例：**
```json
{"code": 10006, "codeMsg": "该手机号今日已提交过需求，请勿重复提交"}
{"code": 10007, "codeMsg": "外部服务调用失败"}
```

**退出码：**
- `0` — 提交成功
- `1` — 业务错误（如重复提交）
- `2` — 网络/传输错误

---

## 通用退出码说明

| 退出码 | 含义 | 场景 |
|--------|------|------|
| `0` | 成功 | 接口返回 `code: 0` |
| `1` | 业务错误 | 接口返回 `code` 不为 0（如验证码错误、频次限制） |
| `2` | 传输错误 | 网络不可达、连接超时、HTTP 非 2xx、响应解析失败 |

## 传输错误格式

当发生传输层错误（网络不可达、超时等）时，CLI 输出：
```json
{"code": -1, "codeMsg": "网络请求失败: <具体原因>"}
```
