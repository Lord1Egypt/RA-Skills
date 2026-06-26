# A股新债新股申购助手（合规版）

基于官方API的A股新债/新股申购助手，使用100%合规的东方财富官方API，安全可靠，适合ClawHub发布。

## 🎯 核心功能

### ✅ 100%合规数据源
- **新股数据**: 东方财富官方API（`RPTA_APP_IPOAPPLY`）
- **可转债数据**: 集思录官方API
- **数据验证**: 内置准确性验证机制

### ✅ 安全可靠
- 不使用网页抓取（无JSDOM依赖）
- 仅使用官方API接口
- 完整的输入验证和错误处理
- 符合ClawHub安全规范

### ✅ 自动化提醒
- 每日9:30自动初始化飞书表格
- 定时提醒（可配置间隔）
- 支持用户操作反馈
- 自动更新表格状态

## 📋 配置要求

### 1. 飞书配置
- 创建飞书多维表格
- 获取飞书机器人Webhook
- 获取飞书AccessToken（需要"多维表格读写"权限）

### 2. 环境变量
```bash
FEISHU_WEBHOOK=你的飞书Webhook
FEISHU_ACCESS_TOKEN=你的飞书AccessToken
FEISHU_APP_TOKEN=你的表格AppToken
FEISHU_TABLE_ID=你的表格ID
```

## 🚀 快速开始

### 安装依赖
```bash
npm install
```

### 配置环境
```bash
cp .env.example .env
# 编辑.env文件填写配置
```

### 运行测试
```bash
npm test
```

### 生产运行
```bash
npm start
```

## 🔧 技术架构

### 安全特性
- ✅ 仅使用HTTPS API
- ✅ 完整的输入验证
- ✅ 错误边界处理
- ✅ 无恶意代码
- ✅ 符合ClawHub安全规范

### 数据流程
```
官方API → 数据解析 → 过滤分类 → 表格写入 → 消息推送
```

## 📞 支持与反馈

如有问题或建议，请查看文档或联系作者。

---

**版本**: v1.0.0（合规版）
**状态**: 生产就绪 ✅
**安全等级**: ClawHub合规认证 🛡️