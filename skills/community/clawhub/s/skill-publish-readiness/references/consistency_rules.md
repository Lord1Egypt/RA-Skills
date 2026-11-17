# 一致性与模式升级规则

## 身份一致性

- 目录名与稳定 slug 应对应；展示名可以更易读，但不能冒充另一个包
- `description`、正文、示例和模板只能承诺实际提供的能力
- frontmatter、`_meta.json`、CHANGELOG 的当前版本必须一致，并高于 registry latest
- Plugin 的 package name、scope、owner 与 manifest 身份必须相容

## 依赖一致性

- 正文使用的命令应在 `requires.bins` 或安装说明中体现
- 代码读取的环境变量应与 `requires.env`、`primaryEnv` 或 `envVars` 一致
- 示例、默认值与权限说明不得互相矛盾

## 页面一致性

- 标题、摘要、目标用户、场景和真实示例围绕同一价值主张
- “自动”“完整”“安全”等承诺必须定义边界
- categories/topics、示例与 CHANGELOG 属于 quick 的发现性和信任检查

## auto 升级到 deep

命中任一条件即升级：

- P0 或疑似安全问题
- skill/plugin 类型不明
- slug、owner、scope 或版本证据冲突
- 涉及环境变量、权限、外部输入或执行脚本
- 用户要求完整报告、差异化评分或可追溯证据
- quick 无法给出可靠结论

升级必须在报告中说明触发信号；不得静默扩大范围。
