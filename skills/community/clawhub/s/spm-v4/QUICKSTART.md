# SPM V4 实操教程

## 从安装到完成一个项目的完整工作流

---

## 第零步：安装

```bash
git clone https://github.com/zhbcher/SPM-V4.git
cd SPM-V4
npm install
```

安装后，你有一个 `src/` 目录（核心模块）和 CLI 命令 `node src/cli.js`。

---

## 第一步：初始化项目

假设你要做一个 Node.js REST API。

```bash
mkdir /tmp/my-rest-api
cd /tmp/my-rest-api
# 初始化常规项目
npm init -y
npm install express

# 然后初始化 SPM
# 回到 SPM-V4 目录运行 CLI
cd /path/to/SPM-V4
node src/cli.js init my-rest-api
# 会在当前目录（SPM-V4）下创建 docs/spm/ledger.md 等
# 但通常你应该在项目目录里用 SPM

# 更实用的方式：把 leder 建在项目目录下
# 直接在项目目录下写 leder.md，然后 spm 命令指向它
```

> **实际用法：** SPM V4 的 CLI 命令可以指定任意路径的 ledger 文件。所以你把 `docs/spm/ledger.md` 放在你的项目目录里，SPM 命令指定这条路经即可。

---

## 第二步：编写 WBS 台账

在你的项目目录下创建 `docs/spm/ledger.md`：

```markdown
# SPM WBS Ledger — My REST API

## WB-001: 搭建项目骨架
- **Status**: todo
- **Dependencies**: none
- **Context**: 创建 Express 项目、package.json、基础启动文件
- **Exit Criteria**: `npm start` 启动成功，curl localhost:3000 返回 200
- **Evidence**:

## WB-002: 实现健康检查接口
- **Status**: todo
- **Dependencies**: WB-001
- **Context**: GET /health 返回 { status: "ok" }
- **Exit Criteria**: curl localhost:3000/health 返回 200 + JSON
- **Evidence**:

## WB-003: 用户登录接口
- **Status**: todo
- **Dependencies**: WB-002
- **Context**: POST /auth/login, JWT token 返回
- **Exit Criteria**: curl 测试返回 token
- **Evidence**:

## WB-004: 用户注册接口
- **Status**: todo
- **Dependencies**: WB-002
- **Context**: POST /auth/register, 用户创建 + 返回 token
- **Exit Criteria**: curl 注册成功后登录验证
- **Evidence**:
```

---

## 第三步：哈希认证

```bash
cd /path/to/SPM-V4
node src/cli.js attest /path/to/your-project/docs/spm/ledger.md
# 输出: ✓ Attested: a3f8c2...
```

这条命令会：
1. 读取台账文件
2. 计算 SHA-256 哈希
3. 存储到 `.spm/wbs-attestation`（在 SP M-V4 目录下）
4. 记录到 Integrity Event Store

---

## 第四步：开始开发（工作循环）

### 循环体：

```
1. 选择一个 todo 任务
2. 更新 ledger: WB-001 的 Status 改为 doing
3. attest 一次
4. 实际编写代码
5. 验证代码：运行测试 / curl
6. 更新 ledger: WB-001 的 Status 改为 done + Evidence 填入验证输出
7. attest 一次
8. 进入下一个任务
```

### 具体操作：

```bash
# 步骤 2：标记为进行中
# 编辑 leder.md：WB-001 Status: todo → doing

# 步骤 3：认证
node src/cli.js attest /path/to/ledger.md

# 步骤 4：写代码（这是实际开发工作）
# ...

# 步骤 6：标记为完成，填入证据
# 编辑 leder.md：
#    Status: doing → done
#    Evidence: curl localhost:3000/health 返回 {"status":"ok"}, exit code 0

# 步骤 7：认证
node src/cli.js attest /path/to/ledger.md
```

---

## 第五步：阶段性验证

### 查看进度

```bash
node src/cli.js status
# 输出：
# WBS: 4 tasks (0 todo, 0 doing, 4 done)
# Attestation: a3f8c2... (verified)
```

### 完整性检查

```bash
node src/cli.js verify /path/to/ledger.md
# 如果哈希匹配：✓ WBS integrity verified
# 如果哈希不匹配：帐号被篡改了！
```

### 质量门禁

```bash
node src/cli.js quality-check /path/to/ledger.md
# 检查所有 done 任务是否有 Evidence
# 检查依赖关系是否完整
```

---

## 第六步：完成项目

```bash
# 1. 最终质量门禁
node src/cli.js quality-check /path/to/ledger.md

# 2. 最终认证
node src/cli.js attest /path/to/ledger.md

# 3. 验证完整性
node src/cli.js verify /path/to/ledger.md

# 4. 查看最终状态
node src/cli.js status
```

所有检查通过 → 项目完成。

---

## 完整示例（一条命令序列）

假设你有一个项目 `/tmp/my-api`：

```bash
# 1. 初始化
node src/cli.js init my-api

# 2. 写完 leder.md 后认证
node src/cli.js attest docs/spm/ledger.md

# 3. 开发循环：完成 WB-001
#   - 编辑 leder.md: WB-001 todo → doing
node src/cli.js attest docs/spm/ledger.md
#   - 写代码...
#   - 编辑 leder.md: WB-001 doing → done, 填入 Evidence
node src/cli.js attest docs/spm/ledger.md

# 4. 开发循环：完成 WB-002，同样的模式
#   ...

# 5. 阶段性检查
node src/cli.js status
node src/cli.js verify docs/spm/ledger.md
node src/cli.js quality-check docs/spm/ledger.md

# 6. 全部完成
echo "项目交付 ✓"
```

---

## AI Agent 如何使用 SPM V4

如果你是一个 AI agent，使用 SPM V4 管理自己的项目开发：

### 在每个会话开始时

```bash
node src/cli.js status               # 看到哪了
node src/cli.js verify leder.md      # 确认没人修改
```

### 在每次开发任务前

```bash
# 1. 读 WBS → 找 todo 任务
# 2. 更新 status 为 doing
# 3. attest
# 4. 写代码
```

### 在每次开发任务后

```bash
# 1. 验证输出（运行测试/curl）
# 2. 更新 status 为 done + 填入 Evidence
# 3. attest
```

### 跨会话恢复

```bash
# 新会话：
# 1. 读 leder.md → 看到 WB-002 是 doing
# 2. 读 contextBrief → 知道上下文
# 3. 读 evidence → 知道上次做了什么
# 4. 继续开发
```

---

## 总结

SPM V4 的核心工作流只有 5 步，反复循环：

```
1. init       → 创建项目骨架
2. 写 WBS     → 分解任务
3. attest     → 锁定状态
4. 开发+更新  → todo→doing→done+evidence
5. attest     → 锁定新状态
             → 回到 4 直到所有任务 done
```

`attest` 是最核心的操作——每次你都用 SHA-256 锁定当前台账状态，下次回来可以验证没人动过你的计划。