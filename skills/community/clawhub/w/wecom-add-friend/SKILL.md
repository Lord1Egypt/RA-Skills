---
name: wecom-add-friend
description: 企业微信自动添加好友技能，支持批量手机号添加
metadata:
  {
    "openclaw": {
      "emoji": "💬",
      "requires": {
        "bins": ["python"],
        "files": ["bin/wecom_auto_add.py"]
      },
      "os": ["win32"]
    }
  }

user-invocable: true
---

# 企业微信自动添加好友技能

## 功能说明
本技能用于在**企业微信 PC 客户端**中批量添加好友。支持：
- 同时添加多个手机号（逗号或空格分隔）
- 自动识别"用户不存在"并跳过
- 可调节添加间隔避免风控

## 使用方式

### 用户指令示例
用户可以说：
- `添加好友 13800138001,13800138002`
- `帮我加几个企业微信好友 13800138001 13800138002`
- `批量加人 13800138001,13800138002 间隔60秒`

### 参数解析规则
- `phones`：必填，手机号列表，支持：
  - 逗号分隔：`13800138001,13800138002`
  - 空格分隔：`13800138001 13800138002`
- `interval`：可选，添加间隔（秒），默认 30 秒

## 执行流程

### 第一步：解析用户输入
从用户消息中提取手机号列表和间隔参数。

### 第二步：执行添加命令
```bash
cd {baseDir}/bin && python wecom_auto_add.py --add --phones "手机号列表" --interval 30
```

## 首次使用设置

如果用户首次使用，需要先设置坐标：
1. 确保企业微信已登录且窗口可见
2. 执行：`cd {baseDir}/bin && python wecom_auto_add.py --setup`
3. 按提示将鼠标依次移动到各个按钮位置

## 注意事项
⚠️ 添加间隔建议≥30秒，避免被平台风控
⚠️ 执行过程中不要遮挡企业微信窗口
⚠️ 紧急停止：鼠标快速移动到屏幕左上角

## License & Credits

**License:** MIT — use freely, modify, distribute. No warranty.