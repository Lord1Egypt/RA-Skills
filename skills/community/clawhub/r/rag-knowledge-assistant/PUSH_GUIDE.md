# RAG 知识库技能 - 推送指南

## 当前状态

✅ 代码已准备就绪

✅ Git 仓库已初始化并提交

## 推送方法

由于 GitHub 需要认证，请选择以下任一方式推送：

---

### 方法 1: 使用 Personal Access Token (推荐)

#### 1. 创建 Token

访问：https://github.com/settings/tokens

- 点击 "Generate new token (classic)"
- 勾选权限：`repo` (完整控制)
- 生成并复制 Token (形如 `ghp_xxxxxxxxxxxx`)

#### 2. 推送代码

```bash
cd <skill-directory>

# 使用 Token 推送 (替换 YOUR_TOKEN)
git push https://YOUR_TOKEN@github.com/AIxbinge/rag-skill.git main
```

---

### 方法 2: 使用 Git Credential Manager

```bash
cd <skill-directory>

# 执行推送，会弹出登录窗口
git push -u origin main
```

---

### 方法 3: 使用 SSH

#### 1. 配置 SSH Key

```bash
# 生成 SSH Key (如已有可跳过)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 将公钥添加到 GitHub: https://github.com/settings/keys
```

#### 2. 更改远程 URL 为 SSH

```bash
cd <skill-directory>

git remote set-url origin git@github.com:AIxbinge/rag-skill.git
git push -u origin main
```

---

## 验证推送

推送成功后，访问仓库查看：
https://github.com/AIxbinge/rag-skill

应该看到以下文件：
- `SKILL.md` - Skill 主文件
- `README.md` - 使用说明
- `rag-config.yaml` - 配置文件
- `scripts/` - Python 脚本目录
  - `index_knowledge.py` - 索引构建
  - `rag_query.py` - 向量检索
  - `requirements.txt` - 依赖
  - `setup.bat` - 安装脚本
  - `build_index.bat` - 索引脚本
- `references/` - 参考文档

---

## 快速推送命令

```bash
# 完整流程 (使用 Token 方式)
cd <skill-directory>

# 如果还没有 Token，先创建一个
# 然后执行:
git push https://ghp_YOUR_TOKEN_HERE@github.com/AIxbinge/rag-skill.git main
```
