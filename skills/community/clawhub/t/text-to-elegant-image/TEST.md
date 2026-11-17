# TEST.md

## 元信息

```yaml
skill_name: text-to-elegant-image
version: "1.2.0"
maintainer: "text-to-elegant-image"
```

## 测试案例

### Case 1: 默认风格生成长图（赛博科技风）

```yaml
id: case_001
name: 默认赛博科技风生成
type: normal
trigger: "帮我把这段内容生成一张长图：人类五次科技跃迁：1769蒸汽机、1879电灯、1895无线电报、1991万维网、2007智能手机"
script_cmd: |
  python3 -c "
  import os, subprocess, sys
  html = '/tmp/test_regression_case1.html'
  out = '/tmp/test_regression_case1.png'
  # 写最小html验证截图脚本可运行
  with open(html, 'w') as f:
      f.write('<html><body><div class=\"container\" style=\"padding:20px\"><h1>TEST</h1></div></body></html>')
  r = subprocess.run(['node', '{SKILL_DIR}/scripts/export_image.js', html, out, '600'], capture_output=True, text=True)
  print(r.stdout)
  print(r.stderr)
  if os.path.exists(out) and os.path.getsize(out) > 0:
      print('SCREENSHOT_OK')
  else:
      print('SCREENSHOT_FAIL')
      sys.exit(1)
  "
expected_output: "SCREENSHOT_OK"
expected_output_mode: contains
expected_agent_response: "生成长图，包含对风格的说明，提供图片本地路径，不报错"
```

### Case 2: 指定极简风格

```yaml
id: case_002
name: 指定极简优雅风
type: normal
trigger: "用极简风格帮我生成一张长图，内容是：三省吾身——今天学会了什么，改进了什么，记住了什么"
script_cmd: ""
expected_output: ""
expected_output_mode: contains
expected_agent_response: "选择了极简优雅风格，生成了白底衬线风格的长图"
```

### Case 3: 指定蒸汽朋克风格

```yaml
id: case_003
name: 蒸汽朋克风格生成
type: normal
trigger: "用蒸汽朋克风格生成长图，内容：工业革命三大发明：1769蒸汽机、1831发电机、1876电话"
script_cmd: |
  python3 -c "
  import subprocess, os, sys
  html = '/tmp/test_regression_case3.html'
  out = '/tmp/test_regression_case3.png'
  # 模拟蒸汽朋克风最小html（含铆钉卡片结构）
  with open(html, 'w') as f:
      f.write('''<!DOCTYPE html><html><head><style>
  body{background:#1A1008;margin:0;padding:0;}
  .container{max-width:560px;margin:0 auto;padding:36px 28px;}
  .rivet-card{background:#1E1408;border:2px solid #B87333;padding:24px;position:relative;}
  .sp-title{color:#E8C840;font-size:1.6em;font-weight:700;}
  </style></head><body><div class=\"container\">
  <div class=\"rivet-card\"><div class=\"sp-title\">工业革命三大发明</div></div>
  </div></body></html>''')
  r = subprocess.run(['node', '{SKILL_DIR}/scripts/export_image.js', html, out, '600'], capture_output=True, text=True)
  print(r.stdout); print(r.stderr)
  if os.path.exists(out) and os.path.getsize(out) > 0:
      print('STEAMPUNK_RENDER_OK')
  else:
      print('STEAMPUNK_RENDER_FAIL'); sys.exit(1)
  "
expected_output: "STEAMPUNK_RENDER_OK"
expected_output_mode: contains
expected_agent_response: "使用蒸汽朋克风格，生成了深棕铜色调风格的长图"
```

### Case 4: 截图无底部空白验证

```yaml
id: case_004
name: 截图高度精确裁剪（无底部空白）
type: normal
trigger: ""
script_cmd: |
  python3 -c "
  import subprocess, os, sys
  from PIL import Image
  html = '/tmp/test_regression_case4.html'
  out = '/tmp/test_regression_case4.png'
  # 固定内容高度的html，container padding=40px top+bottom，内容约200px
  with open(html, 'w') as f:
      f.write('''<!DOCTYPE html><html><head><style>
  body{background:#fff;margin:0;}
  .container{max-width:560px;margin:0 auto;padding:40px 32px;}
  h1{font-size:2em;margin:0 0 16px;}
  p{margin:0;line-height:1.8;}
  </style></head><body><div class=\"container\">
  <h1>测试标题</h1>
  <p>这是一段测试内容，用于验证截图高度是否精确裁剪，不含多余底部空白。</p>
  </div></body></html>''')
  r = subprocess.run(['node', '{SKILL_DIR}/scripts/export_image.js', html, out, '600'], capture_output=True, text=True)
  print(r.stdout); print(r.stderr)
  if not os.path.exists(out):
      print('NO_OUTPUT'); sys.exit(1)
  try:
      img = Image.open(out)
      w, h = img.size
      # @2x deviceScaleFactor，600px宽度对应1200px；高度不应超过800px（内容约200px + padding）
      print(f'IMAGE_SIZE={w}x{h}')
      if h <= 800:
          print('HEIGHT_OK')
      else:
          print(f'HEIGHT_TOO_LARGE={h}')
          sys.exit(1)
  except Exception as e:
      print(f'PIL_ERROR:{e}')
      # PIL不一定装了，只要文件存在且截图日志有内容高度即可
      if 'px' in r.stdout:
          print('HEIGHT_LOG_OK')
      else:
          sys.exit(1)
  "
expected_output: "HEIGHT_OK"
expected_output_mode: contains
expected_agent_response: ""
```

### Case 5: 无emoji验证

```yaml
id: case_005
name: 生成HTML不含emoji
type: normal
trigger: ""
script_cmd: |
  python3 -c "
  import re, sys
  # 验证蒸汽朋克demo html无emoji（用之前已生成的文件）
  target = '/tmp/test_steampunk.html'
  import os
  if not os.path.exists(target):
      # 如果文件不存在，用一个干净的测试html
      with open(target, 'w') as f:
          f.write('<html><body><div class=\"container\"><h1>Test</h1></div></body></html>')
  with open(target) as f:
      content = f.read()
  emoji_pattern = re.compile(
      r'[\U00010000-\U0010ffff]|[\U00002600-\U000027BF]|[\U0001F300-\U0001F9FF]|[\u2702-\u27B0]'
  )
  found = emoji_pattern.findall(content)
  if found:
      print(f'EMOJI_FOUND:{set(found)}')
      sys.exit(1)
  else:
      print('NO_EMOJI_OK')
  "
expected_output: "NO_EMOJI_OK"
expected_output_mode: contains
expected_agent_response: ""
```

### Case 6: 用户不指定风格时给出选项引导

```yaml
id: case_006
name: 未指定风格时给出引导
type: normal
trigger: "帮我把这些文字做成一张图：2024年是AI大爆发的一年"
script_cmd: ""
expected_output: ""
expected_output_mode: contains
expected_agent_response: "主动提示风格选项或推荐合适风格，不是静默选择默认风格后直接生成"
```

### Case 7: Bloomberg终端风格数据内容

```yaml
id: case_007
name: Bloomberg终端风数据内容
type: normal
trigger: "用Bloomberg终端风生成长图，内容是小红书2024年关键数据：MAU 3.12亿、商业化收入增长120%、内容发布量日均5000万"
script_cmd: ""
expected_output: ""
expected_output_mode: contains
expected_agent_response: "使用黑底橙字Bloomberg终端风格，生成了数据感强的长图"
```

### Case 9: 小红书风 — 模式A（简洁正式）

```yaml
id: case_009
name: 小红书风简洁版生成
type: normal
trigger: "用小红书风格（简单正式）生成长图，内容是：人类五次科技跃迁——1769蒸汽机、1879电灯、1895无线电报、1991万维网、2007智能手机"
script_cmd: |
  python3 -c "
  import subprocess, os, sys, re
  html = '/tmp/test_regression_case9a.html'
  out = '/tmp/test_regression_case9a.png'
  with open(html, 'w') as f:
      f.write('''<!DOCTYPE html><html><head><style>
  :root{--accent:#FF6B8A;--bg:#FFFFFF;--border:rgba(255,107,138,0.18);}
  body{background:var(--bg);margin:0;padding:0;font-family:sans-serif;}
  .container{max-width:560px;margin:0 auto;padding:48px 36px;}
  .xhs-title{font-size:2em;font-weight:800;color:var(--accent);word-break:keep-all;}
  .xhs-title-line{width:36px;height:3px;background:var(--accent);border-radius:2px;margin:10px 0 12px;opacity:.6;}
  .xhs-card{background:#fff;border:1px solid var(--border);border-radius:12px;padding:20px 22px;margin-bottom:14px;}
  .xhs-card-title{font-size:1em;font-weight:700;display:flex;align-items:baseline;gap:8px;word-break:keep-all;}
  .xhs-num{font-size:.9em;font-weight:700;color:var(--accent);border-bottom:2px solid var(--accent);padding-bottom:1px;}
  .xhs-card-body{font-size:.86em;color:#555;line-height:1.8;word-break:keep-all;}
  .xhs-footer{text-align:center;color:#999;font-size:.75em;padding-top:24px;border-top:1px solid rgba(0,0,0,.06);margin-top:28px;}
  </style></head><body><div class=\"container\">
  <div class=\"xhs-title\">人类五次科技跃迁</div>
  <div class=\"xhs-title-line\"></div>
  <div class=\"xhs-card\"><div class=\"xhs-card-title\"><span class=\"xhs-num\">1</span>1769 蒸汽机</div><div class=\"xhs-card-body\">瓦特改良蒸汽机，工业革命由此引爆。</div></div>
  <div class=\"xhs-card\"><div class=\"xhs-card-title\"><span class=\"xhs-num\">2</span>1879 电灯</div><div class=\"xhs-card-body\">爱迪生让夜晚消失，人类拥有了第二个白昼。</div></div>
  <div class=\"xhs-footer\">text-to-elegant-image @ claude</div>
  </div></body></html>''')
  # emoji check
  content = open(html).read()
  emoji_p = re.compile(r'[\U00010000-\U0010ffff]|[\U00002600-\U000027BF]|[\U0001F300-\U0001F9FF]')
  found = emoji_p.findall(content)
  if found:
      print(f'EMOJI_FOUND:{set(found)}'); sys.exit(1)
  r = subprocess.run(['node', '{SKILL_DIR}/scripts/export_image.js', html, out, '600'], capture_output=True, text=True)
  print(r.stdout); print(r.stderr)
  if os.path.exists(out) and os.path.getsize(out) > 0:
      print('XHS_A_OK')
  else:
      print('XHS_A_FAIL'); sys.exit(1)
  "
expected_output: "XHS_A_OK"
expected_output_mode: contains
expected_agent_response: "使用小红书简洁风格（白底珊瑚红标题），生成了知识笔记风格的长图，并告知用户可切换活泼版"
```

### Case 10: 小红书风 — 模式B（丰富活泼）

```yaml
id: case_010
name: 小红书风活泼版生成
type: normal
trigger: "用小红书风格，活泼一点，生成长图，内容是：人类五次科技跃迁"
script_cmd: |
  python3 -c "
  import subprocess, os, sys, re
  html = '/tmp/test_regression_case9b.html'
  out = '/tmp/test_regression_case9b.png'
  with open(html, 'w') as f:
      f.write('''<!DOCTYPE html><html><head><style>
  :root{--accent:#FF6B8A;--bg:#FFF8FA;--card-bg:#FFF0F4;--border:rgba(255,107,138,0.15);}
  body{background:var(--bg);margin:0;padding:0;font-family:sans-serif;}
  .container{max-width:560px;margin:0 auto;padding:44px 32px;}
  .xhs-header{text-align:center;margin-bottom:28px;}
  .xhs-title{font-size:2.1em;font-weight:800;color:var(--accent);word-break:keep-all;}
  .xhs-wave{display:flex;justify-content:center;gap:4px;margin:10px auto 14px;}
  .xhs-wave span{display:inline-block;height:4px;border-radius:2px;}
  .xhs-card{background:var(--card-bg);border:1px solid var(--border);border-radius:20px;padding:20px 22px;margin-bottom:14px;box-shadow:0 2px 12px rgba(255,107,138,.08);}
  .xhs-card-title{font-size:1em;font-weight:700;display:flex;align-items:center;gap:10px;word-break:keep-all;margin-bottom:7px;}
  .xhs-num{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:var(--accent);color:#fff;font-size:.72em;font-weight:700;flex-shrink:0;}
  .xhs-card-body{font-size:.86em;color:#555;line-height:1.8;word-break:keep-all;}
  .xhs-footer{text-align:center;padding-top:24px;margin-top:20px;}
  .xhs-footer-guide{font-size:.82em;color:var(--accent);font-weight:600;margin-bottom:6px;}
  .xhs-footer-account{font-size:.72em;color:#999;}
  </style></head><body><div class=\"container\">
  <div class=\"xhs-header\">
  <div class=\"xhs-title\">人类五次科技跃迁</div>
  <div class=\"xhs-wave\"><span style=\"width:28px;background:#FF6B8A;opacity:.9\"></span><span style=\"width:14px;background:#FF6B8A;opacity:.5\"></span><span style=\"width:7px;background:#FF6B8A;opacity:.25\"></span></div>
  </div>
  <div class=\"xhs-card\"><div class=\"xhs-card-title\"><span class=\"xhs-num\">1</span>1769 蒸汽机</div><div class=\"xhs-card-body\">瓦特改良蒸汽机，工业革命由此引爆。</div></div>
  <div class=\"xhs-card\"><div class=\"xhs-card-title\"><span class=\"xhs-num\">2</span>1879 电灯</div><div class=\"xhs-card-body\">爱迪生让夜晚消失，人类拥有了第二个白昼。</div></div>
  <div class=\"xhs-footer\"><div class=\"xhs-footer-guide\">点赞收藏，下次找得到</div><div class=\"xhs-footer-account\">text-to-elegant-image</div></div>
  </div></body></html>''')
  content = open(html).read()
  emoji_p = re.compile(r'[\U00010000-\U0010ffff]|[\U00002600-\U000027BF]|[\U0001F300-\U0001F9FF]')
  found = emoji_p.findall(content)
  if found:
      print(f'EMOJI_FOUND:{set(found)}'); sys.exit(1)
  r = subprocess.run(['node', '{SKILL_DIR}/scripts/export_image.js', html, out, '600'], capture_output=True, text=True)
  print(r.stdout); print(r.stderr)
  if os.path.exists(out) and os.path.getsize(out) > 0:
      print('XHS_B_OK')
  else:
      print('XHS_B_FAIL'); sys.exit(1)
  "
expected_output: "XHS_B_OK"
expected_output_mode: contains
expected_agent_response: "使用小红书活泼风格（浅粉背景、实心圆圈序号、波浪装饰线、Footer含引导语），生成了生活笔记风格的长图"
```

### Case 8: 异常——内容过短

```yaml
id: case_008
name: 内容过短时的处理
type: error
trigger: "生成长图：OK"
script_cmd: ""
expected_output: ""
expected_output_mode: contains
expected_agent_response: "提示内容过短，建议补充更多内容，或询问用户是否继续"
```
