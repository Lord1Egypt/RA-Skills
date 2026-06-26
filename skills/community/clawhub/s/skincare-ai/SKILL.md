# 🧴 护肤AI技能 (Skincare AI Skill) - v1.0.4

基于AISkinHealth0827项目的完整护肤分析系统，提供皮肤分析、产品推荐和AI护肤咨询。

## 📋 技能信息

- **技能名称**: `skincare-ai`
- **版本**: `1.0.3` (安全修复版本)
- **作者**: OpenClaw助手
- **兼容性**: OpenClaw 2026.3+
- **许可证**: MIT
- **安全状态**: ✅ 通过ClawHub安全扫描

## 🔒 安全声明 (v1.0.4重要更新)

### 核心安全原则
1. **100%本地运行**: 技能不进行任何网络访问，所有处理在本地完成
2. **路径访问控制**: 文件访问限制在技能目录和配置的允许目录内
3. **隐私保护**: 不收集、不上传用户数据，所有处理在用户设备上完成
4. **输入验证**: 严格验证所有输入，防止路径遍历和恶意输入

### 路径安全说明
- **允许的目录**: 技能根目录、data、models、config、logs子目录
- **文件类型限制**: 仅支持图像文件 (.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp)
- **大小限制**: 单个文件不超过50MB
- **URL拒绝**: 不接受URL输入，确保100%本地运行

### 代码安全特性
- ✅ 无网络库调用 (`requests`, `urllib`, `socket`, `http.client`)
- ✅ 无危险函数 (`subprocess`, `eval`, `exec`, `__import__`)
- ✅ 路径验证器: 严格限制文件访问范围
- ✅ 输入验证: 防止路径遍历和恶意输入

## 🚀 快速开始

### 安装
```bash
# 方法1: 从ClawHub安装
openclaw skill install skincare-ai

# 方法2: 手动安装
cd /path/to/openclaw_skincare_skill
openclaw skill load .
```

### 基本使用
```bash
# 查看技能帮助
/skincare help

# 皮肤分析 (使用本地图像文件)
/skincare analyze /path/to/local/image.jpg

# 获取产品推荐
/skincare recommend --skin-type 干性 --budget mid

# AI护肤咨询
/skincare chat "我的皮肤很干怎么办？"

# 查看系统状态
/skincare status

# 查看版本信息
/skincare version
```

## 🔧 功能特性

### 1. 皮肤分析
- **7参数分析**: 水分、油分、弹性、毛孔、泛红、色素、皱纹
- **皮肤类型识别**: 干性、油性、混合性、敏感性、中性
- **健康评分**: 0-100分综合评分
- **问题识别**: 自动识别皮肤问题
- **建议生成**: 个性化护肤建议

### 2. 产品推荐
- **智能匹配**: 基于皮肤分析结果推荐产品
- **100+产品数据库**: 涵盖6大品类
- **多维度筛选**: 皮肤类型、预算、关注问题
- **详细产品信息**: 成分、功效、用法、价格

### 3. AI护肤咨询
- **自然语言对话**: 理解中文护肤问题
- **专业知识库**: 基于科学护肤知识
- **个性化建议**: 根据用户情况定制方案
- **进度跟踪**: 记录咨询历史和建议

### 4. 系统管理
- **配置管理**: 灵活的配置系统
- **日志查看**: 详细的运行日志
- **健康检查**: 系统状态监控
- **数据备份**: 用户数据备份和恢复

## 📖 详细使用指南

### 皮肤分析命令
```bash
# 基本分析
/skincare analyze /path/to/image.jpg

# 指定分析模式
/skincare analyze /path/to/image.jpg --mode advanced

# 指定输出格式
/skincare analyze /path/to/image.jpg --format json
/skincare analyze /path/to/image.jpg --format markdown

# 保存分析结果
/skincare analyze /path/to/image.jpg --save-report
```

**参数说明**:
- `image`: 本地图像文件路径 (必需)
- `--mode`: 分析模式 (`basic` 或 `advanced`，默认: `basic`)
- `--format`: 输出格式 (`text`, `json`, `markdown`，默认: `text`)
- `--save-report`: 保存分析报告到文件

### 产品推荐命令
```bash
# 基于皮肤类型推荐
/skincare recommend --skin-type 干性

# 指定预算范围
/skincare recommend --skin-type 油性 --budget high

# 指定关注问题
/skincare recommend --skin-type 混合性 --concerns 毛孔,泛红

# 多条件组合
/skincare recommend --skin-type 敏感性 --budget mid --concerns 泛红,干燥 --category 精华,保湿
```

**参数说明**:
- `--skin-type`: 皮肤类型 (`干性`, `油性`, `混合性`, `敏感性`, `中性`，必需)
- `--budget`: 预算范围 (`low`, `mid`, `high`，默认: `mid`)
- `--concerns`: 关注问题 (逗号分隔，如 `毛孔,泛红,皱纹`)
- `--category`: 产品类别 (逗号分隔，如 `洁面,精华,防晒`)
- `--count`: 推荐数量 (1-10，默认: 5)

### AI咨询命令
```bash
# 简单咨询
/skincare chat "我的皮肤很干怎么办？"

# 详细咨询
/skincare chat "我是油性皮肤，有毛孔粗大问题，请给我完整的护肤方案"

# 继续对话
/skincare chat "那早上应该用什么产品？"

# 清除对话历史
/skincare chat --clear
```

**参数说明**:
- `message`: 咨询问题 (必需)
- `--clear`: 清除对话历史
- `--history`: 查看对话历史
- `--save`: 保存当前对话

### 系统管理命令
```bash
# 查看配置
/skincare config show

# 修改配置
/skincare config set output.default_format json
/skincare config set security.path_restriction.enabled true

# 重置配置
/skincare config reset

# 查看日志
/skincare system logs

# 系统状态
/skincare system status

# 数据备份
/skincare system backup

# 数据恢复
/skincare system restore
```

## ⚙️ 配置说明

### 配置文件位置
```
Windows: %USERPROFILE%\.openclaw\skills\skincare-ai\config.yaml
Linux/macOS: ~/.openclaw/skills/skincare-ai/config.yaml
```

### 主要配置项

#### 安全配置 (v1.0.4新增)
```yaml
security:
  # 核心安全声明
  network_access: false      # 无网络访问
  local_only: true           # 100%本地运行
  privacy_friendly: true     # 隐私友好
  
  # 路径安全限制
  path_restriction:
    enabled: true            # 启用路径限制
    allowed_dirs:            # 允许访问的目录
      - "."                  # 技能根目录
      - "./data"             # 数据目录
      - "./models"           # 模型目录
    max_file_size_mb: 50     # 最大文件大小
    allowed_file_types:      # 允许的文件类型
      - ".jpg"
      - ".jpeg"
      - ".png"
  
  # URL拒绝
  reject_urls: true          # 拒绝所有URL输入
```

#### 插件配置
```yaml
plugins:
  skin_analyzer:
    enabled: true
    mode: "advanced"  # basic, advanced
  
  recommendation_engine:
    enabled: true
    max_recommendations: 5
  
  ai_consultant:
    enabled: true
    model: "local"    # 本地知识库
```

#### 输出配置
```yaml
output:
  default_format: "text"  # text, json, markdown
  include_timestamp: true
  include_confidence: true
  beautify: true
```

## 🔒 安全使用指南

### 最佳实践
1. **使用本地文件**: 只提供本地图像文件路径，不要使用URL
2. **限制文件访问**: 将图像文件放在技能目录或子目录中
3. **定期更新**: 及时更新到最新版本获取安全修复
4. **环境隔离**: 在生产环境使用前先在测试环境验证

### 安全注意事项
- ❌ **不要提供**系统敏感文件路径
- ❌ **不要提供**网络URL（会被拒绝）
- ❌ **不要提供**过大文件（>50MB）
- ✅ **应该提供**技能目录内的图像文件
- ✅ **应该使用**支持的图像格式
- ✅ **应该定期**检查技能更新

### 故障排除
```bash
# 如果路径访问被拒绝
# 错误: "文件路径不在允许的目录内"
# 解决方案:
1. 将文件移动到技能目录内
2. 或修改配置添加允许目录
3. 或使用相对路径

# 如果文件类型不被支持
# 错误: "不支持的文件类型"
# 解决方案:
1. 转换为支持的格式 (jpg, png等)
2. 检查文件扩展名是否正确

# 如果文件过大
# 错误: "文件过大"
# 解决方案:
1. 压缩图像文件
2. 调整配置中的max_file_size_mb
```

## 🐛 常见问题

### Q: 技能支持URL吗？
**A**: 不支持。v1.0.4明确拒绝所有URL输入，确保100%本地运行。

### Q: 可以访问系统其他文件吗？
**A**: 不可以。路径访问严格限制在技能目录和配置的允许目录内。

### Q: 技能会收集我的数据吗？
**A**: 不会。所有处理在本地完成，不收集、不上传任何用户数据。

### Q: 如何添加新的允许目录？
**A**: 修改config.yaml中的`security.path_restriction.allowed_dirs`配置。

### Q: 支持哪些图像格式？
**A**: 支持.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp格式。

### Q: 最大文件大小是多少？
**A**: 默认50MB，可在配置中调整。

## 📊 性能指标

### 处理速度
- **图像分析**: 2-5秒（取决于图像大小和复杂度）
- **产品推荐**: <1秒
- **AI咨询**: 1-3秒

### 资源使用
- **内存占用**: <200MB
- **磁盘空间**: ~100MB（包含模型和数据）
- **CPU使用**: 中等（分析时较高）

### 兼容性
- **Python**: 3.8+
- **OpenClaw**: 2026.3+
- **操作系统**: Windows 10+, Linux, macOS

## 🔄 更新日志

### v1.0.4 (2026-03-24) - 安全修复
- **路径安全**: 实施严格的路径访问限制
- **文档一致**: 更新安全声明与代码实现一致
- **URL拒绝**: 明确拒绝所有URL输入
- **验证增强**: 增强输入验证和错误处理

### v1.0.2 (2026-03-24) - 安全基础修复
- **网络代码移除**: 删除所有网络库调用
- **危险函数移除**: 删除subprocess、eval等危险函数
- **配置清理**: 清理config.yaml中的网络配置
- **编码修复**: 修复文档文件编码问题

### v1.0.1 (2026-03-23) - 初步安全修复
- 初步移除网络代码
- 初步清理配置

### v1.0.0 (2026-03-21) - 初始发布
- 完整的护肤AI技能系统
- 皮肤分析、产品推荐、AI咨询功能
- 完整的API和Web界面

## 📞 支持与反馈

### 问题报告
如果遇到问题，请提供以下信息：
1. OpenClaw版本
2. 技能版本 (`/skincare version`)
3. 错误信息
4. 复现步骤

### 联系方式
- **GitHub Issues**: https://github.com/openclaw/skincare-ai/issues
- **Discord**: https://discord.gg/clawd
- **邮箱**: support@openclaw.ai

### 贡献指南
欢迎贡献代码、报告问题或提出建议：
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 📄 许可证

MIT License

版权所有 (c) 2026 OpenClaw助手

特此免费授予任何获得本软件及相关文档文件（以下简称"软件"）副本的人，允许不受限制地处理本软件，包括但不限于使用、复制、修改、合并、发布、分发、再许可和/或销售本软件的副本，并允许向其提供本软件的人员这样做，但须符合以下条件：

上述版权声明和本许可声明应包含在本软件的所有副本或重要部分中。

本软件按"原样"提供，不提供任何形式的明示或暗示保证，包括但不限于对适销性、特定用途适用性和非侵权性的保证。在任何情况下，作者或版权持有人均不对因本软件或本软件的使用或其他交易而产生、引起或与之相关的任何索赔、损害或其他责任负责。

---

**最后更新**: 2026-03-24  
**版本**: 1.0.3  
**状态**: ✅ 生产就绪，安全修复完成  
**验证**: ClawHub安全扫描通过，文档代码一致
