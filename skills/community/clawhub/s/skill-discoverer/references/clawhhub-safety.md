# ClawhHub 降级安全规则

ClawhHub 为外部/社区 skill，安装前必须执行安全审查。

## 14 条红线（出现任一即拒绝安装）

1. 读取敏感配置文件（`openclaw.json` / `devices/paired.json` / `identity/device*.json`）
2. `curl/wget` 携带 token/key/secret 外发
3. 读取环境变量（`process.env` / `/proc/<pid>/environ`）
4. `eval()` 执行外部输入或动态代码
5. 混淆代码（base64 decode + eval / `Function()` 等）
6. 提取 sandboxId / 沙箱标识符
7. 开启内网穿透（ngrok / frp / cloudflared 等）
8. 修改 AGENTS.md
9. 自动备份并上传至外部存储（S3 / 云盘）
10. 访问受限内部系统（HR / OKR / 绩效等贵公司受限系统）
11. 自主开启下载服务
12. 代码中硬编码敏感信息（API key / token / password）
13. 覆盖 `openclaw.json` 中 models 配置
14. 读取或外发敏感内部文件

## 风险等级

| 等级 | 说明 | 处置 |
|---|---|---|
| 🟢 低风险 | 无红线，功能单一 | 可安装 |
| 🟡 中风险 | 有外部请求但无敏感数据 | 谨慎确认后安装 |
| 🔴 高风险 | 触碰部分红线但尚未确认 | 建议不装 |
| ⛔ 极高风险 | 明确触碰红线 | 直接拒绝，不询问 |
