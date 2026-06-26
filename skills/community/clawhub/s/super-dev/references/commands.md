# Super Dev CLI 完整命令参考

## 流水线命令

```bash
# 0-1 新项目：完整流水线
super-dev pipeline "需求描述" --frontend react --backend node --platform web --domain fintech
super-dev "需求描述"                    # 等价于 pipeline

# 缺陷修复（轻量路径）
super-dev fix "修复登录页 bug"

# 1-N 已有项目：初始化（name 为必填位置参数）
super-dev init my-project -f react-vite -b python

# 跳转到指定阶段
super-dev run research          # 按名称
super-dev run frontend          # 按名称
super-dev run 6                 # 按编号 (1-9)
super-dev run --resume          # 从中断处继续
super-dev run --status          # 查看状态

# 直接命令模式
super-dev "做一个电商平台"       # 等价于 pipeline
super-dev fix "修复登录页 bug"   # bugfix 轻量路径
```

## 状态与诊断

```bash
super-dev status                # 流水线状态
super-dev doctor                # 宿主诊断（所有宿主）
super-dev doctor --host openclaw # 诊断指定宿主
super-dev metrics               # 流水线指标
```

## Spec 管理

```bash
super-dev spec list                                          # 列出活跃变更
super-dev spec show <change-id>                              # 查看详情
super-dev spec propose <change-id> --title "标题" --description "描述"  # 创建提案
super-dev spec scaffold <change-id>                          # 生成实现骨架
super-dev spec scaffold <change-id> --force                  # 强制重新生成
super-dev spec validate <change-id>                          # 验证格式
```

## 质量与审查

```bash
super-dev quality               # 运行所有质量检查
super-dev quality -t code       # 只检查代码质量
super-dev quality -t all        # 检查所有维度
super-dev review docs           # 文档审查
super-dev review ui             # UI 审查
super-dev review architecture   # 架构审查
```

## 专家咨询

```bash
super-dev expert PM "目标用户画像"
super-dev expert ARCHITECT "微服务边界划分"
super-dev expert SECURITY "API 安全审计"
super-dev expert DBA "索引优化策略"
super-dev expert QA "测试覆盖率方案"
super-dev expert DEVOPS "CI/CD 流水线设计"
super-dev expert UI "设计系统规范"
super-dev expert UX "用户体验优化"
super-dev expert CODE "代码重构方案"
super-dev expert RCA "故障根因分析"
```

## 发布与交付

```bash
super-dev release readiness     # 发布就绪度检查
super-dev release proof-pack    # 生成交付证明包
super-dev deploy                # 生成部署配置
super-dev deploy --cicd github  # 生成 GitHub Actions
super-dev deploy --docker       # 生成 Dockerfile
super-dev deploy --rehearsal    # 生成发布演练清单
```

## 配置管理

```bash
super-dev config list           # 列出所有配置
super-dev config get quality_gate # 获取指定配置
super-dev config set quality_gate 90 # 设置配置
```

## 代码库分析

```bash
super-dev analyze               # 分析项目
super-dev repo-map              # 代码库地图
super-dev dependency-graph      # 依赖图
super-dev impact                # 影响分析
super-dev regression-guard      # 回归检查清单
super-dev feature-checklist     # PRD 范围覆盖率
```

## 支持的技术栈

**平台**: web, mobile, wechat, desktop
**前端**: next, react-vite, vue-vite, nuxt, remix, angular, sveltekit, astro, solid, qwik, gatsby
**后端**: node, python, go, java, rust, php, ruby, csharp, kotlin, swift, elixir, scala, dart
**领域**: fintech, ecommerce, medical, social, iot, education, auth, content, saas
**CI/CD**: github, gitlab, jenkins, azure, bitbucket
