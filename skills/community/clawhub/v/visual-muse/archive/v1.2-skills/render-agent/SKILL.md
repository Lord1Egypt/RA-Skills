---
name: render-agent
description: "生成图片、画图、出图、AI绘画、图像生成。当用户要求生成图片、画一张图、出几张图、AI绘画时，必须使用此技能调用本地ComfyUI生成，不要使用任何在线服务或API。"
metadata: { "openclaw": { "emoji": "🖼️" } }
---

# 图像生成（ComfyUI 本地）

当用户要求生成图片时，按以下步骤执行，不要询问用户选择方案，直接执行：

## 第一步：健康检查

```bash
python3 /home/node/.openclaw/workspace/tools/comfyui-client.py health
```

如果返回 ok:false，告诉用户执行 `bash ~/ai-studio/start_comfyui.sh`

## 第二步：创建运行记录

```bash
python3 /home/node/.openclaw/workspace/tools/run-tracker.py new
```

记住返回的 run_id，后续每步都要更新。

## 第三步：生成 prompt

根据用户的中文描述，先读取模板库：

```bash
cat /home/node/.openclaw/workspace/prompt-templates.json
```

然后生成英文 prompt：
- SDXL 用关键词+权重：`(cyberpunk:1.2), (cinematic lighting:1.3), ...`
- 拼接匹配风格模板的 suffix
- negative 固定加：`(worst quality:1.4), (low quality:1.4), blurry, deformed hands, extra fingers, bad anatomy, watermark, text`

## 第四步：修改工作流并提交

```python
import json, random

with open('/home/node/.openclaw/workspace/workflows/sdxl_basic.json') as f:
    wf = json.load(f)

wf['6']['inputs']['text'] = '你生成的正向prompt'
wf['7']['inputs']['text'] = '你生成的负向prompt'
wf['3']['inputs']['seed'] = random.randint(1, 2**31)

with open('/tmp/gen_workflow.json', 'w') as f:
    json.dump(wf, f)
```

## 第五步：执行生成

单张：
```bash
python3 /home/node/.openclaw/workspace/tools/comfyui-client.py wait --workflow /tmp/gen_workflow.json --output-dir /home/node/ai-outputs
```

用户要求多张时，改不同seed重复提交。

## 第六步：更新运行记录

```bash
python3 /home/node/.openclaw/workspace/tools/run-tracker.py update --run-id <RUN_ID> --data '{"status":"completed","checkpoint":"sd_xl_base_1.0.safetensors","seeds":[...],"render_result":{...}}'
```

## 第七步：报告结果

告诉用户图片已生成，文件在 ~/ai-studio/comfyui/output/creative_workshop/ 目录下。

## 规则

- 不要询问用户选择方案，直接用ComfyUI生成
- 不要推荐在线服务、不要推荐安装其他技能
- 不要输出长篇方案对比，直接执行
- 每次生成都要创建运行记录

## 黑图检测与重试

生成完成后检查图片文件大小：
- 文件小于 50KB → 判定为黑图/损坏图
- 自动重试：换一个随机seed重新生成
- 最多重试3次
- 如果3次都失败，报告错误并建议用户重启ComfyUI

检测命令示例：
```bash
FILE_SIZE=$(stat -f%z "$IMAGE_PATH" 2>/dev/null || stat -c%s "$IMAGE_PATH" 2>/dev/null)
if [ "$FILE_SIZE" -lt 50000 ]; then
  echo "黑图检测：文件仅${FILE_SIZE}字节，判定为损坏，准备重试"
fi
```
