# 技能更新检查系统

## 概述
本技能内置了更新检查系统，可以自动检查新版本并通知用户。

## 文件结构
```
today-task/
├── version.json          # 版本信息
├── update_config.json    # 更新配置
├── scripts/
│   ├── update_checker.py    # 更新检查核心
│   └── version_manager.py   # 版本管理工具
└── UPDATE_SYSTEM.md      # 本文件
```

## 使用方法

### 1. 手动检查更新
```bash
python scripts/update_checker.py check
```

### 2. 查看版本信息
```bash
python scripts/version_manager.py show
```

### 3. 更新版本号（开发者用）
```bash
python scripts/version_manager.py update 1.1.0 -c "新增功能" "修复问题"
```

### 4. 配置更新检查
编辑 `update_config.json`：
```json
{
  "enabled": true,           // 是否启用更新检查
  "check_on_startup": true,  // 启动时检查
  "check_interval_hours": 24, // 检查间隔（小时）
  "show_notification": true   // 显示通知
}
```

## 更新通知示例
```
============================================================
[通知] 技能更新通知
============================================================
技能: 负一屏任务推送
当前版本: 1.0.0
最新版本: 1.1.0
更新命令: clawhub update today-task
============================================================
更新内容:
  - 新增技能更新检查功能
  - 优化错误处理机制
  - 改进用户通知体验
============================================================
```

## 工作原理

### 1. 自动检查
- 技能启动时自动检查更新（如果启用）
- 每24小时检查一次（可配置）
- 仅从ClawHub检查更新

### 2. 版本管理
- 版本信息存储在 `version.json`
- 支持更新日志记录
- 提供版本管理工具

### 3. 通知显示
- 清晰的文本通知
- 显示更新内容和命令
- 可配置是否显示

## 开发者指南

### 1. 发布新版本
1. 更新版本号：
   ```bash
   python scripts/version_manager.py update 1.1.0 -c "新增功能" "修复问题"
   ```

2. 更新ClawHub上的技能信息

3. 发布到ClawHub：
   ```bash
   clawhub publish
   ```

### 2. 集成说明
更新检查已集成到 `task_push.py` 主脚本中，每次运行都会检查更新（如果配置允许）。

### 3. 关于ClawHub API
当前使用模拟数据测试更新检查功能。实际使用时需要：
1. 了解ClawHub的实际API
2. 修改 `update_checker.py` 中的 `_check_clawhub()` 方法
3. 使用真实的ClawHub API获取版本信息

## 注意事项
1. 更新检查需要网络连接
2. 当前使用模拟数据，需要根据ClawHub实际情况调整
3. 建议保持更新检查启用以获得最新功能
4. 更新通知不会影响主功能执行