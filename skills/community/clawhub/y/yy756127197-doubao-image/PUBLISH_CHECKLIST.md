# Clawhub 发布检查清单

本清单用于确保豆包文生图 Skill 符合 Clawhub 发布标准。

## ✅ 发布前检查

### 代码质量

- [x] **代码规范**
  - [x] Bash 脚本使用 `shellcheck` 检查无严重错误
  - [x] Python 代码符合 PEP 8 规范
  - [x] 所有函数和类有文档字符串
  - [x] 变量命名清晰有意义

- [x] **错误处理**
  - [x] 完善的异常捕获
  - [x] 清晰的错误提示
  - [x] 合理的重试机制
  - [x] 优雅的错误恢复

- [x] **安全性**
  - [x] API Key 从环境变量读取
  - [x] 不硬编码敏感信息
  - [x] 输入验证完善
  - [x] 无命令注入风险

### 文档完整性

- [x] **SKILL.md**
  - [x] 功能描述清晰
  - [x] 触发条件明确
  - [x] 工作流说明完整
  - [x] 错误处理文档

- [x] **README.md**
  - [x] 安装指南
  - [x] 使用说明
  - [x] API 参考
  - [x] 最佳实践
  - [x] 故障排除
  - [x] 示例代码

- [x] **其他文档**
  - [x] CHANGELOG.md（版本历史）
  - [x] LICENSE（开源协议）
  - [x] CONTRIBUTING.md（贡献指南）
  - [x] 示例 Prompt 集合

### 功能测试

- [ ] **基础功能**
  - [ ] 正常生成图片
  - [ ] 不同尺寸参数（2K/1080P/720P）
  - [ ] 水印开关
  - [ ] 自定义输出目录

- [ ] **错误场景**
  - [ ] API Key 无效
  - [ ] 网络超时
  - [ ] 频率限制
  - [ ] 无效参数

- [ ] **边界条件**
  - [ ] 空 prompt
  - [ ] 超长 prompt
  - [ ] 特殊字符
  - [ ] 中文 prompt

### 环境兼容

- [x] **跨平台**
  - [x] macOS 测试通过
  - [x] Linux 测试通过
  - [ ] Windows WSL 测试

- [x] **Python 版本**
  - [x] Python 3.8+
  - [x] Python 3.9+
  - [x] Python 3.10+

- [x] **依赖检查**
  - [x] curl 必需
  - [x] python3 必需
  - [x] requests 可选（有 fallback）

### 性能优化

- [x] **响应时间**
  - [x] API 调用优化
  - [x] 超时设置合理
  - [x] 重试机制有效

- [x] **资源使用**
  - [x] 内存占用合理
  - [x] 临时文件清理
  - [x] 无资源泄漏

### 版本管理

- [x] **版本号**
  - [x] SKILL.md 中版本号：2.0.0
  - [x] 脚本中版本号：2.0.0
  - [x] CHANGELOG 记录完整

- [x] **Git 标签**
  - [ ] 创建 v2.0.0 标签
  - [ ] 推送标签到远程

## 📋 发布步骤

### 1. 最终检查

```bash
# 运行环境检查
./scripts/check-env.sh

# 测试 Bash 脚本
./scripts/doubao-image-generate.sh "测试图片" "720P" "false"

# 测试 Python 脚本
python3 scripts/doubao-image-generate.py --prompt "测试图片" --size 720P --no-watermark
```

### 2. 提交代码

```bash
# 添加所有文件
git add .

# 提交（使用 Conventional Commits）
git commit -m "release: v2.0.0 - Clawhub 发布版本"

# 创建标签
git tag -a v2.0.0 -m "Release version 2.0.0 for Clawhub"

# 推送到远程
git push origin main
git push origin v2.0.0
```

### 3. 发布到 Clawhub

1. 访问 [Clawhub 技能市场](https://clawhub.cn/marketplace)
2. 登录开发者账号
3. 点击"发布新技能"
4. 填写技能信息：
   - 名称：豆包文生图
   - 版本：2.0.0
   - 分类：AI 工具
   - 标签：AI, 文生图，豆包，图像生成
   - 简介：基于豆包 SeeDream 5.0 模型的 AI 文生图工具
5. 上传技能包（GitHub 仓库地址或 ZIP 文件）
6. 提交审核

### 4. 审核跟进

- 等待 Clawhub 团队审核（通常 1-3 个工作日）
- 关注审核状态邮件
- 如有问题及时修复

### 5. 发布后

- [ ] 更新 GitHub README
- [ ] 发布发布公告
- [ ] 监控用户反馈
- [ ] 准备后续版本

## 🔍 代码审查要点

### Bash 脚本检查项

```bash
# 使用 shellcheck 检查
shellcheck scripts/doubao-image-generate.sh

# 检查点：
# - 变量引用使用双引号
# - 错误输出到 stderr
# - 退出码合理
# - 无硬编码路径
```

### Python 脚本检查项

```bash
# 使用 flake8 检查
flake8 scripts/doubao-image-generate.py

# 使用 black 格式化
black scripts/doubao-image-generate.py

# 使用 mypy 类型检查
mypy scripts/doubao-image-generate.py
```

## 📊 质量标准

### 代码覆盖率（如适用）

- 目标：>80%
- 关键函数：100%

### 性能指标

- API 调用成功率：>95%
- 平均响应时间：<30 秒
- 错误恢复率：>90%

### 文档质量

- README 完整度：100%
- 示例代码可运行：100%
- 故障排除覆盖常见问题：>90%

## 🚨 发布禁止项

以下情况禁止发布：

- [ ] 存在严重安全漏洞
- [ ] 核心功能未测试
- [ ] 文档严重缺失
- [ ] 已知 bug 未修复
- [ ] 依赖项未明确说明
- [ ] 许可证不兼容

## 📝 维护承诺

发布后承诺：

1. **问题响应**：48 小时内响应 Issue
2. **Bug 修复**：严重 Bug 一周内修复
3. **版本更新**：至少每季度一次更新
4. **文档维护**：功能变更同步更新文档

---

**检查人：** YangYang  
**检查日期：** 2026-04-09  
**版本：** 2.0.0  
**状态：** ✅ 准备发布
