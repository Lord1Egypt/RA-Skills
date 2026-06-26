# 配置指南

本文档将指导你如何配置微信公众号发布器技能包。

## 第一步：获取微信公众号 AppID 和 AppSecret

1. 登录微信公众平台：https://mp.weixin.qq.com
2. 进入【开发 - 基本配置】
3. 复制 AppID 和 AppSecret

> ⚠️ **重要提示**：AppSecret 非常重要，请妥善保管，不要泄露给他人！

## 第二步：设置IP白名单（必须）

⚠️ **这一步非常重要！如果不设置IP白名单，技能包将无法发送文章到草稿箱。**

### 为什么需要设置IP白名单？

微信公众号API要求调用接口的IP地址必须在白名单中，否则会返回错误：
```
{"errcode":40164,"errmsg":"invalid ip, hint: [xxxxx]"}
```

### 如何设置IP白名单？

#### 方法一：查看当前IP并设置

1. **查看你的公网IP**
   - 访问：https://www.ip.cn
   - 或在终端执行：`curl ifconfig.me`
   - 记下显示的IP地址

2. **在微信公众平台设置白名单**
   - 登录微信公众平台：https://mp.weixin.qq.com
   - 进入【开发 - 基本配置】
   - 找到【IP白名单】设置
   - 点击【修改】
   - 输入你的IP地址
   - 点击【确认】

#### 方法二：如果不确定IP，可以先尝试发布

1. 先不设置白名单
2. 尝试使用技能包发布文章
3. 如果失败，查看错误信息中的IP地址
4. 将该IP地址添加到白名单

#### 多IP情况处理

如果你有多个IP地址（例如公司、家里、VPN等），可以添加多个IP：

```
IP白名单格式：
192.168.1.100,202.96.128.86,114.114.114.114
```

- 多个IP用英文逗号分隔
- 每个公众号最多可设置20个IP
- 建议添加所有可能使用的IP

### 常见问题

**Q1：我的IP是动态的，经常变化怎么办？**

A: 如果你的IP经常变化（例如家庭宽带），建议：
- 每次使用前先查看IP，更新白名单
- 或者使用固定IP的VPN/代理
- 联系运营商申请固定IP

**Q2：如何验证白名单设置成功？**

A: 在WorkBuddy中说："测试公众号连接"，AI会自动测试API连接是否正常。

**Q3：设置白名单后还是报错怎么办？**

A: 
1. 等待5-10分钟让设置生效
2. 确认IP地址格式正确（不要包含端口号）
3. 确认IP是公网IP，不是内网IP（192.168.x.x 是内网IP）

## 第二步：创建配置文件

### 方式一：复制模板文件（推荐）

1. 复制 `references/config.template.json`
2. 重命名为 `references/my_accounts.json`（或你喜欢的名称）
3. 填写你的公众号信息

### 方式二：从零创建

在 `references/` 目录下创建 JSON 文件，格式如下：

```json
{
  "version": "1.0",
  "last_updated": "",
  "current_account": "account_1",
  "accounts": [
    {
      "id": "account_1",
      "name": "你的公众号名称",
      "app_id": "你的AppID",
      "app_secret": "你的AppSecret",
      "author": "作者名称",
      "description": "公众号简介",
      "base_dir": "公众号-你的公众号名称",
      "theme_color": "#667eea",
      "default_cover_style": 1,
      "active": true,
      "created_at": "",
      "total_articles": 0,
      "last_publish": null
    }
  ],
  "global_settings": {
    "cover_styles": [...]
  }
}
```

## 第三步：配置字段说明

### 必填字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | 公众号名称 | "我与AI那些事" |
| `app_id` | 微信 AppID | "wx94029d52b0b25543" |
| `app_secret` | 微信 AppSecret | "583856bd1c7075ffdd2e9f9bd415a0c2" |
| `author` | 作者名称 | "我与AI那些事" |
| `base_dir` | 工作目录名称 | "公众号-我与AI那些事" |

### 可选字段

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `description` | 公众号简介 | "" |
| `theme_color` | 主题色 | "#667eea" |
| `default_cover_style` | 默认封面风格（1-5） | 1 |
| `active` | 是否启用 | true |

### 封面风格选项

| 编号 | 风格名称 | 适用场景 |
|------|---------|---------|
| 1 | 紫色科技风 | 科技、AI、工具类文章 |
| 2 | 蓝色科技风 | 技术、教程类文章 |
| 3 | 粉色渐变风 | 生活、情感类文章 |
| 4 | 橙色活力风 | 活动、新闻类文章 |
| 5 | 绿色清新风 | 自然、健康类文章 |

## 第四步：配置文件查找顺序

AI 会按以下顺序查找配置文件：

1. 用户指定的配置文件路径（推荐）
2. `references/my_accounts.json`（你的私人配置）
3. `references/config.json`（你的私人配置）
4. `references/multi_account_config.json`（你的私人配置）

如果找不到任何配置文件，AI 会提示你先创建配置。

## 多账号配置

支持同时管理多个公众号，在 `accounts` 数组中添加多个账号即可：

```json
{
  "accounts": [
    {
      "id": "account_1",
      "name": "第一个公众号",
      "app_id": "...",
      "app_secret": "...",
      ...
    },
    {
      "id": "account_2",
      "name": "第二个公众号",
      "app_id": "...",
      "app_secret": "...",
      ...
    }
  ]
}
```

### 多账号管理命令

- "切换到【公众号名称】" - 切换当前公众号
- "列出所有公众号" - 查看所有配置的公众号
- "查看公众号发布情况" - 查看所有公众号的发布记录

## 安全提示

### ⚠️ 重要安全建议

1. **不要上传敏感配置**：包含 AppSecret 的配置文件不要上传到公开仓库
2. **使用 .gitignore**：将敏感配置文件加入忽略列表
3. **定期更换 AppSecret**：建议每 3-6 个月更换一次
4. **限制 IP 白名单**：在微信公众平台设置 IP 白名单

### 推荐的 .gitignore 配置

```gitignore
# 微信公众号配置文件（包含敏感信息）
references/my_accounts.json
references/config.json
references/multi_account_config.json

# 发布日志和文章草稿
公众号-*/
```

## 配置验证

配置完成后，你可以说：

- "列出所有公众号" - 验证配置是否正确加载
- "查看当前公众号状态" - 确认当前公众号配置

如果配置正确，AI 会显示你的公众号信息。

## 常见问题

### Q1：配置文件放在哪里？

配置文件放在技能包的 `references/` 目录下。

### Q2：可以配置多个公众号吗？

可以，在 `accounts` 数组中添加多个账号即可。

### Q3：AppSecret 忘记了怎么办？

登录微信公众平台，在【开发 - 基本配置】中重置 AppSecret。

### Q4：配置文件格式错误怎么办？

请确保 JSON 格式正确，可以使用在线 JSON 验证工具检查。

### Q5：如何备份配置？

建议将配置文件复制到安全的位置备份，或使用加密工具加密后备份。

## 技术支持

如有问题，请访问：

- GitHub Issues: [提交问题](https://github.com/your-repo/issues)
- 文档: [完整文档](README.md)
