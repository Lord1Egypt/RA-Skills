import os
skill_dir = r'C:\Users\beyon\.openclaw\workspace-dapingxia\skills\walter-info'
print('Files in skill dir:')
for f in sorted(os.listdir(skill_dir)):
    print(f'  {f}')
print()
print('config.example.json exists:', os.path.exists(os.path.join(skill_dir, 'config.example.json')))
