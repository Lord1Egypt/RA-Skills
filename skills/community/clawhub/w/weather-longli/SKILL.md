# weather-longli

**龙里县天气日报与穿衣建议技能**  
为贵州省龙里县提供每日天气爬取、穿衣建议生成，支持 OpenClaw cron 定时推送。

## 功能
- 爬取中国天气网（www.weather.com.cn）龙里县页面
- 解析温度、天气现象、风力
- 基于温度与天气生成穿衣建议（规则引擎）
- 支持 OpenClaw cron 定时推送（如工作日 7:20）
- 零 API 成本（纯爬虫 + 本地逻辑）

## 安装
```bash
# 方式一：从 ClawHub 安装（若已发布）
clawdhub install weather-longli

# 方式二：手动安装
cd ~/.openclaw/skills
git clone <repository> weather-longli
```

## 使用方法
### 1. 手动测试
```bash
cd ~/.openclaw/skills/weather-longli/scripts
source /path/to/your/venv/bin/activate  # 如有虚拟环境
python3 daily_weather_report.py
```
输出将直接打印到 stdout，适合 OpenClaw cron 捕获并发送。

### 2. 配置 OpenClaw cron
在 OpenClaw 配置中添加（或通过 `openclaw cron add`）：
```yaml
# cron-example.yaml
name: longli_weather_morning
schedule: "20 7 * * 1-5"  # 工作日 7:20
command: |
  cd ~/.openclaw/skills/weather-longli/scripts
  python3 daily_weather_report.py
```

### 3. 自定义穿衣规则
编辑 `scripts/dress_advice.py` 中的 `generate_dress_advice` 函数，调整温度阈值与建议文本。

## 文件结构
```
weather-longli/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── crawl_longli_weather.py # 爬虫核心
│   ├── dress_advice.py         # 穿衣建议引擎
│   └── daily_weather_report.py # 整合脚本
├── templates/
│   └── cron-example.yaml       # OpenClaw cron 配置示例
└── config.example.yaml         # （预留）配置模板
```

## 依赖
- Python 3.8+
- `requests`、`beautifulsoup4`
- 可选的虚拟环境（推荐）

安装依赖：
```bash
pip install requests beautifulsoup4
```

## 示例输出
```
🌤️ 龙里县今日天气（2026-03-15）
温度：8℃～15℃
天气：多云转晴
风力：东北风 2级

👔 穿衣建议：长袖衬衫+薄外套，早晚温差大，建议带件外套备用。
```

## 注意事项
1. **数据来源**：中国天气网（www.weather.com.cn），页面结构若变更需更新爬虫逻辑。
2. **网络要求**：需能访问外网。
3. **失败处理**：脚本内置简单容错，失败时返回兜底消息。
4. **零成本**：不调用任何付费 API，完全依赖公开数据与本地规则。

## 作者
Lancy（根据用户需求定制）  
创建于 2026-03-14

## 许可证
MIT（可根据需要调整）