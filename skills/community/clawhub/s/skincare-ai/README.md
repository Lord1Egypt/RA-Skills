# 🧴 护肤AI技能 (Skincare AI Skill)

基于AISkinHealth0827项目的完整护肤分析系统，为OpenClaw提供专业的AI护肤解决方案。

## 🎯 特性

### 核心功能
- **7参数皮肤分析** - 水分、油分、弹性、毛孔、泛红、色素、皱纹
- **个性化产品推荐** - 100+产品数据库，智能匹配算法
- **AI护肤咨询** - 自然语言对话，专业护肤建议
- **多模式分析** - 基础、高级分析模式

### 安全特性 (v1.0.4重要更新)
- ✅ **100%本地运行** - 无网络访问，所有处理在本地完成
- ✅ **路径访问控制** - 文件访问限制在技能目录内
- ✅ **隐私保护** - 不收集、不上传用户数据
- ✅ **输入验证** - 严格验证所有输入，防止恶意输入
- ✅ **ClawHub安全认证** - 通过安全扫描，文档代码一致

### 技术优势
- **模块化架构** - 核心插件，易于扩展
- **完整API层** - RESTful端点
- **多格式输出** - JSON/Text/Markdown支持
- **智能降级** - 原始API不可用时自动切换
- **安全防护** - 多层安全验证和防护

### 用户体验
- **命令行工具** - 丰富的命令和选项
- **一键安装** - 自动安装和配置
- **详细文档** - 完整的用户指南
- **跨平台** - 支持Windows、Linux、macOS

## 🚀 快速开始

### 安装
```bash
# 自动安装（推荐）
openclaw skill install skincare-ai

# 或手动安装
git clone https://github.com/your-repo/skincare-ai.git
cd skincare-ai
openclaw skill load .
```

### 基本使用
```bash
# 查看帮助
/skincare help

# 皮肤分析（使用本地文件）
/skincare analyze /path/to/skin.jpg

# 产品推荐
/skincare recommend --type 干性 --budget mid

# AI咨询
/skincare chat "我的皮肤很干怎么办？"

# 查看版本
/skincare version
```

## 🔒 安全使用说明

### 重要安全原则
1. **本地文件优先**: 只使用本地图像文件，不要使用URL
2. **路径限制**: 文件应放在技能目录或子目录中
3. **文件类型**: 仅支持.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp
4. **文件大小**: 单个文件不超过50MB

### 安全配置
```yaml
# config.yaml 安全配置
security:
  network_access: false      # 无网络访问
  local_only: true           # 100%本地运行
  path_restriction:
    enabled: true            # 启用路径限制
    allowed_dirs:            # 允许的目录
      - "."
      - "./data"
      - "./models"
```

## 📖 详细功能

### 皮肤分析
```bash
# 基本分析
/skincare analyze image.jpg

# 高级分析
/skincare analyze image.jpg --mode advanced

# 输出JSON格式
/skincare analyze image.jpg --format json
```

**分析参数**:
- 水分 (Moisture)
- 油分 (Oil)
- 弹性 (Elasticity)
- 毛孔 (Pores)
- 泛红 (Redness)
- 色素 (Pigmentation)
- 皱纹 (Wrinkles)

### 产品推荐
```bash
# 基于皮肤类型
/skincare recommend --skin-type 干性

# 指定预算
/skincare recommend --skin-type 油性 --budget high

# 指定关注问题
/skincare recommend --skin-type 混合性 --concerns 毛孔,泛红
```

**产品类别**:
- 洁面 (Cleanser)
- 爽肤水 (Toner)
- 精华 (Serum)
- 保湿 (Moisturizer)
- 防晒 (Sunscreen)
- 面膜 (Mask)

### AI护肤咨询
```bash
# 简单咨询
/skincare chat "我的皮肤很干怎么办？"

# 详细咨询
/skincare chat "我是油性皮肤，有毛孔粗大问题，请给我护肤建议"

# 查看历史
/skincare chat --history

# 清除历史
/skincare chat --clear
```

## ⚙️ 配置

### 配置文件
```
技能目录/config.yaml
```

### 主要配置项
```yaml
# 安全配置
security:
  network_access: false
  local_only: true
  path_restriction:
    enabled: true
    allowed_dirs:
      - "."
      - "./data"
    max_file_size_mb: 50

# 插件配置
plugins:
  skin_analyzer:
    enabled: true
    mode: "advanced"
  
  recommendation_engine:
    enabled: true
    max_recommendations: 5

# 输出配置
output:
  default_format: "text"
  include_timestamp: true
```

## 🐛 故障排除

### 常见问题

#### 1. 技能无法加载
```bash
# 检查技能列表
openclaw skill list

# 重新加载技能
openclaw skill reload skincare-ai

# 查看错误日志
openclaw logs --tail 50
```

#### 2. 文件路径被拒绝
```
错误: "文件路径不在允许的目录内"
解决方案:
1. 将文件移动到技能目录内
2. 修改配置添加允许目录
3. 使用相对路径
```

#### 3. 文件类型不支持
```
错误: "不支持的文件类型"
解决方案:
1. 转换为支持的格式 (jpg, png等)
2. 检查文件扩展名
```

#### 4. 文件过大
```
错误: "文件过大"
解决方案:
1. 压缩图像文件
2. 调整配置中的max_file_size_mb
```

### 错误代码
| 代码 | 含义 | 解决方法 |
|------|------|----------|
| ERR-101 | 路径不在允许目录内 | 移动文件或修改配置 |
| ERR-102 | 文件类型不支持 | 转换文件格式 |
| ERR-103 | 文件过大 | 压缩文件或调整配置 |
| ERR-104 | URL不被允许 | 使用本地文件 |
| ERR-105 | 文件不存在 | 检查文件路径 |

## 📊 性能

### 系统要求
- **Python**: 3.8+
- **OpenClaw**: 2026.3+
- **内存**: 512MB+
- **磁盘**: 100MB+

### 性能指标
- **图像分析**: 2-5秒
- **产品推荐**: <1秒
- **AI咨询**: 1-3秒
- **内存使用**: <200MB

## 🔄 更新

### 当前版本
- **版本**: 1.0.3
- **发布日期**: 2026-03-24
- **更新类型**: 安全修复

### 更新内容
- ✅ 实施严格的路径访问限制
- ✅ 更新文档与代码一致性
- ✅ 增强输入验证和错误处理
- ✅ 通过ClawHub安全扫描

### 升级指南
```bash
# 从旧版本升级
openclaw skill update skincare-ai

# 验证升级
/skincare version
/skincare test all
```

## 📚 文档

### 核心文档
- [SKILL.md](SKILL.md) - 详细技能文档
- [CHANGELOG.md](CHANGELOG.md) - 更新日志
- [RELEASE_NOTES.md](RELEASE_NOTES.md) - 发布说明

### 在线资源
- **官方文档**: https://docs.openclaw.ai/skills/skincare-ai
- **GitHub**: https://github.com/openclaw/skincare-ai
- **Discord**: https://discord.gg/clawd

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议：

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

### 开发指南
```bash
# 克隆项目
git clone https://github.com/openclaw/skincare-ai.git

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
python -m pytest tests/

# 代码检查
python -m flake8 .
python -m mypy .
```

## 📄 许可证

MIT License

版权所有 (c) 2026 OpenClaw助手

---

**安全第一，质量为本**  
**版本**: 1.0.3  
**状态**: ✅ 生产就绪，安全修复完成  
**最后更新**: 2026-03-24
