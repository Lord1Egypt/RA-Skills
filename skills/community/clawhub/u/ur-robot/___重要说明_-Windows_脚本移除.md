# ⚠️ 重要说明 - Windows 脚本移除

**更新日期:** 2026-04-02  
**影响平台:** Windows  
**影响程度:** ⚠️ 轻微 (核心功能不受影响)

---

## 📋 为什么移除了这些文件？

**原因:** 为符合 ClawHub 技能平台的安全要求

**移除的文件:**
- ❌ `fix-and-test.ps1`
- ❌ `setup-docker-d-drive.ps1`

**保留的文件:**
- ✅ 所有 `.py` Python 脚本
- ✅ 所有 `.md` 文档
- ✅ 所有 `.json` 配置文件

---

## 🔧 替代方案

### 1️⃣ fix-and-test.ps1 替代

**原功能:** 一键修复环境并运行测试

**替代方法:**

```bash
# 方法 1: 运行单个测试
python test_motion_simple.py
python test_rtde_official.py

# 方法 2: 运行示例
python examples/basic_move.py
python examples/io_control.py

# 方法 3: 运行所有测试
python test_continuous_motion.py
```

---

### 2️⃣ setup-docker-d-drive.ps1 替代

**原功能:** 配置 Docker 使用 D 盘存储

**替代方法 1: Docker Desktop GUI (推荐)**

```
1. 打开 Docker Desktop
2. 点击设置 ⚙️
3. Resources → Advanced
4. 修改 "Disk image location" 为 D:\Docker
5. 点击 Apply & Restart
```

**替代方法 2: 手动配置**

```powershell
# 1. 停止 Docker 服务
Stop-Service com.docker.service

# 2. 移动 Docker 数据到 D 盘
Move-Item "C:\ProgramData\Docker" "D:\Docker" -Force

# 3. 创建符号链接
New-Item -ItemType SymbolicLink -Path "C:\ProgramData\Docker" -Target "D:\Docker"

# 4. 重启 Docker 服务
Start-Service com.docker.service
```

**替代方法 3: 编辑 daemon.json**

```json
// C:\ProgramData\Docker\config\daemon.json
{
  "data-root": "D:\\Docker"
}
```

---

## ✅ 核心功能确认

**所有核心功能保留:**

| 功能 | 状态 | 文件 |
|------|------|------|
| URSim 控制 | ✅ | test_motion_simple.py |
| RTDE 数据读取 | ✅ | test_rtde_official.py |
| 连续运动 | ✅ | test_continuous_motion.py |
| 基础运动示例 | ✅ | examples/basic_move.py |
| IO 控制示例 | ✅ | examples/io_control.py |
| 真机测试 | ✅ | examples/real_robot_test.py |
| Python 库 | ✅ | ur_robot.py |
| 安全检查 | ✅ | safety_check.py |
| 完整文档 | ✅ | SKILL.md, README.md |

---

## 📞 需要帮助？

**详细替代方案文档:** `WINDOWS_SCRIPTS_NOTE.md`

**快速入门:** `README.md`

**完整文档:** `SKILL.md`

**问题反馈:** 通过 ClawHub 技能页面留言

---

## 📊 影响对比

| 用户类型 | 影响程度 | 说明 |
|----------|----------|------|
| **Windows 新手** | ⚠️ 轻微 | 需要手动配置 Docker |
| **Windows 熟练** | ✅ 无影响 | 可直接使用 Python 脚本 |
| **Linux/Mac 用户** | ✅ 无影响 | 本来就不使用 .ps1 |
| **真机用户** | ✅ 无影响 | Python 脚本完全保留 |
| **仿真用户** | ✅ 无影响 | 所有测试脚本可用 |

---

*此说明文档为 ClawHub 平台合规性要求而创建*
