# SysGuard - OpenClaw 系统守护技能

> 🛡️ 守护你的 OpenClaw 系统

## 功能

- **系统状态**: CPU/内存/磁盘/Gateway 实时监控
- **健康检查**: 详细检测各项指标
- **诊断报告**: 8 大隐藏事件检测
- **趋势图表**: 纯文本可视化趋势
- **缓存清理**: 释放磁盘空间
- **守护监控**: 持续后台监控

## 指令

| 命令 | 功能 |
|------|------|
| `sg` | 系统状态 + 命令提示 |
| `sgc` | 清理缓存 |
| `sgch` | 健康检查 |
| `sgd` | 诊断报告 |
| `sgt [小时]` | 趋势图（默认12小时） |
| `sgm` | 守护监控 |

## 使用示例

```
sg        # 查看系统状态
sgc       # 清理缓存
sgch      # 运行健康检查
sgd       # 生成诊断报告
sgt 24    # 查看24小时趋势
sgm       # 启动守护监控
```

## 安装

### 方式一：ClawHub 一键安装（推荐）
```bash
clawhub install sysguard
```

### 方式二：GitHub 克隆
```bash
git clone https://github.com/Steventsang18/sysguard.git
```

安装完成后，所有用户在任何 IM 对话中直接说 `sg` 即可使用。

## 技术特点

- 零依赖（纯 Shell）
- < 2s 响应时间
- IM 友好输出
- 中文优先

---

**版本**: v2.1.0
**作者**: Steventsang18
**许可证**: MIT
