# -*- coding: utf-8 -*-
"""
VBTI 16 型定义 + 信号 → 类型评分映射。
每个类型: name, emoji, tagline, code(编号), receipts(4 条: 标签/信号 key/后缀), scoring(信号 → 权重).
"""

TYPES = {
    "SOON": {
        "code": "01", "name": "大饼批发商", "emoji": "🥧",
        "tagline": "下周一定上线",
        "receipts": [
            ('"下周/明天/马上" 出现', "promise_words", "次"),
            ('带 "v2/final/重启" 的目录', "v2_dirs", "个"),
            ('最久"快好了"的项目', "oldest_promise_days", "天"),
            ("今年实际上线的项目", "launched_projects", "个"),
        ],
        "scoring": {"promise_words": 2.0, "v2_dirs": 1.5, "stale_cwds": 0.8},
    },
    "MONK": {
        "code": "02", "name": "赛博苦行", "emoji": "🧘",
        "tagline": "本地 N 个 cwd · git push 0 次",
        "receipts": [
            ("本地有效项目", "total_cwds", "个"),
            ("git push 总次数", "git_push", ""),
            ("gh repo create", "gh_repo_create_word", ""),
            ("最久未发布的项目", "oldest_cwd_days", "天"),
        ],
        "scoring": {"total_cwds": 0.4, "no_push_ratio": 3.0},
    },
    "SHOW": {
        "code": "03", "name": "橱窗工程师", "emoji": "🎭",
        "tagline": "能截图就行",
        "receipts": [
            ("HTML / CSS 改动占比", "html_pct", "%"),
            ("跑过的 API / 测试命令", "api_test_runs", "次"),
            ("项目里截图 / preview 文件", "screenshot_files", "张"),
            ('"封面/演示/发出去" 关键词', "show_words", "次"),
        ],
        "scoring": {"html_pct": 0.5, "show_words": 2.0, "screenshot_files": 1.0},
    },
    "VIBE": {
        "code": "04", "name": "氛围工程师", "emoji": "🌀",
        "tagline": "感觉很对就是跑不起来",
        "receipts": [
            ('"应该/可能/试试" 关键词', "vibe_words", "次"),
            ("报错后再跑一次的次数", "retry_after_error", "次"),
            ("不读报错直接复制给 AI", "error_dumps", "次"),
            ('"works on my machine" 自我安慰', "wfm_words", "次"),
        ],
        "scoring": {"vibe_words": 2.0, "error_dumps": 1.5},
    },
    "BLAM": {
        "code": "05", "name": "甩锅大师", "emoji": "🫵",
        "tagline": "你又写错了",
        "receipts": [
            ('"你又错了 / 不对 / 蠢" 出现', "blame_words", "次"),
            ("模型切换次数", "model_switches", "次"),
            ("AI 输出未读直接重发", "rapid_resends", "次"),
            ("自我反思消息数", "self_reflect", ""),
        ],
        "scoring": {"blame_words": 3.0, "model_switches": 1.0},
    },
    "YEET": {
        "code": "06", "name": "删库飞人", "emoji": "💣",
        "tagline": "凌晨三点 rm -rf",
        "receipts": [
            ("`rm -rf` 命令数", "rm_rf", "次"),
            ("`git reset --hard` 次数", "git_reset_hard", "次"),
            ("凌晨破坏性操作占比", "night_destruct_pct", "%"),
            ("第二天重新 git init", "git_init", "次"),
        ],
        "scoring": {"rm_rf": 3.0, "git_reset_hard": 2.0, "git_init": 1.5},
    },
    "GHST": {
        "code": "07", "name": "凌晨幽魂", "emoji": "👻",
        "tagline": "灵感寿命 6 小时",
        "receipts": [
            ("0-5 点 session 占比", "night_msgs_pct", "%"),
            ("新建项目寿命中位数", "cwd_median_hours", "小时"),
            ("凌晨开的新文件夹", "night_new_cwds", "个"),
            ("早 9 点的羞耻删除", "morning_deletes", "次"),
        ],
        "scoring": {"night_msgs_pct": 0.08, "night_new_cwds": 1.5},
    },
    "LOOP": {
        "code": "08", "name": "重构教主", "emoji": "🔁",
        "tagline": "第八次推倒重来",
        "receipts": [
            ('"重构/重写/refactor" 出现', "refactor_words", "次"),
            ("单文件最高 Edit 次数", "max_edits_one_file", "次"),
            ("main 分支最近 commit", "days_since_main_commit", "天前"),
            ("实际新增功能", "new_features", "个"),
        ],
        "scoring": {"refactor_words": 2.5, "max_edits_one_file": 0.5},
    },
    "MOSS": {
        "code": "09", "name": "长草老登", "emoji": "🌿",
        "tagline": "README 比代码勤",
        "receipts": [
            (".md 文件 Edit 次数", "md_edits", "次"),
            ("代码文件 Edit 次数", "code_edits", "次"),
            ("最近代码改动距今", "days_since_code", "天"),
            ("README 改版", "readme_versions", "版"),
        ],
        "scoring": {"md_ratio": 4.0, "md_edits": 0.3},
    },
    "SORY": {
        "code": "10", "name": "道歉精", "emoji": "🙇",
        "tagline": "对 AI 比对自己客气",
        "receipts": [
            ('"谢谢" 出现次数', "thanks_words", "次"),
            ('"对不起/是我没说清"', "sorry_words", "次"),
            ("同 prompt 自责后重发", "retry_after_apology", "次"),
            ("上次主动 push back", "pushback", ""),
        ],
        "scoring": {"thanks_words": 1.5, "sorry_words": 2.5},
    },
    "NODE": {
        "code": "11", "name": "全自动 yes 党", "emoji": "✅",
        "tagline": '"ok 继续" 按了 N 次',
        "receipts": [
            ('≤3 字回复 ("ok/好/继续") 占比', "short_msg_pct", "%"),
            ("不读 plan 直接同意", "ok_words", "次"),
            ("平均用户消息字数", "avg_msg_len", "字"),
            ("主动验证 AI 输出的次数", "verify_runs", "次"),
        ],
        "scoring": {"short_msg_pct": 0.1, "ok_words": 1.5},
    },
    "DUMP": {
        "code": "12", "name": "报错投掷手", "emoji": "🗑️",
        "tagline": "这是什么错",
        "receipts": [
            ("整段 traceback 糊脸次数", "traceback_dumps", "次"),
            ("贴入错误信息中位字数", "median_error_len", "字"),
            ("用户解释报错的字数", "user_explain_error", "字"),
            ("先 google 再问 AI 的次数", "google_first", ""),
        ],
        "scoring": {"traceback_dumps": 3.0, "median_error_len": 0.005},
    },
    "TOYS": {
        "code": "13", "name": "工具试色师", "emoji": "🧸",
        "tagline": "这库比那个好吗",
        "receipts": [
            ('"X 比 Y 好/推荐" 类问句', "compare_words", "次"),
            ("装过用过 < 1 天的库", "abandoned_packages", "个"),
            ("同需求换框架次数", "framework_switches", "次"),
            ("用过超过一周的库", "kept_packages", "个"),
        ],
        "scoring": {"compare_words": 2.5, "npm_install": 0.3},
    },
    "TIDY": {
        "code": "14", "name": "格式洁癖家", "emoji": "🎨",
        "tagline": "改个变量名",
        "receipts": [
            ("重命名 / 格式化 Edit 占比", "rename_pct", "%"),
            ("真正改逻辑的 Edit 占比", "logic_pct", "%"),
            ('"再优化一下名字" 类消息', "rename_words", "次"),
            ("prettier / black 跑动次数", "formatter_runs", "次"),
        ],
        "scoring": {"rename_words": 2.5, "rename_pct": 0.1},
    },
    "LERN": {
        "code": "15", "name": "解释依赖症", "emoji": "🎓",
        "tagline": "你能解释下吗",
        "receipts": [
            ('"为什么/怎么实现/原理"', "explain_words", "次"),
            ("让 AI 解释自己刚写的代码", "self_explain", "次"),
            ("解释完没改任何东西", "explain_no_change_pct", "%"),
            ("主动看完文档的次数", "doc_reads", ""),
        ],
        "scoring": {"explain_words": 2.5},
    },
    "TEST": {
        "code": "16", "name": "测试绝缘体", "emoji": "🧪",
        "tagline": "没测过应该没事",
        "receipts": [
            ("*test* / *spec* 文件数", "test_files", ""),
            ("跑过 pytest / jest / vitest", "test_runs", "次"),
            ('"应该能跑/不用测了"', "no_test_words", "次"),
            ("上线后被同事骂", "shipped_bugs", "次"),
        ],
        "scoring": {"no_test_bonus": 3.0, "no_test_words": 2.0},
    },
}
