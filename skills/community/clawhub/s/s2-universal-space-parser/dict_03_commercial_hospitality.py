# dict_03_commercial_hospitality.py
COMMERCIAL_HOSPITALITY = {
    "智慧酒店客房": {
        "description": "极具标准化的商旅居住与无卡化体验空间",
        "hardware_matrix": [
            {"element": "电磁", "process": "计算/连接", "name": "酒店专用 RCU (客房控制单元) 强弱电一体网关"},
            {"element": "视", "process": "感知/执行", "name": "门外带屏电子门牌 (显勿扰/清理/房号)"},
            {"element": "电磁", "process": "感知", "name": "天花板暗装毫米波人体存在传感器 (取代传统插卡取电)"},
            {"element": "光", "process": "执行", "name": "DALI 全局平滑调光模块 (防客户突发强光致盲)"},
            {"element": "光", "process": "执行", "name": "遮光卷帘与电动纱帘 (入内自动拉开迎客)"},
            {"element": "声", "process": "交互", "name": "酒店专属定制语音管家 (集成客房服务呼叫)"},
            {"element": "气", "process": "执行", "name": "中央空调风机盘管温控器 (联网下发限温策略)"},
            {"element": "能", "process": "执行", "name": "防漏电安全插座 (电水壶/吹风机专线)"}
        ],
        "default_scenarios": ["迎客模式 (开帘亮灯轻音乐)", "睡眠模式 (断电留夜灯)", "勿扰模式", "退房清扫模式"]
    },
    "智能咖啡馆": {
        "description": "强调氛围感、背景音效与气味管理的社交空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "分区域多色温射灯驱动 (餐桌聚焦，过道柔和)"},
            {"element": "气", "process": "执行", "name": "商业级扩香机/香氛系统 (咖啡豆香气增强)"},
            {"element": "声", "process": "执行", "name": "多区独立音量背景音乐矩阵 (覆盖聊天杂音)"},
            {"element": "电磁", "process": "感知", "name": "3D客流统计雷达 (分析热点落座区域)"},
            {"element": "气", "process": "感知", "name": "高敏 CO2 与异味探测器"},
            {"element": "气", "process": "执行", "name": "商用强排风与新风热交换系统"}
        ],
        "default_scenarios": ["清晨营业模式", "午后高客流模式 (强换气)", "打烊自清洁模式"]
    },
    "智慧奶茶店": {
        "description": "高密度作业、高能耗及前场快节奏交互空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "高亮冷白光操作台照明 (Ra>95 防材料变色)"},
            {"element": "视", "process": "交互", "name": "叫号与广告数字标牌联动屏幕"},
            {"element": "能", "process": "执行", "name": "大功率制冰机/封口机专属智能空开 (防过载跳闸)"},
            {"element": "气", "process": "感知", "name": "冷柜温度与漏水异常探测器 (防止物料报废)"},
            {"element": "声", "process": "感知", "name": "前台环境噪音拾音器 (动态调整叫号音量)"}
        ],
        "default_scenarios": ["早班备料模式", "高峰期模式 (全负荷)", "打烊盘点模式"]
    },
    "智能美容院": {
        "description": "绝对隐私、极致放松与环境微控的疗愈空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "无极柔光色温调节系统 (防仰卧刺眼)"},
            {"element": "视", "process": "感知", "name": "【严禁部署任何视觉摄像头】 (纯物理空间隔离)"},
            {"element": "电磁", "process": "感知", "name": "床铺微动毫米波雷达 (感知客户是否入睡)"},
            {"element": "声", "process": "执行", "name": "白噪音与 432Hz 疗愈频率共振音箱"},
            {"element": "气", "process": "执行", "name": "微正压恒温空调 (防止美容服更换时着凉)"},
            {"element": "能", "process": "执行", "name": "美容仪器安全限载插座"}
        ],
        "default_scenarios": ["迎宾准备模式", "面部护理模式 (高显色聚光)", "身体SPA模式 (昏暗暖光+水流音)"]
    },
    "智能K歌房": {
        "description": "高声压级、强视觉冲击与密闭环境的娱乐空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "DMX512 协议舞台律动灯光控制器 (全彩/爆闪/激光)"},
            {"element": "气", "process": "感知", "name": "烟雾探测器与 PM2.5 (抽烟) 探测器"},
            {"element": "气", "process": "执行", "name": "大功率强排风换气系统 (与烟雾浓度联动)"},
            {"element": "声", "process": "执行", "name": "防啸叫专业级 DSP 音频处理网关"},
            {"element": "视", "process": "交互", "name": "点歌台与全息墙面投影联动主机"}
        ],
        "default_scenarios": ["慢摇听歌模式", "全场嗨爆模式", "打烊强排风模式"]
    },
    "智能书店": {"description": "沉静阅读与文化展示空间", "hardware_matrix": [{"element": "光", "process": "执行", "name": "书架洗墙灯与护眼阅读区照明"}, {"element": "声", "process": "执行", "name": "极低音量白噪音发生器"}, {"element": "电磁", "process": "感知", "name": "书架区域驻留时长感知雷达"}], "default_scenarios": ["日间营业模式", "夜间沙龙模式"]},
    "智能前台": {"description": "企业/商业的门面与接待枢纽", "hardware_matrix": [{"element": "视", "process": "感知", "name": "VIP客户/员工人脸识别探头"}, {"element": "光", "process": "执行", "name": "品牌 Logo 射灯智能控制"}, {"element": "交互", "process": "交互", "name": "迎宾语音交互数字人屏幕"}], "default_scenarios": ["迎宾模式", "夜间安防模式"]}
}