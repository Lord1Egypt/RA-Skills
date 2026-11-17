#!/usr/bin/env node
// yotta-memory（元忆）: 有权限边界的文件式智能体记忆 CLI（零依赖）
// v0.4.0 新增：lan（Windows 计划任务开机自启 serve）/ init --dir（显式指定位置）/ serve --stdio（本地零进程模式）/ MCP 工具补 reindex/export/import
// v0.5.0 新增：隐私硬隔离——私密物理分目录 private/<agent_id>/{prefs,bounds,commits}/ + 关闭 --agent 越权读 + 私密写跨智能体需 --unsafe + 禁 shell 直读写（文档红线）
// v0.4.2 新增：iam/whoami 智能体身份自注册（agents.json 唯一性）+ 自我档案 PREF + 私密记忆须声明 owner
// v0.5.3 新增：CLI 选项可前置（--agent 等允许放在子命令前，不再误报"未知命令"）/ lan enable 成功补"服务不会立刻启动"提示（v0.5.2 lan 引号修复无回归）
// v0.5.4 新增：lan enable 在非管理员（schtasks Access denied）时自动降级为用户级 Startup 静默自启（VBS sh.Run 窗口0 + autostart.cmd，node 路径 process.execPath 自动探测）；lan disable/status 同时管理计划任务与 Startup 双机制
// v0.6.0 新增：profile（用户画像聚合，零推断）/ context（开工上下文包）/ iam 扩展（--name/--user/--relationship）/ remember --verify（写后回读）与 --no-hint（关闭类型启发式提示）+ SKILL「记忆守则」
// v0.6.1 新增：context --budget（token 预算，近记忆按剩余预算放行）/ context 内嵌「多智能体接入铁律」段 / remember --source/--weight（来源 + 重要性权重，去重 weight 取 max）/ 近期记忆排序融合 importance（confidence×recency+updated+weight+immutable）
// v0.6.3 修复：lan 开机自启 VBS 自愈——VBS 内联 autostart.cmd 内容，启动时自动重建 .cmd（根治 80070002：wscript 找不到被引用启动文件）
// v0.6.4 新增：lan 命令扩展 Linux——systemd 用户单元（systemctl --user enable/start，登录自启；--onstart 附加 loginctl enable-linger 开机即启）/ systemd 不可用时自动降级用户 crontab @reboot；lanPlatform 测试钩子（YOTTA_LAN_PLATFORM）
// v0.6.5 修复：recall/context 对同一文件显示 2 条——projectRoot 与 userRoot 指向同一目录（如 cwd=home 或其父）时同一索引被遍历两次；新增 memoryRoots() 唯一化根，hasGrant/recallCore/forgetCore/cmdReindex/contextCore 统一走 memoryRoots()
// v0.7.0 新增：私密区机制级加密（AES-256-GCM 信封加密 + PBKDF2 主密钥 + 恢复钥匙）/ 每 owner 加密索引 / 用户查看平台 yotta-memory view / migrate 迁移 / reset-password / key 授权 / context 收工纪律 / init 新建默认加密（--no-encrypt 降级）
// v0.8.0 新增：自我学习/自我进化/自我提升——语义检索（同义词/拼音/字段加权/模糊 + 可选 embedding 插件协议预留）/ feedback 显式反馈闭环（weight/confidence/feedback_net 演化）/ maintain 规则层自组织（统一效用分 utility + 归档/遗忘/去重，默认 dry-run）/ distill 心理日志蒸馏（启发式统计/主题画像/知识地图 + 可选 --model）
// v0.6.2 修复：remember --verify 写后回读改为直查索引 + 权限判定 + 召回匹配性（不再依赖 recall top-N 排序，消除泛化 subject 下偶发误报「回读未命中」）
// v0.12.2 新增：开工 doctor（根目录/密钥库/索引/身份/最近备份）+ 破坏性操作前事务快照门（maintain/consolidate/merge/archive/purge）
'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');
const http = require('http');
const net = require('net');
const zlib = require('zlib');
const child_process = require('child_process');
const { AsyncLocalStorage } = require('async_hooks');

const VERSION = '0.24.3';
const CLI_VALUE_OPTS = new Set(['--type', '--limit', '--days', '--out', '--owner', '--agent', '--agent-id', '--agent-key', '--agent-key-file', '--plugin-data', '--threshold', '--scope', '--host', '--port', '--dir', '--name', '--user', '--relationship', '--source', '--weight', '--budget', '--password', '--new-password', '--recovery-key', '--recovery-key-out', '--reason', '--merge', '--model', '--subject', '--embedding', '--focus', '--embedding-timeout', '--min-age', '--min-idle', '--max-utility', '--min-group', '--period', '--to', '--id', '--time', '--tools', '--mcp-config', '--skill-dir', '--year', '--evalset', '--k', '--seed', '--bootstrap', '--gate', '--against', '--template', '--path', '--from', '--from-plan', '--batch', '--profile']);
const CLI_FLAG_OPTS = new Set(['--project', '--all', '--unsafe', '--no-auth', '--stdio', '--onstart', '--from-current', '--restart', '--force', '--attach', '--allow-same-volume', '--verify', '--no-hint', '--encrypt', '--no-encrypt', '--password-stdin', '--json', '--manual', '--skip-schedule', '--useful', '--useless', '--undo', '--dry-run', '--apply', '--purge', '--dedup', '--batches', '--propose', '--audit', '--capacity', '--rules', '--explain', '--semantic', '--runtime', '--ablate', '--timing', '--baseline', '--probe', '--quarantine', '--restore', '--no-usage', '--yes', '--keep-memories', '--keep-identity', '--stats', '--include-flat', '--no-policy', '--policy-candidates']);

function helpOption(flag, arg, what, when, caution) {
  return { flag: flag, arg: arg || '', what: what, when: when || '', caution: caution || '' };
}
function helpSub(name, usage, what, when, options) {
  return { name: name, usage: usage || name, what: what, when: when || '', options: options || [] };
}
const HELP_MODEL = [
  { group: '核心记忆', commands: [
    { name: 'init', usage: 'init [--project | --dir <目录>] [--attach | --encrypt | --no-encrypt] [--password-stdin] [--recovery-key-out <文件>]', what: '初始化记忆库', when: '第一次使用，或把已有记忆库接入当前项目 / 智能体时', options: [
      helpOption('--project', '', '把记忆库放在当前项目根目录', '只希望这个项目使用这份记忆时', ''),
      helpOption('--dir', '<目录>', '指定记忆库位置', '不想用默认用户级位置时', ''),
      helpOption('--attach', '', '接入已有记忆库', '目录里已经有一份库，不要重新初始化时', ''),
      helpOption('--encrypt', '', '新建加密记忆库', '想显式要求加密时', ''),
      helpOption('--no-encrypt', '', '新建明文记忆库', '只做临时实验、明确接受明文风险时', '私密记忆会以明文落盘；正式使用不要加这个选项'),
      helpOption('--password-stdin', '', '从标准输入读取主口令', '脚本或非交互环境设置口令时', '只适合纯 ASCII 口令；中文口令请交互输入'),
      helpOption('--recovery-key-out', '<文件>', '把恢复钥匙写到文件', '新建或迁移后需要立刻保存恢复钥匙时', '恢复钥匙能重置主口令，必须单独妥善保管'),
      helpOption('--force', '', '允许覆盖已存在的运行文件', '确认要替换旧运行文件时', '可能覆盖现有内容；先确认目标路径和备份'),
    ] },
    { name: 'remember', usage: 'remember <type> <subject> <statement> [选项]', what: '写入一条记忆', when: '出现事实、偏好、边界或承诺，需要跨会话保留时', options: [
      helpOption('--source', '<来源>', '记录这条记忆的来源', '需要以后追溯「谁说的 / 哪来的」时', ''),
      helpOption('--weight', '<数值>', '设置重要性权重', '这条记忆比普通条目更重要或更次要时', ''),
      helpOption('--verify', '', '写完立刻回读校验', '关键记忆担心写失败或索引异常时', ''),
      helpOption('--no-hint', '', '关闭类型启发式提示', '已经明确知道类型、不想看额外提醒时', ''),
    ] },
    { name: 'recall', usage: 'recall [关键词] [选项]；search 是别名', what: '检索记忆', when: '开工恢复上下文、找旧决定或确认边界时', options: [
      helpOption('--type', '<类型>', '只查某一种类型', '只想看 FACT / PREF / BOUND / COMMIT 中的一类时', ''),
      helpOption('--limit', '<条数>', '限制返回条数', '结果太多、只需看最相关的几条时', ''),
      helpOption('--agent', '<id>', '声明当前智能体身份或按智能体筛选', '当前会话身份需要明确声明时', '声明身份不等于获得跨读权限'),
      helpOption('--owner', '<id>', '指定记忆归属者', '查询某个 owner 的私密记忆时', '读其它智能体的私密区需要授权'),
      helpOption('--all', '', '跨 owner 检索', '确实需要看所有可读范围内的记忆时', '跨读其它智能体私密仍未授权会拒绝并提示'),
      helpOption('--unsafe', '', '跳过越界读取保护', '只有用户明确授权做隔离排查时', '会放宽私密读取边界，日常不要使用'),
      helpOption('--explain', '', '输出命中理由和效用分项', '想理解为什么这条记忆被排到前面时', ''),
      helpOption('--semantic', '', '显式开启语义检索', '想强制使用同义词 / 拼音 / 模糊匹配时', ''),
      helpOption('--embedding', '<命令>', '临时指定本地 embedding 插件命令', '这次检索想使用自定义本地向量命令时', '只在本地执行，不会把记忆上传远端'),
      helpOption('--embedding-timeout', '<毫秒>', '设置 embedding 插件超时', '插件较慢或需要快速失败时', ''),
      helpOption('--year', '<yyyy>', '只检索指定年份的记忆', '库很大、只想在某一年的记忆里找时', '可重复传多次；不传则检索全部年份'),
      helpOption('--no-usage', '', '本次不记录命中打点', '只想临时关闭使用统计时', '只影响这一次调用，不改配置'),
    ] },
    { name: 'forget', usage: 'forget <记忆 id> [选项]', what: '删除一条记忆', when: '确认某条记忆不应继续保留时', options: [
      helpOption('--reason', '<原因>', '记录删除原因', '需要留下为什么删除的审计线索时', ''),
      helpOption('--unsafe', '', '跳过越界删除保护', '只有获得明确授权处理隔离库时', '会放宽删除边界，误删风险很高'),
    ] },
    { name: 'rename', usage: 'rename <记忆 id> <新文件名> [选项]', what: '给单条记忆改名（内容与身份不变）', when: '平铺 / 分层出现同序号冲突、或想整理文件名时', options: [
      helpOption('--dry-run', '', '只预览，不改库', '想先确认改到哪个文件名时', '预演只读，不改任何文件'),
      helpOption('--reason', '<原因>', '记录改名原因', '需要留下为什么改名的审计线索时', ''),
      helpOption('--unsafe', '', '跳过越界写入保护', '只有获得明确授权处理隔离库时', '会放宽写入边界，谨慎使用'),
    ] },
    { name: 'archive', usage: 'archive [选项]', what: '把低价值或过期记忆归档', when: '库变大，想让旧记忆退出主检索但保留可回溯时', options: [
      helpOption('--days', '<天数>', '按未使用天数判断归档', '想调整「多久没用才归档」时', ''),
      helpOption('--threshold', '<数值>', '按效用分阈值判断归档', '想调整「用得少不少」时', ''),
      helpOption('--dry-run', '', '只预览归档结果', '先看会动哪些记忆，再决定是否执行时', '预演只读，不改任何文件'),
      helpOption('--force', '', '关闭冷却期与标签常青豁免', '确认新条目或 evergreen / pinned 条目也要归档时', 'immutable 与 BOUND 仍然豁免；先确认清单'),
    ] },
    { name: 'backup', usage: 'backup <子命令> [选项]', what: '备份、恢复和演练记忆库', when: '配置自动备份、创建备份、恢复误删或验证备份可用时', subcommands: [
      helpSub('volumes', 'volumes [--json]', '列出可用备份卷', '想知道备份会写到哪里时', [helpOption('--json', '', '输出 JSON', '脚本处理备份卷列表时', '')]),
      helpSub('setup', 'setup [--manual] [--skip-schedule] [--allow-same-volume]', '配置备份目录和计划任务', '第一次启用自动备份时', [
        helpOption('--manual', '', '只配置目录，不改计划任务', '由你自己管理定时任务时', ''),
        helpOption('--skip-schedule', '', '跳过自动计划任务', '只想先建备份目录、不注册系统计划时', ''),
        helpOption('--allow-same-volume', '', '允许备份和记忆库在同一磁盘卷', '只有临时测试且接受同盘故障风险时', '同盘备份无法防止整盘损坏；正式使用必须换独立盘'),
      ]),
      helpSub('status', 'status [--json]', '查看备份健康状态', '开工检查或排查备份是否正常时', [helpOption('--json', '', '输出 JSON', '脚本读取备份状态时', '')]),
      helpSub('ensure-daily', 'ensure-daily [--json]', '确保每日备份任务存在', '修复自动备份任务缺失时', [helpOption('--json', '', '输出 JSON', '自动化里检查任务时', '')]),
      helpSub('schedule', 'schedule <on|off|status> [--time <HH:MM>]', '管理每天自动备份', '设置或关闭每日备份时', [helpOption('--time', '<HH:MM>', '设置每日备份时间', '默认 03:30 不合适时', '')]),
      helpSub('create', 'create [--json]', '立即创建一份备份', '手动留一个恢复点、或改库前先备份时', [helpOption('--json', '', '输出 JSON', '脚本读取新备份 id 时', '')]),
      helpSub('list', 'list [--json]', '列出备份历史', '选一个恢复点时', [helpOption('--json', '', '输出 JSON', '脚本读取备份列表时', '')]),
      helpSub('doctor', 'doctor [--json]', '检查备份目录和文件是否健康', '怀疑备份损坏或磁盘异常时', [helpOption('--json', '', '输出 JSON', '自动化体检时', '')]),
      helpSub('restore', 'restore <id> --to <目录> [--force]', '从备份恢复到指定目录', '误删、迁移或需要验证恢复内容时', [
        helpOption('--to', '<目录>', '指定恢复目标目录', '恢复时必须显式给出目标位置', ''),
        helpOption('--id', '<id>', '指定备份 id', '不用位置参数、想显式点名备份时', ''),
        helpOption('--force', '', '允许覆盖非空目标目录', '确认目标可以覆盖时', '可能覆盖目标目录现有文件；先确认目标和备份'),
      ]),
      helpSub('drill', 'drill <id> [--to <目录>] [--probe] [--against <库>] [--password <口令> | --recovery-key <钥匙>] [--password-stdin]', '恢复演练', '验证备份真的能恢复时', [
        helpOption('--to', '<目录>', '指定演练恢复目录', '演练时使用临时空目录更安全', ''),
        helpOption('--id', '<id>', '指定备份 id', '不用位置参数、想显式点名备份时', ''),
        helpOption('--probe', '', '恢复后自动跑恢复 / 迁移基线探针', '想确认恢复副本的身份、近期条目与操作规则都可用时', '复制的索引与访问计数不变，探针只读'),
        helpOption('--against', '<库路径>', '指定对比库做差集校验', '想确认备份没有落后于源库、迁移没有丢条目时', '对比库只读；差集缺失会列出清单并非零退出'),
        helpOption('--password', '<口令>', '直接提供主口令（解密演练副本里的私密记忆）', '自动化环境无法交互输入时', '命令行会留下痕迹；优先交互输入'),
        helpOption('--recovery-key', '<钥匙>', '用恢复钥匙解密演练副本', '忘记主口令时', '恢复钥匙只能由用户本人保管'),
        helpOption('--password-stdin', '', '从标准输入读取主口令', '脚本 / 非交互环境演练时', '只适合纯 ASCII 口令；中文口令请交互输入'),
      ]),
    ] },
    { name: 'doctor', usage: 'doctor [选项]', what: '开工可靠性检查', when: '开工前、异常后或升级后确认系统状态时', options: [
      helpOption('--runtime', '', '同时检查 CLI、current、MCP、进程和技能副本是否漂移', '升级后版本对不上时', ''),
      helpOption('--mcp-config', '<文件>', '补充检查指定 MCP 配置文件', '排查宿主 MCP 是否指向旧运行时', ''),
      helpOption('--skill-dir', '<目录>', '补充检查指定技能副本目录', '排查技能目录是否落后', ''),
      helpOption('--baseline', '', '追加恢复 / 迁移基线探针（六类，只读）', '恢复、迁移或升级后要确认记忆真的可用时', '探针失败会列出缺失清单并以非零状态退出'),
      helpOption('--against', '<库路径>', '探针的对比库（通常是迁移前的源库）', '要确认目标库没有丢条目时', '差集条目缺失会逐条列出'),
      helpOption('--template', '<文件>', '用模板声明显式期望（owner / 最小条数 / 类型条数 / 查询）', '有明确验收清单、要按清单核对时', '模板只加严判定，不会放宽或改写探针'),
      helpOption('--json', '', '输出 JSON', '脚本或自动化读取体检结果时', ''),
    ] },
    { name: 'index', usage: 'index --stats [--json]', what: '只读分析公共索引体积、字段占比与 gzip 分片预估', when: '判断是否需要升级索引格式、压缩或分片时', options: [
      helpOption('--stats', '', '输出索引统计报告', '分析索引膨胀根因与预估压缩收益时', '只读：不重建索引，不改任何记忆文件'),
      helpOption('--json', '', '输出 JSON', '脚本读取字段体积、token 与压缩预估时', ''),
    ] },
    { name: 'layout', usage: 'layout <plan|apply|rollback> [选项]', what: '预演、执行或回滚日级目录重平衡', when: '单个年/月目录文件数超过阈值、需要可回滚迁移时', subcommands: [
      helpSub('plan', 'plan [--threshold <数量>] [--include-flat] [--out <文件>] [--json]', '生成布局迁移计划', '先确定会移动哪些文件、目标路径和冲突时', [
        helpOption('--threshold', '<数量>', '目录文件数超过该值时进入计划', '默认阈值不合适时', ''),
        helpOption('--include-flat', '', '把旧平铺根也纳入计划', '确认愿意迁移旧平铺文件时', '默认只处理年/月桶，旧平铺保持原位'),
        helpOption('--out', '<文件>', '把计划写到指定位置', '需要把计划交给维护窗口审阅时', ''),
        helpOption('--json', '', '输出 JSON', '自动化读取候选、操作与冲突时', ''),
      ]),
      helpSub('apply', 'apply --from-plan <文件> --yes [--json]', '执行已审阅的布局迁移计划', '维护窗口内确认计划无冲突后', [
        helpOption('--from-plan', '<文件>', '指定布局迁移计划文件', '执行 plan 生成的计划时', ''),
        helpOption('--yes', '', '跳过交互确认', '计划已审阅且维护窗口已开始时', '会移动记忆文件；失败时自动逆序回滚'),
        helpOption('--json', '', '输出 JSON', '自动化执行迁移时', ''),
      ]),
      helpSub('rollback', 'rollback --batch <id> --yes [--json]', '按 journal 回滚一次布局迁移', '迁移后发现问题、需要恢复原路径时', [
        helpOption('--batch', '<id>', '指定布局迁移批次', '找回滚 journal 时', ''),
        helpOption('--yes', '', '跳过交互确认', '已确认要恢复原布局时', '会移动记忆文件；按 journal 逆序恢复'),
        helpOption('--json', '', '输出 JSON', '自动化回滚时', ''),
      ]),
    ] },
    { name: 'maintain', usage: 'maintain [选项]', what: '记忆自组织：归档、遗忘候选、去重和合并', when: '定期清理低价值记忆、合并重复条目时', options: [
      helpOption('--capacity', '', '查看容量水位与淘汰 / 晋升建议', '库变大，想看哪些条目值得清理或提升时', '只读报告，不会自动归档或改权重'),
      helpOption('--rules', '', '查看重复踩坑 → 建议升级为规则的清单', '同一类问题反复出现、想把它固化成 BOUND 规则时', '只读报告，不自动写规则；阈值走 config maintain_rule_min_hits'),
      helpOption('--dedup', '', '只做重复检查并给置信度', '想先看哪些条目重复时', ''),
      helpOption('--apply', '', '真正执行，而不是只预览', '确认预览结果后要落盘时', '会改动记忆库并创建事务快照；先跑 dry-run'),
      helpOption('--purge', '', '对遗忘候选执行真删', '确认候选确实不再需要时', '真删不可逆；通常先用归档而不是 purge'),
      helpOption('--dry-run', '', '只预览，不改库', '默认行为，想显式表达时', ''),
      helpOption('--min-age', '<天数>', '设置遗忘候选最小年龄', '想调整「放多久才考虑遗忘」时', ''),
      helpOption('--min-idle', '<天数>', '设置遗忘候选最小闲置天数', '想调整「多久没碰才考虑遗忘」时', ''),
      helpOption('--max-utility', '<数值>', '设置效用分上限', '想调整「用得少到什么程度」时', ''),
      helpOption('--min-group', '<条数>', '设置重复组最小条数', '调整查重灵敏度时', ''),
      helpOption('--merge', '<id列表>', '显式合并指定条目', '已经确认这些条目可以合并时', ''),
      helpOption('--json', '', '输出 JSON', '自动化处理维护结果时', ''),
    ] },
    { name: 'consolidate', usage: 'consolidate [--propose | --apply | --undo <batch> | --batches] [选项]', what: '把旧记忆压缩成周期摘要', when: '库很大，想把超龄、闲置、低效用条目压成摘要时', options: [
      helpOption('--propose', '', '只输出结构化候选报告（默认行为）', '想先审阅会压缩哪些内容、保留与回滚口径时', '不写盘；等价于直接运行 consolidate'),
      helpOption('--apply', '', '真正执行压缩', '确认 propose 报告后要落盘时', '会改动记忆库并创建事务快照；先预览'),
      helpOption('--yes', '', '非交互确认执行', '脚本或自动化环境里已经审阅过 propose 报告时', '跳过交互确认；破坏性操作，务必先看报告'),
      helpOption('--undo', '<batch>', '回滚一个摘要批次', '压缩后发现结果不合适时', ''),
      helpOption('--batches', '', '列出历史批次', '想找回滚批次号时', ''),
      helpOption('--period', '<天数>', '设置摘要周期', '想改变摘要覆盖的时间跨度时', ''),
      helpOption('--threshold', '<数值>', '设置候选效用阈值', '想调整进入摘要的门槛时', ''),
      helpOption('--min-age', '<天数>', '设置候选最小年龄', '想调整「放多久才进入摘要」时', ''),
      helpOption('--min-idle', '<天数>', '设置候选最小闲置天数', '想调整「多久没碰才进入摘要」时', ''),
      helpOption('--max-utility', '<数值>', '设置候选效用分上限', '想调整「用得少到什么程度」时', ''),
      helpOption('--min-group', '<条数>', '设置摘要组最小条数', '调整合并力度时', ''),
      helpOption('--json', '', '输出 JSON', '自动化处理摘要结果时', ''),
    ] },
    { name: 'distill', usage: 'distill [--model <命令>] [选项]', what: '把心理日志蒸馏成统计摘要、主题画像和知识地图', when: '想把长期记录整理成更高层的自我画像时', options: [
      helpOption('--model', '<命令>', '调用本地外部模型辅助蒸馏', '需要更高质量摘要、且已准备本地模型命令时', '命令在本地执行；不要指向会外传原文的服务'),
      helpOption('--subject', '<标题>', '指定蒸馏输出主题', '想给这次摘要一个固定标题时', ''),
      helpOption('--owner', '<id>', '指定蒸馏归属的智能体', '想蒸馏某个 owner 的记忆时', '默认当前身份；跨 owner 私密仍按 owner 门跳过'),
      helpOption('--out', '<路径>', '把蒸馏报告导出到指定路径', '想把报告放到自定义位置时', '不指定时按归属写入 distills 目录'),
      helpOption('--json', '', '输出 JSON', '自动化处理蒸馏结果时', ''),
    ] },
    { name: 'feedback', usage: 'feedback <记忆 id> [--useful | --useless | --undo]', what: '记录记忆是否有用', when: '一条记忆刚刚帮助了你，或明显误导了你时', options: [
      helpOption('--useful', '', '记为有用', '这条记忆确实帮上忙时', ''),
      helpOption('--useless', '', '记为没用', '这条记忆造成误导或噪音时', ''),
      helpOption('--undo', '', '撤销上一次反馈', '误点反馈时', ''),
    ] },
    { name: 'explain', usage: 'explain <记忆 id> [--json] [--no-usage]', what: '解释一条记忆的效用分和归档判定', when: '想理解为什么它被排序、归档或遗忘时', options: [
      helpOption('--json', '', '输出 JSON', '脚本读取解释结果时', ''),
      helpOption('--no-usage', '', '本次不记录命中打点', '只想临时关闭使用统计时', '只影响这一次调用，不改配置'),
    ] },
    { name: 'bench', usage: 'bench [--evalset <文件>] [--k <条数>] [--seed <数值>] [--bootstrap <次数>] [--ablate] [--gate <指标>=<数值>] [--timing] [--json] [--out <文件>]', what: '可复算的检索基准评测', when: '改检索 / 索引逻辑前后要证明「没变差」，或把质量门禁接进 CI 时', options: [
      helpOption('--evalset', '<文件>', '指定评测集 JSON 文件', '想固定一组查询来复算指标时', '不指定时按库内条目做确定性抽样，生成基线评测集'),
      helpOption('--k', '<条数>', '设置结果窗口大小', '想按 Recall@k / nDCG@k 的 k 口径统计时', '默认 5'),
      helpOption('--seed', '<数值>', '设置抽样与置信区间的随机种子', '要让评测集和置信区间可复算时', '默认 20260925；同种子同库必须同结果'),
      helpOption('--bootstrap', '<次数>', '设置 bootstrap 重采样次数', '想调整 95% 置信区间的精度时', '默认 1000；0 表示不重采样'),
      helpOption('--ablate', '', '输出关键词 / 语义 × 融合 / 纯分的消融对比', '想知道哪一层检索贡献最大时', ''),
      helpOption('--gate', '<指标>=<数值>', '设置质量门禁', 'CI 里要求指标达到阈值时', '不达标 exit 1；可重复传多次，指标可选 recall / mrr / ndcg / hit'),
      helpOption('--timing', '', '附带检索耗时 p50 / p95', '想了解检索耗时分布时', '带上耗时后报告不再逐字节可复算'),
      helpOption('--year', '<yyyy>', '只评测指定年份的记忆', '库很大、只想对某一年做基准时', '可重复传多次；不传则覆盖全部年份'),
      helpOption('--json', '', '输出 JSON', '脚本读取指标与门禁结果时', ''),
      helpOption('--out', '<文件>', '把报告写到文件', '想把评测报告归档或交给 CI 时', ''),
    ] },
    { name: 'scan', usage: 'scan [--path <目录>] [--gate <安全级别>] [--quarantine --yes] [--restore] [--json]', what: '扫描记忆库里的注入、凭证泄漏与越权指令', when: '怀疑记忆被污染、要做安全复核或把门禁接进 CI 时', options: [
      helpOption('--path', '<目录>', '指定要扫描的目录', '想扫描另一个记忆库或临时导出目录时', '默认扫描当前记忆库'),
      helpOption('--gate', '<安全级别>', '设置安全门禁', 'CI 里要求不出现某个级别及以上的命中时', '命中该级别及以上 exit 1；可选 safe / low / medium / high / critical'),
      helpOption('--json', '', '输出 JSON', '脚本读取命中清单与分级统计时', ''),
      helpOption('--quarantine', '', '把命中行脱敏隔离（原文件先备份）', '确认某条记忆被污染、要立刻止住它被检索时', '会改写记忆文件：必须先备份原件，且需要显式确认'),
      helpOption('--yes', '', '跳过交互确认', '自动化里执行隔离时', '跳过确认后不再二次询问，请先看一遍命中清单'),
      helpOption('--restore', '', '还原最近一个隔离批次', '隔离后发现问题、要恢复原文时', '会覆盖当前文件；批次已还原过则拒绝重复还原'),
      helpOption('--id', '<id>', '指定要还原的隔离批次', '要还原的不是最近一批时', ''),
      helpOption('--no-policy', '', '忽略扫描例外策略做全量复核', '怀疑策略过期或想重新确认所有历史命中时', '会重新显示已抑制命中，不改策略文件'),
      helpOption('--policy-candidates', '', '只生成例外策略候选清单', '历史安全语料需要人工复核后配置例外时', '只读扫描；不自动写入 security/scan-policy.json'),
      helpOption('--out', '<文件>', '把候选清单写到文件', '想把候选交给人工复核或评审时', '仅用于 --policy-candidates；不会写策略文件'),
    ] },
    { name: 'reindex', usage: 'reindex', what: '重建记忆索引', when: '索引损坏、手动改过记忆文件或 doctor 提示索引异常时', options: [] },
    { name: 'export', usage: 'export --out <文件.json>', what: '导出全部记忆', when: '备份、迁移或做离线检查时', options: [helpOption('--out', '<文件>', '指定导出文件', '导出时必须给出目标 JSON 文件', '')] },
    { name: 'import', usage: 'import <文件.json>', what: '导入记忆 JSON', when: '从导出文件恢复或迁移时', options: [] },
  ] },
  { group: '身份与画像', commands: [
    { name: 'iam', usage: 'iam --name <名字> --user <用户> --relationship <关系>', what: '登记当前智能体身份', when: '第一次接入，或身份信息需要更新时', options: [
      helpOption('--name', '<名字>', '设置智能体显示名', '登记或更新身份时', ''),
      helpOption('--user', '<用户>', '设置用户称呼', '登记或更新身份时', ''),
      helpOption('--relationship', '<关系>', '设置与用户的关系定位', '登记或更新身份时', ''),
    ] },
    { name: 'identity', usage: 'identity remove <id> [选项]', what: '彻底删除一个 AI 身份与它的私密记忆', when: '某个 AI 不再使用、要把它的身份与私密记忆清干净时', subcommands: [
      helpSub('remove', 'remove <id> [--dry-run] [--yes] [--keep-memories] [--keep-identity] [--password <口令> | --recovery-key <钥匙>]', '彻底删除身份 + 私密记忆（真删）', '确认某个 AI 不再使用、要一次清干净时', [
        helpOption('--dry-run', '', '先列出将删除的内容', '想核对清单再决定时', '预演只读，不改任何文件'),
        helpOption('--yes', '', '跳过交互确认', '自动化里执行删除时', '会立刻真删；请先跑 --dry-run 核对'),
        helpOption('--keep-memories', '', '只删身份与授权，保留私密记忆', '想注销身份但保住记忆时', ''),
        helpOption('--keep-identity', '', '只删私密记忆与授权，保留身份登记', '想清记忆但保留登记时', ''),
        helpOption('--password', '<口令>', '用户主口令（加密库用它证明是用户本人）', '由用户本人在 CLI 执行时', '命令行会留下痕迹；优先交互输入'),
        helpOption('--recovery-key', '<钥匙>', '用恢复钥匙证明用户身份', '忘记主口令时', '恢复钥匙只能由用户本人保管'),
      ]),
    ] },
    { name: 'whoami', usage: 'whoami [--json]', what: '查看当前身份和登记状态', when: '不确定当前是谁、是否已登记时', options: [helpOption('--json', '', '输出 JSON', '脚本读取身份状态时', '')] },
    { name: 'profile', usage: 'profile [--owner <id>] [--json]', what: '生成用户画像', when: '想按私密记忆原文结构化查看用户画像时', options: [
      helpOption('--owner', '<id>', '指定画像归属者', '查某个 owner 的私密画像时', '仍然受私密区权限约束'),
      helpOption('--json', '', '输出 JSON', '自动化读取画像时', ''),
    ] },
    { name: 'context', usage: 'context [--audit [--from <文件|->]] [选项]', what: '生成开工上下文包', when: '每个会话开工时恢复身份、边界、近期记忆和承诺', options: [
      helpOption('--audit', '', '审计被压缩掉的内容是否已经落盘', '宿主压缩上下文后，想确认有没有决策只存在于对话里时', '只读：只打印 remember 建议，不会自动补写'),
      helpOption('--from', '<文件|->', '指定待审计内容（- 表示标准输入）', '把宿主压缩摘要或丢弃段落喂给审计时', '不传时审计当前上下文包的丢弃清单'),
      helpOption('--limit', '<条数>', '限制近期记忆条数', '上下文太长、想缩短时', ''),
      helpOption('--json', '', '输出结构化 JSON（hook 块 + text）', '脚本读取上下文包或扩展装载状态时', '未配置扩展提供方时也返回 JSON'),
      helpOption('--owner', '<id>', '指定 owner 范围', '需要看某个 owner 的上下文时', '仍然受私密区权限约束'),
      helpOption('--budget', '<字符数>', '设置动态记忆字符预算', '需要控制上下文包大小时', '0 表示不限制'),
      helpOption('--focus', '<关键词>', '按当前任务聚焦', '这次任务很明确、想优先拉相关记忆时', ''),
      helpOption('--explain', '', '输出 included / dropped 选择解释', '想理解上下文为什么收录或丢弃时', ''),
      helpOption('--embedding', '<命令>', '临时指定本地 embedding 插件命令', '上下文检索想用本地向量命令时', '只在本地执行'),
      helpOption('--embedding-timeout', '<毫秒>', '设置 embedding 插件超时', '插件较慢或需要快速失败时', ''),
      helpOption('--year', '<yyyy>', '只装载指定年份的记忆', '只想让上下文包覆盖某一年份时', '可重复传多次；不传则装载全部年份'),
      helpOption('--no-usage', '', '本次不记录命中打点', '只想临时关闭使用统计时', '只影响这一次调用，不改配置'),
    ] },
    { name: 'token', usage: 'token <子命令> [选项]', what: '管理远端 MCP 访问 token', when: '给远端 MCP 客户端发放或吊销访问凭据时', subcommands: [
      helpSub('new', 'new --agent <id> [--scope <范围>] [--json]', '生成一个访问 token', '远端客户端第一次接入时', [
        helpOption('--agent', '<id>', '指定 token 对应的智能体 id', '发 token 时必须明确给谁用', ''),
        helpOption('--scope', '<范围>', '限制 token 权限范围', '只想给某一类访问权限时', ''),
        helpOption('--json', '', '输出 JSON', '脚本读取新 token 时', ''),
      ]),
      helpSub('list', 'list [--json]', '列出 token', '查当前有哪些 token 时', [helpOption('--json', '', '输出 JSON', '自动化盘点 token 时', '')]),
      helpSub('revoke', 'revoke --agent <id>', '吊销 token', '设备丢失或凭据泄漏时', [helpOption('--agent', '<id>', '指定要吊销 token 的智能体 id', '吊销时必须明确对象', '')]),
    ] },
  ] },
  { group: '加密与安全', commands: [
    { name: 'migrate', usage: 'migrate [--password-stdin] [--recovery-key-out <文件>]', what: '把明文记忆库迁移成加密记忆库；迁移后授权二选一：推荐 yotta-memory view，等价 CLI 为 yotta-memory key bind <id>', when: '旧库还是明文，确认要启用私密区加密时', options: [
      helpOption('--password', '<口令>', '直接提供主口令', '自动化环境无法交互输入时', '命令行会留下痕迹；优先交互输入'),
      helpOption('--password-stdin', '', '从标准输入读取主口令', '脚本迁移时', '只适合纯 ASCII 口令；中文口令请交互输入'),
      helpOption('--agent', '<id>', '声明迁移使用的身份', '迁移时需要指定 owner 时', ''),
      helpOption('--recovery-key', '<钥匙>', '用恢复钥匙参与迁移', '已有恢复钥匙、需要恢复访问时', '恢复钥匙能重置主口令，注意不要泄漏'),
      helpOption('--recovery-key-out', '<文件>', '把恢复钥匙写到文件', '迁移后要立刻保存恢复钥匙时', '恢复钥匙必须单独妥善保管'),
    ] },
    { name: 'view', usage: 'view [--port <端口>] [--host <地址>]', what: '启动用户查看平台', when: '用户本人要浏览、授权或导出记忆时', options: [
      helpOption('--port', '<端口>', '设置查看平台端口', '默认端口被占用时', ''),
      helpOption('--host', '<地址>', '设置监听地址', '需要只在指定网卡上开放时', '监听公网地址前先确认访问控制和防火墙'),
    ] },
    { name: 'reset-password', usage: 'reset-password [--password <旧口令>] [--new-password <新口令>] [--recovery-key <钥匙>]', what: '重设主口令', when: '知道旧口令想更换，或用恢复钥匙救回访问时', options: [
      helpOption('--password', '<口令>', '提供当前主口令', '正常更换口令时', '命令行会留下痕迹；优先交互输入'),
      helpOption('--new-password', '<口令>', '设置新主口令', '更换口令时', '新口令只保存在本地密钥材料中'),
      helpOption('--password-stdin', '', '从标准输入读取口令', '脚本重设口令时', '只适合纯 ASCII 口令'),
      helpOption('--recovery-key', '<钥匙>', '用恢复钥匙重设口令', '忘记主口令时', '恢复钥匙只显示一次；泄漏等于可重置口令'),
    ] },
    { name: 'key', usage: 'key <子命令> [选项]', what: '管理 agent_key 授权绑定', when: '用户授权智能体读取自己的私密记忆、轮换或吊销 key 时', subcommands: [
      helpSub('list', 'list', '列出授权绑定', '盘点哪些智能体已授权时', []),
      helpSub('bind', 'bind <id> [--password <口令> | --recovery-key <钥匙>]', '给智能体绑定 agent_key', '用户明确授权后绑定', [
        helpOption('--password', '<口令>', '提供主口令', '绑定或轮换时', '命令行会留下痕迹；优先交互输入'),
        helpOption('--recovery-key', '<钥匙>', '用恢复钥匙完成绑定', '忘记主口令时', '恢复钥匙必须妥善保管'),
      ]),
      helpSub('rotate', 'rotate <id> [--password <口令> | --recovery-key <钥匙>]', '轮换 agent_key', '怀疑旧 key 泄漏或定期更换时', [
        helpOption('--password', '<口令>', '提供主口令', '轮换时', '命令行会留下痕迹；优先交互输入'),
        helpOption('--recovery-key', '<钥匙>', '用恢复钥匙完成轮换', '忘记主口令时', '恢复钥匙必须妥善保管'),
      ]),
      helpSub('authorize', 'authorize <id> [--password <口令>]', '授权一个 owner', '用户查看平台不方便时，由 CLI 显式授权', [helpOption('--password', '<口令>', '提供主口令', '授权时', '这是用户侧操作，AI 不应代做')]),
      helpSub('claim', 'claim <id> [--to <AI_HOME> | --plugin-data <目录> | --agent-key-file <文件>]', '领取待绑定的 agent_key', '用户授权后，智能体新会话领取只显示一次的 key', [
        helpOption('--to', '<AI_HOME>', '把 key 写到指定 AI_HOME', '宿主有标准 AI_HOME 目录时', ''),
        helpOption('--plugin-data', '<目录>', '把 key 写到插件数据目录', 'Agent Plugin 形态接入时', ''),
        helpOption('--agent-key-file', '<文件>', '把 key 写到显式文件', '希望完全指定路径时', ''),
      ]),
      helpSub('status', 'status <id> [--to <AI_HOME> | --plugin-data <目录> | --agent-key-file <文件>]', '检查 key 是否已领取、绑定是否有效', '新会话开始或 MCP 连不上时', [
        helpOption('--to', '<AI_HOME>', '检查指定 AI_HOME 下的 key', '宿主有标准 AI_HOME 目录时', ''),
        helpOption('--plugin-data', '<目录>', '检查插件数据目录下的 key', 'Agent Plugin 形态接入时', ''),
        helpOption('--agent-key-file', '<文件>', '检查显式 key 文件', '希望完全指定路径时', ''),
      ]),
      helpSub('revoke', 'revoke <id>', '吊销一个 agent_key', '设备丢失、泄漏或不再授权时', []),
    ] },
    { name: 'config', usage: 'config <get | set <键> <值>>', what: '查看或修改元忆配置', when: '调整记忆位置、embedding 命令、备份或维护阈值时', subcommands: [
      helpSub('get', 'get', '查看当前配置', '想知道实际生效值 / 路径时', []),
      helpSub('set', 'set <键> <值>', '修改配置键', '调整 memory_home / backup_dir / embedding_cmd / embedding_timeout / maintain_* / consolidate_* / scale_* 时', []),
    ] },
  ] },
  { group: '平台与服务', commands: [
    { name: 'runtime', usage: 'runtime <子命令> [选项]', what: '管理稳定运行时入口', when: '安装、切换、回滚或盘点元忆运行时版本时', subcommands: [
      helpSub('install', 'install <tarball|版本> [--from-current] [--force]', '安装一个运行时版本', '升级或回退前准备版本目录时', [
        helpOption('--from-current', '', '把当前运行目录打包安装为运行时版本', '把正在用的副本固化成稳定版本时', ''),
        helpOption('--force', '', '允许覆盖内容不同的已安装版本', '确认要替换同版本目录时', '会覆盖已有运行时内容；先确认版本和备份'),
      ]),
      helpSub('use', 'use <版本> [--restart]', '切换 current 到指定版本', '升级后要把 MCP 切到新版本时', [helpOption('--restart', '', '切换后重启托管服务', '希望立即生效时', '')]),
      helpSub('rollback', 'rollback [--restart]', '回滚到上一个运行时版本', '新版本出问题时', [helpOption('--restart', '', '回滚后重启托管服务', '希望立即恢复服务时', '')]),
      helpSub('status', 'status [--json]', '查看 current 与运行时状态', '排查版本漂移时', [helpOption('--json', '', '输出 JSON', '自动化读取运行时状态时', '')]),
      helpSub('list', 'list [--json]', '列出已安装运行时版本', '盘点可切换版本时', [helpOption('--json', '', '输出 JSON', '自动化盘点运行时版本时', '')]),
    ] },
    { name: 'serve', usage: 'serve [--stdio] [--profile <文件>] [--tools core|full] [--host <地址>] [--port <端口>]', what: '启动 MCP 记忆引擎', when: '宿主需要以 MCP 方式访问元忆时', options: [
      helpOption('--stdio', '', '用本地 stdio 模式启动', '本地宿主不需要 HTTP 服务时', ''),
      helpOption('--profile', '<文件>', '读取每用户服务 profile', '自启任务需要固定记忆库与运行时路径时', 'profile 不存在、路径无效或用户不匹配时拒绝启动'),
      helpOption('--tools', 'core|full', '选择工具分组', '想减少工具常驻开销时', 'core 更省上下文，full 暴露全部工具'),
      helpOption('--host', '<地址>', '设置 HTTP 监听地址', '需要远端 MCP 接入时', '监听公网前必须配置鉴权和防火墙'),
      helpOption('--port', '<端口>', '设置 HTTP 监听端口', '默认端口被占用时', ''),
      helpOption('--no-auth', '', '关闭 HTTP 鉴权', '只在本机临时调试时', '任何能访问端口的人都可读写；不要用于远端或正式环境'),
      helpOption('--agent-id', '<id>', 'stdio 模式下声明智能体 id', '本地宿主用固定身份启动时', ''),
      helpOption('--agent-key', '<key>', 'stdio 模式下直接提供 agent_key', '宿主把 key 作为启动参数传入时', '命令行参数可能被进程列表看到；优先用 key 文件'),
      helpOption('--agent-key-file', '<文件>', 'stdio 模式下从文件读取 agent_key', '宿主使用标准 key 文件时', ''),
    ] },
    { name: 'lan', usage: 'lan <子命令> [选项]', what: '管理开机自启', when: '需要元忆服务随系统或登录启动时', subcommands: [
      helpSub('enable', 'enable [--onstart]', '启用开机自启', '希望元忆服务长期可用时', [helpOption('--onstart', '', '同时启用未登录也启动', 'Windows / Linux 上希望开机即启动、不依赖登录时', '')]),
      helpSub('disable', 'disable', '关闭开机自启', '不再需要常驻服务时', []),
      helpSub('status', 'status', '查看自启状态', '确认服务是否会随系统启动时', []),
    ] },
    { name: '--version', usage: '--version；短写法 -v', what: '显示当前版本', when: '确认安装的是哪个版本时', options: [] },
  ] },
];
// v0.22.1：管理台「高级 / CLI」页速查数据 —— 全量覆盖 HELP_MODEL 的每个命令与子命令。
// 这里只维护「引用哪条命令 + 可复制示例 + 危险标记 + 注意事项」，说明文案统一从
// HELP_MODEL 取（单一真源）；覆盖度由 test/view-cli-help.test.js 与
// tools/export_cli_help.js --check 双向门禁。
const VIEW_HELP_QUICK = [
  { group: '核心记忆', items: [
    { cmd: 'init', example: 'yotta-memory init --encrypt' },
    { cmd: 'remember', example: 'yotta-memory remember FACT 主题 内容' },
    { cmd: 'recall', example: 'yotta-memory recall 关键词 --type BOUND' },
    { cmd: 'forget', example: 'yotta-memory forget <记忆 id>', danger: true, note: '删除前先确认 id；重要库先 backup create 留恢复点' },
    { cmd: 'rename', example: 'yotta-memory rename <记忆 id> <新文件名> --dry-run' },
    { cmd: 'archive', example: 'yotta-memory archive --dry-run', note: '先预演；--force 会关闭冷却期与常青豁免' },
    { cmd: 'backup', example: 'yotta-memory backup <子命令>' },
    { cmd: 'backup volumes', example: 'yotta-memory backup volumes' },
    { cmd: 'backup setup', example: 'yotta-memory backup setup' },
    { cmd: 'backup status', example: 'yotta-memory backup status' },
    { cmd: 'backup ensure-daily', example: 'yotta-memory backup ensure-daily' },
    { cmd: 'backup schedule', example: 'yotta-memory backup schedule on --time 03:30' },
    { cmd: 'backup create', example: 'yotta-memory backup create' },
    { cmd: 'backup list', example: 'yotta-memory backup list' },
    { cmd: 'backup doctor', example: 'yotta-memory backup doctor' },
    { cmd: 'backup restore', example: 'yotta-memory backup restore <id> --to <目录>', danger: true, note: '恢复会写入目标目录；覆盖非空目录需显式 --force，先确认目标和备份' },
    { cmd: 'backup drill', example: 'yotta-memory backup drill <id>', note: '先演练确认备份可用，再正式恢复' },
    { cmd: 'doctor', example: 'yotta-memory doctor' },
    { cmd: 'index', example: 'yotta-memory index --stats --json', note: '只读统计；--stats 不会重建索引' },
    { cmd: 'layout', example: 'yotta-memory layout <子命令>' },
    { cmd: 'layout plan', example: 'yotta-memory layout plan --json' },
    { cmd: 'layout apply', example: 'yotta-memory layout apply --from-plan <文件> --yes', danger: true, note: '会移动记忆文件；先审阅计划，失败时自动逆序回滚' },
    { cmd: 'layout rollback', example: 'yotta-memory layout rollback --batch <id> --yes', danger: true, note: '按 journal 逆序恢复原路径；先确认批次' },
    { cmd: 'maintain', example: 'yotta-memory maintain --capacity', note: '只读报告，不会自动归档或改权重' },
    { cmd: 'consolidate', example: 'yotta-memory consolidate --propose' },
    { cmd: 'distill', example: 'yotta-memory distill --model <命令>' },
    { cmd: 'feedback', example: 'yotta-memory feedback <记忆 id> --useful' },
    { cmd: 'explain', example: 'yotta-memory explain <记忆 id>' },
    { cmd: 'bench', example: 'yotta-memory bench' },
    { cmd: 'scan', example: 'yotta-memory scan' },
    { cmd: 'reindex', example: 'yotta-memory reindex' },
    { cmd: 'export', example: 'yotta-memory export --out 记忆导出.json' },
    { cmd: 'import', example: 'yotta-memory import 记忆导出.json', danger: true, note: '导入会写入现有记忆库；先确认文件来源与内容' },
  ] },
  { group: '身份与画像', items: [
    { cmd: 'iam', example: 'yotta-memory iam --name <名字> --user <用户> --relationship <关系>' },
    { cmd: 'identity', example: 'yotta-memory identity remove <id> --dry-run', note: '子命令 remove：真删该 AI 的私密记忆（公共 FACT 保留）' },
    { cmd: 'identity remove', example: 'yotta-memory identity remove <id> --yes', danger: true, note: '先 --dry-run 预览；--yes 后不可恢复（私密记忆真删）' },
    { cmd: 'whoami', example: 'yotta-memory whoami' },
    { cmd: 'profile', example: 'yotta-memory profile --json' },
    { cmd: 'context', example: 'yotta-memory context' },
    { cmd: 'token', example: 'yotta-memory token <子命令>' },
    { cmd: 'token new', example: 'yotta-memory token new --agent <id>', note: '一次性 token，只显示一次，请立即保存' },
    { cmd: 'token list', example: 'yotta-memory token list' },
    { cmd: 'token revoke', example: 'yotta-memory token revoke --agent <id>', danger: true, note: '吊销后该 token 立即失效' },
  ] },
  { group: '加密与安全', items: [
    { cmd: 'migrate', example: 'yotta-memory migrate --recovery-key-out <文件>', note: '迁移后立刻保存恢复钥匙' },
    { cmd: 'view', example: 'yotta-memory view' },
    { cmd: 'reset-password', example: 'yotta-memory reset-password --recovery-key <钥匙>', danger: true, note: '重置后旧口令失效；恢复钥匙必须单独保管' },
    { cmd: 'key', example: 'yotta-memory key <子命令>' },
    { cmd: 'key list', example: 'yotta-memory key list' },
    { cmd: 'key bind', example: 'yotta-memory key bind <id>' },
    { cmd: 'key rotate', example: 'yotta-memory key rotate <id>', danger: true, note: '轮换后旧 key 立即失效' },
    { cmd: 'key authorize', example: 'yotta-memory key authorize <id>', note: '授权该 AI 读写私密区' },
    { cmd: 'key claim', example: 'yotta-memory key claim <id>' },
    { cmd: 'key status', example: 'yotta-memory key status <id>' },
    { cmd: 'key revoke', example: 'yotta-memory key revoke <id>', danger: true, note: '吊销后该 agent_key 立即失效' },
    { cmd: 'config', example: 'yotta-memory config <get | set>' },
    { cmd: 'config get', example: 'yotta-memory config get' },
    { cmd: 'config set', example: 'yotta-memory config set <键> <值>' },
  ] },
  { group: '平台与服务', items: [
    { cmd: 'runtime', example: 'yotta-memory runtime <子命令>' },
    { cmd: 'runtime install', example: 'yotta-memory runtime install <tarball|版本>' },
    { cmd: 'runtime use', example: 'yotta-memory runtime use <版本>' },
    { cmd: 'runtime rollback', example: 'yotta-memory runtime rollback', danger: true, note: '回滚运行时入口；先确认当前版本与目标版本' },
    { cmd: 'runtime status', example: 'yotta-memory runtime status' },
    { cmd: 'runtime list', example: 'yotta-memory runtime list' },
    { cmd: 'serve', example: 'yotta-memory serve' },
    { cmd: 'lan', example: 'yotta-memory lan <子命令>' },
    { cmd: 'lan enable', example: 'yotta-memory lan enable', note: '开机自启；不再需要时用 lan disable 关闭' },
    { cmd: 'lan disable', example: 'yotta-memory lan disable' },
    { cmd: 'lan status', example: 'yotta-memory lan status' },
    { cmd: '--version', example: 'yotta-memory --version' },
  ] },
];
// @generated view-html:start
const VIEW_HTML = "<!doctype html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<meta name=\"robots\" content=\"noindex,nofollow\">\n<link rel=\"icon\" href=\"data:,\">\n<title>元忆 · 记忆管理台</title>\n<style>\n  :root{--bg:#0f0c12;--bg2:#141019;--panel:#191420;--panel2:#1f1828;--line:rgba(255,217,138,.12);--line2:rgba(255,217,138,.24);\n    --text:#f4eee4;--muted:#a79c8e;--faint:#776c60;--amber:#f0a13a;--gold:#ffd98a;--ok:#7fc49a;--danger:#e07070;--shadow:0 10px 30px rgba(0,0,0,.35)}\n  body.light{--bg:#f6f1e8;--bg2:#f1eade;--panel:#fffdf8;--panel2:#faf5ec;--line:rgba(56,42,28,.12);--line2:rgba(56,42,28,.24);\n    --text:#241c14;--muted:#6f6458;--faint:#96897b;--amber:#c1781c;--gold:#9c6a16;--ok:#3e7d57;--danger:#b23c3c;--shadow:0 8px 24px rgba(56,42,28,.10)}\n  *{box-sizing:border-box}[hidden]{display:none!important}\n  html,body{margin:0;padding:0}\n  body{background:var(--bg);color:var(--text);font:14px/1.6 \"Microsoft YaHei\",\"PingFang SC\",\"Noto Sans CJK SC\",system-ui,sans-serif;letter-spacing:0}\n  button{font:inherit;color:inherit;cursor:pointer}\n  input,select,textarea{font:inherit;color:var(--text);background:var(--panel2);border:1px solid var(--line2);border-radius:8px;padding:9px 12px;outline:0;width:100%}\n  input:focus,select:focus,textarea:focus{border-color:var(--amber)}\n  textarea{min-height:96px;resize:vertical}\n  .muted{color:var(--muted)}.faint{color:var(--faint);font-size:12px}\n  .sv{width:16px;height:16px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex:none}\n\n  /* lock */\n  .lock-wrap{min-height:100vh;display:grid;place-items:center;padding:24px}\n  .lock-card{width:min(420px,100%);background:var(--panel);border:1px solid var(--line2);border-radius:12px;padding:26px;box-shadow:var(--shadow)}\n  .lock-card h1{margin:14px 0 6px;font-size:22px}\n  .lock-card .field{margin-top:16px}\n  .err{color:var(--danger);margin-top:10px;font-size:13px;min-height:20px}\n\n  /* shell */\n  .shell{display:grid;grid-template-columns:236px minmax(0,1fr);min-height:100vh}\n  .sidebar{background:var(--bg2);border-right:1px solid var(--line);padding:22px 16px;display:flex;flex-direction:column;gap:22px;position:sticky;top:0;height:100vh;min-width:0}\n  .brand{display:flex;align-items:center;gap:10px;padding:0 6px}\n  .brand-mark{width:34px;height:34px;border-radius:8px;background:rgba(240,161,58,.14);border:1px solid var(--line2);display:grid;place-items:center;color:var(--gold)}\n  .brand-name{font-size:16px;font-weight:600}.brand-sub{font-size:11px;color:var(--faint)}\n  .nav{display:flex;flex-direction:column;gap:4px;min-width:0}\n  .nav button{display:flex;align-items:center;gap:10px;padding:9px 10px;border-radius:6px;border:1px solid transparent;background:transparent;color:var(--muted);text-align:left}\n  .nav button:hover{background:var(--panel);color:var(--text)}\n  .nav button.active{background:var(--panel);color:var(--gold);border-color:var(--line)}\n  .side-foot{margin-top:auto;display:flex;flex-direction:column;gap:10px;min-width:0}\n  .privacy{display:flex;gap:8px;align-items:flex-start;padding:10px;border:1px solid var(--line);border-radius:8px;color:var(--muted);font-size:12px;background:var(--panel)}\n  .privacy .sv{color:var(--ok);margin-top:2px}\n  .ghost-btn{display:flex;align-items:center;justify-content:center;gap:8px;border:1px solid var(--line);background:transparent;color:var(--muted);border-radius:6px;padding:8px}\n  .ghost-btn:hover{color:var(--text);border-color:var(--line2)}\n\n  .main{min-width:0;padding:26px 30px 60px}\n  .topbar{display:flex;align-items:center;gap:14px;margin-bottom:22px;flex-wrap:wrap}\n  .page-title{font-size:20px;font-weight:600;margin:0}.page-sub{color:var(--faint);font-size:12px;margin-top:2px}\n  .spacer{flex:1}\n  .search{display:flex;align-items:center;gap:8px;min-width:240px;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 12px;color:var(--muted)}\n  .search input{background:transparent;border:0;padding:0;width:100%}\n  .chip-user{display:flex;align-items:center;gap:8px;padding:6px 10px;border:1px solid var(--line);border-radius:999px;color:var(--muted);font-size:12px}\n  .dot{width:8px;height:8px;border-radius:50%;background:var(--amber)}\n\n  .view{display:none}.view.active{display:block}\n  .grid{display:grid;gap:14px}.g4{grid-template-columns:repeat(4,minmax(0,1fr))}.g2{grid-template-columns:repeat(2,minmax(0,1fr))}\n  .card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px;min-width:0}\n  .card h3{margin:0 0 4px;font-size:14px}\n  .label{color:var(--muted);font-size:12px}.value{font-size:26px;font-weight:600;margin:8px 0 2px}.delta{font-size:12px;color:var(--ok)}\n  .section{margin-top:20px}\n  .shead{display:flex;align-items:baseline;gap:10px;margin-bottom:10px}.shead h2{font-size:15px;margin:0}\n  .bars{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}\n  .bar{border:1px solid var(--line);border-radius:8px;padding:12px;background:var(--panel2)}\n  .bar b{font-size:18px;display:block;margin-top:6px}\n  .bar .dot{display:inline-block;margin-right:6px}\n\n  .toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap}\n  .chips{display:flex;gap:8px;flex-wrap:wrap}\n  .chip{border:1px solid var(--line);background:transparent;color:var(--muted);border-radius:999px;padding:5px 12px;font-size:12px}\n  .chip.active{color:var(--gold);border-color:var(--line2);background:rgba(240,161,58,.10)}\n  .btn{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:6px;border:1px solid var(--line2);background:transparent;color:var(--text)}\n  .btn:hover{border-color:var(--gold)}\n  .btn.primary{background:var(--amber);border-color:var(--amber);color:#1b1206;font-weight:600}\n  .btn.danger{border-color:rgba(224,112,112,.5);color:var(--danger)}\n  .btn.small{padding:5px 10px;font-size:12px}\n  .btn[disabled]{opacity:.5;cursor:not-allowed}\n\n  .list{display:flex;flex-direction:column;gap:8px;margin-top:14px}\n  .row{display:flex;align-items:center;gap:12px;padding:12px 14px;border:1px solid var(--line);border-radius:8px;background:var(--panel2)}\n  .row:hover{border-color:var(--line2)}\n  .row-main{flex:1;min-width:0;cursor:pointer}\n  .row-title{font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}\n  .row-snippet{color:var(--muted);font-size:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}\n  .row-meta{color:var(--faint);font-size:11px;margin-top:2px}\n  .row-actions{display:flex;gap:6px}\n  .ibtn{width:30px;height:30px;display:grid;place-items:center;border:1px solid var(--line);background:transparent;border-radius:6px;color:var(--muted)}\n  .ibtn:hover{color:var(--text);border-color:var(--line2)}\n  .badge{font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid var(--line2);color:var(--gold);background:rgba(240,161,58,.10);white-space:nowrap}\n  .badge.pref{color:#b79cdd;border-color:rgba(183,156,221,.4);background:rgba(183,156,221,.10)}\n  .badge.bound{color:#8fb4de;border-color:rgba(143,180,222,.4);background:rgba(143,180,222,.10)}\n  .badge.commit{color:var(--ok);border-color:rgba(127,196,154,.4);background:rgba(127,196,154,.10)}\n  .badge.off{color:var(--faint);border-color:var(--line);background:transparent}\n  .empty{color:var(--faint);text-align:center;padding:26px;border:1px dashed var(--line);border-radius:8px;margin-top:14px}\n  .pager{display:flex;align-items:center;gap:10px;margin-top:12px;color:var(--faint);font-size:12px}\n\n  table{width:100%;border-collapse:collapse}\n  th,td{text-align:left;padding:12px 10px;border-bottom:1px solid var(--line);font-size:13px}\n  th{color:var(--faint);font-weight:500;font-size:12px}\n  .owner-name{font-weight:600}\n\n  .field{margin-bottom:12px}\n  .field label{display:block;color:var(--muted);font-size:12px;margin-bottom:6px}\n  .row2{display:grid;grid-template-columns:1fr 1fr;gap:12px}\n  .owner-pick{display:flex;flex-wrap:wrap;gap:6px;max-height:132px;overflow:auto;margin-bottom:8px}\n  .owner-chip{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:transparent;color:var(--muted);border-radius:999px;padding:5px 10px;font-size:12px}\n  .owner-chip:hover{color:var(--text);border-color:var(--line2)}\n  .owner-chip.active{color:var(--gold);border-color:var(--line2);background:rgba(240,161,58,.12)}\n  .owner-chip .tag{font-size:10px;color:var(--faint);border:1px solid var(--line);border-radius:999px;padding:0 6px}\n  .owner-chip.active .tag{color:var(--gold);border-color:var(--line2)}\n\n  .mask{position:fixed;inset:0;background:rgba(0,0,0,.5);display:none;place-items:center;z-index:50;padding:20px}\n  .mask.open{display:grid}\n  #drawerMask{z-index:40}\n  .modal{width:min(560px,100%);max-height:86vh;overflow:auto;background:var(--panel);border:1px solid var(--line2);border-radius:10px;padding:18px;box-shadow:var(--shadow)}\n  .modal h3{margin:0 0 10px;font-size:16px}\n  .modal-actions{display:flex;justify-content:flex-end;gap:8px;margin-top:14px}\n  .drawer{position:fixed;top:0;right:0;bottom:0;width:min(440px,92vw);background:var(--panel);border-left:1px solid var(--line2);padding:20px;overflow:auto;transform:translateX(100%);transition:transform .2s;z-index:45}\n  .drawer.open{transform:none}\n  .kv{display:grid;grid-template-columns:86px 1fr;gap:6px 10px;font-size:13px;margin:14px 0}\n  .kv dt{color:var(--faint)}.kv dd{margin:0;word-break:break-all}\n  .quote{border-left:2px solid var(--line2);padding-left:12px;color:var(--muted);white-space:pre-wrap;word-break:break-word}\n  .keybox{width:100%;min-height:64px;font-family:ui-monospace,Consolas,monospace;font-size:12px}\n\n  .toasts{position:fixed;left:50%;bottom:26px;transform:translateX(-50%);display:flex;flex-direction:column;gap:8px;align-items:center;z-index:60}\n  .toast{display:flex;align-items:center;gap:10px;background:var(--panel2);border:1px solid var(--line2);border-radius:999px;padding:9px 16px;box-shadow:var(--shadow);font-size:13px}\n  .toast button{border:0;background:transparent;color:var(--gold);font-weight:600}\n  .list-plain{display:flex;flex-direction:column;gap:8px;max-height:46vh;overflow:auto}\n  .list-plain .item{display:flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:8px;padding:9px 10px;font-size:12px;color:var(--muted)}\n  .list-plain .item .spacer{flex:1}\n\n  /* advanced cli */\n  .quick-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}\n  .cmd-item{border:1px solid var(--line);border-radius:8px;padding:12px 14px;background:var(--panel2);display:flex;flex-direction:column;gap:8px;min-width:0}\n  .cmd-head{display:flex;align-items:center;gap:8px;flex-wrap:wrap}\n  .cmd-name{font-family:ui-monospace,Consolas,monospace;font-size:12px;color:var(--gold)}\n  .cmd-what{font-weight:600}\n  .cmd-when{color:var(--muted);font-size:12px}\n  .code-line{display:flex;align-items:center;gap:8px;background:rgba(0,0,0,.28);border:1px solid var(--line);border-radius:6px;padding:6px 10px;min-width:0}\n  body.light .code-line{background:rgba(56,42,28,.06)}\n  .code-line code{flex:1;min-width:0;font-family:ui-monospace,Consolas,monospace;font-size:12px;overflow-x:auto;white-space:nowrap}\n  .danger-badge{color:var(--danger);border-color:rgba(224,112,112,.5);background:rgba(224,112,112,.10)}\n  .cmd-note{color:var(--danger);font-size:12px}\n  .quick-group{margin-top:14px}\n  .quick-group h4{margin:0 0 8px;font-size:13px;color:var(--muted)}\n  .help-cmd{border:1px solid var(--line);border-radius:8px;background:var(--panel2);margin-top:10px;min-width:0}\n  .help-cmd summary{cursor:pointer;padding:10px 14px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;list-style:none}\n  .help-cmd summary::-webkit-details-marker{display:none}\n  .help-cmd summary::before{content:'';width:6px;height:6px;border-right:1.6px solid var(--muted);border-bottom:1.6px solid var(--muted);transform:rotate(-45deg);transition:transform .15s;flex:none}\n  .help-cmd[open] summary::before{transform:rotate(45deg)}\n  .help-body{padding:12px 14px;display:flex;flex-direction:column;gap:8px;border-top:1px solid var(--line)}\n  .help-sub{border-top:1px solid var(--line);padding-top:8px;margin-top:2px;display:flex;flex-direction:column;gap:6px}\n  .help-sub .cmd-name{color:var(--text)}\n  .opt-row{display:grid;grid-template-columns:minmax(150px,auto) minmax(0,1fr);gap:2px 12px;padding:7px 0;border-top:1px solid var(--line);font-size:12px}\n  .opt-row:first-child{border-top:0}\n  .opt-flag{font-family:ui-monospace,Consolas,monospace;word-break:break-all}\n  .opt-what{color:var(--muted)}\n  .opt-when{color:var(--faint)}\n  .opt-risk{color:var(--danger)}\n  .opt-row.with-copy{grid-template-columns:minmax(150px,auto) minmax(0,1fr) auto;align-items:start}\n  .opt-row.with-copy .ibtn{width:26px;height:26px}\n\n  @media (max-width:960px){.g4{grid-template-columns:repeat(2,minmax(0,1fr))}.bars{grid-template-columns:repeat(2,minmax(0,1fr))}.quick-list{grid-template-columns:minmax(0,1fr)}}\n  @media (max-width:760px){\n    .shell{grid-template-columns:minmax(0,1fr)}\n    .sidebar{position:static;height:auto;padding:14px;gap:12px}\n    .nav{flex-direction:row;overflow-x:auto;width:100%}\n    .nav button{white-space:nowrap}\n    .side-foot{margin-top:0;flex-direction:row}\n    .privacy{flex:1}\n    .main{padding:18px 16px 48px}\n    .search{min-width:100%;order:3}\n    .g4{grid-template-columns:repeat(2,minmax(0,1fr))}\n    table{display:block;overflow-x:auto;white-space:nowrap}\n    .row{flex-wrap:wrap}.row-actions{width:100%;justify-content:flex-end}\n  }\n</style>\n</head>\n<body>\n<div id=\"lock\" class=\"lock-wrap\">\n  <div class=\"lock-card\">\n    <div class=\"brand\">\n      <div class=\"brand-mark\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><ellipse cx=\"12\" cy=\"5\" rx=\"8\" ry=\"3\"/><path d=\"M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5\"/><path d=\"M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3\"/></svg></div>\n      <div><div class=\"brand-name\">元忆 yotta-memory</div><div class=\"brand-sub\">你的 AI 记忆，由你掌控</div></div>\n    </div>\n    <h1>解锁记忆管理台 <span id=\"ver\" class=\"faint\"></span></h1>\n    <div class=\"field\"><label>主口令（只在本地内存派生，不落盘、不发远端）</label><input type=\"password\" id=\"pw\" placeholder=\"主口令\"></div>\n    <button class=\"btn primary\" id=\"unlockBtn\" style=\"width:100%\">解锁</button>\n    <div class=\"err\" id=\"lockErr\"></div>\n    <div class=\"faint\" style=\"margin-top:8px\">忘记口令可用恢复钥匙在 CLI 重设：<code>yotta-memory reset-password --recovery-key &lt;钥匙&gt;</code></div>\n  </div>\n</div>\n\n<div id=\"app\" class=\"shell\" hidden>\n  <aside class=\"sidebar\">\n    <div class=\"brand\">\n      <div class=\"brand-mark\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><ellipse cx=\"12\" cy=\"5\" rx=\"8\" ry=\"3\"/><path d=\"M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5\"/><path d=\"M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3\"/></svg></div>\n      <div><div class=\"brand-name\">元忆</div><div class=\"brand-sub\">你的 AI 记忆，由你掌控</div></div>\n    </div>\n    <nav class=\"nav\" id=\"nav\">\n      <button data-view=\"overview\" class=\"active\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M3 10.5 12 3l9 7.5\"/><path d=\"M5 9.5V21h14V9.5\"/></svg>概览</button>\n      <button data-view=\"memories\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M4 19.5A2.5 2.5 0 0 1 6.5 17H20\"/><path d=\"M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z\"/></svg>记忆</button>\n      <button data-view=\"access\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2\"/><circle cx=\"9\" cy=\"7\" r=\"4\"/><path d=\"M22 21v-2a4 4 0 0 0-3-3.87\"/></svg>AI 与权限</button>\n      <button data-view=\"settings\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M4 21v-7\"/><path d=\"M4 10V3\"/><path d=\"M12 21v-9\"/><path d=\"M12 8V3\"/><path d=\"M20 21v-5\"/><path d=\"M20 12V3\"/><path d=\"M1 14h6\"/><path d=\"M9 8h6\"/><path d=\"M17 16h6\"/></svg>设置</button>\n      <button data-view=\"cli\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"m4 17 6-6-6-6\"/><path d=\"M12 19h8\"/></svg>高级 / CLI</button>\n    </nav>\n    <div class=\"side-foot\">\n      <div class=\"privacy\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z\"/><path d=\"m9 12 2 2 4-4\"/></svg><span>数据不出本机<br>私密区按 AI 隔离加密</span></div>\n      <button class=\"ghost-btn\" id=\"themeBtn\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><circle cx=\"12\" cy=\"12\" r=\"4\"/><path d=\"M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4\"/></svg>切换主题</button>\n    </div>\n  </aside>\n\n  <main class=\"main\">\n    <div class=\"topbar\">\n      <div><h1 class=\"page-title\" id=\"pageTitle\">概览</h1><div class=\"page-sub\" id=\"pageSub\">你的 AI 记住了什么，一眼看清</div></div>\n      <div class=\"spacer\"></div>\n      <label class=\"search\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><circle cx=\"11\" cy=\"11\" r=\"7\"/><path d=\"m20 20-3.5-3.5\"/></svg><input id=\"globalSearch\" placeholder=\"搜索记忆 / 关键词\"></label>\n      <div class=\"chip-user\"><span class=\"dot\"></span>本机 · 用户</div>\n    </div>\n\n    <section class=\"view active\" id=\"view-overview\">\n      <div class=\"grid g4\">\n        <div class=\"card\"><div class=\"label\">记忆总数</div><div class=\"value\" id=\"ovTotal\">-</div><div class=\"delta\" id=\"ovFiles\">-</div></div>\n        <div class=\"card\"><div class=\"label\">私密记忆</div><div class=\"value\" id=\"ovPrivate\">-</div><div class=\"delta\">仅对应 AI 与本人可见</div></div>\n        <div class=\"card\"><div class=\"label\">AI 智能体</div><div class=\"value\" id=\"ovOwners\">-</div><div class=\"delta\" id=\"ovAuth\">-</div></div>\n        <div class=\"card\"><div class=\"label\">已藏起来（归档）</div><div class=\"value\" id=\"ovArchived\">-</div><div class=\"delta\">可随时放回</div></div>\n      </div>\n      <div class=\"section\">\n        <div class=\"shead\"><h2>四类记忆分布</h2><span class=\"faint\">FACT 共享 · PREF / BOUND / COMMIT 私密</span></div>\n        <div class=\"bars\" id=\"typeBars\"></div>\n      </div>\n      <div class=\"section grid g2\">\n        <div class=\"card\">\n          <h3>最近更新</h3>\n          <div class=\"list\" id=\"recentList\"></div>\n        </div>\n        <div class=\"card\">\n          <h3>备份与安全</h3>\n          <div class=\"kv\" style=\"margin-top:10px\">\n            <dt>备份目录</dt><dd id=\"ovBackup\">-</dd>\n            <dt>存储占用</dt><dd id=\"ovBytes\">-</dd>\n            <dt>私密加密</dt><dd>已启用（AES-256-GCM 信封加密）</dd>\n          </div>\n          <div style=\"display:flex;gap:8px;flex-wrap:wrap\">\n            <button class=\"btn small\" id=\"quickArchived\">查看已藏</button>\n            <button class=\"btn small\" id=\"quickTrash\">最近删除</button>\n            <button class=\"btn small primary\" data-goto=\"memories\">管理记忆</button>\n          </div>\n        </div>\n      </div>\n    </section>\n\n    <section class=\"view\" id=\"view-memories\">\n      <div class=\"card toolbar\">\n        <label class=\"search\" style=\"min-width:280px;flex:1\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><circle cx=\"11\" cy=\"11\" r=\"7\"/><path d=\"m20 20-3.5-3.5\"/></svg><input id=\"memSearch\" placeholder=\"搜索记忆（标题 / 内容 / 标签 / 编号）\"></label>\n        <div class=\"chips\" id=\"typeChips\">\n          <button class=\"chip active\" data-type=\"all\">全部</button>\n          <button class=\"chip\" data-type=\"FACT\">FACT</button>\n          <button class=\"chip\" data-type=\"PREF\">PREF</button>\n          <button class=\"chip\" data-type=\"BOUND\">BOUND</button>\n          <button class=\"chip\" data-type=\"COMMIT\">COMMIT</button>\n        </div>\n        <select id=\"ownerFilter\" title=\"按智能体筛选\" style=\"width:auto;min-width:140px\"><option value=\"\">全部智能体</option></select>\n        <div class=\"spacer\"></div>\n        <button class=\"btn\" id=\"btnArchived\">已藏</button>\n        <button class=\"btn\" id=\"btnTrash\">最近删除</button>\n        <button class=\"btn primary\" id=\"btnNew\">新建记忆</button>\n      </div>\n      <div class=\"list\" id=\"memList\"></div>\n      <div class=\"empty\" id=\"memEmpty\" hidden>没有匹配的记忆。</div>\n      <div class=\"pager\"><button class=\"btn small\" id=\"prevPage\">上一页</button><span id=\"pageInfo\">-</span><button class=\"btn small\" id=\"nextPage\">下一页</button></div>\n    </section>\n\n    <section class=\"view\" id=\"view-access\">\n      <div class=\"card\">\n        <h3>谁看得见什么</h3>\n        <div class=\"faint\" style=\"margin-bottom:10px\">默认拒绝：每个 AI 只能读自己的私密区；公共 FACT 所有已授权 AI 可见。授权会生成只显示一次的 agent_key，请立即单独保存。</div>\n        <table><thead><tr><th>AI 智能体</th><th>FACT 公共</th><th>私密记忆</th><th>状态</th><th></th></tr></thead><tbody id=\"ownerRows\"></tbody></table>\n      </div>\n      <div class=\"section card\">\n        <h3>恢复与备份</h3>\n        <div class=\"kv\"><dt>备份目录</dt><dd id=\"accBackup\">-</dd><dt>恢复钥匙</dt><dd>离线保存；泄露等同口令泄露</dd></div>\n        <div style=\"display:flex;gap:8px;flex-wrap:wrap\"><button class=\"btn small\" id=\"btnRk\">显示恢复钥匙</button><button class=\"btn small\" id=\"btnExport\">导出全部 JSON</button></div>\n      </div>\n    </section>\n\n    <section class=\"view\" id=\"view-settings\">\n      <div class=\"card\">\n        <h3>重设主口令</h3>\n        <div class=\"row2\" style=\"margin-top:10px\">\n          <div class=\"field\"><label>当前口令</label><input type=\"password\" id=\"pwCur\"></div>\n          <div class=\"field\"><label>新口令</label><input type=\"password\" id=\"pwNew\"></div>\n          <div class=\"field\"><label>确认新口令</label><input type=\"password\" id=\"pwNew2\"></div>\n        </div>\n        <button class=\"btn primary\" id=\"btnResetPw\">重设口令</button>\n        <div class=\"err\" id=\"pwOut\"></div>\n      </div>\n      <div class=\"section card\">\n        <h3>危险操作</h3>\n        <div class=\"faint\">删除某个 AI 的身份与其私密记忆（公共 FACT 保留，其它 AI 不受影响）。此操作不可恢复，请谨慎使用。</div>\n        <div style=\"margin-top:10px\"><button class=\"btn danger small\" id=\"btnDangerHint\">在哪里执行？</button></div>\n      </div>\n    </section>\n\n    <section class=\"view\" id=\"view-cli\">\n      <div class=\"card\">\n        <h3>常用命令速查</h3>\n        <div class=\"faint\" style=\"margin-bottom:12px\">只展示与复制；命令都在终端执行，危险操作已标注。</div>\n        <div id=\"cliQuick\"><div class=\"faint\">加载中…</div></div>\n      </div>\n      <div class=\"section card\">\n        <h3>完整命令与参数</h3>\n        <div class=\"faint\" style=\"margin-bottom:12px\">与当前安装版本一致（随版本自动更新）；按需加载，只读展示，不执行任何命令。</div>\n        <button class=\"btn\" id=\"btnFullHelp\">加载完整命令与参数</button>\n        <div id=\"cliFull\" hidden></div>\n      </div>\n    </section>\n  </main>\n</div>\n\n<div class=\"mask\" id=\"modalMask\"><div class=\"modal\"><h3 id=\"modalTitle\"></h3><div id=\"modalBody\"></div><div class=\"modal-actions\"><button class=\"btn\" id=\"modalCancel\">取消</button><button class=\"btn primary\" id=\"modalOk\">确认</button></div></div></div>\n<div class=\"mask\" id=\"drawerMask\"></div>\n<aside class=\"drawer\" id=\"drawer\">\n  <div style=\"display:flex;gap:10px;align-items:flex-start\"><div style=\"flex:1\"><h3 id=\"drTitle\"></h3><div class=\"faint\" id=\"drMeta\"></div></div><button class=\"ibtn\" id=\"drClose\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M18 6 6 18\"/><path d=\"m6 6 12 12\"/></svg></button></div>\n  <div class=\"quote\" id=\"drBody\" style=\"margin-top:12px\"></div>\n  <dl class=\"kv\" id=\"drKv\"></dl>\n  <div style=\"display:flex;gap:8px\"><button class=\"btn\" id=\"drEdit\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M12 20h9\"/><path d=\"M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z\"/></svg>编辑</button><button class=\"btn danger\" id=\"drDelete\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M3 6h18\"/><path d=\"M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2\"/><path d=\"M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6\"/></svg>删除</button></div>\n</aside>\n<div class=\"toasts\" id=\"toasts\"></div>\n\n<script>\n(function () {\n  'use strict';\n  var $ = function (s) { return document.querySelector(s); };\n  var state = { view: 'overview', entries: [], count: 0, offset: 0, limit: 20, query: '', type: 'all', owner: '', owners: [], overview: null, current: null, help: null };\n  var typeNames = { FACT: 'FACT 事实', PREF: 'PREF 偏好', BOUND: 'BOUND 边界', COMMIT: 'COMMIT 承诺' };\n\n  function esc(s) {\n    return String(s == null ? '' : s).replace(/[&<>\"']/g, function (c) {\n      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '\"': '&quot;', \"'\": '&#39;' }[c];\n    });\n  }\n  async function api(pathname, body) {\n    try {\n      var res = await fetch(pathname, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) });\n      var text = await res.text();\n      var data;\n      try { data = JSON.parse(text); } catch (e) { data = { error: text }; }\n      if (res.status === 401) showLock();\n      return data;\n    } catch (e) { return { error: String(e) }; }\n  }\n  function errText(r, fallback) {\n    return r && r.error ? ((r.text || r.message || fallback) || '操作失败') : '';\n  }\n  function fmtBytes(n) {\n    n = Number(n) || 0;\n    if (n < 1024) return n + ' B';\n    if (n < 1024 * 1024) return (n / 1024).toFixed(1) + ' KB';\n    return (n / 1024 / 1024).toFixed(2) + ' MB';\n  }\n  function pad2(n) { return (n < 10 ? '0' : '') + n; }\n  function fmtTime(e) {\n    if (e && e.mtime) {\n      var d = new Date(e.mtime);\n      if (!isNaN(d.getTime())) {\n        return d.getFullYear() + '-' + pad2(d.getMonth() + 1) + '-' + pad2(d.getDate()) + ' ' + pad2(d.getHours()) + ':' + pad2(d.getMinutes()) + ':' + pad2(d.getSeconds());\n      }\n    }\n    return (e && (e.updated || e.created)) || '';\n  }\n  // v0.22.8：卡片时间语义显式化——「创建」用 frontmatter created（文件系统 btime 兜底），「更新」用文件 mtime（打点已不再改写它）。\n  function metaLine(e, withFile) {\n    var parts = [e.owner || '公共'];\n    if (e.created) parts.push('创建 ' + e.created);\n    var up = fmtTime(e);\n    if (up) parts.push('更新 ' + up);\n    if (withFile) parts.push(e.file);\n    return parts.join(' · ');\n  }\n  function applyTypeCounts(typeCounts) {\n    Array.prototype.forEach.call(document.querySelectorAll('#typeChips .chip'), function (c) {\n      c.textContent = (c.dataset.type === 'all' ? '全部' : c.dataset.type) + ' ' + (typeCounts[c.dataset.type] || 0);\n    });\n  }\n  function toast(msg, actionLabel, fn) {\n    var el = document.createElement('div');\n    el.className = 'toast';\n    el.appendChild(document.createTextNode(msg));\n    if (actionLabel && fn) {\n      var b = document.createElement('button');\n      b.textContent = actionLabel;\n      b.addEventListener('click', function () { el.remove(); fn(); });\n      el.appendChild(b);\n    }\n    $('#toasts').appendChild(el);\n    setTimeout(function () { el.remove(); }, actionLabel ? 9000 : 3600);\n  }\n  function showLock() { $('#lock').hidden = false; $('#app').hidden = true; }\n  function showApp() { $('#lock').hidden = true; $('#app').hidden = false; refreshAll(); }\n\n  /* modal / drawer */\n  var modalOkFn = null;\n  function openModal(title, bodyHtml, opts) {\n    opts = opts || {};\n    $('#modalTitle').textContent = title;\n    $('#modalBody').innerHTML = bodyHtml;\n    $('#modalOk').textContent = opts.okText || '确认';\n    $('#modalOk').className = 'btn ' + (opts.danger ? 'danger' : 'primary');\n    $('#modalOk').hidden = !opts.onOk;\n    modalOkFn = opts.onOk || null;\n    $('#modalMask').classList.add('open');\n  }\n  function closeModal() { $('#modalMask').classList.remove('open'); modalOkFn = null; }\n  function confirmModal(title, text, okText, danger, onOk) {\n    openModal(title, '<p class=\"muted\">' + esc(text) + '</p>', { okText: okText, danger: danger, onOk: onOk });\n  }\n  $('#modalCancel').addEventListener('click', closeModal);\n  $('#modalMask').addEventListener('click', function (e) { if (e.target === $('#modalMask')) closeModal(); });\n  $('#modalOk').addEventListener('click', function () { if (modalOkFn) modalOkFn(); });\n  function openDrawer() { $('#drawer').classList.add('open'); $('#drawerMask').classList.add('open'); }\n  function closeDrawer() { $('#drawer').classList.remove('open'); $('#drawerMask').classList.remove('open'); }\n  $('#drClose').addEventListener('click', closeDrawer);\n  $('#drawerMask').addEventListener('click', closeDrawer);\n\n  /* nav */\n  var titles = { overview: ['概览', '你的 AI 记住了什么，一眼看清'], memories: ['记忆', '看 / 改 / 删 / 藏，全在这里'], access: ['AI 与权限', '默认拒绝，按 AI 隔离'], settings: ['设置', '口令 / 备份 / 导出'], cli: ['高级 / CLI', '常用命令速查与完整帮助（只展示与复制）'] };\n  function switchView(name) {\n    state.view = name;\n    Array.prototype.forEach.call(document.querySelectorAll('#nav button'), function (b) { b.classList.toggle('active', b.dataset.view === name); });\n    Array.prototype.forEach.call(document.querySelectorAll('.view'), function (v) { v.classList.toggle('active', v.id === 'view-' + name); });\n    $('#pageTitle').textContent = titles[name][0];\n    $('#pageSub').textContent = titles[name][1];\n    window.scrollTo(0, 0);\n    if (name === 'cli') ensureHelp();\n  }\n  $('#nav').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) switchView(b.dataset.view); });\n  Array.prototype.forEach.call(document.querySelectorAll('[data-goto]'), function (b) { b.addEventListener('click', function () { switchView(b.dataset.goto); }); });\n  $('#themeBtn').addEventListener('click', function () { document.body.classList.toggle('light'); });\n\n  /* data loaders */\n  async function loadOverview() {\n    var d = await api('/api/overview');\n    if (d.error) return;\n    state.overview = d;\n    var priv = d.total - (d.byType.FACT || 0);\n    $('#ovTotal').textContent = d.total;\n    $('#ovFiles').textContent = d.files + ' 个文件';\n    $('#ovPrivate').textContent = priv;\n    $('#ovOwners').textContent = d.owners.length;\n    $('#ovAuth').textContent = d.authorized + ' 已授权';\n    $('#ovArchived').textContent = d.archived;\n    $('#ovBackup').textContent = d.backupDir || '未配置（CLI: yotta-memory backup setup）';\n    $('#ovBytes').textContent = fmtBytes(d.bytes);\n    $('#accBackup').textContent = d.backupDir || '未配置';\n    var colors = { FACT: 'var(--gold)', PREF: '#b79cdd', BOUND: '#8fb4de', COMMIT: 'var(--ok)' };\n    var byType = d.byType || {};\n    var typeCounts = { all: d.total || 0, FACT: byType.FACT || 0, PREF: byType.PREF || 0, BOUND: byType.BOUND || 0, COMMIT: byType.COMMIT || 0 };\n    $('#typeBars').innerHTML = ['FACT', 'PREF', 'BOUND', 'COMMIT'].map(function (t) {\n      return '<div class=\"bar\" data-type=\"' + t + '\" style=\"cursor:pointer\" title=\"查看 ' + typeNames[t] + '\"><span class=\"dot\" style=\"background:' + colors[t] + '\"></span><span class=\"faint\">' + typeNames[t] + '</span><b>' + typeCounts[t] + '</b></div>';\n    }).join('');\n    applyTypeCounts(typeCounts);\n  }\n  async function loadOwners() {\n    var d = await api('/api/owners');\n    state.owners = (d && d.owners) || [];\n    var sel = $('#ownerFilter');\n    if (sel) {\n      sel.innerHTML = '<option value=\"\">全部智能体</option>' + state.owners.map(function (o) {\n        return '<option value=\"' + esc(o.owner) + '\"' + (o.owner === state.owner ? ' selected' : '') + '>' + esc(o.owner) + '</option>';\n      }).join('');\n    }\n    var box = $('#ownerRows');\n    if (!state.owners.length) { box.innerHTML = '<tr><td colspan=\"5\" class=\"faint\">' + esc((d && d.hint) || '当前没有 owner，请先在 CLI 执行 yotta-memory iam <id>。') + '</td></tr>'; return; }\n    box.innerHTML = state.owners.map(function (o) {\n      return '<tr><td><span class=\"owner-name\">' + esc(o.owner) + '</span><div class=\"faint\">' + (o.registered ? '已登记' : '未登记') + '</div></td>' +\n        '<td><span class=\"badge commit\">可见</span></td>' +\n        '<td>' + (o.authorized ? '<span class=\"badge commit\">已授权</span>' : '<span class=\"badge off\">仅自己</span>') + '</td>' +\n        '<td>' + (o.authorized ? '可读自己的私密区' : '未绑定 agent_key') + '</td>' +\n        '<td><button class=\"btn small\" data-auth=\"' + esc(o.owner) + '\">' + (o.authorized ? '吊销' : '授权') + '</button> <button class=\"btn small danger\" data-remove=\"' + esc(o.owner) + '\">删除</button></td></tr>';\n    }).join('');\n  }\n  async function loadEntries() {\n    var d = await api('/api/entries', { query: state.query, offset: state.offset, limit: state.limit, type: state.type === 'all' ? '' : state.type, owner: state.owner || '' });\n    if (d.error) { toast(errText(d, '加载失败')); return; }\n    state.entries = d.entries || [];\n    state.count = d.count || 0;\n    // v0.22.8：chips 计数跟随当前智能体 / 搜索筛选（概览页无筛选时即全局口径）。\n    if (d.counts) applyTypeCounts(d.counts);\n    var totalPg = Math.max(1, Math.ceil(state.count / state.limit));\n    var curPg = Math.floor(state.offset / state.limit) + 1;\n    $('#pageInfo').textContent = '共 ' + state.count + ' 条 · 第 ' + curPg + ' / ' + totalPg + ' 页';\n    $('#prevPage').disabled = state.offset <= 0;\n    $('#nextPage').disabled = !d.hasMore;\n    renderEntries();\n  }\n  function renderEntries() {\n    var box = $('#memList');\n    $('#memEmpty').hidden = state.entries.length > 0;\n    box.innerHTML = state.entries.map(function (e) {\n      var t = String(e.type || 'FACT').toUpperCase();\n      return '<div class=\"row\" data-file=\"' + esc(e.file) + '\"><div class=\"row-main\"><span class=\"badge ' + t.toLowerCase() + '\">' + typeNames[t] + '</span>' +\n        '<div class=\"row-title\">' + esc(e.subject) + '</div><div class=\"row-snippet\">' + esc(e.statement) + '</div>' +\n        '<div class=\"row-meta\">' + esc(metaLine(e, true)) + '</div></div>' +\n        '<div class=\"row-actions\"><button class=\"ibtn\" data-act=\"edit\" title=\"编辑\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M12 20h9\"/><path d=\"M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z\"/></svg></button>' +\n        '<button class=\"ibtn\" data-act=\"archive\" title=\"藏起来（归档）\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M9.9 4.24A9.1 9.1 0 0 1 12 4c7 0 10 8 10 8a17.5 17.5 0 0 1-2.16 3.19\"/><path d=\"M6.6 6.6A16.8 16.8 0 0 0 2 12s3 8 10 8a9.6 9.6 0 0 0 5.4-1.6\"/><path d=\"m2 2 20 20\"/></svg></button>' +\n        '<button class=\"ibtn\" data-act=\"delete\" title=\"删除\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M3 6h18\"/><path d=\"M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2\"/><path d=\"M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6\"/></svg></button></div></div>';\n    }).join('');\n  }\n  async function refreshAll() {\n    await loadOverview();\n    await loadOwners();\n    await loadEntries();\n    var recent = state.entries.slice(0, 4).map(function (e) {\n      var t = String(e.type || 'FACT').toUpperCase();\n      return '<div class=\"row\"><div class=\"row-main\"><div class=\"row-title\">' + esc(e.subject) + '</div><div class=\"row-meta\">' + esc(metaLine(e, false)) + '</div></div><span class=\"badge ' + t.toLowerCase() + '\">' + typeNames[t] + '</span></div>';\n    }).join('');\n    $('#recentList').innerHTML = recent || '<div class=\"faint\">还没有记忆。</div>';\n  }\n\n  /* entries actions */\n  $('#memList').addEventListener('click', async function (e) {\n    var row = e.target.closest('.row');\n    if (!row) return;\n    var file = row.dataset.file;\n    var entry = state.entries.filter(function (x) { return x.file === file; })[0];\n    var act = e.target.closest('button[data-act]');\n    if (!act) { openDetail(entry); return; }\n    if (act.dataset.act === 'edit') openEditor(entry);\n    else if (act.dataset.act === 'delete') doDelete(entry);\n    else if (act.dataset.act === 'archive') doArchive(entry);\n  });\n  function openDetail(entry) {\n    if (!entry) return;\n    state.current = entry;\n    var t = String(entry.type || 'FACT').toUpperCase();\n    $('#drTitle').textContent = entry.subject || '(无标题)';\n    $('#drMeta').textContent = typeNames[t] + ' · ' + metaLine(entry, false);\n    $('#drBody').textContent = entry.statement || '';\n    $('#drKv').innerHTML = '<dt>创建</dt><dd>' + esc(entry.created || (entry.btime ? fmtTime({ mtime: entry.btime }) : '-')) + '</dd>' +\n      '<dt>最近更新</dt><dd>' + esc(fmtTime(entry) || entry.updated || '-') + '</dd>' +\n      '<dt>文件</dt><dd>' + esc(entry.file) + '</dd><dt>可见性</dt><dd>' + (t === 'FACT' ? '所有已授权 AI' : '仅 ' + esc(entry.owner) + '（私密）') + '</dd><dt>标签</dt><dd>' + esc((entry.tags || []).join(', ') || '-') + '</dd>';\n    openDrawer();\n  }\n  $('#drEdit').addEventListener('click', function () { if (state.current) { closeDrawer(); openEditor(state.current); } });\n  $('#drDelete').addEventListener('click', function () { if (state.current) { closeDrawer(); doDelete(state.current); } });\n\n  function editorHtml(entry, isNew) {\n    var t = entry ? String(entry.type || 'FACT').toUpperCase() : 'FACT';\n    var ownerLocked = !isNew && t !== 'FACT';\n    return '<div class=\"field\"><label>类型</label><select id=\"fType\"' + (isNew ? '' : ' disabled') + '>' +\n      ['FACT', 'PREF', 'BOUND', 'COMMIT'].map(function (x) { return '<option value=\"' + x + '\"' + (x === t ? ' selected' : '') + '>' + typeNames[x] + '</option>'; }).join('') + '</select></div>' +\n      '<div class=\"field\" id=\"fOwnerWrap\"><label>' + (t === 'FACT' && !isNew ? '归属 AI（FACT 为公共记忆，归属仅作来源标记，可修改）' : '归属 AI（私密记忆必填；点选或输入自定义 ID）') + '</label>' +\n      '<div class=\"owner-pick\" id=\"fOwnerPick\">' + (state.owners.length ? state.owners.map(function (o) {\n        return '<button type=\"button\" class=\"owner-chip' + ((entry && entry.owner === o.owner) ? ' active' : '') + '\"' + (ownerLocked ? ' disabled' : '') + ' data-owner=\"' + esc(o.owner) + '\">' + esc(o.owner) + '<span class=\"tag\">' + (o.authorized ? '已授权' : '未授权') + '</span></button>';\n      }).join('') : '<span class=\"faint\">还没有已登记的 AI；可直接输入自定义 ID。</span>') + '</div>' +\n      '<input id=\"fOwner\" placeholder=\"自定义 AI ID（如 codex）\" value=\"' + esc(entry && entry.owner || '') + '\"' + (ownerLocked ? ' disabled' : '') + '></div>' +\n      '<div class=\"field\"><label>标题 subject</label><input id=\"fSubject\" value=\"' + esc(entry && entry.subject || '') + '\"></div>' +\n      '<div class=\"field\"><label>内容 statement</label><textarea id=\"fStatement\">' + esc(entry && entry.statement || '') + '</textarea></div>' +\n      '<div class=\"field\"><label>标签（逗号分隔）</label><input id=\"fTags\" value=\"' + esc(entry && (entry.tags || []).join(', ') || '') + '\"></div>' +\n      (isNew ? '' : (t === 'FACT'\n        ? '<div class=\"faint\">类型不可修改；FACT 为公共记忆，归属仅作来源标记，可修改。</div>'\n        : '<div class=\"faint\">类型与归属不可修改；私密记忆如需变更归属请删除后重写。</div>'));\n  }\n  function syncOwnerField() {\n    var t = $('#fType') ? $('#fType').value : 'FACT';\n    var wrap = $('#fOwnerWrap');\n    if (wrap) wrap.hidden = (t === 'FACT');\n  }\n  function bindOwnerPicker() {\n    var pick = $('#fOwnerPick');\n    if (!pick || ($('#fOwner') && $('#fOwner').disabled)) return;\n    pick.addEventListener('click', function (e) {\n      var chip = e.target.closest('.owner-chip');\n      if (!chip) return;\n      Array.prototype.forEach.call(pick.querySelectorAll('.owner-chip'), function (c) { c.classList.toggle('active', c === chip); });\n      $('#fOwner').value = chip.dataset.owner;\n    });\n    $('#fOwner').addEventListener('input', function () {\n      var v = $('#fOwner').value.trim();\n      Array.prototype.forEach.call(pick.querySelectorAll('.owner-chip'), function (c) { c.classList.toggle('active', c.dataset.owner === v); });\n    });\n  }\n  function openEditor(entry) {\n    openModal('编辑记忆', editorHtml(entry, false), {\n      okText: '保存', onOk: async function () {\n        var subject = $('#fSubject').value.trim();\n        var statement = $('#fStatement').value.trim();\n        var tags = $('#fTags').value.split(',').map(function (x) { return x.trim(); }).filter(Boolean);\n        if (!subject || !statement) { toast('标题与内容不能为空'); return; }\n        var body = { file: entry.file, subject: subject, statement: statement, tags: tags };\n        var type = String(entry.type || 'FACT').toUpperCase();\n        if (type === 'FACT' && $('#fOwner') && !$('#fOwner').disabled) body.owner = $('#fOwner').value.trim();\n        var r = await api('/api/memory/update', body);\n        if (r.error) { toast(errText(r, '保存失败')); return; }\n        closeModal();\n        toast('已更新 1 条记忆' + (r.ownerChange ? '（归属已改为 ' + (r.ownerChange.to || '公共') + '）' : ''), '撤销', async function () {\n          var u = await api('/api/memory/restore', { ref: r.undo });\n          toast(errText(u, '撤销失败') || '已撤销这次编辑');\n          refreshAll();\n        });\n        refreshAll();\n      },\n    });\n    bindOwnerPicker();\n  }\n  $('#btnNew').addEventListener('click', function () {\n    openModal('新建记忆', editorHtml(null, true), {\n      okText: '创建', onOk: async function () {\n        var type = $('#fType').value;\n        var owner = $('#fOwner') ? $('#fOwner').value.trim() : '';\n        var subject = $('#fSubject').value.trim();\n        var statement = $('#fStatement').value.trim();\n        var tags = $('#fTags').value.split(',').map(function (x) { return x.trim(); }).filter(Boolean);\n        if (!subject || !statement) { toast('标题与内容不能为空'); return; }\n        var r = await api('/api/memory/create', { type: type, owner: owner, subject: subject, statement: statement, tags: tags });\n        if (r.error) { toast(errText(r, '创建失败')); return; }\n        closeModal();\n        toast('已创建 1 条记忆');\n        refreshAll();\n      },\n    });\n    bindOwnerPicker();\n    syncOwnerField();\n    $('#fType').addEventListener('change', syncOwnerField);\n  });\n  function doDelete(entry) {\n    confirmModal('删除这条记忆？', '将移入回收区（不物理删除），可从「最近删除」恢复。', '删除', true, async function () {\n      var r = await api('/api/memory/delete', { file: entry.file });\n      if (r.error) { toast(errText(r, '删除失败')); return; }\n      closeModal();\n      toast('已删除 1 条记忆', '撤销', async function () {\n        var u = await api('/api/memory/restore', { ref: r.trash });\n        toast(errText(u, '恢复失败') || '已恢复');\n        refreshAll();\n      });\n      refreshAll();\n    });\n  }\n  function doArchive(entry) {\n    confirmModal('藏起来（归档）？', '归档后不参与召回，但数据保留，可随时放回。', '藏起来', false, async function () {\n      var r = await api('/api/memory/archive', { file: entry.file });\n      if (r.error) { toast(errText(r, '归档失败')); return; }\n      closeModal();\n      toast('已藏起来 1 条', '放回', async function () {\n        var u = await api('/api/memory/unarchive', { archive: r.archive });\n        toast(errText(u, '放回失败') || '已放回');\n        refreshAll();\n      });\n      refreshAll();\n    });\n  }\n\n  async function openArchived() {\n    var d = await api('/api/archived');\n    var items = (d.entries || []).map(function (e) {\n      return '<div class=\"item\"><span>' + esc(e.original) + '</span><span class=\"spacer\"></span><button class=\"btn small\" data-unarch=\"' + esc(e.ref) + '\">放回</button></div>';\n    }).join('');\n    openModal('已藏起来（归档）', items ? '<div class=\"list-plain\">' + items + '</div>' : '<p class=\"faint\">没有归档的记忆。</p>', {});\n    $('#modalBody').addEventListener('click', async function (e) {\n      var b = e.target.closest('button[data-unarch]');\n      if (!b) return;\n      var r = await api('/api/memory/unarchive', { archive: b.dataset.unarch });\n      toast(errText(r, '放回失败') || '已放回');\n      closeModal();\n      refreshAll();\n    }, { once: true });\n  }\n  async function openTrash() {\n    var d = await api('/api/trash');\n    var items = (d.entries || []).filter(function (e) { return e.kind === 'trash'; }).map(function (e) {\n      return '<div class=\"item\"><span>' + esc(e.original) + '</span><span class=\"spacer\"></span><button class=\"btn small\" data-restore=\"' + esc(e.ref) + '\">恢复</button></div>';\n    }).join('');\n    openModal('最近删除', items ? '<div class=\"list-plain\">' + items + '</div>' : '<p class=\"faint\">回收区是空的。</p>', {});\n    $('#modalBody').addEventListener('click', async function (e) {\n      var b = e.target.closest('button[data-restore]');\n      if (!b) return;\n      var r = await api('/api/memory/restore', { ref: b.dataset.restore });\n      toast(errText(r, '恢复失败') || '已恢复');\n      closeModal();\n      refreshAll();\n    }, { once: true });\n  }\n  $('#btnArchived').addEventListener('click', openArchived);\n  $('#quickArchived').addEventListener('click', openArchived);\n  $('#btnTrash').addEventListener('click', openTrash);\n  $('#quickTrash').addEventListener('click', openTrash);\n\n  /* search / filter / paging */\n  $('#memSearch').addEventListener('keydown', function (e) { if (e.key === 'Enter') { state.query = e.target.value; state.offset = 0; loadEntries(); } });\n  $('#globalSearch').addEventListener('keydown', function (e) { if (e.key === 'Enter') { state.query = e.target.value; state.offset = 0; switchView('memories'); loadEntries(); } });\n  $('#typeChips').addEventListener('click', function (e) {\n    var b = e.target.closest('.chip');\n    if (!b) return;\n    state.type = b.dataset.type; state.offset = 0;\n    Array.prototype.forEach.call(document.querySelectorAll('#typeChips .chip'), function (c) { c.classList.toggle('active', c === b); });\n    loadEntries();\n  });\n  $('#typeBars').addEventListener('click', function (e) {\n    var bar = e.target.closest('.bar[data-type]');\n    if (!bar) return;\n    state.type = bar.dataset.type; state.offset = 0;\n    Array.prototype.forEach.call(document.querySelectorAll('#typeChips .chip'), function (c) { c.classList.toggle('active', c.dataset.type === state.type); });\n    switchView('memories');\n    loadEntries();\n  });\n  $('#ownerFilter').addEventListener('change', function () { state.owner = this.value; state.offset = 0; loadEntries(); });\n  $('#prevPage').addEventListener('click', function () { if (state.offset > 0) { state.offset -= state.limit; loadEntries(); } });\n  $('#nextPage').addEventListener('click', function () { state.offset += state.limit; loadEntries(); });\n\n  /* owners */\n  $('#ownerRows').addEventListener('click', async function (e) {\n    var authBtn = e.target.closest('button[data-auth]');\n    var rmBtn = e.target.closest('button[data-remove]');\n    if (authBtn) {\n      var owner = authBtn.dataset.auth;\n      var authorized = state.owners.filter(function (o) { return o.owner === owner; })[0].authorized;\n      if (authorized) {\n        confirmModal('吊销 ' + owner + ' 的授权？', '吊销后该智能体立即失去私密读写能力，旧 key 会立即校验失败。', '吊销', true, async function () {\n          var r = await api('/api/revoke', { owner: owner });\n          closeModal(); toast(errText(r, '吊销失败') || '已吊销'); loadOwners();\n        });\n      } else {\n        confirmModal('授权 ' + owner + '？', '「授权」由你（用户）操作：确认后生成只显示一次的 agent_key，请立即单独保存；服务端同时写临时待领取文件 keys/pending/<agent_id>.key，供该 AI 新会话执行 key claim 领取，领取成功后自动删除。AI 不应代为执行该授权操作。', '授权', false, async function () {\n          var r = await api('/api/authorize', { owner: owner });\n          closeModal();\n          if (r.error) { toast(errText(r, '授权失败')); return; }\n          openModal('agent_key（只显示一次）', '<p class=\"muted\">请立即单独保存；AI 新会话执行 key status → key claim 领取。</p><textarea class=\"keybox\" readonly>' + esc(r.agentKey) + '</textarea>', { okText: '我已保存', onOk: closeModal });\n          var box = $('#modalBody').querySelector('textarea');\n          if (box) { box.focus(); box.select(); }\n          loadOwners();\n        });\n      }\n      return;\n    }\n    if (rmBtn) {\n      var target = rmBtn.dataset.remove;\n      openModal('删除 ' + target + ' 的身份与私密记忆', '<p class=\"muted\">不可恢复；公共 FACT 保留，其它 AI 不受影响。请输入完整 ID 确认：</p><input id=\"confirmOwner\" placeholder=\"' + esc(target) + '\">', {\n        okText: '删除', danger: true, onOk: async function () {\n          var typed = $('#confirmOwner').value.trim();\n          if (typed !== target) { toast('ID 不匹配'); return; }\n          var r = await api('/api/identity-remove', { owner: target, confirm: typed });\n          closeModal(); toast(errText(r, '删除失败') || '已删除'); loadOwners(); loadOverview(); loadEntries();\n        },\n      });\n    }\n  });\n\n  /* settings */\n  $('#btnResetPw').addEventListener('click', async function () {\n    var a = $('#pwCur').value, b = $('#pwNew').value, c = $('#pwNew2').value;\n    if (!b || b !== c) { $('#pwOut').textContent = '两次新口令不一致'; return; }\n    var r = await api('/api/reset-password', { currentPassword: a, newPassword: b });\n    $('#pwOut').textContent = r.error ? (r.text || '重设失败') : (r.text || '已重设');\n    if (!r.error) { $('#pwCur').value = $('#pwNew').value = $('#pwNew2').value = ''; }\n  });\n  $('#btnRk').addEventListener('click', async function () {\n    var r = await api('/api/recovery-key');\n    if (r.error) { toast(errText(r, '恢复钥匙读取失败')); return; }\n    openModal('恢复钥匙（离线保存）', '<p class=\"muted\">泄露等同口令泄露。忘记主口令时可用它重设。</p><textarea class=\"keybox\" readonly>' + esc(r.recoveryKey) + '</textarea>', { okText: '我已保存', onOk: closeModal });\n  });\n  $('#btnExport').addEventListener('click', async function () {\n    var r = await api('/api/export');\n    if (r.error) { toast(errText(r, '导出失败')); return; }\n    var blob = new Blob([JSON.stringify(r, null, 2)], { type: 'application/json' });\n    var a = document.createElement('a');\n    a.href = URL.createObjectURL(blob);\n    a.download = 'yottamemory-export.json';\n    a.click();\n    toast('已导出 JSON');\n  });\n  $('#btnDangerHint').addEventListener('click', function () {\n    toast('在「AI 与权限」列表里，每个 AI 右侧有「删除」按钮');\n  });\n\n  /* advanced cli */\n  function findHelpEntry(groups, ref) {\n    var seg = String(ref).split(' ');\n    for (var i = 0; i < groups.length; i++) {\n      var cmds = groups[i].commands || [];\n      for (var j = 0; j < cmds.length; j++) {\n        var c = cmds[j];\n        if (c.name !== seg[0]) continue;\n        if (seg.length === 1) return c;\n        var subs = c.subcommands || [];\n        for (var k = 0; k < subs.length; k++) if (subs[k].name === seg[1]) return subs[k];\n      }\n    }\n    return null;\n  }\n  function copyText(text) {\n    function fallback() {\n      var ta = document.createElement('textarea');\n      ta.value = text;\n      ta.style.position = 'fixed';\n      ta.style.top = '-1000px';\n      document.body.appendChild(ta);\n      ta.select();\n      var ok = false;\n      try { ok = document.execCommand('copy'); } catch (e) {}\n      ta.remove();\n      return ok;\n    }\n    if (navigator.clipboard && navigator.clipboard.writeText) {\n      return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return fallback(); });\n    }\n    return Promise.resolve(fallback());\n  }\n  function copyBtn(text) {\n    return '<button class=\"ibtn copy-btn\" data-copy=\"' + esc(text) + '\" title=\"复制命令\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><rect x=\"9\" y=\"9\" width=\"11\" height=\"11\" rx=\"2\"/><path d=\"M5 15V5a2 2 0 0 1 2-2h10\"/></svg></button>';\n  }\n  function codeLine(text) {\n    return '<div class=\"code-line\"><code>' + esc(text) + '</code>' + copyBtn(text) + '</div>';\n  }\n  function optRows(options) {\n    return (options || []).map(function (o) {\n      return '<div class=\"opt-row\"><div class=\"opt-flag\">' + esc(o.flag + (o.arg ? ' ' + o.arg : '')) + '</div><div>' +\n        '<div class=\"opt-what\">' + esc(o.what) + '</div>' +\n        (o.when ? '<div class=\"opt-when\">' + esc(o.when) + '</div>' : '') +\n        (o.caution ? '<div class=\"opt-risk\">' + esc(o.caution) + '</div>' : '') +\n        '</div></div>';\n    }).join('');\n  }\n  function renderQuick() {\n    if (!state.help) return;\n    var d = state.help;\n    $('#cliQuick').innerHTML = (d.quick || []).map(function (g) {\n      var items = (g.items || []).map(function (it) {\n        var meta = findHelpEntry(d.groups, it.cmd) || {};\n        return '<div class=\"cmd-item\"><div class=\"cmd-head\"><code class=\"cmd-name\">' + esc(it.cmd) + '</code>' +\n          (it.danger ? '<span class=\"badge danger-badge\">危险</span>' : '') + '</div>' +\n          '<div class=\"cmd-what\">' + esc(meta.what || '') + '</div>' +\n          '<div class=\"cmd-when\">' + esc(meta.when || '') + '</div>' +\n          codeLine(it.example) +\n          (it.note ? '<div class=\"cmd-note\">' + esc(it.note) + '</div>' : '') + '</div>';\n      }).join('');\n      return '<div class=\"quick-group\"><h4>' + esc(g.group) + '</h4><div class=\"quick-list\">' + items + '</div></div>';\n    }).join('');\n  }\n  function renderFull() {\n    if (!state.help) return;\n    var keys = state.help.configKeys || [];\n    var keyHelp = state.help.configKeyHelp || {};\n    var keysHtml = keys.length ? '<div class=\"quick-group\" id=\"cliConfigKeys\"><h4>配置键（config set）</h4>' +\n      '<div class=\"cmd-when\">全部可配置键（共 ' + keys.length + ' 个）。用法：yotta-memory config set &lt;键&gt; &lt;值&gt;，改完用 yotta-memory config get 复查；配置保存在 ~/.yottamemory/config.json。</div>' +\n      keys.map(function (k) {\n        var h = keyHelp[k] || {};\n        return '<div class=\"opt-row with-copy\"><div class=\"opt-flag\">' + esc(k) + '</div><div>' +\n          '<div class=\"opt-what\">' + esc(h.what || '') + '</div>' +\n          (h.when ? '<div class=\"opt-when\">' + esc(h.when) + '</div>' : '') +\n          '</div>' + copyBtn('yotta-memory config set ' + k + ' <值>') + '</div>';\n      }).join('') + '</div>' : '';\n    // UX-M-01：配置键块紧随 config 命令（同组相邻）；找不到 config 时回退末尾。\n    var keysPlaced = false;\n    var groupsHtml = (state.help.groups || []).map(function (g) {\n      var cmds = (g.commands || []).map(function (c) {\n        var subs = (c.subcommands || []).map(function (s) {\n          return '<div class=\"help-sub\"><div class=\"cmd-head\"><code class=\"cmd-name\">' + esc(c.name + ' ' + s.name) + '</code></div>' +\n            (s.what ? '<div class=\"cmd-what\">' + esc(s.what) + '</div>' : '') +\n            (s.when ? '<div class=\"cmd-when\">' + esc(s.when) + '</div>' : '') +\n            codeLine('yotta-memory ' + c.name + ' ' + s.usage) + optRows(s.options) + '</div>';\n        }).join('');\n        var cmdHtml = '<details class=\"help-cmd\"><summary><code class=\"cmd-name\">' + esc(c.name) + '</code><span class=\"cmd-what\">' + esc(c.what) + '</span></summary>' +\n          '<div class=\"help-body\">' + (c.when ? '<div class=\"cmd-when\">' + esc(c.when) + '</div>' : '') +\n          codeLine('yotta-memory ' + c.usage) + optRows(c.options) + subs + '</div></details>';\n        if (!keysPlaced && c.name === 'config' && keysHtml) {\n          keysPlaced = true;\n          return cmdHtml + keysHtml;\n        }\n        return cmdHtml;\n      }).join('');\n      return '<div class=\"quick-group\"><h4>' + esc(g.group) + '</h4>' + cmds + '</div>';\n    }).join('');\n    $('#cliFull').innerHTML = groupsHtml + (keysPlaced ? '' : keysHtml);\n  }\n  async function ensureHelp() {\n    if (state.help) { renderQuick(); return; }\n    var d = await api('/api/help');\n    if (!d || d.error) { toast(errText(d, '帮助加载失败')); return; }\n    state.help = d;\n    renderQuick();\n  }\n  $('#btnFullHelp').addEventListener('click', async function () {\n    if (!state.help) await ensureHelp();\n    if (!state.help) return;\n    renderFull();\n    $('#cliFull').hidden = false;\n    $('#btnFullHelp').hidden = true;\n  });\n  document.addEventListener('click', function (e) {\n    var b = e.target.closest('.copy-btn[data-copy]');\n    if (!b) return;\n    copyText(b.dataset.copy).then(function (ok) { toast(ok ? '已复制' : '复制失败，请手动选择'); });\n  });\n\n  /* unlock / boot */\n  $('#unlockBtn').addEventListener('click', async function () {\n    var r = await api('/api/unlock', { password: $('#pw').value });\n    if (r.error) { $('#lockErr').textContent = r.error; return; }\n    $('#lockErr').textContent = '';\n    showApp();\n  });\n  $('#pw').addEventListener('keydown', function (e) { if (e.key === 'Enter') $('#unlockBtn').click(); });\n  (async function boot() {\n    var s = await api('/api/status');\n    if (s && s.version) $('#ver').textContent = 'v' + s.version;\n    if (s && s.unlocked) showApp(); else showLock();\n    if (s && s.encrypted === false) $('#lockErr').textContent = '当前记忆库未启用加密；请先在 CLI 执行 init --encrypt / migrate。';\n  })();\n})();\n</script>\n</body>\n</html>\n";
// @generated view-html:end
// MCP 协议（2026-07-28 无状态 + 2025-11-25 legacy 握手，dual-era）
const MCP_PROTOCOL_MODERN = '2026-07-28';
const MCP_PROTOCOL_LEGACY = '2025-11-25';
const TYPES = ['FACT', 'PREF', 'BOUND', 'COMMIT'];
const TYPE_DIRS = { FACT: 'facts', PREF: 'prefs', BOUND: 'bounds', COMMIT: 'commits' };
const PUBLIC_DIR = 'facts';
const PRIVATE_DIR = 'private';
const PRIVATE_LEAF = ['prefs', 'bounds', 'commits'];
const ARCHIVE_DIR = '.archive';
const INDEX_FILE = 'index.json';
const PRIVATE_TYPES = ['PREF', 'BOUND', 'COMMIT'];
// v0.23.0 D1/D2：上下文包 COMMIT 段保留条数（0 = 全部）与归档默认门槛（与效用分地板对齐）
const CONTEXT_COMMITS_LIMIT_DEFAULT = 20;
const ARCHIVE_UTILITY_DEFAULT = 0.55;
const FIELD_ORDER = ['type', 'subject', 'statement', 'confidence', 'created', 'updated', 'tags', 'immutable', 'scope', 'owner', 'source', 'weight', 'access_count', 'last_accessed', 'feedback_net', 'hit_days', 'hit_queries'];
const CONFIG_FILE = 'config.json';
const SERVER_SUBDIR = '.server';
const TOKENS_FILE = 'tokens.json';
const AGENTS_FILE = 'agents.json';
const PROFILE_FILE = 'profile.md';
const BACKUP_TASK_NAME = 'YottaMemoryBackup';
const BACKUP_SYSTEMD_SERVICE = 'yotta-memory-backup.service';
const BACKUP_SYSTEMD_TIMER = 'yotta-memory-backup.timer';
const BACKUP_CRON_MARKER = '#YTM_BACKUP:yotta-memory-backup';
const BACKUP_LAUNCHD_LABEL = 'cn.yottameta.yotta-memory.backup';
// remember 类型启发式提示关键词（statement 含主观/关系词且 type=FACT 时提示改 PREF，仅提示不拦截）
const HINT_KEYWORDS = ['用户', '偏好', '喜欢', '关系', '称呼', '本人', '希望', '讨厌', '欣赏', '习惯', '忌讳', '介意', '不要', '别用'];

// ---- 全局配置（记忆库位置持久化，固定 ~/.yottamemory/config.json）----
function configPath() {
  if (process.env.YOTTA_MEMORY_CONFIG_DIR) {
    return path.join(path.resolve(process.env.YOTTA_MEMORY_CONFIG_DIR), CONFIG_FILE);
  }
  return path.join(os.homedir(), '.yottamemory', CONFIG_FILE);
}
function loadConfig() {
  try { return JSON.parse(fs.readFileSync(configPath(), 'utf8')) || {}; } catch (e) { return {}; }
}
function saveConfig(cfg) {
  fs.mkdirSync(path.dirname(configPath()), { recursive: true });
  decayConfigCache = null;
  fs.writeFileSync(configPath(), JSON.stringify(cfg, null, 2), 'utf8');
}
function userRoot() {
  if (process.env.YOTTA_MEMORY_HOME) return process.env.YOTTA_MEMORY_HOME;
  const cfg = loadConfig();
  if (cfg.memory_home) return cfg.memory_home;
  return path.join(os.homedir(), '.yottamemory');
}
function projectRoot() {
  return path.join(process.cwd(), '.yottamemory');
}
function memoryRootId(root) {
  let resolved = path.resolve(String(root));
  if (process.platform === 'win32') resolved = resolved.toLowerCase();
  return crypto.createHash('sha256').update(resolved, 'utf8').digest('hex');
}
// 唯一化记忆库根：projectRoot 与 userRoot 可能指向同一目录（如 cwd=home 或其父时），
// 若不唯一化，recall/context 等会对同一索引遍历两次 -> 同一条记忆重复展示（v0.6.5 修复）。
function memoryRoots() {
  const out = [], seen = new Set();
  for (const r of [projectRoot(), userRoot()]) {
    const abs = path.resolve(r);
    if (!fs.existsSync(abs)) continue;
    if (seen.has(abs)) continue;
    seen.add(abs);
    out.push(abs);
  }
  return out;
}
// ---- v0.16.0 M2: runtime stable entry ----
const RUNTIME_SCHEMA = 1;
function runtimeRoot() {
  if (process.env.YOTTA_MEMORY_RUNTIME_HOME) return path.resolve(process.env.YOTTA_MEMORY_RUNTIME_HOME);
  return path.join(path.dirname(configPath()), 'runtime');
}
function runtimeManifestPath() { return path.join(runtimeRoot(), 'runtime.json'); }
function runtimeVersionsDir() { return path.join(runtimeRoot(), 'versions'); }
function runtimeVersionDir(version) { return path.join(runtimeVersionsDir(), String(version)); }
function runtimeCurrentDir() { return path.join(runtimeRoot(), 'current'); }
function runtimeCurrentBin() { return path.join(runtimeCurrentDir(), 'bin', 'yotta-memory.js'); }
function isSafeRuntimeVersion(version) {
  const value = String(version || '').trim();
  if (!value || value === '.' || value === '..') return false;
  if (!/^[0-9A-Za-z][0-9A-Za-z.+-]*$/.test(value)) return false;
  return !/[\\/]/.test(value);
}
function runtimePathWithin(parent, child) {
  const p = path.resolve(parent);
  const c = path.resolve(child);
  return c === p || c.indexOf(p + path.sep) === 0;
}
function readRuntimeManifest() {
  try {
    const parsed = JSON.parse(fs.readFileSync(runtimeManifestPath(), 'utf8'));
    if (!parsed || typeof parsed !== 'object') return null;
    return parsed;
  } catch (e) {
    return null;
  }
}
function writeRuntimeManifest(manifest) {
  fs.mkdirSync(runtimeRoot(), { recursive: true });
  const target = runtimeManifestPath();
  const temp = target + '.tmp-' + process.pid + '-' + Date.now();
  fs.writeFileSync(temp, JSON.stringify(manifest, null, 2) + '\n', 'utf8');
  fs.renameSync(temp, target);
}
function runtimeTreeHash(dir) {
  const hash = crypto.createHash('sha256');
  function walk(rel) {
    const full = path.join(dir, rel);
    const entries = fs.readdirSync(full, { withFileTypes: true })
      .sort(function (a, b) { return a.name < b.name ? -1 : (a.name > b.name ? 1 : 0); });
    for (const entry of entries) {
      if (entry.name === '.git' || entry.name === 'node_modules') continue;
      const childRel = rel ? path.join(rel, entry.name) : entry.name;
      const childFull = path.join(dir, childRel);
      if (entry.isDirectory()) {
        walk(childRel);
      } else if (entry.isFile()) {
        hash.update(childRel.replace(/\\/g, '/') + '\0');
        hash.update(fs.readFileSync(childFull));
        hash.update('\0');
      }
    }
  }
  walk('');
  return hash.digest('hex');
}
function runtimePackageVersion(dir) {
  const pkgPath = path.join(dir, 'package.json');
  const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
  const version = String(pkg.version || '').trim();
  if (!isSafeRuntimeVersion(version)) throw new Error('runtime 包版本非法: ' + version);
  return version;
}
function runtimeVerifyVersionDir(dir, expected, manifest) {
  if (!fs.existsSync(dir)) return { error: true, text: 'runtime 版本目录不存在: ' + dir };
  let version = '';
  try { version = runtimePackageVersion(dir); } catch (e) { return { error: true, text: e.message }; }
  if (version !== expected) return { error: true, text: 'runtime 版本不一致: 目录为 ' + version + '，请求 ' + expected };
  if (!fs.existsSync(path.join(dir, 'bin', 'yotta-memory.js'))) {
    return { error: true, text: 'runtime 版本缺少 bin/yotta-memory.js: ' + dir };
  }
  const treeHash = runtimeTreeHash(dir);
  const record = manifest && manifest.versions && manifest.versions[expected];
  if (record && record.treeHash && record.treeHash !== treeHash) {
    return { error: true, text: 'runtime 版本内容哈希与 runtime.json 不一致；请重新安装 ' + expected, treeHash: treeHash };
  }
  return { error: false, treeHash: treeHash };
}
function compareRuntimeVersions(a, b) {
  const pa = String(a).split('.').map(function (x) { return parseInt(x, 10) || 0; });
  const pb = String(b).split('.').map(function (x) { return parseInt(x, 10) || 0; });
  for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
    const d = (pa[i] || 0) - (pb[i] || 0);
    if (d !== 0) return d;
  }
  return String(a).localeCompare(String(b));
}
function runtimeListVersions() {
  const dir = runtimeVersionsDir();
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter(function (name) {
    if (!isSafeRuntimeVersion(name)) return false;
    return fs.existsSync(path.join(dir, name, 'package.json'));
  }).sort(function (a, b) { return compareRuntimeVersions(b, a); });
}
function runtimeManagedScript() {
  const current = runtimeCurrentBin();
  return fs.existsSync(current) ? current : __filename;
}
function runtimePatternToRegExp(pattern) {
  const escaped = String(pattern).split('*').map(function (part) {
    return part.replace(/[.+?^${}()|[\]\\]/g, '\\$&');
  }).join('.*');
  return new RegExp('^' + escaped + '$');
}
function runtimeMatchExclude(rel, pattern) {
  const r = String(rel).replace(/\\/g, '/');
  const p = String(pattern).replace(/\\/g, '/').replace(/^\.\//, '');
  if (p.indexOf('*') === -1) return r === p || r.indexOf(p.replace(/\/$/, '') + '/') === 0;
  return runtimePatternToRegExp(p).test(r);
}
function runtimeCopyTreeFiltered(src, dst, excludes, relBase) {
  const base = relBase ? relBase + '/' : '';
  const entries = fs.readdirSync(src, { withFileTypes: true });
  fs.mkdirSync(dst, { recursive: true });
  for (const entry of entries) {
    if (entry.name === '.git' || entry.name === 'node_modules') continue;
    const rel = base + entry.name;
    if (excludes.some(function (pattern) { return runtimeMatchExclude(rel, pattern); })) continue;
    const source = path.join(src, entry.name);
    const target = path.join(dst, entry.name);
    if (entry.isDirectory()) runtimeCopyTreeFiltered(source, target, excludes, rel);
    else if (entry.isFile()) fs.copyFileSync(source, target);
  }
}
function runtimeCopyTree(src, dst) {
  const st = fs.statSync(src);
  if (st.isDirectory()) {
    runtimeCopyTreeFiltered(src, dst, [], '');
  } else if (st.isFile()) {
    fs.mkdirSync(path.dirname(dst), { recursive: true });
    fs.copyFileSync(src, dst);
  }
}
function runtimeCopyPackageFromRoot(srcRoot, dstRoot) {
  const pkg = JSON.parse(fs.readFileSync(path.join(srcRoot, 'package.json'), 'utf8'));
  const files = Array.isArray(pkg.files) ? pkg.files : [];
  const includes = ['package.json'].concat(files.filter(function (entry) { return entry && entry[0] !== '!'; }));
  const excludes = files.filter(function (entry) { return entry && entry[0] === '!'; }).map(function (entry) { return entry.slice(1); });
  for (const entry of includes) {
    const rel = String(entry).replace(/^\.\//, '');
    const source = path.join(srcRoot, rel);
    if (!fs.existsSync(source)) continue;
    const target = path.join(dstRoot, rel);
    const st = fs.statSync(source);
    if (st.isDirectory()) {
      runtimeCopyTreeFiltered(source, target, excludes, rel);
    } else if (st.isFile() && !excludes.some(function (pattern) { return runtimeMatchExclude(rel, pattern); })) {
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.copyFileSync(source, target);
    }
  }
}
function runtimeRemoveVersionDir(version) {
  const target = runtimeVersionDir(version);
  if (!runtimePathWithin(runtimeVersionsDir(), target)) throw new Error('拒绝删除 runtime 目录外的路径: ' + target);
  if (fs.existsSync(target)) fs.rmSync(target, { recursive: true, force: true });
}
function runtimeSwitchCurrent(version) {
  const dir = runtimeVersionDir(version);
  if (!fs.existsSync(path.join(dir, 'package.json'))) throw new Error('runtime 版本未安装: ' + version);
  fs.mkdirSync(runtimeRoot(), { recursive: true });
  const temp = path.join(runtimeRoot(), '.current-' + process.pid + '-' + Date.now());
  const current = runtimeCurrentDir();
  try {
    fs.symlinkSync(dir, temp, process.platform === 'win32' ? 'junction' : 'dir');
    if (fs.existsSync(current)) {
      const st = fs.lstatSync(current);
      if (st.isSymbolicLink() || st.isFile()) fs.unlinkSync(current);
      else throw new Error('current 已存在且不是可替换的指针: ' + current);
    }
    fs.renameSync(temp, current);
  } catch (e) {
    try { if (fs.existsSync(temp)) fs.unlinkSync(temp); } catch (ignore) {}
    throw e;
  }
}
function runtimeInstallPrepared(pkgRoot, version, opts) {
  opts = opts || {};
  if (!isSafeRuntimeVersion(version)) return { error: true, text: '非法 runtime 版本: ' + version };
  fs.mkdirSync(runtimeVersionsDir(), { recursive: true });
  const finalDir = runtimeVersionDir(version);
  const staging = path.join(runtimeVersionsDir(), '.' + version + '.tmp-' + process.pid + '-' + Date.now());
  try {
    runtimeCopyTree(pkgRoot, staging);
    if (runtimePackageVersion(staging) !== version) throw new Error('安装包版本与目标版本不一致');
    if (!fs.existsSync(path.join(staging, 'bin', 'yotta-memory.js'))) throw new Error('安装包缺少 bin/yotta-memory.js');
    const treeHash = runtimeTreeHash(staging);
    if (fs.existsSync(finalDir)) {
      const existingHash = runtimeTreeHash(finalDir);
      if (existingHash === treeHash) {
        fs.rmSync(staging, { recursive: true, force: true });
        return { error: false, installed: false, version: version, treeHash: treeHash, path: finalDir, text: 'runtime ' + version + ' 已安装且内容一致。' };
      }
      if (!opts.force) throw new Error('runtime ' + version + ' 已安装且内容不同；如需覆盖请加 --force。');
      runtimeRemoveVersionDir(version);
    }
    fs.renameSync(staging, finalDir);
    const previousManifest = readRuntimeManifest();
    const manifest = previousManifest || { schema: RUNTIME_SCHEMA, current: '', previous: '', versions: {}, updatedAt: '' };
    manifest.schema = RUNTIME_SCHEMA;
    manifest.versions = manifest.versions || {};
    manifest.versions[version] = Object.assign({}, manifest.versions[version], {
      version: version,
      path: finalDir,
      treeHash: treeHash,
      installedAt: new Date().toISOString(),
      source: opts.source || 'unknown',
    });
    if (!manifest.current) manifest.current = version;
    manifest.updatedAt = new Date().toISOString();
    writeRuntimeManifest(manifest);
    if (manifest.current === version) {
      try {
        runtimeSwitchCurrent(version);
      } catch (e) {
        if (previousManifest) writeRuntimeManifest(previousManifest);
        return { error: true, text: '切换 current 失败: ' + e.message };
      }
    }
    return { error: false, installed: true, version: version, treeHash: treeHash, path: finalDir, text: '已安装 runtime ' + version + ' 到 ' + finalDir };
  } catch (e) {
    try { if (fs.existsSync(staging)) fs.rmSync(staging, { recursive: true, force: true }); } catch (ignore) {}
    return { error: true, text: e.message };
  }
}
function runtimeValidateTarballEntries(entries) {
  const normalized = (entries || []).map(function (entry) {
    return String(entry || '').replace(/\\/g, '/').replace(/\/+$/, '');
  }).filter(Boolean);
  if (!normalized.length) throw new Error('runtime tarball 为空');
  for (const entry of normalized) {
    if (entry[0] === '/' || /^[A-Za-z]:/.test(entry)) throw new Error('runtime tarball 含绝对路径成员: ' + entry);
    const parts = entry.split('/');
    if (parts.indexOf('..') !== -1) throw new Error('runtime tarball 含路径穿越成员: ' + entry);
    if (parts[0] !== 'package') throw new Error('runtime tarball 含 package/ 之外的成员: ' + entry);
  }
  if (normalized.indexOf('package/package.json') === -1) throw new Error('runtime tarball 缺少 package/package.json');
}
function runtimeListTarballEntries(tarball) {
  const tarBin = process.env.YOTTA_RUNTIME_TAR || 'tar';
  const listed = child_process.spawnSync(tarBin, ['-tzf', path.basename(tarball)], {
    cwd: path.dirname(tarball),
    encoding: 'utf8',
    maxBuffer: 8 * 1024 * 1024,
  });
  if (listed.error) throw new Error('无法执行 tar: ' + listed.error.message);
  if (listed.status !== 0) throw new Error('读取 runtime tarball 失败: ' + String(listed.stderr || listed.stdout || '').trim());
  return String(listed.stdout || '').split(/\r?\n/).filter(Boolean);
}
function runtimeExtractTarball(tarball, tempDir) {
  runtimeValidateTarballEntries(runtimeListTarballEntries(tarball));
  const tarBin = process.env.YOTTA_RUNTIME_TAR || 'tar';
  const relativeTarball = path.relative(tempDir, tarball).replace(/\\/g, '/');
  const result = child_process.spawnSync(tarBin, ['-xzf', relativeTarball], { cwd: tempDir, encoding: 'utf8' });
  if (result.error) throw new Error('无法执行 tar: ' + result.error.message);
  if (result.status !== 0) throw new Error('解压 runtime tarball 失败: ' + String(result.stderr || result.stdout || '').trim());
  const packaged = path.join(tempDir, 'package');
  if (fs.existsSync(path.join(packaged, 'package.json'))) return packaged;
  if (fs.existsSync(path.join(tempDir, 'package.json'))) return tempDir;
  throw new Error('runtime tarball 中未找到 package/package.json');
}
function runtimeInstallFromCurrent(opts) {
  opts = opts || {};
  const srcRoot = path.join(__dirname, '..');
  const pkgPath = path.join(srcRoot, 'package.json');
  if (!fs.existsSync(pkgPath)) return { error: true, text: '当前运行时不是完整 npm 包（缺少 package.json），无法安装稳定入口。' };
  let version = '';
  try { version = runtimePackageVersion(srcRoot); } catch (e) { return { error: true, text: e.message }; }
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'ytm-runtime-current-'));
  try {
    const staged = path.join(temp, 'package');
    runtimeCopyPackageFromRoot(srcRoot, staged);
    return runtimeInstallPrepared(staged, version, { source: 'current', force: !!opts.force });
  } catch (e) {
    return { error: true, text: e.message };
  } finally {
    try { fs.rmSync(temp, { recursive: true, force: true }); } catch (ignore) {}
  }
}
function runtimeInstallTarball(tarball, requestedVersion, opts) {
  opts = opts || {};
  const abs = path.resolve(String(tarball || ''));
  if (!fs.existsSync(abs) || !fs.statSync(abs).isFile()) return { error: true, text: 'runtime tarball 不存在: ' + abs };
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'ytm-runtime-tarball-'));
  try {
    const pkgRoot = runtimeExtractTarball(abs, temp);
    const version = runtimePackageVersion(pkgRoot);
    if (requestedVersion && String(requestedVersion) !== version) {
      throw new Error('runtime 包版本 ' + version + ' 与请求版本 ' + requestedVersion + ' 不一致');
    }
    return runtimeInstallPrepared(pkgRoot, version, { source: abs, force: !!opts.force });
  } catch (e) {
    return { error: true, text: e.message };
  } finally {
    try { fs.rmSync(temp, { recursive: true, force: true }); } catch (ignore) {}
  }
}
function runtimeNpmSpec() {
  const candidates = [];
  if (process.env.npm_execpath) candidates.push(process.env.npm_execpath);
  candidates.push(path.join(path.dirname(process.execPath), 'node_modules', 'npm', 'bin', 'npm-cli.js'));
  candidates.push(path.resolve(path.dirname(process.execPath), '..', 'lib', 'node_modules', 'npm', 'bin', 'npm-cli.js'));
  for (const candidate of candidates) {
    if (candidate && fs.existsSync(candidate)) return { command: process.execPath, args: [path.resolve(candidate)] };
  }
  return null;
}
function runtimeRunNpm(args, opts) {
  const spec = runtimeNpmSpec();
  if (!spec) throw new Error('无法定位 npm CLI；请改用 runtime install <本地 tarball>。');
  const result = child_process.spawnSync(spec.command, spec.args.concat(args), {
    cwd: (opts && opts.cwd) || process.cwd(),
    encoding: 'utf8',
    timeout: 120000,
  });
  if (result.error) throw new Error('npm 执行失败: ' + result.error.message);
  if (result.status !== 0) throw new Error('npm 执行失败: ' + String(result.stderr || result.stdout || '').trim());
  return result;
}
function runtimeInstallVersion(version, opts) {
  const target = String(version || '').trim();
  if (!isSafeRuntimeVersion(target)) return { error: true, text: '非法 runtime 版本: ' + target };
  if (target === VERSION) return runtimeInstallFromCurrent(opts);
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'ytm-runtime-pack-'));
  try {
    fs.mkdirSync(runtimeRoot(), { recursive: true });
    runtimeRunNpm(['pack', '@yottameta/yotta-memory@' + target, '--pack-destination', temp], { cwd: runtimeRoot() });
    const tarball = fs.readdirSync(temp).filter(function (name) { return /\.tgz$/i.test(name); })[0];
    if (!tarball) throw new Error('npm pack 未生成 tarball');
    return runtimeInstallTarball(path.join(temp, tarball), target, opts);
  } catch (e) {
    return { error: true, text: e.message };
  } finally {
    try { fs.rmSync(temp, { recursive: true, force: true }); } catch (ignore) {}
  }
}
function runtimeUseCore(version, opts) {
  opts = opts || {};
  const target = String(version || '').trim();
  if (!isSafeRuntimeVersion(target)) return { error: true, text: '非法 runtime 版本: ' + target };
  const manifest = readRuntimeManifest();
  if (!manifest) return { error: true, text: 'runtime 未初始化，请先运行 yotta-memory runtime install --from-current。' };
  const dir = runtimeVersionDir(target);
  if (!fs.existsSync(dir)) return { error: true, text: 'runtime 版本未安装: ' + target };
  const check = runtimeVerifyVersionDir(dir, target, manifest);
  if (check.error) return check;
  const previous = manifest.current && manifest.current !== target ? manifest.current : (manifest.previous && manifest.previous !== target ? manifest.previous : '');
  const previousManifest = JSON.parse(JSON.stringify(manifest));
  try {
    runtimeSwitchCurrent(target);
  } catch (e) {
    return { error: true, text: '切换 current 失败: ' + e.message };
  }
  manifest.schema = RUNTIME_SCHEMA;
  manifest.current = target;
  manifest.previous = previous || '';
  manifest.updatedAt = new Date().toISOString();
  manifest.versions = manifest.versions || {};
  manifest.versions[target] = Object.assign({}, manifest.versions[target], { treeHash: check.treeHash, lastUsedAt: new Date().toISOString() });
  try {
    writeRuntimeManifest(manifest);
  } catch (e) {
    try { if (previous) runtimeSwitchCurrent(previous); } catch (ignore) {}
    return { error: true, text: '写入 runtime.json 失败: ' + e.message };
  }
  let tail = '；如需重启受管 server，请加 --restart';
  if (opts.restart) {
    const restart = opts.restartFn ? opts.restartFn() : runtimeRestartManagedServer();
    if (restart && restart.error) {
      let rollbackText = '';
      if (previous) {
        try {
          runtimeSwitchCurrent(previous);
          const rollback = JSON.parse(JSON.stringify(previousManifest));
          rollback.current = previous;
          rollback.previous = target;
          rollback.updatedAt = new Date().toISOString();
          writeRuntimeManifest(rollback);
          (opts.restartFn ? opts.restartFn() : runtimeRestartManagedServer());
          rollbackText = '；已回滚 current 到 ' + previous;
        } catch (e) {
          rollbackText = '；回滚失败: ' + e.message;
        }
      }
      return { error: true, text: '受管 server 重启失败: ' + (restart.text || '') + rollbackText };
    }
    tail = '；受管 server 已重启';
  }
  return { error: false, text: '已切换 current 到 ' + target + tail + '。', version: target, treeHash: check.treeHash };
}
function runtimeRollbackCore(opts) {
  const manifest = readRuntimeManifest();
  if (!manifest || !manifest.current) return { error: true, text: 'runtime 未初始化或没有当前版本。' };
  if (!manifest.previous) return { error: true, text: '没有可回滚的 runtime 版本。' };
  const target = manifest.previous;
  const result = runtimeUseCore(target, opts);
  if (result.error) return result;
  return { error: false, text: '已回滚 current 到 ' + target + '。' + result.text, version: target };
}
function runtimeStatusCore() {
  const root = runtimeRoot();
  const manifest = readRuntimeManifest();
  const lines = ['runtime root: ' + root];
  const drift = [];
  if (!manifest) {
    lines.push('runtime: 未初始化');
    lines.push('提示: yotta-memory runtime install --from-current');
    return { error: false, text: lines.join('\n'), runtimeRoot: root, drift: ['runtime manifest missing'] };
  }
  lines.push('current: ' + (manifest.current || '(none)'));
  lines.push('current path: ' + runtimeCurrentDir());
  if (manifest.previous) lines.push('previous: ' + manifest.previous);
  if (!manifest.current) drift.push('current version missing in runtime.json');
  else {
    const dir = runtimeVersionDir(manifest.current);
    if (!fs.existsSync(dir)) drift.push('current version dir missing');
    if (!fs.existsSync(runtimeCurrentBin())) drift.push('current launcher missing');
    else {
      try {
        const real = fs.realpathSync(runtimeCurrentDir());
        if (path.resolve(real) !== path.resolve(dir)) drift.push('current pointer mismatch');
      } catch (e) {
        drift.push('current pointer unreadable');
      }
    }
  }
  const versions = runtimeListVersions();
  lines.push('versions: ' + (versions.length ? versions.join(', ') : '(none)'));
  lines.push('drift: ' + (drift.length ? drift.join('; ') : 'none'));
  return { error: false, text: lines.join('\n'), runtimeRoot: root, manifest: manifest, drift: drift };
}
function runtimeListCore() {
  const manifest = readRuntimeManifest() || { current: '', versions: {} };
  const versions = runtimeListVersions();
  const lines = ['runtime versions:'];
  if (!versions.length) lines.push('  (none)');
  for (const version of versions) {
    const record = (manifest.versions && manifest.versions[version]) || {};
    lines.push('  ' + version + (manifest.current === version ? '  [current]' : '') + (record.treeHash ? '  ' + record.treeHash.slice(0, 12) + '...' : ''));
  }
  return { error: false, text: lines.join('\n'), versions: versions, current: manifest.current || '' };
}
function runtimeExecutionPath() {
  const invoked = process.argv && process.argv[1] ? path.resolve(process.argv[1]) : '';
  if (invoked && path.basename(invoked).toLowerCase() === 'yotta-memory.js') return invoked;
  return path.resolve(__filename);
}
function runtimeEnsureForManagedTask() {
  const manifest = readRuntimeManifest();
  if (manifest && manifest.current) {
    const check = runtimeVerifyVersionDir(runtimeVersionDir(manifest.current), manifest.current, manifest);
    if (!check.error && fs.existsSync(runtimeCurrentBin())) {
      return { error: false, text: 'runtime current 已就绪: ' + manifest.current, version: manifest.current };
    }
  }
  return runtimeInstallFromCurrent({ force: false });
}
function runtimeRestartManagedServer() {
  const platform = lanPlatform();
  if (platform === 'win32') {
    const query = child_process.spawnSync('schtasks', ['/query', '/tn', LAN_TASK_NAME, '/fo', 'LIST'], { encoding: 'utf8' });
    if (query.status !== 0) return { error: true, text: '未检测到受管计划任务 ' + LAN_TASK_NAME + '。' };
    const end = child_process.spawnSync('schtasks', ['/end', '/tn', LAN_TASK_NAME], { encoding: 'utf8' });
    const run = child_process.spawnSync('schtasks', ['/run', '/tn', LAN_TASK_NAME], { encoding: 'utf8' });
    if (run.status !== 0) return { error: true, text: '计划任务重启失败: ' + String(run.stderr || run.stdout || '').trim() };
    return { error: false, text: '已重启计划任务 ' + LAN_TASK_NAME + (end.status === 0 ? '' : '（原任务未在运行）') };
  }
  if (platform === 'linux') {
    const unit = lanLinuxUnitPath();
    if (fs.existsSync(unit) && lanFileHasMarker(unit)) {
      const result = lanLinuxSystemctl(['restart', LAN_UNIT_NAME]);
      if (result.status !== 0) return { error: true, text: 'systemd 重启失败: ' + String(result.err || '').trim() };
      return { error: false, text: '已重启 systemd 用户单元 ' + LAN_UNIT_NAME };
    }
    if (lanCrontabHasOurLine(lanCrontabRead())) {
      return { error: true, text: '受管 server 由 crontab @reboot 启动，无法在线重启；请手动重启。' };
    }
  }
  return { error: true, text: '未检测到可管理的 server 自启配置，未执行重启。' };
}
function today(override) {
  if (override && /^\d{4}-\d{2}-\d{2}$/.test(String(override))) return String(override);
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
}
let RUNTIME_AGENT = { id: '', agentKey: '' };
const IDENTITY_CONTEXT = new AsyncLocalStorage();
// v0.21.0：view 用户会话的 owner 密钥上下文——请求处理期间让读 / 写 / 索引路径复用已解锁的 ownerKeys。
const VIEW_KEYS_CONTEXT = new AsyncLocalStorage();
const RUNTIME_OWNER_KEYS = new Map();
function setRuntimeAgent(id, agentKey) {
  RUNTIME_AGENT = { id: String(id || '').trim(), agentKey: String(agentKey || '').trim() };
  RUNTIME_OWNER_KEYS.clear();
}
function currentRuntimeIdentity() {
  return IDENTITY_CONTEXT.getStore() || RUNTIME_AGENT;
}
function runWithIdentity(identity, fn) {
  const store = {
    id: String((identity && identity.id) || '').trim(),
    agentKey: String((identity && identity.agentKey) || '').trim(),
  };
  return IDENTITY_CONTEXT.run(store, fn);
}
function legacyIdentityEnvNames() {
  return ['YOTTA_AGENT_ID', 'AGENT_ID', 'YOTTA_MEMORY_AGENT_KEY', 'YOTTA_MEMORY_TRUST_ENV_AGENT']
    .filter(function (name) { return String(process.env[name] || '').trim() !== ''; });
}
function legacyIdentityEnvError() {
  const names = legacyIdentityEnvNames();
  if (!names.length) return '';
  return [
    '[YTM_IDENTITY_ENV_REMOVED] 检测到旧身份环境变量: ' + names.join(', '),
    '0.16.0 已删除身份 env：HTTP / 远程 MCP 只用请求头 Authorization + X-Agent-Id + X-Agent-Key；stdio MCP 只用显式参数 --agent-id <id> + --agent-key-file <path>。',
    'CLI 仍使用 --agent <id> + --agent-key/--agent-key-file。请从宿主 MCP 配置中移除身份 env 后重试。',
  ].join('\n');
}
function resolveIdentity(opts) {
  opts = opts || {};
  const explicitAgent = String(opts.agent || opts.selfAgent || '').trim();
  const explicitAgentId = String(opts.agentId || '').trim();
  if (explicitAgent && explicitAgentId && explicitAgent !== explicitAgentId) {
    return { id: '', agentKey: '', source: 'conflict', error: '身份冲突：--agent ' + explicitAgent + ' 与 --agent-id ' + explicitAgentId + ' 不一致，请只保留一个身份参数。' };
  }
  const explicit = explicitAgent || explicitAgentId;
  let explicitKey = String(opts.agentKey || '').trim();
  const keyFile = String(opts.agentKeyFile || '').trim();
  if (keyFile) {
    let fileKey = '';
    try { fileKey = fs.readFileSync(path.resolve(keyFile), 'utf8').trim(); } catch (e) {
      if (e && e.code === 'ENOENT') {
        return {
          id: explicit,
          agentKey: '',
          source: 'missing-key-file',
          keyFile: keyFile,
          warning: '未找到 agent-key 文件: ' + keyFile + '；已降级为未授权模式（公共 FACT 可读，私密操作需要显式授权）。',
          error: '',
        };
      }
      return { id: '', agentKey: '', source: 'invalid-key-file', error: '无法读取 agent-key 文件: ' + keyFile };
    }
    if (!fileKey) return { id: '', agentKey: '', source: 'invalid-key-file', error: 'agent-key 文件为空: ' + keyFile };
    if (explicitKey && explicitKey !== fileKey) return { id: '', agentKey: '', source: 'key-conflict', error: '--agent-key 与 --agent-key-file 内容不一致。' };
    explicitKey = fileKey;
  }
  if (explicit && !isSafeAgentId(explicit)) {
    return { id: '', agentKey: '', source: 'invalid', error: '非法 agent ID：只允许单段名称，禁止 /、\\、.. 和控制字符。' };
  }
  if (explicit) {
    return { id: explicit, agentKey: explicitKey, source: 'explicit', error: '' };
  }
  return { id: '', agentKey: '', source: 'none', error: '' };
}
function identityDiagnostic(ident) {
  ident = ident || {};
  const invalid = !!ident.error;
  const authenticated = !invalid && !!ident.agentKey;
  const mode = invalid ? 'invalid' : (authenticated ? 'authenticated' : (ident.id ? 'unauthenticated' : 'anonymous'));
  const agentKeyStatus = invalid ? 'invalid' : (authenticated ? 'present' : (ident.source === 'missing-key-file' ? 'missing' : 'not-provided'));
  const out = {
    agentId: ident.id || '',
    mode: mode,
    agentKeyStatus: agentKeyStatus,
    source: ident.source || 'none',
  };
  if (ident.keyFile) out.keyFile = path.resolve(String(ident.keyFile));
  if (ident.source === 'missing-key-file') {
    out.action = '由用户在 yotta-memory view 中授权，或执行 yotta-memory key bind ' + (ident.id || '<id>') + '；随后 AI 执行 key status / key claim。';
  }
  return out;
}

/** 写操作身份回显：让 AI / 用户当场看到本次写入使用的 agent_id 与来源。 */
function identityWriteNote(ident, opts) {
  opts = opts || {};
  if (opts.userUnlocked) return '';
  const id = ident && ident.id ? ident.id : '未声明';
  const source = ident && ident.source ? ident.source : 'none';
  let note = '[身份] agent_id: ' + id + '；来源: ' + source;
  const hostHome = process.env.YOTTA_MEMORY_AGENT_HOME;
  if (hostHome) {
    note += '\n[注意] 检测到宿主身份环境 YOTTA_MEMORY_AGENT_HOME=' + hostHome +
      '；如果这不是本会话 AI 的身份，请显式传 --agent <id> --agent-key-file <path> 覆盖后重试。';
  }
  return note;
}

function isSafeAgentId(id) {
  const value = String(id || '');
  if (!value || value.length > 128) return false;
  if (value === '.' || value === '..') return false;
  if (/[\\/]/.test(value)) return false;
  if (/[\u0000-\u001f]/.test(value)) return false;
  return true;
}
function typeDir(type) {
  const t = String(type).toUpperCase();
  if (!TYPE_DIRS[t]) {
    console.error('未知记忆类型: ' + type + '（可用: ' + TYPES.join(' / ') + '）');
    process.exit(2);
  }
  return TYPE_DIRS[t];
}
function privateIdDir(root, id) { return path.join(root, PRIVATE_DIR, id); }
// 布局：FACT -> <root>/facts；PREF/BOUND/COMMIT -> <root>/private/<owner>/<type>
function typeSubdir(type, owner) {
  const t = String(type).toUpperCase();
  if (t === 'FACT') return PUBLIC_DIR;
  const id = owner || '';
  return path.join(PRIVATE_DIR, id, TYPE_DIRS[t]);
}
// v0.24.0 规模：新写入按 <yyyy>/<mm>/<dd> 分层（公共 facts/<yyyy>/<mm>/<dd>/，
// 私密 private/<owner>/<type>/<yyyy>/<mm>/<dd>/）。
// 只影响新写入；旧平铺文件保持原位继续可读，不自动迁移。
function dateSubdir(dateStr) {
  const d = String(dateStr || '');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) return '';
  return path.join(d.slice(0, 4), d.slice(5, 7), d.slice(8, 10));
}
function entryWriteDir(root, type, owner, dateStr) {
  const base = path.join(root, typeSubdir(type, owner));
  const sub = dateSubdir(dateStr);
  return sub ? path.join(base, sub) : base;
}
// 归档保留年/月分层（不同月份的同名文件不再互相覆盖）；旧平铺文件仍按原样落到归档根。
const MEMORY_FILE_RE = /\.md(\.enc)?$/;
function entryRelParts(rel) {
  const seg = String(rel || '').replace(/\\/g, '/').split('/').filter(Boolean);
  if (seg[0] === PRIVATE_DIR) return { kind: 'private', owner: seg[1] || '', type: seg[2] || '' };
  if (seg[0] === PUBLIC_DIR) return { kind: 'public', owner: '', type: 'facts' };
  return null;
}
function archiveRelFor(root, rel, type, owner) {
  const parts = entryRelParts(rel);
  const t = String(type || (parts && parts.type) || 'FACT').toUpperCase();
  const normalized = String(rel || '').replace(/\\/g, '/');
  const seg = normalized.split('/');
  const idx = seg.findIndex(function (s) { return /^\d{4}$/.test(s); });
  const sub = (idx >= 0 && /^\d{2}$/.test(seg[idx + 1] || '')) ? seg[idx] + '/' + seg[idx + 1] : '';
  const baseName = path.basename(normalized);
  if (t === 'FACT' || (parts && parts.kind === 'public')) {
    return path.posix.join(ARCHIVE_DIR, 'facts', sub, baseName);
  }
  const o = owner || (parts && parts.owner) || '';
  return path.posix.join(ARCHIVE_DIR, PRIVATE_DIR, o, TYPE_DIRS[t] || 'facts', sub, baseName);
}
function defaultScope(type) {
  return PRIVATE_TYPES.indexOf(String(type).toUpperCase()) === -1 ? 'public' : 'private';
}
// ---- 安全边界：路径必须落在记忆库根内（防 MCP 任意路径读写，v0.8.5）----
function resolveWithinRoot(root, p) {
  let abs = path.isAbsolute(p) ? path.resolve(p) : path.resolve(root, p);
  const r = path.resolve(root);
  if (abs === r) return abs;
  if (abs.startsWith(r + path.sep)) return abs;
  return null;
}
function isWithinRoot(root, p) { return !!resolveWithinRoot(root, p); }
// 把命令行安全拆分为 argv（支持 ' " 引号包参，但绝不经过 shell，防元字符注入）
function splitCommandArgv(s) {
  const argv = [];
  let cur = '';
  let quote = null;
  for (let i = 0; i < String(s).length; i++) {
    const c = String(s)[i];
    if (quote) {
      if (c === quote) { quote = null; continue; }
      if (c === '\\' && quote === '"') { cur += String(s)[i + 1] || ''; i++; continue; }
      cur += c; continue;
    }
    if (c === '"' || c === "'") { quote = c; continue; }
    if (c === ' ' || c === '\t') { if (cur) { argv.push(cur); cur = ''; } continue; }
    cur += c;
  }
  if (cur) argv.push(cur);
  return argv;
}
// 模型命令允许清单：环境变量 YOTTA_DISTILL_MODELS（逗号分隔可执行名，不含扩展名）或 config.distill_models；
// 未配置时放行（本地宿主 CLI 自担风险，但已去除 shell 注入面）；MCP 已在上层直接拒绝 model，不达此处。
function distillModelAllowlist() {
  const env = (process.env.YOTTA_DISTILL_MODELS || '').split(',').map(function (x) { return x.trim().toLowerCase(); }).filter(Boolean);
  if (env.length) return env;
  const cfg = loadConfig();
  const c = cfg && (cfg.distill_models || []);
  if (Array.isArray(c) && c.length) return c.map(function (x) { return String(x).trim().toLowerCase(); }).filter(Boolean);
  return null;
}
// 安全执行外部模型命令：仅允许清单内可执行名；argv 分离、不经 shell。
function runDistillModel(modelStr, payload) {
  const argv = splitCommandArgv(modelStr);
  if (!argv.length) throw new Error('模型命令为空');
  const base = path.basename(argv[0]).toLowerCase().replace(/\.exe$/i, '');
  const allow = distillModelAllowlist();
  if (allow && allow.length && allow.indexOf(base) === -1) {
    throw new Error('模型命令不在允许清单内: ' + base + '（可用: ' + allow.join(', ') + '；或设环境变量 YOTTA_DISTILL_MODELS）');
  }
  const r = child_process.spawnSync(argv[0], argv.slice(1), { input: payload, encoding: 'utf8', maxBuffer: 1024 * 1024, shell: false, windowsHide: true });
  return r;
}
function cosineSimilarity(a, b) {
  if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return 0;
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) {
    const x = Number(a[i]) || 0;
    const y = Number(b[i]) || 0;
    dot += x * y;
    na += x * x;
    nb += y * y;
  }
  if (!na || !nb) return 0;
  return dot / (Math.sqrt(na) * Math.sqrt(nb));
}
function runEmbeddingPlugin(command, texts, timeoutMs) {
  const argv = splitCommandArgv(String(command || ''));
  if (!argv.length) throw new Error('embedding 命令为空');
  const payload = JSON.stringify({ texts: (texts || []).map(String) });
  const timeout = Math.max(1, parseInt(timeoutMs, 10) || 3000);
  const r = child_process.spawnSync(argv[0], argv.slice(1), {
    input: payload,
    encoding: 'utf8',
    maxBuffer: 1024 * 1024,
    shell: false,
    windowsHide: true,
    timeout: timeout
  });
  if (r.error) throw r.error;
  if (r.status !== 0) throw new Error('embedding 插件退出码 ' + r.status);
  const parsed = JSON.parse(String(r.stdout || ''));
  if (!parsed || !Array.isArray(parsed.vectors)) throw new Error('embedding 插件输出缺少 vectors 数组');
  if (parsed.vectors.length !== texts.length) throw new Error('embedding 向量数量不匹配');
  return parsed.vectors;
}
function embeddingCandidates(entries, query, opts) {
  opts = opts || {};
  const command = opts.embedding || '';
  if (!command) return [];
  const texts = [String(query || '')].concat((entries || []).map(function (e) {
    return [e.subject || '', e.statement || '', (e.tags || []).join(' ')].join(' ');
  }));
  const root = opts.root ? String(opts.root) : '';
  let cache = {};
  let cachePath = '';
  if (root) {
    cachePath = path.join(root, '.embed', 'cache.json');
    try {
      fs.mkdirSync(path.dirname(cachePath), { recursive: true });
      cache = JSON.parse(fs.readFileSync(cachePath, 'utf8'));
    } catch (err) {
      cache = {};
    }
  }
  const keys = texts.map(function (text) {
    return crypto.createHash('sha256').update(command + '\0' + text).digest('hex');
  });
  const missing = [];
  const missingIndexes = [];
  const vectors = new Array(texts.length);
  for (let i = 0; i < texts.length; i++) {
    if (cache[keys[i]]) {
      vectors[i] = cache[keys[i]];
    } else {
      missing.push(texts[i]);
      missingIndexes.push(i);
    }
  }
  if (missing.length) {
    const missingVectors = runEmbeddingPlugin(command, missing, opts.embeddingTimeout);
    for (let i = 0; i < missingVectors.length; i++) {
      const idx = missingIndexes[i];
      vectors[idx] = missingVectors[i];
      cache[keys[idx]] = missingVectors[i];
    }
    if (cachePath) {
      try { fs.writeFileSync(cachePath, JSON.stringify(cache, null, 2), 'utf8'); } catch (err) {}
    }
  }
  const queryVec = vectors[0];
  const out = [];
  for (let i = 1; i < vectors.length; i++) {
    const sim = cosineSimilarity(queryVec, vectors[i]);
    if (sim > 0) out.push({ entry: entries[i - 1], score: sim, detail: ['embedding:' + round3(sim)] });
  }
  return out;
}
function effectiveEmbeddingCommand(opts) {
  opts = opts || {};
  if (opts.embedding) return String(opts.embedding);
  const cfg = loadConfig();
  return cfg && cfg.embedding_cmd ? String(cfg.embedding_cmd) : '';
}
function effectiveEmbeddingTimeout(opts) {
  opts = opts || {};
  if (opts.embeddingTimeout) return parseInt(opts.embeddingTimeout, 10) || 3000;
  const cfg = loadConfig();
  return cfg && cfg.embedding_timeout ? parseInt(cfg.embedding_timeout, 10) || 3000 : 3000;
}
function parseFrontmatter(text) {
  const m = text.match(/^---\s*\n([\s\S]*?)\n---/);
  if (!m) return { meta: {}, body: text };
  const meta = {};
  for (const line of m[1].split('\n')) {
    const i = line.indexOf(':');
    if (i === -1) continue;
    let k = line.slice(0, i).trim();
    let v = line.slice(i + 1).trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
      v = v.slice(1, -1);
    }
    const arr = parseInlineArray(v);
    meta[k] = arr === null ? v : arr;
  }
  return { meta: meta, body: text.slice(m[0][0].length + m[0].length) };
}
// 内联数组解析：标准 JSON 数组（v0.21.0+ 写出格式）正常解析；
// 历史缺陷留下的逐层 \" 转义污染在这里逐层剥离后解析，使下一次重写自动修复为规范格式。
function parseInlineArray(v) {
  const s = String(v === undefined || v === null ? '' : v).trim();
  if (!(s.startsWith('[') && s.endsWith(']'))) return null;
  let candidate = s;
  for (let i = 0; i < 6; i += 1) {
    try {
      const parsed = JSON.parse(candidate);
      if (Array.isArray(parsed)) return parsed.map(String);
    } catch (e) { /* 兼容历史转义：继续剥离一层 */ }
    if (candidate.indexOf('\\"') === -1) break;
    candidate = candidate.split('\\"').join('"');
  }
  const inner = s.slice(1, -1).trim();
  if (!inner) return [];
  return inner.split(',').map(function (x) {
    return x.trim().replace(/^["']+|["']+$/g, '');
  }).filter(Boolean);
}
function escapeYaml(v) {
  return String(v).replace(/\n/g, ' ').replace(/"/g, '\\"');
}
function parseTags(v) {
  if (Array.isArray(v)) return v.map(String);
  if (typeof v === 'string') {
    const arr = parseInlineArray(v);
    if (arr !== null) return arr;
    return v.split(',').map(function (x) {
      return x.trim().replace(/^["']+|["']+$/g, '');
    }).filter(Boolean);
  }
  return [];
}
function tokenize(s) {
  s = String(s || '').toLowerCase();
  const toks = [];
  const latin = s.match(/[a-z0-9_]+/g);
  if (latin) for (const t of latin) toks.push(t);
  const han = s.match(/[\u4e00-\u9fa5]+/g);
  if (han) {
    for (const seg of han) {
      if (seg.length === 1) toks.push(seg);
      else for (let i = 0; i < seg.length - 1; i++) toks.push(seg.slice(i, i + 2));
    }
  }
  return toks;
}
function buildTokens(subject, statement, tags) {
  const m = {};
  const add = function (tok, w) { if (tok) m[tok] = (m[tok] || 0) + w; };
  const subj = String(subject || '');
  const stmt = String(statement || '');
  const tagArr = Array.isArray(tags) ? tags : parseTags(tags);
  // v0.8.0 字段加权：subject × 3 / tags × 2 / statement × 1
  for (const t of tokenize(subj)) add(t, 3);
  for (const t of tokenize(stmt)) add(t, 1);
  for (const t of tokenize(tagArr.join(' '))) add(t, 2);
  // v0.8.0 拼音 token（py: 全拼 / pyi: 首字母），命中按 0.4 权重（去重防长文本重复字虚高）
  for (const t of new Set(pinyinTokens(subj + ' ' + stmt + ' ' + tagArr.join(' ')))) add(t, 0.4);
  return m;
}
// ---- v0.8.0 自我学习：拼音表 + 同义词表 + 语义匹配（零依赖内置数据）----
function loadPinyinTable() {
  try {
    const p = path.join(__dirname, '..', 'references', 'pinyin-common.json');
    return JSON.parse(fs.readFileSync(p, 'utf8')) || {};
  } catch (e) { return {}; }
}
const PINYIN_TABLE = loadPinyinTable();
// 同义词组：同组内互相视为同义（查询侧扩展，命中按 0.5 权重）
const SYNONYM_GROUPS = [
  ['记', '记住', '记忆', '记录', '铭记'],
  ['忘', '忘记', '遗忘', '忘掉'],
  ['读', '读取', '检索', '查询', '搜索'],
  ['写', '写入', '记录', '保存', '存储'],
  ['偏好', '喜好', '喜欢', '偏爱'],
  ['承诺', '保证', '约定'],
  ['收工', '结束', '完成', '完毕'],
  ['归档', '封存', '存档'],
  ['删除', '移除', '去掉'],
  ['更新', '修改', '刷新'],
  ['边界', '红线', '禁区', '界限'],
  ['画像', '档案', 'profile'],
  ['命令', '指令', 'cli'],
  ['记忆', 'memory', '记忆库']
];
function synonymSet(token) {
  const out = new Set();
  for (const g of SYNONYM_GROUPS) {
    if (g.indexOf(token) !== -1) { for (const w of g) out.add(w); }
  }
  return out;
}
function pinyinOf(ch) {
  const arr = PINYIN_TABLE[ch];
  if (!arr || !arr.length) return null;
  return arr[0];
}
// 中文字符串 -> 拼音 token：全拼 bigram 'py:yueyong' + 首字母 bigram 'pyi:yy'
function pinyinTokens(s) {
  const out = [];
  const han = String(s || '').match(/[\u4e00-\u9fa5]+/g);
  if (!han) return out;
  const all = han.join('');
  if (all.length === 1) {
    const p = pinyinOf(all);
    if (p) { out.push('py:' + p); out.push('pyi:' + p[0]); }
    return out;
  }
  let initials = '';
  for (let i = 0; i < all.length; i++) { const p = pinyinOf(all[i]); if (p) initials += p[0]; }
  for (let i = 0; i < all.length - 1; i++) {
    const p1 = pinyinOf(all[i]), p2 = pinyinOf(all[i + 1]);
    if (p1 && p2) out.push('py:' + p1 + p2);
  }
  for (let i = 0; i < initials.length - 1; i++) out.push('pyi:' + initials.slice(i, i + 2));
  return out;
}
function editDistance(a, b) {
  a = String(a); b = String(b);
  if (a === b) return 0;
  const la = a.length, lb = b.length;
  if (!la) return lb; if (!lb) return la;
  if (Math.abs(la - lb) > 2) return 3;
  let prev = [];
  for (let j = 0; j <= lb; j++) prev[j] = j;
  for (let i = 1; i <= la; i++) {
    const cur = [i];
    for (let j = 1; j <= lb; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
    }
    prev = cur;
  }
  return prev[lb];
}
// 语义匹配：精确(1.0×，字段加权已入 tokens) / 同义(0.5×) / 拼音(0.4×) / 子串兜底 / 模糊(0.3×)
function semanticMatch(entry, query, wantDetail) {
  const q = String(query || '').toLowerCase();
  const qtoks = tokenize(q);
  const qpy = pinyinTokens(q);
  const toks = entry.tokens || {};
  const hay = ((entry.subject || '') + ' ' + (entry.statement || '') + ' ' + (entry.tags || []).join(' ')).toLowerCase();
  let score = 0;
  const detail = [];
  const qset = new Set(qtoks);
  for (const tt of qtoks) {
    if (toks[tt]) { score += toks[tt]; if (wantDetail) detail.push('精确:' + tt + '(+' + round3(toks[tt]) + ')'); }
  }
  const ext = new Set();
  for (const tt of qtoks) { const s = synonymSet(tt); for (const w of s) ext.add(w); }
  for (const w of ext) {
    if (toks[w] && !qset.has(w)) { score += 0.5 * toks[w]; if (wantDetail) detail.push('同义:' + w + '(+' + round3(0.5 * toks[w]) + ')'); }
  }
  for (const t of qpy) {
    if (toks[t]) { score += 0.4 * toks[t]; if (wantDetail) detail.push('拼音:' + t + '(+' + round3(0.4 * toks[t]) + ')'); }
  }
  // 查询为拼音（拉丁 token）时，匹配条目侧 py:/pyi: token（去前缀）
  for (const tt of qtoks) {
    if (/^[a-z]+$/.test(tt)) {
      if (toks['py:' + tt]) { score += 0.4 * toks['py:' + tt]; if (wantDetail) detail.push('拼音:' + tt + '(+' + round3(0.4 * toks['py:' + tt]) + ')'); }
      if (toks['pyi:' + tt]) { score += 0.4 * toks['pyi:' + tt]; if (wantDetail) detail.push('拼音首字母:' + tt + '(+' + round3(0.4 * toks['pyi:' + tt]) + ')'); }
      // 首字母串（如 yyyd）拆 bigram 匹配 pyi: token
      if (tt.length >= 3) {
        for (let i = 0; i < tt.length - 1; i++) {
          const bg = tt.slice(i, i + 2);
          if (toks['pyi:' + bg]) { score += 0.4 * toks['pyi:' + bg]; if (wantDetail) detail.push('拼音首字母:' + bg + '(+' + round3(0.4 * toks['pyi:' + bg]) + ')'); }
        }
      }
    }
  }
  if (score === 0 && hay.indexOf(q) !== -1) { score = 1; if (wantDetail) detail.push('子串命中'); }
  if (score === 0) {
    const longQtoks = qtoks.filter(function (t) { return t.length >= 4; });
    const keys = Object.keys(toks).filter(function (k) { return k.length >= 4 && k.indexOf(':') === -1; });
    outer:
    for (const t of longQtoks) {
      for (const k of keys) {
        if (Math.abs(k.length - t.length) <= 2 && editDistance(k, t) <= 2) {
          score += 0.3 * toks[k];
          if (wantDetail) detail.push('模糊:' + t + '~' + k + '(+' + round3(0.3 * toks[k]) + ')');
          break outer;
        }
      }
    }
  }
  return { score: score, detail: detail };
}
function round3(n) { return Math.round(n * 1000) / 1000; }
// ---- v0.8.0 自我进化：统一效用分（盖棺分）----
function feedbackNetOf(meta) { return parseInt(meta.feedback_net || '0', 10) || 0; }
// ---- v0.18.0 A3：命中打点（本地元数据；查询只存 8 位指纹，不落原文）----
// hit_days 形如 s2026-09-26:2|g2026-09-25:1|u2026-09-24:1（s=search / g=get / u=use）。
// hit_queries 形如 q3f9a1c7:2|q77bd021e:1（sha256(query) 前 8 位十六进制 + 次数）。
const USAGE_SIGNAL_LABELS = { search: 's', get: 'g', use: 'u' };
const USAGE_SIGNAL_ORDER = { s: 0, g: 1, u: 2 };
const USAGE_CONFIG_DEFAULTS = { usage_retention_days: 90, usage_query_slots: 12 };
function usageNumber(cfg, key) {
  const raw = cfg ? cfg[key] : undefined;
  if (raw === undefined || raw === null || raw === '') return USAGE_CONFIG_DEFAULTS[key];
  const n = parseFloat(raw);
  return (n >= 0) ? n : USAGE_CONFIG_DEFAULTS[key];
}
function usageSettings(opts) {
  const cfg = loadConfig();
  return {
    enabled: !(opts && opts.noUsage) && cfg.usage_enabled !== false,
    retentionDays: usageNumber(cfg, 'usage_retention_days'),
    querySlots: usageNumber(cfg, 'usage_query_slots'),
  };
}
function usageFingerprint(query) {
  return crypto.createHash('sha256').update(String(query), 'utf8').digest('hex').slice(0, 8);
}
function parseHitDays(value) {
  const map = {};
  const re = /([sgu])(\d{4}-\d{2}-\d{2}):(\d+)/g;
  let m;
  while ((m = re.exec(String(value || '')))) {
    const key = m[1] + m[2];
    map[key] = (map[key] || 0) + (parseInt(m[3], 10) || 0);
  }
  return map;
}
function serializeHitDays(map) {
  const keys = Object.keys(map).filter(function (k) { return /^[sgu]\d{4}-\d{2}-\d{2}$/.test(k) && map[k] > 0; });
  keys.sort(function (a, b) {
    const da = a.slice(1), db = b.slice(1);
    if (da !== db) return db.localeCompare(da);
    return (USAGE_SIGNAL_ORDER[a[0]] || 0) - (USAGE_SIGNAL_ORDER[b[0]] || 0);
  });
  return keys.map(function (k) { return k + ':' + map[k]; }).join('|');
}
function parseHitQueries(value) {
  const map = {};
  const re = /q([0-9a-f]{8}):(\d+)/g;
  let m;
  while ((m = re.exec(String(value || '')))) {
    map[m[1]] = (map[m[1]] || 0) + (parseInt(m[2], 10) || 0);
  }
  return map;
}
function serializeHitQueries(map, slots) {
  const fps = Object.keys(map).filter(function (fp) { return /^[0-9a-f]{8}$/.test(fp) && map[fp] > 0; });
  fps.sort(function (a, b) {
    if (map[b] !== map[a]) return map[b] - map[a];
    return a.localeCompare(b);
  });
  const limit = (slots >= 0) ? slots : USAGE_CONFIG_DEFAULTS.usage_query_slots;
  return fps.slice(0, limit).map(function (fp) { return 'q' + fp + ':' + map[fp]; }).join('|');
}
// 纯函数：算好本次命中要写入的 frontmatter 字段（不写盘，便于 recall/feedback 复用同一口径）。
function usagePatchForMeta(meta, signal, query, settings, dateStr) {
  const label = USAGE_SIGNAL_LABELS[signal];
  if (!label) return {};
  const patch = {};
  const days = parseHitDays(meta.hit_days);
  const key = label + dateStr;
  days[key] = (days[key] || 0) + 1;
  const kept = {};
  for (const k of Object.keys(days)) {
    const age = daysBetween(k.slice(1), dateStr);
    if (age < 0 || age > settings.retentionDays) continue;
    kept[k] = days[k];
  }
  const daysStr = serializeHitDays(kept);
  if (daysStr) patch.hit_days = daysStr;
  if (signal === 'search' && query) {
    const queries = parseHitQueries(meta.hit_queries);
    const fp = usageFingerprint(query);
    queries[fp] = (queries[fp] || 0) + 1;
    patch.hit_queries = serializeHitQueries(queries, settings.querySlots);
  }
  return patch;
}
// 独立写点（explain / context use 信号）：写失败只计数，不影响读取结果。
// v0.22.8：命中打点是观察性元数据，写回后恢复文件原时间戳——避免管理台按 mtime 排序时旧条目被“搜到→顶到最新”。
function statFileTimes(fp) {
  // BigInt 统计拿纳秒字段：毫秒精度的 Date 会把亚毫秒部分抹平（WorkBuddy 验收 D1）。
  try { return fs.statSync(fp, { bigint: true }); } catch (e) { return null; }
}
function restoreFileTimes(fp, st) {
  if (!st) return;
  try {
    // 毫秒对齐值用 Date 逐 tick 精确还原；带亚毫秒余数的值用纳秒转 float 秒——
    // 误差为 Node 公开 API 上限（亚微秒级；utimesSync 不接受 BigInt 直传）。
    const toTime = function (ns) {
      return (ns % 1000000n === 0n) ? new Date(Number(ns / 1000000n)) : Number(ns) / 1e9;
    };
    fs.utimesSync(fp, toTime(st.atimeNs), toTime(st.mtimeNs));
  } catch (e) { /* 恢复失败不影响打点写入 */ }
}
function applyUsageHits(root, relFiles, signal, query, opts) {
  opts = opts || {};
  const out = { enabled: false, written: 0, skipped: 0, failed: 0 };
  const settings = usageSettings(opts);
  out.enabled = settings.enabled;
  if (!settings.enabled) return out;
  const selfAgent = (opts.selfAgent !== undefined) ? opts.selfAgent : resolveIdentity(opts).id;
  const dateStr = today();
  for (const rel of relFiles) {
    const fp = path.join(root, rel);
    if (!fs.existsSync(fp)) continue;
    const owner = ownerFromPrivatePath(root, fp);
    if (owner && owner !== selfAgent) { out.skipped++; continue; }
    try {
      const parsed = parseFrontmatter(readMemoryText(root, fp, owner));
      if (parsed.meta.immutable === 'true') { out.skipped++; continue; }
      const patch = usagePatchForMeta(parsed.meta, signal, query, settings, dateStr);
      if (!Object.keys(patch).length) continue;
      const meta = Object.assign({}, parsed.meta, patch);
      const prevStat = statFileTimes(fp);
      writeMemoryText(root, fp, frontmatterToText(meta, parsed.body), owner);
      restoreFileTimes(fp, prevStat);
      upsertIndexEntry(root, readEntry(fp, root));
      out.written++;
    } catch (e) {
      out.failed++;
    }
  }
  return out;
}
// 报告侧派生：窗口内命中次数（不落盘，避免派生值与原始值漂移）。
function usageTotals(entry, days) {
  const map = parseHitDays(entry && entry.hit_days);
  let total = 0;
  for (const k of Object.keys(map)) {
    const age = daysBetween(k.slice(1), today());
    if (age >= 0 && age <= days) total += map[k];
  }
  return total;
}
function utilityScore(meta) {
  const conf = Math.min(Math.max(parseFloat(meta.confidence || 1.0) || 1.0, 0), 1);
  const acc = parseInt(meta.access_count || '0', 10) || 0;
  const fb = feedbackNetOf(meta);
  const usageScore = 0.5 * (Math.min(acc, 20) / 20) + 0.5 * (fb / (1 + Math.abs(fb)));
  const last = meta.last_accessed || meta.created || '';
  const recencyScore = decayRecency(String(meta.type || 'FACT').toUpperCase(), last ? daysBetween(last, today()) : 0, decayConfig());
  const typeScore = ({ BOUND: 1.0, COMMIT: 0.9, PREF: 0.8, FACT: 0.6 })[String(meta.type || 'FACT').toUpperCase()] || 0.6;
  let structureScore = 0;
  if (meta.source) structureScore += 0.2;
  const tags = parseTags(meta.tags);
  if (tags.length) structureScore += 0.3;
  if (meta.subject) structureScore += 0.2;
  if (meta.confidence !== undefined && meta.confidence !== null && meta.confidence !== '') structureScore += 0.1;
  structureScore = Math.min(structureScore, 1.0);
  const w = parseFloat(meta.weight || '1.0');
  const weight = (w > 0 ? w : 1.0);
  return ((0.30 * conf) + (0.25 * usageScore) + (0.20 * recencyScore) + (0.15 * typeScore) + (0.10 * structureScore)) * weight;
}
// utility 分项明细（explain / 审计用）
function utilityBreakdown(meta) {
  const conf = Math.min(Math.max(parseFloat(meta.confidence || 1.0) || 1.0, 0), 1);
  const acc = parseInt(meta.access_count || '0', 10) || 0;
  const fb = feedbackNetOf(meta);
  const usageScore = 0.5 * (Math.min(acc, 20) / 20) + 0.5 * (fb / (1 + Math.abs(fb)));
  const last = meta.last_accessed || meta.created || '';
  const recencyScore = decayRecency(String(meta.type || 'FACT').toUpperCase(), last ? daysBetween(last, today()) : 0, decayConfig());
  const typeScore = ({ BOUND: 1.0, COMMIT: 0.9, PREF: 0.8, FACT: 0.6 })[String(meta.type || 'FACT').toUpperCase()] || 0.6;
  let structureScore = 0;
  if (meta.source) structureScore += 0.2;
  const tags = parseTags(meta.tags);
  if (tags.length) structureScore += 0.3;
  if (meta.subject) structureScore += 0.2;
  if (meta.confidence !== undefined && meta.confidence !== null && meta.confidence !== '') structureScore += 0.1;
  structureScore = Math.min(structureScore, 1.0);
  const w = parseFloat(meta.weight || '1.0');
  const weight = (w > 0 ? w : 1.0);
  return {
    confidence: round3(0.30 * conf), usage: round3(0.25 * usageScore), recency: round3(0.20 * recencyScore),
    type: round3(0.15 * typeScore), structure: round3(0.10 * structureScore), weight: round3(weight),
    total: round3(((0.30 * conf) + (0.25 * usageScore) + (0.20 * recencyScore) + (0.15 * typeScore) + (0.10 * structureScore)) * weight)
  };
}
function frontmatterToText(meta, body) {
  const lines = ['---'];
  const ordered = FIELD_ORDER.filter(function (k) { return meta[k] !== undefined && meta[k] !== null && meta[k] !== ''; });
  const extra = Object.keys(meta).filter(function (k) { return FIELD_ORDER.indexOf(k) === -1 && meta[k] !== undefined && meta[k] !== null && meta[k] !== ''; });
  for (const k of ordered.concat(extra)) {
    const v = meta[k];
    if (Array.isArray(v)) lines.push(k + ': ' + JSON.stringify(v));
    else if (typeof v === 'number') lines.push(k + ': ' + v);
    else lines.push(k + ': ' + escapeYaml(v));
  }
  lines.push('---', '');
  const b = body === undefined || body === null ? '' : body;
  return lines.join('\n') + String(b).replace(/^\n+/, '') + '\n';
}
function ensureInit(root) {
  fs.mkdirSync(path.join(root, PUBLIC_DIR), { recursive: true });
  fs.mkdirSync(path.join(root, PRIVATE_DIR), { recursive: true });
  fs.mkdirSync(path.join(root, ARCHIVE_DIR), { recursive: true });
  const readme = path.join(root, 'README.md');
  if (!fs.existsSync(readme)) {
    fs.writeFileSync(readme, '# yotta-memory（元忆）记忆库\n\n有权限边界的文件式智能体记忆存储目录。结构：facts/<年>/<月>/（公共 FACT） private/<agent_id>/{prefs,bounds,commits}/<年>/<月>/（各智能体私密，物理隔离） .archive/（归档）。v0.16 及更早的平铺文件（facts/*.md、private/<agent_id>/<type>/*.md）继续可读，不做自动迁移。\n', 'utf8');
  }
}
// 递归收集目录下（含年/月子目录）的记忆文件路径，跳过 distills/profile.md 等非记忆文件。
function walkEntryFiles(dir, out) {
  let names;
  try { names = fs.readdirSync(dir, { withFileTypes: true }); } catch (e) { return; }
  for (const entry of names) {
    const fp = path.join(dir, entry.name);
    if (entry.isDirectory()) { walkEntryFiles(fp, out); continue; }
    if (!entry.isFile()) continue;
    if (!MEMORY_FILE_RE.test(entry.name)) continue;
    out.push(fp);
  }
}
// 序号在「类型目录 + owner」范围内唯一，跨越旧平铺与新年/月分层，避免同名覆盖。
function maxSeqInTree(dir) {
  let max = 0;
  const files = [];
  if (fs.existsSync(dir)) walkEntryFiles(dir, files);
  for (const fp of files) {
    const f = path.basename(fp);
    const m = f.match(/^\d{4}-\d{2}-\d{2}-(\d{4})\.md(\.enc)?$/);
    if (m) max = Math.max(max, parseInt(m[1], 10));
  }
  return String(max + 1).padStart(4, '0');
}
function nextSeq(dir) { return maxSeqInTree(dir); }
// 分层写入时序号要跨该类型全部分层计算（否则同一年不同月份会重复 0001）。
function nextSeqFor(typeDir, writeDir) {
  return maxSeqInTree(typeDir || writeDir);
}
// 去重只看「最近写入窗口」：当前年/月子目录 + 平铺根，避免大库每次写入都全量扫一遍。
function recentlyWrittenFiles(typeDir, writeDir) {
  const out = [];
  if (path.resolve(typeDir) === path.resolve(writeDir)) {
    if (fs.existsSync(typeDir)) walkEntryFiles(typeDir, out);
    return out;
  }
  if (fs.existsSync(writeDir)) walkEntryFiles(writeDir, out);
  const yearDir = path.dirname(writeDir);
  const seen = new Set(out);
  if (fs.existsSync(yearDir)) {
    walkEntryFiles(yearDir, out);
  }
  if (fs.existsSync(typeDir)) {
    for (const f of fs.readdirSync(typeDir)) {
      const full = path.join(typeDir, f);
      if (fs.statSync(full).isFile() && MEMORY_FILE_RE.test(f) && !seen.has(full)) out.push(full);
    }
  }
  return out;
}


// ================= v0.7.0 加密（AES-256-GCM 信封加密 + PBKDF2 主密钥 + 恢复钥匙）=================
const ENC_MAGIC = 'YTMENC1';
const IDX_MAGIC = 'YTMIDX1';
const KEY_MAGIC = 'YTMKEY1';
const AGENT_MAGIC = 'YTMAGENT1';
const KEYS_DIR = 'keys';
const KEY_CACHE_DIR = 'cache';
const AGENT_BINDINGS_DIR = 'bindings';
const AGENT_PENDING_DIR = 'pending';
const AGENT_KEY_FILENAME = '.yotta-memory-agent-key';
const ENC_INDEX_FILE = 'index.enc';
const ENC_SUFFIX = '.enc';
const PBKDF2_ITER = 600000;
const GCM_NONCE = 12;
const GCM_TAG = 16;
const AES_ALGO = 'aes-256-gcm';

function encKeysDir(root) { return path.join(root, KEYS_DIR); }
function encSaltPath(root) { return path.join(encKeysDir(root), 'salt'); }
function encOwnerKeyPath(root, id) { return path.join(encKeysDir(root), id + '.key.enc'); }
function encOwnerRecPath(root, id) { return path.join(encKeysDir(root), id + '.key.recovery'); }
function encRecoveryEncPath(root) { return path.join(encKeysDir(root), 'recovery.key.enc'); }
function encCacheDir(root) { return path.join(encKeysDir(root), KEY_CACHE_DIR); }
function encCachePath(root, id) { return path.join(encCacheDir(root), id + '.key'); }
function encBindingsDir(root) { return path.join(encKeysDir(root), AGENT_BINDINGS_DIR); }
function encAgentBindingPath(root, id) { return path.join(encBindingsDir(root), id + '.key.agent'); }
function encPendingDir(root) { return path.join(encKeysDir(root), AGENT_PENDING_DIR); }
function encPendingPath(root, id) { return path.join(encPendingDir(root), id + '.key'); }
function agentKeyFilePath(agentHome) { return path.join(path.resolve(agentHome), AGENT_KEY_FILENAME); }
function detectAgentHost(owner) {
  const hint = String(process.env.YOTTA_MEMORY_AGENT_HOST || '').trim().toLowerCase();
  if (hint === 'codex' || hint === 'opencode') return hint;
  const id = String(owner || '').toLowerCase();
  if (/(^|[-_.])opencode([-_.]|$)/.test(id)) return 'opencode';
  if (id === 'codex' || id.indexOf('codex-') === 0) return 'codex';
  if (process.env.OPENCODE_API_KEY || process.env.OPENCODE_CONFIG) return 'opencode';
  if (process.env.CODEX_HOME) return 'codex';
  return 'generic';
}
function resolveAgentKeyLocation(owner, opts) {
  opts = opts || {};
  const explicitHome = String(opts.to || '').trim();
  const explicitFile = String(opts.agentKeyFile || '').trim();
  const explicitPluginData = String(opts.pluginData || '').trim();
  if (explicitHome && explicitFile) {
    return { ok: false, error: '--to 与 --agent-key-file 不能同时使用。' };
  }
  if (explicitPluginData && (explicitHome || explicitFile)) {
    return { ok: false, error: '--plugin-data 不能与 --to / --agent-key-file 同时使用。' };
  }
  if (explicitPluginData) {
    return { ok: true, file: agentKeyFilePath(explicitPluginData), source: 'option:--plugin-data' };
  }
  if (explicitFile) {
    return { ok: true, file: path.resolve(explicitFile), source: 'option:--agent-key-file' };
  }
  if (explicitHome) {
    return { ok: true, file: agentKeyFilePath(explicitHome), source: 'option:--to' };
  }
  const envFile = String(process.env.YOTTA_MEMORY_AGENT_KEY_FILE || '').trim();
  if (envFile) {
    return { ok: true, file: path.resolve(envFile), source: 'env:YOTTA_MEMORY_AGENT_KEY_FILE' };
  }
  const envHome = String(process.env.YOTTA_MEMORY_AGENT_HOME || '').trim();
  if (envHome) {
    return { ok: true, file: agentKeyFilePath(envHome), source: 'env:YOTTA_MEMORY_AGENT_HOME' };
  }
  const host = detectAgentHost(owner);
  if (host === 'codex') {
    const home = process.env.CODEX_HOME ? path.resolve(process.env.CODEX_HOME) : path.join(os.homedir(), '.codex');
    return { ok: true, file: agentKeyFilePath(home), source: 'host:codex' };
  }
  if (host === 'opencode') {
    const base = process.env.XDG_CONFIG_HOME ? path.resolve(process.env.XDG_CONFIG_HOME) : path.join(os.homedir(), '.config');
    return { ok: true, file: agentKeyFilePath(path.join(base, 'opencode')), source: 'host:opencode' };
  }
  return { ok: true, file: agentKeyFilePath(path.join(os.homedir(), '.' + owner)), source: 'host:generic' };
}
function isEncrypted(root) { return fs.existsSync(encKeysDir(root)); }
function isEncFile(fp) { return String(fp).slice(-ENC_SUFFIX.length) === ENC_SUFFIX; }
function ownerFromPrivatePath(root, fp) {
  const rel = path.relative(root, fp).replace(/\\/g, '/');
  const seg = rel.split('/');
  if (seg[0] === PRIVATE_DIR && seg[1]) return seg[1];
  return '';
}
function collectOwners(root) {
  const pdir = path.join(root, PRIVATE_DIR);
  if (!fs.existsSync(pdir)) return [];
  return fs.readdirSync(pdir).filter(function (id) {
    try { return fs.statSync(path.join(pdir, id)).isDirectory(); } catch (e) { return false; }
  });
}
function ensureKeysDir(root) { fs.mkdirSync(encCacheDir(root), { recursive: true }); }
// owner 来源联合：private/<owner>/ 目录 + keys/*.key.enc（只授权未写记忆时 owner 只在 keys/）
function keyOwners(root) {
  const set = new Set();
  for (const o of collectOwners(root)) set.add(o);
  const kd = encKeysDir(root);
  if (fs.existsSync(kd)) {
    for (const f of fs.readdirSync(kd)) {
      if (f === 'recovery.key.enc') continue;
      const m = /^(.+)\.key\.enc$/.exec(f);
      if (m) set.add(m[1]);
    }
  }
  return Array.from(set);
}
function aesEncryptBytes(key, buf, aad) {
  const nonce = crypto.randomBytes(GCM_NONCE);
  const c = crypto.createCipheriv(AES_ALGO, key, nonce);
  if (aad) c.setAAD(aad);
  const ct = Buffer.concat([c.update(buf), c.final()]);
  return Buffer.concat([nonce, c.getAuthTag(), ct]);
}
function aesDecryptBytes(key, env, aad) {
  if (!env || env.length < GCM_NONCE + GCM_TAG) throw new Error('密文数据损坏');
  const nonce = env.slice(0, GCM_NONCE);
  const tag = env.slice(GCM_NONCE, GCM_NONCE + GCM_TAG);
  const ct = env.slice(GCM_NONCE + GCM_TAG);
  const d = crypto.createDecipheriv(AES_ALGO, key, nonce);
  if (aad) d.setAAD(aad);
  d.setAuthTag(tag);
  return Buffer.concat([d.update(ct), d.final()]);
}
function deriveUmk(password, salt) {
  return crypto.pbkdf2Sync(Buffer.from(String(password), 'utf8'), salt, PBKDF2_ITER, 32, 'sha256');
}
function loadSalt(root) {
  const p = encSaltPath(root);
  if (!fs.existsSync(p)) return null;
  return fs.readFileSync(p);
}
function initEncryptionCore(root, password, recoveryKeyIn) {
  ensureKeysDir(root);
  const salt = crypto.randomBytes(16);
  fs.writeFileSync(encSaltPath(root), salt);
  const umk = deriveUmk(password, salt);
  const rk = recoveryKeyIn ? Buffer.from(String(recoveryKeyIn), 'base64') : crypto.randomBytes(32);
  if (rk.length !== 32) throw new Error('恢复钥匙须为 32 字节（base64）');
  fs.writeFileSync(encRecoveryEncPath(root), Buffer.concat([Buffer.from(KEY_MAGIC, 'utf8'), aesEncryptBytes(umk, rk, Buffer.from('recovery', 'utf8'))]));
  return { umk: umk, rk: rk, salt: salt };
}
function unwrapRecoveryEnc(root, umk) {
  const p = encRecoveryEncPath(root);
  if (!fs.existsSync(p)) return null;
  const buf = fs.readFileSync(p);
  if (buf.slice(0, KEY_MAGIC.length).toString('utf8') !== KEY_MAGIC) throw new Error('恢复钥匙文件格式错误');
  return aesDecryptBytes(umk, buf.slice(KEY_MAGIC.length), Buffer.from('recovery', 'utf8'));
}
function wrapOwnerKey(root, umk, rk, owner) {
  const ownerKey = crypto.randomBytes(32);
  const aad = Buffer.from('owner:' + owner, 'utf8');
  fs.writeFileSync(encOwnerKeyPath(root, owner), Buffer.concat([Buffer.from(KEY_MAGIC, 'utf8'), aesEncryptBytes(umk, ownerKey, aad)]));
  fs.writeFileSync(encOwnerRecPath(root, owner), Buffer.concat([Buffer.from(KEY_MAGIC, 'utf8'), aesEncryptBytes(rk, ownerKey, aad)]));
  return ownerKey;
}
function unwrapOwnerKey(root, owner, umk) {
  const p = encOwnerKeyPath(root, owner);
  if (!fs.existsSync(p)) return null;
  const buf = fs.readFileSync(p);
  if (buf.slice(0, KEY_MAGIC.length).toString('utf8') !== KEY_MAGIC) throw new Error('密钥文件格式错误: ' + p);
  return aesDecryptBytes(umk, buf.slice(KEY_MAGIC.length), Buffer.from('owner:' + owner, 'utf8'));
}
function unwrapOwnerKeyRecovery(root, owner, rk) {
  const p = encOwnerRecPath(root, owner);
  if (!fs.existsSync(p)) return null;
  const buf = fs.readFileSync(p);
  if (buf.slice(0, KEY_MAGIC.length).toString('utf8') !== KEY_MAGIC) throw new Error('恢复密钥文件格式错误: ' + p);
  return aesDecryptBytes(rk, buf.slice(KEY_MAGIC.length), Buffer.from('owner:' + owner, 'utf8'));
}
function recoverOwnerKeyFromRecovery(root, owner, umk, rk) {
  if (!isSafeAgentId(owner) || !Buffer.isBuffer(rk)) return null;
  try {
    const ownerKey = unwrapOwnerKeyRecovery(root, owner, rk);
    if (!ownerKey) return null;
    fs.writeFileSync(encOwnerKeyPath(root, owner), Buffer.concat([
      Buffer.from(KEY_MAGIC, 'utf8'),
      aesEncryptBytes(umk, ownerKey, Buffer.from('owner:' + owner, 'utf8')),
    ]));
    return ownerKey;
  } catch (e) {
    return null;
  }
}
function privateOwnerHasData(root, owner) {
  if (!isSafeAgentId(owner)) return false;
  const dir = path.join(root, PRIVATE_DIR, owner);
  if (!fs.existsSync(dir)) return false;
  const stack = [dir];
  while (stack.length) {
    const current = stack.pop();
    let entries = [];
    try { entries = fs.readdirSync(current, { withFileTypes: true }); } catch (e) { continue; }
    for (const entry of entries) {
      if (entry.isDirectory()) {
        stack.push(path.join(current, entry.name));
      } else if (entry.isFile() && entry.name !== ENC_INDEX_FILE) {
        return true;
      }
    }
  }
  return false;
}
function revokeOwnerKeyCache(root, owner) {
  const p = encCachePath(root, owner);
  if (fs.existsSync(p)) { fs.unlinkSync(p); return true; }
  return false;
}
function writeAgentBinding(root, owner, ownerKey, agentKey) {
  if (!isSafeAgentId(owner)) throw new Error('非法 agent ID');
  if (!Buffer.isBuffer(agentKey) || agentKey.length !== 32) throw new Error('agent_key 必须是 32 字节');
  fs.mkdirSync(encBindingsDir(root), { recursive: true });
  const aad = Buffer.from('agent:' + owner, 'utf8');
  const env = aesEncryptBytes(agentKey, ownerKey, aad);
  fs.writeFileSync(encAgentBindingPath(root, owner), Buffer.concat([Buffer.from(AGENT_MAGIC, 'utf8'), env]));
  try { fs.chmodSync(encAgentBindingPath(root, owner), 0o600); } catch (e) {}
}
function writePendingAgentKey(root, owner, agentKey) {
  if (!isSafeAgentId(owner)) throw new Error('非法 agent ID');
  if (!Buffer.isBuffer(agentKey) || agentKey.length !== 32) throw new Error('agent_key 必须是 32 字节');
  fs.mkdirSync(encPendingDir(root), { recursive: true });
  const fp = encPendingPath(root, owner);
  fs.writeFileSync(fp, agentKey.toString('base64') + '\n', { encoding: 'utf8', mode: 0o600 });
  try { fs.chmodSync(fp, 0o600); } catch (e) {}
  return fp;
}
function writeAgentBindingWithPending(root, owner, ownerKey, agentKey) {
  writeAgentBinding(root, owner, ownerKey, agentKey);
  try {
    return writePendingAgentKey(root, owner, agentKey);
  } catch (e) {
    try { fs.unlinkSync(encAgentBindingPath(root, owner)); } catch (ignore) {}
    try { fs.unlinkSync(encPendingPath(root, owner)); } catch (ignore) {}
    throw e;
  }
}
function removePendingAgentKey(root, owner) {
  if (!isSafeAgentId(owner)) return false;
  const fp = encPendingPath(root, owner);
  if (!fs.existsSync(fp)) return false;
  fs.unlinkSync(fp);
  return true;
}
function readPendingAgentKey(root, owner) {
  if (!isSafeAgentId(owner)) return null;
  const fp = encPendingPath(root, owner);
  if (!fs.existsSync(fp)) return null;
  const raw = fs.readFileSync(fp, 'utf8').trim();
  if (!raw) throw new Error('pending agent_key 文件为空');
  const key = Buffer.from(raw, 'base64');
  if (key.length !== 32) throw new Error('pending agent_key 格式错误');
  return key;
}
function readAgentKeyFile(fp) {
  const raw = fs.readFileSync(path.resolve(String(fp)), 'utf8').trim();
  if (!raw) throw new Error('agent-key 文件为空');
  const key = Buffer.from(raw, 'base64');
  if (key.length !== 32) throw new Error('agent-key 文件格式错误');
  return key;
}
function unwrapAgentBinding(root, owner, agentKey) {
  if (!isSafeAgentId(owner)) return null;
  if (!Buffer.isBuffer(agentKey) || agentKey.length !== 32) return null;
  const p = encAgentBindingPath(root, owner);
  if (!fs.existsSync(p)) return null;
  const buf = fs.readFileSync(p);
  if (buf.slice(0, AGENT_MAGIC.length).toString('utf8') !== AGENT_MAGIC) throw new Error('agent binding 文件格式错误: ' + p);
  return aesDecryptBytes(agentKey, buf.slice(AGENT_MAGIC.length), Buffer.from('agent:' + owner, 'utf8'));
}
function getOwnerKeyFor(root, owner, identity) {
  if (!owner) return null;
  const viewKeys = VIEW_KEYS_CONTEXT.getStore();
  if (viewKeys && viewKeys.keys && viewKeys.keys[owner]) return viewKeys.keys[owner];
  if (!isEncrypted(root)) return null;
  const current = identity || currentRuntimeIdentity();
  if (!current.id || current.id !== owner || !current.agentKey) return null;
  const agentKey = Buffer.from(current.agentKey, 'base64');
  return unwrapAgentBinding(root, owner, agentKey);
}
function validatePrivateIdentity(root, ident, owner) {
  if (!ident || !ident.id) return '私密操作必须先声明显式身份。';
  if (!isSafeAgentId(owner || ident.id)) return '非法 owner ID：只允许单段名称，禁止 /、\\、.. 和控制字符。';
  if (!isEncrypted(root)) return '';
  const current = currentRuntimeIdentity();
  const agentKey = ident.agentKey || (current.id === ident.id ? current.agentKey : '');
  if (!agentKey) {
    if (ident.source === 'missing-key-file') {
      return '未找到 agent-key 文件: ' + ident.keyFile + '；当前为未授权模式（公共 FACT 可读）。该私密操作需要先由用户执行 yotta-memory view 授权或 yotta-memory key bind ' + (owner || ident.id) + '，再由 AI 执行 yotta-memory key status ' + (owner || ident.id) + ' → key claim ' + (owner || ident.id) + '。';
    }
    return '记忆库已加密，但缺少 agent_key。CLI 请使用 --agent-key <key> 或 --agent-key-file <path>；stdio MCP 请使用 --agent-id <id> + --agent-key-file <path>；HTTP MCP 请发送 X-Agent-Key 请求头。若该 agent 尚未绑定，请执行 yotta-memory key bind ' + (owner || ident.id) + '。';
  }
  const context = IDENTITY_CONTEXT.getStore();
  if (context) {
    context.id = ident.id;
    context.agentKey = agentKey;
  } else {
    setRuntimeAgent(ident.id, agentKey);
  }
  try {
    if (!getOwnerKeyFor(root, owner || ident.id, { id: ident.id, agentKey: agentKey })) {
      return 'agent_key 校验失败：未找到 ' + (owner || ident.id) + ' 的 agent binding（可能已吊销）。请由用户重新授权，或由用户执行 yotta-memory key bind ' + (owner || ident.id) + '。';
    }
  } catch (e) {
    return 'agent_key 无效或 binding 损坏：' + e.message;
  }
  return '';
}
function legacyCacheOwners(root) {
  if (!isEncrypted(root)) return [];
  const dir = encCacheDir(root);
  if (!fs.existsSync(dir)) return [];
  const found = [];
  let names = [];
  try { names = fs.readdirSync(dir); } catch (e) { return found; }
  for (const f of names) {
    if (!/\.key$/.test(f)) continue;
    const owner = f.slice(0, -4);
    if (!isSafeAgentId(owner)) continue;
    if (found.indexOf(owner) === -1) found.push(owner);
  }
  return found;
}
function migrationRequiredInfo(root) {
  if (!isEncrypted(root)) return null;
  const owners = new Set();
  for (const owner of collectOwners(root)) owners.add(owner);
  for (const owner of legacyCacheOwners(root)) owners.add(owner);
  const actionable = [];
  const legacyOnly = [];
  for (const owner of owners) {
    const hasPrivate = fs.existsSync(path.join(root, PRIVATE_DIR, owner)) || fs.existsSync(path.join(root, PRIVATE_DIR, owner, PROFILE_FILE)) || fs.existsSync(path.join(root, PRIVATE_DIR, owner, PROFILE_FILE + ENC_SUFFIX));
    const hasLegacy = fs.existsSync(encCachePath(root, owner));
    const bound = fs.existsSync(encAgentBindingPath(root, owner));
    if (!hasPrivate) {
      if (hasLegacy) legacyOnly.push(owner);
      continue;
    }
    if (!bound) actionable.push(owner);
  }
  if (!actionable.length) return null;
  const reasons = [];
  if (actionable.some(function (owner) { return fs.existsSync(encCachePath(root, owner)); })) reasons.push('legacy_cache');
  reasons.push('no_agent_binding');
  const entries = actionable.map(function (owner) {
    const ownerReasons = [];
    if (fs.existsSync(encCachePath(root, owner))) ownerReasons.push('legacy_cache');
    ownerReasons.push('no_agent_binding');
    return { agent: owner, reason: ownerReasons.join(',') };
  });
  return {
    marker: '[YTM_MIGRATION_REQUIRED] agent=' + actionable.join(',') + ' reason=' + reasons.join(','),
    owners: actionable,
    reasons: reasons,
    entries: entries,
    legacyOnly: legacyOnly,
  };
}
function migrationReminderText(root) {
  const info = migrationRequiredInfo(root);
  if (!info) return '';
  let text = info.marker + '\nAI 提醒（升级后首次调用元忆 / 重启会话时请主动转达）：旧版授权缓存不再加载，需要重新授权。请让用户自己执行 `yotta-memory view` → 浏览器打开平台 → 输入主口令 → 点「授权」并保存只展示一次的 `agent_key`；这是用户侧操作，AI 不得代替用户执行 `migrate` / `key bind` 迁移，只负责提醒和讲解步骤。';
  if (info.legacyOnly && info.legacyOnly.length) {
    text += '\n另有 legacy 明文 cache 缺少可迁移私密数据（不属于迁移清单）: ' + info.legacyOnly.join(', ') + '；如需清理请单独确认。';
  }
  return text;
}
function encryptMemoryText(text, ownerKey) {
  const fileKey = crypto.randomBytes(32);
  const wk = aesEncryptBytes(ownerKey, fileKey, Buffer.from('filekey', 'utf8'));
  const data = aesEncryptBytes(fileKey, Buffer.from(text, 'utf8'), Buffer.from('file', 'utf8'));
  return Buffer.concat([Buffer.from(ENC_MAGIC, 'utf8'), wk, data]);
}
function decryptMemoryText(buf, ownerKey) {
  if (buf.slice(0, ENC_MAGIC.length).toString('utf8') !== ENC_MAGIC) throw new Error('非密文文件（缺 ' + ENC_MAGIC + ' 头）');
  const env = buf.slice(ENC_MAGIC.length);
  const wkEnv = env.slice(0, GCM_NONCE + GCM_TAG + 32);
  const fileKey = aesDecryptBytes(ownerKey, wkEnv, Buffer.from('filekey', 'utf8'));
  const dataEnv = env.slice(GCM_NONCE + GCM_TAG + 32);
  return aesDecryptBytes(fileKey, dataEnv, Buffer.from('file', 'utf8')).toString('utf8');
}
function readMemoryText(root, fp, owner) {
  if (!isEncFile(fp)) return fs.readFileSync(fp, 'utf8');
  const key = getOwnerKeyFor(root, owner);
  if (!key) throw new Error('私密区已加密：当前无 ' + owner + ' 的授权密钥，请在用户平台授权（yotta-memory view → 授权本智能体）。');
  return decryptMemoryText(fs.readFileSync(fp), key);
}
function writeMemoryText(root, fp, text, owner, opts) {
  const flag = (opts && opts.exclusive) ? 'wx' : 'w';
  if (!isEncFile(fp)) { fs.writeFileSync(fp, text, { encoding: 'utf8', flag: flag }); return; }
  const key = getOwnerKeyFor(root, owner);
  if (!key) throw new Error('私密区已加密：当前无 ' + owner + ' 的授权密钥，请在用户平台授权（yotta-memory view → 授权本智能体）。');
  fs.writeFileSync(fp, encryptMemoryText(text, key), { flag: flag });
}
function ownerIndexPath(root, owner) { return path.join(root, PRIVATE_DIR, owner, ENC_INDEX_FILE); }
function loadOwnerIndex(root, owner, ownerKey) {
  const p = ownerIndexPath(root, owner);
  if (!fs.existsSync(p)) return [];
  const buf = fs.readFileSync(p);
  if (buf.slice(0, IDX_MAGIC.length).toString('utf8') !== IDX_MAGIC) return [];
  const d = aesDecryptBytes(ownerKey, buf.slice(IDX_MAGIC.length), Buffer.from('index:' + owner, 'utf8'));
  const j = JSON.parse(d.toString('utf8'));
  return Array.isArray(j.entries) ? j.entries : [];
}
// ---- v0.22.6 索引一致性加固：跨进程互斥 + 原子落盘 + 静默校准 ----
// 索引是派生数据，记忆文件才是唯一真源；多智能体并发写入时防止互相覆盖，并自动对齐漂移。
function sleepSyncMs(ms) {
  try { Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms); }
  catch (e) { const end = Date.now() + ms; while (Date.now() < end) { /* busy fallback */ } }
}
function atomicWriteFileSync(fp, data) {
  const tmp = fp + '.tmp-' + process.pid + '-' + crypto.randomBytes(4).toString('hex');
  fs.writeFileSync(tmp, data);
  let lastError = null;
  for (let i = 0; i < 5; i++) {
    try { fs.renameSync(tmp, fp); return; }
    catch (e) { lastError = e; sleepSyncMs(15 + i * 25); }
  }
  try { fs.unlinkSync(tmp); } catch (e) { /* ignore */ }
  throw lastError;
}
const INDEX_LOCK_NAME = '.index.lock';
const heldIndexLocks = new Set();
function indexLockPath(root) { return path.join(root, INDEX_LOCK_NAME); }
// 跨进程互斥（mkdir 原子语义）；锁竞争超时后降级为原行为，由静默校准兜底。
function withIndexLock(root, fn) {
  const key = path.resolve(root);
  if (heldIndexLocks.has(key)) return fn();
  const lockPath = indexLockPath(root);
  const started = Date.now();
  let acquired = false;
  while (Date.now() - started < 4000) {
    try { fs.mkdirSync(lockPath); acquired = true; break; }
    catch (e) {
      if (e && e.code !== 'EEXIST') break;
      try {
        const st = fs.statSync(lockPath);
        if (Date.now() - st.mtimeMs > 120000) { fs.rmdirSync(lockPath); continue; }
      } catch (e2) { /* 锁刚释放，直接重试 */ }
      sleepSyncMs(25 + Math.floor(Math.random() * 40));
    }
  }
  if (!acquired) return fn();
  heldIndexLocks.add(key);
  try { return fn(); }
  finally {
    heldIndexLocks.delete(key);
    try { fs.rmdirSync(lockPath); } catch (e) { /* ignore */ }
  }
}
// 只读对账：记忆文件（真源）与索引（根索引 + 有密钥 owner 的私密索引）逐条比对。
function indexConsistencyReport(root, options) {
  options = options || {};
  const fileSet = new Set(collectEntryFiles(root).map(function (fp) {
    return path.relative(root, fp).replace(/\\/g, '/');
  }));
  const entrySet = new Set();
  for (const e of (loadIndex(root) || [])) if (e && e.file) entrySet.add(String(e.file));
  const ownersChecked = [];
  const ownersSkipped = [];
  if (isEncrypted(root)) {
    for (const owner of collectOwners(root)) {
      const key = getOwnerKeyFor(root, owner, options.identity);
      if (!key) { ownersSkipped.push(owner); continue; }
      ownersChecked.push(owner);
      let entries = [];
      try { entries = loadOwnerIndex(root, owner, key); } catch (e) { entries = []; }
      for (const e of entries) if (e && e.file) entrySet.add(String(e.file));
    }
  }
  const skipOwners = new Set(ownersSkipped);
  const missing = [];
  let skippedFiles = 0;
  for (const rel of fileSet) {
    if (rel.indexOf(PRIVATE_DIR + '/') === 0) {
      const owner = rel.split('/')[1] || '';
      if (skipOwners.has(owner)) { skippedFiles += 1; continue; }
    }
    if (!entrySet.has(rel)) missing.push(rel);
  }
  const ghosts = [];
  for (const rel of entrySet) if (!fileSet.has(rel)) ghosts.push(rel);
  return {
    drift: missing.length > 0 || ghosts.length > 0,
    files: fileSet.size - skippedFiles,
    filesTotal: fileSet.size,
    skippedFiles: skippedFiles,
    entries: entrySet.size,
    missing: missing.length,
    missingSample: missing.slice(0, 10),
    ghosts: ghosts.length,
    ghostSample: ghosts.slice(0, 10),
    ownersChecked: ownersChecked,
    ownersSkipped: ownersSkipped,
  };
}
let lastIndexHealAt = 0;
// 静默校准：发现漂移自动按文件真源重建索引；只对齐索引，不动任何记忆文件。
function maybeHealIndex(root, options) {
  options = options || {};
  const now = Date.now();
  if (!options.force && now - lastIndexHealAt < 60000) return { checked: false, healed: false };
  lastIndexHealAt = now;
  let report = null;
  try { report = indexConsistencyReport(root, options); }
  catch (e) { return { checked: true, healed: false, error: e }; }
  if (!report.drift) return { checked: true, healed: false, report: report };
  try { buildIndex(root); }
  catch (e) { return { checked: true, healed: false, error: e, report: report }; }
  let after = report;
  try { after = indexConsistencyReport(root, options); } catch (e) { /* keep pre-heal report */ }
  return { checked: true, healed: true, report: report, after: after };
}
function saveOwnerIndex(root, owner, ownerKey, entries) {
  const data = JSON.stringify({ version: 1, updated: today(), entries: entries }, null, 2);
  const env = aesEncryptBytes(ownerKey, Buffer.from(data, 'utf8'), Buffer.from('index:' + owner, 'utf8'));
  const dir = path.join(root, PRIVATE_DIR, owner);
  fs.mkdirSync(dir, { recursive: true });
  atomicWriteFileSync(path.join(dir, ENC_INDEX_FILE), Buffer.concat([Buffer.from(IDX_MAGIC, 'utf8'), env]));
}
function hasPlaintextPrivate(root) {
  for (const owner of collectOwners(root)) {
    for (const t of PRIVATE_LEAF) {
      const d = path.join(root, PRIVATE_DIR, owner, t);
      if (!fs.existsSync(d)) continue;
      for (const f of fs.readdirSync(d)) if (f.endsWith('.md')) return true;
    }
    if (fs.existsSync(path.join(root, PRIVATE_DIR, owner, PROFILE_FILE))) return true;
  }
  return false;
}
function profilePathFor(root, owner) {
  const base = path.join(root, PRIVATE_DIR, owner, PROFILE_FILE);
  if (fs.existsSync(base)) return base;
  return base + ENC_SUFFIX;
}
function readProfileText(root, owner) {
  const p = profilePathFor(root, owner);
  if (!fs.existsSync(p)) return null;
  return readMemoryText(root, p, owner);
}
function writeProfileText(root, owner, text) {
  const dir = path.join(root, PRIVATE_DIR, owner);
  fs.mkdirSync(dir, { recursive: true });
  const encrypted = isEncrypted(root);
  const p = encrypted ? path.join(dir, PROFILE_FILE + ENC_SUFFIX) : path.join(dir, PROFILE_FILE);
  writeMemoryText(root, p, text, owner);
  if (encrypted && fs.existsSync(path.join(dir, PROFILE_FILE))) {
    try { fs.unlinkSync(path.join(dir, PROFILE_FILE)); } catch (e) {}
  }
  return p;
}

// ---- 索引（index.json）----
function indexPath(root) { return path.join(root, INDEX_FILE); }
const INDEX_VERSION = 5;
const INDEX_MIN_SUPPORTED_VERSION = 4;
// v0.24.0：索引按逻辑体积或条目数触发年份分片；大库使用 gzip 分片。
const INDEX_SHARD_THRESHOLD = 5000;
const INDEX_COMPRESS_TRIGGER_BYTES = 4 * 1024 * 1024;
// 安全校验：只接受 index-YYYY.json(.gz)，防 manifest 篡改导致路径穿越。
const SHARD_RE = /^index-\d{4}\.json(?:\.gz)?$/;
function isSafeShardName(name) { return typeof name === 'string' && SHARD_RE.test(name); }
function isGzipShardName(name) { return typeof name === 'string' && /\.json\.gz$/.test(name); }
function indexShardName(year, compressed) { return 'index-' + year + '.json' + (compressed === false ? '' : '.gz'); }
function shardYear(name) {
  const match = String(name || '').match(/^index-(\d{4})\.json(?:\.gz)?$/);
  return match ? match[1] : '';
}
function readIndexShard(root, name) {
  if (!isSafeShardName(name)) return null;
  const full = path.join(root, name);
  if (!fs.existsSync(full)) return null;
  try {
    const raw = fs.readFileSync(full);
    const text = isGzipShardName(name) ? zlib.gunzipSync(raw).toString('utf8') : raw.toString('utf8');
    const parsed = JSON.parse(text);
    return parsed && Array.isArray(parsed.entries) ? parsed : null;
  } catch (error) {
    return null;
  }
}
function writeIndexShard(root, name, payload) {
  const raw = Buffer.from(JSON.stringify(payload), 'utf8');
  const data = isGzipShardName(name) ? zlib.gzipSync(raw, { level: 9, mtime: 0 }) : raw;
  atomicWriteFileSync(path.join(root, name), data);
}
function entryYear(entry) {
  return String((entry && entry.created) || '').slice(0, 4) || String(today()).slice(0, 4);
}
// v0.17.0：--year 只接受四位年份，可重复；不传即全量（既有行为零变化）。
function normalizeYearList(value) {
  if (value === undefined || value === null) return { years: [], error: '' };
  const list = Array.isArray(value) ? value : [value];
  const years = [];
  for (const raw of list) {
    const year = String(raw === undefined || raw === null ? '' : raw).trim();
    if (!/^\d{4}$/.test(year)) {
      return { years: [], error: '年份格式不正确: ' + String(raw) + '。--year 只接受四位年份（例如 --year 2026），可重复传多次。' };
    }
    if (years.indexOf(year) === -1) years.push(year);
  }
  return { years: years, error: '' };
}
function loadIndexManifest(root) {
  const p = indexPath(root);
  if (!fs.existsSync(p)) return null;
  try {
    const d = JSON.parse(fs.readFileSync(p, 'utf8'));
    if (d && Array.isArray(d.shards) && (!d.version || d.version >= INDEX_MIN_SUPPORTED_VERSION)) return d;
  } catch (e) { /* ignore */ }
  return null;
}
function loadIndex(root) {
  const p = indexPath(root);
  if (!fs.existsSync(p)) return null;
  try {
    const d = JSON.parse(fs.readFileSync(p, 'utf8'));
    if (!d) return null;
    if (Array.isArray(d.entries)) {
      // v4 平铺索引与 v5 平铺索引都继续读取；更旧版本返回 null 触发重建。
      if (d.version && d.version >= INDEX_MIN_SUPPORTED_VERSION) return d.entries;
      return null;
    }
    if (Array.isArray(d.shards)) {
      if (d.version && d.version < INDEX_MIN_SUPPORTED_VERSION) return null;
      const out = [];
      for (const sh of d.shards) {
        const sd = readIndexShard(root, sh);
        if (!sd) return null;
        out.push.apply(out, sd.entries);
      }
      return out;
    }
  } catch (e) { /* ignore */ }
  return null;
}
// v0.17.0 B3：按年份懒加载索引——命中分片 manifest 时只读 years 覆盖的分片；
// years 为空维持全量 loadIndex（逐字节行为不变）。平铺索引无法少读文件，按条目年份过滤。
function loadIndexFor(root, options) {
  const filter = normalizeYearList(options && (options.years !== undefined ? options.years : options.year));
  if (filter.error) return null;
  const years = filter.years;
  if (!years.length) return loadIndex(root);
  const p = indexPath(root);
  if (!fs.existsSync(p)) return null;
  try {
    const d = JSON.parse(fs.readFileSync(p, 'utf8'));
    if (!d) return null;
    if (Array.isArray(d.entries)) {
      if (d.version && d.version < INDEX_MIN_SUPPORTED_VERSION) return null;
      const want = new Set(years);
      return d.entries.filter(function (e) { return want.has(entryYear(e)); });
    }
    if (Array.isArray(d.shards)) {
      if (d.version && d.version < INDEX_MIN_SUPPORTED_VERSION) return null;
      const want = new Set(years);
      const out = [];
      for (const sh of d.shards) {
        if (!isSafeShardName(sh)) continue;
        if (!want.has(shardYear(sh))) continue; // 只读取命中年份的分片文件
        const sd = readIndexShard(root, sh);
        if (!sd) return null;
        out.push.apply(out, sd.entries);
      }
      return out;
    }
  } catch (e) { /* ignore */ }
  return null;
}
function indexEntriesFor(root, options) {
  const filter = normalizeYearList(options && options.years);
  if (filter.error) return { entries: [], error: filter.error };
  if (filter.years.length) {
    const lazy = loadIndexFor(root, { years: filter.years });
    if (lazy) return { entries: lazy, error: '' };
  }
  const all = ensureIndex(root);
  if (!filter.years.length) return { entries: all, error: '' };
  const want = new Set(filter.years);
  return { entries: all.filter(function (e) { return want.has(entryYear(e)); }), error: '' };
}
function getIndex(root) { return loadIndex(root) || []; }
function saveIndex(root, entries, options) {
  options = options || {};
  const clean = entries.map(function (e) { const c = Object.assign({}, e); delete c.meta; return c; });
  const old = loadIndexManifest(root);
  const shardThreshold = options.shardThresholdEntries === undefined ? INDEX_SHARD_THRESHOLD : Number(options.shardThresholdEntries);
  const byteThreshold = options.compressThresholdBytes === undefined ? INDEX_COMPRESS_TRIGGER_BYTES : Number(options.compressThresholdBytes);
  const compress = options.compress !== false;
  const logicalBytes = jsonByteLength(clean);
  if (clean.length > shardThreshold || logicalBytes > byteThreshold) {
    const byYear = {};
    for (const e of clean) {
      const y = entryYear(e);
      (byYear[y] = byYear[y] || []).push(e);
    }
    const newShards = [];
    for (const y of Object.keys(byYear).sort()) {
      const name = indexShardName(y, compress);
      writeIndexShard(root, name, { version: INDEX_VERSION, year: (parseInt(y, 10) || 0), entries: byYear[y] });
      newShards.push(name);
    }
    atomicWriteFileSync(indexPath(root), JSON.stringify({
      version: INDEX_VERSION,
      updated: today(),
      format: compress ? 'gzip-year' : 'json-year',
      shards: newShards,
      count: clean.length,
    }, null, 2), 'utf8');
    if (old && Array.isArray(old.shards)) {
      for (const sh of old.shards) if (newShards.indexOf(sh) === -1 && isSafeShardName(sh)) { try { fs.unlinkSync(path.join(root, sh)); } catch (e) {} }
    }
  } else {
    atomicWriteFileSync(indexPath(root), JSON.stringify({ version: INDEX_VERSION, updated: today(), entries: clean }, null, 2), 'utf8');
    if (old && Array.isArray(old.shards)) {
      for (const sh of old.shards) { try { fs.unlinkSync(path.join(root, sh)); } catch (e) {} }
    }
  }
}
function jsonByteLength(value) {
  return Buffer.byteLength(JSON.stringify(value === undefined ? null : value), 'utf8');
}
function indexFieldBytes(entries) {
  const groups = {
    tokens: ['tokens'],
    statement: ['statement'],
    subject: ['subject'],
    tags: ['tags'],
    usage: ['access_count', 'last_accessed', 'feedback_net', 'hit_days', 'hit_queries'],
  };
  const grouped = new Set();
  for (const names of Object.values(groups)) for (const name of names) grouped.add(name);
  const out = { tokens: 0, statement: 0, subject: 0, tags: 0, usage: 0, other: 0, total: 0, overhead: 0 };
  for (const entry of entries) {
    out.total += jsonByteLength(entry);
    for (const group of Object.keys(groups)) {
      for (const name of groups[group]) out[group] += jsonByteLength(entry[name]);
    }
    for (const name of Object.keys(entry)) {
      if (!grouped.has(name)) out.other += jsonByteLength(entry[name]);
    }
  }
  out.overhead = Math.max(0, out.total - (out.tokens + out.statement + out.subject + out.tags + out.usage + out.other));
  return out;
}
function indexTokenStats(entries) {
  let unique = 0;
  let weighted = 0;
  let pinyin = 0;
  for (const entry of entries) {
    const tokens = entry && entry.tokens && typeof entry.tokens === 'object' ? entry.tokens : {};
    for (const key of Object.keys(tokens)) {
      unique += 1;
      weighted += Number(tokens[key]) || 0;
      if (key.indexOf('py:') === 0 || key.indexOf('pyi:') === 0) pinyin += 1;
    }
  }
  return {
    unique: unique,
    weighted: Math.round(weighted * 1000) / 1000,
    pinyin: pinyin,
    averageUniquePerEntry: entries.length ? Math.round((unique / entries.length) * 1000) / 1000 : 0,
  };
}
function indexGzipProjection(entries) {
  const byYear = {};
  for (const entry of entries) {
    const clean = Object.assign({}, entry);
    delete clean.meta;
    const year = entryYear(clean);
    (byYear[year] = byYear[year] || []).push(clean);
  }
  const shards = [];
  let gzipBytes = 0;
  for (const year of Object.keys(byYear).sort()) {
    const raw = Buffer.from(JSON.stringify({ version: 5, year: parseInt(year, 10) || 0, entries: byYear[year] }), 'utf8');
    const compressed = zlib.gzipSync(raw, { level: 9, mtime: 0 });
    gzipBytes += compressed.length;
    shards.push({
      year: year,
      entries: byYear[year].length,
      jsonBytes: raw.length,
      gzipBytes: compressed.length,
    });
  }
  const manifest = Buffer.from(JSON.stringify({
    version: 5,
    updated: '',
    shards: shards.map(function (item) { return 'index-' + item.year + '.json.gz'; }),
    count: entries.length,
  }), 'utf8');
  const storageBytes = gzipBytes + manifest.length;
  return {
    format: 'index-v5-gzip-year',
    storageBytes: storageBytes,
    manifestBytes: manifest.length,
    shards: shards,
  };
}
function indexStatsCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.root || userRoot());
  const idx = indexPath(root);
  if (!fs.existsSync(idx)) {
    return { error: true, format: 'missing', entryCount: 0, storageBytes: 0, text: '索引不存在: ' + idx + '。请先运行 yotta-memory reindex。' };
  }
  let manifestBytes = 0;
  let data = null;
  try {
    manifestBytes = fs.statSync(idx).size;
    data = JSON.parse(fs.readFileSync(idx, 'utf8'));
  } catch (error) {
    return { error: true, format: 'invalid', entryCount: 0, storageBytes: manifestBytes, text: '索引无法解析: ' + error.message };
  }
  if (!data || (!Array.isArray(data.entries) && !Array.isArray(data.shards))) {
    return { error: true, format: 'invalid', entryCount: 0, storageBytes: manifestBytes, text: '索引结构无效：缺少 entries 或 shards 数组。' };
  }
  const warnings = [];
  const entries = [];
  let shardBytes = 0;
  const shards = [];
  if (Array.isArray(data.entries)) {
    entries.push.apply(entries, data.entries);
  } else {
    for (const shard of data.shards) {
      if (!isSafeShardName(shard)) {
        warnings.push('忽略不安全分片名: ' + String(shard));
        continue;
      }
      const full = path.join(root, shard);
      if (!fs.existsSync(full)) {
        warnings.push('分片缺失: ' + shard);
        continue;
      }
      try {
        const bytes = fs.statSync(full).size;
        const parsed = readIndexShard(root, shard);
        shardBytes += bytes;
        if (parsed) {
          entries.push.apply(entries, parsed.entries);
          shards.push({ name: shard, bytes: bytes, entries: parsed.entries.length });
        } else {
          warnings.push('分片结构无效: ' + shard);
        }
      } catch (error) {
        warnings.push('分片无法解析: ' + shard + '（' + error.message + '）');
      }
    }
  }
  const storageBytes = manifestBytes + shardBytes;
  const logicalBytes = jsonByteLength(entries);
  const fieldBytes = indexFieldBytes(entries);
  const tokens = indexTokenStats(entries);
  const gzipProjection = indexGzipProjection(entries);
  const warnBytes = scaleThreshold(loadConfig(), 'scale_warn_index_bytes');
  gzipProjection.underWarningThreshold = gzipProjection.storageBytes <= warnBytes;
  gzipProjection.warningThresholdBytes = warnBytes;
  gzipProjection.compressionRatio = storageBytes ? Math.round((gzipProjection.storageBytes / storageBytes) * 1000) / 1000 : 0;
  const triggerReasons = [];
  if (entries.length > INDEX_SHARD_THRESHOLD) triggerReasons.push('entries');
  if (logicalBytes > INDEX_COMPRESS_TRIGGER_BYTES) triggerReasons.push('logical_bytes');
  const lines = [
    '索引统计（只读）',
    '- 格式: ' + (Array.isArray(data.entries) ? 'inline' : 'sharded'),
    '- 条目: ' + entries.length,
    '- 索引存储: ' + storageBytes + ' 字节（manifest ' + manifestBytes + ' / 分片 ' + shardBytes + '）',
    '- 逻辑原始体积: ' + logicalBytes + ' 字节',
    '- token: ' + tokens.unique + ' 个唯一 token（加权 ' + tokens.weighted + ' / 拼音 ' + tokens.pinyin + ' / 平均 ' + tokens.averageUniquePerEntry + ' 每条例）',
    '- 字段体积: tokens ' + fieldBytes.tokens + ' / statement ' + fieldBytes.statement + ' / subject ' + fieldBytes.subject + ' / tags ' + fieldBytes.tags + ' / usage ' + fieldBytes.usage + ' / other ' + fieldBytes.other,
    '- gzip 年份分片预估: ' + gzipProjection.storageBytes + ' 字节（压缩比 ' + gzipProjection.compressionRatio + ' / 低于告警线 ' + (gzipProjection.underWarningThreshold ? '是' : '否') + '）',
    '- 触发建议: ' + (triggerReasons.length ? triggerReasons.join(' + ') : '当前无需按现有阈值分片'),
  ];
  if (warnings.length) lines.push('- 告警: ' + warnings.join('；'));
  return {
    error: false,
    root: root,
    format: Array.isArray(data.entries) ? 'inline' : 'sharded',
    version: Number(data.version || 0),
    updated: data.updated || '',
    entryCount: entries.length,
    shardCount: shards.length,
    shards: shards,
    manifestBytes: manifestBytes,
    shardBytes: shardBytes,
    storageBytes: storageBytes,
    logicalBytes: logicalBytes,
    fieldBytes: fieldBytes,
    tokens: tokens,
    gzipProjection: gzipProjection,
    trigger: {
      entryThreshold: INDEX_SHARD_THRESHOLD,
      logicalByteThreshold: INDEX_COMPRESS_TRIGGER_BYTES,
      reasons: triggerReasons,
    },
    warnings: warnings,
    text: lines.join('\n'),
  };
}
function collectEntryFiles(root) {
  const dirs = [];
  const facts = path.join(root, PUBLIC_DIR);
  if (fs.existsSync(facts)) dirs.push(facts);
  const pdir = path.join(root, PRIVATE_DIR);
  if (fs.existsSync(pdir)) {
    for (const id of fs.readdirSync(pdir)) {
      const idDir = path.join(pdir, id);
      if (!fs.statSync(idDir).isDirectory()) continue;
      for (const t of PRIVATE_LEAF) {
        const d = path.join(idDir, t);
        if (fs.existsSync(d)) dirs.push(d);
      }
    }
  }
  const out = [];
  // v0.17.0：递归下探年/月子目录；旧平铺文件依旧按原路径收集。
  for (const dir of dirs) walkEntryFiles(dir, out);
  return out;
}
// v0.17.0：平铺 / 分层只影响存放位置，不改变条目身份。
// 身份键 = 类型 + owner + 文件名（YYYY-MM-DD-NNNN.md），同身份先比较内容摘要。
const LAYOUT_TYPE_BY_DIR = { facts: 'FACT', prefs: 'PREF', bounds: 'BOUND', commits: 'COMMIT' };
function publicFrontmatterOwner(fp) {
  try {
    return String(parseFrontmatter(fs.readFileSync(fp, 'utf8')).meta.owner || '').trim();
  } catch (e) {
    return '';
  }
}
function layoutEntryIdentity(root, fp) {
  const rel = path.relative(root, fp).replace(/\\/g, '/');
  const parts = entryRelParts(rel);
  if (!parts) return null;
  const type = LAYOUT_TYPE_BY_DIR[parts.type];
  if (!type) return null;
  const base = path.basename(rel).replace(/\.enc$/, '');
  if (!/^\d{4}-\d{2}-\d{2}-\d{4}\.md$/.test(base)) return null;
  const owner = parts.kind === 'public' ? publicFrontmatterOwner(fp) : parts.owner;
  return {
    key: [parts.kind, owner, type, base].join('\0'),
    rel: rel,
    owner: owner,
  };
}
function normalizedLayoutDigest(buf) {
  // latin1 往返保留原始字节，同时把 CRLF 归一，避免 Windows / Linux 检出差异制造假冲突。
  const normalized = Buffer.from(buf.toString('latin1').replace(/\r\n/g, '\n'), 'latin1');
  return crypto.createHash('sha256').update(normalized).digest('hex');
}
function layoutFileDigests(root, fp, owner) {
  const buf = fs.readFileSync(fp);
  const rawDigest = normalizedLayoutDigest(buf);
  if (!isEncFile(fp)) return { rawDigest: rawDigest, plainDigest: rawDigest };
  const key = getOwnerKeyFor(root, owner);
  if (key) {
    try {
      return { rawDigest: rawDigest, plainDigest: normalizedLayoutDigest(Buffer.from(decryptMemoryText(buf, key), 'utf8')) };
    } catch (e) { /* 密钥不可用或密文损坏时按待核处理 */ }
  }
  return { rawDigest: rawDigest, plainDigest: null };
}
function layoutCollisionReport(root) {
  const grouped = new Map();
  for (const fp of collectEntryFiles(root)) {
    const info = layoutEntryIdentity(root, fp);
    if (!info) continue;
    if (!grouped.has(info.key)) grouped.set(info.key, []);
    grouped.get(info.key).push({ fp: fp, rel: info.rel, owner: info.owner });
  }
  const report = { ok: true, duplicates: 0, conflicts: 0, unverified: 0, groups: [], warnings: [] };
  for (const items of grouped.values()) {
    if (items.length < 2) continue;
    for (const item of items) {
      try {
        const digests = layoutFileDigests(root, item.fp, item.owner);
        item.rawDigest = digests.rawDigest;
        item.plainDigest = digests.plainDigest;
      } catch (e) {
        item.rawDigest = null;
        item.plainDigest = null;
      }
    }
    const plainDigests = items.map(function (item) { return item.plainDigest; });
    const rawDigests = items.map(function (item) { return item.rawDigest; });
    let status;
    if (plainDigests.every(Boolean)) status = new Set(plainDigests).size === 1 ? 'duplicate' : 'conflict';
    else if (rawDigests.every(Boolean) && new Set(rawDigests).size === 1) status = 'duplicate';
    else status = 'unverified';
    const sorted = items.slice().sort(function (a, b) {
      const depth = b.rel.split('/').length - a.rel.split('/').length;
      return depth !== 0 ? depth : a.rel.localeCompare(b.rel);
    });
    const paths = items.map(function (item) { return item.rel; }).sort();
    const group = {
      status: status,
      paths: paths,
      keep: sorted[0].rel,
      drop: sorted.slice(1).map(function (item) { return item.rel; }),
    };
    report.groups.push(group);
    if (status === 'duplicate') report.duplicates++;
    else if (status === 'conflict') {
      report.conflicts++;
      report.warnings.push('布局: 平铺/分层同序号冲突（内容不同，两份均保留可读）: ' + paths.join(' ↔ '));
    } else {
      report.unverified++;
      report.warnings.push('布局: 平铺/分层同序号待核（加密内容当前无法比较，两份均保留）: ' + paths.join(' ↔ '));
    }
  }
  report.ok = report.conflicts === 0 && report.unverified === 0;
  return report;
}
const LAYOUT_PLAN_DIR = path.join('.maintenance', 'layout-plans');
const LAYOUT_JOURNAL_DIR = path.join('.maintenance', 'layout-journals');
function safeLayoutRel(value) {
  const rel = String(value || '').replace(/\\/g, '/');
  if (!rel || path.isAbsolute(rel) || rel.split('/').includes('..')) return false;
  if (!MEMORY_FILE_RE.test(path.posix.basename(rel))) return false;
  return rel.indexOf(PUBLIC_DIR + '/') === 0 || rel.indexOf(PRIVATE_DIR + '/') === 0;
}
function layoutInsideRoot(root, rel) {
  const base = path.resolve(root);
  const full = path.resolve(root, String(rel || ''));
  return full === base || full.indexOf(base + path.sep) === 0;
}
function layoutBaseInfo(rel) {
  const parts = String(rel || '').split('/');
  if (parts[0] === PUBLIC_DIR) return { kind: 'public', baseDepth: 1, owner: '', type: 'facts' };
  if (parts[0] === PRIVATE_DIR && parts.length >= 3) {
    return { kind: 'private', baseDepth: 3, owner: parts[1], type: parts[2] };
  }
  return null;
}
function isLayoutMonthBucket(rel, includeFlat) {
  const parts = String(rel || '').split('/');
  const info = layoutBaseInfo(rel);
  if (!info) return false;
  if (parts.length === info.baseDepth) return !!includeFlat;
  if (parts.length !== info.baseDepth + 2) return false;
  return /^\d{4}$/.test(parts[info.baseDepth]) && /^\d{2}$/.test(parts[info.baseDepth + 1]);
}
function layoutTargetFor(rel) {
  const parts = String(rel || '').split('/');
  const info = layoutBaseInfo(rel);
  const base = path.basename(rel);
  const match = base.match(/^(\d{4})-(\d{2})-(\d{2})-\d{4}\.md(?:\.enc)?$/);
  if (!info || !match) return '';
  return parts.slice(0, info.baseDepth).concat([match[1], match[2], match[3], base]).join('/');
}
function layoutCandidateDirs(root, includeFlat, threshold) {
  const seeds = [];
  const facts = path.join(root, PUBLIC_DIR);
  if (fs.existsSync(facts)) seeds.push({ dir: facts, baseDepth: 1, owner: '' });
  const pdir = path.join(root, PRIVATE_DIR);
  if (fs.existsSync(pdir)) {
    for (const owner of fs.readdirSync(pdir)) {
      const ownerDir = path.join(pdir, owner);
      if (!fs.statSync(ownerDir).isDirectory()) continue;
      for (const type of PRIVATE_LEAF) {
        const typeDir = path.join(ownerDir, type);
        if (fs.existsSync(typeDir)) seeds.push({ dir: typeDir, baseDepth: 3, owner: owner });
      }
    }
  }
  const found = [];
  const visit = function (dir) {
    const rel = path.relative(root, dir).replace(/\\/g, '/');
    if (isLayoutMonthBucket(rel, includeFlat)) {
      const files = fs.readdirSync(dir, { withFileTypes: true })
        .filter(function (entry) { return entry.isFile() && MEMORY_FILE_RE.test(entry.name); })
        .map(function (entry) { return entry.name; });
      if (files.length > threshold) {
        const info = layoutBaseInfo(rel);
        if (info && info.kind === 'private' && isEncrypted(root) && !getOwnerKeyFor(root, info.owner)) {
          found.push({ path: rel, files: files.length, skipped: true, reason: 'encrypted_owner_without_key' });
        } else {
          found.push({ path: rel, files: files.length, skipped: false, reason: '' });
        }
      }
    }
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.isDirectory()) visit(path.join(dir, entry.name));
    }
  };
  for (const seed of seeds) visit(seed.dir);
  return found.sort(function (a, b) { return a.path.localeCompare(b.path); });
}
function layoutBatchId(now) {
  return 'layout-' + now.toISOString().replace(/[:.]/g, '-') + '-' + crypto.randomBytes(3).toString('hex');
}
function layoutPlanCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.root || userRoot());
  const cfg = loadConfig();
  const threshold = opts.threshold === undefined ? scaleThreshold(cfg, 'scale_warn_files_per_dir') : Number(opts.threshold);
  const includeFlat = !!opts.includeFlat;
  const now = opts.now ? new Date(opts.now) : new Date();
  const batch = layoutBatchId(now);
  const candidates = layoutCandidateDirs(root, includeFlat, threshold);
  const operations = [];
  const conflicts = [];
  const warnings = [];
  for (const candidate of candidates) {
    if (candidate.skipped) {
      warnings.push('跳过 ' + candidate.path + ': 加密 owner 无可用密钥');
      continue;
    }
    const dir = path.join(root, candidate.path);
    for (const name of fs.readdirSync(dir)) {
      if (!MEMORY_FILE_RE.test(name)) continue;
      const from = path.posix.join(candidate.path, name);
      const to = layoutTargetFor(from);
      if (!to || !safeLayoutRel(to)) {
        conflicts.push({ from: from, to: to, reason: 'target_invalid' });
        continue;
      }
      if (fs.existsSync(path.join(root, to))) {
        conflicts.push({ from: from, to: to, reason: 'target_exists' });
        continue;
      }
      operations.push({
        from: from,
        to: to,
        sha256: normalizedLayoutDigest(fs.readFileSync(path.join(root, from))),
        status: 'pending',
      });
    }
  }
  operations.sort(function (a, b) { return a.from.localeCompare(b.from); });
  const plan = {
    batch: batch,
    createdAt: now.toISOString(),
    root: root,
    threshold: threshold,
    includeFlat: includeFlat,
    candidates: candidates,
    operations: operations,
    conflicts: conflicts,
    warnings: warnings,
    planFile: '',
  };
  if (conflicts.length) {
    plan.error = true;
    plan.text = '布局迁移计划存在 ' + conflicts.length + ' 个冲突，拒绝生成可执行计划。\n'
      + conflicts.map(function (item) { return '- ' + item.from + ' -> ' + item.to + '（' + item.reason + '）'; }).join('\n');
    return plan;
  }
  const planFile = opts.out
    ? path.resolve(String(opts.out))
    : path.join(root, LAYOUT_PLAN_DIR, batch + '.json');
  fs.mkdirSync(path.dirname(planFile), { recursive: true });
  plan.planFile = planFile;
  atomicWriteFileSync(planFile, JSON.stringify(plan, null, 2), 'utf8');
  plan.error = false;
  plan.text = '布局迁移计划: ' + batch + '\n- 目录: ' + candidates.length + ' 个候选'
    + '（可迁移 ' + candidates.filter(function (item) { return !item.skipped; }).length + '）\n'
    + '- 文件: ' + operations.length + ' 个\n- 计划: ' + planFile
    + (warnings.length ? '\n- 告警: ' + warnings.join('；') : '');
  return plan;
}
function validateLayoutPlan(root, plan) {
  if (!plan || plan.root !== root) return '计划 root 与当前记忆库不一致，拒绝执行。';
  if (!/^layout-[A-Za-z0-9-]+$/.test(String(plan.batch || ''))) return '计划 batch 不安全。';
  if (!Array.isArray(plan.operations) || !plan.operations.length) return '计划没有可执行文件。';
  if (Array.isArray(plan.conflicts) && plan.conflicts.length) return '计划包含冲突，拒绝执行。';
  for (const op of plan.operations) {
    if (!safeLayoutRel(op.from) || !safeLayoutRel(op.to) || !layoutInsideRoot(root, op.from) || !layoutInsideRoot(root, op.to)) {
      return '计划包含不安全路径: ' + String(op.from) + ' -> ' + String(op.to);
    }
  }
  return '';
}
function writeLayoutJournal(pathname, journal) {
  atomicWriteFileSync(pathname, JSON.stringify(journal, null, 2), 'utf8');
}
function restoreLayoutDone(root, journal, pathname) {
  let ok = true;
  for (let i = journal.operations.length - 1; i >= 0; i--) {
    const op = journal.operations[i];
    if (op.status !== 'done') continue;
    const from = path.join(root, op.from);
    const to = path.join(root, op.to);
    if (!fs.existsSync(to) || fs.existsSync(from)) {
      op.status = 'rollback_conflict';
      ok = false;
      continue;
    }
    fs.mkdirSync(path.dirname(from), { recursive: true });
    fs.renameSync(to, from);
    op.status = 'rolled_back';
    writeLayoutJournal(pathname, journal);
  }
  return ok;
}
function withLayoutLock(root, fn) {
  const lock = path.join(root, '.maintenance', 'layout.lock');
  fs.mkdirSync(path.dirname(lock), { recursive: true });
  try {
    fs.writeFileSync(lock, JSON.stringify({ pid: process.pid, created: new Date().toISOString() }), { encoding: 'utf8', flag: 'wx' });
  } catch (error) {
    return { error: true, text: '已有布局迁移在运行或上次未清理 lock: ' + lock };
  }
  try {
    return fn();
  } finally {
    try { fs.unlinkSync(lock); } catch (error) { /* ignore */ }
  }
}
function layoutApplyCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.root || userRoot());
  if (!opts.yes) return { error: true, text: '拒绝执行布局迁移：请复核计划后显式加 --yes。' };
  if (!opts.planFile) return { error: true, text: '请用 --from-plan <文件> 指定布局迁移计划。' };
  const planFile = path.resolve(String(opts.planFile));
  let plan = null;
  try { plan = JSON.parse(fs.readFileSync(planFile, 'utf8')); } catch (error) {
    return { error: true, text: '无法读取布局迁移计划: ' + error.message };
  }
  const invalid = validateLayoutPlan(root, plan);
  if (invalid) return { error: true, text: invalid };
  return withLayoutLock(root, function () {
    const journalFile = path.join(root, LAYOUT_JOURNAL_DIR, plan.batch + '.json');
    if (fs.existsSync(journalFile)) return { error: true, text: '该计划已有 journal，拒绝重复执行: ' + journalFile };
    const journal = {
      batch: plan.batch,
      createdAt: plan.createdAt,
      startedAt: new Date().toISOString(),
      root: root,
      status: 'applying',
      operations: plan.operations.map(function (op) {
        return { from: op.from, to: op.to, sha256: op.sha256, status: 'pending' };
      }),
    };
    fs.mkdirSync(path.dirname(journalFile), { recursive: true });
    writeLayoutJournal(journalFile, journal);
    let moved = 0;
    try {
      for (const op of journal.operations) {
        const from = path.join(root, op.from);
        const to = path.join(root, op.to);
        if (!fs.existsSync(from)) throw new Error('源文件缺失: ' + op.from);
        const digest = normalizedLayoutDigest(fs.readFileSync(from));
        if (digest !== op.sha256) throw new Error('源文件哈希变化: ' + op.from);
        if (fs.existsSync(to)) throw new Error('目标已存在: ' + op.to);
        fs.mkdirSync(path.dirname(to), { recursive: true });
        fs.renameSync(from, to);
        op.status = 'done';
        moved += 1;
        writeLayoutJournal(journalFile, journal);
      }
      buildIndex(root);
      journal.status = 'applied';
      journal.completedAt = new Date().toISOString();
      writeLayoutJournal(journalFile, journal);
      return {
        error: false,
        batch: plan.batch,
        moved: moved,
        rolledBack: false,
        planFile: planFile,
        journalFile: journalFile,
        text: '布局迁移完成: ' + plan.batch + '（' + moved + ' 文件）\n计划: ' + planFile + '\nJournal: ' + journalFile,
      };
    } catch (error) {
      const rolledBack = restoreLayoutDone(root, journal, journalFile);
      journal.status = rolledBack ? 'rolled_back' : 'rollback_failed';
      journal.error = error.message;
      journal.completedAt = new Date().toISOString();
      writeLayoutJournal(journalFile, journal);
      try { buildIndex(root); } catch (e) { /* ignore */ }
      return {
        error: true,
        batch: plan.batch,
        moved: moved,
        rolledBack: rolledBack,
        planFile: planFile,
        journalFile: journalFile,
        text: '布局迁移失败并' + (rolledBack ? '已回滚' : '回滚不完整') + ': ' + error.message + '\nJournal: ' + journalFile,
      };
    }
  });
}
function layoutRollbackCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.root || userRoot());
  if (!opts.yes) return { error: true, text: '拒绝回滚布局迁移：请显式加 --yes。' };
  if (!/^layout-[A-Za-z0-9-]+$/.test(String(opts.batch || ''))) return { error: true, text: '请用 --batch <id> 指定安全的布局迁移批次。' };
  const journalFile = path.join(root, LAYOUT_JOURNAL_DIR, opts.batch + '.json');
  let journal = null;
  try { journal = JSON.parse(fs.readFileSync(journalFile, 'utf8')); } catch (error) {
    return { error: true, text: '无法读取布局迁移 journal: ' + error.message };
  }
  if (journal.root !== root) return { error: true, text: 'journal root 与当前记忆库不一致。' };
  if (journal.status === 'rolled_back') return { error: false, batch: opts.batch, rolledBack: 0, journalFile: journalFile, text: '布局迁移批次已回滚，无需重复操作。' };
  if (journal.status !== 'applied') return { error: true, text: '批次状态不是 applied，不能常规回滚: ' + journal.status };
  return withLayoutLock(root, function () {
    let restored = 0;
    try {
      for (let i = journal.operations.length - 1; i >= 0; i--) {
        const op = journal.operations[i];
        if (op.status !== 'done') continue;
        const from = path.join(root, op.from);
        const to = path.join(root, op.to);
        if (!fs.existsSync(to)) throw new Error('迁移目标缺失: ' + op.to);
        if (fs.existsSync(from)) throw new Error('回滚目标已存在: ' + op.from);
        fs.mkdirSync(path.dirname(from), { recursive: true });
        fs.renameSync(to, from);
        op.status = 'rolled_back';
        restored += 1;
        writeLayoutJournal(journalFile, journal);
      }
      buildIndex(root);
      journal.status = 'rolled_back';
      journal.rolledBackAt = new Date().toISOString();
      writeLayoutJournal(journalFile, journal);
      return { error: false, batch: opts.batch, restored: restored, journalFile: journalFile, text: '布局迁移已回滚: ' + opts.batch + '（' + restored + ' 文件）' };
    } catch (error) {
      journal.status = 'rollback_failed';
      journal.rollbackError = error.message;
      writeLayoutJournal(journalFile, journal);
      return { error: true, batch: opts.batch, restored: restored, journalFile: journalFile, text: '布局回滚失败: ' + error.message };
    }
  });
}
// 迁移：把根下旧平铺 prefs|bounds|commits/*.md 按 frontmatter owner 迁入 private/<owner>/<type>/
function migrateLayout(root) {
  let moved = 0;
  for (const t of PRIVATE_LEAF) {
    const dir = path.join(root, t);
    if (!fs.existsSync(dir)) continue;
    for (const f of fs.readdirSync(dir)) {
      const fp = path.join(dir, f);
      if (!fs.statSync(fp).isFile()) continue;
      const meta = parseFrontmatter(fs.readFileSync(fp, 'utf8')).meta;
      const owner = meta.owner || '';
      if (!owner) continue;
      const target = path.join(root, PRIVATE_DIR, owner, t, f);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.renameSync(fp, target);
      moved++;
    }
  }
  return moved;
}
function buildIndex(root) {
  return withIndexLock(root, function () {
    migrateLayout(root);
    const layout = layoutCollisionReport(root);
    const skip = new Set();
    for (const group of layout.groups) {
      if (group.status !== 'duplicate') continue;
      for (const rel of group.drop) skip.add(rel);
    }
    const publicEntries = [];
    const privateByOwner = {};
    for (const fp of collectEntryFiles(root)) {
      const rel = path.relative(root, fp).replace(/\\/g, '/');
      if (skip.has(rel)) continue;
      if (rel.indexOf(PRIVATE_DIR + '/') === 0) {
        const owner = rel.split('/')[1] || '';
        // v0.23.0 修复（WorkBuddy D2）：未加密库没有 owner key（getOwnerKeyFor 恒为 null），
        // 私密条目须与公共条目同存主索引（与 upsertIndexEntry 口径一致），
        // 否则 reindex / 静默校准会把私密条目整段跳过，索引越重建越空。
        if (isEncrypted(root)) {
          if (!getOwnerKeyFor(root, owner)) continue;
          let e;
          try { e = readEntry(fp, root); } catch (err) { continue; }
          (privateByOwner[owner] = privateByOwner[owner] || []).push(e);
        } else {
          try { publicEntries.push(readEntry(fp, root)); } catch (err) { /* ignore */ }
        }
      } else {
        try { publicEntries.push(readEntry(fp, root)); } catch (err) { /* ignore */ }
      }
    }
    saveIndex(root, publicEntries);
    for (const owner of Object.keys(privateByOwner)) {
      const key = getOwnerKeyFor(root, owner);
      if (key) saveOwnerIndex(root, owner, key, privateByOwner[owner]);
    }
    const all = publicEntries.slice();
    for (const owner of Object.keys(privateByOwner)) all.push.apply(all, privateByOwner[owner]);
    return all;
  });
}
function ensureIndex(root) {
  try { maybeHealIndex(root); } catch (e) { /* 静默校准失败不阻断读取 */ }
  if (!isEncrypted(root)) {
    const idx = loadIndex(root);
    return idx || buildIndex(root);
  }
  const all = [];
  const pub = loadIndex(root);
  if (pub) all.push.apply(all, pub);
  for (const owner of collectOwners(root)) {
    const key = getOwnerKeyFor(root, owner);
    if (!key) continue;
    let idx = [];
    try { idx = loadOwnerIndex(root, owner, key); } catch (err) { idx = []; }
    all.push.apply(all, idx);
  }
  return all;
}
function upsertIndexEntry(root, entry) {
  return withIndexLock(root, function () {
    if (isEncrypted(root) && entry.scope !== 'public' && String(entry.file).indexOf(PUBLIC_DIR + '/') !== 0) {
      const owner = entry.owner || String(entry.file).split('/')[1] || '';
      const key = getOwnerKeyFor(root, owner);
      if (!key) return;
      const idx = loadOwnerIndex(root, owner, key);
      const i = idx.findIndex(function (e) { return e.file === entry.file; });
      if (i >= 0) idx[i] = entry; else idx.push(entry);
      saveOwnerIndex(root, owner, key, idx);
      return;
    }
    const idx = getIndex(root);
    const i = idx.findIndex(function (e) { return e.file === entry.file; });
    if (i >= 0) idx[i] = entry; else idx.push(entry);
    saveIndex(root, idx);
  });
}
function removeIndexEntry(root, file) {
  return withIndexLock(root, function () {
    if (isEncrypted(root) && String(file).indexOf(PRIVATE_DIR + '/') === 0) {
      const owner = String(file).split('/')[1] || '';
      const key = getOwnerKeyFor(root, owner);
      if (!key) return;
      const idx = loadOwnerIndex(root, owner, key);
      const next = idx.filter(function (e) { return e.file !== file; });
      if (next.length !== idx.length) saveOwnerIndex(root, owner, key, next);
      return;
    }
    const idx = getIndex(root);
    const i = idx.findIndex(function (e) { return e.file === file; });
    if (i >= 0) { idx.splice(i, 1); saveIndex(root, idx); }
  });
}
function removeIndexEntries(root, files) {
  return withIndexLock(root, function () {
    const set = new Set(files);
    const byOwner = {};
    const pub = [];
    for (const f of files) {
      if (String(f).indexOf(PRIVATE_DIR + '/') === 0) {
        const o = String(f).split('/')[1] || '';
        (byOwner[o] = byOwner[o] || []).push(f);
      } else pub.push(f);
    }
    if (pub.length) {
      const idx = getIndex(root);
      const next = idx.filter(function (e) { return !set.has(e.file); });
      if (next.length !== idx.length) saveIndex(root, next);
    }
    for (const o of Object.keys(byOwner)) {
      const key = getOwnerKeyFor(root, o);
      if (!key) continue;
      const idx = loadOwnerIndex(root, o, key);
      const oset = new Set(byOwner[o]);
      const next = idx.filter(function (e) { return !oset.has(e.file); });
      if (next.length !== idx.length) saveOwnerIndex(root, o, key, next);
    }
  });
}

// ---- 读取 / 写入记忆文件 ----
function readEntry(fp, root) {
  const owner = ownerFromPrivatePath(root, fp);
  let text;
  if (isEncFile(fp)) {
    const key = getOwnerKeyFor(root, owner);
    if (!key) throw new Error('私密区已加密：当前无 ' + owner + ' 的授权密钥（yotta-memory view → 授权本智能体）。');
    text = decryptMemoryText(fs.readFileSync(fp), key);
  } else {
    text = fs.readFileSync(fp, 'utf8');
  }
  const parsed = parseFrontmatter(text);
  const meta = parsed.meta;
  const type = (meta.type || 'FACT').toUpperCase();
  const subject = meta.subject || '';
  const statement = meta.statement || '';
  const tags = parseTags(meta.tags);
  return {
    file: path.relative(root, fp).replace(/\\/g, '/'),
    type: type,
    scope: meta.scope || defaultScope(type),
    owner: meta.owner || '',
    subject: subject,
    statement: statement,
    tags: tags,
    confidence: parseFloat(meta.confidence || 1.0),
    created: meta.created || '',
    updated: meta.updated || '',
    access_count: parseInt(meta.access_count || '0', 10) || 0,
    last_accessed: meta.last_accessed || '',
    immutable: meta.immutable === 'true',
    source: meta.source || '',
    weight: (parseFloat(meta.weight) > 0 ? parseFloat(meta.weight) : 1.0),
    feedback_net: feedbackNetOf(meta),
    hit_days: meta.hit_days || '',
    hit_queries: meta.hit_queries || '',
    tokens: buildTokens(subject, statement, tags),
    meta: meta,
  };
}
function rewriteFrontmatter(fp, patch, root, owner, bodyOverride) {
  let text;
  try { text = readMemoryText(root || memoryRootForFile(fp), fp, owner || ownerFromPrivatePath(root || memoryRootForFile(fp), fp)); }
  catch (e) { throw e; }
  const parsed = parseFrontmatter(text);
  const meta = Object.assign({}, parsed.meta);
  for (const k of Object.keys(patch)) meta[k] = patch[k];
  const body = bodyOverride === undefined ? parsed.body : String(bodyOverride);
  writeMemoryText(root || memoryRootForFile(fp), fp, frontmatterToText(meta, body), owner || ownerFromPrivatePath(root || memoryRootForFile(fp), fp));
}
function bumpReadMeta(root, relFiles, options) {
  options = options || {};
  const now = today();
  const settings = usageSettings(options);
  const selfAgent = (options.selfAgent !== undefined) ? options.selfAgent : resolveIdentity(options).id;
  const usageByFile = {};
  for (const rel of relFiles) {
    const fp = path.join(root, rel);
    if (!fs.existsSync(fp)) continue;
    const owner = ownerFromPrivatePath(root, fp);
    // v0.18.0：跨 owner 私密条目一律不写（读得到也不代表能改别人的文件）。
    if (owner && owner !== selfAgent) continue;
    let parsed;
    try { parsed = parseFrontmatter(readMemoryText(root, fp, owner)); } catch (e) { continue; }
    const meta = parsed.meta;
    if (meta.immutable === 'true') continue;
    const acc = (parseInt(meta.access_count || '0', 10) || 0) + 1;
    const patch = { access_count: acc, last_accessed: now };
    if (settings.enabled) {
      const usagePatch = usagePatchForMeta(meta, 'search', options.query || '', settings, now);
      Object.assign(patch, usagePatch);
      usageByFile[rel] = usagePatch;
    }
    try {
      const prevStat = statFileTimes(fp);
      rewriteFrontmatter(fp, patch, root, owner);
      restoreFileTimes(fp, prevStat);
    } catch (e) {
      // 打点写失败不影响读取结果本身；索引也保持原样。
      delete usageByFile[rel];
    }
  }
  return { usageByFile: usageByFile };
}
function touchIndex(root, relFiles, options) {
  options = options || {};
  const set = new Set(relFiles);
  const now = today();
  const usageByFile = options.usageByFile || {};
  const bumpEntry = function (e) {
    e.access_count = (parseInt(e.access_count, 10) || 0) + 1;
    e.last_accessed = now;
    const usage = usageByFile[e.file];
    if (usage) {
      if (usage.hit_days !== undefined) e.hit_days = usage.hit_days;
      if (usage.hit_queries !== undefined) e.hit_queries = usage.hit_queries;
    }
  };
  // v0.18.0：加密库的私密条目命中必须当场同步 owner index（旧版会滞后到 reindex）。
  if (isEncrypted(root)) {
    const byOwner = {};
    for (const rel of set) {
      if (String(rel).indexOf(PRIVATE_DIR + '/') !== 0) continue;
      const owner = String(rel).split('/')[1] || '';
      (byOwner[owner] = byOwner[owner] || []).push(rel);
    }
    for (const owner of Object.keys(byOwner)) {
      const key = getOwnerKeyFor(root, owner);
      if (!key) continue;
      withIndexLock(root, function () {
        let ownerIdx;
        try { ownerIdx = loadOwnerIndex(root, owner, key); } catch (e) { return; }
        let dirty = false;
        for (const e of ownerIdx) {
          if (set.has(e.file)) { bumpEntry(e); dirty = true; }
        }
        if (dirty) saveOwnerIndex(root, owner, key, ownerIdx);
      });
    }
  }
  // v0.17.0 B3：带 --year 的检索只碰命中年份的分片（命中条目必然来自这些分片），
  // 不传年份时行为与旧版一致（遍历全部 shards）。
  const filterYears = (options && Array.isArray(options.years)) ? options.years : [];
  const yearSet = filterYears.length ? new Set(filterYears) : null;
  const manifest = loadIndexManifest(root);
  if (manifest && Array.isArray(manifest.shards)) {
    withIndexLock(root, function () {
      for (const sh of manifest.shards) {
        if (!isSafeShardName(sh)) continue;
        if (yearSet && !yearSet.has(shardYear(sh))) continue;
        const sd = readIndexShard(root, sh);
        if (!sd) continue;
        let dirty = false;
        for (const e of sd.entries) {
          if (set.has(e.file)) { bumpEntry(e); dirty = true; }
        }
        if (dirty) writeIndexShard(root, sh, sd);
      }
    });
    return;
  }
  withIndexLock(root, function () {
    const idx = getIndex(root);
    let dirty = false;
    for (const e of idx) {
      if (set.has(e.file)) { bumpEntry(e); dirty = true; }
    }
    if (dirty) saveIndex(root, idx);
  });
}
function daysBetween(a, b) {
  const da = new Date(a);
  const db = new Date(b);
  if (isNaN(da.getTime()) || isNaN(db.getTime())) return 99999;
  return Math.round((db.getTime() - da.getTime()) / (24 * 60 * 60 * 1000));
}
function vitality(meta) {
  const conf = parseFloat(meta.confidence || 1.0);
  const acc = parseInt(meta.access_count || '0', 10) || 0;
  const last = meta.last_accessed || '';
  const accScore = Math.min(acc, 10) / 10;
  let recency = 0;
  if (last) { const d = daysBetween(last, today()); recency = Math.max(0, 1 - Math.floor(d / 30) * 0.2); }
  return 0.4 * conf + 0.3 * accScore + 0.3 * recency;
}
// importance 融合：confidence × (0.5 + recency) + updated 加分 + weight 乘子 + immutable 加分
function importanceScore(meta) {
  const conf = parseFloat(meta.confidence || 1.0);
  let ageDays = 999;
  if (meta.created) {
    const d = daysBetween(meta.created, today());
    if (!isNaN(d)) ageDays = d;
  }
  const recency = 1.0 / (1.0 + Math.max(ageDays, 0) / 180.0);
  let score = conf * (0.5 + recency);
  if (meta.updated && meta.created && meta.updated !== meta.created) score += 0.5;
  const w = parseFloat(meta.weight || 1.0); if (w > 0) score *= w;
  if (meta.immutable === 'true') score += 2.0;
  return score;
}
function loadGrants(root) {
  const fp = path.join(root, 'grants.json');
  try { return JSON.parse(fs.readFileSync(fp, 'utf8')) || {}; } catch (e) { return {}; }
}
function hasGrant(userAgent, ownerAgent) {
  if (!userAgent || !ownerAgent) return false;
  for (const root of memoryRoots()) {
    if (!fs.existsSync(root)) continue;
    const grants = loadGrants(root);
    const list = grants[userAgent];
    if (Array.isArray(list) && list.indexOf(ownerAgent) !== -1) return true;
  }
  return false;
}
// 三态读取判定：'read' | 'denied'
// selfAgent 为调用方显式声明的可信身份（CLI 参数 / stdio 参数 / HTTP 请求头）；--owner 仅供授权与展示，不得授予跨智能体私密读取。
function classifyRead(entry, agent, ownerFilter, unsafe, selfAgent) {
  if (entry.scope === 'public') return 'read';
  const owner = entry.owner || '';
  if (!owner) return 'read';
  const own = selfAgent || agent;
  if (own && owner === own) return 'read';
  if (unsafe || String(ownerFilter).toLowerCase() === 'user' || String(agent || '').toLowerCase() === 'user') return 'read';
  if (hasGrant(agent || selfAgent, owner)) return 'read';
  return 'denied';
}
// verify 写后回读：直查索引 + 权限判定 + 召回匹配性，不依赖 recall top-N 排序
// （v0.6.2 修复：泛化 subject 下新条目被挤出前 N 条导致误报「回读未命中」）
function verifyWrittenReadable(root, rel, subj, agent) {
  const entries = ensureIndex(root);
  let target = null;
  for (const e of entries) { if (e.file === rel) { target = e; break; } }
  if (!target) return false;
  if (classifyRead(target, agent, '', false, agent) !== 'read') return false;
  const q = String(subj || '').toLowerCase();
  const qtoks = tokenize(q);
  let score = 0;
  for (const tt of qtoks) { if (target.tokens && target.tokens[tt]) score += target.tokens[tt]; }
  if (score === 0) {
    const hay = ((target.subject || '') + ' ' + (target.statement || '') + ' ' + target.tags.join(' ')).toLowerCase();
    if (hay.indexOf(q) !== -1) score = 1;
  }
  return score > 0;
}

// ---- 命令 core（CLI 与 MCP 共用；返回 { error, exitCode, text }，不 process.exit）----
function isExistingStore(root) {
  return ['facts', 'private', 'keys', 'index.json'].some(function (name) {
    return fs.existsSync(path.join(root, name));
  });
}
function initCore(opts) {
  opts = opts || {};
  const root = opts.dir ? path.resolve(String(opts.dir)) : (opts.project ? projectRoot() : userRoot());
  const existing = isExistingStore(root);
  if (existing && opts.attach) {
    const mode = isEncrypted(root) ? '加密' : '明文';
    let text = '已接入现有记忆库（当前模式：' + mode + '）: ' + root;
    if (!isEncrypted(root)) text += '\n提示：当前为明文模式，私密内容未加密；如需启用加密，请运行 yotta-memory migrate（空明文库同样可用）。';
    return { error: false, text: text };
  }
  if (existing && opts.force) {
    return { error: true, text: '拒绝: --force 不能覆盖现有记忆库；已有记忆库的强制重建必须由完整备份与显式确认保护，当前版本不提供覆盖初始化路径。如只是接入，请使用 init --attach。' };
  }
  if (existing) {
    return { error: true, text: '拒绝: 目标已是现有记忆库: ' + root + '。如只是接入，请使用 init --attach；不要执行覆盖初始化。' };
  }
  const fresh = true;
  ensureInit(root);
  const wantEncrypt = opts.encrypt || (!opts.noEncrypt && fresh);
  if (wantEncrypt) {
    if (isEncrypted(root)) return { error: false, text: '已初始化记忆库（已启用加密）: ' + root };
    if (hasPlaintextPrivate(root)) return { error: true, text: '检测到明文私密区，请先 yotta-memory migrate 迁移到密文；新建空库可直接 init --encrypt。' };
    const password = String(opts.password || process.env.YOTTA_MEMORY_PASS || '');
    if (!password) return { error: true, text: '启用加密需要主口令：交互输入、--password-stdin（推荐）或 YOTTA_MEMORY_PASS 环境变量（自动化）。' };
    const r = initEncryptionCore(root, password, null);
    if (opts.recoveryKeyOut) {
      const outPath = path.resolve(String(opts.recoveryKeyOut));
      fs.mkdirSync(path.dirname(outPath), { recursive: true });
      fs.writeFileSync(outPath, r.rk.toString('base64') + '\n', { encoding: 'utf8', mode: 0o600 });
      return { error: false, text: '已初始化加密记忆库: ' + root + '\n[恢复钥匙] 已写入文件: ' + outPath + '（务必离线保存，仅此一次，泄露=可解全部私密；不要把钥匙粘贴到对话中）' };
    }
    return { error: false, text: '已初始化加密记忆库: ' + root + '\n[恢复钥匙]（务必离线保存，仅此一次，泄露=可解全部私密）: ' + r.rk.toString('base64') };
  }
  return { error: false, text: '已初始化记忆库: ' + root + (isEncrypted(root) ? '（已启用加密）' : '（明文；私密内容未加密，如需启用加密请运行 migrate）') };
}

function backupDestination(opts) {
  opts = opts || {};
  const configured = opts.dir || process.env.YOTTA_MEMORY_BACKUP_DIR || loadConfig().backup_dir || '';
  return configured ? path.resolve(String(configured)) : null;
}
function sameVolume(left, right) {
  return path.parse(path.resolve(left)).root.toLowerCase() === path.parse(path.resolve(right)).root.toLowerCase();
}
function platformPathApi(platform) {
  return platform === 'win32' ? path.win32 : path.posix;
}
function normalizeVolumeCandidate(candidate, platform) {
  const p = platformPathApi(platform);
  const value = String(candidate || '').trim();
  if (!value) return '';
  if (platform === 'win32') {
    const drive = /^([A-Za-z]):[\\/]*$/.exec(value);
    if (drive) return drive[1].toUpperCase() + ':\\';
  }
  return p.resolve(value);
}
function sameVolumeOnPlatform(left, right, platform, statFn) {
  if (platform === 'win32') {
    return path.win32.parse(left).root.toLowerCase() === path.win32.parse(right).root.toLowerCase();
  }
  try {
    return statFn(left).dev === statFn(right).dev;
  } catch (_) {
    return left === right;
  }
}
function defaultVolumeCandidates(platform) {
  if (platform === 'win32') {
    const out = [];
    for (let i = 65; i <= 90; i++) {
      const root = String.fromCharCode(i) + ':\\';
      if (fs.existsSync(root)) out.push(root);
    }
    return out;
  }
  try {
    const output = child_process.execFileSync('df', ['-Pk'], {
      encoding: 'utf8',
      timeout: 3000,
      stdio: ['ignore', 'pipe', 'ignore'],
    });
    const excluded = /^\/(proc|sys|dev|run|snap|boot)(\/|$)/;
    return output.split(/\r?\n/).slice(1).map(function (line) {
      const parts = line.trim().split(/\s+/);
      return parts.length >= 6 ? parts[parts.length - 1] : '';
    }).filter(function (mount) {
      return mount && mount.charAt(0) === '/' && !excluded.test(mount);
    });
  } catch (_) {
    return [];
  }
}
function formatBytes(bytes) {
  const value = Number(bytes) || 0;
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let n = value;
  let unit = 0;
  while (n >= 1024 && unit < units.length - 1) { n /= 1024; unit++; }
  return (unit === 0 ? Math.round(n) : n.toFixed(1)) + ' ' + units[unit];
}
function listBackupVolumesCore(opts) {
  opts = opts || {};
  const platform = opts.platform || process.platform;
  const p = platformPathApi(platform);
  const rootForStore = opts.root || userRoot();
  const storeRoot = normalizeVolumeCandidate(rootForStore, platform);
  const candidates = opts.candidates || defaultVolumeCandidates(platform);
  const existsFn = opts.existsFn || fs.existsSync;
  const statFn = opts.statFn || fs.statSync;
  const statfsFn = opts.statfsFn || fs.statfsSync;
  const accessFn = opts.accessFn || fs.accessSync;
  const volumes = [];
  const seen = new Set();
  for (const candidate of candidates) {
    const normalized = normalizeVolumeCandidate(candidate, platform);
    if (!normalized || seen.has(normalized)) continue;
    seen.add(normalized);
    try {
      if (!existsFn(normalized)) continue;
      const stat = statFn(normalized);
      if (!stat || !stat.isDirectory()) continue;
      accessFn(normalized, fs.constants.W_OK);
      if (sameVolumeOnPlatform(storeRoot, normalized, platform, statFn)) continue;
      const usage = statfsFn(normalized);
      const blockSize = Number(usage && usage.bsize) || 0;
      const availableBlocks = Number(usage && usage.bavail) || 0;
      const totalBlocks = Number(usage && usage.blocks) || 0;
      volumes.push({
        root: normalized,
        writable: true,
        sameVolume: false,
        free: blockSize * availableBlocks,
        total: blockSize * totalBlocks,
      });
    } catch (_) {
      // A mounted path that is not currently accessible is not a valid recommendation.
    }
  }
  volumes.sort(function (a, b) { return String(a.root).localeCompare(String(b.root)); });
  const lines = volumes.length
    ? ['可用的独立卷（排除记忆库所在卷 ' + storeRoot + '）:'].concat(volumes.map(function (v) {
      return '- ' + v.root + '  可用 ' + formatBytes(v.free);
    }))
    : ['未发现可写的独立卷（已排除记忆库所在卷 ' + storeRoot + '）；请接入另一块磁盘或独立分区后重试。'];
  return { error: false, volumes: volumes, text: lines.join('\n') };
}
function validBackupTime(value) {
  return /^([01]\d|2[0-3]):([0-5]\d)$/.test(String(value || ''));
}
function backupTimeParts(value) {
  const text = String(value || '');
  if (!validBackupTime(text)) throw new Error('备份时间格式无效: ' + text + '（应为 HH:MM）');
  const parts = text.split(':');
  return { hour: parseInt(parts[0], 10), minute: parseInt(parts[1], 10), text: text };
}
function xmlEscape(value) {
  return String(value === undefined || value === null ? '' : value).replace(/[&<>"']/g, function (ch) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' }[ch];
  });
}
function backupWindowsTaskXml(opts) {
  opts = opts || {};
  const time = backupTimeParts(opts.time || '03:30');
  const nodePath = opts.nodePath || process.execPath;
  const scriptPath = opts.scriptPath || runtimeManagedScript();
  const userId = opts.userId || '';
  const principal = userId
    ? '<Principal id="Author"><UserId>' + xmlEscape(userId) + '</UserId><LogonType>InteractiveToken</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal>'
    : '<Principal id="Author"><LogonType>InteractiveToken</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal>';
  const cmdPath = opts.cmdPath || process.env.ComSpec || 'cmd.exe';
  // v0.22.5: Electron 宿主（如 YottaCode shim）下 process.execPath 是 Electron 可执行文件，
  // 任务需经 cmd /c + ELECTRON_RUN_AS_NODE=1 包装，否则拉起的是桌面程序本体而非 Node。
  const action = lanElectronHost(opts)
    ? '<Actions Context="Author"><Exec><Command>' + xmlEscape(cmdPath) + '</Command><Arguments>/c "set "ELECTRON_RUN_AS_NODE=1" &amp;&amp; "' + xmlEscape(nodePath) + '" "' + xmlEscape(scriptPath) + '" backup ensure-daily"</Arguments></Exec></Actions>'
    : '<Actions Context="Author"><Exec><Command>' + xmlEscape(nodePath) + '</Command><Arguments>"' + xmlEscape(scriptPath) + '" backup ensure-daily</Arguments></Exec></Actions>';
  return [
    '<?xml version="1.0" encoding="UTF-16"?>',
    '<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">',
    '<RegistrationInfo><Description>Yotta Memory daily backup</Description></RegistrationInfo>',
    '<Triggers><CalendarTrigger><StartBoundary>2026-01-01T' + time.text + ':00</StartBoundary><Enabled>true</Enabled><ScheduleByDay><DaysInterval>1</DaysInterval></ScheduleByDay></CalendarTrigger></Triggers>',
    '<Principals>' + principal + '</Principals>',
    '<Settings>',
    '<MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>',
    '<DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>',
    '<StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>',
    '<AllowHardTerminate>true</AllowHardTerminate>',
    '<StartWhenAvailable>true</StartWhenAvailable>',
    '<RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>',
    '<IdleSettings><StopOnIdleEnd>false</StopOnIdleEnd><RestartOnIdle>false</RestartOnIdle></IdleSettings>',
    '<Enabled>true</Enabled>',
    '<Hidden>false</Hidden>',
    '<RunOnlyIfIdle>false</RunOnlyIfIdle>',
    '<WakeToRun>false</WakeToRun>',
    '<ExecutionTimeLimit>PT2H</ExecutionTimeLimit>',
    '<Priority>7</Priority>',
    '</Settings>',
    action,
    '</Task>',
  ].join('\r\n');
}
function backupSystemdServiceContent(opts) {
  opts = opts || {};
  const nodePath = opts.nodePath || process.execPath;
  const scriptPath = opts.scriptPath || runtimeManagedScript();
  const lines = [
    '[Unit]',
    'Description=Yotta Memory daily backup',
    '',
    '[Service]',
    'Type=oneshot',
  ];
  if (lanElectronHost(opts)) lines.push('Environment=ELECTRON_RUN_AS_NODE=1');
  lines.push(
    'ExecStart=' + systemdEscapeArg(nodePath) + ' ' + systemdEscapeArg(scriptPath) + ' backup ensure-daily',
    'Nice=10',
    '',
  );
  return lines.join('\n');
}
function backupSystemdTimerContent(opts) {
  opts = opts || {};
  const time = backupTimeParts(opts.time || '03:30');
  return [
    '[Unit]',
    'Description=Yotta Memory daily backup timer',
    '',
    '[Timer]',
    'OnCalendar=*-*-* ' + time.text + ':00',
    'Persistent=true',
    'RandomizedDelaySec=300',
    '',
    '[Install]',
    'WantedBy=timers.target',
    '',
  ].join('\n');
}
function backupCronLine(opts) {
  opts = opts || {};
  const time = backupTimeParts(opts.time || '03:30');
  const nodePath = opts.nodePath || process.execPath;
  const scriptPath = opts.scriptPath || runtimeManagedScript();
  const logPath = opts.logPath || '';
  const redirect = logPath ? ' >> ' + shQuote(logPath) + ' 2>&1' : '';
  const env = lanElectronHost(opts) ? 'ELECTRON_RUN_AS_NODE=1 ' : '';
  return time.minute + ' ' + time.hour + ' * * * ' + env + shQuote(nodePath) + ' ' + shQuote(scriptPath) + ' backup ensure-daily' + redirect + ' ' + BACKUP_CRON_MARKER;
}
function backupLaunchdPlist(opts) {
  opts = opts || {};
  const time = backupTimeParts(opts.time || '03:30');
  const nodePath = opts.nodePath || process.execPath;
  const scriptPath = opts.scriptPath || runtimeManagedScript();
  const logPath = opts.logPath || '';
  const lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">',
    '<plist version="1.0"><dict>',
  ];
  if (lanElectronHost(opts)) {
    lines.push('<key>EnvironmentVariables</key><dict><key>ELECTRON_RUN_AS_NODE</key><string>1</string></dict>');
  }
  lines.push(
    '<key>Label</key><string>' + BACKUP_LAUNCHD_LABEL + '</string>',
    '<key>ProgramArguments</key><array>',
    '<string>' + xmlEscape(nodePath) + '</string>',
    '<string>' + xmlEscape(scriptPath) + '</string>',
    '<string>backup</string>',
    '<string>ensure-daily</string>',
    '</array>',
    '<key>StartCalendarInterval</key><dict>',
    '<key>Hour</key><integer>' + time.hour + '</integer>',
    '<key>Minute</key><integer>' + time.minute + '</integer>',
    '</dict>',
  );
  if (logPath) {
    lines.push('<key>StandardOutPath</key><string>' + xmlEscape(logPath) + '</string>');
    lines.push('<key>StandardErrorPath</key><string>' + xmlEscape(logPath) + '</string>');
  }
  lines.push('</dict></plist>');
  return lines.join('\n');
}
function schedulerExec(opts, command, args, input) {
  if (opts && typeof opts.execFileFn === 'function') return opts.execFileFn(command, args, { input: input });
  return child_process.execFileSync(command, args, {
    encoding: 'utf8',
    timeout: 15000,
    input: input,
    stdio: [input === undefined ? 'ignore' : 'pipe', 'pipe', 'pipe'],
  });
}
function schedulerTry(opts, command, args, input) {
  try {
    return { ok: true, stdout: String(schedulerExec(opts, command, args, input) || '') };
  } catch (error) {
    return {
      ok: false,
      stdout: String((error && error.stdout) || ''),
      error: String((error && error.message) || error),
    };
  }
}
function backupScheduleEnableCore(opts) {
  opts = opts || {};
  const platform = opts.platform || process.platform;
  const time = opts.time || '03:30';
  try { backupTimeParts(time); } catch (error) { return { error: true, text: error.message }; }
  const nodePath = opts.nodePath || process.execPath;
  const scriptPath = opts.scriptPath || runtimeManagedScript();
  try {
    if (platform === 'win32') {
      const userId = opts.userId || (process.env.USERDOMAIN && process.env.USERNAME ? process.env.USERDOMAIN + '\\' + process.env.USERNAME : '');
      const taskName = opts.taskName || BACKUP_TASK_NAME;
      const xmlPath = opts.xmlPath || path.join(os.tmpdir(), taskName + '.xml');
      fs.writeFileSync(xmlPath, '\ufeff' + backupWindowsTaskXml({ time: time, nodePath: nodePath, scriptPath: scriptPath, userId: userId, electronHost: opts.electronHost }), 'utf16le');
      schedulerExec(opts, 'schtasks', ['/create', '/tn', taskName, '/xml', xmlPath, '/f']);
      return { error: false, scheduler: 'windows-task', taskName: taskName, text: '已注册 Windows 每日备份任务: ' + taskName };
    }
    if (platform === 'linux') {
      const unitDir = opts.unitDir || path.join(os.homedir(), '.config', 'systemd', 'user');
      const servicePath = path.join(unitDir, BACKUP_SYSTEMD_SERVICE);
      const timerPath = path.join(unitDir, BACKUP_SYSTEMD_TIMER);
      fs.mkdirSync(unitDir, { recursive: true });
      fs.writeFileSync(servicePath, backupSystemdServiceContent({ nodePath: nodePath, scriptPath: scriptPath, electronHost: opts.electronHost }), 'utf8');
      fs.writeFileSync(timerPath, backupSystemdTimerContent({ time: time }), 'utf8');
      const reload = schedulerTry(opts, 'systemctl', ['--user', 'daemon-reload']);
      const enable = reload.ok ? schedulerTry(opts, 'systemctl', ['--user', 'enable', '--now', BACKUP_SYSTEMD_TIMER]) : reload;
      if (enable.ok) {
        return { error: false, scheduler: 'linux-systemd', unit: BACKUP_SYSTEMD_TIMER, text: '已注册 systemd 用户定时器: ' + BACKUP_SYSTEMD_TIMER };
      }
      const logPath = opts.logPath || path.join(os.homedir(), '.yottamemory', 'backup.log');
      const line = backupCronLine({ time: time, nodePath: nodePath, scriptPath: scriptPath, logPath: logPath, electronHost: opts.electronHost });
      const current = schedulerTry(opts, 'crontab', ['-l']);
      const kept = current.stdout.split(/\r?\n/).filter(function (item) {
        return item && item.indexOf(BACKUP_CRON_MARKER) === -1;
      });
      kept.push(line);
      schedulerExec(opts, 'crontab', ['-'], kept.join('\n') + '\n');
      return {
        error: false,
        scheduler: 'linux-cron',
        unit: 'crontab',
        warning: 'systemd 用户定时器不可用，已降级用户 crontab: ' + enable.error,
        text: '已注册用户 crontab 每日备份；systemd 不可用。',
      };
    }
    if (platform === 'darwin') {
      const dir = opts.launchAgentDir || path.join(os.homedir(), 'Library', 'LaunchAgents');
      const plistPath = path.join(dir, BACKUP_LAUNCHD_LABEL + '.plist');
      fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(plistPath, backupLaunchdPlist({
        time: time,
        nodePath: nodePath,
        scriptPath: scriptPath,
        logPath: opts.logPath || path.join(os.homedir(), 'Library', 'Logs', 'yotta-memory-backup.log'),
        electronHost: opts.electronHost,
      }), 'utf8');
      const uid = typeof process.getuid === 'function' ? process.getuid() : '';
      const bootstrap = schedulerTry(opts, 'launchctl', ['bootstrap', 'gui/' + uid, plistPath]);
      if (!bootstrap.ok) schedulerTry(opts, 'launchctl', ['load', '-w', plistPath]);
      return { error: false, scheduler: 'macos-launchd', plist: plistPath, text: '已注册 macOS LaunchAgent 每日备份。' };
    }
  } catch (error) {
    return { error: true, text: '注册自动备份调度失败: ' + error.message };
  }
  return { error: true, text: '当前平台暂不支持自动备份调度: ' + platform };
}
function backupScheduleDisableCore(opts) {
  opts = opts || {};
  const platform = opts.platform || process.platform;
  try {
    if (platform === 'win32') {
      const taskName = opts.taskName || BACKUP_TASK_NAME;
      const result = schedulerTry(opts, 'schtasks', ['/delete', '/tn', taskName, '/f']);
      if (!result.ok && !/cannot find|找不到|不存在/i.test(result.error)) return { error: true, text: result.error };
      return { error: false, scheduler: 'windows-task', text: result.ok ? '已移除 Windows 备份任务。' : 'Windows 备份任务未注册。' };
    }
    if (platform === 'linux') {
      schedulerTry(opts, 'systemctl', ['--user', 'disable', '--now', BACKUP_SYSTEMD_TIMER]);
      const unitDir = opts.unitDir || path.join(os.homedir(), '.config', 'systemd', 'user');
      for (const name of [BACKUP_SYSTEMD_SERVICE, BACKUP_SYSTEMD_TIMER]) {
        try { fs.unlinkSync(path.join(unitDir, name)); } catch (_) {}
      }
      const current = schedulerTry(opts, 'crontab', ['-l']);
      const kept = current.stdout.split(/\r?\n/).filter(function (item) {
        return item && item.indexOf(BACKUP_CRON_MARKER) === -1;
      });
      schedulerTry(opts, 'crontab', ['-'], kept.join('\n') + (kept.length ? '\n' : ''));
      return { error: false, scheduler: 'linux', text: '已移除 systemd 定时器与备份 cron 行。' };
    }
    if (platform === 'darwin') {
      const dir = opts.launchAgentDir || path.join(os.homedir(), 'Library', 'LaunchAgents');
      const plistPath = path.join(dir, BACKUP_LAUNCHD_LABEL + '.plist');
      const uid = typeof process.getuid === 'function' ? process.getuid() : '';
      schedulerTry(opts, 'launchctl', ['bootout', 'gui/' + uid, plistPath]);
      try { fs.unlinkSync(plistPath); } catch (_) {}
      return { error: false, scheduler: 'macos-launchd', text: '已移除 macOS LaunchAgent 备份。' };
    }
  } catch (error) {
    return { error: true, text: '移除自动备份调度失败: ' + error.message };
  }
  return { error: true, text: '当前平台暂不支持自动备份调度: ' + platform };
}
function backupScheduleStatusCore(opts) {
  opts = opts || {};
  const platform = opts.platform || process.platform;
  if (platform === 'win32') {
    const taskName = opts.taskName || BACKUP_TASK_NAME;
    const result = schedulerTry(opts, 'schtasks', ['/query', '/tn', taskName, '/fo', 'LIST']);
    return { error: false, registered: result.ok, scheduler: 'windows-task', text: result.ok ? 'Windows 备份任务已注册。' : 'Windows 备份任务未注册。' };
  }
  if (platform === 'linux') {
    const unitDir = opts.unitDir || path.join(os.homedir(), '.config', 'systemd', 'user');
    const timer = fs.existsSync(path.join(unitDir, BACKUP_SYSTEMD_TIMER));
    let cron = false;
    try {
      cron = schedulerTry(opts, 'crontab', ['-l']).stdout.indexOf(BACKUP_CRON_MARKER) !== -1;
    } catch (_) {}
    return { error: false, registered: timer || cron, scheduler: timer ? 'linux-systemd' : (cron ? 'linux-cron' : ''), text: timer || cron ? 'Linux 备份定时器已注册。' : 'Linux 备份定时器未注册。' };
  }
  if (platform === 'darwin') {
    const dir = opts.launchAgentDir || path.join(os.homedir(), 'Library', 'LaunchAgents');
    const registered = fs.existsSync(path.join(dir, BACKUP_LAUNCHD_LABEL + '.plist'));
    return { error: false, registered: registered, scheduler: 'macos-launchd', text: registered ? 'macOS 备份 LaunchAgent 已注册。' : 'macOS 备份 LaunchAgent 未注册。' };
  }
  return { error: false, registered: false, scheduler: '', text: '当前平台不支持自动备份调度: ' + platform };
}
function backupFallbackCommand() {
  return { command: process.execPath, args: [runtimeManagedScript(), 'backup', 'ensure-daily'] };
}
function startBackupFallback() {
  const cfg = loadConfig();
  if (!cfg.backup_enabled) return;
  const launch = function () {
    try {
      const spec = backupFallbackCommand();
      const child = child_process.spawn(spec.command, spec.args, {
        detached: true,
        stdio: 'ignore',
        windowsHide: true,
      });
      child.unref();
    } catch (error) {
      console.error('备份补跑启动失败: ' + error.message);
    }
  };
  const initial = setTimeout(launch, 10000);
  if (initial.unref) initial.unref();
  const interval = setInterval(launch, 6 * 60 * 60 * 1000);
  if (interval.unref) interval.unref();
}
function backupSetupCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.root || userRoot());
  if (!isExistingStore(root)) return { error: true, text: '记忆库不存在或未初始化: ' + root };
  const cfg = loadConfig();
  const nowIso = new Date().toISOString();
  if (opts.manual) {
    cfg.backup_enabled = false;
    cfg.backup_schedule = 'manual';
    cfg.backup_setup_choice = 'manual';
    cfg.backup_setup_at = nowIso;
    delete cfg.backup_dir;
    saveConfig(cfg);
    return {
      error: false,
      configured: false,
      manual: true,
      text: '已记录：用户选择手动备份。未注册自动备份，也不会在会话开工时反复提示。',
    };
  }
  if (!opts.dir) return { error: true, text: '缺少备份目录 --dir <目录>。请先运行 backup volumes，只从实际枚举结果中选择。' };
  const dir = path.resolve(String(opts.dir));
  const same = opts.sameVolumeFn ? !!opts.sameVolumeFn(root, dir) : sameVolume(root, dir);
  if (same) return { error: true, text: '拒绝: 备份目录与记忆库在同一卷，请选择实际存在的独立卷。' };
  const time = String(opts.time || '03:30');
  if (!validBackupTime(time)) return { error: true, text: '备份时间格式无效: ' + time + '（应为 HH:MM，例如 03:30）' };
  try {
    fs.mkdirSync(dir, { recursive: true });
    fs.accessSync(dir, fs.constants.W_OK);
  } catch (error) {
    return { error: true, text: '备份目录不可写: ' + dir + '（' + error.message + '）' };
  }
  const created = backupCreateCore({
    root: root,
    dir: dir,
    allowSameVolume: !!opts.allowSameVolume,
  });
  if (created.error) return created;
  cfg.backup_dir = dir;
  cfg.backup_enabled = true;
  cfg.backup_schedule = 'daily';
  cfg.backup_time = time;
  cfg.backup_max_age_hours = opts.maxAgeHours !== undefined ? opts.maxAgeHours : 36;
  cfg.backup_setup_choice = 'daily';
  cfg.backup_setup_at = nowIso;
  cfg.backup_last_success = created.manifest.created;
  cfg.backup_last_backup_id = created.id;
  delete cfg.backup_last_error;
  saveConfig(cfg);
  let schedule = null;
  if (!opts.skipSchedule && typeof backupScheduleEnableCore === 'function') {
    schedule = backupScheduleEnableCore({ dir: dir, time: time, root: root });
    if (schedule && schedule.error) {
      cfg.backup_scheduler_error = schedule.text;
      delete cfg.backup_scheduler;
    } else if (schedule) {
      cfg.backup_scheduler = schedule.scheduler || '';
      delete cfg.backup_scheduler_error;
    }
    saveConfig(cfg);
  }
  return {
    error: false,
    configured: true,
    id: created.id,
    dir: dir,
    time: time,
    schedule: schedule,
    text: '已启用每日自动备份: ' + dir + '（每天 ' + time + '）\n首份备份: ' + created.id
      + (schedule && schedule.error ? '\n[警告] ' + schedule.text + '；serve 补跑仍会在启动后检查。' : ''),
  };
}
const BACKUP_FUTURE_TOLERANCE_MS = 15 * 60 * 1000;
function backupCreatedTs(value) {
  const ts = Date.parse(String(value || ''));
  return Number.isFinite(ts) ? ts : null;
}
function compareBackupCreatedDesc(a, b) {
  const at = backupCreatedTs(a && a.created);
  const bt = backupCreatedTs(b && b.created);
  if (at !== null && bt !== null && at !== bt) return bt - at;
  if (at !== null && bt === null) return -1;
  if (at === null && bt !== null) return 1;
  return String((b && b.id) || '').localeCompare(String((a && a.id) || ''));
}
function selectLatestValidBackup(backups, nowMs) {
  const now = Number.isFinite(nowMs) ? nowMs : Date.now();
  const valid = [];
  const anomalies = [];
  for (const backup of backups || []) {
    if (!backup || !backup.manifest) {
      anomalies.push({ id: backup && backup.id || '', type: 'manifest_missing', created: backup && backup.created || '' });
      continue;
    }
    if (!Array.isArray(backup.manifest.files)) {
      anomalies.push({ id: backup.id, type: 'manifest_incomplete', created: backup.created || '' });
      continue;
    }
    const createdTs = backupCreatedTs(backup.created);
    if (createdTs === null) {
      anomalies.push({ id: backup.id, type: 'invalid_created', created: backup.created || '' });
      continue;
    }
    if (createdTs > now + BACKUP_FUTURE_TOLERANCE_MS) {
      anomalies.push({ id: backup.id, type: 'future_timestamp', created: backup.created || '' });
      continue;
    }
    valid.push(Object.assign({}, backup, { createdTs: createdTs }));
  }
  valid.sort(compareBackupCreatedDesc);
  return { latestValid: valid[0] || null, anomalies: anomalies };
}
function backupAnomalyLabel(type) {
  if (type === 'future_timestamp') return '未来时间';
  if (type === 'manifest_missing') return 'manifest 缺失';
  if (type === 'manifest_incomplete') return 'manifest 不完整';
  if (type === 'invalid_created') return 'created 无效';
  return type;
}
function backupStatusCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.root || userRoot());
  const cfg = loadConfig();
  const configuredDir = opts.dir || opts.backupDir || cfg.backup_dir;
  const dir = configuredDir ? path.resolve(String(configuredDir)) : '';
  const maxAge = Number(cfg.backup_max_age_hours) || 36;
  if (!dir) {
    const manual = cfg.backup_setup_choice === 'manual';
    return {
      error: false,
      configured: false,
      enabled: false,
      healthy: false,
      manual: manual,
      text: manual
        ? '备份状态: 手动模式（未配置自动备份）'
        : '备份状态: 未配置\n请运行 backup volumes，只从实际枚举结果中选择独立卷，并由用户确认后再运行 backup setup。',
    };
  }
  const listed = backupListCore({ dir: dir });
  const now = opts.now ? new Date(opts.now).getTime() : Date.now();
  const selection = selectLatestValidBackup(listed.backups, now);
  const latest = selection.latestValid;
  const ageHours = latest ? (now - latest.createdTs) / 3600000 : null;
  const fresh = ageHours !== null && ageHours <= maxAge;
  const same = opts.sameVolumeFn ? !!opts.sameVolumeFn(root, dir) : sameVolume(root, dir);
  const independent = !same;
  const healthy = !!latest && fresh && independent && !cfg.backup_last_error && !cfg.backup_scheduler_error;
  const configLastSuccess = cfg.backup_last_success || null;
  const effectiveLastSuccess = latest ? latest.created : configLastSuccess;
  const source = latest ? 'latest_valid' : (configLastSuccess ? 'config' : 'none');
  const anomalyLines = selection.anomalies.map(function (item) {
    return item.id + '（' + backupAnomalyLabel(item.type) + (item.created ? ' / ' + item.created : '') + '）';
  });
  const lines = [
    '备份状态: ' + (cfg.backup_enabled ? '已启用' : '已关闭'),
    '- 备份目录: ' + dir,
    '- 独立卷: ' + (independent ? '是' : '否（不可作为可靠备份）'),
    '- 计划: ' + (cfg.backup_schedule || 'manual') + (cfg.backup_time ? ' ' + cfg.backup_time : ''),
    '- 调度器: ' + (cfg.backup_scheduler || '(未注册)'),
    '- 调度异常: ' + (cfg.backup_scheduler_error || '(无)'),
    '- 配置缓存上次成功: ' + (configLastSuccess || '(无)'),
    '- 有效备份: ' + (latest ? latest.id + ' / ' + latest.created : '(无)'),
    '- 有效上次成功: ' + (effectiveLastSuccess || '(无)'),
    '- 来源: ' + source,
    '- 备份年龄: ' + (ageHours === null ? '(无可用备份)' : ageHours.toFixed(1) + ' 小时'),
    '- 异常备份: ' + (anomalyLines.length ? anomalyLines.join('；') : '(无)'),
    '- 最近失败: ' + (cfg.backup_last_error || '(无)'),
    '- 健康: ' + (healthy ? '正常' : '异常'),
  ];
  return {
    error: false,
    configured: true,
    enabled: !!cfg.backup_enabled,
    healthy: healthy,
    independent: independent,
    latest: latest,
    latest_valid: latest,
    config_last_success: configLastSuccess,
    effective_last_success: effectiveLastSuccess,
    source: source,
    anomalies: selection.anomalies,
    ageHours: ageHours,
    text: lines.join('\n'),
  };
}
function localDateKey(value) {
  const d = value instanceof Date ? value : new Date(value);
  const p = (n) => String(n).padStart(2, '0');
  return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
}
function latestBackupByCreated(backups) {
  return (backups || []).slice().sort(compareBackupCreatedDesc)[0] || null;
}
function acquireBackupLock(lockPath, now, staleHours) {
  const nowMs = now instanceof Date ? now.getTime() : new Date(now).getTime();
  const maxAgeMs = (staleHours || 6) * 3600000;
  try {
    fs.mkdirSync(path.dirname(lockPath), { recursive: true });
    fs.writeFileSync(lockPath, JSON.stringify({
      pid: process.pid,
      created: new Date(nowMs).toISOString(),
    }), { encoding: 'utf8', flag: 'wx' });
    return { acquired: true };
  } catch (error) {
    if (error.code !== 'EEXIST') return { acquired: false, error: error };
    try {
      const stat = fs.statSync(lockPath);
      if (nowMs - stat.mtimeMs > maxAgeMs) {
        fs.unlinkSync(lockPath);
        return acquireBackupLock(lockPath, now, staleHours);
      }
    } catch (_) {
      try { fs.unlinkSync(lockPath); } catch (__) {}
      return acquireBackupLock(lockPath, now, staleHours);
    }
    return { acquired: false, fresh: true };
  }
}
function releaseBackupLock(lockPath) {
  try { fs.unlinkSync(lockPath); } catch (_) {}
}
function backupEnsureDailyCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.root || userRoot());
  const cfg = loadConfig();
  const now = opts.now ? new Date(opts.now) : new Date();
  const nowIso = now.toISOString();
  if (!cfg.backup_enabled || cfg.backup_schedule === 'manual') {
    return { error: false, created: false, skipped: true, reason: 'disabled', text: '自动备份未启用；跳过 ensure-daily。' };
  }
  const dir = cfg.backup_dir ? path.resolve(String(cfg.backup_dir)) : '';
  if (!dir) {
    const text = '自动备份已启用但未配置 backup_dir；拒绝执行。';
    cfg.backup_last_attempt = nowIso;
    cfg.backup_last_error = text;
    saveConfig(cfg);
    return { error: true, created: false, skipped: false, text: text };
  }
  const same = opts.sameVolumeFn ? !!opts.sameVolumeFn(root, dir) : sameVolume(root, dir);
  if (same) {
    const text = '拒绝: 备份目录与记忆库在同一卷，不执行每日备份。';
    cfg.backup_last_attempt = nowIso;
    cfg.backup_last_error = text;
    saveConfig(cfg);
    return { error: true, created: false, skipped: false, text: text };
  }
  const lockPath = opts.lockPath || path.join(path.dirname(configPath()), 'backup.lock');
  const lock = acquireBackupLock(lockPath, now, opts.staleHours);
  if (!lock.acquired) {
    if (lock.error) {
      const text = '备份锁创建失败: ' + lock.error.message;
      cfg.backup_last_attempt = nowIso;
      cfg.backup_last_error = text;
      saveConfig(cfg);
      return { error: true, created: false, skipped: false, text: text };
    }
    return { error: false, created: false, skipped: true, reason: 'already-running', text: '已有备份任务在运行；跳过本次 ensure-daily。' };
  }
  try {
    const listed = backupListCore({ dir: dir });
    if (listed.error) throw new Error(listed.text);
    const todayKey = localDateKey(now);
    const latest = selectLatestValidBackup(listed.backups, now.getTime()).latestValid;
    if (latest && latest.created && localDateKey(latest.created) === todayKey) {
      cfg.backup_last_check = nowIso;
      cfg.backup_last_success = latest.created;
      cfg.backup_last_backup_id = latest.id;
      delete cfg.backup_last_error;
      saveConfig(cfg);
      return { error: false, created: false, skipped: true, reason: 'already-backed-up', id: latest.id, text: '今天已有备份 ' + latest.id + '；跳过。' };
    }
    const created = backupCreateCore({
      root: root,
      dir: dir,
      now: nowIso,
      allowSameVolume: !!opts.allowSameVolume,
    });
    if (created.error) throw new Error(created.text);
    cfg.backup_last_attempt = nowIso;
    cfg.backup_last_check = nowIso;
    cfg.backup_last_success = created.manifest.created;
    cfg.backup_last_backup_id = created.id;
    delete cfg.backup_last_error;
    saveConfig(cfg);
    return { error: false, created: true, skipped: false, id: created.id, path: created.path, text: '每日备份完成: ' + created.id };
  } catch (error) {
    cfg.backup_last_attempt = nowIso;
    cfg.backup_last_check = nowIso;
    cfg.backup_last_error = error.message;
    saveConfig(cfg);
    return { error: true, created: false, skipped: false, text: '每日备份失败: ' + error.message };
  } finally {
    releaseBackupLock(lockPath);
  }
}
function backupHealthCore(opts) {
  opts = opts || {};
  const cfg = loadConfig();
  const configuredDir = opts.dir || opts.backupDir || cfg.backup_dir;
  if (!configuredDir && cfg.backup_setup_choice !== 'manual') {
    return {
      level: 'warning',
      needsSetup: true,
      text: '尚未配置独立盘备份。AI 应先运行 yotta-memory backup volumes，只展示当前实际存在的可写异卷；由用户确认目录后，再运行 backup setup 启用每日自动备份。',
    };
  }
  if (!configuredDir && cfg.backup_setup_choice === 'manual') return { level: 'none', needsSetup: false, text: '' };
  const status = backupStatusCore(opts);
  const maxAge = Number(cfg.backup_max_age_hours) || 36;
  if (cfg.backup_last_error) return { level: 'warning', needsSetup: false, text: '最近一次备份失败: ' + cfg.backup_last_error };
  if (cfg.backup_scheduler_error) return { level: 'warning', needsSetup: false, text: '每日备份调度注册异常: ' + cfg.backup_scheduler_error };
  if (!status.latest_valid) {
    const anomalies = (status.anomalies || []).map(function (item) { return item.id + '（' + item.type + '）'; });
    return {
      level: 'warning',
      needsSetup: true,
      text: '自动备份已启用，但没有可用备份。' + (anomalies.length ? '检测到异常备份: ' + anomalies.join('；') + '。' : '请检查 backup 目录与调度器。'),
    };
  }
  if (status.ageHours !== null && status.ageHours > maxAge) {
    return { level: 'warning', needsSetup: false, text: '最近备份已过期（' + status.ageHours.toFixed(1) + ' 小时，超过 ' + maxAge + ' 小时）；请检查备份盘与每日调度。' };
  }
  return { level: 'none', needsSetup: false, text: '' };
}
// ---- v0.16.0 M3: runtime drift diagnosis ----
function runtimePathList(value) {
  const pattern = path.delimiter === ':' ? /[;:\n]/ : /[;\n]/;
  return String(value || '').split(pattern).map(function (item) { return item.trim(); }).filter(Boolean);
}
function runtimeVersionFromDir(dir) {
  let current = path.resolve(String(dir || ''));
  for (let i = 0; i < 8; i++) {
    const pkgPath = path.join(current, 'package.json');
    if (fs.existsSync(pkgPath)) {
      try {
        const version = String(JSON.parse(fs.readFileSync(pkgPath, 'utf8')).version || '').trim();
        if (version) return version;
      } catch (e) {}
    }
    const skillPath = path.join(current, 'SKILL.md');
    if (fs.existsSync(skillPath)) {
      try {
        const text = fs.readFileSync(skillPath, 'utf8');
        const match = text.match(/^---\s*\n([\s\S]*?)\n---/);
        if (match) {
          const versionLine = match[1].split(/\r?\n/).find(function (line) { return /^version\s*:/.test(line); });
          if (versionLine) {
            const version = versionLine.slice(versionLine.indexOf(':') + 1).trim().replace(/^["']|["']$/g, '');
            if (version) return version;
          }
        }
      } catch (e) {}
    }
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }
  return '';
}
function runtimeVersionFromPath(target) {
  const value = String(target || '').trim();
  if (!value) return '';
  const normalized = value.replace(/\\/g, '/');
  const versionMatch = normalized.match(/\/versions\/([^/]+)\/bin\/yotta-memory\.js$/i);
  if (versionMatch) return versionMatch[1];
  const abs = path.resolve(value);
  if (fs.existsSync(abs) && fs.statSync(abs).isDirectory()) return runtimeVersionFromDir(abs);
  const base = path.basename(abs).toLowerCase();
  const dir = path.dirname(abs);
  return runtimeVersionFromDir(base === 'yotta-memory.js' ? path.dirname(dir) : dir);
}
function runtimeExtractLauncherPaths(text) {
  const found = new Set();
  const add = function (value) {
    const raw = String(value || '').trim().replace(/^['"]|['"]$/g, '');
    if (!raw) return;
    const parts = splitCommandArgv(raw);
    for (const part of parts) {
      const token = part.replace(/^['"]|['"]$/g, '');
      if (/yotta-memory\.js$/i.test(token.replace(/[;,]$/, ''))) found.add(token.replace(/[;,]$/, ''));
    }
  };
  const parsed = [];
  try {
    const value = JSON.parse(String(text || ''));
    const walk = function (node) {
      if (typeof node === 'string') parsed.push(node);
      else if (Array.isArray(node)) node.forEach(walk);
      else if (node && typeof node === 'object') Object.keys(node).forEach(function (key) { walk(node[key]); });
    };
    walk(value);
  } catch (e) {}
  for (const value of parsed) if (/yotta-memory\.js/i.test(value)) add(value);
  const raw = String(text || '').replace(/\\\\/g, '\\');
  const patterns = [
    /[A-Za-z]:[\\/][^"'\r\n|;]+?yotta-memory\.js/gi,
    /(?:\.{0,2}[\\/])?[^"'\s|;]+?yotta-memory\.js/gi,
  ];
  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(raw)) !== null) add(match[0]);
  }
  return Array.from(found);
}
function runtimeConfigIdentityMode(text) {
  const raw = String(text || '');
  if (/YOTTA_AGENT_ID|YOTTA_MEMORY_AGENT_KEY|YOTTA_MEMORY_TRUST_ENV_AGENT/.test(raw)) return 'legacy-env';
  if (/--agent-id/.test(raw) && /--agent-key-file/.test(raw)) return 'stdio-args';
  if (/X-Agent-Id|Authorization/i.test(raw)) return 'headers';
  return 'unknown';
}
function runtimeDiscoverProcesses() {
  try {
    if (process.platform === 'win32') {
      const script = "$p=Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*yotta-memory*' }; if ($p) { $p | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress }";
      const result = child_process.spawnSync('powershell.exe', ['-NoProfile', '-Command', script], {
        encoding: 'utf8',
        timeout: 15000,
        windowsHide: true,
      });
      if (result.status !== 0 || !String(result.stdout || '').trim()) return [];
      const parsed = JSON.parse(String(result.stdout).trim());
      const rows = Array.isArray(parsed) ? parsed : [parsed];
      return rows.map(function (row) {
        return { pid: row.ProcessId, commandLine: row.CommandLine || '' };
      });
    }
    const result = child_process.spawnSync('ps', ['-eo', 'pid=,args='], { encoding: 'utf8', timeout: 10000 });
    if (result.status !== 0) return [];
    return String(result.stdout || '').split(/\r?\n/).filter(Boolean).map(function (line) {
      const match = line.trim().match(/^(\d+)\s+(.*)$/);
      return match ? { pid: parseInt(match[1], 10), commandLine: match[2] } : null;
    }).filter(Boolean);
  } catch (e) {
    return [];
  }
}
function runtimeDiscoverSkillDirs() {
  const explicit = runtimePathList(process.env.YOTTA_MEMORY_SKILL_DIRS);
  if (explicit.length) return explicit;
  const candidates = [];
  const add = function (base) {
    if (!base) return;
    candidates.push(path.join(base, 'skills', 'yotta-memory'));
    candidates.push(path.join(base, 'yotta-memory'));
  };
  add(process.env.CODEX_HOME);
  if (process.env.XDG_CONFIG_HOME) candidates.push(path.join(process.env.XDG_CONFIG_HOME, 'opencode', 'skills', 'yotta-memory'));
  add(process.env.HERMES_HOME);
  add(path.join(os.homedir(), '.codex'));
  candidates.push(path.join(os.homedir(), '.config', 'opencode', 'skills', 'yotta-memory'));
  return Array.from(new Set(candidates)).filter(function (dir) { return fs.existsSync(dir); });
}
function runtimeDoctorCore(opts) {
  opts = opts || {};
  const drifts = [];
  const warnings = [];
  const mcpConfigPaths = opts.mcpConfigPaths !== undefined
    ? opts.mcpConfigPaths
    : runtimePathList(process.env.YOTTA_MEMORY_MCP_CONFIGS);
  const skillDirs = opts.skillDirs !== undefined ? opts.skillDirs : runtimeDiscoverSkillDirs();
  const processes = opts.processes !== undefined ? opts.processes : runtimeDiscoverProcesses();
  const manifest = readRuntimeManifest();
  const currentDir = runtimeCurrentDir();
  const currentBin = runtimeCurrentBin();
  const manifestVersion = manifest && manifest.current ? String(manifest.current) : '';
  const installedCurrentVersion = fs.existsSync(path.join(currentDir, 'package.json'))
    ? runtimeVersionFromDir(currentDir)
    : '';

  const checks = {
    cli: { path: runtimeExecutionPath(), version: VERSION },
    current: {
      path: currentDir,
      version: manifestVersion || installedCurrentVersion || '',
      installedVersion: installedCurrentVersion,
      manifestVersion: manifestVersion,
    },
    runtimeRoot: runtimeRoot(),
    mcpConfigs: [],
    runningServers: [],
    skillCopies: [],
    identityModes: [],
    drifts: drifts,
  };

  if (!manifest || !manifest.current) {
    drifts.push({
      kind: 'current-runtime',
      source: runtimeManifestPath(),
      actual: 'missing',
      expected: VERSION,
      fix: 'yotta-memory runtime install --from-current',
      blocking: true,
    });
  } else {
    const versionDir = runtimeVersionDir(manifest.current);
    if (!fs.existsSync(versionDir)) {
      drifts.push({
        kind: 'current-runtime',
        source: runtimeManifestPath(),
        actual: manifest.current,
        expected: VERSION,
        fix: 'yotta-memory runtime install --from-current && yotta-memory runtime use ' + VERSION + ' --restart',
        blocking: true,
      });
    } else if (manifest.current !== VERSION) {
      drifts.push({
        kind: 'current-runtime',
        source: runtimeManifestPath(),
        actual: manifest.current,
        expected: VERSION,
        fix: 'yotta-memory runtime install --from-current && yotta-memory runtime use ' + VERSION + ' --restart',
        blocking: true,
      });
    }
    if (fs.existsSync(versionDir)) {
      if (!fs.existsSync(currentBin)) {
        drifts.push({
          kind: 'current-runtime',
          source: currentDir,
          actual: 'launcher-missing',
          expected: VERSION,
          fix: 'yotta-memory runtime use ' + manifest.current + ' --force',
          blocking: true,
        });
      } else {
        try {
          const real = fs.realpathSync(currentDir);
          if (path.resolve(real) !== path.resolve(versionDir)) {
            drifts.push({
              kind: 'current-runtime',
              source: currentDir,
              actual: 'pointer-mismatch',
              expected: manifest.current,
              fix: 'yotta-memory runtime use ' + manifest.current + ' --restart',
              blocking: true,
            });
          }
        } catch (e) {
          drifts.push({
            kind: 'current-runtime',
            source: currentDir,
            actual: 'pointer-unreadable',
            expected: manifest.current,
            fix: 'yotta-memory runtime use ' + manifest.current + ' --restart',
            blocking: true,
          });
        }
      }
    }
  }

  const legacyEnv = legacyIdentityEnvNames();
  if (legacyEnv.length) {
    drifts.push({
      kind: 'identity-mode',
      source: 'process-env',
      actual: 'legacy-env',
      expected: 'headers|stdio-args',
      fix: '移除 ' + legacyEnv.join(', ') + '，HTTP 改用请求头，stdio 改用 --agent-id + --agent-key-file',
      blocking: true,
    });
  }

  for (const configPath of mcpConfigPaths) {
    const abs = path.resolve(String(configPath));
    let text = '';
    try {
      text = fs.readFileSync(abs, 'utf8');
    } catch (e) {
      warnings.push('MCP 配置无法读取: ' + abs);
      checks.mcpConfigs.push({ path: abs, readable: false, version: 'unknown', identityMode: 'unknown' });
      continue;
    }
    const launchers = runtimeExtractLauncherPaths(text);
    const identityMode = runtimeConfigIdentityMode(text);
    const version = launchers.length ? (runtimeVersionFromPath(launchers[0]) || 'unknown') : 'unknown';
    checks.mcpConfigs.push({ path: abs, readable: true, launcher: launchers[0] || '', version: version, identityMode: identityMode });
    checks.identityModes.push({ source: abs, mode: identityMode });
    if (identityMode === 'legacy-env') {
      drifts.push({
        kind: 'identity-mode',
        source: abs,
        actual: 'legacy-env',
        expected: 'headers|stdio-args',
        fix: '从 MCP 配置移除身份 env，HTTP 改用请求头，stdio 改用 --agent-id + --agent-key-file',
        blocking: true,
      });
    }
    if (version !== 'unknown' && version !== VERSION) {
      drifts.push({
        kind: 'mcp-config',
        source: abs,
        actual: version,
        expected: VERSION,
        fix: '把 MCP 配置中的运行时路径改为 ' + runtimeCurrentBin() + ' 后重启该 MCP',
        blocking: true,
      });
    }
  }

  for (const processInfo of processes || []) {
    const row = typeof processInfo === 'string' ? { pid: '', commandLine: processInfo } : (processInfo || {});
    const commandLine = String(row.commandLine || '');
    if (!commandLine || commandLine.indexOf('yotta-memory') === -1 || commandLine.indexOf('serve') === -1) continue;
    const launchers = runtimeExtractLauncherPaths(commandLine);
    const launcher = launchers[0] || '';
    const version = launcher ? (runtimeVersionFromPath(launcher) || 'unknown') : 'unknown';
    checks.runningServers.push({ pid: row.pid || '', launcher: launcher, version: version });
    if (version !== 'unknown' && version !== VERSION) {
      drifts.push({
        kind: 'running-server',
        source: 'pid=' + String(row.pid || 'unknown'),
        actual: version,
        expected: VERSION,
        fix: 'yotta-memory runtime use ' + VERSION + ' --restart 或重启对应 MCP 客户端',
        blocking: false,
      });
    }
  }

  for (const skillDir of skillDirs) {
    const abs = path.resolve(String(skillDir));
    if (!fs.existsSync(path.join(abs, 'SKILL.md'))) continue;
    const version = runtimeVersionFromDir(abs) || 'unknown';
    checks.skillCopies.push({ path: abs, version: version });
    if (version !== 'unknown' && version !== VERSION) {
      drifts.push({
        kind: 'skill-copy',
        source: abs,
        actual: version,
        expected: VERSION,
        fix: '用官方安装器更新该 yotta-memory 技能副本',
        blocking: false,
      });
    }
  }

  const lines = [
    '## 运行时一致性',
    '- CLI: ' + VERSION + ' (' + runtimeExecutionPath() + ')',
    '- current: ' + (checks.current.version || '(missing)') + ' (' + currentDir + ')',
    '- runtime.json: ' + runtimeManifestPath(),
  ];
  if (checks.mcpConfigs.length) {
    for (const item of checks.mcpConfigs) lines.push('- MCP 配置: ' + item.path + ' -> ' + item.version + ' / ' + item.identityMode);
  } else lines.push('- MCP 配置: (未提供或未发现)');
  if (checks.runningServers.length) {
    for (const item of checks.runningServers) lines.push('- 运行中 server: pid=' + item.pid + ' -> ' + item.version);
  } else lines.push('- 运行中 server: (未发现)');
  if (checks.skillCopies.length) {
    for (const item of checks.skillCopies) lines.push('- 技能副本: ' + item.path + ' -> ' + item.version);
  } else lines.push('- 技能副本: (未提供或未发现)');
  if (!drifts.length) lines.push('- 漂移: 无');
  for (const drift of drifts) {
    lines.push('- [漂移] ' + drift.kind + ': actual=' + drift.actual + ' expected=' + drift.expected + ' fix=' + drift.fix + ' blocking=' + (drift.blocking ? 'yes' : 'no'));
  }
  return {
    ok: !drifts.some(function (drift) { return drift.blocking; }),
    checks: checks,
    drifts: drifts,
    warnings: warnings,
    text: lines.join('\n'),
  };
}
function storeHasMemoryData(root) {
  if (storeHasPublicFacts(root)) return true;
  if (hasPlaintextPrivate(root)) return true;
  // v0.17.0：年/月分层后必须递归统计，否则新布局会被误判为空库。
  if (collectEntryFiles(root).length) return true;
  return false;
}
function storeHasPublicFacts(root) {
  const factsDir = path.join(root, PUBLIC_DIR);
  if (!fs.existsSync(factsDir)) return false;
  const files = [];
  walkEntryFiles(factsDir, files);
  return files.length > 0;
}
// ---- v0.17.0 B2：doctor 规模体检（只读；阈值走 config，info / warning 两级）----
const SCALE_THRESHOLD_DEFAULTS = {
  scale_warn_entries: 50000,
  scale_warn_files_per_dir: 500,
  scale_warn_index_bytes: 5 * 1024 * 1024,
  scale_warn_cold_start_ms: 2000,
  scale_info_entries: 30000,
  scale_info_files_per_dir: 300,
  scale_info_index_bytes: 3 * 1024 * 1024,
  scale_info_cold_start_ms: 1200,
  // v0.23.0 D3：超长 statement / 单类型堆积（防写法走偏）
  scale_warn_long_statements: 50,
  scale_info_long_statements: 10,
  scale_warn_type_count: 500,
  scale_info_type_count: 200,
};
function scaleThreshold(cfg, key) {
  const raw = cfg ? cfg[key] : undefined;
  if (raw === undefined || raw === null || raw === '') return SCALE_THRESHOLD_DEFAULTS[key];
  const n = parseFloat(raw);
  return (n >= 0) ? n : SCALE_THRESHOLD_DEFAULTS[key];
}
function maxFilesInDir(dir) {
  let max = 0;
  let names;
  try { names = fs.readdirSync(dir, { withFileTypes: true }); } catch (e) { return 0; }
  let files = 0;
  for (const item of names) {
    if (item.isDirectory()) max = Math.max(max, maxFilesInDir(path.join(dir, item.name)));
    else if (item.isFile()) files++;
  }
  return Math.max(max, files);
}
function indexSizeBytes(root) {
  let total = 0;
  const manifest = indexPath(root);
  try { total += fs.statSync(manifest).size; } catch (e) { /* 尚未建索引 */ }
  for (const sh of (loadIndexManifest(root) || { shards: [] }).shards || []) {
    if (!isSafeShardName(sh)) continue;
    try { total += fs.statSync(path.join(root, sh)).size; } catch (e) { /* 分片缺失已由 doctor 其它段报出 */ }
  }
  return total;
}
function measureIndexColdStart(root) {
  const started = process.hrtime.bigint();
  loadIndex(root);
  const elapsed = Number(process.hrtime.bigint() - started) / 1e6;
  return Math.round(elapsed * 1000) / 1000;
}
function scaleMetric(key, value, unit, info, warn) {
  const level = value > warn ? 'warning' : (value > info ? 'info' : 'ok');
  return { key: key, value: value, unit: unit, info: info, warn: warn, level: level };
}
function typePressureReport(entries, cfg) {
  const archiveUtility = parseFloat(cfg && cfg.maintain_archived_utility || ARCHIVE_UTILITY_DEFAULT);
  const archiveAge = parseInt(cfg && cfg.maintain_archived_age || '180', 10) || 180;
  const report = {};
  for (const entry of entries) {
    const type = String(entry.type || 'FACT').toUpperCase();
    if (!report[type]) {
      report[type] = {
        total: 0,
        stale_180d: 0,
        archive_candidates: 0,
        growth_30d: 0,
        stale_ratio: 0,
        growth_ratio_30d: 0,
        pressure_level: 'ok',
        observation_days: 7,
        final_thresholds_deferred: true,
        warnings: [],
      };
    }
    const row = report[type];
    row.total += 1;
    const last = entry.last_accessed || entry.updated || entry.created || '';
    if (last && daysBetween(last, today()) > 180) row.stale_180d += 1;
    if (entry.created && daysBetween(entry.created, today()) <= 30) row.growth_30d += 1;
    const createdAge = entry.created ? daysBetween(entry.created, today()) : 0;
    if (type !== 'BOUND' && !entry.immutable && createdAge > archiveAge && utilityScore(entry) < archiveUtility) {
      row.archive_candidates += 1;
    }
  }
  for (const type of Object.keys(report)) {
    const row = report[type];
    row.stale_ratio = row.total ? Math.round((row.stale_180d / row.total) * 1000) / 1000 : 0;
    const prior = Math.max(0, row.total - row.growth_30d);
    row.growth_ratio_30d = prior ? Math.round((row.growth_30d / prior) * 1000) / 1000 : (row.growth_30d ? 1 : 0);
    if (row.total > 5000) {
      row.pressure_level = 'warning';
      row.warnings.push('类型压力: ' + type + ' 总量 ' + row.total + ' 超过 5000，需要分类型瘦身或归档。');
    } else if (row.total > 500 && row.stale_ratio >= 0.3 && row.archive_candidates > 0) {
      row.pressure_level = 'warning';
      row.warnings.push('类型压力: ' + type + ' ' + row.total + ' 条中 ' + row.stale_180d
        + ' 条超过 180 天未活跃，且有 ' + row.archive_candidates + ' 条归档候选。');
    } else if (row.total > 500 || row.growth_ratio_30d >= 0.2) {
      row.pressure_level = 'info';
    } else {
      row.pressure_level = 'observe';
    }
  }
  return report;
}
function scaleReport(root, cfg) {
  const thresholds = {};
  for (const key of Object.keys(SCALE_THRESHOLD_DEFAULTS)) thresholds[key] = scaleThreshold(cfg, key);
  const entries = collectEntryFiles(root).length;
  const filesPerDir = Math.max(maxFilesInDir(path.join(root, PUBLIC_DIR)), maxFilesInDir(path.join(root, PRIVATE_DIR)));
  const indexBytes = indexSizeBytes(root);
  // v0.23.0 D3：超长 statement（> 2000 字）与单类型堆积（读索引，不逐条解密读文件）
  const scaleEntries = loadIndex(root) || [];
  let indexData = null;
  try { indexData = JSON.parse(fs.readFileSync(indexPath(root), 'utf8')); } catch (e) { indexData = null; }
  const indexShards = indexData && Array.isArray(indexData.shards) ? indexData.shards.length : 0;
  const indexFormat = indexData
    ? String(indexData.format || (Array.isArray(indexData.entries) ? 'inline' : (indexShards && indexData.shards.every(isGzipShardName) ? 'gzip-year' : 'json-year')))
    : 'missing';
  const indexLogicalBytes = jsonByteLength(scaleEntries);
  let longStatements = 0;
  const typeCounts = { FACT: 0, PREF: 0, BOUND: 0, COMMIT: 0 };
  for (const e of scaleEntries) {
    const t = String(e.type || 'FACT').toUpperCase();
    typeCounts[t] = (typeCounts[t] || 0) + 1;
    if (String(e.statement || '').length > 2000) longStatements++;
  }
  let typeMax = 0;
  let typeMaxName = 'FACT';
  for (const t of Object.keys(typeCounts)) {
    if (typeCounts[t] > typeMax) { typeMax = typeCounts[t]; typeMaxName = t; }
  }
  // 冷启动取多次测量的中位数，避免单次抖动影响只读体检结果。
  const samples = [];
  for (let i = 0; i < 3; i++) samples.push(measureIndexColdStart(root));
  samples.sort(function (a, b) { return a - b; });
  const coldStartMs = samples[Math.floor(samples.length / 2)];
  const typePressure = typePressureReport(scaleEntries, cfg);
  const metrics = [
    scaleMetric('entries', entries, '条', thresholds.scale_info_entries, thresholds.scale_warn_entries),
    scaleMetric('files_per_dir', filesPerDir, '个文件', thresholds.scale_info_files_per_dir, thresholds.scale_warn_files_per_dir),
    scaleMetric('index_bytes', indexBytes, '字节', thresholds.scale_info_index_bytes, thresholds.scale_warn_index_bytes),
    scaleMetric('cold_start_ms', coldStartMs, 'ms', thresholds.scale_info_cold_start_ms, thresholds.scale_warn_cold_start_ms),
    scaleMetric('long_statements', longStatements, '条', thresholds.scale_info_long_statements, thresholds.scale_warn_long_statements),
    scaleMetric('type_max', typeMax, '条', thresholds.scale_info_type_count, thresholds.scale_warn_type_count),
  ];
  const warnings = [];
  if (metrics[0].level === 'warning') {
    warnings.push('规模: 记忆条数 ' + entries + ' 超过阈值 ' + thresholds.scale_warn_entries + '（考虑按年归档旧条目，或分批导出冷数据）');
  }
  if (metrics[1].level === 'warning') {
    warnings.push('规模: 单个目录文件数 ' + filesPerDir + ' 超过阈值 ' + thresholds.scale_warn_files_per_dir + '（检查是否有目录未按年/月分层）');
  }
  if (metrics[2].level === 'warning') {
    warnings.push('规模: 索引总体积 ' + indexBytes + ' 字节超过阈值 ' + thresholds.scale_warn_index_bytes + '（可用 reindex 重建，或按年份分片）');
  }
  if (metrics[3].level === 'warning') {
    warnings.push('规模: 索引冷启动 ' + coldStartMs + 'ms 超过阈值 ' + thresholds.scale_warn_cold_start_ms + 'ms（可用 reindex 重建索引）');
  }
  if (metrics[4].level === 'warning') {
    warnings.push('规模: 超长 statement（> 2000 字）' + longStatements + ' 条超过阈值 ' + thresholds.scale_warn_long_statements + '（建议拆分：记忆宜短句高密度，长文另存文档）');
  }
  if (metrics[5].level === 'warning') {
    warnings.push('规模: 单类型堆积（' + typeMaxName + ' ' + typeMax + ' 条）超过阈值 ' + thresholds.scale_warn_type_count + '（考虑归档 / 合并 / 精简；COMMIT 收工锚点建议短写）');
  }
  for (const type of Object.keys(typePressure)) {
    for (const message of typePressure[type].warnings) warnings.push(message);
  }
  // v0.18.0 A6：分级只影响 level 与提示文案；超 warn 仍进 warnings（既有行为），info 不阻断。
  const pressureWarning = Object.keys(typePressure).some(function (type) { return typePressure[type].pressure_level === 'warning'; });
  const level = pressureWarning || metrics.some(function (m) { return m.level === 'warning'; })
    ? 'warning'
    : (metrics.some(function (m) { return m.level === 'info'; }) ? 'info' : 'ok');
  return {
    entries: entries,
    files_per_dir: filesPerDir,
    index_bytes: indexBytes,
    index_logical_bytes: indexLogicalBytes,
    index_shards: indexShards,
    index_format: indexFormat,
    cold_start_ms: coldStartMs,
    thresholds: thresholds,
    metrics: metrics,
    type_pressure: typePressure,
    level: level,
    warnings: warnings,
  };
}
// 开工可靠性检查：只读检查根目录、密钥库、索引、身份登记与最近备份。
function doctorCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.root || userRoot());
  const cfg = loadConfig();
  const resolvedIdentity = resolveIdentity(opts);
  const identity = identityDiagnostic(resolvedIdentity);
  const checks = {};
  const warnings = [];
  const critical = [];
  const exists = isExistingStore(root);
  const hasData = storeHasMemoryData(root);
  const hasPublicFacts = storeHasPublicFacts(root);
  checks.root = { ok: exists, path: root };
  if (!exists) critical.push('记忆库不存在或基本结构缺失: ' + root);

  const encrypted = isEncrypted(root);
  checks.encrypted = { enabled: encrypted };
  if (encrypted) {
    const saltOk = fs.existsSync(encSaltPath(root));
    const recoveryOk = fs.existsSync(encRecoveryEncPath(root));
    checks.keys = { salt: saltOk, recovery: recoveryOk };
    if (!saltOk) critical.push('密钥库异常: 缺少 keys/salt');
    if (!recoveryOk) critical.push('密钥库异常: 缺少 keys/recovery.key.enc（恢复钥匙文件）');
  } else if (exists && hasPlaintextPrivate(root)) {
    checks.keys = { mode: 'plaintext' };
    warnings.push('当前私密区为明文；建议运行 yotta-memory migrate 启用加密。');
  } else {
    checks.keys = { mode: 'plaintext' };
  }

  const idxFile = indexPath(root);
  if (!fs.existsSync(idxFile)) {
    checks.index = { exists: false, valid: false };
    if (hasPublicFacts) warnings.push('公共索引缺失；可运行 yotta-memory reindex 重建。');
    else checks.index.fresh = true;
  } else if (!loadIndex(root)) {
    checks.index = { exists: true, valid: false };
    warnings.push('公共索引无法解析或版本过旧；可运行 yotta-memory reindex 重建。');
  } else {
    checks.index = { exists: true, valid: true };
  }
  // v0.22.6：索引一致性（文件为真源）；发现漂移先静默校准，再报告对齐结果。
  if (exists) {
    let consistency = null;
    try { consistency = indexConsistencyReport(root, { identity: resolvedIdentity }); } catch (e) { consistency = null; }
    if (consistency && consistency.drift) {
      try { maybeHealIndex(root, { identity: resolvedIdentity, force: true }); } catch (e) { /* ignore */ }
      try { consistency = indexConsistencyReport(root, { identity: resolvedIdentity }); } catch (e) { consistency = null; }
    }
    if (consistency) {
      checks.index = Object.assign({}, checks.index || {}, {
        consistent: !consistency.drift,
        files: consistency.files,
        entries: consistency.entries,
      });
      if (consistency.drift) warnings.push('索引一致性待校准；可运行 yotta-memory reindex。');
    }
  }

  // v0.17.0 B2：规模体检（只读，不产生写入）
  if (exists) {
    const scale = scaleReport(root, cfg);
    checks.scale = scale;
    for (const message of scale.warnings) warnings.push(message);
    const layout = layoutCollisionReport(root);
    checks.layout = layout;
    for (const message of layout.warnings) warnings.push(message);
  }

  if (!fs.existsSync(agentsPath(root))) {
    checks.agents = { exists: false, valid: false };
    if (hasData) warnings.push('agents.json 缺失；智能体身份登记不可用。');
    else checks.agents.fresh = true;
  } else {
    try {
      JSON.parse(fs.readFileSync(agentsPath(root), 'utf8'));
      checks.agents = { exists: true, valid: true };
    } catch (error) {
      checks.agents = { exists: true, valid: false };
      warnings.push('agents.json 无法解析；请先恢复身份登记。');
    }
  }
  checks.identity = identity;

  const migration = migrationRequiredInfo(root);
  if (migration) {
    checks.agentBindings = { ok: false, pending: migration.owners };
    warnings.push(migrationReminderText(root));
  } else if (encrypted) {
    checks.agentBindings = { ok: true, pending: [] };
  }

  const configuredDir = opts.dir || opts.backupDir || cfg.backup_dir;
  if (!configuredDir) {
    if (cfg.backup_setup_choice === 'manual') {
      checks.backup = { configured: false, manual: true, independent: false };
    } else {
      const health = backupHealthCore({ root: root, now: opts.now, sameVolumeFn: opts.sameVolumeFn });
      checks.backup = { configured: false, manual: false, independent: false };
      if (health.text) warnings.push(health.text);
    }
  } else {
    const status = backupStatusCore({
      root: root,
      dir: configuredDir,
      now: opts.now,
      sameVolumeFn: opts.sameVolumeFn,
    });
    checks.backup = {
      configured: true,
      manual: false,
      independent: !!status.independent,
      latest: status.latest ? status.latest.id : '',
      ageHours: status.ageHours,
      healthy: !!status.healthy,
    };
    if (!status.independent) {
      critical.push('备份目录与记忆库在同一卷，不能作为可靠备份。');
    }
    if (!status.latest) {
      warnings.push('备份目录已配置，但还没有成功备份；请运行 yotta-memory backup create 或 backup ensure-daily。');
    } else {
      const maxAge = Number(cfg.backup_max_age_hours) || 36;
      if (status.ageHours !== null && status.ageHours > maxAge) {
        warnings.push('最近备份已过期（' + status.ageHours.toFixed(1) + ' 小时，超过 ' + maxAge + ' 小时）；请检查备份盘与每日调度。');
      }
    }
    if (cfg.backup_last_error) warnings.push('最近一次备份失败: ' + cfg.backup_last_error);
    if (cfg.backup_scheduler_error) warnings.push('每日备份调度异常: ' + cfg.backup_scheduler_error);
  }

  let runtimeReport = null;
  if (opts.runtime) {
    runtimeReport = runtimeDoctorCore(opts);
    checks.runtime = runtimeReport.checks;
    for (const drift of runtimeReport.drifts) {
      const message = '运行时漂移 [' + drift.kind + ']: actual=' + drift.actual + ' expected=' + drift.expected + '；修复: ' + drift.fix + '；阻断: ' + (drift.blocking ? '是' : '否');
      if (drift.blocking) critical.push(message);
      else warnings.push(message);
    }
    for (const warning of runtimeReport.warnings || []) warnings.push(warning);
  }

  // v0.17.0 A2：基线探针只在显式 --baseline 时运行；失败进 warnings + baselineError，并让 CLI 非零退出。
  let baselineReport = null;
  let baselineError = '';
  if (opts.baseline) {
    baselineReport = baselineCore({
      root: root,
      against: opts.against,
      template: opts.template,
      seed: opts.seed,
      agent: opts.agent,
      agentId: opts.agentId,
      agentKey: opts.agentKey,
      agentKeyFile: opts.agentKeyFile,
    });
    checks.baseline = baselineReport;
    if (baselineReport.error) {
      baselineError = baselineReport.text;
      warnings.push(baselineReport.text);
    } else {
      for (const probe of baselineReport.probes || []) {
        if (probe.status === 'fail') warnings.push('基线探针 [' + probe.id + '] 失败: ' + probe.detail);
      }
    }
  }

  const level = critical.length ? 'critical' : (warnings.length ? 'warning' : 'ok');
  const agentHomeEnv = String(process.env.YOTTA_MEMORY_AGENT_HOME || '').trim();
  const lines = [
    '# yotta-memory doctor（开工可靠性检查）',
    '',
    '- 结果: ' + (level === 'critical' ? '严重' : (level === 'warning' ? '警告' : '正常')),
    '- 记忆库: ' + root,
    '- 加密: ' + (encrypted ? '是' : '否'),
    '- agent home: ' + (agentHomeEnv || '(未设置 YOTTA_MEMORY_AGENT_HOME，按宿主默认检测)'),
    '- 备份目录: ' + (configuredDir || (cfg.backup_setup_choice === 'manual' ? '手动模式' : '(未配置)')),
  ];
  if (checks.scale) {
    const scaleLevelLabel = checks.scale.level === 'warning' ? '告警' : (checks.scale.level === 'info' ? '提示' : '正常');
    const scaleTop = (checks.scale.metrics || []).filter(function (m) { return m.level !== 'ok'; })
      .sort(function (a, b) {
        const rank = { warning: 2, info: 1, ok: 0 };
        return rank[b.level] - rank[a.level];
      })[0];
    lines.push('- 规模: ' + checks.scale.entries + ' 条记忆 / 单目录最大 ' + checks.scale.files_per_dir + ' 个文件 / 索引 ' + checks.scale.index_bytes + ' 字节 / 冷启动 ' + checks.scale.cold_start_ms + 'ms（' + scaleLevelLabel + (scaleTop ? '，最高项 ' + scaleTop.key + ' ' + scaleTop.value + scaleTop.unit : '') + '）');
  }
  if (checks.layout && (checks.layout.duplicates || checks.layout.conflicts || checks.layout.unverified)) {
    lines.push('- 布局: 同序号重复 ' + checks.layout.duplicates + ' 组 / 冲突 ' + checks.layout.conflicts + ' 组 / 待核 ' + checks.layout.unverified + ' 组');
  }
  if (checks.index && typeof checks.index.consistent === 'boolean') {
    lines.push('- 索引一致性: ' + (checks.index.consistent ? '正常（' + checks.index.entries + ' 条 = ' + checks.index.files + ' 个文件）' : '待校准'));
  }
  for (const message of critical) lines.push('- [严重] ' + message);
  for (const message of warnings) lines.push('- [警告] ' + message);
  if (!critical.length && !warnings.length) lines.push('- 检查项: 全部通过');
  if (baselineReport && !baselineReport.error) {
    lines.push('');
    lines.push(baselineReport.text);
  }
  if (runtimeReport) {
    lines.push('');
    lines.push(runtimeReport.text);
  }
  if (level === 'critical') {
    lines.push('');
    lines.push('- 破坏性写入已锁定：先运行 yotta-memory doctor 修复严重问题。');
  }
  return {
    error: false,
    schemaVersion: 1,
    ok: critical.length === 0,
    level: level,
    encryption: encrypted,
    migration_required: migration ? migration.entries : [],
    critical: critical,
    warnings: warnings,
    baseline: baselineReport,
    baselineError: baselineError,
    checks: checks,
    identity: identity,
    root: root,
    text: lines.join('\n'),
  };
}
// 破坏性写入前的统一快照门：先 doctor，再创建新的整库快照，最后写事务审计。
function destructiveGuardCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.root || userRoot());
  // snapshotDir / allowSameVolumeForTest 仅用于 core 测试注入；CLI 的 --allow-same-volume 不进入破坏性写入门。
  const snapshotDir = opts.snapshotDir || opts.backupDir || loadConfig().backup_dir || '';
  const sameVolumeFn = opts.sameVolumeFn || (opts.allowSameVolumeForTest ? function () { return false; } : undefined);
  const report = doctorCore({
    root: root,
    backupDir: snapshotDir || undefined,
    now: opts.now,
    sameVolumeFn: sameVolumeFn,
  });
  if (!report.ok) {
    return {
      error: true,
      doctor: report,
      text: '拒绝: 开工可靠性检查未通过，破坏性操作已锁定。\n' + report.text,
    };
  }
  if (!snapshotDir) {
    return {
      error: true,
      doctor: report,
      text: '拒绝: 未配置独立备份目录，不能执行破坏性操作。请先运行 backup volumes，由用户确认位置后执行 backup setup。',
    };
  }
  const snapshot = backupCreateCore({
    root: root,
    dir: snapshotDir,
    now: opts.now,
    allowSameVolume: !!opts.allowSameVolumeForTest,
    sameVolumeFn: sameVolumeFn,
  });
  if (snapshot.error) {
    return {
      error: true,
      doctor: report,
      text: '拒绝: 事务快照失败，原记忆未改动。\n' + snapshot.text,
    };
  }
  const transaction = 'txn-' + Date.now() + '-' + crypto.randomBytes(3).toString('hex');
  const auditOk = appendAudit(root, 'audit', {
    action: 'transaction_start',
    ts: new Date().toISOString(),
    transaction: transaction,
    operation: opts.action || 'destructive',
    root: root,
    snapshot: snapshot.id,
    snapshotPath: snapshot.path,
  });
  if (!auditOk) {
    return {
      error: true,
      doctor: report,
      snapshot: snapshot,
      text: '拒绝: 事务审计写入失败，原记忆未改动。快照已保留: ' + snapshot.id,
    };
  }
  return {
    error: false,
    doctor: report,
    snapshot: snapshot,
    transaction: transaction,
    text: '事务快照: ' + snapshot.id,
  };
}
function sha256File(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}
function listBackupFiles(dir, baseDir) {
  const out = [];
  const walk = function (current) {
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.isFile()) {
        out.push({
          path: path.relative(baseDir, full).replace(/\\/g, '/'),
          size: fs.statSync(full).size,
          sha256: sha256File(full),
        });
      }
    }
  };
  walk(dir);
  return out;
}
function isAllowedBackupPath(rel) {
  const normalized = String(rel || '').replace(/\\/g, '/').replace(/^\/+|\/+$/g, '');
  if (!normalized) return true;
  const top = normalized.split('/')[0];
  if (top === 'facts' || top === 'private' || top === '.archive') return true;
  if (top === 'agents.json' || top === 'index.json' || /^index-\d{4}\.json(?:\.gz)?$/.test(top)) return true;
  if (top === 'keys') {
    return normalized !== 'keys/cache' && normalized.indexOf('keys/cache/') !== 0 &&
      normalized !== 'keys/pending' && normalized.indexOf('keys/pending/') !== 0;
  }
  return false;
}
function backupCreateCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.root || userRoot());
  if (!isExistingStore(root)) return { error: true, text: '记忆库不存在或未初始化: ' + root };
  const destBase = backupDestination(opts);
  if (!destBase) return { error: true, text: '未配置备份目录。请用 --dir <目录>、YOTTA_MEMORY_BACKUP_DIR 或 config set backup_dir <目录>。' };
  const same = opts.sameVolumeFn ? !!opts.sameVolumeFn(root, destBase) : sameVolume(root, destBase);
  if (!opts.allowSameVolume && same) {
    return { error: true, text: '拒绝: 备份目录与记忆库在同一卷。请把备份放到独立盘或独立卷。' };
  }
  const createdAt = new Date(opts.now || Date.now()).toISOString();
  const id = os.hostname() + '-' + createdAt.replace(/[:.]/g, '-') + '-' + crypto.randomBytes(3).toString('hex');
  const target = path.join(destBase, id);
  try {
    fs.mkdirSync(destBase, { recursive: true });
    fs.cpSync(root, target, {
      recursive: true,
      force: false,
      errorOnExist: true,
      filter: function (src) {
        const rel = path.relative(root, src).replace(/\\/g, '/');
        return isAllowedBackupPath(rel);
      },
    });
    const files = listBackupFiles(target, target);
    const manifest = {
      id: id,
      version: VERSION,
      created: createdAt,
      source: root,
      files: files,
    };
    fs.writeFileSync(path.join(target, 'manifest.json'), JSON.stringify(manifest, null, 2), 'utf8');
    return { error: false, id: id, path: target, manifest: manifest, text: '已创建备份: ' + target + '（' + files.length + ' 文件）' };
  } catch (error) {
    return { error: true, text: '备份失败: ' + error.message };
  }
}
function backupListCore(opts) {
  opts = opts || {};
  const destBase = backupDestination(opts);
  if (!destBase) return { error: true, backups: [], text: '未配置备份目录。请用 --dir <目录>、YOTTA_MEMORY_BACKUP_DIR 或 config set backup_dir <目录>。' };
  if (!fs.existsSync(destBase)) return { error: false, backups: [], text: '（无备份）' };
  const backups = [];
  for (const entry of fs.readdirSync(destBase, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const full = path.join(destBase, entry.name);
    let manifest = null;
    try { manifest = JSON.parse(fs.readFileSync(path.join(full, 'manifest.json'), 'utf8')); } catch (_) {}
    backups.push({
      id: entry.name,
      path: full,
      created: manifest && manifest.created ? manifest.created : '',
      files: manifest && Array.isArray(manifest.files) ? manifest.files.length : null,
      manifest: manifest,
    });
  }
  backups.sort(compareBackupCreatedDesc);
  const lines = backups.length
    ? backups.map(function (b) { return '- ' + b.id + '  ' + (b.created || '?') + '  ' + (b.files === null ? 'manifest 缺失' : b.files + ' 文件'); })
    : ['（无备份）'];
  return { error: false, backups: backups, text: lines.join('\n') };
}
function backupDoctorCore(opts) {
  opts = opts || {};
  const listed = backupListCore(opts);
  if (listed.error) return { error: true, ok: false, text: listed.text };
  const id = opts.id || (selectLatestValidBackup(listed.backups, Date.now()).latestValid || {}).id;
  if (!id) return { error: false, ok: false, text: '没有可检查的备份。' };
  const backup = listed.backups.find(function (item) { return item.id === id; });
  if (!backup) return { error: true, ok: false, text: '未找到备份: ' + id };
  if (!backup.manifest || !Array.isArray(backup.manifest.files)) {
    return { error: false, ok: false, text: '备份 manifest 缺失或损坏: ' + id };
  }
  const bad = [];
  for (const file of backup.manifest.files) {
    if (!isSafeRelativePathForBackup(file.path)) { bad.push(file.path + '（路径不安全）'); continue; }
    const full = path.join(backup.path, file.path);
    if (!fs.existsSync(full)) { bad.push(file.path + '（缺失）'); continue; }
    const stat = fs.statSync(full);
    if (stat.size !== file.size) { bad.push(file.path + '（大小不符）'); continue; }
    if (sha256File(full) !== file.sha256) bad.push(file.path + '（哈希不符）');
  }
  return {
    error: false,
    ok: bad.length === 0,
    text: bad.length ? '备份体检失败: ' + id + '\n' + bad.join('\n') : '备份体检通过: ' + id + '（' + backup.manifest.files.length + ' 文件）',
  };
}
function isSafeRelativePathForBackup(value) {
  if (typeof value !== 'string' || value === '' || path.isAbsolute(value)) return false;
  return !value.split(/[\\/]+/).includes('..');
}
function backupRestoreCore(id, opts) {
  opts = opts || {};
  if (!id) return { error: true, text: '请指定备份 ID: yotta-memory backup restore <id> --to <目录>' };
  const destBase = backupDestination(opts);
  if (!destBase) return { error: true, text: '未配置备份目录。请用 --dir <目录> 或 config set backup_dir <目录>。' };
  const source = path.join(destBase, id);
  if (!fs.existsSync(path.join(source, 'manifest.json'))) return { error: true, text: '备份不存在或 manifest 缺失: ' + id };
  if (!opts.to) return { error: true, text: '拒绝恢复到未指定位置。请使用 --to <新目录>；默认不覆盖正在使用的记忆库。' };
  const target = path.resolve(String(opts.to));
  if (fs.existsSync(target) && fs.readdirSync(target).length > 0) {
    return { error: true, text: '恢复目标非空，拒绝覆盖: ' + target };
  }
  try {
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.cpSync(source, target, {
      recursive: true,
      force: false,
      errorOnExist: true,
      filter: function (src) { return path.basename(src) !== 'manifest.json'; },
    });
    return { error: false, path: target, text: '已恢复到: ' + target };
  } catch (error) {
    return { error: true, text: '恢复失败: ' + error.message };
  }
}
function findFirstEncryptedPrivateFile(root) {
  const pdir = path.join(root, PRIVATE_DIR);
  if (!fs.existsSync(pdir)) return null;
  const owners = fs.readdirSync(pdir);
  for (const owner of owners) {
    const ownerDir = path.join(pdir, owner);
    if (!fs.statSync(ownerDir).isDirectory()) continue;
    for (const type of PRIVATE_LEAF) {
      const dir = path.join(ownerDir, type);
      if (!fs.existsSync(dir)) continue;
      // v0.22.8：递归查找年 / 月分层（0.17+ 写入布局）；只看平铺一层会让纯分层库静默跳过私密解密校验。
      const stack = [dir];
      while (stack.length) {
        const current = stack.pop();
        let items = [];
        try { items = fs.readdirSync(current, { withFileTypes: true }); } catch (e) { continue; }
        for (const item of items) {
          const fp = path.join(current, item.name);
          if (item.isDirectory()) { stack.push(fp); continue; }
          if (!item.name.endsWith('.md' + ENC_SUFFIX)) continue;
          if (fs.statSync(fp).isFile()) return { fp: fp, owner: owner, rel: relOf(root, fp) };
        }
      }
    }
  }
  return null;
}
function backupDrillCore(opts) {
  opts = opts || {};
  const destBase = backupDestination(opts);
  if (!destBase) return { error: true, ok: false, text: '未配置备份目录。请用 --dir <目录> 或 config set backup_dir <目录>。' };
  const listed = backupListCore({ dir: destBase });
  if (listed.error) return { error: true, ok: false, text: listed.text };
  const id = opts.id || (listed.backups[0] && listed.backups[0].id);
  if (!id) return { error: true, ok: false, text: '没有可演练的备份。' };
  let target = opts.to ? path.resolve(String(opts.to)) : '';
  let tempParent = '';
  if (!target) {
    tempParent = fs.mkdtempSync(path.join(os.tmpdir(), 'ytm-drill-'));
    target = path.join(tempParent, 'restored');
  }
  function fail(text, checks, extra) {
    if (tempParent) {
      try { fs.rmSync(tempParent, { recursive: true, force: true }); } catch (_) {}
    }
    return Object.assign({ error: true, ok: false, text: text, checks: checks || {} }, extra || {});
  }
  const verified = backupDoctorCore({ dir: destBase, id: id });
  if (!verified.ok) return fail('恢复演练失败: 备份 manifest 校验未通过。\n' + verified.text, { manifest: false });
  const restored = backupRestoreCore(id, { dir: destBase, to: target });
  if (restored.error) return fail(restored.text, { manifest: true, index: false });
  let indexOk = false;
  let indexError = '';
  try {
    buildIndex(target);
    indexOk = true;
  } catch (error) {
    indexError = error.message;
  }
  if (!indexOk) return fail('恢复演练失败: 恢复副本无法重建索引: ' + indexError, { manifest: true, index: false });
  const privateFile = findFirstEncryptedPrivateFile(target);
  let privateCheck = { checked: false, decrypted: true, source: 'no-private-entry' };
  if (privateFile) {
    let ownerKey = null;
    let source = '';
    try {
      if (opts.recoveryKey) {
        ownerKey = unwrapOwnerKeyRecovery(target, privateFile.owner, Buffer.from(String(opts.recoveryKey), 'base64'));
        source = 'recovery-key';
      } else if (opts.password) {
        const salt = loadSalt(target);
        if (!salt) throw new Error('恢复副本缺少 keys/salt');
        ownerKey = unwrapOwnerKey(target, privateFile.owner, deriveUmk(opts.password, salt));
        source = 'password';
      }
    } catch (error) {
      ownerKey = null;
    }
    if (!ownerKey) {
      // v0.22.8：未提供任何凭证时上报 needPassword，由 CLI 层复用 resolvePasswordInput（交互 / stdin / env）再演练；
      // 提供了但无效的凭证仍按普通失败处理，避免反复提示。
      const needPassword = !opts.password && !opts.recoveryKey;
      return fail('恢复演练失败: 已恢复文件结构，但无法解密测试私密记忆。请提供 --recovery-key 或 --password；legacy keys/cache 明文缓存不再作为恢复凭证。', {
        manifest: true,
        index: true,
        private: { checked: true, decrypted: false, source: '', file: privateFile.rel },
      }, needPassword ? { needPassword: true } : null);
    }
    try {
      decryptMemoryText(fs.readFileSync(privateFile.fp), ownerKey);
      privateCheck = { checked: true, decrypted: true, source: source, file: privateFile.rel, owner: privateFile.owner };
    } catch (error) {
      return fail('恢复演练失败: 测试私密记忆解密失败（' + error.message + '）。', {
        manifest: true,
        index: true,
        private: { checked: true, decrypted: false, source: source, file: privateFile.rel },
      });
    }
  }
  if (tempParent) {
    try { fs.rmSync(tempParent, { recursive: true, force: true }); } catch (_) {}
  }
  // v0.17.0 A2：--probe 时在恢复副本上跑基线探针（探针只读；探针失败则整体演练失败，临时副本照旧清理）。
  let probeReport = null;
  if (opts.probe) {
    probeReport = baselineCore({
      root: target,
      against: opts.against,
      template: opts.template,
      seed: opts.seed,
      agent: opts.agent,
      agentId: opts.agentId,
      agentKey: opts.agentKey,
      agentKeyFile: opts.agentKeyFile,
    });
    if (probeReport.error || !probeReport.ok) {
      return fail('恢复演练失败: 基线探针未通过。\n' + probeReport.text, {
        manifest: true,
        index: true,
        private: privateCheck,
        baseline: probeReport,
      });
    }
  }
  const checks = { manifest: true, index: true, private: privateCheck, baseline: probeReport };
  const lines = [
    '恢复演练通过: ' + id,
    '- manifest / SHA-256: 通过',
    '- 恢复副本索引: 通过',
    '- 测试私密解密: ' + (privateCheck.checked ? ('通过（' + privateCheck.source + '，' + privateCheck.file + '）') : '跳过（备份中没有加密私密条目）'),
  ];
  if (probeReport) {
    lines.push('');
    lines.push(probeReport.text);
  }
  return {
    error: false,
    ok: true,
    id: id,
    restoredTo: tempParent ? '(临时副本已清理)' : target,
    checks: checks,
    probes: probeReport ? probeReport.probes : null,
    text: lines.join('\n'),
  };
}
function rememberCore(type, subject, statement, opts) {
  opts = opts || {};
  const root = opts.root ? path.resolve(String(opts.root)) : userRoot();
  ensureInit(root);
  const t = String(type).toUpperCase();
  if (!TYPE_DIRS[t]) return { error: true, text: '未知记忆类型: ' + type + '（可用: ' + TYPES.join(' / ') + '）' };
  const stmt = String(statement || '').trim();
  const subj = String(subject || '').trim();
  if (!stmt) return { error: true, text: 'statement 不能为空' };
  if (!subj) return { error: true, text: 'subject 不能为空' };
  const ident = opts.userUnlocked ? { id: '', error: '' } : resolveIdentity(opts);
  const selfAgent = ident.id;
  const owner = opts.owner || selfAgent;
  const scope = opts.scope || defaultScope(t);
  if (scope === 'private' && ident.error && !opts.userUnlocked) {
    return { error: true, text: ident.error };
  }
  if (scope === 'private' && !opts.userUnlocked) {
    const keyError = validatePrivateIdentity(root, ident, owner);
    if (keyError) return { error: true, text: keyError };
  }
  if (scope === 'private' && !owner) {
    return { error: true, text: '私密记忆必须显式声明归属智能体：CLI 传 --agent <id>；stdio MCP 传 --agent-id <id> + --agent-key-file <path>；HTTP MCP 发送 X-Agent-Id + X-Agent-Key。公共记忆(FACT)不受影响。' };
  }
  if (scope === 'private' && owner && selfAgent && owner !== selfAgent && !opts.unsafe && !opts.userUnlocked) {
    return { error: true, text: '拒绝: 当前显式身份 ' + selfAgent + ' 不能写入其它智能体 ' + owner + ' 的私密区。请传正确的 --agent <id>，或加 --unsafe（用户显式授权）。' };
  }
  const encrypted = isEncrypted(root);
  if (scope === 'private' && encrypted && !getOwnerKeyFor(root, owner)) {
    return { error: true, text: '私密区已加密：当前无 ' + owner + ' 的授权密钥，请在用户平台授权（yotta-memory view → 授权本智能体）后再写私密记忆。公共 FACT 不受影响。' };
  }
  const typeDir = path.join(root, typeSubdir(t, owner));
  const writeDate = today(opts._today);
  const dir = entryWriteDir(root, t, owner, writeDate);
  fs.mkdirSync(dir, { recursive: true });
  // 去重扫描覆盖旧平铺 + 最近写入窗口，避免同一内容按两种布局各存一份。
  const existingFiles = recentlyWrittenFiles(typeDir, dir);
  if (existingFiles.length) {
    for (const fp of existingFiles) {
      let parsed;
      try { parsed = parseFrontmatter(readMemoryText(root, fp, owner)); } catch (err) { continue; }
      const meta = parsed.meta;
      if ((meta.type || '').toUpperCase() === t && meta.subject === subj && meta.statement === stmt) {
        const patch = { updated: writeDate };
        if (owner && !meta.owner) patch.owner = owner;
        if (scope && !meta.scope) patch.scope = scope;
        if (opts.source && !meta.source) patch.source = opts.source;
        const w = parseFloat(opts.weight); if (w > 0) patch.weight = Math.max(parseFloat(meta.weight || '1.0') || 1.0, w);
        rewriteFrontmatter(fp, patch, root, owner);
        upsertIndexEntry(root, readEntry(fp, root));
        let text = '已更新: ' + fp;
        if (opts.hint !== false && t === 'FACT') {
          const hit = HINT_KEYWORDS.filter(function (w) { return stmt.indexOf(w) !== -1; });
          if (hit.length) text += '\n[提示] statement 含主观/关系词（' + hit.join('、') + '），疑似用户偏好 / 关系内容——若属此类建议改用 PREF（私密，仅本人可读）。仅提示不拦截；--no-hint 可关闭。';
        }
        if (opts.hint !== false && t === 'COMMIT' && stmt.length > 1200) {
          text += '\n[提示] 这条 COMMIT 较长（' + stmt.length + ' 字）：开工上下文包默认只展示最近 ' + CONTEXT_COMMITS_LIMIT_DEFAULT + ' 条 COMMIT；收工锚点建议 ≤500 字（重点放 subject），重要承诺可加 --weight 1.5 或 tags pinned 保持常显。仅提示不拦截；--no-hint 可关闭。';
        }
        if (opts.verify) {
          const rel = path.relative(root, fp).replace(/\\/g, '/');
          const ok = verifyWrittenReadable(root, rel, subj, selfAgent || opts.agent);
          text += '\n[verify] ' + (ok ? '已写回读 OK: ' + rel : '回读未命中，请检查: ' + rel);
        }
        return { error: false, text: text };
      }
    }
  }
  const rec = {
    type: t, subject: subj, statement: stmt,
    confidence: 1.0, created: writeDate, updated: writeDate,
    tags: Array.isArray(opts.tags) ? opts.tags.map(function (x) { return String(x).trim(); }).filter(Boolean) : [],
    immutable: false,
    scope: scope, owner: owner,
    source: opts.source || '',
    weight: (parseFloat(opts.weight) > 0 ? parseFloat(opts.weight) : 1.0),
    access_count: 0, last_accessed: '',
  };
  // v0.22.6：序号分配 + 文件落盘 + 索引更新同处一个临界区，防多进程算出同序号互相覆盖。
  let file = '';
  withIndexLock(root, function () {
    const suffix = (encrypted && scope === 'private') ? ENC_SUFFIX : '';
    let seqNum = parseInt(nextSeqFor(typeDir, dir), 10) || 1;
    for (let attempt = 0; attempt < 100; attempt++) {
      const candidate = path.join(dir, writeDate + '-' + String(seqNum).padStart(4, '0') + '.md' + suffix);
      try {
        writeMemoryText(root, candidate, frontmatterToText(rec, stmt), owner, { exclusive: true });
        file = candidate;
        break;
      } catch (e) {
        if (e && e.code === 'EEXIST') { seqNum += 1; continue; }
        throw e;
      }
    }
    if (!file) throw new Error('无法分配记忆文件名（连续冲突）');
    upsertIndexEntry(root, readEntry(file, root));
  });
  let text = '已记录: ' + file;
  if (opts.hint !== false && t === 'FACT') {
    const hit = HINT_KEYWORDS.filter(function (w) { return stmt.indexOf(w) !== -1; });
    if (hit.length) text += '\n[提示] statement 含主观/关系词（' + hit.join('、') + '），疑似用户偏好 / 关系内容——若属此类建议改用 PREF（私密，仅本人可读）。仅提示不拦截；--no-hint 可关闭。';
  }
  if (opts.hint !== false && t === 'COMMIT' && stmt.length > 1200) {
    text += '\n[提示] 这条 COMMIT 较长（' + stmt.length + ' 字）：开工上下文包默认只展示最近 ' + CONTEXT_COMMITS_LIMIT_DEFAULT + ' 条 COMMIT；收工锚点建议 ≤500 字（重点放 subject），重要承诺可加 --weight 1.5 或 tags pinned 保持常显。仅提示不拦截；--no-hint 可关闭。';
  }
  if (opts.verify) {
    const rel = path.relative(root, file).replace(/\\/g, '/');
    const ok = verifyWrittenReadable(root, rel, subj, selfAgent || opts.agent);
    text += '\n[verify] ' + (ok ? '已写回读 OK: ' + rel : '回读未命中，请检查: ' + rel);
  }
  return { error: false, text: text };
}
// v0.8.1: recall 候选预过滤——查询侧一次构建候选 token 集（精确/同义/拼音/拉丁 py），
// 逐条用 token 交集 + 子串 + 模糊长度门槛做粗筛，命中候选才进语义打分，避免 N 大时逐条全量语义/模糊/编辑距离。
// 该闸门是 semanticMatch 命中集的超集，绝不漏掉同义词/拼音/模糊命中，仅做性能粗筛不改语义。
function recallPrefilter(q) {
  const qtoks = tokenize(q);
  const qset = new Set(qtoks);
  const qpy = pinyinTokens(q);
  const ext = new Set();
  for (const tt of qtoks) { const s = synonymSet(tt); for (const w of s) ext.add(w); }
  const qkeys = new Set();
  for (const tt of qtoks) qkeys.add(tt);
  for (const w of ext) qkeys.add(w);
  for (const t of qpy) qkeys.add(t);
  const longQtoks = qtoks.filter(function (t) { return t.length >= 4; });
  for (const tt of qtoks) {
    if (/^[a-z]+$/.test(tt)) {
      qkeys.add('py:' + tt); qkeys.add('pyi:' + tt);
      if (tt.length >= 3) { for (let i = 0; i < tt.length - 1; i++) qkeys.add('pyi:' + tt.slice(i, i + 2)); }
    }
  }
  return function (e) {
    const toks = e.tokens || {};
    const keys = Object.keys(toks);
    for (const k of keys) {
      if (qkeys.has(k)) return true;
      if (longQtoks.length && k.length >= 4 && k.indexOf(':') === -1) {
        for (const t of longQtoks) {
          if (Math.abs(k.length - t.length) <= 2) return true;
        }
      }
    }
    const hay = ((e.subject || '') + ' ' + (e.statement || '') + ' ' + (e.tags || []).join(' ')).toLowerCase();
    if (hay.indexOf(q) !== -1) return true;
    return false;
  };
}
// v0.17.0：命中打分与排序抽成共享原语，recall 与 bench 用同一套逻辑（评测才不会与真实检索漂移）。
function scoreCandidates(entries, query, options) {
  options = options || {};
  const useSemantic = options.semantic !== false;
  const prefilter = options.prefilter || null;
  const wantExplain = !!options.wantExplain;
  const embeddingMap = options.embeddingMap || null;
  const root = options.root ? String(options.root) : '';
  const out = [];
  for (const e of entries || []) {
    let score = 0;
    let detail = null;
    const embeddingHit = embeddingMap ? (embeddingMap.get(root + '\0' + e.file) || null) : null;
    if (query) {
      if (useSemantic) {
        if (prefilter && !prefilter(e) && !embeddingHit) continue; // v0.8.1 候选预过滤：粗筛后再语义打分；embedding 命中可越过词法预过滤
        const m = semanticMatch(e, query, wantExplain);
        score = m.score;
        if (wantExplain && m.detail && m.detail.length) detail = m.detail;
        if (embeddingHit) {
          score = Math.max(score, embeddingHit.score);
          if (wantExplain && embeddingHit.detail) detail = (detail || []).concat(embeddingHit.detail);
        }
      } else {
        const qtoks = tokenize(query);
        for (const tt of qtoks) { if (e.tokens && e.tokens[tt]) score += e.tokens[tt]; }
        if (score === 0) {
          const hay = ((e.subject || '') + ' ' + (e.statement || '') + ' ' + (e.tags || []).join(' ')).toLowerCase();
          if (hay.indexOf(query) !== -1) score = 1;
        }
      }
      if (score === 0) continue;
    } else {
      score = 1;
    }
    out.push({ entry: e, score: score, detail: detail });
  }
  return out;
}
function rankHits(hits, options) {
  options = options || {};
  const fuse = options.fuse !== false;
  if (hits.length > 1 && fuse) {
    // v0.8.0 融合排序：0.65 × 语义分归一 + 0.35 × 效用分归一
    let minSem = Infinity, maxSem = -Infinity, minUtil = Infinity, maxUtil = -Infinity;
    for (const h of hits) {
      if (h.score < minSem) minSem = h.score;
      if (h.score > maxSem) maxSem = h.score;
      const u = utilityScore(h.entry);
      if (u < minUtil) minUtil = u;
      if (u > maxUtil) maxUtil = u;
    }
    const spanSem = maxSem - minSem;
    const spanUtil = maxUtil - minUtil;
    for (const h of hits) {
      h.semNorm = spanSem > 0 ? (h.score - minSem) / spanSem : 1;
      h.utilNorm = spanUtil > 0 ? (utilityScore(h.entry) - minUtil) / spanUtil : 1;
      h.finalScore = 0.65 * h.semNorm + 0.35 * h.utilNorm;
    }
    hits.sort(function (a, b) {
      if (b.finalScore !== a.finalScore) return b.finalScore - a.finalScore;
      if (b.score !== a.score) return b.score - a.score;
      const pa = a.root === projectRoot() ? 0 : 1;
      const pb = b.root === projectRoot() ? 0 : 1;
      if (pa !== pb) return pa - pb;
      return String(b.entry.created).localeCompare(String(a.entry.created));
    });
    return hits;
  }
  hits.sort(function (a, b) {
    if (options.sortByScore && b.score !== a.score) return b.score - a.score;
    const pa = a.root === projectRoot() ? 0 : 1;
    const pb = b.root === projectRoot() ? 0 : 1;
    if (pa !== pb) return pa - pb;
    return String(b.entry.created).localeCompare(String(a.entry.created));
  });
  return hits;
}
function recallCore(query, opts) {
  opts = opts || {};
  const roots = memoryRoots();
  if (!roots.length) return { error: false, exitCode: 0, text: '记忆库不存在，请先运行: yotta-memory init' };
  const limit = opts.limit || 50;
  const onlyType = opts.type ? String(opts.type).toUpperCase() : null;
  const q = query ? String(query).toLowerCase() : '';
  const ident = resolveIdentity(opts);
  if (ident.error) return { error: true, exitCode: 3, text: ident.error };
  const selfAgent = ident.id;
  const agent = selfAgent;
  const ownerFilter = opts.owner || '';
  const allSafe = !!opts.unsafe;
  if (ownerFilter && !isSafeAgentId(ownerFilter)) {
    return { error: true, exitCode: 3, text: '非法 owner ID：只允许单段名称，禁止 /、\\、.. 和控制字符。' };
  }
  if (!selfAgent && (opts.all || ownerFilter)) {
    return {
      error: true,
      exitCode: 3,
      text: '显式跨智能体读取必须先声明身份：CLI 传 --agent <id>；stdio MCP 传 --agent-id <id> + --agent-key-file <path>；HTTP MCP 发送 X-Agent-Id + X-Agent-Key。',
    };
  }
  if (selfAgent && !allSafe) {
    for (const root of roots) {
      const keyError = validatePrivateIdentity(root, ident, ownerFilter || selfAgent);
      if (keyError && isEncrypted(root)) {
        return { error: true, exitCode: 3, text: keyError };
      }
    }
  }
  const explicitCross = !!opts.all || (!!ownerFilter && ownerFilter !== agent);
  const wantExplain = !!opts.explain;
  const useSemantic = opts.semantic !== false;
  const yearFilter = normalizeYearList(opts.years);
  if (yearFilter.error) return { error: true, exitCode: 2, text: yearFilter.error };
  const years = yearFilter.years;
  const prefilter = (q && useSemantic) ? recallPrefilter(q) : null;
  const embeddingMap = new Map();
  const embeddingCommand = effectiveEmbeddingCommand(opts);
  const embeddingTimeout = effectiveEmbeddingTimeout(opts);
  if (q && embeddingCommand) {
    for (const root of roots) {
      const rootEntries = indexEntriesFor(root, { years: years }).entries.filter(function (e) {
        return classifyRead(e, agent, ownerFilter, allSafe, selfAgent) !== 'denied';
      });
      try {
        const hits = embeddingCandidates(rootEntries, q, {
          embedding: embeddingCommand,
          embeddingTimeout: embeddingTimeout,
          root: root
        });
        for (const h of hits) {
          embeddingMap.set(root + '\0' + h.entry.file, h);
        }
      } catch (err) {
        // Plugin failure is not fatal; keep lexical-only recall.
      }
    }
  }
  const hits = [];
  let deniedCount = 0;
  for (const root of roots) {
    const entries = indexEntriesFor(root, { years: years }).entries;
    const readable = [];
    for (const e of entries) {
      if (onlyType && e.type !== onlyType) continue;
      const r = classifyRead(e, agent, ownerFilter, allSafe, selfAgent);
      if (r === 'denied') { deniedCount++; continue; }
      readable.push(e);
    }
    const scored = scoreCandidates(readable, q, {
      semantic: useSemantic,
      prefilter: prefilter,
      wantExplain: wantExplain,
      embeddingMap: embeddingMap,
      root: root,
    });
    for (const s of scored) {
      hits.push({ entry: s.entry, score: s.score, root: root, detail: s.detail });
    }
  }
  rankHits(hits, {});
  const shown = hits.slice(0, limit);
  if (!shown.length) {
    if (deniedCount > 0 && explicitCross) {
      return { error: false, exitCode: 3, text: '检测到 ' + deniedCount + ' 条越界访问已被拒绝。\n如需读取其它智能体私密记忆，请加 --unsafe（用户显式授权）或 --owner user。' };
    }
    return { error: false, exitCode: 0, text: '无匹配记忆。' };
  }
  const touchAll = shown.filter(function (h) { return !h.entry.immutable; }).map(function (h) { return h.entry.file; });
  let usageSkipped = 0;
  if (touchAll.length) {
    for (const root of roots) {
      const touchRel = touchAll.filter(function (rel) {
        if (!fs.existsSync(path.join(root, rel))) return false;
        const owner = ownerFromPrivatePath(root, path.join(root, rel));
        if (owner && owner !== selfAgent) { usageSkipped++; return false; }
        return true;
      });
      if (!touchRel.length) continue;
      const bump = bumpReadMeta(root, touchRel, { selfAgent: selfAgent, query: q, noUsage: !!opts.noUsage });
      touchIndex(root, touchRel, { years: years, usageByFile: bump.usageByFile });
    }
  }
  const lines = ['共 ' + shown.length + ' 条记忆（' + (hits.length > limit ? '前 ' + limit + ' 条' : '全部') + '）：'];
  if (!selfAgent) lines.push('[注意] 未声明身份，本次仅读取公共 FACT；私密 PREF / BOUND / COMMIT 已跳过。');
  for (const h of shown) {
    lines.push('[' + h.entry.type + '] ' + h.entry.subject + ': ' + h.entry.statement);
    lines.push('  ' + path.join(h.root, h.entry.file));
    if (wantExplain) {
      if (h.detail && h.detail.length) lines.push('    命中: ' + h.detail.join('、'));
      const ub = utilityBreakdown(h.entry);
      lines.push('    效用分: ' + round3(ub.total) + '（conf ' + ub.confidence + ' + 使用 ' + ub.usage + ' + 时效 ' + ub.recency + ' + 类型 ' + ub.type + ' + 结构 ' + ub.structure + '）×weight ' + ub.weight);
    }
  }
  if (deniedCount > 0 && explicitCross) {
    lines.push('\n[警告] 本次检索共拒绝 ' + deniedCount + ' 条越界访问（其它智能体私密记忆，未授权不展示）。如需读取请加 --unsafe 或 --owner user。');
  }
  if (usageSkipped > 0) {
    lines.push('\n[提示] 跨 owner 私密条目未记录命中打点（' + usageSkipped + ' 条）：只有条目所属 owner 才能更新自己的打点。');
  }
  return {
    error: false,
    exitCode: 0,
    text: lines.join('\n'),
    entries: shown.map(function (h) {
      return {
        root: h.root,
        file: h.entry.file,
        type: h.entry.type,
        subject: h.entry.subject,
        statement: h.entry.statement,
        score: h.finalScore === undefined ? h.score : h.finalScore
      };
    })
  };
}
function resolveMemoryFile(root, ref) {
  const map = {};
  for (const fp of collectEntryFiles(root)) {
    const rel = path.relative(root, fp).replace(/\\/g, '/');
    map[rel] = fp;
    const base = path.basename(rel);
    if (!map[base]) map[base] = fp;
  }
  if (map[ref]) return { fp: map[ref], rel: relOf(root, map[ref]) };
  const base = path.basename(ref.replace(/\\/g, '/'));
  if (map[base]) return { fp: map[base], rel: relOf(root, map[base]) };
  return null;
}
function relOf(root, fp) { return path.relative(root, fp).replace(/\\/g, '/'); }
function appendTrashAudit(root, record) {
  const dir = path.join(root, '.trash');
  fs.mkdirSync(dir, { recursive: true });
  fs.appendFileSync(path.join(dir, 'audit-' + today() + '.jsonl'), JSON.stringify(record) + '\n', 'utf8');
}

// v0.17.4：给单条记忆改名（消除「平铺 / 分层同序号」冲突的最小手段）。
// 身份键 = 类型 + owner + 文件名：目标名必须避开同身份占用，跨平铺 / 分层一起查；
// 走 destructiveGuardCore（doctor + 独立备份 + 事务快照），改名后重建索引并写审计。
function renameCore(fileRef, newName, opts) {
  opts = opts || {};
  const selfAgent = resolveIdentity(opts).id;
  const target = resolveMemoryTarget(fileRef);
  if (!target) return { error: true, text: '未找到记忆文件: ' + fileRef };
  const deny = checkOwnerWritable(target.root, target.rel, selfAgent, opts.unsafe);
  if (deny) return { error: true, text: deny };
  const name = String(newName || '').trim();
  if (!/^\d{4}-\d{2}-\d{2}-\d{4}\.md$/.test(name)) {
    return { error: true, text: '新文件名需形如 YYYY-MM-DD-NNNN.md（例：2026-09-25-0354.md）' };
  }
  const oldBase = path.basename(target.fp);
  if (name === oldBase) return { error: true, text: '新文件名与原名相同，无需改名。' };
  const owner = ownerFromPrivatePath(target.root, target.fp);
  let meta;
  try { meta = parseFrontmatter(readMemoryText(target.root, target.fp, owner)).meta; }
  catch (e) { return { error: true, text: '读取失败: ' + e.message }; }
  const type = (meta.type || 'FACT').toUpperCase();
  const conflicts = [];
  for (const fp of collectEntryFiles(target.root)) {
    if (fp === target.fp) continue;
    if (path.basename(fp) !== name) continue;
    const otherOwner = ownerFromPrivatePath(target.root, fp);
    if (otherOwner !== owner) continue;
    let otherMeta;
    try { otherMeta = parseFrontmatter(readMemoryText(target.root, fp, otherOwner)).meta; }
    catch (e) { conflicts.push(relOf(target.root, fp)); continue; }
    if ((otherMeta.type || 'FACT').toUpperCase() === type) conflicts.push(relOf(target.root, fp));
  }
  if (conflicts.length) {
    return { error: true, text: '目标文件名已被同 owner 同类型记忆占用，拒绝改名（跨平铺 / 分层检查）: ' + conflicts.join('、') };
  }
  const dest = path.join(path.dirname(target.fp), name);
  if (fs.existsSync(dest)) return { error: true, text: '目标文件已存在，拒绝覆盖: ' + relOf(target.root, dest) };
  const destRel = relOf(target.root, dest);
  if (opts.dryRun) {
    return { error: false, text: '预览（未改动）: ' + target.rel + ' → ' + destRel };
  }
  const guard = destructiveGuardCore({
    root: target.root,
    action: 'rename',
    snapshotDir: opts.snapshotDir,
    backupDir: opts.backupDir,
    allowSameVolumeForTest: opts.allowSameVolumeForTest,
    sameVolumeFn: opts.sameVolumeFn,
    now: opts.now,
  });
  if (guard.error) return { error: true, text: guard.text };
  try {
    fs.renameSync(target.fp, dest);
  } catch (e) {
    return { error: true, text: '改名失败，原文件未动: ' + e.message };
  }
  try {
    removeIndexEntry(target.root, target.rel);
    buildIndex(target.root);
  } catch (e) { /* 索引失败不回滚文件改名；下一次 reindex 会重建 */ }
  appendAudit(target.root, 'audit', {
    ts: new Date().toISOString(),
    file: target.rel,
    action: 'rename',
    to: destRel,
    reason: opts.reason ? String(opts.reason) : '',
  });
  return { error: false, text: '已改名: ' + target.rel + ' → ' + destRel + '\n事务快照: ' + guard.snapshot.id };
}

function forgetCore(fileRef, opts) {
  opts = opts || {};
  const selfAgent = opts.userUnlocked ? '' : resolveIdentity(opts).id;
  const roots = opts.root ? [path.resolve(String(opts.root))] : memoryRoots();
  const ref = String(fileRef || '').replace(/\\/g, '/');
  let target = null, targetRoot = null, targetRel = null;
  for (const root of roots) {
    const found = resolveMemoryFile(root, ref);
    if (found) { target = found.fp; targetRoot = root; targetRel = found.rel; break; }
  }
  if (!target) return { error: true, text: '未找到记忆文件: ' + fileRef };
  const seg = targetRel.replace(/\\/g, '/').split('/');
  if (seg[0] === 'private') {
    const owner = seg[1] || '';
    if (!opts.userUnlocked && !opts.unsafe && (owner && (selfAgent ? owner !== selfAgent : true))) {
      return { error: true, text: '拒绝: 不能删除其它智能体 ' + owner + ' 的私密记忆（当前身份 ' + (selfAgent || '未声明') + '）。请用 --agent / --agent-id 声明自己的身份，或加 --unsafe（用户显式授权）。' };
    }
  }
  const trashFile = path.join(
    targetRoot,
    '.trash',
    new Date().toISOString().replace(/[:.]/g, '-'),
    targetRel,
  );
  try {
    fs.mkdirSync(path.dirname(trashFile), { recursive: true });
    fs.renameSync(target, trashFile);
  } catch (error) {
    return { error: true, text: '召回区写入失败，原记忆未删除: ' + error.message };
  }
  if (targetRoot) removeIndexEntry(targetRoot, targetRel);
  if (targetRoot) {
    appendTrashAudit(targetRoot, {
      ts: new Date().toISOString(),
      action: 'forget',
      file: targetRel,
      trash: relOf(targetRoot, trashFile),
      owner: ownerFromPrivatePath(targetRoot, target),
      selfAgent,
    });
  }
  return { error: false, text: '已移入回收区: ' + trashFile, trash: relOf(targetRoot, trashFile) };
}
// ---- v0.18.0 A3：容量水位 / 淘汰候选 / 晋升建议（只读报告，不自动动数据）----
const CAPACITY_CONFIG_DEFAULTS = {
  capacity_warn_bytes: 50 * 1024 * 1024,
  capacity_cooldown_days: 30,
  capacity_candidate_limit: 20,
  promotion_min_hits: 3,
  promotion_min_queries: 3,
};
function capacityNumber(cfg, key) {
  const raw = cfg ? cfg[key] : undefined;
  if (raw === undefined || raw === null || raw === '') return CAPACITY_CONFIG_DEFAULTS[key];
  const n = parseFloat(raw);
  return (n >= 0) ? n : CAPACITY_CONFIG_DEFAULTS[key];
}
function isEvergreenTagged(meta) {
  // tags 在真实库里可能是 JSON 数组串（["pinned"]），parseTags 会保留引号，这里统一去掉再比较。
  const tags = parseTags(meta && meta.tags).map(function (t) {
    return String(t).toLowerCase().replace(/^["']|["']$/g, '');
  });
  return tags.indexOf('evergreen') !== -1 || tags.indexOf('pinned') !== -1;
}
function capacityMemoryBytes(root) {
  let total = 0;
  for (const fp of collectEntryFiles(root)) {
    try { total += fs.statSync(fp).size; } catch (e) { /* 单文件缺失不影响整体水位 */ }
  }
  return total;
}
function capacityCandidateRow(e) {
  return {
    file: e.file,
    type: e.type,
    subject: e.subject,
    hits_30d: e.hits_30d,
    hits_90d: e.hits_90d,
    last_used: e.last_used,
    age_days: e.age_days,
    utility: e.utility,
    suggested_command: 'yotta-memory explain ' + e.file,
  };
}
function capacityCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.root || userRoot());
  if (!fs.existsSync(root)) return { error: false, text: '记忆库不存在。', report: null };
  const cfg = loadConfig();
  const selfAgent = (opts.selfAgent !== undefined) ? opts.selfAgent : resolveIdentity(opts).id;
  const cooldownDays = capacityNumber(cfg, 'capacity_cooldown_days');
  const limit = (opts.limit !== undefined && opts.limit !== null)
    ? (parseInt(opts.limit, 10) || 0)
    : capacityNumber(cfg, 'capacity_candidate_limit');
  const minHits = capacityNumber(cfg, 'promotion_min_hits');
  const minQueries = capacityNumber(cfg, 'promotion_min_queries');
  const skipped = { cooldown: 0, evergreen: 0, denied: 0, unreadable: 0 };
  const activityBase = [];
  const candidatesForCleanup = [];
  for (const fp of collectEntryFiles(root)) {
    const r = relOf(root, fp);
    if (checkOwnerWritable(root, r, selfAgent, opts.unsafe)) { skipped.denied++; continue; }
    let e;
    try { e = readEntry(fp, root); } catch (err) { skipped.unreadable++; continue; }
    e.hits_30d = usageTotals(e, 30);
    e.hits_90d = usageTotals(e, 90);
    e.last_used = e.last_accessed || e.created || '';
    e.age_days = e.created ? daysBetween(e.created, today()) : -1;
    e.utility = round3(utilityScore(e.meta));
    activityBase.push(e);
    if (e.immutable || e.type === 'BOUND' || isEvergreenTagged(e.meta)) { skipped.evergreen++; continue; }
    if (e.age_days >= 0 && e.age_days < cooldownDays) { skipped.cooldown++; continue; }
    candidatesForCleanup.push(e);
  }
  const byOldest = function (a, b) {
    const la = a.last_used || '', lb = b.last_used || '';
    if (la !== lb) return la.localeCompare(lb);
    return String(a.file).localeCompare(String(b.file));
  };
  const lru = candidatesForCleanup.slice().sort(byOldest).slice(0, limit).map(capacityCandidateRow);
  const lfu = candidatesForCleanup.slice().sort(function (a, b) {
    if (a.hits_90d !== b.hits_90d) return a.hits_90d - b.hits_90d;
    return byOldest(a, b);
  }).slice(0, limit).map(capacityCandidateRow);
  const promotions = candidatesForCleanup.filter(function (e) {
    if (e.hits_90d < minHits) return false;
    if (Object.keys(parseHitQueries(e.hit_queries)).length < minQueries) return false;
    if (e.weight >= 1.5) return false;
    if (isConsolidatedSummary(e)) return false;
    return true;
  }).map(function (e) {
    const row = capacityCandidateRow(e);
    row.distinct_queries = Object.keys(parseHitQueries(e.hit_queries)).length;
    row.suggested_command = 'yotta-memory feedback ' + e.file + ' --useful';
    return row;
  });
  const scale = scaleReport(root, cfg);
  const memoryBytes = capacityMemoryBytes(root);
  const warnBytes = capacityNumber(cfg, 'capacity_warn_bytes');
  const infoBytes = warnBytes * 0.6;
  const memoryLevel = memoryBytes > warnBytes ? 'warning' : (memoryBytes > infoBytes ? 'info' : 'ok');
  const waterLevel = (scale.level === 'warning' || memoryLevel === 'warning')
    ? 'warning'
    : ((scale.level === 'info' || memoryLevel === 'info') ? 'info' : 'ok');
  const thresholds = Object.assign({}, scale.thresholds, {
    capacity_warn_bytes: warnBytes,
    capacity_cooldown_days: cooldownDays,
    capacity_candidate_limit: limit,
    promotion_min_hits: minHits,
    promotion_min_queries: minQueries,
  });
  const water = {
    entries: scale.entries,
    files_per_dir: scale.files_per_dir,
    index_bytes: scale.index_bytes,
    cold_start_ms: scale.cold_start_ms,
    memory_bytes: memoryBytes,
    thresholds: thresholds,
    metrics: scale.metrics.concat([{
      key: 'memory_bytes', value: memoryBytes, unit: '字节', info: infoBytes, warn: warnBytes, level: memoryLevel,
    }]),
    level: waterLevel,
  };
  const activity = {
    readable: activityBase.length,
    hits_30d_entries: activityBase.filter(function (e) { return e.hits_30d > 0; }).length,
    hits_90d_entries: activityBase.filter(function (e) { return e.hits_90d > 0; }).length,
    never_hit: activityBase.filter(function (e) { return e.hits_90d === 0 && (parseInt(e.access_count, 10) || 0) === 0; }).length,
    top: activityBase.filter(function (e) { return e.hits_90d > 0; })
      .sort(function (a, b) {
        if (b.hits_90d !== a.hits_90d) return b.hits_90d - a.hits_90d;
        return byOldest(a, b);
      })
      .slice(0, Math.min(limit, 10))
      .map(capacityCandidateRow),
  };
  const lines = ['## yotta-memory maintain --capacity（容量水位）'];
  const waterLabel = waterLevel === 'warning' ? '告警' : (waterLevel === 'info' ? '提示' : '正常');
  lines.push('- 水位: ' + waterLabel
    + '（条目 ' + scale.entries + ' / 记忆文件 ' + memoryBytes + ' 字节（阈值 ' + warnBytes + '）'
    + ' / 索引 ' + scale.index_bytes + ' 字节 / 单目录最大 ' + scale.files_per_dir + ' 个文件 / 冷启动 ' + scale.cold_start_ms + 'ms）');
  lines.push('- 活跃度: 可读 ' + activity.readable + ' 条；30 天命中 ' + activity.hits_30d_entries
    + ' 条 / 90 天命中 ' + activity.hits_90d_entries + ' 条 / 无命中记录 ' + activity.never_hit + ' 条');
  lines.push('');
  lines.push('### LRU 淘汰候选（最久未用，' + lru.length + ' 条）');
  if (!lru.length) lines.push('（无）');
  for (const row of lru) {
    lines.push('- [' + row.type + '] ' + row.file + '（90 天命中 ' + row.hits_90d + '，' + row.age_days + ' 天龄，utility ' + row.utility + '）— ' + row.subject);
  }
  lines.push('');
  lines.push('### LFU 淘汰候选（命中最少，' + lfu.length + ' 条）');
  if (!lfu.length) lines.push('（无）');
  for (const row of lfu) {
    lines.push('- [' + row.type + '] ' + row.file + '（90 天命中 ' + row.hits_90d + '，最久未用 ' + row.last_used + '）— ' + row.subject);
  }
  lines.push('');
  lines.push('### 晋升建议（只出建议，不自动改权重，' + promotions.length + ' 条）');
  if (!promotions.length) lines.push('（无：需要 90 天命中 ≥ ' + minHits + ' 且不同查询 ≥ ' + minQueries + ' 且 weight < 1.5）');
  for (const row of promotions) {
    lines.push('- ' + row.file + '（90 天命中 ' + row.hits_90d + '，不同查询 ' + row.distinct_queries + '）→ ' + row.suggested_command);
  }
  lines.push('');
  lines.push('### 跳过（不进候选）');
  lines.push('- 冷却期（<' + cooldownDays + ' 天）: ' + skipped.cooldown + ' 条 / 常青（immutable、BOUND、evergreen、pinned）: '
    + skipped.evergreen + ' 条 / 其它 owner: ' + skipped.denied + ' 条 / 无法读取: ' + skipped.unreadable + ' 条');
  lines.push('- 本命令只读：不改记忆、不改权重；归档请显式执行 yotta-memory archive。');
  const report = {
    schemaVersion: 1,
    root: root,
    thresholds: thresholds,
    water: water,
    activity: activity,
    candidates: { lru: lru, lfu: lfu },
    promotions: promotions,
    skipped: skipped,
  };
  return { error: false, text: lines.join('\n'), report: report };
}
function archiveCore(opts) {
  opts = opts || {};
  const cfg = loadConfig();
  const days = opts.days || parseInt(cfg.maintain_archived_age || '180', 10) || 180;
  const threshold = (opts.threshold !== undefined && opts.threshold !== null) ? opts.threshold : (parseFloat(cfg.maintain_archived_utility || ARCHIVE_UTILITY_DEFAULT));
  const cooldownDays = capacityNumber(cfg, 'capacity_cooldown_days');
  const root = userRoot();
  if (!fs.existsSync(root)) return { error: false, text: '记忆库不存在。' };
  const dryRun = !!opts.dryRun;
  const force = !!opts.force;
  const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
  const selfAgent = resolveIdentity(opts).id;
  // v0.18.0 修正：先只读扫描候选与跳过统计，再决定要不要过破坏性闸门 ——
  // 预演（--dry-run）与「没有候选」两种情况下都不写盘。
  // 旧行为是进门就建整库快照 + 写审计，且 --dry-run 标志被静默吞掉（照常归档）。
  const candidates = [];
  let deniedCrossOwner = 0;
  let skippedCooldown = 0;
  let skippedEvergreen = 0;
  for (const fp of collectEntryFiles(root)) {
    const owner = ownerFromPrivatePath(root, fp);
    // v0.17.2：只归档自己有权写的条目 —— 旧行为遍历全部 owner，
    // 任何身份都能把别的智能体的私密记忆移进归档区。
    if (checkOwnerWritable(root, relOf(root, fp), selfAgent, opts.unsafe)) {
      deniedCrossOwner++;
      continue;
    }
    let meta;
    try { meta = parseFrontmatter(readMemoryText(root, fp, owner)).meta; } catch (e) { continue; }
    if (meta.immutable === 'true') continue;
    if (!meta.created) continue;
    const createdTs = new Date(meta.created).getTime();
    if (isNaN(createdTs)) continue;
    const t = (meta.type || 'FACT').toUpperCase();
    if (t === 'BOUND') continue; // v0.10.0 BOUND 豁免归档（边界常驻）
    if (!force && isEvergreenTagged(meta)) { skippedEvergreen++; continue; }
    const ageDays = meta.created ? daysBetween(meta.created, today()) : -1;
    if (!force && ageDays >= 0 && ageDays < cooldownDays) { skippedCooldown++; continue; }
    // v0.8.0 统一效用分（盖棺分）替代 vitality
    const score = utilityScore(meta);
    if (score < threshold && createdTs < cutoff) {
      candidates.push({
        fp: fp,
        owner: owner,
        entry: {
          file: relOf(root, fp),
          type: t,
          subject: String(meta.subject || ''),
          age_days: ageDays,
          utility: round3(score),
        },
      });
    }
  }
  const skippedLines = [];
  if (deniedCrossOwner) {
    skippedLines.push('跨 owner 私密条目已跳过（' + deniedCrossOwner + ' 条）：请用 --agent <id> 声明自己的身份；只有用户显式授权（--unsafe）才能越界维护。');
  }
  if (skippedCooldown || skippedEvergreen) {
    skippedLines.push('因冷却期 / 常青豁免跳过 ' + (skippedCooldown + skippedEvergreen) + ' 条（冷却期 ' + skippedCooldown + ' / 常青 ' + skippedEvergreen + '）；确认要一并归档时加 --force（immutable 与 BOUND 仍豁免）。');
  }
  const report = {
    schemaVersion: 1,
    root: root,
    mode: dryRun ? 'dry-run' : 'apply',
    days: days,
    threshold: threshold,
    cooldown_days: cooldownDays,
    force: force,
    candidates: candidates.map(function (c) { return c.entry; }),
    archived: [],
    skipped: { cooldown: skippedCooldown, evergreen: skippedEvergreen, cross_owner: deniedCrossOwner },
  };
  if (dryRun) {
    // 预演只读：不动文件、不建事务快照、不写审计、不改索引。
    const lines = ['预览（未改动）: 将归档 ' + candidates.length + ' 条旧记忆到 ' + path.join(root, ARCHIVE_DIR)];
    lines.push('- 判定: 效用 < ' + threshold + ' 且未使用 > ' + days + ' 天' + (force
      ? '（--force：冷却期与常青标签不再豁免）'
      : '（冷却期 ' + cooldownDays + ' 天内与 immutable / BOUND / evergreen / pinned 豁免）'));
    for (const c of candidates) {
      lines.push('- [' + c.entry.type + '] ' + c.entry.file + '（' + c.entry.age_days + ' 天龄，utility ' + c.entry.utility + '）— ' + c.entry.subject);
    }
    if (!candidates.length) lines.push('（无符合条件的记忆）');
    lines.push('- 预演只读：未创建事务快照、未写审计、未移动文件；去掉 --dry-run 才执行（执行前先过破坏性写入闸门：doctor + 独立备份目录 + 异卷）。');
    lines.push.apply(lines, skippedLines);
    return { error: false, dryRun: true, text: lines.join('\n'), report: report };
  }
  if (!candidates.length) {
    // 无候选 = 无写入：不创建整库事务快照，也不写审计。
    const lines = ['已归档 0 条旧记忆到 ' + path.join(root, ARCHIVE_DIR), '没有符合条件的记忆：未创建事务快照（无写入）。'];
    lines.push.apply(lines, skippedLines);
    return { error: false, text: lines.join('\n'), report: report };
  }
  const guard = destructiveGuardCore({
    root: root,
    action: 'archive',
    snapshotDir: opts.snapshotDir,
    backupDir: opts.backupDir,
    allowSameVolumeForTest: opts.allowSameVolumeForTest,
    sameVolumeFn: opts.sameVolumeFn,
    now: opts.now,
  });
  if (guard.error) return { error: true, text: guard.text };
  const movedFiles = [];
  for (const c of candidates) {
    const dest = path.join(root, archiveRelFor(root, c.entry.file, c.entry.type, c.owner));
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.renameSync(c.fp, dest);
    movedFiles.push(c.entry.file);
  }
  if (movedFiles.length) removeIndexEntries(root, movedFiles);
  report.archived = movedFiles;
  let text = '已归档 ' + movedFiles.length + ' 条旧记忆到 ' + path.join(root, ARCHIVE_DIR) + '\n事务快照: ' + guard.snapshot.id;
  if (skippedLines.length) text += '\n' + skippedLines.join('\n');
  return { error: false, text: text, report: report };
}

// ---- v0.8.0 自我学习/自我进化/自我提升：feedback / explain / maintain / distill ----
function auditPath(root, kind) {
  return path.join(root, ARCHIVE_DIR, kind + '-' + today() + '.jsonl');
}
function appendAudit(root, kind, rec) {
  try {
    fs.mkdirSync(path.join(root, ARCHIVE_DIR), { recursive: true });
    fs.appendFileSync(auditPath(root, kind), JSON.stringify(rec) + '\n', 'utf8');
    return true;
  } catch (e) { return false; }
}
function resolveMemoryTarget(ref) {
  const roots = memoryRoots();
  const targetRef = String(ref || '').replace(/\\/g, '/');
  for (const root of roots) {
    const found = resolveMemoryFile(root, targetRef);
    if (found) return { fp: found.fp, root: root, rel: found.rel };
  }
  return null;
}
function checkOwnerWritable(targetRoot, targetRel, selfAgent, unsafe) {
  const seg = String(targetRel).split('/');
  if (seg[0] === PRIVATE_DIR) {
    const owner = seg[1] || '';
    if (!unsafe && (owner && (selfAgent ? owner !== selfAgent : true))) {
      return '拒绝: 不能操作其它智能体 ' + owner + ' 的私密记忆（当前身份 ' + (selfAgent || '未声明') + '）。请用 --agent / --agent-id 声明自己的身份，或加 --unsafe（用户显式授权）。';
    }
  }
  return null;
}
// 显式使用反馈：useful/useless → weight/confidence/feedback_net 演化（自我学习闭环）
function feedbackCore(ref, opts) {
  opts = opts || {};
  const selfAgent = resolveIdentity(opts).id;
  const target = resolveMemoryTarget(ref);
  if (!target) return { error: true, text: '未找到记忆文件: ' + ref };
  const deny = checkOwnerWritable(target.root, target.rel, selfAgent, opts.unsafe);
  if (deny) return { error: true, text: deny };
  const owner = ownerFromPrivatePath(target.root, target.fp);
  let meta;
  try { meta = parseFrontmatter(readMemoryText(target.root, target.fp, owner)).meta; } catch (e) { return { error: true, text: '读取失败: ' + e.message }; }
  if (opts.undo) {
    return feedbackUndoCore(target, owner, meta, selfAgent, opts);
  }
  const useful = !!opts.useful;
  const useless = !!opts.useless;
  if (!useful && !useless) return { error: true, text: '请指定 --useful（有用）或 --useless（没用）。' };
  const cfg = loadConfig();
  const stepW = parseFloat(cfg.feedback_weight_step || 0.2);
  const stepC = parseFloat(cfg.feedback_confidence_step || 0.05);
  const w = parseFloat(meta.weight || '1.0'); const weight = (w > 0 ? w : 1.0);
  const conf = parseFloat(meta.confidence || '1.0'); const confidence = (conf > 0 ? conf : 1.0);
  const fb = feedbackNetOf(meta);
  let nw = weight, nc = confidence, nfb = fb;
  if (useful) { nw = Math.min(weight * (1 + stepW), 3.0); nc = Math.min(confidence + stepC, 1.0); nfb = fb + 1; }
  if (useless) { nw = Math.max(weight * (1 - stepW), 0.2); nc = Math.max(confidence - stepC, 0.3); nfb = fb - 1; }
  const before = { weight: round3(weight), confidence: round3(confidence), feedback_net: fb };
  const after = { weight: round3(nw), confidence: round3(nc), feedback_net: nfb };
  const patch = { weight: after.weight, confidence: after.confidence, feedback_net: after.feedback_net, updated: today() };
  if (useful) {
    const usageCfg = usageSettings(opts);
    if (usageCfg.enabled) Object.assign(patch, usagePatchForMeta(meta, 'use', '', usageCfg, today()));
  }
  rewriteFrontmatter(target.fp, patch, target.root, owner);
  upsertIndexEntry(target.root, readEntry(target.fp, target.root));
  appendAudit(target.root, 'feedback', { ts: new Date().toISOString(), file: target.rel, action: useful ? 'useful' : 'useless', before: before, after: after, reason: opts.reason || '' });
  const lines = [(useful ? '已反馈 [有用]' : '已反馈 [没用]') + ': ' + target.rel];
  lines.push('  weight ' + before.weight + ' -> ' + after.weight + ' / confidence ' + before.confidence + ' -> ' + after.confidence + ' / feedback_net ' + before.feedback_net + ' -> ' + after.feedback_net);
  if (opts.reason) lines.push('  原因: ' + opts.reason);
  lines.push('  提示: yotta-memory explain ' + target.rel + ' 查看效用分项；feedback --undo 回滚最近一次');
  return { error: false, text: lines.join('\n') };
}
function feedbackUndoCore(target, owner, meta, selfAgent, opts) {
  const cfg = loadConfig();
  const lines = [];
  let restored = false;
  try {
    const log = auditPath(target.root, 'feedback');
    if (!fs.existsSync(log)) return { error: true, text: '无可回滚的反馈记录（' + log + ' 不存在）。' };
    const recs = fs.readFileSync(log, 'utf8').split('\n').filter(Boolean).map(function (l) { try { return JSON.parse(l); } catch (e) { return null; } }).filter(Boolean);
    const mine = recs.filter(function (r) { return r.file === target.rel && (r.action === 'useful' || r.action === 'useless'); });
    if (!mine.length) return { error: true, text: '该文件无反馈记录可回滚。' };
    const last = mine[mine.length - 1];
    const patch = { weight: last.before.weight, confidence: last.before.confidence, feedback_net: last.before.feedback_net, updated: today() };
    rewriteFrontmatter(target.fp, patch, target.root, owner);
    upsertIndexEntry(target.root, readEntry(target.fp, target.root));
    appendAudit(target.root, 'feedback', { ts: new Date().toISOString(), file: target.rel, action: 'undo', before: last.after, after: last.before, reason: opts.reason || '' });
    lines.push('已回滚最近一次反馈: ' + target.rel);
    lines.push('  ' + last.action + ' -> 恢复 weight ' + last.after.weight + ' -> ' + last.before.weight + ' / feedback_net ' + last.after.feedback_net + ' -> ' + last.before.feedback_net);
    restored = true;
  } catch (e) { return { error: true, text: '回滚失败: ' + e.message }; }
  return { error: false, text: lines.join('\n') };
}
// 解释单条记忆效用分项（为什么靠前/归档/遗忘）
function explainCore(ref, opts) {
  opts = opts || {};
  const selfAgent = resolveIdentity(opts).id;
  const target = resolveMemoryTarget(ref);
  if (!target) return { error: true, text: '未找到记忆文件: ' + ref };
  const owner = ownerFromPrivatePath(target.root, target.fp);
  let entry;
  try { entry = readEntry(target.fp, target.root); } catch (e) { return { error: true, text: '读取失败: ' + e.message }; }
  const deny = checkOwnerWritable(target.root, target.rel, selfAgent, opts.unsafe);
  // v0.17.2：跨 owner 私密条目 fail-closed —— 旧行为只是加一句「仅元数据」，
  // 正文（subject / statement）照样输出，等于把别人的私密记忆读给调用方。
  if (deny) return { error: true, text: deny };
  applyUsageHits(target.root, [target.rel], 'get', '', { selfAgent: selfAgent, noUsage: !!opts.noUsage });
  const ub = utilityBreakdown(entry);
  const ageDays = entry.created ? daysBetween(entry.created, today()) : 0;
  const cfg = loadConfig();
  const hlText = entry.type === 'BOUND' ? 'BOUND 不衰减' : (decayHalflifeDays(entry.type, cfg) + ' 天');
  const archU = parseFloat(cfg.maintain_archived_utility || ARCHIVE_UTILITY_DEFAULT);
  const archAge = parseInt(cfg.maintain_archived_age || '180', 10) || 180;
  const forgetU = parseFloat(cfg.maintain_forget_utility || 0.12);
  const forgetAge = parseInt(cfg.maintain_forget_age || '365', 10) || 365;
  const lines = ['[' + entry.type + '] ' + entry.subject + ': ' + entry.statement];
  lines.push('  文件: ' + target.rel);
  lines.push('  效用分: ' + ub.total + ' = confidence ' + ub.confidence + ' + 使用 ' + ub.usage + ' + 时效 ' + ub.recency + '（半衰 ' + hlText + '） + 类型 ' + ub.type + ' + 结构 ' + ub.structure + '）×weight ' + ub.weight);
  lines.push('  年龄: ' + ageDays + ' 天 / access_count ' + (entry.access_count || 0) + ' / feedback_net ' + entry.feedback_net + ' / immutable ' + (entry.immutable ? '是' : '否'));
  const importScore = round3(importanceScore(entry));
  lines.push('  importance(旧): ' + importScore + ' / vitality(旧): ' + round3(vitality(entry)));
  if (entry.immutable) lines.push('  状态: immutable 豁免自动归档/遗忘');
  else if (entry.type === 'BOUND') lines.push('  状态: BOUND 豁免归档/遗忘（边界常驻）');
  else if (ub.total < forgetU && ageDays > forgetAge) lines.push('  状态: 遗忘候选（utility < ' + forgetU + ' 且年龄 > ' + forgetAge + ' 天；--purge 才真删）');
  else if (ub.total < archU && ageDays > archAge) lines.push('  状态: 归档候选（utility < ' + archU + ' 且年龄 > ' + archAge + ' 天）');
  else lines.push('  状态: 保留（未达归档/遗忘阈值）');
  return { error: false, text: lines.join('\n') };
}
function jaccardTokens(a, b) {
  const sa = new Set(Object.keys(a.tokens || {}).filter(function (k) { return k.indexOf(':') === -1; }));
  const sb = new Set(Object.keys(b.tokens || {}).filter(function (k) { return k.indexOf(':') === -1; }));
  if (!sa.size || !sb.size) return 0;
  let inter = 0;
  for (const k of sa) { if (sb.has(k)) inter++; }
  const union = sa.size + sb.size - inter;
  return union ? inter / union : 0;
}
function subjectsSimilar(a, b) {
  const sa = String(a.subject || '').toLowerCase();
  const sb = String(b.subject || '').toLowerCase();
  if (!sa || !sb) return false;
  if (sa === sb) return true;
  return editDistance(sa, sb) <= 3;
}
// 记忆自组织：规则层自动归档/遗忘/去重（默认 dry-run，--apply 才执行，--purge 才真删）
// ---- v0.18.1 A10：重复踩坑 → 建议升级为规则（只读报告）----
function normalizeRuleSubject(s) {
  return String(s || '').toLowerCase().replace(/[^\u4e00-\u9fa5a-z]+/g, '');
}
function ruleGroupKeyFor(entry) {
  for (const t of (entry.tags || [])) {
    const m = /^pattern-key:(.+)$/i.exec(String(t));
    if (m) return { key: 'pattern-key:' + m[1].trim(), kind: 'pattern-key' };
  }
  const sm = /^yotta-learn:\s*(.+)$/i.exec(String(entry.subject || ''));
  const cm = /^\[([a-z_]+)\]/i.exec(String(entry.statement || '').trim());
  if (sm && cm) return { key: cm[1].toLowerCase() + '@' + sm[1].trim(), kind: 'yotta-learn' };
  const domains = (entry.tags || []).filter(function (t) {
    return !distillHasWord(t, DISTILL_LESSON_WORDS) && !/^pattern-key:/i.test(String(t)) && String(t) !== '规则' && String(t) !== '边界';
  }).map(function (t) { return String(t).toLowerCase(); }).sort();
  if (domains.length) return { key: domains.join('+'), kind: 'tags' };
  return { key: normalizeRuleSubject(entry.subject), kind: 'subject' };
}
function isRuleLessonCandidate(entry) {
  const hay = (entry.tags || []).join(',') + ' ' + String(entry.subject || '');
  if (distillHasWord(hay, DISTILL_LESSON_WORDS)) return true;
  const head = String(entry.statement || '').trim().slice(0, 40);
  return /^\[([a-z_]+)\]/i.test(head) && distillHasWord(head, DISTILL_LESSON_WORDS);
}
function ruleMiningCore(root, opts) {
  opts = opts || {};
  const cfg = loadConfig();
  const rawMin = (opts.ruleMinHits !== undefined && opts.ruleMinHits !== null) ? opts.ruleMinHits : cfg.maintain_rule_min_hits;
  const minHits = Math.max(2, parseInt(rawMin || '3', 10) || 3);
  const selfAgent = resolveIdentity(opts).id;
  const buckets = {};
  let scanned = 0, candidates = 0, denied = 0;
  for (const fp of collectEntryFiles(root)) {
    const rel = relOf(root, fp);
    if (checkOwnerWritable(root, rel, selfAgent, opts.unsafe)) { denied += 1; continue; }
    let e;
    try { e = readEntry(fp, root); } catch (err) { continue; }
    scanned += 1;
    if (['COMMIT', 'FACT', 'PREF'].indexOf(e.type) === -1) continue;
    if (!isRuleLessonCandidate(e)) continue;
    const gk = ruleGroupKeyFor(e);
    if (!gk.key) continue;
    candidates += 1;
    (buckets[gk.key] = buckets[gk.key] || []).push({ e: e, kind: gk.kind, file: rel });
  }
  const groups = Object.keys(buckets).map(function (key) {
    const items = buckets[key].slice().sort(function (a, b) {
      return String(b.e.updated || b.e.created || '').localeCompare(String(a.e.updated || a.e.created || ''));
    });
    const best = items.slice().sort(function (a, b) { return (b.e.confidence || 0) - (a.e.confidence || 0); })[0].e;
    const dates = items.map(function (x) { return x.e.created || x.e.updated || ''; }).filter(Boolean).sort();
    return {
      key: key,
      kind: items[0].kind,
      count: items.length,
      files: items.map(function (x) { return x.file; }),
      span: dates.length ? dates[0] + ' ~ ' + dates[dates.length - 1] : '',
      best: best,
    };
  }).filter(function (g) { return g.count >= minHits; }).sort(function (a, b) {
    return b.count - a.count || a.key.localeCompare(b.key);
  });
  return { error: false, groups: groups, scanned: scanned, candidates: candidates, denied: denied, minHits: minHits };
}
function ruleMiningLines(result) {
  const lines = ['### 建议升级为规则（只读，不自动写入）'];
  if (!result.groups.length) {
    lines.push('- （无重复踩坑组达到阈值：同组 ≥ ' + result.minHits + ' 条；可用 config set maintain_rule_min_hits N 调整）');
    return lines;
  }
  for (const g of result.groups) {
    lines.push('- 组键: ' + g.key + '（' + g.count + ' 条' + (g.span ? '，' + g.span : '') + '）');
    lines.push('  代表: [' + g.best.type + '] ' + (g.best.subject || '') + ' — ' + String(g.best.statement || '').slice(0, 60));
    lines.push('  建议: 人工确认后执行 yotta-memory remember BOUND "规则：' + g.key + '" "<陈述>"');
  }
  lines.push('- 说明: 元忆只给晋升信号，不自动写 BOUND；与元习 .learnings/ 的分工见 SKILL「记忆守则」。');
  return lines;
}

function maintainCore(opts) {
  opts = opts || {};
  const apply = !!opts.apply;
  const purge = !!opts.purge;
  const root = userRoot();
  if (!fs.existsSync(root)) return { error: false, text: '记忆库不存在。' };
  if (opts.rules && (apply || purge || opts.dedup)) {
    return { error: true, exitCode: 2, text: '拒绝: --rules 是只读筛选，不能与 --apply / --purge / --dedup 同时使用。' };
  }
  if (opts.rules) {
    const lines = ['## yotta-memory maintain --rules（重复踩坑 → 规则晋升建议）', ''];
    const result = ruleMiningCore(root, opts);
    lines.push.apply(lines, ruleMiningLines(result));
    return { error: false, text: lines.join('\n'), report: result };
  }
  let guard = null;
  if (apply) {
    guard = destructiveGuardCore({
      root: root,
      action: opts.dedup ? 'maintain --dedup --apply' : (purge ? 'maintain --apply --purge' : 'maintain --apply'),
      snapshotDir: opts.snapshotDir,
      backupDir: opts.backupDir,
      allowSameVolumeForTest: opts.allowSameVolumeForTest,
      sameVolumeFn: opts.sameVolumeFn,
      now: opts.now,
    });
    if (guard.error) return { error: true, text: guard.text };
  }
  const cfg = loadConfig();
  const archU = parseFloat(opts.threshold !== undefined && opts.threshold !== null ? opts.threshold : (cfg.maintain_archived_utility || ARCHIVE_UTILITY_DEFAULT));
  const archAge = parseInt(opts.age || cfg.maintain_archived_age || '180', 10) || 180;
  const forgetU = parseFloat(cfg.maintain_forget_utility || 0.12);
  const forgetAge = parseInt(cfg.maintain_forget_age || '365', 10) || 365;
  const mode = opts.dedup ? (apply ? '查重执行（--dedup --apply 只自动合并高置信重复组，不执行归档/遗忘）' : '查重预览（--dedup；不执行归档/遗忘）') : (apply ? (purge ? '执行（含遗忘真删 --purge）' : '执行') : '预览（dry-run，未改动；加 --apply 执行，--purge 才真删）');
  const lines = ['## yotta-memory maintain（记忆自组织）'];
  lines.push('- 模式: ' + mode);
  lines.push('- 归档阈值: utility < ' + archU + ' 且年龄 > ' + archAge + ' 天；遗忘阈值: utility < ' + forgetU + ' 且年龄 > ' + forgetAge + ' 天');
  if (guard) lines.push('- 事务快照: ' + guard.snapshot.id);
  lines.push('');
  const toArchive = [], toForget = [], skipped = [];
  const selfAgent = resolveIdentity(opts).id;
  let deniedCrossOwner = 0;
  for (const fp of collectEntryFiles(root)) {
    const owner = ownerFromPrivatePath(root, fp);
    // v0.17.2：跨 owner 私密条目默认跳过（旧行为会遍历全部 owner 做归档 / 遗忘）。
    if (checkOwnerWritable(root, relOf(root, fp), selfAgent, opts.unsafe)) {
      deniedCrossOwner++;
      continue;
    }
    let meta;
    try { meta = parseFrontmatter(readMemoryText(root, fp, owner)).meta; } catch (e) { continue; }
    if (meta.immutable === 'true') { skipped.push({ fp: fp, reason: 'immutable 豁免' }); continue; }
    if (!meta.created) { skipped.push({ fp: fp, reason: '无 created' }); continue; }
    const type = (meta.type || 'FACT').toUpperCase();
    const ageDays = daysBetween(meta.created, today());
    const u = utilityScore(meta);
    const rec = { fp: fp, rel: relOf(root, fp), type: type, ageDays: ageDays, utility: u, meta: meta, owner: owner };
    if (u < forgetU && ageDays > forgetAge) {
      if (type === 'BOUND') { skipped.push({ fp: fp, reason: 'BOUND 豁免遗忘' }); }
      else { toForget.push(rec); continue; }
    }
    if (u < archU && ageDays > archAge) {
      if (type === 'BOUND') skipped.push({ fp: fp, reason: 'BOUND 豁免归档' });
      else toArchive.push(rec);
    }
  }
  let archived = 0, forgotten = 0;
  if (toArchive.length) {
    lines.push('### 归档候选（' + toArchive.length + ' 条）');
    for (const rec of toArchive) {
      lines.push('- [' + rec.type + '] ' + rec.rel + '（utility ' + round3(rec.utility) + '，' + rec.ageDays + ' 天）— ' + (rec.meta.subject || '') + ': ' + String(rec.meta.statement || '').slice(0, 40) + (rec.type === 'COMMIT' ? '  ⚠️ COMMIT 收工纪律锚点，请确认' : ''));
      if (apply && !opts.dedup) {
        const dest = path.join(root, archiveRelFor(root, rec.rel, rec.type, rec.owner));
        const destDir = path.dirname(dest);
        fs.mkdirSync(destDir, { recursive: true });
        fs.renameSync(rec.fp, dest);
        appendAudit(root, 'audit', { ts: new Date().toISOString(), file: rec.rel, action: 'archive', reason: 'utility<' + round3(rec.utility) + ',age>' + rec.ageDays, utility: round3(rec.utility) });
        archived++;
      }
    }
    lines.push('');
  }
  if (toForget.length) {
    lines.push('### 遗忘候选（' + toForget.length + ' 条，默认不真删；--purge 才删除）');
    for (const rec of toForget) {
      lines.push('- [' + rec.type + '] ' + rec.rel + '（utility ' + round3(rec.utility) + '，' + rec.ageDays + ' 天）');
      if (apply && purge && !opts.dedup) {
        const dest = path.join(root, archiveRelFor(root, rec.rel, rec.type, rec.owner));
        const destDir = path.dirname(dest);
        fs.mkdirSync(destDir, { recursive: true });
        fs.renameSync(rec.fp, dest);
        appendAudit(root, 'audit', { ts: new Date().toISOString(), file: rec.rel, action: 'forget', reason: 'utility<' + round3(rec.utility) + ',age>' + rec.ageDays + ',purge', utility: round3(rec.utility) });
        // 真删前二次确认标记：purge 已显式授权，删除 .archive 内副本前的最终动作 = 记录审计后删除
        try { fs.unlinkSync(dest); } catch (e) { /* 保留副本 */ }
        forgotten++;
      } else if (apply && !opts.dedup) {
        lines.push('    （--purge 未开启，跳过真删）');
      }
    }
    lines.push('');
  }
  if (!opts.dedup) {
    if (apply) {
      if (archived || forgotten) {
        const allMoved = toArchive.concat(toForget).filter(function (r) { return true; });
        removeIndexEntries(root, allMoved.map(function (r) { return r.rel; }));
      }
      lines.push('- 已执行: 归档 ' + archived + ' 条，遗忘 ' + forgotten + ' 条。审计: ' + auditPath(root, 'audit'));
    } else {
      lines.push('- 未执行任何变更（dry-run）。加 --apply 执行归档，--purge 才真删遗忘候选。');
    }
  }
  if (skipped.length) {
    lines.push('');
    lines.push('### 跳过（' + skipped.length + ' 条）');
    const grouped = {};
    for (const s of skipped) { grouped[s.reason] = (grouped[s.reason] || 0) + 1; }
    for (const k of Object.keys(grouped)) lines.push('- ' + k + ': ' + grouped[k] + ' 条');
  }
  if (deniedCrossOwner) {
    lines.push('');
    lines.push('- 跨 owner 私密条目已跳过（' + deniedCrossOwner + ' 条）：请用 --agent <id> 声明自己的身份；只有用户显式授权（--unsafe）才能越界维护。');
  }
  if (!opts.dedup) {
    const ruleResult = ruleMiningCore(root, opts);
    if (ruleResult.groups.length) {
      lines.push('');
      lines.push.apply(lines, ruleMiningLines(ruleResult));
    }
  }
  // 去重（v0.10.0：置信度分档 + --apply 自动合并；--dedup 与归档/遗忘互斥）
  if (opts.dedup) appendDedupBlock(lines, root, opts);
  return { error: false, text: lines.join('\n') };
}
// 手动合并两条相似记忆：保留高 confidence，低 confidence 移入 .archive
function mergeCore(refA, refB, opts) {
  opts = opts || {};
  const selfAgent = resolveIdentity(opts).id;
  const ta = resolveMemoryTarget(refA);
  const tb = resolveMemoryTarget(refB);
  if (!ta || !tb) return { error: true, text: '未找到记忆文件: ' + refA + ' / ' + refB };
  for (const t of [ta, tb]) {
    const deny = checkOwnerWritable(t.root, t.rel, selfAgent, opts.unsafe);
    if (deny) return { error: true, text: deny };
  }
  if (ta.root !== tb.root) return { error: true, text: '暂不支持跨记忆库合并（' + ta.root + ' vs ' + tb.root + '）。' };
  const root = ta.root;
  const guard = destructiveGuardCore({
    root: root,
    action: 'merge',
    snapshotDir: opts.snapshotDir,
    backupDir: opts.backupDir,
    allowSameVolumeForTest: opts.allowSameVolumeForTest,
    sameVolumeFn: opts.sameVolumeFn,
    now: opts.now,
  });
  if (guard.error) return { error: true, text: guard.text };
  const ea = readEntry(ta.fp, root);
  const eb = readEntry(tb.fp, root);
  const keep = ea.confidence >= eb.confidence ? ea : eb;
  const drop = ea.confidence >= eb.confidence ? eb : ea;
  const keepFp = ea.confidence >= eb.confidence ? ta.fp : tb.fp;
  const dropFp = ea.confidence >= eb.confidence ? tb.fp : ta.fp;
  const owner = ownerFromPrivatePath(root, keepFp);
  const tags = Array.from(new Set((keep.tags || []).concat(drop.tags || [])));
  const patch = { updated: today(), tags: JSON.stringify(tags), access_count: (keep.access_count || 0) + (drop.access_count || 0), feedback_net: (keep.feedback_net || 0) + (drop.feedback_net || 0) };
  rewriteFrontmatter(keepFp, patch, root, owner);
  upsertIndexEntry(root, readEntry(keepFp, root));
  const destDir = path.join(root, ARCHIVE_DIR, TYPE_DIRS[drop.type]);
  fs.mkdirSync(destDir, { recursive: true });
  const dest = path.join(destDir, path.basename(dropFp));
  fs.renameSync(dropFp, dest);
  removeIndexEntry(root, drop.file);
  appendAudit(root, 'audit', { ts: new Date().toISOString(), file: drop.file, action: 'merge', reason: '并入 ' + keep.file, utility: round3(utilityScore(keep)) });
  return { error: false, text: '已合并: ' + drop.file + ' -> ' + keep.file + '\n  保留: [' + keep.type + '] ' + keep.subject + ': ' + keep.statement + '\n  归档低 confidence: ' + drop.file + '\n  事务快照: ' + guard.snapshot.id };
}
// ---- v0.18.1 A8：蒸馏分类型提取 / 溯源锚点 / 质量指标（确定性，零依赖）----
const DISTILL_CLASS_NAMES = ['教训', '待办', '成长', '事件', '规则边界', '其他'];
const DISTILL_LESSON_WORDS = ['教训', '踩坑', '失误', '错误', '故障', '事故', '纠正', 'learning', 'error', 'correction', 'incident'];
const DISTILL_TASK_WORDS = ['待办', '任务', 'action', 'next', '跟进'];
const DISTILL_TASK_TAG_RE = /^t(o)?do$/i;
const DISTILL_GROWTH_WORDS = ['成长', '改进', '提升', '洞见', '最佳实践', '复盘', 'insight', 'growth', 'improvement', 'best-practice'];
const DISTILL_EVENT_WORDS = ['事件', '里程碑', '发布', '上线', '会议', '活动', 'release', 'milestone'];
const DISTILL_FIELD_LIMIT = 500;
function distillHasWord(haystack, words) {
  const s = String(haystack || '').toLowerCase();
  for (const w of words) if (s.indexOf(String(w).toLowerCase()) !== -1) return true;
  return false;
}
function distillClassify(entry, meta) {
  if (!meta || !meta.type) return '其他';
  if (entry.type === 'BOUND') return '规则边界';
  const hay = (entry.tags || []).join(',') + ' ' + String(entry.subject || '');
  if (distillHasWord(hay, DISTILL_LESSON_WORDS)) return '教训';
  const hasTaskTag = (entry.tags || []).some(function (t) { return DISTILL_TASK_TAG_RE.test(String(t).trim()); });
  if (distillHasWord(hay, DISTILL_TASK_WORDS) || hasTaskTag) return '待办';
  if (distillHasWord(hay, DISTILL_GROWTH_WORDS)) return '成长';
  if (distillHasWord(hay, DISTILL_EVENT_WORDS)) return '事件';
  if (entry.type === 'COMMIT') return '待办';
  if (entry.type === 'PREF') return '成长';
  if (entry.type === 'FACT') return '事件';
  return '其他';
}
function distillSentences(body) {
  return String(body || '').replace(/([。！？])/g, '$1\n').split('\n').map(function (s) { return s.trim(); }).filter(Boolean);
}
function distillLineOf(lines, needle) {
  const n = String(needle || '');
  if (!n) return 0;
  for (let i = 0; i < lines.length; i++) if (lines[i].indexOf(n) !== -1) return i + 1;
  return 0;
}
function distillClamp(value, limit) {
  const s = String(value === undefined || value === null ? '' : value);
  const max = limit || DISTILL_FIELD_LIMIT;
  if (s.length <= max) return { value: s, truncated: false };
  return { value: s.slice(0, max) + '…（截断 ' + (s.length - max) + ' 字符，全文见溯源）', truncated: true };
}
function distillDateNear(sentences, body) {
  const dateRe = /\d{4}-\d{2}-\d{2}/;
  for (const s of sentences) {
    if (dateRe.test(s) && /(截止|前完成|之前|deadline|due)/i.test(s)) return s.match(dateRe)[0];
  }
  const all = String(body || '');
  if (/(截止|前完成|deadline|due)/i.test(all)) {
    const m = all.match(dateRe);
    if (m) return m[0];
  }
  return '';
}
function distillExtract(entry, cls, body, lines) {
  const sents = distillSentences(body);
  const statement = String(entry.statement || '');
  const subject = String(entry.subject || '');
  const tags = (entry.tags || []).join(', ');
  const fields = {};
  const used = [];
  const take = function (name, value) {
    const ok = value !== undefined && value !== null && String(value) !== '';
    fields[name] = ok ? String(value) : '未记录';
    if (ok) used.push(String(value));
  };
  let fieldNames = [];
  if (cls === '教训') {
    fieldNames = ['教训', '触发条件', '规避方法'];
    const avoid = sents.filter(function (s) { return /(避免|应该|下次|教训)/.test(s); })[0];
    take('教训', statement);
    take('触发条件', tags || subject);
    take('规避方法', avoid);
    if (avoid) used.push(avoid);
  } else if (cls === '待办') {
    fieldNames = ['任务', '优先级', '截止'];
    let priority = '';
    for (const t of (entry.tags || [])) if (/^(high|medium|low|高|中|低)$/i.test(String(t))) { priority = t; break; }
    const due = distillDateNear(sents.concat([statement]), body + ' ' + statement);
    take('任务', statement);
    take('优先级', priority);
    take('截止', due);
    if (due) used.push(due);
  } else if (cls === '成长') {
    fieldNames = ['改进点', '前后对比', '效果'];
    const before = sents.filter(function (s) { return /(之前|后来|从.+到)/.test(s); })[0];
    const effect = sents.filter(function (s) { return /(效果|提升|%|更好)/.test(s); })[0];
    take('改进点', statement);
    take('前后对比', before);
    take('效果', effect);
    if (before) used.push(before);
    if (effect) used.push(effect);
  } else if (cls === '事件') {
    fieldNames = ['时间', '内容', '结果'];
    const last = sents.length ? sents[sents.length - 1] : '';
    take('时间', entry.created || entry.updated);
    take('内容', subject + (statement ? ': ' + statement : ''));
    take('结果', last);
    if (last) used.push(last);
  } else if (cls === '规则边界') {
    fieldNames = ['规则', '适用范围', '例外'];
    const ex = sents.filter(function (s) { return /(除非|例外)/.test(s); })[0];
    take('规则', statement);
    take('适用范围', tags || subject);
    take('例外', ex);
    if (ex) used.push(ex);
  } else {
    fieldNames = ['内容'];
    take('内容', statement || (sents[0] || String(body || '').trim().slice(0, 200)));
  }
  const lineNumbers = used.map(function (v) { return distillLineOf(lines, v); }).filter(Boolean);
  if (!lineNumbers.length) {
    const fallback = distillLineOf(lines, statement) || distillLineOf(lines, subject) || 1;
    lineNumbers.push(fallback);
  }
  let truncated = false;
  for (const name of fieldNames) {
    if (fields[name] === '未记录') continue;
    const clamped = distillClamp(fields[name]);
    if (clamped.truncated) { fields[name] = clamped.value; truncated = true; }
  }
  return {
    fields: fields,
    fieldNames: fieldNames,
    anchor: { start: Math.min.apply(null, lineNumbers), end: Math.max.apply(null, lineNumbers) },
    truncated: truncated,
  };
}
function distillElementStats(entry, cls, body) {
  const sents = distillSentences(body);
  const tags = (entry.tags || []).join(', ');
  const hasPriority = (entry.tags || []).some(function (t) { return /^(high|medium|low|高|中|低)$/i.test(String(t)); });
  let specs = [];
  if (cls === '教训') specs = [!!entry.statement, !!(tags || entry.subject), /(避免|应该|下次|教训)/.test(body)];
  else if (cls === '待办') specs = [!!entry.statement, hasPriority, !!distillDateNear(sents.concat([String(entry.statement || '')]), body + ' ' + String(entry.statement || ''))];
  else if (cls === '成长') specs = [!!entry.statement, /(之前|后来|从.+到)/.test(body), /(效果|提升|%|更好)/.test(body)];
  else if (cls === '事件') specs = [!!(entry.created || entry.updated), !!(entry.subject || entry.statement), sents.length > 0];
  else if (cls === '规则边界') specs = [!!entry.statement, !!(tags || entry.subject), /(除非|例外)/.test(body)];
  else specs = [!!(entry.statement || body)];
  const detected = specs.filter(Boolean).length;
  return { detected: detected, expected: specs.length };
}
function distillAnalyze(root, entries, owner) {
  const classes = {};
  for (const name of DISTILL_CLASS_NAMES) classes[name] = { name: name, count: 0, items: [] };
  const skipped = [];
  let analyzed = 0, entriesWithItems = 0, itemCount = 0, traceOk = 0;
  let sourceChars = 0, extractedChars = 0, detected = 0, filled = 0;
  const refusedRe = /\uFFFD/;
  for (const e of entries) {
    const entryRoot = e._root || root;
    const fp = path.join(entryRoot, e.file);
    const entryOwner = ownerFromPrivatePath(entryRoot, fp) || owner;
    let raw;
    try {
      raw = readMemoryText(entryRoot, fp, entryOwner);
    } catch (err) {
      skipped.push({ file: e.file, reason: 'encoding', detail: String(err.message || err) });
      continue;
    }
    raw = String(raw).replace(/^\uFEFF/, '');
    if (!raw.trim()) {
      skipped.push({ file: e.file, reason: 'empty', detail: '' });
      continue;
    }
    if (refusedRe.test(raw)) {
      skipped.push({ file: e.file, reason: 'encoding', detail: 'UTF-8 解码失败' });
      continue;
    }
    const parsed = parseFrontmatter(raw);
    const hasMeta = !!(parsed.meta && parsed.meta.type);
    const local = Object.assign({}, e);
    if (hasMeta) {
      local.type = String(parsed.meta.type || e.type).toUpperCase();
      local.subject = parsed.meta.subject || e.subject;
      local.statement = parsed.meta.statement || e.statement;
      local.tags = parseTags(parsed.meta.tags);
      local.created = parsed.meta.created || e.created;
      local.updated = parsed.meta.updated || e.updated;
    } else {
      local.type = '';
      local.tags = [];
      local.subject = path.basename(e.file).replace(/\.md(\.enc)?$/, '');
      local.statement = String(parsed.body || raw).trim().split('\n')[0].slice(0, 200);
      skipped.push({ file: e.file, reason: 'no-structure', detail: '按裸文本处理', analyzed: true });
    }
    const cls = distillClassify(local, hasMeta ? parsed.meta : null);
    const body = String(parsed.body || '');
    const lines = raw.split('\n');
    const ex = distillExtract(local, cls, body, lines);
    const stats = distillElementStats(local, cls, body);
    detected += stats.detected;
    filled += ex.fieldNames.filter(function (n) { return ex.fields[n] !== '未记录'; }).length;
    const anchorText = '[溯源: ' + e.file + '#L' + ex.anchor.start + '-L' + ex.anchor.end + ']';
    const item = {
      ref: e.file,
      type: local.type || 'UNKNOWN',
      subject: local.subject,
      statement: local.statement,
      fields: ex.fields,
      anchor: e.file + '#L' + ex.anchor.start + '-L' + ex.anchor.end,
      anchorText: anchorText,
      truncated: ex.truncated,
    };
    classes[cls].items.push(item);
    classes[cls].count += 1;
    analyzed += 1;
    entriesWithItems += 1;
    itemCount += 1;
    traceOk += 1;
    sourceChars += String(local.statement || '').length + body.length;
    for (const n of ex.fieldNames) if (ex.fields[n] !== '未记录') extractedChars += String(ex.fields[n]).length;
    if (ex.truncated) skipped.push({ file: e.file, reason: 'truncated', detail: '超长字段已截断到 ' + DISTILL_FIELD_LIMIT + ' 字符', analyzed: true });
  }
  const mainLines = ['## 二、分类型提取清单', ''];
  if (!itemCount) mainLines.push('（无可提取条目）');
  for (const name of DISTILL_CLASS_NAMES) {
    const c = classes[name];
    if (!c.count) continue;
    mainLines.push('### ' + name + '（' + c.count + ' 条）');
    for (const item of c.items) {
      mainLines.push('- [' + item.type + '] ' + item.subject);
      for (const fn of Object.keys(item.fields)) mainLines.push('  - ' + fn + ': ' + item.fields[fn]);
      mainLines.push('  - ' + item.anchorText);
      mainLines.push('');
    }
  }
  const compression = extractedChars > 0 ? Math.round((sourceChars / extractedChars) * 100) / 100 : 0;
  const entryCoverage = analyzed > 0 ? round4(entriesWithItems / analyzed) : 1;
  const traceCoverage = itemCount > 0 ? round4(traceOk / itemCount) : 1;
  const elementRate = detected > 0 ? round4(filled / detected) : 1;
  mainLines.push('## 三、质量指标', '');
  mainLines.push('- 源正文字符: ' + sourceChars + ' / 提取要点字符: ' + extractedChars + ' → 实测压缩比 ' + compression + '（只报本次实测，不承诺倍数）');
  mainLines.push('- 条目覆盖率: ' + Math.round(entryCoverage * 100) + '%（' + entriesWithItems + '/' + analyzed + '）');
  mainLines.push('- 溯源覆盖率: ' + Math.round(traceCoverage * 100) + '%（' + traceOk + '/' + itemCount + '，目标 100%）');
  mainLines.push('- 要素提取率: ' + Math.round(elementRate * 100) + '%（' + filled + '/' + detected + '，确定性回归护栏，不是语义保真承诺）');
  const tailLines = ['## 六、跳过与边界', ''];
  if (!skipped.length) tailLines.push('（无跳过项）');
  for (const s of skipped) {
    tailLines.push('- ' + s.file + ': ' + s.reason + (s.detail ? '（' + s.detail + '）' : '') + (s.analyzed ? '（已分析）' : '（已跳过）'));
  }
  return {
    classes: DISTILL_CLASS_NAMES.map(function (n) { return classes[n]; }).filter(function (c) { return c.count > 0; }),
    skipped: skipped,
    mainLines: mainLines,
    tailLines: tailLines,
    analyzed: analyzed,
    metrics: {
      compression_ratio: compression,
      entry_coverage: entryCoverage,
      trace_coverage: traceCoverage,
      element_extract_rate: elementRate,
    },
  };
}

// 心理日志蒸馏：统计摘要 / 分类型提取 / 质量指标 / 主题画像 / 知识地图（启发式默认，可选 --model）
function distillCore(opts) {
  opts = opts || {};
  const root = userRoot();
  if (!fs.existsSync(root)) return { error: false, text: '记忆库不存在。' };
  const selfAgent = resolveIdentity(opts).id;
  const owner = opts.owner || selfAgent;
  const entries = [];
  for (const r of memoryRoots()) {
    for (const e of ensureIndex(r)) {
      if (classifyRead(e, owner, '', !!opts.unsafe, selfAgent) === 'denied') continue;
      entries.push(Object.assign({}, e, { _root: r }));
    }
  }
  const lines = [];
  lines.push('# 元忆记忆蒸馏报告（v' + VERSION + '）');
  lines.push('');
  lines.push('> 生成: yotta-memory distill | 启发式蒸馏（零依赖）；--model <cmd> 可选外部模型增强');
  lines.push('> 时间: ' + new Date().toISOString() + ' / 可读条目: ' + entries.length + ' 条');
  lines.push('');
  const analysis = distillAnalyze(root, entries, owner);
  // 1) 统计摘要
  lines.push('## 一、统计摘要');
  lines.push('');
  if (!entries.length) lines.push('（无记忆）');
  const byType = {};
  for (const e of entries) byType[e.type] = (byType[e.type] || 0) + 1;
  lines.push('- 类型分布: ' + Object.keys(byType).map(function (k) { return k + ' ' + byType[k]; }).join(' / '));
  let young = 0, mid = 0, old = 0, veryOld = 0;
  for (const e of entries) {
    if (!e.created) continue;
    const d = daysBetween(e.created, today());
    if (d < 30) young++; else if (d < 90) mid++; else if (d < 180) old++; else veryOld++;
  }
  lines.push('- 年龄分布: <30天 ' + young + ' / 30-90 ' + mid + ' / 90-180 ' + old + ' / >180天 ' + veryOld);
  const hot = entries.slice().sort(function (a, b) { return (b.access_count || 0) - (a.access_count || 0); }).slice(0, 5);
  lines.push('- 热度 Top5（access_count）:');
  for (const h of hot) lines.push('  - [' + h.type + '] ' + h.subject + '（' + (h.access_count || 0) + ' 次）');
  let fbSum = 0, usefulN = 0, uselessN = 0;
  for (const e of entries) { const n = e.feedback_net || 0; fbSum += n; if (n > 0) usefulN++; else if (n < 0) uselessN++; }
  lines.push('- 反馈统计: feedback_net 总和 ' + fbSum + '（正 ' + usefulN + ' 条 / 负 ' + uselessN + ' 条）');
  lines.push('');
  lines.push.apply(lines, analysis.mainLines);
  lines.push('');
  // 2) 主题画像（按 subject 聚类合并）
  lines.push('## 四、主题画像（按 subject 聚类，启发式合并）');
  lines.push('');
  const groups = {};
  for (const e of entries) {
    const key = String(e.subject || '（无主题）');
    (groups[key] = groups[key] || []).push(e);
  }
  const sortedKeys = Object.keys(groups).sort(function (a, b) { return groups[b].length - groups[a].length; });
  for (const k of sortedKeys) {
    const g = groups[k];
    const best = g.slice().sort(function (a, b) { return (b.confidence || 0) - (a.confidence || 0); })[0];
    const tags = Array.from(new Set([].concat.apply([], g.map(function (e) { return e.tags || []; }))));
    lines.push('### ' + k + '（' + g.length + ' 条）');
    lines.push('- 代表: ' + best.statement);
    if (tags.length) lines.push('- 标签: ' + tags.join(', '));
    lines.push('- 引用: ' + g.map(function (e) { return e.file; }).join(' / '));
    lines.push('');
  }
  // 3) 知识地图（type + tags 层级）
  lines.push('## 五、知识地图（type → tags）');
  lines.push('');
  const map = {};
  for (const e of entries) {
    const t = e.type;
    (map[t] = map[t] || {});
    const tagKey = (e.tags && e.tags.length) ? e.tags.join(',') : '（无标签）';
    (map[t][tagKey] = map[t][tagKey] || []).push(e);
  }
  for (const t of Object.keys(map).sort()) {
    lines.push('### ' + t);
    for (const tk of Object.keys(map[t]).sort()) {
      lines.push('- ' + tk + ': ' + map[t][tk].map(function (e) { return e.subject; }).join(' / '));
    }
  }
  lines.push('');
  lines.push.apply(lines, analysis.tailLines);
  let body = lines.join('\n') + '\n';
  // 可选模型增强：--model <cmd>，stdin 传结构化摘要，stdout 取提炼文本
  let modelOut = '';
  if (opts.model) {
    try {
      const payload = JSON.stringify({ summary: lines.join('\n'), entries: entries.map(function (e) { return { type: e.type, subject: e.subject, statement: e.statement, tags: e.tags, confidence: e.confidence, access_count: e.access_count, feedback_net: e.feedback_net }; }).slice(0, 200) });
      const r = runDistillModel(String(opts.model), payload);
      if (r.stdout) modelOut = String(r.stdout).trim();
      if (!modelOut) modelOut = '（模型无输出）';
      body += '\n## 七、模型提炼（--model ' + opts.model + '）\n\n' + modelOut + '\n';
    } catch (e) {
      modelOut = '（模型调用失败: ' + e.message + '）';
      body += '\n## 七、模型提炼\n\n' + modelOut + '\n';
    }
  }
  const makeReport = function (writtenPath) {
    return {
      schemaVersion: 1,
      generated: new Date().toISOString(),
      root: root,
      scope: { owner: owner, entries: entries.length, analyzed: analysis.analyzed },
      classes: analysis.classes,
      metrics: analysis.metrics,
      skipped: analysis.skipped,
      written: writtenPath || '',
    };
  };
  // 落盘：--out 指定 / 私密 distills / 公共 facts/distills
  let written = '';
  try {
    if (opts.out) {
      const outPath = path.resolve(String(opts.out));
      fs.mkdirSync(path.dirname(outPath), { recursive: true });
      fs.writeFileSync(outPath, body, 'utf8');
      written = outPath;
    } else {
      const slug = String((opts.subject || 'distill').replace(/[^\w\u4e00-\u9fa5-]+/g, '-').slice(0, 40));
      const fname = today() + '-' + slug + '.md';
      if (owner && entries.some(function (e) { return e.scope !== 'public' && e.owner === owner; })) {
        const dir = path.join(root, PRIVATE_DIR, owner, 'distills');
        fs.mkdirSync(dir, { recursive: true });
        const fp = path.join(dir, fname);
        const text = frontmatterToText({ type: 'COMMIT', subject: '蒸馏报告 ' + slug, statement: '记忆蒸馏报告（' + today() + '）', confidence: 1.0, created: today(), updated: today(), tags: ['distill'], immutable: false, scope: 'private', owner: owner, source: 'distill', weight: 1.0, access_count: 0, last_accessed: '', feedback_net: 0 }, body);
        writeMemoryText(root, fp, text, owner);
        upsertIndexEntry(root, readEntry(fp, root));
        written = fp;
      } else {
        const dir = path.join(root, PUBLIC_DIR, 'distills');
        fs.mkdirSync(dir, { recursive: true });
        const fp = path.join(dir, fname);
        const text = frontmatterToText({ type: 'FACT', subject: '蒸馏报告 ' + slug, statement: '记忆蒸馏报告（' + today() + '）', confidence: 1.0, created: today(), updated: today(), tags: ['distill'], immutable: false, scope: 'public', owner: '', source: 'distill', weight: 1.0, access_count: 0, last_accessed: '', feedback_net: 0 }, body);
        fs.writeFileSync(fp, text, 'utf8');
        upsertIndexEntry(root, readEntry(fp, root));
        written = fp;
      }
    }
  } catch (e) {
    return { error: false, text: lines.join('\n') + '\n\n[落盘失败] ' + e.message, report: makeReport('') };
  }
  return { error: false, text: body + '\n[已写入] ' + written, report: makeReport(written) };
}

function promptPassword(promptText) {
  return new Promise(function (resolve) {
    const stdin = process.stdin;
    if (!stdin.isTTY) { resolve(null); return; }
    process.stdout.write(promptText);
    let buf = '';
    function done(abort) {
      try { stdin.setRawMode(false); } catch (e) {}
      stdin.pause();
      stdin.removeListener('data', onData);
      process.stdout.write('\n');
      resolve(abort ? null : buf);
    }
    function onData(chunk) {
      const s = String(chunk);
      for (const c of s) {
        if (c === '\r' || c === '\n') { done(false); return; }
        if (c === '\u0003') { done(true); return; }
        if (c === '\u007f' || c === '\b') buf = buf.slice(0, -1);
        else buf += c;
      }
    }
    try { stdin.setRawMode(true); } catch (e) { resolve(null); return; }
    stdin.resume();
    stdin.setEncoding('utf8');
    stdin.on('data', onData);
  });
}

// 交互确认输入（回显明文，用于「输入 id 确认删除」这类非机密输入）。
function promptLine(promptText) {
  return new Promise(function (resolve) {
    const stdin = process.stdin;
    if (!stdin.isTTY) { resolve(null); return; }
    process.stdout.write(promptText);
    let buf = '';
    function done(abort) {
      try { stdin.setRawMode(false); } catch (e) {}
      stdin.pause();
      stdin.removeListener('data', onData);
      process.stdout.write('\n');
      resolve(abort ? null : buf);
    }
    function onData(chunk) {
      const s = String(chunk);
      for (const c of s) {
        if (c === '\r' || c === '\n') { done(false); return; }
        if (c === '\u0003') { done(true); return; }
        if (c === '\u007f' || c === '\b') {
          if (buf.length) { buf = buf.slice(0, -1); process.stdout.write('\b \b'); }
          continue;
        }
        buf += c;
        process.stdout.write(c);
      }
    }
    try { stdin.setRawMode(true); } catch (e) { resolve(null); return; }
    stdin.resume();
    stdin.setEncoding('utf8');
    stdin.on('data', onData);
  });
}

async function cmdIdentityRemove(id, opts) {
  opts = opts || {};
  const root = userRoot();
  if (!id) {
    console.error('请指定 <id>：yotta-memory identity remove <id> [--dry-run] [--yes] [--keep-memories] [--keep-identity]');
    process.exit(2);
  }
  let local = Object.assign({}, opts);
  if (!local.dryRun && !local.yes && process.stdin.isTTY) {
    const typed = await promptLine('将彻底删除 ' + id + ' 的身份与私密记忆（不可恢复；公共明文保留）。请输入 ' + id + ' 确认: ');
    if (typed !== id) {
      console.log('已取消：未删除任何内容。');
      process.exit(2);
    }
    local.yes = true;
  }
  if (!local.dryRun && isEncrypted(root) && !local.password && !local.recoveryKey && !process.env.YOTTA_MEMORY_PASS) {
    const got = await resolvePasswordInput(local, '主口令: ');
    if (got.error) { console.error(got.error); process.exit(2); }
    local.password = got.password;
  }
  const result = identityRemoveCore(root, id, local);
  console.log(result.text);
  if (result.error) process.exit(result.exitCode || 2);
}

function readPasswordFromStdin() {
  try {
    const text = fs.readFileSync(0, 'utf8');
    // Windows PowerShell 管道可能带 UTF-8 BOM；BOM 不能成为口令的一部分。
    return String(text || '').replace(/^\uFEFF/, '').replace(/\r?\n$/, '');
  } catch (e) {
    return '';
  }
}

async function resolvePasswordInput(opts, promptText, options) {
  opts = opts || {};
  options = options || {};
  const direct = options.field === 'new' ? String(opts.newPassword || '') : String(opts.password || '');
  if (direct) return { password: direct, source: 'option', error: '' };
  if (opts.passwordStdin) {
    const password = readPasswordFromStdin();
    if (!password) {
      return { password: '', source: 'stdin', error: '--password-stdin 没有读到内容；请通过管道传入主口令。' };
    }
    return { password: password, source: 'stdin', error: '' };
  }
  const envPass = String(process.env.YOTTA_MEMORY_PASS || '');
  if (envPass) return { password: envPass, source: 'env', error: '' };
  if (!process.stdin.isTTY) {
    return { password: '', source: 'non-tty', error: '当前为非交互环境，无法读取主口令。请使用 --password-stdin（推荐，管道传入）或设置 YOTTA_MEMORY_PASS；不要把口令直接写在命令行参数里。' };
  }
  const password = await promptPassword(promptText);
  if (!password) return { password: '', source: 'prompt', error: '已取消。' };
  return { password: password, source: 'prompt', error: '' };
}

function migrateCore(root, password, recoveryKeyIn) {
  // 第三个参数历史上是 recovery key；兼容旧调用，同时支持 { agent, recoveryKey } 选项对象。
  const opts = recoveryKeyIn && typeof recoveryKeyIn === 'object' ? recoveryKeyIn : {};
  if (!fs.existsSync(root)) return { error: true, text: '记忆库不存在，请先 yotta-memory init。' };
  if (isEncrypted(root)) return { error: true, text: '记忆库已启用加密（keys/ 存在），无需迁移。' };
  const salt = crypto.randomBytes(16);
  ensureKeysDir(root);
  fs.writeFileSync(encSaltPath(root), salt);
  const umk = deriveUmk(password, salt);
  const rk = crypto.randomBytes(32);
  fs.writeFileSync(encRecoveryEncPath(root), Buffer.concat([Buffer.from(KEY_MAGIC, 'utf8'), aesEncryptBytes(umk, rk, Buffer.from('recovery', 'utf8'))]));
  let moved = 0;
  const owners = collectOwners(root);
  const self = resolveIdentity(opts).id;
  for (const owner of owners) {
    const ok = wrapOwnerKey(root, umk, rk, owner);
    for (const t of PRIVATE_LEAF) {
      const d = path.join(root, PRIVATE_DIR, owner, t);
      if (!fs.existsSync(d)) continue;
      // v0.17.0：递归下探年/月子目录，明文库迁移到加密时不能漏掉分层文件。
      const plaintexts = [];
      const collectPlaintext = function (current) {
        let names = [];
        try { names = fs.readdirSync(current, { withFileTypes: true }); } catch (e) { return; }
        for (const item of names) {
          const fp = path.join(current, item.name);
          if (item.isDirectory()) { collectPlaintext(fp); continue; }
          if (item.isFile() && /\.md$/.test(item.name) && !isEncFile(fp)) plaintexts.push(fp);
        }
      };
      collectPlaintext(d);
      for (const fp of plaintexts) {
        const text = fs.readFileSync(fp, 'utf8');
        fs.writeFileSync(fp + ENC_SUFFIX, encryptMemoryText(text, ok));
        fs.unlinkSync(fp);
        moved++;
      }
    }
    const pf = path.join(root, PRIVATE_DIR, owner, PROFILE_FILE);
    if (fs.existsSync(pf)) {
      const text = fs.readFileSync(pf, 'utf8');
      fs.writeFileSync(pf + ENC_SUFFIX, encryptMemoryText(text, ok));
      fs.unlinkSync(pf);
      moved++;
    }
  }
  buildIndex(root);
  let tail = moved > 0
    ? ('已迁移 ' + moved + ' 个私密文件（' + owners.length + ' 个 owner）到密文。')
    : '私密区为空；已为明文库启用加密（未迁移文件、未创建 owner key）。';
  if (opts.recoveryKeyOut) {
    const outPath = path.resolve(String(opts.recoveryKeyOut));
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, rk.toString('base64') + '\n', { encoding: 'utf8', mode: 0o600 });
    tail += '\n[恢复钥匙] 已写入文件: ' + outPath + '（务必离线保存，仅此一次，泄露=可解全部私密；不要把钥匙粘贴到对话中）';
  } else {
    tail += '\n[恢复钥匙]（务必离线保存，仅此一次，泄露=可解全部私密）: ' + rk.toString('base64');
  }
  tail += '\n迁移不会写明文 owner key cache。下一步为每个 agent 做一次授权，二选一（等价）：';
  tail += '\n  推荐：yotta-memory view → 浏览器解锁 → 授权 <id> → 保存一次性 agent_key';
  tail += '\n  高级：yotta-memory key bind <id>';
  tail += '\n授权后 AI 执行：yotta-memory key status <id> → yotta-memory key claim <id> → <AI_HOME>/.yotta-memory-agent-key';
  tail += '\n然后带 agent-key-file 重建加密索引：yotta-memory reindex --agent <id> --agent-key-file <AI_HOME>/.yotta-memory-agent-key';
  if (self && owners.indexOf(self) !== -1) tail += '\n你的身份：' + self + '。推荐直接在 yotta-memory view 页面授权它。';
  return { error: false, text: tail };
}

async function cmdMigrate(opts) {
  const root = userRoot();
  if (isEncrypted(root)) { console.error('记忆库已启用加密，无需迁移。'); process.exit(2); }
  let password = opts.password || process.env.YOTTA_MEMORY_PASS || '';
  if (!password) {
    const got = await resolvePasswordInput(opts, '主口令（迁移后私密区加密，勿忘；忘口令可用恢复钥匙重设）: ');
    if (got.error) { console.error(got.error); process.exit(2); }
    password = got.password;
  }
  const r = migrateCore(root, password, { agent: opts.agent, recoveryKey: null, recoveryKeyOut: opts.recoveryKeyOut });
  console.log(r.text);
  if (r.error) process.exit(2);
}

function resetPasswordCore(root, opts) {
  opts = opts || {};
  if (!isEncrypted(root)) return { error: true, text: '记忆库未启用加密。' };
  const salt = loadSalt(root);
  if (!salt) return { error: true, text: '密钥库损坏（缺 keys/salt）。' };
  const owners = keyOwners(root).filter(function (o) { return fs.existsSync(encOwnerKeyPath(root, o)); });
  if (!owners.length) return { error: true, text: '没有可重设的 owner 密钥（keys/ 下无 *.key.enc）。' };
  const newPass = String(opts.newPassword || '');
  if (!newPass) return { error: true, text: '请提供新口令（--new-password 或交互输入）。' };
  if (opts.recoveryKey) {
    const rk = Buffer.from(String(opts.recoveryKey).trim(), 'base64');
    if (rk.length !== 32) return { error: true, text: '恢复钥匙格式错误（须为 32 字节 base64）。' };
    let verified = false;
    for (const o of owners) { try { unwrapOwnerKeyRecovery(root, o, rk); verified = true; break; } catch (e) {} }
    if (!verified) return { error: true, text: '恢复钥匙无效（无法解开任何 owner 密钥）。' };
    const newUmk = deriveUmk(newPass, salt);
    for (const o of owners) {
      const ok = unwrapOwnerKeyRecovery(root, o, rk);
      const aad = Buffer.from('owner:' + o, 'utf8');
      fs.writeFileSync(encOwnerKeyPath(root, o), Buffer.concat([Buffer.from(KEY_MAGIC, 'utf8'), aesEncryptBytes(newUmk, ok, aad)]));
    }
    fs.writeFileSync(encRecoveryEncPath(root), Buffer.concat([Buffer.from(KEY_MAGIC, 'utf8'), aesEncryptBytes(newUmk, rk, Buffer.from('recovery', 'utf8'))]));
    return { error: false, text: '口令已重设（恢复钥匙验证通过，已重新包裹全部 owner 密钥）。' };
  }
  const curPass = String(opts.password || '');
  if (!curPass) return { error: true, text: '请提供当前口令（--password 或交互输入），或用 --recovery-key。' };
  const curUmk = deriveUmk(curPass, salt);
  let verified = false;
  for (const o of owners) { try { unwrapOwnerKey(root, o, curUmk); verified = true; break; } catch (e) {} }
  if (!verified) return { error: true, text: '当前口令错误。' };
  const newUmk = deriveUmk(newPass, salt);
  for (const o of owners) {
    const ok = unwrapOwnerKey(root, o, curUmk);
    const aad = Buffer.from('owner:' + o, 'utf8');
    fs.writeFileSync(encOwnerKeyPath(root, o), Buffer.concat([Buffer.from(KEY_MAGIC, 'utf8'), aesEncryptBytes(newUmk, ok, aad)]));
  }
  fs.writeFileSync(encRecoveryEncPath(root), Buffer.concat([Buffer.from(KEY_MAGIC, 'utf8'), aesEncryptBytes(newUmk, unwrapRecoveryEnc(root, curUmk), Buffer.from('recovery', 'utf8'))]));
  return { error: false, text: '口令已重设（当前口令验证通过）。' };
}

async function cmdResetPassword(opts) {
  const root = userRoot();
  if (!isEncrypted(root)) { console.error('记忆库未启用加密。'); process.exit(2); }
  let cur = opts.password || '';
  let rk = opts.recoveryKey || '';
  let np = opts.newPassword || process.env.YOTTA_MEMORY_PASS || '';
  if (!rk && !cur) {
    const got = await resolvePasswordInput(opts, '当前口令（或 --recovery-key 用恢复钥匙）: ');
    if (got.error) { console.error(got.error); process.exit(2); }
    cur = got.password;
  }
  if (!np) {
    const got = await resolvePasswordInput(opts, '新口令: ', { field: 'new' });
    if (got.error) { console.error(got.error); process.exit(2); }
    np = got.password;
    if (got.source === 'prompt') {
      const np2 = await promptPassword('再次输入确认: ') || '';
      if (np2 !== np) { console.error('两次输入不一致。'); process.exit(2); }
    }
  }
  const r = resetPasswordCore(root, { password: cur, recoveryKey: rk, newPassword: np });
  console.log(r.text);
  if (r.error) process.exit(2);
}

function keyBindCore(root, owner, opts) {
  opts = opts || {};
  if (!isSafeAgentId(owner)) return { error: true, text: '非法 agent ID：只允许单段名称，禁止 /、\\、.. 和控制字符。' };
  if (!isEncrypted(root)) return { error: true, text: '记忆库未启用加密。' };
  const salt = loadSalt(root);
  if (!salt) return { error: true, text: '密钥库损坏（缺 keys/salt）。' };
  let ownerKey = null;
  if (opts.recoveryKey) {
    const rk = Buffer.from(String(opts.recoveryKey), 'base64');
    if (rk.length !== 32) return { error: true, text: '恢复钥匙须为 32 字节（base64）。' };
    try { ownerKey = unwrapOwnerKeyRecovery(root, owner, rk); } catch (e) { ownerKey = null; }
    if (!ownerKey) return { error: true, text: '恢复钥匙无法解开 ' + owner + ' 的 owner key。' };
  } else {
    const password = String(opts.password || '');
    if (!password) return { error: true, text: '请提供主口令（--password 或交互输入），或用 --recovery-key。' };
    const umk = deriveUmk(password, salt);
    try { ownerKey = unwrapOwnerKey(root, owner, umk); } catch (e) { ownerKey = null; }
    if (!ownerKey) {
      let rk = null;
      try { rk = unwrapRecoveryEnc(root, umk); } catch (e) { rk = null; }
      if (!rk) return { error: true, text: '口令错误，或该 owner 的密钥不存在。' };
      ownerKey = recoverOwnerKeyFromRecovery(root, owner, umk, rk);
      if (!ownerKey) {
        if (privateOwnerHasData(root, owner)) {
          return { error: true, text: '检测到 private/' + owner + ' 仍有密文，但 keys/' + owner + '.key.enc 与恢复文件均不可用；拒绝新建 owner key（会导致旧数据无法解密）。请从备份恢复原 owner key，或使用恢复钥匙修复后重试。' };
        }
        ownerKey = wrapOwnerKey(root, umk, rk, owner);
      }
    }
  }
  const agentKey = crypto.randomBytes(32);
  const pendingFile = writeAgentBindingWithPending(root, owner, ownerKey, agentKey);
  revokeOwnerKeyCache(root, owner);
  return {
    error: false,
    agentKey: agentKey.toString('base64'),
    pendingFile: pendingFile,
    text: '已绑定 ' + owner + ' 的 agent_key，并删除旧明文 cache。\nagent_key: ' + agentKey.toString('base64') + '\n待领取文件: ' + pendingFile + '\nAI 在新会话执行 yotta-memory key status ' + owner + '，有 pending 再执行 yotta-memory key claim ' + owner + '；用户请另外保存此 key；此 key 只显示一次。',
  };
}

function keyRevokeCore(root, owner) {
  if (!isSafeAgentId(owner)) return { error: true, text: '非法 agent ID：只允许单段名称，禁止 /、\\、.. 和控制字符。' };
  let removed = false;
  const binding = encAgentBindingPath(root, owner);
  if (fs.existsSync(binding)) { fs.unlinkSync(binding); removed = true; }
  if (removePendingAgentKey(root, owner)) removed = true;
  if (revokeOwnerKeyCache(root, owner)) removed = true;
  if (!removed) return { error: false, text: owner + ' 无 agent binding（已是未绑定状态）。' };
  return { error: false, text: '已吊销 ' + owner + ' 的 agent_key binding；该 agent 将无法解密其私密。' };
}

// ---- v0.17.0：彻底删除一个 AI 身份 + 它的私密记忆（只能用户本人执行；公共明文保留）----
const IDENTITY_REMOVE_STEPS = [
  ['agents', 'agents.json 身份登记'],
  ['owner-key', 'keys/<id>.key.enc（owner 密钥与恢复侧文件）'],
  ['binding', 'keys/bindings/<id>.key.agent（授权绑定）'],
  ['pending', 'keys/pending/<id>.key（待领取 key）'],
  ['cache', 'keys/cache/<id>.key（明文缓存）'],
  ['memories', 'private/<id>/（私密记忆 + owner 索引 + profile / distill）'],
  ['token', '.server/tokens.json 里的 token'],
  ['grants', 'grants.json 里的授权引用'],
  ['reindex', '重建索引并写审计'],
];
function countFilesInTree(dir) {
  let count = 0;
  (function walk(current) {
    let items = [];
    try { items = fs.readdirSync(current, { withFileTypes: true }); } catch (error) { return; }
    for (const item of items) {
      const fp = path.join(current, item.name);
      if (item.isDirectory()) walk(fp);
      else if (item.isFile()) count++;
    }
  })(dir);
  return count;
}
function identityRemoveInventory(root, id) {
  const agents = loadAgents(root);
  const grants = loadGrants(root);
  const tokens = loadTokens(root);
  const grantRefs = [];
  for (const key of Object.keys(grants)) {
    if (key === id) grantRefs.push(key + ' → 其它 owner');
    if (Array.isArray(grants[key]) && grants[key].indexOf(id) !== -1) grantRefs.push(key + ' → ' + id);
  }
  const privateDir = path.join(root, PRIVATE_DIR, id);
  const hasDir = fs.existsSync(privateDir);
  return {
    registered: !!(agents.agents && agents.agents[id]),
    ownerKey: fs.existsSync(encOwnerKeyPath(root, id)),
    ownerRecovery: fs.existsSync(encOwnerRecPath(root, id)),
    binding: fs.existsSync(encAgentBindingPath(root, id)),
    pending: fs.existsSync(encPendingPath(root, id)),
    cache: fs.existsSync(encCachePath(root, id)),
    memories: hasDir,
    memoryFiles: hasDir ? countFilesInTree(privateDir) : 0,
    token: Object.prototype.hasOwnProperty.call(tokens, id),
    grants: grantRefs,
  };
}
function identityRemoveExists(inventory) {
  return !!(inventory.registered || inventory.ownerKey || inventory.ownerRecovery || inventory.binding
    || inventory.pending || inventory.cache || inventory.memories || inventory.token || inventory.grants.length);
}
// 用户授权证明：加密库要主口令（能解开任一 owner key 或恢复材料）或恢复钥匙；
// view 已用主口令解锁的会话视为用户本人；明文库无机密凭据可校验，要求显式 --agent user。AI 不得删除身份。
function verifyIdentityRemoveAuthority(root, id, opts) {
  if (opts.userUnlocked === true) return { ok: true, mode: 'view-session' };
  if (isEncrypted(root)) {
    const candidates = [id].concat(collectOwners(root));
    if (opts.recoveryKey) {
      const rk = Buffer.from(String(opts.recoveryKey), 'base64');
      if (rk.length !== 32) return { ok: false, error: '恢复钥匙须为 32 字节（base64），已拒绝删除。' };
      for (const owner of candidates) {
        if (!fs.existsSync(encOwnerKeyPath(root, owner))) continue;
        try { if (unwrapOwnerKeyRecovery(root, owner, rk)) return { ok: true, mode: 'recovery-key' }; } catch (error) { /* 试下一个 */ }
      }
      return { ok: false, error: '恢复钥匙无法解开任何 owner key，已拒绝删除。' };
    }
    const password = String(opts.password || process.env.YOTTA_MEMORY_PASS || '');
    if (!password) {
      return { ok: false, error: '加密库删除身份必须由用户本人执行：请提供主口令（--password / YOTTA_MEMORY_PASS / 交互输入）或 --recovery-key，或用 yotta-memory view 操作。AI 不得删除身份。' };
    }
    const salt = loadSalt(root);
    if (!salt) return { ok: false, error: '密钥库损坏（缺 keys/salt），无法校验主口令；请改用 --recovery-key。' };
    const umk = deriveUmk(password, salt);
    for (const owner of candidates) {
      if (!fs.existsSync(encOwnerKeyPath(root, owner))) continue;
      try { if (unwrapOwnerKey(root, owner, umk)) return { ok: true, mode: 'password' }; } catch (error) { /* 试下一个 */ }
    }
    let rk = null;
    try { rk = unwrapRecoveryEnc(root, umk); } catch (error) { rk = null; }
    if (rk) return { ok: true, mode: 'password' };
    return { ok: false, error: '主口令不正确（用它解不开任何 owner 密钥与恢复材料），已拒绝删除；也可以改用 --recovery-key。' };
  }
  if (String(opts.agent || '').trim() !== 'user') {
    return { ok: false, error: '明文库没有可校验的用户凭据：请显式声明用户身份（CLI 加 --agent user，或用 yotta-memory view 操作）。AI 不得删除身份。' };
  }
  return { ok: true, mode: 'user-claim' };
}
function renderIdentityRemoveInventory(id, inventory, opts) {
  const lines = [
    '# 删除 AI 身份与私密记忆: ' + id,
    '',
    '将删除（私密侧；公共明文 FACT 按口径保留，其它 owner 不受影响）:',
    '- 身份登记 agents.json: ' + (inventory.registered ? '有' : '无'),
    '- owner 密钥 keys/' + id + '.key.enc: ' + (inventory.ownerKey ? '有' : '无') + (inventory.ownerRecovery ? '（含恢复侧文件）' : ''),
    '- 授权绑定 / 待领取 key / 明文缓存: ' + [inventory.binding, inventory.pending, inventory.cache].map(function (x) { return x ? '有' : '无'; }).join(' / '),
    '- 私密记忆 private/' + id + '/: ' + (inventory.memories ? inventory.memoryFiles + ' 个文件' : '无'),
    '- token / grants 引用: ' + (inventory.token ? '有 token' : '无 token') + ' / ' + (inventory.grants.length ? inventory.grants.join('；') : '无引用'),
  ];
  if (opts.keepMemories) lines.push('- 开关: --keep-memories 只删身份与授权，private/' + id + '/ 保留');
  if (opts.keepIdentity) lines.push('- 开关: --keep-identity 只删私密记忆与授权，agents.json 登记保留');
  return lines.join('\n');
}
function identityRemoveCore(root, id, opts) {
  opts = opts || {};
  root = path.resolve(root || userRoot());
  if (!isSafeAgentId(id)) {
    return { error: true, exitCode: 2, removed: [], steps: [], text: '非法 agent ID：只允许单段名称，禁止 /、\\、.. 和控制字符。' };
  }
  const inventory = identityRemoveInventory(root, id);
  if (!identityRemoveExists(inventory)) {
    return { error: false, exitCode: 0, removed: [], steps: [], inventory: inventory, text: id + ' 不存在（无需处理）。' };
  }
  const summary = renderIdentityRemoveInventory(id, inventory, opts);
  if (opts.dryRun) {
    return { error: false, exitCode: 0, dryRun: true, removed: [], steps: [], inventory: inventory, text: summary + '\n\n预演结束：未改动任何文件；确认后加 --yes 执行。' };
  }
  const authority = verifyIdentityRemoveAuthority(root, id, opts);
  if (!authority.ok) {
    return { error: true, exitCode: 2, removed: [], steps: [], inventory: inventory, text: authority.error + '\n\n' + summary };
  }
  if (!opts.yes) {
    return { error: true, exitCode: 2, removed: [], steps: [], inventory: inventory, text: summary + '\n\n需要显式确认：CLI 加 --yes，或在交互提示里输入完整 id。' };
  }
  const guard = destructiveGuardCore({
    root: root,
    action: 'identity_remove:' + id,
    snapshotDir: opts.snapshotDir,
    backupDir: opts.backupDir,
    allowSameVolumeForTest: !!opts.allowSameVolumeForTest,
    sameVolumeFn: opts.sameVolumeFn,
    now: opts.now,
  });
  if (guard.error) {
    return { error: true, exitCode: 2, removed: [], steps: [], inventory: inventory, doctor: guard.doctor, text: guard.text + '\n\n' + summary };
  }

  const steps = [];
  function step(stepId, changed, detail) {
    const meta = IDENTITY_REMOVE_STEPS.filter(function (row) { return row[0] === stepId; })[0];
    steps.push({ id: stepId, label: meta ? meta[1] : stepId, changed: !!changed, detail: detail || '' });
  }

  if (opts.keepIdentity) {
    step('agents', false, '按 --keep-identity 保留');
  } else {
    const data = loadAgents(root);
    if (data.agents && data.agents[id]) {
      delete data.agents[id];
      saveAgents(root, data);
      step('agents', true, '');
    } else {
      step('agents', false, '未登记');
    }
  }

  let keyChanged = false;
  for (const fp of [encOwnerKeyPath(root, id), encOwnerRecPath(root, id)]) {
    if (!fs.existsSync(fp)) continue;
    fs.unlinkSync(fp);
    keyChanged = true;
  }
  step('owner-key', keyChanged, keyChanged ? 'owner key 已删除（密文不可再解）' : '无密钥文件');

  const bindingPath = encAgentBindingPath(root, id);
  const bindingChanged = fs.existsSync(bindingPath);
  if (bindingChanged) fs.unlinkSync(bindingPath);
  step('binding', bindingChanged, '');

  const pendingChanged = removePendingAgentKey(root, id);
  step('pending', pendingChanged, '');

  const cacheChanged = revokeOwnerKeyCache(root, id);
  step('cache', cacheChanged, '');

  const privateDir = path.join(root, PRIVATE_DIR, id);
  if (opts.keepMemories) {
    step('memories', false, '按 --keep-memories 保留');
  } else if (fs.existsSync(privateDir)) {
    fs.rmSync(privateDir, { recursive: true, force: true });
    step('memories', true, inventory.memoryFiles + ' 个文件已删除');
  } else {
    step('memories', false, '无目录');
  }

  const tokens = loadTokens(root);
  if (Object.prototype.hasOwnProperty.call(tokens, id)) {
    delete tokens[id];
    saveTokens(root, tokens);
    step('token', true, '');
  } else {
    step('token', false, '无 token');
  }

  const grants = loadGrants(root);
  let grantChanged = false;
  if (Object.prototype.hasOwnProperty.call(grants, id)) {
    delete grants[id];
    grantChanged = true;
  }
  for (const key of Object.keys(grants)) {
    if (!Array.isArray(grants[key]) || grants[key].indexOf(id) === -1) continue;
    grants[key] = grants[key].filter(function (x) { return x !== id; });
    grantChanged = true;
  }
  if (grantChanged) fs.writeFileSync(path.join(root, 'grants.json'), JSON.stringify(grants, null, 2), 'utf8');
  step('grants', grantChanged, '');

  let reindexed = false;
  try { buildIndex(root); reindexed = true; } catch (error) { reindexed = false; }
  const auditOk = appendAudit(root, 'audit', {
    action: 'identity_remove',
    ts: new Date().toISOString(),
    transaction: guard.transaction,
    owner: id,
    snapshot: guard.snapshot ? guard.snapshot.id : '',
    authority: authority.mode,
    inventory: inventory,
    removed: steps.filter(function (s) { return s.changed; }).map(function (s) { return s.id; }),
  });
  step('reindex', reindexed || auditOk, 'reindex=' + (reindexed ? 'ok' : 'failed') + ' audit=' + (auditOk ? 'ok' : 'failed'));

  const removed = steps.filter(function (s) { return s.changed; }).map(function (s) { return s.id; });
  const lines = [summary, '', '执行结果（' + removed.length + ' / ' + steps.length + ' 步有改动）:'];
  for (const row of steps) {
    lines.push('- [' + (row.changed ? '已删除' : '未改动') + '] ' + row.label + (row.detail ? '：' + row.detail : ''));
  }
  lines.push('');
  lines.push('- 事务快照: ' + (guard.snapshot ? guard.snapshot.id : '(无)'));
  lines.push('- 公共明文 FACT 属共享事实，本命令不会删除；如需清理请单独用 forget / maintain 处理。');
  return {
    error: false,
    exitCode: 0,
    removed: removed,
    steps: steps,
    inventory: inventory,
    authority: authority.mode,
    snapshot: guard.snapshot,
    transaction: guard.transaction,
    text: lines.join('\n'),
  };
}

function keyClaimCore(root, owner, opts) {
  if (!isSafeAgentId(owner)) return { error: true, text: '非法 agent ID：只允许单段名称，禁止 /、\\、.. 和控制字符。' };
  const location = resolveAgentKeyLocation(owner, opts);
  if (!location.ok) return { error: true, text: location.error };
  const pending = encPendingPath(root, owner);
  if (!fs.existsSync(pending)) {
    return { error: true, text: '未找到待领取 agent_key：' + pending + '。请先在 yotta-memory view 中授权，或执行 yotta-memory key bind ' + owner + '。' };
  }
  let agentKey;
  try {
    agentKey = readPendingAgentKey(root, owner);
    if (!agentKey) throw new Error('pending agent_key 不存在');
    if (!unwrapAgentBinding(root, owner, agentKey)) {
      throw new Error('agent binding 不存在或已失效');
    }
  } catch (e) {
    return { error: true, text: 'agent_key 校验失败：' + e.message + '。未写入宿主目录，pending 文件保留。' };
  }
  let targetDir;
  let targetFile;
  let tempFile;
  try {
    targetFile = location.file;
    targetDir = path.dirname(targetFile);
    fs.mkdirSync(targetDir, { recursive: true });
    tempFile = path.join(targetDir, AGENT_KEY_FILENAME + '.tmp-' + process.pid + '-' + crypto.randomBytes(4).toString('hex'));
    fs.writeFileSync(tempFile, agentKey.toString('base64') + '\n', { encoding: 'utf8', mode: 0o600 });
    try { fs.chmodSync(tempFile, 0o600); } catch (e) {}
    try {
      fs.renameSync(tempFile, targetFile);
    } catch (e) {
      fs.rmSync(targetFile, { force: true });
      fs.renameSync(tempFile, targetFile);
    }
    const readBack = fs.readFileSync(targetFile, 'utf8').trim();
    if (readBack !== agentKey.toString('base64')) throw new Error('宿主 key 文件回读不一致');
  } catch (e) {
    try { if (tempFile) fs.rmSync(tempFile, { force: true }); } catch (ignore) {}
    return { error: true, text: '写入宿主 key 文件失败：' + e.message + '。pending 文件保留，可重试。' };
  }
  removePendingAgentKey(root, owner);
  let identityFile = '';
  if (opts && opts.pluginData) {
    try {
      const dataDir = path.resolve(String(opts.pluginData));
      fs.mkdirSync(dataDir, { recursive: true });
      identityFile = path.join(dataDir, 'identity.json');
      const tempIdentity = identityFile + '.tmp-' + process.pid + '-' + crypto.randomBytes(4).toString('hex');
      fs.writeFileSync(tempIdentity, JSON.stringify({ agent_id: owner }, null, 2) + '\n', { encoding: 'utf8' });
      try { fs.renameSync(tempIdentity, identityFile); }
      catch (e) { fs.rmSync(identityFile, { force: true }); fs.renameSync(tempIdentity, identityFile); }
    } catch (e) {
      identityFile = '';
    }
  }
  const identityLine = identityFile ? '\n插件身份文件: ' + identityFile : '';
  return {
    error: false,
    targetFile: targetFile,
    identityFile: identityFile,
    source: location.source,
    text: '已领取 ' + owner + ' 的 agent_key。\n目标文件: ' + targetFile + identityLine + '\n发现规则: ' + location.source + '\npending 文件已删除。',
  };
}

function keyStatusCore(root, owner, opts) {
  if (!isSafeAgentId(owner)) return { error: true, text: '非法 agent ID：只允许单段名称，禁止 /、\\、.. 和控制字符。' };
  const location = resolveAgentKeyLocation(owner, opts);
  if (!location.ok) return { error: true, text: location.error };
  const binding = fs.existsSync(encAgentBindingPath(root, owner));
  const pending = fs.existsSync(encPendingPath(root, owner));
  let hostKey = 'missing';
  if (fs.existsSync(location.file)) {
    hostKey = 'invalid';
    try {
      const key = readAgentKeyFile(location.file);
      if (binding && unwrapAgentBinding(root, owner, key)) hostKey = 'valid';
    } catch (e) {}
  }
  return {
    error: false,
    binding: binding,
    pending: pending,
    hostKey: hostKey,
    targetFile: location.file,
    source: location.source,
    text: 'agent: ' + owner + '\nbinding: ' + (binding ? 'yes' : 'no') + '\npending: ' + (pending ? 'yes' : 'no') + '\nhost_key: ' + hostKey + '\nchecked: ' + location.file + '\ndiscovery: ' + location.source,
  };
}

function keyListCore(root) {
  root = root || userRoot();
  if (!isEncrypted(root)) return { text: '记忆库未启用加密。' };
  const owners = keyOwners(root);
  const bound = owners.filter(function (o) { return fs.existsSync(encAgentBindingPath(root, o)); });
  const pending = owners.filter(function (o) { return fs.existsSync(encPendingPath(root, o)); });
  const legacy = owners.filter(function (o) { return fs.existsSync(encCachePath(root, o)); });
  const lines = [
    'owner: ' + (owners.length ? owners.join(', ') : '（无）'),
    '已绑定 agent_key: ' + (bound.length ? bound.join(', ') : '（无）'),
    '待领取 agent_key: ' + (pending.length ? pending.join(', ') : '（无）'),
    'legacy 明文 cache: ' + (legacy.length ? legacy.join(', ') + '（升级后不再加载）' : '（无）'),
  ];
  return { text: lines.join('\n'), owners: owners, bound: bound, pending: pending, legacy: legacy };
}

function cmdKeyList() {
  const root = userRoot();
  const r = keyListCore(root);
  console.log(r.text);
  if (!r.owners) return;
  const reminder = migrationReminderText(root);
  if (reminder) console.log('\n' + reminder);
}

async function cmdKeyBind(id, opts) {
  const root = userRoot();
  if (!isEncrypted(root)) { console.error('记忆库未启用加密。'); process.exit(2); }
  if (!id) { console.error('请指定 <id>：yotta-memory key bind <id>'); process.exit(2); }
  let password = opts.password || process.env.YOTTA_MEMORY_PASS || '';
  if (!password && !opts.recoveryKey) {
    const got = await resolvePasswordInput(opts, '主口令: ');
    if (got.error) { console.error(got.error); process.exit(2); }
    password = got.password;
  }
  const r = keyBindCore(root, id, { password: password, recoveryKey: opts.recoveryKey });
  console.log(r.text);
  if (r.error) process.exit(2);
}

async function cmdKeyAuthorize(id, opts) {
  console.error('提示: key authorize 已由 key bind 替代，本次按 bind 执行。');
  return cmdKeyBind(id, opts);
}

function cmdKeyRevoke(id) {
  const root = userRoot();
  if (!id) { console.error('请指定 <id>：yotta-memory key revoke <id>'); process.exit(2); }
  const r = keyRevokeCore(root, id);
  console.log(r.text);
  if (r.error) process.exit(2);
}

function cmdKeyClaim(id, opts) {
  const root = userRoot();
  if (!id) { console.error('请指定 <id>：yotta-memory key claim <id> [--to <AI_HOME> | --plugin-data <PLUGIN_DATA> | --agent-key-file <文件>]'); process.exit(2); }
  const r = keyClaimCore(root, id, opts);
  console.log(r.text);
  if (r.error) process.exit(2);
}

function cmdKeyStatus(id, opts) {
  const root = userRoot();
  if (!id) { console.error('请指定 <id>：yotta-memory key status <id> [--to <AI_HOME> | --plugin-data <PLUGIN_DATA> | --agent-key-file <文件>]'); process.exit(2); }
  const r = keyStatusCore(root, id, opts);
  console.log(r.text);
  if (r.error) process.exit(2);
}

// v0.8.1: 查看平台分页——服务端只返回当前页（offset/limit），避免记忆多了一次全量加载/渲染/传输
// v0.22.6：列表按文件时间排序需要 stat 全库；3 秒 TTL 缓存让翻页 / 搜索重复请求保持轻快。
const VIEW_STAT_CACHE = new Map();
const VIEW_STAT_TTL_MS = 3000;
function viewStatCached(fp) {
  const now = Date.now();
  const hit = VIEW_STAT_CACHE.get(fp);
  if (hit && now - hit.at < VIEW_STAT_TTL_MS) return hit.st;
  let st = null;
  try { st = fs.statSync(fp); } catch (err) { st = null; }
  if (VIEW_STAT_CACHE.size > 20000) VIEW_STAT_CACHE.clear();
  VIEW_STAT_CACHE.set(fp, { st: st, at: now });
  return st;
}
function viewEntriesCore(root, session, query, offset, limit, type, owner) {
  limit = Math.max(1, parseInt(limit, 10) || 50);
  offset = Math.max(0, parseInt(offset, 10) || 0);
  const q = String(query || '').toLowerCase();
  const entries = [];
  for (const e of (loadIndex(root) || [])) entries.push(e);
  for (const o of collectOwners(root)) {
    const key = session.ownerKeys[o];
    if (!key) continue;
    try { for (const e of loadOwnerIndex(root, o, key)) entries.push(e); } catch (err) {}
  }
  let all = q ? entries.filter(function (e) {
    const hay = (e.subject || '') + ' ' + (e.statement || '') + ' ' + (e.tags || []).join(' ') + ' ' + (e.owner || '') + ' ' + (e.file || '');
    return hay.toLowerCase().indexOf(q) !== -1;
  }) : entries;
  const ownerFilter = String(owner || '').trim();
  if (ownerFilter) {
    all = all.filter(function (e) { return String(e.owner || '') === ownerFilter; });
  }
  // v0.22.8：chips 计数跟随当前 owner + 查询筛选（在类型过滤前统计），避免选中智能体后仍显示全局数。
  const counts = { all: all.length, FACT: 0, PREF: 0, BOUND: 0, COMMIT: 0 };
  for (const e of all) {
    const t = String(e.type || 'FACT').toUpperCase();
    if (counts[t] !== undefined) counts[t] += 1;
  }
  const typeFilter = String(type || '').toUpperCase();
  if (typeFilter && typeFilter !== 'ALL') {
    all = all.filter(function (e) { return String(e.type || '').toUpperCase() === typeFilter; });
  }
  // v0.22.6：默认按时间倒序（文件 mtime 优先，其次 updated/created 与文件名），最新在最前。
  const decorated = all.map(function (e) {
    const st = viewStatCached(path.join(root, String(e.file || '')));
    return { e: e, st: st, t: st && st.mtimeMs ? st.mtimeMs : 0 };
  });
  decorated.sort(function (a, b) {
    if (b.t !== a.t) return b.t - a.t;
    const ka = String(a.e.updated || a.e.created || '');
    const kb = String(b.e.updated || b.e.created || '');
    if (ka !== kb) return kb.localeCompare(ka);
    return String(b.e.file || '').localeCompare(String(a.e.file || ''));
  });
  const count = decorated.length;
  const page = decorated.slice(offset, offset + limit).map(function (x) {
    const out = Object.assign({}, x.e);
    if (x.st) {
      out.mtime = x.st.mtime ? x.st.mtime.toISOString() : '';
      out.btime = x.st.birthtime && !isNaN(x.st.birthtime.getTime()) ? x.st.birthtime.toISOString() : '';
    }
    return out;
  });
  return { count: count, offset: offset, limit: limit, hasMore: offset + limit < count, counts: counts, entries: page };
}

// ---- v0.21.0 M1：记忆管理台（view）真读写 ----
function viewOverviewCore(root, session) {
  const entries = [];
  for (const e of (loadIndex(root) || [])) entries.push(e);
  for (const o of collectOwners(root)) {
    const key = session && session.ownerKeys ? session.ownerKeys[o] : null;
    if (!key) continue;
    try { for (const e of loadOwnerIndex(root, o, key)) entries.push(e); } catch (err) {}
  }
  const byType = { FACT: 0, PREF: 0, BOUND: 0, COMMIT: 0 };
  for (const e of entries) {
    const t = String(e.type || 'FACT').toUpperCase();
    if (byType[t] !== undefined) byType[t] += 1;
  }
  const owners = keyOwners(root).map(function (o) {
    return { owner: o, authorized: fs.existsSync(encAgentBindingPath(root, o)) };
  });
  let bytes = 0;
  let files = 0;
  for (const fp of collectEntryFiles(root)) {
    files += 1;
    try { bytes += fs.statSync(fp).size; } catch (e) {}
  }
  const archivedFiles = [];
  const archiveBase = path.join(root, ARCHIVE_DIR);
  if (fs.existsSync(archiveBase)) walkEntryFiles(archiveBase, archivedFiles);
  const cfg = loadConfig();
  return {
    total: entries.length,
    files: files,
    byType: byType,
    owners: owners,
    authorized: owners.filter(function (o) { return o.authorized; }).length,
    bytes: bytes,
    archived: archivedFiles.length,
    backupDir: cfg.backup_dir || '',
  };
}

function viewRememberCore(root, payload) {
  payload = payload || {};
  const type = String(payload.type || '').toUpperCase();
  if (!TYPE_DIRS[type]) return { error: true, text: '未知记忆类型: ' + payload.type };
  const scope = payload.scope || defaultScope(type);
  const owner = String(payload.owner || '');
  if (scope === 'private' && !isSafeAgentId(owner)) return { error: true, text: '私密记忆必须选择归属智能体（owner）。' };
  return rememberCore(type, payload.subject, payload.statement, {
    root: root,
    owner: owner,
    scope: scope,
    tags: Array.isArray(payload.tags) ? payload.tags : [],
    weight: payload.weight,
    source: 'view',
    hint: false,
    userUnlocked: true,
  });
}

function viewUpdateCore(root, payload) {
  payload = payload || {};
  const found = resolveMemoryFile(root, String(payload.file || ''));
  if (!found) return { error: true, text: '未找到记忆文件: ' + payload.file };
  const rel = found.rel;
  const owner = ownerFromPrivatePath(root, found.fp);
  let parsedOriginal;
  try { parsedOriginal = parseFrontmatter(readMemoryText(root, found.fp, owner)); } catch (e) { return { error: true, text: '读取失败: ' + e.message }; }
  if (!parsedOriginal || !parsedOriginal.meta) return { error: true, text: '读取失败: 无法解析记忆文件' };
  const original = parsedOriginal.meta;
  const type = String(original.type || 'FACT').toUpperCase();
  const patch = {};
  let ownerChange = null;
  if (payload.subject !== undefined) {
    const s = String(payload.subject).trim();
    if (!s) return { error: true, text: 'subject 不能为空' };
    patch.subject = s;
  }
  if (payload.statement !== undefined) {
    const s = String(payload.statement).trim();
    if (!s) return { error: true, text: 'statement 不能为空' };
    patch.statement = s;
  }
  if (payload.tags !== undefined) {
    patch.tags = Array.isArray(payload.tags) ? payload.tags.map(String).filter(Boolean) : parseTags(String(payload.tags));
  }
  if (payload.owner !== undefined) {
    const nextOwner = String(payload.owner || '').trim();
    const currentOwner = String(original.owner || '').trim();
    if (nextOwner !== currentOwner) {
      if (type !== 'FACT') {
        return { error: true, text: '私密记忆（' + type + '）的归属不可直接修改；如需变更请删除后重写，或等待「归属迁移」功能。' };
      }
      if (nextOwner && !isSafeAgentId(nextOwner)) {
        return { error: true, text: '归属 AI ID 非法：只允许单段名称，禁止 /、\\、.. 和控制字符。' };
      }
      patch.owner = nextOwner;
      ownerChange = { from: currentOwner, to: nextOwner };
    }
  }
  if (!Object.keys(patch).length) return { error: true, text: '没有可更新的字段（subject / statement / tags / owner）。' };
  const ts = new Date().toISOString().replace(/[:.]/g, '-');
  const undoRel = path.posix.join('.trash', 'view-history', ts, rel);
  const undoPath = path.join(root, undoRel);
  try {
    fs.mkdirSync(path.dirname(undoPath), { recursive: true });
    fs.copyFileSync(found.fp, undoPath);
  } catch (e) { return { error: true, text: '编辑前备份失败: ' + e.message }; }
  patch.updated = today();
  // 常规条目约定 body 镜像 statement；长文（如 distill 报告）保留原 body。
  const bodyMirrorsStatement = String(parsedOriginal.body || '').trim() === String(original.statement || '').trim();
  const nextBody = patch.statement !== undefined && bodyMirrorsStatement ? patch.statement : undefined;
  try { rewriteFrontmatter(found.fp, patch, root, owner, nextBody); } catch (e) { return { error: true, text: '更新失败: ' + e.message }; }
  upsertIndexEntry(root, readEntry(found.fp, root));
  appendAudit(root, 'audit', {
    action: 'view_update',
    ts: new Date().toISOString(),
    file: rel,
    undo: undoRel,
    before_updated: original.updated || '',
    ...(ownerChange ? { owner_from: ownerChange.from, owner_to: ownerChange.to } : {}),
  });
  return {
    error: false,
    file: rel,
    undo: undoRel,
    ...(ownerChange ? { ownerChange: ownerChange } : {}),
    text: '已更新: ' + rel + (ownerChange ? '（归属 ' + (ownerChange.from || '公共') + ' → ' + (ownerChange.to || '公共') + '）' : ''),
  };
}

function viewDeleteCore(root, payload) {
  payload = payload || {};
  const result = forgetCore(String(payload.file || ''), { root: root, userUnlocked: true });
  if (result.error) return result;
  appendAudit(root, 'audit', { action: 'view_delete', ts: new Date().toISOString(), file: payload.file, trash: result.trash || '' });
  return { error: false, file: payload.file, trash: result.trash || '', text: result.text };
}

function viewRestoreCore(root, payload) {
  payload = payload || {};
  const ref = String(payload.ref || '').replace(/\\/g, '/');
  if (ref.indexOf('.trash/') !== 0) return { error: true, text: '只能从回收区 / 编辑历史恢复。' };
  const abs = resolveWithinRoot(root, ref);
  if (!abs || !fs.existsSync(abs) || fs.statSync(abs).isDirectory()) return { error: true, text: '回收区文件不存在: ' + ref };
  const seg = ref.split('/');
  const isHistory = seg[1] === 'view-history';
  const originalRel = isHistory ? seg.slice(3).join('/') : seg.slice(2).join('/');
  if (!originalRel) return { error: true, text: '无法解析原路径。' };
  const dest = resolveWithinRoot(root, originalRel);
  if (!dest) return { error: true, text: '原路径非法。' };
  let redoRel = null;
  if (fs.existsSync(dest)) {
    // 编辑历史撤销允许覆盖：先把当前版本留作重做快照；回收区直恢复仍 fail-closed。
    if (!isHistory) return { error: true, text: '原位置已有文件，拒绝覆盖: ' + originalRel };
    const ts = new Date().toISOString().replace(/[:.]/g, '-');
    redoRel = path.posix.join('.trash', 'view-history', ts, originalRel);
    const redoAbs = path.join(root, redoRel);
    try {
      fs.mkdirSync(path.dirname(redoAbs), { recursive: true });
      fs.renameSync(dest, redoAbs);
    } catch (e) { return { error: true, text: '撤销失败: 当前版本快照失败: ' + e.message }; }
  }
  try {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.renameSync(abs, dest);
  } catch (e) {
    if (redoRel) { try { fs.renameSync(path.join(root, redoRel), dest); } catch (_) { /* keep redo copy */ } }
    return { error: true, text: '恢复失败: ' + e.message };
  }
  upsertIndexEntry(root, readEntry(dest, root));
  appendAudit(root, 'audit', {
    action: 'view_restore',
    ts: new Date().toISOString(),
    file: originalRel,
    from: ref,
    ...(redoRel ? { redo: redoRel } : {}),
  });
  return { error: false, file: originalRel, ...(redoRel ? { redo: redoRel } : {}), text: '已恢复: ' + originalRel };
}

function viewArchiveCore(root, payload) {
  payload = payload || {};
  const found = resolveMemoryFile(root, String(payload.file || ''));
  if (!found) return { error: true, text: '未找到记忆文件: ' + payload.file };
  const rel = found.rel;
  const owner = ownerFromPrivatePath(root, found.fp);
  let meta;
  try { meta = parseFrontmatter(readMemoryText(root, found.fp, owner)).meta; } catch (e) { return { error: true, text: '读取失败: ' + e.message }; }
  const type = String(meta.type || 'FACT').toUpperCase();
  const destRel = archiveRelFor(root, rel, type, owner);
  const dest = resolveWithinRoot(root, destRel);
  if (!dest) return { error: true, text: '归档路径非法。' };
  if (fs.existsSync(dest)) return { error: true, text: '归档区已存在同名文件，拒绝覆盖: ' + destRel };
  try {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.renameSync(found.fp, dest);
  } catch (e) { return { error: true, text: '归档失败: ' + e.message }; }
  removeIndexEntry(root, rel);
  appendAudit(root, 'audit', { action: 'view_archive', ts: new Date().toISOString(), file: rel, archive: destRel });
  return { error: false, file: rel, archive: destRel, text: '已藏起来（归档）: ' + rel };
}

function viewUnarchiveCore(root, payload) {
  payload = payload || {};
  const ref = String(payload.archive || payload.file || '').replace(/\\/g, '/');
  if (ref.indexOf(ARCHIVE_DIR + '/') !== 0) return { error: true, text: '只能从归档区放回。' };
  const abs = resolveWithinRoot(root, ref);
  if (!abs || !fs.existsSync(abs) || fs.statSync(abs).isDirectory()) return { error: true, text: '归档文件不存在: ' + ref };
  const originalRel = ref.slice(ARCHIVE_DIR.length + 1);
  const dest = resolveWithinRoot(root, originalRel);
  if (!dest) return { error: true, text: '原路径非法。' };
  if (fs.existsSync(dest)) return { error: true, text: '原位置已有文件，拒绝覆盖: ' + originalRel };
  try {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.renameSync(abs, dest);
  } catch (e) { return { error: true, text: '放回失败: ' + e.message }; }
  upsertIndexEntry(root, readEntry(dest, root));
  appendAudit(root, 'audit', { action: 'view_unarchive', ts: new Date().toISOString(), file: originalRel, archive: ref });
  return { error: false, file: originalRel, text: '已放回: ' + originalRel };
}

function viewArchiveListCore(root) {
  const files = [];
  const base = path.join(root, ARCHIVE_DIR);
  if (fs.existsSync(base)) walkEntryFiles(base, files);
  return {
    entries: files.map(function (fp) {
      return { ref: relOf(root, fp), original: path.relative(base, fp).replace(/\\/g, '/') };
    }),
  };
}

function viewTrashListCore(root) {
  const files = [];
  const base = path.join(root, '.trash');
  if (fs.existsSync(base)) walkEntryFiles(base, files);
  return {
    entries: files.map(function (fp) {
      const ref = relOf(root, fp);
      const seg = ref.split('/');
      const history = seg[1] === 'view-history';
      return { ref: ref, kind: history ? 'history' : 'trash', original: history ? seg.slice(3).join('/') : seg.slice(2).join('/') };
    }),
  };
}

function viewHostName(req) {
  const raw = String(req.headers.host || '').trim();
  if (!raw) return '';
  try {
    return new URL('http://' + raw).hostname.toLowerCase().replace(/^\[|\]$/g, '');
  } catch (e) {
    return '';
  }
}
function viewHostAllowed(req, bindHost) {
  const name = viewHostName(req);
  if (!name) return false;
  const bind = String(bindHost || '').trim().toLowerCase().replace(/^\[|\]$/g, '');
  if (bind !== '127.0.0.1' && bind !== 'localhost' && bind !== '::1') return true;
  return name === '127.0.0.1' || name === 'localhost' || name === '::1';
}
function viewOriginAllowed(req) {
  const origin = req.headers.origin;
  if (!origin) return true;
  let originHost = '';
  try {
    originHost = new URL(String(origin)).host.toLowerCase();
  } catch (e) {
    return false;
  }
  const requestHost = String(req.headers.host || '').trim().toLowerCase();
  return !!requestHost && originHost === requestHost;
}
function viewServerCore(root, port, host, opts) {
  opts = opts || {};
  let session = { umk: null, ownerKeys: {} };
  const server = http.createServer(function (req, res) {
    if (!viewHostAllowed(req, host) || !viewOriginAllowed(req)) {
      res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store' });
      res.end('forbidden');
      return;
    }
    let pathname = '/';
    try { pathname = new URL(req.url, 'http://' + (req.headers.host || 'localhost')).pathname; } catch (e) {}
    function json(code, obj) {
      res.writeHead(code, {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-store',
        'X-Content-Type-Options': 'nosniff',
      });
      res.end(JSON.stringify(obj));
    }
    function readBody(cb) {
      let body = '';
      req.on('data', function (c) { body += c; });
      req.on('end', function () {
        let d = {};
        try { d = JSON.parse(body || '{}'); } catch (e) {}
        cb(d);
      });
    }
    if (req.method === 'GET' && pathname === '/') {
      res.writeHead(200, {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'no-store',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'",
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'Referrer-Policy': 'no-referrer',
      });
      res.end(viewHtml());
      return;
    }
    if (req.method === 'POST' && pathname === '/api/status') {
      return json(200, { encrypted: isEncrypted(root), unlocked: !!session.umk, version: VERSION, rootId: memoryRootId(root) });
    }
    if (req.method === 'POST' && pathname === '/api/unlock') {
      return readBody(function (d) {
        const password = String(d.password || '');
        const salt = loadSalt(root);
        if (!salt) return json(400, { error: '记忆库未启用加密。' });
        const umk = deriveUmk(password, salt);
        const ownerKeys = {};
        const owners = keyOwners(root);
        let verified = false;
        for (const o of owners) {
          try { ownerKeys[o] = unwrapOwnerKey(root, o, umk); verified = true; } catch (e) {}
        }
        if (!verified && owners.length === 0) {
          try { unwrapRecoveryEnc(root, umk); verified = true; } catch (e) {}
        }
        if (!verified) return json(401, { error: owners.length === 0 ? '口令错误；空加密库已用恢复钥匙校验失败。' : '口令错误。' });
        session = { umk: umk, ownerKeys: ownerKeys };
        try { VIEW_KEYS_CONTEXT.run({ keys: ownerKeys }, function () { maybeHealIndex(root, { force: true }); }); } catch (e) { /* 静默校准失败不阻断解锁 */ }
        json(200, {
          ok: true,
          owners: Object.keys(ownerKeys),
          hint: owners.length === 0 ? '当前没有 owner。请先在终端执行 yotta-memory iam <id>，再回到本页授权。' : '',
        });
      });
    }
    if (req.method === 'POST' && pathname === '/api/owners') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      const agents = loadAgents(root).agents || {};
      const owners = keyOwners(root);
      const all = Array.from(new Set(owners.concat(Object.keys(agents))));
      return json(200, {
        owners: all.map(function (o) { return { owner: o, registered: !!agents[o], authorized: fs.existsSync(encAgentBindingPath(root, o)) }; }),
        hint: all.length ? '' : '当前没有 owner。请先在终端执行 yotta-memory iam <id>，再回到本页授权。',
      });
    }
    if (req.method === 'POST' && pathname === '/api/entries') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return readBody(function (d) {
        try { VIEW_KEYS_CONTEXT.run({ keys: session.ownerKeys }, function () { maybeHealIndex(root); }); } catch (e) { /* 静默校准失败不阻断查询 */ }
        json(200, viewEntriesCore(root, session, d.query, d.offset, d.limit, d.type, d.owner));
      });
    }
    if (req.method === 'POST' && pathname === '/api/help') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return json(200, { version: VERSION, quick: VIEW_HELP_QUICK, groups: HELP_MODEL, configKeys: CONFIG_VALUE_KEYS, configKeyHelp: CONFIG_KEY_HELP });
    }
    if (req.method === 'POST' && pathname === '/api/overview') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return json(200, VIEW_KEYS_CONTEXT.run({ keys: session.ownerKeys }, function () {
        try { maybeHealIndex(root); } catch (e) { /* 静默校准失败不阻断概览 */ }
        return viewOverviewCore(root, session);
      }));
    }
    if (req.method === 'POST' && pathname === '/api/memory/create') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return readBody(function (d) {
        const r = VIEW_KEYS_CONTEXT.run({ keys: session.ownerKeys }, function () { return viewRememberCore(root, d); });
        json(r.error ? 400 : 200, r);
      });
    }
    if (req.method === 'POST' && pathname === '/api/memory/update') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return readBody(function (d) {
        const r = VIEW_KEYS_CONTEXT.run({ keys: session.ownerKeys }, function () { return viewUpdateCore(root, d); });
        json(r.error ? 400 : 200, r);
      });
    }
    if (req.method === 'POST' && pathname === '/api/memory/delete') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return readBody(function (d) {
        const r = VIEW_KEYS_CONTEXT.run({ keys: session.ownerKeys }, function () { return viewDeleteCore(root, d); });
        json(r.error ? 400 : 200, r);
      });
    }
    if (req.method === 'POST' && pathname === '/api/memory/restore') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return readBody(function (d) {
        const r = VIEW_KEYS_CONTEXT.run({ keys: session.ownerKeys }, function () { return viewRestoreCore(root, d); });
        json(r.error ? 400 : 200, r);
      });
    }
    if (req.method === 'POST' && pathname === '/api/memory/archive') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return readBody(function (d) {
        const r = VIEW_KEYS_CONTEXT.run({ keys: session.ownerKeys }, function () { return viewArchiveCore(root, d); });
        json(r.error ? 400 : 200, r);
      });
    }
    if (req.method === 'POST' && pathname === '/api/memory/unarchive') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return readBody(function (d) {
        const r = VIEW_KEYS_CONTEXT.run({ keys: session.ownerKeys }, function () { return viewUnarchiveCore(root, d); });
        json(r.error ? 400 : 200, r);
      });
    }
    if (req.method === 'POST' && pathname === '/api/trash') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return json(200, viewTrashListCore(root));
    }
    if (req.method === 'POST' && pathname === '/api/archived') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return json(200, viewArchiveListCore(root));
    }
    if (req.method === 'POST' && pathname === '/api/export') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      const memories = [];
      for (const e of (loadIndex(root) || [])) memories.push({ file: e.file, meta: e.meta });
      for (const o of collectOwners(root)) {
        const key = session.ownerKeys[o];
        if (!key) continue;
        try { for (const e of loadOwnerIndex(root, o, key)) memories.push({ file: e.file, meta: e.meta }); } catch (err) {}
      }
      return json(200, { format: 'yottamemory', version: 2, exported: today(), memories: memories });
    }
    if (req.method === 'POST' && pathname === '/api/authorize') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return readBody(function (d) {
        const owner = String(d.owner || '');
        if (!owner) return json(400, { error: '缺少 owner。' });
        if (!isSafeAgentId(owner)) return json(400, { error: '非法 owner ID：只允许单段名称，禁止 /、\\、.. 和控制字符。' });
        if (fs.existsSync(encAgentBindingPath(root, owner))) {
          return json(409, { error: '该智能体已有 agent binding。为避免打断在用的 agent_key，请先“吊销”，再重新授权生成新 key。' });
        }
        let ok = session.ownerKeys[owner];
        let rk = null;
        try { rk = unwrapRecoveryEnc(root, session.umk); } catch (e) { rk = null; }
        if (!ok) {
          if (!rk) return json(400, { error: '密钥库缺少恢复钥匙（recovery.key.enc），无法为新 owner 建钥。' });
          ok = recoverOwnerKeyFromRecovery(root, owner, session.umk, rk);
          if (!ok) {
            if (privateOwnerHasData(root, owner)) {
              return json(400, { error: '检测到 private/' + owner + ' 仍有密文，但 keys/' + owner + '.key.enc 与恢复文件均不可用；拒绝新建 owner key（会导致旧数据无法解密）。请从备份恢复原 owner key，或使用 CLI 恢复钥匙修复后重试。' });
            }
            ok = wrapOwnerKey(root, session.umk, rk, owner);
          }
          session.ownerKeys[owner] = ok;
        }
        const agentKey = crypto.randomBytes(32);
        const pendingFile = writeAgentBindingWithPending(root, owner, ok, agentKey);
        revokeOwnerKeyCache(root, owner);
        json(200, { ok: true, agentKey: agentKey.toString('base64'), pendingFile: pendingFile, text: 'agent_key 只显示一次，请用户自行保存；AI 可由 pending 文件领取并写入宿主目录。' });
      });
    }
    if (req.method === 'POST' && pathname === '/api/revoke') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return readBody(function (d) {
        const owner = String(d.owner || '');
        if (!isSafeAgentId(owner)) return json(400, { error: '非法 owner ID：只允许单段名称，禁止 /、\\、.. 和控制字符。' });
        const binding = encAgentBindingPath(root, owner);
        if (fs.existsSync(binding)) fs.unlinkSync(binding);
        removePendingAgentKey(root, owner);
        revokeOwnerKeyCache(root, owner);
        json(200, { ok: true });
      });
    }
    if (req.method === 'POST' && pathname === '/api/identity-remove') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return readBody(function (d) {
        const owner = String((d && d.owner) || '');
        const confirm = String((d && d.confirm) || '');
        if (!isSafeAgentId(owner)) return json(400, { error: '非法 owner ID：只允许单段名称，禁止 /、\\、.. 和控制字符。' });
        if (confirm !== owner) return json(400, { error: '确认串不匹配：请输入完整 agent ID 以确认删除。' });
        const result = identityRemoveCore(root, owner, {
          yes: true,
          userUnlocked: true,
          snapshotDir: opts.snapshotDir,
          backupDir: opts.backupDir,
          allowSameVolumeForTest: !!opts.allowSameVolumeForTest,
          now: opts.now,
        });
        if (result.error) return json(400, { error: result.text });
        json(200, { ok: true, removed: result.removed, steps: result.steps, text: result.text });
      });
    }
    if (req.method === 'POST' && pathname === '/api/reset-password') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      return readBody(function (d) {
        const r = resetPasswordCore(root, { password: String(d.currentPassword || ''), recoveryKey: String(d.recoveryKey || ''), newPassword: String(d.newPassword || '') });
        if (r.error) return json(400, { error: r.text });
        const salt = loadSalt(root);
        if (salt) session = { umk: deriveUmk(String(d.newPassword || ''), salt), ownerKeys: {} };
        json(200, { ok: true, text: r.text });
      });
    }
    if (req.method === 'POST' && pathname === '/api/recovery-key') {
      if (!session.umk) return json(401, { error: '请先解锁。' });
      const rk = unwrapRecoveryEnc(root, session.umk);
      if (!rk) return json(400, { error: '未找到恢复钥匙。' });
      return json(200, { recoveryKey: rk.toString('base64') });
    }
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('not found');
  });
  server.on('error', function (e) {
    const message = 'yotta-memory view 启动失败: ' + (e && e.message ? e.message : String(e)) + '；请检查端口是否被占用，或使用 --port <其它端口>。';
    if (typeof opts.onError === 'function') {
      opts.onError(e, message);
      return;
    }
    console.error(message);
  });
  try { maybeHealIndex(root, { force: true }); } catch (e) { /* 启动静默校准失败不阻断服务 */ }
  server.listen(port, host, function () {
    console.log('yotta-memory 用户查看平台已启动（v' + VERSION + '）');
    console.log('URL: http://' + host + ':' + port + '（默认仅本机 127.0.0.1；远程需 --host 显式开启）');
    console.log('记忆库: ' + root);
    console.log('输入主口令解锁后可浏览 / 搜索 / 导出全部 AI 的记忆（含私密）。');
    console.log('按 Ctrl+C 停止');
  });
  return server;
}

function probeViewPort(host, port) {
  return new Promise(function (resolve) {
    const socket = net.connect({ host: host, port: port });
    let done = false;
    function finish(state) {
      if (done) return;
      done = true;
      try { socket.destroy(); } catch (e) {}
      resolve(state);
    }
    socket.setTimeout(800, function () { finish('timeout'); });
    socket.once('connect', function () { finish('open'); });
    socket.once('error', function (e) { finish(e && e.code === 'ECONNREFUSED' ? 'closed' : 'error'); });
  });
}

function probeViewStatus(host, port) {
  return new Promise(function (resolve) {
    const body = JSON.stringify({});
    const req = http.request({
      host: host,
      port: port,
      path: '/api/status',
      method: 'POST',
      timeout: 800,
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
    }, function (res) {
      let data = '';
      res.on('data', function (chunk) { data += chunk; });
      res.on('end', function () {
        try {
          const parsed = JSON.parse(data);
          if (!parsed.version || typeof parsed.unlocked !== 'boolean') {
            resolve({ detected: false });
            return;
          }
          resolve({
            detected: true,
            rootId: typeof parsed.rootId === 'string' ? parsed.rootId : '',
            version: String(parsed.version),
            unlocked: !!parsed.unlocked,
          });
        } catch (e) {
          resolve({ detected: false });
        }
      });
    });
    req.on('timeout', function () { req.destroy(); resolve({ detected: false }); });
    req.on('error', function () { resolve({ detected: false }); });
    req.end(body);
  });
}

async function cmdView(opts) {
  const root = userRoot();
  ensureInit(root);
  if (!isEncrypted(root)) {
    console.log('记忆库未启用加密（无 keys/）。yotta-memory view 是加密库的用户查看平台；请先 init --encrypt 或 migrate。');
    process.exit(2);
  }
  const host = opts.host || '127.0.0.1';
  const port = opts.port || 8788;
  const state = await probeViewPort(host, port);
  if (state === 'open') {
    const status = await probeViewStatus(host, port);
    if (status.detected && status.rootId === memoryRootId(root)) {
      console.log('检测到已在运行的 yotta-memory view: http://' + host + ':' + port + '（无需重复启动）');
      return;
    }
    if (status.detected) {
      const reason = status.rootId
        ? '该服务属于另一个 memory_home（rootId 不匹配）'
        : '该服务是旧版 view，未提供 memory_home 指纹（rootId）';
      console.error('检测到端口 ' + host + ':' + port + ' 上的 yotta-memory view 无法复用：' + reason + '。请关闭该进程，或使用 --port <其它端口>。');
      process.exit(2);
    }
    console.error('端口已被占用: ' + host + ':' + port + '。请关闭占用进程，或使用 --port <其它端口>。');
    process.exit(2);
  }
  viewServerCore(root, port, host, {
    onError: function (e, message) {
      console.error(message);
      process.exit(2);
    },
  });
}

function viewHtml() {
  return VIEW_HTML;
}

// ---- 命令包装（CLI 入口）----
async function cmdInit(opts) {
  const root = opts.dir ? path.resolve(String(opts.dir)) : (opts.project ? projectRoot() : userRoot());
  if (isExistingStore(root) && !opts.attach) {
    const blocked = initCore(Object.assign({}, opts));
    console.log(blocked.text);
    if (blocked.error) process.exit(2);
    return;
  }
  const fresh = !isExistingStore(root);
  const wantEncrypt = opts.encrypt || (!opts.noEncrypt && fresh);
  let o = Object.assign({}, opts);
  if (wantEncrypt && !o.password) {
    const got = await resolvePasswordInput(o, '主口令（启用加密，勿忘；忘口令可用恢复钥匙重设）: ');
    if (got.error) { console.error(got.error); process.exit(2); }
    if (got.source === 'prompt') {
      const pw2 = await promptPassword('再次输入确认: ');
      if (pw2 !== got.password) { console.error('两次输入不一致。'); process.exit(2); }
    }
    o.password = got.password;
  }
  const r = initCore(o);
  console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdRemember(type, subject, statement, opts) {
  const o = Object.assign({}, opts);
  if (o.noHint) o.hint = false;
  const r = rememberCore(type, subject, statement, o);
  console.log(r.text);
  if (!r.error) {
    const note = identityWriteNote(resolveIdentity(o), o);
    if (note) console.error(note);
  }
  if (r.error) process.exit(2);
}
function cmdRecall(query, opts) {
  const r = recallCore(query, opts);
  console.log(r.text);
  if (r.exitCode) process.exit(r.exitCode);
}
function cmdFeedback(ref, opts) {
  const r = feedbackCore(ref, opts);
  console.log(r.text);
  if (r.exitCode) process.exit(r.exitCode);
  if (r.error) process.exit(2);
}
function cmdExplain(ref, opts) {
  const r = explainCore(ref, opts);
  console.log(r.text);
  if (r.exitCode) process.exit(r.exitCode);
  if (r.error) process.exit(2);
}
function cmdMaintain(opts) {
  if (opts.capacity) {
    const r = capacityCore(opts);
    if (opts.json && r.report) console.log(JSON.stringify(r.report, null, 2));
    else console.log(r.text);
    if (r.error) process.exit(2);
    return;
  }
  if (opts.merge) {
    const parts = String(opts.merge).split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    if (parts.length < 2) { console.error('--merge 需要两个文件，逗号分隔'); process.exit(2); }
    const r = mergeCore(parts[0], parts[1], opts);
    console.log(r.text);
    if (r.error) process.exit(2);
    return;
  }
  const r = maintainCore(opts);
  console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdDistill(opts) {
  const r = distillCore(opts);
  if (opts.json && r.report) console.log(JSON.stringify(r.report, null, 2));
  else console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdForget(fileRef, opts) {
  const ident = resolveIdentity(opts);
  if (ident.error) {
    console.log(ident.error);
    process.exit(3);
  }
  const r = forgetCore(fileRef, {
    selfAgent: ident.id,
    unsafe: !!(opts && opts.unsafe),
  });
  console.log(r.text);
  const note = identityWriteNote(ident, opts);
  if (note) console.error(note);
  if (r.error) process.exit(2);
}

function cmdRename(fileRef, newName, opts) {
  const ident = resolveIdentity(opts);
  if (ident.error) {
    console.log(ident.error);
    process.exit(3);
  }
  const r = renameCore(fileRef, newName, {
    selfAgent: ident.id,
    unsafe: !!(opts && opts.unsafe),
    dryRun: !!(opts && opts.dryRun),
    reason: opts && opts.reason,
  });
  console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdArchive(opts) {
  const r = archiveCore(opts);
  if (opts.json && r.report) console.log(JSON.stringify(r.report, null, 2));
  else console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdBackupCreate(opts) {
  const r = backupCreateCore(opts);
  console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdBackupVolumes(opts) {
  const r = listBackupVolumesCore(opts);
  if (opts.json) console.log(JSON.stringify({ root: userRoot(), volumes: r.volumes }, null, 2));
  else console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdBackupSetup(opts) {
  const r = backupSetupCore(opts);
  console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdBackupStatus(opts) {
  const r = backupStatusCore(opts);
  if (opts.json) console.log(JSON.stringify(r, null, 2));
  else console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdBackupEnsureDaily(opts) {
  const r = backupEnsureDailyCore(opts);
  console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdBackupSchedule(action, opts) {
  let r;
  if (action === 'enable') {
    const runtime = runtimeEnsureForManagedTask();
    if (runtime.error) {
      console.error('runtime 稳定入口未就绪，拒绝注册备份任务: ' + runtime.text);
      process.exit(1);
    }
    opts = Object.assign({}, opts, { scriptPath: runtimeManagedScript() });
    r = backupScheduleEnableCore(opts);
  }
  else if (action === 'disable') r = backupScheduleDisableCore(opts);
  else if (action === 'status') r = backupScheduleStatusCore(opts);
  else {
    console.error('backup schedule 子命令: enable [--time HH:MM] / disable / status');
    process.exit(2);
  }
  console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdBackupList(opts) {
  const r = backupListCore(opts);
  console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdBackupDoctor(opts) {
  const r = backupDoctorCore(opts);
  console.log(r.text);
  if (r.error || !r.ok) process.exit(2);
}
function cmdIndex(opts) {
  if (!opts.stats) {
    console.error('index 只提供只读统计：请使用 yotta-memory index --stats [--json]。');
    process.exit(2);
  }
  const r = indexStatsCore(opts);
  if (opts.json) console.log(JSON.stringify(r, null, 2));
  else console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdLayout(action, opts) {
  let r;
  if (action === 'plan') r = layoutPlanCore(opts);
  else if (action === 'apply') r = layoutApplyCore(Object.assign({}, opts, { planFile: opts.fromPlan }));
  else if (action === 'rollback') r = layoutRollbackCore(opts);
  else {
    console.error('layout 子命令: plan [--threshold N] [--include-flat] [--out <文件>] / apply --from-plan <文件> --yes / rollback --batch <id> --yes');
    process.exit(2);
  }
  if (opts.json) console.log(JSON.stringify(r, null, 2));
  else console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdBackupRestore(id, opts) {
  const r = backupRestoreCore(id, opts);
  console.log(r.text);
  if (r.error) process.exit(2);
}
async function cmdBackupDrill(id, opts) {
  const run = function (extra) {
    return backupDrillCore(Object.assign({}, opts, { id: id || opts.id }, extra || {}));
  };
  let r = run();
  // v0.22.8：备份含加密私密条目且未给凭证时，复用统一凭证入口（--password / --password-stdin / YOTTA_MEMORY_PASS / 交互）。
  if (r.needPassword) {
    const got = await resolvePasswordInput(opts, '主口令（恢复演练解密私密记忆）: ');
    if (got.error) { console.error(got.error); process.exit(2); }
    r = run({ password: got.password });
  }
  console.log(r.text);
  if (r.error) process.exit(2);
}
function cmdDoctor(opts) {
  const r = doctorCore(opts);
  if (opts.json) console.log(JSON.stringify(r, null, 2));
  else console.log(r.text);
  if (!r.ok) process.exit(2);
  if (r.baselineError) process.exit(2);
  if (r.checks && r.checks.baseline && r.checks.baseline.error === false && r.checks.baseline.ok === false) process.exit(2);
}
function cmdReindex() {
  const roots = memoryRoots();
  if (!roots.length) { console.log('记忆库不存在。'); return; }
  for (const root of roots) {
    const n = buildIndex(root).length;
    console.log('已重建索引 ' + root + '（' + n + ' 条）');
    // v0.23.0 修复（WorkBuddy D2）：无授权 key 的加密私密区无法重建——明确提示，
    // 避免「已重建索引」误导（doctor 建议 → reindex 死路），并给出可执行路径。
    try {
      const report = indexConsistencyReport(root);
      if (report.ownersSkipped && report.ownersSkipped.length) {
        console.log('[提示] 跳过无授权私密 owner: ' + report.ownersSkipped.join(', ')
          + '（' + report.skippedFiles + ' 个文件未重建）。加密库重建私密索引请带 --agent <id> --agent-key-file <path> 重跑。');
      }
    } catch (e) { /* 提示失败不影响重建结果 */ }
  }
}
function collectAll(root) {
  const out = [];
  const skipped = {};
  for (const fp of collectEntryFiles(root)) {
    const owner = ownerFromPrivatePath(root, fp);
    if (isEncFile(fp) && !getOwnerKeyFor(root, owner)) { skipped[owner] = true; continue; }
    try {
      const e = readEntry(fp, root);
      out.push({ file: e.file, meta: e.meta });
    } catch (err) { if (owner) skipped[owner] = true; }
  }
  return { memories: out, skipped: Object.keys(skipped) };
}
function exportCore(root, outPath) {
  const res = collectAll(root);
  const data = { format: 'yottamemory', version: 2, exported: today(), memories: res.memories, skippedOwners: res.skipped };
  const target = outPath || path.join(root, 'yottamemory-export-' + today() + '.json');
  fs.writeFileSync(target, JSON.stringify(data, null, 2), 'utf8');
  return { error: false, text: '已导出 ' + data.memories.length + ' 条记忆 -> ' + target + (res.skipped.length ? '（跳过无授权私密 owner: ' + res.skipped.join(', ') + '）' : '') };
}
function importCore(root, src) {
  if (!src) return { error: true, text: '请提供 JSON 文件路径' };
  let fp = String(src);
  if (!fs.existsSync(fp)) {
    const alt = path.resolve(root, fp);
    if (fs.existsSync(alt)) fp = alt;
  }
  if (!fs.existsSync(fp)) return { error: true, text: 'JSON 文件不存在: ' + src };
  let data;
  try { data = JSON.parse(fs.readFileSync(fp, 'utf8')); }
  catch (e) { return { error: true, text: 'JSON 解析失败: ' + (e && e.message ? e.message : String(e)) }; }
  if (!data.memories || !Array.isArray(data.memories)) return { error: true, text: 'JSON 格式不正确（缺少 memories 数组）' };
  for (const item of data.memories) {
    const meta = item.meta || {};
    const t = (meta.type || 'FACT').toUpperCase();
    if (!TYPE_DIRS[t]) continue;
    const owner = String(meta.owner || '');
    const scope = meta.scope || defaultScope(t);
    if (scope === 'private' && !isSafeAgentId(owner)) {
      return { error: true, text: '拒绝: 导入的私密条目 owner 非法（只允许单段名称，禁止 /、\\、.. 和控制字符）。' };
    }
  }
  ensureInit(root);
  const encrypted = isEncrypted(root);
  let m = 0, skippedPriv = 0;
  for (const item of data.memories) {
    const meta = item.meta || {};
    const t = (meta.type || 'FACT').toUpperCase();
    if (!TYPE_DIRS[t]) continue;
    const owner = meta.owner || '';
    const scope = meta.scope || defaultScope(t);
    if (encrypted && scope === 'private' && !getOwnerKeyFor(root, owner)) { skippedPriv++; continue; }
    // 导入沿用条目的 created 日期决定分层目录，避免历史记忆被塞进当前月。
    const importDate = /^\d{4}-\d{2}-\d{2}$/.test(String(meta.created || '')) ? String(meta.created) : today();
    const dir = entryWriteDir(root, t, owner, importDate);
    fs.mkdirSync(dir, { recursive: true });
    let seq = nextSeqFor(path.join(root, typeSubdir(t, owner)), dir);
    const suffix = (encrypted && scope === 'private') ? ENC_SUFFIX : '';
    let file = path.join(dir, importDate + '-' + seq + '.md' + suffix);
    while (fs.existsSync(file)) { seq = String(parseInt(seq, 10) + 1).padStart(4, '0'); file = path.join(dir, importDate + '-' + seq + '.md' + suffix); }
    const rec = {
      type: t,
      subject: meta.subject || '',
      statement: meta.statement || '',
      confidence: parseFloat(meta.confidence || 1.0),
      created: importDate,
      updated: meta.updated || today(),
      tags: parseTags(meta.tags),
      immutable: meta.immutable === true || meta.immutable === 'true',
      source: meta.source || '',
      weight: (parseFloat(meta.weight) > 0 ? parseFloat(meta.weight) : 1.0),
      scope: scope,
      owner: owner,
      access_count: parseInt(meta.access_count || '0', 10) || 0,
      last_accessed: meta.last_accessed || '',
    };
    writeMemoryText(root, file, frontmatterToText(rec, rec.statement), owner);
    upsertIndexEntry(root, readEntry(file, root));
    m++;
  }
  return { error: false, text: '已导入 ' + m + ' 条记忆 -> ' + root + (skippedPriv ? '（跳过 ' + skippedPriv + ' 条无授权私密）' : '') };
}
function cmdExport(outPath) {
  const r = exportCore(userRoot(), outPath || 'yottamemory-export-' + today() + '.json');
  console.log(r.text);
}
function cmdImport(src) {
  const r = importCore(userRoot(), src);
  console.log(r.text);
  if (r.error) process.exit(2);
}

// ---- token 管理（每智能体一个，登记 <记忆库>/.server/tokens.json）----
function serverDir(root) { return path.join(root, SERVER_SUBDIR); }
function tokensPath(root) { return path.join(serverDir(root), TOKENS_FILE); }
function loadTokens(root) {
  try { return JSON.parse(fs.readFileSync(tokensPath(root), 'utf8')) || {}; } catch (e) { return {}; }
}
function saveTokens(root, data) {
  fs.mkdirSync(serverDir(root), { recursive: true });
  fs.writeFileSync(tokensPath(root), JSON.stringify(data, null, 2), 'utf8');
  try { fs.chmodSync(tokensPath(root), 0o600); } catch (e) {}
}
function cmdTokenNew(agentId, opts) {
  const root = userRoot();
  ensureInit(root);
  if (!agentId) { console.error('请指定 --agent <id>'); process.exit(2); }
  if (!isSafeAgentId(agentId)) { console.error('非法 agent ID：只允许单段名称，禁止 /、\\、.. 和控制字符。'); process.exit(2); }
  const data = loadTokens(root);
  data.version = 1;
  data.tokens = data.tokens || {};
  const conflict = identityConflict(root, agentId);
  if (conflict && !opts.force) {
    console.error("错误: 智能体 ID '" + agentId + "' " + conflict + '。每个 AI 智能体的 ID 必须唯一；确认是同一智能体后加 --force 覆盖。');
    process.exit(2);
  }
  const token = 'ytm_' + crypto.randomBytes(16).toString('hex');
  data.tokens[agentId] = { token: token, created: today() };
  saveTokens(root, data);
  console.log(token);
}
function cmdTokenList() {
  const root = userRoot();
  const data = loadTokens(root);
  const map = data.tokens || {};
  const ids = Object.keys(map);
  if (!ids.length) { console.log('暂无已登记 token（yotta-memory token new --agent <id> 生成）'); return; }
  console.log('已登记智能体:');
  for (const id of ids) console.log('  ' + id + '  (创建于 ' + map[id].created + ')');
}
function cmdTokenRevoke(agentId) {
  const root = userRoot();
  if (!agentId) { console.error('请指定 --agent <id>'); process.exit(2); }
  if (!isSafeAgentId(agentId)) { console.error('非法 agent ID：只允许单段名称，禁止 /、\\、.. 和控制字符。'); process.exit(2); }
  const data = loadTokens(root);
  data.tokens = data.tokens || {};
  if (data.tokens[agentId]) { delete data.tokens[agentId]; saveTokens(root, data); console.log('已吊销: ' + agentId); }
  else { console.log('未找到已登记智能体: ' + agentId); }
}


// ---- 智能体身份登记（agents.json）+ 自我档案 ----
function agentsPath(root) { return path.join(root, AGENTS_FILE); }
function loadAgents(root) {
  try { return JSON.parse(fs.readFileSync(agentsPath(root), 'utf8')) || {}; } catch (e) { return {}; }
}
function saveAgents(root, data) {
  fs.mkdirSync(root, { recursive: true });
  fs.writeFileSync(agentsPath(root), JSON.stringify(data, null, 2), 'utf8');
}
const SELF_PROFILE_SUBJECT = '自我接入档案';
function selfPrefsDir(root, agentId) { return path.join(root, PRIVATE_DIR, agentId, 'prefs'); }
function findSelfProfile(root, agentId) {
  const dir = selfPrefsDir(root, agentId);
  if (!fs.existsSync(dir)) return '';
  for (const f of fs.readdirSync(dir)) {
    if (!/\.md(\.enc)?$/.test(f)) continue;
    const fp = path.join(dir, f);
    if (!fs.statSync(fp).isFile()) continue;
    let text;
    try { text = readMemoryText(root, fp, agentId); } catch (err) { continue; }
    const meta = parseFrontmatter(text).meta;
    if (meta.subject === SELF_PROFILE_SUBJECT && (meta.owner || '') === agentId) return f;
  }
  return '';
}
function parseKvBody(body) {
  const out = {};
  for (const seg of String(body || '').split(';')) {
    const m = /^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*([\s\S]*)$/.exec(seg);
    if (m && m[2] !== undefined) out[m[1]] = m[2].trim();
  }
  return out;
}
function selfProfileBody(agentId, root, extra) {
  const lines = [];
  lines.push('agent_id: ' + agentId);
  lines.push('host: ' + os.hostname());
  lines.push('memory_home: ' + root);
  lines.push('mcp_mode: ' + (extra.mcpMode || 'stdio'));
  if (extra.engineUrl) lines.push('engine_url: ' + extra.engineUrl);
  if (extra.token) lines.push('token: ' + extra.token);
  if (extra.name) lines.push('agent_name: ' + extra.name);
  if (extra.userName) lines.push('user_name: ' + extra.userName);
  if (extra.relationship) lines.push('relationship: ' + extra.relationship);
  return lines.join('; ');
}
function writeSelfProfile(root, agentId, extra) {
  extra = extra || {};
  const dir = selfPrefsDir(root, agentId);
  fs.mkdirSync(dir, { recursive: true });
  const encrypted = isEncrypted(root);
  const existing = findSelfProfile(root, agentId);
  if (existing) {
    const fp = path.join(dir, existing);
    const parsed = parseFrontmatter(readMemoryText(root, fp, agentId));
    const kv = parseKvBody(parsed.body);
    kv.agent_id = agentId;
    kv.host = os.hostname();
    kv.memory_home = root;
    kv.mcp_mode = extra.mcpMode || kv.mcp_mode || 'stdio';
    if (extra.engineUrl) kv.engine_url = extra.engineUrl;
    if (extra.token) kv.token = extra.token;
    if (extra.name) kv.agent_name = extra.name;
    if (extra.userName) kv.user_name = extra.userName;
    if (extra.relationship) kv.relationship = extra.relationship;
    const body = Object.keys(kv).map(function (k) { return k + ': ' + kv[k]; }).join('; ');
    const meta = Object.assign({}, parsed.meta);
    meta.updated = today();
    meta.statement = body;
    writeMemoryText(root, fp, frontmatterToText(meta, body), agentId);
    upsertIndexEntry(root, readEntry(fp, root));
    return fp;
  }
  const seq = nextSeq(dir);
  const file = path.join(dir, today() + '-' + seq + '.md' + (encrypted ? ENC_SUFFIX : ''));
  const body = selfProfileBody(agentId, root, extra);
  const rec = {
    type: 'PREF', subject: SELF_PROFILE_SUBJECT, statement: body,
    confidence: 1.0, created: today(), updated: today(),
    tags: ['自我档案'], immutable: false,
    scope: 'private', owner: agentId, access_count: 0, last_accessed: '',
  };
  writeMemoryText(root, file, frontmatterToText(rec, body), agentId);
  upsertIndexEntry(root, readEntry(file, root));
  return file;
}
function identityConflict(root, agentId) {
  const agents = loadAgents(root).agents || {};
  const tokens = loadTokens(root).tokens || {};
  const host = os.hostname();
  const a = agents[agentId];
  if (a && a.host && a.host !== host) return '已被智能体身份登记占用（host=' + a.host + '）';
  if (tokens[agentId]) return '已被远端 token 登记占用（.server/tokens.json）';
  return '';
}
function cmdIam(agentId, opts) {
  const root = userRoot();
  ensureInit(root);
  if (!agentId) { console.error('请指定 <id>：yotta-memory iam <id> [--name <显示名>] [--user <用户名>] [--relationship <关系>] [--force]'); process.exit(2); }
  if (!isSafeAgentId(agentId)) { console.error('非法 agent ID：只允许单段名称，禁止 /、\\、.. 和控制字符。'); process.exit(2); }
  const conflict = identityConflict(root, agentId);
  if (conflict && !opts.force) {
    console.error("错误: ID '" + agentId + "' " + conflict + '。每个 AI 智能体的 ID 必须唯一。请换一个唯一 ID，或确认是同一智能体后加 --force 覆盖。');
    process.exit(2);
  }
  const data = loadAgents(root);
  data.version = 1;
  data.agents = data.agents || {};
  const host = os.hostname();
  const existed = data.agents[agentId];
  data.agents[agentId] = { host: host, created: (existed && existed.created) || today() };
  saveAgents(root, data);
  const profileIdentity = resolveIdentity({ agent: agentId, agentKey: opts.agentKey, agentKeyFile: opts.agentKeyFile });
  if (profileIdentity && !profileIdentity.error && profileIdentity.id) {
    setRuntimeAgent(profileIdentity.id, profileIdentity.agentKey);
  }
  let profile = '';
  let profileWarning = '';
  try {
    profile = writeSelfProfile(root, agentId, { mcpMode: 'stdio', name: opts.name, userName: opts.user, relationship: opts.relationship });
  } catch (e) {
    const message = e && e.message ? e.message : String(e);
    if (isEncrypted(root) && /授权密钥|加密/.test(message)) {
      profileWarning = '自我档案暂未写入：当前加密库还没有 ' + agentId + ' 的授权密钥。请先完成授权（yotta-memory view 或 yotta-memory key bind ' + agentId + '），再在已授权的会话中执行 yotta-memory iam ' + agentId + ' --force --agent-key-file <宿主key文件> 写入档案。';
    } else {
      throw e;
    }
  }
  console.log('已登记智能体身份: ' + agentId + '（host=' + host + '，' + (conflict ? '--force 覆盖' : '新建') + '）');
  if (opts.name || opts.user || opts.relationship) {
    console.log('自我档案扩展: ' + [opts.name && '显示名=' + opts.name, opts.user && '用户=' + opts.user, opts.relationship && '关系=' + opts.relationship].filter(Boolean).join(' / '));
  }
  if (profile) console.log('已写入自我档案: ' + profile);
  if (profileWarning) console.log(profileWarning);
  console.log('本机免 token：以后用 whoami 确认身份；远端接入需 token new --agent ' + agentId);
}
function cmdWhoami(opts) {
  const root = userRoot();
  const ident = resolveIdentity(opts);
  if (ident.error) {
    if (opts.json) console.log(JSON.stringify({ identity: identityDiagnostic(ident), error: ident.error }, null, 2));
    else console.log(ident.error);
    process.exit(2);
  }
  const id = ident.id;
  if (!id) {
    if (opts.json) {
      console.log(JSON.stringify({ identity: identityDiagnostic(ident), registration: 'none', profile: '' }, null, 2));
      return;
    }
    console.log('当前未声明显式智能体身份（身份不再从环境变量读取）。');
    console.log('CLI：请传 --agent <唯一ID>。stdio MCP：使用 --agent-id <唯一ID> + --agent-key-file <path>。HTTP MCP：发送 X-Agent-Id + X-Agent-Key。');
    console.log('远端：token + X-Agent-Id + X-Agent-Key（token new --agent <id>；agent_key 由 view 授权生成）。');
    return;
  }
  const agents = loadAgents(root).agents || {};
  const tokens = loadTokens(root).tokens || {};
  let reg = '未登记';
  if (agents[id]) reg = 'agents.json 已登记（host=' + agents[id].host + '）';
  else if (tokens[id]) reg = 'tokens.json 已登记（远端）';
  const profile = findSelfProfile(root, id);
  const kv = profile ? selfProfileKv(root, id) : {};
  if (opts.json) {
    console.log(JSON.stringify({
      identity: identityDiagnostic(ident),
      registration: reg,
      profile: profile || '',
      agentName: kv.agent_name || '',
      userName: kv.user_name || '',
      relationship: kv.relationship || '',
    }, null, 2));
    return;
  }
  console.log('当前智能体身份: ' + id);
  console.log('登记状态: ' + reg);
  console.log('自我档案: ' + (profile ? profile : '未写入（请执行 yotta-memory iam ' + id + '）'));
  if (profile) {
    if (kv.agent_name) console.log('显示名: ' + kv.agent_name);
    if (kv.user_name) console.log('用户: ' + kv.user_name);
    if (kv.relationship) console.log('关系: ' + kv.relationship);
  }
  if (!agents[id] && !tokens[id]) console.log('提示: 请先 yotta-memory iam ' + id + ' 登记唯一身份并落自我档案，再写私密记忆。');
}

// ---- 用户画像聚合（v0.6.0，零推断：只归组呈现原文，结论由承载 AI 依据「记忆守则」内部形成）----
function profileGroups(root, owner) {
  const entries = [];
  for (const t of PRIVATE_LEAF) {
    const dir = path.join(root, PRIVATE_DIR, owner, t);
    if (!fs.existsSync(dir)) continue;
    const files = [];
    walkEntryFiles(dir, files);
    for (const fp of files) {
      let e;
      try { e = readEntry(fp, root); } catch (err) { continue; }
      entries.push(e);
    }
  }
  return profileGroupsFromEntries(entries);
}
function profileGroupsFromEntries(entries) {
  const groups = [];
  const map = {};
  for (const e of (entries || [])) {
    const key = e.type + '\u0000' + (e.subject || '') + '\u0000' + (e.tags || []).join(',');
    if (!map[key]) {
      map[key] = { type: e.type, subject: e.subject || '', tags: e.tags || [], items: [] };
      groups.push(map[key]);
    }
    map[key].items.push({
      file: e.file, statement: e.statement, confidence: e.confidence,
      last_accessed: e.last_accessed, updated: e.updated,
    });
  }
  return groups;
}
function renderProfileText(owner, groups) {
  const lines = [];
  lines.push('# 用户画像（' + owner + '）');
  lines.push('');
  lines.push('> 生成: yotta-memory profile | 引擎零推断：以下为私密记忆原文的结构化归组，画像结论由承载 AI 依据「记忆守则」在内部形成，不当面贴标签。');
  lines.push('> 刷新: ' + today());
  lines.push('');
  for (const g of (groups || [])) {
    lines.push('## ' + g.type + ' · ' + (g.subject || '（无主题）') + (g.tags.length ? '  [tags: ' + g.tags.join(', ') + ']' : ''));
    lines.push('');
    for (const it of g.items) {
      const acc = it.last_accessed ? '最近访问 ' + it.last_accessed : '未访问';
      lines.push('- ' + it.statement + '（confidence ' + it.confidence + ' · ' + acc + '）');
      lines.push('  - ' + it.file);
    }
    lines.push('');
  }
  return lines.join('\n');
}
function profileCore(opts) {
  opts = opts || {};
  const root = userRoot();
  const ident = resolveIdentity(opts);
  if (ident.error) return { error: true, exitCode: 3, text: ident.error };
  if (!ident.id) {
    return {
      error: true,
      exitCode: 3,
      text: '生成私密画像必须先声明身份：CLI 传 --agent <id>；stdio MCP 传 --agent-id <id> + --agent-key-file <path>；HTTP MCP 发送 X-Agent-Id + X-Agent-Key。',
    };
  }
  const selfAgent = ident.id;
  const owner = opts.owner || selfAgent;
  const keyError = validatePrivateIdentity(root, ident, owner);
  if (keyError) return { error: true, exitCode: 3, text: keyError };
  if (!owner) return { error: true, exitCode: 2, text: '请先声明身份（--agent / --agent-id）或传 --owner <id>，再生成画像。' };
  if (selfAgent && owner !== selfAgent && owner !== 'user' && !opts.unsafe && !hasGrant(selfAgent, owner)) {
    return { error: true, exitCode: 3, text: '拒绝: 不能生成其它智能体 ' + owner + ' 的画像（private/' + owner + '/ 为私密区）。如需读取请 --owner user 或 --unsafe（用户显式授权）。' };
  }
  const ownerDir = path.join(root, PRIVATE_DIR, owner);
  if (!fs.existsSync(ownerDir)) return { error: false, text: '该智能体（' + owner + '）暂无画像：private/' + owner + '/ 不存在或为空。' };
  if (isEncrypted(root) && !getOwnerKeyFor(root, owner)) {
    return { error: true, exitCode: 3, text: '私密区已加密：当前无 ' + owner + ' 的授权密钥，请在用户平台授权（yotta-memory view → 授权本智能体）后生成画像。' };
  }
  const groups = profileGroups(root, owner);
  if (!groups.length) return { error: false, text: '该智能体（' + owner + '）暂无画像：private/' + owner + '/ 下无 PREF / BOUND / COMMIT 条目。' };
  const text = renderProfileText(owner, groups);
  const outFile = writeProfileText(root, owner, text + '\n');
  return { error: false, text: text + '\n\n[已写入] ' + outFile };
}
function cmdProfile(opts) {
  const r = profileCore(opts);
  console.log(r.text);
  if (r.exitCode) process.exit(r.exitCode);
  if (r.error) process.exit(2);
}

// ---- 开工上下文包（v0.6.0：身份 + 画像 + 近期记忆 + 边界 + 承诺，stdout 不落盘）----
function selfProfileKv(root, id) {
  const profile = findSelfProfile(root, id);
  if (!profile) return {};
  let text;
  try { text = readMemoryText(root, path.join(selfPrefsDir(root, id), profile), id); } catch (e) { return {}; }
  return parseKvBody(parseFrontmatter(text).body);
}
// v0.14.0：长期摘要优先 / 近期走廊 / 会话闭环上下文编排。
// 摘要只认 consolidate 产物，不新增第二套摘要格式。
function isConsolidatedSummary(entry) {
  if (!entry) return false;
  if (entry.source === 'consolidate') return true;
  const tags = Array.isArray(entry.tags) ? entry.tags : [];
  return tags.indexOf('consolidate') !== -1 && tags.indexOf('summary') !== -1;
}
function contextRecentKey(entry) {
  return String((entry && (entry.updated || entry.created)) || '');
}
function compareContextRecent(a, b) {
  const byTime = contextRecentKey(b).localeCompare(contextRecentKey(a));
  if (byTime !== 0) return byTime;
  return (b.access_count || 0) - (a.access_count || 0);
}
// v0.23.0 D1：COMMIT 段保留策略 —— 最近 N 条 + weight≥1.5 / pinned / evergreen 恒显；0 = 全部。
function contextCommitsLimit(cfg) {
  const raw = cfg ? cfg.context_commits_limit : undefined;
  if (raw === undefined || raw === null || raw === '') return CONTEXT_COMMITS_LIMIT_DEFAULT;
  const n = parseInt(raw, 10);
  return (n >= 0) ? n : CONTEXT_COMMITS_LIMIT_DEFAULT;
}
function commitAlwaysShown(entry) {
  if (!entry) return false;
  const w = parseFloat(entry.weight || '1.0');
  if (w >= 1.5) return true;
  return isEvergreenTagged(entry);
}
// v0.23.0 修复（WorkBuddy D1）：COMMIT 段按「立下时间」（created）倒序取最近 N 条；
// 同日条目再按文件名序号倒序（写入先后）。旧实现按 updated（只到「日」）排序，
// 同日全平局后退化为索引插入序（最旧在前）——刚写入的承诺被折叠、最老的反而进上下文。
function commitRecencyKey(entry) {
  return String((entry && (entry.created || entry.updated)) || '');
}
function compareCommitRecency(a, b) {
  const byCreated = commitRecencyKey(b).localeCompare(commitRecencyKey(a));
  if (byCreated !== 0) return byCreated;
  const byFile = String((b && b.file) || '').localeCompare(String((a && a.file) || ''));
  if (byFile !== 0) return byFile;
  return (b.access_count || 0) - (a.access_count || 0);
}

const MEMORY_HOOK_MAX_CANDIDATES = 500;
const MEMORY_HOOK_STATEMENT_LIMIT = 2000;

function contextEntryLine(entry) {
  return '- [' + entry.type + '] ' + entry.subject + ': ' + entry.statement;
}

function isSelfProfileEntry(entry, owner) {
  if (!entry || entry.type !== 'PREF' || entry.subject !== SELF_PROFILE_SUBJECT) return false;
  if (owner && entry.owner && entry.owner !== owner) return false;
  const file = String(entry.file || '').replace(/\\/g, '/');
  return owner ? file.indexOf('private/' + owner + '/prefs/') === 0 : false;
}

function contextPageableEntries(readableEntries, owner) {
  return (readableEntries || [])
    .filter(function (entry) {
      return entry.type !== 'BOUND' && entry.type !== 'COMMIT' && !isSelfProfileEntry(entry, owner);
    })
    .sort(compareContextRecent);
}

function hookBlock(status, providerId, note) {
  return {
    status: status || 'not_installed',
    provider_id: providerId || '',
    applied: false,
    evicted: [],
    dropped: [],
    note: note || '',
  };
}

function hookStatusText(hook) {
  if (!hook) return '';
  if (hook.status === 'active') {
    const who = hook.provider_id ? '提供方 ' + hook.provider_id : '提供方';
    return '已应用（' + who + '；驱逐 ' + hook.evicted.length + ' / 丢弃 ' + hook.dropped.length + '）';
  }
  if (hook.status === 'license_required') return '需授权（该能力需要授权后使用；普通记忆不受影响）';
  if (hook.status === 'timeout') return '未生效（提供方超时，已回落普通记忆）';
  if (hook.status === 'invalid_output') return '未生效（提供方输出无效，已回落普通记忆）';
  if (hook.status === 'error') return '未生效（提供方异常，已回落普通记忆）';
  return hook.status;
}

function pagingBlock(status, providerId, note) {
  return {
    status: status || 'not_installed',
    provider_id: providerId || '',
    applied: false,
    dropped: [],
    ordered: [],
    truncated: false,
    budget: 0,
    used: 0,
    note: note || '',
  };
}

function pagingStatusText(paging) {
  if (!paging) return '';
  if (paging.status === 'active') {
    const who = paging.provider_id ? '提供方 ' + paging.provider_id : '提供方';
    return '已应用（' + who + '；丢弃 ' + paging.dropped.length + ' / 排序 ' + paging.ordered.length + '）';
  }
  if (paging.status === 'license_required') return '需授权（该能力需要授权后使用；普通记忆不受影响）';
  if (paging.status === 'timeout') return '未生效（提供方超时，已回落普通记忆）';
  if (paging.status === 'invalid_output') return '未生效（提供方输出无效，已回落普通记忆）';
  if (paging.status === 'error') return '未生效（提供方异常，已回落普通记忆）';
  return '';
}

function pagingCandidatePayload(entry, baselineSection) {
  return {
    file: entry.file,
    type: entry.type,
    subject: entry.subject,
    statement: String(entry.statement || '').slice(0, MEMORY_HOOK_STATEMENT_LIMIT),
    created: entry.created || '',
    updated: entry.updated || '',
    chars: contextEntryLine(entry).length,
    baseline_section: baselineSection || 'high_value',
  };
}

function applyContextPaging(pageable, opts, meta) {
  opts = opts || {};
  meta = meta || {};
  const budget = parseInt(opts.budget || 0, 10) || 0;
  if (budget <= 0) {
    return {
      block: pagingBlock('not_requested', '', '未传 --budget，未调用 context.paging'),
      drop: new Set(),
      order: null,
      applied: false,
    };
  }
  const block = pagingBlock('not_installed', '', '');
  block.budget = budget;
  const truncated = pageable.length > MEMORY_HOOK_MAX_CANDIDATES;
  block.truncated = truncated;
  const candidates = pageable.slice(0, MEMORY_HOOK_MAX_CANDIDATES);
  const payload = {
    agent: opts.owner || '',
    budget: budget,
    focus: opts.focus || '',
    truncated: truncated,
    protected: Array.isArray(meta.protected) ? meta.protected.slice() : [],
    sections: meta.sections || {},
    candidates: candidates.map(function (entry) {
      return pagingCandidatePayload(entry, (meta.baselineSections || {})[entry.file]);
    }),
  };
  let run;
  try {
    run = require('./provider').runCapability('context.paging', payload);
  } catch (e) {
    block.status = 'error';
    block.note = '预算分页失败：' + e.message;
    return { block: block, drop: new Set(), order: null, applied: false };
  }
  block.status = run.status;
  block.provider_id = run.provider_id || '';
  block.note = run.note || run.message || '';
  if (run.status !== 'active' || !run.data || typeof run.data !== 'object') {
    return { block: block, drop: new Set(), order: null, applied: false };
  }
  const sent = new Set(payload.candidates.map(function (item) { return item.file; }));
  const rejected = [];
  const dropped = [];
  for (const item of (Array.isArray(run.data.drop) ? run.data.drop : [])) {
    const file = String(item || '');
    if (!file) continue;
    if (!sent.has(file)) {
      if (rejected.indexOf(file) === -1) rejected.push(file);
      continue;
    }
    if (dropped.indexOf(file) === -1) dropped.push(file);
  }
  let order = null;
  if (Array.isArray(run.data.order)) {
    if (run.data.complete === true && !truncated) {
      const picked = [];
      for (const item of run.data.order) {
        const file = String(item || '');
        if (!file) continue;
        if (!sent.has(file)) {
          if (rejected.indexOf(file) === -1) rejected.push(file);
          continue;
        }
        if (picked.indexOf(file) === -1) picked.push(file);
      }
      order = picked;
    } else if (truncated) {
      block.note = block.note || '候选超过 ' + MEMORY_HOOK_MAX_CANDIDATES + '，order 未应用（保护）';
    } else {
      block.note = block.note || 'provider 未声明 complete=true，order 未应用（保护）';
    }
  }
  if (rejected.length) {
    const text = '候选集外文件已忽略：' + rejected.join(', ');
    block.note = block.note ? block.note + '；' + text : text;
  }
  block.dropped = dropped;
  block.ordered = order || [];
  block.applied = dropped.length > 0 || (order !== null && order.length > 0);
  return { block: block, drop: new Set(dropped), order: order, applied: block.applied };
}

/**
 * memory.hook 装载点：只把「可驱逐」条目（非 BOUND / COMMIT）交给 provider。
 * provider 只能返回本次候选集内的 evict（驱逐清单）；complete=true 时可选 selected（白名单）。
 * 身份画像、BOUND / COMMIT、预算 / 去重 / 宽限始终由引擎掌控；任何失败都走普通记忆。
 * 协议见 references/provider-protocol.md。
 */
function applyMemoryHook(readableEntries, opts) {
  const block = hookBlock('not_installed', '', '');
  const pageable = contextPageableEntries(readableEntries, opts.owner || '');
  const truncated = pageable.length > MEMORY_HOOK_MAX_CANDIDATES;
  const payload = {
    agent: opts.owner || '',
    budget: opts.budget || 0,
    focus: opts.focus || '',
    truncated: truncated,
    candidates: pageable.slice(0, MEMORY_HOOK_MAX_CANDIDATES).map(function (entry) {
      return {
        file: entry.file,
        type: entry.type,
        subject: entry.subject,
        statement: String(entry.statement || '').slice(0, MEMORY_HOOK_STATEMENT_LIMIT),
        created: entry.created || '',
        updated: entry.updated || '',
      };
    }),
  };
  let run;
  try {
    run = require('./provider').runCapability('memory.hook', payload);
  } catch (e) {
    block.status = 'error';
    block.note = '扩展装载失败：' + e.message;
    return { block: block, evict: new Set(), selected: null };
  }
  block.status = run.status;
  block.provider_id = run.provider_id || '';
  block.note = run.note || run.message || '';
  if (run.status !== 'active' || !run.data || typeof run.data !== 'object') {
    return { block: block, evict: new Set(), selected: null };
  }
  const sent = new Set(payload.candidates.map(function (item) { return item.file; }));
  const evicted = [];
  for (const item of (Array.isArray(run.data.evict) ? run.data.evict : [])) {
    const file = String(item || '');
    if (!file) continue;
    if (!sent.has(file)) {
      block.dropped.push(file);
      continue;
    }
    if (evicted.indexOf(file) === -1) evicted.push(file);
  }
  let selected = null;
  if (Array.isArray(run.data.selected) && run.data.complete === true && !truncated) {
    const picked = [];
    for (const item of run.data.selected) {
      const file = String(item || '');
      if (!file) continue;
      if (!sent.has(file)) {
        block.dropped.push(file);
        continue;
      }
      if (picked.indexOf(file) === -1) picked.push(file);
    }
    selected = new Set(picked);
  }
  block.evicted = evicted;
  block.applied = evicted.length > 0 || selected !== null;
  if (truncated && Array.isArray(run.data.selected)) {
    block.note = block.note || '候选超过 ' + MEMORY_HOOK_MAX_CANDIDATES + '，白名单模式未应用（保护）';
  }
  return { block: block, evict: new Set(evicted), selected: selected };
}

function replaceContextProfileSection(lines, profileText, fence) {
  const start = lines.indexOf('## 2. 用户画像摘要');
  if (start === -1) return false;
  const marker = lines.indexOf('## 2.5 长期理解摘要');
  const end = marker === -1 ? lines.length : marker;
  if (end < start) return false;
  const block = ['## 2. 用户画像摘要', ''];
  if (profileText) {
    block.push(fence + 'markdown');
    block.push(String(profileText).trim());
    block.push(fence);
  } else {
    block.push('（该身份暂无画像；可运行 yotta-memory profile 生成）');
  }
  block.push('');
  lines.splice.apply(lines, [start, end - start].concat(block));
  return true;
}

function contextCore(opts) {
  opts = opts || {};
  const roots = memoryRoots();
  if (!roots.length) return { error: false, exitCode: 0, text: '记忆库不存在，请先运行: yotta-memory init' };
  if (opts.audit) return contextAuditCore(opts);
  const root = userRoot();
  const limit = parseInt(opts.limit || '10', 10) || 10;
  const ident = resolveIdentity(opts);
  if (ident.error) return { error: true, exitCode: 3, text: ident.error };
  if (!ident.id) {
    return {
      error: true,
      exitCode: 3,
      text: '开工上下文包含私密画像 / 边界 / 承诺，必须先声明身份：CLI 传 --agent <id>；stdio MCP 传 --agent-id <id> + --agent-key-file <path>；HTTP MCP 发送 X-Agent-Id + X-Agent-Key。',
    };
  }
  const selfAgent = ident.id;
  const owner = opts.owner || selfAgent;
  const keyError = validatePrivateIdentity(root, ident, owner);
  if (keyError) return { error: true, exitCode: 3, text: keyError };
  const unsafe = !!opts.unsafe;
  const budget = opts.budget ? parseInt(opts.budget, 10) : 0;
  const focus = opts.focus ? String(opts.focus) : '';
  const yearFilter = normalizeYearList(opts.years);
  if (yearFilter.error) return { error: true, exitCode: 2, text: yearFilter.error };
  const years = yearFilter.years;
  const explain = !!opts.explain;
  const embeddingCommand = effectiveEmbeddingCommand(opts);
  const embeddingTimeout = effectiveEmbeddingTimeout(opts);
  const trace = [];
  const lines = [];
  const shownFiles = new Set();
  const usedFiles = new Set();
  let usedDynamicChars = 0;
  const FENCE = String.fromCharCode(96, 96, 96);
  function usedChars() { return lines.reduce(function (s, x) { return s + String(x).length + 1; }, 0); }
  function appendContextEntry(entry, reason, options) {
    options = options || {};
    if (!entry) return false;
    if (shownFiles.has(entry.file)) {
      trace.push('[dropped] ' + entry.file + ' reason: duplicate');
      return false;
    }
    const line = contextEntryLine(entry);
    if (options.budget !== false && budget > 0 && usedChars() + line.length > budget) {
      trace.push('[dropped] ' + entry.file + ' reason: budget_exceeded');
      return false;
    }
    lines.push(line);
    shownFiles.add(entry.file);
    usedFiles.add(entry.file);
    usedDynamicChars += line.length;
    trace.push('[included] ' + entry.file + ' reason: ' + reason);
    return true;
  }
  lines.push('# 开工上下文包（yotta-memory context）');
  lines.push('');
  lines.push('## 1. 身份');
  lines.push('');
  if (!owner) {
    lines.push('- 未声明智能体身份（无 --agent / --agent-id / X-Agent-Id）。私密记忆与画像不可用；请先 whoami / iam。');
  } else {
    lines.push('- agent_id: ' + owner);
    const kv = selfProfileKv(root, owner);
    if (kv.agent_name) lines.push('- agent_name: ' + kv.agent_name);
    if (kv.user_name) lines.push('- user_name: ' + kv.user_name);
    if (kv.relationship) lines.push('- relationship: ' + kv.relationship);
    lines.push('- host: ' + os.hostname());
    lines.push('- memory_home: ' + root);
  }
  lines.push('');
  lines.push('## 1.5 多智能体接入铁律');
  lines.push('');
  lines.push('- 可读：A. 公共 FACT（facts/）B. 本智能体私密（private/<owner>/）C. 其它智能体私密 = 禁区（grant / identity=user / --unsafe 显式授权除外）。');
  lines.push('- 可写：FACT→公共；PREF / BOUND / COMMIT→仅本智能体私密区；禁止写其它智能体私密区。');
  lines.push('- 违规红线：禁止搜索 / 读取 / 总结其它智能体私密；禁止把用户私密关系 / 心理健康 / 生活隐私写入公共区。');
  lines.push('');
  lines.push('## 2. 用户画像摘要');
  lines.push('');
  if (owner) {
    let pf = profilePathFor(root, owner);
    let pfText = null;
    if (fs.existsSync(pf)) { try { pfText = readProfileText(root, owner); } catch (e) { pfText = null; } }
    if (pfText !== null && pfText !== undefined) {
      lines.push(FENCE + 'markdown');
      lines.push(pfText.trim());
      lines.push(FENCE);
    } else {
      const pr = profileCore({ owner: owner, unsafe: unsafe, selfAgent: selfAgent });
      pf = profilePathFor(root, owner);
      if (!pr.error && pr.text.indexOf('[已写入]') !== -1 && fs.existsSync(pf)) {
        lines.push('（画像不存在，已自动生成一次，见下）');
        lines.push(FENCE + 'markdown');
        let t2 = null; try { t2 = readProfileText(root, owner); } catch (e) {}
        lines.push((t2 === null || t2 === undefined) ? '' : t2.trim());
        lines.push(FENCE);
      } else {
        lines.push('（该身份暂无画像；可运行 yotta-memory profile 生成）');
      }
    }
  } else {
    lines.push('（未声明身份，跳过画像；先 iam 登记后可生成）');
  }
  lines.push('');

  const readableEntries = [];
  for (const r of roots) {
    for (const e of indexEntriesFor(r, { years: years }).entries) {
      if (classifyRead(e, owner, '', unsafe, selfAgent) === 'denied') continue;
      readableEntries.push(e);
    }
  }

  const memHook = applyMemoryHook(readableEntries, { owner: owner, budget: budget, focus: focus, limit: limit });
  const hookState = memHook.block;
  function hookAllows(entry) {
    if (!entry) return false;
    if (memHook.selected && !memHook.selected.has(entry.file)) return false;
    if (memHook.evict.has(entry.file)) return false;
    return true;
  }
  let focusedEntries = [];
  if (focus) {
    const focused = recallCore(focus, {
      limit: limit,
      owner: owner,
      unsafe: unsafe,
      selfAgent: selfAgent,
      years: years,
      embedding: embeddingCommand,
      embeddingTimeout: embeddingTimeout,
      noUsage: true
    });
    focusedEntries = focused.entries || [];
  }
  const pageable = contextPageableEntries(readableEntries, owner).filter(hookAllows);
  const summaryLimit = Math.min(3, Math.max(0, limit));
  const summaryCandidates = pageable.filter(isConsolidatedSummary).slice(0, summaryLimit);
  const summaryFiles = new Set(summaryCandidates.map(function (entry) { return entry.file; }));
  const pageableFiles = new Set(pageable.map(function (entry) { return entry.file; }));
  const focusCandidates = focusedEntries.filter(function (entry) {
    return hookAllows(entry) && pageableFiles.has(entry.file);
  });
  const focusFiles = new Set(focusCandidates.map(function (entry) { return entry.file; }));
  const corridorCandidates = pageable
    .filter(function (entry) {
      return !isConsolidatedSummary(entry) && !summaryFiles.has(entry.file) && !focusFiles.has(entry.file);
    })
    .slice(0, limit);
  const corridorFiles = new Set(corridorCandidates.map(function (entry) { return entry.file; }));
  const highValueCandidates = pageable
    .filter(function (entry) {
      return !isConsolidatedSummary(entry) && !summaryFiles.has(entry.file) && !focusFiles.has(entry.file) && !corridorFiles.has(entry.file);
    })
    .map(function (entry) { return { e: entry, s: 0.5 * importanceScore(entry) + 0.5 * utilityScore(entry) }; })
    .sort(function (a, b) { return b.s - a.s; })
    .slice(0, limit)
    .map(function (item) { return item.e; });
  const baselineSections = {};
  function markBaseline(entries, section) {
    for (const entry of entries) baselineSections[entry.file] = section;
  }
  markBaseline(summaryCandidates, 'summary');
  markBaseline(focusCandidates, 'focus');
  markBaseline(corridorCandidates, 'corridor');
  markBaseline(highValueCandidates, 'high_value');
  const paging = applyContextPaging(pageable, {
    owner: owner,
    budget: budget,
    focus: focus,
    limit: limit,
  }, {
    protected: readableEntries
      .filter(function (entry) { return isSelfProfileEntry(entry, owner); })
      .map(function (entry) { return entry.file; }),
    sections: {
      summary: summaryCandidates.map(function (entry) { return entry.file; }),
      focus: focusCandidates.map(function (entry) { return entry.file; }),
      corridor: corridorCandidates.map(function (entry) { return entry.file; }),
      high_value: highValueCandidates.map(function (entry) { return entry.file; }),
    },
    baselineSections: baselineSections,
  });
  const pagingState = paging.block;
  const pagingOrder = new Map();
  for (let i = 0; i < pagingState.ordered.length; i++) pagingOrder.set(pagingState.ordered[i], i);
  function pagingAllows(entry) {
    return !entry || !paging.drop.has(entry.file);
  }
  function decisionAllows(entry) {
    return hookAllows(entry) && pagingAllows(entry);
  }
  function pagingOrderIndex(entry) {
    if (!entry || !pagingOrder.has(entry.file)) return Number.MAX_SAFE_INTEGER;
    return pagingOrder.get(entry.file);
  }
  function compareWithPaging(a, b, fallback) {
    const byOrder = pagingOrderIndex(a) - pagingOrderIndex(b);
    if (byOrder !== 0) return byOrder;
    return fallback(a, b);
  }
  if ((hookState.applied || pagingState.applied) && owner) {
    const liveGroups = profileGroupsFromEntries(
      readableEntries
        .filter(function (entry) { return entry.type === 'PREF' || entry.type === 'BOUND' || entry.type === 'COMMIT'; })
        .filter(decisionAllows)
    );
    replaceContextProfileSection(lines, renderProfileText(owner, liveGroups), FENCE);
    trace.push('[profile] source: live reason: ' + (hookState.applied ? 'memory.hook' : 'context.paging'));
  }
  const statusLines = [];
  if (hookState.status !== 'not_installed') {
    statusLines.push('- 扩展装载（memory.hook）: ' + hookStatusText(hookState));
    trace.push('[hook] status: ' + hookState.status
      + ' provider: ' + (hookState.provider_id || '-')
      + ' evicted: ' + hookState.evicted.length
      + ' dropped: ' + hookState.dropped.length);
  }
  const pagingText = pagingStatusText(pagingState);
  if (pagingText) {
    statusLines.push('- 预算分页（context.paging）: ' + pagingText);
    trace.push('[paging] status: ' + pagingState.status
      + ' provider: ' + (pagingState.provider_id || '-')
      + ' dropped: ' + pagingState.dropped.length
      + ' ordered: ' + pagingState.ordered.length
      + ' truncated: ' + (pagingState.truncated ? 'true' : 'false'));
  }
  if (statusLines.length) {
    const anchor = lines.indexOf('## 1. 身份');
    statusLines.push('');
    lines.splice.apply(lines, [anchor === -1 ? 2 : anchor, 0].concat(statusLines));
  }

  lines.push('## 2.5 长期理解摘要');
  lines.push('');
  const summaries = readableEntries
    .filter(isConsolidatedSummary)
    .filter(decisionAllows)
    .sort(function (a, b) { return compareWithPaging(a, b, compareContextRecent); });
  if (!summaries.length) lines.push('（暂无周期摘要；可用 yotta-memory consolidate --apply 生成）');
  for (const e of summaries.slice(0, summaryLimit)) {
    appendContextEntry(e, 'summary_priority', { budget: false });
  }
  lines.push('');

  if (focus) {
    lines.push('## 2.6 任务相关记忆（--focus）');
    lines.push('');
    if (!focusedEntries.length) lines.push('（无匹配记忆）');
    const focusedVisible = focusedEntries
      .filter(decisionAllows)
      .sort(function (a, b) { return compareWithPaging(a, b, function () { return 0; }); });
    for (const e of focusedVisible) {
      appendContextEntry(e, 'focus_match score: ' + round3(e.score));
    }
    lines.push('');
  }

  lines.push('## 3. 近期走廊（按时间）');
  lines.push('');
  const corridor = readableEntries
    .filter(function (e) { return !isConsolidatedSummary(e) && e.type !== 'BOUND' && e.type !== 'COMMIT'; })
    .filter(decisionAllows)
    .sort(function (a, b) { return compareWithPaging(a, b, compareContextRecent); })
    .filter(function (e) { return !shownFiles.has(e.file); })
    .slice(0, limit);
  if (!corridor.length) lines.push('（暂无近期记忆）');
  for (const e of corridor) appendContextEntry(e, 'recent_corridor');
  lines.push('');

  lines.push('## 4. 近期高价值记忆（补位）');
  lines.push('');
  const highValue = readableEntries
    .filter(function (e) { return !isConsolidatedSummary(e) && e.type !== 'BOUND' && e.type !== 'COMMIT' && !shownFiles.has(e.file) && decisionAllows(e); })
    .map(function (e) { return { e: e, s: 0.5 * importanceScore(e) + 0.5 * utilityScore(e) }; })
    .sort(function (a, b) { return compareWithPaging(a.e, b.e, function (x, y) { return y.s - x.s; }); })
    .slice(0, limit);
  if (!highValue.length) lines.push('（暂无补位条目）');
  for (const h of highValue) appendContextEntry(h.e, 'high_value_backfill');
  lines.push('');
  lines.push('## 5. 边界提醒（BOUND）');
  lines.push('');
  const bounds = readableEntries.filter(function (e) { return e.type === 'BOUND'; }).sort(compareContextRecent);
  if (!bounds.length) lines.push('（无）');
  for (const e of bounds) lines.push('- ' + (e.subject || '边界') + ': ' + e.statement);
  lines.push('');
  lines.push('## 6. 承诺 / 锚点（COMMIT）');
  lines.push('');
  // v0.23.0 D1：保留策略 —— 默认只展示最近 N 条（context_commits_limit，0=全部）；
  // weight≥1.5 / pinned / evergreen 恒显；其余折叠为一行提示（recall 仍可检索全部）。
  // v0.23.0 修复（WorkBuddy D1）：排序键改 created 倒序 + 同日按文件名序号倒序（见 compareCommitRecency）。
  const ctxCfg = decayConfig();
  const commitsAll = readableEntries.filter(function (e) { return e.type === 'COMMIT'; }).sort(compareCommitRecency);
  const commitLimit = contextCommitsLimit(ctxCfg);
  const commits = [];
  const hiddenCommits = [];
  for (let i = 0; i < commitsAll.length; i++) {
    if (commitLimit > 0 && i >= commitLimit && !commitAlwaysShown(commitsAll[i])) hiddenCommits.push(commitsAll[i]);
    else commits.push(commitsAll[i]);
  }
  if (!commitsAll.length) lines.push('（无）');
  for (const e of commits) lines.push('- ' + (e.subject || '承诺') + ': ' + e.statement);
  if (hiddenCommits.length) {
    const oldest = commitRecencyKey(hiddenCommits[hiddenCommits.length - 1]);
    const newest = commitRecencyKey(hiddenCommits[0]);
    lines.push('- （另有 ' + hiddenCommits.length + ' 条更早的 COMMIT 未展示：' + (oldest || '?') + ' ~ ' + (newest || '?') + '；可用 yotta-memory recall --type COMMIT 检索；重要承诺可加 weight / pinned 标签保持常显）');
  }
  lines.push('');
  lines.push('## 7. 本会话闭环契约');
  lines.push('');
  lines.push('- 开工：本上下文包已加载；身份、长期摘要、边界与承诺以本包为准。');
  lines.push('- 进行中：出现事实 / 偏好 / 边界 / 纠正 / 承诺信号时立即 `remember <type> <subject> <statement> --verify`，不攒到收工。');
  lines.push('- 收工前复盘：检查本轮是否留下 COMMIT / 会话小结；有关键结论但未落盘时补写并 `recall` 回读，无长期价值不硬凑。');
  lines.push('');
  const allEntries = readableEntries;
  const myCommits = allEntries.filter(function (e) { return e.type === 'COMMIT' && classifyRead(e, owner, '', unsafe, selfAgent) !== 'denied'; });
  if (!myCommits.length) {
    lines.push('- 最近承诺: 无（收工请补 COMMIT / 交接锚点）');
  } else {
    const latest = myCommits.map(function (e) { return e.updated || e.created || ''; }).sort().pop();
    const d = daysBetween(latest, today());
    lines.push('- 最近承诺: ' + latest + (d > 7 ? '（超期 ' + d + ' 天，请补 COMMIT）' : ''));
  }
  // v0.23.0 D2：归档提醒可执行化（按 config 门槛算达线条数；只读，不触发写入）
  const archiveAge = parseInt(ctxCfg.maintain_archived_age || '180', 10) || 180;
  const archiveUtilityRaw = parseFloat(ctxCfg.maintain_archived_utility || String(ARCHIVE_UTILITY_DEFAULT));
  const archiveUtility = isNaN(archiveUtilityRaw) ? ARCHIVE_UTILITY_DEFAULT : archiveUtilityRaw;
  const agedCount = allEntries.filter(function (e) { return e.created && daysBetween(e.created, today()) > archiveAge && classifyRead(e, owner, '', unsafe, selfAgent) !== 'denied'; }).length;
  const archivableCount = allEntries.filter(function (e) {
    if (!e.created || classifyRead(e, owner, '', unsafe, selfAgent) === 'denied') return false;
    if (daysBetween(e.created, today()) <= archiveAge) return false;
    if (e.immutable || e.type === 'BOUND' || isEvergreenTagged(e)) return false;
    return utilityScore(e) < archiveUtility;
  }).length;
  if (agedCount > 0) {
    lines.push('- 归档提醒: ' + agedCount + ' 条超 ' + archiveAge + ' 天' + (archivableCount > 0
      ? '，其中 ' + archivableCount + ' 条已达归档门槛（运行 yotta-memory maintain 预览 / --apply 执行）'
      : '，暂无达门槛条目（可用 yotta-memory maintain 预览）'));
  }
  if (explain) {
    lines.push('');
    lines.push('## 8. 选择解释（--explain）');
    lines.push('');
    if (!trace.length) lines.push('（无选择记录）');
    for (const t of trace) lines.push(t);
  }
  // v0.18.0 A3：纳入上下文包的条目记 use 信号（本次调用内按文件去重；--no-usage 可关）。
  if (usedFiles.size) {
    const usageOpts = { selfAgent: selfAgent, noUsage: !!opts.noUsage };
    for (const r of roots) {
      const rels = Array.from(usedFiles).filter(function (rel) { return fs.existsSync(path.join(r, rel)); });
      if (rels.length) applyUsageHits(r, rels, 'use', '', usageOpts);
    }
  }
  const reliability = doctorCore({ root: root });
  if (reliability.level !== 'ok') {
    lines.push('');
    lines.push('## 可靠性提醒');
    lines.push('');
    for (const message of reliability.critical) lines.push('- [严重] ' + message);
    for (const message of reliability.warnings) lines.push('- [警告] ' + message);
    if (!reliability.ok) lines.push('- 破坏性写入已锁定：先运行 yotta-memory doctor 修复严重问题。');
  }
  pagingState.used = usedDynamicChars;
  return { error: false, exitCode: 0, text: lines.join('\n'), trace: trace, hook: hookState, paging: pagingState };
}
function cmdContext(opts) {
  const r = contextCore(opts);
  if (opts.json) {
    if (r.report) console.log(JSON.stringify(r.report, null, 2));
    else console.log(JSON.stringify({ schema: 1, hook: r.hook || null, paging: r.paging || null, text: r.text }, null, 2));
  } else {
    console.log(r.text);
  }
  if (r.error) {
    const reminder = migrationReminderText(userRoot());
    if (reminder) console.log('\n' + reminder);
  }
  if (r.exitCode) process.exit(r.exitCode);
}

// ---- v0.18.0 A7：context --audit 上下文压缩审计（只读；不自动补写）----
function contextAuditGate(opts) {
  const raw = Array.isArray(opts.gate) ? opts.gate[opts.gate.length - 1] : opts.gate;
  if (raw === undefined || raw === null || raw === '') return null;
  const n = parseInt(raw, 10);
  return isNaN(n) ? null : n;
}
function contextAuditReadStdin() {
  // 只在 fd 0 明确是管道 / socket 时读取，避免测试运行器或交互终端被阻塞。
  try {
    const st = fs.fstatSync(0);
    if (!st.isFIFO() && !st.isSocket()) return null;
    return fs.readFileSync(0, 'utf8');
  } catch (e) {
    return null;
  }
}
function contextAuditSegments(text) {
  const out = [];
  // 中文信号词为主；补英文决策词，保证中英混排的宿主压缩摘要也能切出候选句。
  const keywordRe = /决定|敲定|约定|口径|红线|规则|承诺|下一步|待办|遗留|注意|以后|必须|不要|decision|decided|agreement|policy|rule|commit|next step|todo|remaining|note|must|never/i;
  const sectionRe = /^#{1,6}\s*(决策|下一步|遗留问题|decisions?|next\s*steps?|remaining|todos?)/i;
  let inSection = false;
  let inCode = false;
  for (const raw of String(text || '').split(/\r?\n/)) {
    const line = raw.trim();
    if (/^```/.test(line)) { inCode = !inCode; continue; }
    if (inCode || !line) continue;
    if (/^#{1,6}\s+/.test(line)) { inSection = sectionRe.test(line); continue; }
    if (/^\|/.test(line)) continue;
    const item = line.replace(/^[-*+]\s+/, '').replace(/^\d+[.、)]\s*/, '').trim();
    if (item.length < 4) continue;
    if (inSection || keywordRe.test(item)) {
      if (out.indexOf(item) === -1) out.push(item);
    }
  }
  return out;
}
function contextAuditCoverage(candidate, entries, minCoverage) {
  for (const e of entries) {
    const corpus = String(e.subject || '') + ' ' + String(e.statement || '');
    if (corpus.indexOf(candidate) !== -1) return { entry: e, coverage: 1, best: e };
    const stmt = String(e.statement || '');
    if (stmt.length >= 6 && candidate.indexOf(stmt) !== -1) return { entry: e, coverage: 1, best: e };
  }
  const tokens = new Set(tokenize(candidate).filter(function (t) { return t.indexOf(':') === -1; }));
  if (!tokens.size) return { entry: null, coverage: 0, best: null };
  let best = null;
  let bestCoverage = 0;
  for (const e of entries) {
    const etoks = new Set(tokenize(String(e.subject || '') + ' ' + String(e.statement || '')).filter(function (t) { return t.indexOf(':') === -1; }));
    let inter = 0;
    for (const t of tokens) if (etoks.has(t)) inter++;
    const coverage = inter / tokens.size;
    if (coverage > bestCoverage) { bestCoverage = coverage; best = e; }
  }
  return { entry: bestCoverage >= minCoverage ? best : null, coverage: bestCoverage, best: best };
}
function contextAuditRememberCommand(text) {
  const clean = String(text || '').replace(/"/g, "'").trim();
  const specificity = clean.replace(/^[^：:]*[：:]\s*/, '').trim();
  const subject = contextAuditSuggestionSubject(specificity || clean, 20);
  return 'yotta-memory remember FACT "' + subject + '" "' + clean + '" --verify';
}
function contextAuditSuggestionSubject(text, max) {
  // v0.18.0 修正：截断回退到非标点边界，避免切在「（」这类标点中间。
  const limit = parseInt(max, 10) || 20;
  const clean = String(text || '').trim();
  if (clean.length <= limit) return clean;
  const cut = clean.slice(0, limit);
  const trimmed = cut.replace(/[\s，。；：、,.;:!?！？（）()【】\[\]「」『』“”'"—–\-]+$/, '');
  return trimmed.length >= 8 ? trimmed : cut;
}
function contextAuditCore(opts) {
  opts = opts || {};
  const roots = memoryRoots();
  if (!roots.length) return { error: false, exitCode: 0, text: '记忆库不存在，请先运行: yotta-memory init' };
  const ident = resolveIdentity(opts);
  if (ident.error) return { error: true, exitCode: 3, text: ident.error };
  if (!ident.id) {
    return {
      error: true,
      exitCode: 3,
      text: 'context --audit 需要先声明身份：CLI 传 --agent <id>；stdio MCP 传 --agent-id <id> + --agent-key-file <path>；HTTP MCP 发送 X-Agent-Id + X-Agent-Key。',
    };
  }
  const selfAgent = ident.id;
  const owner = opts.owner || selfAgent;
  const root = userRoot();
  const keyError = validatePrivateIdentity(root, ident, owner);
  if (keyError) return { error: true, exitCode: 3, text: keyError };
  const cfg = loadConfig();
  const rawMin = parseFloat(cfg.context_audit_min_coverage);
  const minCoverage = (rawMin > 0 && rawMin <= 1) ? rawMin : 0.5;
  let input = null;
  let source = '';
  if (opts.text !== undefined && opts.text !== null && String(opts.text) !== '') {
    // v0.18.0：内联文本输入（MCP 侧用它替代文件路径，避免把 --from 变成任意文件读取通道）。
    input = String(opts.text);
    source = 'inline';
  } else if (opts.from !== undefined && opts.from !== null && String(opts.from) !== '') {
    if (String(opts.from) === '-') {
      input = fs.readFileSync(0, 'utf8');
      source = 'stdin';
    } else {
      const fp = path.resolve(String(opts.from));
      if (!fs.existsSync(fp)) return { error: true, exitCode: 2, text: '输入文件不存在: ' + fp };
      input = fs.readFileSync(fp, 'utf8');
      source = fp;
    }
  } else {
    // noStdin：MCP（stdio）的 fd 0 是协议流，绝不能被当成待审计内容读走。
    const piped = opts.noStdin ? null : contextAuditReadStdin();
    if (piped !== null && piped.trim()) { input = piped; source = 'stdin'; }
  }
  const entries = [];
  for (const r of roots) {
    for (const e of indexEntriesFor(r, {}).entries) {
      if (classifyRead(e, owner, '', !!opts.unsafe, selfAgent) === 'denied') continue;
      entries.push(e);
    }
  }
  const gate = contextAuditGate(opts);
  if (input === null) {
    const ctx = contextCore(Object.assign({}, opts, { audit: false, explain: true, noUsage: true }));
    const drops = (ctx.trace || []).filter(function (t) { return t.indexOf('[dropped]') === 0; });
    const items = drops.map(function (line) {
      const m = /^\[dropped\]\s+(\S+)\s+reason:\s+(\S+)/.exec(line);
      const file = m ? m[1] : '';
      const reason = m ? m[2] : '';
      const found = entries.filter(function (e) { return e.file === file; })[0];
      return {
        file: file,
        reason: reason,
        recallable: !!found,
        subject: found ? found.subject : '',
      };
    });
    const unrecallable = items.filter(function (x) { return !x.recallable; }).length;
    const lines = ['## yotta-memory context --audit（丢弃清单审计）', ''];
    lines.push('- 模式: 无输入内容，审计当前上下文包的丢弃清单（duplicate / budget_exceeded）');
    lines.push('- 计数: dropped ' + items.length + ' 条 / 仍可召回 ' + (items.length - unrecallable) + ' 条 / 无法召回 ' + unrecallable + ' 条');
    lines.push('');
    if (!items.length) lines.push('（本次上下文包无丢弃项。）');
    for (const item of items) {
      lines.push('- ' + item.file + '（' + item.reason + '）' + (item.recallable
        ? ' → 仍可召回: yotta-memory recall "' + String(item.subject).replace(/"/g, "'") + '"'
        : ' → 未在当前可读索引中找到，请人工核对'));
    }
    if (gate !== null) lines.push('', '- --gate ' + gate + ': 无法召回条数 ' + unrecallable + '（超过门槛时 exit 1）');
    return {
      error: false,
      exitCode: (gate !== null && unrecallable > gate) ? 1 : 0,
      text: lines.join('\n'),
      report: {
        schemaVersion: 1,
        mode: 'dropped',
        summary: { dropped: items.length, recallable: items.length - unrecallable, unrecallable: unrecallable },
        items: items,
      },
    };
  }
  const segments = contextAuditSegments(input);
  const items = segments.map(function (text) {
    const cov = contextAuditCoverage(text, entries, minCoverage);
    let status = 'missing';
    let matched = null;
    if (cov.entry) { status = 'landed'; matched = cov.entry; }
    else if (cov.best && cov.coverage > 0 && cov.coverage >= minCoverage * 0.6) status = 'uncertain';
    return {
      text: text,
      status: status,
      coverage: round3(cov.coverage),
      matched_file: matched ? matched.file : '',
      matched_subject: matched ? matched.subject : '',
      suggested_command: status === 'missing' ? contextAuditRememberCommand(text) : '',
    };
  });
  const landed = items.filter(function (x) { return x.status === 'landed'; });
  const missing = items.filter(function (x) { return x.status === 'missing'; });
  const uncertain = items.filter(function (x) { return x.status === 'uncertain'; });
  const lines = ['## yotta-memory context --audit（上下文压缩审计）', ''];
  lines.push('- 来源: ' + source + '（只读；不会自动补写记忆）');
  lines.push('- 汇总: 候选 ' + items.length + ' 条 / 已落盘 ' + landed.length + ' 条 / 未落盘 ' + missing.length + ' 条 / 无法判定 ' + uncertain.length + ' 条');
  lines.push('');
  lines.push('### 未落盘（建议落盘，命令仅打印不执行）');
  if (!missing.length) lines.push('（无）');
  for (const item of missing) {
    lines.push('- ' + item.text.slice(0, 120));
    lines.push('  → ' + item.suggested_command);
  }
  lines.push('');
  lines.push('### 无法判定（人工核对）');
  if (!uncertain.length) lines.push('（无）');
  for (const item of uncertain) lines.push('- ' + item.text.slice(0, 120) + '（覆盖率 ' + item.coverage + '）');
  lines.push('');
  lines.push('### 已落盘');
  if (!landed.length) lines.push('（无）');
  for (const item of landed) lines.push('- ' + item.text.slice(0, 120) + ' → ' + item.matched_file);
  if (gate !== null) lines.push('', '- --gate ' + gate + ': 未落盘 ' + missing.length + ' 条（超过门槛时 exit 1）');
  return {
    error: false,
    exitCode: (gate !== null && missing.length > gate) ? 1 : 0,
    text: lines.join('\n'),
    report: {
      schemaVersion: 1,
      mode: 'input',
      source: source,
      thresholds: { min_coverage: minCoverage },
      summary: { candidates: items.length, landed: landed.length, missing: missing.length, uncertain: uncertain.length },
      items: items,
    },
  };
}

// ---- v0.17.0 A1: bench 可复算基准评测（只读 / 本地 / 零依赖）----
const BENCH_SCHEMA_VERSION = 1;
const BENCH_DEFAULT_SEED = 20260925;
const BENCH_DEFAULT_BOOTSTRAP = 1000;
const BENCH_AUTO_QUERY_LIMIT = 20;
const BENCH_GATE_METRICS = {
  recall: 'recallAtK',
  recall_at_k: 'recallAtK',
  mrr: 'mrr',
  ndcg: 'ndcgAtK',
  ndcg_at_k: 'ndcgAtK',
  hit: 'hitRate',
  hitrate: 'hitRate',
  hit_rate: 'hitRate',
};
// 消融四组：关键词 / 语义 × 融合（0.65 语义 + 0.35 效用）/ 纯分排序
const BENCH_VARIANTS = [
  { variant: 'semantic-fused', semantic: true, fuse: true },
  { variant: 'lexical-fused', semantic: false, fuse: true },
  { variant: 'semantic-score', semantic: true, fuse: false },
  { variant: 'lexical-score', semantic: false, fuse: false },
];
function sha256Hex(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }
function round4(n) { return Math.round((Number(n) || 0) * 10000) / 10000; }
function seededRandom(seed) {
  let a = (Number(seed) || 0) >>> 0;
  if (!a) a = 1;
  return function () {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
// 索引指纹：index.json + 各分片内容一起哈希，改一条记忆就会变。
function indexFingerprint(root) {
  const manifestPath = indexPath(root);
  if (!fs.existsSync(manifestPath)) return { sha256: '', bytes: 0, files: 0 };
  const parts = ['ytm-index-fingerprint-v1\n'];
  let bytes = 0;
  let files = 0;
  const manifestBytes = fs.readFileSync(manifestPath);
  bytes += manifestBytes.length;
  files++;
  parts.push(INDEX_FILE + '\n' + sha256Hex(manifestBytes) + '\n');
  let shards = [];
  try {
    const d = JSON.parse(manifestBytes.toString('utf8'));
    if (d && Array.isArray(d.shards)) shards = d.shards;
  } catch (e) { /* ignore */ }
  for (const sh of shards) {
    if (!isSafeShardName(sh)) continue;
    const sp = path.join(root, sh);
    if (!fs.existsSync(sp)) continue;
    const buf = fs.readFileSync(sp);
    bytes += buf.length;
    files++;
    parts.push(sh + '\n' + sha256Hex(buf) + '\n');
  }
  return { sha256: sha256Hex(Buffer.from(parts.join(''), 'utf8')), bytes: bytes, files: files };
}
function benchEvalsetDigest(queries) {
  return sha256Hex(Buffer.from(JSON.stringify({ version: 1, queries: queries }), 'utf8'));
}
function autoBenchQueries(entries, seed) {
  const pool = entries
    .filter(function (e) { return String(e.subject || '').trim().length > 0; })
    .sort(function (a, b) { return String(a.file).localeCompare(String(b.file)); });
  const count = Math.min(BENCH_AUTO_QUERY_LIMIT, pool.length);
  const remaining = pool.slice();
  const rnd = seededRandom(seed);
  const queries = [];
  for (let i = 0; i < count; i++) {
    const picked = remaining.splice(Math.floor(rnd() * remaining.length), 1)[0];
    queries.push({ query: String(picked.subject), expect: [String(picked.file)] });
  }
  return queries;
}
function loadBenchEvalset(file, entries, seed) {
  if (!file) {
    const queries = autoBenchQueries(entries, seed);
    return { source: 'auto', file: '', queries: queries, sha256: benchEvalsetDigest(queries) };
  }
  const fp = path.resolve(String(file));
  if (!fs.existsSync(fp)) {
    return { error: '找不到评测集文件: ' + fp + '。请检查路径，或省略 --evalset 用库内自动基线集。' };
  }
  let data = null;
  try {
    data = JSON.parse(fs.readFileSync(fp, 'utf8'));
  } catch (e) {
    return { error: '评测集不是合法 JSON: ' + fp + '（' + (e && e.message ? e.message : String(e)) + '）' };
  }
  if (!data || data.version !== 1) {
    return { error: '评测集版本不支持: ' + fp + '。bench 评测集 v1 格式为 { "version": 1, "queries": [ { "query": "...", "expect": ["<记忆 id>"] } ] }。' };
  }
  if (!Array.isArray(data.queries) || !data.queries.length) {
    return { error: '评测集缺少 queries: ' + fp + '。至少需要一条 { "query": "...", "expect": ["<记忆 id>"] }。' };
  }
  const queries = [];
  for (const row of data.queries) {
    const query = row && typeof row.query === 'string' ? row.query.trim() : '';
    const expect = row && Array.isArray(row.expect) ? row.expect.map(String).filter(Boolean) : [];
    if (!query) return { error: '评测集存在空 query: ' + fp + '。每条查询都需要非空 query 字符串。' };
    if (!expect.length) return { error: '评测集缺少 expect: ' + fp + '（query=' + query + '）。expect 必须是记忆 id 数组。' };
    queries.push({ query: query, expect: expect });
  }
  return { source: 'file', file: fp, queries: queries, sha256: benchEvalsetDigest(queries) };
}
function parseBenchGates(list) {
  const out = [];
  for (const raw of list || []) {
    const text = String(raw);
    const cut = text.indexOf('=');
    if (cut <= 0) {
      return { error: '门禁格式不正确: ' + text + '。应为 <指标>=<数值>，例如 --gate mrr=0.6；指标可选 recall / mrr / ndcg / hit。' };
    }
    const metric = text.slice(0, cut).trim().toLowerCase();
    const value = parseFloat(text.slice(cut + 1));
    if (!BENCH_GATE_METRICS[metric]) {
      return { error: '门禁指标不支持: ' + text.slice(0, cut).trim() + '。可选指标: recall / mrr / ndcg / hit。' };
    }
    if (!isFinite(value)) {
      return { error: '门禁数值不正确: ' + text + '。门禁需要可比较的数值，例如 --gate mrr=0.6。' };
    }
    out.push({ metric: metric, key: BENCH_GATE_METRICS[metric], value: value });
  }
  return { gates: out, error: '' };
}
function entryMatchesExpect(entry, expectSet) {
  const ref = String((entry && entry.file) || '');
  return expectSet.has(ref) || expectSet.has(path.basename(ref));
}
function benchQueryMetrics(hits, expect, k) {
  const expectSet = new Set((expect || []).map(String));
  const top = hits.slice(0, k);
  let found = 0;
  let rr = 0;
  let dcg = 0;
  for (let i = 0; i < top.length; i++) {
    if (!entryMatchesExpect(top[i].entry, expectSet)) continue;
    found++;
    if (!rr) rr = 1 / (i + 1);
    dcg += 1 / Math.log2(i + 2);
  }
  let idcg = 0;
  const idealCount = Math.min(k, expectSet.size);
  for (let i = 0; i < idealCount; i++) idcg += 1 / Math.log2(i + 2);
  return {
    recall: expectSet.size ? Math.min(1, found / expectSet.size) : 0,
    mrr: rr,
    ndcg: idcg > 0 ? Math.min(1, dcg / idcg) : 0,
    hit: found ? 1 : 0,
  };
}
function bootstrapCI(values, seed, rounds) {
  if (!values.length) return [0, 0];
  const mean = values.reduce(function (s, v) { return s + v; }, 0) / values.length;
  const n = parseInt(rounds, 10) || 0;
  if (n <= 0) return [round4(mean), round4(mean)];
  const rnd = seededRandom(seed);
  const means = [];
  for (let b = 0; b < n; b++) {
    let sum = 0;
    for (let i = 0; i < values.length; i++) sum += values[Math.floor(rnd() * values.length)];
    means.push(sum / values.length);
  }
  means.sort(function (a, b) { return a - b; });
  const pick = function (p) {
    const idx = Math.min(means.length - 1, Math.max(0, Math.floor(p * (means.length - 1))));
    return round4(means[idx]);
  };
  return [pick(0.025), pick(0.975)];
}
function benchEvaluate(corpusByRoot, queries, options) {
  const perQuery = [];
  for (const row of queries) {
    const prefilter = options.semantic ? recallPrefilter(row.query) : null;
    const hits = [];
    for (const group of corpusByRoot) {
      const scored = scoreCandidates(group.entries, row.query, { semantic: options.semantic, prefilter: prefilter });
      for (const s of scored) hits.push({ entry: s.entry, score: s.score, root: group.root, detail: s.detail });
    }
    rankHits(hits, { fuse: options.fuse !== false, sortByScore: options.fuse === false });
    perQuery.push(benchQueryMetrics(hits, row.expect, options.k));
  }
  const mean = function (pick) {
    if (!perQuery.length) return 0;
    return perQuery.reduce(function (s, row) { return s + pick(row); }, 0) / perQuery.length;
  };
  const metrics = {
    recallAtK: round4(mean(function (r) { return r.recall; })),
    mrr: round4(mean(function (r) { return r.mrr; })),
    ndcgAtK: round4(mean(function (r) { return r.ndcg; })),
    hitRate: round4(mean(function (r) { return r.hit; })),
  };
  const ci95 = {
    recallAtK: bootstrapCI(perQuery.map(function (r) { return r.recall; }), options.seed, options.bootstrap),
    mrr: bootstrapCI(perQuery.map(function (r) { return r.mrr; }), options.seed, options.bootstrap),
    ndcgAtK: bootstrapCI(perQuery.map(function (r) { return r.ndcg; }), options.seed, options.bootstrap),
    hitRate: bootstrapCI(perQuery.map(function (r) { return r.hit; }), options.seed, options.bootstrap),
  };
  return { metrics: metrics, ci95: ci95, perQuery: perQuery.length };
}
function benchCore(opts) {
  opts = opts || {};
  const k = parseInt(opts.k, 10) > 0 ? Math.min(50, parseInt(opts.k, 10)) : 5;
  const seed = opts.seed === undefined || opts.seed === null || isNaN(parseInt(opts.seed, 10)) ? BENCH_DEFAULT_SEED : parseInt(opts.seed, 10);
  if (seed < 0) return { error: true, exitCode: 2, text: '随机种子必须是非负整数: ' + opts.seed };
  const bootstrap = opts.bootstrap === undefined || opts.bootstrap === null || isNaN(parseInt(opts.bootstrap, 10)) ? BENCH_DEFAULT_BOOTSTRAP : parseInt(opts.bootstrap, 10);
  if (bootstrap < 0) return { error: true, exitCode: 2, text: 'bootstrap 次数必须是非负整数: ' + opts.bootstrap };
  const yearFilter = normalizeYearList(opts.years);
  if (yearFilter.error) return { error: true, exitCode: 2, text: yearFilter.error };
  const years = yearFilter.years;
  const gates = parseBenchGates(opts.gate);
  if (gates.error) return { error: true, exitCode: 2, text: gates.error };

  const roots = memoryRoots();
  if (!roots.length) return { error: true, exitCode: 2, text: '记忆库不存在，请先运行: yotta-memory init' };
  const ident = resolveIdentity(opts);
  if (ident.error) return { error: true, exitCode: 3, text: ident.error };
  const selfAgent = ident.id;

  const corpusByRoot = [];
  const rootReports = [];
  let denied = 0;
  let privateSkipped = 0;
  for (const root of roots) {
    const pub = loadIndexFor(root, { years: years });
    if (!pub) {
      return { error: true, exitCode: 2, text: '索引缺失或版本过旧（' + root + '）：请先运行 yotta-memory reindex，再执行 bench。' };
    }
    const entries = [];
    for (const e of pub) {
      if (classifyRead(e, selfAgent, '', false, selfAgent) === 'denied') { denied++; continue; }
      entries.push(e);
    }
    if (isEncrypted(root)) {
      for (const owner of collectOwners(root)) {
        const key = getOwnerKeyFor(root, owner, { id: ident.id, agentKey: ident.agentKey });
        if (!key) { privateSkipped++; continue; }
        let idx = [];
        try { idx = loadOwnerIndex(root, owner, key); } catch (err) { idx = []; }
        for (const e of idx) {
          if (years.length && years.indexOf(entryYear(e)) === -1) continue;
          if (classifyRead(e, selfAgent, '', false, selfAgent) === 'denied') { denied++; continue; }
          entries.push(e);
        }
      }
    }
    corpusByRoot.push({ root: root, entries: entries });
    rootReports.push({ path: root, entries: entries.length, index: indexFingerprint(root) });
  }
  const corpusEntries = [];
  for (const group of corpusByRoot) for (const e of group.entries) corpusEntries.push(e);

  const evalset = loadBenchEvalset(opts.evalset, corpusEntries, seed);
  if (evalset.error) return { error: true, exitCode: 2, text: evalset.error };

  const baseOptions = { k: k, seed: seed, bootstrap: bootstrap, semantic: true, fuse: true };
  let timing = null;
  if (opts.timing) {
    const samples = [];
    for (const row of evalset.queries) {
      const started = process.hrtime.bigint();
      benchEvaluate(corpusByRoot, [row], baseOptions);
      samples.push(Number(process.hrtime.bigint() - started) / 1e6);
    }
    samples.sort(function (a, b) { return a - b; });
    const pick = function (p) { return round4(samples[Math.min(samples.length - 1, Math.max(0, Math.round(p * (samples.length - 1))))]); };
    timing = { p50Ms: pick(0.5), p95Ms: pick(0.95) };
  }
  const baseline = benchEvaluate(corpusByRoot, evalset.queries, baseOptions);
  const gateResults = (gates.gates || []).map(function (g) {
    const actual = baseline.metrics[g.key];
    return { metric: g.metric, value: g.value, actual: actual, pass: actual >= g.value };
  });
  const level = gateResults.every(function (g) { return g.pass; }) ? 'ok' : 'fail';
  const report = {
    schemaVersion: BENCH_SCHEMA_VERSION,
    command: 'bench',
    version: VERSION,
    params: { k: k, seed: seed, bootstrap: bootstrap },
    corpus: {
      entries: corpusEntries.length,
      denied: denied,
      privateSkipped: privateSkipped,
      roots: rootReports,
    },
    evalset: {
      source: evalset.source,
      file: evalset.file || '',
      sha256: evalset.sha256,
      queries: evalset.queries.length,
    },
    metrics: Object.assign({}, baseline.metrics, { ci95: baseline.ci95 }),
    gates: gateResults,
    embedding: {
      status: 'not-run',
      reason: 'bench 只跑本地确定性检索（关键词 / 语义），不调用外部 embedding 插件，保证可复算与只读',
    },
    reproducible: !opts.timing,
    level: level,
  };
  if (years.length) report.years = years.slice();
  if (opts.ablate) {
    report.ablation = BENCH_VARIANTS.map(function (v) {
      const result = benchEvaluate(corpusByRoot, evalset.queries, { k: k, seed: seed, bootstrap: bootstrap, semantic: v.semantic, fuse: v.fuse });
      return { variant: v.variant, metrics: result.metrics };
    });
  }
  if (timing) report.timing = timing;
  return { error: false, exitCode: level === 'fail' ? 1 : 0, text: renderBenchText(report), report: report };
}
function renderBenchText(report) {
  const lines = [];
  const m = report.metrics;
  lines.push('# 元忆基准评测（bench）');
  lines.push('');
  lines.push('- 记忆库: ' + report.corpus.roots.map(function (r) { return r.path; }).join('、'));
  lines.push('- 条目数: ' + report.corpus.entries +
    '；索引指纹: ' + report.corpus.roots.map(function (r) { return String(r.index.sha256).slice(0, 12) + '…'; }).join('、') +
    '（' + report.corpus.roots.map(function (r) { return r.index.files + ' 个文件 / ' + r.index.bytes + ' 字节'; }).join('；') + '）');
  lines.push('- 评测集: ' + (report.evalset.source === 'auto' ? '库内自动基线集（确定性抽样）' : report.evalset.file) +
    '；sha256 ' + report.evalset.sha256.slice(0, 12) + '…；' + report.evalset.queries + ' 条查询');
  lines.push('- 参数: k=' + report.params.k + '；seed=' + report.params.seed + '；bootstrap=' + report.params.bootstrap +
    (report.years && report.years.length ? '；年份=' + report.years.join(',') : ''));
  lines.push('');
  lines.push('检索质量：');
  lines.push('- Recall@' + report.params.k + ': ' + m.recallAtK + '（95% CI ' + m.ci95.recallAtK[0] + ' - ' + m.ci95.recallAtK[1] + '）');
  lines.push('- MRR: ' + m.mrr + '（95% CI ' + m.ci95.mrr[0] + ' - ' + m.ci95.mrr[1] + '）');
  lines.push('- nDCG@' + report.params.k + ': ' + m.ndcgAtK + '（95% CI ' + m.ci95.ndcgAtK[0] + ' - ' + m.ci95.ndcgAtK[1] + '）');
  lines.push('- HitRate: ' + m.hitRate + '（95% CI ' + m.ci95.hitRate[0] + ' - ' + m.ci95.hitRate[1] + '）');
  if (report.ablation && report.ablation.length) {
    lines.push('');
    lines.push('消融对比：');
    for (const row of report.ablation) {
      lines.push('- ' + row.variant + ': Recall@' + report.params.k + ' ' + row.metrics.recallAtK +
        '；MRR ' + row.metrics.mrr + '；nDCG@' + report.params.k + ' ' + row.metrics.ndcgAtK + '；HitRate ' + row.metrics.hitRate);
    }
    lines.push('- 口径: 关键词 / 语义 × 融合排序（0.65 语义 + 0.35 效用）/ 纯分排序；embedding 插件不参与。');
  }
  if (report.timing) {
    lines.push('');
    lines.push('检索耗时（--timing，非可复算项）：');
    lines.push('- p50: ' + report.timing.p50Ms + ' ms；p95: ' + report.timing.p95Ms + ' ms');
  }
  lines.push('');
  lines.push('门禁：');
  if (!report.gates.length) {
    lines.push('- 未设置（--gate <指标>=<数值> 可接入 CI）');
  } else {
    for (const g of report.gates) {
      lines.push('- ' + g.metric + ' >= ' + g.value + '：' + (g.pass ? '通过' : '未通过') + '（实际 ' + g.actual + '）');
    }
  }
  if (report.corpus.denied) lines.push('- 已跳过 ' + report.corpus.denied + ' 条当前身份不可读的记忆');
  lines.push('');
  lines.push('复算口径：库指纹 + 评测集指纹 + 参数一致时必须同输出；默认报告不含墙钟时间，只读、不写生产库。');
  return lines.join('\n');
}
function cmdBench(opts) {
  const r = benchCore(opts || {});
  if (r.error) {
    console.error(r.text);
    process.exit(r.exitCode || 2);
  }
  const json = JSON.stringify(r.report, null, 2);
  if (opts && opts.out) {
    const target = path.resolve(String(opts.out));
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, json + '\n', 'utf8');
  }
  console.log(opts && opts.json ? json : r.text);
  if (r.exitCode) process.exit(r.exitCode);
}

// ---- v0.17.0 A2：恢复 / 迁移基线探针（只读 / 本地 / 零依赖）----
const BASELINE_SCHEMA_VERSION = 1;
const BASELINE_DEFAULT_SEED = 20260925;
const BASELINE_MISSING_LIMIT = 20;
const CJK_RE = /[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/;
// 探针只读遍历记忆文件（不建索引、不碰访问计数）：恢复 / 迁移场景要验的是文件本身，而不是可能过期的索引。
function baselineReadEntries(root) {
  const entries = [];
  const unreadable = [];
  for (const fp of collectEntryFiles(root)) {
    const rel = relOf(root, fp);
    const owner = ownerFromPrivatePath(root, fp);
    if (isEncFile(fp) && !getOwnerKeyFor(root, owner)) {
      unreadable.push({ file: rel, reason: 'encrypted', owner: owner });
      continue;
    }
    try {
      entries.push(readEntry(fp, root));
    } catch (error) {
      const message = error && error.message ? error.message : String(error);
      // .enc 后缀但内容是明文（历史恢复残留）与「密钥在位但解不开」要分开报，修法完全不同。
      const reason = isEncFile(fp) ? (message.indexOf('非密文文件') !== -1 ? 'mislabelled' : 'undecryptable') : 'unreadable';
      unreadable.push({ file: rel, reason: reason, owner: owner, error: message });
    }
  }
  return { entries: entries, unreadable: unreadable };
}
// 条目身份键与布局无关（旧平铺 facts/x.md 与新年/月分层指向同一条记忆时键相同）。
function baselineEntryKey(entry) {
  return String(entry.type || 'FACT') + '/' + String(entry.owner || 'public') + '/' + path.basename(String(entry.file || ''));
}
function baselineSample(pool, seed, count) {
  const list = pool.slice().sort(function (a, b) { return String(a.file).localeCompare(String(b.file)); });
  const rnd = seededRandom(seed);
  const picked = [];
  const remaining = list.slice();
  for (let i = 0; i < Math.min(count, remaining.length); i++) {
    picked.push(remaining.splice(Math.floor(rnd() * remaining.length), 1)[0]);
  }
  return picked;
}
function baselineRecall(root, entries, query, limit) {
  const prefilter = query ? recallPrefilter(query) : null;
  const hits = [];
  for (const scored of scoreCandidates(entries, query, { semantic: true, prefilter: prefilter, root: root })) {
    hits.push({ entry: scored.entry, score: scored.score, root: root, detail: scored.detail });
  }
  rankHits(hits, { fuse: true });
  return hits.slice(0, limit || 5);
}
function loadBaselineTemplate(file) {
  const fp = path.resolve(String(file));
  if (!fs.existsSync(fp)) {
    return { error: '找不到基线模板: ' + fp + '。请检查路径，或省略 --template 用库内确定性探针。' };
  }
  let data = null;
  try {
    data = JSON.parse(fs.readFileSync(fp, 'utf8'));
  } catch (error) {
    return { error: '基线模板不是合法 JSON: ' + fp + '（' + (error && error.message ? error.message : String(error)) + '）' };
  }
  if (!data || data.version !== 1) {
    return { error: '基线模板版本不支持: ' + fp + '。v1 格式为 { "version": 1, "expect_owners": [], "expect_min_entries": 0, "expect_types": {}, "queries": [] }。' };
  }
  const out = { version: 1, file: fp, expect_owners: [], expect_min_entries: 0, expect_types: {}, queries: [] };
  if (data.expect_owners !== undefined) {
    if (!Array.isArray(data.expect_owners)) return { error: '基线模板 expect_owners 必须是数组: ' + fp };
    out.expect_owners = data.expect_owners.map(String).filter(Boolean);
  }
  if (data.expect_min_entries !== undefined) {
    const n = parseInt(data.expect_min_entries, 10);
    if (!isFinite(n) || n < 0) return { error: '基线模板 expect_min_entries 必须是非负整数: ' + fp };
    out.expect_min_entries = n;
  }
  if (data.expect_types !== undefined) {
    if (!data.expect_types || typeof data.expect_types !== 'object' || Array.isArray(data.expect_types)) {
      return { error: '基线模板 expect_types 必须是 { "类型": 最小条数 } 对象: ' + fp };
    }
    for (const key of Object.keys(data.expect_types)) {
      const type = String(key).toUpperCase();
      if (TYPES.indexOf(type) === -1) {
        return { error: '基线模板 expect_types 含未知类型 ' + key + '（可选: ' + TYPES.join(' / ') + '）: ' + fp };
      }
      const n = parseInt(data.expect_types[key], 10);
      if (!isFinite(n) || n < 0) return { error: '基线模板 expect_types.' + key + ' 必须是非负整数: ' + fp };
      out.expect_types[type] = n;
    }
  }
  if (data.queries !== undefined) {
    if (!Array.isArray(data.queries)) return { error: '基线模板 queries 必须是数组: ' + fp };
    for (const row of data.queries) {
      const query = row && typeof row.query === 'string' ? row.query.trim() : '';
      const expect = row && Array.isArray(row.expect) ? row.expect.map(String).filter(Boolean) : [];
      if (!query) return { error: '基线模板存在空 query: ' + fp };
      if (!expect.length) return { error: '基线模板缺少 expect（query=' + query + '）: ' + fp };
      out.queries.push({ id: String((row && row.id) || query), query: query, expect: expect });
    }
  }
  return out;
}
// 六类固定探针：身份 / 近期 / 仅源库独有 / CJK / 操作规则 / owner 范围；模板可在其上追加显式期望。
function baselineCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.root || userRoot());
  const seed = parseInt(opts.seed, 10) || BASELINE_DEFAULT_SEED;
  const empty = { schemaVersion: BASELINE_SCHEMA_VERSION, error: true, exitCode: 2, ok: false, level: 'fail', root: root, against: '', template: '', seed: seed, counts: {}, probes: [], unreadable: [] };
  let template = null;
  if (opts.template) {
    template = loadBaselineTemplate(opts.template);
    if (template.error) return Object.assign({}, empty, { text: template.error });
  }
  const against = opts.against ? path.resolve(String(opts.against)) : '';
  if (against && !fs.existsSync(against)) {
    return Object.assign({}, empty, { against: against, text: '找不到对比库: ' + against + '。--against 需要指向另一个记忆库根目录（通常是迁移前的源库）。' });
  }
  const ident = resolveIdentity(opts);
  const selfAgent = (ident && !ident.error && ident.id) ? ident.id : '';
  const read = baselineReadEntries(root);
  const entries = read.entries;
  const readable = entries.filter(function (e) { return classifyRead(e, selfAgent, '', false, selfAgent) !== 'denied'; });
  const probes = [];
  const baselineCounts = {};
  function record(id, title, status, detail) {
    probes.push({ id: id, title: title, status: status, detail: detail });
  }
  function recallProbe(id, title, pick) {
    const query = String(pick.subject || '').trim() || String(pick.statement || '').trim().slice(0, 24);
    const hits = baselineRecall(root, readable, query, 5);
    const expect = new Set([String(pick.file)]);
    if (query && hits.some(function (h) { return entryMatchesExpect(h.entry, expect); })) {
      record(id, title, 'pass', '可召回: ' + pick.file);
    } else {
      record(id, title, 'fail', '无法召回: ' + pick.file + '（按该条目自己的主题检索未命中）');
    }
  }

  // ① 身份：agents.json / iam 在位
  const expectedOwners = template ? template.expect_owners : [];
  const agentsFile = agentsPath(root);
  if (!fs.existsSync(agentsFile)) {
    if (entries.length) record('identity', '身份登记', 'fail', '缺少 agents.json（智能体身份登记）；恢复后请用 yotta-memory iam <id> 重新登记。');
    else record('identity', '身份登记', 'skip', '库内没有记忆条目且没有 agents.json，暂不判定。');
  } else {
    let data = null;
    let parseError = '';
    try { data = JSON.parse(fs.readFileSync(agentsFile, 'utf8')); } catch (error) { parseError = error && error.message ? error.message : String(error); }
    const registered = data && data.agents && typeof data.agents === 'object' ? Object.keys(data.agents) : [];
    if (parseError) {
      record('identity', '身份登记', 'fail', 'agents.json 无法解析（' + parseError + '）；请先恢复身份登记。');
    } else if (!registered.length) {
      record('identity', '身份登记', 'fail', 'agents.json 没有任何智能体登记；恢复后请用 yotta-memory iam <id> 重新登记。');
    } else {
      const missingOwners = expectedOwners.filter(function (o) { return registered.indexOf(o) === -1; });
      if (missingOwners.length) {
        record('identity', '身份登记', 'fail', 'agents.json 缺少模板要求的 owner: ' + missingOwners.join(', ') + '（已登记: ' + registered.join(', ') + '）');
      } else {
        record('identity', '身份登记', 'pass', 'agents.json 已登记 ' + registered.join(', '));
      }
    }
  }

  // ② 近期：最近条目可召回
  const byRecency = readable.slice().sort(function (a, b) {
    return String(b.created || '').localeCompare(String(a.created || '')) || String(b.file).localeCompare(String(a.file));
  });
  if (!byRecency.length) record('recent', '近期条目', 'skip', '没有当前身份可读的记忆条目。');
  else recallProbe('recent', '近期条目', byRecency[0]);

  // ③ 仅源库独有：--against 差集条目必须已在目标库
  if (!against) {
    record('source-only', '对比库差集', 'skip', '未提供 --against 对比库，跳过迁移差集校验。');
  } else {
    const sourceRead = baselineReadEntries(against);
    const targetKeys = new Set(entries.map(baselineEntryKey));
    const sourceKeys = new Set();
    const missing = [];
    for (const e of sourceRead.entries) {
      const key = baselineEntryKey(e);
      if (sourceKeys.has(key)) continue;
      sourceKeys.add(key);
      if (!targetKeys.has(key)) missing.push(e);
    }
    let targetOnly = 0;
    for (const key of targetKeys) if (!sourceKeys.has(key)) targetOnly++;
    const counts = { source_entries: sourceRead.entries.length, missing: missing.length, target_only: targetOnly };
    if (missing.length) {
      const shown = missing.slice(0, BASELINE_MISSING_LIMIT).map(function (e) { return e.file; });
      record('source-only', '对比库差集', 'fail', '相对对比库缺失 ' + missing.length + ' 条: ' + shown.join(', ') + (missing.length > shown.length ? ' …' : ''));
    } else {
      record('source-only', '对比库差集', 'pass', '对比库 ' + sourceRead.entries.length + ' 条全部在目标库命中' + (targetOnly ? '（目标库另有 ' + targetOnly + ' 条新增）' : ''));
    }
    baselineCounts.sourceOnly = counts;
  }

  // ④ CJK：中文条目可召回
  const cjkPool = readable.filter(function (e) { return CJK_RE.test(String(e.subject || '') + String(e.statement || '')); });
  if (!cjkPool.length) record('cjk', '中文条目', 'skip', '没有当前身份可读的中文条目。');
  else recallProbe('cjk', '中文条目', baselineSample(cjkPool, seed, 1)[0]);

  // ⑤ 操作规则：BOUND 类可读
  const boundPool = entries.filter(function (e) { return e.type === 'BOUND'; });
  if (!boundPool.length) {
    record('rules', '操作规则', 'skip', '库内没有 BOUND 操作规则条目。');
  } else {
    const pick = boundPool.slice().sort(function (a, b) { return String(a.file).localeCompare(String(b.file)); })[0];
    const fp = path.join(root, String(pick.file));
    try {
      readEntry(fp, root);
      record('rules', '操作规则', 'pass', 'BOUND 规则可读: ' + pick.file);
    } catch (error) {
      const owner = ownerFromPrivatePath(root, fp);
      if (isEncFile(fp) && !getOwnerKeyFor(root, owner)) {
        record('rules', '操作规则', 'skip', 'BOUND 规则为加密私密条目，缺少 ' + owner + ' 的授权密钥，未做可读性验证。');
      } else {
        record('rules', '操作规则', 'fail', 'BOUND 规则不可读: ' + pick.file + '（' + (error && error.message ? error.message : String(error)) + '）');
      }
    }
  }

  // ⑥ owner 范围：各 owner 计数 + 模板条数期望
  const ownerCounts = {};
  for (const fp of collectEntryFiles(root)) {
    const owner = ownerFromPrivatePath(root, fp) || 'public';
    ownerCounts[owner] = (ownerCounts[owner] || 0) + 1;
  }
  baselineCounts.owners = ownerCounts;
  const ownerNames = Object.keys(ownerCounts).sort();
  const corrupted = read.unreadable.filter(function (u) { return u.reason !== 'encrypted'; });
  if (!ownerNames.length) {
    record('owner', 'owner 范围', 'skip', '库内没有记忆文件。');
  } else if (corrupted.length) {
    const labels = { undecryptable: '密钥在位但解不开', mislabelled: '.enc 后缀但内容是明文', unreadable: '读取失败' };
    const reasonCounts = {};
    for (const item of corrupted) reasonCounts[item.reason] = (reasonCounts[item.reason] || 0) + 1;
    const summary = Object.keys(reasonCounts).map(function (reason) {
      return (labels[reason] || reason) + ' ' + reasonCounts[reason] + ' 个';
    }).join('；');
    record('owner', 'owner 范围', 'fail', '存在无法作为记忆读取的文件: ' + summary + '；例如 ' + corrupted.slice(0, 5).map(function (u) { return u.file; }).join(', '));
  } else if (template && template.expect_min_entries && entries.length < template.expect_min_entries) {
    const parts = ownerNames.map(function (o) { return o + '=' + ownerCounts[o]; });
    record('owner', 'owner 范围', 'fail', '记忆条数 ' + entries.length + ' 少于模板要求的 ' + template.expect_min_entries + '：缺少 ' + (template.expect_min_entries - entries.length) + ' 条（owner: ' + parts.join(', ') + '）');
  } else {
    const typeCounts = {};
    for (const e of entries) typeCounts[e.type] = (typeCounts[e.type] || 0) + 1;
    const shortTypes = [];
    const expectedTypes = template ? template.expect_types : {};
    for (const type of Object.keys(expectedTypes)) {
      const got = typeCounts[type] || 0;
      if (got < expectedTypes[type]) shortTypes.push(type + ' 缺少 ' + (expectedTypes[type] - got) + ' 条');
    }
    const parts = ownerNames.map(function (o) { return o + '=' + ownerCounts[o]; });
    if (shortTypes.length) {
      record('owner', 'owner 范围', 'fail', '模板要求的类型条数不足: ' + shortTypes.join('；') + '（owner: ' + parts.join(', ') + '）');
    } else {
      record('owner', 'owner 范围', 'pass', 'owner 计数: ' + parts.join(', ') + (read.unreadable.length ? '（另有 ' + read.unreadable.length + ' 个加密条目未读取）' : ''));
    }
  }

  // 模板显式查询（可选追加探针，不替代上面六类）
  if (template && template.queries.length) {
    const failed = [];
    for (const row of template.queries) {
      const hits = baselineRecall(root, readable, row.query, 5);
      const expect = new Set(row.expect);
      if (!hits.some(function (h) { return entryMatchesExpect(h.entry, expect); })) failed.push(row.id);
    }
    if (failed.length) record('template-queries', '模板查询', 'fail', '模板查询未命中: ' + failed.join(', ') + '（共 ' + template.queries.length + ' 条）');
    else record('template-queries', '模板查询', 'pass', '模板查询全部命中（共 ' + template.queries.length + ' 条）');
  }

  const fails = probes.filter(function (p) { return p.status === 'fail'; });
  const skips = probes.filter(function (p) { return p.status === 'skip'; });
  const counts = {
    entries: entries.length,
    readable: readable.length,
    unreadable: read.unreadable.length,
    owners: baselineCounts.owners,
    missing: baselineCounts.sourceOnly ? baselineCounts.sourceOnly.missing : 0,
    target_only: baselineCounts.sourceOnly ? baselineCounts.sourceOnly.target_only : 0,
    source_entries: baselineCounts.sourceOnly ? baselineCounts.sourceOnly.source_entries : 0,
  };
  const report = {
    schemaVersion: BASELINE_SCHEMA_VERSION,
    error: false,
    ok: fails.length === 0,
    level: fails.length ? 'fail' : 'pass',
    root: root,
    against: against,
    template: template ? template.file : '',
    seed: seed,
    counts: counts,
    probes: probes,
    unreadable: read.unreadable,
  };
  const statusLabel = { pass: '通过', fail: '失败', skip: '跳过' };
  const lines = [
    '# 元忆基线探针（恢复 / 迁移）',
    '',
    '- 记忆库: ' + root,
    '- 对比库: ' + (against || '(未提供，跳过差集校验)'),
    '- 条目: ' + counts.entries + ' 条可读 / ' + counts.readable + ' 条当前身份可读 / ' + counts.unreadable + ' 个未读取',
    '- 结果: ' + (report.ok ? '通过' : '失败') + '（通过 ' + (probes.length - fails.length - skips.length) + ' / 失败 ' + fails.length + ' / 跳过 ' + skips.length + '）',
  ];
  for (const probe of probes) {
    lines.push('- [' + statusLabel[probe.status] + '] ' + probe.title + ' · ' + probe.detail);
  }
  if (fails.length) lines.push('- 缺失项清单: ' + fails.map(function (p) { return p.id; }).join(', '));
  report.text = lines.join('\n');
  return report;
}

// ---- v0.17.0 A4：记忆库安全扫描（默认只读 / 本地 / 零依赖）----
// 分工口径：元钥扫源码仓库、元信扫技能包、元忆扫记忆库。规则词表不另起一套——
// 每条规则的 ref 指向家族规则表里的原始规则 id（<规则 id>@<技能 slug>），
// test/memory-scan.test.js 会在源码仓库内逐条回查这些规则 id 在对应技能里是否仍存在。
const SCAN_SCHEMA_VERSION = 1;
const SCAN_CLASSES = ['malicious-instruction', 'prompt-injection', 'credential-leak', 'data-exfiltration', 'guardrail-bypass', 'behavior-manipulation', 'privilege-escalation'];
const SCAN_SEVERITIES = ['safe', 'low', 'medium', 'high', 'critical'];
const SCAN_MAX_FINDINGS = 500;
const SCAN_MAX_FILES = 20000;
const SCAN_QUARANTINE_DIR = '.memory-scan';
const SCAN_POLICY_FILE = 'security/scan-policy.json';
const MEMORY_SCAN_RULES = [
  // ── 恶意指令（元安 DownloadExec / 元盾危险命令）──
  { id: 'YTM-MAL-001', class: 'malicious-instruction', severity: 'critical', ref: 'DEX-001@yotta-security-audit', title: 'curl 下载内容交给 shell 执行', mask: false, re: /\bcurl\b[^\n|;]{0,120}\|\s*(?:ba)?sh\b/i },
  { id: 'YTM-MAL-002', class: 'malicious-instruction', severity: 'critical', ref: 'CMD-PIPE-WGET@yotta-guardian', title: 'wget 下载内容交给 shell 执行', mask: false, re: /\bwget\b[^\n|;]{0,120}\|\s*(?:ba)?sh\b/i },
  { id: 'YTM-MAL-003', class: 'malicious-instruction', severity: 'critical', ref: 'CMD-REV-BASH@yotta-guardian', title: '反弹 shell', mask: false, re: /\b(?:bash\s+-i\s*>&?\s*\/dev\/tcp|nc\s+-e\s+\/bin\/(?:ba)?sh)\b/i },
  { id: 'YTM-MAL-004', class: 'malicious-instruction', severity: 'high', ref: 'CMD-PS-ENCODED@yotta-guardian', title: '编码后的 PowerShell 命令', mask: false, re: /powershell(?:\.exe)?[^\n]{0,40}\s-(?:enc|e|encodedcommand)\b/i },
  // ── Prompt 注入（元信 PIJ）──
  { id: 'YTM-PIJ-001', class: 'prompt-injection', severity: 'high', ref: 'PIJ-001@yotta-verify', title: '要求忽略之前的指令', mask: false, re: /(?:ignore|disregard|forget|overlook|skip)\s+(?:all\s+|any\s+|the\s+|previous\s+)*(?:previous\s+|earlier\s+)*(?:instructions?|prompts?|directives?|guidelines?|rules?|context|messages?)/i },
  { id: 'YTM-PIJ-002', class: 'prompt-injection', severity: 'high', ref: 'PIJ-002@yotta-verify', title: '要求忽略之前指令（中文）', mask: false, re: /(?:忽略|无视|忘记|不要理会|别管|忘掉)(?:之前|以上|前面|所有|一切)?(?:的)?(?:指令|提示|设定|规则|上下文|内容)/ },
  { id: 'YTM-PIJ-003', class: 'prompt-injection', severity: 'high', ref: 'PIJ-009@yotta-verify', title: '伪系统消息', mask: false, re: /(?:以下内容|下面这段|注意).{0,30}(?:系统消息|系统指令|来自系统|这是系统)/ },
  { id: 'YTM-PIJ-004', class: 'prompt-injection', severity: 'medium', ref: 'PIJ-014@yotta-verify', title: '伪系统标签', mask: false, re: /<\s*(?:system|sysadmin)\s*(?:message|prompt|instruction|role)?\s*>/i },
  { id: 'YTM-PIJ-005', class: 'prompt-injection', severity: 'high', ref: 'PIJ-015@yotta-verify', title: '要求泄露系统提示词', mask: false, re: /(?:reveal|show|print|output|display)\s+(?:me\s+|your\s+)?(?:system\s+)?(?:prompt|instructions?|system\s+message)/i },
  { id: 'YTM-PIJ-006', class: 'prompt-injection', severity: 'high', ref: 'PIJ-016@yotta-verify', title: '要求泄露系统提示词（中文）', mask: false, re: /(?:输出|显示|打印|告诉我).{0,20}(?:你的|系统)?(?:系统提示词|系统指令|内部指令)/ },
  { id: 'YTM-PIJ-007', class: 'prompt-injection', severity: 'medium', ref: 'PIJ-017@yotta-verify', title: '条件触发注入', mask: false, re: /when\s+(?:i|the\s+user)\s+(?:say|type|send|input)\s+[^\n]{0,40}\s*(?:then|you\s+will|ignore|do)/i },
  // ── 凭证泄漏（元钥；命中片段一律打码，避免二次泄露）──
  { id: 'YTM-SEC-001', class: 'credential-leak', severity: 'critical', ref: 'github@yotta-secret', title: 'GitHub Token', mask: true, re: /\bgh[pousr]_[0-9A-Za-z]{36,}\b|\bgithub_pat_[0-9A-Za-z_]{20,}\b/ },
  { id: 'YTM-SEC-002', class: 'credential-leak', severity: 'critical', ref: 'aws_secret@yotta-secret', title: 'AWS 秘密访问密钥', mask: true, re: /aws[_-]?secret[_-]?access[_-]?key\b\s*[=:]\s*["']?[A-Za-z0-9/+=]{40}/i },
  { id: 'YTM-SEC-003', class: 'credential-leak', severity: 'high', ref: 'openai@yotta-secret', title: 'OpenAI API Key', mask: true, re: /\bsk-(?!ant-)[A-Za-z0-9_-]{20,}\b/ },
  { id: 'YTM-SEC-004', class: 'credential-leak', severity: 'critical', ref: 'pem_private@yotta-secret', title: 'PEM 私钥块', mask: true, re: /-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----/ },
  { id: 'YTM-SEC-005', class: 'credential-leak', severity: 'high', ref: 'credential@yotta-secret', title: '凭据赋值', mask: true, re: /(?:password|passwd|pwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|private[_-]?key|token)\s*[:=]\s*["']?[^\s"',;]{6,}/i },
  { id: 'YTM-SEC-006', class: 'credential-leak', severity: 'high', ref: 'url_userinfo@yotta-secret', title: 'URL 内嵌账号密码', mask: true, re: /\b(?:https?|ftp|smtp|mongodb(?:\+srv)?|redis|mysql|postgres(?:ql)?):\/\/[^/\s:@]+:[^/\s@]+@/i },
  // ── 数据外泄（元信 PIJ 外传指令 / 元安 Exfiltration）──
  { id: 'YTM-EXF-001', class: 'data-exfiltration', severity: 'high', ref: 'PIJ-011@yotta-verify', title: '把上下文/密钥发送到远端', mask: false, re: /(?:send|upload|post|exfiltrate|transmit)\s+(?:the|all|your|any)?\s*(?:contents?|data|files?|env|environment|keys?|secrets?|memory|context|conversation|prompts?)\s*(?:to|via|using)\s*(?:this\s+)?(?:url|endpoint|server|http)/i },
  { id: 'YTM-EXF-002', class: 'data-exfiltration', severity: 'high', ref: 'PIJ-012@yotta-verify', title: '把上下文/密钥发送到远端（中文）', mask: false, re: /(?:把|将|请将)(?:你的|所有|全部)?(?:上下文|记忆|环境变量|密钥|文件|对话|提示词).{0,40}(?:发送|上传|提交|传给|发给)/ },
  { id: 'YTM-EXF-003', class: 'data-exfiltration', severity: 'high', ref: 'EXF-001@yotta-security-audit', title: '命令行上传数据到远端', mask: false, re: /\b(?:curl|wget)\b[^\n]{0,80}(?:--data\b|--upload-file\b|-d\s|-T\s)/i },
  // ── 护栏绕过（元信 PIJ 隐藏意图 / 覆盖护栏）──
  { id: 'YTM-GRD-001', class: 'guardrail-bypass', severity: 'high', ref: 'PIJ-004@yotta-verify', title: '要求覆盖/绕过安全护栏', mask: false, re: /(?:override|disregard|bypass)\s+(?:all\s+)?(?:previous\s+)?(?:instructions?|rules?|safety|guardrails?|security)/i },
  { id: 'YTM-GRD-002', class: 'guardrail-bypass', severity: 'high', ref: 'PIJ-022@yotta-verify', title: '禁止告知用户（中文）', mask: false, re: /(?:不要告诉用户|别告诉用户|无需告知用户|不用告诉用户|不要让用户知道)/ },
  { id: 'YTM-GRD-003', class: 'guardrail-bypass', severity: 'high', ref: 'PIJ-021@yotta-verify', title: '禁止告知用户', mask: false, re: /(?:do not|don'?t|never)\s+(?:tell|inform|notify|mention|reveal)\s+(?:the\s+)?user/i },
  { id: 'YTM-GRD-004', class: 'guardrail-bypass', severity: 'high', ref: 'PIJ-026@yotta-verify', title: '要求不经用户同意直接执行（中文）', mask: false, re: /(?:不要问用户|无需询问|不用问|不需要征求|别问用户)/ },
  { id: 'YTM-GRD-005', class: 'guardrail-bypass', severity: 'high', ref: 'PIJ-025@yotta-verify', title: '要求不经用户同意直接执行', mask: false, re: /(?:without|no\s+need\s+to)\s+(?:telling|informing|asking|consulting)\s+(?:the\s+)?user/i },
  // ── 行为操纵（元信 PIJ 角色伪造）──
  { id: 'YTM-BHV-001', class: 'behavior-manipulation', severity: 'medium', ref: 'PIJ-007@yotta-verify', title: '宣称新角色（中文）', mask: false, re: /(?:你现在是|从现在起你是|你的新角色是|从此刻起你是|你正在扮演)/ },
  { id: 'YTM-BHV-002', class: 'behavior-manipulation', severity: 'medium', ref: 'PIJ-005@yotta-verify', title: '角色伪造：冒充系统/管理员', mask: false, re: /\byou\s+are\s+now\b[^\n]{0,60}(?:mode|role|system|admin|root|developer|assistant)/i },
  { id: 'YTM-BHV-003', class: 'behavior-manipulation', severity: 'medium', ref: 'PIJ-006@yotta-verify', title: '角色伪造：扮演系统/管理员', mask: false, re: /(?:act|behave|pretend)\s+as\s+(?:a\s+|an\s+)?(?:system|admin|root|god\s+mode|developer)/i },
  { id: 'YTM-BHV-004', class: 'behavior-manipulation', severity: 'high', ref: 'PIJ-003@yotta-verify', title: '从现在起重定向行为', mask: false, re: /from\s+now\s+on[^\n]{0,40}(?:follow|obey|you\s+are|act)/i },
  { id: 'YTM-BHV-005', class: 'behavior-manipulation', severity: 'high', ref: 'PIJ-024@yotta-verify', title: '要求只回复确认词（中文）', mask: false, re: /(?:只回复|仅回复|直接回复)\s*(?:OK|ok|收到|好|是)/ },
  // ── 权限提升（元信 PIJ 全权暗示 / 元盾 setuid / 元安 PrivilegeEscalation）──
  { id: 'YTM-PRV-001', class: 'privilege-escalation', severity: 'high', ref: 'PIJ-008@yotta-verify', title: '以全权/管理员权限执行', mask: false, re: /with\s+(?:full|super|root|admin|system|unrestricted|unlimited)\s+(?:privileges|access|permissions?|power)/i },
  { id: 'YTM-PRV-002', class: 'privilege-escalation', severity: 'critical', ref: 'CMD-CHMOD-SETUID@yotta-guardian', title: '设置 setuid 权限', mask: false, re: /\bchmod\s+(?:[ug]\+s|[0-7]{0,3}4[0-7]{3})\b/ },
  { id: 'YTM-PRV-003', class: 'privilege-escalation', severity: 'high', ref: 'PRI-001@yotta-security-audit', title: '提权到 shell', mask: false, re: /\bsudo\s+(?:su|bash|sh|-i)\b/ },
  { id: 'YTM-PRV-004', class: 'privilege-escalation', severity: 'high', ref: 'PIJ-027@yotta-verify', title: '采集键盘/凭据', mask: false, re: /(?:capture|record|log|monitor)\s+(?:all\s+)?(?:keystrokes|input|credentials?|passwords?|everything\s+the\s+user)/i },
  { id: 'YTM-PRV-005', class: 'privilege-escalation', severity: 'high', ref: 'PIJ-028@yotta-verify', title: '采集键盘/凭据（中文）', mask: false, re: /(?:记录|收集|监控|窃取)(?:用户)?(?:输入|键盘|密码|凭据|按键)/ },
  { id: 'YTM-PRV-006', class: 'privilege-escalation', severity: 'high', ref: 'PIJ-020@yotta-verify', title: '要求执行下载内容（中文）', mask: false, re: /(?:执行|运行|下载并运行|安装).{0,40}(?:curl|wget|下载).{0,60}(?:然后|并)?(?:执行|运行)/ },
];
function scanSeverityRank(severity) { return SCAN_SEVERITIES.indexOf(String(severity || '').toLowerCase()); }
function scanEmptySummary() {
  const byClass = {};
  for (const cls of SCAN_CLASSES) byClass[cls] = 0;
  const bySeverity = {};
  for (const sev of SCAN_SEVERITIES) bySeverity[sev] = 0;
  return {
    files: 0,
    encrypted: 0,
    mislabelled: 0,
    scanned: 0,
    hits: 0,
    suppressed: 0,
    invalid_policy: 0,
    expired_policy: 0,
    byClass: byClass,
    bySeverity: bySeverity,
    maxSeverity: 'safe',
    truncated: false,
  };
}
function scanLineHash(line) {
  return crypto.createHash('sha256').update(String(line || ''), 'utf8').digest('hex');
}
function loadScanPolicy(root, noPolicy) {
  const pathname = path.join(root, SCAN_POLICY_FILE);
  if (noPolicy) {
    return { path: pathname, entries: [], map: new Map(), invalid: 0, expired: 0, used: new Set(), warnings: [] };
  }
  if (!fs.existsSync(pathname)) {
    return { path: pathname, entries: [], map: new Map(), invalid: 0, expired: 0, used: new Set(), warnings: [] };
  }
  let data = null;
  try { data = JSON.parse(fs.readFileSync(pathname, 'utf8')); } catch (error) {
    return { path: pathname, entries: [], map: new Map(), invalid: 1, expired: 0, used: new Set(), warnings: ['扫描策略 JSON 无法解析: ' + error.message] };
  }
  const rawEntries = data && Array.isArray(data.entries) ? data.entries : [];
  const entries = [];
  const map = new Map();
  let invalid = data && Array.isArray(data.entries) ? 0 : 1;
  let expired = 0;
  const warnings = [];
  if (!data || !Array.isArray(data.entries)) warnings.push('扫描策略结构无效：缺少 entries 数组。');
  for (const raw of rawEntries) {
    const rule = String(raw && raw.rule || '').trim();
    const file = String(raw && raw.file || '').replace(/\\/g, '/');
    const hash = String(raw && raw.line_sha256 || '').trim().toLowerCase();
    const reviewBy = String(raw && raw.review_by || '').trim();
    const reason = String(raw && raw.reason || '').trim();
    const valid = /^YTM-[A-Z]+-\d{3}$/.test(rule) &&
      isSafeRelPath(file) && file.indexOf('*') === -1 && MEMORY_FILE_RE.test(file) &&
      /^[a-f0-9]{64}$/.test(hash) &&
      /^\d{4}-\d{2}-\d{2}$/.test(reviewBy) && !isNaN(new Date(reviewBy).getTime()) &&
      reason.length > 0;
    if (!valid) {
      invalid++;
      continue;
    }
    if (reviewBy < today()) {
      expired++;
      continue;
    }
    const entry = {
      rule: rule,
      file: file,
      line_sha256: hash,
      reason: reason,
      review_by: reviewBy,
      added_by: String(raw.added_by || ''),
      added_at: String(raw.added_at || ''),
    };
    entries.push(entry);
    map.set(rule + '\0' + file + '\0' + hash, entry);
  }
  if (invalid) warnings.push('扫描策略有 ' + invalid + ' 条无效条目，已 fail-closed 忽略。');
  if (expired) warnings.push('扫描策略有 ' + expired + ' 条已过期，已恢复为命中。');
  return { path: pathname, entries: entries, map: map, invalid: invalid, expired: expired, used: new Set(), warnings: warnings };
}
function isSafeRelPath(rel) {
  const value = String(rel || '');
  if (!value || value.indexOf('\u0000') !== -1) return false;
  if (path.isAbsolute(value)) return false;
  const norm = path.normalize(value);
  if (norm === '..' || norm.indexOf('..' + path.sep) === 0 || norm.indexOf('/') === 0) return false;
  return true;
}
// 命中片段一律做凭证打码：规则本身命中的密钥不会出现在报告里，同一行里的其它密钥也不会被顺带泄露。
function scrubSecrets(line) {
  let out = String(line);
  for (const rule of MEMORY_SCAN_RULES) {
    if (!rule.mask) continue;
    const re = new RegExp(rule.re.source, rule.re.flags.indexOf('g') === -1 ? rule.re.flags + 'g' : rule.re.flags);
    out = out.replace(re, '[已打码]');
  }
  return out;
}
function scanTargetFiles(root) {
  // 递归扫记忆库内的 .md / .md.enc（含 facts、private、.archive、distills、profile）；
  // 跳过 .git / node_modules / 隔离目录本身，避免把隔离副本再扫一遍。
  const skip = ['.git', 'node_modules', SCAN_QUARANTINE_DIR];
  const out = [];
  (function walk(dir) {
    if (out.length >= SCAN_MAX_FILES) return;
    let names;
    try { names = fs.readdirSync(dir, { withFileTypes: true }); } catch (e) { return; }
    for (const item of names) {
      const fp = path.join(dir, item.name);
      if (item.isDirectory()) {
        if (skip.indexOf(item.name) !== -1) continue;
        walk(fp);
        continue;
      }
      if (!item.isFile()) continue;
      if (!MEMORY_FILE_RE.test(item.name)) continue;
      out.push(fp);
      if (out.length >= SCAN_MAX_FILES) return;
    }
  })(root);
  return Array.from(new Set(out)).sort();
}
function scanQuarantineCore(root, findings) {
  if (!findings.length) return { error: false, batch: '', files: 0, lines: 0, text: '没有命中项，无需隔离。' };
  const batch = 'scan-' + Date.now() + '-' + crypto.randomBytes(2).toString('hex');
  const batchDir = path.join(root, SCAN_QUARANTINE_DIR, 'quarantine', batch);
  const byFile = new Map();
  for (const finding of findings) {
    if (!byFile.has(finding.file)) byFile.set(finding.file, []);
    byFile.get(finding.file).push(finding);
  }
  const manifest = { version: 1, batch: batch, created: new Date().toISOString(), root: root, restored: false, files: [] };
  let lineCount = 0;
  for (const rel of Array.from(byFile.keys()).sort()) {
    if (!isSafeRelPath(rel)) return { error: true, text: '拒绝隔离: 非法相对路径 ' + rel };
    const src = path.join(root, rel);
    if (!fs.existsSync(src)) continue;
    const backup = path.join(batchDir, rel);
    fs.mkdirSync(path.dirname(backup), { recursive: true });
    fs.copyFileSync(src, backup);
    const lineMap = new Map();
    for (const hit of byFile.get(rel)) if (!lineMap.has(hit.line)) lineMap.set(hit.line, hit);
    const lines = fs.readFileSync(src, 'utf8').split(/\r?\n/);
    for (const lineNo of Array.from(lineMap.keys()).sort(function (a, b) { return a - b; })) {
      if (lineNo < 1 || lineNo > lines.length) continue;
      lines[lineNo - 1] = '[已隔离: ' + lineMap.get(lineNo).rule + ' ' + lineMap.get(lineNo).class + ']';
      lineCount++;
    }
    fs.writeFileSync(src, lines.join('\n'), 'utf8');
    manifest.files.push({
      file: rel,
      lines: Array.from(lineMap.keys()).sort(function (a, b) { return a - b; }),
      rules: Array.from(new Set(byFile.get(rel).map(function (h) { return h.rule; }))),
    });
  }
  fs.writeFileSync(path.join(batchDir, 'manifest.json'), JSON.stringify(manifest, null, 2), 'utf8');
  return {
    error: false,
    batch: batch,
    files: manifest.files.length,
    lines: lineCount,
    text: '已隔离 ' + lineCount + ' 行（' + manifest.files.length + ' 个文件）到 ' + path.join(SCAN_QUARANTINE_DIR, 'quarantine', batch) + '；原文件命中行已替换为占位符，可用 scan --restore 还原。',
  };
}
function scanRestoreCore(root, opts) {
  const base = path.join(root, SCAN_QUARANTINE_DIR, 'quarantine');
  const report = { schemaVersion: SCAN_SCHEMA_VERSION, error: true, exitCode: 2, ok: false, level: 'safe', root: root, findings: [], summary: scanEmptySummary() };
  if (!fs.existsSync(base)) return Object.assign(report, { text: '没有可还原的隔离批次: ' + base + '。' });
  const wanted = opts && opts.id ? String(opts.id) : '';
  const batches = fs.readdirSync(base).filter(function (name) {
    return fs.existsSync(path.join(base, name, 'manifest.json'));
  }).sort();
  const chosen = wanted
    ? (batches.indexOf(wanted) === -1 ? null : wanted)
    : (batches.length ? batches[batches.length - 1] : null);
  if (!chosen) return Object.assign(report, { text: wanted ? ('找不到隔离批次: ' + wanted + '。') : '没有可还原的隔离批次。' });
  const batchDir = path.join(base, chosen);
  let manifest = null;
  try {
    manifest = JSON.parse(fs.readFileSync(path.join(batchDir, 'manifest.json'), 'utf8'));
  } catch (error) {
    return Object.assign(report, { text: '隔离批次 manifest 无法解析: ' + chosen + '（' + (error && error.message ? error.message : String(error)) + '）' });
  }
  if (manifest && manifest.restored) {
    return Object.assign(report, { text: '隔离批次 ' + chosen + ' 已还原过，不会重复还原。' });
  }
  let restored = 0;
  for (const item of (manifest && manifest.files) || []) {
    if (!isSafeRelPath(item.file)) return Object.assign(report, { text: '拒绝还原: 非法相对路径 ' + item.file });
    const backup = path.join(batchDir, item.file);
    if (!fs.existsSync(backup)) continue;
    const target = path.join(root, item.file);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.copyFileSync(backup, target);
    restored++;
  }
  manifest.restored = true;
  manifest.restored_at = new Date().toISOString();
  fs.writeFileSync(path.join(batchDir, 'manifest.json'), JSON.stringify(manifest, null, 2), 'utf8');
  return {
    schemaVersion: SCAN_SCHEMA_VERSION,
    error: false,
    exitCode: 0,
    ok: true,
    level: 'safe',
    root: root,
    batch: chosen,
    files: restored,
    findings: [],
    summary: scanEmptySummary(),
    text: '已还原 ' + restored + ' 个文件（批次 ' + chosen + '）。',
  };
}
function renderScanText(report) {
  const label = { safe: '安全', low: '低危', medium: '中危', high: '高危', critical: '严重' };
  const lines = [
    '# 元忆记忆库安全扫描（scan）',
    '',
    '- 扫描路径: ' + report.root,
    '- 扫描文件: ' + report.summary.files + '（加密跳过 ' + report.summary.encrypted + (report.summary.mislabelled ? '；.enc 后缀但内容是明文 ' + report.summary.mislabelled + ' 个已按文本扫描' : '') + '）',
    '- 结果: ' + label[report.level] + ' · 命中 ' + report.summary.hits + ' 条'
      + (report.summary.suppressed ? ' · 已抑制 ' + report.summary.suppressed + ' 条' : '')
      + (report.summary.truncated ? '（已达上限，结果被截断）' : ''),
    '- 分级: ' + SCAN_SEVERITIES.map(function (s) { return s + '=' + report.summary.bySeverity[s]; }).join(' / '),
    '- 类别: ' + SCAN_CLASSES.map(function (c) { return c + '=' + report.summary.byClass[c]; }).join(' / '),
  ];
  if (report.policy && (report.policy.invalid || report.policy.expired || report.policy.unused)) {
    lines.push('- 策略: 无效 ' + report.policy.invalid + ' / 过期 ' + report.policy.expired + ' / 未命中 ' + report.policy.unused);
  }
  for (const warning of (report.policy && report.policy.warnings) || []) lines.push('- [策略警告] ' + warning);
  if (report.gate) lines.push('- 门禁: 命中 ' + report.gate + ' 及以上即 exit 1（当前 ' + report.level + '）');
  if (!report.findings.length) lines.push('- 未发现可疑内容。');
  for (const finding of report.findings) {
    lines.push('- [' + label[finding.severity] + '] ' + finding.evidence + ' ' + finding.rule + ' ' + finding.title + '（' + finding.class + ' / ' + finding.ref + '）');
    lines.push('  片段: ' + finding.snippet);
  }
  if (report.quarantine) {
    lines.push('');
    lines.push(report.quarantine.text);
  }
  if (report.restore) {
    lines.push('');
    lines.push(report.restore.text);
  }
  return lines.join('\n');
}
function scanCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.path || opts.root || userRoot());
  const gateRaw = Array.isArray(opts.gate) ? opts.gate[opts.gate.length - 1] : opts.gate;
  let gate = '';
  if (gateRaw !== undefined && gateRaw !== null && String(gateRaw) !== '') {
    gate = String(gateRaw).trim().toLowerCase();
    if (SCAN_SEVERITIES.indexOf(gate) === -1) {
      const bad = Object.assign({ schemaVersion: SCAN_SCHEMA_VERSION, error: true, exitCode: 2, ok: false, level: 'safe', root: root, findings: [], summary: scanEmptySummary() }, {});
      bad.text = '安全级别不支持: ' + gateRaw + '。门禁可选安全级别: safe / low / medium / high / critical（例如 --gate high）。';
      return bad;
    }
  }
  if (!fs.existsSync(root)) {
    const missing = Object.assign({ schemaVersion: SCAN_SCHEMA_VERSION, error: true, exitCode: 2, ok: false, level: 'safe', root: root, findings: [], summary: scanEmptySummary() }, {});
    missing.text = '扫描路径不存在: ' + root + '。请检查 --path 指向的记忆库目录。';
    return missing;
  }
  if (opts.restore) return scanRestoreCore(root, opts);

  const findings = [];
  const suppressed = [];
  const policy = loadScanPolicy(root, opts.noPolicy);
  const byClass = {};
  for (const cls of SCAN_CLASSES) byClass[cls] = 0;
  const bySeverity = {};
  for (const sev of SCAN_SEVERITIES) bySeverity[sev] = 0;
  let files = 0;
  let encrypted = 0;
  let mislabelled = 0;
  let truncated = false;
  for (const fp of scanTargetFiles(root)) {
    files++;
    if (isEncFile(fp)) {
      // 历史恢复残留：.enc 后缀但内容其实是明文（缺 YTMENC1 头）→ 按文本继续扫，否则等于漏扫。
      let head = Buffer.alloc(0);
      try { head = fs.readFileSync(fp).slice(0, ENC_MAGIC.length); } catch (error) { encrypted++; continue; }
      if (head.toString('utf8') !== ENC_MAGIC) mislabelled++;
      else { encrypted++; continue; }
    }
    let text = '';
    try { text = fs.readFileSync(fp, 'utf8'); } catch (error) { continue; }
    const rel = relOf(root, fp);
    const lines = text.split(/\r?\n/);
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (!line.trim()) continue;
      for (const rule of MEMORY_SCAN_RULES) {
        rule.re.lastIndex = 0;
        const match = rule.re.exec(line);
        if (!match) continue;
        if (findings.length >= SCAN_MAX_FINDINGS) { truncated = true; break; }
        // 片段给命中位置前后各 40 字符（不是行首），否则长行会看起来「没有命中内容」。
        const start = Math.max(0, match.index - 40);
        const end = Math.min(line.length, match.index + match[0].length + 40);
        const snippet = scrubSecrets((start > 0 ? '…' : '') + line.slice(start, end) + (end < line.length ? '…' : '')).slice(0, 200);
        const lineHash = scanLineHash(line);
        const policyKey = rule.id + '\0' + rel + '\0' + lineHash;
        if (policy.map.has(policyKey)) {
          const exception = policy.map.get(policyKey);
          policy.used.add(policyKey);
          suppressed.push({
            file: rel,
            line: i + 1,
            evidence: rel + ':' + (i + 1),
            rule: rule.id,
            class: rule.class,
            severity: rule.severity,
            title: rule.title,
            line_sha256: lineHash,
            reason: exception.reason,
            review_by: exception.review_by,
          });
          continue;
        }
        findings.push({
          file: rel,
          line: i + 1,
          evidence: rel + ':' + (i + 1),
          rule: rule.id,
          class: rule.class,
          severity: rule.severity,
          title: rule.title,
          ref: rule.ref,
          line_sha256: lineHash,
          match: scrubSecrets(match[0]).slice(0, 80),
          snippet: snippet,
        });
        byClass[rule.class]++;
        bySeverity[rule.severity]++;
      }
      if (truncated) break;
    }
    if (truncated) break;
  }
  const hitSeverities = SCAN_SEVERITIES.filter(function (sev) { return bySeverity[sev] > 0; });
  const level = hitSeverities.length ? hitSeverities[hitSeverities.length - 1] : 'safe';
  const summary = {
    files: files,
    encrypted: encrypted,
    mislabelled: mislabelled,
    scanned: files - encrypted,
    hits: findings.length,
    byClass: byClass,
    bySeverity: bySeverity,
    maxSeverity: level,
    truncated: truncated,
    suppressed: suppressed.length,
    invalid_policy: policy.invalid,
    expired_policy: policy.expired,
  };
  const report = {
    schemaVersion: SCAN_SCHEMA_VERSION,
    error: false,
    exitCode: 0,
    ok: level === 'safe',
    level: level,
    root: root,
    gate: gate,
    findings: findings,
    suppressed: suppressed,
    summary: summary,
    policy: {
      path: policy.path,
      entries: policy.entries.length,
      invalid: policy.invalid,
      expired: policy.expired,
      unused: Math.max(0, policy.entries.length - policy.used.size),
      warnings: policy.warnings,
    },
    quarantine: null,
    restore: null,
  };
  if (opts.quarantine) {
    if (!opts.yes) {
      report.error = true;
      report.exitCode = 2;
      report.text = '拒绝: --quarantine 会改写记忆文件，需要显式确认。确认后重试：yotta-memory scan --quarantine --yes；未确认时不会改动任何文件。';
      return report;
    }
    const quarantined = scanQuarantineCore(root, findings);
    if (quarantined.error) {
      report.error = true;
      report.exitCode = 2;
      report.text = quarantined.text;
      return report;
    }
    report.quarantine = quarantined;
  }
  report.text = renderScanText(report);
  if (gate) {
    const gateRank = scanSeverityRank(gate);
    const levelRank = scanSeverityRank(level);
    const failed = gate === 'safe' ? level !== 'safe' : levelRank >= gateRank;
    if (failed) report.exitCode = 1;
  }
  return report;
}
function scanPolicyCandidatesCore(opts) {
  opts = opts || {};
  const root = path.resolve(opts.path || opts.root || userRoot());
  const scan = scanCore({
    root: root,
    noPolicy: true,
    quarantine: false,
    restore: false,
    gate: '',
  });
  if (scan.error) return scan;
  const seen = new Set();
  const candidates = [];
  for (const finding of scan.findings) {
    const key = finding.rule + '\0' + finding.file + '\0' + finding.line_sha256;
    if (seen.has(key)) continue;
    seen.add(key);
    candidates.push({
      rule: finding.rule,
      file: finding.file,
      line: finding.line,
      line_sha256: finding.line_sha256,
      class: finding.class,
      severity: finding.severity,
      title: finding.title,
      reason: '',
      review_by: '',
      added_by: '',
      added_at: '',
    });
  }
  let outPath = '';
  if (opts.out) {
    const rel = String(opts.out).replace(/\\/g, '/');
    if (!layoutInsideRoot(root, rel)) {
      return {
        schemaVersion: SCAN_SCHEMA_VERSION,
        error: true,
        exitCode: 2,
        candidates: [],
        text: '拒绝写出策略候选：--out 必须位于当前记忆库内。',
      };
    }
    outPath = path.resolve(root, rel);
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    atomicWriteFileSync(outPath, JSON.stringify({ version: 1, candidates: candidates }, null, 2), 'utf8');
  }
  return {
    schemaVersion: SCAN_SCHEMA_VERSION,
    error: false,
    exitCode: 0,
    root: root,
    candidates: candidates,
    out: outPath,
    text: '扫描策略候选: ' + candidates.length + ' 条'
      + (outPath ? '\n已写出: ' + outPath : '\n未写文件；请人工复核后配置 security/scan-policy.json。'),
  };
}
// 交互确认：非 TTY 一律返回 null（由调用方给 --yes 指引），避免自动化里静默改写记忆。
function promptYesNo(promptText) {
  return new Promise(function (resolve) {
    const stdin = process.stdin;
    if (!stdin.isTTY) { resolve(null); return; }
    process.stdout.write(promptText + ' [y/N] ');
    let buf = '';
    function done(abort) {
      try { stdin.setRawMode(false); } catch (e) {}
      stdin.pause();
      stdin.removeListener('data', onData);
      process.stdout.write('\n');
      resolve(abort ? null : /^y(es)?$/i.test(buf.trim()));
    }
    function onData(chunk) {
      const s = String(chunk);
      for (const c of s) {
        if (c === '\r' || c === '\n') { done(false); return; }
        if (c === '\u0003') { done(true); return; }
        if (c === '\u007f' || c === '\b') buf = buf.slice(0, -1);
        else buf += c;
      }
    }
    try { stdin.setRawMode(true); } catch (e) { resolve(null); return; }
    stdin.resume();
    stdin.setEncoding('utf8');
    stdin.on('data', onData);
  });
}
async function cmdScan(opts) {
  opts = opts || {};
  if (opts.policyCandidates) {
    const candidates = scanPolicyCandidatesCore(opts);
    console.log(opts.json ? JSON.stringify(candidates, null, 2) : candidates.text);
    if (candidates.error) process.exit(candidates.exitCode || 2);
    return;
  }
  if (opts.quarantine && !opts.yes) {
    const preview = scanCore(Object.assign({}, opts, { quarantine: false }));
    if (preview.error) {
      console.log(opts.json ? JSON.stringify(preview, null, 2) : preview.text);
      process.exit(2);
    }
    const answer = await promptYesNo('即将隔离 ' + preview.summary.hits + ' 处命中（原文件先备份到 ' + SCAN_QUARANTINE_DIR + '/quarantine）');
    if (answer !== true) {
      console.log('已取消：未确认时不会改动记忆文件。确认后请重试：yotta-memory scan --quarantine --yes');
      process.exit(2);
    }
    opts = Object.assign({}, opts, { yes: true });
  }
  const r = scanCore(opts);
  console.log(opts.json ? JSON.stringify(r, null, 2) : r.text);
  if (r.error) process.exit(r.exitCode || 2);
  if (r.exitCode) process.exit(r.exitCode);
}

// ---- config 命令 ----
// v0.10.0：maintain_* / consolidate_* 数值键纳入 config set/get（此前只支持 3 个键但文档已写可调）
function isNumericConfigKey(key) { return /^(maintain_|consolidate_|scale_|backup_max_age_hours$|usage_retention_days$|usage_query_slots$|capacity_|promotion_|context_audit_min_coverage$|context_commits_limit$)/.test(key); }
// v0.17.0 B2：doctor 规模体检阈值键（0 表示只要超过 0 就告警，便于压测与演练）
const SCALE_CONFIG_KEYS = ['scale_warn_entries', 'scale_warn_files_per_dir', 'scale_warn_index_bytes', 'scale_warn_cold_start_ms', 'scale_info_entries', 'scale_info_files_per_dir', 'scale_info_index_bytes', 'scale_info_cold_start_ms', 'scale_warn_long_statements', 'scale_info_long_statements', 'scale_warn_type_count', 'scale_info_type_count'];
// v0.18.1 验收修正：config set / get 共用一份键列表，新增配置键不会再出现「读端认、写端拒」。
const CONFIG_VALUE_KEYS = ['memory_home', 'backup_dir', 'backup_enabled', 'backup_schedule', 'backup_time', 'backup_max_age_hours', 'backup_setup_choice', 'embedding_cmd', 'embedding_timeout', 'maintain_archived_utility', 'maintain_archived_age', 'maintain_forget_utility', 'maintain_forget_age', 'maintain_decay_halflife_FACT', 'maintain_decay_halflife_PREF', 'maintain_decay_halflife_COMMIT', 'maintain_rule_min_hits', 'consolidate_min_age', 'consolidate_min_idle', 'consolidate_max_utility', 'consolidate_min_group', 'consolidate_period', 'usage_enabled', 'usage_retention_days', 'usage_query_slots', 'capacity_cooldown_days', 'capacity_warn_bytes', 'capacity_candidate_limit', 'promotion_min_hits', 'promotion_min_queries', 'context_commits_limit', 'context_audit_min_coverage'].concat(SCALE_CONFIG_KEYS);
// v0.22.7：配置键逐键人话说明（管理台「高级 / CLI」页与官网 /product/ 共用；必须与 CONFIG_VALUE_KEYS 一一对应）
const CONFIG_KEY_HELP = {
  memory_home: { what: '记忆库根目录：所有记忆文件、索引都放在这个文件夹里。改它 = 换一个记忆库，原库内容不会自动搬过去。', when: '默认 ~/.yottamemory。优先级：环境变量 YOTTA_MEMORY_HOME > 本键 > 默认。把库换到数据盘 / 移动盘时改这里，改完用 config get 复查。' },
  backup_dir: { what: '自动备份的存放目录：每日备份会把整个记忆库打包写到这里。', when: '未配置 = 不启用自动备份。建议选独立硬盘（别和记忆库同一块盘）；由 backup setup 引导写入。' },
  backup_enabled: { what: '每日自动备份的总开关：true 按计划自动备份，false 只有手动 backup create 才备份。', when: '默认关闭。backup setup 选每日备份时自动置 true，选手动模式置 false。可随时手动改。' },
  backup_schedule: { what: '备份计划模式：daily = 每天定时自动备份；manual = 不注册系统定时器，只手动备份。', when: '默认 manual。一般由 backup setup 写入，不需要手改。' },
  backup_time: { what: '每天自动备份的执行时间（24 小时制，HH:MM）。', when: '由 backup setup --time 写入，例如 03:30。想换时间可重跑 backup setup 或直接改本键。' },
  backup_max_age_hours: { what: '备份“新鲜度”阈值：最近一次成功备份超过这么多小时，doctor 和概览就会提醒备份过期。', when: '默认 36 小时。每天备份保持 36 即可；每周才备份一次可调成 200。' },
  backup_setup_choice: { what: '备份配置向导的选择记录：上次选的是每日备份（daily）还是手动模式（manual）。', when: '默认 manual；选 manual 后 doctor 不再提醒“未配置备份”。一般由 backup setup 自动写入。' },
  embedding_cmd: { what: '本地语义检索（embedding）插件命令：配置后，搜索会额外按“意思相近”找记忆，而不只是按字面词匹配。', when: '可选，默认关闭。命令只在本机执行、不联网上传；需要自备插件程序。示例：python embed.py' },
  embedding_timeout: { what: 'embedding 插件的调用超时：超时就不等它，自动退回普通关键词检索。', when: '毫秒，默认 3000（3 秒）。插件较慢（如本地大模型）可调大，例如 15000。' },
  maintain_archived_utility: { what: '归档门槛之一：效用分（越高越有价值）低于这个值的旧记忆，才可能被 archive 归档。', when: '默认 0.55（v0.23.0 起与效用分地板对齐——记忆写出来就有约 0.42~0.47 的底分，门槛低于它会永远打不到）。调低 = 更难归档（更保守），调高 = 更容易归档。改完可用 maintain 预览候选。' },
  maintain_archived_age: { what: '归档门槛之一：只有保存超过这么多天的旧记忆，才可能被归档。', when: '默认 180 天。想保守可调大（如 365），想积极瘦身可调小。' },
  maintain_forget_utility: { what: '遗忘（彻底删除）门槛之一：效用分低于这个值的记忆才可能进入遗忘候选，比归档更严格。', when: '默认 0.12，建议保持很低；误删不可恢复（只能靠备份）。' },
  maintain_forget_age: { what: '遗忘（彻底删除）门槛之一：只有保存超过这么多天的记忆才可能进入遗忘候选。', when: '默认 365 天。' },
  maintain_decay_halflife_FACT: { what: 'FACT（公共事实）记忆的半衰期：每过这么久，它的“时效分”衰减一半，越老权重越低。', when: '天，默认 730（约两年）。调大 = 老事实保持更久权重；调小 = 更快“褪色”。' },
  maintain_decay_halflife_PREF: { what: 'PREF（个人偏好）记忆的半衰期：每过这么久，时效分衰减一半。', when: '天，默认 365（一年）。' },
  maintain_decay_halflife_COMMIT: { what: 'COMMIT（承诺 / 任务）记忆的半衰期，这类记忆过期最快。', when: '天，默认 90（三个月）。BOUND（边界铁律）固定不衰减，没有对应配置键。' },
  maintain_rule_min_hits: { what: '“重复踩坑 → 升级成规则”的建议门槛：同类教训出现达到这么多条，maintain --rules 才建议固化成 BOUND 规则。', when: '默认 3、最低 2。只出建议、不自动写规则。' },
  consolidate_min_age: { what: '记忆压缩（consolidate：把多条旧记忆合并成周期摘要）候选门槛：保存超过这么多天才可能被压缩。', when: '默认 180 天。想暂停压缩可调到很大，例如 99999。' },
  consolidate_min_idle: { what: '压缩候选门槛：超过这么多天没被用过的记忆才可能被压缩，近期还在用的不动。', when: '默认 90 天。' },
  consolidate_max_utility: { what: '压缩候选门槛：效用分高于这个值的记忆不动（还有价值的保留原文）。', when: '默认 0.6。调低 = 更保守，只压缩更“没用”的。' },
  consolidate_min_group: { what: '压缩成组的最少条数：同一主题至少这么多条，才会合并成一条摘要。', when: '默认 2；单条不成组。' },
  consolidate_period: { what: '周期摘要的时间窗口：生成的摘要按这个天数分期（例如 90 天一期）。', when: '天，默认 90。' },
  usage_enabled: { what: '命中打点开关：打开后，被搜到的记忆会在自己的文件里记一笔“哪天被用过”（仅本地统计，用于容量清理与晋升建议）。', when: '默认开启；false 关闭。只存本地、不联网、不保存查询原文。' },
  usage_retention_days: { what: '命中打点的保留窗口：超过这么多天的打点记录自动丢弃。', when: '天，默认 90。' },
  usage_query_slots: { what: '每条记忆保留多少个“查询指纹”槽位（只存哈希前 8 位，不保存查询原文）。', when: '默认 12 个。' },
  capacity_cooldown_days: { what: '容量淘汰的冷却期：最近这么多天内被用过的记忆，不会被列为淘汰候选。', when: '天，默认 30。' },
  capacity_warn_bytes: { what: '容量水位告警线：记忆库总字节超过它就提示“容量偏高”。', when: '默认 52428800（50 MB）。maintain --capacity 与 doctor 都按它分级。' },
  capacity_candidate_limit: { what: 'maintain --capacity 一次最多列出多少个淘汰候选。', when: '默认 20。' },
  promotion_min_hits: { what: '晋升建议门槛之一：一条记忆累计被命中至少这么多次，才可能被建议“升级”。', when: '默认 3 次；需与 promotion_min_queries 同时满足。' },
  promotion_min_queries: { what: '晋升建议门槛之一：命中要来自至少这么多个不同查询（防止同一句话反复搜把分数刷上去）。', when: '默认 3 个。' },
  context_commits_limit: { what: '开工上下文包里 COMMIT（承诺 / 收工锚点）段最多展示多少条：超出的旧条目折叠为一行提示，不删除、仍可用 recall 检索。', when: '默认 20；0 = 全部展示（旧行为）。weight ≥ 1.5 或带 pinned / evergreen 标签的条目不受上限影响、始终展示。' },
  context_audit_min_coverage: { what: 'context --audit 的覆盖率闸门：落盘覆盖率低于这个比例时，提示“还有内容没落盘”。', when: '0-1 之间的小数，默认 0.5（即 50%）。' },
  scale_warn_entries: { what: '规模体检（doctor 的“规模”段）：记忆条数超过这个值，升级为 warning 告警。', when: '默认 50000 条。' },
  scale_warn_files_per_dir: { what: '规模体检：单个目录里的文件数超过这个值，升级为 warning。', when: '默认 500 个文件。' },
  scale_warn_index_bytes: { what: '规模体检：索引文件总体积超过这个值，升级为 warning。', when: '默认 5242880 字节（5 MB）。' },
  scale_warn_cold_start_ms: { what: '规模体检：索引冷启动耗时超过这个毫秒数，升级为 warning。', when: '默认 2000 毫秒。' },
  scale_info_entries: { what: '规模体检：记忆条数超过这个值，提示 info（只提醒、不告警）。', when: '默认 30000 条。' },
  scale_info_files_per_dir: { what: '规模体检：单目录文件数超过这个值，提示 info。', when: '默认 300 个文件。' },
  scale_info_index_bytes: { what: '规模体检：索引体积超过这个值，提示 info。', when: '默认 3145728 字节（3 MB）。' },
  scale_info_cold_start_ms: { what: '规模体检：索引冷启动超过这个值，提示 info。', when: '默认 1200 毫秒。' },
  scale_warn_long_statements: { what: '规模体检：超过 2000 字的 statement 条数超过这个值，升级为 warning。', when: '默认 50 条。记忆宜短句高密度，长文建议拆分或另存文档。' },
  scale_info_long_statements: { what: '规模体检：超过 2000 字的 statement 条数超过这个值，提示 info。', when: '默认 10 条。' },
  scale_warn_type_count: { what: '规模体检：单类型（FACT / PREF / BOUND / COMMIT 之一）条数超过这个值，升级为 warning。', when: '默认 500 条。COMMIT 堆积通常意味着收工锚点写太长或该跑 maintain 归档了。' },
  scale_info_type_count: { what: '规模体检：单类型条数超过这个值，提示 info。', when: '默认 200 条。' },
};
function cmdConfigSet(key, value) {
  const known = CONFIG_VALUE_KEYS;
  if (known.indexOf(key) === -1) { console.error('未知配置项: ' + key + '（可用: memory_home / backup_dir / embedding_cmd / embedding_timeout / maintain_* / consolidate_* / scale_* / usage_* / capacity_* / promotion_*）'); process.exit(2); }
  if (value === undefined || value === null || value === '') { console.error('缺少值: config set ' + key + ' <值>'); process.exit(2); }
  const cfg = loadConfig();
  if (key === 'memory_home') cfg.memory_home = value;
  else if (key === 'backup_dir') cfg.backup_dir = value;
  else if (key === 'backup_enabled') cfg.backup_enabled = value !== 'false' && value !== '0';
  else if (key === 'usage_enabled') cfg.usage_enabled = value !== 'false' && value !== '0';
  else if (key === 'backup_schedule' || key === 'backup_time' || key === 'backup_setup_choice') cfg[key] = value;
  else if (key === 'embedding_cmd') cfg.embedding_cmd = value;
  else if (key === 'embedding_timeout') cfg.embedding_timeout = parseInt(value, 10) || 3000;
  else if (isNumericConfigKey(key)) {
    const n = parseFloat(value);
    if (!(n >= 0)) { console.error('配置项 ' + key + ' 需要非负数值'); process.exit(2); }
    cfg[key] = n;
  }
  saveConfig(cfg);
  console.log('已写入配置: ' + key + ' = ' + (key === 'memory_home' || key === 'backup_dir' || key === 'embedding_cmd' ? value : cfg[key]));
}
function cmdConfigGet(opts) {
  const cfg = loadConfig();
  if (opts && opts.json) {
    console.log(JSON.stringify(Object.assign({}, cfg, {
      effective_memory_home: userRoot(),
      identity: identityDiagnostic(resolveIdentity(opts)),
    }), null, 2));
    return;
  }
  console.log('memory_home: ' + (cfg.memory_home || '(未设置，默认 ~/.yottamemory)'));
  console.log('backup_dir: ' + (cfg.backup_dir || '(未设置)'));
  console.log('backup_enabled: ' + (cfg.backup_enabled === undefined ? '(未设置)' : cfg.backup_enabled));
  console.log('backup_schedule: ' + (cfg.backup_schedule || '(未设置)'));
  console.log('backup_time: ' + (cfg.backup_time || '(未设置)'));
  console.log('usage_enabled: ' + (cfg.usage_enabled === undefined ? '(默认 true)' : cfg.usage_enabled));
  console.log('embedding_cmd: ' + (cfg.embedding_cmd || '(未设置)'));
  console.log('embedding_timeout: ' + (cfg.embedding_timeout || 3000));
  const keys = CONFIG_VALUE_KEYS;
  for (const k of keys) {
    if (k === 'memory_home' || k === 'backup_dir' || k === 'backup_enabled' || k === 'backup_schedule' || k === 'backup_time' || k === 'embedding_cmd' || k === 'embedding_timeout' || k === 'usage_enabled') continue;
    if (cfg[k] !== undefined) console.log(k + ': ' + cfg[k]);
  }
  console.log('当前生效用户级位置: ' + userRoot());
  if (cfg.serve && Object.keys(cfg.serve).length) console.log('serve: ' + JSON.stringify(cfg.serve));
}

// ---- MCP serve（局域网 streamable HTTP 记忆引擎，零依赖）----
const MCP_CORE_TOOL_NAMES = ['context', 'recall', 'search', 'remember'];
function normalizeMcpToolProfile(profile) {
  return String(profile || 'full').trim().toLowerCase() === 'core' ? 'core' : 'full';
}
function mcpTools(profile) {
  const tools = [
    { name: 'remember', description: '写入一条记忆。参数 type(FACT/PREF/BOUND/COMMIT)、subject、statement 必填；owner 可选，默认当前智能体', inputSchema: { type: 'object', properties: { type: { type: 'string', description: 'FACT/PREF/BOUND/COMMIT' }, subject: { type: 'string' }, statement: { type: 'string' }, owner: { type: 'string' } }, required: ['type', 'subject', 'statement'] } },
    { name: 'recall', description: '检索记忆。query 可选；type 可选；limit 可选（默认 20）；explain 可选。只返回当前智能体可读记忆；embedding 插件只能由本机 config 配置，远端不可传命令', inputSchema: { type: 'object', properties: { query: { type: 'string' }, type: { type: 'string' }, limit: { type: 'number' }, embeddingTimeout: { type: 'number' }, explain: { type: 'boolean' } } } },
    { name: 'search', description: '检索记忆（同 recall）。query 可选；type 可选；limit 可选（默认 20）；explain 可选；embedding 插件只能由本机 config 配置，远端不可传命令', inputSchema: { type: 'object', properties: { query: { type: 'string' }, type: { type: 'string' }, limit: { type: 'number' }, embeddingTimeout: { type: 'number' }, explain: { type: 'boolean' } } } },
    { name: 'context', description: '生成开工上下文包。focus 可选；limit 可选；budget 可选；explain 可选；audit=true 时改为上下文压缩审计（用 auditText 传待审计文本，只读），gate 控制未落盘条数门槛；embedding 插件只能由本机 config 配置，远端不可传命令', inputSchema: { type: 'object', properties: { focus: { type: 'string' }, limit: { type: 'number' }, budget: { type: 'number' }, explain: { type: 'boolean' }, embeddingTimeout: { type: 'number' }, audit: { type: 'boolean' }, auditText: { type: 'string' }, gate: { type: 'number' } } } },
    { name: 'doctor', description: '开工可靠性检查：检查记忆库根目录、密钥库、索引、身份登记与最近备份；只读，不会修改记忆', inputSchema: { type: 'object', properties: {} } },
    { name: 'forget', description: '删除一条记忆。file 为记忆文件路径（如 facts/2026-08-24-0001.md 或文件名）', inputSchema: { type: 'object', properties: { file: { type: 'string' } }, required: ['file'] } },
    { name: 'archive', description: '归档旧记忆。days 默认 180；threshold 默认 0.4；dryRun=true 只预览、不落盘。破坏性覆盖 --force 仅本机 CLI 提供（MCP 不接受）', inputSchema: { type: 'object', properties: { days: { type: 'number' }, threshold: { type: 'number' }, dryRun: { type: 'boolean' } } } },
    { name: 'reindex', description: '重建索引（手动改 .md 后校正；扫描 facts/prefs/bounds/commits 四目录）', inputSchema: { type: 'object', properties: {} } },
    { name: 'export', description: '导出全部记忆到记忆库内的 JSON 文件。out 可选（默认 <记忆库>/yottamemory-export-<日期>.json；仅限记忆库内路径）', inputSchema: { type: 'object', properties: { out: { type: 'string' } } } },
    { name: 'import', description: '从记忆库内的 JSON 文件导入记忆。src 为文件路径（相对记忆库目录，或记忆库内绝对路径；仅限记忆库内）', inputSchema: { type: 'object', properties: { src: { type: 'string' } }, required: ['src'] } },
    { name: 'agent_info', description: '查看当前智能体身份与登记状态（HTTP 读经 token 校验的 X-Agent-Id；stdio 读 --agent-id 显式参数）。开工先确认「我是谁」，禁止从记忆里抄别人的 ID', inputSchema: { type: 'object', properties: {} } },
    { name: 'profile', description: '生成当前智能体的用户画像（只读聚合 private/<owner>/ 下 PREF/BOUND/COMMIT 原文，零推断，写入 private/<owner>/profile.md）。owner 默认当前智能体', inputSchema: { type: 'object', properties: { owner: { type: 'string' } } } },
    { name: 'feedback', description: '显式使用反馈（自我学习）：useful/useless 调整记忆 weight/confidence/feedback_net。file 为记忆文件路径或文件名', inputSchema: { type: 'object', properties: { file: { type: 'string' }, useful: { type: 'boolean' }, useless: { type: 'boolean' }, reason: { type: 'string' } }, required: ['file'] } },
    { name: 'maintain', description: '记忆自组织（自我进化）：规则层归档/遗忘/去重预览。默认 dry-run；apply 才执行，purge 才真删；capacity=true 改为只读容量水位报告；rules=true 改为只读规则晋升建议', inputSchema: { type: 'object', properties: { apply: { type: 'boolean' }, purge: { type: 'boolean' }, dedup: { type: 'boolean' }, capacity: { type: 'boolean' }, rules: { type: 'boolean' }, limit: { type: 'number' }, threshold: { type: 'number' }, age: { type: 'number' } } } },
    { name: 'consolidate', description: '周期摘要压缩候选报告（只读 propose 模式）。MCP 不提供 --apply / --undo / --batches；执行与回滚请在本机 CLI 由用户确认后运行', inputSchema: { type: 'object', properties: { minAge: { type: 'number' }, minIdle: { type: 'number' }, maxUtility: { type: 'number' }, minGroup: { type: 'number' }, period: { type: 'number' }, type: { type: 'string' } } } },
    { name: 'distill', description: '心理日志蒸馏（自我提升）：统计摘要/主题画像/知识地图。owner 默认当前智能体（MCP 不支持 --model 外部命令）', inputSchema: { type: 'object', properties: { owner: { type: 'string' }, subject: { type: 'string' } } } },
    { name: 'explain', description: '解释单条记忆效用分项（为什么靠前/归档/遗忘）。file 为记忆文件路径或文件名', inputSchema: { type: 'object', properties: { file: { type: 'string' } }, required: ['file'] } },
  ];
  if (normalizeMcpToolProfile(profile) !== 'core') return tools;
  return MCP_CORE_TOOL_NAMES
    .map((name) => tools.find((tool) => tool.name === name))
    .filter(Boolean);
}
function callTool(name, args, ctx) {
  return runWithIdentity({
    id: ctx && ctx.agent,
    agentKey: ctx && ctx.agentKey,
  }, function () {
    return callToolInner(name, args, ctx);
  });
}
function callToolInner(name, args, ctx) {
  const agent = (ctx && ctx.agent) || '';
  const toolProfile = normalizeMcpToolProfile(ctx && ctx.toolProfile);
  if (toolProfile === 'core' && MCP_CORE_TOOL_NAMES.indexOf(name) === -1) {
    return { text: '工具 ' + name + ' 属于 full 分组，当前 MCP 以 core 模式启动。需要完整工具集时请使用 --tools full 重新启动。', error: true };
  }
  if (agent && !isSafeAgentId(agent)) return { text: '非法 agent ID：只允许单段名称，禁止 /、\\、.. 和控制字符。', error: true };
  try {
    if (name === 'remember') {
      const ownerArg = args.owner ? String(args.owner) : '';
      if (ownerArg && ownerArg !== agent) return { text: '拒绝: MCP 写入的 owner 必须等于当前智能体身份（' + agent + '），不能写其它智能体私密区。', error: true };
      const r = rememberCore(String(args.type || ''), String(args.subject || ''), String(args.statement || ''), { owner: agent, selfAgent: agent });
      return { text: r.text, error: r.error };
    }
    if (name === 'recall' || name === 'search') {
      const r = recallCore(args.query ? String(args.query) : null, {
        limit: args.limit || 20,
        type: args.type ? String(args.type) : null,
        agent: agent,
        embeddingTimeout: args.embeddingTimeout || 3000,
        explain: !!args.explain
      });
      return { text: r.text, error: r.error };
    }
    if (name === 'context') {
      if (args.audit) {
        // v0.18.0 A7：MCP 侧只接受内联文本（不接受文件路径，避免把 --from 变成任意文件读取通道），
        // 也不读 stdin（stdio MCP 的 fd 0 是协议流）。
        const auditText = (args.auditText !== undefined && args.auditText !== null) ? String(args.auditText) : '';
        if (!auditText.trim()) {
          return { text: '拒绝: MCP 的 context audit 只接受内联文本（auditText）。审计本地文件或标准输入请在本机 CLI 运行 yotta-memory context --audit --from <文件|->。', error: true };
        }
        const r = contextAuditCore({ selfAgent: agent, owner: agent, text: auditText, gate: args.gate, noStdin: true });
        return { text: r.text, error: r.error };
      }
      const r = contextCore({
        focus: args.focus ? String(args.focus) : '',
        limit: args.limit || 10,
        budget: args.budget || 0,
        explain: !!args.explain,
        embeddingTimeout: args.embeddingTimeout || 3000,
        selfAgent: agent
      });
      return { text: r.text, error: r.error };
    }
    if (name === 'doctor') {
      const r = doctorCore({ selfAgent: agent });
      return { text: r.text, error: !r.ok };
    }
    if (name === 'forget') {
      const r = forgetCore(String(args.file || ''), { selfAgent: agent });
      return { text: r.text, error: r.error };
    }
    if (name === 'archive') {
      const r = archiveCore({ selfAgent: agent, days: args.days, threshold: args.threshold, dryRun: !!args.dryRun });
      return { text: r.text, error: r.error };
    }
    if (name === 'reindex') {
      const root = userRoot();
      if (!fs.existsSync(root)) return { text: '记忆库不存在。', error: false };
      const cnt = buildIndex(root).length;
      return { text: '已重建索引 ' + root + '（' + cnt + ' 条）', error: false };
    }
    if (name === 'export') {
      const root = userRoot();
      let out = null;
      if (args.out) {
        const safe = resolveWithinRoot(root, String(args.out));
        if (!safe) return { text: '拒绝: MCP 导出路径必须位于记忆库内（' + root + '），已阻止任意路径写入。', error: true };
        out = safe;
      }
      const r = exportCore(root, out);
      return { text: r.text, error: r.error };
    }
    if (name === 'import') {
      const root = userRoot();
      const src = String(args.src || '');
      const safe = resolveWithinRoot(root, src);
      if (!safe) return { text: '拒绝: MCP 导入路径必须位于记忆库内（' + root + '），已阻止任意路径读取。', error: true };
      const r = importCore(root, safe);
      return { text: r.text, error: r.error };
    }
    if (name === 'agent_info') {
      const root = userRoot();
      const id = agent || '';
      if (!id) return { text: '当前未声明智能体身份（无 X-Agent-Id / --agent-id）。stdio 请使用 --agent-id <唯一ID> + --agent-key-file <path>；HTTP 请发送 X-Agent-Id + X-Agent-Key。', error: false };
      const agents = loadAgents(root).agents || {};
      const tokens = loadTokens(root).tokens || {};
      let reg = '未登记';
      if (agents[id]) reg = 'agents.json 已登记（host=' + agents[id].host + '）';
      else if (tokens[id]) reg = 'tokens.json 已登记（远端）';
      const profile = findSelfProfile(root, id);
      let rel = '';
      if (profile) {
        const kv = selfProfileKv(root, id);
        if (kv.agent_name) rel += '\n显示名: ' + kv.agent_name;
        if (kv.user_name) rel += '\n用户: ' + kv.user_name;
        if (kv.relationship) rel += '\n关系: ' + kv.relationship;
      }
      return { text: '当前智能体身份: ' + id + '\n登记状态: ' + reg + '\n自我档案: ' + (profile || '未写入（本地引擎主机执行 yotta-memory iam ' + id + '）') + rel, error: false };
    }
    if (name === 'profile') {
      const ownerArg = args.owner ? String(args.owner) : '';
      const r = profileCore({ owner: ownerArg || agent, selfAgent: agent });
      return { text: r.text, error: r.error };
    }
    if (name === 'feedback') {
      const r = feedbackCore(String(args.file || ''), { selfAgent: agent, useful: !!args.useful, useless: !!args.useless, reason: args.reason ? String(args.reason) : '' });
      return { text: r.text, error: r.error };
    }
    if (name === 'maintain') {
      const r = args.capacity
        ? capacityCore({ selfAgent: agent, limit: args.limit })
        : maintainCore({ selfAgent: agent, apply: !!args.apply, purge: !!args.purge, dedup: !!args.dedup, rules: !!args.rules, threshold: args.threshold, age: args.age });
      return { text: r.text, error: r.error };
    }
    if (name === 'consolidate') {
      // v0.18.0 A5：MCP 只读 propose；apply / undo / batches 留在本机 CLI（由用户确认后执行）。
      if (args.apply || args.undo || args.batches || args.yes) {
        return { text: '拒绝: MCP 的 consolidate 只提供只读 propose 报告；--apply / --undo / --batches 请在本机 CLI 由用户确认后运行（AI 不得代替用户执行 --apply）。', error: true };
      }
      const r = consolidateCore({ selfAgent: agent, apply: false, minAge: args.minAge, minIdle: args.minIdle, maxUtility: args.maxUtility, minGroup: args.minGroup, period: args.period, type: args.type });
      return { text: r.text, error: r.error };
    }
    if (name === 'distill') {
      if (args.model) return { text: '拒绝: MCP 不支持 --model（任意命令执行风险）；请在引擎主机本地 CLI 执行 yotta-memory distill --model <命令>。', error: true };
      const r = distillCore({ selfAgent: agent, owner: args.owner ? String(args.owner) : agent, subject: args.subject ? String(args.subject) : '', model: '' });
      return { text: r.text, error: r.error };
    }
    if (name === 'explain') {
      const r = explainCore(String(args.file || ''), { selfAgent: agent });
      return { text: r.text, error: r.error };
    }
    return { text: '未知工具: ' + name, error: true };
  } catch (e) {
    return { text: '错误: ' + (e && e.message ? e.message : String(e)), error: true };
  }
}
function reqVersion(params) {
  const meta = (params && params._meta) || {};
  return meta['io.modelcontextprotocol/protocolVersion'] || null;
}
function mcpIdentityMode(ctx) {
  const mode = String((ctx && ctx.identityMode) || '').trim().toLowerCase();
  if (mode === 'headers' || mode === 'stdio-args') return mode;
  if (ctx && ctx.agent) return 'stdio-args';
  return 'unknown';
}
function mcpServerInfo(ctx) {
  return {
    name: 'yotta-memory',
    version: VERSION,
    runtimePath: runtimeExecutionPath(),
    identityMode: mcpIdentityMode(ctx),
    toolProfile: normalizeMcpToolProfile(ctx && ctx.toolProfile),
  };
}
function modernOk(payload, ttl, ctx) {
  const out = { resultType: 'complete' };
  Object.assign(out, payload);
  if (ttl) { out.ttlMs = ttl[0]; out.cacheScope = ttl[1]; }
  out._meta = { 'io.modelcontextprotocol/serverInfo': mcpServerInfo(ctx) };
  return out;
}
function unsupportedVersion(id, pv) {
  return { jsonrpc: '2.0', id: id, error: { code: -32022, message: 'Unsupported protocol version', data: { supported: [MCP_PROTOCOL_MODERN], requested: pv } } };
}
function handleMessage(msg, ctx) {
  if (!msg || msg.jsonrpc !== '2.0') return { jsonrpc: '2.0', id: msg && msg.id, error: { code: -32600, message: 'invalid request' } };
  const id = msg.id;
  if (id === undefined || id === null) return null;
  const method = msg.method || '';
  const params = msg.params || {};
  const pv = reqVersion(params);
  if (pv !== null) {
    // ---- modern（2026-07-28 无状态）----
    if (pv !== MCP_PROTOCOL_MODERN) return unsupportedVersion(id, pv);
    const toolProfile = normalizeMcpToolProfile(ctx && ctx.toolProfile);
    if (method === 'server/discover') {
      return { jsonrpc: '2.0', id: id, result: modernOk({
        supportedVersions: [MCP_PROTOCOL_MODERN],
        capabilities: { tools: {} },
        instructions: '元忆 MCP（基于 MCP 最新协议 2026-07-28，向后兼容 2025-11-25 及更早握手）：当前工具分组 ' + toolProfile + '；文件式智能体记忆 remember/recall/search/context/forget/archive/maintain 等读写检索与维护；私密按 owner 物理隔离，数据不出本机。'
      }, [3600000, 'public'], ctx) };
    }
    if (method === 'tools/list') return { jsonrpc: '2.0', id: id, result: modernOk({ tools: mcpTools(toolProfile) }, [300000, 'public'], ctx) };
    if (method === 'tools/call') {
      const out = callTool(params.name || '', params.arguments || {}, ctx);
      return { jsonrpc: '2.0', id: id, result: modernOk({ content: [{ type: 'text', text: out.text }], isError: !!out.error }, null, ctx) };
    }
    if (method === 'initialize') {
      return { jsonrpc: '2.0', id: id, error: { code: -32601, message: "initialize removed in MCP 2026-07-28; use server/discover. supported: ['2026-07-28']" } };
    }
    return { jsonrpc: '2.0', id: id, error: { code: -32601, message: 'Method not found: ' + method } };
  }
  // ---- legacy（<=2025-11-25，initialize 握手；响应保持旧形状）----
  if (method === 'initialize') {
    return { jsonrpc: '2.0', id: id, result: { protocolVersion: MCP_PROTOCOL_LEGACY, capabilities: { tools: {} }, serverInfo: mcpServerInfo(ctx) } };
  }
  if (method === 'ping') return { jsonrpc: '2.0', id: id, result: {} };
  if (method === 'tools/list') return { jsonrpc: '2.0', id: id, result: { tools: mcpTools(ctx && ctx.toolProfile) } };
  if (method === 'tools/call') {
    const out = callTool(params.name || '', params.arguments || {}, ctx);
    return { jsonrpc: '2.0', id: id, result: { content: [{ type: 'text', text: out.text }], isError: !!out.error } };
  }
  return { jsonrpc: '2.0', id: id, error: { code: -32601, message: 'Method not found: ' + method } };
}
function cmdServe(opts) {
  if (opts.stdio) { cmdServeStdio(opts); return; }
  const legacyEnvError = legacyIdentityEnvError();
  if (legacyEnvError) {
    console.error(legacyEnvError);
    process.exit(2);
  }
  if (opts.agent || opts.agentId) {
    console.error('HTTP MCP 不接受 --agent/--agent-id 启动参数：身份只从请求头 Authorization + X-Agent-Id + X-Agent-Key 读取。');
    process.exit(2);
  }
  const host = opts.host || '0.0.0.0';
  const port = opts.port || 8787;
  const noAuth = !!opts.noAuth;
  const root = userRoot();
  ensureInit(root);
  function authorize(req) {
    const agentId = String(req.headers['x-agent-id'] || '').trim();
    const agentKey = String(req.headers['x-agent-key'] || '').trim();
    const toolProfile = normalizeMcpToolProfile(opts.toolProfile);
    if (noAuth) return { agent: agentId, agentKey: agentKey, toolProfile: toolProfile, identityMode: 'headers' };
    if (!agentId || !agentKey) return null;
    const auth = req.headers['authorization'] || '';
    const m = /^Bearer\s+(.+)$/i.exec(auth);
    if (!m) return null;
    const token = m[1].trim();
    const agent = agentId;
    const tokenMap = (loadTokens(root).tokens) || {};
    if (tokenMap[agent] && tokenMap[agent].token === token) return { agent: agent, agentKey: agentKey, toolProfile: toolProfile, identityMode: 'headers' };
    return null;
  }
  function originAllowed(req) {
    const origin = req.headers['origin'];
    if (!origin) return true;
    let oHost = '';
    try { oHost = new URL(origin).host; } catch (e) { return false; }
    const hHost = req.headers['host'] || '';
    const allowed = [hHost, 'localhost', 'localhost:' + port, '127.0.0.1', '127.0.0.1:' + port, '[::1]', '[::1]:' + port];
    return oHost === hHost || allowed.indexOf(oHost) !== -1;
  }
  function sendJson(res, code, obj) {
    res.writeHead(code, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(obj));
  }
  const server = http.createServer(function (req, res) {
    let pathname = '/';
    try { pathname = new URL(req.url, 'http://' + (req.headers.host || 'localhost')).pathname; } catch (e) {}
    if (pathname !== '/mcp') { res.writeHead(404, { 'Content-Type': 'text/plain' }); res.end('not found'); return; }
    if (!originAllowed(req)) {
      sendJson(res, 403, { jsonrpc: '2.0', error: { code: -32000, message: 'origin not allowed' } });
      return;
    }
    const auth = authorize(req);
    if (!auth) {
      sendJson(res, 401, { jsonrpc: '2.0', error: { code: -32001, message: 'unauthorized: 需要有效 Bearer token 与 X-Agent-Id；加密私密操作还需 X-Agent-Key' } });
      return;
    }
    if (req.method === 'GET') {
      // deprecated 兼容：HTTP+SSE 端点（MCP 2026-07-28 起正式 Deprecated，12 个月窗口内保留给老客户端；新客户端走 POST）
      res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive' });
      res.write('event: endpoint\ndata: /mcp\n\n');
      const iv = setInterval(function () { res.write(': keep-alive\n\n'); }, 15000);
      req.on('close', function () { clearInterval(iv); });
      return;
    }
    if (req.method === 'POST') {
      let body = '';
      req.on('data', function (c) { body += c; });
      req.on('end', function () {
        let msg;
        try { msg = JSON.parse(body); } catch (e) {
          sendJson(res, 400, { jsonrpc: '2.0', error: { code: -32700, message: 'parse error' } });
          return;
        }
        const metaPv = reqVersion(msg.params) || null;
        const hdrPv = req.headers['mcp-protocol-version'] || null;
        if (hdrPv && metaPv && hdrPv !== metaPv) {
          sendJson(res, 400, { jsonrpc: '2.0', id: msg.id, error: { code: -32020, message: 'HeaderMismatch: MCP-Protocol-Version header/body 不一致', data: { header: hdrPv, body: metaPv } } });
          return;
        }
        const mcpMethod = req.headers['mcp-method'];
        if (mcpMethod && metaPv === MCP_PROTOCOL_MODERN && mcpMethod !== msg.method) {
          sendJson(res, 400, { jsonrpc: '2.0', id: msg.id, error: { code: -32020, message: 'HeaderMismatch: Mcp-Method header/body 不一致', data: { header: mcpMethod, body: msg.method } } });
          return;
        }
        const resp = handleMessage(msg, auth);
        if (resp === null) { res.writeHead(204); res.end(); return; }
        sendJson(res, 200, resp);
      });
      return;
    }
    res.writeHead(405, { 'Content-Type': 'text/plain' }); res.end('method not allowed');
  });
  server.listen(port, host, function () {
    console.log('yotta-memory 记忆引擎已启动（v' + VERSION + '）');
    console.log('URL: http://' + host + ':' + port + '/mcp');
    if (opts.profile) console.log('服务 profile: ' + path.resolve(String(opts.profile)));
    console.log('记忆库: ' + root);
    console.log('MCP 协议: 2026-07-28（modern，server/discover）/ 2025-11-25（legacy 握手兼容）');
    console.log('工具分组: ' + normalizeMcpToolProfile(opts.toolProfile));
    if (noAuth) console.log('鉴权: 已关闭（--no-auth，仅限可信内网）');
    else console.log('鉴权: Bearer token + X-Agent-Id + X-Agent-Key（token 由 token new 生成，agent_key 由 view 授权生成）');
    console.log('按 Ctrl+C 停止');
    startBackupFallback();
  });
}
// ---- stdio 本地零进程模式（客户端按需拉起 CLI）----
function cmdServeStdio(opts) {
  const legacyEnvError = legacyIdentityEnvError();
  if (legacyEnvError) {
    console.error(legacyEnvError);
    process.exit(2);
  }
  if (opts.agent) {
    console.error('stdio MCP 不接受 --agent：请使用显式参数 --agent-id <id> + --agent-key-file <path>。');
    process.exit(2);
  }
  if (opts.agentKey) {
    console.error('stdio MCP 不接受 --agent-key：命令行会暴露 key；请使用 --agent-key-file <path>。');
    process.exit(2);
  }
  const ident = resolveIdentity(opts);
  if (ident.error) {
    console.error(ident.error);
    process.exit(2);
  }
  const root = userRoot();
  ensureInit(root);
  const ctx = {
    agent: ident.id,
    agentKey: ident.agentKey,
    toolProfile: normalizeMcpToolProfile(opts && opts.toolProfile),
    identityMode: 'stdio-args',
  };
  let buf = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', function (chunk) {
    buf += chunk;
    let idx;
    while ((idx = buf.indexOf('\n')) !== -1) {
      const line = buf.slice(0, idx).trim();
      buf = buf.slice(idx + 1);
      if (!line) continue;
      let msg;
      try { msg = JSON.parse(line); } catch (e) { continue; }
      const resp = handleMessage(msg, ctx);
      if (resp !== null) process.stdout.write(JSON.stringify(resp) + '\n');
    }
  });
  process.stdin.on('end', function () { process.exit(0); });
}

// ---- lan command (autostart management for serve) ----
// Windows dual mechanism: (1) schtasks scheduled task registered from task XML (default, needs
// permission; v0.22.4: S4U principal -> silent in background for both logon/boot triggers, no
// console window; battery limits and the 72h execution time limit removed); (2) non-admin
// (Access denied) auto-fallback to user-level Startup silent autostart (VBS sh.Run <autostart.cmd>,
// 0, False + autostart.cmd; node path process.execPath auto-detected, 0.5.4)
// Linux (v0.6.4): (1) systemd user unit (systemctl --user enable/start, login autostart; --onstart
// additionally runs loginctl enable-linger for boot autostart); (2) auto-fallback to user crontab
// @reboot when no systemd user session is available.
const LAN_TASK_NAME = 'YottaMemoryServe';
const LAN_GEN_MARKER = 'Generated by yotta-memory lan enable';
const LAN_UNIT_NAME = 'yotta-memory-serve.service';
const LAN_CRONTAB_MARKER = '#YTM_LAN:yotta-memory-serve';
const SERVE_PROFILE_FILE = 'serve-profile.json';
const SERVE_PROFILE_SCHEMA = 1;

function resolveProfilePath(value) {
  const text = String(value || '');
  if (!text) return '';
  if (path.isAbsolute(text)) return path.resolve(text);
  if (path.win32.isAbsolute(text)) return path.win32.normalize(text);
  return path.resolve(text);
}

function lanServeProfilePath(opts) {
  opts = opts || {};
  if (opts.profilePath) return resolveProfilePath(opts.profilePath);
  if (process.env.YOTTA_LAN_PROFILE_FILE) return resolveProfilePath(process.env.YOTTA_LAN_PROFILE_FILE);
  const configDir = opts.configDir || process.env.YOTTA_MEMORY_CONFIG_DIR || path.dirname(configPath());
  return path.join(path.resolve(String(configDir)), SERVE_PROFILE_FILE);
}

function lanCurrentUser(opts) {
  opts = opts || {};
  if (opts.currentUser) return String(opts.currentUser);
  if (lanPlatform() === 'win32') return lanWindowsTaskUser(opts);
  try {
    const info = os.userInfo();
    return String(info.username || '');
  } catch (e) {
    return '';
  }
}

function sameLanUser(a, b) {
  const left = String(a || '').trim().toLowerCase();
  const right = String(b || '').trim().toLowerCase();
  return !left || !right || left === right;
}

function lanWriteServeProfile(opts) {
  opts = opts || {};
  try {
    const memoryHome = path.resolve(String(opts.memoryHome || userRoot()));
    const runtimeHome = path.resolve(String(opts.runtimeHome || runtimeRoot()));
    const configDir = path.resolve(String(opts.configDir || process.env.YOTTA_MEMORY_CONFIG_DIR || path.dirname(configPath())));
    const profilePath = lanServeProfilePath(Object.assign({}, opts, { configDir: configDir }));
    if (!fs.existsSync(memoryHome) || !fs.statSync(memoryHome).isDirectory()) {
      return { error: true, text: '记忆库不存在或不是目录: ' + memoryHome + '。请先初始化或修正 memory_home。' };
    }
    const profile = {
      schemaVersion: SERVE_PROFILE_SCHEMA,
      generatedAt: new Date().toISOString(),
      userId: String(opts.userId || lanCurrentUser(opts)),
      memoryHome: memoryHome,
      runtimeHome: runtimeHome,
      configDir: configDir,
      host: String(opts.host || '0.0.0.0'),
      port: parseInt(opts.port, 10) || 8787,
    };
    fs.mkdirSync(path.dirname(profilePath), { recursive: true });
    atomicWriteFileSync(profilePath, JSON.stringify(profile, null, 2) + '\n', 'utf8');
    return { error: false, profilePath: profilePath, profile: profile };
  } catch (e) {
    return { error: true, text: '写入服务 profile 失败: ' + String((e && e.message) || e) };
  }
}

function loadServeProfile(profilePath, opts) {
  opts = opts || {};
  const resolved = resolveProfilePath(profilePath);
  try {
    if (!profilePath) return { error: true, text: 'profile 路径不能为空。' };
    const profile = JSON.parse(String(fs.readFileSync(resolved, 'utf8')).replace(/^\uFEFF/, ''));
    if (!profile || profile.schemaVersion !== SERVE_PROFILE_SCHEMA) {
      return { error: true, text: 'profile schemaVersion 无效，需要 ' + SERVE_PROFILE_SCHEMA + '。' };
    }
    for (const key of ['memoryHome', 'runtimeHome', 'configDir']) {
      const value = String(profile[key] || '').trim();
      if (!value || !path.isAbsolute(value)) {
        return { error: true, text: 'profile 字段 ' + key + ' 必须是绝对路径。' };
      }
    }
    const memoryHome = path.resolve(String(profile.memoryHome));
    const runtimeHome = path.resolve(String(profile.runtimeHome));
    const configDir = path.resolve(String(profile.configDir));
    if (!fs.existsSync(memoryHome) || !fs.statSync(memoryHome).isDirectory()) {
      return { error: true, text: 'profile memoryHome 指定的记忆库不存在或不是目录: ' + memoryHome };
    }
    if (!fs.existsSync(runtimeHome) || !fs.statSync(runtimeHome).isDirectory()) {
      return { error: true, text: 'profile runtimeHome 指定的运行时目录不存在或不是目录: ' + runtimeHome };
    }
    const currentUser = opts.currentUser || lanCurrentUser(opts);
    if (!sameLanUser(profile.userId, currentUser)) {
      return { error: true, text: 'profile userId 与当前用户不匹配: ' + String(profile.userId || '(empty)') + ' != ' + String(currentUser || '(empty)') };
    }
    return {
      error: false,
      profilePath: resolved,
      profile: Object.assign({}, profile, {
        memoryHome: memoryHome,
        runtimeHome: runtimeHome,
        configDir: configDir,
      }),
    };
  } catch (e) {
    return { error: true, text: '无法读取服务 profile ' + resolved + ': ' + String((e && e.message) || e) };
  }
}

function applyServeProfile(profilePath, opts) {
  const loaded = loadServeProfile(profilePath, opts);
  if (loaded.error) return loaded;
  process.env.YOTTA_MEMORY_HOME = loaded.profile.memoryHome;
  process.env.YOTTA_MEMORY_RUNTIME_HOME = loaded.profile.runtimeHome;
  process.env.YOTTA_MEMORY_CONFIG_DIR = loaded.profile.configDir;
  return loaded;
}

function serveProfileDrift(profile) {
  if (!profile) return [];
  const drift = [];
  if (path.resolve(String(profile.memoryHome || '')) !== path.resolve(userRoot())) drift.push('memoryHome');
  if (path.resolve(String(profile.runtimeHome || '')) !== path.resolve(runtimeRoot())) drift.push('runtimeHome');
  if (path.resolve(String(profile.configDir || '')) !== path.resolve(path.dirname(configPath()))) drift.push('configDir');
  return drift;
}

function lanTaskRunCmd(opts) {
  opts = opts || {};
  const host = opts.host || '0.0.0.0';
  const port = opts.port || 8787;
  const profilePath = lanServeProfilePath(opts);
  // schtasks /tr 不接受多余内嵌引号：路径无空格不加引号，含空格/引号用 \" 转义（0.5.2 修复）
  const q = (p) => /[\s"]/.test(p) ? '\\"' + p.replace(/"/g, '\\"') + '\\"' : p;
  const prefix = lanElectronHost(opts) ? 'set "ELECTRON_RUN_AS_NODE=1" && ' : '';
  return prefix + q(process.execPath) + ' ' + q(runtimeManagedScript()) + ' serve --profile ' + q(profilePath) + ' --host ' + host + ' --port ' + port;
}

function lanServeArgs(opts) {
  return ['serve', '--profile', lanServeProfilePath(opts), '--host', String(opts.host || '0.0.0.0'), '--port', String(opts.port || 8787)];
}
// generic spawn wrapper: YOTTA_LAN_*_BIN may point to a .js stub (testing/advanced use;
// on Windows run it with the current node interpreter automatically)
function lanSpawn(bin, args, spawnOpts) {
  if (process.platform === 'win32' && /\.js$/i.test(String(bin))) {
    return child_process.spawnSync(process.execPath, [bin].concat(args), spawnOpts);
  }
  return child_process.spawnSync(bin, args, spawnOpts);
}
// platform override for testing/advanced use (YOTTA_LAN_PLATFORM=linux/win32/...)
function lanPlatform() { return process.env.YOTTA_LAN_PLATFORM || process.platform; }
// ---- v0.22.5: Electron 宿主（YottaCode shim）适配 ----
// 背景：宿主运行时为 Electron 时（如 YottaCode.exe 以 ELECTRON_RUN_AS_NODE=1 当 Node 运行本脚本），
// process.execPath 指向 Electron 可执行文件；自启 / 定时任务环境不带 ELECTRON_RUN_AS_NODE=1 时，
// 拉起的是桌面程序本体而非 Node 服务（0.22.4 后新机首例实测）。生成任务 / 兜底 / 定时配置时统一注入。
function lanElectronHost(opts) {
  opts = opts || {};
  if (typeof opts.electronHost === 'boolean') return opts.electronHost;
  if (process.env.YOTTA_LAN_ELECTRON_HOST === '1') return true;
  if (process.env.YOTTA_LAN_ELECTRON_HOST === '0') return false;
  return !!(process.versions && process.versions.electron);
}
// 任务 / 兜底命令是否指向 Electron 可执行文件且缺少 ELECTRON_RUN_AS_NODE（旧任务告警用）
function lanTaskCommandNeedsElectronEnv(text) {
  const t = String(text || '');
  if (!t || /ELECTRON_RUN_AS_NODE/.test(t)) return false;
  if (/electron|yottacode/i.test(t)) return true;
  if (lanElectronHost({})) {
    const exe = String(process.execPath || '');
    if (exe && t.toLowerCase().indexOf(exe.toLowerCase()) !== -1) return true;
  }
  return false;
}
// sh-style single-quote quoting (crontab line is executed via /bin/sh -c)
function shQuote(s) {
  const p = String(s);
  if (!/[\s'"\\$\`]/.test(p)) return p;
  return "'" + p.replace(/'/g, "'\\''") + "'";
}
// systemd ExecStart quoting (systemd's own parse rules: double quotes group, \" escapes a quote,
// \\ escapes a backslash)
function systemdEscapeArg(s) {
  const p = String(s);
  if (!/[\s"\\$;]/.test(p)) return p;
  return '"' + p.replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"';
}
function lanStartupDir(opts) {
  if (opts && opts.startupDir) return String(opts.startupDir);
  // 测试/高级用途可用 YOTTA_LAN_STARTUP_DIR 覆盖（默认用户级 Startup 目录，免管理员）
  if (process.env.YOTTA_LAN_STARTUP_DIR) return process.env.YOTTA_LAN_STARTUP_DIR;
  const base = process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming');
  return path.join(base, 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup');
}
function lanAutostartDir(opts) {
  if (opts && opts.autostartDir) return String(opts.autostartDir);
  // 产品自有目录 ~/.yottamemory/autostart/（引擎数据目录内，非系统配置）；测试可用 YOTTA_LAN_AUTOSTART_DIR 覆盖
  if (process.env.YOTTA_LAN_AUTOSTART_DIR) return process.env.YOTTA_LAN_AUTOSTART_DIR;
  return path.join(os.homedir(), '.yottamemory', 'autostart');
}
function lanVbsPath(opts) { return path.join(lanStartupDir(opts), 'yotta-memory-serve.vbs'); }
function lanAutostartCmdPath(opts) { return path.join(lanAutostartDir(opts), 'yotta-memory-autostart.cmd'); }
function lanLogPath(opts) {
  if (opts && opts.logPath) return String(opts.logPath);
  if (process.env.YOTTA_LAN_LOG_FILE) return process.env.YOTTA_LAN_LOG_FILE;
  return path.join(os.homedir(), '.yottamemory', 'serve-' + (opts.port || 8787) + '.log');
}
function lanAutostartCmdContent(opts) {
  opts = opts || {};
  const host = opts.host || '0.0.0.0';
  const port = opts.port || 8787;
  const profilePath = lanServeProfilePath(opts);
  const q = (p) => '"' + String(p).replace(/"/g, '""') + '"';
  // 生成文件用纯 ASCII（避免 cmd/VBS 按系统代码页读取中文注释乱码；VBS 自愈内联同一内容）
  // v0.22.5: Electron 宿主下需先设 ELECTRON_RUN_AS_NODE=1，否则拉起桌面程序本体而非 Node。
  return '@echo off\r\n'
    + 'chcp 65001 >nul\r\n'
    + 'rem ' + LAN_GEN_MARKER + '; remove with: yotta-memory lan disable (English only, keep ASCII)\r\n'
    + (lanElectronHost(opts) ? 'set "ELECTRON_RUN_AS_NODE=1"\r\n' : '')
    + q(process.execPath) + ' ' + q(runtimeManagedScript()) + ' serve --profile ' + q(profilePath) + ' --host ' + host + ' --port ' + port + ' >> ' + q(lanLogPath(opts)) + ' 2>&1\r\n';
}
function lanVbsContent(opts) {
  // v0.6.3 自愈：VBS 内联 autostart.cmd 内容，启动时若 .cmd 缺失/被清理即就地重建，
  // 根治 80070002（wscript 找不到被引用的启动文件）。VBS 写 UTF-16LE，wscript 按 Unicode 读取。
  const cmdContent = lanAutostartCmdContent(opts || {});
  // VBS 字符串字面量不能含原始换行：把 CRLF 编码为 Chr(13) & Chr(10) & 拼接，
  // 生成的 VBS 保持单行合法（否则 wscript 报语法错误，.cmd 重建失败）。
  const vbsCmdLiteral = cmdContent
    .replace(/\r\n/g, '\n')
    .replace(/\n/g, '\n')
    .split('\n')
    .map(function (seg) {
      // 每段都带引号（VBS 字符串字面量），换行用 Chr(13) & Chr(10) 拼接
      return '"' + seg.replace(/"/g, '""') + '"';
    })
    .join(' & Chr(13) & Chr(10) & ');
  const vbsCmdPath = String(lanAutostartCmdPath(opts)).replace(/"/g, '""');
  const lines = [
    "' " + LAN_GEN_MARKER + '; remove with: yotta-memory lan disable',
    "' v0.6.3 self-heal: always rebuild autostart.cmd from embedded content, then run it (fix 80070002)",
    'Set fso = CreateObject("Scripting.FileSystemObject")',
    'Set sh = CreateObject("WScript.Shell")',
    'cmdPath = "' + vbsCmdPath + '"',
    'On Error Resume Next',
    'Set dir = fso.GetParentFolderName(cmdPath)',
    'If Not fso.FolderExists(dir) Then fso.CreateFolder(dir)',
    'Set f = fso.CreateTextFile(cmdPath, True)',
    'f.Write ' + vbsCmdLiteral,
    'f.Close',
    'sh.Run cmdPath, 0, False',
    '',
  ];
  return lines.join('\r\n') + '\r\n';
}
function lanInstallStartup(opts) {
  fs.mkdirSync(lanAutostartDir(opts), { recursive: true });
  fs.writeFileSync(lanAutostartCmdPath(opts), lanAutostartCmdContent(opts), 'utf8');
  fs.mkdirSync(lanStartupDir(opts), { recursive: true });
  // VBS 用 UTF-16LE+BOM：wscript 按 Unicode 读取，中文路径不乱码（纯 ANSI 读取会按系统代码页误读）
  fs.writeFileSync(lanVbsPath(opts), '\ufeff' + lanVbsContent(opts), 'utf16le');
}
function lanRemoveStartupFiles(opts) {
  // 只删除带产品标记的生成文件，绝不误删用户自己的 Startup 文件
  const removed = [];
  for (const f of [lanVbsPath(opts), lanAutostartCmdPath(opts)]) {
    try {
      if (lanFileHasMarker(f)) { fs.unlinkSync(f); removed.push(f); }
    } catch (e) { /* 单个文件失败不阻断其它清理 */ }
  }
  return removed;
}
function lanFileHasMarker(f) {
  try {
    if (!fs.existsSync(f)) return false;
    const buf = fs.readFileSync(f);
    const m8 = Buffer.from(LAN_GEN_MARKER, 'utf8');
    const m16 = Buffer.from(LAN_GEN_MARKER, 'utf16le');
    return buf.indexOf(m8) !== -1 || buf.indexOf(m16) !== -1;
  } catch (e) { return false; }
}
function isSchtasksAccessDenied(e) {
  const msg = typeof e === 'string' ? e : String((e && e.stderr) || (e && e.message) || e || '');
  return /access\s+is\s+denied|access\s+denied|拒绝访问/i.test(msg);
}

// ---- lan Windows task XML (v0.22.4: S4U silent principal) ----
// 背景（0.22.3 及更早缺陷）：schtasks /create 未指定主体 -> 默认交互式（仅登录时运行）：
// ① 在登录会话里运行控制台程序会弹窗口；② --onstart 开机触发时无登录会话，任务起不来且不补跑。
// 修复：改为注册任务 XML —— S4U 主体（“不管用户是否登录都运行”，不存密码、非交互、无窗口），
// 默认去掉电池限制与 72 小时执行时限（PT0S = 不限时），开机/登录触发均可后台静默启动。
function lanSchTasksBin() { return process.env.YOTTA_LAN_SCHTASKS_BIN || 'schtasks'; }
function lanWindowsRunSchtasks(opts, args) {
  if (opts && typeof opts.execFileFn === 'function') {
    try {
      const out = opts.execFileFn(lanSchTasksBin(), args);
      return { status: 0, stdout: String(out || ''), stderr: '' };
    } catch (e) {
      return {
        status: typeof e.status === 'number' ? e.status : 1,
        stdout: String((e && e.stdout) || ''),
        stderr: String((e && e.stderr) || (e && e.message) || e),
      };
    }
  }
  const r = lanSpawn(lanSchTasksBin(), args, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
  return {
    status: r.error ? 1 : r.status,
    stdout: String(r.stdout || ''),
    stderr: String(r.stderr || (r.error && r.error.message) || ''),
  };
}
function lanWindowsTaskUser(opts) {
  opts = opts || {};
  if (opts.userId) return String(opts.userId);
  // 测试/高级用途可用 YOTTA_LAN_TASK_USER 覆盖（S4U 主体必须是当前用户名）
  if (process.env.YOTTA_LAN_TASK_USER) return String(process.env.YOTTA_LAN_TASK_USER);
  if (process.env.USERDOMAIN && process.env.USERNAME) return process.env.USERDOMAIN + '\\' + process.env.USERNAME;
  if (process.env.COMPUTERNAME && process.env.USERNAME) return process.env.COMPUTERNAME + '\\' + process.env.USERNAME;
  try {
    const r = lanSpawn('whoami', [], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
    if (r.status === 0 && String(r.stdout || '').trim()) return String(r.stdout).trim();
  } catch (e) { /* 用户名探测失败 -> 主体省略 UserId，由 schtasks 按当前用户注册 */ }
  return '';
}
function lanWindowsTaskXml(opts) {
  opts = opts || {};
  const onstart = opts.trigger ? String(opts.trigger) === 'onstart' : !!opts.onstart;
  const host = opts.host || '0.0.0.0';
  const port = opts.port || 8787;
  const nodePath = opts.nodePath || process.execPath;
  const scriptPath = opts.scriptPath || runtimeManagedScript();
  const logPath = opts.logPath || lanLogPath(opts);
  const profilePath = lanServeProfilePath(opts);
  const userId = opts.userId || '';
  const cmdPath = opts.cmdPath || process.env.ComSpec || 'cmd.exe';
  // cmd /c 外层引号：命令首段带引号时必须用 ""..." 包裹（cmd 的 /c 引号规则），
  // 让 node/脚本/日志路径里的空格与中文都能安全传递；S4U 非交互会话下不弹窗口。
  // 注意：重定向 `2>&1` 的 & 在 XML 文本里必须写成 &amp;（DOM 解码后仍是 2>&1），
  // 否则 schtasks 报 "The task XML is malformed"。
  // v0.22.5: Electron 宿主（YottaCode shim）下先 set ELECTRON_RUN_AS_NODE=1，
  // 否则任务会拉起桌面程序本体（GUI）而不是 Node 服务。
  const envPrefix = lanElectronHost(opts) ? 'set "ELECTRON_RUN_AS_NODE=1" &amp;&amp; ' : '';
  const inner = envPrefix + '"' + xmlEscape(nodePath) + '" "' + xmlEscape(scriptPath) + '" serve --profile "' + xmlEscape(profilePath) + '" --host ' + host + ' --port ' + port
    + ' >> "' + xmlEscape(logPath) + '" 2>&amp;1';
  const triggerXml = onstart
    ? '<BootTrigger><Enabled>true</Enabled></BootTrigger>'
    : '<LogonTrigger><Enabled>true</Enabled></LogonTrigger>';
  const principal = userId
    ? '<Principal id="Author"><UserId>' + xmlEscape(userId) + '</UserId><LogonType>S4U</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal>'
    : '<Principal id="Author"><LogonType>S4U</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal>';
  return [
    '<?xml version="1.0" encoding="UTF-16"?>',
    '<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">',
    '<RegistrationInfo><Description>Yotta Memory serve autostart (generated by yotta-memory lan enable; S4U silent, no window)</Description></RegistrationInfo>',
    '<Triggers>' + triggerXml + '</Triggers>',
    '<Principals>' + principal + '</Principals>',
    '<Settings>',
    '<MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>',
    '<DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>',
    '<StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>',
    '<AllowHardTerminate>true</AllowHardTerminate>',
    '<StartWhenAvailable>true</StartWhenAvailable>',
    '<RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>',
    '<IdleSettings><StopOnIdleEnd>false</StopOnIdleEnd><RestartOnIdle>false</RestartOnIdle></IdleSettings>',
    '<Enabled>true</Enabled>',
    '<Hidden>false</Hidden>',
    '<RunOnlyIfIdle>false</RunOnlyIfIdle>',
    '<WakeToRun>false</WakeToRun>',
    '<ExecutionTimeLimit>PT0S</ExecutionTimeLimit>',
    '<Priority>7</Priority>',
    '</Settings>',
    '<Actions Context="Author"><Exec><Command>' + xmlEscape(cmdPath) + '</Command><Arguments>/c "' + inner + '"</Arguments></Exec></Actions>',
    '</Task>',
  ].join('\r\n');
}
function lanWindowsEnableCore(opts) {
  opts = opts || {};
  const profileResult = lanWriteServeProfile(opts);
  if (profileResult.error) return { error: true, phase: 'profile', text: profileResult.text };
  const trigger = opts.onstart ? 'onstart' : 'onlogon';
  const host = opts.host || '0.0.0.0';
  const port = opts.port || 8787;
  const nodePath = opts.nodePath || process.execPath;
  const scriptPath = opts.scriptPath || runtimeManagedScript();
  const logPath = lanLogPath(opts);
  const userId = lanWindowsTaskUser(opts);
  const xml = lanWindowsTaskXml({ trigger: trigger, host: host, port: port, nodePath: nodePath, scriptPath: scriptPath, logPath: logPath, profilePath: profileResult.profilePath, userId: userId, electronHost: opts.electronHost });
  const xmlDir = opts.xmlDir || process.env.YOTTA_LAN_TASK_XML_DIR || os.tmpdir();
  const xmlPath = opts.xmlPath || path.join(xmlDir, LAN_TASK_NAME + '-task-' + process.pid + '-' + Date.now() + '.xml');
  let failure = null;
  try {
    fs.mkdirSync(path.dirname(xmlPath), { recursive: true });
    // UTF-16LE + BOM：与 schtasks /query /xml 导出格式一致，schtasks /create /xml 必然可读
    fs.writeFileSync(xmlPath, '\ufeff' + xml, 'utf16le');
    const r = lanWindowsRunSchtasks(opts, ['/create', '/tn', LAN_TASK_NAME, '/xml', xmlPath, '/f']);
    if (r.status !== 0) failure = String(r.stderr || r.stdout || '').trim() || ('schtasks 退出码 ' + r.status);
  } catch (e) {
    failure = String((e && e.message) || e);
  } finally {
    try { fs.unlinkSync(xmlPath); } catch (e) { /* 临时 XML 清理尽力而为 */ }
  }
  if (!failure) {
    let removedStartup = [];
    try { removedStartup = lanRemoveStartupFiles(opts); } catch (e) { removedStartup = []; }
    return { error: false, mode: 'task', taskName: LAN_TASK_NAME, trigger: trigger, logPath: logPath, profilePath: profileResult.profilePath, removedStartup: removedStartup };
  }
  try {
    lanInstallStartup(opts);
  } catch (e2) {
    return { error: true, mode: 'startup', reason: failure, text: String((e2 && e2.message) || e2) };
  }
  return {
    error: false,
    mode: 'startup',
    trigger: trigger,
    reason: failure,
    accessDenied: isSchtasksAccessDenied(failure),
    vbsPath: lanVbsPath(opts),
    cmdPath: lanAutostartCmdPath(opts),
    logPath: logPath,
    profilePath: profileResult.profilePath,
  };
}

// ---- lan Linux (systemd user unit / user crontab @reboot) ----
function lanLinuxSystemdUserDir() {
  // override with YOTTA_LAN_SYSTEMD_USER_DIR for testing/advanced use (default ~/.config/systemd/user)
  if (process.env.YOTTA_LAN_SYSTEMD_USER_DIR) return process.env.YOTTA_LAN_SYSTEMD_USER_DIR;
  const cfg = process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config');
  return path.join(cfg, 'systemd', 'user');
}
function lanLinuxUnitPath() { return path.join(lanLinuxSystemdUserDir(), LAN_UNIT_NAME); }
function lanLinuxSystemctlBin() { return process.env.YOTTA_LAN_SYSTEMCTL_BIN || 'systemctl'; }
function lanLinuxLoginctlBin() { return process.env.YOTTA_LAN_LOGINCTL_BIN || 'loginctl'; }
function lanLinuxExecStart(opts) {
  return [systemdEscapeArg(process.execPath), systemdEscapeArg(runtimeManagedScript())]
    .concat(lanServeArgs(opts).map(systemdEscapeArg))
    .join(' ');
}
function lanLinuxUnitContent(opts) {
  // keep comments ASCII (avoid locale/encoding issues); ExecStart uses systemd's own quote rules
  const lines = [
    '# ' + LAN_GEN_MARKER + '; remove with: yotta-memory lan disable (English only, keep ASCII)',
    '',
    '[Unit]',
    'Description=yotta-memory memory engine (lan autostart)',
    '',
    '[Service]',
    'Type=simple',
  ];
  if (lanElectronHost(opts)) lines.push('Environment=ELECTRON_RUN_AS_NODE=1');
  lines.push(
    'ExecStart=' + lanLinuxExecStart(opts),
    'Restart=on-failure',
    'RestartSec=3',
    '',
    '[Install]',
    'WantedBy=default.target',
    '',
  );
  return lines.join('\n');
}
function lanCrontabBin() { return process.env.YOTTA_LAN_CRONTAB_BIN || 'crontab'; }
function lanCrontabLine(opts) {
  const parts = ['@reboot'];
  if (lanElectronHost(opts)) parts.push('ELECTRON_RUN_AS_NODE=1');
  parts.push(shQuote(process.execPath), shQuote(runtimeManagedScript()));
  return parts.concat(lanServeArgs(opts).map(shQuote)).join(' ') + ' >> ' + shQuote(lanLogPath(opts)) + ' 2>&1 ' + LAN_CRONTAB_MARKER;
}
function lanCrontabRead() {
  try {
    const r = lanSpawn(lanCrontabBin(), ['-l'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    if (r.status === 0) return String(r.stdout || '').split(/\r?\n/).filter(function (l) { return l !== ''; });
  } catch (e) { /* crontab unavailable -> treat as empty */ }
  return [];
}
function lanCrontabWrite(lines) {
  const content = lines.join('\n') + (lines.length ? '\n' : '');
  const r = lanSpawn(lanCrontabBin(), ['-'], { input: content, encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
  if (r.error) throw r.error;
  if (r.status !== 0) throw new Error(String(r.stderr || r.stdout || '').toString().split(/\r?\n/)[0]);
}
function lanCrontabHasOurLine(lines) {
  return lines.some(function (l) { return l.indexOf(LAN_CRONTAB_MARKER) !== -1; });
}
function lanCrontabWithoutOurLine(lines) {
  return lines.filter(function (l) { return l.indexOf(LAN_CRONTAB_MARKER) === -1; });
}
function lanLinuxHasSystemd() {
  try {
    const r = lanSpawn(lanLinuxSystemctlBin(), ['--user', 'show-environment'], { stdio: ['ignore', 'ignore', 'ignore'] });
    return r.status === 0;
  } catch (e) { return false; }
}
function lanLinuxSystemctl(args) {
  const r = lanSpawn(lanLinuxSystemctlBin(), ['--user'].concat(args), { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
  if (r.error) throw r.error;
  return { status: r.status, out: String(r.stdout || ''), err: String(r.stderr || '') };
}
function lanLinuxInstallSystemd(opts) {
  const dir = lanLinuxSystemdUserDir();
  fs.mkdirSync(dir, { recursive: true });
  const unit = lanLinuxUnitPath();
  fs.writeFileSync(unit, lanLinuxUnitContent(opts), 'utf8');
  lanLinuxSystemctl(['daemon-reload']);
  const en = lanLinuxSystemctl(['enable', LAN_UNIT_NAME]);
  if (en.status !== 0) throw new Error('systemctl --user enable 失败: ' + en.err.split(/\r?\n/)[0]);
  const st = lanLinuxSystemctl(['start', LAN_UNIT_NAME]);
  if (st.status !== 0) {
    console.error('启动服务失败（已注册，稍后可执行 systemctl --user start yotta-memory-serve.service）: ' + st.err.split(/\r?\n/)[0]);
  }
  if (opts.onstart) {
    try {
      const lr = lanSpawn(lanLinuxLoginctlBin(), ['enable-linger'], { stdio: ['ignore', 'pipe', 'pipe'] });
      if (lr.status === 0) console.log('已启用 lingering（开机即启，无需登录）');
      else console.error('提示: 开机即启需 loginctl enable-linger，当前未生效（' + String(lr.stderr || '').split(/\r?\n/)[0] + '）');
    } catch (e) {
      console.error('提示: 开机即启需 loginctl enable-linger，当前无 loginctl（' + String((e && e.message) || e).split(/\r?\n/)[0] + '）');
    }
  }
  return unit;
}
function lanLinuxRemoveSystemd() {
  // only remove our own marker unit file, never a user's own systemd unit
  const unit = lanLinuxUnitPath();
  if (!fs.existsSync(unit) || !lanFileHasMarker(unit)) return false;
  try { lanLinuxSystemctl(['disable', LAN_UNIT_NAME]); } catch (e) {}
  try { lanLinuxSystemctl(['stop', LAN_UNIT_NAME]); } catch (e) {}
  try { fs.unlinkSync(unit); } catch (e) {}
  try { lanLinuxSystemctl(['daemon-reload']); } catch (e) {}
  return true;
}
function lanLinuxInstallCrontab(opts) {
  const lines = lanCrontabWithoutOurLine(lanCrontabRead());
  lines.push(lanCrontabLine(opts));
  lanCrontabWrite(lines);
  return lanCrontabLine(opts);
}
function lanLinuxRemoveCrontab() {
  const cur = lanCrontabRead();
  const lines = lanCrontabWithoutOurLine(cur);
  if (lines.length === cur.length) return false;
  lanCrontabWrite(lines);
  return true;
}
function cmdLanLinuxEnable(opts) {
  const profileResult = lanWriteServeProfile(opts);
  if (profileResult.error) {
    console.error('服务 profile 写入失败，拒绝注册开机自启: ' + profileResult.text);
    process.exit(1);
  }
  opts = Object.assign({}, opts, { profilePath: profileResult.profilePath });
  if (lanLinuxHasSystemd()) {
    try {
      const unit = lanLinuxInstallSystemd(opts);
      console.log('已注册开机自启: systemd 用户单元 ' + LAN_UNIT_NAME);
      console.log('单元文件: ' + unit);
      console.log('备注: 登录后自动启动（systemctl --user）；如需现在运行请执行 yotta-memory serve');
      if (!opts.onstart) console.log('提示: 如需开机即启（无需登录），请用 --onstart 重新执行 yotta-memory lan enable');
      return;
    } catch (e) {
      const msg = String((e && e.message) || e).split(/\r?\n/)[0];
      console.error('systemd 注册失败: ' + msg);
      console.log('自动改用用户 crontab @reboot 自启...');
    }
  } else {
    console.log('未检测到 systemd 用户会话，改用用户 crontab @reboot 自启...');
  }
  try {
    const line = lanLinuxInstallCrontab(opts);
    console.log('已启用用户 crontab @reboot 自启');
    console.log('启动命令: ' + line);
    console.log('日志: ' + lanLogPath(opts));
    console.log('备注: 开机时自动启动；如需现在运行请执行 yotta-memory serve');
  } catch (e2) {
    console.error('crontab 注册失败: ' + String((e2 && e2.message) || e2).split(/\r?\n/)[0]);
    console.error('请手动配置开机自启（如 ~/.config/autostart/*.desktop 或系统服务），或直接运行 yotta-memory serve');
    process.exit(1);
  }
}
function cmdLanLinuxDisable() {
  let removedAny = false;
  let sawError = false;
  try {
    if (lanLinuxRemoveSystemd()) { console.log('已移除 systemd 用户单元 ' + LAN_UNIT_NAME); removedAny = true; }
  } catch (e) { console.error('移除 systemd 单元失败: ' + String((e && e.message) || e).split(/\r?\n/)[0]); sawError = true; }
  try {
    if (lanLinuxRemoveCrontab()) { console.log('已移除 crontab @reboot 自启'); removedAny = true; }
  } catch (e) { console.error('移除 crontab 自启失败: ' + String((e && e.message) || e).split(/\r?\n/)[0]); sawError = true; }
  if (!removedAny && !sawError) console.log('未启用: 未发现任何自启配置（systemd 单元与 crontab 均不存在）');
  if (sawError) process.exit(1);
}
function cmdLanLinuxStatus() {
  let any = false;
  const profilePath = lanServeProfilePath();
  if (fs.existsSync(profilePath)) {
    console.log('服务 profile: ' + profilePath);
    const loaded = loadServeProfile(profilePath);
    if (loaded.error) {
      console.log('  警告: ' + loaded.text);
    } else {
      console.log('  记忆库: ' + loaded.profile.memoryHome);
      console.log('  运行时: ' + loaded.profile.runtimeHome);
      const drift = serveProfileDrift(loaded.profile);
      if (drift.length) {
        console.log('  警告: 服务 profile 与当前配置漂移(' + drift.join(', ') + ')，请重新执行 yotta-memory lan enable');
      }
    }
  } else {
    console.log('服务 profile: 不存在 ' + profilePath + '（请重新执行 yotta-memory lan enable）');
  }
  const unit = lanLinuxUnitPath();
  const unitExists = fs.existsSync(unit) && lanFileHasMarker(unit);
  if (unitExists) {
    any = true;
    console.log('systemd 用户单元 ' + LAN_UNIT_NAME + ': 已注册');
    try {
      const en = lanLinuxSystemctl(['is-enabled', LAN_UNIT_NAME]);
      if (en.status === 0) console.log('  启用状态: ' + String(en.out).trim());
    } catch (e) {}
    try {
      const ac = lanLinuxSystemctl(['is-active', LAN_UNIT_NAME]);
      if (ac.status === 0) console.log('  运行状态: ' + String(ac.out).trim());
    } catch (e) {}
    console.log('  单元文件: ' + unit);
  } else {
    console.log('systemd 用户单元 ' + LAN_UNIT_NAME + ': 未注册');
  }
  const lines = lanCrontabRead();
  if (lanCrontabHasOurLine(lines)) {
    any = true;
    console.log('crontab @reboot: 已启用');
    for (const l of lines) {
      if (l.indexOf(LAN_CRONTAB_MARKER) === -1) continue;
      console.log('  ' + l.trim());
      if (!/--profile(?:\s|$)/.test(l)) {
        console.log('  警告: crontab 命令未固定服务 profile；请重新执行 yotta-memory lan enable 修复');
      }
    }
  } else {
    console.log('crontab @reboot: 未启用');
  }
  if (!any) console.log('未启用任何开机自启（可用 yotta-memory lan enable 注册）');
}
function cmdLanWinEnable(opts) {
  if (lanPlatform() !== 'win32') {
    console.error('lan 命令当前仅支持 Windows（计划任务 / Startup 自启）；本机平台: ' + lanPlatform());
    process.exit(2);
  }
  const result = lanWindowsEnableCore(opts);
  if (result.mode === 'task') {
    opts = Object.assign({}, opts, { profilePath: result.profilePath });
    const triggerText = result.trigger === 'onstart' ? '开机触发（无需登录）' : '登录触发';
    console.log('已注册开机自启: 计划任务 ' + LAN_TASK_NAME + '（' + triggerText + '，后台静默运行，不弹窗口）');
    console.log('运行命令: ' + lanTaskRunCmd(opts));
    console.log('服务 profile: ' + result.profilePath);
    console.log('日志: ' + result.logPath);
    if (result.removedStartup && result.removedStartup.length) {
      console.log('已清理旧 Startup 兜底文件 ' + result.removedStartup.length + ' 个（避免双份自启）');
    }
    console.log('备注: 服务不会立刻启动，需重启/重新登录后自动启动；如需现在运行请执行 yotta-memory serve');
    return;
  }
  if (result.error) {
    if (result.phase === 'profile') {
      console.error('服务 profile 写入失败，拒绝注册开机自启: ' + String(result.text || '').split(/\r?\n/)[0]);
      process.exit(1);
    }
    console.error('计划任务注册失败: ' + String(result.reason || '').split(/\r?\n/)[0]);
    console.error('写 Startup 自启失败: ' + String(result.text || '').split(/\r?\n/)[0]);
    console.error('请用管理员终端执行 yotta-memory lan enable，或将以下命令手动加入启动项: ' + lanTaskRunCmd(opts));
    process.exit(1);
  }
  const firstLine = String(result.reason || '').split(/\r?\n/)[0];
  if (result.accessDenied) console.error('计划任务注册被拒绝（当前用户非管理员，Access denied）: ' + firstLine);
  else console.error('计划任务注册失败（当前环境不可用计划任务）: ' + firstLine);
  console.log('自动改用用户级 Startup 静默自启（免管理员）...');
  console.log('已启用用户级 Startup 静默自启（无需管理员）');
  console.log('启动脚本: ' + result.vbsPath);
  console.log('启动命令: ' + result.cmdPath);
  console.log('服务 profile: ' + result.profilePath);
  console.log('日志: ' + result.logPath);
  console.log('备注: 服务不会立刻启动，需重新登录后自动启动；如需现在运行请执行 yotta-memory serve');
  console.log('提示: 如需改回计划任务（后台静默），请用管理员终端重新执行 yotta-memory lan enable');
}
function cmdLanWinDisable() {
  if (lanPlatform() !== 'win32') {
    console.error('lan 命令当前仅支持 Windows（计划任务 / Startup 自启）；本机平台: ' + lanPlatform());
    process.exit(2);
  }
  let sawError = false;
  let removedAny = false;
  const del = lanWindowsRunSchtasks({}, ['/delete', '/tn', LAN_TASK_NAME, '/f']);
  if (del.status === 0) {
    console.log('已移除开机自启计划任务 ' + LAN_TASK_NAME);
    removedAny = true;
  } else {
    const msg = String(del.stderr || del.stdout || '');
    if (!/cannot find the (path|file)|没有找到|找不到|不存在/i.test(msg)) {
      console.error('移除计划任务失败: ' + msg.split(/\r?\n/)[0]);
      if (isSchtasksAccessDenied(msg)) console.error('（当前非管理员，无法移除管理员注册的计划任务；请用管理员终端执行 yotta-memory lan disable）');
      sawError = true;
    }
  }
  for (const f of lanRemoveStartupFiles()) {
    console.log('已移除 Startup 自启文件: ' + f);
    removedAny = true;
  }
  if (!removedAny && !sawError) console.log('未启用: 未发现任何自启配置（计划任务与 Startup 文件均不存在）');
  if (sawError) process.exit(1);
}
function cmdLanWinStatus() {
  if (lanPlatform() !== 'win32') {
    console.log('lan 命令当前仅支持 Windows（计划任务 / Startup 自启）；本机平台: ' + lanPlatform());
    return;
  }
  let taskFound = false;
  const profilePath = lanServeProfilePath();
  const q = lanWindowsRunSchtasks({}, ['/query', '/tn', LAN_TASK_NAME, '/fo', 'LIST', '/v']);
  if (q.status === 0) {
    taskFound = true;
    const xmlQ = lanWindowsRunSchtasks({}, ['/query', '/tn', LAN_TASK_NAME, '/xml']);
    const xmlSaysS4U = xmlQ.status === 0 && /<LogonType>\s*S4U\s*<\/LogonType>/i.test(String(xmlQ.stdout || ''));
    console.log('计划任务 ' + LAN_TASK_NAME + ': 已启用');
    const re = /^(状态|Status|登录模式|Logon Mode|上次运行时间|Last Run Time|上次结果|Last Result|要运行的任务|Task To Run)\s*[:=]\s*(.+)$/;
    let logonMode = '';
    let taskRun = '';
    for (const line of String(q.stdout).split(/\r?\n/)) {
      const m = re.exec(line.trim());
      if (!m) continue;
      console.log('  ' + m[1] + ': ' + m[2]);
      if (/^(登录模式|Logon Mode)$/.test(m[1])) logonMode = m[2];
      if (/^(要运行的任务|Task To Run)$/.test(m[1])) taskRun = m[2];
    }
    if (/interactive|交互式/i.test(logonMode) && !xmlSaysS4U) {
      console.log('  提示: 登录模式为交互式（仅登录时运行，且在登录会话会弹窗口）——这是旧版任务；请重新执行 yotta-memory lan enable 修复为后台静默');
    }
    if (lanTaskCommandNeedsElectronEnv(taskRun)) {
      console.log('  警告: 任务命令指向 Electron 可执行文件（如 YottaCode.exe）但缺少 ELECTRON_RUN_AS_NODE —— 开机将拉起桌面程序而非服务；请重新执行 yotta-memory lan enable 修复');
    }
    if (taskRun && !/--profile(?:\s|$)/.test(taskRun)) {
      console.log('  警告: 任务命令未固定服务 profile，S4U / 无用户环境启动可能落到错误记忆库；请重新执行 yotta-memory lan enable 修复');
    }
    if (fs.existsSync(profilePath)) {
      console.log('  服务 profile: ' + profilePath);
      const loaded = loadServeProfile(profilePath);
      if (loaded.error) {
        console.log('  警告: ' + loaded.text);
      } else {
        console.log('  记忆库: ' + loaded.profile.memoryHome);
        console.log('  运行时: ' + loaded.profile.runtimeHome);
        const drift = serveProfileDrift(loaded.profile);
        if (drift.length) {
          console.log('  警告: 服务 profile 与当前配置漂移(' + drift.join(', ') + ')，请重新执行 yotta-memory lan enable');
        }
      }
    } else {
      console.log('  警告: 服务 profile 不存在: ' + profilePath + '；请重新执行 yotta-memory lan enable');
    }
  } else {
    console.log('计划任务 ' + LAN_TASK_NAME + ': 未启用');
  }
  const vbsOk = lanFileHasMarker(lanVbsPath());
  const cmdOk = lanFileHasMarker(lanAutostartCmdPath());
  if (vbsOk && cmdOk) {
    console.log('Startup 静默自启（免管理员）: 已启用');
    console.log('  启动脚本: ' + lanVbsPath());
    console.log('  启动命令: ' + lanAutostartCmdPath());
    try {
      const cmdText = fs.readFileSync(lanAutostartCmdPath(), 'utf8');
      if (lanTaskCommandNeedsElectronEnv(cmdText)) {
        console.log('  警告: Startup 兜底脚本缺少 ELECTRON_RUN_AS_NODE —— Electron 宿主下会拉起桌面程序而非服务；请重新执行 yotta-memory lan enable 修复');
      }
    } catch (e) { /* 读取失败不影响状态输出 */ }
  } else if (vbsOk || cmdOk) {
    console.log('Startup 静默自启: 部分残留（建议执行 yotta-memory lan disable 后重新 lan enable）');
  } else {
    console.log('Startup 静默自启（免管理员）: 未启用');
  }
  if (!taskFound && !vbsOk && !cmdOk) console.log('未启用任何开机自启（可用 yotta-memory lan enable 注册）');
}

function cmdLanEnable(opts) {
  const runtime = runtimeEnsureForManagedTask();
  if (runtime.error) {
    console.error('runtime 稳定入口未就绪，拒绝注册开机自启: ' + runtime.text);
    process.exit(1);
  }
  const p = lanPlatform();
  if (p === 'win32') return cmdLanWinEnable(opts);
  if (p === 'linux') return cmdLanLinuxEnable(opts);
  console.error('lan 命令当前仅支持 Windows / Linux；本机平台: ' + p);
  process.exit(2);
}
function cmdLanDisable() {
  const p = lanPlatform();
  if (p === 'win32') return cmdLanWinDisable();
  if (p === 'linux') return cmdLanLinuxDisable();
  console.error('lan 命令当前仅支持 Windows / Linux；本机平台: ' + p);
  process.exit(2);
}
function cmdLanStatus() {
  const p = lanPlatform();
  if (p === 'win32') return cmdLanWinStatus();
  if (p === 'linux') return cmdLanLinuxStatus();
  console.log('lan 命令当前仅支持 Windows / Linux；本机平台: ' + p);
}

// ================= v0.10.0 压缩遗忘：分类型衰减 / consolidate 周期摘要 / 自动合并 / 批次回滚 =================
var decayConfigCache = null;

function decayConfig() {
  if (decayConfigCache) return decayConfigCache;
  try { decayConfigCache = loadConfig() || {}; } catch (e) { decayConfigCache = {}; }
  return decayConfigCache;
}

// 分类型衰减半衰期（天）：FACT 慢 / PREF 中 / COMMIT（任务类）快；BOUND 固定不衰减
function decayHalflifeDays(type, cfg) {
  cfg = cfg || {};
  const t = String(type || 'FACT').toUpperCase();
  if (t === 'BOUND') return null;
  const d = parseFloat(cfg['maintain_decay_halflife_' + t]);
  if (d > 0) return d;
  return ({ FACT: 730, PREF: 365, COMMIT: 90 })[t] || 365;
}

// 指数半衰时效：recency = 0.5^(d / halfLife)；BOUND 恒 1.0（不衰减）
function decayRecency(type, ageDays, cfg) {
  const hl = decayHalflifeDays(type, cfg);
  if (hl === null) return 1;
  if (!(ageDays > 0)) return 1;
  return Math.pow(0.5, ageDays / hl);
}

// v0.10.0 归档目标目录：公共 .archive/facts/；私密 .archive/private/<owner>/<type>/（带 owner，防跨 owner 撞名）
function archiveDirFor(root, type, owner) {
  const t = String(type || 'FACT').toUpperCase();
  if (t === 'FACT') return path.join(root, ARCHIVE_DIR, 'facts');
  if (owner) return path.join(root, ARCHIVE_DIR, PRIVATE_DIR, owner, TYPE_DIRS[t] || 'facts');
  return path.join(root, ARCHIVE_DIR, TYPE_DIRS[t] || 'facts');
}

function newBatchId() {
  const d = new Date();
  const p = function (n, w) { return String(n).padStart(w || 2, '0'); };
  let rand = '';
  try { rand = crypto.randomBytes(3).toString('hex'); } catch (e) { rand = String(Math.floor(Math.random() * 16777215)).padStart(6, '0'); }
  return p(d.getFullYear(), 4) + p(d.getMonth() + 1) + p(d.getDate()) + '-' + p(d.getHours()) + p(d.getMinutes()) + p(d.getSeconds()) + '-' + rand;
}

function collectAuditRecords(root) {
  const out = [];
  const log = auditPath(root, 'audit');
  if (!fs.existsSync(log)) return out;
  const raw = fs.readFileSync(log, 'utf8');
  for (const line of raw.split('\n')) {
    if (!line.trim()) continue;
    try { out.push(JSON.parse(line)); } catch (e) { /* 跳过坏行 */ }
  }
  return out;
}

function listBatchesCore(opts) {
  opts = opts || {};
  const limit = (opts.limit && opts.limit > 0) ? opts.limit : 20;
  const roots = memoryRoots();
  const manifests = [];
  for (const root of roots) {
    for (const rec of collectAuditRecords(root)) {
      if (rec.action !== 'manifest') continue;
      manifests.push({ root: root, batch: rec.batch, ts: rec.ts || '', command: rec.command || '', mode: rec.mode || '' });
    }
  }
  manifests.sort(function (a, b) { return String(b.batch).localeCompare(String(a.batch)); });
  const lines = ['## yotta-memory consolidate --batches（近期批次审计）'];
  if (!manifests.length) lines.push('（无批次记录；批次由 v0.10.0+ consolidate / maintain --dedup --apply 写入 .archive/audit-<日期>.jsonl）');
  const shown = manifests.slice(0, limit);
  for (const m of shown) {
    lines.push('- ' + m.batch + '  [' + (m.command || '?') + ' / ' + (m.mode || '') + ']  root=' + m.root);
  }
  if (manifests.length > shown.length) lines.push('（共 ' + manifests.length + ' 个批次，显示前 ' + shown.length + ' 个；--limit N 查看更多）');
  lines.push('回滚: yotta-memory consolidate --undo <batch>');
  return { error: false, text: lines.join('\n') };
}

function findBatchRecords(batch) {
  const out = [];
  for (const root of memoryRoots()) {
    for (const rec of collectAuditRecords(root)) {
      if (rec.batch === batch) out.push({ root: root, rec: rec });
    }
  }
  return out;
}

function consolidateUndoCore(batch, opts) {
  opts = opts || {};
  const lines = ['## yotta-memory consolidate --undo ' + batch];
  const recs = findBatchRecords(batch);
  if (!recs.length) return { error: true, text: '未找到批次 ' + batch + '（.archive/audit-<日期>.jsonl 无该 batch 记录）。' };
  const done = recs.some(function (x) { return x.rec.action === 'undo_done'; });
  if (done) return { error: false, text: lines.join('\n') + '\n批次 ' + batch + ' 已回滚过（幂等拒绝重复执行）。' };
  const force = !!opts.force;
  let err = null;
  // 1) 删除 consolidate 生成的摘要（含索引）
  for (const x of recs) {
    if (x.rec.action !== 'summary_create') continue;
    const fp = path.join(x.root, x.rec.file);
    try { if (resolveWithinRoot(x.root, fp) && fs.existsSync(fp)) fs.unlinkSync(fp); } catch (e) { err = err || ('摘要删除失败: ' + x.rec.file + ' ' + e.message); }
    if (resolveWithinRoot(x.root, fp)) removeIndexEntry(x.root, x.rec.file);
    lines.push('- 已删除摘要: ' + x.rec.file);
  }
  // 2) 合并回滚：keep 还原最早 before 影像；drop 从 .archive 归位
  const mergeKeeps = {};
  for (const x of recs) {
    if (x.rec.action !== 'merge') continue;
    const kf = x.rec.keepFile;
    if (!mergeKeeps[kf]) mergeKeeps[kf] = [];
    mergeKeeps[kf].push(x);
  }
  for (const kf of Object.keys(mergeKeeps)) {
    const xs = mergeKeeps[kf].sort(function (a, b) { return String(a.rec.ts || '').localeCompare(String(b.rec.ts || '')); });
    const first = xs[0];
    const keepFp = path.join(first.root, kf);
    const owner = ownerFromPrivatePath(first.root, keepFp);
    const before = first.rec.before || {};
    try {
      const patch = {};
      if (before.updated !== undefined) patch.updated = before.updated;
      if (before.tags !== undefined) patch.tags = JSON.stringify(before.tags);
      if (before.access_count !== undefined) patch.access_count = before.access_count;
      if (before.feedback_net !== undefined) patch.feedback_net = before.feedback_net;
      if (Object.keys(patch).length && fs.existsSync(keepFp)) {
        rewriteFrontmatter(keepFp, patch, first.root, owner);
        upsertIndexEntry(first.root, readEntry(keepFp, first.root));
        lines.push('- 已还原 keep: ' + kf);
      }
    } catch (e) { err = err || ('keep 还原失败: ' + kf + ' ' + e.message); }
    for (const x of xs) {
      const dropFp = path.join(x.root, x.rec.dropFile);
      const dropTo = path.join(x.root, x.rec.dropTo);
      if (!resolveWithinRoot(x.root, dropFp)) continue;
      if (fs.existsSync(dropFp) && !force) { err = err || ('归位冲突: ' + x.rec.dropFile + ' 已存在（--force 覆盖）'); continue; }
      try {
        if (fs.existsSync(dropFp)) fs.unlinkSync(dropFp);
        if (fs.existsSync(dropTo)) {
          fs.mkdirSync(path.dirname(dropFp), { recursive: true });
          fs.renameSync(dropTo, dropFp);
          upsertIndexEntry(x.root, readEntry(dropFp, x.root));
          lines.push('- 已归位 drop: ' + x.rec.dropFile);
        } else {
          err = err || ('drop 归档副本缺失: ' + x.rec.dropFile + '（无法归位）');
        }
      } catch (e2) { err = err || ('drop 归位失败: ' + x.rec.dropFile + ' ' + e2.message); }
    }
  }
  // 3) consolidate 归档原文归位
  for (const x of recs) {
    if (x.rec.action !== 'archive') continue;
    const to = path.join(x.root, x.rec.file);
    const from = path.join(x.root, x.rec.to);
    if (!resolveWithinRoot(x.root, to)) continue;
    if (fs.existsSync(to) && !force) { err = err || ('归位冲突: ' + x.rec.file + ' 已存在（--force 覆盖）'); continue; }
    try {
      if (fs.existsSync(to)) fs.unlinkSync(to);
      if (fs.existsSync(from)) {
        const archiveOwner = archiveOwnerFromPath(x.root, from);
        try {
          const marked = readMemoryText(x.root, from, archiveOwner);
          const clean = stripConsolidateMarker(marked, x.rec.had_trailing_newline !== false);
          if (clean !== marked) writeMemoryText(x.root, from, clean, archiveOwner);
        } catch (eMarker) {
          err = err || ('巩固标记剥离失败: ' + x.rec.file + ' ' + eMarker.message);
        }
        fs.mkdirSync(path.dirname(to), { recursive: true });
        fs.renameSync(from, to);
        upsertIndexEntry(x.root, readEntry(to, x.root));
        lines.push('- 已归位: ' + x.rec.file);
      } else {
        err = err || ('归档副本缺失: ' + x.rec.to + '（无法归位）');
      }
    } catch (e3) { err = err || ('归位失败: ' + x.rec.file + ' ' + e3.message); }
  }
  // 4) 幂等标记
  const roots = [];
  for (const x of recs) if (roots.indexOf(x.root) === -1) roots.push(x.root);
  for (const r of roots) appendAudit(r, 'audit', { ts: new Date().toISOString(), batch: batch, action: 'undo_done', note: err ? 'partial: ' + err : 'ok' });
  lines.push(err ? '- 结果: 部分失败 —— ' + err : '- 结果: 回滚完成（重复 --undo 会被幂等拒绝）');
  return { error: false, text: lines.join('\n') };
}

function pickSummaryTheme(group) {
  let best = group[0];
  for (const c of group) {
    if (c.e.confidence > best.e.confidence) best = c;
    else if (c.e.confidence === best.e.confidence && String(c.e.updated || '') > String(best.e.updated || '')) best = c;
  }
  let s = String(best.e.subject || '（无主题）').replace(/\s+/g, ' ').trim();
  if (s.length > 30) s = s.slice(0, 29) + '…';
  return s;
}

function sharedTag(a, b) {
  const ta = a.e.tags || [], tb = b.e.tags || [];
  for (const t of ta) if (tb.indexOf(t) !== -1) return true;
  return false;
}

function similarForConsolidate(a, b) {
  if (subjectsSimilar(a.e, b.e)) return true;
  if (jaccardTokens(a.e, b.e) >= 0.35) return true;
  if (sharedTag(a, b)) return true;
  return false;
}

function clusterConsolidateCandidates(cands) {
  const buckets = {};
  for (const c of cands) {
    const key = (c.scope === 'private' ? 'priv:' + c.owner : 'pub') + '|' + c.type;
    (buckets[key] = buckets[key] || []).push(c);
  }
  const groups = [];
  for (const key of Object.keys(buckets)) {
    const arr = buckets[key].slice().sort(function (a, b) { return String(a.e.created || '').localeCompare(String(b.e.created || '')); });
    const clusters = [];
    for (const c of arr) {
      let placed = false;
      for (const cl of clusters) {
        if (similarForConsolidate(c, cl[0])) { cl.push(c); placed = true; break; }
      }
      if (!placed) clusters.push([c]);
    }
    for (const cl of clusters) if (cl.length >= 2) groups.push(cl);
  }
  return groups;
}

// ---- v0.18.1 A9：相对日期绝对化 + 归档巩固标记 ----
const CONSOLIDATE_MARKER_PREFIX = '<!-- yotta-memory: consolidated to ';
const CONSOLIDATE_MARKER_RE = /<!-- yotta-memory: consolidated to [^\n]* -->\n?/;
function ymdPad(n) { return String(n).padStart(2, '0'); }
function ymdParse(s) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s || ''));
  if (!m) return null;
  const d = new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
  if (d.getFullYear() !== Number(m[1]) || d.getMonth() !== Number(m[2]) - 1 || d.getDate() !== Number(m[3])) return null;
  return d;
}
function ymdFormat(d) { return d.getFullYear() + '-' + ymdPad(d.getMonth() + 1) + '-' + ymdPad(d.getDate()); }
function ymdAdd(s, days) { const d = ymdParse(s); if (!d) return ''; d.setDate(d.getDate() + days); return ymdFormat(d); }
function ymdWeekRange(s) {
  const d = ymdParse(s);
  if (!d) return '';
  const mondayOffset = (d.getDay() + 6) % 7;
  const mon = new Date(d.getFullYear(), d.getMonth(), d.getDate() - mondayOffset);
  const sun = new Date(mon.getFullYear(), mon.getMonth(), mon.getDate() + 6);
  return ymdFormat(mon) + ' ~ ' + ymdFormat(sun);
}
function ymdMonthRange(s, offset) {
  const d = ymdParse(s);
  if (!d) return '';
  const first = new Date(d.getFullYear(), d.getMonth() + (offset || 0), 1);
  const last = new Date(first.getFullYear(), first.getMonth() + 1, 0);
  return ymdFormat(first) + ' ~ ' + ymdFormat(last);
}
function ymdYearRange(s, offset) {
  const d = ymdParse(s);
  if (!d) return '';
  const y = d.getFullYear() + (offset || 0);
  return y + '-01-01 ~ ' + y + '-12-31';
}
const RELATIVE_DATE_MAP = {
  '大前天': function (b) { return ymdAdd(b, -3); },
  '上上周': function (b) { return ymdWeekRange(ymdAdd(b, -7)); },
  '上个月': function (b) { return ymdMonthRange(b, -1); },
  '这个月': function (b) { return ymdMonthRange(b, 0); },
  '前天': function (b) { return ymdAdd(b, -2); },
  '昨天': function (b) { return ymdAdd(b, -1); },
  '昨日': function (b) { return ymdAdd(b, -1); },
  '今天': function (b) { return ymdAdd(b, 0); },
  '今日': function (b) { return ymdAdd(b, 0); },
  '明天': function (b) { return ymdAdd(b, 1); },
  '后天': function (b) { return ymdAdd(b, 2); },
  '上周': function (b) { return ymdWeekRange(ymdAdd(b, -7)); },
  '本周': function (b) { return ymdWeekRange(b); },
  '这周': function (b) { return ymdWeekRange(b); },
  '上月': function (b) { return ymdMonthRange(b, -1); },
  '本月': function (b) { return ymdMonthRange(b, 0); },
  '今年': function (b) { return ymdYearRange(b, 0); },
  '去年': function (b) { return ymdYearRange(b, -1); },
};
const RELATIVE_DATE_RE = /(大前天|上上周|上个月|这个月|前天|昨天|昨日|今天|今日|明天|后天|上周|本周|这周|上月|本月|今年|去年)(?![（(]\d{4}-\d{2}-\d{2})/g;
function absolutizeRelativeDates(text, baseYmd) {
  const s = String(text || '');
  if (!ymdParse(baseYmd)) return { text: s, count: 0 };
  let count = 0;
  const out = s.replace(RELATIVE_DATE_RE, function (word) {
    const fn = RELATIVE_DATE_MAP[word];
    if (!fn) return word;
    const rep = fn(baseYmd);
    if (!rep) return word;
    count += 1;
    return word + '（' + rep + '）';
  });
  return { text: out, count: count };
}
function consolidateMarkerText(summaryRel, batch) {
  return CONSOLIDATE_MARKER_PREFIX + summaryRel + ' | batch ' + batch + ' | ' + today() + ' -->';
}
function archiveOwnerFromPath(root, fp) {
  const seg = path.relative(root, fp).split(/[\\/]/);
  if (seg[0] === ARCHIVE_DIR && seg[1] === PRIVATE_DIR && seg[2]) return seg[2];
  return ownerFromPrivatePath(root, fp);
}
function appendConsolidateMarker(root, fp, summaryRel, batch, owner, opts) {
  if (opts && opts.markerFailForTest) throw new Error('marker fail for test');
  let text = readMemoryText(root, fp, owner);
  if (text.indexOf(CONSOLIDATE_MARKER_PREFIX) !== -1) return { appended: false, hadTrailingNewline: text.endsWith('\n') };
  const hadTrailingNewline = text.endsWith('\n');
  if (!hadTrailingNewline) text += '\n';
  text += consolidateMarkerText(summaryRel, batch) + '\n';
  writeMemoryText(root, fp, text, owner);
  return { appended: true, hadTrailingNewline: hadTrailingNewline };
}
function stripConsolidateMarker(text, hadTrailingNewline) {
  let out = String(text || '');
  if (out.indexOf(CONSOLIDATE_MARKER_PREFIX) === -1) return out;
  out = out.replace(CONSOLIDATE_MARKER_RE, '');
  if (hadTrailingNewline === false && out.endsWith('\n')) out = out.slice(0, -1);
  return out;
}

function applyConsolidateGroup(root, group, batch, period, opts) {
  const e0 = group[0];
  const type = e0.type;
  const owner = e0.scope === 'private' ? e0.owner : '';
  const theme = pickSummaryTheme(group);
  const subject = '周期摘要 ' + theme + '（' + period + ' 天窗）';
  const absDir = path.join(root, typeSubdir(type, owner));
  fs.mkdirSync(absDir, { recursive: true });
  const enc = isEncrypted(root) && owner ? ENC_SUFFIX : '';
  let fname = today() + '-' + nextSeq(absDir) + '.md' + enc;
  let fp = path.join(absDir, fname);
  let guard = 0;
  while (fs.existsSync(fp) && guard < 100) { guard++; fname = today() + '-' + nextSeq(absDir) + '.md' + enc; fp = path.join(absDir, fname); }
  const confs = group.map(function (c) { return c.e.confidence; });
  const maxConf = Math.max.apply(null, confs);
  const ws = group.map(function (c) { return c.e.weight || 1.0; }).sort(function (a, b) { return a - b; });
  const medW = ws.length % 2 ? ws[(ws.length - 1) / 2] : (ws[ws.length / 2 - 1] + ws[ws.length / 2]) / 2;
  const allTags = [];
  for (const c of group) for (const t of (c.e.tags || [])) if (allTags.indexOf(t) === -1) allTags.push(t);
  const tags = ['consolidate', 'summary'].concat(allTags);
  const createdDates = group.map(function (c) { return c.e.created; }).sort();
  const avgU = round3(group.reduce(function (s, c) { return s + c.utility; }, 0) / group.length);
  const bodyLines = ['# 周期摘要：' + theme, '', '> 生成: yotta-memory consolidate | 类型 ' + type + ' | 范围 ' + createdDates[0] + ' ~ ' + createdDates[createdDates.length - 1] + ' | ' + group.length + ' 条 | 平均效用 ' + avgU, '', '## 主题要点', ''];
  const sorted = group.slice().sort(function (a, b) { return String(b.e.updated || '').localeCompare(String(a.e.updated || '')); });
  let dateNormalized = 0;
  for (const c of sorted) {
    const norm = absolutizeRelativeDates(c.e.statement || '', c.e.created || c.e.updated || '');
    dateNormalized += norm.count;
    bodyLines.push('- [' + c.e.type + '] ' + (c.e.subject || '') + ': ' + norm.text);
  }
  bodyLines.push('', '## 溯源（原文已入 .archive，可 consolidate --undo <batch> 恢复）', '');
  for (const c of group) bodyLines.push('- ' + c.e.file + '（created ' + c.e.created + ' / confidence ' + c.e.confidence + ' / utility ' + round3(c.utility) + '）');
  const body = bodyLines.join('\n');
  const statement = '周期摘要 ' + theme + '：' + group.length + ' 条 ' + type + '（' + createdDates[0] + ' ~ ' + createdDates[createdDates.length - 1] + '，平均效用 ' + avgU + '）。要点与溯源见正文。';
  const meta = { type: type, subject: subject, statement: statement, confidence: round3(maxConf), created: today(), updated: today(), tags: tags, immutable: false, scope: owner ? 'private' : 'public', owner: owner, source: 'consolidate', weight: round3(medW), access_count: 0, last_accessed: '', feedback_net: 0 };
  writeMemoryText(root, fp, frontmatterToText(meta, body), owner);
  const summaryRel = relOf(root, fp);
  upsertIndexEntry(root, readEntry(fp, root));
  appendAudit(root, 'audit', { action: 'summary_create', ts: new Date().toISOString(), batch: batch, file: summaryRel, sourceFiles: group.map(function (c) { return c.e.file; }) });
  let moved = 0;
  let markersWritten = 0;
  let markerErrors = 0;
  for (const c of group) {
    const destDir = archiveDirFor(root, type, owner);
    fs.mkdirSync(destDir, { recursive: true });
    const dest = path.join(destDir, path.basename(c.e.file));
    fs.renameSync(path.join(root, c.e.file), dest);
    let marker = { appended: false, hadTrailingNewline: true };
    try {
      marker = appendConsolidateMarker(root, dest, summaryRel, batch, owner, opts);
      if (marker.appended) markersWritten += 1;
    } catch (e) {
      markerErrors += 1;
      appendAudit(root, 'audit', { action: 'marker_failed', ts: new Date().toISOString(), batch: batch, file: c.e.file, to: relOf(root, dest), error: String(e.message || e) });
    }
    removeIndexEntry(root, c.e.file);
    appendAudit(root, 'audit', { action: 'archive', ts: new Date().toISOString(), batch: batch, file: c.e.file, to: relOf(root, dest), type: type, owner: owner, utility: round3(c.utility), had_trailing_newline: marker.hadTrailingNewline === true });
    moved++;
  }
  return { made: 1, moved: moved, summaryRel: summaryRel, dateNormalized: dateNormalized, markersWritten: markersWritten, markerErrors: markerErrors };
}

// v0.18.0 A5：首次启用说明按 .archive 审计判定（不新建标记文件）。
function consolidateHasManifest(root) {
  const dir = path.join(root, ARCHIVE_DIR);
  let names;
  try { names = fs.readdirSync(dir); } catch (e) { return false; }
  for (const name of names) {
    if (!/^audit-\d{4}-\d{2}-\d{2}\.jsonl$/.test(name)) continue;
    let raw;
    try { raw = fs.readFileSync(path.join(dir, name), 'utf8'); } catch (e) { continue; }
    for (const line of raw.split('\n')) {
      if (!line.trim()) continue;
      let rec;
      try { rec = JSON.parse(line); } catch (e) { continue; }
      if (rec && rec.action === 'manifest' && rec.command === 'consolidate') return true;
    }
  }
  return false;
}
function consolidateFirstRunNotice() {
  return [
    '### 首次启用说明（只显示一次）',
    '- 保留期：原文移入 .archive/ 后一直保留，直到你显式 purge 或 undo；不会自动删除。',
    '- 检查：yotta-memory consolidate（默认 --propose，只出报告不写盘）。',
    '- 纠正：yotta-memory consolidate --undo <batch>。',
    '- 导出：yotta-memory export。',
    '- 停用：不再执行 --apply，或用 yotta-memory config set consolidate_min_age 99999 抬高门槛。',
    '- 删除：yotta-memory maintain --purge（对遗忘候选真删）。',
    '- AI 不得代替用户执行 --apply；--apply 需要确认，非交互必须显式加 --yes。',
  ];
}

function consolidateCore(opts) {
  opts = opts || {};
  if (opts.undo) return consolidateUndoCore(String(opts.undo), opts);
  if (opts.batches) return listBatchesCore(opts);
  const root = userRoot();
  if (!fs.existsSync(root)) return { error: false, text: '记忆库不存在。' };
  const apply = !!opts.apply;
  // v0.18.0 A5：--apply 是破坏性写入；非交互必须显式 --yes，交互确认在 cmdConsolidate 完成。
  if (apply && !opts.yes) {
    return {
      error: true,
      exitCode: 2,
      text: '拒绝: consolidate --apply 会移动原文并生成摘要（原文保留在 .archive/，可用 --undo 回滚）。请先运行 yotta-memory consolidate 审阅候选报告；交互式执行会要求输入确认串，非交互必须显式加 --yes。',
    };
  }
  const firstRunNotice = consolidateHasManifest(root) ? [] : consolidateFirstRunNotice();
  const selfAgent = resolveIdentity(opts).id;
  const unsafe = !!opts.unsafe;
  const cfg = loadConfig();
  const minAge = (opts.minAge !== undefined && opts.minAge !== null) ? opts.minAge : (parseInt(cfg.consolidate_min_age || '180', 10) || 180);
  const minIdle = (opts.minIdle !== undefined && opts.minIdle !== null) ? opts.minIdle : (parseInt(cfg.consolidate_min_idle || '90', 10) || 90);
  const maxUTmp = (opts.maxUtility !== undefined && opts.maxUtility !== null) ? parseFloat(opts.maxUtility) : parseFloat(cfg.consolidate_max_utility);
  const maxU = (maxUTmp > 0) ? maxUTmp : 0.6;
  const minGroup = (opts.minGroup !== undefined && opts.minGroup !== null) ? opts.minGroup : (parseInt(cfg.consolidate_min_group || '2', 10) || 2);
  const period = (opts.period !== undefined && opts.period !== null) ? opts.period : (parseInt(cfg.consolidate_period || '90', 10) || 90);
  const typeOnly = opts.type ? String(opts.type).toUpperCase() : '';
  const lines = ['## yotta-memory consolidate（周期摘要压缩）'];
  lines.push('- 模式: ' + (apply ? 'apply（执行压缩）' : 'propose（只出报告，未改动；确认后加 --apply --yes 执行）'));
  lines.push('- 候选: 天龄 ≥ ' + minAge + ' 天 ∧ 闲置 ≥ ' + minIdle + ' 天 ∧ utility ≤ ' + maxU + (typeOnly ? ' ∧ 仅类型 ' + typeOnly : '') + '；immutable / BOUND 豁免');
  lines.push('');
  const cands = [];
  const stats = { scan: 0, denied: 0, immutable: 0, bound: 0, typeSkip: 0, noCreated: 0, active: 0 };
  for (const fp of collectEntryFiles(root)) {
    stats.scan++;
    const owner = ownerFromPrivatePath(root, fp);
    const rel = relOf(root, fp);
    if (checkOwnerWritable(root, rel, selfAgent, unsafe)) { stats.denied++; continue; }
    let e;
    try { e = readEntry(fp, root); } catch (err) { stats.denied++; continue; }
    if (e.immutable) { stats.immutable++; continue; }
    if (e.type === 'BOUND') { stats.bound++; continue; }
    if (typeOnly && e.type !== typeOnly) { stats.typeSkip++; continue; }
    if (!e.created) { stats.noCreated++; continue; }
    const age = daysBetween(e.created, today());
    const last = e.last_accessed || e.created || '';
    const idle = last ? daysBetween(last, today()) : age;
    const u = utilityScore(e.meta);
    if (age < minAge || idle < minIdle || u > maxU) { stats.active++; continue; }
    cands.push({ e: e, owner: owner, type: e.type, age: age, idle: idle, utility: u, scope: e.scope === 'private' ? 'private' : 'public' });
  }
  const makeConsolidateGroup = function (g) {
    const type = g[0].type;
    const owner = g[0].scope === 'private' ? (g[0].owner || '') : '';
    const ages = g.map(function (c) { return c.age; });
    const theme = pickSummaryTheme(g);
    return {
      type: type,
      scope: g[0].scope === 'private' ? 'private' : 'public',
      owner: owner,
      count: g.length,
      age_min: Math.min.apply(null, ages),
      age_max: Math.max.apply(null, ages),
      avg_utility: round3(g.reduce(function (s, c) { return s + c.utility; }, 0) / g.length),
      theme: theme,
      summary_subject: '周期摘要 ' + theme + '（' + period + ' 天窗）',
      files: g.map(function (c) { return c.e.file; }),
      archive_to: path.relative(root, archiveDirFor(root, type, owner)).replace(/\\/g, '/'),
      date_normalized_preview: g.reduce(function (s, c) {
        return s + absolutizeRelativeDates(c.e.statement || '', c.e.created || c.e.updated || '').count;
      }, 0),
    };
  };
  const makeConsolidateReport = function (builtGroups, batch, extras) {
    return {
      schemaVersion: 1,
      mode: apply ? 'apply' : 'propose',
      batch: batch || '',
      root: root,
      thresholds: {
        min_age: minAge,
        min_idle: minIdle,
        max_utility: maxU,
        min_group: minGroup,
        period: period,
      },
      stats: stats,
      candidates: cands.length,
      groups: builtGroups.map(makeConsolidateGroup),
      date_normalized: (extras && extras.dateNormalized) || 0,
      markers_written: (extras && extras.markersWritten) || 0,
      marker_errors: (extras && extras.markerErrors) || 0,
      retention: '原文移入 .archive/ 后一直保留，直到显式 purge 或 undo。',
      rollback: batch
        ? ('yotta-memory consolidate --undo ' + batch)
        : 'yotta-memory consolidate --undo <batch>（执行后批次号见报告）',
    };
  };
  if (!cands.length) {
    lines.push('（无可压缩候选；扫描 ' + stats.scan + ' 条，跳过: 其它 owner/无密钥 ' + stats.denied + ' / immutable ' + stats.immutable + ' / BOUND ' + stats.bound + ' / 类型过滤 ' + stats.typeSkip + ' / 无 created ' + stats.noCreated + ' / 不够老或仍活跃 ' + stats.active + '）');
    if (firstRunNotice.length) { lines.push(''); lines.push.apply(lines, firstRunNotice); }
    return { error: false, text: lines.join('\n'), report: makeConsolidateReport([], '') };
  }
  const groups = clusterConsolidateCandidates(cands);
  lines.push('候选 ' + cands.length + ' 条（扫描 ' + stats.scan + '，跳过: 其它 owner/无密钥 ' + stats.denied + ' / immutable ' + stats.immutable + ' / BOUND ' + stats.bound + ' / 类型过滤 ' + stats.typeSkip + ' / 无 created ' + stats.noCreated + ' / 不够老或仍活跃 ' + stats.active + '）');
  if (!groups.length) {
    lines.push('');
    lines.push('（无可归纳组：同主题聚类 ≥ ' + minGroup + ' 条才生成周期摘要；零散单条旧记忆请用 maintain --apply 归档）');
    if (firstRunNotice.length) { lines.push(''); lines.push.apply(lines, firstRunNotice); }
    return { error: false, text: lines.join('\n'), report: makeConsolidateReport([], '') };
  }
  lines.push('');
  lines.push('### 周期摘要组（' + groups.length + ' 组，每组将生成摘要 1 条 + 归档原文 N 条）');
  for (const g of groups) {
    const type = g[0].type;
    const scopeLabel = g[0].scope === 'private' ? ('private/' + g[0].owner) : 'public';
    const ages = g.map(function (c) { return c.age; });
    const minA = Math.min.apply(null, ages), maxA = Math.max.apply(null, ages);
    const avgU = round3(g.reduce(function (s, c) { return s + c.utility; }, 0) / g.length);
    lines.push('- [' + type + '] 主题: ' + pickSummaryTheme(g) + '（' + scopeLabel + '，' + g.length + ' 条，' + minA + '~' + maxA + ' 天，平均效用 ' + avgU + '）' + (type === 'COMMIT' ? '  ⚠️ COMMIT 承诺/任务类，请确认' : ''));
    const datePreview = g.reduce(function (s, c) {
      return s + absolutizeRelativeDates(c.e.statement || '', c.e.created || c.e.updated || '').count;
    }, 0);
    lines.push('    → 将生成 周期摘要 ' + pickSummaryTheme(g) + '（' + period + ' 天窗），日期归一预览 ' + datePreview + ' 处，原文归档到 ' + path.relative(root, archiveDirFor(root, type, g[0].owner || '')).replace(/\\/g, '/'));
    for (const c of g) lines.push('    · ' + c.e.file + ' — ' + String(c.e.subject || '').slice(0, 32) + ': ' + String(c.e.statement || '').slice(0, 60));
  }
  if (!apply) {
    lines.push('');
    lines.push('- 保留期: 原文移入 .archive/ 后一直保留，直到显式 purge 或 undo。');
    lines.push('- 回滚: 执行后可用 yotta-memory consolidate --undo <batch> 恢复。');
    lines.push('未执行任何变更。确认后加 --apply（非交互再加 --yes）执行。');
    if (firstRunNotice.length) { lines.push(''); lines.push.apply(lines, firstRunNotice); }
    return { error: false, text: lines.join('\n'), report: makeConsolidateReport(groups, '') };
  }
  const guard = destructiveGuardCore({
    root: root,
    action: 'consolidate --apply',
    snapshotDir: opts.snapshotDir,
    backupDir: opts.backupDir,
    allowSameVolumeForTest: opts.allowSameVolumeForTest,
    sameVolumeFn: opts.sameVolumeFn,
    now: opts.now,
  });
  if (guard.error) return { error: true, text: guard.text };
  const batch = newBatchId();
  appendAudit(root, 'audit', { action: 'manifest', ts: new Date().toISOString(), batch: batch, command: 'consolidate', mode: 'apply', root: root, active_before: collectEntryFiles(root).length, undone: false });
  lines.push('');
  lines.push('- 事务快照: ' + guard.snapshot.id);
  lines.push('- 批次: ' + batch + '（审计 .archive/audit-<日期>.jsonl；回滚: yotta-memory consolidate --undo ' + batch + '）');
  let made = 0, moved = 0, dateNormalized = 0, markersWritten = 0, markerErrors = 0;
  for (const g of groups) {
    const res = applyConsolidateGroup(root, g, batch, period, opts);
    made += res.made; moved += res.moved;
    dateNormalized += res.dateNormalized; markersWritten += res.markersWritten; markerErrors += res.markerErrors;
    lines.push('- 已生成摘要 ' + res.summaryRel + '（归档原文 ' + res.moved + ' 条）');
  }
  appendAudit(root, 'audit', { action: 'batch_done', ts: new Date().toISOString(), batch: batch, command: 'consolidate', summaries: made, archived: moved, active_after: collectEntryFiles(root).length });
  lines.push('- 完成: 生成摘要 ' + made + ' 条 / 原文归档 ' + moved + ' 条');
  lines.push('- 日期归一: ' + dateNormalized + ' 处；巩固标记: ' + markersWritten + ' 条（失败 ' + markerErrors + '）');
  if (firstRunNotice.length) { lines.push(''); lines.push.apply(lines, firstRunNotice); }
  return { error: false, text: lines.join('\n'), report: makeConsolidateReport(groups, batch, { dateNormalized: dateNormalized, markersWritten: markersWritten, markerErrors: markerErrors }) };
}

async function cmdConsolidate(opts) {
  // v0.18.0 A5：交互式确认串（X 组 / Y 条）；非交互明确拒绝并提示 --yes。
  if (opts.apply && !opts.yes) {
    if (!process.stdin.isTTY) {
      const blocked = consolidateCore(opts);
      console.log(blocked.text);
      process.exit(blocked.exitCode || 2);
    }
    const plan = consolidateCore(Object.assign({}, opts, { apply: false }));
    const groups = (plan.report && plan.report.groups) || [];
    const items = groups.reduce(function (s, g) { return s + g.count; }, 0);
    if (groups.length) {
      const token = groups.length + ' 组 / ' + items + ' 条';
      const typed = await promptLine('即将把 ' + token + ' 压缩为摘要（原文保留在 .archive/，可 --undo 回滚）。输入「' + token + '」确认: ');
      if (typed === null || String(typed).trim() !== token) {
        console.log('已取消，未做任何改动。');
        process.exit(2);
      }
    }
    opts = Object.assign({}, opts, { yes: true });
  }
  const r = consolidateCore(opts);
  if (opts.json && r.report) console.log(JSON.stringify(r.report, null, 2));
  else console.log(r.text);
  if (r.exitCode) process.exit(r.exitCode);
  if (r.error) process.exit(2);
}

// ---- 近重复自动合并：置信度分档 + --apply 批量执行（maintain --dedup 增强）----
function dupScorePair(a, b) {
  const jac = jaccardTokens(a, b);
  const sa = String(a.subject || '').toLowerCase(), sb = String(b.subject || '').toLowerCase();
  let subSim = 0;
  if (sa && sb) { if (sa === sb) subSim = 1; else subSim = Math.max(0, 1 - editDistance(sa, sb) / 3); }
  const typeEq = (a.type === b.type) ? 1 : 0;
  const scopeEq = (String(a.scope || '') === String(b.scope || '') && String(a.owner || '') === String(b.owner || '')) ? 1 : 0;
  let score = 0.45 * jac + 0.25 * subSim + 0.15 * typeEq + 0.15 * scopeEq;
  const la = String(a.statement || '').length, lb = String(b.statement || '').length;
  const mn = Math.min(la, lb), mx = Math.max(la, lb);
  if (mx > 0 && mn / mx < 0.3) score = 0;
  return round3(score);
}

function groupDupScore(g) {
  if (g.length < 2) return 0;
  let mn = 2, sum = 0, n = 0;
  for (let i = 0; i < g.length; i++) for (let j = i + 1; j < g.length; j++) {
    const sc = dupScorePair(g[i], g[j]);
    if (sc < mn) mn = sc;
    sum += sc; n++;
  }
  return round3(n ? (mn + sum / n) / 2 : 0);
}

function dupGroupMergeable(g) {
  if (g.length < 2) return false;
  const t = g[0].type, sc = String(g[0].scope || ''), ow = String(g[0].owner || '');
  for (const e of g) {
    if (e.type !== t || String(e.scope || '') !== sc || String(e.owner || '') !== ow) return false;
    if (e.immutable || e.type === 'BOUND') return false;
  }
  return true;
}

function autoMergePairCore(root, keepE, dropE, batch, selfAgent, unsafe) {
  for (const f of [keepE.file, dropE.file]) {
    const deny = checkOwnerWritable(root, f, selfAgent, unsafe);
    if (deny) return { error: true, text: deny };
  }
  const keepFp = path.join(root, keepE.file);
  const dropFp = path.join(root, dropE.file);
  const keepOwner = ownerFromPrivatePath(root, keepFp);
  const dropOwner = ownerFromPrivatePath(root, dropFp);
  let kMeta, dMeta;
  try {
    kMeta = parseFrontmatter(readMemoryText(root, keepFp, keepOwner)).meta;
    dMeta = parseFrontmatter(readMemoryText(root, dropFp, dropOwner)).meta;
  } catch (e) { return { error: true, text: '读取失败: ' + e.message }; }
  const before = { updated: kMeta.updated || '', tags: parseTags(kMeta.tags), access_count: parseInt(kMeta.access_count || '0', 10) || 0, feedback_net: feedbackNetOf(kMeta) };
  const mergedTags = [];
  for (const t of parseTags(kMeta.tags).concat(parseTags(dMeta.tags))) if (mergedTags.indexOf(t) === -1) mergedTags.push(t);
  const patch = {
    updated: today(),
    tags: JSON.stringify(mergedTags),
    access_count: before.access_count + (parseInt(dMeta.access_count || '0', 10) || 0),
    feedback_net: round3(before.feedback_net + feedbackNetOf(dMeta))
  };
  rewriteFrontmatter(keepFp, patch, root, keepOwner);
  upsertIndexEntry(root, readEntry(keepFp, root));
  const destDir = archiveDirFor(root, String(dMeta.type || 'FACT').toUpperCase(), dropOwner);
  fs.mkdirSync(destDir, { recursive: true });
  const dest = path.join(destDir, path.basename(dropFp));
  fs.renameSync(dropFp, dest);
  removeIndexEntry(root, dropE.file);
  appendAudit(root, 'audit', { ts: new Date().toISOString(), batch: batch, action: 'merge', keepFile: keepE.file, dropFile: dropE.file, dropTo: relOf(root, dest), before: before, after: { updated: patch.updated, tags: mergedTags, access_count: patch.access_count, feedback_net: patch.feedback_net } });
  return { error: false, text: '已合并 ' + dropE.file + ' -> ' + keepE.file };
}

function appendDedupBlock(lines, root, opts) {
  const apply = !!opts.apply;
  const selfAgent = resolveIdentity(opts).id;
  const unsafe = !!opts.unsafe;
  lines.push('');
  lines.push('### 重复候选与置信度（--dedup' + (apply ? ' --apply 自动合并' : '') + '）');
  const entries = ensureIndex(root);
  const groups = [];
  const used = new Set();
  for (let i = 0; i < entries.length; i++) {
    if (used.has(i)) continue;
    const g = [entries[i]];
    used.add(i);
    for (let j = i + 1; j < entries.length; j++) {
      if (used.has(j)) continue;
      if (subjectsSimilar(entries[i], entries[j]) && jaccardTokens(entries[i], entries[j]) >= 0.5) {
        g.push(entries[j]); used.add(j);
      }
    }
    if (g.length > 1) groups.push(g);
  }
  if (!groups.length) { lines.push('（无重复候选）'); return; }
  const plans = [];
  for (const g of groups) {
    const score = groupDupScore(g);
    const mergeable = dupGroupMergeable(g) && score >= 0.85;
    plans.push({ g: g, score: score, mergeable: mergeable });
  }
  const high = plans.filter(function (p) { return p.mergeable; });
  const suggest = plans.filter(function (p) { return !p.mergeable && p.score >= 0.65; });
  for (const p of plans) {
    const tag = p.mergeable ? '可自动合并' : (p.score >= 0.65 ? '建议手动合并' : '低置信（忽略）');
    lines.push('- 置信度 ' + p.score + ' [' + tag + '] 组: ' + p.g.map(function (e) { return e.file; }).join(' | '));
    lines.push('  ' + p.g.map(function (e) { return e.subject + ': ' + String(e.statement || '').slice(0, 60); }).join(' / '));
  }
  if (!apply) {
    lines.push('  执行: yotta-memory maintain --dedup --apply（自动合并高置信组，写入批次审计可回滚）；手动: maintain --merge <A>,<B>');
    return;
  }
  if (!high.length) { lines.push('  （无高置信可自动合并组）'); return; }
  const batch = newBatchId();
  appendAudit(root, 'audit', { action: 'manifest', ts: new Date().toISOString(), batch: batch, command: 'dedup-merge', mode: 'apply', root: root, undone: false });
  let merged = 0;
  for (const p of high) {
    const arr = p.g.slice().sort(function (a, b) {
      const ca = a.confidence - b.confidence;
      if (ca !== 0) return b.confidence - a.confidence;
      return String(b.updated || '').localeCompare(String(a.updated || ''));
    });
    const keep = arr[0];
    for (let k = 1; k < arr.length; k++) {
      const r = autoMergePairCore(root, keep, arr[k], batch, selfAgent, unsafe);
      lines.push('- ' + r.text + (r.error ? '（失败）' : ''));
      if (!r.error) merged++;
    }
  }
  appendAudit(root, 'audit', { action: 'batch_done', ts: new Date().toISOString(), batch: batch, command: 'dedup-merge', merged: merged });
  lines.push('- 批次: ' + batch + '（自动合并 ' + merged + ' 条；回滚: yotta-memory consolidate --undo ' + batch + '）');
}


// ---- usage / main ----
function cmdRuntimeInstall(arg, opts) {
  let result;
  if (opts.fromCurrent) result = runtimeInstallFromCurrent(opts);
  else if (!arg) {
    console.error('runtime install 需要 <tarball|版本>，或使用 --from-current。');
    process.exit(2);
  } else if (/\.tgz$/i.test(arg) || fs.existsSync(path.resolve(arg))) {
    result = runtimeInstallTarball(arg, '', opts);
  } else {
    result = runtimeInstallVersion(arg, opts);
  }
  console.log(result.text);
  if (result.error) process.exit(2);
}
function cmdRuntimeUse(version, opts) {
  const result = runtimeUseCore(version, opts);
  console.log(result.text);
  if (result.error) process.exit(2);
}
function cmdRuntimeRollback(opts) {
  const result = runtimeRollbackCore(opts);
  console.log(result.text);
  if (result.error) process.exit(2);
}
function cmdRuntimeStatus() {
  console.log(runtimeStatusCore().text);
}
function cmdRuntimeList() {
  console.log(runtimeListCore().text);
}
function helpDisplayWidth(text) {
  let width = 0;
  for (const ch of String(text)) {
    const cp = ch.codePointAt(0);
    width += (
      (cp >= 0x1100 && cp <= 0x115f) ||
      (cp >= 0x2e80 && cp <= 0xa4cf) ||
      (cp >= 0xac00 && cp <= 0xd7a3) ||
      (cp >= 0xf900 && cp <= 0xfaff) ||
      (cp >= 0xfe30 && cp <= 0xfe6f) ||
      (cp >= 0xff00 && cp <= 0xff60) ||
      (cp >= 0xffe0 && cp <= 0xffe6)
    ) ? 2 : 1;
  }
  return width;
}
function helpPad(text, width) {
  return text + ' '.repeat(Math.max(0, width - helpDisplayWidth(text)));
}
function helpText(item) {
  const parts = [];
  // v0.17.3：去掉逐项重复的「做什么：」前缀，直接写说明；「什么时候用 / 注意」保留。
  if (item.what) parts.push(item.what);
  if (item.when) parts.push('什么时候用：' + item.when);
  if (item.caution) parts.push('注意：' + item.caution);
  return parts.join('；');
}
function helpOptionLabel(option) {
  return option.flag + (option.arg ? ' ' + option.arg : '');
}
function renderHelp(model) {
  const commands = [];
  for (const group of model) for (const command of group.commands) commands.push(command);

  let optionCol = 0;
  for (const command of commands) {
    for (const option of command.options || []) optionCol = Math.max(optionCol, helpDisplayWidth(helpOptionLabel(option)));
    for (const sub of command.subcommands || []) {
      for (const option of sub.options || []) optionCol = Math.max(optionCol, helpDisplayWidth(helpOptionLabel(option)));
    }
  }
  optionCol += 2;

  const lines = [
    'yotta-memory v' + VERSION + ' — 元忆：有权限边界的文件式智能体记忆',
    '',
    '用法:',
    '  yotta-memory <命令> [选项]',
    '  yotta-memory --help    显示这份完整帮助',
    '  yotta-memory --version 显示版本',
    '',
  ];
  for (const group of model) {
    lines.push(group.group + ':');
    for (const command of group.commands) {
      lines.push('  ' + command.name + '  ' + helpText(command));
      lines.push('    用法: yotta-memory ' + command.usage);
      for (const sub of command.subcommands || []) {
        lines.push('    ' + (sub.usage || sub.name) + '  ' + helpText(sub));
        for (const option of sub.options || []) {
          lines.push('      ' + helpPad(helpOptionLabel(option), optionCol) + helpText(option));
        }
      }
      for (const option of command.options || []) {
        lines.push('    ' + helpPad(helpOptionLabel(option), optionCol) + helpText(option));
      }
    }
    lines.push('');
  }
  lines.push('类型: FACT(公共共享) / PREF(偏好) / BOUND(边界) / COMMIT(承诺)');
  lines.push('环境变量: YOTTA_MEMORY_HOME 临时覆盖用户级位置; 身份不再读取 env；CLI 用 --agent + --agent-key/--agent-key-file，stdio MCP 用 --agent-id + --agent-key-file，HTTP MCP 用请求头');
  lines.push('隔离: 公共 FACT 在 facts/；私密 PREF/BOUND/COMMIT 物理分目录 private/<agent_id>/<type>/，禁止 shell 直读写记忆库，一律走本命令');
  lines.push('远端接入: MCP url http://<主机IP>:8787/mcp；请求头 Authorization: Bearer <token> + X-Agent-Id: <id> + X-Agent-Key: <agent_key>');
  return lines.join('\n');
}
function usage() {
  console.log(renderHelp(HELP_MODEL));
}
async function main() {
  const args = process.argv.slice(2);
  if (!args.length) { usage(); return; }
  const opts = {};
  const positional = [];
  const valueOpts = CLI_VALUE_OPTS;
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--version' || a === '-v') { console.log(VERSION); return; }
    if (a === '--help' || a === '-h') { usage(); return; }
    if (a === '--project') opts.project = true;
    else if (a === '--all') opts.all = true;
    else if (a === '--unsafe') opts.unsafe = true;
    else if (a === '--no-auth') opts.noAuth = true;
    else if (a === '--stdio') opts.stdio = true;
    else if (a === '--onstart') opts.onstart = true;
    else if (a === '--from-current') opts.fromCurrent = true;
    else if (a === '--restart') opts.restart = true;
    else if (a === '--force') opts.force = true;
    else if (a === '--attach') opts.attach = true;
    else if (a === '--allow-same-volume') opts.allowSameVolume = true;
    else if (a === '--verify') opts.verify = true;
    else if (a === '--no-hint') opts.noHint = true;
    else if (a === '--encrypt') opts.encrypt = true;
    else if (a === '--no-encrypt') opts.noEncrypt = true;
    else if (a === '--password-stdin') opts.passwordStdin = true;
    else if (a === '--json') opts.json = true;
    else if (a === '--manual') opts.manual = true;
    else if (a === '--skip-schedule') opts.skipSchedule = true;
    else if (a === '--useful') opts.useful = true;
    else if (a === '--useless') opts.useless = true;
    else if (a === '--undo') opts.undo = true;
    else if (a === '--dry-run') opts.dryRun = true;
    else if (a === '--apply') opts.apply = true;
    else if (a === '--purge') opts.purge = true;
    else if (a === '--dedup') opts.dedup = true;
    else if (a === '--batches') opts.batches = true;
    else if (a === '--explain') opts.explain = true;
    else if (a === '--semantic') opts.semantic = true;
    else if (a === '--runtime') opts.runtime = true;
    else if (a === '--ablate') opts.ablate = true;
    else if (a === '--timing') opts.timing = true;
    else if (a === '--baseline') opts.baseline = true;
    else if (a === '--probe') opts.probe = true;
    else if (a === '--quarantine') opts.quarantine = true;
    else if (a === '--restore') opts.restore = true;
    else if (a === '--yes') opts.yes = true;
    else if (a === '--keep-memories') opts.keepMemories = true;
    else if (a === '--keep-identity') opts.keepIdentity = true;
    else if (a === '--no-usage') opts.noUsage = true;
    else if (a === '--capacity') opts.capacity = true;
    else if (a === '--rules') opts.rules = true;
    else if (a === '--propose') opts.propose = true;
    else if (a === '--audit') opts.audit = true;
    else if (a === '--stats') opts.stats = true;
    else if (a === '--include-flat') opts.includeFlat = true;
    else if (a === '--no-policy') opts.noPolicy = true;
    else if (a === '--policy-candidates') opts.policyCandidates = true;
    else if (valueOpts.has(a)) {
      const v = args[++i];
      if (a === '--type') opts.type = v;
      else if (a === '--limit') opts.limit = parseInt(v, 10) || 50;
      else if (a === '--days') opts.days = parseInt(v, 10) || 180;
      else if (a === '--threshold') opts.threshold = parseFloat(v);
      else if (a === '--out') opts.out = v;
      else if (a === '--owner') opts.owner = v;
      else if (a === '--agent') opts.agent = v;
      else if (a === '--agent-id') opts.agentId = v;
      else if (a === '--agent-key') opts.agentKey = v;
      else if (a === '--agent-key-file') opts.agentKeyFile = v;
      else if (a === '--scope') opts.scope = v;
      else if (a === '--host') opts.host = v;
      else if (a === '--port') opts.port = parseInt(v, 10) || 8787;
      else if (a === '--dir') opts.dir = v;
      else if (a === '--name') opts.name = v;
      else if (a === '--user') opts.user = v;
      else if (a === '--relationship') opts.relationship = v;
      else if (a === '--source') opts.source = v;
      else if (a === '--weight') opts.weight = parseFloat(v);
      else if (a === '--budget') opts.budget = parseInt(v, 10) || 0;
      else if (a === '--password') opts.password = v;
      else if (a === '--new-password') opts.newPassword = v;
      else if (a === '--recovery-key') opts.recoveryKey = v;
      else if (a === '--recovery-key-out') opts.recoveryKeyOut = v;
      else if (a === '--reason') opts.reason = v;
      else if (a === '--merge') opts.merge = v;
      else if (a === '--model') opts.model = v;
      else if (a === '--subject') opts.subject = v;
      else if (a === '--embedding') opts.embedding = v;
      else if (a === '--focus') opts.focus = v;
      else if (a === '--embedding-timeout') opts.embeddingTimeout = parseInt(v, 10) || 3000;
      else if (a === '--min-age') opts.minAge = parseInt(v, 10) || 0;
      else if (a === '--min-idle') opts.minIdle = parseInt(v, 10) || 0;
      else if (a === '--max-utility') opts.maxUtility = parseFloat(v);
      else if (a === '--min-group') opts.minGroup = parseInt(v, 10) || 0;
      else if (a === '--period') opts.period = parseInt(v, 10) || 0;
      else if (a === '--to') opts.to = v;
      else if (a === '--plugin-data') opts.pluginData = v;
      else if (a === '--id') opts.id = v;
      else if (a === '--time') opts.time = v;
      else if (a === '--tools') opts.toolProfile = v;
      else if (a === '--profile') opts.profile = v;
      else if (a === '--mcp-config') opts.mcpConfigPaths = (opts.mcpConfigPaths || []).concat(v);
      else if (a === '--skill-dir') opts.skillDirs = (opts.skillDirs || []).concat(v);
      else if (a === '--year') opts.years = (opts.years || []).concat(v);
      else if (a === '--evalset') opts.evalset = v;
      else if (a === '--k') opts.k = parseInt(v, 10);
      else if (a === '--seed') opts.seed = parseInt(v, 10);
      else if (a === '--bootstrap') opts.bootstrap = parseInt(v, 10);
      else if (a === '--gate') opts.gate = (opts.gate || []).concat(v);
      else if (a === '--against') opts.against = v;
      else if (a === '--template') opts.template = v;
      else if (a === '--path') opts.path = v;
      else if (a === '--from') opts.from = v;
      else if (a === '--from-plan') opts.fromPlan = v;
      else if (a === '--batch') opts.batch = v;
    } else if (a.startsWith('--')) {
      if (a === '--query') {
        console.error('未知选项: --query。recall/search 的关键词是位置参数：yotta-memory recall [关键词]');
        process.exit(2);
      }
      console.error('未知选项: ' + a);
      process.exit(2);
    } else {
      positional.push(a);
    }
  }
  if (opts.toolProfile !== undefined) {
    opts.toolProfile = String(opts.toolProfile).trim().toLowerCase();
    if (opts.toolProfile !== 'core' && opts.toolProfile !== 'full') {
      console.error('工具分组必须是 core 或 full（例如：yotta-memory serve --stdio --tools core）。');
      process.exit(2);
    }
  }
  const first = positional[0];
  const rest = positional.slice(1);
  if (first === 'remember' && opts.type) {
    console.error('位置参数用法：yotta-memory remember <type> <subject> <statement>。--type 仅用于 recall/maintain/consolidate 等筛选，不是 remember 的类型参数。');
    process.exit(2);
  }
  if (first === 'remember' && rest.length < 3) {
    console.error('位置参数不足：yotta-memory remember <type> <subject> <statement>');
    process.exit(2);
  }
  if (first === 'serve' && opts.profile) {
    const applied = applyServeProfile(opts.profile);
    if (applied.error) {
      console.error('服务 profile 启动失败: ' + applied.text);
      process.exit(2);
    }
    opts.profile = applied.profilePath;
    if (opts.host === undefined && applied.profile.host) opts.host = applied.profile.host;
    if (opts.port === undefined && applied.profile.port) opts.port = applied.profile.port;
  }
  const runtimeIdentity = resolveIdentity(opts);
  setRuntimeAgent(runtimeIdentity.error ? '' : runtimeIdentity.id, runtimeIdentity.error ? '' : runtimeIdentity.agentKey);
  switch (first) {
    case 'init': await cmdInit(opts); break;
    case 'whoami': cmdWhoami(opts); break;
    case 'iam': cmdIam(rest[0], opts); break;
    case 'identity': {
      const sub = rest[0];
      if (sub === 'remove') await cmdIdentityRemove(rest[1], opts);
      else { console.error('identity 子命令: remove <id> [--dry-run] [--yes] [--keep-memories] [--keep-identity] [--password <口令> | --recovery-key <钥匙>]'); process.exit(2); }
      break;
    }
    case 'config': {
      const sub = rest[0];
      if (sub === 'set') cmdConfigSet(rest[1], rest[2]);
      else if (sub === 'get') cmdConfigGet(opts);
      else { console.error('config 子命令: set <键> <值>（memory_home / embedding_cmd / embedding_timeout / maintain_* / consolidate_*）/ get'); process.exit(2); }
      break;
    }
    case 'remember': cmdRemember(rest[0], rest[1], rest[2], opts); break;
    case 'recall': cmdRecall(rest[0] || null, opts); break;
    case 'search': cmdRecall(rest[0] || null, opts); break;
    case 'feedback': cmdFeedback(rest[0], opts); break;
    case 'explain': cmdExplain(rest[0], opts); break;
    case 'bench': cmdBench(opts); break;
    case 'scan': await cmdScan(opts); break;
    case 'maintain': cmdMaintain(opts); break;
    case 'distill': cmdDistill(opts); break;
    case 'consolidate': if (opts.undo === true && rest.length) opts.undo = rest[0]; await cmdConsolidate(opts); break;
    case 'forget': cmdForget(rest[0], opts); break;
    case 'rename': cmdRename(rest[0], rest[1], opts); break;
    case 'archive': cmdArchive(opts); break;
    case 'backup': {
      const sub = rest[0];
      if (sub === 'volumes') cmdBackupVolumes(opts);
      else if (sub === 'setup') cmdBackupSetup(opts);
      else if (sub === 'status') cmdBackupStatus(opts);
      else if (sub === 'ensure-daily') cmdBackupEnsureDaily(opts);
      else if (sub === 'schedule') cmdBackupSchedule(rest[1], opts);
      else if (sub === 'create') cmdBackupCreate(opts);
      else if (sub === 'list') cmdBackupList(opts);
      else if (sub === 'doctor') cmdBackupDoctor(opts);
      else if (sub === 'restore') cmdBackupRestore(rest[1] || opts.id, opts);
      else if (sub === 'drill') await cmdBackupDrill(rest[1] || opts.id, opts);
      else { console.error('backup 子命令: volumes / setup / status / ensure-daily / schedule / create / list / doctor / restore <id> --to <目录> / drill'); process.exit(2); }
      break;
    }
    case 'reindex': cmdReindex(); break;
    case 'index': cmdIndex(opts); break;
    case 'layout': cmdLayout(rest[0], opts); break;
    case 'doctor': cmdDoctor(opts); break;
    case 'profile': cmdProfile(opts); break;
    case 'context': cmdContext(opts); break;
    case 'export': cmdExport(opts.out); break;
    case 'import': cmdImport(rest[0]); break;
    case 'token': {
      const sub = rest[0];
      if (sub === 'new') cmdTokenNew(opts.agent, opts);
      else if (sub === 'list') cmdTokenList();
      else if (sub === 'revoke') cmdTokenRevoke(opts.agent);
      else { console.error('token 子命令: new --agent <id> / list / revoke --agent <id>'); process.exit(2); }
      break;
    }
    case 'migrate': await cmdMigrate(opts); break;
    case 'view': await cmdView(opts); break;
    case 'reset-password': await cmdResetPassword(opts); break;
    case 'key': {
      const sub = rest[0];
      if (sub === 'list') cmdKeyList();
      else if (sub === 'bind' || sub === 'rotate') await cmdKeyBind(rest[1], opts);
      else if (sub === 'authorize') await cmdKeyAuthorize(rest[1], opts);
      else if (sub === 'claim') cmdKeyClaim(rest[1], opts);
      else if (sub === 'status') cmdKeyStatus(rest[1], opts);
      else if (sub === 'revoke') cmdKeyRevoke(rest[1]);
      else { console.error('key 子命令: list / bind <id> / rotate <id> / claim <id> --to <AI_HOME> / status <id> / revoke <id>'); process.exit(2); }
      break;
    }
    case 'runtime': {
      const sub = rest[0];
      if (sub === 'install') cmdRuntimeInstall(rest[1], opts);
      else if (sub === 'use') cmdRuntimeUse(rest[1], opts);
      else if (sub === 'rollback') cmdRuntimeRollback(opts);
      else if (sub === 'status') cmdRuntimeStatus();
      else if (sub === 'list') cmdRuntimeList();
      else { console.error('runtime 子命令: list / install <tarball|版本> [--from-current] [--force] / use <版本> [--restart] / rollback [--restart] / status'); process.exit(2); }
      break;
    }
    case 'serve': cmdServe(opts); break;
    case 'lan': {
      const sub = rest[0];
      if (sub === 'enable') cmdLanEnable(opts);
      else if (sub === 'disable') cmdLanDisable();
      else if (sub === 'status') cmdLanStatus();
      else { console.error('lan 子命令: enable [--onstart] / disable / status'); process.exit(2); }
      break;
    }
    default:
      if (!first) { usage(); return; }
      console.error('未知命令: ' + first);
      usage();
      process.exit(2);
  }
}

if (require.main === module) { main().catch(function (e) { console.error('错误: ' + (e && e.message ? e.message : String(e))); console.error('修复建议: 若与记忆库/密钥/权限有关，请检查 memory_home 路径、主口令与恢复钥匙，或运行 yotta-memory config get 确认位置；仍无法解决请把上面的错误信息反馈给开发者。'); process.exit(2); }); }
module.exports = {
  VERSION: VERSION,
  HELP_MODEL: HELP_MODEL,
  CONFIG_VALUE_KEYS: CONFIG_VALUE_KEYS,
  CONFIG_KEY_HELP: CONFIG_KEY_HELP,
  VIEW_HELP_QUICK: VIEW_HELP_QUICK,
  CLI_FLAG_OPTS: CLI_FLAG_OPTS,
  CLI_VALUE_OPTS: CLI_VALUE_OPTS,
  renderHelp: renderHelp,
  userRoot: userRoot,
  projectRoot: projectRoot,
  memoryRoots: memoryRoots,
  rememberCore: rememberCore,
  recallCore: recallCore,
  profileCore: profileCore,
  contextCore: contextCore,
  contextAuditCore: contextAuditCore,
  applyMemoryHook: applyMemoryHook,
  importanceScore: importanceScore,
  usageSettings: usageSettings,
  usageTotals: usageTotals,
  usagePatchForMeta: usagePatchForMeta,
  applyUsageHits: applyUsageHits,
  parseHitDays: parseHitDays,
  getOwnerKeyFor: getOwnerKeyFor,
  loadOwnerIndex: loadOwnerIndex,
  forgetCore: forgetCore,
  renameCore: renameCore,
  archiveCore: archiveCore,
  capacityCore: capacityCore,
  maintainCore: maintainCore,
  consolidateCore: consolidateCore,
  mergeCore: mergeCore,
  utilityScore: utilityScore,
  utilityBreakdown: utilityBreakdown,
  decayRecency: decayRecency,
  decayHalflifeDays: decayHalflifeDays,
  mcpTools: mcpTools,
  callTool: callTool,
  handleMessage: handleMessage,
  loadConfig: loadConfig,
  saveConfig: saveConfig,
  loadTokens: loadTokens,
  saveTokens: saveTokens,
  collectEntryFiles: collectEntryFiles,
  walkEntryFiles: walkEntryFiles,
  withIndexLock: withIndexLock,
  indexConsistencyReport: indexConsistencyReport,
  maybeHealIndex: maybeHealIndex,
  viewEntriesCore: viewEntriesCore,
  viewOverviewCore: viewOverviewCore,
  migrateLayout: migrateLayout,
  layoutPlanCore: layoutPlanCore,
  layoutApplyCore: layoutApplyCore,
  layoutRollbackCore: layoutRollbackCore,
  loadIndexFor: loadIndexFor,
  indexEntriesFor: indexEntriesFor,
  loadOwnerIndex: loadOwnerIndex,
  getOwnerKeyFor: getOwnerKeyFor,
  normalizeYearList: normalizeYearList,
  indexFingerprint: indexFingerprint,
  benchCore: benchCore,
  baselineCore: baselineCore,
  loadBaselineTemplate: loadBaselineTemplate,
  scanCore: scanCore,
  scanPolicyCandidatesCore: scanPolicyCandidatesCore,
  loadScanPolicy: loadScanPolicy,
  scanLineHash: scanLineHash,
  SCAN_POLICY_FILE: SCAN_POLICY_FILE,
  scanQuarantineCore: scanQuarantineCore,
  scanRestoreCore: scanRestoreCore,
  promptYesNo: promptYesNo,
  MEMORY_SCAN_RULES: MEMORY_SCAN_RULES,
  SCAN_CLASSES: SCAN_CLASSES,
  SCAN_SEVERITIES: SCAN_SEVERITIES,
  SCAN_QUARANTINE_DIR: SCAN_QUARANTINE_DIR,
  exportCore: exportCore,
  importCore: importCore,
  typeSubdir: typeSubdir,
  dateSubdir: dateSubdir,
  entryWriteDir: entryWriteDir,
  archiveRelFor: archiveRelFor,
  SCALE_CONFIG_KEYS: SCALE_CONFIG_KEYS,
  SCALE_THRESHOLD_DEFAULTS: SCALE_THRESHOLD_DEFAULTS,
  scaleReport: scaleReport,
  USAGE_CONFIG_DEFAULTS: USAGE_CONFIG_DEFAULTS,
  usageSettings: usageSettings,
  usageTotals: usageTotals,
  applyUsageHits: applyUsageHits,
  runtimeRoot: runtimeRoot,
  runtimeManifestPath: runtimeManifestPath,
  runtimeVersionsDir: runtimeVersionsDir,
  runtimeVersionDir: runtimeVersionDir,
  runtimeCurrentDir: runtimeCurrentDir,
  runtimeCurrentBin: runtimeCurrentBin,
  runtimeExecutionPath: runtimeExecutionPath,
  runtimeManagedScript: runtimeManagedScript,
  runtimeTreeHash: runtimeTreeHash,
  runtimeListVersions: runtimeListVersions,
  runtimeSwitchCurrent: runtimeSwitchCurrent,
  runtimeInstallFromCurrent: runtimeInstallFromCurrent,
  runtimeInstallTarball: runtimeInstallTarball,
  runtimeInstallVersion: runtimeInstallVersion,
  runtimeValidateTarballEntries: runtimeValidateTarballEntries,
  runtimeUseCore: runtimeUseCore,
  runtimeRollbackCore: runtimeRollbackCore,
  runtimeStatusCore: runtimeStatusCore,
  runtimeListCore: runtimeListCore,
  runtimeDoctorCore: runtimeDoctorCore,
  runtimeEnsureForManagedTask: runtimeEnsureForManagedTask,
  runtimeRestartManagedServer: runtimeRestartManagedServer,
  lanServeProfilePath: lanServeProfilePath,
  resolveProfilePath: resolveProfilePath,
  lanWriteServeProfile: lanWriteServeProfile,
  loadServeProfile: loadServeProfile,
  applyServeProfile: applyServeProfile,
  serveProfileDrift: serveProfileDrift,
  lanTaskRunCmd: lanTaskRunCmd,
  lanStartupDir: lanStartupDir,
  lanAutostartDir: lanAutostartDir,
  lanVbsPath: lanVbsPath,
  lanAutostartCmdPath: lanAutostartCmdPath,
  lanLogPath: lanLogPath,
  lanAutostartCmdContent: lanAutostartCmdContent,
  lanVbsContent: lanVbsContent,
  lanInstallStartup: lanInstallStartup,
  lanRemoveStartupFiles: lanRemoveStartupFiles,
  lanFileHasMarker: lanFileHasMarker,
  isSchtasksAccessDenied: isSchtasksAccessDenied,
  lanServeArgs: lanServeArgs,
  lanSpawn: lanSpawn,
  lanPlatform: lanPlatform,
  lanElectronHost: lanElectronHost,
  shQuote: shQuote,
  systemdEscapeArg: systemdEscapeArg,
  lanLinuxSystemdUserDir: lanLinuxSystemdUserDir,
  lanLinuxUnitPath: lanLinuxUnitPath,
  lanLinuxSystemctlBin: lanLinuxSystemctlBin,
  lanLinuxLoginctlBin: lanLinuxLoginctlBin,
  lanLinuxExecStart: lanLinuxExecStart,
  lanLinuxUnitContent: lanLinuxUnitContent,
  lanCrontabBin: lanCrontabBin,
  lanCrontabLine: lanCrontabLine,
  lanCrontabRead: lanCrontabRead,
  lanCrontabWrite: lanCrontabWrite,
  lanCrontabHasOurLine: lanCrontabHasOurLine,
  lanCrontabWithoutOurLine: lanCrontabWithoutOurLine,
  lanLinuxHasSystemd: lanLinuxHasSystemd,
  lanLinuxSystemctl: lanLinuxSystemctl,
  lanLinuxInstallSystemd: lanLinuxInstallSystemd,
  lanLinuxRemoveSystemd: lanLinuxRemoveSystemd,
  lanLinuxInstallCrontab: lanLinuxInstallCrontab,
  lanLinuxRemoveCrontab: lanLinuxRemoveCrontab,
  cmdLanWinEnable: cmdLanWinEnable,
  cmdLanWinDisable: cmdLanWinDisable,
  cmdLanWinStatus: cmdLanWinStatus,
  cmdLanLinuxEnable: cmdLanLinuxEnable,
  cmdLanLinuxDisable: cmdLanLinuxDisable,
  cmdLanLinuxStatus: cmdLanLinuxStatus,
  feedbackCore: feedbackCore,
  explainCore: explainCore,
  maintainCore: maintainCore,
  mergeCore: mergeCore,
  distillCore: distillCore,
  utilityScore: utilityScore,
  utilityBreakdown: utilityBreakdown,
  semanticMatch: semanticMatch,
  runEmbeddingPlugin: runEmbeddingPlugin,
  cosineSimilarity: cosineSimilarity,
  embeddingCandidates: embeddingCandidates,
  pinyinTokens: pinyinTokens,
  isEncrypted: isEncrypted,
  collectOwners: collectOwners,
  hasPlaintextPrivate: hasPlaintextPrivate,
  initEncryptionCore: initEncryptionCore,
  deriveUmk: deriveUmk,
  loadSalt: loadSalt,
  wrapOwnerKey: wrapOwnerKey,
  unwrapOwnerKey: unwrapOwnerKey,
  unwrapOwnerKeyRecovery: unwrapOwnerKeyRecovery,
  unwrapRecoveryEnc: unwrapRecoveryEnc,
  revokeOwnerKeyCache: revokeOwnerKeyCache,
  getOwnerKeyFor: getOwnerKeyFor,
  keyListCore: keyListCore,
  migrationRequiredInfo: migrationRequiredInfo,
  migrationReminderText: migrationReminderText,
  encryptMemoryText: encryptMemoryText,
  decryptMemoryText: decryptMemoryText,
  readMemoryText: readMemoryText,
  writeMemoryText: writeMemoryText,
  loadOwnerIndex: loadOwnerIndex,
  saveOwnerIndex: saveOwnerIndex,
  viewEntriesCore: viewEntriesCore,
  viewHtml: viewHtml,
  ensureIndex: ensureIndex,
  recallPrefilter: recallPrefilter,
  tokenize: tokenize,
  buildTokens: buildTokens,
  synonymSet: synonymSet,

  loadIndex: loadIndex,
  saveIndex: saveIndex,
  indexStatsCore: indexStatsCore,
  INDEX_VERSION: INDEX_VERSION,
  INDEX_SHARD_THRESHOLD: INDEX_SHARD_THRESHOLD,
  INDEX_COMPRESS_TRIGGER_BYTES: INDEX_COMPRESS_TRIGGER_BYTES,
  buildIndex: buildIndex,
  getIndex: getIndex,
  touchIndex: touchIndex,
  loadIndexManifest: loadIndexManifest,
  indexShardName: indexShardName,
  isSafeShardName: isSafeShardName,
  ownerFromPrivatePath: ownerFromPrivatePath,
  isEncFile: isEncFile,
  profilePathFor: profilePathFor,
  readProfileText: readProfileText,
  writeProfileText: writeProfileText,
  migrateCore: migrateCore,
  resetPasswordCore: resetPasswordCore,
  keyBindCore: keyBindCore,
  keyRevokeCore: keyRevokeCore,
  keyClaimCore: keyClaimCore,
  identityRemoveCore: identityRemoveCore,
  identityRemoveInventory: identityRemoveInventory,
  verifyIdentityRemoveAuthority: verifyIdentityRemoveAuthority,
  IDENTITY_REMOVE_STEPS: IDENTITY_REMOVE_STEPS,
  keyStatusCore: keyStatusCore,
  writeAgentBinding: writeAgentBinding,
  unwrapAgentBinding: unwrapAgentBinding,
  writePendingAgentKey: writePendingAgentKey,
  removePendingAgentKey: removePendingAgentKey,
  readPendingAgentKey: readPendingAgentKey,
  agentKeyFilePath: agentKeyFilePath,
  setRuntimeAgent: setRuntimeAgent,
  promptPassword: promptPassword,
  initCore: initCore,
  backupCreateCore: backupCreateCore,
  listBackupVolumesCore: listBackupVolumesCore,
  backupSetupCore: backupSetupCore,
  backupStatusCore: backupStatusCore,
  selectLatestValidBackup: selectLatestValidBackup,
  BACKUP_FUTURE_TOLERANCE_MS: BACKUP_FUTURE_TOLERANCE_MS,
  backupEnsureDailyCore: backupEnsureDailyCore,
  backupHealthCore: backupHealthCore,
  doctorCore: doctorCore,
  destructiveGuardCore: destructiveGuardCore,
  backupWindowsTaskXml: backupWindowsTaskXml,
  lanWindowsTaskXml: lanWindowsTaskXml,
  lanWindowsEnableCore: lanWindowsEnableCore,
  lanWindowsTaskUser: lanWindowsTaskUser,
  backupSystemdServiceContent: backupSystemdServiceContent,
  backupSystemdTimerContent: backupSystemdTimerContent,
  backupCronLine: backupCronLine,
  backupLaunchdPlist: backupLaunchdPlist,
  backupScheduleEnableCore: backupScheduleEnableCore,
  backupScheduleDisableCore: backupScheduleDisableCore,
  backupScheduleStatusCore: backupScheduleStatusCore,
  backupFallbackCommand: backupFallbackCommand,
  backupListCore: backupListCore,
  backupDoctorCore: backupDoctorCore,
  backupRestoreCore: backupRestoreCore,
  backupDrillCore: backupDrillCore,
  memoryRootId: memoryRootId,
  viewServerCore: viewServerCore,

};
