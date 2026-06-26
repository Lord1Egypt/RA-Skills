# yaniw-wechat-publisher

微信公众号自动化发布工具，支持多账号管理。

## 功能特性

- **多账号管理** - 支持同时管理多个公众号，快速切换
- **智能文章生成** - 根据主题自动生成符合公众号风格的文章
- **5种封面风格** - 紫色科技、蓝色科技、粉色渐变、橙色活力、绿色清新
- **自动截图** - 使用 Playwright 自动生成封面图 PNG
- **一键发布** - 自动发布到微信公众号草稿箱
- **严格确认机制** - 每个环节都需要用户确认，防止误操作

## 快速开始

### 1. 环境要求

- Python 3.7+
- Playwright
- requests

### 2. 安装依赖

```bash
pip install requests playwright
playwright install chromium
```

### 3. 配置公众号

**方式一：环境变量配置（推荐，更安全）**

1. 复制 `.env.example` 为 `.env`
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填写你的 AppID 和 AppSecret
   ```bash
   WECHAT_APP_ID_1=你的AppID
   WECHAT_APP_SECRET_1=你的AppSecret
   ```

**方式二：配置文件（传统方式）**

1. 复制 `references/config.template.json` 为 `references/my_accounts.json`
2. 填写你的 AppID 和 AppSecret

⚠️ **安全提示：** 环境变量方式更安全，推荐使用！

4. **设置IP白名单**（必须，否则无法发布文章）
   - 访问微信公众平台【开发 - 基本配置 - IP白名单】
   - 添加你当前使用的IP地址
   - 详细步骤请查看 [CONFIGURATION.md](CONFIGURATION.md#第二步设置ip白名单必须)

5. 详细配置请查看 [CONFIGURATION.md](CONFIGURATION.md)

### 4. 使用方法

在 WorkBuddy 中说：

- "今天给公众号写一篇文章"
- "切换到家有野猫公众号"
- "列出所有公众号"
- "查看发布情况"

## 工作流程

```
生成内容 → 用户确认 → 生成封面 → 用户选择 → 自动发布
```

⚠️ **每个环节都需要用户确认，绝对不会自动发布**

### 详细流程

#### 第一步：选择公众号

```
用户："今天给'我与AI那些事'写一篇文章"
AI：✅ 已切换到"我与AI那些事"公众号
```

#### 第二步：生成文章

```
用户："写一篇关于AI写作的文章"
AI：📄 文章已生成...
    ⚠️ 请确认文章内容是否满意？
```

#### 第三步：生成封面

```
用户："内容没问题"
AI：✅ 已生成5个封面图风格
    ⚠️ 请选择你喜欢的封面图风格？（输入编号1-5）
```

#### 第四步：发布文章

```
用户："选择风格1"
AI：✅ 封面图已生成
    ✅ 已发布到公众号草稿箱
```

## 文档

- **[用户使用指南](USER_GUIDE.md)** - 完整的用户使用流程和常见问题解答
- **[配置指南](CONFIGURATION.md)** - 如何配置公众号信息和IP白名单
- **[测试流程](TEST_GUIDE.md)** - 功能测试和验证步骤
- **[打包上架指南](PUBLISH_GUIDE.md)** - 技能包打包和上架流程
- [工作流程](references/workflow_guide.md) - 详细工作流程说明
- [文章格式](references/article_format.md) - 文章格式规范
- [封面风格](references/cover_styles.md) - 5种封面风格说明

## 目录结构

```
yaniw-wechat-publisher/
├── SKILL.md                      # 技能主文档
├── README.md                     # 本文件
├── CONFIGURATION.md              # 配置指南
├── scripts/                      # Python 脚本
│   ├── init_account.py          # 初始化账号
│   ├── switch_account.py        # 切换账号
│   ├── generate_article.py      # 生成文章
│   ├── generate_covers.py       # 生成封面图
│   ├── screenshot_cover.py      # 截图生成 PNG
│   ├── publish_to_wechat.py     # 发布到微信
│   └── log_publish.py           # 记录日志
├── references/                   # 参考文档和配置
│   ├── config.template.json     # 配置模板
│   ├── workflow_guide.md        # 工作流程指南
│   ├── article_format.md        # 文章格式规范
│   └── cover_styles.md          # 封面风格说明
└── assets/                       # 资源文件
    └── cover_templates/         # 封面图 HTML 模板
        ├── style_1_purple.html
        ├── style_2_blue.html
        ├── style_3_pink.html
        ├── style_4_orange.html
        └── style_5_green.html
```

## 封面风格

| 编号 | 风格名称 | 颜色特征 | 适用场景 |
|------|---------|---------|---------|
| 1 | 紫色科技风 | 渐变紫色调 | 科技、AI、工具类 |
| 2 | 蓝色科技风 | 深蓝色调 | 技术、教程类 |
| 3 | 粉色渐变风 | 粉红色调 | 生活、情感类 |
| 4 | 橙色活力风 | 橙色色调 | 活动、新闻类 |
| 5 | 绿色清新风 | 绿色色调 | 自然、健康类 |

## 常见问题

### Q1：如何添加新公众号？

编辑配置文件，在 `accounts` 数组中添加新账号即可。

### Q2：AppSecret 泄露了怎么办？

立即在微信公众平台重置 AppSecret，并更新配置文件。

### Q3：文章发布失败怎么办？

检查以下内容：
- AppID 和 AppSecret 是否正确
- **IP白名单是否已设置**（最常见原因）
- 网络连接是否正常
- 微信公众平台是否有其他限制

### Q4：如何查看我的IP地址？

访问 https://www.ip.cn 或在终端执行：
```bash
curl ifconfig.me
```

### Q4：封面图生成失败怎么办？

确保已安装 Playwright：
```bash
playwright install chromium
```

### Q5：可以自定义封面风格吗？

可以，修改 `assets/cover_templates/` 中的 HTML 模板文件。

## 安全建议

1. **不要上传敏感配置** - 包含 AppSecret 的配置文件不要上传到公开仓库
2. **定期更换 AppSecret** - 建议每 3-6 个月更换一次
3. **设置IP白名单** - 必须设置IP白名单才能使用API发布文章
4. **使用 .gitignore** - 将敏感配置文件加入忽略列表

详见 [CONFIGURATION.md](CONFIGURATION.md) 中的安全提示。

## 版本历史

### v1.1.0 (2026-03-12)

- **安全增强**：支持环境变量配置（推荐使用 .env 文件）
- **凭证管理器**：新增 credential_manager.py，支持多源凭证获取
- **错误脱敏**：API 错误信息自动脱敏，避免泄露敏感配置
- 降低安全风险等级（从"中等风险"优化到"低风险"）

### v1.0.0 (2026-03-12)

- 首次发布
- 支持多账号管理
- 5种封面风格模板
- 完整的确认机制
- 自动发布到草稿箱

## 开源协议

MIT License

## 作者

yaniw

## 技术支持

如有问题或建议，欢迎：

- 提交 Issue
- 发送反馈
- 查看文档

---

**享受自动化发布带来的效率提升！** 🚀
