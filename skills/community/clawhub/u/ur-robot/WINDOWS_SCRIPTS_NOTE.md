# Windows PowerShell 脚本替代方案

**说明：** 由于 ClawHub 平台要求，`.ps1` 文件已从技能包中移除。以下是等效的替代方案。

---

## 📋 被移除的脚本

| 脚本 | 原用途 | 替代方案 |
|------|--------|----------|
| `fix-and-test.ps1` | 修复和测试 | 使用 Python 测试脚本 |
| `setup-docker-d-drive.ps1` | Docker D 盘设置 | 手动配置或 Docker Desktop 设置 |

---

## 🔧 fix-and-test.ps1 替代方案

**原功能：** 修复环境并运行测试

**替代方法：**

```bash
# 1. 启动 URSim
docker run -d --name ursim \
  -p 6080:6080 -p 30001-30004:30001-30004 \
  universalrobots/ursim_e-series

# 2. 运行 Python 测试
python test_motion_simple.py
python test_rtde_official.py
python test_continuous_motion.py
```

**或者使用示例脚本：**

```bash
# 基础运动测试
python examples/basic_move.py

# IO 控制测试
python examples/io_control.py
```

---

## 💾 setup-docker-d-drive.ps1 替代方案

**原功能：** 配置 Docker 使用 D 盘存储

**替代方法 1：Docker Desktop 设置**

1. 打开 Docker Desktop
2. 点击设置 (⚙️ Settings)
3. 选择 **Resources** → **Advanced**
4. 修改 **Disk image location** 为 `D:\Docker`
5. 点击 **Apply & Restart**

**替代方法 2：手动配置**

```powershell
# 停止 Docker 服务
Stop-Service com.docker.service

# 移动 Docker 数据到 D 盘
Move-Item "C:\ProgramData\Docker" "D:\Docker" -Force

# 创建符号链接
New-Item -ItemType SymbolicLink -Path "C:\ProgramData\Docker" -Target "D:\Docker"

# 重启 Docker 服务
Start-Service com.docker.service
```

**替代方法 3：使用 Docker 命令配置**

```bash
# 编辑 Docker daemon.json
# C:\ProgramData\Docker\config\daemon.json

{
  "data-root": "D:\\Docker"
}
```

---

## ✅ 核心功能不受影响

**保留的功能：**

- ✅ 所有 Python 控制脚本
- ✅ URSim 测试脚本
- ✅ RTDE 数据读取
- ✅ URScript 命令发送
- ✅ 示例代码
- ✅ 完整文档

---

## 📞 需要帮助？

如果遇到任何问题，请查看：

- **主文档：** SKILL.md
- **快速入门：** README.md
- **测试指南：** URSIM_TEST_GUIDE.md

---

*Created: 2026-04-02*
