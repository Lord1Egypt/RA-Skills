# 豆包文生图 Skill - Clawhub 发布指南

**版本：** 2.0.0  
**发布日期：** 2026-04-10  
**状态：** ✅ 准备发布

---

## 📦 发布包内容

发布包位置：`/Users/yangyang713/.workbuddy/skills/doubao-image-v2.0.0.zip`

包含文件：
```
doubao-image/
├── SKILL.md                    # ✅ Skill 定义（必需）
├── README.md                   # ✅ 使用文档（必需）
├── CHANGELOG.md                # ✅ 版本历史
├── LICENSE                     # ✅ 开源协议
├── .gitignore                  # Git 配置
├── examples/
│   └── promtps.md              # Prompt 示例
└── scripts/
    ├── doubao-image-generate.sh    # ✅ Bash 实现
    ├── doubao-image-generate.py    # ✅ Python 实现
    └── check-env.sh                # 环境检查工具
```

---

## 🚀 发布方式（三种选一）

### 方式一：通过 Clawhub 平台上传（推荐）

#### 步骤 1：访问发布页面

打开浏览器访问：
```
https://clawhub.cn/marketplace/publish
```

#### 步骤 2：登录/注册

- 如有账号直接登录
- 如无账号先注册开发者账号

#### 步骤 3：填写技能信息

**基本信息：**
- **技能名称：** 豆包文生图
- **技能标识：** doubao-image
- **版本号：** 2.0.0
- **分类：** AI 工具
- **标签：** AI, 文生图，豆包，图像生成，Doubao, SeeDream

**简介（短描述）：**
```
基于字节跳动豆包 SeeDream 5.0 模型的 AI 文生图工具，支持 2K/1080P/720P 分辨率，
提供 Bash 和 Python 双实现，完善的错误处理和详细文档。
```

**详细描述：**
```markdown
## 功能特性

✨ **核心功能**
- 🎨 AI 图像生成 - 基于豆包 SeeDream 5.0 模型
- 📐 多分辨率支持 - 2K/1080P/720P 可选
- 💧 水印控制 - 灵活选择是否添加水印
- 🔄 自动重试 - 智能错误处理和指数退避
- 📦 双实现方案 - Bash 和 Python 两种脚本

✨ **技术特性**
- 完善的错误处理和日志记录
- 支持环境变量配置
- 跨平台兼容（macOS/Linux）
- 详细的中文文档

## 使用方法

### 前置条件
1. 获取火山引擎 ARK API Key：https://console.volcengine.com/ark
2. 设置环境变量：export ARK_API_KEY="your_key"

### Bash 脚本
./scripts/doubao-image-generate.sh "一只在月光下的白色小猫"

### Python 脚本
python3 scripts/doubao-image-generate.py --prompt "一只在月光下的白色小猫"

## 适用场景
- AI 艺术创作
- 插画设计
- 内容创作
- 社交媒体配图
- 概念艺术

## 技术栈
- Bash 4.0+
- Python 3.8+
- curl 7.0+
- 火山引擎 ARK API
```

**其他信息：**
- **作者：** YangYang
- **主页：** （可选，如有 GitHub 仓库可填写）
- **邮箱：** （你的联系邮箱）
- **许可证：** MIT License

#### 步骤 4：上传文件

选择上传方式：

**A. ZIP 文件上传**
- 点击"上传文件"
- 选择：`/Users/yangyang713/.workbuddy/skills/doubao-image-v2.0.0.zip`
- 系统会自动解析

**B. GitHub 仓库关联**（如已推送到 GitHub）
- 选择"从 GitHub 导入"
- 输入仓库地址：`https://github.com/your-username/doubao-image-skill`
- 选择分支：`main` 或 `master`

#### 步骤 5：配置运行环境

**环境变量要求：**
```
ARK_API_KEY - 火山引擎 ARK API Key（必需）
```

**系统依赖：**
```
- curl 7.0+
- python3 3.8+
- bash 4.0+
```

#### 步骤 6：提交审核

- 勾选"我已阅读并同意 Clawhub 开发者协议"
- 点击"提交审核"按钮
- 等待审核结果（通常 1-3 个工作日）

---

### 方式二：通过 GitHub 仓库发布

#### 步骤 1：推送到 GitHub

```bash
cd /Users/yangyang713/.workbuddy/skills/doubao-image

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "release: v2.0.0 - Initial release for Clawhub"

# 创建标签
git tag -a v2.0.0 -m "Release version 2.0.0"

# 创建 GitHub 仓库并推送
# （先在 GitHub 上创建空仓库）
git remote add origin https://github.com/your-username/doubao-image-skill.git
git push -u origin main
git push origin v2.0.0
```

#### 步骤 2：在 Clawhub 关联

1. 访问 https://clawhub.cn/marketplace/publish
2. 选择"从 GitHub 导入"
3. 授权 Clawhub 访问 GitHub
4. 选择 `doubao-image-skill` 仓库
5. 选择分支和版本标签
6. 填写技能信息（参考方式一）
7. 提交审核

---

### 方式三：命令行发布（如支持）

如果 Clawhub 提供 CLI 工具：

```bash
# 安装 Clawhub CLI（示例）
npm install -g @clawhub/cli

# 登录
clawhub login

# 发布
cd /Users/yangyang713/.workbuddy/skills/doubao-image
clawhub publish --version 2.0.0
```

*注：具体命令请参考 Clawhub 官方文档*

---

## 📋 发布前检查清单

### ✅ 必需项

- [x] SKILL.md 文件存在且格式正确
- [x] README.md 包含完整使用说明
- [x] 脚本文件可执行（已设置 chmod +x）
- [x] 无硬编码的 API Key 或敏感信息
- [x] 环境变量说明清晰
- [x] 错误处理完善

### ✅ 推荐项

- [x] CHANGELOG.md 版本历史
- [x] LICENSE 开源协议
- [x] 示例代码和 Prompt
- [x] 环境检查脚本
- [x] .gitignore 配置

### ⚠️ 注意事项

1. **API Key 安全**
   - ❌ 不要在任何文件中硬编码 API Key
   - ✅ 使用环境变量读取
   - ✅ 在文档中说明获取方式

2. **版权合规**
   - ✅ 使用 MIT 等兼容协议
   - ✅ 注明使用的第三方 API（火山引擎 ARK）
   - ✅ 遵守平台使用规范

3. **内容规范**
   - ✅ 不包含违法不良信息
   - ✅ 不侵犯他人权益
   - ✅ 符合 Clawhub 社区准则

---

## 🔍 审核流程

### 时间线

```
提交 → 初审（1 天）→ 技术审核（1-2 天）→ 上架（1 天）
```

**总计：** 1-3 个工作日

### 审核内容

1. **安全性检查**
   - 无恶意代码
   - 无敏感信息泄露
   - API 调用合规

2. **功能检查**
   - 基本功能可用
   - 错误处理正常
   - 文档准确

3. **质量检查**
   - 代码规范
   - 文档完整
   - 用户体验

### 审核结果

**通过：**
- 收到邮件通知
- 技能上架到市场
- 用户可搜索安装

**不通过：**
- 收到驳回原因邮件
- 根据反馈修改
- 重新提交审核

---

## 📊 发布后运营

### 监控指标

1. **下载量**
   - 每日/周/月下载统计
   - 累计下载量

2. **用户评价**
   - 星级评分
   - 用户评论

3. **问题反馈**
   - GitHub Issues
   - Clawhub 问题区

### 维护承诺

- **问题响应：** 48 小时内
- **Bug 修复：** 严重 Bug 一周内
- **版本更新：** 至少每季度一次

### 更新流程

```bash
# 修改代码和文档
# ...

# 更新版本号（SKILL.md 和脚本）
# 修改 CHANGELOG.md

# 提交新版本
git commit -m "release: v2.1.0 - New features"
git tag -a v2.1.0 -m "Release version 2.1.0"
git push origin main
git push origin v2.1.0

# 在 Clawhub 后台提交新版本
```

---

## 🆘 常见问题

### Q1: 审核被驳回怎么办？

**A:** 
1. 仔细阅读驳回原因邮件
2. 根据反馈逐条修改
3. 在回复中说明修改内容
4. 重新提交审核

### Q2: 如何修改已发布的技能？

**A:**
1. 在 Clawhub 开发者后台找到技能
2. 点击"更新版本"
3. 上传新版本或更新 GitHub 仓库
4. 填写更新说明
5. 提交审核

### Q3: 技能可以下架吗？

**A:** 
可以。在开发者后台选择"下架技能"，已安装的用户仍可使用，但新用户无法安装。

### Q4: 如何获得收益？

**A:** 
查看 Clawhub 的创作者激励计划，可能包括：
- 付费技能销售
- 打赏功能
- 流量分成
- 商业合作

具体政策请咨询 Clawhub 官方。

---

## 📞 联系方式

### Clawhub 官方

- **官网：** https://clawhub.cn
- **邮箱：** support@clawhub.cn（示例）
- **开发者文档：** https://clawhub.cn/docs

### 技术支持

如遇到发布问题：
1. 查看官方文档
2. 在开发者社区提问
3. 联系官方客服

---

## 🎉 发布成功后的下一步

### 1. 宣传推广

- 在社交媒体分享
- 写技术博客介绍
- 在相关社区推广
- 邀请朋友试用

### 2. 收集反馈

- 关注用户评价
- 回复用户问题
- 收集改进建议

### 3. 持续迭代

- 定期更新版本
- 添加新功能
- 优化用户体验

### 4. 数据分析

- 查看下载趋势
- 分析用户地域
- 了解使用场景

---

## 📝 发布清单

### 发布前

- [x] 完成代码优化
- [x] 编写完整文档
- [x] 创建发布包
- [x] 检查安全性
- [ ] 测试基本功能
- [ ] 准备宣传材料

### 发布中

- [ ] 填写技能信息
- [ ] 上传文件
- [ ] 配置环境变量
- [ ] 提交审核

### 发布后

- [ ] 等待审核通过
- [ ] 技能上架
- [ ] 宣传推广
- [ ] 收集反馈
- [ ] 规划下一版本

---

**祝发布顺利！** 🎉

如有问题，随时联系。

**最后更新：** 2026-04-10  
**版本：** 2.0.0
