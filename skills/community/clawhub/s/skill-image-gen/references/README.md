# References 目录说明

本目录包含 free-image-gen 技能的参考文件和示例配置。

## 📁 目录内容

### config.example.json
配置文件示例模板,包含所有可配置项的示例值。

**⚠️ 注意**: 这个文件只是示例模板,不会被技能自动加载。

## 🔧 配置文件查找路径

技能会按以下优先级自动查找配置文件:

1. **环境变量** (最高优先级)
   ```bash
   export FREE_IMAGE_GEN_CONFIG=/path/to/your/config.json
   ```

2. **当前工作目录**
   - `./skills/free-image-gen/config.json`
   - `./.free-image-gen/config.json`

3. **全局技能配置** (推荐)
   ```
   ~/.openclaw/skills/free-image-gen/config.json
   ```
   这是推荐的配置文件位置,统一管理所有技能配置。

4. **全局配置** (向后兼容)
   ```
   ~/.openclaw/free-image-gen/config.json
   ```

5. **技能所在目录**
   ```
   <技能目录>/config.json
   ```

## 📝 如何配置

### 方法一: 复制示例文件到推荐位置

```bash
# 复制示例文件到全局配置目录
cp references/config.example.json ~/.openclaw/skills/free-image-gen/config.json

# 编辑配置文件
nano ~/.openclaw/skills/free-image-gen/config.json
```

### 方法二: 直接创建配置文件

```bash
# 创建配置目录
mkdir -p ~/.openclaw/skills/free-image-gen

# 创建配置文件
cat > ~/.openclaw/skills/free-image-gen/config.json << 'EOF'
{
  "gitee": {
    "api_key": "your_gitee_api_key_here",
    "model": "Kolors"
  },
  "cos": {
    "enabled": false
  },
  "output": {
    "path": "./output",
    "format": "png"
  }
}
EOF
```

## ⚙️ 重要提示

1. **不要在 `references/` 目录下创建 `config.json`** - 这个目录只放示例文件
2. **推荐使用全局配置目录** - `~/.openclaw/skills/free-image-gen/config.json`
3. **配置文件包含敏感信息** - 请确保不要提交到 git 仓库

## 🔗 相关文档

- [SKILL.md](../SKILL.md) - 完整的技能文档
- [config.example.json](./config.example.json) - 配置文件示例
