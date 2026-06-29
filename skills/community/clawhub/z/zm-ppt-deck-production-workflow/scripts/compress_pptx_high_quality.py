#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image
import io, sys, re

if len(sys.argv) < 3:
    print('usage: compress_pptx_high_quality.py <input.pptx> <output.pptx> [quality=95]', file=sys.stderr); sys.exit(2)
src=Path(sys.argv[1]); out=Path(sys.argv[2]); q=int(sys.argv[3]) if len(sys.argv)>3 else 95
out.parent.mkdir(parents=True,exist_ok=True)
with ZipFile(src,'r') as zin, ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9) as zout:
    for item in zin.infolist():
        data=zin.read(item.filename); lower=item.filename.lower()
        if lower.startswith('ppt/media/') and lower.endswith(('.png','.jpg','.jpeg')):
            try:
                im=Image.open(io.BytesIO(data))
                if im.mode in ('RGBA','LA') or ('transparency' in im.info):
                    im=im.convert('RGBA'); buf=io.BytesIO(); im.save(buf,format='PNG',optimize=True,compress_level=9); new=buf.getvalue()
                else:
                    im=im.convert('RGB'); buf=io.BytesIO(); im.save(buf,format='JPEG',quality=q,optimize=True,progressive=True,subsampling=0); new=buf.getvalue()
                if len(new) < len(data): data=new
            except Exception: pass
        zout.writestr(item,data)
with ZipFile(out) as z:
    slides=[n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)]
    media=[n for n in z.namelist() if n.startswith('ppt/media/')]
print({'input_size':src.stat().st_size,'output_size':out.stat().st_size,'quality':q,'slides':len(slides),'media':len(media),'output':str(out)})
