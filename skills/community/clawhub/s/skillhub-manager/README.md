# SkillHub Manager

English

SkillHub Manager helps agents and developers search, inspect, and publish skills through SkillHub compatible registries such as ClawHub. It is designed for repeatable registry workflows instead of ad hoc HTTP calls.

What it solves
- Publishes a local skill folder through the clawhub CLI
- Searches and previews registry-hosted skills
- Documents authentication patterns for token-based publishing
- Asks the user for the SkillHub address before touching any registry
- Keeps registry targeting explicit through environment variables

Who needs it
- Developers maintaining reusable skills
- Operators running a private SkillHub registry
- Agents that need a safe, documented publishing workflow

Key features
- Search and inspect commands for existing skills
- Token-based login guidance
- Publish workflow for local skill packages
- Mandatory SkillHub address confirmation before use
- Repeat-back confirmation of the chosen SkillHub address before execution
- Registry override support with CLAWHUB_REGISTRY

When to use
- When a user asks to submit or publish a skill
- When you need to inspect a skill before installing it
- When you need a repeatable SkillHub or ClawHub workflow

Main files
- SKILL.md: core operating instructions for the agent
- references/workflows.md: step by step command examples

Interaction rule
- Ask the user for the SkillHub address first
- Wait for the answer
- Repeat the address back for confirmation
- Then run the clawhub command with either the default registry or CLAWHUB_REGISTRY

中文

SkillHub Manager 用于帮助代理和开发者通过兼容 SkillHub 的注册表，例如 ClawHub，完成技能的搜索、预览和发布。它强调可重复执行的注册表工作流，而不是临时拼接 HTTP 请求。

解决的问题
- 通过 clawhub CLI 发布本地 skill 文件夹
- 搜索和预览注册表中的技能
- 记录基于 token 的认证方式
- 在执行任何注册表操作前先询问用户 SkillHub 地址
- 通过环境变量显式指定目标注册表

适用人群
- 维护可复用技能的开发者
- 运行私有 SkillHub 注册表的运维人员
- 需要安全、可审计发布流程的代理

关键能力
- 搜索与 inspect 工作流
- 基于 token 的登录说明
- 本地 skill 包发布流程
- 使用前必须确认 SkillHub 地址
- 执行前必须先复述并确认用户提供的地址
- 通过 CLAWHUB_REGISTRY 覆盖目标注册表

适用场景
- 用户要求提交或发布 skill
- 安装前需要先检查 skill 内容
- 需要一套可复用的 SkillHub 或 ClawHub 工作流

交互规则
- 先询问用户 SkillHub 地址
- 等待用户回复
- 复述该地址并再次确认
- 然后再执行默认 registry 或带 CLAWHUB_REGISTRY 的命令
