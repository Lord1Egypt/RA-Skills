## Description: <br>
Compétence pour manipuler les fichiers Excel (.xlsx, .xlsm, .csv, .tsv). Utiliser quand l'utilisateur veut : ouvrir, lire, éditer ou créer un fichier tableur ; ajouter des colonnes, calculer des formules, formater, créer des graphiques, nettoyer des données ; convertir entre formats tabulaires. Le livrable doit être un fichier tableur. NE PAS utiliser si le livrable est un document Word, HTML, script Python standalone, ou intégration Google Sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricobaboule](https://clawhub.ai/user/ricobaboule) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and spreadsheet-focused agents use this skill to create, edit, format, and validate Excel, CSV, and TSV deliverables with Excel formulas preserved instead of Python-hardcoded calculated values. It is especially suited for formula-heavy workbooks and financial-model-style formatting where optional LibreOffice recalculation and error scanning are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LibreOffice automation can persist a macro in the user's LibreOffice profile. <br>
Mitigation: Use an isolated container or disposable LibreOffice profile and review or remove the generated macro after use. <br>
Risk: The helper can load a locally compiled native shim through LD_PRELOAD when the environment needs it. <br>
Mitigation: Run the skill only in trusted or isolated environments and inspect temporary native artifacts before reuse. <br>
Risk: Untrusted spreadsheets can exercise LibreOffice parsing and macro-related surfaces. <br>
Mitigation: Avoid untrusted spreadsheets or process them in a sandbox with restricted filesystem and network access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ricobaboule/xlsx-pro) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples, plus JSON output from recalculation checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces spreadsheet files as the expected user-facing deliverable; recalculation checks may report formula counts and Excel error locations.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
