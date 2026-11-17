# 企业微信智能机器人 — 分步部署指南

本教程带你**从零开始**搭建一个能接收语音消息的企业微信智能机器人。
按照以下步骤操作，**不需要任何编程基础**。

---

## 第一步：前提条件

确保你已具备：

- [ ] 一台 Windows 电脑（已安装企业微信）
- [ ] 注册一个企业微信账号
- [ ] 安装 Python 3.8+

检查 Python 安装：

```bash
python --version
```

---

## 第二步：获取企业微信 CorpID 和 Secret

### 2.1 获取 CorpID

1. 打开 https://work.weixin.qq.com
2. 登录你的企业微信管理后台
3. 点击 **我的企业** → 下拉找到 **企业ID**
4. 复制并保存这个 ID（例如：`ww1234567890abcdef`）

### 2.2 创建自建应用

1. 管理后台 → **应用管理** → **自建** → **创建应用**
2. 填写应用名称（如"语音助手"），上传一个 logo
3. 可见范围选择 **全部成员**
4. 创建后进入该应用，记录以下信息：
   - **AgentID**（应用 ID）
   - **Secret**（应用密钥）

---

## 第三步：配置智能机器人回调

1. 在应用详情页面找到 **智能机器人**
2. 点击 **开启**，设置以下参数：

```
回调 Token: 任意字符串（如 my_wecom_voice_bot_2026）
EncodingAESKey: 随机生成或自己填写一个 43 位字符串
```

3. **回调 URL**：先填写一个临时地址（如 `http://example.com/callback`），等服务器启动后再更新

---

## 第四步：启动本地服务器

### 4.1 进入技能目录

```bash
cd D:\skill\wecom-voice-agent
```

### 4.2 启动 Webhook 服务器

```bash
python scripts/wecom_webhook_server.py --port 8080
```

看到以下输出说明启动成功：

```
============================================================
企业微信语音消息回调服务器已启动
监听地址: http://0.0.0.0:8080
...
============================================================
```

### 4.3 URL 验证

企业微信会向你的回调 URL 发送 GET 请求验证。确保：
- 你的服务器正在运行
- URL 路径是 `/`（即服务器访问地址 + `/`）

验证通过后，服务器日志会显示：

```
INFO: URL 验证请求已处理
```

---

## 第五步：内网穿透（如果你的电脑没有公网 IP）

大多数公司/家庭网络没有公网 IP，需要使用内网穿透工具暴露 8080 端口。

### 使用 frp（推荐）

```bash
# 安装 frp 后
frpc http -l 8080 -p your-domain.com
```

### 使用 ngrok（快速）

```bash
ngrok http 8080
```

获得一个公网地址如 `https://abc123.ngrok-free.app`，将其作为回调 URL。

---

## 第六步：更新回调 URL

回到企业微信管理后台 → 智能机器人 → 编辑回调 URL：

```
https://abc123.ngrok-free.app/
```

提交后企业微信会重新验证 URL，看到验证成功即可。

---

## 第七步：测试语音消息

1. 打开企业微信客户端
2. 搜索你刚刚创建的机器人应用（如"语音助手"）
3. 发送一条语音消息："明天有什么会议？"
4. 机器人应该回复一个帮助信息的文字消息

**成功！** 你的企业微信语音助手已经上线了。

---

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| 验证 URL 失败 | 检查服务器是否启动、端口是否正确、穿透工具是否运行 |
| 收不到语音消息 | 确保回调 URL 正确、智能机器人已开启、消息类型支持语音 |
| 中文乱码 | 服务器已使用 UTF-8 编码，检查终端编码设置 |
| 被动回复超时 | 单次回复超过 5 秒会被企业微信丢弃，检查代码性能 |

---

## 高级配置

### 配置 Token/AESKey 解密

本技能默认部署。如需加密解密消息，请修改配置：

```python
WECHAT_CONFIG = {
    "token": "your_real_token",
    "encoding_aes_key": "your_real_key",
    ...
}
```

并安装加密包：

```bash
pip install pycryptodome
```

### 扩展功能（接入企业微信 API）

当你的技能需要回发消息、查询日历时，需要获取 access_token：

```bash
curl -s -X POST \
  'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ww1234567890abcdef&corpsecret=YOUR_SECRET' \
  | python -c "import sys,json;d=json.load(sys.stdin);print(d['access_token'])"
```

---

## 下一步

配置好服务器后，继续学习：
- [企业微信机器人 API 参考](../../references/wecom_bot_api.md)
- [意图解析器配置]（修改 `wecom_webhook_server.py` 中的 `intent_keywords` 字典）
- [会话持久化]（将 `self.sessions` 替换为文件或数据库存储）

如有问题，发送邮件至：**njskills@agent.qq.com**
