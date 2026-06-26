# GitHub 仓库审查

## 触发条件

- 用户发送 GitHub 仓库链接请求评估
- 克隆或安装来自 GitHub 的代码

## 审查流程

### 第 1 步：元数据评估

| 检查项 | 方法 | 关注点 |
|-------|------|-------|
| **Star/Fork** | GitHub 页面 | Star 可购买——高 star 无活动需额外审查 |
| **创建时间** | GitHub Insights | 全新仓库 vs 老牌仓库 |
| **最后提交** | GitHub 主页 | 长期不活跃可能意味着废弃 |
| **贡献者** | Contributors 页面 | 单一贡献者 vs 社区维护 |
| **Issues/PRs** | Issues 页面 | 安全研究员发现的问题？未解决的问题类型？ |
| **License** | 仓库根目录 | MIT/Apache 是好的，No License 需注意 |
| **是否 Fork** | 仓库顶部 | Fork 需单独审查其与上游的差异 |

**Trust Tier 映射：**
- Tier 1-2 来源 → 中等审查
- Tier 4 高 star 活跃仓库 → 高级审查，必须验证代码
- Tier 5 未知来源 → 最高审查

### 第 2 步：代码安全审计

按优先级审查以下区域：

| 优先级 | 区域 | 红旗 |
|-------|------|------|
| 高 | 入口点、API 路由、主处理逻辑 | eval() on user input, exec() on untrusted |
| 高 | 认证/授权模块 | 空 api_key 配置跳过认证 |
| 高 | 配置文件 | 硬编码凭证、调试标志 |
| 中 | 依赖声明 | `dependencies: {}` 或私有 npm 引用 |
| 中 | GitHub Actions | 见下方专项检查 |
| 低 | 文档、测试 | -- |

**GitHub Actions 专项红旗（必须检查）：**

| 检查项 | 红旗 | 严重性 |
|-------|------|-------|
| `GITHUB_TOKEN` 权限 `contents: write`+ | 可导致仓库被篡改 | 🔴 |
| `pull_request_target` trigger | 可能引入恶意代码到 PR | 🔴 |
| `workflow_dispatch` + 外部输入 | 允许外部触发器执行 | 🟡 |
| Secrets 在 logs 中打印 | `echo ${{ secrets.SECRET }}` | 🔴 |
| 第三方 Action（未知作者） | 可能包含恶意代码 | 🟡 |
| Actions 指向外部仓库 | checkout 时可能执行恶意代码 | 🔴 |

**GitHub Actions 专项红旗（必须检查）：**

| 检查项 | 红旗 | 严重性 |
|-------|------|-------|
| `GITHUB_TOKEN` 权限 `contents: write`+ | 可导致仓库被篡改 | 🔴 |
| `pull_request_target` trigger | 可能引入恶意代码到 PR | 🔴 |
| `workflow_dispatch` + 外部输入 | 允许外部触发器执行 | 🟡 |
| Secrets 在 logs 中打印 | `echo ${{ secrets.SECRET }}` | 🔴 |
| 第三方 Action（未知作者） | 可能包含恶意代码 | 🟡 |
| Actions 指向外部仓库 | checkout 时可能执行恶意代码 | 🔴 |

**常见仓库级红旗：**
- `eval()` 处理用户输入
- SQL 字符串拼接（SQL 注入）
- CORS 设为 `*`（生产环境）
- JWT 无过期时间
- Dockerfile 以 root 运行
- 空的 `api_key` 配置
- `exec_policy.mode = "Full"` 绕过安全

### 第 3 步：架构分析

| 方面 | 安全 | 不安全 |
|------|------|-------|
| **认证** | 多因素、短期 token、会话管理 | 长期 API key 无轮换 |
| **授权** | 最小权限、范围明确 | 过度权限请求 |
| **数据流** | 加密传输、范围受限 | 明文日志、过度数据收集 |
| **输入验证** | 白名单、类型检查 | 黑名单或无验证 |
| **密钥管理** | 密钥轮换、加密存储 | 环境变量硬编码 |
| **更新机制** | 签名验证、手动触发 | 远程自动下载执行 |

### 第 4 步：依赖审查

1. **package.json / requirements.txt / Cargo.toml** — 逐个检查依赖
2. **已知恶意包** — 检查是否匹配 typosquatting 或供应链攻击模式
3. **依赖版本** — 是否有版本范围过大（`*`, `latest`）的依赖
4. **私有依赖** — 是否引用私有仓库或未知来源

参考 [supply-chain.md](supply-chain.md) 中的完整供应链攻击模式。

### 第 5 步：Fork 分析

审查 Fork 时，**仅关注与上游的差异**——这些修改是实际风险面：
- 查看 `git diff HEAD~N..HEAD`（N = 总提交数）
- 特别关注新增文件和新依赖
- 检查上游仓库是否已弃用或被攻击

### 评级决策

| 条件 | 评级 |
|------|------|
| Tier 1-2 官方仓库，代码清晰，无红旗 | 🟢 LOW |
| Tier 4 仓库，存在可修复问题 | 🟡 MEDIUM |
| 涉及认证、资金或敏感操作 | 🔴 HIGH |
| 存在 eval/exec/SQL注入等确认漏洞 | ⛔ REJECT |
| 源代码未验证或无法审计 | 🔴 HIGH 起步 |

**报告格式（必须使用 Box Drawing）：**

```
╔══════════════════════════════════════════════════╗
  REPOSITORY SECURITY ASSESSMENT
╠══════════════════════════════════════════════════╣
  Repository:   [owner/repo]
  Trust Tier:   [N]
  Stars:        N | Forks: N | License: [type]
  Last Commit:  YYYY-MM-DD | Contributors: N
╠══════════════════════════════════════════════════╣
  RATING:      [🟢/🟡/🔴/⛔]
╠══════════════════════════════════════════════════╣
  METADATA AUDIT
  - [check result]
╠══════════════════════════════════════════════════╣
  CODE AUDIT FINDINGS
  - [红旗 1]
  - [红旗 2]
╠══════════════════════════════════════════════════╣
  DEPENDENCY REVIEW
  - [issue 1]
  - [issue 2]
╠══════════════════════════════════════════════════╣
  RECOMMENDATION
  [基于评级的行动建议]
╚══════════════════════════════════════════════════╝
```
