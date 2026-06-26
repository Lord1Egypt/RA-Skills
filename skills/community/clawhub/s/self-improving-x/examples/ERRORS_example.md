
# 错误日志

## [ERR-20250115-A3F] docker_build

**记录时间**: 2025-01-15T09:15:00Z
**优先级**: high
**状态**: pending
**领域**: infra

### 摘要
Docker build 在 M1 Mac 上因平台不匹配而失败

### 错误

error: failed to solve: python:3.11-slim: no match for platform linux/arm64

### 上下文
- 命令: `docker build -t myapp .`
- Dockerfile 使用 `FROM python:3.11-slim`
- 在 Apple Silicon（M1/M2）上运行

### 建议修复
添加平台标志: `docker build --platform linux/amd64 -t myapp .`
或更新 Dockerfile: `FROM --platform=linux/amd64 python:3.11-slim`

### 元数据
- 可复现: yes
- 相关文件: Dockerfile

---

## [ERR-20250120-B2C] api_timeout

**记录时间**: 2025-01-20T11:30:00Z
**优先级**: critical
**状态**: pending
**领域**: backend


### 摘要
结账时第三方支付 API 超时

### 错误

TimeoutError: Request to payments.example.com timed out after 30000ms

### 上下文
- 命令: POST /api/checkout
- 超时设置为 30 秒
- 在高峰时间发生（午餐、傍晚）

### 建议修复
实现指数退避重试。考虑断路器模式。

### 元数据
- 可复现: yes（在高峰时间）
- 相关文件: src/services/payment.ts
- 另请参阅: ERR-20250115-X1Y, ERR-20250118-Z3W

---
