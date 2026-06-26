# 腾讯文档鉴权检查

腾讯文档授权流程，**必须按以下步骤执行**：

> 💡 **说明**：授权成功后，Token 会同时配置到 `tencent-docs` 、 `tencent-docengine`、`tencent-sheetengine` 三个服务，无需为 tencent-docengine和tencent-sheetengine 单独授权。

## 第一步：检查状态（立即返回）

```bash
bash ./setup.sh tdoc_check_and_start_auth
```

| 输出                  | 处理方式                                                     |
| --------------------- | ------------------------------------------------------------ |
| `READY`               | ✅ 直接执行用户任务，**无需第二步**                           |
| `AUTH_REQUIRED:<url>` | **立即**向用户展示授权链接（见下方模板），**然后执行第二步** |
| `ERROR:*`             | 告知用户对应错误                                             |

## 第二步：等待授权完成（仅 AUTH_REQUIRED 时执行）

**展示授权链接后**，立即执行：

```bash
bash ./setup.sh tdoc_wait_auth
```

| 输出                  | 处理方式                                     |
| --------------------- | -------------------------------------------- |
| `TOKEN_READY:*`       | ✅ 授权成功，继续执行用户任务                 |
| `AUTH_TIMEOUT`        | 告知用户：「授权超时，请重新发起请求。」     |
| `ERROR:expired`       | 告知用户：「授权码已过期，请重新发起请求。」 |
| `ERROR:token_invalid` | 告知用户：「Token 已失效，请重新发起请求。」 |
| `ERROR:*`             | 告知用户对应错误，请重新发起请求             |

## 第三步：人工兜底（前两步都失败的情况）

🔑 **检查 Token 配置**：可访问 [https://docs.qq.com/scenario/open-claw.html](https://docs.qq.com/scenario/open-claw.html) 获取 Token，再执行以下命令来设置mcporter:
```bash
# 使用传入的 Token 写入 mcporter 配置（tencent-docs）
mcporter config add tencent-docs "https://docs.qq.com/openapi/mcp" \
    --header "Authorization=$Token" \
    --transport http \
    --scope home

# 同时配置 tencent-docengine（复用相同 Token）
mcporter config add tencent-docengine "https://docs.qq.com/api/v6/doc/mcp" \
    --header "Authorization=$Token" \
    --transport http \
    --scope home

# 同时配置 tencent-sheetengine（复用相同 Token）
mcporter config add tencent-sheetengine "https://docs.qq.com/api/v6/sheet/mcp" \
    --header "Authorization=$Token" \
    --transport http \
    --scope home
```

## 授权链接展示模板

当第一步输出 `AUTH_REQUIRED:<url>` 时，**立即**向用户展示：

> 🔑 **需要先完成腾讯文档授权**
>
> 请确保在**浏览器**中打开以下链接完成授权：**[点击授权腾讯文档]({url})**
>
> ⚠️ 请使用 **QQ 或微信** 扫码 / 登录授权
>
> _(授权后将自动继续，无需回复)_

## 错误说明

| 错误                       | 含义                               |
| -------------------------- | ---------------------------------- |
| `ERROR:mcporter_not_found` | 缺少依赖，请先安装 Node.js         |
| `ERROR:expired`            | 授权码已过期，重新发起请求         |
| `ERROR:token_invalid`      | Token 鉴权失败（400006），重新授权 |
| `ERROR:save_token_failed`  | Token 写入配置失败                 |
| `AUTH_TIMEOUT`             | 用户未在时限内完成授权             |
