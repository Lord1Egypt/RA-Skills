# dict_01_residential_core.py
RESIDENTIAL_CORE = {
    "智慧客厅": {
        "description": "家庭起居与社交的核心枢纽",
        "hardware_matrix": [
            {"element": "光", "process": "交互", "name": "多模态触控全面屏 (集成温控/调光/场景)"},
            {"element": "光", "process": "执行", "name": "DALI/无极调光调色 LED 驱动器 (主照明/防眩光)"},
            {"element": "光", "process": "执行", "name": "超静音开合帘电机 + 纱帘电机 (双轨双层)"},
            {"element": "光", "process": "执行", "name": "RGBW 幻彩灯带控制器 (洗墙/氛围)"},
            {"element": "气", "process": "感知", "name": "五合一空气质量雷达 (温湿度/PM2.5/TVOC/CO2)"},
            {"element": "气", "process": "执行", "name": "VRV 中央空调/地暖/新风底层协议网关"},
            {"element": "声", "process": "交互/感知", "name": "远场拾音阵列 (唤醒/异常声纹抓取)"},
            {"element": "声", "process": "执行", "name": "高保真全景声吸顶音箱系统 (背景音乐/家庭影院)"},
            {"element": "电磁", "process": "感知", "name": "24GHz/77GHz 毫米波人体存在传感器 (防静坐误判)"},
            {"element": "能", "process": "感知/执行", "name": "带功率计量的智能墙壁插座 (落地灯/加湿器)"},
            {"element": "视", "process": "感知/交互", "name": "3D人脸/指静脉入户智能门锁 (玄关过渡区)"},
            {"element": "视", "process": "执行", "name": "激光电视联动升降台/智能画框幕布"}
        ],
        "default_scenarios": ["回家模式", "离家模式", "会客模式", "观影模式 (沉浸)", "休闲放松 (白噪音+暗光)"]
    },
    "智能厨房": {
        "description": "极具烟火气的高危监控与自动化烹饪空间",
        "hardware_matrix": [
            {"element": "光", "process": "感知/执行", "name": "橱柜手扫/人体感应操作台局部照明"},
            {"element": "光", "process": "执行", "name": "高显色指数 (CRI>95) 烹饪主灯"},
            {"element": "气", "process": "感知", "name": "工业级可燃气体泄漏探测器 (甲烷/丙烷)"},
            {"element": "气", "process": "感知", "name": "光电式烟雾/火灾报警器"},
            {"element": "气", "process": "感知", "name": "地面暗装水浸传感器 (水槽下侧)"},
            {"element": "气", "process": "执行", "name": "燃气/水管机械机械手 (泄漏自动切断阀)"},
            {"element": "气", "process": "执行", "name": "自动推窗器/油烟机联动模块 (强制通风)"},
            {"element": "声", "process": "交互", "name": "防油污声学语音控制面板 (烹饪时免接触)"},
            {"element": "能", "process": "执行", "name": "16A 大功率智能插座 (烤箱/微波炉等)"},
            {"element": "能", "process": "感知/执行", "name": "冰箱专属不间断智能微断 (防跳闸)"}
        ],
        "default_scenarios": ["烹饪模式 (高亮+排风)", "备餐模式", "安全防御模式 (水电气全天候熔断监测)"]
    },
    "智能卧室": {
        "description": "绝对隐私、深度疗愈与生理数据监测的休憩空间",
        "hardware_matrix": [
            {"element": "光", "process": "交互", "name": "床头双控 OLED 场景面板 (低亮防眩晕)"},
            {"element": "光", "process": "执行", "name": "低色温 (2700K) 褪黑素助眠主灯驱动"},
            {"element": "光", "process": "感知/执行", "name": "床底/地脚起夜柔光灯带 (防伴侣干扰)"},
            {"element": "光", "process": "执行", "name": "100% 全遮光智能卷帘/开合帘电机"},
            {"element": "气", "process": "感知/执行", "name": "睡眠级静音新风控制器 (依 CO2 浓度自适应)"},
            {"element": "气", "process": "执行", "name": "卧室独立分区恒温恒湿空调面板"},
            {"element": "声", "process": "执行", "name": "助眠白噪音/舒缓音乐背景音箱"},
            {"element": "声", "process": "感知", "name": "打鼾/咳嗽声纹特征采集器 (本地脱敏)"},
            {"element": "电磁", "process": "感知", "name": "非接触式睡眠监测毫米波雷达 (心率/呼吸/翻身)"},
            {"element": "能", "process": "计算", "name": "隐私断网物理开关 (一键物理屏蔽云端上传)"}
        ],
        "default_scenarios": ["晨起唤醒 (节律光+轻音乐)", "深度睡眠模式 (全屋静默+落锁)", "睡前阅读模式", "浪漫氛围模式", "起夜模式"]
    },
    "智能卫生间": {
        "description": "高湿度环境下的无感交互与健康监测区",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "防雾智能魔镜 (触控显示+去雾+健康数据)"},
            {"element": "光", "process": "感知/执行", "name": "IP65 级防水防眩光筒灯/射灯"},
            {"element": "气", "process": "感知", "name": "异味/氨气/TVOC/高湿度传感器"},
            {"element": "气", "process": "执行", "name": "智能排气扇/风暖浴霸联动控制器"},
            {"element": "气", "process": "感知", "name": "暗管/马桶旁水浸探测器"},
            {"element": "声", "process": "执行", "name": "防水吸顶音箱 (蓝牙/Wi-Fi 直连)"},
            {"element": "电磁", "process": "感知", "name": "顶装跌倒检测毫米波雷达 (保护老人隐私，不使用摄像头)"},
            {"element": "能", "process": "执行", "name": "智能马桶防漏电保护专用插座"}
        ],
        "default_scenarios": ["如厕模式 (换气+轻柔光)", "沐浴模式 (暖风+音乐+高亮)", "起夜模式 (极暗微光导引)", "无人排湿模式"]
    },
    "智能儿童房": {
        "description": "伴随儿童成长、强调护眼与安全的弹性空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "全光谱 (Ra>98) 无频闪防蓝光主照明灯"},
            {"element": "光", "process": "执行", "name": "书桌区域智能读写台灯 (照度自适应联动)"},
            {"element": "光", "process": "交互", "name": "防误触童锁智能面板"},
            {"element": "气", "process": "感知", "name": "甲醛/TVOC/温湿度高敏环境雷达"},
            {"element": "气", "process": "执行", "name": "防直吹空调导风板联动模块"},
            {"element": "声", "process": "交互/执行", "name": "儿童专属唤醒词语音助手/睡前故事播放器"},
            {"element": "电磁", "process": "感知", "name": "防坠床/爬窗毫米波雷达围栏"},
            {"element": "能", "process": "执行", "name": "防触电安全保护智能插座 (超时自动断电)"},
            {"element": "视", "process": "感知", "name": "AI 守护摄像头 (仅限婴儿期，长大后物理遮挡)"}
        ],
        "default_scenarios": ["学习模式 (高照度冷白光)", "玩耍模式 (活力暖光)", "睡眠安抚模式", "防踢被监控预警"]
    },
    "智能餐厅": {
        "description": "就餐氛围营造与家庭交流的聚合点",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "餐桌核心区高显色吊灯调光驱动 (让食物色彩更佳)"},
            {"element": "光", "process": "执行", "name": "餐边柜/酒柜氛围灯带联动模块"},
            {"element": "气", "process": "执行", "name": "独立送回风新风调节口"},
            {"element": "声", "process": "执行", "name": "就餐背景音乐扬声器 (轻音乐)"},
            {"element": "电磁", "process": "感知", "name": "红外/微波人体传感器 (入座即亮)"},
            {"element": "能", "process": "执行", "name": "轨道插座/餐桌底部地插智能控制"}
        ],
        "default_scenarios": ["温馨就餐模式", "生日派对模式", "烛光晚餐模式", "清扫模式"]
    },
    "智能书房": {
        "description": "高度沉浸、无干扰的专注与办公空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "5000K-6000K 高效办公冷白光照明"},
            {"element": "光", "process": "执行", "name": "日照补偿智能窗帘 (防屏幕反光自适应)"},
            {"element": "气", "process": "感知/执行", "name": "高敏 CO2 探测器与新风联动 (防大脑缺氧)"},
            {"element": "声", "process": "感知/执行", "name": "环境噪音感知与白噪音主动掩蔽系统"},
            {"element": "电磁", "process": "感知", "name": "静坐微动检测雷达 (保持阅读时灯光常亮)"},
            {"element": "能", "process": "执行", "name": "电脑设备/网络设备专属 UPS 或防涌插排"}
        ],
        "default_scenarios": ["深度专注模式", "阅读模式", "视频会议模式", "游戏电竞模式"]
    },
    "智能浴室": {
        "description": "独立于卫生间的洗浴疗愈空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "IP65 级防水幻彩氛围灯 (色彩疗法)"},
            {"element": "气", "process": "执行", "name": "大功率快速排湿排气系统"},
            {"element": "气", "process": "感知", "name": "防溢水智能地漏传感器"},
            {"element": "声", "process": "执行", "name": "防水骨传导/水下音箱共振系统"},
            {"element": "电磁", "process": "感知", "name": "浴缸内防溺水/生命体征监测雷达"}
        ],
        "default_scenarios": ["泡澡疗愈模式", "极速淋浴模式", "高温排湿模式"]
    },
    "智能衣帽间": {
        "description": "服饰收纳与穿搭准备的辅助空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "高显色指数层板灯/衣通灯 (入内渐亮)"},
            {"element": "光", "process": "执行", "name": "试衣镜前无影美颜灯驱动"},
            {"element": "气", "process": "感知/执行", "name": "防霉防潮智能除湿机联动模块"},
            {"element": "气", "process": "执行", "name": "衣物护理机/智能衣柜控制网关"},
            {"element": "电磁", "process": "感知", "name": "红外感应/门磁 (开门即亮灯)"}
        ],
        "default_scenarios": ["选衣模式", "长效防潮除湿模式"]
    },
    "智能试衣间": {
        "description": "商用或高级住宅的穿搭视觉空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "多色温无极调节灯光 (模拟室外/晚宴/办公室光照)"},
            {"element": "声", "process": "交互", "name": "语音换光面板 ('切换到酒吧灯光')"},
            {"element": "视", "process": "执行", "name": "3D虚拟试衣AR魔镜终端"}
        ],
        "default_scenarios": ["日常通勤光感", "户外阳光光感", "晚宴昏暗光感"]
    }
}