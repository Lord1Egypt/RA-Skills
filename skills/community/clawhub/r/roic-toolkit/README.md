# QQ 机器人快速开始

基于 NapCat + NoneBot2 的 QQ 机器人

## 前置要求

1. 安装 Python 3.8 或更高版本
2. 安装并配置 NapCat（QQ 机器人后端）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 NapCat

#### 方案 A：使用 NapCat（推荐）

1. 下载 NapCat：https://github.com/NapNeko/NapCatQQ/releases
2. 解压并运行 NapCat
3. 登录你的 QQ 账号
4. 在配置文件中设置 WebSocket 端口（默认 3001）

配置示例（config.json）：
```json
{
  "ws": {
    "enable": true,
    "port": 3001
  },
  "http": {
    "enable": true,
    "port": 3000
  }
}
```

#### 方案 B：使用 LLOneBot

1. 在 QQ 客户端中安装 LLOneBot 插件
2. 配置 WebSocket 连接

### 3. 修改机器人配置

编辑 `config.py` 文件，修改以下配置：

```python
# 命令前缀
COMMAND_START = ["/", ""]

# 超级管理员QQ号（重要！）
SUPERUSERS = [你的QQ号]

# NapCat WebSocket 地址（根据你的实际配置）
ONEBOT_WS_URLS = ["ws://127.0.0.1:3001"]
```

### 4. 启动机器人

```bash
python bot.py
```

## 可用命令

- `/ping` - 测试机器人是否在线
- `/hello` - 打招呼
- `/群信息` - 查看当前群信息
- `/测试` - 发送测试消息

## 添加新功能

在 `plugins` 目录下创建新的 `.py` 文件，编写你的插件逻辑。

参考 `plugins/basic.py` 了解如何编写命令处理器。

## 常见问题

### Q: 机器人无法连接？
A: 检查以下几点：
1. NapCat 是否已启动并登录
2. WebSocket 端口是否正确
3. 防火墙是否阻止了连接

### Q: 如何获取 QQ 号？
A: 在任意聊天窗口中，右键点击自己的头像，选择"查看资料"即可看到 QQ 号。

## 更多资源

- NoneBot2 文档：https://nonebot.dev/
- OneBot 11 协议：https://11.onebot.dev/
- NapCat 文档：https://napneko.com/

## 许可证

MIT License
