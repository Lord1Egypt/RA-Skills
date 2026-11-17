# 发布检查清单

在创建 Git tag 或上传前执行 `python tests/validate.py --strict`。任何失败均阻止发布。

1. `VERSION`、`SKILL.md`、README、CHANGELOG、registry、配置与 schema 版本一致。
2. README 的 SHA256 与当前 `install.sh`、`install.ps1` 一致。
3. 安装器支持 `--dry-run`，不含递归删除回退，遇到本地变更或快进失败时保留目录并中止。
4. 所有外部搜索默认关闭，且每次执行需要明确同意。
5. GitHub 比较与安装作用域协议完整，推荐不会省略证据、许可证、兼容性或目标路径。
6. YAML 解析、评分权重、平台配置、流程引用和数据目录验证通过。
7. 输出契约通过：默认只读、未知数据不回填、报告包含事实状态和证据、执行前已明确确认。
8. 最后创建与 `VERSION` 一致的 Git tag；实际发布仍需独立确认。
