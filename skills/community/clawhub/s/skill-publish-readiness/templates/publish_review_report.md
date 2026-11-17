# Publish Readiness 统一报告模板

## 运行信息

- 审查对象：
- 对象类型：skill / plugin / 未确认
- 请求模式：auto / quick / deep
- 实际模式：quick / deep
- 选择原因：
- 是否从 quick 升级：否 / 是（原因）

## 发布结论

- 结论：可以发 / 补完再发 / 先别发
- 置信度：高 / 中 / 低
- 一句话依据：

## Quick 输出（quick 模式必填，deep 可作为摘要）

### 闸门

| 检查项 | 状态 | 证据 |
|---|---|---|
| SKILL.md/frontmatter | 通过 / 失败 / 未验证 | |
| name/slug/version | 通过 / 失败 / 未验证 | |
| 首屏与目标用户 | 通过 / 失败 / 未验证 | |
| 分类、示例与信任信号 | 通过 / 失败 / 未验证 | |
| 明显安全风险 | 通过 / 失败 / 未验证 | |
| dry-run 前置项 | 通过 / 失败 / 未验证 | |

### 最多三个关键问题

1. P0/P1/P2：
2. P0/P1/P2：
3. P0/P1/P2：

### 最小补法

1.
2.
3.

## Deep 输出（仅 deep 模式）

### 证据矩阵

| 层级 | 状态 | 证据 | 能证明 | 不能证明 |
|---|---|---|---|---|
| 文件与 frontmatter | | | | |
| 版本、slug 与身份 | | | | |
| 依赖与环境 | | | | |
| 安全与权限 | | | | |
| 页面与差异化 | | | | |
| validation/dry-run | | | | |
| registry/moderation/install | | | | |

### 问题清单

| 优先级 | 问题 | 证据 | 影响 | 最小修复 | 验收 |
|---|---|---|---|---|---|
| P0/P1/P2 | | | | | |

### 差异化评分（0–25）

- 用户定位：/5
- 场景具体度：/5
- 输出独特性：/5
- 判断壁垒：/5
- 记忆点：/5
- 总分：/25

## 下一步命令

### Skill（仅保留匹配分支）

```bash
clawhub skill publish <path> --slug <stable-slug> --name "<Human Readable Name>" --dry-run --owner <owner>
```

### Plugin（仅保留匹配分支）

```bash
clawhub package validate <path>
clawhub package publish <path> --dry-run
```

## 修复后验收

- [ ] frontmatter 可解析且 slug 保持稳定
- [ ] 版本高于 registry latest
- [ ] 文案、示例、依赖和环境声明一致
- [ ] 无硬编码凭据、危险默认行为、字节码缓存或路径穿越
- [ ] 实际执行结果与报告记录一致
- [ ] 正式发布后另行用 inspect 与隔离安装验证

## 证据边界

- 已验证：
- 未验证：
- 冲突信号：
- 不应宣称：
