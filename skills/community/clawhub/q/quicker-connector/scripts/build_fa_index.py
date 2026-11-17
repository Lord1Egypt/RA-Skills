"""一次性：从 Quicker 自带的 FontAwesomeIconsWpf.dll 提取全部图标 SVG 路径 -> data/fontawesome5_svg_index.json.gz"""
import clr, gzip, json, os, sys, time

DLL = r'C:\Program Files\Quicker\FontAwesomeIconsWpf.dll'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'fontawesome5_svg_index.json.gz')

clr.AddReference(DLL)
import System
a = System.Reflection.Assembly.LoadFrom(DLL)
T = a.GetType('FontAwesome5.EFontAwesomeIcon')
AT = a.GetType('FontAwesome5.FontAwesomeSvgInformationAttribute')

t0 = time.time()
index = {}
names = System.Enum.GetNames(T)
for n in names:
    fld = T.GetField(n)
    if fld is None:
        continue
    ats = fld.GetCustomAttributes(AT, False)
    if not ats:
        continue
    at = ats[0]
    try:
        index[n] = [at.Path, int(at.Width), int(at.Height)]
    except Exception:
        pass

print('extracted', len(index), 'in %.1fs' % (time.time() - t0))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
raw = json.dumps(index, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
with gzip.open(OUT, 'wb', compresslevel=9) as f:
    f.write(raw)
print('written', OUT, 'raw', len(raw), 'gz', os.path.getsize(OUT))
