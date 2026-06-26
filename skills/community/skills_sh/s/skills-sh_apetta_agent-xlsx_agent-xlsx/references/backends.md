# Rendering Backends

agent-xlsx uses three rendering engines for `screenshot`, `objects`, and `recalc` commands.

## Auto-Detection Priority

Priority differs by command:

**screenshot / recalc:**
```
1. Aspose.Cells → 2. Excel (xlwings) → 3. LibreOffice → NoRenderingBackendError
```

**objects:**
```
1. Aspose.Cells → 2. Excel (xlwings) → ExcelRequiredError (no LibreOffice support)
```

Force a specific engine with `--engine excel|aspose|libreoffice`. Available engines vary by command — see the Command × Engine Matrix below.

## Excel (xlwings)

- **Platforms:** macOS, Windows (requires Microsoft Excel)
- **Fidelity:** Perfect — native Excel rendering
- **Speed:** Fast
- **Commands:** screenshot, objects, recalc, vba --run

**macOS quirk:** Requires `visible=True` with 0.5s delay for CopyPicture API. Windows runs headless.

Auto-fits columns before capture (`sheet.autofit('c')`) to prevent `####` display.

## Aspose.Cells

- **Platforms:** All (cross-platform, headless)
- **Fidelity:** Near-perfect
- **Speed:** Fast
- **Commands:** screenshot, objects, recalc

Aspose.Cells is included as a core dependency of agent-xlsx — no separate install required.

**Licensing:** Aspose.Cells is a **proprietary, commercially licensed** library by [Aspose Pty Ltd](https://www.aspose.com/) — **not** covered by agent-xlsx's Apache-2.0 licence. Users are subject to [Aspose's EULA](https://company.aspose.com/legal/eula). A [separate commercial licence](https://purchase.aspose.com/pricing/cells/python-java) is required for production use without watermarks. Evaluation mode works but adds watermarks and has a 100-file-per-session limit.

**Setting a licence:**

| Method | Usage |
|--------|-------|
| CLI | `agent-xlsx license --set /path/to/Aspose.Cells.lic` |
| Env var (file) | `ASPOSE_LICENSE_PATH=/path/to/Aspose.Cells.lic` |
| Env var (base64) | `ASPOSE_LICENSE_DATA=<base64 .lic content>` |
| Config file | Stored in `~/.agent-xlsx/config.json` |

Priority: env var → config file. Licence applied once per process (cached).

> **Security note:** Prefer `ASPOSE_LICENSE_PATH` (file path) over `ASPOSE_LICENSE_DATA`
> (base64 inline). Base64 licence data stored as an env var is visible in `ps aux` and can
> accidentally land in shell history (`.bashrc`, `.zshrc`) or CI/CD logs. When
> `ASPOSE_LICENSE_DATA` is detected, agent-xlsx automatically emits a warning to stderr.

Evaluation mode output includes `"evaluation_mode": true` and `"evaluation_notice"` in JSON.

## LibreOffice

- **Platforms:** All (free, open-source)
- **Fidelity:** Good
- **Speed:** Slower (multi-step pipeline)
- **Commands:** screenshot, recalc

**Screenshot pipeline:** `.xlsx → LibreOffice PDF export → PyMuPDF PNG render`

Each invocation uses a unique temp user profile to avoid lock conflicts.

**Standard install locations checked:**
- macOS: `/Applications/LibreOffice.app/Contents/MacOS/soffice`
- Linux: `/usr/bin/libreoffice`, `/usr/bin/soffice`, `/snap/bin/libreoffice`

`--timeout` is LibreOffice-specific (default: 30s for screenshot, 60s for recalc).

## Supported Formats

| Format | Extension | Read | Write | VBA | Screenshot |
|--------|-----------|------|-------|-----|------------|
| Excel 2007+ | `.xlsx` | yes | yes | — | yes |
| Excel Macro | `.xlsm` | yes | yes | yes | yes |
| Excel Binary | `.xlsb` | yes | — | yes | yes |
| Excel 97-2003 | `.xls` | yes | — | yes | yes |
| OpenDocument | `.ods` | yes | — | — | yes |

Only `.xlsx` and `.xlsm` support in-place writes. Using `-o` with a non-writable extension (e.g. `-o out.xls`) auto-converts the output to `.xlsx`.

## Command × Engine Matrix

| Command | Excel | Aspose | LibreOffice |
|---------|-------|--------|-------------|
| screenshot | yes | yes | yes |
| objects (list) | yes | yes | — |
| objects (export) | yes | yes | — |
| recalc | yes | yes | yes |
| vba --run | yes | — | — |
