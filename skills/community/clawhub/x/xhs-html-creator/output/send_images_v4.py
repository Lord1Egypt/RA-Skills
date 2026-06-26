import subprocess, time, os
shots_dir = r'C:\Users\95116\.openclaw\workspace\skills\xhs-content-matrix\output\shots'
script = r'C:\Users\95116\.openclaw\workspace\skills\feishu-image\scripts\feishu_image.py'
user_id = 'ou_620fceb1cd2bccee9363926691161a2d'
images = ['daishengbao_cover_v4.png','daishengbao_doc_v4.png','daishengbao_baby1_v4.png','daishengbao_baby2_v4.png','daishengbao_mom_v4.png','daishengbao_ending_v4.png']
for img in images:
    path = os.path.join(shots_dir, img)
    print(f'Sending {img}...', flush=True)
    result = subprocess.run(['python', script, path, user_id], capture_output=True)
    stdout = result.stdout.decode('utf-8', errors='replace') if result.stdout else ''
    stderr = result.stderr.decode('utf-8', errors='replace') if result.stderr else ''
    print(f'  stdout: {stdout.strip()}', flush=True)
    if stderr: print(f'  stderr: {stderr.strip()}', flush=True)
    time.sleep(1.5)
print('All done!', flush=True)
