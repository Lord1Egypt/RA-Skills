// =====================================================================
// AI 智能客服 - 国际化字典（IM 气泡风格 + 手动评分）
// =====================================================================
(function () {
    const DICT = {
        zh: {
            appName: 'AI 电商客服',
            langSwitch: 'EN',

            // 配置
            collapseConfig: '收起配置',
            expandConfig: '展开配置',
            config: '基础设置',
            sectionLanguage: '语言',
            sectionMode: '对话模式',
            modeVoice: '语音',
            modeAvatar: '数智人',
            modeAvatarDisabled: '数智人 (未配置)',
            sectionTurnMode: '断句模式',
            turnSemantic: '语义断句',
            turnVad: '普通断句',
            sectionInterrupt: '打断模式',
            interruptSmart: '智能打断',
            interruptManual: '手动打断',
            configMore: '其他设置',
            sectionStt: '语音识别引擎',
            sectionVadLevel: '远场人声抑制等级',
            tipVadLevel: '远场人声抑制等级用于控制远场人声抑制能力，等级越高远场人声抑制能力越强，注意较高等级可能会将单字当作噪声过滤。',
            sectionVadSilenceTime: 'VAD 时长 (ms)',
            tipVadSilenceTime: 'VAD 时长用于控制 AI 在用户说话时的响应速度，数值越小反应越快，越大越避免 AI 抢话。',
            sectionInterruptDuration: '打断时长 (ms)',
            tipInterruptDuration: '打断时长用于控制智能打断模式下 AI 被打断的灵敏度，数值越小越灵敏，越大越避免误打断。',
            tipInterruptDurationOnlySmart: '* 仅"智能打断"模式生效',
            sliderFaster: '更快',
            sliderSlower: '更慢',
            sliderWeaker: '更弱',
            sliderStronger: '更强',
            sliderSensitive: '更灵敏',
            sliderStable: '更稳定',
            btnMute: '静音',
            btnUnmute: '取消静音',

            // 客服选择
            sectionAgentSelect: '请选择客服',
            agentFemaleName: '客服 001 号',
            agentMaleName: '客服 002 号',
            btnStart: '开始对话',

            // 对话状态
            tipConnecting: '正在连接...',
            tipConnected: '已连接',
            tipEnterRoomFailed: '进房失败，请检查网络与权限',
            tipMicrophoneFailed: '麦克风启动失败，请允许麦克风权限',
            tipAIStartFailed: '启动 AI 客服失败：',
            tipSdkLoadFailed: 'TRTC SDK 加载失败',

            // AI 状态
            statusOffline: '未连接',
            statusConnecting: '连接中',
            statusListening: '聆听中',
            statusThinking: '思考中',
            statusSpeaking: '说话中',
            statusInterrupted: '已打断',
            statusFinished: '已结束',

            // 气泡与输入
            welcomePlaceholder: '你好！有什么我可以帮您的吗？',
            typing: '正在输入',
            btnInterrupt: '点击打断',
            inputPlaceholder: '请输入文字与 AI 客服交流...',
            inputVoiceHint: '🎤 语音对话中，或点击键盘图标切换文字输入',
            btnEnd: '结束',
            btnSend: '发送',
            btnVoiceMode: '语音',
            btnKeyboardMode: '文字',

            // 手动评分弹窗
            ratingTitle: '请为本次服务评分',
            ratingSubtitle: '您的反馈将帮助我们改进服务质量',
            ratingScoreHint: '（0 最差，10 最优）',
            ratingDimOverall: '整体满意度',
            ratingDimResolution: '问题解决度',
            ratingDimProfessionalism: '响应专业性',
            ratingDimFriendliness: '沟通友好度',
            ratingBtnSkip: '跳过',
            ratingBtnSubmit: '提交评分',
            ratingThanks: '感谢您的评价！',
            ratingThanksDesc: '您的 {overall} 分反馈已收到',
            ratingBtnRestart: '再次咨询',
            ratingBtnClose: '关闭',

            // 角色
            roleAgent: 'AI 客服',
            roleUser: '我',

            // 电商功能
            btnOrders: '订单',
            orderPanelTitle: '选择订单',
            orderSend: '发送',
            orderStatus_pending: '待发货',
            orderStatus_shipped: '运输中',
            orderStatus_delivered: '已签收',
            orderStatus_refunding: '退款中',
            btnTransfer: '转人工',
            transferTitle: '转接人工客服',
            transferDesc: '已加入人工客服排队（演示模式，生产环境请对接客服路由系统）。',
            transferBtnBack: '返回首页',
        },
        en: {
            appName: 'AI E-Commerce Service',
            langSwitch: '中',

            collapseConfig: 'Collapse',
            expandConfig: 'Expand',
            config: 'Basic Settings',
            sectionLanguage: 'Language',
            sectionMode: 'Mode',
            modeVoice: 'Audio',
            modeAvatar: 'Avatar',
            modeAvatarDisabled: 'Avatar (Disabled)',
            sectionTurnMode: 'Segmentation Mode',
            turnSemantic: 'Semantic',
            turnVad: 'VAD',
            sectionInterrupt: 'Interrupt Mode',
            interruptSmart: 'Intelligent',
            interruptManual: 'Manual',
            configMore: 'Advanced',
            sectionStt: 'ASR Engine',
            sectionVadLevel: 'Far-field Suppression',
            tipVadLevel: 'Controls far-field voice suppression. Higher levels provide stronger suppression, but may filter out single-word utterances as noise.',
            sectionVadSilenceTime: 'VAD Duration (ms)',
            tipVadSilenceTime: "VAD duration controls the AI's response speed when you speak. Smaller values mean faster responses, while larger values prevent the AI from interrupting.",
            sectionInterruptDuration: 'Interruption Duration (ms)',
            tipInterruptDuration: 'Interruption duration controls AI sensitivity in intelligent interruption mode. Smaller values increase sensitivity, while larger values reduce false interruptions.',
            tipInterruptDurationOnlySmart: '* Only effective in "Intelligent" mode',
            sliderFaster: 'Faster',
            sliderSlower: 'Slower',
            sliderWeaker: 'Weaker',
            sliderStronger: 'Stronger',
            sliderSensitive: 'Sensitive',
            sliderStable: 'Stable',
            btnMute: 'Mute',
            btnUnmute: 'Unmute',

            sectionAgentSelect: 'Choose Your Agent',
            agentFemaleName: 'Agent 001',
            agentMaleName: 'Agent 002',
            btnStart: 'Start Chat',

            tipConnecting: 'Connecting...',
            tipConnected: 'Connected',
            tipEnterRoomFailed: 'Failed to enter room.',
            tipMicrophoneFailed: 'Microphone failed. Allow mic permission.',
            tipAIStartFailed: 'Failed to start AI: ',
            tipSdkLoadFailed: 'TRTC SDK load failed',

            statusOffline: 'Offline',
            statusConnecting: 'Connecting',
            statusListening: 'Listening',
            statusThinking: 'Thinking',
            statusSpeaking: 'Speaking',
            statusInterrupted: 'Interrupted',
            statusFinished: 'Finished',

            welcomePlaceholder: "Hi! How can I help you today?",
            typing: 'typing',
            btnInterrupt: 'Click to interrupt',
            inputPlaceholder: 'Type to chat with AI agent...',
            inputVoiceHint: '🎤 Voice chat active, or click keyboard icon to type',
            btnEnd: 'End',
            btnSend: 'Send',
            btnVoiceMode: 'Voice',
            btnKeyboardMode: 'Text',

            ratingTitle: 'Please Rate This Service',
            ratingSubtitle: 'Your feedback helps us improve',
            ratingScoreHint: '(0 worst, 10 best)',
            ratingDimOverall: 'Overall Satisfaction',
            ratingDimResolution: 'Resolution',
            ratingDimProfessionalism: 'Professionalism',
            ratingDimFriendliness: 'Friendliness',
            ratingBtnSkip: 'Skip',
            ratingBtnSubmit: 'Submit',
            ratingThanks: 'Thank you for your feedback!',
            ratingThanksDesc: 'Your rating of {overall}/10 has been received',
            ratingBtnRestart: 'New Chat',
            ratingBtnClose: 'Close',

            roleAgent: 'AI Agent',
            roleUser: 'You',

            btnOrders: 'Orders',
            orderPanelTitle: 'Select Order',
            orderSend: 'Send',
            orderStatus_pending: 'Pending',
            orderStatus_shipped: 'Shipped',
            orderStatus_delivered: 'Delivered',
            orderStatus_refunding: 'Refunding',
            btnTransfer: 'Agent',
            transferTitle: 'Transfer to Human Agent',
            transferDesc: 'Added to queue (demo mode — connect to your agent routing system in production).',
            transferBtnBack: 'Back to Home',
        },
        yue: {
            appName: 'AI 電商客服',
            langSwitch: '粤',

            collapseConfig: '收起配置',
            expandConfig: '展開配置',
            config: '基礎設置',
            sectionMode: '對話模式',
            modeVoice: '語音',
            modeAvatar: '數智人',
            modeAvatarDisabled: '數智人 (未配置)',
            sectionTurnMode: '斷句模式',
            turnSemantic: '語義斷句',
            turnVad: '普通斷句',
            sectionInterrupt: '打斷模式',
            interruptSmart: '智能打斷',
            interruptManual: '手動打斷',
            configMore: '其他設置',
            sectionVadLevel: '遠場人聲抑制等級',
            tipVadLevel: '遠場人聲抑制等級用於控制遠場人聲抑制能力，等級越高遠場人聲抑制能力越強，注意較高等級可能會將單字當作噪聲過濾。',
            sectionVadSilenceTime: 'VAD 時長 (ms)',
            tipVadSilenceTime: 'VAD 時長用於控制 AI 喺用戶講嘢時嘅響應速度，數值越小反應越快，越大越避免 AI 搶話。',
            sectionInterruptDuration: '打斷時長 (ms)',
            tipInterruptDuration: '打斷時長用於控制智能打斷模式下 AI 被打斷嘅靈敏度，數值越小越靈敏，越大越避免誤打斷。',
            tipInterruptDurationOnlySmart: '* 僅「智能打斷」模式生效',
            sliderFaster: '更快',
            sliderSlower: '更慢',
            sliderWeaker: '更弱',
            sliderStronger: '更強',
            sliderSensitive: '更靈敏',
            sliderStable: '更穩定',
            btnMute: '靜音',
            btnUnmute: '取消靜音',

            sectionAgentSelect: '請選擇客服',
            agentFemaleName: '客服 001 號',
            agentMaleName: '客服 002 號',
            btnStart: '開始對話',

            tipConnecting: '正在連接...',
            tipConnected: '已連接',
            tipEnterRoomFailed: '進房失敗，請檢查網絡與權限',
            tipMicrophoneFailed: '麥克風啟動失敗，請允許麥克風權限',
            tipAIStartFailed: '啟動 AI 客服失敗：',
            tipSdkLoadFailed: 'TRTC SDK 加載失敗',

            statusOffline: '未連接',
            statusConnecting: '連接中',
            statusListening: '聆聽中',
            statusThinking: '思考中',
            statusSpeaking: '講緊嘢',
            statusInterrupted: '已打斷',
            statusFinished: '已結束',

            welcomePlaceholder: '你好！有咩可以幫到您？',
            typing: '正在輸入',
            btnInterrupt: '點擊打斷',
            inputPlaceholder: '請輸入文字與 AI 客服交流...',
            inputVoiceHint: '🎤 語音對話中，或點擊鍵盤圖標切換文字輸入',
            btnEnd: '結束',
            btnSend: '發送',
            btnVoiceMode: '語音',
            btnKeyboardMode: '文字',

            ratingTitle: '請為本次服務評分',
            ratingSubtitle: '您嘅反饋將幫助我哋改進服務質量',
            ratingScoreHint: '（0 最差，10 最優）',
            ratingDimOverall: '整體滿意度',
            ratingDimResolution: '問題解決度',
            ratingDimProfessionalism: '響應專業性',
            ratingDimFriendliness: '溝通友好度',
            ratingBtnSkip: '跳過',
            ratingBtnSubmit: '提交評分',
            ratingThanks: '多謝您嘅評價！',
            ratingThanksDesc: '您嘅 {overall} 分反饋已收到',
            ratingBtnRestart: '再次諮詢',
            ratingBtnClose: '關閉',

            roleAgent: 'AI 客服',
            roleUser: '我',

            btnOrders: '訂單',
            orderPanelTitle: '選擇訂單',
            orderSend: '發送',
            orderStatus_pending: '待發貨',
            orderStatus_shipped: '運輸中',
            orderStatus_delivered: '已簽收',
            orderStatus_refunding: '退款中',
            btnTransfer: '轉人工',
            transferTitle: '轉接人工客服',
            transferDesc: '已加入人工客服排隊（演示模式，生產環境請對接客服路由系統）。',
            transferBtnBack: '返回首頁',
        },
    };

    const STORAGE_KEY = 'cs_lang';
    let currentLang = (function () {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved && DICT[saved]) return saved;
        const browser = (navigator.language || 'zh').toLowerCase();
        return browser.startsWith('en') ? 'en' : 'zh';
    })();

    function t(key, params) {
        let text = (DICT[currentLang] && DICT[currentLang][key]) || key;
        if (params) {
            for (const k of Object.keys(params)) {
                text = text.replace('{' + k + '}', params[k]);
            }
        }
        return text;
    }
    function getLang() { return currentLang; }
    function setLang(lang) {
        if (!DICT[lang]) return;
        currentLang = lang;
        localStorage.setItem(STORAGE_KEY, lang);
        window.dispatchEvent(new CustomEvent('langChange', { detail: { lang } }));
    }
    const LANG_CYCLE = ['zh', 'yue', 'en'];
    function toggleLang() {
        const idx = LANG_CYCLE.indexOf(currentLang);
        setLang(LANG_CYCLE[(idx + 1) % LANG_CYCLE.length]);
    }

    window.I18N = { t, getLang, setLang, toggleLang, DICT };
    Object.defineProperty(window.I18N, 'currentLang', { get: () => currentLang });
})();
