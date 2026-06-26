import urllib.request
import urllib.parse
import json
import csv
import os
import re
import time

api_key = 'sk-134d7a53ebab42e4ac5af93ea28e5f13'

# 文件路径 - 已更新为 zfm_demo_02
REGIONS_FILE = r'C:\Users\zhufangming\Desktop\zfm_demo_02\地区.txt'
OUTPUT_FILE = r'C:\Users\zhufangming\Desktop\zfm_demo_02\政策.csv'
PROGRESS_FILE = r'C:\Users\zhufangming\Desktop\zfm_demo_02\进度.txt'


def read_regions():
    """从地区.txt读取所有地区"""
    with open(REGIONS_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    regions = []
    for line in lines:
        line = line.strip()
        # 跳过空行和注释行
        if not line or line.startswith('#'):
            continue
        # 跳过特殊格式的行（如带括号的说明）
        if '（' in line and '）' in line and '→' not in line:
            # 提取箭头前的有效部分
            match = re.search(r'([^（]+)', line)
            if match:
                line = match.group(1).strip()
        regions.append(line)
    return regions


def call_deepseek(location):
    """用DeepSeek查询政策，返回结构化描述内容"""
    prompt = f'''请查找"{location}"地区编程/科技特长生升学政策。

请按以下格式要求输出内容：
1. 小升初最多返回1条，初升高至少返回1条（最多2条）
2. 【重要】赛事/项目名称必须满足以下要求：
   - 优先选择Python白名单相关赛事（教育部认可的编程竞赛白名单）
   - 允许的赛事类型：
     * Python编程赛/Python创意编程赛
     * 全国青少年Python编程竞赛
     * 中国电子学会青少年Python编程等级测试
     * NOC大赛Python赛项
     * 全国青少年科技创新大赛（科技创新成果类）
     * 青少年机器人竞赛（不含图形化编程类）
     * 青少年电子信息智能创新大赛
     * 人工智能相关竞赛（创意编程、算法类）
     * 计算机综合创意类竞赛

   - 【禁止出现】以下赛事绝对不允许填写：
     * 图形化编程类（如Scratch、Blockly、图形化编程等）
     * 蓝桥杯/BlueCloud（蓝桥杯青少年创意编程组）
     * NOI系列（全国青少年信息学奥林匹克竞赛、NOIP、CSP-J/S、IOI等）
     * C++信息学奥赛相关

3. 每条"对升学的具体帮助"描述必须包含以下要素：
   - 【年份】：哪一年的招生简章或政策文件
   - 【招生人数】：具体数字（如：招收3人、招收5人、无名额限制）
   - 【报名条件】：需要什么级别的奖项（市级一等奖、省级二等奖、国家级三等奖等）
   - 【招生对象】：面向哪些学生（如：全区应届初中毕业生、本校科技特长生等）
   - 【过程/方式】：如何录取（如：学校测试后按中考成绩择优录取、综合素质评定等）

4. 不要在返回内容中包含任何URL或链接

请严格按以下CSV格式输出（每行一条，不要输出其他文字）：
学段,地区,学校名称,赛事/项目名称,对升学的具体帮助

示例格式：
学段,地区,学校名称,赛事/项目名称,对升学的具体帮助
小升初,桂林秀峰区,桂林市某小学,Python创意编程赛,2025年该校科技特长生招生简章显示招收3人，报名条件为Python编程赛获市级一等奖以上，对象为秀峰区等五城区小学应届毕业生，流程为提交材料+学校面试+综合素质评定，获奖学生优先录取。
初升高,桂林秀峰区,桂林中学,NOC大赛Python赛项,2024年桂林市科技特长生招生简章显示招收5人，报名条件为NOC大赛Python赛项获省级二等奖以上，对象为全市应届初中毕业生，流程为网上报名+学校专业测试+中考成绩达普高线，按综合成绩从高到低录取。

重要提醒：
- 赛事/项目名称必须填写具体赛事名称，不能写"科技类特长生"、"编程特长生"、"信息学特长生"等模糊名称
- 【严格禁止】禁止填写NOIP、CSP-J/S、Scratch、蓝桥杯、图形化编程等赛事
- 每个地区的初升高案例必须至少1条
- 每个地区的小升初案例最多1条'''

    payload = {
        'model': 'deepseek-chat',
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0
    }
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        'https://api.deepseek.com/chat/completions',
        data=data,
        headers={
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {api_key}'
        }
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        return result['choices'][0]['message']['content']


def parse_csv_lines(text):
    """解析CSV行"""
    records = []
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('学段,') or line.startswith('#') or line.startswith('**') or line.startswith('示例'):
            continue
        if line.count(',') >= 4:
            parts = []
            in_quote = False
            current = ''
            for ch in line:
                if ch == '"':
                    in_quote = not in_quote
                elif ch == ',' and not in_quote:
                    parts.append(current.strip().strip('"'))
                    current = ''
                else:
                    current += ch
            parts.append(current.strip().strip('"'))
            if len(parts) >= 5:
                while len(parts) < 5:
                    parts.append('')
                records.append(parts[:5])
    return records


def enhance_description(desc, school, competition):
    """补充描述中缺失的要素"""
    desc = desc.strip()

    has_year = bool(re.search(r'20[1-9][0-9]年', desc))
    has_count = bool(re.search(r'招收\d+人|招生\d+人|名额\d+人|无名额限制', desc))
    has_condition = bool(re.search(r'一等奖|二等奖|三等奖|特等奖|国家[级等奖]|省级|市级', desc))

    if not (has_year and has_count and has_condition):
        year_match = re.search(r'20[1-9][0-9]年', desc)
        year = year_match.group(0) if year_match else '近年'

        if not has_count:
            desc = re.sub(r'，', f'（名额以当年招生简章为准），' if '（' in desc else f'，名额以当年招生简章为准，', desc)

    return desc


def save_progress(current_index, total):
    """保存当前进度"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        f.write(f'{current_index}/{total}')


def load_progress():
    """加载进度"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if '/' in content:
                current, total = content.split('/')
                return int(current)
    return 0


# ========== 主流程 ==========
print('=' * 60)
print('科技特长生升学政策批量查询系统 (v2)')
print('=' * 60)

# 读取所有地区
regions = read_regions()
total = len(regions)
print(f'\n从 {REGIONS_FILE} 读取到 {total} 个地区')

# 每次执行时清空旧数据，写入表头（用Python写，保证utf-8-sig编码）
with open(OUTPUT_FILE, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['学段', '地区', '学校名称', '赛事/项目名称', '对升学的具体帮助'])
print('已清空旧数据，写入表头完成')

# 每次都从头开始
start_index = 0
print(f'从第 1 条开始查询')
print(f'\n开始查询...\n')

# 统计
new_records_count = 0

# 遍历所有地区
for i in range(start_index, total):
    loc = regions[i]
    print(f'\n[{i+1}/{total}] 查询: {loc}')

    try:
        resp = call_deepseek(loc)
        print(f'--- DeepSeek 返回 (前300字) ---')
        print(resp[:300])
        print('...')

        records = parse_csv_lines(resp)
        print(f'解析出 {len(records)} 条')

        # 限制：小升初最多1条，初升高至少1条（最多2条）
        stage_counts = {}
        limited = []
        for rec in records:
            stage = rec[0].strip()
            cnt = stage_counts.get(stage, 0)
            if stage == '小升初' and cnt < 1:
                stage_counts[stage] = cnt + 1
                limited.append(rec)
            elif stage == '初升高' and cnt < 2:
                stage_counts[stage] = cnt + 1
                limited.append(rec)

        # 确保初升高至少有1条（如果没有，尝试从其他记录借用）
        has_zsg = any(r[0] == '初升高' for r in limited)
        if not has_zsg:
            for rec in records:
                if rec[0] == '初升高' and rec not in limited:
                    limited.append(rec)
                    break

        print(f'限制后 {len(limited)} 条（小升初≤1条，初升高≥1条）')

        # 补充/校验描述
        for rec in limited:
            rec[4] = enhance_description(rec[4], rec[2], rec[3])


        # 写入CSV（追加模式）
        with open(OUTPUT_FILE, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(limited)

        new_records_count += len(limited)
        print(f'追加 {len(limited)} 条到 {OUTPUT_FILE}')

        # 保存进度
        save_progress(i + 1, total)
        print(f'进度已保存: {i+1}/{total}')

        # 每10条打印一次统计
        if (i + 1) % 10 == 0:
            print(f'\n>>> 进度汇报: 已完成 {i+1}/{total} 个地区，新增 {new_records_count} 条政策记录')

    except Exception as e:
        print(f'出错: {e}')
        import traceback
        traceback.print_exc()
        print('继续下一个地区...')
        continue

# 最终统计
print('\n' + '=' * 60)
print('查询完成！')
print(f'总计处理 {total} 个地区')
print(f'新增 {new_records_count} 条政策记录')
print(f'数据已保存到: {OUTPUT_FILE}')
print('=' * 60)

# 删除进度文件（完成）
if os.path.exists(PROGRESS_FILE):
    os.remove(PROGRESS_FILE)
    print('进度文件已清除，下次运行将从头开始')
