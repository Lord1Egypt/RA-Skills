import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

tests = [
    ('急诊分流', '我的狗一直在抽搐'),
    ('价格查询', '多少钱绝育'),
    ('营业时间', '几点开门'),
    ('知识问答', '犬瘟热症状是什么'),
    ('库存查询', '库存'),
    ('化验解读', 'WBC: 25.3 RBC: 5.2'),
    ('地址查询', '地址在哪'),
    ('新客户建档', '主人：张三 电话：13800138000 宠物名：旺财 种类：狗 品种：金毛 年龄：3岁'),
    ('日报', '每日运营报表'),
]

passed = 0
for name, msg in tests:
    req = urllib.request.Request('http://localhost:8000/api/chat',
        data=json.dumps({'message': msg, 'session_id': 'test'}).encode(),
        headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode('utf-8'))
    skill = data['skill']
    response = data['response']
    ok = skill is not None and len(response) > 10
    status = 'PASS' if ok else 'FAIL'
    if ok:
        passed += 1
    print(f'[{status}] {name} -> skill={skill}')
    print(f'  {response[:120]}')
    print()

print(f'\nResult: {passed}/{len(tests)} passed')
