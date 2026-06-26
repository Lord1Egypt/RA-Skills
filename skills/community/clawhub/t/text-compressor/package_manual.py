import sys, os, zipfile, pathlib, re

skill_path = pathlib.Path(r'C:\Users\funky\.openclaw\workspace\skills\text-compressor')
output_dir = pathlib.Path(r'C:\Users\funky\.openclaw\workspace\skills')

# Validate
md_file = skill_path / 'SKILL.md'
if not md_file.exists():
    print("ERROR: SKILL.md not found")
    sys.exit(1)

content = md_file.read_text(encoding='utf-8')
if not content.startswith('---'):
    print("ERROR: SKILL.md must start with YAML frontmatter")
    sys.exit(1)

fm_end = content.index('---', 3)
fm = content[3:fm_end].strip()
name_match = re.search(r'^name:\s*(.+)$', fm, re.M)
desc_match = re.search(r'^description:\s*(.+)$', fm, re.M)
if not name_match or not desc_match:
    print("ERROR: frontmatter must have name and description")
    sys.exit(1)

skill_name = name_match.group(1).strip()
skill_file = output_dir / f'{skill_name}.skill'

# Package
with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in skill_path.rglob('*'):
        if f.is_file():
            arcname = f.relative_to(skill_path)
            zf.write(f, arcname)

print(f"Packaged: {skill_file}")