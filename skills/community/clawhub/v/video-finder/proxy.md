---
name: video_finder_proxy
description: "管理代理配置与网络可达性探测。直连探测、代理重试、代理配置持久化。触发：代理、proxy、换代理、网络不通、连不上"
---

# proxy — 代理配置与探测

管理代理配置（`proxy.json`）并在每次访问站点前探测网络可达性。

## 前置条件

- **称呼约定**：`{{{user}}}` 为占位符
- **配置文件**：`./proxy.json`（skill 根目录）
- **安全约束**：`proxy.json` 含密码，**不在对话/日志/代码示例中输出**

## 初始化

**触发时机**：第一次遇到目标站点直连不通时

1. 从模板创建：`cp proxy.example.json proxy.json`
2. 询问用户：

```
{{{user}}}，<站点名>直连连不上呢～你有代理可以用吗？
```

**情况 A**：用户提供代理信息（host / port / auth）
→ 写入 `proxy.json`：

```json
{
  "host": "<代理IP>",
  "port": <端口>,
  "auth": { "username": "<用户名>", "password": "<密码>" },
  "proxy_required_sites": ["<站点1>", "<站点2>"]
}
```

**情况 B**：用户暂不配代理
→ 写空值 `{}`，后续遇不通仍会再问

**情况 C**：用户本次能用但不想存
→ 本次加 `--proxy` 但不写文件，仅会话有效

## 每次访问站点前探测

```
1. 读取 proxy.json
   ├─ 有配置 → 构建代理 URL
   │   http://{username}:***}@{host}:{port}
   │
   └─ 无配置 / 空值 → 直连探测
       curl --connect-timeout 5 "<target>"
       ├─ 200/30x → 直连可用 ✅
       └─ 超时/拒绝 → 触发初始化流程
```

### 有代理时重试

```bash
curl -x "http://<用户名>:<密码>@<代理IP>:<端口>" \
     -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "<target>"
```

## 代理判断（下载时）

- 站点在 `proxy_required_sites` 中 → 用代理
- 直连测试可达 → 不用代理
- 直连不通且 `proxy.json` 为空 → 触发初始化

## 用户干预

```
"换个代理"       → 重新初始化，覆盖 proxy.json
"这次不用代理"   → 不加 --proxy，不写文件
"记得这个代理"   → 写入 proxy.json 持久化
```
