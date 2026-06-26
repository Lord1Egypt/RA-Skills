# Update Approval Guard - 技能发布包

## ✅ 硟认结果

**这是一个原创技能！** 很可能是在之前的会话中创建的本地技能。

---

## 📦 已准备好的文件

我已为你准备了两个压缩包：

### 1. 基础技能包（4.8KB）
- **位置**: `/root/.openclaw/workspace/update-approval-guard.tar.gz`
- **包含**: SKILL.md, README.md, package.json, LICENSE, examples/

### 2. 完整发布包（30KB）
- **位置**: `/root/.openclaw/workspace/update-approval-guard-with-publish.tar.gz`
- **包含**: 基础技能包 + 自动发布脚本（publish.sh）

---

## 🚀 快速发布（推荐）

### 方式一：使用自动脚本

```bash
cd ~/.openclaw/workspace
tar -xzf update-approval-guard-with-publish.tar.gz
cd update-approval-guard
./publish.sh
```

脚本会自动完成：
1. ✅ 检查和配置 Git
2. ✅ 初始化 Git 仓库
3. ✅ 创建提交
4. ✅ 提示创建 GitHub 仓库
5. ✅ 推送到 GitHub
6. ✅ 发布到 ClawHub

### 方式二：手动发布

详细步骤请查看飞书文档：
- 📄 **技能详细手册**: https://feishu.cn/docx/EKn6dmGxsoj4SZxJEbOciyIVnNf
- 📄 **发布指南**: https://feishu.cn/docx/ZU8ZdvND0oHV79xSVe1cbqeinrd

---

## 📋 技能信息

| 字段 | 值 |
|------|-----|
| **名称** | Update Approval Guard |
| **版本** | 1.0.0 |
| **描述** | Daily update checker for OpenClaw and installed skills with approval workflow |
| **作者** | 曹力文 |
| **许可证** | MIT |
| **创建时间** | 2026-03-13 14:25:48 |

---

## 🎯 技能特点

**解决的问题**: 让OpenClaw自动检查更新，但不自动执行，需要人工审批。

**核心功能**:
1. 定时检查（每天00:00）
2. 生成待更新计划
3. 请求用户审批
4. 审批后执行更新
5. 自动健康检查

**安全特性**:
- ✅ 检查阶段只使用 dry-run 模式
- ✅ 不自动执行更新
- ✅ 需要明确的关键词审批
- ✅ 计划24小时后自动过期
- ✅ 更新后自动健康检查

---

## ✅ 发布后验证

```bash
# 搜索技能
clawhub search update-approval-guard

# 安装技能
clawhub install update-approval-guard

# 查看技能详情
clawhub inspect update-approval-guard

# 查看已安装
clawhub list | grep update-approval-guard
```

---

## 🔗 相关资源

- **飞书技能手册**: https://feishu.cn/docx/EKn6dmGxsoj4SZxJEbOciyIVnNf
- **飞书发布指南**: https://feishu.cn/docx/ZU8ZdvND0oHV79xSVe1cbqeinrd
- **ClawHub 文档**: https://docs.clawhub.com
- **OpenClaw 文档**: https://docs.openclaw.ai

---

_准备完成时间: 2026-03-19 11:14 Asia/Shanghai_