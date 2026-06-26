# VC 5.0 Python 3 API 全网最全解读

## 📖 技能说明

这是全网最详细的 Visual Components 5.0 Python 3 API 解读文档，包含所有核心模块的完整参数说明、使用示例和实战案例。

## 🎯 内容亮点

1. **完整模块结构** - 9 大核心模块详解
2. **参数全解读** - 每个方法的参数、返回值、异常
3. **代码示例** - 可直接运行的完整示例
4. **实战案例** - 码垛、分拣、AGV 调度
5. **迁移指南** - Python 2 到 Python 3 完整迁移

## 📁 文件结构

```
vc-python-3-api-guide/
├── SKILL.md          # 完整 API 解读文档
└── README.md         # 本说明文档
```

## 📚 目录结构

1. VC 5.0 Python 3 API 概述
2. 核心模块详解
3. vcCore 模块完整参数解读 ⭐⭐⭐⭐⭐
4. vcBehaviors 模块详解
5. vcRobotics 模块详解
6. vcProcessModel 模块详解
7. 异步编程指南
8. 实战案例
9. 从 Python 2 迁移到 Python 3
10. 常见问题 FAQ

## 🔑 核心内容

### vcCore 模块（最常用）

| 方法 | 用途 | 使用频率 |
|------|------|----------|
| `getApplication()` | 获取应用对象 | ⭐⭐⭐⭐⭐ |
| `getComponent()` | 获取组件对象 | ⭐⭐⭐⭐⭐ |
| `delay()` | 延时等待 | ⭐⭐⭐⭐⭐ |
| `condition()` | 条件等待 | ⭐⭐⭐⭐⭐ |
| `allTasks()` | 等待所有任务 | ⭐⭐⭐⭐ |
| `anyTask()` | 等待任意任务 | ⭐⭐⭐⭐ |

### 事件处理器

| 事件 | 触发时机 | 用途 |
|------|----------|------|
| `OnRun` | 仿真开始 | 主程序 |
| `OnSignal` | 信号触发 | 信号处理 |
| `OnSimulationUpdate` | 每帧更新 | 实时更新 |

## 💡 使用建议

1. **先学 vcCore** - 最基础、最常用
2. **掌握异步** - Async/Await 是核心
3. **多练示例** - 直接运行示例代码
4. **参考论坛** - 结合精华帖学习

## 🔗 官方资源

- **API 文档:** https://help.visualcomponents.com/5.0/Premium/en/Python_3_API/Overview.html
- **vcCore 模块:** https://help.visualcomponents.com/5.0/Premium/en/Python_3_API/Modules/vcCore.html
- **示例代码:** 参考 SKILL.md 中的完整示例

## 📊 版本信息

| 项目 | 信息 |
|------|------|
| VC 版本 | 5.0 Premium |
| Python 版本 | 3.12.2 |
| 文档版本 | v1.0 |
| 最后更新 | 2026-03-13 |

---

*版本：v1.0*  
*作者：JMO / Robotqu*  
*整理：小橙 🍊*
