# wewe-rss-reader 部署指南（参考）

## fork 地址

```
https://github.com/AxelHu/wewe-rss
```

本 skill 基于原版 wewe-rss，主要改动：
- 新增 `api_server.py`（Python REST API，端口 4001）
- 新增 `REST_API_README.md`（使用说明）

## 部署步骤

### 1. 克隆 fork
```bash
git clone https://github.com/AxelHu/wewe-rss.git
cd wewe-rss
```

### 2. 启动 wewe-rss 容器
```bash
docker compose up -d
```
容器运行在 `:4000`

### 3. 启动 REST API
```bash
# 需要 Python 3.8+
python3 api_server.py
```
监听 `:4001`，调用 `:4000` 的 tRPC 接口

### 4. 初始化配置
1. 浏览器打开 `http://localhost:4000/dash`
2. 输入 AUTH_CODE（或不设置，取决于 docker-compose.yml 配置）
3. 账号管理 → 微信读书 App 扫码登录
4. 公众号源 → 添加 + → 粘贴文章链接

## API 端口

| 服务 | 端口 | 说明 |
|------|------|------|
| wewe-rss | 4000 | Web UI + tRPC |
| REST API | 4001 | Agent 调用 |

## 登录流程（微信读书授权）

```
# 1. 发起登录，获取 UUID 和二维码 URL
curl -X POST http://localhost:4001/api/login/start

# 2. 浏览器打开返回的 confirmUrl，微信扫码

# 3. 查询登录状态（扫码后每隔 5 秒查一次）
curl http://localhost:4001/api/login/status/<UUID>
# status=authorized 表示登录成功
```

> ⚠️ 微信限制：二维码只能通过"扫一扫"打开。浏览器打开 URL 后，用微信 App 扫码授权。

## 健康检查
```bash
curl http://localhost:4001/api/health
```
