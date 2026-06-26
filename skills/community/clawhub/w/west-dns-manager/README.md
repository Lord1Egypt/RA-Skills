# 西部数码域名解析管理 Skill (west-dns-manager)
OpenClaw 平台专用 Skill，基于西部数码API实现域名解析的添加、修改、删除操作。

## 功能特性
- 支持添加域名解析记录（A/CNAME/MX/TXT/AAAA类型）
- 支持修改域名解析记录（优先通过record_id精准修改）
- 支持删除域名解析记录（支持ID删除/host+type删除）
- 完整的参数校验和异常处理
- 标准化的输入输出格式，兼容OpenClaw平台

## 前置条件
1. 西部数码账号及API密码（非登录密码）
   - 获取路径：西部数码官网 → 管理中心 → 代理商管理 → API接口配置
2. Python 3.6+ 环境
3. 安装依赖包（见requirements.txt）

## 依赖安装
```bash
pip install -r requirements.txt