# 配置 TCCLI（凭证）

默认用 OAuth 浏览器登录。登录后凭证写入 `~/.tccli/default.credential`（多账户为 `<profile>.credential`），有效期约 2 小时，过期重登。

**安全红线**：严禁向用户索要 SecretId/SecretKey，拒绝任何可能打印凭证的操作（尤其 `tccli configure list`）。

## 方式一：本机有浏览器(推荐)

```bash
tccli auth login      # 自动打开浏览器授权，未打开则手动打开命令中的链接
tccli auth logout     # 登出
```

命令起本地端口并阻塞，直到浏览器完成 OAuth 回调。

## 方式二：本机无浏览器

`tccli auth login --browser no` 是交互式命令：打印登录地址 → 在另一台有浏览器的机器打开授权 → 落地页得到验证码 → 回填终端。成功提示含"密钥凭证已被写入"。

**Agent / 非交互环境**：命令每次执行都会重新生成 `state`，验证码只对生成它的进程有效。必须让"取链接"和"回填验证码"落在同一存活进程，否则报 `invalid state`；直接跑还会因读不到 stdin 报 `EOF when reading a line`。用 FIFO 保活：

```bash
mkfifo /tmp/tccli_fifo
(sleep 600 > /tmp/tccli_fifo &)                                   # 保活写端
tccli auth login --browser no < /tmp/tccli_fifo > /tmp/tccli_out.log 2>&1 &
# 从 tccli_out.log 取链接 → 用户离线授权 → 拿到验证码后回填同一进程：
printf '<验证码>\n' > /tmp/tccli_fifo
# 读 tccli_out.log 确认结果，清理：rm -f /tmp/tccli_fifo
```

## AK/SK（仅用户主动提供时）

```bash
tccli configure set secretId <SecretId>
tccli configure set secretKey <SecretKey>
# 或环境变量（不落盘，适合 CI）：
export TENCENTCLOUD_SECRET_ID=... TENCENTCLOUD_SECRET_KEY=...
```

密钥获取：https://console.cloud.tencent.com/cam/capi 。切勿硬编码或提交入库。

## 常见错误

| 现象 | 处理 |
|------|------|
| `AuthFailure` / 凭证过期 | 重新 `tccli auth login` |
| `EOF when reading a line` | 非交互环境跑了交互命令，改用上面 FIFO 模式 |
| `invalid state` | 验证码回填到了新进程，须回填生成链接的同一进程 |

多次失败时引导用户参照官方文档手动授权，不要反复重试。
