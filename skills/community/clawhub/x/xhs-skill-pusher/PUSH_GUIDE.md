# 🚀 推送到GitHub指南

## 📋 项目信息

### 基本信息
- **仓库名称**: `xhs-skill-pusher`
- **描述**: 小红书内容发布技能 - 规范化cookie管理 + xhs-kit自动化发布
- **版本**: v1.0.0
- **许可证**: MIT

### 核心特性
1. ✅ **规范化Cookie管理** - 集中存储，规范命名
2. ✅ **自动化发布流程** - 完整验证，错误处理
3. ✅ **简单易用** - 无环境变量，统一接口
4. ✅ **多账号支持** - 一键切换，透明管理

## 📁 项目结构

```
xhs-skill-pusher/
├── bin/xhs-pusher.mjs         # Node.js CLI工具
├── scripts/                   # 发布脚本
├── docs/                      # 完整文档
├── package.json              # Node.js依赖
├── SKILL.md                  # OpenClaw技能文档
└── README.md                 # 项目README
```

## 🛠️ 推送步骤

### 步骤1: 创建GitHub仓库
1. 访问: https://github.com/new
2. 填写信息:
   - **Repository name**: `xhs-skill-pusher`
   - **Description**: `小红书内容发布技能 - 规范化cookie管理 + xhs-kit自动化发布`
   - **Public** (公开) 或 **Private** (私有)
   - 不要初始化README、.gitignore或license

### 步骤2: 设置远程仓库
```bash
cd ~/.openclaw/workspace/xhs-skill-pusher

# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/xhs-skill-pusher.git

# 或使用SSH
git remote add origin git@github.com:YOUR_USERNAME/xhs-skill-pusher.git
```

### 步骤3: 推送到GitHub
```bash
# 推送代码
git push -u origin main

# 或使用推送脚本
./push_to_github.sh
```

### 步骤4: 验证推送
1. 访问: `https://github.com/YOUR_USERNAME/xhs-skill-pusher`
2. 确认所有文件已上传
3. 检查README.md显示正常

## 📦 发布准备

### 1. 更新版本号
如果需要发布新版本，更新:
- `package.json` 中的 `version` 字段
- `SKILL.md` 中的版本信息
- `README.md` 中的版本说明

### 2. 创建发布标签
```bash
# 创建标签
git tag -a v1.0.0 -m "xhs-skill-pusher v1.0.0: 规范化cookie管理 + xhs-kit自动化发布"

# 推送标签
git push origin v1.0.0
```

### 3. 创建GitHub Release
1. 访问仓库的 **Releases** 页面
2. 点击 **Draft a new release**
3. 选择标签 `v1.0.0`
4. 标题: `xhs-skill-pusher v1.0.0`
5. 描述: 复制 `CHANGELOG.md` 内容（如有）
6. 发布!

## 🔧 后续维护

### 更新代码
```bash
# 拉取最新代码
git pull origin main

# 提交更改
git add .
git commit -m "feat: 描述更改内容"

# 推送更改
git push origin main
```

### 处理合并冲突
```bash
# 拉取并合并
git pull --rebase origin main

# 解决冲突后
git add .
git rebase --continue
git push origin main
```

### 分支管理
```bash
# 创建功能分支
git checkout -b feature/new-feature

# 开发完成后
git add .
git commit -m "feat: 新功能"
git push origin feature/new-feature

# 创建Pull Request
```

## 📄 文档说明

### 主要文档
1. **README.md** - 项目概览和快速开始
2. **SKILL.md** - OpenClaw技能详细文档
3. **docs/QUICK_START.md** - 快速开始指南
4. **docs/XHS_FINAL_SOLUTION.md** - 完整解决方案

### 用户指南
- **安装**: 依赖安装和环境配置
- **使用**: 基本命令和示例
- **管理**: Cookie管理和多账号切换
- **故障排除**: 常见问题和解决方案

## 🎯 项目亮点

### 技术亮点
1. **无环境变量设计** - 完全基于文件路径，避免配置混乱
2. **自动化格式转换** - 支持原始cookie字符串自动转换
3. **完整错误处理** - 清晰的错误提示和恢复建议
4. **多账号透明管理** - 基于文件系统的账号切换

### 用户体验
1. **简单命令** - `--list-cookies`查看，`--cookie`使用
2. **完整验证** - 状态检查 → debug验证 → 实际发布
3. **详细日志** - 彩色输出，步骤清晰
4. **灵活配置** - 支持定时发布、多图片、多标签

## 🤝 贡献指南

### 报告问题
1. 使用GitHub Issues报告bug
2. 提供复现步骤和环境信息
3. 附上相关日志和截图

### 提交代码
1. Fork仓库
2. 创建功能分支
3. 编写测试
4. 提交Pull Request

### 代码规范
- 使用一致的代码风格
- 添加必要的注释
- 更新相关文档
- 确保向后兼容

## 📞 支持

### 文档资源
- 项目文档: `docs/` 目录
- 在线文档: GitHub Pages（可选）
- 示例代码: `examples/` 目录（可选添加）

### 社区支持
- GitHub Issues: 问题反馈
- GitHub Discussions: 讨论交流
- Pull Requests: 代码贡献

---

**项目已准备就绪，可以推送到GitHub！** 🚀