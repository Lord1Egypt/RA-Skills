# 豆包 SeedTTS 2.0 故障排查指南

---

## 🔍 常见问题

### 1. 缺少必要配置

**错误信息**：
```
ValueError: 缺少必要配置：APP_ID, ACCESS_TOKEN
请设置环境变量或在 openclaw.json 中配置
```

**原因**：未配置火山引擎凭证

**解决方案**：

**方式一：环境变量**（推荐）
```bash
export VOLCANO_APP_ID="你的 APP ID"
export VOLCANO_ACCESS_TOKEN="你的 Access Token"
```

**方式二：OpenClaw 配置**
```json
{
  "skills": {
    "entries": {
      "seedtts2": {
        "env": {
          "VOLCANO_APP_ID": "你的 APP ID",
          "VOLCANO_ACCESS_TOKEN": "你的 Access Token"
        }
      }
    }
  }
}
```

**验证配置**：
```bash
# 检查环境变量
echo $VOLCANO_APP_ID
echo $VOLCANO_ACCESS_TOKEN

# 测试调用
seedtts2 "测试" -o test.mp3
```

---

### 2. 认证失败（401 Unauthorized）

**错误信息**：
```
请求失败：{"message": "Unauthorized"}
```

**原因**：
- Access Token 错误
- Token 格式错误
- Token 已过期

**解决方案**：

1. **检查 Token 是否正确**
   - 登录火山引擎控制台
   - 进入「应用管理」
   - 确认 Access Token 正确复制

2. **检查 Token 格式**
   - 正确格式：`Bearer; {token}`（注意**分号后有空格**）
   - 错误格式：`Bearer;{token}`（缺少空格）

3. **重新获取 Token**
   - 在控制台重新生成 Access Token
   - 更新配置后重试

---

### 3. 音色不可用（403 Forbidden）

**错误信息**：
```
请求失败：{"message": "Forbidden"}
```

**原因**：该音色需要单独开通

**解决方案**：

1. 登录火山引擎控制台
2. 进入「语音合成」→「音色管理」
3. 查看音色状态：
   - ✅ 已开通 → 可直接使用
   - ⚠️ 未开通 → 点击开通
   - ❌ 已过期 → 需续费

4. **免费音色**（无需开通）：
   - `zh_male_ruyayichen_uranus_bigtts`（儒雅逸辰 2.0）
   - `zh_female_vv_uranus_bigtts`（Vivi 2.0）
   - `zh_male_m191_uranus_bigtts`（云舟）
   - 等通用场景音色

---

### 4. 音频无法播放

**现象**：生成成功但无法播放

**解决方案**：

**macOS**：
```bash
# 使用系统播放器
afplay output.mp3
```

**Linux**：
```bash
# 安装 alsa-utils
sudo apt install alsa-utils

# 播放
aplay output.mp3
```

**Windows**：
```cmd
start output.mp3
```

**Python 播放**：
```python
from tts_client import SeedTTS2

tts = SeedTTS2()
tts.say_and_play("你好")  # 自动播放
```

---

### 5. 响应解析失败

**错误信息**：
```
❌ 未获取到音频数据
```

**原因**：API 响应格式变化或网络问题

**解决方案**：

1. **检查网络连接**
   ```bash
   curl -I https://openspeech.bytedance.com
   ```

2. **检查 API 端点**
   - 确认使用的是 v3 接口
   - URL：`https://openspeech.bytedance.com/api/v3/tts/unidirectional`

3. **打印原始响应**（调试用）
   ```python
   import requests
   
   # ... 发送请求后
   for line in response.iter_lines():
       if line:
           print(line.decode('utf-8'))  # 打印原始响应
   ```

---

### 6. 生成速度慢

**现象**：每次生成需要 10-30 秒

**原因**：
- 网络延迟
- 音频较长
- 服务器负载

**解决方案**：

1. **使用更短的文本**
   - 单次合成建议 < 200 字
   - 长文本分段合成

2. **批量生成**
   ```python
   tts.batch_generate([
       {"text": "第一句"},
       {"text": "第二句"},
   ])
   ```

3. **检查网络**
   ```bash
   ping openspeech.bytedance.com
   ```

---

### 7. 音色列表为空

**现象**：`seedtts2 --list` 返回空列表

**原因**：配置未加载

**解决方案**：
```bash
# 检查环境变量
env | grep VOLCANO

# 显式设置环境变量
export VOLCANO_APP_ID="xxx"
export VOLCANO_ACCESS_TOKEN="xxx"
seedtts2 --list
```

---

## 🛠️ 调试技巧

### 1. 启用详细输出

```python
from tts_client import SeedTTS2
import logging

logging.basicConfig(level=logging.DEBUG)

tts = SeedTTS2()
tts.say("测试")
```

### 2. 测试连接

```python
import requests

headers = {
    "X-Api-App-Id": "你的 APP_ID",
    "X-Api-Access-Key": "你的 ACCESS_TOKEN",
    "X-Api-Resource-Id": "seed-tts-2.0",
}

response = requests.post(
    "https://openspeech.bytedance.com/api/v3/tts/unidirectional",
    headers=headers,
    json={
        "user": {"uid": "test"},
        "req_params": {
            "text": "测试",
            "speaker": "zh_male_ruyayichen_uranus_bigtts",
        }
    },
    timeout=10
)

print(f"状态码：{response.status_code}")
print(f"响应：{response.text[:200]}")
```

### 3. 检查配置文件

```bash
# 查看 OpenClaw 配置
cat ~/.openclaw/openclaw.json | jq '.skills.entries.seedtts2'

# 检查环境变量
env | grep VOLCANO
```

---

## 📞 获取帮助

1. **查看文档**
   - [部署手册](volcano-tts2-deployment-guide.md)
   - [音色库](voice-library.md)
   - [复盘报告](tts2-debug-retrospective.md)

2. **提交 Issue**
   - GitHub Issues
   - ClawHub 社区

3. **联系支持**
   - 火山引擎工单系统
   - OpenClaw 社区 Discord

---

**最后更新**: 2026-03-24  
**版本**: 1.0.0
