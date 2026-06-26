# RELEASE-NOTES.md

## xiaoai-ha-control

一个通过 **Home Assistant + Xiaomi Miot** 控制小爱音箱的 OpenClaw skill，支持：

- `say`：让小爱播报文本
- `exec`：让小爱执行文本指令
- `play`：让小爱播放 URL 音频
- 可选：`bridge_server.py` 实现 **小爱语音 → OpenClaw** 的桥接

---

## 本次版本重点

### 1. 明确拆分两类能力

#### A. OpenClaw → 小爱音箱
这是核心能力，也是推荐新用户先跑通的部分：

- 让小爱播报
- 让小爱执行文本命令
- 让小爱播放 URL 音频

#### B. 小爱音箱 → OpenClaw（可选）
通过 Home Assistant conversation sensor + 宿主机 bridge，把小爱语音文本转给 OpenClaw。

---

### 2. 新增桥接网关思路

当前推荐桥接架构：

```text
小爱语音 → Home Assistant → bridge_server.py → OpenClaw main
```

其中：

- HA 只做入口转发
- `bridge_server.py` 做白名单放行和状态记录
- main 统一调度子 agent 和最终出口

---

### 3. 新增语义方向规则

推荐规则：

- **带 `【来自小爱】` / `【来自小爱语音】` 标识**
  - 视为：**小爱控制 OpenClaw**
- **普通聊天消息中，不带上述标识，但文本里出现 `小爱` / `小爱同学`**
  - 视为：**OpenClaw 控制小爱**

---

### 4. 新增 bridge 白名单原则

为了避免把小爱原生命令误转给 OpenClaw，bridge 推荐采用：

- 默认拒绝
- 命中白名单才放行

例如：

- `告诉管家...` → 放行
- `问一下研究员...` → 放行
- `打开客厅灯` → 留给小爱原生处理

---

### 5. 文档结构更新

当前目录中的文档分工：

- `SKILL.md`：skill 触发与能力边界
- `README.md`：从零搭建总览
- `references/bridge-setup.md`：桥接搭建与排障
- `NOTES.md`：兼容性边界与分享注意事项
- `STATUS.md`：当前架构定位

---

## 适合谁使用

适合：

- 已接入 Home Assistant + Xiaomi Miot 的小爱用户
- 想通过 OpenClaw 控制小爱音箱的人
- 想进一步尝试“小爱语音桥接到 OpenClaw”的进阶用户

不适合：

- 还没有 Home Assistant 环境的人
- 希望开箱即用，不愿处理实体 ID、Token、Docker/宿主机网络的人

---

## 使用建议

推荐顺序：

1. 先配置 `.env`
2. 先验证：
   - `say`
   - `exec`
   - `play`
3. 再考虑接 `bridge_server.py`
4. 最后再调桥接白名单和子 agent 分流

---

## 已知限制

- 不同小爱型号暴露的实体可能不同
- Xiaomi Miot 的 conversation 拉取可能超时
- Docker 中的 HA 到宿主机 bridge 可能存在网络可达性问题
- `exec` 是否成功依赖小爱本身能否理解命令
- `bridge_server.py` 当前包含示例型白名单与本地实现细节，分享给别人时需要按环境调整
