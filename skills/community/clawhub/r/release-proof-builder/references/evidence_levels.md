# 发布证据等级

## E0 未发布

证据：

- 只有本地文件
- 或本地提交尚未进入远端

不能声称：

- 已推送
- 已上架
- 可下载

## E1 已推送

证据：

- 本地 HEAD 与 GitHub 远端 HEAD 一致

仍需证明：

- 发布 workflow 是否执行
- registry 是否接受

## E2 流水线成功

证据：

- 发布 workflow 已处理目标提交或目录
- 对应 workflow 已完成且结论为成功

不满足 E2：

- workflow 仅被触发、仍在运行、失败、取消或跳过

仍需证明：

- 目标 slug 是否进入 registry

## E3 已上架且审核正常

证据：

- `clawhub inspect` 能读取目标 slug
- 版本、展示名和元数据符合预期
- `moderation.verdict` 明确为 `clean`

不满足 E3：

- moderation 待处理、字段缺失或 verdict 非 `clean`

仍需证明：

- 是否能在干净目录中安装

## E4 可安装

证据：

- 在隔离目录中完成安装
- 安装后的 `SKILL.md` 与目标版本一致
- 核心配套文件存在
- 记录安装时间、slug、版本和验收原因
- 标记验收时段及紧随其后的 downloads / installs 增量为主动安装污染
- 以安装完成时间重新建立自然观察起点

可以声称：

- 已上线
- 可下载
- 已完成安装验证
