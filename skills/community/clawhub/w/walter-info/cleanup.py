import os
skill_dir = r'C:\Users\beyon\.openclaw\workspace-dapingxia\skills\walter-info'
example = os.path.join(skill_dir, 'config.example.json')
if os.path.exists(example):
    os.remove(example)
    print('Removed: config.example.json')
else:
    print('Already removed')
print('Files:', os.listdir(skill_dir))
