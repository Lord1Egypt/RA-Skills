# Qmsg 酱推送

通过 Qmsg 酱（qmsg.zendee.cn）向 QQ 主动发送推送通知，无需 API Key。

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | Skill 核心定义，触发词和调用方式 |
| `qmsg_push.py` | 推送脚本，调用 Qmsg API 发送消息 |

## 快速配置

### 第一步：获取 Qmsg KEY

1. 访问 [qmsg.zendee.cn](https://qmsg.zendee.cn)，登录账号
2. 选择**公开机器人**，添加一个机器人 QQ 号（需为机器人 QQ）
3. 在 Qmsg 后台添加**需要接收消息的 QQ 号**（即你自己的 QQ）
4. 复制生成的 KEY

### 第二步：配置密钥文件

创建 `~/.workbuddy/secrets.json`：

```json
{
  "qmsg": {
    "key": "你的QmsgKEY"
  }
}
```

### 第三步：安装 Skill

将 `qmsg-push-release` 文件夹重命名为 `qmsg-push`，放入 `~/.workbuddy/skills/` 目录。

## 调用方式

```bash
python ~/.workbuddy/qmsg_push.py "消息内容"
```

## 适用场景

- 自动化任务执行完成后的状态通知
- 定时提醒推送到手机 QQ
- 无需开启微信即可接收系统通知
