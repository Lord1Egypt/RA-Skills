/* skill-to-http Console 中英双语字典 + i18n 工具
 *
 * 用法：
 *   HTML 中：<span x-text="t('nav.all')"></span>
 *   JS 中：  showToast(t('toast.startOk'))
 *   带参数：  t('toast.exposeFail', { name: 'foo' })  → 用 {name} 占位
 *   切换语言：Alpine.store('i18n').setLang('en')  // localStorage 持久化
 */
(function () {
  const DICT = {
    zh: {
      // ── Top Bar ───────────────────────────────────
      'top.running': '运行中',
      'top.stopped': '已停止',
      'top.port': '端口',
      'top.executor': '执行器',
      'top.uptime': '已运行',
      'top.active': '活跃',
      'top.start': '▶ 启动',
      'top.starting': '⏳ 启动中...',
      'top.stop': '■ 停止',
      'top.reload': '🔄 热重载',
      'top.apiKey': 'API Key',
      'top.langZh': '中',
      'top.langEn': 'EN',

      // ── Sidebar Nav ───────────────────────────────
      'nav.all': '全部 Skill',
      'nav.exposed': '已开启',
      'nav.hidden': '未开启',
      'nav.jobs': 'Job 历史',
      'nav.tls': 'HTTPS 证书',
      'nav.logs': '服务日志',

      // ── Skill Page ────────────────────────────────
      'skill.search': '搜索 Skill...',
      'skill.total': '共 {n} 个',
      'skill.enabled': '已开启',
      'skill.disabled': '未开启',
      'skill.enable': '开启',
      'skill.disable': '关闭',
      'skill.test': '测试',
      'skill.deps': '依赖',
      'skill.todayRuns': '{n} 次/今日',
      'skill.testTitle': '测试 {name}',
      'skill.testPlaceholder': '输入测试消息...',
      'skill.testRun': '运行',
      'skill.testCancel': '取消',
      'skill.testExecuting': '执行中...',
      'skill.testResult': '执行结果',
      'skill.testError': '执行失败',
      'skill.testSuccess': '执行成功',
      'skill.contextLevel': '上下文',
      'skill.contextFull': '完整',
      'skill.contextLight': '精简',

      // ── Jobs Page ─────────────────────────────────
      'jobs.title': 'Job 历史',
      'jobs.refresh': '🔄 刷新',
      'jobs.filterAll': '全部',
      'jobs.filterOk': '成功',
      'jobs.filterFail': '失败',
      'jobs.filterRunning': '进行中',
      'jobs.empty': '暂无 Job 记录',
      'jobs.col.time': '时间',
      'jobs.col.skill': 'Skill',
      'jobs.col.status': '状态',
      'jobs.col.duration': '耗时',
      'jobs.col.action': '操作',
      'jobs.viewDetail': '详情',

      // ── TLS Page ──────────────────────────────────
      'tls.title': 'HTTPS 证书',
      'tls.enabled': '✅ HTTPS 已启用',
      'tls.notEnabled': '⚠️ HTTPS 未启用',
      'tls.notEnabledDesc': '当前使用明文 HTTP，API Key 和数据传输未加密。建议启用 HTTPS。',
      'tls.upgrade.method1': '方式一：在服务器执行',
      'tls.upgrade.method2': '方式二：让 Agent 帮你操作',
      'tls.upgrade.copyCmd': '📋 复制命令',
      'tls.upgrade.copyAgent': '📋 复制给 Agent',
      'tls.upgrade.agentMsg': '帮我把 skill-to-http 服务升级到 HTTPS（自签证书 SAN 自动）',
      'tls.cert.subject': '证书主题',
      'tls.cert.san': 'SAN',
      'tls.cert.expiry': '到期时间',
      'tls.cert.renew': '🔁 续期证书',
      'tls.renew.title': '🔁 续期 TLS 证书',
      'tls.renew.warn': '续期将生成新证书并重启服务，客户端需重新信任。',
      'tls.renew.cmd': '在服务器执行以下命令：',
      'tls.renew.agentMsg': '帮我给 skill-to-http 续期 TLS 证书',
      'tls.renew.confirm': '确认续期 →',
      'tls.renew.cancel': '取消',

      // ── Logs Page ─────────────────────────────────
      'logs.title': '服务日志',
      'logs.refresh': '🔄 刷新',
      'logs.download': '⬇ 下载',
      'logs.tail': '尾部 {n} 行',
      'logs.empty': '暂无日志',

      // ── Auth Guide Modal ──────────────────────────
      'auth.title': '🔑 需要 API Key',
      'auth.desc': '控制台已开启鉴权保护，首次访问请填入 API Key。',
      'auth.howTitle': '如何获取？',
      'auth.how1': '查看配置文件 config.json 中的 api_key 字段',
      'auth.how2': '或在服务器执行：cat <workspace>/.http/secrets/api-keys/skill-to-http.key',
      'auth.how3': '也可以直接询问部署这个服务的同学 / Agent',
      'auth.placeholder': '粘贴 API Key，回车或点击下方按钮',
      'auth.later': '暂不填写',
      'auth.save': '保存并刷新 →',
      'auth.saving': '验证中...',
      'auth.note': 'Key 只保存在你浏览器本地（localStorage），不会上传到其他地方。',

      // ── Speed Mode ────────────────────────────────
      'speed.title': '⚡ 极速模式',
      'speed.on': '⚡ 极速',
      'speed.off': '极速',
      'speed.enabling': '启用中...',
      'speed.disabling': '关闭中...',
      'speed.confirm': '开启后 Skill 执行速度预计提升 2-4x（30-140s → 8-20s）',
      'speed.confirmDetail': '将创建独立的轻量 agent（stt-runner），仅用于加速 skill 执行，不影响主 agent。',
      'speed.confirmOn': '开启',
      'speed.confirmCancel': '取消',

      // ── Toasts (JS) ───────────────────────────────
      'toast.startOk': '服务已启动',
      'toast.startFail': '启动失败: {msg}',
      'toast.stopOk': '服务已停止',
      'toast.stopFail': '停止失败: {msg}',
      'toast.reloadOk': '已热重载',
      'toast.reloadFail': '重载失败: {msg}',
      'toast.serverNotRunning': '主服务未运行，请先点顶部「▶ 启动」按钮启动服务',
      'toast.serverStopped': '主服务已停止，请点顶部「▶ 启动」按钮重新启动后再测试',
      'toast.reqTimeout': '请求超时（主服务响应慢或已停止），请检查服务状态后重试',
      'toast.netError': '无法连接后端服务，请检查主服务是否运行（顶部状态栏），或刷新页面重试',
      'toast.execFail': '执行失败: {msg}',
      'toast.exposeFail': '开启失败: {msg}',
      'toast.hideFail': '关闭失败: {msg}',
      'toast.exposeOk': '已开启 {name}',
      'toast.hideOk': '已关闭 {name}',
      'toast.copyOk': '{label}已复制 ✅',
      'toast.copyFail': '复制失败，请手动选中复制',
      'toast.startTimeout': '启动超时或服务未就绪，请稍后刷新页面查看状态',
      'toast.authInvalid': 'API Key 不正确，请检查后重试',
      'toast.authOk': 'API Key 已保存，即将刷新',
      'toast.renewOk': '证书已续期',
      'toast.renewFail': '续期失败: {msg}',
      'toast.speedOn': '极速模式已开启',
      'toast.speedOff': '极速模式已关闭',
      'toast.speedFail': '极速模式操作失败: {msg}',
      'toast.certLoadFail': '加载证书信息失败 ({code})',

      // 通用
      'common.unknownError': '未知错误',

      // Auth 引导
      'auth.keyEmpty': '请输入 API Key',
      'auth.verifyFail': '验证失败：{msg}',

      // 测试 / 详情 / 日志
      'test.pollTimeout': '轮询超时 (240s)，任务可能仍在后台运行，可到 Job 历史页查看结果',
      'test.execFail': '执行失败',
      'detail.loadFail': '详情加载失败，显示列表缓存数据',
      'detail.netError': '网络错误：{msg}',
      'log.loading': '加载中...',
      'log.empty': '无日志',
      'log.loadFail': '加载失败: {msg}',

      // 极速模式按钮 / 提示
      'sm.connectFail': '连接失败: {msg}',
      'sm.btnLabel': '⚡ 极速模式',
      'sm.btnOn': '⚡ 极速',
      'sm.btnInitializing': '⏳ 初始化中...',
      'sm.titleNa': '仅 openclaw 执行器支持极速模式（当前: {exec}）',
      'sm.titleOn': '已开启极速模式（点击关闭）',
      'sm.titleOff': '开启极速模式，提升 2-4x 执行速度',

      // ── 补充：HTML/JS 静态文案（按原文匹配替换）───────────────
      // 顶栏 & 通用
      'p.loading': '加载中...',
      'p.loading2': '加载中',
      'p.preparing': '准备中...',
      'p.initializing': '⏳ 初始化中...',
      'p.execute': '▶ 执行',
      'p.copy': '📋 复制',
      'p.copyCmd': '📋 复制命令',
      'p.done': '完成',
      'p.match': '匹配',
      'p.field': '字段',
      // 顶栏字段 label（含冒号）
      '端口:': '端口:',
      '执行器:': '执行器:',
      '已运行:': '已运行:',
      '活跃:': '活跃:',
      '端口': '端口',
      '执行器': '执行器',
      '已运行': '已运行',
      '活跃': '活跃',
      // 带 emoji 前缀的标题
      'HTTPS 未启用': 'HTTPS 未启用',
      '🔐 当前证书': '🔐 当前证书',
      '📋 客户端如何信任此证书': '📋 客户端如何信任此证书',
      '续期结果': '续期结果',
      '证书主题': '证书主题',
      '证书路径': '证书路径',
      '私钥路径': '私钥路径',
      '到期时间': '到期时间',
      '服务正以 HTTP 模式运行。内网 IP 暴露场景建议启用 HTTPS。': '服务正以 HTTP 模式运行。内网 IP 暴露场景建议启用 HTTPS。',
      '方式一：在服务器上执行（复制命令）': '方式一：在服务器上执行（复制命令）',
      '方式二：发给你的 Agent 帮你执行（复制话术）': '方式二：发给你的 Agent 帮你执行（复制话术）',
      'HTTPS 已启用': 'HTTPS 已启用',
      '服务正在以 HTTPS 模式运行': '服务正在以 HTTPS 模式运行',
      '刷新': '刷新',
      // 确认弹窗（appState.showConfirm 通用组件）
      'cf.title': '确认操作',
      'cf.stopMsg': '确认停止服务？',
      'cf.ok': '确定',
      'cf.cancel': '取消',
      // 通用「取消」多处按钮
      '取消': '取消',
      '确定': '确定',
      '确认关闭': '确认关闭',
      '确认开启 →': '确认开启 →',
      '确认续期 →': '确认续期 →',
      // TLS 升级命令 / Agent 话术
      'tls.upgradeCmd': 'cd <skill-to-http目录>/scripts && python3 server.py upgrade-to-https',
      'tls.agentUpgradeMsg': '帮我把 skill-to-http 服务升级为 HTTPS：进入 skill-to-http 的 scripts 目录执行 python3 server.py upgrade-to-https，完成后重启服务并告诉我新的访问地址。',
      'tls.agentRenewMsg': '帮我给 skill-to-http 续期 TLS 证书：进入 skill-to-http 的 scripts 目录执行 python3 gen_cert.py renew --san auto，然后重启 skill-to-http 服务使新证书生效。',
      'tls.upgradeNote': '把 <code>&lt;skill-to-http目录&gt;</code> 替换为实际安装路径（通常在 workspace 的 skills/skill-to-http/）。升级会生成自签证书、更新配置，之后以 HTTPS 重启服务。',
      'tls.renewNote': '将重新生成自签证书，自动嗅探本机所有 IP 写入 SAN。',
      // HTTPS 说明文字（原样保留）
      '把': '把',
      '替换为实际安装路径（通常在 workspace 的 skills/skill-to-http/）。': '替换为实际安装路径（通常在 workspace 的 skills/skill-to-http/）。',
      '升级会生成自签证书、更新配置，之后以 HTTPS 重启服务。': '升级会生成自签证书、更新配置，之后以 HTTPS 重启服务。',
      '将重新生成自签证书，自动嗅探本机所有 IP 写入 SAN。': '将重新生成自签证书，自动嗅探本机所有 IP 写入 SAN。',

      // Speed Mode 弹窗全量
      'sm.confirmDesc1': '开启后 Skill 执行速度预计提升 ',
      'sm.confirmDesc2': '原理：为 skill-to-http 创建专用轻量 Agent（',
      'sm.confirmDesc3': '），减少每次执行注入的 system prompt（155k → ~35k tokens）。',
      'sm.sideEffect': '⚠️ 副作用：会在 OpenClaw 中注册一个名为 ',
      'sm.sideEffect2': ' 的 Agent，Gateway 会短暂重启（约 2-5s）',
      'sm.confirmOn': '确认开启 →',
      'sm.disableTitle': '关闭极速模式',
      'sm.disableDesc': '将从 OpenClaw 移除 ',
      'sm.disableDesc2': ' Agent，Gateway 会短暂重启。',
      'sm.disableConfirm': '确认关闭',
      'sm.initTitle': '⚡ 正在初始化极速模式...',

      // Skill 卡片、参数表
      'sk.noDesc': '（无描述）',
      'sk.paramsTable.param': '参数',
      'sk.paramsTable.type': '类型',
      'sk.paramsTable.required': '必填',
      'sk.paramsTable.desc': '说明',
      'sk.paramsTable.yes': '是',
      'sk.paramsTable.no': '否',
      'sk.noSchema': '无参数 schema',
      'sk.testPlaceholder': '输入测试消息...',
      'sk.testRunning': '⏳ 运行中... ',
      'sk.testDone': '✅ 完成',
      'sk.testFail': '❌ 失败',

      // Jobs 页
      'jb.filterPlaceholder': '按 Skill 名过滤...',
      'jb.refresh': '刷新',
      'jb.col.jobId': 'Job ID',
      'jb.col.skill': 'Skill',
      'jb.col.status': '状态',
      'jb.col.elapsed': '耗时',
      'jb.col.time': '时间',
      'jb.empty': '暂无记录',
      'jb.modalTitle': '📋 Job 详情',
      'jb.label.status': '状态',
      'jb.label.elapsed': '耗时',
      'jb.label.createdAt': '创建时间',
      'jb.label.finishedAt': '完成时间',
      'jb.label.errorType': '错误类型',
      'jb.label.message': 'Message',

      // 依赖弹窗
      'dep.title': '🔗 发现潜在依赖',
      'dep.desc1': '开启 ',
      'dep.desc2': ' 时检测到以下依赖：',
      'dep.viewEvidence': '查看证据',
      'dep.warn1': '⚠️ 如确认有依赖，极速模式执行时会自动注入依赖 Skill 的描述，如仍失败则降级到完整模式。',
      'dep.warn2': '选“无依赖”：不注入依赖描述，极速模式下可能因缺少上下文而运行失败。',
      'dep.noDeps': '无依赖，忽略',
      'dep.hasDeps': '确认有依赖',

      // TLS 页 补齐
      'tls2.currentCert': '当前证书',
      'tls2.daysLeft': '剩余天数',
      'tls2.expired': '已过期',
      'tls2.daysSuggest': '天（建议续期）',
      'tls2.loadFail': '加载证书信息失败 (HTTP ',
      'tls2.clientGuide': '客户端信任指南',
      'tls2.clientTitle': '客户端如何信任此证书',
      'tls2.doubleClick': '双击',
      'tls2.doubleClickInstall': '双击 → 安装到「受信任的根证书颁发机构」',
      'tls2.renewNote': '将重新生成自签证书，自动嗅探本机所有 IP 写入 SAN',
      'tls2.enabled': '✅ 已启用',
      'tls2.altAgent': '也可以不在页面操作，把下面命令发给你的 Agent 或在服务器执行',
      'tls2.copyAgent': '复制给 Agent',
      'tls2.copyResult': '复制结果',
      'tls2.instruction': '指令',
      'tls2.command': '命令',
      'tls2.content': '内容',

      // 复制/剪贴板
      'cp.copied': '已复制 ✅',
      'cp.copiedTo': '已复制到剪贴板',
      'cp.fail': '复制失败，请手动选中复制',
      'cp.copy': '复制',
      'cp.command': '命令',
      'cp.agentPrompt': 'Agent 指令',
      'cp.content': '内容',

      // Auth Guide 弹窗 补齐
      'ag.savedReloading': 'API Key 已保存，正在刷新...',
      'ag.localOnly': 'Key 只保存在你浏览器本地（localStorage），不会上传到其他地方。',
      'ag.howGet': '如何获取？',
      'ag.serverCmd': '或在服务器执行：',
      'ag.askDeployer': '也可以直接询问部署这个服务的同学 / Agent',
      'ag.checkConfig': '查看配置文件 ',
      'ag.checkConfig2': ' 中的 ',
      'ag.checkConfig3': ' 字段',

      // Toast/错误 补齐
      't2.startWait': '启动等待超时（服务可能仍在启动中，稍后点刷新查看状态）',
      't2.loadFail': '加载失败: ',
      't2.serverNotRunningPart': '主服务未运行，请先点顶部「▶ 启动',
      't2.speedNotOpenclaw': '仅 openclaw 执行器支持极速模式（当前: ',
      't2.speedSideRestart': '会短暂重启',

      // Speed mode 按钮 title
      'sb.enable': '开启极速模式，提升 2-4x 执行速度',
      'sb.disable': '已开启极速模式（点击关闭）',
      'sb.switchTip': '切换到中文',
    },

    en: {
      // ── Top Bar ───────────────────────────────────
      'top.running': 'Running',
      'top.stopped': 'Stopped',
      'top.port': 'Port',
      'top.executor': 'Executor',
      'top.uptime': 'Uptime',
      'top.active': 'Active',
      'top.start': '▶ Start',
      'top.starting': '⏳ Starting...',
      'top.stop': '■ Stop',
      'top.reload': '🔄 Reload',
      'top.apiKey': 'API Key',
      'top.langZh': '中',
      'top.langEn': 'EN',

      // ── Sidebar Nav ───────────────────────────────
      'nav.all': 'All Skills',
      'nav.exposed': 'Enabled',
      'nav.hidden': 'Disabled',
      'nav.jobs': 'Job History',
      'nav.tls': 'HTTPS Cert',
      'nav.logs': 'Service Logs',

      // ── Skill Page ────────────────────────────────
      'skill.search': 'Search skills...',
      'skill.total': '{n} total',
      'skill.enabled': 'Enabled',
      'skill.disabled': 'Disabled',
      'skill.enable': 'Enable',
      'skill.disable': 'Disable',
      'skill.test': 'Test',
      'skill.deps': 'Deps',
      'skill.todayRuns': '{n} runs today',
      'skill.testTitle': 'Test {name}',
      'skill.testPlaceholder': 'Enter test message...',
      'skill.testRun': 'Run',
      'skill.testCancel': 'Cancel',
      'skill.testExecuting': 'Executing...',
      'skill.testResult': 'Result',
      'skill.testError': 'Failed',
      'skill.testSuccess': 'Success',
      'skill.contextLevel': 'Context',
      'skill.contextFull': 'Full',
      'skill.contextLight': 'Light',

      // ── Jobs Page ─────────────────────────────────
      'jobs.title': 'Job History',
      'jobs.refresh': '🔄 Refresh',
      'jobs.filterAll': 'All',
      'jobs.filterOk': 'Success',
      'jobs.filterFail': 'Failed',
      'jobs.filterRunning': 'Running',
      'jobs.empty': 'No job records',
      'jobs.col.time': 'Time',
      'jobs.col.skill': 'Skill',
      'jobs.col.status': 'Status',
      'jobs.col.duration': 'Duration',
      'jobs.col.action': 'Action',
      'jobs.viewDetail': 'Detail',

      // ── TLS Page ──────────────────────────────────
      'tls.title': 'HTTPS Certificate',
      'tls.enabled': '✅ HTTPS Enabled',
      'tls.notEnabled': '⚠️ HTTPS Not Enabled',
      'tls.notEnabledDesc': 'Currently using plain HTTP. API Key and data transfer are not encrypted. It is recommended to enable HTTPS.',
      'tls.upgrade.method1': 'Option 1: Run on server',
      'tls.upgrade.method2': 'Option 2: Ask an Agent to help',
      'tls.upgrade.copyCmd': '📋 Copy Command',
      'tls.upgrade.copyAgent': '📋 Copy for Agent',
      'tls.upgrade.agentMsg': 'Please upgrade the skill-to-http service to HTTPS (self-signed cert with auto SAN)',
      'tls.cert.subject': 'Subject',
      'tls.cert.san': 'SAN',
      'tls.cert.expiry': 'Expires',
      'tls.cert.renew': '🔁 Renew Certificate',
      'tls.renew.title': '🔁 Renew TLS Certificate',
      'tls.renew.warn': 'Renewal will generate a new certificate and restart the service. Clients must re-trust it.',
      'tls.renew.cmd': 'Run the following on the server:',
      'tls.renew.agentMsg': 'Please renew the TLS certificate for skill-to-http',
      'tls.renew.confirm': 'Confirm Renew →',
      'tls.renew.cancel': 'Cancel',

      // ── Logs Page ─────────────────────────────────
      'logs.title': 'Service Logs',
      'logs.refresh': '🔄 Refresh',
      'logs.download': '⬇ Download',
      'logs.tail': 'Last {n} lines',
      'logs.empty': 'No logs',

      // ── Auth Guide Modal ──────────────────────────
      'auth.title': '🔑 API Key Required',
      'auth.desc': 'The console has auth enabled. Please provide an API Key on first access.',
      'auth.howTitle': 'How to get it?',
      'auth.how1': 'Check the api_key field in config.json',
      'auth.how2': 'Or run on the server: cat <workspace>/.http/secrets/api-keys/skill-to-http.key',
      'auth.how3': 'Or ask the person / Agent who deployed this service',
      'auth.placeholder': 'Paste API Key, press Enter or click below',
      'auth.later': 'Later',
      'auth.save': 'Save & Reload →',
      'auth.saving': 'Verifying...',
      'auth.note': 'The key is only stored locally in your browser (localStorage). It will not be uploaded anywhere.',

      // ── Speed Mode ────────────────────────────────
      'speed.title': '⚡ Speed Mode',
      'speed.on': '⚡ Speed',
      'speed.off': 'Speed',
      'speed.enabling': 'Enabling...',
      'speed.disabling': 'Disabling...',
      'speed.confirm': 'Speed mode boosts skill execution ~2-4x (30-140s → 8-20s)',
      'speed.confirmDetail': 'Creates a dedicated lightweight agent (stt-runner) for skill acceleration only. Does not affect the main agent.',
      'speed.confirmOn': 'Enable',
      'speed.confirmCancel': 'Cancel',

      // ── Toasts (JS) ───────────────────────────────
      'toast.startOk': 'Service started',
      'toast.startFail': 'Start failed: {msg}',
      'toast.stopOk': 'Service stopped',
      'toast.stopFail': 'Stop failed: {msg}',
      'toast.reloadOk': 'Reloaded',
      'toast.reloadFail': 'Reload failed: {msg}',
      'toast.serverNotRunning': 'Main service is not running. Please click "▶ Start" at the top first.',
      'toast.serverStopped': 'Main service has stopped. Please click "▶ Start" at the top to restart before testing.',
      'toast.reqTimeout': 'Request timed out (main service is slow or stopped). Please check status and retry.',
      'toast.netError': 'Cannot reach backend. Please check if the main service is running (top status bar) or reload the page.',
      'toast.execFail': 'Failed: {msg}',
      'toast.exposeFail': 'Enable failed: {msg}',
      'toast.hideFail': 'Disable failed: {msg}',
      'toast.exposeOk': 'Enabled {name}',
      'toast.hideOk': 'Disabled {name}',
      'toast.copyOk': '{label} copied ✅',
      'toast.copyFail': 'Copy failed, please select and copy manually',
      'toast.startTimeout': 'Start timed out or service not ready. Please reload the page later to check status.',
      'toast.authInvalid': 'Invalid API Key. Please check and retry.',
      'toast.authOk': 'API Key saved. Reloading...',
      'toast.renewOk': 'Certificate renewed',
      'toast.renewFail': 'Renew failed: {msg}',
      'toast.speedOn': 'Speed mode enabled',
      'toast.speedOff': 'Speed mode disabled',
      'toast.speedFail': 'Speed mode operation failed: {msg}',
      'toast.certLoadFail': 'Failed to load certificate info ({code})',

      // Common
      'common.unknownError': 'Unknown error',

      // Auth guide
      'auth.keyEmpty': 'Please enter API Key',
      'auth.verifyFail': 'Verification failed: {msg}',

      // Test / Detail / Log
      'test.pollTimeout': 'Polling timeout (240s). Job may still be running in background; check Job History.',
      'test.execFail': 'Execution failed',
      'detail.loadFail': 'Failed to load details, showing cached list data',
      'detail.netError': 'Network error: {msg}',
      'log.loading': 'Loading...',
      'log.empty': 'No logs',
      'log.loadFail': 'Load failed: {msg}',

      // Speed mode button / tooltip
      'sm.connectFail': 'Connection failed: {msg}',
      'sm.btnLabel': '⚡ Speed Mode',
      'sm.btnOn': '⚡ Speed',
      'sm.btnInitializing': '⏳ Initializing...',
      'sm.titleNa': 'Speed mode only supported by openclaw executor (current: {exec})',
      'sm.titleOn': 'Speed mode is on (click to disable)',
      'sm.titleOff': 'Enable speed mode for 2-4x execution boost',

      // ── 补充：HTML/JS 静态文案 ─────────────────────────
      'p.loading': 'Loading...',
      'p.loading2': 'Loading',
      'p.preparing': 'Preparing...',
      'p.initializing': '⏳ Initializing...',
      'p.execute': '▶ Run',
      'p.copy': '📋 Copy',
      'p.copyCmd': '📋 Copy command',
      'p.done': 'Done',
      'p.match': 'match',
      'p.field': 'field',
      '端口:': 'Port:',
      '执行器:': 'Executor:',
      '已运行:': 'Uptime:',
      '活跃:': 'Active:',
      '端口': 'Port',
      '执行器': 'Executor',
      '已运行': 'Uptime',
      '活跃': 'Active',
      'HTTPS 未启用': 'HTTPS Not Enabled',
      '🔐 当前证书': '🔐 Current Certificate',
      '📋 客户端如何信任此证书': '📋 How to Trust This Certificate',
      '续期结果': 'Renewal Result',
      '证书主题': 'Subject',
      '证书路径': 'Cert Path',
      '私钥路径': 'Key Path',
      '到期时间': 'Expires',
      '服务正以 HTTP 模式运行。内网 IP 暴露场景建议启用 HTTPS。': 'Service is running in plain HTTP mode. HTTPS is recommended when the internal IP is exposed.',
      '方式一：在服务器上执行（复制命令）': 'Option 1: Run on the server (copy the command)',
      '方式二：发给你的 Agent 帮你执行（复制话术）': 'Option 2: Send to your Agent (copy the prompt)',
      'HTTPS 已启用': 'HTTPS Enabled',
      '服务正在以 HTTPS 模式运行': 'Service is running in HTTPS mode',
      '刷新': 'Refresh',
      // 确认弹窗
      'cf.title': 'Confirm',
      'cf.stopMsg': 'Stop the service?',
      'cf.ok': 'OK',
      'cf.cancel': 'Cancel',
      '取消': 'Cancel',
      '确定': 'OK',
      '确认关闭': 'Confirm Disable',
      '确认开启 →': 'Confirm Enable →',
      '确认续期 →': 'Confirm Renew →',
      // TLS 升级命令 / Agent 话术（EN）
      'tls.upgradeCmd': 'cd <skill-to-http-dir>/scripts && python3 server.py upgrade-to-https',
      'tls.agentUpgradeMsg': 'Please upgrade skill-to-http to HTTPS: cd into skill-to-http/scripts and run `python3 server.py upgrade-to-https`, then restart the service and tell me the new URL.',
      'tls.agentRenewMsg': 'Please renew the TLS certificate for skill-to-http: cd into skill-to-http/scripts and run `python3 gen_cert.py renew --san auto`, then restart the service so the new cert takes effect.',
      'tls.upgradeNote': 'Replace <code>&lt;skill-to-http-dir&gt;</code> with the actual install path (typically workspace/skills/skill-to-http/). The upgrade generates a self-signed cert, updates the config, then restarts the service in HTTPS mode.',
      'tls.renewNote': 'Regenerates a self-signed cert and auto-detects all local IPs into SAN.',
      // HTTPS 说明文字
      '把': 'Replace',
      '替换为实际安装路径（通常在 workspace 的 skills/skill-to-http/）。': ' with the actual install path (typically workspace/skills/skill-to-http/).',
      '升级会生成自签证书、更新配置，之后以 HTTPS 重启服务。': 'The upgrade generates a self-signed cert, updates the config, then restarts the service in HTTPS.',
      '将重新生成自签证书，自动嗅探本机所有 IP 写入 SAN。': 'Regenerates a self-signed cert, auto-detects all local IPs into SAN.',

      'sm.confirmDesc1': 'After enabling, skill execution speed is expected to boost ',
      'sm.confirmDesc2': 'How it works: creates a dedicated lightweight Agent (',
      'sm.confirmDesc3': ') for skill-to-http, reducing the system prompt injected on each run (155k → ~35k tokens).',
      'sm.sideEffect': '⚠️ Side effect: registers an Agent named ',
      'sm.sideEffect2': ' in OpenClaw. Gateway will briefly restart (~2-5s).',
      'sm.confirmOn': 'Confirm Enable →',
      'sm.disableTitle': 'Disable Speed Mode',
      'sm.disableDesc': 'Will remove ',
      'sm.disableDesc2': ' Agent from OpenClaw. Gateway will briefly restart.',
      'sm.disableConfirm': 'Confirm Disable',
      'sm.initTitle': '⚡ Initializing speed mode...',

      'sk.noDesc': '(no description)',
      'sk.paramsTable.param': 'Param',
      'sk.paramsTable.type': 'Type',
      'sk.paramsTable.required': 'Required',
      'sk.paramsTable.desc': 'Description',
      'sk.paramsTable.yes': 'Yes',
      'sk.paramsTable.no': 'No',
      'sk.noSchema': 'No params schema',
      'sk.testPlaceholder': 'Enter test message...',
      'sk.testRunning': '⏳ Running... ',
      'sk.testDone': '✅ Done',
      'sk.testFail': '❌ Failed',

      'jb.filterPlaceholder': 'Filter by skill name...',
      'jb.refresh': 'Refresh',
      'jb.col.jobId': 'Job ID',
      'jb.col.skill': 'Skill',
      'jb.col.status': 'Status',
      'jb.col.elapsed': 'Elapsed',
      'jb.col.time': 'Time',
      'jb.empty': 'No records',
      'jb.modalTitle': '📋 Job Detail',
      'jb.label.status': 'Status',
      'jb.label.elapsed': 'Elapsed',
      'jb.label.createdAt': 'Created',
      'jb.label.finishedAt': 'Finished',
      'jb.label.errorType': 'Error Type',
      'jb.label.message': 'Message',

      'dep.title': '🔗 Potential Dependencies Detected',
      'dep.desc1': 'Enabling ',
      'dep.desc2': ' detected the following dependencies:',
      'dep.viewEvidence': 'View evidence',
      'dep.warn1': '⚠️ If confirmed, speed mode will auto-inject dependency skill descriptions on execution, and fall back to full mode on failure.',
      'dep.warn2': 'Choose "No deps": no dependency descriptions injected, speed mode may fail due to missing context.',
      'dep.noDeps': 'No deps, ignore',
      'dep.hasDeps': 'Confirm deps',

      'tls2.currentCert': 'Current Certificate',
      'tls2.daysLeft': 'Days remaining',
      'tls2.expired': 'Expired',
      'tls2.daysSuggest': ' days (renewal recommended)',
      'tls2.loadFail': 'Failed to load certificate info (HTTP ',
      'tls2.clientGuide': 'Client Trust Guide',
      'tls2.clientTitle': 'How to trust this certificate on client',
      'tls2.doubleClick': 'Double-click',
      'tls2.doubleClickInstall': 'Double-click → install to "Trusted Root Certification Authorities"',
      'tls2.renewNote': 'Regenerates the self-signed cert, auto-detects all local IPs into SAN',
      'tls2.enabled': '✅ Enabled',
      'tls2.altAgent': 'You can also skip the UI and send the command below to your Agent, or run it on the server',
      'tls2.copyAgent': 'Copy for Agent',
      'tls2.copyResult': 'Result',
      'tls2.instruction': 'Instruction',
      'tls2.command': 'Command',
      'tls2.content': 'Content',

      'cp.copied': 'Copied ✅',
      'cp.copiedTo': 'Copied to clipboard',
      'cp.fail': 'Copy failed, please select and copy manually',
      'cp.copy': 'Copy',
      'cp.command': 'Command',
      'cp.agentPrompt': 'Agent Prompt',
      'cp.content': 'Content',

      'ag.savedReloading': 'API Key saved, reloading...',
      'ag.localOnly': 'The key is only stored locally in your browser (localStorage). It will not be uploaded anywhere.',
      'ag.howGet': 'How to get it?',
      'ag.serverCmd': 'Or run on the server:',
      'ag.askDeployer': 'Or ask the person / Agent who deployed this service',
      'ag.checkConfig': 'Check the ',
      'ag.checkConfig2': ' field in ',
      'ag.checkConfig3': ' file',

      't2.startWait': 'Start wait timeout (service may still be starting; click Refresh later to check status)',
      't2.loadFail': 'Load failed: ',
      't2.serverNotRunningPart': 'Main service not running. Please click "▶ Start" at the top',
      't2.speedNotOpenclaw': 'Only openclaw executor supports speed mode (current: ',
      't2.speedSideRestart': 'briefly restart',

      'sb.enable': 'Enable speed mode for 2-4x execution boost',
      'sb.disable': 'Speed mode is on (click to disable)',
      'sb.switchTip': 'Switch to Chinese',
    },
  };

  const STORAGE_KEY = 'stt-lang';
  const DEFAULT_LANG = (() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved === 'zh' || saved === 'en') return saved;
    } catch (_) {}
    // 依据浏览器语言初值
    const nav = (navigator.language || 'zh').toLowerCase();
    return nav.startsWith('zh') ? 'zh' : 'en';
  })();

  const state = {
    lang: DEFAULT_LANG,
  };

  function interpolate(str, params) {
    if (!params) return str;
    return str.replace(/\{(\w+)\}/g, (_, k) => (k in params ? params[k] : '{' + k + '}'));
  }

  // ── 反向映射：zh 原文 → key ──────────────────────────────────
  // 用于运行时 DOM 扫描替换：找到 zh 字典里存在的原文就替换成当前语言
  const REVERSE_ZH = {};
  Object.entries(DICT.zh).forEach(([k, v]) => {
    // 只索引 "纯静态无占位符" 的短语，占位符（含 {n} {name} 等）走 t() 显式调用
    if (!/\{\w+\}/.test(v)) REVERSE_ZH[v.trim()] = k;
  });

  // 从当前 DOM 节点的中文文本反查 key，返回目标语言译文
  function translateByReverse(text) {
    if (!text) return null;
    const trimmed = text.trim();
    if (!trimmed) return null;
    const key = REVERSE_ZH[trimmed];
    if (!key) return null;
    const target = (DICT[state.lang] || DICT.zh)[key];
    if (!target) return null;
    // 保留原来两侧的空白
    return text.replace(trimmed, target);
  }

  // 递归遍历 DOM，替换 text node 和常见属性（placeholder/title/alt）
  function walkAndTranslate(root) {
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
    let node;
    while ((node = walker.nextNode())) {
      if (node.nodeType === 3) {
        // TEXT_NODE
        // 跳过 <script>/<style> 里的文本
        const p = node.parentNode;
        if (!p) continue;
        const tag = (p.tagName || '').toLowerCase();
        if (tag === 'script' || tag === 'style') continue;
        // 保存原文（首次），以便切回 zh 时能恢复
        if (!node.__i18nOrig) node.__i18nOrig = node.nodeValue;
        const orig = node.__i18nOrig;
        const t2 = translateByReverse(orig);
        if (t2 !== null) node.nodeValue = t2;
        else if (state.lang === 'zh') node.nodeValue = orig; // 无匹配时切回原文
      } else if (node.nodeType === 1) {
        // ELEMENT_NODE - 属性
        ['placeholder', 'title', 'alt', 'aria-label'].forEach((attr) => {
          if (node.hasAttribute(attr)) {
            const origAttr = '__i18nOrig_' + attr;
            if (!node[origAttr]) node[origAttr] = node.getAttribute(attr);
            const orig = node[origAttr];
            const t2 = translateByReverse(orig);
            if (t2 !== null) node.setAttribute(attr, t2);
            else if (state.lang === 'zh') node.setAttribute(attr, orig);
          }
        });
      }
    }
  }

  // 全局 t()
  window.t = function (key, params) {
    const dict = DICT[state.lang] || DICT.zh;
    const s = dict[key];
    if (s === undefined) return key; // 回退：直接显示 key，便于发现漏翻
    return interpolate(s, params);
  };

  // 供外部调用的 DOM 扫描函数（切换语言或 Alpine 渲染更新后调用）
  window.i18nApply = function () {
    walkAndTranslate(document.body);
  };

  // 注册 Alpine store（Alpine 加载后调用）
  document.addEventListener('alpine:init', () => {
    Alpine.store('i18n', {
      lang: state.lang,
      // 变更 tick，触发所有 x-text="$store.i18n.tick, t('key')" 重算
      tick: 0,
      setLang(l) {
        if (l !== 'zh' && l !== 'en') return;
        state.lang = l;
        this.lang = l;
        this.tick++;
        try { localStorage.setItem(STORAGE_KEY, l); } catch (_) {}
        document.documentElement.setAttribute('lang', l === 'en' ? 'en' : 'zh-CN');
        // 更新 <title>
        document.title = l === 'en' ? 'skill-to-http Console' : 'skill-to-http 控制台';
        // 触发 DOM 扫描替换
        setTimeout(() => window.i18nApply(), 30);
      },
      toggle() {
        this.setLang(this.lang === 'zh' ? 'en' : 'zh');
      },
    });

    // 初始化 lang 属性
    document.documentElement.setAttribute('lang', state.lang === 'en' ? 'en' : 'zh-CN');
    document.title = state.lang === 'en' ? 'skill-to-http Console' : 'skill-to-http 控制台';
  });

  // 首次 DOM 就绪后应用一次
  const initialApply = () => {
    if (state.lang !== 'zh') {
      // 稍延迟等 Alpine 完成初始渲染
      setTimeout(() => window.i18nApply(), 100);
      // 再兜底几次（Alpine 异步渲染 skill 列表等）
      setTimeout(() => window.i18nApply(), 500);
      setTimeout(() => window.i18nApply(), 1500);
    }
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialApply);
  } else {
    initialApply();
  }

  // MutationObserver 兜底：Alpine 动态渲染新节点时自动翻译
  const observer = new MutationObserver((muts) => {
    if (state.lang === 'zh') return; // zh 不需要翻译（DOM 原文就是 zh）
    // 节流：合并多次变更
    if (observer._t) return;
    observer._t = setTimeout(() => {
      observer._t = null;
      window.i18nApply();
    }, 80);
  });
  if (document.body) {
    observer.observe(document.body, { childList: true, subtree: true, characterData: true });
  } else {
    document.addEventListener('DOMContentLoaded', () => {
      observer.observe(document.body, { childList: true, subtree: true, characterData: true });
    });
  }
})();
