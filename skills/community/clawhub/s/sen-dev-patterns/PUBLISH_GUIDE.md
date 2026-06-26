# Sen-Dev-Patterns 发布指南

## GitHub 发布成功！✓

**仓库地址**: https://github.com/the13ai/sen-dev-patterns

---

## 提交到 ClawHub 市场

### 方式一：通过 GitHub 导入（推荐）

1. 访问 https://clawhub.ai/import
2. 选择 "Import from GitHub"
3. 授权 GitHub 账号
4. 选择仓库 `the13ai/sen-dev-patterns`
5. 填写信息并提交审核

### 方式二：手动导入

1. 访问 https://clawhub.ai/import
2. 选择 "Upload ZIP"
3. 下载仓库ZIP: https://github.com/the13ai/sen-dev-patterns/archive/refs/heads/master.zip
4. 上传并填写信息

---

## 国内分发方案

### Gitee（码云）- 国内可直接访问

```bash
# 方式1: 使用脚本
python publish_gitee.py

# 方式2: 手动
git remote add gitee https://gitee.com/the13ai/sen-dev-patterns.git
git push -u gitee master
```

**Gitee Token 获取**:
1. 访问 https://gitee.com/oauth/applications
2. 创建应用，勾选 `projects` 权限
3. 获取 Access Token
4. 设置: `set GITEE_TOKEN=your_token`

---

## 本地开发

### 目录结构

```
sen-dev-patterns/
├── SKILL.md                    # Skill主文件（含metadata）
├── README.md                   # 市场展示页
├── references/                 # 参考文档库（11个）
│   ├── ui-style-guide.md       # UI样式规范
│   ├── coding-standards.md     # 编程规范
│   ├── algorithm-library.md    # 算法库
│   ├── pitfalls-record.md      # 踩坑记录
│   └── ...
└── scripts/
    └── init_module.py          # 模块初始化
```

### 测试 Skill

在 CodeBuddy IDE 中：
1. 打开 Skill 管理
2. 添加本地 Skill
3. 选择此文件夹

---

## 更新发布

```bash
# 1. 更新代码
git add -A
git commit -m "Update description"

# 2. 推送到GitHub
git push origin master

# 3. 推送到Gitee（如配置了）
git push gitee master

# 4. 在ClawHub市场更新版本
```

---

## 文件说明

| 文件 | 说明 |
|------|------|
| SKILL.md | Skill主文件，CodeBuddy加载此文件 |
| README.md | 市场展示页面 |
| references/ | 参考文档库 |
| publish_gitee.py | Gitee发布脚本 |
| publish_skill.py | GitHub发布脚本 |

---

## 下一步操作

### 1. 提交到 ClawHub 市场

访问以下链接直接导入：
```
https://clawhub.ai/import?repo=the13ai/sen-dev-patterns
```

### 2. 发布到 Gitee（国内访问）

**手动方式（推荐，无需Token）**：
1. 打开 https://gitee.com/new
2. 创建仓库，名称填 `sen-dev-patterns`
3. 运行：
   ```bash
   cd C:\Users\sen\.codebuddy\skills\sen-dev-patterns
   git remote add gitee https://gitee.com/the13ai/sen-dev-patterns.git
   git push -u gitee master
   ```

## 版本历史

- **v1.3.0**: 完善metadata和市场展示，包含11个参考文档
- **v1.2.0**: 添加算法库、踩坑记录
- **v1.1.0**: 完善UI规范、代码模块
- **v1.0.0**: 初始版本
