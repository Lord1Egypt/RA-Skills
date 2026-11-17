import struct,sys,re
def strs(p):
    d=open(p,'rb').read(); o=1; res=[]
    while o+4<=len(d):
        n=struct.unpack_from('<i',d,o)[0]
        if 0<n<=900 and o+4+n*2<=len(d)+2:
            try:
                s=d[o+4:o+4+n*2].decode('utf-16-le')
                if s.isprintable() and s.strip(): res.append((o,s)); o+=4+n*2; continue
            except: pass
        o+=1
    return res,len(d)
r,sz=strs(sys.argv[1])
st=int(sys.argv[2]) if len(sys.argv)>2 else 0
for o,s in r:
    if o>=st: print(f'{o:>7}\t{s}')
