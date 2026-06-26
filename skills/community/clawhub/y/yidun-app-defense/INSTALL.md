# 易盾应用加固 - 安装指南

## 系统要求

在安装之前，请确保您的系统满足以下要求：

### 必需软件
- **Java Runtime Environment (JRE)**: 8 或更高版本（推荐 JRE 11+）
- **curl 或 wget**: 用于下载加固工具
- **操作系统**: macOS 10.14+ / Ubuntu 18.04+ / Debian 10+ / CentOS 7+

### 检查 Java 版本
```bash
java -version
```

如果未安装 Java，请参考下方的安装说明。

---

## 安装方式

### 方式一：从 ClawHub 安装（推荐）

1. 访问 ClawHub 技能市场：
   ```
   https://clawhub.ai/skills/yidun-app-defense
   ```

2. 点击"安装"按钮，Skill 将自动安装到本地

3. 安装完成后，进入 Skill 目录：
   ```bash
   cd ~/.openclaw/skills/yidun-app-defense
   ```

4. 运行初始化脚本：
   ```bash
   ./scripts/setup.sh
   ```

### 方式二：手动安装（从压缩包）

1. **下载压缩包**
   ```bash
   # 从 ClawHub 或 GitHub 下载
   curl -L -o yidun-app-defense-1.0.1.tar.gz \
     https://clawhub.ai/skills/yidun-app-defense/download
   ```

2. **解压到目标目录**
   ```bash
   mkdir -p ~/.openclaw/skills/
   tar -xzf yidun-app-defense-1.0.1.tar.gz -C ~/.openclaw/skills/
   cd ~/.openclaw/skills/yidun-app-defense
   ```

3. **验证文件完整性**
   ```bash
   ls -la
   # 应该看到: SKILL.md, package.json, scripts/, config/, docs/
   ```

4. **设置脚本执行权限**（如果需要）
   ```bash
   chmod +x scripts/*.sh
   ```

5. **运行初始化**
   ```bash
   ./scripts/setup.sh
   ```

### 方式三：符号链接（开发/测试）

如果您从源代码仓库克隆，可以创建符号链接：

```bash
# 克隆仓库
git clone <repository-url> ~/yidun/YiDunAppDefense

# 创建符号链接
mkdir -p ~/.openclaw/skills/
ln -s ~/yidun/YiDunAppDefense ~/.openclaw/skills/yidun-app-defense

# 进入目录并初始化
cd ~/yidun/YiDunAppDefense
./scripts/setup.sh
```

---

## 初始化配置

### 1. 运行 setup.sh

初始化脚本会自动：
- 检查 Java 环境
- 创建工作目录（`~/.yidun-defense/`）
- 下载易盾加固工具
- 创建配置文件模板

```bash
./scripts/setup.sh
```

**预期输出**：
```
========================================
  易盾应用加固工具 - 环境检查
========================================
✓ Java 环境检查通过 (version: 11.0.12)
✓ curl 命令可用
✓ 工作目录已创建: ~/.yidun-defense/
✓ 正在下载易盾加固工具...
✓ 工具下载完成
✓ 配置文件模板已创建

========================================
  安装成功！
========================================
```

### 2. 获取 AppKey

1. 访问 [易盾控制台](https://dun.163.com/dashboard#/login/)
2. 注册或登录账号
3. 进入"应用加固"服务
4. 创建应用并获取 AppKey
5. 记录您的 AppKey（32位字符串）

### 3. 配置 AppKey

运行配置脚本：

```bash
./scripts/configure.sh
```

按提示输入您的 AppKey。

或者直接传入 AppKey：

```bash
./scripts/configure.sh your_appkey_here
```

**配置成功输出**：
```
✓ AppKey 配置成功！
配置文件: ~/.yidun-defense/config.ini

使用示例：
  ./scripts/defense-smart.sh /path/to/your-file
```

---

## 验证安装

### 测试加固功能

准备一个测试文件（APK/IPA/HAP），然后运行：

```bash
./scripts/defense-smart.sh /path/to/test-file.apk
```

如果一切正常，您应该看到类似输出：
```
检测到 Android APK 文件
平台: Android
正在加固...
✓ 加固完成！
输出文件: /path/to/test-file_protected.apk
```

---

## Java 环境安装

### macOS

使用 Homebrew：
```bash
brew install openjdk@11
```

设置环境变量（添加到 `~/.zshrc` 或 `~/.bash_profile`）：
```bash
export PATH="/usr/local/opt/openjdk@11/bin:$PATH"
```

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install openjdk-11-jre
```

### CentOS / RHEL

```bash
sudo yum install java-11-openjdk
```

### 验证安装

```bash
java -version
# 应该显示 JRE 8+ 版本信息
```

---

## 故障排查

### 问题 1: Java 环境未找到

**错误信息**：
```
错误: 未检测到 Java 环境！
```

**解决方案**：
1. 安装 Java（参考上方的 Java 安装部分）
2. 确认 `java` 命令在 PATH 中：
   ```bash
   which java
   ```

### 问题 2: 工具下载失败

**错误信息**：
```
错误: 下载失败！请检查网络连接
```

**解决方案**：
1. 检查网络连接
2. 手动下载工具：
   ```bash
   mkdir -p ~/.yidun-defense
   cd ~/.yidun-defense
   curl -o yidun-tool.zip \
     "https://clienttool.dun.163.com/api/v1/client/jarTool/download"
   unzip yidun-tool.zip
   # 复制 NHPProtect.jar 和 tool 目录到 ~/.yidun-defense/
   ```

### 问题 3: 权限问题

**错误信息**：
```
Permission denied
```

**解决方案**：
```bash
# 设置脚本执行权限
chmod +x scripts/*.sh

# 确保工作目录可写
chmod 755 ~/.yidun-defense
```

### 问题 4: AppKey 配置失败

**解决方案**：
1. 确认 AppKey 格式正确（通常是32位字符串）
2. 手动编辑配置文件：
   ```bash
   nano ~/.yidun-defense/config.ini
   ```
   在 `[appkey]` 部分设置：
   ```ini
   [appkey]
   key=your_appkey_here
   ```

---

## 卸载

如果需要卸载 Skill：

```bash
# 删除 Skill 目录
rm -rf ~/.openclaw/skills/yidun-app-defense

# 删除工作目录（可选）
rm -rf ~/.yidun-defense
```

---

## 更新

### 从 ClawHub 更新

ClawHub 会自动检查并提示更新。

### 手动更新

```bash
# 下载新版本压缩包
curl -L -o yidun-app-defense-latest.tar.gz \
  https://clawhub.ai/skills/yidun-app-defense/download

# 备份旧版本
mv ~/.openclaw/skills/yidun-app-defense \
   ~/.openclaw/skills/yidun-app-defense.bak

# 解压新版本
tar -xzf yidun-app-defense-latest.tar.gz \
  -C ~/.openclaw/skills/

# 验证更新
cd ~/.openclaw/skills/yidun-app-defense
cat package.json | grep version
```

---

## 技术支持

- **官方文档**: https://support.dun.163.com/
- **控制台**: https://dun.163.com/dashboard
- **ClawHub**: https://clawhub.ai/
- **使用指南**: 参见 [docs/GUIDE.md](docs/GUIDE.md)
- **API 文档**: 参见 [docs/API.md](docs/API.md)

---

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**祝您使用愉快！** 🛡️
