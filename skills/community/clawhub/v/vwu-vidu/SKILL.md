# vwu-vidu Models for vwu.ai

vwu.ai 平台上的 Vidu 视频生成模型技能。

## ✅ 支持的模型

**已验证可用**:
- viduq3-pro - Vidu Q3 Pro（推荐，完全支持）
- viduq2-turbo - Vidu Q2 Turbo（需测试）

**不支持**:
- vidu2.0, viduq1, viduq1-classic - 旧版本已下线
- viduq2-pro - API 不支持

## 🎬 功能特性

### 文生视频
从文本描述生成视频：

```bash
vwu-video --model viduq3-pro \
  --prompt "一只可爱的猫咪在跳舞" \
  --duration 5 \
  --wait
```

### 图生视频
从静态图片生成动态视频：

```bash
vwu-video --model viduq3-pro \
  --image photo.jpg \
  --prompt "让图片中的人物跳舞" \
  --duration 5 \
  --wait
```

## ⚙️ 配置

### 1. 获取 API Key

**重要**: 使用前必须在 vwu.ai 控制台创建 API Key

1. 访问 https://vwu.ai
2. 登录账号
3. 进入**「令牌管理」**
4. 点击**「新建令牌」**
5. 设置名称（如：claw-video）
6. 复制生成的密钥

### 2. 设置环境变量

```bash
export VWU_API_KEY="sk-your-key-here"
```

**建议添加到 shell 配置文件** (~/.zshrc 或 ~/.bashrc):

```bash
echo 'export VWU_API_KEY="sk-your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## 📖 使用示例

### 基础文生视频

```bash
# 最简单的用法
vwu-video --prompt "猫咪跳舞" --wait

# 指定参数
vwu-video \
  --model viduq3-pro \
  --prompt "一朵花在风中摇曳，4K高清" \
  --duration 5 \
  --ratio 16:9 \
  --output flower.mp4 \
  --wait
```

### 图生视频

```bash
# 使用图片作为参考
vwu-video \
  --image /path/to/photo.jpg \
  --prompt "让图片中的人物开始跳舞" \
  --duration 5 \
  --output dance.mp4 \
  --wait
```

### 查询任务状态

```bash
# 查询任务状态
vwu-video --status 931029583942135808

# 下载已完成的视频
vwu-video --download 931029583942135808 --output video.mp4
```

### 高级参数

```bash
vwu-video \
  --model viduq3-pro \
  --prompt "电影级风景延时" \
  --duration 10 \
  --ratio 16:9 \
  --metadata '{"resolution":"1080p","fps":24}' \
  --wait
```

## 📋 参数说明

### 选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--model` | 模型名称 | viduq3-pro |
| `--prompt` | 视频描述（必需） | - |
| `--image` | 参考图片路径（可选） | - |
| `--duration` | 视频时长（秒） | 5 |
| `--ratio` | 宽高比 | 16:9 |
| `--output` | 输出文件名 | video_时间戳.mp4 |
| `--wait` | 等待生成完成并下载 | false |
| `--status` | 查询任务状态 | - |
| `--download` | 下载已完成的视频 | - |
| `--list-models` | 列出可用模型 | - |

### 宽高比选项

- `16:9` - 横屏（默认）
- `9:16` - 竖屏（手机视频）
- `1:1` - 方形（社交媒体）

### metadata 字段

```json
{
  "duration": 5,           // 时长 2-10 秒
  "aspect_ratio": "16:9",  // 宽高比
  "resolution": "1080p",   // 分辨率（可选）
  "fps": 24,               // 帧率（可选）
  "style": "realistic"     // 风格（可选）
}
```

## 🎯 提示词建议

### 好的提示词特征

1. **详细描述场景**
   - ✅ "一只橘色的猫咪坐在木地板上，头部左右摇摆，阳光从窗户射入"
   - ❌ "猫跳舞"

2. **指定动作和风格**
   - ✅ "人物优雅地旋转，手臂舒展，芭蕾舞风格，慢动作"
   - ❌ "人跳舞"

3. **添加质量关键词**
   - ✅ "4K高清，电影级质量，专业摄影，光线柔和"
   - ❌ "视频"

### 示例提示词

```
- "一只柯基犬在草地上奔跑，尾巴摇摆，阳光明媚"
- "城市夜景，车流延时摄影，灯光流动，高质量"
- "一朵玫瑰花慢慢绽放，花瓣层层展开，微距拍摄"
- "海浪拍打礁石，水花四溅，慢动作，日落时分"
```

## ⚠️ 限制和注意事项

### API Key 额度

- 每次生成会消耗 API key 额度
- 如提示"额度不足"，请在 vwu.ai 控制台充值
- 或创建新的 API 令牌

### 生成时间

- 通常需要 2-5 分钟
- 取决于服务器负载和视频时长
- 使用 `--wait` 参数会自动等待完成

### 视频参数

- **时长**: 建议使用 5 秒，最长 10 秒
- **分辨率**: 默认 1080p，可达 4K
- **格式**: 输出为 MP4 格式

## 🔄 API 信息

**端点**: https://api.vwu.ai/v1/videos
**文档**: https://platform.vidu.cn/docs/image-to-video
**模式**: 异步任务（创建 → 查询 → 下载）

### 任务状态

- `queued` - 队列中
- `in_progress` - 生成中
- `succeeded` / `completed` - 完成
- `failed` - 失败

## 💡 故障排除

### 常见问题

**Q: 提示"未设置 VWU_API_KEY"**
```
A: 需要先创建 API Key
   1. 访问 https://vwu.ai
   2. 登录 → 令牌管理 → 新建令牌
   3. 设置环境变量: export VWU_API_KEY='your-key'
```

**Q: 生成失败，返回错误**
```
A: 检查以下几点：
   1. API key 额度是否充足
   2. 提示词是否合规
   3. 图片格式是否正确（JPG/PNG）
   4. 查看详细错误信息
```

**Q: 视频生成时间过长**
```
A: 正常情况：
   - 文生视频: 2-4 分钟
   - 图生视频: 3-5 分钟
   - 如超过 10 分钟未完成，可能失败
```

**Q: 生成的视频质量不满意**
```
A: 优化提示词：
   1. 更详细地描述场景
   2. 添加质量关键词（4K、电影级等）
   3. 指定风格和动作
   4. 尝试不同的宽高比
```

## 📞 相关链接

- **vwu.ai 控制台**: https://vwu.ai
- **Vidu 官方文档**: https://platform.vidu.cn/docs/image-to-video
- **New API 文档**: https://docs.newapi.ai/en
- **ClawHub**: https://clawhub.com

## 🆕 更新日志

**v1.1.0** (2026-03-16)
- ✅ 修正 API 端点（api.vwu.ai）
- ✅ 添加图生视频支持
- ✅ 添加完整的 vwu-video.sh 脚本
- ✅ 更新模型列表（移除不支持的模型）
- ✅ 添加 API Key 配置指引

**v1.0.0** (2026-03-16)
- 初始版本

---

**技能维护**: Claw AI Assistant
**最后更新**: 2026-03-16
**版本**: 1.1.0
