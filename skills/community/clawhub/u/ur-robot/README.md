# UR Robot Skill - 快速入门

**5 分钟上手 Universal Robots 机器人控制！**

---

## 📝 重要说明 (Windows 用户必读)

### ⚠️ PowerShell 脚本已移除

**原因:** 符合 ClawHub 平台安全要求

**移除的脚本:**
- ❌ `fix-and-test.ps1` → **替代:** `python test_*.py`
- ❌ `setup-docker-d-drive.ps1` → **替代:** 手动配置 (见下方)

**核心功能:** ✅ 完全保留 - 所有 Python 脚本可用

---

### 🔧 替代方案速查

**运行测试:**
```bash
python test_motion_simple.py      # 运动测试
python test_rtde_official.py      # RTDE 测试
python examples/basic_move.py     # 基础示例
```

**配置 Docker D 盘:**
1. 打开 Docker Desktop → 设置 ⚙️
2. Resources → Advanced
3. 修改 Disk image location 为 `D:\Docker`
4. Apply & Restart

---

### 💾 Windows 用户 - 一键运行工具 (可选)

**如果你想用一键运行的 .ps1 脚本：**

📦 **配套技能包：** [ur-robot-windows-scripts](https://clawhub.ai/skills/<username>/ur-robot-windows-scripts)

```bash
# 安装配套技能包
npx skills add <username>/ur-robot-windows-scripts

# 一键配置 Docker
.\setup-docker-d-drive.ps1

# 一键启动并测试
.\fix-and-test.ps1
```

**包含脚本：**
- `fix-and-test.ps1` - 一键修复环境并运行测试
- `setup-docker-d-drive.ps1` - 一键配置 Docker D 盘

**注意：**
- ⚡ 这是**可选工具**，核心功能不需要它
- ✅ 核心功能：直接使用 Python 脚本 (`python test_xxx.py`)
- 🐧 Mac/Linux 用户不需要此技能包

---

### 📊 两个技能包的关系

| 技能包 | 用途 | 必需 | 平台 |
|--------|------|------|------|
| **ur-robot** | Python 核心功能 | ✅ 必需 | 全平台 |
| **ur-robot-windows-scripts** | .ps1 一键工具 | ⚡ 可选 | Windows |

**推荐：**
- Windows 新手：两个都装
- Windows 熟练：只装主包
- Mac/Linux：只装主包

---

**详细说明:** 📄 `⚠️ 重要说明 -Windows 脚本移除.md` 或 `WINDOWS_SCRIPTS_NOTE.md`

---

## ⚠️ 重要声明

### 🧪 测试状态

| 环境 | 状态 |
|------|------|
| **URSim 仿真** | ✅ 已完成测试 |
| **真机验证** | ❌ **未验证** |

**本技能包仅在 URSim 仿真器中测试，未在真实机器人上验证！**

**真机使用必须：**
1. 重新验证所有命令
2. 使用低速参数 (v=0.1-0.3)
3. 专业人员监督
4. 进行风险评估

---

## 🎯 这是什么？

这是一个完整的 UR 机器人控制技能包，包含：

- ✅ URSim 仿真器配置
- ✅ Python 控制库
- ✅ URScript 命令参考
- ✅ RTDE 数据读取
- ✅ 完整测试脚本

---

## 🚀 5 分钟快速开始

### 步骤 1: 启动 URSim (1 分钟)

```bash
docker run -d --name ursim \
  -p 6080:6080 -p 30001-30004:30001-30004 \
  universalrobots/ursim_e-series
```

### 步骤 2: 打开浏览器 (30 秒)

```
http://localhost:6080/vnc.html
```

### 步骤 3: 初始化机器人 (1 分钟)

1. 点击 **ON** 按钮
2. 点击 **START** 按钮
3. 点击 **Program** → **Empty Program**
4. 点击 **Play** (▶)

### 步骤 4: 运行测试 (2 分钟)

```bash
# 测试关节运动
python skills/ur-robot/test_motion_simple.py

# 测试 RTDE 读取
python skills/ur-robot/test_rtde_official.py
```

---

## 📚 常用命令

### 关节运动

```python
# Home 位置
movej([0, -1.57, 1.57, -1.57, -1.57, 0])

# J1 旋转 30 度
movej([0.52, 0, 0, 0, 0, 0])
```

### 直线运动

```python
# 移动到目标位置
movel([0.3, 0.3, 0.5, 3.14, 0, 0])

# 相对移动 (+200mm X 轴)
movel(pose_trans(get_actual_tcp_pose(), p[0.2, 0, 0, 0, 0, 0]))
```

### IO 控制

```python
# 打开数字输出
set_digital_out(0, True)

# 关闭数字输出
set_digital_out(0, False)
```

---

## 📋 完整文档

| 文档 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | 完整技能文档 |
| [URSCRIPT_FEATURES.md](URSCRIPT_FEATURES.md) | URScript 功能清单 |
| [ur_robot.py](ur_robot.py) | Python 库 API |

---

## ⚠️ 注意事项

1. **仿真环境测试** - 确认在 URSim 中测试后再用于真机
2. **程序运行状态** - 确保 URSim 程序在运行（绿色 Play 按钮）
3. **运动范围** - 确保目标位置在机器人工作范围内
4. **低速测试** - 初次测试使用较低速度 (v=0.2-0.5)

---

## 🆘 常见问题

### Q: 机器人不动？
**A:** 检查程序是否运行 - 点击 Play 按钮

### Q: 连接失败？
**A:** 检查 Docker 端口映射 - `docker port ursim`

### Q: 命令不执行？
**A:** 检查 URSim 状态 - 应该是绿色 "Running"

---

## 📞 需要帮助？

查看详细文档：[SKILL.md](SKILL.md)

---

*Created: 2026-04-02*
