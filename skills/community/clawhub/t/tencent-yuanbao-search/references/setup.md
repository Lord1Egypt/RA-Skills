# 元宝搜索skill - 环境配置指南 （OpenClaw）

**推荐**: 使用 OpenClaw 配置文件进行管理

## 未配置环境变量 TENCENTCLOUD_WSA_APIKEY
如果环境变量 `TENCENTCLOUD_WSA_APIKEY` 没有设置，则参考以下步骤：

### 获取 API key密钥

访问 https://console.cloud.tencent.com/wsapi/index?tab=apikey

1. 登录腾讯云账号，开通元宝搜索服务。
2. 查看你的API key，如果没有则新建一个API key并保存
3. 复制你要使用的API key

## 配置 OpenClaw

### 方法一：在可视化界面中操作
在OpenClaw管理界面中配置 TENCENTCLOUD_WSA_APIKEY

### 方法二：编辑.env文件 
在OpenClaw中，使用.env文件配置环境变量是管理API Key的推荐方式，防止敏感信息泄露。
文件的位置为：
- Linux/MacOS: `~/.openclaw/.env`
- Windows: ：`%USERPROFILE%/.openclaw/.env`
如果没有可自己创建。

在.env中定义：
```
TENCENTCLOUD_WSA_APIKEY=<your_actual_api_key_here>
```

### 方法三：编辑OpenClaw配置文件
OpenClaw配置文件的位置为：
- Linux/MacOS: `~/.openclaw/openclaw.json`
- Windows: ：`%USERPROFILE%/.openclaw/openclaw.json`

添加或修改以下部分：
```json
{
  "env": {
    "vars": {
      "TENCENTCLOUD_WSA_APIKEY": "your_actual_api_key_here"
    }
  }
}
```
替换 `"your_actual_api_key_here"` 为你自己的 API key.

重启OpenClaw


## 故障排除

### API 密钥无效

- 确认密钥正确复制，没有多余空格
- 检查腾讯云控制台，确认密钥状态

### 环境变量不生效

- macOS / Linux：确认编辑的是正确的 shell 配置文件（bash vs zsh）
- Windows：设置后需要重启终端或应用程序
- 某些系统需要完全重启才能生效
