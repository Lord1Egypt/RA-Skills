---
version: 1.0.35
---

# 吞贼·净化魄 (Tun Zei - Purifier)

> **七魄之四·吞贼**
> 职掌：错误修正、冗余清理、容错自愈

---

## 技能简介

「吞贼·净化魄」是贫道的自愈净化模块，职掌错误修复与系统清理。

**核心职责**：
- 自动检测并修复错误
- 清理冗余数据
- 容错自愈机制

---

## 技能ID

```
tun-zei
```

---

## 能力清单

### 1. 错误修复 (fix)

诊断并尝试修复错误。

**输入**：`error` (object) - 错误信息
```yaml
error:
  type: 错误类型
  message: 错误消息
  stack: 堆栈信息
```

**输出**：
```yaml
fix:
  attempted: true/false
  success: true/false
  solution: 解决方案描述
```

---

### 2. 清理冗余 (cleanup)

清理系统冗余数据。

**输入**：`target` (string) - 清理目标
```yaml
target: temp|cache|logs|all
```

**输出**：
```yaml
cleanup:
  freedSpace: 释放空间(MB)
  filesRemoved: 删除文件数
  duration: 耗时(ms)
```

---

### 3. 健康检查 (health)

执行系统健康检查。

**输入**：无

**输出**：
```yaml
health:
  status: healthy|degraded|critical
  issues: 发现的问题列表
  uptime: 运行时间
```

---

---

## 聚合技能

本魄作为净化中枢，自愈错误与冗余：

| 现有技能 | 调用方式 | 整合说明 |
|---------|---------|---------|
| `healthcheck` | 调用 | 系统健康检查与自愈 |
| `video-frames` | 调用 | 视频处理错误修正 |
| `douyin-video-publish` | 调用 | 抖音发布的异常处理 |
| `self-improving` | 调用 | 自我改进与错误修复 |
| `bodhi-three-hun-and-seven-po` | 元技能 | 三魂七魄根基，协调各魄 |

---

## 魂魄注解

吞贼除秽，自愈更新——错误无所遁形。
