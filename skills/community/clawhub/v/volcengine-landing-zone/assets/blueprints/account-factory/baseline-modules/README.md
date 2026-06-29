# Account Factory Baseline Modules

本目录用于保存 `Account Factory` 的 baseline 预置模块。

## 设计原则

- 预置模块与用户自定义 Terraform 模块在 baseline `*.baseline.json` 文件中使用同一种 `modules` 引用模型
- 两者的区别只在于 `source` 指向的位置不同
- 预置模块用于降低首次创建 baseline 的门槛

## 当前模块

- `network-cross-account-connectivity`
