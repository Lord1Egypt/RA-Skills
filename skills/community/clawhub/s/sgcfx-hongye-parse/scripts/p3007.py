# -*- coding: utf-8 -*-
"""SGCFX 3007 工料机汇总表 解析器 v4
行布局：[数字块] [材料编码] [材料名称] [规格?] [单位] % [招标编码] [价格来源?] ... [类别] [供货方式] [尾整数]
解算 (数量,基价,合价)：在数字块中找 ±成对 的 基价p 与 合价t，使 t/p ≈ 块内某数 c（c 即数量，以 c 为准）
打分消歧：c 在块内重复次数 > 价格来源串含 p > 合价 t 更大
"""
import struct,sys,re,json,os

UNIT=set('m3 m2 m m² m³ t kg L 个 台 套 樘 组 座 根 块 副 株 项 处 站 只 部 件 条 面 元 扇 支 张 片 千块 万块 桶 束 环 段 层 10m3 10m2 100m 千匹 具 间 百个 100个'.split())
NUMS=re.compile(r'^-?\d+(?:\.\d+)?$')
CODE=re.compile(r'^(?:[A-Za-z]{0,4}\d{4,14}|QTCLF)$')
RELTOL=3e-4

def tlv(p):
    d=open(p,'rb').read(); o=1; res=[]
    while o+4<=len(d):
        n=struct.unpack_from('<i',d,o)[0]
        if 0<n<=900 and o+4+n*2<=len(d)+2:
            try:
                s=d[o+4:o+4+n*2].decode('utf-16-le')
                if s.isprintable() and s.strip(): res.append((o,s)); o+=4+n*2; continue
            except: pass
        o+=1
    return res

def solve(blk,src=''):
    vals=[float(x) for x in blk]; S=set(vals)
    cands=[]
    for p in set(vals):
        if p<=0 or -p not in S: continue
        for t in set(vals):
            if t<=0 or -t not in S: continue
            want=t/p
            best=min(vals,key=lambda c:abs(c-want))
            if best<=0: continue
            if abs(best-want)/max(want,1e-12)>RELTOL: continue
            dup=sum(1 for x in vals if abs(x-best)<=max(1e-9,abs(best)*1e-9))
            sm=1 if f'{p:g}' in src else 0
            q=best
            if abs(q*p-t)/max(t,1e-12)>5e-3: continue   # 一致性底线
            cands.append((dup,sm,t,q,p))
    if not cands:
        # 第二遍：基价被四舍五入时放宽一致性，但要求数量在块内重复出现
        for p in set(vals):
            if p<=0 or -p not in S: continue
            for t in set(vals):
                if t<=0 or -t not in S: continue
                for q in set(vals):
                    if q<=0: continue
                    dup=sum(1 for x in vals if abs(x-q)<=max(1e-9,abs(q)*1e-9))
                    if dup<2: continue
                    if abs(q*p-t)/max(t,1e-12)>2e-2: continue
                    cands.append((dup,1 if f'{p:g}' in src else 0,t,q,p))
    if not cands: return None
    cands.sort(key=lambda z:(z[0],z[1],z[2]),reverse=True)
    dup,sm,t,q,p=cands[0]
    return (round(q,6),round(p,6),round(t,2))

def rows(p):
    rs=tlv(p); idx=[]
    for i,(off,s) in enumerate(rs):
        if i+1<len(rs) and rs[i+1][1].strip() in UNIT:
            anchor=s.strip(); code=''; name=''; coff=None
            for j in range(i,max(i-4,-1),-1):
                cand=rs[j-1][1].strip() if j>0 else ''
                if CODE.match(cand): code=cand; name=rs[j][1].strip(); coff=rs[j-1][0]; break
            if not code or coff is None: continue
            idx.append((i,off,code,name,anchor,rs[i+1][1].strip(),coff))
    out=[]
    for k,(i,off,code,name,spec,unit,coff) in enumerate(idx):
        wstart=idx[k-1][1] if k>0 else 0
        win=[(o,x) for o,x in rs if wstart<=o<coff]
        lastnn=max([j for j,(o,x) in enumerate(win) if not NUMS.match(x)],default=-1)
        blk=[x for j,(o,x) in enumerate(win) if j>lastnn and NUMS.match(x)]
        if blk and re.fullmatch(r'-?\d+',blk[0]): blk=blk[1:]
        src=''
        for kk in range(i+2,min(i+10,len(rs))):
            t2=rs[kk][1]
            if '信息价' in t2 or '元/' in t2 or '市场价' in t2 or '协商' in t2: src=t2; break
        sol=solve(blk,src)
        out.append(dict(off=off,code=code,name=name,spec=spec if spec!=name else '',unit=unit,
                        qty=sol[0] if sol else None, price=sol[1] if sol else None,
                        amt=sol[2] if sol else None, src=src[:230], raw=blk))
    return out

if __name__=='__main__':
    tot=ok=0; bad=[]
    for p in sys.argv[1:]:
        r=rows(p); n=sum(1 for x in r if x['qty'] is not None); tot+=len(r); ok+=n
        print(f'{p}  行={len(r)}  已解={n}')
        for x in r:
            if x['qty'] is None: print('   ✗',x['code'],x['name'],x['spec'],x['unit'],x['raw'][:8])
    print(f'合计 行={tot} 已解={ok} ({ok/tot*100 if tot else 0:.1f}%)')
