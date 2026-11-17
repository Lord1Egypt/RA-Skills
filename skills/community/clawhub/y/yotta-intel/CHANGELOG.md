# Changelog

## v0.2.4 (2026-11-05)

- 发布包排除测试脚本；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

# 更新日志

## v0.2.3 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.2.2 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。
- 自带安装器测试（`test/install.test.js`）更新为统一行为断言。

## v0.2.1 (2026-09-25)

维护性发布：安装器加固 + README 锁定版本。

- 安装器：拒绝对符号链接目标写入、目标不是目录时拒绝、不做整目录删除。
- README（中英）：安装命令改为锁定版本写法（去掉 `@版本` 即跟随最新）。
- 输出示例与 references 头部版本号同步 0.2.1。
- 修复：IPv4 前导零写法（`010.000.000.001`）归一为 `10.0.0.1` —— Python 3.9.5 起
  `ipaddress.IPv4Address` 拒绝前导零八位组，旧引擎会静默丢掉该地址；`999.1.1.1` 仍判非法。

## v0.2.0 (2026-09-09)

- 评测完善批 2：新增 references/faq.md（12 条常见问题 + 速查索引 + 安装排障）；SKILL.md 增加 FAQ 速查节。
- 安装器错误处理：用法/目标/安装错误统一退出码与修复建议；新增 test/install.test.js。
- package.json 补 npm test 脚本；版本对齐 0.2.0（package / SKILL / CHANGELOG / CLI）。

## v0.1.1 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-intel --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-intel.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.1.1。
- 无功能变更（仅文档与版本同步）。

## v0.1.0 (2026-08-27)

初始发布：

- 引擎：零依赖（Python 3.8+ 标准库）威胁情报 IOC 提取与规范化。
- 七类 IOC：IPv4 / IPv6 / 域名 / URL / 邮箱 / 哈希（MD5/SHA1/SHA256/SHA512）/ CVE 编号。
- defang / refang：识别 `hxxp`、`[.]`、`(.)`、`[dot]`、`[:]`、`[@]`、`[/]` 等常见去活性写法并还原；
  每条结果自带统一 defang 安全形态。
- 归一化：域名小写 + IDN punycode、URL 去默认端口 / 去 fragment / 保留 userinfo、哈希小写、IPv6 压缩写法。
- 去重计数：`(类型, 规范值)` 为键合并，记录 count / first_line / snippet。
- 误报控制：域名 TLD 白名单 + 文件名过滤（README.md / test.py 不算域名）+ 中文标点截断 + 哈希长度校验。
- 四种输出：text / JSON / CSV / STIX-lite（STIX 2.1 Bundle + indicator pattern，uuid5 确定性）。
- 测试：103 个用例全绿；含 CLI 端到端（stdin / 文件 / 退出码）。
- 文档：SKILL.md + README 中英双版 + references（ioc-spec / defang-rules / stix-lite-spec）。
