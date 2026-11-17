"""Build a portable ZIP using an explicit distribution whitelist, with SHA-256 manifest."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from value_model import VERSION


def package(output,root=None):
    root=Path(root) if root else Path(__file__).resolve().parent.parent
    output=Path(output)
    required=[root/'SKILL.md']
    required+=sorted((root/'scripts').glob('*.py'))
    required+=sorted((root/'references').glob('*.md'))
    required+= [root/'config'/name for name in ('calibration.json','backtest_strategy.json')]
    # assets/icon.png 不进包：SkillHub 服务端会拒绝，报「不允许的文件类型: assets/icon.png」。
    # 技能图标走 SkillHub 托管的 iconUrl 字段，不是随包文件；仓库里仍保留该图供 GitHub 展示。
    optional=[root/'assets'/name for name in ('report.css','icon.prompt.md')]
    missing=[p for p in required if not p.is_file()]
    if missing:
        raise SystemExit('缺少必需文件，无法打包：'+'、'.join(str(p.relative_to(root)) for p in missing))
    files=required+[p for p in optional if p.is_file()]
    contents={str(path.relative_to(root)).replace('\\','/'):path.read_bytes() for path in files}
    # Never ship a user's learned weights, audit history or personal portfolio data.
    contents['config/weights.json']=b'{"schema_version": 1, "releases": []}\n'
    manifest={'version':VERSION,'python':'>=3.10','runtime_dependencies':'Python standard library only',
              'files':{k:hashlib.sha256(v).hexdigest() for k,v in sorted(contents.items())}}
    contents['MANIFEST.json']=json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf-8')
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,content in sorted(contents.items()):
            entry=zipfile.ZipInfo('stock-portfolio-advisor/'+name,date_time=(2026,1,1,0,0,0))
            entry.compress_type=zipfile.ZIP_DEFLATED
            entry.external_attr=0o644<<16
            z.writestr(entry,content)
    with zipfile.ZipFile(output) as z:
        if z.testzip():raise ValueError('ZIP integrity check failed')
        for name,expected in manifest['files'].items():
            if hashlib.sha256(z.read('stock-portfolio-advisor/'+name)).hexdigest()!=expected:
                raise ValueError('Packaged file checksum mismatch')
    checksum=hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix+'.sha256').write_text(checksum+'  '+output.name+'\n',encoding='ascii')
    return output,checksum,len(contents)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',default=f'dist/stock-portfolio-advisor-{VERSION}.zip')
    a=p.parse_args();path,checksum,count=package(a.output)
    print(f'[OK] {path} ({count} files)\nSHA256 {checksum}')


if __name__=='__main__':main()
