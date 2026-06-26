# SkillPilot 安全声明

**版本**: v0.4.6  
**更新日期**: 2026-03-24  
**扫描状态**: ✅ 所有警告已修复

---

## 🔒 安全概览

### ClawHub 安全扫描结果

| 检查项 | 状态 | 说明 |
|--------|------|------|
| PURPOSE & CAPABILITY | ✅ 通过 | 技能目的与代码一致 |
| INSTALL MECHANISM | ✅ 通过 | 无自动下载/安装 |
| INSTRUCTION SCOPE | ✅ 修复 | 已声明所有操作范围 |
| CREDENTIALS | ✅ 修复 | 已声明环境变量使用 |
| PERSISTENCE & PRIVILEGE | ✅ 修复 | 已声明写入权限 |

---

## 📋 权限声明

### 文件读取

**范围**: `~/.openclaw/workspace/skills/*`

**用途**:
- 读取其他技能的配置和脚本
- 加载技能注册信息
- 读取用户偏好配置

**限制**:
- 仅限 OpenClaw workspace 内的技能目录
- 不读取用户个人文件
- 不读取系统文件

---

### 文件写入

**范围**: `~/.openclaw/workspace/skills/skill-pilot/`

**子目录**:
- `config/` - 用户偏好和模式配置
- `history/` - 执行历史记录
- `reports/` - 调度报告
- `env_cache.json` - 环境探测缓存

**用途**:
- 保存调度决策历史
- 记录工具性能数据
- 存储环境探测结果
- 生成可观测性报告

**限制**:
- 仅限 skill-pilot 自有目录
- 不修改其他技能文件
- 不修改系统配置

---

### 网络探测

**探测内容**:
- DNS 解析速度
- 网络延迟 (RTT)
- 代理服务器检测
- IPv6 可用性
- 区域判断 (cn/global)

**用途**:
- 优化技能路由决策
- 选择最适合当前网络的工具
- 避免使用被封锁的服务

**限制**:
- 仅探测网络连通性
- 不发送用户数据
- 不收集隐私信息

---

### 技能调用

**调用方式**:
1. **Python 模块导入** - 有 `scripts/main.py` 的技能
2. **脚本执行** - 有 `scripts/*.py/sh/js/mjs` 的技能
3. **OpenClaw 通道** - 无脚本的技能

**安全措施**:
- ✅ 输入验证 (危险字符检测)
- ✅ 输入清理 (移除不安全字符)
- ✅ 参数长度限制 (≤1000 字符)
- ✅ 超时保护 (默认 30 秒)
- ✅ 列表形式调用 subprocess (无 shell=True)

---

### 环境变量

**读取的环境变量**:

| 变量名 | 用途 | 必需 |
|--------|------|------|
| `TAVILY_API_KEY` | 传递给 tavily-search 技能 | 否 |
| `BRAVE_API_KEY` | 传递给 brave-search 技能 | 否 |
| `HTTP_PROXY` | 代理配置 | 否 |
| `HTTPS_PROXY` | 代理配置 | 否 |
| `OPENCLAW_GATEWAY_URL` | 自定义 Gateway 地址 | 否 |
| `OPENCLAW_TOKEN` | 自定义认证 Token | 否 |

**传递规则**:
- 环境变量仅传递给子进程 (技能脚本)
- 不主动收集或记录环境变量值
- 不将环境变量发送到外部服务
- 子进程继承是 Python subprocess 的默认行为

**安全建议**:
```bash
# 如担心环境变量泄露，可：
# 1. 在受限环境运行 (Docker/VM)
# 2. 移除高价值环境变量
# 3. 使用最小权限运行
```

---

## 🛡️ 安全修复历史

### v0.4.6 (2026-03-24) - 安全声明完善

**修复**:
- ✅ 完善 SKILL.md manifest 声明
- ✅ 添加 required_env 和 optional_env
- ✅ 添加 security_notes 说明权限范围
- ✅ 创建 SECURITY_DECLARATION.md 详细文档

### v0.4.5 (2026-03-20) - Shell 注入修复

**修复**:
- ✅ 移除所有 `shell=True` 调用
- ✅ 添加输入验证 (`_validate_args`)
- ✅ 添加输入清理 (`_sanitize_query`)
- ✅ 使用列表形式调用 subprocess

**测试**:
```bash
# 正常查询
python3 run_search.py "今日热点"  # ✅ 正常执行

# 注入尝试
python3 run_search.py "test; rm -rf /"  # ❌ 拒绝执行
python3 run_search.py "test | cat /etc/passwd"  # ❌ 拒绝执行
python3 run_search.py 'test $(whoami)'  # ❌ 拒绝执行
```

---

## 📊 风险评估

### 已识别风险

| 风险 | 严重性 | 缓解措施 | 状态 |
|------|--------|----------|------|
| Shell 注入 | 🔴 高 | 输入验证 + 移除 shell=True | ✅ 已修复 |
| 环境变量泄露 | 🟡 中 | 声明 + 最小权限建议 | ✅ 已声明 |
| 文件写入滥用 | 🟡 中 | 限制写入范围 | ✅ 已声明 |
| 网络探测隐私 | 🟢 低 | 仅探测连通性 | ✅ 已声明 |

### 剩余风险

**无已知高风险**。

**建议**:
- 在可信环境运行 (个人电脑/私有服务器)
- 定期审查技能代码
- 使用最新版本的 SkillPilot

---

## 🔍 审计指南

### 代码审计重点

**1. 输入验证** (`scripts/engine.py`)
```python
# 检查点：_validate_args 方法
def _validate_args(self, args: list) -> bool:
    # 应检查：危险字符、长度限制、类型验证
```

**2. 命令执行** (`scripts/engine.py`)
```python
# 检查点：_run_script 方法
# 应检查：使用列表形式、无 shell=True、有超时
cmd = ['python3', script_path] + args  # ✅ 正确
subprocess.run(cmd, shell=False, timeout=30)  # ✅ 正确
```

**3. 环境变量传递** (`scripts/engine.py`)
```python
# 检查点：subprocess.run 的 env 参数
env = os.environ.copy()  # 继承环境变量
result = subprocess.run(cmd, env=env, ...)
```

### 运行时审计

**日志位置**:
- `~/.openclaw/workspace/skills/skill-pilot/history/` - 执行历史
- `~/.openclaw/workspace/memory/YYYY-MM-DD.md` - 每日日志

**监控命令**:
```bash
# 查看最近的技能调用
tail -f ~/.openclaw/workspace/skills/skill-pilot/history/*.json

# 查看系统调用 (高级)
strace -e trace=execve -f python3 scripts/engine.py
```

---

## 📞 安全反馈

发现安全问题？请联系:
- GitHub Issues: https://github.com/openclaw/openclaw/issues
- 安全邮件：security@openclaw.ai (如配置)

---

*安全是持续过程。如发现任何问题，请立即报告。*
