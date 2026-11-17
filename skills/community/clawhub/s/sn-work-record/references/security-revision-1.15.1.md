# 1.15.1 安全整改核对（未发布）

扫描来源：ClawHub 已发布的 `sn-work-record:1.15.0` 完整 ZIP；manifest 指纹 `3126e3a81e15d6cd22ab5aa031d9724b584fd79c730651c7e1225b2a071f8fd9`。skillspector.json 的 issueCount=13，issues 数组13项（含同一位置重复报告），ClawScan=suspicious；endor.json=null。未修改扫描器、规则、原始报告，也未声称1.15.1已获得远端 Clean。

|序号|扫描标识/位置|分析及处置|
|---|---|---|
|1|TP4 / SKILL.md|真实能力披露缺口。description 和正文不再宣称恢复可用；生产删除/恢复入口因无可靠服务端恢复契约暂禁。|
|2|E2 / runtime_bootstrap.py|真实过宽环境继承。改为按名称的最小白名单；依赖探测无OA密钥、无代理凭据，实际切换保留必需代理、CA、OA密钥、guard目录，不复制全环境。没有证据证明此前发生外传。|
|3|AST5 / runtime_bootstrap.py execve|已审查，保留。是显式 argv 的解释器切换，不是 shell 文本求值；候选是本地解释器、用户指定解释器和既有 venv。执行本地代码是功能边界，不证明注入。指定解释器应可信，不把替换成 subprocess 当作实质安全修复。|
|4|LP3 / SKILL.md|补充执行、网络、文件、环境及本地缓存的实际工具范围；不添加预授权工具或虚假权限沙箱承诺。宿主权限隔离未验证，仍作为剩余边界说明。|
|5|AST4 / oa_utils.py openssl|真实密钥进程参数暴露风险。改成匿名管道 fd 输入，子进程参数与环境不含 OA 密钥；保留旧 AES-256-CBC/base64/PBKDF2 格式。未轮换实际密钥或凭据。|
|6|TT2 / 同上|第5项同源重复，不是额外shell注入；同一修复覆盖。|
|7|AST3 / oa_utils.py __import__('sys')|常量标准库 sys，非动态不可信模块。已在文件顶部普通 import sys，现有写法冗余但无已证实风险；不为迎合规则改写或隐藏。|
|8|AST4 / runtime_bootstrap.py subprocess|固定 Python 探测代码、显式 argv、shell=False 默认，模块名作为数据传入，不拼接成代码。没有证实命令注入；实质问题是原先继承环境，已按第2项修复。|
|9|TM3 / tests/test_query_time_ranges.py|误报：`Auth=no` 是 `OAAuth=noisy` 子串，noisy 是离线测试中故意抛异常以验证脱敏的 fake。没有关闭认证/TLS或宽权限默认；保持测试不变。|
|10|SQP-3 / references/write-workflow.md|文档中文固定回复可改为按用户语言翻译示例，但属于输出政策范围外实质变更，暂不改，交父agent确认；与凭据外泄或删除安全无关。|
|11|AST7 / configure_personal_settings.py|getattr 目标由固定五字段元组限定，不接受任意属性名，不存在报告所称绕过访问控制证据。保持不变。|
|12|AST7 / submit_time_entry.py|getattr 目标由固定四字段元组限定，仅读取 argparse 选项；没有任意属性访问。保持不变。|
|13|AST7 / submit_time_entry.py|与第12项位置及内容重复，独立记录但不虚报额外缺陷；同一判定。|

## 新增保护与兼容性

生产删除/恢复暂禁：CLI 在读取凭据前拒绝，公共 update_time_entry 对任何非空 is_deleted 在网络前拒绝；无布尔绕过开关。deletion_guard 仅保留离线 fake 流程，不接入生产入口。既有 submission/amendment guard 不删除、迁移或重置。见 deletion-recovery.md。

服务端无可靠恢复契约，不得用 fake 成功承诺隔离或可逆。本地锁不是服务端 CAS，不能阻止其他客户端并发；不得通过另增记录或清除 guard 替代恢复。

白名单仅约束派生子进程/替换解释器；当前解释器满足依赖时直接返回，不净化现有进程，也不能撤销启动前注入，不构成宿主权限隔离。运行时切换不再继承 PYTHONPATH/PYTHONHOME/LD_PRELOAD、无关token；若用户有额外依赖定制，先评估兼容再精确扩充白名单，不回退全环境。OpenSSL密钥必须是单行且不超过1022 UTF-8字节；超限在启动子进程前拒绝。离线合成探针确认1022字节末字节有效，1024字节已出现截断，采用保守上限1022，不静默改变原密钥；超长/换行密钥需求需单独批准兼容策略。

## 验证口径

已为子进程环境白名单、密钥fd、离线 fake 删除备份/同ID恢复、API显式确认、CLI确认及锁内日期变化保存RED日志，并进行GREEN/全量离线回归。另覆盖旧密文读取、未知写结果不重发、超时/连接失败/401/中断、无备份恢复拒绝、业务字段冲突、并发提交锁和已有持久保护不改写。

测试日志与精确测试数由交付报告记录，不把编译成功或fake回归当作OA实测。未执行任何真实OA写操作，未发布1.15.1，未修改个人配置、真实凭据或既有持久保护文件。
