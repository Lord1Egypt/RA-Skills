# dict_02_leisure_outdoor.py
LEISURE_OUTDOOR = {
    "智能影音室": {
        "description": "极致声光电同步的家庭影院沉浸空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "阶梯式渐暗星空顶/跑道灯控制器"},
            {"element": "光", "process": "执行", "name": "100% 遮光吸音智能厚窗帘"},
            {"element": "气", "process": "执行", "name": "超静音剧院级独立新风循环系统"},
            {"element": "声", "process": "执行", "name": "杜比全景声 7.1.4 功放与音频矩阵网关"},
            {"element": "电磁", "process": "感知", "name": "沙发久坐/入座震动感知传感器"},
            {"element": "能", "process": "执行", "name": "时序电源控制器 (按顺序开启影音设备防冲击)"},
            {"element": "视", "process": "执行", "name": "投影仪升降架与电动透声幕布联动器"}
        ],
        "default_scenarios": ["一键观影模式 (灯灭幕降)", "中场休息模式 (灯光微亮)", "游戏电竞模式 (灯带律动)"]
    },
    "智能花园": {
        "description": "植物养护与户外环境的自动化生态空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "光照度自适应太阳能草坪灯/景观射灯"},
            {"element": "气", "process": "感知", "name": "户外气象站 (风速/雨量/温湿度/光照)"},
            {"element": "气", "process": "感知", "name": "土壤湿度与肥力传感器"},
            {"element": "气", "process": "执行", "name": "多路智能电磁阀 (滴灌/喷灌控制)"},
            {"element": "声", "process": "执行", "name": "户外防水伪装岩石音箱"},
            {"element": "视", "process": "感知", "name": "周界防范 AI 摄像头/电子围栏"}
        ],
        "default_scenarios": ["自动灌溉模式 (依据天气预报与土壤湿度)", "夏夜烧烤模式", "安防警戒模式"]
    },
    "智能宠物房": {
        "description": "非碳基人类生命的专属监控与照料空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "符合宠物视觉光谱的护眼照明"},
            {"element": "气", "process": "执行", "name": "宠物专属恒温加热垫/新风除味机"},
            {"element": "气", "process": "感知", "name": "猫砂盆异味/粉尘监测器"},
            {"element": "能", "process": "执行", "name": "智能自动喂食器/饮水机网关接入"},
            {"element": "视", "process": "感知", "name": "宠物追踪 AI 摄像头 (带互动激光笔)"}
        ],
        "default_scenarios": ["定时投喂模式", "智能除味排风模式", "远程逗宠模式"]
    },
    "智能阳台": {
        "description": "半户外晾晒、生态延展与过渡空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "吸顶防潮阳台主灯/夜间微光灯"},
            {"element": "气", "process": "感知", "name": "户外风雨传感器"},
            {"element": "气", "process": "执行", "name": "自动推窗器 (遇雨自动关窗)"},
            {"element": "电磁", "process": "执行", "name": "智能升降晾衣机 (带烘干/杀菌功能)"},
            {"element": "视", "process": "感知", "name": "阳台越界入侵报警雷达/探头"}
        ],
        "default_scenarios": ["一键晾衣模式", "狂风暴雨防御模式", "午后观景模式"]
    },
    "智能酒窖": {
        "description": "极致苛刻的恒温恒湿藏品级空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "冷光源无紫外线 LED 藏酒照明 (防止酒体变质)"},
            {"element": "气", "process": "感知", "name": "高精度工业级温湿度探头阵列"},
            {"element": "气", "process": "执行", "name": "酒窖专用恒温恒湿精密空调网关"},
            {"element": "电磁", "process": "感知", "name": "防盗门磁与人员存在雷达"},
            {"element": "视", "process": "感知", "name": "贵重藏品区视频监控系统"}
        ],
        "default_scenarios": ["严格恒温恒湿监控", "取酒照明模式", "异常波动紧急告警"]
    },
    "别墅智能车库": {
        "description": "人车过渡、安防第一道防线的物理空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "车辆入库高亮引导车道灯"},
            {"element": "气", "process": "感知", "name": "CO/汽车尾气探测器"},
            {"element": "气", "process": "执行", "name": "超标尾气强力排风机联动模块"},
            {"element": "电磁", "process": "执行", "name": "智能电动车库门控制器 (联动车辆到达)"},
            {"element": "能", "process": "执行", "name": "新能源汽车充电桩智能调度控制盒"},
            {"element": "视", "process": "感知", "name": "车牌识别 AI 摄像头"}
        ],
        "default_scenarios": ["无感归家模式 (识牌开门+亮灯)", "夜间防盗警戒模式", "错峰充电调度模式"]
    },
    "智能健身房": {
        "description": "荷尔蒙释放、生理机能激活与监测空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "高亮冷白光与 RGB 动感灯光切换驱动"},
            {"element": "气", "process": "感知/执行", "name": "高需氧量 CO2 探测器与最大功率新风联动"},
            {"element": "气", "process": "执行", "name": "剧烈运动空调直吹规避/快速降温模块"},
            {"element": "声", "process": "执行", "name": "强低音高爆发运动音响系统"},
            {"element": "视", "process": "执行", "name": "智能运动魔镜 (AI 体态纠正指导)"}
        ],
        "default_scenarios": ["高强度有氧模式 (动感声光)", "瑜伽冥想模式 (柔光白噪音)", "空闲通风换气模式"]
    },
    "智能茶室": {
        "description": "东方禅意与高端会客的文化空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "低色温聚光射灯 (茶台聚焦) 与竹木暗纹氛围灯"},
            {"element": "气", "process": "执行", "name": "茶香辅助抽风系统 (控制香炉烟雾走向)"},
            {"element": "声", "process": "执行", "name": "隐藏式古风/禅音背景音乐扬声器"},
            {"element": "能", "process": "执行", "name": "茶台自动煮水炉/电磁炉智能插座"}
        ],
        "default_scenarios": ["品茗会客模式", "禅意独处模式"]
    },
    "智能化妆间": {
        "description": "专业级脸部高显色光源与私密护理空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "Ra>98 多色温专业美妆镜前灯 (模拟各种社交场合光线)"},
            {"element": "能", "process": "执行", "name": "美容仪/卷发棒安全断电插座"},
            {"element": "气", "process": "执行", "name": "化妆品小冰箱智能监控模块"}
        ],
        "default_scenarios": ["职场妆容光", "约会晚宴妆容光", "卸妆护理模式"]
    },
    "智能鱼池": {
        "description": "水生动植物的水质微生态维持空间",
        "hardware_matrix": [
            {"element": "光", "process": "执行", "name": "水下 RGB 景观灯光与植物生长射灯"},
            {"element": "气", "process": "感知", "name": "水质传感器 (PH值/溶氧量/温度/浊度)"},
            {"element": "能", "process": "执行", "name": "水泵/增氧机/杀菌灯循环定时控制器"},
            {"element": "能", "process": "执行", "name": "自动定时投饵机"}
        ],
        "default_scenarios": ["日常生态循环模式", "观赏模式 (全亮灯)", "夜间静音溶氧模式"]
    },
    "智能假山": {"description": "庭院水景联动", "hardware_matrix": [{"element": "能", "process": "执行", "name": "水泵跌水控制模块"}, {"element": "光", "process": "执行", "name": "假山雾化器与局部光带联动"}], "default_scenarios": ["迎客水景模式"]},
    "智能凉亭": {"description": "户外半开放休憩空间", "hardware_matrix": [{"element": "光", "process": "执行", "name": "驱蚊灯/户外复古吊灯"}, {"element": "气", "process": "执行", "name": "户外降温喷雾系统"}], "default_scenarios": ["纳凉模式", "夜间驱蚊模式"]},
    "智能屋顶": {"description": "建筑顶端光伏与气象空间", "hardware_matrix": [{"element": "能", "process": "感知", "name": "屋顶光伏发电与储能逆变器接入网关"}, {"element": "气", "process": "感知", "name": "雷暴/积雪传感器"}], "default_scenarios": ["能源回收模式", "恶劣天气防护"]}
}