# rm-safety | rm 安全检查

[![ClawHub](https://img.shields.io/badge/ClawHub-rm--safety-blue)](https://clawhub.ai/caesaryp/rm-safety)
[![License](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)
[![Security](https://img.shields.io/badge/security-benign-success)](https://clawhub.ai/caesaryp/rm-safety)

**Intercepts risky `rm` commands to assess impact, confirm user intent, and suggest safer alternatives before execution to prevent accidental data loss.**

**拦截高危 `rm` 命令，评估影响并确认用户意图，提供安全替代方案，防止误删数据。**

---

## 🌟 Features | 功能特性

- ✅ **Pre-execution Safety Check** | **执行前安全检查**
  - Intercepts `rm`, `rm -rf`, `unlink`, `shred` commands
  - 拦截危险删除命令
- ✅ **Impact Assessment** | **影响评估**
  - Counts files and directories before deletion
  - 删除前统计文件和目录数量
- ✅ **Safer Alternatives** | **安全替代方案**
  - Suggests `trash`, backup, or temp move options
  - 推荐更安全的替代方案
- ✅ **Bilingual Support** | **双语支持**
  - English & Chinese documentation
  - 中英文文档支持
- ✅ **Security Hardened** | **安全加固**
  - Path quoting, option separators, injection prevention
  - 路径引用、选项分隔符、防止注入

---

## 📦 Installation | 安装

### Via ClawHub CLI (Recommended | 推荐)

```bash
npx clawhub@latest install rm-safety
```

### Manual Install | 手动安装

```bash
# Clone this repository | 克隆仓库
git clone https://github.com/CaesarYP/rm-safety.git

# Copy to your OpenClaw skills directory | 复制到 OpenClaw skills 目录
cp -r rm-safety ~/.openclaw/workspace/skills/
```

---

## 🚀 Usage | 使用方法

Once installed, rm-safety automatically activates when you attempt to delete files:

安装后，当你尝试删除文件时会自动激活：

### Example 1 | 示例 1: Simple Delete

```bash
rm file.txt
```

**Output | 输出:**
```
🚨 High-Risk Command Confirmation | 高危命令确认

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Command Details | 命令详情
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Command | 命令：rm file.txt
Working Directory | 执行位置：/Users/caesar/project
Target Path | 目标路径：/Users/caesar/project/file.txt

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Impact Assessment | 影响评估
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Will delete 1 file | 将删除 1 个文件
[ ] Location: Inside workspace
[ ] Recoverable via trash: No

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Alternatives | 替代方案
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Use trash command → Recoverable in Finder
2. Backup before delete → cp file.txt file.txt.bak
3. Move to temp directory → mv file.txt /tmp/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❓ Please Confirm | 请确认
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply [y] to execute
Reply [n] to cancel
Reply [backup] to backup first
Reply [trash] to use trash instead
```

### Example 2 | 示例 2: Directory Delete

```bash
rm -rf ./build
```

**Output | 输出:**
```
🚨 High-Risk Command Confirmation | 高危命令确认

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Impact Assessment | 影响评估
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Will delete 156 files
[ ] Will delete 23 directories (179 total items)
[ ] Location: Inside workspace
[ ] Recoverable via trash: No
```

---

## 🛡️ Security Features | 安全特性

### Path Protection | 路径保护

```bash
# ✅ Safe: Quoted paths, option separator
ls -la -- "$path"
find -- "$path" -type f 2>/dev/null

# ❌ Unsafe: Unquoted, no separator
ls -la $path        # Space injection risk
find $path -type f  # Option parsing risk
```

### Dangerous Command Blocking | 危险命令拦截

The skill will **directly refuse** these commands:

以下命令会被**直接拒绝**：

- `rm -rf /` - System destruction | 系统毁灭
- `rm -rf ~` - Home directory destruction | 家目录毁灭
- `rm -rf /home/*` - User data destruction | 用户数据毁灭
- Paths with unescaped special characters | 包含未转义特殊字符的路径

---

## 📋 Configuration | 配置

### Exceptions | 例外情况

**No confirmation needed | 无需确认:**
- Temp files in `/tmp/` (verified by `ls -la`)
- `/tmp/` 下的临时文件（已验证）
- Explicit user permission in same session
- 同一会话内的明确书面许可

**Always requires confirmation | 始终需要确认:**
- Workspace directory deletion
- workspace 目录删除
- User home directory
- 用户主目录

---

## 🧪 Testing | 测试

### Test Cases | 测试用例

```bash
# Should trigger confirmation | 应该触发确认
rm file.txt
rm -rf ./folder
rm -r /path/to/something
unlink file
shred secret.txt

# Should NOT trigger | 不应触发
trash file.txt
mv file.txt ~/.Trash/
```

---

## 📖 Documentation | 文档

- **[SKILL.md](SKILL.md)** - Complete skill specification | 完整技能规范
- **[ClawHub Page](https://clawhub.ai/caesaryp/rm-safety)** - Installation & reviews | 安装与评价
- **[OpenClaw Docs](https://docs.openclaw.ai)** - Platform documentation | 平台文档

---

## 🤝 Contributing | 贡献

Contributions welcome! Please:

欢迎贡献！请：

1. Fork the repository |  Fork 仓库
2. Create a feature branch | 创建功能分支
3. Make your changes | 进行修改
4. Submit a pull request | 提交 PR

---

## 📄 License | 许可证

**MIT-0** - Free to use, modify, and redistribute. No attribution required.

**MIT-0** - 自由使用、修改和分发，无需署名。

See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments | 致谢

- [OpenClaw](https://openclaw.ai) - Agent platform | 智能体平台
- [ClawHub](https://clawhub.ai) - Skill registry | 技能注册中心

---

## 📬 Contact | 联系

- **Author:** Caesar (@CaesarYP)
- **Issues:** [GitHub Issues](https://github.com/CaesarYP/rm-safety/issues)
- **Discord:** [OpenClaw Community](https://discord.com/invite/clawd)

---

<div align="center">

**Made with ❤️ for safer file operations**

**为更安全的文件操作而生**

[⬆ Back to Top](#rm-safety--rm-安全检查)

</div>
