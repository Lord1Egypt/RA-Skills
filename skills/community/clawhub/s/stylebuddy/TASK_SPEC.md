# StyleBuddy v0.3.0 开发任务书

**任务模式**: 后台异步开发  
**目标**: 完成 Free 版本全部功能  
**数据调整**: 女性穿搭图片占比 90%，共 50 张  
**交付标准**: 可运行的完整 Skill + 预置数据

---

## 📋 任务清单

### Phase 1: 项目框架 (Day 1)
- [ ] 创建项目结构
- [ ] 配置 SQLite 数据库
- [ ] 能力检测模块
- [ ] 基础工具类

### Phase 2: 核心功能 (Day 2-3)
- [ ] 单品录入（文字+图片）
- [ ] 衣橱管理（CRUD）
- [ ] 基础推荐引擎
- [ ] 可视化合成（PIL 拼图）

### Phase 3: 智能增强 (Day 4-5)
- [ ] 天气 API 集成
- [ ] 日历读取
- [ ] 图片搜索（Serper）
- [ ] AI 生成（SiliconFlow）

### Phase 4: 高级功能 (Day 6-7)
- [ ] 穿搭日历
- [ ] 衣橱诊断
- [ ] 一衣多穿
- [ ] 数据备份/恢复

### Phase 5: 预置数据 (Day 8-9)
- [ ] 生成 300 条搭配模板
- [ ] 下载 50 张女性穿搭参考图
- [ ] 整理配色方案和场合规则
- [ ] 验证数据完整性

### Phase 6: 测试优化 (Day 10)
- [ ] 功能测试
- [ ] 降级测试
- [ ] 性能优化
- [ ] 文档更新

---

## 📁 项目结构

```
/Users/mac/.openclaw/workspace/stylebuddy_v3/
├── SKILL.md
├── agent.json
├── main.py
├── requirements.txt
├── config.yaml
│
├── assets/
│   ├── data/
│   │   ├── templates.json          # 300条模板
│   │   ├── color_schemes.json      # 50条配色
│   │   └── occasions.json          # 30条场合
│   └── images/
│       └── outfits/                # 50张女性穿搭图
│
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── router.py               # 能力路由
│   │   ├── recommender.py          # 推荐引擎
│   │   └── analyzer.py             # 衣橱分析
│   ├── models/
│   │   ├── wardrobe.py
│   │   ├── outfit.py
│   │   └── user.py
│   ├── services/
│   │   ├── visualizer.py           # 可视化
│   │   ├── weather.py
│   │   ├── calendar.py
│   │   └── searcher.py
│   ├── storage/
│   │   ├── database.py             # SQLite
│   │   └── assets.py               # 资源管理
│   └── utils/
│       ├── image.py
│       └── text.py
│
└── tests/
    └── test_core.py
```

---

## 🎨 数据规范

### 穿搭图片要求
- **数量**: 50 张
- **主题**: 90% 女性穿搭，10% 中性/通用
- **来源**: Unsplash/Pexels (CC0 授权)
- **尺寸**: 统一 512x512px
- **格式**: JPEG，质量 80%，单张 < 50KB
- **分类**: 职场 30% | 休闲 30% | 约会 20% | 运动 10% | 其他 10%

### 模板数据格式
```json
{
  "id": "t_casual_001",
  "name": "风衣休闲搭配",
  "category": "休闲",
  "gender": "female",
  "occasions": ["日常", "逛街"],
  "items": {
    "outer": ["风衣"],
    "top": ["卫衣", "T恤"],
    "bottom": ["牛仔裤", "休闲裤"],
    "shoes": ["小白鞋", "帆布鞋"]
  },
  "colors": {
    "primary": ["米色", "卡其色"],
    "accent": ["白色", "蓝色"]
  },
  "image_refs": ["casual_001"],
  "tips": "敞开穿更休闲，内搭塞进去显腿长"
}
```

---

## 🔧 技术要点

### 1. 能力检测
```python
class CapabilityRouter:
    def detect(self):
        return {
            "model_tier": self._detect_model(),  # high/medium/low
            "image_search": self._test_serper(),
            "image_gen": self._test_siliconflow(),
            "weather_api": self._test_openmeteo(),
        }
```

### 2. 降级策略
- 无图片搜索 → 本地图库
- 无 AI 生成 → PIL 拼图
- 无天气 API → 用户手动输入
- 无高级模型 → 模板匹配

### 3. 数据库 Schema
```sql
-- 单品表
CREATE TABLE items (
    id TEXT PRIMARY KEY,
    name TEXT,
    category TEXT,  -- outer/top/bottom/shoes/accessory
    color TEXT,
    style TEXT,
    season TEXT,
    image_path TEXT,
    created_at TIMESTAMP
);

-- 穿搭记录表
CREATE TABLE outfits (
    id TEXT PRIMARY KEY,
    date DATE,
    items TEXT,  -- JSON array of item_ids
    occasion TEXT,
    notes TEXT
);

-- 用户偏好表
CREATE TABLE preferences (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

---

## 📊 验收标准

### 功能验收
- [ ] 可录入单品（文字+图片）
- [ ] 可查看可视化衣橱
- [ ] 可获取搭配推荐（3套方案）
- [ ] 天气联动可用
- [ ] 穿搭日历可用
- [ ] 衣橱诊断可用
- [ ] 数据备份/恢复可用

### 性能验收
- [ ] 启动 < 3秒
- [ ] 推荐响应 < 3秒
- [ ] 支持 100+ 单品
- [ ] 离线功能完整

### 数据验收
- [ ] 50 张图片下载完成
- [ ] 300 条模板生成完成
- [ ] 数据总大小 < 10MB

---

## 📝 进度报告

每完成一个 Phase，在 `/Users/mac/.openclaw/workspace/stylebuddy_v3/PROGRESS.md` 中更新：

```markdown
## Phase X 完成 - 日期
- 完成功能: ...
- 遇到问题: ...
- 下一步: ...
- 代码位置: ...
```

---

## ⚠️ 注意事项

1. **频繁提交**: 每完成一个功能 `git commit`
2. **错误处理**: 所有外部 API 调用要有 try-catch
3. **降级优先**: 确保无外部依赖时也能工作
4. **女性为主**: 图片和模板 90% 面向女性用户
5. **版权安全**: 只使用 CC0 或 AI 生成图片

---

**开始执行！**
