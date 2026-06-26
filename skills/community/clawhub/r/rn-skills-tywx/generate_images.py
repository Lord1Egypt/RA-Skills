#!/usr/bin/env python3
import subprocess
import json
import os
import time

# 尝试从环境变量获取，如果不存在则从 ~/.zshrc 读取
API_KEY = os.environ.get('DASHSCOPE_API_KEY')
if not API_KEY:
    # 从 ~/.zshrc 读取
    zshrc_path = os.path.expanduser('~/.zshrc')
    if os.path.exists(zshrc_path):
        with open(zshrc_path, 'r') as f:
            for line in f:
                if line.startswith('export DASHSCOPE_API_KEY='):
                    API_KEY = line.strip().split('=', 1)[1]
                    break
    
if not API_KEY:
    print("错误：未找到 DASHSCOPE_API_KEY 环境变量")
    exit(1)

# 春日空气感叠穿图片 prompt
prompts_airy = [
    "一位年轻女性穿着浅蓝色薄纱开衫和白色吊带背心，搭配米色高腰阔腿裤，站在公园花丛中，空气感叠穿风格，春日清新穿搭，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着浅蓝色薄纱开衫和白色吊带，搭配珍珠项链和小巧耳钉，站在咖啡厅门口，空气感叠穿风格，春日清新穿搭，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着浅蓝色薄纱开衫和米色阔腿裤，搭配细款编织腰带，站在简约建筑前，空气感叠穿风格，春日清新穿搭，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着白色吊带背心和浅蓝色薄纱开衫，搭配白色平底单鞋，坐在咖啡厅窗边，空气感叠穿风格，春日清新穿搭，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着浅蓝色薄纱开衫和米色阔腿裤，衣摆飘动，走在春日街道上，空气感叠穿风格，春日清新穿搭，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着浅蓝色薄纱开衫和白色吊带，搭配米色阔腿裤和珍珠项链，站在公园树下微笑，空气感叠穿风格，春日清新穿搭，专业时尚摄影，高清画质，竖版构图"
]

# 新中式茶道穿搭 prompt
prompts_tea = [
    "一位年轻女性穿着淡青色改良款对襟衫和米白色内搭，搭配深青色禅意阔腿裤，站在茶室庭院中，新中式茶道美学风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着淡青色对襟衫和棉麻材质上衣，搭配玉石手串和银质吊坠，手持茶具，新中式茶道美学风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着淡青色对襟衫和深青色阔腿裤，搭配同色系织带腰带，站在素雅背景前，新中式茶道美学风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着米白色内搭和淡青色对襟衫，搭配布面禅意鞋，坐在茶室中斟茶，新中式茶道美学风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着淡青色对襟衫和深青色阔腿裤，低头品茶侧颜，新中式茶道美学风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着淡青色对襟衫和米白色内搭，搭配深青色阔腿裤，站在庭院树下，新中式茶道美学风格，专业时尚摄影，高清画质，竖版构图"
]

# Clean Fit 极简通勤 prompt
prompts_clean = [
    "一位年轻女性穿着白色高支数棉质衬衫和浅灰色西装马甲，搭配黑色高腰直筒西裤，站在现代化办公楼前，Clean Fit 极简通勤风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着白色衬衫和灰色马甲，搭配黑色皮带和黑色乐福鞋，手拿咖啡杯走在写字楼大堂，Clean Fit 极简通勤风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着白色衬衫和浅灰马甲，搭配黑色西裤和极简金属手表，坐在办公室窗边，Clean Fit 极简通勤风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着白色高支衬衫和灰色西装马甲，搭配黑色直筒裤，站在简约咖啡厅，Clean Fit 极简通勤风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着白衬衫灰马甲黑西裤，搭配黑色乐福鞋和小巧耳钉，自然行走姿态，Clean Fit 极简通勤风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着白色衬衫和浅灰色马甲，搭配黑色高腰西裤，站在办公楼电梯口，Clean Fit 极简通勤风格，专业时尚摄影，高清画质，竖版构图"
]

# 复古港风约会穿搭 prompt
prompts_retro = [
    "一位年轻女性穿着酒红色丝绒吊带上衣和黑色高腰 A 字长裙，搭配金色大耳环，站在霓虹灯下的老式建筑前，复古港风约会风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着酒红色丝绒上衣和黑色长裙，搭配短款小香风外套，红唇卷发，站在西餐厅门口，复古港风约会风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着酒红吊带和黑裙，搭配复古项链和金色耳环，侧身回眸姿态，夜晚霓虹灯背景，复古港风约会风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着酒红色丝绒吊带和黑色 A 字裙，搭配黑色尖头高跟鞋，慵懒坐在复古沙发，复古港风约会风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着酒红上衣和黑色长裙，外搭小香风外套，红唇微卷长发，站在夜晚街道上，复古港风约会风格，专业时尚摄影，高清画质，竖版构图",
    "一位年轻女性穿着酒红色丝绒吊带和黑色高腰裙，搭配金色配饰，优雅站立姿态，复古港风氛围，专业时尚摄影，高清画质，竖版构图"
]

def submit_task(prompt):
    cmd = f'''curl -s "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer {API_KEY}" \\
  -H "X-DashScope-Async: enable" \\
  -d '{{
    "model": "wanx2.1-t2i-turbo",
    "input": {{
      "prompt": "{prompt}"
    }},
    "parameters": {{
      "size": "720*1280",
      "n": 1
    }}
  }}'
'''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def get_task_status(task_id):
    cmd = f'''curl -s "https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}" \\
  -H "Authorization: Bearer {API_KEY}"
'''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def download_image(url, output_path):
    cmd = f'curl -s "{url}" -o "{output_path}"'
    subprocess.run(cmd, shell=True)

print("=" * 60)
print("开始生成穿搭图片...")
print("=" * 60)

# 存储所有任务 ID 和对应的输出路径
all_tasks = []

# 春日空气感叠穿
print("\n🌿 [1/4] 春日空气感叠穿...")
airy_dir = "/Users/yk/Documents/work/skills/rn-skills/output/2026-03-15_春日空气感叠穿"
for i, prompt in enumerate(prompts_airy):
    print(f"  提交任务 {i+1}/6...")
    response = submit_task(prompt)
    try:
        resp_json = json.loads(response)
        task_id = resp_json.get('output', {}).get('task_id')
        if task_id:
            all_tasks.append((task_id, f"{airy_dir}/page_{i}.png", f"春日空气感_{i}"))
            print(f"  ✓ 任务 ID: {task_id}")
    except:
        print(f"  ✗ 提交失败：{response}")

# 新中式茶道穿搭
print("\n🍵 [2/4] 新中式茶道春日穿搭...")
tea_dir = "/Users/yk/Documents/work/skills/rn-skills/output/2026-03-15_新中式茶道春日穿搭"
for i, prompt in enumerate(prompts_tea):
    print(f"  提交任务 {i+1}/6...")
    response = submit_task(prompt)
    try:
        resp_json = json.loads(response)
        task_id = resp_json.get('output', {}).get('task_id')
        if task_id:
            all_tasks.append((task_id, f"{tea_dir}/page_{i}.png", f"新中式_{i}"))
            print(f"  ✓ 任务 ID: {task_id}")
    except:
        print(f"  ✗ 提交失败：{response}")

# Clean Fit 极简通勤
print("\n💼 [3/4] Clean Fit 极简通勤...")
clean_dir = "/Users/yk/Documents/work/skills/rn-skills/output/2026-03-23_Clean Fit 极简通勤"
for i, prompt in enumerate(prompts_clean):
    print(f"  提交任务 {i+1}/6...")
    response = submit_task(prompt)
    try:
        resp_json = json.loads(response)
        task_id = resp_json.get('output', {}).get('task_id')
        if task_id:
            all_tasks.append((task_id, f"{clean_dir}/page_{i}.png", f"CleanFit_{i}"))
            print(f"  ✓ 任务 ID: {task_id}")
    except:
        print(f"  ✗ 提交失败：{response}")

# 复古港风约会穿搭
print("\n🌹 [4/4] 复古港风约会穿搭...")
retro_dir = "/Users/yk/Documents/work/skills/rn-skills/output/2026-03-23_复古港风约会穿搭"
for i, prompt in enumerate(prompts_retro):
    print(f"  提交任务 {i+1}/6...")
    response = submit_task(prompt)
    try:
        resp_json = json.loads(response)
        task_id = resp_json.get('output', {}).get('task_id')
        if task_id:
            all_tasks.append((task_id, f"{retro_dir}/page_{i}.png", f"港风_{i}"))
            print(f"  ✓ 任务 ID: {task_id}")
    except:
        print(f"  ✗ 提交失败：{response}")

print(f"\n✅ 共提交 {len(all_tasks)} 个任务，等待生成完成...")

# 等待并下载图片
completed = 0
while completed < len(all_tasks):
    completed = 0
    for task_id, output_path, name in all_tasks:
        if os.path.exists(output_path):
            completed += 1
            continue
        
        status_resp = get_task_status(task_id)
        try:
            status_json = json.loads(status_resp)
            task_status = status_json.get('output', {}).get('task_status', 'PENDING')
            
            if task_status == 'SUCCEEDED':
                image_url = status_json.get('output', {}).get('results', [{}])[0].get('url')
                if image_url:
                    print(f"  ⬇️ 下载 {name}...")
                    download_image(image_url, output_path)
                    completed += 1
            elif task_status == 'FAILED':
                print(f"  ✗ {name} 生成失败")
                completed += 1
        except Exception as e:
            print(f"  ? {name} 状态检查异常：{e}")
    
    if completed < len(all_tasks):
        print(f"  等待中... 已完成 {completed}/{len(all_tasks)}")
        time.sleep(5)

print("\n" + "=" * 60)
print("🎉 所有图片生成完成！")
print("=" * 60)

# 为每个目录生成 cover.png（使用第一张图片）
print("\n生成封面图...")
for dir_path, prefix in [
    (airy_dir, "春日空气感"),
    (tea_dir, "新中式"),
    (clean_dir, "CleanFit"),
    (retro_dir, "港风")
]:
    page0 = f"{dir_path}/page_0.png"
    cover = f"{dir_path}/cover.png"
    if os.path.exists(page0) and not os.path.exists(cover):
        subprocess.run(f'cp "{page0}" "{cover}"', shell=True)
        print(f"  ✓ {cover}")

print("\n✅ 全部完成！")
