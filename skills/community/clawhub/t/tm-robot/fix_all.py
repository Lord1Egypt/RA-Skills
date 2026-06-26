with open(r'C:/Users/JMO/.openclaw/workspace/skills/tm-robot/tm_robot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all duplicate lines
fixes = [
    ('''        except Exception as e:
                print(f"[警告] SVR 解析错误：{e}")
            print(f"[警告] SVR 解析错误：{e}")
            return {}''',
     '''        except Exception as e:
            print(f"[警告] SVR 解析错误：{e}")
            return {}'''),
]

for old, new in fixes:
    content = content.replace(old, new)

with open(r'C:/Users/JMO/.openclaw/workspace/skills/tm-robot/tm_robot.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed all!')
