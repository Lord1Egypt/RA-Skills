# 提示词模板

复制以下提示词到任意 OpenClaw 会话中即可使用 Skill Vetter。

## 安装 Skill Vetter

```text
请帮我安装 Skill Vetter，并按安全优先方式操作。

来源：useai-pro/openclaw-skills-security@skill-vetter (ClawHub)

要求：
1. 先获取并审查该 skill 的全部文件
2. 输出审查报告：来源、作者、更新时间、文件数量、红旗项、权限范围、风险等级、verdict
3. 审查通过后安装到 ~/.agents/skills/skill-vetter/
4. 验证 skill 可被当前 OpenClaw 识别
5. 告诉我安装路径、来源、版本、调用方式

规则：
- 如发现外联、敏感文件读取、混淆代码、sudo/elevated 权限请求，必须标红说明
- HIGH 或 EXTREME 风险不要安装，先等我确认
```

## 审查 Skill（不安装）

```text
请用 Skill Vetter 协议审查这个 skill，先不要安装：
[粘贴 skill 链接]

要求：
1. 读取并检查全部文件
2. 检查风险：外部网络请求、敏感文件访问、base64/混淆、eval/exec、浏览器 cookie/session、workspace 外部文件修改、凭证请求
3. 输出标准化报告（名称、来源、作者、更新时间、文件数、红旗、权限、风险等级、verdict）
4. 结论：SAFE / CAUTION / DO NOT INSTALL
```

## 审查并安装 Skill

```text
我想安装这个第三方 skill：
[粘贴 skill 链接]

请按 SOP 执行：
1. 完整 skill vetting
2. 审查全部文件，列出红旗项和权限范围
3. 输出标准化 vetting report
4. 仅 LOW 风险或明确安全时才安装
5. 安装路径默认 ~/.agents/skills/
6. 安装后告诉我：实际路径、安装文件、调用方式、是否建议加入 AGENTS.md

规则：HIGH 或 EXTREME 风险时停止等待确认
```

## 强制执行"先审后装"规则

```text
请帮我把以下规则加入当前 agent 的 AGENTS.md：

所有 Skills 安装前，必须先用 Skill Vetter 审查，通过后才能安装。无例外。

要求：
1. 告诉我应该写入哪个文件
2. 直接写入
3. 解释此规则如何影响后续 skill 安装任务
4. 给一个示例说明以后怎么说 agent 就会自动先 vet 再安装
```

## 巡检已安装 Skills

```text
请对当前机器上已安装的第三方 skills 做安全巡检。

范围：~/.agents/skills/

要求：
1. 列出所有第三方 skill
2. 扫描风险：可疑外联、敏感文件读取、eval/exec、base64/混淆、新增可疑文件、workspace 外修改
3. 每个 skill 状态：✅ 正常 / ⚠️ 需关注 / ❌ 有问题
4. 结果写入带时间戳的 markdown 文件
5. 总体建议：是否有 skill 应移除、隔离或复审
```

## 创建自动巡检定时任务

```text
请为当前 OpenClaw 创建一个每 4 小时运行的 skills 安全巡检任务。

要求：
1. 使用 isolated session 执行
2. 巡检 ~/.agents/skills/ 下所有第三方 skill
3. 按 skill-vetter 红旗清单检查
4. 结果写入 security-audits/skills-audit-YYYY-MM-DD_HHMM.md
5. 保留历史文件
6. 简要摘要发送回当前聊天
```
