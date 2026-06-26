# Evidence Schema — 统一证据格式

## 目的

统一各 source lane 采集的证据格式，便于：
- 结构化存储和检索
- 跨方案对比
- 证据可信度评估
- 报告自动生成

---

## 核心 Schema

```yaml
Evidence:
  id: string              # 唯一标识，格式：{lane}-{candidate}-{seq}
  lane: enum              # 来源车道：official-docs | github | clawhub | platform-native | community-discourse | runtime-test | internal-assets
  candidate: string       # 候选方案名称
  type: enum              # 证据类型：claim | benchmark | code | issue | tutorial | review | test-result
  content: string         # 证据内容摘要（markdown）
  source_url: string      # 原始来源 URL
  source_metadata:        # 来源元数据
    author: string | null
    published_date: string | null
    last_updated: string | null
    version: string | null
  claim_type: enum | null # 声称类型（仅当 type=claim）：feature | performance | security | cost | compatibility
  metric: object | null   # 量化指标（仅当 type=benchmark|test-result）
    name: string
    value: number
    unit: string
    higher_is_better: boolean
  confidence: enum        # 可信度：high | medium | low
  confidence_reason: string # 可信度理由
  extracted_at: string    # 采集时间（ISO 8601）
  extracted_by: string    # 采集者（agent 名）
  cross_refs: string[]    # 交叉引用的其他证据 ID
  verification_status: enum # 验证状态：verified | conflicting | unverified | pending-test
  notes: string | null    # 备注
```

---

## 各 Lane 证据规范

### official-docs

```yaml
lane: official-docs
type: claim | benchmark
source_metadata:
  version: "文档对应的版本号"
  last_updated: "文档最后更新时间"
claim_type: feature | performance | security | cost | compatibility
confidence: medium  # 官方声称需经第三方或实测验证
```

**示例**：
```yaml
id: official-docs-playwright-001
lane: official-docs
candidate: Playwright
type: claim
content: "支持 Chromium、Firefox、WebKit 三大引擎，自动等待元素可操作"
source_url: "https://playwright.dev/docs/intro"
source_metadata:
  last_updated: "2026-03-15"
  version: "1.42.0"
claim_type: feature
confidence: medium
confidence_reason: "官方文档声明，需实测验证"
extracted_at: "2026-03-29T10:00:00Z"
extracted_by: "tech-solution-research"
verification_status: unverified
```

---

### github

```yaml
lane: github
type: code | issue | benchmark
source_metadata:
  repo: "owner/repo"
  star_count: number
  issue_count: number
  last_commit: "ISO 8601"
  release_version: "latest release"
```

**示例**：
```yaml
id: github-playwright-001
lane: github
candidate: Playwright
type: code
content: "仓库 microsoft/playwright，12k issues，98% 关闭率，平均响应时间 2 天"
source_url: "https://github.com/microsoft/playwright"
source_metadata:
  repo: "microsoft/playwright"
  star_count: 65000
  issue_count: 12000
  last_commit: "2026-03-28"
  release_version: "1.42.0"
confidence: high
confidence_reason: "GitHub 官方数据，客观可验证"
extracted_at: "2026-03-29T10:05:00Z"
extracted_by: "tech-solution-research"
verification_status: verified
```

---

### community

```yaml
lane: community
type: tutorial | review | issue | benchmark
source_metadata:
  author: "作者/发布者"
  published_date: "ISO 8601"
  platform: "平台名称"
  engagement: 
    likes: number | null
    comments: number | null
```

**示例**：
```yaml
id: community-discourse-playwright-001
lane: community-discourse
candidate: Playwright
type: review
content: "Reddit 用户反馈：'从 Selenium 迁移到 Playwright 后，测试稳定性提升 80%，但学习曲线较陡'"
source_url: "https://reddit.com/r/webdev/comments/xxx"
source_metadata:
  author: "u/webdev_user"
  published_date: "2026-02-15"
  platform: "Reddit"
  engagement:
    likes: 150
    comments: 45
confidence: medium
confidence_reason: "单一用户经验，需更多案例验证"
extracted_at: "2026-03-29T10:10:00Z"
extracted_by: "tech-solution-research"
verification_status: unverified
```

---

### runtime-test

```yaml
lane: runtime-test
type: test-result | benchmark
metric:
  name: "指标名称"
  value: number
  unit: "单位"
  higher_is_better: boolean
source_metadata:
  test_environment: "测试环境描述"
  test_script: "测试脚本路径或 URL"
  test_date: "ISO 8601"
confidence: high
verification_status: verified
```

**示例**：
```yaml
id: runtime-test-playwright-001
lane: runtime-test
candidate: Playwright
type: benchmark
content: "本地实测：启动时间 1.2s，内存占用 150MB，100 次页面加载平均耗时 2.3s"
source_url: null
source_metadata:
  test_environment: "M1 Max 32GB, macOS 14.3, Node 20"
  test_script: "tests/browser-benchmark/playwright-test.js"
  test_date: "2026-03-29"
metric:
  name: "页面加载时间"
  value: 2.3
  unit: "seconds"
  higher_is_better: false
confidence: high
confidence_reason: "本地实测，环境可复现"
extracted_at: "2026-03-29T11:00:00Z"
extracted_by: "tech-solution-research"
verification_status: verified
```

---

## 证据矩阵格式

用于报告中的对比展示：

```markdown
| 证据 ID | Lane | 候选方案 | 类型 | 关键内容 | 可信度 | 验证状态 |
|---------|------|----------|------|----------|--------|----------|
| official-docs-playwright-001 | official-docs | Playwright | claim | 支持三大引擎 | medium | unverified |
| github-playwright-001 | github | Playwright | code | 65k stars, 98% issue 关闭率 | high | verified |
| runtime-test-playwright-001 | runtime-test | Playwright | benchmark | 启动 1.2s, 内存 150MB | high | verified |
```

---

## 冲突检测规则

当多个证据对同一事实有矛盾描述时：

1. **识别冲突**：相同 claim_type + 矛盾内容
2. **优先级仲裁**：runtime-test > official-docs > github > community
3. **标注冲突**：在 verification_status 标注 "conflicting"
4. **记录冲突详情**：在 notes 字段说明冲突双方

**示例**：
```yaml
id: official-docs-x-001
content: "官方声称支持 IE11"
verification_status: conflicting
notes: "与 runtime-test-x-001 冲突：实测 IE11 下功能异常"

id: runtime-test-x-001
content: "实测 IE11 下页面渲染异常"
verification_status: verified
notes: "与官方声称不一致，以实测为准"
```

---

## 证据采集 Checklist

采集每个候选方案时，至少覆盖：

- [ ] **official-docs**: 核心功能声明、API 文档、版本信息
- [ ] **github**: Star 数、issue 活跃度、最近 commit、最新 release
- [ ] **community**: 至少 2 个独立来源（博客/论坛/社交媒体）
- [ ] **runtime-test**: 关键功能实测或标注"待补核"
- [ ] **internal-assets**: 检查是否有内部使用历史

**最低要求**：每个候选方案至少 5 条证据，覆盖至少 4 个 lanes。

---

## 证据存储建议

- **临时存储**：调研过程中用 JSON/Markdown 暂存
- **归档存储**：完成后存入 `research/{topic}/evidence/` 目录
- **可追溯**：保留原始 URL 和采集时间，便于后续验证

---

## 版本

- **0.1.0**（2026-03-29）：初版 schema
注 "conflicting"
4. **记录冲突详情**：在 notes 字段说明冲突双方

**示例**：
```yaml
id: official-docs-x-001
content: "官方声称支持 IE11"
verification_status: conflicting
notes: "与 runtime-test-x-001 冲突：实测 IE11 下功能异常"

id: runtime-test-x-001
content: "实测 IE11 下页面渲染异常"
verification_status: verified
notes: "与官方声称不一致，以实测为准"
```

---

## 证据采集 Checklist

采集每个候选方案时，至少覆盖：

- [ ] **official-docs**: 核心功能声明、API 文档、版本信息
- [ ] **github**: Star 数、issue 活跃度、最近 commit、最新 release
- [ ] **community**: 至少 2 个独立来源（博客/论坛/社交媒体）
- [ ] **runtime-test**: 关键功能实测或标注"待补核"
- [ ] **internal-assets**: 检查是否有内部使用历史

**最低要求**：每个候选方案至少 5 条证据，覆盖至少 4 个 lanes。

---

## 证据存储建议

- **临时存储**：调研过程中用 JSON/Markdown 暂存
- **归档存储**：完成后存入 `research/{topic}/evidence/` 目录
- **可追溯**：保留原始 URL 和采集时间，便于后续验证

---

## 版本

- **0.1.0**（2026-03-29）：初版 schema
