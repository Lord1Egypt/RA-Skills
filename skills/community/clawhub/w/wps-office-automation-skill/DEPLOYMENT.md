# WPS Office Automation Skill - 部署指南

## 📦 发布准备

### 1. 检查当前配置

确保以下文件已正确配置：

```bash
# 检查关键文件
ls -la skill.yaml requirements.txt setup.py MANIFEST.in
```

### 2. 验证配置完整性

- ✅ **skill.yaml**: 已配置完整的元数据
- ✅ **requirements.txt**: 已锁定依赖版本
- ✅ **setup.py**: 已创建发布配置
- ✅ **MANIFEST.in**: 已定义包包含文件

## 🚀 部署到 ClawHub 平台

### 方法一：使用 ClawHub CLI 工具

```bash
# 1. 安装 ClawHub CLI
pip install clawhub-cli

# 2. 登录到 ClawHub 平台
clawhub login

# 3. 构建 Skill 包
clawhub skill build

# 4. 发布 Skill
clawhub skill publish
```

### 方法二：手动打包发布

```bash
# 1. 创建发布包
python setup.py sdist bdist_wheel

# 2. 检查生成的包
ls -la dist/

# 3. 上传到 PyPI（可选）
twine upload dist/*

# 4. 在 ClawHub 平台手动上传
# 访问 https://clawhub.com/developer/skills
# 点击"新建 Skill"，上传 dist 目录中的包文件
```

### 方法三：GitHub Actions 自动发布

创建 `.github/workflows/release.yml`：

```yaml
name: Release Skill
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: pip install build twine clawhub-cli
    
    - name: Build package
      run: python setup.py sdist bdist_wheel
    
    - name: Publish to ClawHub
      run: |
        clawhub login --token ${{ secrets.CLAWHUB_TOKEN }}
        clawhub skill publish
      env:
        CLAWHUB_TOKEN: ${{ secrets.CLAWHUB_TOKEN }}
```

## 🔧 环境要求

### 运行时环境
- Python 3.9+
- 至少 512MB 内存
- 文件系统访问权限
- 网络访问权限（可选）

### 依赖项检查

```bash
# 检查依赖兼容性
pip check

# 安装依赖
pip install -r requirements.txt

# 验证安装
python -c "from main import execute; print('Skill加载成功')"
```

## 📋 发布检查清单

### 发布前检查
- [ ] skill.yaml 配置完整
- [ ] 依赖版本已锁定
- [ ] 所有功能测试通过
- [ ] 文档已更新
- [ ] 版本号已递增
- [ ] CHANGELOG.md 已更新

### 发布后验证
- [ ] Skill 在 ClawHub 平台可见
- [ ] 所有功能正常可用
- [ ] 错误处理正常
- [ ] 性能符合预期
- [ ] 用户反馈收集机制就绪

## 🐛 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   # 清理缓存重新安装
   pip cache purge
   pip install --no-cache-dir -r requirements.txt
   ```

2. **权限不足**
   - 检查 required_permissions 配置
   - 确保 Skill 有足够的文件系统权限

3. **内存不足**
   - 优化大文件处理
   - 实现流式处理
   - 增加内存限制配置

4. **网络连接问题**
   - 检查网络权限配置
   - 实现离线降级处理

## 🔄 更新流程

### 版本更新
1. 更新 `skill.yaml` 中的版本号
2. 更新 `CHANGELOG.md`
3. 运行测试确保兼容性
4. 构建新版本包
5. 发布到 ClawHub 平台

### 热修复
- 使用补丁版本号（如 1.1.1）
- 优先修复关键问题
- 确保向后兼容

## 📞 技术支持

- **文档**: [README.md](README.md)
- **问题反馈**: GitHub Issues
- **社区支持**: ClawHub 开发者社区
- **紧急联系**: dev@clawhub.com

## 📊 监控和日志

部署后建议配置：
- 错误日志收集
- 使用量统计
- 性能监控
- 用户反馈收集

---

**最后更新**: 2026-03-16  
**版本**: 1.1.0  
**状态**: ✅ 可发布