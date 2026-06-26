# 风险白名单

## 概述

定义高风险操作的分类标准和白名单机制。

## 风险等级分类

### P0 - 极高风险（必须二次确认）

**定义：** 不可逆操作，可能造成数据永久丢失或系统级影响

**操作类型：**
- 删除文件（`rm`, `del`, Remove-Item）
- 格式化磁盘或分区
- 修改系统配置（注册表、系统文件）
- 批量发送消息（群发、广播）
- 执行外部脚本（来源不明）

**确认方式：**
```
⚠️ 【二次确认】此操作不可逆
操作：删除 C:\temp\test.txt
影响：文件将被永久删除

请回复 CONFIRM 执行，或 CANCEL 取消。
```

### P1 - 高风险（建议二次确认）

**定义：** 可能影响系统或产生副作用的操作

**操作类型：**
- 安装/卸载软件
- 修改网络配置
- 重启服务
- 占用大量磁盘空间的操作
- 发送消息给陌生人/群组

**确认方式：**
```
⚠️ 确认执行？
操作：清理 30 天前的日志文件（约 2.3GB）
影响：释放磁盘空间，部分日志将无法恢复

回复 CONFIRM 继续，或 CANCEL 取消。
```

### P2 - 中风险（可选确认）

**定义：** 操作有明确范围，但仍需明确

**操作类型：**
- 创建新文件（可能覆盖）
- 修改配置文件
- 发送邮件
- 占用网络带宽的操作

**确认方式：**
```
即将执行：压缩并归档 download 文件夹
大小：约 500MB
目标：发送到邮箱 xxx@qq.com

是否继续？回复 Y 确认，N 取消。
```

### P3 - 低风险（直接执行）

**定义：** 可逆操作或影响极小

**操作类型：**
- 读取信息
- 查询数据
- 生成报告
- 创建临时文件

**处理：** 直接执行，无需确认

## 白名单规则

### 按路径白名单

```json
{
  "whitelist": {
    "paths": [
      "C:\\Users\\Admin\\.openclaw\\workspace\\temp\\*",
      "C:\\Windows\\Temp\\*",
      "/tmp/*",
      "/var/tmp/*"
    ],
    "description": "临时文件夹内的删除操作可放行"
  }
}
```

### 按操作特征白名单

```json
{
  "whitelist": {
    "patterns": [
      {
        "pattern": ".*\\.tmp$",
        "description": "临时文件删除"
      },
      {
        "pattern": ".*\\.log$",
        "description": "日志文件清理（保留最近N个）"
      },
      {
        "pattern": "download_\\d+\\.csv",
        "description": "旧的下载文件"
      }
    ]
  }
}
```

### 按用户白名单

```json
{
  "whitelist": {
    "trustedCommands": [
      {
        "cmd": "openclaw tasks list",
        "description": "查看任务列表"
      },
      {
        "cmd": "openclaw status",
        "description": "查看状态"
      }
    ]
  }
}
```

## 确认超时

- **默认超时：** 60秒
- **超时后：** 自动取消，等待用户重新发起
- **重试限制：** 连续3次取消后，提示用户稍后再试

## 智能判断

### 文件删除判断

```javascript
function assessDeleteRisk(filePath) {
  // 极高风险：系统目录
  if (/^(C:\\Windows|C:\\Program Files)/i.test(filePath)) {
    return "P0";
  }
  
  // 高风险：系统用户目录
  if (/^(C:\\Users\\Admin\\Documents|C:\\Users\\Admin\\Desktop)/i.test(filePath)) {
    return "P1";
  }
  
  // 白名单：临时目录
  if (/^(C:\\Windows\\Temp|C:\\Users\\Admin\\.openclaw\\workspace\\temp)/i.test(filePath)) {
    return "P3";
  }
  
  // 默认：P1
  return "P1";
}
```

### 消息发送判断

```javascript
function assessMessageRisk(recipients, channel) {
  // 高风险：外部渠道、陌生人群
  if (channel === "external" || recipients === "all") {
    return "P0";
  }
  
  // 中风险：私人群组
  if (recipients.includes("group") && recipients.length > 10) {
    return "P1";
  }
  
  // 低风险：私聊
  return "P2";
}
```

## 配置接口

### 添加白名单

```
白名单 + 路径:C:\temp\*
白名单 + 命令:openclaw status
```

### 移除白名单

```
白名单 - 路径:C:\temp\*
```

### 查看白名单

```
白名单 查看
```