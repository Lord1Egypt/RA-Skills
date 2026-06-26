# 参数术语解释

## 通用参数字段

| 字段名 | 英文名称 | 描述 | 数据类型 |
|--------|----------|------|----------|
| 型号 | model | 设备型号 | 字符串 |
| 类型 | type | 设备类型 | 字符串 |
| 品牌 | brand | 设备品牌 | 字符串 |
| 量程 | range | 测量范围 | 字符串 |
| 精度 | accuracy | 测量精度 | 字符串 |
| IP等级 | ip_rating | 防护等级 | 字符串 |
| 供电 | power_supply | 供电方式 | 字符串 |
| 通讯协议 | protocol | 通讯接口和协议 | 字符串 |
| 工作温度 | operating_temperature | 工作温度范围 | 字符串 |
| 工作压力 | operating_pressure | 工作压力范围 | 字符串 |
| 介质温度 | media_temperature | 介质温度范围 | 字符串 |
| 安装方式 | installation | 安装方式 | 字符串 |
| 适用介质 | suitable_media | 适用的介质类型 | 字符串 |
| 应用场景 | application | 典型应用场景 | 字符串 |
| 价格 | price | 参考价格 | 字符串 |

## 液位计特有的参数字段

| 字段名 | 英文名称 | 描述 | 数据类型 |
|--------|----------|------|----------|
| 测量原理 | measurement_principle | 测量原理（雷达、超声波等） | 字符串 |
| 频率 | frequency | 工作频率 | 字符串 |
| 波束角 | beam_angle | 雷达波/超声波波束角 | 字符串 |
| 盲区 | dead_zone | 测量盲区 | 字符串 |
| 输出信号 | output_signal | 输出信号类型 | 字符串 |
| 过程连接 | process_connection | 过程连接方式 | 字符串 |
| 防爆等级 | explosion_proof | 防爆等级 | 字符串 |

## 水尺特有的参数字段

| 字段名 | 英文名称 | 描述 | 数据类型 |
|--------|----------|------|----------|
| 材质 | material | 水尺材质 | 字符串 |
| 长度 | length | 水尺长度 | 字符串 |
| 刻度间隔 | scale_interval | 刻度间隔 | 字符串 |
| 读数精度 | reading_accuracy | 读数精度 | 字符串 |
| 颜色 | color | 水尺颜色 | 字符串 |
| 耐腐蚀等级 | corrosion_resistance | 耐腐蚀等级 | 字符串 |

## 流量计特有的参数字段

| 字段名 | 英文名称 | 描述 | 数据类型 |
|--------|----------|------|----------|
| 测量原理 | measurement_principle | 测量原理（电磁、超声波等） | 字符串 |
| 口径 | diameter | 管道直径 | 字符串 |
| 流速范围 | flow_velocity | 测量流速范围 | 字符串 |
| 输出信号 | output_signal | 输出信号类型 | 字符串 |
| 安装方式 | installation | 安装方式（插入式、管段式等） | 字符串 |
| 精度等级 | accuracy_class | 精度等级 | 字符串 |
| 重复性 | repeatability | 测量重复性 | 字符串 |
| 线性度 | linearity | 测量线性度 | 字符串 |

## 水质传感器特有的参数字段

| 字段名 | 英文名称 | 描述 | 数据类型 |
|--------|----------|------|----------|
| 测量参数 | measurement_parameter | 测量的水质参数（PH、浊度等） | 字符串 |
| 测量范围 | measurement_range | 参数测量范围 | 字符串 |
| 分辨率 | resolution | 测量分辨率 | 字符串 |
| 响应时间 | response_time | 测量响应时间 | 字符串 |
| 校准周期 | calibration_period | 校准周期 | 字符串 |
| 电极材质 | electrode_material | 传感器电极材质 | 字符串 |
| 防护等级 | protection_level | 传感器防护等级 | 字符串 |

## 压力传感器特有的参数字段

| 字段名 | 英文名称 | 描述 | 数据类型 |
|--------|----------|------|----------|
| 压力类型 | pressure_type | 压力类型（表压、绝压、差压） | 字符串 |
| 测量范围 | measurement_range | 压力测量范围 | 字符串 |
| 输出信号 | output_signal | 输出信号类型 | 字符串 |
| 精度等级 | accuracy_class | 精度等级 | 字符串 |
| 稳定性 | stability | 测量稳定性 | 字符串 |
| 过载能力 | overload_capability | 最大过载能力 | 字符串 |
| 长期漂移 | long_term_drift | 长期漂移值 | 字符串