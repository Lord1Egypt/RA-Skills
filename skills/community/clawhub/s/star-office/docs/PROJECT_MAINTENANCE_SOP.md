# Star-Office-UI 项目维护 SOP（轻量版）

> 目标：让 Star-Office-UI 在继续增长的同时，保持仓库干净、回复友好、节奏稳定、社区感明确。

---

## 1. 总原则

### 1.1 关闭 issue / PR 时，一定留一句 closure reason

无论是：
- 已修复
- 重复
- 超出当前范围
- 提问者自行取消
- 已被其他 PR / issue 吸收

都尽量留一句话说明原因。

**最小模板：**
- Fixed in `commit/PR #xxx`, thanks for the report!
- Closing as duplicate of #xxx, thank you!
- Out of current scope for now, but welcome a focused PR.
- Canceled by requester / resolved in latest master.

目标不是“正式”，而是让后来人一眼看懂为什么被关。

---

## 2. Issue 处理规则

### 2.1 先判断 issue 类型

收到 issue 后，先分到四类之一：

#### A. Bug report
特征：报错、页面打不开、功能异常、状态不对

处理方式：
1. 复现 / 判断是否已知问题
2. 如果已修：回复 + 给 commit / PR 号
3. 如果未修：标记为待处理，必要时自己修 / 等 PR
4. close 时一定写清楚“修在哪了”

**推荐回复模板：**
> 感谢反馈！这个问题已在 `PR #xx` / `commit xxx` 中修复。请拉取最新 master 后再试一下，如果还有问题欢迎继续反馈。

---

#### B. Support / setup question
特征：怎么部署、为什么 Unauthorized、如何自动同步等

处理方式：
1. 先回答问题
2. 给最短路径（README / SKILL / 命令）
3. 如果文档能优化，顺手记成后续动作
4. close 时说明“问题已答复，如仍有问题欢迎 reopen”

**推荐回复模板：**
> 这个问题大概率和 xxx 有关。最新版已经做了相关修复 / 文档补充。你可以先试试最新 master；如果还有问题，欢迎重新打开 issue。

---

#### C. Feature request
特征：希望支持某个新能力、新方向、新体验

处理方式：
1. 明确是否感兴趣
2. 不要误关成“已修复”
3. 如果暂不做，也要说清楚“当前不做，但欢迎 PR / 后续讨论”

**推荐回复模板：**
> 这是个很好的方向，我们对这个想法感兴趣。不过它还不是当前阶段的既定工作项。如果你愿意推进，欢迎提一个更聚焦的 PR，我们可以一起讨论实现方式。

---

#### D. Duplicate / canceled / absorbed
特征：重复提问、提问者自己放弃、已被其他 issue 吸收

处理方式：
1. 链接到对应 issue / PR
2. 简短说明关闭原因
3. 保持礼貌

---

## 3. PR 处理规则

### 3.1 Merge 前检查四件事

#### 1) 这个 PR 是不是解决了真实问题？
- 是 bug fix 还是只是作者个人偏好？
- 是否对应某个 issue / 用户痛点？

#### 2) 改动范围是否可控？
- 小而聚焦 → 倾向合并
- 大而混杂 → 要求拆分 / 暂缓

#### 3) 是否引入额外维护负担？
- 新依赖
- 新配置
- 新架构
- 新文档成本

#### 4) 是否需要同步 README / changelog / release notes？
如果影响用户使用路径，必须同步文档。

---

### 3.2 PR 结果分三类

#### A. 直接合并
适合：
- 小 bug fix
- 文档修正
- 明确提升 onboarding / 稳定性

#### B. 关闭但感谢
适合：
- 已被 master 提前修复
- 重复 PR
- 方向不错但当前不合适

**原则：不合并 ≠ 否定贡献者**

#### C. 请求作者调整后再看
适合：
- 思路对，但改动太大
- 混入不相关内容
- 需要拆小

---

### 3.3 关闭 PR 时，尽量做到三件事

1. **先感谢**
2. **再说明原因**
3. **如果 possible，指出未来更容易被接受的方向**

**推荐模板：**
> Thanks for the PR — this is a thoughtful direction. We’re not merging it right now because xxx. If you’d like, a smaller / more focused PR around yyy would be much easier for us to review and land.

---

## 4. Release / 大版本收口流程

适用于：
- 一轮 bug fix 完成
- 一次文档重构完成
- 一次功能包发布（如 v1.0）

### 发布前 checklist
- [ ] 关键功能本机验证一次（至少 health / status / agents / set_state）
- [ ] smoke test 跑通
- [ ] README / SKILL / relevant docs 已同步
- [ ] CHANGELOG 已更新
- [ ] 相关 issue 已回复 / 关闭
- [ ] 如果有贡献者，考虑在 README / release note 致谢
- [ ] 确认仓库 worktree 干净，没有误提交文件

### Release note 结构建议
1. 这次版本是什么
2. 核心变化 3-5 条
3. 对用户有什么实际影响
4. 快速体验方式
5. 感谢贡献者

---

## 5. README / 文档维护规则

### 5.1 README 优先回答四个问题
1. 这是什么？
2. 适合谁？
3. 最快怎么用？
4. 如果我是 OpenClaw 用户，最短路径是什么？

### 5.2 文档更新触发条件
以下情况发生时，要同步 README / docs：
- 默认端口改变
- 默认安装方式改变
- 核心依赖或路径改变
- onboarding 流程改变
- 修复了高频 issue（尤其是部署 / 401 / loading 这类）

---

## 6. 社区关系维护

### 6.1 要主动做的三件事
- 在 README 或 release note 感谢明显贡献者
- 对早期贡献者保持尊重，即使 PR 没合并
- 对误解 / 错判及时补充说明

### 6.2 哪些 contributor 值得重点维护
优先维护这些人：
- 连续提多个高质量 PR 的
- 会主动补文档 / onboarding 的
- 不只是修自己问题，而是在帮项目补完整性的

---

## 7. 当前阶段最适合 Star-Office-UI 的维护策略

### 适合优先接收
- bug fix
- onboarding 改进
- 文档优化
- 小而明确的稳定性修复
- 与 OpenClaw / agent 体验强相关的增强

### 暂时谨慎对待
- 大规模重构
- 引入重依赖
- 强绑定某个个人工作流的改动
- 边界不清的大 feature

---

## 8. Star 自己要记住的维护原则

- 不要为了“显得热情”而模糊关闭原因
- 不要把 feature request 当成 bug fix 关掉
- 不要 merge 之后忘了补文档
- 不要忽略早期贡献者
- 仓库看起来干净，本身就是产品体验的一部分

---

## 一句话版本

> **小问题及时收口，大问题说清边界；每次关闭都留痕，每次发布都成阶段。**
