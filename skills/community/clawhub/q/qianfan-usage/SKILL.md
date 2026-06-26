# qianfan-usage

查询百度千帆 Coding Plan 用量和额度。

## 使用方法

```
/qianfan-usage          # 自动登录并查询用量详情
/qianfan-usage --web    # 打开百度千帆控制台
```

## 用量详情

查询 Coding Plan 的三级用量：

| 周期 | 说明 | 重置时间 |
|------|------|----------|
| 5小时 | 短期用量 | 每5小时重置 |
| 周 | 周用量 | 每周一重置 |
| 月 | 月用量 | 套餐到期时重置 |

## 自动登录

脚本使用 `agent-browser` 自动登录百度账号：
- 手机号：从环境变量 `QIANFAN_PHONE` 读取
- 验证码：需要手动输入（或等待短信）

## 配置

在 `~/.openclaw/workspace/.env` 中设置手机号：

```
QIANFAN_PHONE=你的手机号
```

## API 端点

```
GET https://console.bce.baidu.com/api/qianfan/charge/codingPlan/quota
```

返回格式：
```json
{
  "success": true,
  "result": {
    "quota": {
      "fiveHour": { "used": 338, "limit": 1200, "resetAt": "..." },
      "week": { "used": 499, "limit": 9000, "resetAt": "..." },
      "month": { "used": 499, "limit": 18000, "resetAt": "..." }
    }
  }
}
```

## 依赖

- agent-browser（自动安装）
- Python 3
