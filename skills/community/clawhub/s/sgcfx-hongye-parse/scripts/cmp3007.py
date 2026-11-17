# -*- coding: utf-8 -*-
import csv,collections
rows=list(csv.DictReader(open('materials_3007.csv',encoding='utf-8-sig')))
def f(v):
    try: return float(v)
    except: return 0.0
def k(r): return (r['name'].strip(), r['spec'].strip(), r['unit2'].strip())
def agg(file,ver,unit=None):
    d=collections.defaultdict(lambda:[0.0,0.0])
    for r in rows:
        if r['file']!=file or r['ver']!=ver: continue
        if unit and r['unit']!='': pass
        key=k(r); d[key][0]+=f(r['qty']); d[key][1]+=f(r['amt'])
    return d
A=agg('NEW','4'); B=agg('OLD','3')
keys=sorted(set(A)|set(B), key=lambda x:(-max(A.get(x,[0])[0],B.get(x,[0])[0])))
out=[]
for key in keys:
    n,s,u=key
    a=A.get(key,[0,0]); b=B.get(key,[0,0])
    if a[0]==0 and b[0]==0: continue
    out.append((n,s,u,a[0],b[0],(a[0]-b[0]),a[1],b[1]))
with open('materials_cmp_NEW4_vs_OLD3.csv','w',newline='',encoding='utf-8-sig') as fh:
    w=csv.writer(fh); w.writerow(['材料名称','规格型号','单位','新版(审)数量','财评审结数量','差量','新版合价','财评合价'])
    for r in out: w.writerow(r)
print('对比行数',len(out))
# 大宗筛选
BIG={'t','m3','m2','kg','m'}
print('\n=== 按单位=t (吨) ===')
for n,s,u,a,b,d,aa,bb in out:
    if u=='t': print(f'{n:<34}{s:<22}{a:>10.3f}{b:>12.3f}{d:>12.3f}   {aa:>12.0f}{bb:>12.0f}')
