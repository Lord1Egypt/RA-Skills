# 商服机器人 Skill 调用说明

> **技能名称**：商服机器人
> **适用版本**: sebot_aicatering / aiSkill.py
> **最后更新**: 2026-07-11（经实际测试验证）

---

## 1. 环境准备与部署

> **重要：** 商服机器人与 Agent 电脑为两台独立设备，Agent 通过 SSH 远程登录机器人执行指令。**不可在机器人上写入或修改代码。**

### 1.1 网络环境

商服机器人与 Agent 电脑必须连接在**同一个局域网（WiFi）**下。

### 1.2 查询机器人 IP 地址

在机器人桌面操作：
1. 点击 **WiFi 图标** → **「设置」**
2. 查看当前 IP 地址（如 `192.168.100.165`）

> 验证 IP 可达性：`ping <机器人IP>`

### 1.3 SSH 连接

| 项目 | 值 |
|------|-----|
| 用户名 | `root` |
| 密码 | `root` |

```bash
# 验证连接
ssh root@<机器人IP> "echo OK"
```

### 1.4 ROS 环境确认

登录机器人后，确认 ROS 工作空间路径和话题在线：

```bash
# 确认 ROS 版本
ls /opt/ros/
# → melodic

# 确认工作空间（实际路径可能与文档不同）
ls ~/workspace/sebot-t710-competition/sebot_catering/devel/setup.bash

# 确认关键话题在线
source /opt/ros/melodic/setup.bash && \
  source ~/workspace/sebot-t710-competition/sebot_catering/devel/setup.bash && \
  rostopic list | grep agent
# 应显示: /agent/cmd  /agent/reply
```

### 1.5 ROS_DOMAIN_ID

```bash
echo $ROS_DOMAIN_ID
```

若不为空，后续所有命令需在前面追加 `export ROS_DOMAIN_ID=<值> &&`。

---

## 2. 系统架构

```
Agent 电脑 (外部系统)
   │
   │  SSH 远程执行 rostopic
   │
   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    商服机器人 (root@<IP>)                        │
│                                                                 │
│  /agent/cmd (std_msgs/String)     ← 外部发送文本指令            │
│  /agent/reply (std_msgs/String)   → 机器人回复文本              │
│  /instruct (std_msgs/String)      ↔ 内部控制指令(外部勿操作)     │
│  /audio (std_msgs/String)         → 执行事件反馈                │
│                                                                 │
│  aiSkill.py 指令处理流程:                                       │
│    cmd_callback() → deque 缓冲 → decide() 分流                  │
│      ├─ WordsMatching 关键词匹配 (interaction.json)             │
│      ├─ AiChat LLM (千帆 deepseek-v3.2 / ernie-5.0 vision)     │
│      └─ order/aiOrder → /instruct → aiCatering.cpp              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. ROS 话题接口

### 3.1 `/agent/cmd` — 输入指令

| 属性 | 值 |
|------|-----|
| 类型 | `std_msgs/String` |
| 方向 | Agent → 机器人 |
| 说明 | 发送自然语言文本，支持中文 |

### 3.2 `/agent/reply` — 输出回复

| 属性 | 值 |
|------|-----|
| 类型 | `std_msgs/String` |
| 方向 | 机器人 → Agent |
| 说明 | 与 TTS 语音播报同步发布，是判断 Skill 调用结果的主要依据 |

### 3.3 `/instruct` — 内部控制指令

| 属性 | 值 |
|------|-----|
| 类型 | `std_msgs/String` |
| 方向 | aiSkill.py → C++ |
| 说明 | **Agent 不应直接操作此话题。** 由 aiSkill.py 根据指令自动发布 |

### 3.4 `/audio` — 执行事件

| 属性 | 值 |
|------|-----|
| 类型 | `std_msgs/String` |
| 方向 | C++ → aiSkill.py |
| 说明 | 用于追踪取餐/导航等动作的执行进度 |

---

## 4. Skill 功能与调用方式

### 4.1 对话 Skill（chat / aiChat）

触发任意不含点餐/结账/视觉关键词的文本。

| 指令 | 预期回复示例 | 说明 |
|------|-------------|------|
| `你好` | `你好,欢迎使用商服机器人!` | 预设关键词 |
| `介绍一下你自己` | `我是DeepSeek...` | LLM 兜底 |
| `有什么吃的` | 菜单列表 | 预设关键词 |

**关键词匹配优先级:**
1. `catering` 餐饮 → 进入点餐流程
2. `cmd` → 系统指令
3. `chat` → 预设对话
4. 无匹配 → `aiChat` LLM 语义理解

### 4.2 点餐 Skill（catering）⭐ 核心

多轮交互流程：**发起点餐 → 选择食物 → 确认下单 → (机器人取餐) → 结账**

```
① 发起点餐:
  发送: "我要点餐" 或 "我想下单"
  回复: "您好,请问您需要什么？"
  ── aiSkill.py 自动发布 "order" 到 /instruct ──

② 选择食物:
  发送: "汉堡"
  回复: "请问需要我帮您下单汉堡吗?"
  ── 确认阶段，等待用户确认 ──

③ 确认下单:
  发送: "好的" 或 "需要" 或 "嗯"
  回复: "好的,请稍等,正在为您获取汉堡。"
  ── aiSkill.py 自动发布 "3" 到 /instruct ──
  ── 机器人开始导航+抓取，此时拒绝新指令 ──

④ 取餐中 (机器人繁忙):
  发送: 任何指令
  回复: "小赛正在执行任务，请您等小赛忙完了再下达指令。"
  ── 正确做法: 等待 /audio 事件 "OK" 或回复恢复正常 ──

⑤ 继续点餐或结账:
  发送: "再来一杯咖啡" → 回复: "请问需要我帮您下单咖啡吗?"
  发送: "嗯" → 回复: "好的,请稍等,正在为您获取咖啡。"
  发送: "结账" → 回复: "好的,一共是XX元。"
```

> **⚠️ 关键限制：**
> - 最多点 6 份食物，超出会回复"已达上限"
> - 机器人在执行取餐时（`pickOk` → `putOk` → `OK` 阶段）拒绝新指令
> - 结账前必须等所有取餐任务完成（通过 `/audio` 的 `OK` 事件或对话测试确认空闲）

### 4.3 视觉观察 Skill

| 指令 | 触发关键词 | 说明 |
|------|-----------|------|
| `帮我看看桌上有什么` | 看看/桌上 | 拍照+LLM 视觉分析 |
| `你看前面有什么` | 看/看见/图像 | 同上 |

**注意：** 视觉分析需调用千帆 ernie-5.0 大模型（含图像），耗时 5-15 秒。如摄像头不可用，回复"摄像头数据获取失败"。

### 4.4 查看餐台 Skill

```
发送: "去餐台看看" 或 "到餐台"
回复: "好的，小赛将前往餐台帮您查看。"
── 机器人自主导航到取餐台 ──
```

### 4.5 系统指令

| 指令 | 行为 |
|------|------|
| `结束` | 播放结束语 → 关闭 ROS 进程 → 退出程序 |

---

## 5. 判断调用是否成功

### 5.1 通过 `/agent/reply` 文本判断

| 场景 | ✅ 成功标志 | ❌ 失败标志 |
|------|-----------|-----------|
| 对话 | 收到非空文本 | 空字符串 / 超时 |
| 点餐-发起 | `"您好,请问您需要什么？"` | 无回复 |
| 点餐-确认 | `"好的,请稍等,正在为您获取..."` | `"已达上限"` |
| 点餐-结账 | `"好的,一共是XX元。"` | 机器人繁忙 |
| 视觉 | 场景描述文本 | `"摄像头数据获取失败"` / `"Error"` |
| 餐台 | `"好的，小赛将前往餐台..."` | 无回复 |
| 繁忙 | `"小赛正在执行任务"` | —（需等待后重试） |

### 5.2 通过 `/audio` 事件追踪（点餐场景）

| 事件 | 含义 | 阶段 |
|------|------|------|
| `caterStart` | 任务启动 | 初始化 |
| `menu` | 菜单介绍 | 点餐 |
| `pickBurger` / `pickCoffee` / ... | 开始抓取 | 取餐中 |
| `pickOk` | 抓取成功 | 取餐完成 |
| `stockout` | 抓取失败/缺货 | ⚠️ 需处理 |
| `putOk` | 放置完成 | 配送完成 |
| `OK` | 回到餐桌 | ✅ 任务完成 |
| `naviTimeout` | 导航超时 | ❌ 异常 |
| `errMovebase` | 导航连接失败 | ❌ 异常 |

### 5.3 食物编号映射

| 食物 | `/instruct` | `/audio` 事件 | 单价 |
|------|------------|--------------|------|
| 调料 | `1` | `pickCondiment` | 0 元 |
| 咖啡 | `2` | `pickCoffee` | 20 元 |
| 汉堡 | `3` | `pickBurger` | 22 元 |
| 瑞士卷 | `4` | `pickCake` | 6 元 |
| 面包 | `5` | `pickBread` | 10 元 |
| 冰淇淋 | `6` | `pickSundae` | 8 元 |

---

## 6. 实战调用示例（SSH 方式，已验证通过）

### 6.1 依赖安装

```bash
pip install paramiko
```

### 6.2 完整 Python 客户端

```python
#!/usr/bin/env python3
"""
商服机器人 Skill 调用客户端
通过 SSH 远程执行 rostopic 命令，发送指令并接收回复

基于 2026-07-11 实际测试验证的可用方案
"""
import paramiko
import re
import time


class RobotSkillClient:
    """商服机器人 Skill SSH 客户端"""

    # ==== 配置（按实际情况修改）====
    ROBOT_IP = "192.168.100.165"          # 机器人 IP（桌面 WiFi 设置查看）
    SSH_USER = "root"
    SSH_PASS = "root"
    ROS_DOMAIN_ID = None                   # 如 "101"，None 表示不设置
    # ROS 环境 source 路径（需在机器人上确认）
    ROS_SETUP_BASH = (
        "source /opt/ros/melodic/setup.bash && "
        "source ~/workspace/sebot-t710-competition/sebot_catering/devel/setup.bash"
    )
    # ==============================

    def __init__(self):
        self._ros_env = self.ROS_SETUP_BASH
        if self.ROS_DOMAIN_ID:
            self._ros_env = f"export ROS_DOMAIN_ID={self.ROS_DOMAIN_ID} && " + self._ros_env

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            hostname=self.ROBOT_IP,
            username=self.SSH_USER,
            password=self.SSH_PASS,
            timeout=10,
        )
        print(f"[连接] {self.SSH_USER}@{self.ROBOT_IP} OK")

    def send_cmd(self, text: str, timeout: int = 12) -> tuple:
        """
        发送文本指令并等待 /agent/reply 回复

        Args:
            text:    指令文本，如 "你好"、"我要点餐"、"汉堡"
            timeout: 等待回复超时（秒），视觉指令建议 25+

        Returns:
            (success: bool, reply_text: str | None)
        """
        # 核心技巧：必须先启动 echo 监听（后台），等订阅注册后，再发送 pub
        # 否则 reply 在 echo 订阅建立前就发出，会丢失消息
        inner = (
            f"timeout {timeout} rostopic echo /agent/reply -n 1 & "
            "E=$!; "
            "sleep 0.8; "               # 等待 ROS 订阅者注册
            f'rostopic pub /agent/cmd std_msgs/String "{text}" -1 > /dev/null 2>&1; '
            "wait $E 2>/dev/null"
        )
        cmd = f"{self._ros_env} && bash -c {repr(inner)}"

        _stdin, stdout, _stderr = self.ssh.exec_command(cmd, timeout=timeout + 10)
        out = stdout.read().decode("utf-8", errors="replace")

        # 解析 "data: !!python/str \"...\"" 格式，支持跨行回复
        m = re.search(
            r'data:\s*(?:!!python/str\s*)?["\'](.+?)["\']\s*$',
            out, re.DOTALL | re.MULTILINE,
        )
        if m:
            reply = m.group(1)
            reply = re.sub(r"\n\s+", "", reply)  # 合并跨行文本
            # 处理 \uXXXX Unicode 转义
            try:
                reply = reply.encode("ascii").decode("unicode_escape")
            except (ValueError, UnicodeDecodeError):
                pass
            return True, reply

        return False, None

    def is_busy(self) -> bool:
        """检查机器人是否正在执行任务"""
        ok, reply = self.send_cmd("你好", timeout=8)
        return reply and "正在执行" in str(reply)

    def wait_idle(self, max_wait: int = 120) -> bool:
        """等待机器人空闲"""
        start = time.time()
        while time.time() - start < max_wait:
            if not self.is_busy():
                print(f"[状态] 机器人空闲 (已等待 {time.time()-start:.0f}s)")
                return True
            print(f"[状态] 机器人繁忙，等待中...")
            time.sleep(10)
        print(f"[状态] 超时: 等待 {max_wait}s 后仍未空闲")
        return False

    def close(self):
        self.ssh.close()
        print("[连接] 已关闭")


# ============================================================
# 使用示例：完整点餐 + 结账流程
# ============================================================
if __name__ == "__main__":
    client = RobotSkillClient()

    # ----- 对话测试 -----
    ok, reply = client.send_cmd("你好")
    print(f"对话: {reply}")

    # ----- 点餐流程 -----
    # ① 发起点餐
    ok, reply = client.send_cmd("我要点餐")
    print(f"点餐: {reply}")

    # ② 选食物
    ok, reply = client.send_cmd("汉堡")
    print(f"选餐: {reply}")

    # ③ 确认下单（机器人开始取餐）
    ok, reply = client.send_cmd("好的")
    print(f"确认: {reply}")

    # ④ 等待取餐完成
    if client.wait_idle():
        # ⑤ 继续点餐或结账
        ok, reply = client.send_cmd("结账")
        print(f"结账: {reply}")

    client.close()
```

### 6.3 关键使用约束

| 约束 | 说明 | 解决方案 |
|------|------|---------|
| **时序** | echo 必须先于 pub 启动 | 代码中已处理（sleep 0.8s） |
| **间隔** | 两次 `send_cmd()` 调用间需间隔 ≥1s | 顺序调用，等回复后再发下一条 |
| **繁忙** | 取餐中拒绝新指令 | 调用 `wait_idle()` 等待 |
| **视觉超时** | 拍照+LLM 需 5~15s | 将 timeout 设为 25+ |
| **不可修改机器人代码** | Agent 不应在机器人上写文件 | 所有命令通过 SSH exec 执行 |

---

## 7. 常见问题与排查

### 7.1 收不到回复 (send_cmd 返回 False)

| 可能原因 | 排查方法 |
|---------|---------|
| aiSkill.py 未运行 | `ps aux \| grep aiSkill` 检查进程 |
| ROS 环境未 source | 检查 `ros_setup_bash` 路径是否正确 |
| 指令被吞（队列满） | 等待后重试 |
| 机器人忙 | 检查回复是否为"正在执行任务" |
| 时序问题 | echo 启动太晚，增加 `sleep` 时间 |

### 7.2 SSH 连接失败

```
Permission denied (publickey,password)
```

- 确认用户名密码：`root / root`
- 确认 IP 正确（通过机器人桌面 WiFi 设置查看）
- 确认两台设备在同一网络

### 7.3 rostopic: command not found

SSH 默认 shell 未加载 ROS 环境。必须在命令中显式 source setup.bash，或使用本文档提供的 `ROS_SETUP_BASH` 模板。

### 7.4 视觉指令返回"摄像头数据获取失败"

摄像头硬件偶发故障，属于正常错误处理。重试通常可恢复。

### 7.5 GBK 编码错误（Windows 终端）

机器人回复含 emoji 或其他非 GBK 字符时，Windows 终端打印会报 `UnicodeEncodeError`。解决：

```python
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
```

---

## 8. 经验总结

1. **Agent 不得修改机器人代码** — 所有交互必须通过 SSH 远程执行 `rostopic` 命令完成
2. **echo-before-pub 是关键** — `rostopic echo` 订阅者必须先于 `rostopic pub` 注册，否则丢消息。间隔 ≥0.8s
3. **点餐是异步流程** — 确认下单后机器人开始物理取餐，此时拒绝新指令。用 `wait_idle()` 或监听 `/audio` 的 `OK` 事件判断完成
4. **简洁指令效果更好** — "汉堡"比"我想要一个汉堡"更容易命中关键词匹配（但 LLM 兜底可以处理后者）
5. **回复含 Unicode 转义** — 需 `encode('ascii').decode('unicode_escape')` 解码
6. **视觉指令超时长** — 建议 timeout ≥ 25 秒
7. **不要 pkill 清理 echo 进程** — 容易误杀新启动的监听进程
