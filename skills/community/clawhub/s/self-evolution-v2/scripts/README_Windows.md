# Windows 安装指南

## OpenClaw on Windows

OpenClaw 支持 Windows 原生安装。本技能同样兼容，**无需任何脚本**。

## 安装步骤

### 第一步：安装技能

在 OpenClaw 中执行：

```bash
skillhub install self-evolution
```

### 第二步：告诉AI应用这个技能

```
在OpenClaw对话中输入：

"应用self-evolution技能"

AI会自动完成所有配置，包括：
- 把进化规则写入你的SOUL.md
- 创建必要的learnings模板文件
```

**不需要运行任何PowerShell脚本，不需要bash，完全通过对话完成。**

---

## 路径参考

| 文件 | Windows路径 |
|------|------------|
| SOUL.md | `C:\Users\用户名\.openclaw\workspace\SOUL.md` |
| MEMORY.md | `C:\Users\用户名\.openclaw\workspace\MEMORY.md` |
| .learnings | `C:\Users\用户名\.openclaw\workspace\.learnings\` |
| 技能目录 | `C:\Users\用户名\.openclaw\skills\self-evolution\` |

## 常见问题

**Q: 安装后没反应？**
A: 确保技能安装完成，然后在OpenClaw中发送"应用self-evolution技能"

**Q: 技能装好了但规则没生效？**
A: 关闭当前OpenClaw会话，重新打开。新规则需要在新会话中加载。

**Q: 怎么确认规则生效了？**
A: 新会话开始后，AI会自带自我审视能力，不再需要任何额外操作。
