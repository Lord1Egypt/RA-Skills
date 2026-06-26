# 拒选词表 — Rejection Word Lists

三重拒选防线使用的关键词。守卫在 _is_noise() 方法中。

## 防线0：信息查询意图检测 (INFO_SEEK_WORDS)

query 命中这些词 → 认为是纯信息查询 → 不进 skill 路由，直接走 L0 工具。

```
查  找  搜  搜索  检索  查找  查询
search  lookup  find
最新  最近
有什么  有哪些  告诉我
是什么  什么是  怎么  如何  为什么
哪个  哪种  哪个好  区别  对比
天气  时间  现在几点
多少钱  免费  收费  价格
教程  怎么用
用法  用量  用法用量  剂量  吃什么  吃多少  吃几
在哪  哪里有
症状  病因  治疗  能治  能不能
副作用  不良反应  注意事项
```

## 强技能意图豁免 (STRONG_SKILL_WORDS)

即使含有信息查询词，只要命中这些 → 放行，认为是真正的技能需求。

```
# Meta/系统综述
系统性综述  系统综述  systematic review
meta分析  meta-analysis  metaanalysis

# 文献计量
文献计量  bibliometric  bibliometrics

# 写作/论文
写  撰写  写作  做一篇  论文  manuscript  draft  草稿

# 文献
文献检索  文献搜索  文献  literature  pubmed

# 孟德尔/基因
prisma  孟德尔  gwas  mendelian  mendelian randomization  mr分析

# 图表
画图  图表  可视化  森林图  visualization  forest plot  figure

# 邮件
发邮件  send  email

# 系统操作
挂载  mount  重启  restart  debug  审查代码  重构  git

# 任务
列出来  列出  显示  展示  list  任务  task  待办  todo

# 评审/引用
评审  审稿  review  引用  参考文献  citation  vancouver  指南  guideline

# 生物信息
差异表达  转录组  基因
```

## 动作短语豁免 (ACTION_PHRASES)

query 开头包含这些短语 → 判断为指令而非查询，豁免拒选。

```
列出来  列一下  列个  列表  显示  展示  列出  给我
发给  发邮件  发一封  做一篇  做一
画一个  画个  写一篇  写一
查一下  查一
把
```

## 防线A+B：任务词检测 (TASK_WORDS)

query 中的任务词与 skill 能力匹配。无匹配 + 分数低 → 噪声拒绝。

```
# Meta/系统综述
系统性综述  系统综述  系统评价  systematic review
meta分析  meta-analysis  metaanalysis  meta

# 文献计量
文献计量  bibliometric  bibliometrics

# 文献检索
文献检索  文献搜索  搜索文献  检索文献
literature search  literature review  prisma

# 指南/综述
指南  guideline  guidelines  综述  review

# 论文/写作
论文  article  paper  manuscript  写  撰写  写作  draft

# 分析/统计
分析  analysis  统计  statistics

# 图表
图表  chart  可视化  visualization  画图  森林图  forest plot  figure  plot

# 邮件
邮件  email  mail

# 下载
下载  download  pdf

# 基因/孟德尔
gwas  基因  gene  genetics  孟德尔  mr分析  mendelian

# R语言
r语言  rstats  rstudio

# 引用
引用  参考文献  reference  citation  apa  vancouver  bibliography

# 评审
评审  审稿  peer review

# 系统操作
挂载  mount  重启  restart  debug  调试  bug

# 任务
任务  task  todo  待办  优先级  priority  分配  schedule

# 列表/Git
列出来  列出  列表  list  git  push  commit

# 审查
审查  review code
```
