# Video Pro 模板系统

Video Pro 提供多种专业视频模板，满足不同场景需求。

## 🎨 可用模板

### 免费模板
1. **basic** - 基础模板
   - 简洁的赛博线框风格
   - 适合通用内容
   - 免费版默认模板

### 高级模板（需要许可证）
2. **marketing** - 营销模板
   - 动态产品展示
   - 强调关键卖点
   - 适合产品推广

3. **education** - 教育模板
   - 清晰的知识点展示
   - 逐步讲解风格
   - 适合教学视频

4. **social-media** - 社交媒体模板
   - TikTok/抖音风格
   - 快速节奏
   - 适合短视频平台

5. **corporate** - 企业模板
   - 专业商务风格
   - 品牌色彩定制
   - 适合企业培训

6. **news** - 新闻模板
   - 新闻报道风格
   - 严肃正式
   - 适合时事评论

## 🛠️ 使用模板

### 命令行使用
```bash
# 使用营销模板
./generate.sh "产品介绍脚本" --template marketing

# 使用教育模板
./generate.sh "课程内容" --template education

# 使用社交媒体模板
./generate.sh "短视频内容" --template social-media
```

### 批量生成使用
```bash
# 批量使用特定模板
./batch-generate.sh scripts.txt --template corporate
```

## 🎯 模板特性

### 视觉风格
- **basic**: 蓝紫色赛博线框
- **marketing**: 金色+品牌色强调
- **education**: 蓝色+绿色清新风格
- **social-media**: 多彩动态效果
- **corporate**: 深色专业风格
- **news**: 红白经典配色

### 动画效果
- **basic**: 基础淡入淡出
- **marketing**: 弹跳强调动画
- **education**: 平滑过渡
- **social-media**: 快速切换
- **corporate**: 稳重平移
- **news**: 新闻条滚动

### 字体选择
- **basic**: 科技感字体
- **marketing**: 现代无衬线字体
- **education**: 清晰易读字体
- **social-media**: 时尚字体
- **corporate**: 专业字体
- **news**: 新闻字体

## 🔧 自定义模板

### 创建自定义模板
```bash
# 复制基础模板
cp -r templates/basic templates/my-custom

# 编辑配置文件
nano templates/my-custom/config.json

# 编辑样式文件
nano templates/my-custom/styles.css
```

### 模板配置文件示例
```json
{
  "name": "my-custom",
  "display_name": "我的自定义模板",
  "version": "1.0.0",
  "author": "你的名字",
  "description": "自定义视频模板",
  "styles": {
    "primary_color": "#FF6B6B",
    "secondary_color": "#4ECDC4",
    "background_color": "#1A1A2E",
    "text_color": "#FFFFFF",
    "font_family": "Arial, sans-serif"
  },
  "animations": {
    "title_effect": "glitch",
    "transition_speed": "normal",
    "emphasis_effect": "zoom"
  },
  "requirements": {
    "license_level": "professional",
    "max_duration": 60
  }
}
```

## 📊 模板性能

### 渲染时间
- **basic**: 最快，约20秒/视频
- **marketing**: 中等，约25秒/视频
- **education**: 中等，约25秒/视频
- **social-media**: 较快，约22秒/视频
- **corporate**: 较慢，约30秒/视频
- **news**: 中等，约25秒/视频

### 文件大小
- **basic**: 最小，约5MB/分钟
- **marketing**: 中等，约8MB/分钟
- **education**: 中等，约7MB/分钟
- **social-media**: 较小，约6MB/分钟
- **corporate**: 较大，约10MB/分钟
- **news**: 中等，约8MB/分钟

## 🔒 许可证要求

### 免费版
- 仅限 **basic** 模板
- 720p分辨率
- 基础效果

### 个人版
- 所有模板
- 1080p分辨率
- 标准效果

### 专业版
- 所有模板 + 自定义模板
- 4K分辨率
- 高级效果
- 优先渲染

### 企业版
- 所有功能
- 自定义开发
- 专属优化

## 📈 模板选择建议

### 内容类型推荐
- **产品推广**: marketing
- **知识分享**: education
- **社交媒体**: social-media
- **企业培训**: corporate
- **新闻资讯**: news
- **通用内容**: basic

### 平台适配
- **TikTok/抖音**: social-media
- **YouTube**: marketing/education
- **企业网站**: corporate
- **新闻平台**: news
- **通用平台**: basic

## 🆕 模板更新

Video Pro 会定期更新和添加新模板。要获取最新模板：

```bash
# 更新所有模板
./update-templates.sh

# 查看可用更新
./list-template-updates.sh
```

## 📞 模板支持

如有模板相关问题：
1. 查看文档：https://docs.video-pro.cza999.com/templates
2. 社区讨论：https://discord.gg/video-pro
3. 技术支持：support@video-pro.cza999.com

---

**注意**: 高级模板需要相应许可证级别才能使用。
**更新**: 模板系统会定期更新，建议保持最新版本。