'use strict';

/**
 * yotta-skills（元阁）CLI 帮助单一真源。
 *
 * - CLI_HELP_MODEL：分组 → 命令 → usage / what / when / options（引用全局选项）
 * - CLI_HELP_QUICK：全量速查（每个命令与子命令至少一条：示例 + 危险标记 + 注意）
 * - CLI_GLOBAL_OPTIONS：全局选项明细（--help 选项区 / 面板完整参数 / 官网导出）
 *
 * 面板 /api/help、CLI --help、官网结构化导出都从这里取；新增命令必须同步本文件，
 * 否则 test/cli-help-coverage.test.js 会 FAIL（防漂移）。
 */

const CLI_GLOBAL_OPTIONS = [
  { flag: '--agent', arg: '<name>', what: '指定智能体（用它的默认用户级技能目录）', when: '给某个智能体装 / 链接 / 解除时', caution: '未收录的智能体请改用 --dir' },
  { flag: '--dir', arg: '<path>', what: '指定技能目录（技能落到 <path>/<slug>）', when: '给任意宿主或自定义目录安装 / 分发时', caution: '' },
  { flag: '--pin', arg: '', what: '锁死清单精确版本（默认）', when: '需要可复现安装时（默认行为）', caution: '' },
  { flag: '--range', arg: '', what: '跟随同 major 最新 patch（非默认：显式指定后才浮动跟随）', when: '想主动跟随 patch 更新时', caution: '浮动版本每次安装结果可能不同' },
  { flag: '--force', arg: '', what: '已是最新也重装；hub link 时替换同名真目录 / 外部链接', when: '确认要覆盖现有内容时', caution: '可能替换目标目录；先确认目标与备份' },
  { flag: '--skip-scan', arg: '', what: '跳过元信装前扫描（装了元信时自动启用）', when: '已确认来源可信、需要离线安装时', caution: '跳过后风险自负；安装记录会标记 explicit-unverified' },
  { flag: '--only', arg: '<a,b>', what: 'install / update 只处理指定技能', when: '只维护几个技能时', caution: '' },
  { flag: '--domain', arg: '<name>', what: 'install / update 只处理指定家族', when: '按领域批量维护时', caution: '可用值见 --list 的家族列' },
  { flag: '--installed-only', arg: '', what: 'update 只维护目标目录已安装的技能（不补装缺失）', when: '接管现有技能、不想新增时', caution: '无匹配时退出码 0（无动作）' },
  { flag: '--npm', arg: '<path>', what: '指定 npm 可执行文件', when: 'npm 不在 PATH 或需要指定版本时', caution: '' },
  { flag: '--python', arg: '<path>', what: '指定 python 可执行文件（元信扫描用）', when: 'Python 不在 PATH 时', caution: '' },
  { flag: '--verify', arg: '<path>', what: '指定 yotta_verify.py 路径', when: '使用自带的元信引擎时', caution: '' },
  { flag: '--json', arg: '', what: '输出 JSON（inventory / reindex / route / doctor / rollback / hub 等）', when: '脚本或自动化读取结果时', caution: '' },
  { flag: '--slug', arg: '<slug>', what: 'doctor / rollback 只处理指定技能', when: '只检查 / 回滚一个技能时', caution: '' },
  { flag: '--route', arg: '<需求>', what: '静态编排路由：组合 / 顺序 / 依据 / 缺失技能建议', when: '想知道该用哪些技能时', caution: '只建议不自动安装' },
  { flag: '--check', arg: '', what: 'update 时只读检查更新（对 npm 最新版本，不改动）', when: '定期检查或发布前核对时', caution: '退出码 0=最新 / 3=有更新 / 1=检查失败' },
  { flag: '--scheduled', arg: '', what: '与 update --check 合用：后台周检（未到期不联网）', when: '挂后台定时检查时', caution: '只与 update --check 一起使用' },
  { flag: '--auto', arg: '', what: 'update 检查到家族更新后自动更新（仅 yotta-* 家族）', when: '想自动跟进家族更新时', caution: '自动更新含装前扫描；不会自动安装缺失技能' },
  { flag: '--registry', arg: '<url>', what: 'npm registry 地址（默认官方源）', when: '需要走镜像或私有源时', caution: '' },
  { flag: '--host', arg: '<name>', what: 'hook 适配宿主名（默认 generic）', when: '评估 / 绑定宿主 hook 时', caution: '当前已实测 codex' },
  { flag: '--event', arg: '<event>', what: 'hook 六事件之一', when: 'evaluate / 排查 hook 时', caution: '六事件：before_start / before_tool / before_install / before_publish / after_milestone / before_send' },
  { flag: '--manifest', arg: '<file>', what: 'hook evaluate / bind 使用的 skill-manifest.json', when: '按技能声明评估 hook 时', caution: '' },
  { flag: '--context', arg: '<json>', what: 'hook evaluate 的检查结果 JSON', when: '外部传入 checks / wrapperRegistered / evidence 时', caution: '' },
  { flag: '--skill', arg: '<slug>', what: 'usage mark 的技能 slug', when: '记录技能使用信号时', caution: '' },
  { flag: '--signal', arg: '<name>', what: 'usage mark 的信号：used / named / accepted', when: '记录技能使用信号时', caution: '' },
  { flag: '--yes', arg: '', what: '确认开关（usage reset / hub hosts remove --purge / hub cleanup-backups / hub config rollback）', when: '确认执行破坏性或迁移类操作时', caution: '默认都是预览；--yes 才真正执行' },
  { flag: '--explain', arg: '', what: 'decide-memory 文本报告追加信号明细', when: '想看裁决依据时', caution: '' },
  { flag: '--promote', arg: '', what: 'decide-memory 只写本地建议文件（不写元忆）', when: '想留下裁决建议文件时', caution: '不会写元忆、不会删除任何内容' },
  { flag: '--hub', arg: '<path>', what: 'Hub 目录（默认 ~/.yottaskills/hub；持久配置见 hub config）', when: '使用自定义 Hub 位置时', caution: '覆盖顺序：--hub > YOTTA_SKILLS_HUB > config.json > 默认' },
  { flag: '--move', arg: '', what: 'hub config set 迁移：复制校验旧 Hub → 重链宿主 → 旧 Hub 入回收站（7 天）', when: '换 Hub 位置并带上已有技能时', caution: 'fail-closed：校验失败不切配置；重链失败保留旧 Hub' },
  { flag: '--clean-residue', arg: '', what: 'hub config set --move / rollback：目标只含空 Hub 台账残留时先移入回收站再迁移', when: '迁移 / 回滚目标目录有 .yotta-hub.json 残留时', caution: '只清理元阁自己的空台账残留，不合并其它内容' },
  { flag: '--port', arg: '<n>', what: 'view 面板端口（默认 8789）', when: '端口冲突或想固定端口时', caution: '仅 127.0.0.1 监听' },
  { flag: '--all', arg: '', what: 'hub link / unlink 作用于全部已核实宿主', when: '全量分发或解除时', caution: '' },
  { flag: '--include-discovered', arg: '', what: 'hub link / unlink / remove 时纳入自动发现目录', when: '确认要扩围到未核实目录时', caution: '默认只链已核实宿主；桥接目录永不链接' },
  { flag: '--state', arg: '<state>', what: 'hub hosts 状态过滤（available / orphan / missing / marker-only / ignored）；hub hosts mark 时为手动状态', when: '只看某类宿主、或手动标记宿主状态时', caution: '' },
  { flag: '--label', arg: '<名称>', what: 'hub hosts add 的显示名称（默认取目录名）', when: '注册自定义宿主时', caution: '最长 48 字符，禁控制字符' },
  { flag: '--id', arg: '<agentId>', what: 'hub hosts add / remove 的智能体标识', when: '按智能体注册或移除自定义宿主时', caution: '' },
  { flag: '--purge', arg: '', what: 'hub hosts remove 清理残留目录（默认预览；--yes 执行）', when: '清理实体未确认的残留技能目录时', caution: '只删指向 Hub 的链接；目录移入回收站保留 7 天' },
  { flag: '--clear', arg: '', what: 'hub hosts set 恢复内置映射（删除目录覆盖）', when: '想撤销目录覆盖时', caution: '' },
  { flag: '--scan', arg: '', what: 'hub adopt 只读预演（默认行为）', when: '先看收编候选与冲突时', caution: '' },
  { flag: '--apply', arg: '', what: 'hub adopt 执行收编', when: '确认候选后执行时', caution: '执行时逐项运行元信扫描；high / critical 默认阻断' },
  { flag: '--in-place', arg: '', what: 'hub adopt 原地登记，不复制', when: '想让 Hub 直接指向原目录时', caution: '原目录删除即断链；默认复制保真更安全' },
  { flag: '--allow-unverified', arg: '', what: '显式允许未扫描导入（默认 high / critical 阻断）', when: '已人工确认来源可信时', caution: '会放宽装前扫描门禁，谨慎使用' },
  { flag: '--from', arg: '<path>', what: 'hub refresh 的来源目录', when: '手动同步非元阁技能时', caution: '无统一更新源，需显式指定来源' },
  { flag: '--include', arg: '<a,b>', what: 'hub adopt --apply 只收编指定技能', when: '从候选中挑几个收编时', caution: '' },
  { flag: '--project', arg: '', what: 'inventory / reindex 附加扫描当前项目 .agents/skills / .codex/skills', when: '盘点项目级技能时', caution: '' },
  { flag: '--no-reindex', arg: '', what: '安装 / 更新后不自动重扫注册表', when: '批量操作后再统一重扫时', caution: '' },
  { flag: '--dry-run', arg: '', what: '只预览不写入（install / update / hub link / hub unlink / hub remove）', when: '执行前先看影响时', caution: '预演只读，不改动任何文件' },
  { flag: '--list', arg: '', what: '列出全家技能 + 版本 + 说明', when: '查看清单或核对版本时', caution: '' },
  { flag: '--inventory', arg: '', what: '盘点本机已装技能（自研扫描）', when: '接手机器或排查技能分布时', caution: '' },
  { flag: '--reindex', arg: '', what: '重扫本地技能注册表', when: '手工安装技能后刷新注册表时', caution: '' },
  { flag: '-h, --help', arg: '', what: '显示帮助', when: '忘了命令怎么用时', caution: '' },
  { flag: '-v, --version', arg: '', what: '显示版本', when: '确认安装版本时', caution: '' },
];

const CLI_HELP_MODEL = [
  {
    group: '安装与更新',
    commands: [
      {
        name: 'install',
        usage: 'install [skill...] [--agent <name> | --dir <path>] [--only <a,b> | --domain <name>] [--dry-run]',
        what: '装全家或指定技能到目标目录',
        when: '新机器铺齐、补装单个技能、按领域安装时',
        options: ['--agent', '--dir', '--only', '--domain', '--pin', '--range', '--dry-run', '--force', '--skip-scan', '--no-reindex'],
      },
      {
        name: 'update',
        usage: 'update [--agent <name> | --dir <path>] [--installed-only] [--check [--scheduled] | --auto] [--only <a,b> | --domain <name>]',
        what: '增量更新已装技能（补齐缺失 / 升级；只升不降：本地更高保留，--force 才显式降级）',
        when: '日常维护、只读检查更新、后台周检、自动跟进时',
        options: ['--agent', '--dir', '--installed-only', '--check', '--scheduled', '--auto', '--only', '--domain', '--dry-run', '--skip-scan'],
      },
      {
        name: '--dry-run',
        usage: '--dry-run',
        what: '只预览将安装 / 更新 / 链接 / 删除的清单，不联网不改动（与 install / update / hub link / hub unlink / hub remove 合用）',
        when: '执行前先确认影响面时',
        options: ['--dry-run'],
      },
      {
        name: 'install-self',
        usage: 'install-self [--dir <path>] [--dry-run] [--force] [--json]',
        what: '元阁独立安装：把管理引擎装到独立位置（默认 ~/.yottaskills/yotta-skills），与 Hub / 宿主分离',
        when: '想把元阁装成独立 CLI（不依赖任何智能体）时',
        options: ['--dir', '--dry-run', '--force', '--json'],
      },
      {
        name: 'where',
        usage: 'where [--json]',
        what: '查看元阁位置：运行中 CLI / 独立安装目录（标记当前运行项）/ Hub 真源',
        when: '确认元阁装在哪、是否独立安装时',
        options: ['--json', '--hub'],
      },
    ],
  },
  {
    group: '体检与回滚',
    commands: [
      {
        name: 'doctor',
        usage: 'doctor [--agent <name> | --dir <path>] [--slug <slug>] [--json]',
        what: '只读自检技能目录（SKILL / 版本 / manifest / 注册表）',
        when: '安装后、异常后、升级后确认状态时',
        options: ['--agent', '--dir', '--slug', '--json'],
      },
      {
        name: 'rollback',
        usage: 'rollback [--agent <name> | --dir <path>] [--slug <slug>] [--list] [--json]',
        what: '回滚最近一次技能安装或更新',
        when: '新版本有问题、想回到快照时',
        options: ['--agent', '--dir', '--slug', '--list', '--json'],
      },
    ],
  },
  {
    group: '盘点与路由',
    commands: [
      {
        name: '--list',
        usage: '--list',
        what: '列出全家技能 + 版本 + 说明',
        when: '查看清单、核对版本、确认技能名时',
        options: ['--list'],
      },
      {
        name: '--inventory',
        usage: '--inventory [--project] [--json]',
        what: '盘点本机已装技能（自研扫描，不依赖任何元技能）',
        when: '接手机器、排查技能分布、找同名多副本时',
        options: ['--inventory', '--project', '--json'],
      },
      {
        name: '--reindex',
        usage: '--reindex [--project]',
        what: '重扫本地技能注册表（install / update 后也会自动重扫）',
        when: '手工安装技能后刷新注册表时',
        options: ['--reindex', '--project'],
      },
      {
        name: '--route',
        usage: '--route "<需求摘要>" [--json]',
        what: '按需求给出技能组合、调用顺序、缺失技能安装建议',
        when: '不知道该用哪些技能、想按场景组合时',
        options: ['--route', '--json'],
      },
      {
        name: 'decide-memory',
        usage: 'decide-memory [--dry-run | --promote] [--explain] [--json]',
        what: 'M1 记忆裁决：输出 promote / hold / demote 只读建议',
        when: '判断哪些技能值得长期记忆时',
        options: ['--dry-run', '--promote', '--explain', '--json'],
      },
    ],
  },
  {
    group: '技能 Hub',
    commands: [
      {
        name: 'hub',
        usage: 'hub <子命令> [选项]',
        what: 'Hub 单点真源：发现宿主、安装 / 收编、链接分发、体检、删除',
        when: '多智能体共享技能、统一管理技能目录时',
        options: ['--hub', '--all', '--include-discovered', '--dry-run', '--json'],
        subcommands: [
          { name: 'hosts', usage: 'hub hosts [--json] [--state <state>]', what: '发现宿主与技能目录（可用 / 残留 / 未创建 / 仅标记 / 桥接）', when: '先看这台机器有哪些宿主目录时', options: ['--json', '--state'] },
          { name: 'hosts add', usage: 'hub hosts add <dir> [--label <名称>] [--id <agentId>] [--json]', what: '注册自定义宿主目录（纳入发现 / 分发 / 收编；不创建目录）', when: '宿主未被自动识别或识别错误时', options: ['--label', '--id', '--json'] },
          { name: 'hosts rename', usage: 'hub hosts rename <dir | --id <agentId>> --label <名称> [--json]', what: '一步改名（只改显示名；目录与手动状态保持）', when: '自定义宿主显示名不合适时', options: ['--label', '--id', '--json'] },
          { name: 'hosts remove', usage: 'hub hosts remove <dir | --id <agentId>> [--purge [--yes]] [--json]', what: '移除注册（绝不删目录）；--purge = 清理残留目录（默认预览，--yes 执行）', when: '注销自定义宿主、清理残留目录时', options: ['--id', '--purge', '--yes', '--json'], impact: '影响面：只移除注册表条目（目录保留）；--purge 会把残留目录移入回收站（保留 7 天）；不会自动清理该目录里已有的 Hub 链接。', alternative: '替代路径：只想暂停接管用 hub hosts exclude；清理该目录链接用 hub unlink --dir "<目录>"。' },
          { name: 'hosts list', usage: 'hub hosts list [--json]', what: '查看自定义宿主注册表（仅手动 add 的目录；全部宿主用 hub hosts）', when: '核对已注册的自定义目录时', options: ['--json'] },
          { name: 'hosts mark', usage: 'hub hosts mark <dir> --state <available|orphan|ignored> [--json]', what: '手动标记宿主状态（可用 / 残留 / 隐藏标记）；隐藏标记只影响显示，不拦截行为', when: '实体证据不足需要人工确认、或想让某行从列表淡化时', options: ['--state', '--json'], impact: '影响面：纯状态标记（available / orphan / ignored），不移动目录、不改链接。真正拦截行为的是「不接管」（hosts exclude）。' },
          { name: 'hosts exclude', usage: 'hub hosts exclude <agentId|dir> [--json]', what: '加入「不接管」名单（发现 / 显示 / 链接三层跳过）', when: '某宿主 / 目录不归元阁管理时', options: ['--json'], impact: '影响面：发现 / 显示 / 链接三层全部跳过（--include-discovered 也不纳入）；已有链接不动。', alternative: '替代路径：只淡化显示用 hub hosts mark --state ignored；恢复接管用 hub hosts include。' },
          { name: 'hosts include', usage: 'hub hosts include <agentId|dir> [--json]', what: '恢复接管（移出「不接管」名单）', when: '重新纳入发现 / 链接时', options: ['--json'] },
          { name: 'hosts set', usage: 'hub hosts set <agentId> --dir <dir> [--label <名称>] [--json] | hub hosts set <agentId> --clear', what: '目录覆盖：用户级覆盖内置映射；--clear 恢复默认', when: '宿主技能目录与内置映射不一致时', options: ['--dir', '--label', '--clear', '--json'] },
          { name: 'config get', usage: 'hub config get [--json]', what: '查看生效 Hub 位置与来源（--hub / YOTTA_SKILLS_HUB / config.json / 默认）', when: '确认当前 Hub 与配置覆盖时', options: ['--json'] },
          { name: 'config set', usage: 'hub config set --hub <path> [--move [--clean-residue]]', what: '持久化 Hub 位置；--move 迁移旧 Hub（复制校验 → 重链 → 回收站 7 天）；未迁移时记录原位置供面板提示', when: '换 Hub 存储位置时', options: ['--hub', '--move', '--clean-residue', '--json'] },
          { name: 'config rollback', usage: 'hub config rollback [--yes] [--clean-residue]', what: '回滚到上次迁移前的 Hub 位置（位置回退，用当前内容；反向迁移同内核）', when: '迁移后想退回原位置时', options: ['--yes', '--clean-residue', '--json'], impact: '影响面：位置回退（用当前内容复制回原位置并重链，不恢复旧快照）；目标非空时 fail-closed 阻断。', alternative: '替代路径：只查看历史迁移用 hub config get；继续当前位置则不需要操作。' },
          { name: 'config clear', usage: 'hub config clear [--yes] [--json]', what: '清除配置覆盖，恢复 flag > env > 默认；当前 Hub 有技能时默认阻断，--yes 显式确认', when: '撤销持久 Hub 位置时', options: ['--yes', '--json'], impact: '影响面：清除后生效位置回落到默认（可能是空目录）；Hub 真源与宿主链接不移动，但元阁命令将按新位置工作（表现为台账 / 链接空转）。', alternative: '替代路径：迁移位置用 hub config set --hub "<新路径>" --move；想回原位置用 hub config set --hub "<原路径>"。' },
          { name: 'cleanup-backups', usage: 'hub cleanup-backups [--yes] [--include-discovered]', what: '清理宿主 / Hub 里的 .yottaskills-backup-* / .yottaskills-staging 历史残留（移入回收站 7 天）', when: '宿主把备份当技能扫描、或迁移后要清残留时', options: ['--yes', '--include-discovered', '--dir', '--agent', '--json'] },
          { name: 'install', usage: 'hub install [skill...]', what: '把元技能装进 Hub 真源（清单 27 + 特殊家族 5）', when: '初始化 Hub 或补装技能时', options: ['--hub'] },
          { name: 'update', usage: 'hub update', what: '更新 Hub 内的元技能（非元技能不参与；只升不降）', when: '日常维护 Hub 真源时', options: ['--hub'] },
          { name: 'adopt', usage: 'hub adopt [--scan | --apply] [--include <a,b>] [--in-place]', what: '把各宿主已有技能收编进 Hub（默认复制保真）', when: '接管机器上已装的技能时', options: ['--scan', '--apply', '--include', '--in-place', '--force', '--skip-scan', '--allow-unverified'] },
          { name: 'refresh', usage: 'hub refresh <slug> --from <path>', what: '手动同步非元阁技能（无统一更新源）', when: '外部技能更新后刷新 Hub 副本时', options: ['--from'] },
          { name: 'link', usage: 'hub link [skill...] [--all | --agent <id> | --dir <path>] [--include-discovered] [--dry-run]', what: '把 Hub 技能链接到宿主目录（指定智能体 / 全量）', when: '分发技能到各智能体时', options: ['--all', '--agent', '--dir', '--include-discovered', '--force', '--dry-run'] },
          { name: 'unlink', usage: 'hub unlink [skill...] [--all | --agent <id> | --dir <path>] [--dry-run]', what: '只删除链接，不动 Hub 真源（fail-closed；--dir 无 slug 时以文件系统为真源清理该目录全部 Hub 链接）', when: '解除某个 / 全部宿主的链接时', options: ['--all', '--agent', '--dir', '--include-discovered', '--dry-run'], impact: '影响面：只删除宿主目录中的链接（Hub 真源保留）；只处理指向当前 Hub 的链接，指向其它位置的链接 fail-closed 不动并给出错位警告。', alternative: '替代路径：删除整个技能用 hub remove <slug>；重建链接用 hub link --dir "<目录>" --force。' },
          { name: 'remove', usage: 'hub remove <slug> [--dry-run] [--include-discovered]', what: '删除 Hub 技能：全宿主清链接（含死链）+ 目录入回收站 + 清台账 + 审计', when: '彻底删除某个 Hub 技能时', options: ['--dry-run', '--include-discovered', '--json'], impact: '影响面：全宿主清理该技能链接（含死链）→ Hub 目录移入回收站（保留 7 天）→ 清台账；影响范围大。', alternative: '替代路径：只想解除某宿主链接用 hub unlink；只想清死链用 hub remove <slug> --agent/--dir（目标缺失时）。' },
          { name: 'status', usage: 'hub status [--json]', what: '查看 Hub 技能 / 来源 / 版本 / 链接 / 宿主', when: '核对 Hub 现状时', options: ['--json'] },
          { name: 'doctor', usage: 'hub doctor [--json]', what: '检查断链 / 目标缺失 / slug 不一致 / 单一真源 / 链接范围', when: 'Hub 异常后排查时', options: ['--json'] },
        ],
      },
    ],
  },
  {
    group: '使用记录与 Hook',
    commands: [
      {
        name: 'usage',
        usage: 'usage <子命令>',
        what: '本地技能使用记录（默认关闭；只记结构化计数）',
        when: '想看技能使用信号、给路由 / 裁决提供依据时',
        options: ['--json'],
        subcommands: [
          { name: 'status', usage: 'usage status [--json]', what: '查看开关与计数', when: '核对记录状态时', options: ['--json'] },
          { name: 'enable', usage: 'usage enable', what: '开启本地使用记录', when: '想开始积累使用信号时', options: [] },
          { name: 'disable', usage: 'usage disable', what: '关闭本地使用记录', when: '不想再记录时', options: [] },
          { name: 'mark', usage: 'usage mark --skill <slug> --signal used|named|accepted', what: '记录一次使用信号', when: '技能被实际使用 / 点名 / 接受时', options: ['--skill', '--signal'] },
          { name: 'reset', usage: 'usage reset --yes', what: '清空本地使用记录', when: '确认要重置计数时', options: ['--yes'] },
        ],
      },
      {
        name: 'hook',
        usage: 'hook <子命令> [--host <name>]',
        what: '宿主 hook 适配：能力矩阵 / 评估 / 绑定 / 反注册',
        when: '接入宿主六事件、排查 hook 时',
        options: ['--host', '--event', '--manifest', '--context', '--json'],
        subcommands: [
          { name: 'capabilities', usage: 'hook capabilities [--host <name>] [--json]', what: '查看宿主六事件能力矩阵', when: '确认宿主支持哪些 hook 时', options: ['--host', '--json'] },
          { name: 'evaluate', usage: 'hook evaluate --event <event> --manifest <file> [--context <json>]', what: '评估 hook 声明并留证', when: '上线前验证 hook 行为时', options: ['--host', '--event', '--manifest', '--context', '--json'] },
          { name: 'bind', usage: 'hook bind --manifest <file> [--host <name>]', what: '注册 hook 声明（幂等）', when: '给宿主登记 hook 时', options: ['--host', '--manifest', '--json'] },
          { name: 'unbind', usage: 'hook unbind <binding-id> [--host <name>]', what: '反注册 hook 声明', when: '下线 hook 时', options: ['--host', '--json'] },
        ],
      },
    ],
  },
  {
    group: '面板与帮助',
    commands: [
      {
        name: 'view',
        usage: 'view [--port <n>]',
        what: '启动本机技能枢纽面板（127.0.0.1:8789）',
        when: '想图形化管理 Hub、看宿主矩阵 / 体检 / 路由时',
        options: ['--port'],
      },
      {
        name: '--version',
        usage: '--version；短写法 -v',
        what: '显示当前版本',
        when: '确认安装的是哪个版本时',
        options: [],
      },
      {
        name: '--help',
        usage: '--help；短写法 -h',
        what: '显示命令与选项帮助',
        when: '忘了命令怎么用时',
        options: [],
      },
    ],
  },
];

const CLI_HELP_QUICK = [
  {
    group: '安装与更新',
    items: [
      { cmd: 'install', example: 'yotta-skills install --agent codex', note: '装全家到指定智能体' },
      { cmd: 'install', example: 'yotta-skills install yotta-memory --dir <技能目录>', note: '只装一个技能到指定目录' },
      { cmd: 'update', example: 'yotta-skills update --installed-only --dir <技能目录>', note: '接管现有技能（只升不降）' },
      { cmd: 'update', example: 'yotta-skills update --check', note: '只读检查 npm 更新（不改动）' },
      { cmd: 'update', example: 'yotta-skills update --auto', note: '检查到家族更新后自动更新' },
      { cmd: '--dry-run', example: 'yotta-skills install --dry-run --agent codex', note: '预演安装 / 更新清单（不联网不改动）' },
      { cmd: 'install-self', example: 'yotta-skills install-self', note: '把元阁装成独立 CLI' },
      { cmd: 'where', example: 'yotta-skills where', note: '查看运行中 / 独立安装 / Hub 位置' },
    ],
  },
  {
    group: '体检与回滚',
    items: [
      { cmd: 'doctor', example: 'yotta-skills doctor --dir <技能目录>', note: '只读自检技能目录与注册表' },
      { cmd: 'rollback', example: 'yotta-skills rollback --list', note: '列出可回滚的备份点' },
      { cmd: 'rollback', example: 'yotta-skills rollback --slug <技能> --dir <技能目录>', note: '回滚指定技能到上一个备份' },
    ],
  },
  {
    group: '盘点与路由',
    items: [
      { cmd: '--list', example: 'yotta-skills --list', note: '列出全家技能与版本' },
      { cmd: '--inventory', example: 'yotta-skills --inventory --json', note: '盘点本机已装技能' },
      { cmd: '--reindex', example: 'yotta-skills --reindex', note: '重扫本地技能注册表' },
      { cmd: '--route', example: 'yotta-skills --route "帮我做发布前质量检查"', note: '按需求给技能组合建议（不自动安装）' },
      { cmd: 'decide-memory', example: 'yotta-skills decide-memory --dry-run', note: 'M1 记忆裁决只读建议' },
    ],
  },
  {
    group: '技能 Hub',
    items: [
      { cmd: 'hub', example: 'yotta-skills hub', note: 'Hub 子命令总览' },
      { cmd: 'hub hosts', example: 'yotta-skills hub hosts', note: '查看全部宿主与技能目录状态' },
      { cmd: 'hub hosts', example: 'yotta-skills hub hosts --state orphan', note: '只筛选「残留」状态的宿主' },
      { cmd: 'hub hosts add', example: 'yotta-skills hub hosts add <技能目录>', note: '注册自定义宿主目录（不创建目录）' },
      { cmd: 'hub hosts rename', example: 'yotta-skills hub hosts rename <技能目录> --label <新名称>', note: '只改显示名；目录与手动状态保持' },
      { cmd: 'hub hosts list', example: 'yotta-skills hub hosts list', note: '查看手动注册的自定义宿主' },
      { cmd: 'hub hosts mark', example: 'yotta-skills hub hosts mark <技能目录> --state orphan', note: '手动标记状态（可用 / 残留 / 隐藏标记）' },
      { cmd: 'hub hosts exclude', example: 'yotta-skills hub hosts exclude <agentId|目录>', note: '加入「不接管」名单' },
      { cmd: 'hub hosts include', example: 'yotta-skills hub hosts include <agentId|目录>', note: '恢复接管' },
      { cmd: 'hub hosts set', example: 'yotta-skills hub hosts set <agentId> --dir <目录>', note: '覆盖某智能体的技能目录映射' },
      { cmd: 'hub config get', example: 'yotta-skills hub config get', note: '查看生效位置与来源' },
      { cmd: 'hub config set', example: 'yotta-skills hub config set --hub <Hub目录>', note: '持久化 Hub 位置；迁移旧 Hub 加 --move' },
      { cmd: 'hub config rollback', example: 'yotta-skills hub config rollback --yes', note: '回滚到上次迁移前的位置（位置回退，用当前内容）', danger: true },
      { cmd: 'hub config clear', example: 'yotta-skills hub config clear', danger: true, note: '清除持久覆盖，恢复默认解析；当前 Hub 有技能时默认阻断，确认影响后加 --yes' },
      { cmd: 'hub cleanup-backups', example: 'yotta-skills hub cleanup-backups --yes', note: '历史备份 / 暂存残留移入回收站（7 天可恢复）', danger: true },
      { cmd: 'hub hosts remove', example: 'yotta-skills hub hosts remove <技能目录>', note: '只移除注册，不删目录；该目录已有链接不清理（用 hub unlink --dir）' },
      { cmd: 'hub hosts remove', example: 'yotta-skills hub hosts remove <技能目录> --purge', danger: true, note: '清理残留目录：先预览，--yes 才执行；目录入回收站保留 7 天' },
      { cmd: 'hub install', example: 'yotta-skills hub install', note: '把元技能装进 Hub 真源' },
      { cmd: 'hub update', example: 'yotta-skills hub update', note: '更新 Hub 内元技能（只升不降）' },
      { cmd: 'hub adopt', example: 'yotta-skills hub adopt --scan', note: '只读预演收编候选与冲突' },
      { cmd: 'hub adopt', example: 'yotta-skills hub adopt --apply --include <技能>', note: '执行收编（逐项元信扫描，high / critical 阻断）' },
      { cmd: 'hub refresh', example: 'yotta-skills hub refresh <技能> --from <技能目录>', note: '手动同步非元阁技能（需 --from）' },
      { cmd: 'hub link', example: 'yotta-skills hub link --all', note: '全量分发到全部已核实宿主' },
      { cmd: 'hub link', example: 'yotta-skills hub link <技能> --agent codex', note: '针对指定智能体分发' },
      { cmd: 'hub unlink', example: 'yotta-skills hub unlink <技能> --agent codex', note: '只解除该智能体的链接，Hub 真源保留' },
      { cmd: 'hub unlink', example: 'yotta-skills hub unlink --dir <技能目录>', note: '清理该目录全部指向当前 Hub 的链接（文件系统为真源；其它位置链接不动）' },
      { cmd: 'hub unlink', example: 'yotta-skills hub unlink --all', note: '解除全部已核实宿主的链接' },
      { cmd: 'hub remove', example: 'yotta-skills hub remove <技能> --dry-run', danger: true, note: '删除 Hub 技能：全宿主清链接（含死链）+ 目录入回收站（7 天）+ 清台账；先 --dry-run 看影响' },
      { cmd: 'hub status', example: 'yotta-skills hub status', note: '查看 Hub 技能 / 版本 / 链接 / 宿主' },
      { cmd: 'hub doctor', example: 'yotta-skills hub doctor', note: '检查断链 / 缺失 / slug 不一致' },
    ],
  },
  {
    group: '使用记录与 Hook',
    items: [
      { cmd: 'usage', example: 'yotta-skills usage status', note: '使用记录开关与计数总览' },
      { cmd: 'usage status', example: 'yotta-skills usage status --json', note: '查看开关与计数（JSON）' },
      { cmd: 'usage enable', example: 'yotta-skills usage enable', note: '开启本地使用记录' },
      { cmd: 'usage disable', example: 'yotta-skills usage disable', note: '关闭本地使用记录' },
      { cmd: 'usage mark', example: 'yotta-skills usage mark --skill yotta-memory --signal used', note: '记录一次使用信号' },
      { cmd: 'usage reset', example: 'yotta-skills usage reset --yes', danger: true, note: '清空本地使用记录，先确认不再需要计数' },
      { cmd: 'hook', example: 'yotta-skills hook capabilities', note: 'hook 子命令总览' },
      { cmd: 'hook capabilities', example: 'yotta-skills hook capabilities --host codex --json', note: '查看宿主六事件能力矩阵' },
      { cmd: 'hook evaluate', example: 'yotta-skills hook evaluate --event before_install --manifest <file>', note: '评估 hook 声明并留证' },
      { cmd: 'hook bind', example: 'yotta-skills hook bind --manifest <file>', note: '注册 hook 声明（幂等）' },
      { cmd: 'hook unbind', example: 'yotta-skills hook unbind <binding-id>', note: '反注册 hook 声明' },
    ],
  },
  {
    group: '面板与帮助',
    items: [
      { cmd: 'view', example: 'yotta-skills view', note: '打开本地控制面板（仅 127.0.0.1）' },
      { cmd: 'view', example: 'yotta-skills view --port 8790', note: '指定端口打开（默认 8789）' },
      { cmd: '--version', example: 'yotta-skills --version', note: '查看当前版本' },
      { cmd: '--help', example: 'yotta-skills --help', note: '查看终端帮助（与面板同一真源）' },
    ],
  },
];

/**
 * UX-10：速查引用解析（单一真源，服务端随 /api/help 下发）。
 *
 * 按「最深前缀」把速查条目的 cmd 解析到模型条目：
 * - 'hub hosts add'  → 'hub hosts add'（不是父级 'hub hosts'）
 * - 'hub hosts --state orphan' → 'hub hosts'（旗标 / 参数尾段容忍）
 * - '--list' 等伪命令按全名精确匹配
 */
function resolveHelpEntry(groups, ref) {
  const raw = String(ref || '').trim();
  if (!raw) return null;
  const entries = [];
  for (const group of groups) {
    for (const cmd of group.commands) {
      entries.push({ path: cmd.name, entry: cmd });
      for (const sub of cmd.subcommands || []) {
        entries.push({ path: cmd.name + ' ' + sub.name, entry: sub });
      }
    }
  }
  for (const item of entries) {
    if (item.path === raw) return item.entry;
  }
  const tokens = [];
  for (const token of raw.split(/\s+/)) {
    if (token.startsWith('-') || token.startsWith('<') || token.startsWith('[')) break;
    tokens.push(token);
  }
  if (!tokens.length) return null;
  let best = null;
  let bestLen = -1;
  for (const item of entries) {
    const pathTokens = item.path.split(' ');
    if (pathTokens.length > tokens.length || pathTokens.length <= bestLen) continue;
    if (pathTokens.every((token, index) => token === tokens[index])) {
      best = item.entry;
      bestLen = pathTokens.length;
    }
  }
  return best;
}

/** 速查数据 + 服务端解析结果（面板直接用 meta，不再自行解析）。 */
function quickWithMeta() {
  return CLI_HELP_QUICK.map((group) => ({
    group: group.group,
    items: group.items.map((item) => Object.assign({}, item, {
      meta: resolveHelpEntry(CLI_HELP_MODEL, item.cmd) || {},
    })),
  }));
}

module.exports = {
  CLI_HELP_MODEL,
  CLI_HELP_QUICK,
  CLI_GLOBAL_OPTIONS,
  resolveHelpEntry,
  quickWithMeta,
};
