# yixiaoer-rotator-skill

蚁小二账号轮询管理器，用于多账号矩阵的自动轮询发布。

## 功能特性

- ✅ 自动同步蚁小二账号列表
- ✅ 按平台独立维护轮询索引（哔哩哔哩、头条号、百家号等）
- ✅ 状态持久化，重启不丢失
- ✅ 命令行工具，可集成到发布流程
- ✅ 智能账号管理：新增账号自动追加，删除账号自动调整

## 快速开始

### 安装

```bash
clawhub install yixiaoer-rotator-skill
```

### 配置

```bash
export YIXIAOER_API_KEY="你的蚁小二 API Key"
export YIXIAOER_MEMBER_ID="你的成员 ID"
```

### 使用

```bash
# 同步账号
node scripts/account-rotator.js sync

# 获取下一个账号
node scripts/account-rotator.js next 哔哩哔哩
```

## 依赖

- [yixiaoer-skill](https://clawhub.ai/yixiaoer-skill) - 蚁小二 API 封装

## 许可证

MIT License
