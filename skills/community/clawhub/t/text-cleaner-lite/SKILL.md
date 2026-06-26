# Skill Name
text-cleaner-lite

## Function Description
Normalize whitespace, remove duplicated blank lines, and trim leading/trailing spaces.

## Input Parameters
- raw_text (string), keep_newlines (boolean, optional)

## Output Result
- cleaned_text (string)

## Usage Example
`ash
python main.py --input sample.txt --mode clean
`

## Risk Statement
- Risk level: L1
- This skill may perform actions matching category $(@{skill_id=skill_001; name=text-cleaner-lite; category=text-processing; risk_level=L1; source_template=skillsmp_download/1/SKILL.md; description=Normalize whitespace, remove duplicated blank lines, and trim leading/trailing spaces.; input=raw_text (string), keep_newlines (boolean, optional); output=cleaned_text (string); tags=System.Object[]; example=python main.py --input sample.txt --mode clean}.category) and should be reviewed before production use.

## Category Tags
- text-processing, normalization, safe
