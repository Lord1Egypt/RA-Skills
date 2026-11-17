# Platform Support

## Full Matrix

| Category | Software | Notes |
|----------|----------|-------|
| ✅ All platforms (Win + Mac + Linux, CLI) | R, Stata, SAS, CmdStan, GenStat, Gretl, H2O.ai, JAGS, Julia, KNIME, Mathematica, Matlab, OpenBUGS, Orange, OxMetrics, PSPP, Rattle, SHAZAM, Stat/Transfer, Tanagra, TSP, Weka | Full CLI automation on all platforms |
| ✅ Win + Mac + Limited Linux | Mplus | Limited Linux support |
| ⚠️ Win + Limited Mac/Linux | Minitab | Limited Mac/Linux |
| 🔴 Windows only | SPSS Statistics, EViews, JMP, LIMDEP, Microfit, NCSS, NLOGIT, Origin, Q (MRKS), SPSS Modeler, Statistica | Windows-only CLI |
| 🔴 GUI-only (detection + manual-launch only) | AMOS, GraphPad Prism, JASP, jamovi | Can detect and guide manual GUI launch; no CLI batch automation |

## GUI-Only Software

GUI-only software (AMOS, GraphPad Prism, JASP, jamovi) is limited to **detection + manual-launch guidance** — this skill never drives them via CLI/headless automation, and never creates or modifies their project/data files (including GraphPad Prism `.pzfx`).

## Version-Specific Notes

See `version-specifics.md` for version differences (SPSS 26/30, R 4.5/4.1, Python 3.4/3.13).