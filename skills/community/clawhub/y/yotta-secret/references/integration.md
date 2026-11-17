# 联动与使用姿势（yotta-secret 元钥）

## 与元史（yotta-logs）脱敏词库共享

- **分工**：元钥 = 源头（提交 / 发布前扫描源码与 git 历史找泄露）；
  元史 = 输出（检索会话日志时默认 redact 脱敏，避免日志二次带出密钥）。
- **同源词库**：元史 yotta_logs.py 的 redact() 词库（sk-/rk-/pk-、gh[pousr]_、xox[baprs]-、
  AKIA/ASIA、JWT、Bearer、PEM、token/password 等赋值、40+ 位长 token）是元钥规则集的子集；
  元钥 mask 子命令行为与元史 redact 一致，规则为其超集。
- **维护**：改词库时两边同步（元钥 references/rules.md ↔ 元史 scripts/yotta_logs.py redact()），
  并保持 mask 与 redact 对同一文本输出一致（测试覆盖）。

## 与元盾（yotta-guardian）联动

- **提交 / 写入前门禁**：先跑 scan，退出码 1 = 发现疑似密钥 → 拦截并提示人工处理；
  确属误报用 --exclude / --types 收窄，或人工复核后放行。
- **审计留痕**：scan --format json 输出可直接交给元盾 audit 或 CI：
  - 示例：scan --path . --format json --output secret-report.json，脚本按退出码终止提交 / 构建。
- **配合意图验证**：元盾 check write 评估写操作，元钥 scan 评估内容本身，两者叠加
  （先内容后动作）可覆盖「写入前检查」场景。

## 使用姿势

### 场景一：提交前自检

    python3 scripts/yotta_secret.py scan --path . --types cloud,private_key,credential
    # 退出码 1 时：定位 findings（file:line + commit），处理后再提交

### 场景二：历史泄露溯源

    python3 scripts/yotta_secret.py scan --git --path repo/ --format json --output leak.json
    # findings 带 commit 与 path_in_commit，可定位是哪次提交引入

### 场景三：分享前脱敏

    python3 scripts/yotta_secret.py mask --path notes.txt --output safe.txt
    # 与元史 redact 同源；URL 保留原文，密钥打码

### 场景四：单值校验

    python3 scripts/yotta_secret.py verify --value ghp_xxxxxxxxxxxxxxxx
    # likely_secret / high_entropy / no_match 三态

## 结果处理建议（给用户的决策纪律）

- 所有结果只是「疑似密钥」：是否真实、是否已泄露需人工核实；
- 确认真实泄露：立即轮换 / 吊销 → 从代码与历史中移除 → 排查日志 / 工单是否已带出（可用元钥 mask / 元史 redact 复查）；
- 不要只删文件：git 历史里的旧版本也要处理（--git 扫描可复查）。
