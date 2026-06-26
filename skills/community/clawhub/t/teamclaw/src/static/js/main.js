const i18n = {
    'zh-CN': {
        // 通用
        loading: '加载中...',
        error: '错误',
        success: '成功',
        cancel: '取消',
        confirm: '确认',
        close: '关闭',

        // 登录页
        login_title: 'Teamclaw',
        login_subtitle: '请登录以开始对话',
        username: '用户名',
        password: '密码',
        login_btn: '登录',
        login_verifying: '验证中...',
        login_error_invalid: '用户名只能包含字母、数字、下划线、短横线或中文',
        login_error_failed: '登录失败',
        login_error_network: '网络错误',
        login_footer: '身份验证后方可使用，对话和文件按用户隔离',

        // 头部
        encrypted: '● 已加密',
        history: '🤖Agents',
        new_chat: '+新',
        new_chat_mobile: '+',
        logout: '退出',
        current_session: '当前对话号',
        more_actions: '更多操作',

        // 移动端菜单
        menu_history: '🤖 Agents',
        menu_new: '➕ 新对话',
        menu_oasis: '🏛️ TeamsWork',
        menu_logout: '🚪 退出',

        // 聊天区域
        welcome_message: '你好！我是 TeamBot 智能助手。我已经准备好为你服务，请输入你的指令。',
        new_session_message: '🆕 已开启新对话。我是 TeamBot 智能助手，请输入你的指令。',
        input_placeholder: '输入指令...（可粘贴图片/上传文件/录音）',
        send_btn: '发送',
        cancel_btn: '终止',
        busy_btn: '系统占用中',
        new_system_msg: '有新的系统消息',
        click_refresh: '点击刷新',
        no_response: '（无响应）',
        thinking_stopped: '⚠️ 已终止思考',
        login_expired: '⚠️ 登录已过期，请重新登录',
        agent_error: '❌ 错误',

        // 工具面板
        available_tools: '🧰 可用工具',
        tool_calling: '（调用工具中...）',
        tool_return: '🔧 工具返回',

        // 文件上传
        max_images: '最多上传5张图片',
        max_files: '最多上传3个文件',
        max_audios: '最多上传2个音频',
        audio_too_large: '音频过大，上限 25MB',
        video_too_large: '视频过大，上限 50MB',
        pdf_too_large: 'PDF过大，上限 10MB',
        file_too_large: '文件过大，上限 512KB',
        unsupported_type: '不支持的文件类型',
        supported_types: '支持: txt, md, csv, json, py, js, pdf, mp3, wav, avi, mp4 等',

        // 录音
        recording_title: '录音',
        recording_stop: '点击停止录音',
        mic_permission_denied: '无法访问麦克风，请检查浏览器权限设置。',
        recording_too_long: '录音过长，上限 25MB',

        // 历史会话
        history_title: '🤖 Agents',
        history_loading: '加载中...',
        history_empty: '暂无历史对话',
        history_error: '加载失败',
        history_loading_msg: '加载历史消息...',
        history_no_msg: '（此对话暂无消息记录）',
        new_session_confirm: '开启新对话？当前对话的历史记录将保留，可通过切回对话号恢复。',
        messages_count: '条消息',
        session_id: '对话号',
        delete_session: '删除',
        delete_session_confirm: '确定删除此对话？删除后不可恢复。',
        delete_all_confirm: '确定删除所有对话记录？此操作不可恢复！',
        delete_success: '删除成功',
        delete_fail: '删除失败',
        delete_all: '🗑️ 清空全部',

        // TTS
        tts_read: '朗读',
        tts_stop: '停止',
        tts_loading: '加载中...',
        tts_request_failed: 'TTS 请求失败',
        code_omitted: '（代码省略）',
        image_placeholder: '(图片)',
        audio_placeholder: '(语音)',
        file_placeholder: '(文件)',

        // OASIS
        oasis_title: 'TeamsWork 讨论论坛',
        oasis_subtitle: '多专家并行讨论系统',
        oasis_topics: '📋 讨论话题',
        oasis_topics_count: '个话题',
        oasis_no_topics: '暂无讨论话题',
        oasis_start_hint: '在聊天中让 Agent 发起 TeamsWork 讨论',
        oasis_back: '← 返回',
        oasis_conclusion: '讨论结论',
        oasis_waiting: '等待专家发言...',
        oasis_status_pending: '等待中',
        oasis_status_discussing: '讨论中',
        oasis_status_concluded: '已完成',
        oasis_status_error: '出错',
        oasis_status_cancelled: '已终止',
        oasis_round: '轮',
        oasis_posts: '帖',
        oasis_expert_creative: '创意专家',
        oasis_expert_critical: '批判专家',
        oasis_expert_data: '数据分析师',
        oasis_expert_synthesis: '综合顾问',
        oasis_cancel: '终止讨论',
        oasis_cancel_confirm: '确定要强制终止此讨论？',
        oasis_cancel_success: '讨论已终止',
        oasis_delete: '删除记录',
        oasis_delete_confirm: '确定要永久删除此讨论记录？删除后不可恢复。',
        oasis_delete_success: '记录已删除',
        oasis_action_fail: '操作失败',

        // 页面切换
        tab_chat: '💬 对话',
        tab_group: '👥 群聊',
        tab_orchestrate: '🎨 编排',

        // 群聊
        group_title: '👥 群聊列表',
        group_new: '+ 新建',
        group_no_groups: '暂无群聊',
        group_select_hint: '选择或创建一个群聊',
        group_members_btn: '👤 成员',
        group_mute: '🔇 急停',
        group_unmute: '🔊 恢复',
        group_members: '成员管理',
        group_current_members: '当前成员',
        group_add_agents: '添加 Agent Session',
        group_input_placeholder: '发送消息...',
        group_create_title: '创建群聊',
        group_name_placeholder: '群聊名称',
        group_no_sessions: '没有可用的 Agent Session',
        group_create_btn: '创建',
        group_delete_confirm: '确定删除此群聊？',
        group_owner: '群主',
        group_agent: 'Agent',
        group_msg_count: '条消息',
        group_member_count: '人',

        // 离线提示
        offline_banner: '⚠️ 网络已断开，请检查连接',

        // 编排面板
        orch_expert_pool: '🧑‍💼 专家池',
        orch_expert_pool_text: '专家池',
        orch_preset_experts: '📚 预设专家',
        orch_custom_experts: '🛠️ 自定义专家',
        orch_session_agents: '💬 Session Agent',
orch_openclaw_sessions: '🦞 OpenClaw',
        orch_manual_inject: '手动注入',
        orch_shortcuts_title: '快捷操作：',
        orch_shortcuts_body: '拖入专家到画布 · 连接端口=工作流 · Ctrl+G=分组 · 双击快速添加',
        // Orchestration toolbar buttons
        orch_btn_arrange: '🔄 排列',
        orch_btn_save: '💾 保存',
        orch_btn_load: '📂 加载',
        orch_btn_ai: '🤖 AI编排',
        orch_btn_export: '📋 导出',
        orch_btn_status: '🔄 状态',
        orch_btn_clear: '🗑️ 清空',
        orch_tip_arrange: '自动排列',
        orch_tip_save: '保存布局',
        orch_tip_load: '加载布局',
        orch_tip_ai: 'AI 生成 YAML',
        orch_tip_export: '复制 YAML',
        orch_tip_status: '刷新 session 状态',
        orch_tip_clear: '清空画布',
        // Canvas hints
        orch_hint_drag: '拖入专家开始编排',
        // Nav controls
        orch_tip_up: '上移',
        orch_tip_down: '下移',
        orch_tip_left: '左移',
        orch_tip_right: '右移',
        orch_tip_reset: '重置视图',
        orch_tip_zoomout: '缩小',
        orch_tip_zoomin: '放大',
        // Right panel
        orch_settings: '⚙️ 设置',
        orch_repeat: '每轮重复计划',
        orch_rounds: '轮次:',
        orch_stateful: '有状态模式',
        orch_threshold: '聚类阈值:',
        orch_ai_gen: '🤖 AI 生成',
        orch_ai_hint: '点击「🤖 AI编排」自动生成 YAML',
        orch_prompt_label: '📨 发送的 Prompt',
        orch_prompt_copy: '复制',
        orch_prompt_hint: '点击 AI编排 后显示',
        orch_agent_yaml_label: '🤖 Agent YAML',
        orch_agent_yaml_copy: '复制',
        orch_agent_yaml_hint: '等待 Agent 生成',
        orch_rule_yaml: '📄 规则 YAML',
        orch_rule_yaml_hint: '拖入专家后自动生成...',
        orch_status_bar: '节点: {nodes} | 连线: {edges} | 分组: {groups}',
        orch_status_bar_init: '节点: 0 | 连线: 0 | 分组: 0',
        orch_manual_inject: '手动注入',
        orch_node_remove: '移除',
        orch_default_author: '主持人',
        orch_yaml_valid: '✅ 有效 YAML — {steps} 步骤 [{types}]',
        orch_yaml_saved_suffix: ' | 💾 已保存: {file}',
        orch_yaml_warn: '⚠️ YAML 校验问题: {error}',
        orch_comm_fail: '# 通信失败: {msg}',
        // Context menu
        orch_ctx_duplicate: '📋 复用此专家 (同序号)',
        orch_ctx_new_instance: '➕ 新建实例 (新序号)',
        orch_ctx_group_parallel: '🔀 创建并行分组',
        orch_ctx_group_all: '👥 创建全员分组',
        orch_ctx_delete: '🗑️ 删除选中',
        orch_ctx_refresh_yaml: '🔄 刷新 YAML',
        orch_ctx_clear: '🗑️ 清空画布',
        // Group labels
        orch_group_parallel: '🔀 并行',
        orch_group_all: '👥 全员',
        orch_group_dissolve: '解散',
        // Modals
        orch_modal_edit_manual: '📝 编辑手动注入内容',
        orch_modal_author_ph: '作者',
        orch_modal_content_ph: '注入内容...',
        orch_modal_cancel: '取消',
        orch_modal_save: '保存',
        orch_modal_select_session: '🎯 选择目标 Agent Session',
        orch_modal_select_desc: '选择一个已有的对话 Session，或新建一个，生成完成后可跳转继续对话。',
        orch_modal_loading: '⏳ 加载中...',
        orch_modal_new_session: '新建对话',
        orch_modal_confirm_gen: '确认并生成',
        orch_modal_select_layout: '📂 选择布局',
        orch_modal_delete: '🗑️ 删除',
        orch_modal_load: '加载',
        // Toast messages
        orch_toast_arranged: '已自动排列',
        orch_toast_saved: '已保存: {name}',
        orch_toast_save_fail: '保存失败',
        orch_toast_no_layouts: '没有已保存的布局',
        orch_toast_deleted: '已删除: {name}',
        orch_toast_del_fail: '删除失败',
        orch_toast_loaded: '已加载: {name}',
        orch_toast_load_fail: '加载失败',
        orch_toast_yaml_copied: 'YAML 已复制!',
        orch_toast_gen_yaml: '请先生成 YAML',
        orch_toast_prompt_copied: 'Prompt 已复制',
        orch_toast_agent_yaml_copied: 'Agent YAML 已复制',
        orch_toast_select_2: '请先选中至少2个节点',
        orch_toast_add_first: '请先添加专家节点',
        orch_toast_agent_unavail: 'Agent 不可用',
        orch_toast_yaml_generated: 'YAML 已生成并保存! ✅',
        orch_toast_agent_valid: 'Agent 生成了有效的 YAML! ✅',
        orch_toast_session_updated: 'Session 状态已更新',
        orch_toast_session_fail: '获取状态失败',
        orch_toast_no_session: '没有选中的 Session',
        orch_toast_jumped: '已跳转到对话 #{id}',
        orch_toast_custom_added: '自定义专家已添加: {name}',
        orch_toast_fill_info: '请填写完整信息',
        orch_toast_net_error: '网络错误',
        orch_toast_expert_deleted: '已删除: {name}',
        orch_toast_expert_del_fail: '删除失败',
        // Confirm dialogs
        orch_confirm_del_expert: '删除自定义专家 "{name}"？',
        orch_confirm_del_layout: '确定删除布局 "{name}"？',
        orch_prompt_layout_name: '布局名称:',
        // Agent status
        orch_status_communicating: '🔄 正在与 Agent 通信 (Session: #{id})...',
        orch_status_generating: '⏳ 生成中...',
        orch_status_waiting: '⏳ 等待 Agent 返回...',
        orch_status_auth_fail: '认证失败',
        orch_status_agent_unavail: 'Agent 不可用',
        orch_status_conn_error: '❌ 连接错误',
        orch_goto_chat: '💬 跳转到对话 {session} 继续聊天',
        orch_no_custom: '暂无自定义专家',
        orch_no_session: '暂无 Session',
        orch_load_fail: '❌ 加载失败',
        orch_load_session_fail: '❌ 加载 Session 列表失败',
        orch_msg_count: '{count}条消息',
        orch_add_expert_title: '🛠️ 添加自定义专家',
        orch_add_expert_btn: '添加自定义专家',
        orch_label_name: '名称',
        orch_label_tag: 'Tag (英文)',
        orch_label_temp: 'Temperature',
        orch_label_persona: 'Persona (角色描述)',
        orch_ph_name: '如：金融分析师',
        orch_ph_tag: '如：finance',
        orch_ph_persona: '描述这位专家的角色、专长和行为风格...',

        // Add Workflow
        wf_btn_title: '添加工作流',
        wf_popup_title: '📋 选择工作流',
        wf_no_workflows: '暂无已保存的工作流',
        wf_cancel: '取消',
        wf_confirm: '添加',
        wf_context_prefix: '[工作流: {name}] ',

        // 其他
        splash_subtitle: 'TeamBot AI Agent',
        secure_footer: 'Secured by Nginx Reverse Proxy & SSH Tunnel',
        refresh: '刷新',
        collapse: '收起',

        // 设置
        settings: '⚙️',
        settings_title: '⚙️ 系统设置',
        settings_save: '保存',
        settings_saved: '✅ 设置已保存',
        settings_save_fail: '❌ 保存失败',
        settings_load_fail: '❌ 加载设置失败',
        settings_restart_hint: '部分配置需要重启服务后生效',
        menu_settings: '⚙️ 设置',
        settings_group_llm: 'LLM 模型配置',
        settings_group_tts: 'TTS 语音配置',
        settings_group_openclaw: 'OpenClaw 集成',
        settings_group_ports: '端口配置',
        settings_group_bots: '机器人集成',
        settings_group_other: '其他',
    },
    'en': {
        // General
        loading: 'Loading...',
        error: 'Error',
        success: 'Success',
        cancel: 'Cancel',
        confirm: 'Confirm',
        close: 'Close',

        // Login
        login_title: 'Teamclaw',
        login_subtitle: 'Please login to start',
        username: 'Username',
        password: 'Password',
        login_btn: 'Login',
        login_verifying: 'Verifying...',
        login_error_invalid: 'Username can only contain letters, numbers, underscore, hyphen or Chinese',
        login_error_failed: 'Login failed',
        login_error_network: 'Network error',
        login_footer: 'Authentication required. Conversations and files are isolated by user',

        // Header
        encrypted: '● Encrypted',
        history: '🤖 Agents',
        new_chat: '+New',
        new_chat_mobile: '+',
        logout: 'Logout',
        current_session: 'Current session',
        more_actions: 'More actions',

        // Mobile menu
        menu_history: '🤖 Agents',
        menu_new: '➕ New Chat',
        menu_oasis: '🏛️ TeamsWork',
        menu_logout: '🚪 Logout',

        // Chat area
        welcome_message: 'Hello! I am TeamBot AI Assistant. Ready to serve you. Please enter your instructions.',
        new_session_message: '🆕 New conversation started. I am TeamBot AI Assistant. Please enter your instructions.',
        input_placeholder: 'Enter command... (paste images/upload files/record audio)',
        send_btn: 'Send',
        cancel_btn: 'Stop',
        busy_btn: 'System Busy',
        new_system_msg: 'New system message',
        click_refresh: 'Click to refresh',
        no_response: '(No response)',
        thinking_stopped: '⚠️ Thinking stopped',
        login_expired: '⚠️ Session expired, please login again',
        agent_error: '❌ Error',

        // Tool panel
        available_tools: '🧰 Available Tools',
        tool_calling: '(Calling tool...)',
        tool_return: '🔧 Tool Return',

        // File upload
        max_images: 'Maximum 5 images',
        max_files: 'Maximum 3 files',
        max_audios: 'Maximum 2 audio files',
        audio_too_large: 'Audio too large, limit 25MB',
        video_too_large: 'Video too large, limit 50MB',
        pdf_too_large: 'PDF too large, limit 10MB',
        file_too_large: 'File too large, limit 512KB',
        unsupported_type: 'Unsupported file type',
        supported_types: 'Supported: txt, md, csv, json, py, js, pdf, mp3, wav, avi, mp4, etc.',

        // Recording
        recording_title: 'Record',
        recording_stop: 'Click to stop recording',
        mic_permission_denied: 'Cannot access microphone. Please check browser permissions.',
        recording_too_long: 'Recording too long, limit 25MB',

        // History sessions
        history_title: '🤖 Agents',
        history_loading: 'Loading...',
        history_empty: 'No history',
        history_error: 'Failed to load',
        history_loading_msg: 'Loading messages...',
        history_no_msg: '(No messages in this conversation)',
        new_session_confirm: 'Start new conversation? Current history will be preserved.',
        messages_count: 'messages',
        session_id: 'Session',
        delete_session: 'Delete',
        delete_session_confirm: 'Delete this conversation? This cannot be undone.',
        delete_all_confirm: 'Delete ALL conversations? This cannot be undone!',
        delete_success: 'Deleted',
        delete_fail: 'Delete failed',
        delete_all: '🗑️ Clear All',

        // TTS
        tts_read: 'Read',
        tts_stop: 'Stop',
        tts_loading: 'Loading...',
        tts_request_failed: 'TTS request failed',
        code_omitted: '(code omitted)',
        image_placeholder: '(image)',
        audio_placeholder: '(audio)',
        file_placeholder: '(file)',

        // OASIS
        oasis_title: 'TeamsWork Discussion Forum',
        oasis_subtitle: 'Multi-Expert Parallel Discussion System',
        oasis_topics: '📋 Discussion Topics',
        oasis_topics_count: 'topics',
        oasis_no_topics: 'No discussion topics',
        oasis_start_hint: 'Ask Agent to start a TeamsWork discussion in chat',
        oasis_back: '← Back',
        oasis_conclusion: 'Conclusion',
        oasis_waiting: 'Waiting for experts...',
        oasis_status_pending: 'Pending',
        oasis_status_discussing: 'Discussing',
        oasis_status_concluded: 'Completed',
        oasis_status_error: 'Error',
        oasis_status_cancelled: 'Cancelled',
        oasis_round: 'rounds',
        oasis_posts: 'posts',
        oasis_expert_creative: 'Creative Expert',
        oasis_expert_critical: 'Critical Expert',
        oasis_expert_data: 'Data Analyst',
        oasis_expert_synthesis: 'Synthesis Advisor',
        oasis_cancel: 'Stop Discussion',
        oasis_cancel_confirm: 'Force stop this discussion?',
        oasis_cancel_success: 'Discussion stopped',
        oasis_delete: 'Delete',
        oasis_delete_confirm: 'Permanently delete this discussion? This cannot be undone.',
        oasis_delete_success: 'Record deleted',
        oasis_action_fail: 'Action failed',

        // Page switch
        tab_chat: '💬 Chat',
        tab_group: '👥 Groups',
        tab_orchestrate: '🎨 Orchestrate',

        // Group chat
        group_title: '👥 Group Chats',
        group_new: '+ New',
        group_no_groups: 'No group chats',
        group_select_hint: 'Select or create a group chat',
        group_members_btn: '👤 Members',
        group_mute: '🔇 Stop',
        group_unmute: '🔊 Resume',
        group_members: 'Member Management',
        group_current_members: 'Current Members',
        group_add_agents: 'Add Agent Session',
        group_input_placeholder: 'Send a message...',
        group_create_title: 'Create Group Chat',
        group_name_placeholder: 'Group name',
        group_no_sessions: 'No available Agent Sessions',
        group_create_btn: 'Create',
        group_delete_confirm: 'Delete this group chat?',
        group_owner: 'Owner',
        group_agent: 'Agent',
        group_msg_count: 'messages',
        group_member_count: 'members',

        // Offline
        offline_banner: '⚠️ Network disconnected, please check connection',

        // Orchestration panel
        orch_expert_pool: '🧑‍💼 Expert Pool',
        orch_expert_pool_text: 'Expert Pool',
        orch_preset_experts: '📚 Preset Experts',
        orch_custom_experts: '🛠️ Custom Experts',
        orch_session_agents: '💬 Session Agents',
orch_openclaw_sessions: '🦞 OpenClaw',
        orch_manual_inject: 'Manual Inject',
        orch_shortcuts_title: 'Shortcuts: ',
        orch_shortcuts_body: 'Drag expert to canvas · Connect ports=workflow · Ctrl+G=group · Double-click to add',
        // Orchestration toolbar buttons
        orch_btn_arrange: '🔄 Arrange',
        orch_btn_save: '💾 Save',
        orch_btn_load: '📂 Load',
        orch_btn_ai: '🤖 AI Orch',
        orch_btn_export: '📋 Export',
        orch_btn_status: '🔄 Status',
        orch_btn_clear: '🗑️ Clear',
        orch_tip_arrange: 'Auto arrange',
        orch_tip_save: 'Save layout',
        orch_tip_load: 'Load layout',
        orch_tip_ai: 'AI generate YAML',
        orch_tip_export: 'Copy YAML',
        orch_tip_status: 'Refresh session status',
        orch_tip_clear: 'Clear canvas',
        // Canvas hints
        orch_hint_drag: 'Drag experts to start orchestrating',
        // Nav controls
        orch_tip_up: 'Pan up',
        orch_tip_down: 'Pan down',
        orch_tip_left: 'Pan left',
        orch_tip_right: 'Pan right',
        orch_tip_reset: 'Reset view',
        orch_tip_zoomout: 'Zoom out',
        orch_tip_zoomin: 'Zoom in',
        // Right panel
        orch_settings: '⚙️ Settings',
        orch_repeat: 'Repeat plan each round',
        orch_rounds: 'Rounds:',
        orch_stateful: 'Stateful mode',
        orch_threshold: 'Cluster threshold:',
        orch_ai_gen: '🤖 AI Generate',
        orch_ai_hint: 'Click "🤖 AI Orch" to auto-generate YAML',
        orch_prompt_label: '📨 Prompt Sent',
        orch_prompt_copy: 'Copy',
        orch_prompt_hint: 'Shown after AI Orch',
        orch_agent_yaml_label: '🤖 Agent YAML',
        orch_agent_yaml_copy: 'Copy',
        orch_agent_yaml_hint: 'Waiting for Agent',
        orch_rule_yaml: '📄 Rule YAML',
        orch_rule_yaml_hint: 'Auto-generated after adding experts...',
        orch_status_bar: 'Nodes: {nodes} | Edges: {edges} | Groups: {groups}',
        orch_status_bar_init: 'Nodes: 0 | Edges: 0 | Groups: 0',
        orch_manual_inject: 'Manual Inject',
        orch_node_remove: 'Remove',
        orch_default_author: 'Moderator',
        orch_yaml_valid: '✅ Valid YAML — {steps} steps [{types}]',
        orch_yaml_saved_suffix: ' | 💾 Saved: {file}',
        orch_yaml_warn: '⚠️ YAML validation issue: {error}',
        orch_comm_fail: '# Communication failed: {msg}',
        // Context menu
        orch_ctx_duplicate: '📋 Duplicate (same instance)',
        orch_ctx_new_instance: '➕ New Instance',
        orch_ctx_group_parallel: '🔀 Group as Parallel',
        orch_ctx_group_all: '👥 Group as All Experts',
        orch_ctx_delete: '🗑️ Delete Selected',
        orch_ctx_refresh_yaml: '🔄 Refresh YAML',
        orch_ctx_clear: '🗑️ Clear Canvas',
        // Group labels
        orch_group_parallel: '🔀 Parallel',
        orch_group_all: '👥 All Experts',
        orch_group_dissolve: 'Dissolve',
        // Modals
        orch_modal_edit_manual: '📝 Edit Manual Injection',
        orch_modal_author_ph: 'Author',
        orch_modal_content_ph: 'Injection content...',
        orch_modal_cancel: 'Cancel',
        orch_modal_save: 'Save',
        orch_modal_select_session: '🎯 Select Target Agent Session',
        orch_modal_select_desc: 'Select an existing conversation session or create a new one. You can jump to it after generation.',
        orch_modal_loading: '⏳ Loading...',
        orch_modal_new_session: 'New Conversation',
        orch_modal_confirm_gen: 'Confirm & Generate',
        orch_modal_select_layout: '📂 Select Layout',
        orch_modal_delete: '🗑️ Delete',
        orch_modal_load: 'Load',
        // Toast messages
        orch_toast_arranged: 'Auto-arranged',
        orch_toast_saved: 'Saved: {name}',
        orch_toast_save_fail: 'Save failed',
        orch_toast_no_layouts: 'No saved layouts found',
        orch_toast_deleted: 'Deleted: {name}',
        orch_toast_del_fail: 'Delete failed',
        orch_toast_loaded: 'Loaded: {name}',
        orch_toast_load_fail: 'Load failed',
        orch_toast_yaml_copied: 'YAML copied!',
        orch_toast_gen_yaml: 'Generate YAML first',
        orch_toast_prompt_copied: 'Prompt copied',
        orch_toast_agent_yaml_copied: 'Agent YAML copied',
        orch_toast_select_2: 'Select at least 2 nodes',
        orch_toast_add_first: 'Add expert nodes first',
        orch_toast_agent_unavail: 'Agent unavailable',
        orch_toast_yaml_generated: 'YAML generated and saved! ✅',
        orch_toast_agent_valid: 'Agent generated valid YAML! ✅',
        orch_toast_session_updated: 'Session status updated',
        orch_toast_session_fail: 'Failed to get status',
        orch_toast_no_session: 'No session selected',
        orch_toast_jumped: 'Jumped to chat #{id}',
        orch_toast_custom_added: 'Custom expert added: {name}',
        orch_toast_fill_info: 'Please fill in all fields',
        orch_toast_net_error: 'Network error',
        orch_toast_expert_deleted: 'Deleted: {name}',
        orch_toast_expert_del_fail: 'Delete failed',
        // YAML file operations
        orch_btn_download: '⬇️ Download',
        orch_btn_upload: '⬆️ Upload',
        orch_tip_download: 'Download YAML file',
        orch_tip_upload: 'Upload YAML file',
        orch_toast_yaml_downloaded: 'YAML file downloaded',
        orch_toast_yaml_uploaded: 'YAML imported: {name}',
        orch_toast_yaml_upload_fail: 'YAML import failed',
        orch_toast_yaml_parse_fail: 'Invalid YAML file',
        orch_toast_drop_yaml: 'Drop YAML file here to import',
        orch_drop_hint: 'Release to import YAML file',
        orch_toast_not_yaml: 'Only .yaml / .yml files supported',
        // Confirm dialogs
        orch_confirm_del_expert: 'Delete custom expert "{name}"?',
        orch_confirm_del_layout: 'Delete layout "{name}"?',
        orch_prompt_layout_name: 'Layout name:',
        // Agent status
        orch_status_communicating: '🔄 Communicating with Agent (Session: #{id})...',
        orch_status_generating: '⏳ Generating...',
        orch_status_waiting: '⏳ Waiting for Agent response...',
        orch_status_auth_fail: 'Authentication failed',
        orch_status_agent_unavail: 'Agent unavailable',
        orch_status_conn_error: '❌ Connection error',
        orch_goto_chat: '💬 Jump to chat {session} to continue',
        orch_no_custom: 'No custom experts yet',
        orch_no_session: 'No sessions yet',
        orch_load_fail: '❌ Load failed',
        orch_load_session_fail: '❌ Failed to load session list',
        orch_msg_count: '{count} messages',
        orch_add_expert_title: '🛠️ Add Custom Expert',
        orch_add_expert_btn: 'Add custom expert',
        orch_label_name: 'Name',
        orch_label_tag: 'Tag (English)',
        orch_label_temp: 'Temperature',
        orch_label_persona: 'Persona (Role Description)',
        orch_ph_name: 'e.g. Financial Analyst',
        orch_ph_tag: 'e.g. finance',
        orch_ph_persona: 'Describe this expert\'s role, expertise and behavior style...',

        // Add Workflow
        wf_btn_title: 'Add Workflow',
        wf_popup_title: '📋 Select Workflow',
        wf_no_workflows: 'No saved workflows',
        wf_cancel: 'Cancel',
        wf_confirm: 'Add',
        wf_context_prefix: '[Workflow: {name}] ',

        // Others
        splash_subtitle: 'TeamBot AI Agent',
        secure_footer: 'Secured by Nginx Reverse Proxy & SSH Tunnel',
        refresh: 'Refresh',
        collapse: 'Collapse',

        // Settings
        settings: '⚙️',
        settings_title: '⚙️ System Settings',
        settings_save: 'Save',
        settings_saved: '✅ Settings saved',
        settings_save_fail: '❌ Save failed',
        settings_load_fail: '❌ Failed to load settings',
        settings_restart_hint: 'Some settings require a service restart to take effect',
        menu_settings: '⚙️ Settings',
        settings_group_llm: 'LLM Model',
        settings_group_tts: 'TTS Voice',
        settings_group_openclaw: 'OpenClaw Integration',
        settings_group_ports: 'Ports',
        settings_group_bots: 'Bot Integration',
        settings_group_other: 'Other',
    }
};

// 当前语言
let currentLang = localStorage.getItem('lang') || 'zh-CN';
// 确保语言值有效
if (!i18n[currentLang]) { currentLang = 'zh-CN'; localStorage.setItem('lang', 'zh-CN'); }

// 获取翻译文本
function t(key, params) {
    let text = (i18n[currentLang] && i18n[currentLang][key]) || i18n['zh-CN'][key] || key;
    if (params) {
        Object.keys(params).forEach(k => {
            text = text.replace(new RegExp('\{' + k + '\}', 'g'), params[k]);
        });
    }
    return text;
}

// 切换语言
function toggleLanguage() {
    currentLang = currentLang === 'zh-CN' ? 'en' : 'zh-CN';
    localStorage.setItem('lang', currentLang);
    document.documentElement.lang = currentLang;
    applyTranslations();
}

// 应用翻译到页面
function applyTranslations() {
    // 更新语言按钮显示
    const langBtn = document.getElementById('lang-toggle-btn');
    if (langBtn) {
        langBtn.textContent = currentLang === 'zh-CN' ? 'EN' : '中文';
    }

    // 更新 data-i18n 属性的元素
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (el.tagName === 'INPUT' && el.hasAttribute('placeholder')) {
            el.placeholder = t(key);
        } else if (el.tagName === 'TEXTAREA' && el.hasAttribute('placeholder')) {
            el.placeholder = t(key);
        } else {
            el.textContent = t(key);
        }
    });

    // 更新 data-i18n-placeholder 属性
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        el.placeholder = t(el.getAttribute('data-i18n-placeholder'));
    });

    // 更新 data-i18n-title 属性
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        el.title = t(el.getAttribute('data-i18n-title'));
    });

    // 更新 title
    document.title = 'Teamclaw | AI Agent';
}

marked.setOptions({
    highlight: function(code, lang) {
        const language = hljs.getLanguage(lang) ? lang : 'plaintext';
        return hljs.highlight(code, { language }).value;
    },
    langPrefix: 'hljs language-'
});

let currentUserId = null;
let currentSessionId = null;
let currentAbortController = null;
let cancelTargetSessionId = null;  // 终止按钮绑定的会话ID
let pendingImages = []; // [{base64: "data:image/...", name: "file.jpg"}, ...]
let pendingFiles = [];  // [{name: "data.csv", content: "...(text content)"}, ...]
let pendingAudios = []; // [{base64: "data:audio/...", name: "recording.wav", format: "wav"}, ...]
let isRecording = false;

// OpenAI API 配置
function getAuthToken() { return sessionStorage.getItem('authToken') || ''; }
const TEXT_EXTENSIONS = new Set(['.txt','.md','.csv','.json','.xml','.yaml','.yml','.log','.py','.js','.ts','.html','.css','.java','.c','.cpp','.h','.go','.rs','.sh','.bat','.ini','.toml','.cfg','.conf','.sql','.r','.rb']);
const AUDIO_EXTENSIONS = new Set(['.mp3','.wav','.ogg','.m4a','.webm','.flac','.aac']);
const VIDEO_EXTENSIONS = new Set(['.avi','.mp4','.mkv','.mov']);
const MAX_FILE_SIZE = 512 * 1024; // 512KB per text file
const MAX_PDF_SIZE = 10 * 1024 * 1024; // 10MB per PDF
const MAX_AUDIO_SIZE = 25 * 1024 * 1024; // 25MB per audio
const MAX_VIDEO_SIZE = 50 * 1024 * 1024; // 50MB per video
const MAX_IMAGE_SIZE = 10 * 1024 * 1024; // 压缩目标：10MB
const MAX_IMAGE_DIMENSION = 2048; // 最大边长

function compressImage(file) {
    return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => {
            let { width, height } = img;
            if (width > MAX_IMAGE_DIMENSION || height > MAX_IMAGE_DIMENSION) {
                const scale = MAX_IMAGE_DIMENSION / Math.max(width, height);
                width = Math.round(width * scale);
                height = Math.round(height * scale);
            }
            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);
            let quality = 0.85;
            let result = canvas.toDataURL('image/jpeg', quality);
            while (result.length > MAX_IMAGE_SIZE * 1.37 && quality > 0.3) {
                quality -= 0.1;
                result = canvas.toDataURL('image/jpeg', quality);
            }
            resolve(result);
        };
        img.src = URL.createObjectURL(file);
    });
}

// ===== File Upload Logic (images + text files + PDF + audio) =====
function handleFileSelect(event) {
    const files = event.target.files;
    if (!files.length) return;
    for (const file of files) {
        if (file.type.startsWith('image/')) {
            if (pendingImages.length >= 5) { alert(t('max_images')); break; }
            if (file.size <= MAX_IMAGE_SIZE) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    pendingImages.push({ base64: e.target.result, name: file.name });
                    renderImagePreviews();
                };
                reader.readAsDataURL(file);
            } else {
                compressImage(file).then((compressed) => {
                    pendingImages.push({ base64: compressed, name: file.name });
                    renderImagePreviews();
                });
            }
        } else if (file.type.startsWith('audio/') || AUDIO_EXTENSIONS.has('.' + file.name.split('.').pop().toLowerCase())) {
            if (file.size > MAX_AUDIO_SIZE) { alert(`${file.name}: ${t('audio_too_large')} (${(file.size/1024/1024).toFixed(1)}MB)`); continue; }
            if (pendingAudios.length >= 2) { alert(t('max_audios')); break; }
            const ext = file.name.split('.').pop().toLowerCase();
            const fmt = ({'mp3':'mp3','wav':'wav','ogg':'ogg','m4a':'m4a','webm':'webm','flac':'flac','aac':'aac'})[ext] || 'mp3';
            const reader = new FileReader();
            reader.onload = (e) => {
                pendingAudios.push({ base64: e.target.result, name: file.name, format: fmt });
                renderAudioPreviews();
            };
            reader.readAsDataURL(file);
        } else if (file.type.startsWith('video/') || VIDEO_EXTENSIONS.has('.' + file.name.split('.').pop().toLowerCase())) {
            // 视频文件：以 dataURL 形式存入 pendingFiles，type='media'
            if (file.size > MAX_VIDEO_SIZE) { alert(`${file.name}: ${t('video_too_large')} (${(file.size/1024/1024).toFixed(1)}MB)`); continue; }
            if (pendingFiles.length >= 3) { alert(t('max_files')); break; }
            const reader = new FileReader();
            reader.onload = (e) => {
                pendingFiles.push({ name: file.name, content: e.target.result, type: 'media' });
                renderFilePreviews();
            };
            reader.readAsDataURL(file);
        } else if (file.name.toLowerCase().endsWith('.pdf') || file.type === 'application/pdf') {
            if (file.size > MAX_PDF_SIZE) { alert(`${file.name}: ${t('pdf_too_large')} (${(file.size/1024/1024).toFixed(1)}MB)`); continue; }
            if (pendingFiles.length >= 3) { alert(t('max_files')); break; }
            const reader = new FileReader();
            reader.onload = (e) => {
                pendingFiles.push({ name: file.name, content: e.target.result, type: 'pdf' });
                renderFilePreviews();
            };
            reader.readAsDataURL(file);
        } else {
            const ext = '.' + file.name.split('.').pop().toLowerCase();
            if (!TEXT_EXTENSIONS.has(ext)) { alert(`${t('unsupported_type')}: ${ext}\n${t('supported_types')}`); continue; }
            if (file.size > MAX_FILE_SIZE) { alert(`${file.name}: ${t('file_too_large')} (${(file.size/1024).toFixed(0)}KB)`); continue; }
            if (pendingFiles.length >= 3) { alert(t('max_files')); break; }
            const reader = new FileReader();
            reader.onload = (e) => {
                pendingFiles.push({ name: file.name, content: e.target.result, type: 'text' });
                renderFilePreviews();
            };
            reader.readAsText(file);
        }
    }
    event.target.value = '';
}

// ===== Audio Recording =====
async function toggleRecording() {
    if (isRecording) {
        stopRecording();
    } else {
        await startRecording();
    }
}

// --- WAV 编码辅助函数 ---
function encodeWAV(samples, sampleRate) {
    const buffer = new ArrayBuffer(44 + samples.length * 2);
    const view = new DataView(buffer);
    function writeString(offset, string) {
        for (let i = 0; i < string.length; i++) view.setUint8(offset + i, string.charCodeAt(i));
    }
    writeString(0, 'RIFF');
    view.setUint32(4, 36 + samples.length * 2, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true); // PCM
    view.setUint16(22, 1, true); // mono
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true);
    view.setUint16(32, 2, true);
    view.setUint16(34, 16, true);
    writeString(36, 'data');
    view.setUint32(40, samples.length * 2, true);
    for (let i = 0; i < samples.length; i++) {
        const s = Math.max(-1, Math.min(1, samples[i]));
        view.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }
    return new Blob([buffer], { type: 'audio/wav' });
}

let audioContext = null;
let audioSourceNode = null;
let audioProcessorNode = null;
let recordedSamples = [];

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
        audioSourceNode = audioContext.createMediaStreamSource(stream);
        audioProcessorNode = audioContext.createScriptProcessor(4096, 1, 1);
        recordedSamples = [];
        audioProcessorNode.onaudioprocess = (e) => {
            const data = e.inputBuffer.getChannelData(0);
            recordedSamples.push(new Float32Array(data));
        };
        audioSourceNode.connect(audioProcessorNode);
        audioProcessorNode.connect(audioContext.destination);
        isRecording = true;
        document.getElementById('record-btn').classList.add('recording');
        document.getElementById('record-btn').title = t('recording_stop');
    } catch (err) {
        alert(t('mic_permission_denied') + '\n' + err.message);
    }
}

function stopRecording() {
    if (!audioContext) return;
    const stream = audioSourceNode.mediaStream;
    audioProcessorNode.disconnect();
    audioSourceNode.disconnect();
    stream.getTracks().forEach(t => t.stop());
    // 合并所有采样
    let totalLen = 0;
    for (const chunk of recordedSamples) totalLen += chunk.length;
    const merged = new Float32Array(totalLen);
    let offset = 0;
    for (const chunk of recordedSamples) { merged.set(chunk, offset); offset += chunk.length; }
    const sampleRate = audioContext.sampleRate;
    audioContext.close();
    audioContext = null;
    audioSourceNode = null;
    audioProcessorNode = null;
    recordedSamples = [];
    isRecording = false;
    document.getElementById('record-btn').classList.remove('recording');
    document.getElementById('record-btn').title = t('recording_title');
    const blob = encodeWAV(merged, sampleRate);
    if (blob.size > MAX_AUDIO_SIZE) { alert(t('recording_too_long')); return; }
    if (pendingAudios.length >= 2) { alert(t('max_audios')); return; }
    const reader = new FileReader();
    reader.onload = (e) => {
        const ts = new Date().toLocaleTimeString(currentLang === 'zh-CN' ? 'zh-CN' : 'en-US', {hour:'2-digit',minute:'2-digit',second:'2-digit'});
        const recName = currentLang === 'zh-CN' ? `录音_${ts}.wav` : `recording_${ts}.wav`;
        pendingAudios.push({ base64: e.target.result, name: recName, format: 'wav' });
        renderAudioPreviews();
    };
    reader.readAsDataURL(blob);
}

function removeAudio(index) {
    pendingAudios.splice(index, 1);
    renderAudioPreviews();
}

function renderAudioPreviews() {
    const area = document.getElementById('audio-preview-area');
    if (pendingAudios.length === 0) {
        area.style.display = 'none';
        area.innerHTML = '';
        return;
    }
    area.style.display = 'flex';
    area.innerHTML = pendingAudios.map((a, i) => `
        <div class="audio-preview-item">
            <span class="file-icon">🎤</span>
            <span class="file-name" title="${escapeHtml(a.name)}">${escapeHtml(a.name)}</span>
            <button class="remove-btn" onclick="removeAudio(${i})">&times;</button>
        </div>
    `).join('');
}

function handlePasteImage(event) {
    const items = event.clipboardData?.items;
    if (!items) return;
    for (const item of items) {
        if (!item.type.startsWith('image/')) continue;
        event.preventDefault();
        if (pendingImages.length >= 5) { alert(t('max_images')); break; }
        const file = item.getAsFile();
        const reader = new FileReader();
        reader.onload = (e) => {
            pendingImages.push({ base64: e.target.result, name: 'pasted_image.png' });
            renderImagePreviews();
        };
        reader.readAsDataURL(file);
    }
}

function removeImage(index) {
    pendingImages.splice(index, 1);
    renderImagePreviews();
}

function removeFile(index) {
    pendingFiles.splice(index, 1);
    renderFilePreviews();
}

function renderImagePreviews() {
    const area = document.getElementById('image-preview-area');
    if (pendingImages.length === 0) {
        area.style.display = 'none';
        area.innerHTML = '';
        return;
    }
    area.style.display = 'flex';
    area.innerHTML = pendingImages.map((img, i) => `
        <div class="image-preview-item">
            <img src="${img.base64}" alt="${img.name}">
            <button class="remove-btn" onclick="removeImage(${i})">&times;</button>
        </div>
    `).join('');
}

function renderFilePreviews() {
    const area = document.getElementById('file-preview-area');
    if (pendingFiles.length === 0) {
        area.style.display = 'none';
        area.innerHTML = '';
        return;
    }
    area.style.display = 'flex';
    area.innerHTML = pendingFiles.map((f, i) => `
        <div class="file-preview-item">
            <span class="file-icon">${f.type === 'media' ? '🎬' : '📄'}</span>
            <span class="file-name" title="${escapeHtml(f.name)}">${escapeHtml(f.name)}</span>
            <button class="remove-btn" onclick="removeFile(${i})">&times;</button>
        </div>
    `).join('');
}

// ===== Session (conversation) ID management =====
function generateSessionId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 4);
}

function initSession() {
    let saved = sessionStorage.getItem('sessionId');
    if (!saved) {
        saved = generateSessionId();
        sessionStorage.setItem('sessionId', saved);
    }
    currentSessionId = saved;
    updateSessionDisplay();
}

function updateSessionDisplay() {
    const el = document.getElementById('session-display');
    if (el && currentSessionId) {
        el.textContent = '#' + currentSessionId.slice(-6);
        el.title = t('session_id') + ': ' + currentSessionId;
    }
}

function handleNewSession() {
    if (!confirm(t('new_session_confirm'))) return;
    currentSessionId = generateSessionId();
    sessionStorage.setItem('sessionId', currentSessionId);
    updateSessionDisplay();
    // Clear chat box for new conversation
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = `
        <div class="flex justify-start">
            <div class="message-agent bg-white border p-4 max-w-[85%] shadow-sm text-gray-700">
                ${t('new_session_message')}
            </div>
        </div>`;
}

// ===== 历史会话侧边栏 =====
let sessionSidebarOpen = false;
let _historyPollingTimer = null;

function startHistoryPolling() {
    stopHistoryPolling();
    _historyPollingTimer = setInterval(() => {
        if (sessionSidebarOpen) {
            refreshHistoryList();
        } else {
            // sidebar 未打开也刷新状态（发光效果），以便打开时立即可见
            refreshSessionStatus();
        }
    }, 1000);
}
function stopHistoryPolling() {
    if (_historyPollingTimer) { clearInterval(_historyPollingTimer); _historyPollingTimer = null; }
}

function toggleSessionSidebar() {
    if (sessionSidebarOpen) { closeSessionSidebar(); } else { openSessionSidebar(); }
}

async function openSessionSidebar() {
    const sidebar = document.getElementById('session-sidebar');
    sidebar.style.display = 'flex';
    sessionSidebarOpen = true;
    // 移动端加遮罩
    if (window.innerWidth <= 768) {
        let overlay = document.getElementById('session-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'session-overlay';
            overlay.className = 'session-overlay';
            overlay.onclick = closeSessionSidebar;
            sidebar.parentElement.appendChild(overlay);
        }
        overlay.style.display = 'block';
    }
    // 已有列表内容则增量刷新，否则全量加载
    const listEl = document.getElementById('session-list');
    if (listEl.querySelector('.session-item')) {
        refreshHistoryList();
    } else {
        await loadSessionList();
    }
}

function closeSessionSidebar() {
    document.getElementById('session-sidebar').style.display = 'none';
    const overlay = document.getElementById('session-overlay');
    if (overlay) overlay.style.display = 'none';
    sessionSidebarOpen = false;
}

// Session filter mode: 'oasis' = only show oasis sessions, 'other' = only show non-oasis sessions
let sessionFilterMode = 'oasis';

function isOasisSession(sessionId) {
    return sessionId && sessionId.includes('#oasis#');
}

function shouldShowSession(sessionId) {
    const isOasis = isOasisSession(sessionId);
    return sessionFilterMode === 'oasis' ? isOasis : !isOasis;
}

function toggleOasisSessionsVisible() {
    sessionFilterMode = sessionFilterMode === 'oasis' ? 'other' : 'oasis';
    const btn = document.getElementById('toggle-oasis-sessions-btn');
    if (btn) {
        btn.textContent = sessionFilterMode === 'oasis' ? '🏛️ OASIS' : '💬 会话';
    }
    // Apply filter to all session items
    document.querySelectorAll('.session-item[data-session-id]').forEach(el => {
        el.style.display = shouldShowSession(el.dataset.sessionId) ? '' : 'none';
    });
}

async function loadSessionList() {
    const listEl = document.getElementById('session-list');
    if (!listEl.querySelector('.session-item')) {
        listEl.innerHTML = `<div class="text-xs text-gray-400 text-center py-4">${t('loading')}</div>`;
    }
    try {
        const resp = await fetch('/proxy_sessions');
        const data = await resp.json();
        if (!data.sessions || data.sessions.length === 0) {
            listEl.innerHTML = `<div class="text-xs text-gray-400 text-center py-4">${t('history_empty')}</div>`;
            return;
        }
        listEl.innerHTML = '';
        data.sessions.sort((a, b) => b.session_id.localeCompare(a.session_id));
        for (const s of data.sessions) {
            const isActive = s.session_id === currentSessionId;
            const div = document.createElement('div');
            div.className = 'session-item' + (isActive ? ' active' : '');
            div.dataset.sessionId = s.session_id;
            div.innerHTML = `
                <div class="session-title">${escapeHtml(s.title)}</div>
                <div class="session-meta">#${s.session_id.slice(-6)} · ${s.message_count}${t('messages_count')}</div>
                <button class="session-delete" onclick="event.stopPropagation(); deleteSession('${s.session_id}')">${t('delete_session')}</button>
            `;
            div.onclick = () => switchToSession(s.session_id);
            if (!shouldShowSession(s.session_id)) {
                div.style.display = 'none';
            }
            listEl.appendChild(div);
        }
        refreshSessionStatus();
    } catch (e) {
        listEl.innerHTML = `<div class="text-xs text-red-400 text-center py-4">${t('history_error')}</div>`;
    }
}

// 增量刷新：不重建DOM，只更新标题/计数 + 状态发光
async function refreshHistoryList() {
    try {
        const [sessResp, statusResp] = await Promise.all([
            fetch('/proxy_sessions'),
            fetch('/proxy_sessions_status')
        ]);
        const sessData = await sessResp.json();
        const statusData = statusResp.ok ? await statusResp.json() : {};
        const sessions = sessData.sessions || [];
        const listEl = document.getElementById('session-list');
        if (sessions.length === 0) {
            listEl.innerHTML = `<div class="text-xs text-gray-400 text-center py-4">${t('history_empty')}</div>`;
            return;
        }
        // 构建 session map
        const sessMap = {};
        for (const s of sessions) sessMap[s.session_id] = s;
        const statusMap = {};
        if (statusData.sessions) {
            for (const s of statusData.sessions) statusMap[s.session_id] = s;
        }
        // 现有 DOM 的 session id 集合
        const existingEls = listEl.querySelectorAll('.session-item[data-session-id]');
        const existingIds = new Set();
        existingEls.forEach(el => existingIds.add(el.dataset.sessionId));
        const newIds = new Set(sessions.map(s => s.session_id));
        // 删除不存在的
        existingEls.forEach(el => {
            if (!newIds.has(el.dataset.sessionId)) el.remove();
        });
        // 更新现有的 + 添加新的
        sessions.sort((a, b) => b.session_id.localeCompare(a.session_id));
        let prevEl = null;
        for (const s of sessions) {
            let div = listEl.querySelector(`.session-item[data-session-id="${s.session_id}"]`);
            if (div) {
                // 更新标题和计数
                const titleEl = div.querySelector('.session-title');
                const newTitle = escapeHtml(s.title);
                if (titleEl && titleEl.innerHTML !== newTitle) titleEl.innerHTML = newTitle;
                const metaEl = div.querySelector('.session-meta');
                if (metaEl) {
                    const badge = metaEl.querySelector('.session-busy-badge');
                    const newMeta = `#${s.session_id.slice(-6)} · ${s.message_count}${t('messages_count')}`;
                    // 只更新文本部分，保留badge
                    const textNode = metaEl.firstChild;
                    if (textNode && textNode.nodeType === 3) {
                        if (textNode.textContent.trim() !== newMeta.trim()) textNode.textContent = newMeta;
                    } else {
                        // 重建meta但保留badge
                        const savedBadge = badge;
                        metaEl.textContent = newMeta;
                        if (savedBadge) metaEl.appendChild(savedBadge);
                    }
                }
                // active 状态
                div.classList.toggle('active', s.session_id === currentSessionId);
                // session 可见性
                div.style.display = shouldShowSession(s.session_id) ? '' : 'none';
            } else {
                // 新增的 session
                div = document.createElement('div');
                div.className = 'session-item' + (s.session_id === currentSessionId ? ' active' : '');
                div.dataset.sessionId = s.session_id;
                div.innerHTML = `
                    <div class="session-title">${escapeHtml(s.title)}</div>
                    <div class="session-meta">#${s.session_id.slice(-6)} · ${s.message_count}${t('messages_count')}</div>
                    <button class="session-delete" onclick="event.stopPropagation(); deleteSession('${s.session_id}')">${t('delete_session')}</button>
                `;
                div.onclick = () => switchToSession(s.session_id);
                if (!shouldShowSession(s.session_id)) {
                    div.style.display = 'none';
                }
                if (prevEl && prevEl.nextSibling) {
                    listEl.insertBefore(div, prevEl.nextSibling);
                } else if (!prevEl) {
                    listEl.prepend(div);
                } else {
                    listEl.appendChild(div);
                }
            }
            // 更新发光状态（不移除再添加class，避免动画重启）
            const info = statusMap[s.session_id];
            const wantUser = info && info.busy && info.source !== 'system';
            const wantSystem = info && info.busy && info.source === 'system';
            const hasUser = div.classList.contains('busy-user');
            const hasSystem = div.classList.contains('busy-system');
            if (wantUser && !hasUser) { div.classList.remove('busy-system'); div.classList.add('busy-user'); }
            else if (wantSystem && !hasSystem) { div.classList.remove('busy-user'); div.classList.add('busy-system'); }
            else if (!wantUser && !wantSystem) { div.classList.remove('busy-user', 'busy-system'); }
            // badge
            const existingBadge = div.querySelector('.session-busy-badge');
            if (info && info.busy) {
                const badgeCls = info.source === 'system' ? 'system' : 'user';
                const badgeText = info.source === 'system' ? '⚙️' : '💬';
                if (existingBadge) {
                    if (!existingBadge.classList.contains(badgeCls)) {
                        existingBadge.className = 'session-busy-badge ' + badgeCls;
                        existingBadge.textContent = badgeText;
                    }
                } else {
                    const badge = document.createElement('span');
                    badge.className = 'session-busy-badge ' + badgeCls;
                    badge.textContent = badgeText;
                    div.querySelector('.session-meta')?.appendChild(badge);
                }
            } else if (existingBadge) {
                existingBadge.remove();
            }
            prevEl = div;
        }
    } catch (e) { /* silent */ }
}

async function refreshSessionStatus() {
    try {
        const resp = await fetch('/proxy_sessions_status');
        if (!resp.ok) return;
        const data = await resp.json();
        if (!data.sessions) return;
        const statusMap = {};
        for (const s of data.sessions) statusMap[s.session_id] = s;
        document.querySelectorAll('.session-item[data-session-id]').forEach(el => {
            const sid = el.dataset.sessionId;
            const info = statusMap[sid];
            el.classList.remove('busy-user', 'busy-system');
            el.querySelector('.session-busy-badge')?.remove();
            if (info && info.busy) {
                const cls = info.source === 'system' ? 'busy-system' : 'busy-user';
                el.classList.add(cls);
                const badge = document.createElement('span');
                badge.className = 'session-busy-badge ' + (info.source === 'system' ? 'system' : 'user');
                badge.textContent = info.source === 'system' ? '⚙️' : '💬';
                el.querySelector('.session-meta')?.appendChild(badge);
            }
        });
    } catch (e) { /* silent */ }
}

async function deleteSession(sessionId) {
    if (!confirm(t('delete_session_confirm'))) return;
    try {
        const resp = await fetch('/proxy_delete_session', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ session_id: sessionId })
        });
        const data = await resp.json();
        if (resp.ok && data.status === 'success') {
            // 如果删除的是当前会话，自动开一个新的
            if (sessionId === currentSessionId) {
                currentSessionId = generateSessionId();
                sessionStorage.setItem('sessionId', currentSessionId);
                updateSessionDisplay();
                document.getElementById('chat-box').innerHTML = `
                    <div class="flex justify-start">
                        <div class="message-agent bg-white border p-4 max-w-[85%] shadow-sm text-gray-700">
                            ${t('new_session_message')}
                        </div>
                    </div>`;
            }
            await loadSessionList();
        } else {
            alert(t('delete_fail') + ': ' + (data.detail || data.error || ''));
        }
    } catch (e) {
        alert(t('delete_fail') + ': ' + e.message);
    }
}

async function deleteAllSessions() {
    // Collect visible session ids based on current filter mode
    const visibleIds = [];
    document.querySelectorAll('.session-item[data-session-id]').forEach(el => {
        if (el.style.display !== 'none') {
            visibleIds.push(el.dataset.sessionId);
        }
    });
    if (visibleIds.length === 0) return;
    const modeLabel = sessionFilterMode === 'oasis' ? 'OASIS' : '普通';
    if (!confirm(`确认删除当前显示的 ${visibleIds.length} 个${modeLabel}会话？`)) return;
    try {
        let failCount = 0;
        await Promise.all(visibleIds.map(async sid => {
            try {
                const resp = await fetch('/proxy_delete_session', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ session_id: sid })
                });
                const data = await resp.json();
                if (!resp.ok || data.status !== 'success') failCount++;
            } catch { failCount++; }
        }));
        // If current session was among deleted, reset it
        if (visibleIds.includes(currentSessionId)) {
            currentSessionId = generateSessionId();
            sessionStorage.setItem('sessionId', currentSessionId);
            updateSessionDisplay();
            document.getElementById('chat-box').innerHTML = `
                <div class="flex justify-start">
                    <div class="message-agent bg-white border p-4 max-w-[85%] shadow-sm text-gray-700">
                        ${t('new_session_message')}
                    </div>
                </div>`;
        }
        await loadSessionList();
        if (failCount > 0) alert(`${failCount} 个会话删除失败`);
    } catch (e) {
        alert(t('delete_fail') + ': ' + e.message);
    }
}

async function switchToSession(sessionId, force = false) {
    if (!force && sessionId === currentSessionId) { closeSessionSidebar(); return; }
    hideNewMsgBanner();
    // 切换前先重置按钮到 idle 状态（避免旧 session 的 streaming/busy 状态残留）
    setStreamingUI(false);
    setSystemBusyUI(false);
    currentSessionId = sessionId;
    cancelTargetSessionId = null;  // 重置终止目标
    sessionStorage.setItem('sessionId', sessionId);
    updateSessionDisplay();
    closeSessionSidebar();

    // 加载该会话的历史消息
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = `<div class="text-xs text-gray-400 text-center py-4">${t('history_loading_msg')}</div>`;

    try {
        const resp = await fetch('/proxy_session_history', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ session_id: sessionId })
        });
        const data = await resp.json();
        chatBox.innerHTML = '';

        if (!data.messages || data.messages.length === 0) {
            chatBox.innerHTML = `
                <div class="flex justify-start">
                    <div class="message-agent bg-white border p-4 max-w-[85%] shadow-sm text-gray-700">
                        ${t('history_no_msg')}
                    </div>
                </div>`;
            return;
        }

        for (const msg of data.messages) {
            if (msg.role === 'user') {
                // 支持多模态历史消息（content 可能是 string 或 array）
                let textContent = '';
                let imagesHtml = '';
                if (typeof msg.content === 'string') {
                    textContent = msg.content;
                } else if (Array.isArray(msg.content)) {
                    for (const part of msg.content) {
                        if (part.type === 'text') textContent = part.text || '';
                        else if (part.type === 'image_url') {
                            imagesHtml += `<img src="${part.image_url.url}" class="chat-inline-image">`;
                        }
                    }
                }
                chatBox.innerHTML += `
                    <div class="flex justify-end">
                        <div class="message-user bg-blue-600 text-white p-4 max-w-[85%] shadow-sm">
                            ${imagesHtml}${imagesHtml ? '<div style="margin-top:6px">' : ''}${escapeHtml(textContent || '('+t('image_placeholder')+')')}${imagesHtml ? '</div>' : ''}
                        </div>
                    </div>`;
            } else if (msg.role === 'tool') {
                chatBox.innerHTML += `
                    <div class="flex justify-start">
                        <div class="bg-gray-100 border border-dashed border-gray-300 p-3 max-w-[85%] shadow-sm text-xs text-gray-500 rounded-lg">
                            <div class="font-semibold text-gray-600 mb-1">🔧 ${t('tool_return')}: ${escapeHtml(msg.tool_name || '')}</div>
                            <pre class="whitespace-pre-wrap break-words">${escapeHtml(msg.content.length > 500 ? msg.content.slice(0, 500) + '...' : msg.content)}</pre>
                        </div>
                    </div>`;
            } else {
                let toolCallsHtml = '';
                if (msg.tool_calls && msg.tool_calls.length > 0) {
                    const callsList = msg.tool_calls.map(tc =>
                        `<span class="inline-block bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded mr-1 mb-1">🔧 ${escapeHtml(tc.name)}</span>`
                    ).join('');
                    toolCallsHtml = `<div class="mb-2">${callsList}</div>`;
                }
                chatBox.innerHTML += `
                    <div class="flex justify-start">
                        <div class="message-agent bg-white border p-4 max-w-[85%] shadow-sm text-gray-700 markdown-body" data-tts-ready="1">
                            ${toolCallsHtml}${msg.content ? marked.parse(msg.content) : '<span class="text-gray-400 text-xs">('+t('tool_calling')+')</span>'}
                        </div>
                    </div>`;
            }
        }
        // 为历史 AI 消息添加朗读按钮
        chatBox.querySelectorAll('[data-tts-ready="1"]').forEach(div => {
            div.removeAttribute('data-tts-ready');
            const ttsBtn = createTtsButton(() => div.innerText || div.textContent || '');
            div.appendChild(ttsBtn);
        });
        // 高亮代码块
        chatBox.querySelectorAll('pre code').forEach((block) => hljs.highlightElement(block));
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (e) {
        chatBox.innerHTML = `
            <div class="text-xs text-red-400 text-center py-4">${t('history_error')}: ${e.message}</div>`;
    }

    // 切换 session 后立即检查一次 busy 状态
    try {
        const sr = await fetch('/proxy_session_status', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ session_id: sessionId })
        });
        const sd = await sr.json();
        if (sd.busy) {
            setSystemBusyUI(true);
        } else {
            setSystemBusyUI(false);
        }
    } catch(e) {}
}

// ===== 登录逻辑 =====
async function handleLogin() {
    const nameInput = document.getElementById('username-input');
    const pwInput = document.getElementById('password-input');
    const errorDiv = document.getElementById('login-error');
    const loginBtn = document.getElementById('login-btn');
    const name = nameInput.value.trim();
    const password = pwInput.value;

    errorDiv.classList.add('hidden');

    if (!name) { nameInput.focus(); return; }
    if (!password) { pwInput.focus(); return; }

    if (!/^[a-zA-Z0-9_\-\u4e00-\u9fa5]+$/.test(name)) {
        errorDiv.textContent = t('login_error_invalid');
        errorDiv.classList.remove('hidden');
        return;
    }

    loginBtn.disabled = true;
    loginBtn.textContent = t('login_verifying');

    try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 15000);
        const resp = await fetch("/proxy_login", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: name, password: password }),
            signal: controller.signal
        });
        clearTimeout(timeout);
        let data;
        try { data = await resp.json(); } catch (_) { data = { error: 'Invalid server response' }; }
        if (!resp.ok) {
            errorDiv.textContent = data.detail || data.error || t('login_error_failed');
            errorDiv.classList.remove('hidden');
            return;
        }

        currentUserId = name;
        sessionStorage.setItem('userId', name);
        // 存储 OpenAI 格式的 Bearer token: user_id:password
        const authToken = name + ':' + password;
        sessionStorage.setItem('authToken', authToken);
        initSession();

        document.getElementById('uid-display').textContent = 'UID: ' + name;
        document.getElementById('login-screen').style.display = 'none';
        document.getElementById('chat-screen').style.display = 'flex';
        document.getElementById('user-input').focus();
        loadTools();
        refreshOasisTopics(); // Load OASIS topics after login
        startHistoryPolling();
    } catch (e) {
        if (e.name === 'AbortError') {
            errorDiv.textContent = '连接超时，请确认后端服务已启动后重试';
        } else {
            errorDiv.textContent = t('login_error_network') + ': ' + e.message;
        }
        errorDiv.classList.remove('hidden');
    } finally {
        loginBtn.disabled = false;
        loginBtn.textContent = t('login_btn');
    }
}

// ===================== Settings Modal =====================
const SETTINGS_GROUPS = {
    llm: { label: 'settings_group_llm', keys: ['LLM_API_KEY', 'LLM_BASE_URL', 'LLM_MODEL', 'LLM_PROVIDER', 'LLM_VISION_SUPPORT'] },
    tts: { label: 'settings_group_tts', keys: ['TTS_MODEL', 'TTS_VOICE'] },
    openclaw: { label: 'settings_group_openclaw', keys: ['OPENCLAW_API_URL', 'OPENCLAW_API_KEY', 'OPENCLAW_SESSIONS_FILE'] },
    ports: { label: 'settings_group_ports', keys: ['PORT_AGENT', 'PORT_SCHEDULER', 'PORT_OASIS', 'PORT_FRONTEND', 'PORT_BARK'] },
    bots: { label: 'settings_group_bots', keys: ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_ALLOWED_USERS', 'QQ_APP_ID', 'QQ_BOT_SECRET', 'QQ_BOT_USERNAME'] },
    other: { label: 'settings_group_other', keys: ['PUBLIC_DOMAIN', 'OPENAI_STANDARD_MODE', 'ALLOWED_COMMANDS', 'EXEC_TIMEOUT', 'MAX_OUTPUT_LENGTH'] },
};

let _settingsCache = {};

async function openSettings() {
    const modal = document.getElementById('settings-modal');
    const body = document.getElementById('settings-body');
    modal.style.display = 'flex';
    body.innerHTML = `<div class="settings-loading">${t('loading')}</div>`;
    try {
        const r = await fetch('/proxy_settings');
        const data = await r.json();
        if (data.error || !data.settings) throw new Error(data.error || 'unknown');
        _settingsCache = data.settings;
        renderSettings(data.settings);
    } catch (e) {
        body.innerHTML = `<div class="settings-error">${t('settings_load_fail')}: ${e.message}</div>`;
    }
}

function renderSettings(settings) {
    const body = document.getElementById('settings-body');
    let html = `<div class="settings-hint">${t('settings_restart_hint')}</div>`;
    for (const [gid, group] of Object.entries(SETTINGS_GROUPS)) {
        const hasValues = group.keys.some(k => settings[k] !== undefined && settings[k] !== '');
        html += `<div class="settings-group">`;
        html += `<div class="settings-group-title" onclick="this.parentElement.classList.toggle('collapsed')">${t(group.label)} <span class="settings-chevron">▼</span></div>`;
        html += `<div class="settings-group-body">`;
        for (const key of group.keys) {
            const val = settings[key] || '';
            const isPassword = key.includes('KEY') || key.includes('TOKEN') || key.includes('SECRET');
            html += `<div class="settings-field">`;
            html += `<label class="settings-label" title="${key}">${key}</label>`;
            html += `<input class="settings-input" data-key="${key}" type="${isPassword ? 'password' : 'text'}" value="${escapeHtml(val)}" placeholder="${key}" autocomplete="off" />`;
            html += `</div>`;
        }
        html += `</div></div>`;
    }
    body.innerHTML = html;
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML.replace(/"/g, '&quot;');
}

function closeSettings() {
    document.getElementById('settings-modal').style.display = 'none';
}

async function saveSettings() {
    const inputs = document.querySelectorAll('#settings-body .settings-input');
    const updates = {};
    inputs.forEach(inp => {
        const key = inp.dataset.key;
        const val = inp.value.trim();
        const orig = _settingsCache[key] || '';
        if (val !== orig) {
            updates[key] = val;
        }
    });
    if (Object.keys(updates).length === 0) {
        closeSettings();
        return;
    }
    try {
        const r = await fetch('/proxy_settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ settings: updates }),
        });
        const data = await r.json();
        if (data.status === 'success') {
            appendMessage(t('settings_saved') + (data.updated?.length ? ': ' + data.updated.join(', ') : ''), false);
            closeSettings();
        } else {
            alert(t('settings_save_fail'));
        }
    } catch (e) {
        alert(t('settings_save_fail') + ': ' + e.message);
    }
}

function handleLogout() {
    currentUserId = null;
    currentSessionId = null;
    stopHistoryPolling();
    sessionStorage.removeItem('userId');
    sessionStorage.removeItem('authToken');
    sessionStorage.removeItem('sessionId');
    fetch("/proxy_logout", { method: 'POST' });
    document.getElementById('chat-screen').style.display = 'none';
    document.getElementById('login-screen').style.display = 'flex';
    document.getElementById('username-input').value = '';
    document.getElementById('password-input').value = '';
    document.getElementById('login-error').classList.add('hidden');
    document.getElementById('username-input').focus();
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = `
        <div class="flex justify-start">
            <div class="message-agent bg-white border p-4 max-w-[85%] shadow-sm text-gray-700">
                ${t('welcome_message')}
            </div>
        </div>`;
    // Stop OASIS polling
    stopOasisPolling();
}

// ===== Tool Panel 逻辑 =====
let toolPanelOpen = false;
let allTools = [];
let enabledToolSet = new Set();

function toggleToolPanel() {
    const panel = document.getElementById('tool-panel');
    const icon = document.getElementById('tool-toggle-icon');
    toolPanelOpen = !toolPanelOpen;
    if (toolPanelOpen) {
        panel.classList.remove('collapsed');
        panel.classList.add('expanded');
        icon.classList.add('open');
    } else {
        panel.classList.remove('expanded');
        panel.classList.add('collapsed');
        icon.classList.remove('open');
    }
}

function updateToolCount() {
    const toolCount = document.getElementById('tool-count');
    toolCount.textContent = '(' + enabledToolSet.size + '/' + allTools.length + ')';
}

function toggleTool(name, tagEl) {
    if (enabledToolSet.has(name)) {
        enabledToolSet.delete(name);
        tagEl.classList.remove('enabled');
        tagEl.classList.add('disabled');
    } else {
        enabledToolSet.add(name);
        tagEl.classList.remove('disabled');
        tagEl.classList.add('enabled');
    }
    updateToolCount();
}

function getEnabledTools() {
    if (enabledToolSet.size === allTools.length) return null;
    return Array.from(enabledToolSet);
}

async function loadTools() {
    try {
        const resp = await fetch('/proxy_tools');
        if (!resp.ok) return;
        const data = await resp.json();
        const tools = data.tools || [];
        const toolList = document.getElementById('tool-list');
        const wrapper = document.getElementById('tool-panel-wrapper');

        if (tools.length === 0) {
            wrapper.style.display = 'none';
            return;
        }

        allTools = tools;
        enabledToolSet = new Set(tools.map(t => t.name));
        toolList.innerHTML = '';
        tools.forEach(t => {
            const tag = document.createElement('span');
            tag.className = 'tool-tag enabled';
            tag.title = t.description || '';
            tag.textContent = t.name;
            tag.onclick = () => toggleTool(t.name, tag);
            toolList.appendChild(tag);
        });
        updateToolCount();
        wrapper.style.display = 'block';
    } catch (e) {
        console.warn('Failed to load tools:', e);
    }
}

// Session check
(function checkSession() {
    // 初始化语言
    document.documentElement.lang = currentLang;
    applyTranslations();

    const saved = sessionStorage.getItem('userId');
    if (saved) {
        currentUserId = saved;
        initSession();
        document.getElementById('uid-display').textContent = 'UID: ' + saved;
        document.getElementById('login-screen').style.display = 'none';
        document.getElementById('chat-screen').style.display = 'flex';
        loadTools();
        refreshOasisTopics();
        startHistoryPolling();
    }
})();

// Login input handlers
document.getElementById('username-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') { e.preventDefault(); document.getElementById('password-input').focus(); }
});
document.getElementById('password-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') { e.preventDefault(); handleLogin(); }
});

// ===== 聊天逻辑 =====
const chatBox = document.getElementById('chat-box');
const inputField = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const cancelBtn = document.getElementById('cancel-btn');
const busyBtn = document.getElementById('busy-btn');
const refreshChatBtn = document.getElementById('refresh-chat-btn');
let _hasUnreadSystemMsg = 0;  // 0=无未读, 1=有未读

function showNewMsgBanner() {
    if (_hasUnreadSystemMsg) return;
    _hasUnreadSystemMsg = 1;
    refreshChatBtn.classList.add('has-new');
}

function hideNewMsgBanner() {
    _hasUnreadSystemMsg = 0;
    refreshChatBtn.classList.remove('has-new');
}

function handleNewMsgRefresh() {
    hideNewMsgBanner();
    switchToSession(currentSessionId, true);
}

// 按钮三态：idle(发送) / streaming(终止) / busy(系统占用中)
function setStreamingUI(streaming) {
    if (streaming) {
        sendBtn.style.display = 'none';
        cancelBtn.style.display = 'inline-block';
        busyBtn.style.display = 'none';
        inputField.disabled = true;
        cancelTargetSessionId = currentSessionId;
    } else {
        sendBtn.style.display = 'inline-block';
        cancelBtn.style.display = 'none';
        busyBtn.style.display = 'none';
        sendBtn.disabled = false;
        inputField.disabled = false;
        cancelTargetSessionId = null;
    }
}

function setSystemBusyUI(busy) {
    if (busy) {
        sendBtn.style.display = 'none';
        cancelBtn.style.display = 'inline-block';
        busyBtn.style.display = 'none';
        inputField.disabled = true;
        cancelTargetSessionId = currentSessionId;
    } else {
        sendBtn.style.display = 'inline-block';
        cancelBtn.style.display = 'none';
        busyBtn.style.display = 'none';
        sendBtn.disabled = false;
        inputField.disabled = false;
        cancelTargetSessionId = null;
    }
}

async function handleCancel() {
    const targetSession = cancelTargetSessionId || currentSessionId;
    if (currentAbortController) {
        currentAbortController.abort();
        currentAbortController = null;
    }
    try {
        await fetch("/proxy_cancel", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ session_id: targetSession })
        });
    } catch(e) { /* ignore */ }
    // 恢复 UI（无论是用户流式还是系统调用被终止）
    setStreamingUI(false);
    setSystemBusyUI(false);
}

// ===== TTS 朗读功能 =====
let currentTtsAudio = null;
let currentTtsBtn = null;

function stripMarkdownForTTS(md) {
    // 移除代码块（含内容）
    let text = md.replace(/```[\s\S]*?```/g, '('+t('code_omitted')+')');
    // 移除行内代码
    text = text.replace(/`[^`]+`/g, '');
    // 移除图片
    text = text.replace(/!\[.*?\]\(.*?\)/g, '');
    // 移除链接，保留文字
    text = text.replace(/\[([^\]]+)\]\(.*?\)/g, '$1');
    // 移除标题标记
    text = text.replace(/^#{1,6}\s+/gm, '');
    // 移除粗体/斜体标记
    text = text.replace(/\*{1,3}([^*]+)\*{1,3}/g, '$1');
    // 移除工具调用提示行
    text = text.replace(/.*🔧.*调用工具.*\n?/g, '');
    text = text.replace(/.*✅.*工具执行完成.*\n?/g, '');
    // 清理多余空行
    text = text.replace(/\n{3,}/g, '\n\n').trim();
    return text;
}

function stopTtsPlayback() {
    if (currentTtsAudio) {
        currentTtsAudio.pause();
        currentTtsAudio.src = '';
        currentTtsAudio = null;
    }
    if (currentTtsBtn) {
        currentTtsBtn.classList.remove('playing', 'loading');
        currentTtsBtn.querySelector('.tts-label').textContent = t('tts_read');
        currentTtsBtn = null;
    }
}

async function handleTTS(btn, text) {
    // 如果点击的是正在播放的按钮，则停止
    if (btn === currentTtsBtn && currentTtsAudio) {
        stopTtsPlayback();
        return;
    }
    // 停止上一个播放
    stopTtsPlayback();

    const cleanText = stripMarkdownForTTS(text);
    if (!cleanText) return;

    currentTtsBtn = btn;
    btn.classList.add('loading');
    btn.querySelector('.tts-label').textContent = t('tts_loading');

    try {
        const resp = await fetch('/proxy_tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: cleanText })
        });
        if (!resp.ok) throw new Error(t('tts_request_failed'));

        const blob = await resp.blob();
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);
        currentTtsAudio = audio;

        btn.classList.remove('loading');
        btn.classList.add('playing');
        btn.querySelector('.tts-label').textContent = t('tts_stop');

        audio.onended = () => {
            URL.revokeObjectURL(url);
            stopTtsPlayback();
        };
        audio.onerror = () => {
            URL.revokeObjectURL(url);
            stopTtsPlayback();
        };
        audio.play();
    } catch (e) {
        console.error('TTS error:', e);
        stopTtsPlayback();
    }
}

function createTtsButton(textRef) {
    const btn = document.createElement('div');
    btn.className = 'tts-btn';
    btn.innerHTML = `
        <span class="tts-spinner"></span>
        <svg class="tts-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
            <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
            <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
        </svg>
        <span class="tts-label">${t('tts_read')}</span>`;
    btn.onclick = () => handleTTS(btn, textRef());
    return btn;
}

function appendMessage(content, isUser = false, images = [], fileNames = [], audioNames = []) {
    const wrapper = document.createElement('div');
    wrapper.className = `flex ${isUser ? 'justify-end' : 'justify-start'} animate-in fade-in duration-300`;
    const div = document.createElement('div');
    div.className = `p-4 max-w-[85%] shadow-sm ${isUser ? 'bg-blue-600 text-white message-user' : 'bg-white border text-gray-800 message-agent'}`;
    if (isUser) {
        let extraHtml = '';
        if (images && images.length > 0) {
            extraHtml += images.map(src => `<img src="${src}" class="chat-inline-image">`).join('');
        }
        if (fileNames && fileNames.length > 0) {
            extraHtml += fileNames.map(n => `<div class="chat-file-tag">📄 ${escapeHtml(n)}</div>`).join('');
        }
        if (audioNames && audioNames.length > 0) {
            extraHtml += audioNames.map(n => `<div class="chat-audio-tag">🎤 ${escapeHtml(n)}</div>`).join('');
        }
        if (extraHtml) {
            div.innerHTML = extraHtml + '<div style="margin-top:6px">' + escapeHtml(content) + '</div>';
        } else {
            div.innerText = content;
        }
    } else {
        div.className += " markdown-body";
        div.innerHTML = marked.parse(content);
        div.querySelectorAll('pre code').forEach((block) => hljs.highlightElement(block));
        // AI 消息添加朗读按钮（content 非空时）
        if (content) {
            const ttsBtn = createTtsButton(() => div.innerText || div.textContent || '');
            div.appendChild(ttsBtn);
        }
    }
    wrapper.appendChild(div);
    chatBox.appendChild(wrapper);
    chatBox.scrollTop = chatBox.scrollHeight;
    return div;
}

function showTyping() {
    const wrapper = document.createElement('div');
    wrapper.id = 'typing-indicator';
    wrapper.className = 'flex justify-start';
    wrapper.innerHTML = `
        <div class="message-agent bg-white border p-4 flex space-x-2 items-center shadow-sm">
            <div class="dot"></div><div class="dot"></div><div class="dot"></div>
        </div>`;
    chatBox.appendChild(wrapper);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function handleSend() {
    const text = inputField.value.trim();
    if (!text && pendingImages.length === 0 && pendingFiles.length === 0 && pendingAudios.length === 0) return;
    if (sendBtn.disabled) return;

    // Stop recording if active
    if (isRecording) stopRecording();

    // Capture images, files, audios before clearing
    const imagesToSend = pendingImages.map(img => img.base64);
    const imagePreviewSrcs = [...imagesToSend];
    const filesToSend = pendingFiles.map(f => ({ name: f.name, content: f.content, type: f.type }));
    const fileNames = pendingFiles.map(f => f.name);
    const audiosToSend = pendingAudios.map(a => ({ base64: a.base64, name: a.name, format: a.format }));
    const audioNames = pendingAudios.map(a => a.name);

    const label = text || (imagePreviewSrcs.length ? '('+t('image_placeholder')+')' : audioNames.length ? '('+t('audio_placeholder')+')' : '('+t('file_placeholder')+')');
    appendMessage(label, true, imagePreviewSrcs, fileNames, audioNames);
    inputField.value = '';
    inputField.style.height = 'auto';
    pendingImages = [];
    pendingFiles = [];
    pendingAudios = [];
    pendingWorkflows = [];
    renderImagePreviews();
    renderFilePreviews();
    renderAudioPreviews();
    renderWorkflowPreviews();
    sendBtn.disabled = true;
    showTyping();

    currentAbortController = new AbortController();
    setStreamingUI(true);

    let agentDiv = null;
    let fullText = '';

    try {
        // --- 构造 OpenAI 格式的 content parts ---
        const contentParts = [];
        if (text) {
            contentParts.push({ type: 'text', text: text });
        }
        // 图片 → image_url
        for (const img of imagesToSend) {
            contentParts.push({ type: 'image_url', image_url: { url: img } });
        }
        // 音频 → input_audio
        for (const audio of audiosToSend) {
            contentParts.push({
                type: 'input_audio',
                input_audio: { data: audio.base64, format: audio.format || 'webm' }
            });
        }
        // 文件 → file
        for (const f of filesToSend) {
            const fileData = f.content.startsWith('data:') ? f.content : 'data:application/octet-stream;base64,' + f.content;
            contentParts.push({
                type: 'file',
                file: { filename: f.name, file_data: fileData }
            });
        }

        // 如果只有纯文本，content 用字符串；否则用 parts 数组
        let msgContent;
        if (contentParts.length === 1 && contentParts[0].type === 'text') {
            msgContent = contentParts[0].text;
        } else if (contentParts.length > 0) {
            msgContent = contentParts;
        } else {
            msgContent = '(空消息)';
        }

        // --- 构造 OpenAI /v1/chat/completions 请求 ---
        const openaiPayload = {
            model: 'mini-timebot',
            messages: [{ role: 'user', content: msgContent }],
            stream: true,
            session_id: currentSessionId,
            enabled_tools: getEnabledTools(),
        };

        const response = await fetch("/v1/chat/completions", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getAuthToken()
            },
            body: JSON.stringify(openaiPayload),
            signal: currentAbortController.signal
        });

        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) typingIndicator.remove();

        if (response.status === 401) {
            appendMessage(t('login_expired'), false);
            handleLogout();
            return;
        }
        if (!response.ok) throw new Error("Agent error");

        agentDiv = appendMessage('', false);

        // --- 解析 OpenAI SSE 流式响应（支持分段渲染） ---
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let allSegmentTexts = [];  // 记录所有段落的文本

        // 辅助函数：封存当前文本气泡，添加朗读按钮
        function sealCurrentBubble() {
            if (fullText && agentDiv) {
                agentDiv.innerHTML = marked.parse(fullText);
                agentDiv.querySelectorAll('pre code').forEach(b => hljs.highlightElement(b));
                const ttsBtn = createTtsButton(() => agentDiv.innerText || agentDiv.textContent || '');
                agentDiv.appendChild(ttsBtn);
                allSegmentTexts.push(fullText);
            }
        }

        // 辅助函数：创建新的 AI 文本气泡
        function startNewBubble() {
            fullText = '';
            agentDiv = appendMessage('', false);
        }

        // 辅助函数：创建工具调用指示区
        function createToolIndicator(toolName, type) {
            if (type === 'end') {
                // 查找最后一个同名且仍在运行的 indicator 并更新
                const allRunning = chatBox.querySelectorAll(`.stream-tool-indicator[data-tool-name="${CSS.escape(toolName)}"] .stream-tool-running`);
                const last = allRunning.length ? allRunning[allRunning.length - 1] : null;
                if (last) {
                    last.textContent = '✅';
                    last.classList.remove('stream-tool-running');
                    last.classList.add('stream-tool-done');
                }
                return;
            }
            const w = document.createElement('div');
            w.className = 'flex justify-start animate-in fade-in duration-200';
            const d = document.createElement('div');
            d.className = 'stream-tool-indicator';
            d.dataset.toolName = toolName;
            d.innerHTML = `<span class="stream-tool-icon">🔧</span> <span class="stream-tool-name">${escapeHtml(toolName)}</span> <span class="stream-tool-status stream-tool-running">…</span>`;
            w.appendChild(d);
            chatBox.appendChild(w);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop();

            for (const line of lines) {
                if (!line.startsWith('data: ')) continue;
                const data = line.slice(6).trim();
                if (data === '[DONE]') continue;

                try {
                    const chunk = JSON.parse(data);
                    const delta = chunk.choices && chunk.choices[0] && chunk.choices[0].delta;
                    if (!delta) continue;

                    // --- 处理结构化 meta 事件 ---
                    if (delta.meta) {
                        const m = delta.meta;
                        if (m.type === 'tools_start') {
                            // LLM 回复结束，即将调工具 → 封存当前气泡
                            sealCurrentBubble();
                        } else if (m.type === 'tool_start') {
                            createToolIndicator(m.name, 'start');
                        } else if (m.type === 'tool_end') {
                            createToolIndicator(m.name, 'end');
                        } else if (m.type === 'tools_end') {
                            // 所有工具执行完毕（可选：加分隔符）
                        } else if (m.type === 'ai_start') {
                            // 新一轮 LLM 开始 → 创建新文本气泡
                            startNewBubble();
                        }
                        continue;
                    }

                    // --- 处理文本内容 ---
                    if (delta.content) {
                        fullText += delta.content;
                        agentDiv.innerHTML = marked.parse(fullText);
                        agentDiv.querySelectorAll('pre code').forEach((block) => {
                            if (!block.dataset.highlighted) {
                                hljs.highlightElement(block);
                                block.dataset.highlighted = 'true';
                            }
                        });
                        chatBox.scrollTop = chatBox.scrollHeight;
                    }
                } catch(e) {
                    // 跳过无法解析的 chunk
                }
            }
        }

        // 流式结束：封存最后一个气泡
        if (fullText) {
            agentDiv.innerHTML = marked.parse(fullText);
            agentDiv.querySelectorAll('pre code').forEach((block) => hljs.highlightElement(block));
            const ttsBtn = createTtsButton(() => agentDiv.innerText || agentDiv.textContent || '');
            agentDiv.appendChild(ttsBtn);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        if (!fullText && allSegmentTexts.length === 0) {
            agentDiv.innerHTML = `<span class="text-gray-400">${t('no_response')}</span>`;
        }

        // After agent response, refresh OASIS topics (in case a new discussion was started)
        setTimeout(() => refreshOasisTopics(), 1000);

    } catch (error) {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) typingIndicator.remove();
        if (error.name === 'AbortError') {
            if (agentDiv) {
                fullText += '\n\n' + t('thinking_stopped');
                agentDiv.innerHTML = marked.parse(fullText);
            } else {
                appendMessage(t('thinking_stopped'), false);
            }
        } else {
            appendMessage(t('agent_error') + ': ' + error.message, false);
        }
    } finally {
        currentAbortController = null;
        setStreamingUI(false);
        hideNewMsgBanner();
    }
}

inputField.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});
inputField.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
});
inputField.addEventListener('paste', handlePasteImage);

// ================================================================
// ===== Add Workflow 功能 =====
// ================================================================
let pendingWorkflows = [];  // [{name: 'xxx'}, ...]

function renderWorkflowPreviews() {
    const area = document.getElementById('workflow-preview-area');
    if (!pendingWorkflows.length) { area.style.display = 'none'; return; }
    area.style.display = 'flex';
    area.innerHTML = pendingWorkflows.map((wf, i) =>
        `<span class="workflow-tag">📋 ${escapeHtml(wf.name)}<span class="wf-remove" onclick="removeWorkflow(${i})">&times;</span></span>`
    ).join('');
}

function removeWorkflow(idx) {
    pendingWorkflows.splice(idx, 1);
    renderWorkflowPreviews();
}

async function showWorkflowPopup() {
    try {
        const r = await fetch('/proxy_visual/load-layouts', {
            headers: { 'Authorization': 'Bearer ' + getAuthToken() }
        });
        const layouts = await r.json();
        if (!layouts.length) { alert(t('wf_no_workflows')); return; }

        const overlay = document.createElement('div');
        overlay.className = 'orch-modal-overlay';
        overlay.id = 'wf-popup-overlay';
        overlay.innerHTML = `
            <div class="orch-modal" style="min-width:320px;max-width:420px;">
                <h3>${t('wf_popup_title')}</h3>
                <div id="wf-select-list" style="max-height:300px;overflow-y:auto;"></div>
                <div class="orch-modal-btns">
                    <button id="wf-cancel-btn" style="padding:6px 14px;border-radius:6px;border:1px solid #d1d5db;background:white;color:#374151;cursor:pointer;font-size:12px;">${t('wf_cancel')}</button>
                    <button id="wf-confirm-btn" disabled style="padding:6px 14px;border-radius:6px;border:none;background:#7c3aed;color:white;cursor:pointer;font-size:12px;opacity:0.5;">${t('wf_confirm')}</button>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        let selectedName = null;
        overlay.querySelector('#wf-cancel-btn').addEventListener('click', () => overlay.remove());
        overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });

        const listEl = overlay.querySelector('#wf-select-list');
        for (const name of layouts) {
            const item = document.createElement('div');
            item.className = 'orch-session-item';
            item.style.cssText = 'padding:10px 12px;border-radius:8px;cursor:pointer;border:1px solid transparent;margin-bottom:4px;display:flex;align-items:center;gap:8px;transition:all 0.15s;';
            item.innerHTML = `<span style="font-size:16px;">📋</span><span style="flex:1;font-size:13px;color:#374151;">${escapeHtml(name)}</span>`;
            item.addEventListener('click', () => {
                listEl.querySelectorAll('.orch-session-item').forEach(el => {
                    el.style.background = '';
                    el.style.borderColor = 'transparent';
                });
                item.style.background = '#f5f3ff';
                item.style.borderColor = '#c4b5fd';
                selectedName = name;
                const btn = overlay.querySelector('#wf-confirm-btn');
                btn.disabled = false;
                btn.style.opacity = '1';
            });
            item.addEventListener('dblclick', () => {
                selectedName = name;
                addWorkflowToContext(selectedName);
                overlay.remove();
            });
            listEl.appendChild(item);
        }

        overlay.querySelector('#wf-confirm-btn').addEventListener('click', () => {
            if (selectedName) {
                addWorkflowToContext(selectedName);
                overlay.remove();
            }
        });
    } catch(e) {
        console.error('Failed to load workflows:', e);
    }
}

function addWorkflowToContext(name) {
    // Avoid duplicate
    if (pendingWorkflows.some(w => w.name === name)) return;
    pendingWorkflows.push({ name });
    renderWorkflowPreviews();
    // Also prepend workflow context to input
    const prefix = t('wf_context_prefix', { name });
    inputField.value = prefix + inputField.value;
    inputField.focus();
}

// ================================================================
// ===== OASIS 讨论面板逻辑 =====
// ================================================================

let oasisPanelOpen = false;
let oasisCurrentTopicId = null;
let oasisPollingTimer = null;
let oasisStreamReader = null;

// Expert avatar mapping
const expertAvatars = {
    [t('oasis_expert_creative')]: { cls: 'expert-creative', icon: '💡' },
    [t('oasis_expert_critical')]: { cls: 'expert-critical', icon: '🔍' },
    [t('oasis_expert_data')]: { cls: 'expert-data', icon: '📊' },
    [t('oasis_expert_synthesis')]: { cls: 'expert-synthesis', icon: '🎯' },
};

function getExpertAvatar(name) {
    return expertAvatars[name] || { cls: 'expert-default', icon: '🤖' };
}

function getStatusBadge(status) {
    const map = {
        'pending': { cls: 'oasis-status-pending', text: t('oasis_status_pending') },
        'discussing': { cls: 'oasis-status-discussing', text: t('oasis_status_discussing') },
        'concluded': { cls: 'oasis-status-concluded', text: t('oasis_status_concluded') },
        'error': { cls: 'oasis-status-error', text: t('oasis_status_error') },
        'cancelled': { cls: 'oasis-status-error', text: t('oasis_status_cancelled') },
    };
    return map[status] || { cls: 'oasis-status-pending', text: status };
}

function formatTime(ts) {
    const d = new Date(ts * 1000);
    return d.toLocaleTimeString(currentLang === 'zh-CN' ? 'zh-CN' : 'en-US', { hour: '2-digit', minute: '2-digit' });
}

function toggleOasisPanel() {
    const panel = document.getElementById('oasis-panel');
    oasisPanelOpen = !oasisPanelOpen;
    if (oasisPanelOpen) {
        panel.classList.remove('collapsed-panel');
        panel.classList.remove('mobile-open');
        refreshOasisTopics();
    } else {
        panel.classList.add('collapsed-panel');
        panel.classList.remove('mobile-open');
        stopOasisPolling();
    }
}

function toggleOasisMobile() {
    const panel = document.getElementById('oasis-panel');
    if (panel.classList.contains('mobile-open')) {
        panel.classList.remove('mobile-open');
        stopOasisPolling();
    } else {
        panel.classList.remove('collapsed-panel');
        panel.classList.add('mobile-open');
        refreshOasisTopics();
    }
}

function toggleMobileMenu() {
    const dd = document.getElementById('mobile-menu-dropdown');
    if (dd.style.display === 'none') {
        dd.style.display = 'block';
        // close when tapping outside
        setTimeout(() => document.addEventListener('click', closeMobileMenuOutside, { once: true }), 0);
    } else {
        dd.style.display = 'none';
    }
}
function closeMobileMenu() {
    document.getElementById('mobile-menu-dropdown').style.display = 'none';
}
function closeMobileMenuOutside(e) {
    const wrapper = document.querySelector('.mobile-menu-wrapper');
    if (!wrapper.contains(e.target)) closeMobileMenu();
}

function stopOasisPolling() {
    if (oasisPollingTimer) {
        clearInterval(oasisPollingTimer);
        oasisPollingTimer = null;
    }
    if (oasisStreamReader) {
        oasisStreamReader.cancel();
        oasisStreamReader = null;
    }
}

async function refreshOasisTopics() {
    try {
        const resp = await fetch('/proxy_oasis/topics');
        console.log('[OASIS] Topics response status:', resp.status);
        if (!resp.ok) {
            console.error('[OASIS] Failed to fetch topics:', resp.status);
            return;
        }
        const topics = await resp.json();
        console.log('[OASIS] Topics data:', topics);
        renderTopicList(topics);
    } catch (e) {
        console.error('[OASIS] Failed to load topics:', e);
    }
}

function renderTopicList(topics) {
    const container = document.getElementById('oasis-topic-list');
    const countEl = document.getElementById('oasis-topic-count');
    countEl.textContent = topics.length + ' ' + t('oasis_topics_count');

    if (topics.length === 0) {
        container.innerHTML = `
            <div class="p-6 text-center text-gray-400 text-sm">
                <div class="text-3xl mb-2">🏛️</div>
                <p>${t('oasis_no_topics')}</p>
                <p class="text-xs mt-1">${t('oasis_start_hint')}</p>
            </div>`;
        return;
    }

    // Sort: discussing first, then by created_at desc
    topics.sort((a, b) => {
        if (a.status === 'discussing' && b.status !== 'discussing') return -1;
        if (b.status === 'discussing' && a.status !== 'discussing') return 1;
        return (b.created_at || 0) - (a.created_at || 0);
    });

    container.innerHTML = topics.map(topic => {
        const badge = getStatusBadge(topic.status);
        const isActive = topic.topic_id === oasisCurrentTopicId;
        const isRunning = topic.status === 'discussing' || topic.status === 'pending';
        return `
            <div class="oasis-topic-item p-3 border-b ${isActive ? 'active' : ''}" onclick="openOasisTopic('${topic.topic_id}')">
                <div class="flex items-center justify-between mb-1">
                    <span class="oasis-status-badge ${badge.cls}">${badge.text}</span>
                    <div class="flex items-center space-x-1">
                        ${isRunning ? `<button onclick="event.stopPropagation(); cancelOasisTopic('${topic.topic_id}')" class="oasis-action-btn oasis-btn-cancel" title="${t('oasis_cancel')}">⏹</button>` : ''}
                        <button onclick="event.stopPropagation(); deleteOasisTopic('${topic.topic_id}')" class="oasis-action-btn oasis-btn-delete" title="${t('oasis_delete')}">🗑</button>
                        <span class="text-[10px] text-gray-400">${topic.created_at ? formatTime(topic.created_at) : ''}</span>
                    </div>
                </div>
                <p class="text-sm text-gray-800 font-medium line-clamp-2">${escapeHtml(topic.question)}</p>
                <div class="flex items-center space-x-3 mt-1 text-[10px] text-gray-400">
                    <span>💬 ${topic.post_count || 0} ${t('oasis_posts')}</span>
                    <span>🔄 ${topic.current_round}/${topic.max_rounds} ${t('oasis_round')}</span>
                </div>
            </div>`;
    }).join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function openOasisTopic(topicId) {
    oasisCurrentTopicId = topicId;
    stopOasisPolling();

    // Switch to detail view
    document.getElementById('oasis-topic-list-view').style.display = 'none';
    document.getElementById('oasis-detail-view').style.display = 'flex';

    // Load topic detail
    await loadTopicDetail(topicId);
}

function showOasisTopicList() {
    stopOasisPolling();
    oasisCurrentTopicId = null;
    document.getElementById('oasis-detail-view').style.display = 'none';
    document.getElementById('oasis-topic-list-view').style.display = 'flex';
    refreshOasisTopics();
}

async function loadTopicDetail(topicId) {
    try {
        const resp = await fetch(`/proxy_oasis/topics/${topicId}`);
        console.log('[OASIS] Detail response status:', resp.status);
        if (!resp.ok) {
            console.error('[OASIS] Failed to fetch detail:', resp.status);
            return;
        }
        const detail = await resp.json();
        console.log('[OASIS] Detail data:', detail);
        console.log('[OASIS] Posts count:', (detail.posts || []).length);
        renderTopicDetail(detail);

        // If still discussing, start polling for updates
        if (detail.status === 'discussing' || detail.status === 'pending') {
            startDetailPolling(topicId);
        }
    } catch (e) {
        console.warn('Failed to load topic detail:', e);
    }
}

function renderTopicDetail(detail) {
    const badge = getStatusBadge(detail.status);
    document.getElementById('oasis-detail-status').className = 'oasis-status-badge ' + badge.cls;
    document.getElementById('oasis-detail-status').textContent = badge.text;
    const roundText = currentLang === 'zh-CN' ? `第 ${detail.current_round}/${detail.max_rounds} ${t('oasis_round')}` : `Round ${detail.current_round}/${detail.max_rounds}`;
    document.getElementById('oasis-detail-round').textContent = roundText;
    document.getElementById('oasis-detail-question').textContent = detail.question;

    // Render action buttons in detail header
    const actionsEl = document.getElementById('oasis-detail-actions');
    const isRunning = detail.status === 'discussing' || detail.status === 'pending';
    let btns = '';
    if (isRunning) {
        btns += `<button onclick="cancelOasisTopic('${detail.topic_id}')" class="oasis-detail-action-btn cancel">⏹ ${t('oasis_cancel')}</button>`;
    }
    btns += `<button onclick="deleteOasisTopic('${detail.topic_id}')" class="oasis-detail-action-btn delete">🗑 ${t('oasis_delete')}</button>`;
    actionsEl.innerHTML = btns;

    renderPosts(detail.posts || [], detail.timeline || [], detail.discussion !== false);

    // Show/hide conclusion
    const conclusionArea = document.getElementById('oasis-conclusion-area');
    if (detail.conclusion && detail.status === 'concluded') {
        document.getElementById('oasis-conclusion-text').innerHTML = marked.parse(detail.conclusion || '');
        conclusionArea.style.display = 'block';
        // Reset to expanded state
        const textEl = document.getElementById('oasis-conclusion-text');
        const toggleEl = document.getElementById('oasis-conclusion-toggle');
        textEl.style.display = '';
        if (toggleEl) toggleEl.textContent = '▼';
    } else {
        conclusionArea.style.display = 'none';
    }
}

function toggleConclusionCollapse() {
    const textEl = document.getElementById('oasis-conclusion-text');
    const toggleEl = document.getElementById('oasis-conclusion-toggle');
    if (!textEl) return;
    const collapsed = textEl.style.display === 'none';
    textEl.style.display = collapsed ? '' : 'none';
    if (toggleEl) toggleEl.textContent = collapsed ? '▼' : '▶';
}

function fmtElapsed(sec) {
    if (sec === undefined || sec === null) return '';
    const s = Math.round(sec);
    if (s < 60) return 'T+' + s + 's';
    const m = Math.floor(s / 60);
    return 'T+' + m + 'm' + (s % 60) + 's';
}

function renderPosts(posts, timeline, isDiscussion) {
    const box = document.getElementById('oasis-posts-box');

    if (posts.length === 0 && (!timeline || timeline.length === 0)) {
        box.innerHTML = `
            <div class="text-center text-gray-400 text-sm py-8">
                <div class="text-2xl mb-2">💭</div>
                <p>${t('oasis_waiting')}</p>
            </div>`;
        return;
    }

    // ── timeline 事件（绿色卡片）+ 帖子混排 ──
    const items = [];
    if (timeline) {
        for (const ev of timeline) {
            // 讨论模式下不显示 agent_done
            if (ev.event === 'agent_done') continue;
            items.push({type: 'event', elapsed: ev.elapsed, data: ev});
        }
    }
    for (const p of posts) {
        items.push({type: 'post', elapsed: p.elapsed || 0, data: p});
    }
    items.sort((a, b) => a.elapsed - b.elapsed);

    box.innerHTML = items.map(item => {
        if (item.type === 'event') {
            const ev = item.data;
            const evIcons = {start:'🚀', round:'📢', agent_call:'⏳', conclude:'🏁', manual_post:'📝'};
            const icon = evIcons[ev.event] || '⏱';
            const label = ev.agent ? ev.agent + (ev.detail ? ' · ' + ev.detail : '') : (ev.detail || ev.event);
            return `
                <div class="oasis-post bg-green-50 rounded-xl p-3 border border-green-200 shadow-sm">
                    <div class="flex items-start space-x-2">
                        <div class="flex-1 min-w-0">
                            <div class="flex items-center justify-between">
                                <span class="text-xs font-semibold text-green-700">${icon} ${escapeHtml(label)}</span>
                                <span class="text-[10px] font-mono text-green-500">${fmtElapsed(ev.elapsed)}</span>
                            </div>
                        </div>
                    </div>
                </div>`;
        }
        // Post
        const p = item.data;
        const avatar = getExpertAvatar(p.author);
        const isReply = p.reply_to !== null && p.reply_to !== undefined;
        const totalVotes = p.upvotes + p.downvotes;
        const upPct = totalVotes > 0 ? (p.upvotes / totalVotes * 100) : 50;

        return `
            <div class="oasis-post bg-white rounded-xl p-3 border shadow-sm ${isReply ? 'ml-4 border-l-2 border-l-blue-300' : ''}">
                <div class="flex items-start space-x-2">
                    <div class="oasis-expert-avatar ${avatar.cls}" title="${escapeHtml(p.author)}">${avatar.icon}</div>
                    <div class="flex-1 min-w-0">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-semibold text-gray-700">${escapeHtml(p.author)}</span>
                            <div class="flex items-center space-x-2 text-[10px] text-gray-400">
                                <span class="font-mono text-blue-500">${fmtElapsed(p.elapsed)}</span>
                                ${isReply ? '<span>↩️ #' + p.reply_to + '</span>' : ''}
                                <span>#${p.id}</span>
                            </div>
                        </div>
                        <div class="text-xs text-gray-600 mt-1 leading-relaxed markdown-body">${marked.parse(p.content || '')}</div>
                        <div class="flex items-center space-x-3 mt-2">
                            <div class="flex items-center space-x-1">
                                <span class="text-[10px]">👍 ${p.upvotes}</span>
                                <span class="text-[10px]">👎 ${p.downvotes}</span>
                            </div>
                            ${totalVotes > 0 ? `
                                <div class="flex-1 oasis-vote-bar flex">
                                    <div class="oasis-vote-up" style="width: ${upPct}%"></div>
                                    <div class="oasis-vote-down" style="width: ${100 - upPct}%"></div>
                                </div>` : ''}
                        </div>
                    </div>
                </div>
            </div>`;
    }).join('');

    // Auto-scroll to bottom
    box.scrollTop = box.scrollHeight;

    // Highlight code blocks in rendered markdown
    box.querySelectorAll('pre code').forEach(el => {
        try { hljs.highlightElement(el); } catch(e) {}
    });
}

function startDetailPolling(topicId) {
    stopOasisPolling();
    let lastPostCount = 0;
    let lastTimelineCount = 0;
    let errorCount = 0;
    oasisPollingTimer = setInterval(async () => {
        if (oasisCurrentTopicId !== topicId) {
            stopOasisPolling();
            return;
        }
        try {
            const resp = await fetch(`/proxy_oasis/topics/${topicId}`);
            if (!resp.ok) {
                errorCount++;
                console.warn(`OASIS polling error: HTTP ${resp.status}`);
                if (errorCount >= 5) {
                    console.error('OASIS polling failed 5 times, stopping');
                    stopOasisPolling();
                }
                return;
            }
            errorCount = 0;
            const detail = await resp.json();

            // Re-render if posts or timeline changed
            const currentPostCount = (detail.posts || []).length;
            const currentTimelineCount = (detail.timeline || []).length;
            if (currentPostCount !== lastPostCount || currentTimelineCount !== lastTimelineCount || detail.status !== 'discussing') {
                renderTopicDetail(detail);
                lastPostCount = currentPostCount;
                lastTimelineCount = currentTimelineCount;
            }

            // Stop polling when discussion ends
            if (detail.status === 'concluded' || detail.status === 'error') {
                stopOasisPolling();
                refreshOasisTopics();
            }
        } catch (e) {
            errorCount++;
            console.warn('OASIS polling error:', e);
        }
    }, 1500); // Poll every 1.5 seconds for faster updates
}

async function cancelOasisTopic(topicId) {
    if (!confirm(t('oasis_cancel_confirm'))) return;
    try {
        const resp = await fetch(`/proxy_oasis/topics/${topicId}/cancel`, { method: 'POST' });
        const data = await resp.json();
        if (resp.ok) {
            stopOasisPolling();
            if (oasisCurrentTopicId === topicId) {
                await loadTopicDetail(topicId);
            }
            refreshOasisTopics();
        } else {
            alert(t('oasis_action_fail') + ': ' + (data.error || data.detail || data.message || ''));
        }
    } catch (e) {
        alert(t('oasis_action_fail') + ': ' + e.message);
    }
}

async function deleteOasisTopic(topicId) {
    if (!confirm(t('oasis_delete_confirm'))) return;
    try {
        const resp = await fetch(`/proxy_oasis/topics/${topicId}/purge`, { method: 'POST' });
        const data = await resp.json();
        if (resp.ok) {
            stopOasisPolling();
            if (oasisCurrentTopicId === topicId) {
                showOasisTopicList();
            } else {
                refreshOasisTopics();
            }
        } else {
            alert(t('oasis_action_fail') + ': ' + (data.error || data.detail || data.message || ''));
        }
    } catch (e) {
        alert(t('oasis_action_fail') + ': ' + e.message);
    }
}

async function deleteAllOasisTopics() {
    const countEl = document.getElementById('oasis-topic-count');
    const count = parseInt(countEl.textContent) || 0;
    if (count === 0) {
        alert(t('oasis_no_topics') || '暂无讨论话题');
        return;
    }
    const confirmMsg = (currentLang === 'zh-CN')
        ? `确定要清空所有 ${count} 个讨论话题吗？此操作不可恢复！`
        : `Delete all ${count} topics? This cannot be undone!`;
    if (!confirm(confirmMsg)) return;

    try {
        const resp = await fetch('/proxy_oasis/topics', { method: 'DELETE' });
        const data = await resp.json();
        if (resp.ok) {
            stopOasisPolling();
            showOasisTopicList();
            alert((currentLang === 'zh-CN' ? '已删除 ' : 'Deleted ') + data.deleted_count + (currentLang === 'zh-CN' ? ' 个话题' : ' topics'));
        } else {
            alert(t('oasis_action_fail') + ': ' + (data.error || data.detail || data.message || ''));
        }
    } catch (e) {
        alert(t('oasis_action_fail') + ': ' + e.message);
    }
}

// Auto-refresh topic list periodically when panel is open
setInterval(() => {
    if (oasisPanelOpen && !oasisCurrentTopicId && currentUserId) {
        refreshOasisTopics();
    }
}, 10000); // Every 10 seconds

// === System trigger polling: 检测后台系统触发产生的新消息 ===
let _sessionStatusTimer = null;

function startSessionStatusPolling() {
    stopSessionStatusPolling();
    _sessionStatusTimer = setInterval(async () => {
        if (!currentUserId || !currentSessionId) return;
        // 用户正在流式对话中，跳过轮询
        if (cancelBtn.style.display !== 'none') return;
        try {
            const resp = await fetch('/proxy_session_status', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ session_id: currentSessionId })
            });
            const data = await resp.json();

            // --- 系统占用状态 ---
            if (data.busy) {
                setSystemBusyUI(true);
            } else if (busyBtn.style.display !== 'none') {
                // busy → 不busy：恢复按钮，显示刷新横幅
                setSystemBusyUI(false);
                showNewMsgBanner();
            }
        } catch(e) {
            // 静默忽略
        }
    }, 5000); // 每 5 秒轮询一次
}

function stopSessionStatusPolling() {
    if (_sessionStatusTimer) {
        clearInterval(_sessionStatusTimer);
        _sessionStatusTimer = null;
    }
}

// 登录成功后启动轮询
const _origLogin = typeof handleLogin === 'function' ? null : null;
// 监听 chat-container 可见性来启动/停止轮询
const _chatObserver = new MutationObserver(() => {
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer && chatContainer.style.display !== 'none') {
        startSessionStatusPolling();
    } else {
        stopSessionStatusPolling();
    }
});
_chatObserver.observe(document.body, { childList: true, subtree: true, attributes: true });

// ================================================================
// ===== Group Chat (群聊) 逻辑 =====
// ================================================================

// Agent 颜色方案：根据名字 hash 分配一致的颜色
const _agentColorPalette = [
    { bg: '#f0fdf4', border: '#bbf7d0', text: '#166534', sender: '#15803d', pre: '#1a2e1a', code: '#d1fae5' },
    { bg: '#eff6ff', border: '#bfdbfe', text: '#1e40af', sender: '#2563eb', pre: '#1e2a4a', code: '#dbeafe' },
    { bg: '#fdf4ff', border: '#e9d5ff', text: '#6b21a8', sender: '#7c3aed', pre: '#2d1a3e', code: '#ede9fe' },
    { bg: '#fff7ed', border: '#fed7aa', text: '#9a3412', sender: '#ea580c', pre: '#3b1a0a', code: '#ffedd5' },
    { bg: '#fef2f2', border: '#fecaca', text: '#991b1b', sender: '#dc2626', pre: '#3b1212', code: '#fee2e2' },
    { bg: '#f0fdfa', border: '#99f6e4', text: '#115e59', sender: '#0d9488', pre: '#0f2d2a', code: '#ccfbf1' },
    { bg: '#fefce8', border: '#fde68a', text: '#854d0e', sender: '#ca8a04', pre: '#2d2305', code: '#fef9c3' },
    { bg: '#fdf2f8', border: '#fbcfe8', text: '#9d174d', sender: '#db2777', pre: '#3b0d24', code: '#fce7f3' },
];
const _agentColorCache = {};
function getAgentColor(sender) {
    if (_agentColorCache[sender]) return _agentColorCache[sender];
    let hash = 0;
    for (let i = 0; i < sender.length; i++) {
        hash = ((hash << 5) - hash) + sender.charCodeAt(i);
        hash |= 0;
    }
    const color = _agentColorPalette[Math.abs(hash) % _agentColorPalette.length];
    _agentColorCache[sender] = color;
    return color;
}
function applyAgentColor(el, sender) {
    const c = getAgentColor(sender);
    const content = el.querySelector('.group-msg-content');
    const senderEl = el.querySelector('.group-msg-sender');
    if (content) {
        content.style.background = c.bg;
        content.style.borderColor = c.border;
        content.style.color = c.text;
    }
    if (senderEl) senderEl.style.color = c.sender;
    el.querySelectorAll('.group-msg-content pre').forEach(pre => { pre.style.background = c.pre; });
    el.querySelectorAll('.group-msg-content code').forEach(code => { code.style.color = c.code; });
}

let currentPage = 'chat'; // 'chat' or 'group'
let currentGroupId = null;
let groupPollingTimer = null;
let groupLastMsgId = 0;
let groupMuted = false;
const groupSenderTitles = {};  // sender -> display title mapping

function getGroupSenderTitle(sender) {
    let name = groupSenderTitles[sender] || sender;
    if (name.length > 7) name = name.slice(0, 7) + '…';
    return name;
}

// === @ Mention 功能 ===
let mentionSelectedIds = [];  // 被 @ 选中的 agent session_id 列表
let currentGroupMembers = []; // 当前群的 agent 成员缓存

function onGroupInputChange(e) {
    const input = document.getElementById('group-input');
    const val = input.value;
    const cursorPos = input.selectionStart;
    // 检测光标前一个字符是否刚输入了 @
    if (cursorPos > 0 && val[cursorPos - 1] === '@') {
        showMentionPopup();
    }
}

function showMentionPopup() {
    const popup = document.getElementById('mention-popup');
    const listEl = document.getElementById('mention-list');
    // 从 groupSenderTitles 构建 agent 列表
    const agents = [];
    for (const [key, title] of Object.entries(groupSenderTitles)) {
        agents.push({ id: key, title: title });
    }
    if (agents.length === 0) {
        listEl.innerHTML = '<div style="padding:10px 14px;font-size:12px;color:#9ca3af;">群内暂无 Agent 成员</div>';
        popup.classList.add('show');
        return;
    }
    currentGroupMembers = agents;
    listEl.innerHTML = agents.map(a => {
        const sel = mentionSelectedIds.includes(a.id) ? ' selected' : '';
        const check = mentionSelectedIds.includes(a.id) ? '✓' : '';
        return `<div class="mention-item${sel}" data-id="${a.id}" onclick="toggleMentionItem(this, '${a.id}')">
            <div class="mention-check">${check}</div>
            <div class="mention-name" title="${a.title}">${a.title}</div>
        </div>`;
    }).join('');
    popup.classList.add('show');
}

function toggleMentionItem(el, agentId) {
    const idx = mentionSelectedIds.indexOf(agentId);
    if (idx >= 0) {
        mentionSelectedIds.splice(idx, 1);
        el.classList.remove('selected');
        el.querySelector('.mention-check').textContent = '';
    } else {
        mentionSelectedIds.push(agentId);
        el.classList.add('selected');
        el.querySelector('.mention-check').textContent = '✓';
    }
}

function confirmMention() {
    const popup = document.getElementById('mention-popup');
    popup.classList.remove('show');
    const input = document.getElementById('group-input');
    // 删掉输入框里刚输入的 @，替换为 @name 标签
    let val = input.value;
    // 找到最后一个 @ 的位置并替换
    const lastAt = val.lastIndexOf('@');
    if (lastAt >= 0) {
        const before = val.slice(0, lastAt);
        const after = val.slice(lastAt + 1);
        const tags = mentionSelectedIds.map(id => '@' + (groupSenderTitles[id] || id)).join(' ');
        input.value = before + tags + ' ' + after;
    }
    input.focus();
}

function hideMentionPopup() {
    document.getElementById('mention-popup').classList.remove('show');
}

// 点击输入区域外关闭弹层
document.addEventListener('click', function(e) {
    const popup = document.getElementById('mention-popup');
    const inputArea = document.querySelector('.group-input-area');
    if (popup && inputArea && !inputArea.contains(e.target)) {
        popup.classList.remove('show');
    }
});

function switchPage(page) {
    currentPage = page;
    // Update tabs
    document.getElementById('tab-chat').classList.toggle('active', page === 'chat');
    document.getElementById('tab-group').classList.toggle('active', page === 'group');
    document.getElementById('tab-orchestrate').classList.toggle('active', page === 'orchestrate');
    // Show/hide pages
    const chatPage = document.getElementById('page-chat');
    const groupPage = document.getElementById('page-group');
    const orchPage = document.getElementById('page-orchestrate');
    if (page === 'chat') {
        chatPage.classList.remove('hidden-page');
        chatPage.style.display = 'flex';
        groupPage.classList.remove('active');
        groupPage.classList.remove('mobile-chat-open');
        if (orchPage) orchPage.classList.remove('active');
        stopGroupPolling();
        stopGroupListPolling();
    } else if (page === 'group') {
        chatPage.classList.add('hidden-page');
        chatPage.style.display = 'none';
        groupPage.classList.add('active');
        if (orchPage) orchPage.classList.remove('active');
        loadGroupList();
        startGroupListPolling();
        // 如果已有打开的群，恢复消息轮询
        if (currentGroupId) {
            startGroupPolling(currentGroupId);
        }
    } else if (page === 'orchestrate') {
        chatPage.classList.add('hidden-page');
        chatPage.style.display = 'none';
        groupPage.classList.remove('active');
        groupPage.classList.remove('mobile-chat-open');
        if (orchPage) orchPage.classList.add('active');
        stopGroupPolling();
        stopGroupListPolling();
        if (!window._orchInitialized) { orchInit(); window._orchInitialized = true; }
    }
}

function stopGroupPolling() {
    if (groupPollingTimer) { clearInterval(groupPollingTimer); groupPollingTimer = null; }
}

let _groupListPollingTimer = null;
function startGroupListPolling() {
    stopGroupListPolling();
    _groupListPollingTimer = setInterval(() => {
        if (currentPage === 'group' && currentUserId) {
            loadGroupList();
        }
    }, 8000);
}
function stopGroupListPolling() {
    if (_groupListPollingTimer) { clearInterval(_groupListPollingTimer); _groupListPollingTimer = null; }
}

async function loadGroupList() {
    try {
        const resp = await fetch('/proxy_groups', {
            headers: { 'Authorization': 'Bearer ' + getAuthToken() }
        });
        if (!resp.ok) return;
        const groups = await resp.json();
        renderGroupList(groups);
    } catch (e) {
        console.error('Failed to load groups:', e);
    }
}

function renderGroupList(groups) {
    const container = document.getElementById('group-list');
    if (!groups || groups.length === 0) {
        container.innerHTML = `
            <div class="group-empty-state" style="padding:40px 0;">
                <div class="empty-icon">👥</div>
                <div class="empty-text">${t('group_no_groups')}</div>
            </div>`;
        return;
    }
    container.innerHTML = groups.map(g => {
        const isActive = g.group_id === currentGroupId;
        return `
            <div class="group-item ${isActive ? 'active' : ''}" onclick="openGroup('${g.group_id}')">
                <div class="group-name">${escapeHtml(g.name)}</div>
                <div class="group-meta">${g.member_count || 0} ${t('group_member_count')} · ${g.message_count || 0} ${t('group_msg_count')}</div>
                <button class="group-delete-btn" onclick="event.stopPropagation(); deleteGroup('${g.group_id}')">${t('delete_session')}</button>
            </div>`;
    }).join('');
}

async function openGroup(groupId) {
    currentGroupId = groupId;
    groupLastMsgId = 0;
    stopGroupPolling();

    // Mobile: switch to chat view
    document.getElementById('page-group').classList.add('mobile-chat-open');

    document.getElementById('group-empty-placeholder').style.display = 'none';
    const activeChat = document.getElementById('group-active-chat');
    activeChat.style.display = 'flex';

    // Load group detail
    try {
        const resp = await fetch(`/proxy_groups/${groupId}`, {
            headers: { 'Authorization': 'Bearer ' + getAuthToken() }
        });
        if (!resp.ok) return;
        const detail = await resp.json();

        document.getElementById('group-active-name').textContent = detail.name;
        document.getElementById('group-active-id').textContent = '#' + groupId.slice(-8);

        // Build sender -> title mapping from members
        for (const key of Object.keys(groupSenderTitles)) delete groupSenderTitles[key];
        for (const m of (detail.members || [])) {
            if (m.is_agent && m.title) {
                const senderKey = m.user_id + '#' + m.session_id;
                groupSenderTitles[senderKey] = m.title;
            }
        }

        renderGroupMessages(detail.messages || []);
        renderGroupMembers(detail.members || []);

        // Track last message ID
        if (detail.messages && detail.messages.length > 0) {
            groupLastMsgId = detail.messages[detail.messages.length - 1].id;
        }

        // Start polling for new messages
        startGroupPolling(groupId);

        // Load mute status
        await loadGroupMuteStatus(groupId);

        // Update group list selection
        loadGroupList();
    } catch (e) {
        console.error('Failed to open group:', e);
    }
}

function groupBackToList() {
    document.getElementById('page-group').classList.remove('mobile-chat-open');
    // Close member panel if open
    if (groupMemberPanelOpen) toggleGroupMemberPanel();
}

function renderGroupMessages(messages) {
    const box = document.getElementById('group-messages-box');
    if (messages.length === 0) {
        box.innerHTML = '<div style="text-align:center;color:#9ca3af;padding:40px 0;font-size:13px;">暂无消息</div>';
        return;
    }
    box.innerHTML = messages.map(m => {
        const isSelf = m.sender === currentUserId || m.sender === currentUserId;
        const isAgent = !isSelf && m.sender_session;
        const msgClass = isSelf ? 'self' : (isAgent ? 'agent' : 'other');
        const displayName = isAgent ? getGroupSenderTitle(m.sender) : m.sender;
        const timeStr = new Date(m.timestamp * 1000).toLocaleTimeString(currentLang === 'zh-CN' ? 'zh-CN' : 'en-US', {hour:'2-digit',minute:'2-digit'});
        return `
            <div class="group-msg ${msgClass}" ${isAgent ? 'data-agent-sender="'+escapeHtml(m.sender)+'"' : ''}>
                <div class="group-msg-sender">${escapeHtml(displayName)}</div>
                <div class="group-msg-content markdown-body">${marked.parse(m.content || '')}</div>
                <div class="group-msg-time">${timeStr}</div>
            </div>`;
    }).join('');
    box.querySelectorAll('pre code').forEach((block) => hljs.highlightElement(block));
    box.querySelectorAll('.group-msg.agent[data-agent-sender]').forEach(el => applyAgentColor(el, el.dataset.agentSender));
    box.scrollTop = box.scrollHeight;
}

function appendGroupMessages(messages) {
    const box = document.getElementById('group-messages-box');
    // Remove "no messages" placeholder if present
    const placeholder = box.querySelector('div[style*="text-align:center"]');
    if (placeholder && messages.length > 0) placeholder.remove();

    for (const m of messages) {
        const isSelf = m.sender === currentUserId || m.sender === currentUserId;
        const isAgent = !isSelf && m.sender_session;
        const msgClass = isSelf ? 'self' : (isAgent ? 'agent' : 'other');
        const displayName = isAgent ? getGroupSenderTitle(m.sender) : m.sender;
        const timeStr = new Date(m.timestamp * 1000).toLocaleTimeString(currentLang === 'zh-CN' ? 'zh-CN' : 'en-US', {hour:'2-digit',minute:'2-digit'});
        const div = document.createElement('div');
        div.className = `group-msg ${msgClass}`;
        div.innerHTML = `
            <div class="group-msg-sender">${escapeHtml(displayName)}</div>
            <div class="group-msg-content markdown-body">${marked.parse(m.content || '')}</div>
            <div class="group-msg-time">${timeStr}</div>`;
        div.querySelectorAll('pre code').forEach((block) => hljs.highlightElement(block));
        if (isAgent) applyAgentColor(div, m.sender);
        box.appendChild(div);
        if (m.id > groupLastMsgId) groupLastMsgId = m.id;
    }
    box.scrollTop = box.scrollHeight;
}

function startGroupPolling(groupId) {
    stopGroupPolling();
    groupPollingTimer = setInterval(async () => {
        if (currentGroupId !== groupId || currentPage !== 'group') {
            stopGroupPolling();
            return;
        }
        try {
            const resp = await fetch(`/proxy_groups/${groupId}/messages?after_id=${groupLastMsgId}`, {
                headers: { 'Authorization': 'Bearer ' + getAuthToken() }
            });
            if (!resp.ok) return;
            const data = await resp.json();
            if (data.messages && data.messages.length > 0) {
                appendGroupMessages(data.messages);
                // 有新消息时也刷新群列表（更新消息计数）
                loadGroupList();
            }
        } catch (e) {
            // silent
        }
    }, 5000);
}

async function sendGroupMessage() {
    const input = document.getElementById('group-input');
    const text = input.value.trim();
    if (!text || !currentGroupId) return;

    // 收集 mentions：从 mentionSelectedIds 中取出被 @ 的 agent
    const mentions = mentionSelectedIds.length > 0 ? [...mentionSelectedIds] : null;
    // 发送后清空 mention 选中状态
    mentionSelectedIds = [];
    hideMentionPopup();
    input.value = '';

    try {
        const body = { content: text };
        if (mentions) body.mentions = mentions;
        const resp = await fetch(`/proxy_groups/${currentGroupId}/messages`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getAuthToken()
            },
            body: JSON.stringify(body)
        });
        const result = await resp.json();
        const realId = result.id || (groupLastMsgId + 1);
        // Immediately show in UI with real server ID
        appendGroupMessages([{
            id: realId,
            sender: currentUserId,
            content: text,
            timestamp: Date.now() / 1000
        }]);
    } catch (e) {
        console.error('Failed to send group message:', e);
    }
}

function renderGroupMembers(members) {
    const container = document.getElementById('group-current-members');
    container.innerHTML = members.map(m => {
        const badge = m.is_agent
            ? `<span class="member-badge badge-agent">${t('group_agent')}</span>`
            : `<span class="member-badge badge-owner">${t('group_owner')}</span>`;
        let displayName = m.is_agent && m.title ? m.title : (m.user_id + (m.session_id !== 'default' ? '#' + m.session_id : ''));
        if (displayName.length > 7) displayName = displayName.slice(0, 7) + '…';
        return `
            <div class="member-item">
                <span class="member-name" title="${escapeHtml(m.user_id + '#' + m.session_id)}">${escapeHtml(displayName)}</span>
                ${badge}
            </div>`;
    }).join('');
}

let groupMemberPanelOpen = false;
function toggleGroupMemberPanel() {
    groupMemberPanelOpen = !groupMemberPanelOpen;
    document.getElementById('group-member-panel').style.display = groupMemberPanelOpen ? 'flex' : 'none';
    if (groupMemberPanelOpen && currentGroupId) {
        loadAvailableSessions();
    }
}

async function loadAvailableSessions() {
    const container = document.getElementById('group-available-sessions');
    container.innerHTML = '<div class="text-xs text-gray-400 p-2">' + t('loading') + '</div>';
    try {
        const resp = await fetch(`/proxy_groups/${currentGroupId}/sessions`, {
            headers: { 'Authorization': 'Bearer ' + getAuthToken() }
        });
        if (!resp.ok) return;
        const data = await resp.json();
        const sessions = data.sessions || [];

        // Get current members to mark them
        const detailResp = await fetch(`/proxy_groups/${currentGroupId}`, {
            headers: { 'Authorization': 'Bearer ' + getAuthToken() }
        });
        const detail = await detailResp.json();
        const memberSet = new Set((detail.members || []).map(m => m.user_id + '#' + m.session_id));

        if (sessions.length === 0) {
            container.innerHTML = '<div class="text-xs text-gray-400 p-2">' + t('group_no_sessions') + '</div>';
            return;
        }

        container.innerHTML = sessions.map(s => {
            const key = currentUserId + '#' + s.session_id;
            const checked = memberSet.has(key) ? 'checked' : '';
            const title = s.title || s.session_id;
            return `
                <label class="session-checkbox">
                    <input type="checkbox" ${checked} onchange="toggleGroupAgent('${s.session_id}', this.checked)">
                    <span class="session-label" title="${escapeHtml(title)}">${escapeHtml(title)}</span>
                </label>`;
        }).join('');
    } catch (e) {
        container.innerHTML = '<div class="text-xs text-red-400 p-2">加载失败</div>';
    }
}

async function toggleGroupAgent(sessionId, add) {
    if (!currentGroupId) return;
    try {
        await fetch(`/proxy_groups/${currentGroupId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getAuthToken()
            },
            body: JSON.stringify({
                members: [{
                    user_id: currentUserId,
                    session_id: sessionId,
                    action: add ? 'add' : 'remove'
                }]
            })
        });
        // Refresh member list
        const resp = await fetch(`/proxy_groups/${currentGroupId}`, {
            headers: { 'Authorization': 'Bearer ' + getAuthToken() }
        });
        const detail = await resp.json();
        renderGroupMembers(detail.members || []);
    } catch (e) {
        console.error('Failed to toggle group agent:', e);
    }
}

function showCreateGroupModal() {
    // 用自定义弹窗替代 prompt()，兼容移动端
    let overlay = document.getElementById('group-create-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'group-create-overlay';
        overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.4);z-index:300;display:flex;align-items:center;justify-content:center;';
        overlay.innerHTML = `
            <div style="background:white;border-radius:12px;padding:20px;width:90%;max-width:320px;box-shadow:0 10px 40px rgba(0,0,0,0.2);">
                <div style="font-size:14px;font-weight:600;color:#374151;margin-bottom:12px;" data-i18n="group_create_title">${t('group_create_title')}</div>
                <input id="group-create-name-input" type="text" placeholder="${t('group_name_placeholder')}" data-i18n-placeholder="group_name_placeholder"
                    style="width:100%;box-sizing:border-box;padding:8px 12px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;outline:none;" />
                <div style="display:flex;gap:8px;margin-top:14px;justify-content:flex-end;">
                    <button onclick="closeCreateGroupModal()" style="padding:6px 16px;border-radius:8px;border:1px solid #d1d5db;background:white;font-size:13px;cursor:pointer;color:#6b7280;">取消</button>
                    <button onclick="submitCreateGroup()" style="padding:6px 16px;border-radius:8px;border:none;background:#2563eb;color:white;font-size:13px;font-weight:600;cursor:pointer;">${t('group_create_btn')}</button>
                </div>
            </div>`;
        document.body.appendChild(overlay);
        // Enter to submit
        document.getElementById('group-create-name-input').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') { e.preventDefault(); submitCreateGroup(); }
        });
    } else {
        overlay.style.display = 'flex';
    }
    const input = document.getElementById('group-create-name-input');
    input.value = '';
    setTimeout(() => input.focus(), 100);
}

function closeCreateGroupModal() {
    const overlay = document.getElementById('group-create-overlay');
    if (overlay) overlay.style.display = 'none';
}

function submitCreateGroup() {
    const input = document.getElementById('group-create-name-input');
    const name = (input.value || '').trim();
    if (!name) return;
    closeCreateGroupModal();
    createGroup(name);
}

async function createGroup(name) {
    try {
        const resp = await fetch('/proxy_groups', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getAuthToken()
            },
            body: JSON.stringify({ name: name, members: [] })
        });
        if (!resp.ok) { alert('创建失败'); return; }
        const data = await resp.json();
        await loadGroupList();
        openGroup(data.group_id);
    } catch (e) {
        alert('创建失败: ' + e.message);
    }
}

async function deleteGroup(groupId) {
    if (!confirm(t('group_delete_confirm'))) return;
    try {
        await fetch(`/proxy_groups/${groupId}`, {
            method: 'DELETE',
            headers: { 'Authorization': 'Bearer ' + getAuthToken() }
        });
        if (currentGroupId === groupId) {
            currentGroupId = null;
            document.getElementById('group-active-chat').style.display = 'none';
            document.getElementById('group-empty-placeholder').style.display = 'flex';
            document.getElementById('page-group').classList.remove('mobile-chat-open');
            stopGroupPolling();
        }
        loadGroupList();
    } catch (e) {
        alert('删除失败: ' + e.message);
    }
}

function updateMuteButton() {
    const btn = document.getElementById('group-mute-btn');
    if (!btn) return;
    if (groupMuted) {
        btn.textContent = t('group_unmute');
        btn.style.background = '#f0fdf4';
        btn.style.color = '#16a34a';
        btn.style.borderColor = '#bbf7d0';
    } else {
        btn.textContent = t('group_mute');
        btn.style.background = '#fef2f2';
        btn.style.color = '#dc2626';
        btn.style.borderColor = '#fecaca';
    }
}

async function loadGroupMuteStatus(groupId) {
    try {
        const resp = await fetch(`/proxy_groups/${groupId}/mute_status`, {
            headers: { 'Authorization': 'Bearer ' + getAuthToken() }
        });
        if (resp.ok) {
            const data = await resp.json();
            groupMuted = data.muted;
            updateMuteButton();
        }
    } catch (e) { console.error('Failed to load mute status:', e); }
}

async function toggleGroupMute() {
    if (!currentGroupId) return;
    const action = groupMuted ? 'unmute' : 'mute';
    try {
        const resp = await fetch(`/proxy_groups/${currentGroupId}/${action}`, {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + getAuthToken() }
        });
        if (resp.ok) {
            groupMuted = !groupMuted;
            updateMuteButton();
        }
    } catch (e) { console.error('Failed to toggle mute:', e); }
}
