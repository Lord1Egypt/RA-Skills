# Call AIDA App Skill - 完整文档索引

## 📌 技能信息

**名称:** Call AIDA App
**版本:** 1.0.0
**类型:** OpenClaw 通用技能
**发布日期:** 2026-03-14
**许可证:** MIT

## 📂 文件说明

### 核心文件

| 文件 | 说明 |
|------|------|
| **call_aida_app.py** | 主要脚本，包含所有实现逻辑 |
| **SKILL.md** | 完整的 API 文档和功能说明 |
| **README.zh.md** | 中文快速开始指南 |
| **EXAMPLES.md** | 详细的使用示例 |
| **QUICKSTART.txt** | 快速参考卡 |

### 工具文件

| 文件 | 说明 |
|------|------|
| **install.sh** | 技能安装和验证脚本 |
| **test.sh** | 自动化测试脚本 |
| **INDEX.md** | 本文件，文档索引 |

## 🎯 快速导航

### 根据你的需求选择文档

**我是新手，想快速上手**
→ 阅读 `QUICKSTART.txt`（2分钟）

**我想了解完整功能**
→ 阅读 `SKILL.md`（5分钟）

**我需要实际使用示例**
→ 阅读 `EXAMPLES.md`（10分钟）

**我想快速开始使用**
→ 阅读 `README.zh.md`（3分钟）

**我要在代码中集成**
→ 参考 `EXAMPLES.md` 中的 Python 集成示例

## 🚀 三步快速开始

### 1. 验证安装

```bash
bash ~/.openclaw/skills/call-aida-app/install.sh
```

### 2. 查看帮助

```bash
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py --help
```

### 3. 第一次调用

```bash
echo '{"appid":"your-app-id","inputs":{"test":"value"}}' | \
  python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py
```

## 📖 完整文档阅读顺序

对于初次使用的用户，建议按以下顺序阅读：

1. **QUICKSTART.txt** - 了解基本概念（5分钟）
2. **README.zh.md** - 学习三种调用方式（10分钟）
3. **EXAMPLES.md** - 查看实际示例（15分钟）
4. **SKILL.md** - 深入了解 API 细节（20分钟）

总时间：约 50 分钟即可完全掌握

## 🔍 功能清单

### 核心功能

- ✅ 调用 AI 搭（AIDA）chat-messages 接口
- ✅ 支持自定义输入参数
- ✅ 返回完整的应用响应数据
- ✅ 完整的错误处理

### 调用方式

- ✅ 命令行参数 (`--appid`, `--inputs`)
- ✅ stdin JSON 输入（推荐）
- ✅ 环境变量 (`AIDA_APPID`, `AIDA_INPUTS`)

### 特性

- ✅ Bearer Token 认证
- ✅ 120 秒超时保护
- ✅ JSON 响应解析
- ✅ 详细的错误信息
- ✅ 支持自定义用户标识
- ✅ 无外部依赖（仅使用 Python 标准库）

## 💡 常见使用场景

### 场景 1：从 Shell 脚本调用

```bash
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
  --appid "my-app" \
  --inputs '{"key":"value"}'
```

查看详情 → `README.zh.md` 方式2

### 场景 2：从 OpenClaw Agent 调用

在 Agent 的任务中使用此技能来调用 AIDA 应用

查看详情 → `EXAMPLES.md` "与 OpenClaw Agent 集成"

### 场景 3：Python 代码集成

```python
import json, subprocess
result = subprocess.run([...], capture_output=True)
response = json.loads(result.stdout)
```

查看详情 → `EXAMPLES.md` "Python 集成"

### 场景 4：链式调用多个应用

第一个应用的输出作为第二个应用的输入

查看详情 → `EXAMPLES.md` "链式调用"

### 场景 5：批量处理

对多个输入调用同一个应用

查看详情 → `EXAMPLES.md` "批量处理"

## 🛠️ 故障排除

### 问题速查表

| 问题 | 原因 | 解决方案 |
|------|------|--------|
| HTTP 401 | appid 无效 | 检查 appid 是否正确 |
| 缺少 answer 字段 | API 响应格式异常 | 查看完整的 data 字段 |
| 超时 | 网络或服务问题 | 检查网络连接 |
| JSON 错误 | 输入格式错误 | 验证 inputs 是有效 JSON |

详细排除步骤 → `SKILL.md` "故障排除"

## 🔐 安全特性

- 🔒 使用 HTTPS 连接
- 🔒 Bearer Token 认证
- 🔒 无密钥硬编码
- 🔒 完整的错误日志
- 🔒 超时保护

## 🌍 API 信息

**端点:** `https://aida.vip.sankuai.com/v1/chat-messages`
**认证:** Bearer Token（使用 appid）
**超时:** 120 秒
**响应模式:** Blocking（阻塞）

## 📊 性能指标

- 典型响应时间：1-10 秒（取决于应用）
- 最大超时时间：120 秒
- 支持 JSON body 流式读取

## 🎓 学习资源

### 对于初学者

1. 查看 `QUICKSTART.txt` 了解基础
2. 运行 `test.sh` 验证安装
3. 尝试第一个简单调用

### 对于开发者

1. 查看 `SKILL.md` 了解 API 细节
2. 参考 `EXAMPLES.md` 中的 Python 示例
3. 查看源代码 `call_aida_app.py`

### 对于集成商

1. 参考 `EXAMPLES.md` "与 OpenClaw Agent 集成"
2. 使用 stdin 方式获得最大灵活性
3. 实现完整的错误处理

## 🤝 支持

### 获取帮助

1. **查看文档**
   ```bash
   cat ~/.openclaw/skills/call-aida-app/SKILL.md
   ```

2. **查看示例**
   ```bash
   cat ~/.openclaw/skills/call-aida-app/EXAMPLES.md
   ```

3. **查看快速参考**
   ```bash
   cat ~/.openclaw/skills/call-aida-app/QUICKSTART.txt
   ```

4. **运行测试**
   ```bash
   bash ~/.openclaw/skills/call-aida-app/test.sh
   ```

## 📝 变更日志

### v1.0.0 (2026-03-14)

- ✨ 首次发布
- ✅ 支持 AIDA chat-messages API
- ✅ 三种参数传入方式
- ✅ 完整的错误处理
- ✅ 详细文档

## 📄 许可证

MIT License - 自由使用、修改和分发

## 🙏 致谢

感谢 OpenClaw 社区的支持！

---

**文档版本:** 1.0.0
**最后更新:** 2026-03-14
**维护者:** OpenClaw Skill Team
**位置:** `~/.openclaw/skills/call-aida-app/`

