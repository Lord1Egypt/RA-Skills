# 社区标准汇总

蒸馏自 6 个权威来源的 README 写作标准。

## 来源

| 来源 | 核心贡献 |
|------|----------|
| [awesome-readme](https://github.com/matiassingers/awesome-readme) | 优秀 README 范例集，GIF demo 是最受推崇的视觉元素 |
| [Standard README](https://github.com/RichardLitt/standard-readme) | 形式化规范：必需/可选节、排序规则、合规检查清单 |
| [Art of README](https://github.com/hackergrrl/art-of-readme) | 「认知漏斗」概念、「无源码测试」原则、10 项检查清单 |
| [Make a README](https://makeareadme.com/) | 面向新手的结构模板、「太长好过太短」原则 |
| [GitHub 官方文档](https://docs.github.com/en/repositories) | 500 KiB 截断限制、相对链接、自动 TOC |
| [thoughtbot](https://thoughtbot.com/blog/how-to-write-a-great-readme) | 技术文档也是写作、慷慨链接、可 grep 性 |

## 共识排序

所有来源一致同意的节顺序：

1. Title / Name
2. Short Description (one-liner, < 120 chars)
3. Badges
4. Long Description (optional)
5. Table of Contents (if > 100 lines)
6. Install
7. Usage (with code examples)
8. API (optional)
9. Contributing
10. License (always last)

## Art of README — 认知漏斗

读者的决策路径：

1. **名字** → 跟我有关吗？（0.5 秒决定）
2. **一行描述** → 大致对口吗？（2 秒决定）
3. **用法示例** → API 风格适合我的代码吗？（30 秒决定）
4. **API 细节** → 具体能做我要的事吗？（2 分钟决定）
5. **安装** → 已确定要用，怎么装？
6. **许可证** → 法律上能用吗？

核心洞察：按读者短路退出的速度排列信息。宽泛信息在前，具体细节在后。

## Standard README — 合规清单

- [ ] 文件名为 `README.md`（大写）
- [ ] 节按规定顺序出现
- [ ] 标题与 repo/包名一致
- [ ] 短描述 < 120 字符
- [ ] 短描述与包管理器和 GitHub 描述一致
- [ ] 超过 100 行有 Table of Contents
- [ ] TOC 链接到所有节
- [ ] Install 节有代码块
- [ ] Usage 节有代码块
- [ ] Contributing 节说明是否接受 PR
- [ ] License 用 SPDX 标识符
- [ ] License 是最后一节
- [ ] 无死链
- [ ] 代码示例和项目代码用同样的 lint 规则

## Make a README — 关键引用

> 考虑到读你 README 的人可能是新手。

> 太长好过太短。如果感觉太长了，把内容移到 wiki 或文档站，而不是删掉信息。

> 把隐含步骤写明：环境变量、setup 脚本、OS 特定指令。

## thoughtbot — 写作风格

- 技术文档仍然是写作，不必枯燥
- 用 **粗体** 标注核心功能描述
- 在合适的地方加文化引用
- 让 README 「可 grep」——帮助搜索引擎发现
- 慷慨链接：关联项目、Wikipedia、甚至 Urban Dictionary

## 质量分级（综合所有来源）

**Tier 1 — 最小可用 README：**
Title + one-liner + install + usage example + license

**Tier 2 — 好的 README：**
Tier 1 + description + TOC + contributing + badges + screenshots

**Tier 3 — 标杆级 README：**
Tier 2 + GIF demo + background/motivation + API docs + architecture diagram + runnable examples + known issues + project status + credits
