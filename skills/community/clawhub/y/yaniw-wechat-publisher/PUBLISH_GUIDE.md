# 技能包打包上架流程

本文档说明如何将 `yaniw-wechat-publisher` 技能包打包并上架到技能市场。

---

## 📋 上架前检查清单

### 第一步：功能测试

在打包之前，请务必完成以下测试：

#### 1.1 基础功能测试

- [ ] **多账号管理**
  - 测试切换账号功能
  - 测试列出所有公众号
  - 测试查看发布记录

- [ ] **文章生成**
  - 测试文章内容生成
  - 检查文章格式是否正确
  - 检查标题、摘要、文末关键字

- [ ] **封面图生成**
  - 测试5种封面风格生成
  - 检查封面图尺寸（900x383）
  - 检查封面图质量

- [ ] **截图功能**
  - 测试 Playwright 截图
  - 检查PNG文件生成

- [ ] **发布功能**
  - 测试上传封面图
  - 测试发布到草稿箱
  - 检查发布日志记录

#### 1.2 错误处理测试

- [ ] 测试IP白名单错误提示
- [ ] 测试AppSecret错误提示
- [ ] 测试网络错误处理
- [ ] 测试配置文件缺失处理

#### 1.3 配置测试

- [ ] 测试 `config.template.json` 格式正确
- [ ] 测试用户创建 `my_accounts.json` 后功能正常
- [ ] 测试配置文件路径查找逻辑

### 第二步：安全检查

#### 2.1 敏感信息检查

**必须确认以下文件不包含敏感信息：**

```bash
# 检查配置模板
cat references/config.template.json
# 确认：
# - app_id: "你的AppID"（不是真实AppID）
# - app_secret: "你的AppSecret"（不是真实AppSecret）
# - name: "你的公众号名称"（不是真实名称）

# 检查SKILL.md
cat SKILL.md
# 确认没有硬编码的真实信息

# 检查README.md
cat README.md
# 确认示例不是真实信息
```

#### 2.2 文件完整性检查

**必须存在的文件：**

```
yaniw-wechat-publisher/
├── SKILL.md                      ✅
├── README.md                     ✅
├── CONFIGURATION.md              ✅
├── USER_GUIDE.md                 ✅
├── CHANGELOG.md                  ✅
├── requirements.txt              ✅
├── .gitignore                    ✅
├── scripts/                      ✅
│   ├── init_account.py          ✅
│   ├── switch_account.py        ✅
│   ├── generate_article.py      ✅
│   ├── generate_covers.py       ✅
│   ├── screenshot_cover.py      ✅
│   ├── publish_to_wechat.py     ✅
│   └── log_publish.py           ✅
├── references/                   ✅
│   ├── config.template.json     ✅
│   ├── workflow_guide.md        ✅
│   ├── article_format.md        ✅
│   └── cover_styles.md          ✅
└── assets/                       ✅
    └── cover_templates/         ✅
        ├── style_1_purple.html  ✅
        ├── style_2_blue.html    ✅
        ├── style_3_pink.html    ✅
        ├── style_4_orange.html  ✅
        └── style_5_green.html   ✅
```

**不能存在的文件：**

```
❌ references/my_accounts.json
❌ references/config.json
❌ references/multi_account_config.json
❌ 任何包含真实AppSecret的文件
❌ 任何包含真实公众号信息的文件
```

#### 2.3 .gitignore 检查

确认 `.gitignore` 包含：

```
references/my_accounts.json
references/config.json
references/multi_account_config.json
公众号-*/
```

### 第三步：文档检查

#### 3.1 文档完整性

- [ ] README.md 包含功能介绍、快速开始、使用方法
- [ ] CONFIGURATION.md 包含详细配置步骤、IP白名单设置
- [ ] USER_GUIDE.md 包含完整用户使用指南
- [ ] SKILL.md 包含技能说明、工作流程、错误处理
- [ ] CHANGELOG.md 包含版本更新记录
- [ ] requirements.txt 包含依赖列表

#### 3.2 文档准确性

- [ ] 所有示例都是占位符，不是真实信息
- [ ] IP白名单设置说明清晰完整
- [ ] 错误处理说明详细
- [ ] 用户能够独立完成配置

---

## 📦 打包流程

### 方式一：手动打包（推荐）

#### 步骤1：进入技能目录

```bash
cd /Users/zgedu/WorkBuddy/Claw/.codebuddy/skills/
```

#### 步骤2：检查敏感信息

```bash
# 确认没有敏感配置文件
ls yaniw-wechat-publisher/references/

# 应该看到：
# article_format.md  config.template.json  cover_styles.md  workflow_guide.md
# 不应该看到：my_accounts.json、config.json、multi_account_config.json
```

#### 步骤3：创建ZIP包

```bash
zip -r yaniw-wechat-publisher-v1.0.0.zip yaniw-wechat-publisher/
```

#### 步骤4：验证ZIP包

```bash
# 解压测试
unzip -l yaniw-wechat-publisher-v1.0.0.zip

# 确认文件列表正确
# 确认没有敏感文件
```

### 方式二：使用Git（如果有仓库）

#### 步骤1：初始化Git仓库

```bash
cd yaniw-wechat-publisher/
git init
```

#### 步骤2：创建 .gitignore

确保 `.gitignore` 已存在且包含敏感文件。

#### 步骤3：提交代码

```bash
git add .
git commit -m "v1.0.0 - 首次发布"
git tag v1.0.0
```

#### 步骤4：推送到远程仓库

```bash
git remote add origin https://github.com/your-username/yaniw-wechat-publisher.git
git push -u origin master
git push --tags
```

---

## 🚀 上架流程

### 平台选择

#### 平台1：ClawHub（国际平台）

**优点：**
- 国际化平台
- 英文界面
- 全球用户

**上架步骤：**

1. 访问 https://clawhub.io
2. 注册开发者账号
3. 点击"Publish Skill"
4. 填写技能信息：
   - Name: `yaniw-wechat-publisher`
   - Description: `WeChat Official Account automation tool with multi-account support`
   - Version: `1.0.0`
   - Author: `yaniw`
   - Tags: `wechat, official-account, automation, publisher, multi-account`
   - Category: `Productivity`
5. 上传ZIP文件或提供Git仓库地址
6. 提交审核

#### 平台2：SkillHub（腾讯云技能市场）

**优点：**
- 中文界面
- 中国用户多
- 腾讯官方支持

**上架步骤：**

1. 访问腾讯云技能市场
2. 登录腾讯云账号
3. 点击"发布技能"
4. 填写技能信息：
   - 名称：`yaniw-wechat-publisher`
   - 描述：`微信公众号自动化发布工具，支持多账号管理`
   - 版本：`1.0.0`
   - 作者：`yaniw`
   - 标签：`微信、公众号、自动化、发布工具、多账号管理`
   - 分类：`生产力工具`
5. 上传ZIP文件
6. 提交审核

### 审核流程

#### 审核时间

- ClawHub: 1-3个工作日
- SkillHub: 1-3个工作日

#### 审核内容

1. **安全性审核**
   - 检查是否有恶意代码
   - 检查是否有敏感信息泄露
   - 检查是否有安全漏洞

2. **功能审核**
   - 检查功能是否正常
   - 检查文档是否完整
   - 检查用户体验

3. **合规性审核**
   - 检查是否符合平台规范
   - 检查是否有侵权内容
   - 检查是否符合法律法规

#### 审核结果

- **通过**：技能上架，用户可以下载使用
- **不通过**：根据反馈修改后重新提交

---

## 📝 上架后维护

### 版本更新流程

#### 小版本更新（1.0.0 → 1.0.1）

适用于：Bug修复、小优化

```bash
# 1. 修改代码
# 2. 更新 CHANGELOG.md
# 3. 提交代码
git commit -am "v1.0.1 - 修复xxx问题"
git tag v1.0.1

# 4. 打包
zip -r yaniw-wechat-publisher-v1.0.1.zip yaniw-wechat-publisher/

# 5. 在技能市场更新版本
```

#### 大版本更新（1.0.0 → 1.1.0）

适用于：新功能、大改进

```bash
# 1. 开发新功能
# 2. 更新文档
# 3. 更新 CHANGELOG.md
# 4. 提交代码
git commit -am "v1.1.0 - 新增xxx功能"
git tag v1.1.0

# 5. 打包
zip -r yaniw-wechat-publisher-v1.1.0.zip yaniw-wechat-publisher/

# 6. 在技能市场更新版本
```

### 用户反馈处理

1. 定期查看技能市场的用户评论
2. 收集用户问题和建议
3. 及时回复用户反馈
4. 根据反馈优化功能
5. 发布更新版本

---

## ✅ 上架检查清单（最终确认）

在点击"提交审核"之前，请再次确认：

### 安全检查

- [ ] 确认ZIP包中无真实AppID/AppSecret
- [ ] 确认ZIP包中无真实公众号名称
- [ ] 确认ZIP包中无个人敏感信息
- [ ] 确认 `.gitignore` 配置正确

### 文档检查

- [ ] README.md 完整且准确
- [ ] CONFIGURATION.md 包含IP白名单设置说明
- [ ] USER_GUIDE.md 用户使用指南完整
- [ ] SKILL.md 技能说明准确
- [ ] CHANGELOG.md 版本记录完整

### 功能检查

- [ ] 所有功能测试通过
- [ ] 错误处理完善
- [ ] 配置模板格式正确
- [ ] 用户能独立完成配置

### 打包检查

- [ ] ZIP包文件列表正确
- [ ] ZIP包大小合理（建议<10MB）
- [ ] ZIP包可以正常解压

### 上架信息检查

- [ ] 技能名称正确
- [ ] 描述准确
- [ ] 版本号正确
- [ ] 作者信息正确
- [ ] 标签合适
- [ ] 分类正确

---

**全部确认后，点击"提交审核"！** 🚀

---

## 📞 遇到问题？

如果在打包或上架过程中遇到问题：

1. 查看平台官方文档
2. 查看平台社区问答
3. 联系平台客服
4. 在GitHub提交Issue

---

**祝你上架成功！** 🎉
