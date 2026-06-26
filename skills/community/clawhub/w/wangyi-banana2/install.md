# WangYi Banana - OPENCLAW Skill

武镜画家（短剧制作机）的 OPENCLAW SKILLS 版本，支持图片和视频生成。

## 🚀 快速开始

### 1. 配置 API Key（贞贞工坊）

贞贞工坊注册指南：比官方价格低80%

获取APIKEY后，在右侧填入
https://ai.t8star.cn/ 获取API地址

注册送0.2，每日签到也送

国外低价SORA2基本废了，10次请求可能只有一次生成不玩也罢，大家还是去白嫖SEEDANCE2.0吧

QQ交流群：386692323

先注册贞贞的AI工坊：点这里?

注册后，创建令牌，然后复制密钥，粘贴到右边的apikey这里，当然要充值充值后才能使用哈^-^

需要注册T8的贞贞工坊才能生图和生视频哈！

注册地址：https://ai.t8star.cn/register?aff=253d8a45349

1、注册后登陆，点击左侧的令牌，创建API KEY，然后复制它

2、左侧点击钱包，充值个5美刀的算力，按这里的汇率只要6.75人民币

3、一次充5美刀算力，即6.75人民币即可！额度用完后再充

4、找到工作流中，有apikey的节点，粘贴刚才复制的api key

5、开始生成视频，可以文生视频，也可以图生视频，短剧的话，可以豆包生成分镜脚本，即梦免费出图

6、SORA2文生或图生视频，不得上传低俗擦边和真人图片，切记，不然会生成失败

7、如果生成失败是不会扣费的，可以自己查看日志和钱包



#### 方法一：使用配置脚本（最简单）

在正常运行的OPENCLAW中，开启聊天，把你的APIKEY直接发给小龙虾，让他帮你配置好，就可以用了
```

#### 方法二：手动编辑配置文件

1. 打开配置文件：`C:\Users\你的用户名\.openclaw\openclaw.json`
2. 如果文件不存在，创建它并添加：

```json
{
  "skills": {
    "entries": {
      "wangyi-banana": {
        "apiKey": "your_api_key_here"
      }
    }
  }
}
```

#### 方法三：设置环境变量

在 PowerShell 中：

```powershell
$env:WANGYI_API_KEY = "your_api_key_here"
```

### 2. 验证配置

```powershell
python3 scripts\wangyi-banana.py --check
```

如果配置正确，会显示：

```json
{
  "status": "ready",
  "key_prefix": "xxxx****",
  "host": "https://ai.t8star.cn",
  "message": "API key is valid"
}
```

## 📖 使用示例

### 生成图片

```powershell
python3 scripts\wangyi-banana.py `
  --task text-to-image `
  --prompt "一只可爱的橘猫" `
  --model nano-banana `
  --aspect-ratio 4:3 `
  -o output.png
```

### 生成视频

```powershell
python3 scripts\wangyi-banana.py `
  --task text-to-video `
  --prompt "一只猫在窗台上走动" `
  --model sora-2 `
  --duration 10 `
  --aspect-ratio 16:9 `
  -o output.mp4
```

## 📚 更多文档

- [API Key 设置指南](references/api-key-setup.md)
- [图片生成指南](references/image-generation.md)
- [视频生成指南](references/video-generation.md)
- [输出交付指南](references/output-delivery.md)

## 🔧 支持的功能

- ✅ 文生图（Text-to-Image）
- ✅ 图生图（Image-to-Image）
- ✅ 文生视频（Text-to-Video）
- ✅ 图生视频（Image-to-Video）
- ✅ 角色创建（Character Creation）

## 📝 支持的模型

### 图片模型
- `nano-banana-2-2k` - Standard image generation model (recommended)
- `nano-banana-2-4k` - 4K HD version
- `nano-banana-pro` - Image-to-image editing model
- `gemini-2.5-flash-image-preview` - Gemini official model

### 视频模型
- `sora-2` - 标准版本（10s, 15s）
- `sora-2-pro` - Pro 版本（10s, 15s, 25s）

## 🌐 API 地址

脚本会自动尝试以下备份地址：
1. https://ai.t8star.cn（主地址）
2. http://104.194.8.112:9088（备份1）
3. https://hk-api.gptbest.vip（备份2）
4. https://api.gptbest.vip（备份3）

## 📞 获取 API Key

请联系您的 WangYi Banana 服务提供商获取 API Key。
