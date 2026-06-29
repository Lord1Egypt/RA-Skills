#!/usr/bin/env python3
from pathlib import Path
import sys, json
if len(sys.argv)<2:
    print('usage: verify_delivery_package.py <package_dir>', file=sys.stderr); sys.exit(2)
root=Path(sys.argv[1])
required_dirs=['成品PPT','最终资料','页面源图','预览图']
required_keywords=['内容大纲','制作规范','逐页制作说明','审核']
result={'root':str(root),'exists':root.exists(),'missing_dirs':[],'required_docs':{},'pptx':[],'page_sources':0,'previews':0,'status':'PASS'}
for d in required_dirs:
    if not (root/d).exists(): result['missing_dirs'].append(d)
for kw in required_keywords:
    hits=[str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and kw in p.name]
    result['required_docs'][kw]=hits
result['pptx']=[str(p.relative_to(root)) for p in root.rglob('*.pptx')]
result['page_sources']=len(list((root/'页面源图').glob('*'))) if (root/'页面源图').exists() else 0
result['previews']=len(list((root/'预览图').glob('*'))) if (root/'预览图').exists() else 0
if result['missing_dirs'] or any(not v for v in result['required_docs'].values()) or not result['pptx']:
    result['status']='NEEDS_FIX'
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if result['status']=='PASS' else 1)
