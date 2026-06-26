# system_cmd 技能快速启动指南

## 🚀 立即开始使用

### 基本命令
```
/system_cmd ipconfig      # 查看网络配置
/system_cmd tasklist      # 查看进程列表
/system_cmd netstat       # 查看网络连接
/system_cmd systeminfo    # 查看系统信息
```

### 获取帮助
```
/system_cmd help
```
或
```
/system_cmd
```

## 📋 命令速查表

| 命令 | 功能 | 示例输出 |
|------|------|----------|
| `ipconfig` | 查看IP地址和网络配置 | 主机名、IP地址、DNS、网关等 |
| `tasklist` | 查看运行中的进程 | 进程名、PID、内存使用等 |
| `netstat` | 查看网络连接状态 | 协议、本地地址、远程地址、状态 |
| `systeminfo` | 查看系统详细信息 | 系统版本、硬件信息、安装日期等 |

## 🎯 常见使用场景

### 场景1: 网络故障排查
```
/system_cmd ipconfig   # 检查IP配置是否正确
/system_cmd netstat    # 检查网络连接状态
```

### 场景2: 系统性能检查
```
/system_cmd tasklist    # 查看哪些进程占用资源
/system_cmd systeminfo  # 查看系统资源使用情况
```

### 场景3: 系统信息收集
```
/system_cmd systeminfo  # 获取完整的系统配置信息
```

## ⚠️ 注意事项

1. **执行时间**: `systeminfo` 命令执行较慢（5-10秒），请耐心等待
2. **输出大小**: `tasklist` 和 `netstat` 可能输出大量数据
3. **权限**: 普通用户权限即可执行所有命令
4. **编码**: 已处理中文编码问题，输出正常显示

## 🔧 故障排除

### 问题1: 命令执行失败
**症状**: 返回错误信息
**解决**: 检查命令名称是否正确，或使用 `/system_cmd help` 查看支持的命令

### 问题2: 输出乱码
**症状**: 中文显示为乱码
**解决**: 技能已自动处理编码，如果仍有问题请反馈

### 问题3: 命令执行超时
**症状**: 长时间无响应
**解决**: `systeminfo` 命令可能需要较长时间，请等待或检查系统状态

## 📚 更多资源

- `references/commands.md` - 命令详细参考文档
- `references/usage_examples.md` - 完整使用示例
- `scripts/system_cmd_simple.js` - 技能实现源代码

## 🆘 获取帮助

如有问题或建议，请：
1. 使用 `/system_cmd help` 查看帮助
2. 参考 `references/` 目录下的文档
3. 检查命令是否正确输入

---

**技能状态**: ✅ 已就绪  
**最后更新**: 2026-04-08  
**版本**: 1.0.0