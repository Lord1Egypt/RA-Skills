# API 接口文档

此处用于存放婴儿大便颜色识别（陶土色/血便）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动婴儿大便颜色识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取大便颜色分类与风险结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史筛查记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_INFANT_STOOL_COLOR_ABNORMALITY_ANALYSIS` - 婴儿大便颜色识别（陶土色/血便）

## 输入约束

- 设备：婴儿护理台上方固定摄像头 / 智能婴儿护理设备 / 手机后置摄像头
- 拍摄对象：婴儿尿不湿区域（更换时）或直接拍摄排泄物；建议正上方俯拍、距离 15-40 cm
- **光照要求**：自然白光或冷白 LED 光最佳；**严禁使用偏色光（黄光夜灯、暖光、护肤紫光等会引起严重误判）**；禁用美颜/滤镜
- 推荐附带可见参考色卡（标准白卡）放在尿不湿旁，便于白平衡校正
- 图像高清单张 1-3 MB；建议拍摄 1-3 张不同角度

## 大便颜色分类（婴儿适用）

| 颜色类别 | 颜色描述 | 临床意义 | 风险等级 |
|----------|----------|----------|----------|
| `normal_yellow` | 金黄色（母乳喂养） | 正常 | safe |
| `normal_yellow_green` | 黄绿色 / 草绿色 | 大多数情况正常（受饮食影响） | safe |
| `normal_brown` | 黄褐色 / 棕色（已添加辅食） | 正常 | safe |
| `clay_pale` | **白陶土色 / 灰白色** | **疑似胆道梗阻 / 胆道闭锁** | **urgent（必须就医）** |
| `bright_red_blood` | 鲜红色 / 表面带鲜血丝 | 疑似下消化道出血、肛裂 | warning（建议就医） |
| `dark_red_or_black_tarry` | 暗红色 / 柏油样黑色（且非铁剂引起） | 疑似上消化道出血 | warning（建议就医） |
| `dark_green_thin` | 大量稀绿色水样 | 可能腹泻 / 喂养异常（参考） | notice |
| `inconclusive` | 颜色不可判定（光线差/遮挡） | 需重拍 | recapture |

## 输出字段（参考）

- `diaper_or_stool_detected` - 是否检测到尿不湿/排泄物
- `image_quality` - 图像质量（low / medium / high）
- `light_quality_score` - 光照质量（0-1）
- `color_card_calibrated` - 是否进行了色卡白平衡校准
- `dominant_color_lab` - 主色 Lab 值
- `dominant_color_rgb` - 主色 RGB 值
- `stool_color_class` - 颜色分类（见上表）
- `risk_level` - 风险等级（safe / notice / warning / urgent / recapture）
- `confidence` - 分类置信度（0-1）
- `recommended_action` - 建议动作（home_observe / clinic_visit_soon / urgent_hospital_visit / recapture_better_light）
- `alert_message` - 推送给家长的文本（如"检测到宝宝大便呈白陶土色，提示可能胆道异常，请立即前往儿科/小儿外科就诊"）

## 强制规则

- **任何 `clay_pale` 结果（即使置信度较低）都必须返回 `urgent` 级别并强烈建议就医**（胆道闭锁手术黄金窗口期 ≤ 60 天）
- 黑色柏油样需排查是否近期服用铁剂/铋剂，可在 alert_message 中提示

> 仅输出基于视觉的颜色分类与方向性提示，不提供肝胆/消化道疾病的医学诊断；中高风险务必尽快由儿科/小儿外科医生评估并进行专业检查。
