# 文叔叔文件上传 (wenshushu-file-uploader)

**版本**: 1.0.0  
**作者**: OpenClaw  
**许可证**: MIT  
**最后更新**: 2026-03-16

---

## 📋 技能简介

wenshushu-file-uploader 是一个 OpenClaw 技能，提供快速、便捷的文件上传到文叔叔（wenshushu.cn）的功能。支持自动生成分享链接、取件码，并可通过 QQ 对话直接发送给用户。

**核心价值**:
- 🚀 命令行一键上传，无需打开浏览器
- 🔗 自动生成短链接和4位取件码
- 📦 支持大文件（5GB+）和多线程
- 🔄 断点续传，网络不稳定也不怕
- 🤖 完美集成 OpenClaw 对话场景

---

## ✨ 主要功能

### 1. 文件上传
- ✅ 上传任意类型文件（文档、图片、视频、压缩包等）
- ✅ 自动压缩目录为 tar.gz
- ✅ 支持匿名上传（5GB 空间）和登录上传（40GB 空间）
- ✅ 实时显示上传进度

### 2. 智能取件码
- 🎲 自动随机生成4位数字取件码
- 🔢 支持自定义取件码（4位数字）
- 🔄 可指定取件码或随机生成

### 3. 链接管理
- 🌐 生成公共下载链接（无需登录即可访问）
- ⚙️ 生成个人管理链接（可查看上传记录、删除文件）
- 📋 自动将链接和取件码发送给用户

### 4. 高级特性
- ⚡ 多线程下载支持（1-16线程）
- 📈 断点续传（支持单个文件和大文件）
- 🌍 代理支持（HTTP/HTTPS代理）
- 👥 多用户账户管理（保存多个登录token）
- 📊 上传历史记录

---

## 🛠️ 安装要求

### 系统要求
- **Python**: 3.8+
- **OpenClaw**: 最新版本
- **网络**: 可访问 wenshushu.cn

### 依赖工具
- **uv** (推荐): 现代 Python 包管理器
- **wssf**: 文叔叔官方命令行工具（v5.0.6+）

### 自动安装
首次使用时，技能会自动检查并安装依赖：
```bash
# 如果未安装 uv，会自动安装
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建虚拟环境
uv venv

# 安装 wssf
uv pip install wssf==5.0.6
```

---

## 📖 使用方法

### 方式一：对话触发（推荐）
当用户说"发文件给我"或"上传文件"时，OpenClaw 会自动调用此技能。

**示例对话**:
```
用户: 把架构分析文档发给我
AI: 📤 正在上传: hertzbeat-architecture-analysis.md
    上传成功！
    🔗 下载链接: https://c.wss.ink/f/xxxxx
    🔢 取件码: 7010
```

### 方式二：命令行直接调用
```bash
# 基本上传（随机取件码）
python3 skills/wenshushu-file-uploader/scripts/upload.py /path/to/file

# 自定义取件码
python3 skills/wenshushu-uploader/scripts/upload.py /path/to/file 1234

# 使用已登录账户
python3 skills/wenshushu-uploader/scripts/upload.py /path/to/file --login

# 使用代理
python3 skills/wenshushu-uploader/scripts/upload.py /path/to/file --proxy http://127.0.0.1:7890
```

### 方式三：在 OpenClaw 脚本中调用
```python
# 导入技能模块
from skills.wenshushu_uploader.scripts.upload import upload_file

# 上传文件
result = upload_file(
    filepath="/path/to/file.zip",
    pickup_code="1234",  # 可选，不填则随机生成
    use_login=False,     # 是否使用登录账户
    proxy=None           # 代理地址
)

if result["success"]:
    print(f"下载链接: {result['public_url']}")
    print(f"取件码: {result['pickup_code']}")
    print(f"管理链接: {result['management_url']}")
```

---

## ⚙️ 配置选项

### 环境变量
| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `WSSF_USE_LOGIN` | `false` | 默认使用登录账户上传 |
| `WSSF_RANDOM_KEY` | `true` | 自动随机生成取件码 |
| `WSSF_PROXY` | `null` | 默认代理服务器 |
| `WSSF_THREADS` | `4` | 下载线程数 |

### 登录配置（可选）
如需更大存储空间（40GB）和更长保留时间，可配置登录：

1. 访问 https://www.wenshushu.cn 并登录
2. 打开开发者工具（F12）→ Network 标签
3. 刷新页面，找到请求头中的 `X-TOKEN`
4. 复制 token（以 30 或 31 开头）
5. 保存到 `~/.config/wenshushu/token.txt`

```bash
# 或直接使用 wssf 登录命令
uv run wssf login
```

---

## 📂 文件结构

```
wenshushu-uploader/
├── SKILL.md              # 技能说明文档（本文件）
├── _meta.json            # 技能元数据
├── package.json          # 依赖配置
├── install.sh            # 自动安装脚本
├── scripts/
│   └── upload.py        # 主上传逻辑
├── references/           # 参考文档（可选）
└── .clawhub/            # ClawHub 元数据
```

---

## 🔄 工作流程

```
┌─────────────┐
│  用户请求   │ "发文件给我"
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ 检查文件是否存在     │
│ 检查 wssf 是否安装  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  调用 wssf upload   │
│  (通过 uv 运行)     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  解析返回结果       │
│  - 公共链接         │
│  - 取件码           │
│  - 管理链接         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  格式化为消息       │
│  发送给用户         │
└─────────────────────┘
```

---

## 💬 示例对话

### 例1：基本上传
**User**: "把 HertzBeat 架构分析文档发给我"

**AI**:
```
📤 正在上传: hertzbeat-architecture-analysis.md (10.6 KB)
✅ 上传成功！

📄 文件名: hertzbeat-architecture-analysis.md
📏 大小: 10.6 KB

🔗 下载链接:
  https://c.wss.ink/f/jfgffcbqack

🔢 取件码: 3835

📋 管理链接:
  https://www.wenshushu.cn/t/jfgffCbQD8zbtJCs

请在浏览器中打开下载链接，输入取件码即可下载。
```

### 例2：自定义取件码
**User**: "上传文件，取件码设置为 8888"

**AI**:
```
📤 正在上传: large-file.zip (156.3 MB)
  使用取件码: 8888
✅ 上传成功！

🔗 下载链接: https://c.wss.ink/f/xxxxxx
🔢 取件码: 8888
```

### 例3：批量上传
**User**: "把这三个文件发到文叔叔：a.txt b.pdf c.zip"

**AI**:
```
📤 开始批量上传（3个文件）...

1/3 上传 a.txt ✅
   🔗 https://c.wss.ink/f/aaa
   🔢 1234

2/3 上传 b.pdf ✅
   🔗 https://c.wss.ink/f/bbb
   🔢 5678

3/3 上传 c.zip ✅
   🔗 https://c.wss.ink/f/ccc
   🔢 9012

✅ 全部上传完成！
```

---

## ⚠️ 注意事项

### 1. 文件大小限制
- **匿名用户**: 单文件 ≤ 5GB
- **登录用户**: 单文件 ≤ 40GB
- **建议**: 大文件（>1GB）建议使用登录账户

### 2. 网络与验证
- ⚠️ 首次使用可能遇到滑块验证（需手动完成）
- 🌐 如遇网络问题，可配置代理
- 🔄 上传失败会自动重试3次

### 3. 隐私与安全
- 🔒 上传链接 anyone with link can download
- ⏳ 文件保留时间未明确说明，建议定期清理
- 🔐 敏感文件请先加密再上传
- 🎲 取件码建议随机生成，避免简单序列

### 4. 性能优化
- 📊 大文件上传建议使用登录账户（速度更快）
- 🌐 代理可提升上传速度
- 🔄 断点续传可避免网络中断导致重传

---

## 🐛 故障排除

### 问题1：wssf 安装失败
**症状**: `ModuleNotFoundError: No module named 'wssf'`

**解决**:
```bash
# 手动安装
uv venv
uv pip install wssf==5.0.6
```

### 问题2：上传时遇到滑块验证
**症状**: 上传过程中出现验证码页面

**解决**:
1. 在浏览器中手动访问 wenshushu.cn 并完成验证
2. 或使用已登录账户（通常不需要验证）

### 问题3：文件太大上传失败
**症状**: 上传中断或超时

**解决**:
- 使用登录账户（更大空间和速度）
- 配置代理：`uv run wssf upload file.zip -p http://proxy:port`
- 分卷压缩后分批上传

### 问题4：下载链接无法访问
**症状**: 打开链接显示404或错误

**解决**:
- 确认链接和取件码是否正确
- 检查是否已过有效期（文叔叔未明确说明保留时间）
- 登录管理链接查看文件状态

---

## 📈 版本历史

### v1.0.0 (2026-03-16)
- ✨ 初始版本发布
- ✅ 基本文件上传功能
- ✅ 自动生成链接和取件码
- ✅ 支持随机/自定义取件码
- ✅ uv 虚拟环境依赖管理
- ✅ 完整文档和示例

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**开发指南**:
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License. 详见 [LICENSE](LICENSE) 文件。

---

## 🔗 相关链接

- **文叔叔官网**: https://wenshushu.cn
- **wssf GitHub**: https://github.com/JianMoP/wssf
- **OpenClaw 官网**: https://openclaw.ai
- **技能仓库**: https://github.com/gcdd1993/wenshushu-uploader

---

## 💡 致谢

- 感谢文叔叔团队提供免费的文件分享服务
- 感谢 OpenClaw 社区的支持
- 特别感谢 self-improving-agent-cn 技能的记忆功能

---

**最后更新**: 2026-03-16 15:48 (Asia/Shanghai)  
**维护者**: OpenClaw Assistant