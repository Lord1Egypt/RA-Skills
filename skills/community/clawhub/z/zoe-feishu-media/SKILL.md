---
name: feishu-media
description: 飞书媒体文件发送skill,支持发送图片到飞书群或个人.用于发送截图、设计图等场景.
version: 1.0.0
author: Zoe
license: MIT

# 飞书媒体发送 Skill

## 简介
本skill提供将本地图片发送到飞书群或个人聊天的功能。

## 什么时候用
- 用户说"发图片"、"发送图片"、"发到飞书"
- 用户需要把本地图片发送到飞书群

## 安装依赖
```bash
pip install requests
```

## 安全配置 ⚠️ 重要
**必须配置飞书凭证，建议使用环境变量，切勿硬编码！**

### 方式一：环境变量（推荐）
```bash
# Windows
set FEISHU_APP_ID=你的AppID
set FEISHU_APP_SECRET=你的AppSecret

# Linux/Mac
export FEISHU_APP_ID=你的AppID
export FEISHU_APP_SECRET=你的AppSecret
```

### 方式二：命令行参数
```python
send_image(
    image_path="C:/path/to/image.png",
    chat_id="oc_xxx",
    app_id="cli_xxx",      # 你的App ID
    app_secret="xxx"       # 你的App Secret
)
```

## 使用方法

### 发送图片
```python
from feishu_image import send_image

# 方式一：环境变量配置后
send_image(
    image_path="C:/path/to/image.png",
    chat_id="oc_xxx"  # 群聊ID
)

# 方式二：命令行传入
# python feishu_image.py <图片路径> <chat_id> <app_id> <app_secret>
```

### 参数说明
| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| image_path | 图片本地路径 | 是 | C:/Users/admin/Desktop/xxx.png |
| chat_id | 接收者ID | 是 | oc_xxx (群) 或 ou_xxx (个人) |
| app_id | 飞书应用ID | 否 | cli_xxx（环境变量优先） |
| app_secret | 飞书应用密钥 | 否 | xxx（环境变量优先） |

## 获取飞书凭证

### 1. 创建飞书应用
1. 登录 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 App ID 和 App Secret

### 2. 添加权限
在应用详情中添加以下权限：
- `im:resource` - 上传图片和文件
- `im:message:send` - 发送消息
- `im:chat:send` - 发送群消息

### 3. 获取chat_id
- 群聊：在群设置中查看群ID
- 个人：获取用户的 open_id

## 示例

### 发送UI设计图
```python
send_image(
    image_path="C:/Users/admin/Desktop/battery-ui.png",
    chat_id="oc_205333d14cf0881ef8b79fa223ff902b"
)
```

### 发送文件（扩展）
```python
# 发送文件类似，只需改用 file 相关API
```

## 注意事项 ⚠️
1. **安全**：不要将包含真实凭证的代码提交到公开仓库！
2. **权限**：飞书应用需要开启相应权限才能使用
3. **图片格式**：支持 JPEG, PNG, WEBP, GIF, BMP 等
4. **文件大小**：最大 30MB
5. **频率限制**：注意飞书API的调用频率限制

## 故障排除

### 错误码 230001
- 原因：无效的请求内容
- 解决：检查image_key是否正确

### 错误码 99991663
- 原因：应用没有权限
- 解决：在飞书开放平台给应用添加对应权限

### 错误码 230013
- 原因：机器人对该用户不可用
- 解决：用户需要先与机器人建立会话

## 更新日志
- v1.0.0 (2026-03-19): 初始版本，支持发送图片
