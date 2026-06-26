# dict_05_health_mobility.py
HEALTH_MOBILITY = {
    "智慧健康养老空间": {
        "description": "极度关注生命体征、适老化防跌倒与无感介护的居住空间",
        "hardware_matrix": [
            {"element": "视", "process": "感知", "name": "【严禁使用视觉摄像头】(保护老人生活隐私)"},
            {"element": "电磁", "process": "感知", "name": "卫生间/起居室 3D 点云跌倒检测雷达"},
            {"element": "电磁", "process": "感知", "name": "床垫级非接触式心率/呼吸暂停监测带"},
            {"element": "声", "process": "交互", "name": "拉绳式/大按键式紧急求助报警器 (多重冗余)"},
            {"element": "声", "process": "交互", "name": "AI 离线语音提醒器 (吃药/喝水/防诈骗提示)"},
            {"element": "光", "process": "感知/执行", "name": "防眩目地脚灯/床底灯带 (起夜安全防绊倒)"},
            {"element": "能", "process": "执行", "name": "忘关火自动切断智能灶具插座/防干烧模块"},
            {"element": "气", "process": "感知", "name": "轮椅/助行器室内高精度定位标签"}
        ],
        "default_scenarios": ["日常适老起居模式", "起夜防跌倒照明", "突发健康危机 (声光电报警+断气断水)"]
    },
    "智慧病房": {
        "description": "医疗级监护、医护协同与病患心理干预空间",
        "hardware_matrix": [
            {"element": "电磁", "process": "连接", "name": "医疗级内网隔离边缘网关"},
            {"element": "光", "process": "执行", "name": "可调节医疗检查灯 (高照度) 与 康复氛围灯"},
            {"element": "视", "process": "交互", "name": "床头智能交互平板 (病历/点餐/呼叫护士)"},
            {"element": "电磁", "process": "感知", "name": "静脉滴注余量监测雷达/红外感应"},
            {"element": "气", "process": "执行", "name": "病房级防交叉感染独立微正压新风阀"},
            {"element": "光", "process": "执行", "name": "自动防晒/防窥百叶中空玻璃联动器"}
        ],
        "default_scenarios": ["医生查房模式 (高亮)", "病人静养模式", "点滴耗尽自动呼叫模式"]
    },
    "智慧教室": {
        "description": "大班额、护眼导向与环境健康维持的公共学习空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "国标防眩光护眼黑板灯与教室主灯阵列"},
            {"element": "光", "process": "感知", "name": "恒照度探头 (靠窗与靠墙排灯光亮度自动补差)"},
            {"element": "气", "process": "感知", "name": "高敏 CO2 探测器 (大班额极易缺氧影响智力)"},
            {"element": "气", "process": "执行", "name": "强力静音新风机联动模块"},
            {"element": "声", "process": "执行", "name": "全向声场扩音系统 (保护教师嗓子)"},
            {"element": "电磁", "process": "感知", "name": "课间人员清空感知雷达 (人走自动关灯关空调)"}
        ],
        "default_scenarios": ["投影上课模式 (黑板亮/主灯灭)", "自习模式", "课间强制换气模式", "放学自动断电模式"]
    },
    "智能车内空间": {
        "description": "DC直流供电、高震动、极致狭小与移动特性的房车/越野舱空间",
        "hardware_matrix": [
            {"element": "能", "process": "计算/连接", "name": "车载 12V/24V 专用 DC 智能边缘中控主机"},
            {"element": "能", "process": "感知", "name": "磷酸铁锂副电瓶 BMS/库仑计状态读取网关"},
            {"element": "气", "process": "执行", "name": "房车专用驻车空调/柴暖排风智能面板"},
            {"element": "气", "process": "感知", "name": "防一氧化碳中毒/燃气泄漏探测器"},
            {"element": "光", "process": "执行", "name": "车厢星空顶/床铺阅读灯 DC 调光模块"},
            {"element": "电磁", "process": "感知", "name": "水箱清水/灰水/黑水液位超声波雷达传感器"},
            {"element": "视", "process": "感知", "name": "驻车 360 度环视安防哨兵系统"}
        ],
        "default_scenarios": ["行车锁定模式", "驻车露营模式 (氛围光+水泵开启)", "极寒保暖模式", "离车哨兵警戒模式"]
    },
    "智能船内空间": {"description": "游艇/船舱防潮、防盐雾的离网封闭空间", "hardware_matrix": [{"element": "电磁", "process": "连接", "name": "卫星通信转本地 Wi-Fi 边缘网关"}, {"element": "气", "process": "执行", "name": "船舱专用强力抽湿机与底舱抽水泵联动"}, {"element": "光", "process": "执行", "name": "防眩晕甲板光环境调配器"}], "default_scenarios": ["航海模式", "靠岸休整模式", "防台风锁仓模式"]},
    "智慧候车厅": {"description": "高吞吐量的人员中转区域", "hardware_matrix": [{"element": "光", "process": "执行", "name": "DALI 分区智能照明 (深夜少人区降载)"}, {"element": "电磁", "process": "感知", "name": "座位占有率热力雷达"}, {"element": "声", "process": "执行", "name": "定向发声广播播音阵列"}], "default_scenarios": ["白天高负荷运营", "深夜节能低功耗模式"]},
    "智慧停车场": {"description": "地下密闭的车辆集散地", "hardware_matrix": [{"element": "气", "process": "感知/执行", "name": "CO浓度监测联动诱导排风机"}, {"element": "光", "process": "执行", "name": "车至灯亮/车走微亮雷达感应灯管"}, {"element": "视", "process": "感知", "name": "视频车牌反寻导航探头"}], "default_scenarios": ["日常节能照明", "尾气超标强排风"]}
}