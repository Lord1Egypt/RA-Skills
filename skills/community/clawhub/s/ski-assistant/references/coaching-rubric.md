# AI 电子教练评分参考

本文件定义滑雪姿态分析的评分维度、评分细则和分析输出格式。为 `modules/coaching.md` 提供评分标准的详细参考。

## 评分维度（满分 10 分）

### 一、基础姿态（posture）

| 子项 | 英文 key | 评分要点 |
|------|---------|---------|
| 重心位置 | center_of_gravity | 重心应在双脚之间偏前，膝盖在脚尖正上方。重心过后（坐在板上）扣分严重 |
| 膝盖弯曲 | knee_bend | 膝盖应保持适度弯曲（约 15-25°），过直或过弯都扣分 |
| 上半身姿态 | upper_body | 上半身应微前倾，面向山下。后仰或侧倾扣分 |
| 手臂位置 | arm_position | 双臂自然前伸，高度在腰部以上。手臂乱甩或紧贴身体扣分 |
| 髋部对齐 | hip_alignment | 髋部应面向行进方向，不应过度旋转 |
| 踝关节屈曲 | ankle_flex | 踝关节应有适度前压，保持小腿贴合雪鞋前壁 |

### 二、转弯技术（turning）

| 子项 | 英文 key | 评分要点 |
|------|---------|---------|
| 平行站姿 | parallel_stance | 双板应保持平行，间距约肩宽。内八字或外八字扣分 |
| 立刃角度 | edge_angle | 转弯时雪板应有明确立刃，角度越大表示技术越好 |
| 换刃时机 | edge_transition | 换刃应平滑连贯，不应有明显停顿或中间阶段 |
| 卡宾质量 | carving_quality | 雪面应留下清晰弧线（非搓雪），雪花飞溅越少越好 |
| 弯型控制 | turn_shape | 弯型应圆滑对称，大小一致。S 弯连接流畅 |
| 点杖技术 | pole_plant | 点杖应在转弯入弯点前方，动作轻巧，引导转弯节奏 |

### 三、自由式/公园（freestyle）

仅在公园/mogul/跳台场景评分。普通雪道不评此维度。

| 子项 | 英文 key | 评分要点 |
|------|---------|---------|
| 起跳 | takeoff | 起跳时机、角度和力度 |
| 空中控制 | air_control | 空中身体姿态控制、轴心稳定 |
| 落地 | landing | 落地稳定性、膝盖缓冲 |
| 技巧完成度 | trick_execution | 动作完成度和精确性 |
| 风格表现 | style | 动作流畅度和个人风格 |

### 四、综合滑行（overall）

| 子项 | 英文 key | 评分要点 |
|------|---------|---------|
| 速度控制 | speed_control | 能否根据地形和人流控制速度，不失控 |
| 路线选择 | line_choice | 是否选择合适的滑行路线，利用地形 |
| 地形适应 | terrain_adaptation | 对不同地形（陡坡、缓坡、冰面、粉雪）的适应能力 |
| 节奏感 | rhythm | 转弯和滑行的节奏是否连贯一致 |
| 自信度 | confidence | 滑行是否自信流畅，无犹豫或恐惧感 |
| 安全意识 | safety_awareness | 是否注意周围环境、保持安全距离 |

---

## 分析输出格式

Agent 分析完照片后，输出须包含以下内容：

```json
{
  "scores": {
    "posture": {
      "center_of_gravity": 7.5,
      "knee_bend": 6.0,
      "upper_body": 8.0,
      "arm_position": 7.0,
      "hip_alignment": 6.5,
      "ankle_flex": 5.5
    },
    "turning": {
      "edge_angle": 6.5,
      "turn_shape": 7.0,
      "edge_transition": 5.5,
      "carving_quality": 6.0,
      "pole_plant": 4.0
    },
    "overall": {
      "speed_control": 7.5,
      "line_choice": 7.0,
      "terrain_adaptation": 6.0,
      "confidence": 7.5,
      "safety_awareness": 8.0
    }
  },
  "highlights": ["亮点1", "亮点2"],
  "issues": ["问题1", "问题2"],
  "advice": ["具体可执行的改进建议1", "建议2"],
  "coach_note": "一句话总结"
}
```

### 关键规则

1. **所有分数 1-10 分**，精确到 0.5
2. **freestyle 维度**仅在公园/mogul/跳台场景出现，普通雪道不评
3. **highlights** 和 **issues** 应具体到动作细节（如"膝盖弯曲角度好"而非"姿势不错"）
4. **advice** 必须是可执行的训练建议（如"在缓坡反复练习换刃，关注上半身保持面向山下"）
5. 照片模糊或角度不佳时，在 coach_note 中说明，并建议侧面 15-60 秒视频或清晰静态照片

---

## 记录保存格式（JSON Lines）

每次分析结果追加到 `~/.ski-assistant/records.json`（JSON 数组格式）：

```json
{
  "id": "20260115-143025",
  "date": "2026-01-15",
  "resort": "万龙滑雪场",
  "run_name": "银龙道",
  "trail_difficulty": "blue",
  "snow_condition": "粉雪",
  "media_type": "photo",
  "media_path": "/path/to/photo.jpg",
  "level": "intermediate",
  "sport_type": "alpine",
  "scores": { ... },
  "dimension_averages": {"posture": 6.8, "turning": 5.8, "overall": 7.0},
  "total_score": 6.5,
  "highlights": [...],
  "issues": [...],
  "advice": [...],
  "coach_note": "...",
  "recorded_at": "2026-01-15T14:30:25+08:00"
}
```

- `dimension_averages`：每个维度所有子项的平均分
- `total_score`：所有维度平均分的平均值
- `id` 格式：`YYYYMMDD-HHMMSS`

---

## 进步报告规则

生成进步报告时，对比首次和最近一次记录：

- 变化 > +0.5 → 标记为"进步"
- 变化 < -0.5 → 标记为"退步"
- 变化在 ±0.5 以内 → 标记为"稳定"

统计反复出现的 issues（出现 2 次以上），作为重点改进方向。

## 雪季总结规则

雪季定义：当年 10 月 1 日至次年 5 月 31 日。自动按最近记录的日期推断所属雪季。

总结包含：总次数、去过的雪场、评分变化趋势、各维度成长、本季亮点、持续改进方向、水平提升情况。

## 视觉模型配置

支持的视觉模型提供商：

| 提供商 | 模型 | API Key 环境变量 | 端点 |
|--------|------|-----------------|------|
| OpenAI | gpt-4o, gpt-4o-mini | OPENAI_API_KEY | https://api.openai.com |
| Anthropic | claude-sonnet-4-20250514, claude-3.5-sonnet | ANTHROPIC_API_KEY | https://api.anthropic.com |
| Google | gemini-2.0-flash, gemini-2.0-pro | GOOGLE_API_KEY | generativelanguage.googleapis.com |
| 通义千问 | qwen-vl-max, qwen-vl-plus | DASHSCOPE_API_KEY | dashscope.aliyuncs.com/compatible-mode |
| 豆包 | doubao-vision-pro, doubao-vision-lite | DOUBAO_API_KEY | ark.cn-beijing.volces.com |
| 阶跃星辰 | step-1v | STEPFUN_API_KEY | api.stepfun.com |
| 智谱 | glm-4v-plus, glm-4v | ZHIPU_API_KEY | open.bigmodel.cn |

未配置任何 API Key 时，Agent 使用自身视觉能力按本文档标准完成分析。
