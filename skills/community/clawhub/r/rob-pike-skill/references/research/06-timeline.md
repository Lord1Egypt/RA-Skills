# Rob Pike - 时间线

## 早年与教育

**1956年** - 出生于加拿大

**教育背景**:
- 多伦多大学 (University of Toronto) - 学士学位 (BS)
- 加州理工学院 (California Institute of Technology)

---

## 贝尔实验室时期 (1980-2002)

### 1980年代 - Unix 核心贡献期

- **1980年**: 加入贝尔实验室 (Bell Labs)，成为技术团队成员
  - 位置: 新泽西州默里山
  - 部门: 计算科学研究中心 (Computing Sciences Research Center) - Unix 的诞生地
  - 同年获得奥林匹克射箭银牌（个人主页幽默声称）

- **1981年**: 编写了 Unix 第一个位图窗口系统
  - 这是他在图形界面领域的开创性工作
  - 成为重叠窗口显示的美国专利唯一发明人

- **1982年**: 与 Bart Locanthi 设计 Blit 终端
  - Blit 是一种多路复用图形终端
  - 制作了经典动画短片解释鼠标工作原理

- **1984年**: 发表 Blit 终端论文 (AT&T Bell Laboratories Technical Journal)

- **1985年**: 与 Dave Presotto 发表 "Face the Nation" (USENIX)
  - 开发了 vismon 程序，用于显示邮件作者的面孔

### 中期 - 操作系统与语言创新

- **1990年**: 开发 Newsqueak 并发编程语言
  - 这是后来 Go 语言并发模型的先驱
  - 发表论文 "The Implementation of Newsqueak"
  - 5月: 与 Penn & Teller 一起登上 David Letterman 晚间秀

- **1992年**: UTF-8 编码诞生
  - 与 Ken Thompson 在新泽西餐厅的餐垫上设计
  - 9月2日完成设计
  - Plan 9 系统率先全面采用 UTF-8
  - 1993年1月在圣迭戈 USENIX 会议上正式发布

- **1990年代中期**: Plan 9 操作系统核心开发者
  - 与 Ken Thompson、Dave Presotto、Phil Winterbottom 共同领导
  - Dennis Ritchie 担任计算技术研究部门主管

- **1995年**: Plan 9 第二版发布 (面向非商业用途)

- **1990年代后期**: Inferno 操作系统和 Limbo 编程语言开发
  - 继续与贝尔实验室团队合作

### 其他重要贡献

- **文本编辑器**: 开发了多个文本编辑器，最著名的是:
  - sam - 结构化正则表达式编辑器
  - acme - Plan 9 的集成开发环境

- **书籍著作**:
  - 与 Brian Kernighan 合著《The Unix Programming Environment》
  - 与 Brian Kernighan 合著《The Practice of Programming》

- **其他项目**:
  - Mark V. Shaney - 人工智能 Usenet 发布程序
  - 设计了一个伽马射线望远镜（几乎被航天飞机任务发射）
  - 光污染研究（1970年代中期，与 Richard Berry 合作）

- **2000年**: 发表著名演讲 "Systems Software Research is Irrelevant"
  - 又名 Utah 2000
  - 对操作系统研究现状的深刻反思

- **2002年**: 离开贝尔实验室，加入 Google

---

## Google 时期 (2002-至今)

### 早期项目

- **2002年**: 加入 Google
  - 动机之一: 一次构建需要45分钟的挫折体验

- **2005年**: Sawzall 编程语言
  - 与 Sean Dorward、Robert Griesemer、Sean Quinlan 合作
  - 用于并行数据分析的日志处理语言
  - 发表论文 "Interpreting the Data: Parallel Analysis with Sawzall"

### Go 语言时代

- **2007年**: Go 语言设计开始
  - 与 Robert Griesemer、Ken Thompson 共同设计
  - 目标: 解决 Google 内部的软件开发效率问题
  - 动机: 对 C++ 的不满、构建时间过长、依赖管理复杂

- **2008年**: Go 语言规范第一稿
  - 在悉尼 Darling Harbour 的建筑18层完成
  - Ian Lance Taylor 根据 draft spec 独立实现了 gccgo 前端

- **2009年11月10日**: Go 开源发布
  - 下午3点（加州时间）网站上线
  - 团队: Ken Thompson、Robert Griesemer、Russ Cox、Ian Taylor、Adam Langley、Jini Kim
  - Gopher 吉祥物由妻子 Renée French 设计

- **2012年3月**: Go 1.0 发布
  - 确立 Go 1 兼容性承诺
  - 这是 Go 成功的关键决策之一

### 演讲与影响力

- **2013年**: SPLASH 会议演讲
  - "Go at Google: Language Design in the Service of Software Engineering"
  - 解释 Go 为什么诞生

- **2018年**: Google Sydney Tech Week
  - 分享 Unix 早期历史的个人经历

- **2023年11月10日**: GopherConAU (悉尼)
  - 主题演讲: "What We Got Right, What We Got Wrong"
  - Go 开源14周年纪念
  - 深度回顾 Go 项目的成功与教训

---

## 最近12个月动态 (2025.4-2026.4)

### 持续开发项目

- **Ivy 项目持续更新** (APL 风格计算器)
  - GitHub: github.com/robpike/ivy
  - 支持 Go 1.24
  - 提供 iOS 和 Android 应用
  - 持续添加新特性

- **其他个人项目**:
  - lisp - Toy Lisp 1.5 解释器
  - filter - 简单的 apply/filter/reduce 包
  - typo - Unix typo 命令的 Go 版本
  - translate - Google 翻译 API 的命令行工具

### Go 语言演进参与

- **Go 1.24** (2025年2月) - 持续关注
- **Go 1.25** (2025年8月) - Green Tea GC、Flight Recorder
- **Go 1.26** (2026年2月) - 新 GC 默认启用、SIMD 支持
- **Go 16周年** (2025年11月) - Go 团队发布纪念文章

### 社区活动

- **2023年11月 GopherConAU** 后继续通过博客和社区发声
- 博客: commandcenter.blogspot.com
- 个人主页: herpolhode.com/rob/
- GitHub 活跃: robpike

---

## 当前状态

### 职业状态

- **雇主**: Google (截至 2026年4月)
- **工作年限**: 2002年至今 (约24年)
- **主要角色**: Go 语言核心团队成员

### 居住情况

- 与妻子 Renée French (作家、插画家) 居住
- 在美国和澳大利亚两地生活
- 妻子设计了 Go 的 Gopher 吉祥物和 Plan 9 的 Glenda 吉祥物

### 持续贡献

- 继续维护个人开源项目
- 参与 Go 社区讨论
- 通过博客分享见解

---

## 获得荣誉与奖项

### 专业认可

虽然 Rob Pike 本人没有像 Ken Thompson 那样获得 Turing Award，但他的贡献被广泛认可：

- **UTF-8**: 互联网主导编码格式 (99% 网页使用，截至2026年)
- **Go 语言**: 全球最流行的编程语言之一
  - 2025年 Go 开发者调查显示持续增长
  - 云原生基础设施的首选语言
- **Plan 9**: 操作系统研究的里程碑
- **Unix 贡献**: 作为核心团队成员参与 Unix 发展

### 专利

- 重叠窗口显示的美国专利唯一发明人

### 行业影响

- **gofmt**: 推动了整个编程社区对代码格式化工具的重视
- **并发模型**: Go 的 goroutine/channel 模型影响了众多现代语言
- **软件工程实践**: Go 的工具链设计成为行业标准

---

## 关键贡献总结

| 领域 | 贡献 | 重要性 |
|------|------|--------|
| Unix | 第一个窗口系统、核心团队成员 | ⭐⭐⭐⭐⭐ |
| UTF-8 | 与 Ken Thompson 共同设计 | ⭐⭐⭐⭐⭐ |
| Plan 9 | 核心设计师和开发者 | ⭐⭐⭐⭐⭐ |
| Go | 三位创始人之一 | ⭐⭐⭐⭐⭐ |
| 文本编辑器 | sam, acme | ⭐⭐⭐⭐ |
| 并发编程 | Newsqueak (Go 并发的先驱) | ⭐⭐⭐⭐ |
| 编程书籍 | 与 Kernighan 合著经典 | ⭐⭐⭐⭐ |

---

## 个人特点

- **幽默风格**: 个人主页充满自嘲式幽默（如声称1980年获奥运射箭银牌）
- **设计哲学**: 追求简洁、实用的工程解决方案
- **开源贡献**: 持续维护多个开源项目
- **教育分享**: 通过演讲和博客分享经验教训

---

*信息截止日期：2026-04-08*

*主要信息来源：Wikipedia, GitHub, commandcenter.blogspot.com, go.dev/blog*