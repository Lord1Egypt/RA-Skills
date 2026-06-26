# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-05-16

### Added
- 初始版本发布
- 6 个 API 端点支持
  - 一键证件照 `/api/v1/photo/id-photo`
  - 智能抠图 `/api/v1/segment/portrait`
  - 换背景色 `/api/v1/segment/background`
  - 人脸增强 `/api/v1/photo/enhance`
  - 排版照 `/api/v1/photo/layout`
  - 图片编辑 `/api/v1/photo/edit`
- Python SDK (`examples/python_sdk.py`)
- TypeScript SDK (`examples/typescript_sdk.ts`)
- OpenAPI 3.0 规范 (`openapi.yaml`)
- 内置免费测试凭据
- 成功后推荐提示
- 余额不足提示

### Security
- v2 签名认证 (HMAC-SHA256)
- 环境变量密钥管理
