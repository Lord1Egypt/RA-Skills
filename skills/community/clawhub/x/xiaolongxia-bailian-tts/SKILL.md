# Bailian TTS Skill

百炼 TTS 语音合成技能，基于阿里通义千问 qwen3-tts 大模型，支持 50+ 种系统音色、多语言、方言及指令控制。

## 支持的模型

- `qwen3-tts-flash` - 默认模型，稳定版，通用语音合成
- `qwen3-tts-instruct-flash` - 支持指令控制，适合情感化配音、有声书、广播剧
- `qwen3-tts-vd-2026-01-26` - 声音设计，基于文本描述创建定制音色
- `qwen3-tts-vc-2026-01-22` - 声音复刻，基于音频样本复刻音色

## 系统音色（50+种）

### 中文普通话（热门推荐）

- `Cherry` (芊悦, 女) - 阳光积极、亲切自然（默认女声）
- `Ethan` (晨煦, 男) - 阳光温暖、活力朝气（默认男声）
- `Momo` (茉兔, 女) - 撒娇搞怪、逗你开心
- `Dylan` (晓东, 男) - 北京胡同里长大的少年
- `Bella` (萌宝, 女) - 喝酒不打醉拳的小萝莉
- `Serena` (苏瑶, 女) - 温柔小姐姐
- `Vivian` (十三, 女) - 拽拽的、可爱的小暴躁
- `Moon` (月白, 男) - 率性帅气
- `Neil` (阿闻, 男) - 专业新闻主持人

### 中文方言

- `Jada` (上海-阿珍) - 上海话，风风火火的沪上阿姐
- `Dylan` (北京-晓东) - 北京话，北京胡同里长大的少年
- `Sunny` (四川-晴儿) - 四川话，甜到你心里的川妹子
- `Eric` (四川-程川) - 四川话，跳脱市井的成都男子
- `Rocky` (粤语-阿强) - 粤语，幽默风趣的阿强
- `Kiki` (粤语-阿清) - 粤语，甜美的港妹闺蜜
- `Li` (南京-老李) - 南京话，耐心的瑜伽老师
- `Marcus` (陕西-秦川) - 陕西话，面宽话短、心实声沉
- `Roy` (闽南-阿杰) - 闽南语，诙谐直爽的台湾哥仔
- `Peter` (天津-李彼得) - 天津话，天津相声，专业捧哏

### 外语音色

- `Jennifer` (詹妮弗) - 英语，品牌级、电影质感美语女声
- `Ryan` (甜茶) - 英语，节奏拉满、戏感炸裂
- `Bodega` (博德加) - 西班牙语，热情的西班牙大叔
- `Sonrisa` (索尼莎) - 西班牙语，热情开朗的拉美大姐
- `Alek` (阿列克) - 俄语，战斗民族的冷与暖
- `Dolce` (多尔切) - 意大利语，慵懒的意大利大叔
- `Sohee` (素熙) - 韩语，温柔开朗的韩国欧尼
- `Ono Anna` (小野杏) - 日语，鬼灵精怪的青梅竹马
- `Lenn` (莱恩) - 德语，穿西装也听后朋克的德国青年
- `Emilien` (埃米尔安) - 法语，浪漫的法国大哥哥

### 特色角色音

- `Eldric Sage` (沧明子, 男) - 沉稳睿智的老者，沧桑如松
- `Mia` (乖小妹, 女) - 温顺如春水，乖巧如初雪
- `Mochi` (沙小弥, 男) - 聪明伶俐的小大人
- `Bellona` (燕铮莺, 女) - 金戈铁马入梦来，字正腔圆
- `Vincent` (田叔, 男) - 沙哑烟嗓，道尽千军万马
- `Arthur` (徐大爷, 男) - 被岁月和旱烟浸泡过的质朴嗓音
- `Nini` (邻家妹妹, 女) - 糯米糍一样又软又黏
- `Stella` (少女阿月, 女) - 代表月亮消灭你
- `Radio Gol` (拉迪奥·戈尔, 男) - 足球诗人，用名字解说足球

## 使用方法

### 命令行

```bash
# 基础使用（默认音色 Cherry）
python3 scripts/tts.py "你好，这是测试"

# 指定音色
python3 scripts/tts.py "你好，这是测试" --voice Ethan

# 指定输出文件
python3 scripts/tts.py "你好，这是测试" --output /tmp/test.opus

# 指定模型（instruct 版支持指令控制）
python3 scripts/tts.py "你好" --voice Cherry --model qwen3-tts-instruct-flash --instructions "语速较快，充满活力"

# 方言合成
python3 scripts/tts.py "你好呀" --voice Sunny --language_type Chinese

# 外语合成
python3 scripts/tts.py "Hello world" --voice Jennifer --language_type English

# 查看所有音色
python3 scripts/tts.py --list-voices
```

### Python API

```python
from scripts.tts import generate_tts

# 基础合成
result = generate_tts(
    text="你好，这是测试",
    voice="Cherry",
    output_file="/tmp/output.opus"
)

# 指令控制（仅 instruct 模型支持）
result = generate_tts(
    text="今天是个好日子",
    voice="Cherry",
    model="qwen3-tts-instruct-flash",
    instructions="语速较快，带有明显的上扬语调，充满活力",
    output_file="/tmp/output.opus"
)

# 方言合成
result = generate_tts(
    text="你好呀",
    voice="Sunny",  # 四川话
    language_type="Chinese",
    output_file="/tmp/output.opus"
)
```

## 配置

需要设置百炼 API Key：

```bash
export DASHSCOPE_API_KEY="sk-your-api-key"
```

或在代码中传入：

```python
generate_tts("你好", voice="Cherry", api_key="sk-your-api-key")
```

## 依赖

```bash
pip3 install dashscope requests
```

## 参数说明

- `text` (str, 必填) - 要合成的文本
- `voice` (str, default: Cherry) - 音色名称
- `model` (str, default: qwen3-tts-flash) - 模型名称
- `language_type` (str, default: Chinese) - 语言类型（Chinese/English等）
- `instructions` (str, optional) - 指令控制（仅instruct模型）
- `stream` (bool, default: False) - 是否流式输出
- `output_file` (str, optional) - 输出文件路径

## 价格

- 中国内地：0.8元/万字符
- 国际：0.8元/万字符（部分模型略有差异）

## 官方文档

- [语音合成-千问官方文档](https://help.aliyun.com/zh/model-studio/qwen-tts)
- [声音复刻](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)
- [声音设计](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)
