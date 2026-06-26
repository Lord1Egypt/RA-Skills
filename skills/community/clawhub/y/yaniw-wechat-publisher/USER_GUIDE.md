# 用户使用指南

本文档面向下载并使用 `yaniw-wechat-publisher` 技能包的用户。

## 📋 使用前准备清单

在开始使用之前，请确保完成以下准备工作：

- [ ] 已安装 WorkBuddy
- [ ] 已安装 Python 3.7+
- [ ] 已安装 Playwright（`pip install playwright && playwright install chromium`）
- [ ] 已下载技能包
- [ ] 已获取微信公众号 AppID 和 AppSecret
- [ ] **已设置IP白名单**（必须）

---

## 🚀 快速开始（5步完成配置）

### 第1步：下载技能包

从技能市场下载 `yaniw-wechat-publisher` 技能包，放置在 WorkBuddy 的技能目录下：

```
你的工作目录/.codebuddy/skills/yaniw-wechat-publisher/
```

### 第2步：获取公众号信息

1. 登录微信公众平台：https://mp.weixin.qq.com
2. 进入【开发 - 基本配置】
3. 复制 **AppID** 和 **AppSecret**

### 第3步：设置IP白名单（必须）

⚠️ **这一步非常重要！不设置IP白名单将无法发布文章。**

#### 如何设置？

**方式一：先查看IP，再设置**

1. 查看你的公网IP地址
   - 访问：https://www.ip.cn
   - 或在终端执行：`curl ifconfig.me`
   
2. 在微信公众平台设置白名单
   - 进入【开发 - 基本配置 - IP白名单】
   - 点击【修改】
   - 输入你的IP地址
   - 点击【确认】

**方式二：先尝试发布，根据错误提示设置**

1. 先不设置白名单
2. 尝试使用技能包发布文章
3. 如果失败，AI会显示你的IP地址
4. 将显示的IP添加到白名单
5. 等待5-10分钟后重试

#### 多IP处理

如果你有多个IP地址（公司、家里、VPN等），可以添加多个IP：

```
格式：192.168.1.100,202.96.128.86,114.114.114.114
```

- 多个IP用英文逗号分隔
- 每个公众号最多可设置20个IP

### 第4步：创建配置文件

1. 进入技能包目录：
   ```bash
   cd 你的工作目录/.codebuddy/skills/yaniw-wechat-publisher/references/
   ```

2. 复制配置模板：
   ```bash
   cp config.template.json my_accounts.json
   ```

3. 编辑 `my_accounts.json`，填写你的公众号信息：
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
       ...
     }
   }
   ```

### 第5步：开始使用

在 WorkBuddy 中说：

- "今天给公众号写一篇文章"
- "写一篇关于AI的文章"

---

## 💡 使用方法

### 场景1：生成文章并发布

**完整流程：**

```
用户："今天给公众号写一篇关于AI写作的文章"
    ↓
AI生成文章内容
    ↓
用户确认："内容没问题"
    ↓
AI生成5种封面图风格
    ↓
用户选择："选择风格1"
    ↓
AI自动截图并发布到草稿箱
    ↓
完成！
```

**每个环节都需要你确认，不会自动发布。**

### 场景2：多账号管理

如果你有多个公众号：

1. **配置多账号**
   
   在 `my_accounts.json` 中添加多个账号：
   ```json
   {
     "accounts": [
       {
         "id": "account_1",
         "name": "第一个公众号",
         ...
       },
       {
         "id": "account_2",
         "name": "第二个公众号",
         ...
       }
     ]
   }
   ```

2. **切换账号**
   
   在 WorkBuddy 中说：
   - "切换到【公众号名称】"
   - "切换到家有野猫"

3. **查看所有公众号**
   
   说："列出所有公众号"

### 场景3：查看发布记录

说："查看公众号发布情况"

AI会显示所有公众号的发布记录。

---

## ⚠️ 常见问题解决

### 问题1：发布失败，提示"invalid ip"

**原因**：IP白名单未设置或设置错误

**解决方案**：

1. AI会自动显示你的当前IP
2. 将该IP添加到微信公众平台的白名单中
3. 等待5-10分钟
4. 重试发布

**详细步骤**：
1. 访问微信公众平台【开发 - 基本配置 - IP白名单】
2. 点击【修改】
3. 输入IP地址
4. 点击【确认】

### 问题2：AppSecret 错误

**原因**：配置文件中的 AppSecret 不正确

**解决方案**：

1. 登录微信公众平台
2. 进入【开发 - 基本配置】
3. 查看或重置 AppSecret
4. 更新配置文件 `my_accounts.json`

### 问题3：封面图生成失败

**原因**：Playwright 未安装或安装不完整

**解决方案**：

```bash
pip install playwright
playwright install chromium
```

### 问题4：我的IP经常变化怎么办？

**原因**：使用的是动态IP（如家庭宽带）

**解决方案**：

1. 每次使用前查看IP并更新白名单
2. 使用固定IP的VPN
3. 联系运营商申请固定IP

### 问题5：如何验证配置是否正确？

在 WorkBuddy 中说：

- "测试公众号连接"
- "列出所有公众号"

如果配置正确，会显示你的公众号信息。

---

## 📚 文档索引

- [README.md](README.md) - 项目说明和功能介绍
- [CONFIGURATION.md](CONFIGURATION.md) - 详细配置指南
- [CHANGELOG.md](CHANGELOG.md) - 版本更新记录
- [工作流程](references/workflow_guide.md) - 详细工作流程说明
- [文章格式](references/article_format.md) - 文章格式规范
- [封面风格](references/cover_styles.md) - 5种封面风格说明

---

## 🔒 安全提示

1. **不要分享配置文件**
   
   `my_accounts.json` 包含你的 AppSecret，不要分享给他人。

2. **不要上传到公开仓库**
   
   如果使用Git管理，确保配置文件在 `.gitignore` 中。

3. **定期更换 AppSecret**
   
   建议每3-6个月更换一次 AppSecret。

4. **保护IP白名单**
   
   只添加你信任的IP地址。

---

## 📞 技术支持

如有问题，可以：

1. 查看本文档和 [CONFIGURATION.md](CONFIGURATION.md)
2. 在技能包的 GitHub 仓库提交 Issue
3. 联系技能包开发者

---

## ✅ 检查清单

使用前请确认：

- [ ] 已安装 Python 3.7+
- [ ] 已安装 Playwright 和 Chromium
- [ ] 已获取 AppID 和 AppSecret
- [ ] **已设置IP白名单**
- [ ] 已创建 `my_accounts.json` 配置文件
- [ ] 配置文件中的信息正确
- [ ] 已在 WorkBuddy 中测试连接

全部完成后，就可以开始使用了！🎉
