---
paths:
  - "dofiles/**/*.do"
  - "templates/**/*.do"
  - "scripts/run_*.sh"
  - "scripts/run_*.bat"
---

# Stata Reproducibility Protocol

> 源自 codex-stata-for-economists (陈铸)

**底线：** 任何人只要拥有本仓库和原始数据，就能用 **一条命令** 复现所有提交的表格和图形：
`bash scripts/run_pipeline.sh` 或 `python dofiles/00_master.py`。无需交互编辑，无需手动排序。

---

## 单一入口点

`dofiles/00_master.do` (或 `00_master.py`) 是整个流水线的唯一合法入口：

1. 设置项目级选项（`version`, `clear all`, `set more off`, `set varabbrev off`）
2. 可选运行依赖安装（ssc install → gated by flag）
3. 保存 `creturn list` 快照到 `logs/00_master_environment.log`
4. 按依赖顺序调用各阶段do文件，首个错误即停止
5. 若任意阶段失败，退出码非零

子do文件也应当可以**独立运行**以方便调试——不要求必须从 `master.do` 调用。

---

## 版本锁定

- 每个do文件顶部：`version 17`（或你分支的锁定版本）
- `master.do` 顶部的版本行后加注释记录上次验证的补丁级别：`// Validated on Stata 17.0 (rev. 2024-04-30)`
- 锁定用户自编命令版本：在 `logs/00_master_environment.log` 中通过 `which reghdfe`, `which esttab` 记录安装日期

---

## 随机性

- `set seed YYYYMMDD` 每个do文件**恰好一次**，在文件顶部
- 绝对不要在循环、`program` 函数或模拟内部设置seed——Stata的RNG状态是全局的，中途重设种子破坏可复现性
- Monte Carlo工作：在do文件头 **和** 生成的日志中记录bootstrap次数和种子

---

## 日志记录

每个do文件必须开启和关闭自己的日志：

```stata
capture log close
log using "logs/<stage>_<name>.log", replace text
... do-file body ...
log close
```

使用 `text` 格式（非 `smcl`）使日志可grep搜索，以支持 `log-validator` agent工作。

---

## 环境快照

`master.do` 写入 `logs/00_master_environment.log`：

```
* Stata version + flavor
display "Stata version: " c(stata_version)
display "Flavor: " c(flavor)
display "OS: " c(os)
display "Username: " c(username)
display "Date: " c(current_date) " " c(current_time)

* Key user-written commands
which reghdfe
which esttab
which ivreg2
which boottest
```

这个日志是审查者判断环境是否匹配的唯一人工产物。

---

## 反模式

| 反模式 | 为什么错 |
|:-------|:---------|
| 手动编辑 `data/derived/` | 破坏流水线；中间文件必须能从原始数据复现 |
| do文件中 `cd` 到绝对路径 | 只在本机有效 |
| 在控制台运行 `display r(N)` 作为结果 | 不在任何日志中；不可复现 |
| 手动编辑 `output/tables/*.tex` | 下次流水线运行覆盖修改；把调整写在do文件的 `esttab` 选项中 |
| 从子do文件内部调用 `master.do` | 无限递归风险；混淆依赖方向 |
