# PSScriptAnalyzer Rule Taxonomy
> PowerShell's Official Static Analysis Tool — Organized by Code Quality Dimension  
> Source: Microsoft Learn, PSScriptAnalyzer GitHub (PowerShell/PSScriptAnalyzer), PSGallery Publishing Guidelines  
> Last updated: 2026-03-05

---

## Table of Contents

1. [Overview](#1-overview)
2. [Severity Levels](#2-severity-levels)
3. [Built-in Presets](#3-built-in-presets)
4. [Master Rule Table](#4-master-rule-table)
5. [Rules by Quality Dimension](#5-rules-by-quality-dimension)
   - 5.1 [Security](#51-security)
   - 5.2 [Reliability](#52-reliability)
   - 5.3 [Maintainability](#53-maintainability)
   - 5.4 [Style & Formatting](#54-style--formatting)
   - 5.5 [Compatibility](#55-compatibility)
   - 5.6 [DSC (Desired State Configuration)](#56-dsc-desired-state-configuration)
6. [PSGallery Requirements](#6-psgallery-requirements)
7. [PowerShell-Specific Code Hygiene](#7-powershell-specific-code-hygiene)
8. [Agentic & Automation Patterns](#8-agentic--automation-patterns)
9. [Custom Rules & Configuration](#9-custom-rules--configuration)
10. [Quality Dimension Cross-Reference](#10-quality-dimension-cross-reference)

---

## 1. Overview

**PSScriptAnalyzer** is Microsoft's official static analysis (SAST) tool for PowerShell. It evaluates scripts, modules, and manifests against a set of community-curated and Microsoft-endorsed rules. It is:

- Required by **PowerShell Gallery** — all published packages are scanned; errors must be resolved before publication
- Integrated into **VS Code PowerShell extension**, **GitHub Actions**, and **Azure DevOps** pipelines
- Extensible via custom rule modules
- Configurable via `.psd1` settings files with **IncludeRules**, **ExcludeRules**, and **Severity** filters

**Key characteristics:**
- Rules are prefixed with `PS` (e.g., `PSAvoidUsingWriteHost`)
- Rules fire against `.ps1`, `.psm1`, `.psd1` files
- Output contains: `RuleName`, `Severity`, `ScriptName`, `Line`, `Message`
- Parser errors are surfaced as `ParseError` severity (not suppressable)

---

## 2. Severity Levels

| Severity | Meaning | Action Required |
|----------|---------|-----------------|
| **Error** | Definitive violation — functional correctness or serious security risk. Blocks PSGallery publication. | Must fix |
| **Warning** | Likely problem — best practice deviation with real risk. PSGallery strongly recommends fixing all. | Should fix |
| **Information** | Advisory — low-risk patterns worth reviewing; often style or documentation gaps. | Review |
| **ParseError** | PowerShell parser cannot parse the file. Cannot be suppressed. Surfaced since v1.18.0. | Must fix |
| **TBD** | Identified best practices without a current rule implementation. Community roadmap items. | Awareness |

**PSGallery enforcement:** All Errors must be corrected before publication. All Warnings must be reviewed and addressed where applicable.

---

## 3. Built-in Presets

PSScriptAnalyzer ships three built-in presets selectable via `-Settings`:

### PSGallery Preset
Invoked with: `Invoke-ScriptAnalyzer -Path . -Settings PSGallery -Recurse`

Rules enforced:
```
PSUseApprovedVerbs, PSReservedCmdletChar, PSReservedParams, PSShouldProcess,
PSUseShouldProcessForStateChangingFunctions, PSUseSingularNouns,
PSMissingModuleManifestField, PSAvoidDefaultValueSwitchParameter,
PSAvoidUsingCmdletAliases, PSAvoidUsingWMICmdlet, PSAvoidUsingEmptyCatchBlock,
PSUseCmdletCorrectly, PSAvoidUsingPositionalParameters, PSAvoidGlobalVars,
PSUseDeclaredVarsMoreThanAssignments, PSAvoidUsingInvokeExpression,
PSAvoidUsingPlainTextForPassword, PSAvoidUsingComputerNameHardcoded,
PSUsePSCredentialType, PSDSC*
```

### CodeFormatting Preset
Invoked with: `Invoke-ScriptAnalyzer -Path . -Settings CodeFormatting -Recurse`

Rules enforced:
```
PSPlaceOpenBrace, PSPlaceCloseBrace, PSUseConsistentWhitespace,
PSUseConsistentIndentation, PSAlignAssignmentStatement, PSUseCorrectCasing
```

Default settings: 4-space indentation, open brace on same line, pipeline indentation enabled.

### DSC Preset
Invoked with: `Invoke-ScriptAnalyzer -Path . -Settings DSC -Recurse`

Rules enforced: `PSDSC*` (all DSC-prefixed rules)

---

## 4. Master Rule Table

Complete list of 69 built-in rules, as of PSScriptAnalyzer latest release.

| Rule Name | Severity | Default On | Configurable | Quality Dimension |
|-----------|----------|-----------|--------------|-------------------|
| AlignAssignmentStatement | Warning | No | Yes | Style |
| AvoidAssignmentToAutomaticVariable | Warning | Yes | — | Reliability |
| AvoidDefaultValueForMandatoryParameter | Warning | Yes | — | Reliability |
| AvoidDefaultValueSwitchParameter | Warning | Yes | — | Reliability |
| AvoidExclaimOperator | Warning | No | — | Style |
| AvoidGlobalAliases ¹ | Warning | Yes | — | Maintainability |
| AvoidGlobalFunctions | Warning | Yes | — | Maintainability |
| AvoidGlobalVars | Warning | Yes | — | Maintainability |
| AvoidInvokingEmptyMembers | Warning | Yes | — | Reliability |
| AvoidLongLines | Warning | No | Yes | Style |
| AvoidMultipleTypeAttributes ¹ | Warning | Yes | — | Reliability |
| AvoidNullOrEmptyHelpMessageAttribute | Warning | Yes | — | Maintainability |
| AvoidOverwritingBuiltInCmdlets | Warning | Yes | Yes | Maintainability |
| AvoidReservedWordsAsFunctionNames | Warning | Yes | — | Maintainability |
| AvoidSemicolonsAsLineTerminators | Warning | No | — | Style |
| AvoidShouldContinueWithoutForce | Warning | Yes | — | Reliability |
| AvoidTrailingWhitespace | Warning | Yes | — | Style |
| AvoidUsingAllowUnencryptedAuthentication | Warning | Yes | — | Security |
| AvoidUsingBrokenHashAlgorithms | Warning | Yes | — | Security |
| AvoidUsingCmdletAliases | Warning | Yes | Yes ² | Maintainability |
| AvoidUsingComputerNameHardcoded | **Error** | Yes | — | Security |
| AvoidUsingConvertToSecureStringWithPlainText | **Error** | Yes | — | Security |
| AvoidUsingDeprecatedManifestFields | Warning | Yes | — | Maintainability |
| AvoidUsingDoubleQuotesForConstantString | Information | No | — | Style |
| AvoidUsingEmptyCatchBlock | Warning | Yes | — | Reliability |
| AvoidUsingInvokeExpression | Warning | Yes | — | Security |
| AvoidUsingPlainTextForPassword | Warning | Yes | — | Security |
| AvoidUsingPositionalParameters | Warning | Yes | — | Maintainability |
| AvoidUsingUsernameAndPasswordParams | **Error** | Yes | — | Security |
| AvoidUsingWMICmdlet | Warning | Yes | — | Maintainability |
| AvoidUsingWriteHost | Warning | Yes | — | Maintainability |
| DSCDscExamplesPresent | Information | Yes | — | DSC |
| DSCDscTestsPresent | Information | Yes | — | DSC |
| DSCReturnCorrectTypesForDSCFunctions | Information | Yes | — | DSC |
| DSCStandardDSCFunctionsInResource | **Error** | Yes | — | DSC |
| DSCUseIdenticalMandatoryParametersForDSC | **Error** | Yes | — | DSC |
| DSCUseIdenticalParametersForDSC | **Error** | Yes | — | DSC |
| DSCUseVerboseMessageInDSCResource | **Error** | Yes | — | DSC |
| MisleadingBacktick | Warning | Yes | — | Reliability |
| MissingModuleManifestField | Warning | Yes | — | Maintainability |
| PlaceCloseBrace | Warning | No | Yes | Style |
| PlaceOpenBrace | Warning | No | Yes | Style |
| PossibleIncorrectComparisonWithNull | Warning | Yes | — | Reliability |
| PossibleIncorrectUsageOfAssignmentOperator | Warning | Yes | — | Reliability |
| PossibleIncorrectUsageOfRedirectionOperator | Warning | Yes | — | Reliability |
| ProvideCommentHelp | Information | Yes | Yes | Maintainability |
| ReservedCmdletChar | **Error** | Yes | — | Reliability |
| ReservedParams | **Error** | Yes | — | Reliability |
| ReviewUnusedParameter | Warning | Yes | Yes ² | Maintainability |
| ShouldProcess | Warning | Yes | — | Reliability |
| UseApprovedVerbs | Warning | Yes | — | Maintainability |
| UseBOMForUnicodeEncodedFile | Warning | Yes | — | Compatibility |
| UseCmdletCorrectly | Warning | Yes | — | Reliability |
| UseCompatibleCmdlets | Warning | Yes | Yes ² | Compatibility |
| UseCompatibleCommands | Warning | No | Yes | Compatibility |
| UseCompatibleSyntax | Warning | No | Yes | Compatibility |
| UseCompatibleTypes | Warning | No | Yes | Compatibility |
| UseConsistentIndentation | Warning | No | Yes | Style |
| UseConsistentWhitespace | Warning | No | Yes | Style |
| UseCorrectCasing | Information | No | Yes | Style |
| UseDeclaredVarsMoreThanAssignments | Warning | Yes | — | Reliability |
| UseLiteralInitializerForHashtable | Warning | Yes | — | Reliability |
| UseOutputTypeCorrectly | Information | Yes | — | Maintainability |
| UseProcessBlockForPipelineCommand | Warning | Yes | — | Reliability |
| UsePSCredentialType | Warning | Yes | — | Security |
| UseShouldProcessForStateChangingFunctions | Warning | Yes | — | Maintainability |
| UseSingularNouns | Warning | Yes | Yes | Maintainability |
| UseSupportsShouldProcess | Warning | Yes | — | Maintainability |
| UseToExportFieldsInManifest | Warning | Yes | — | Maintainability |
| UseUsingScopeModifierInNewRunspaces | Warning | Yes | — | Reliability |
| UseUTF8EncodingForHelpFile | Warning | Yes | — | Compatibility |

**Notes:**
- ¹ Not available on all PowerShell versions/editions/platforms — check rule docs for availability
- ² Has configurable properties but cannot be fully disabled like other configurable rules
- **Total: 69 rules** (7 Error, 51 Warning, 8 Information, 3 DSC Error)

---

## 5. Rules by Quality Dimension

### 5.1 Security

Security rules target credential exposure, injection risks, and unsafe authentication patterns. These are the highest-priority rules for any production or automation context.

| Rule | Severity | Default | Risk Description |
|------|----------|---------|-----------------|
| **AvoidUsingConvertToSecureStringWithPlainText** | Error | Yes | `ConvertTo-SecureString -AsPlainText` exposes plaintext secrets in script. Secrets visible in logs, memory dumps, version control. |
| **AvoidUsingComputerNameHardcoded** | Error | Yes | Hardcoded `-ComputerName` embeds infrastructure topology in code — information disclosure, portability failure. |
| **AvoidUsingUsernameAndPasswordParams** | Error | Yes | Separate `-Username`/`-Password` parameters expose credentials as plaintext strings. Use `PSCredential` instead. |
| **AvoidUsingPlainTextForPassword** | Warning | Yes | Parameter names like `$Password`, `$pass`, `$Pwd` without `SecureString` type signal plaintext credential handling. |
| **AvoidUsingAllowUnencryptedAuthentication** | Warning | Yes | `-AllowUnencryptedAuthentication` on `Invoke-WebRequest`/`Invoke-RestMethod` sends credentials over HTTP. |
| **AvoidUsingBrokenHashAlgorithms** | Warning | Yes | Flags use of MD5, SHA1 — cryptographically broken; use SHA256+ for integrity checks. |
| **AvoidUsingInvokeExpression** | Warning | Yes | `Invoke-Expression` evaluates arbitrary strings — primary vector for code injection. Avoid entirely in automation/agentic contexts. |
| **UsePSCredentialType** | Warning | Yes | Credential parameters should be typed `[PSCredential]` to enforce structured handling and prevent accidental string conversion. |

**Additional security best practices (TBD — no rule yet):**
- Avoid initializing API key/credential variables (information disclosure)
- Use `-SecureString` for all sensitive parameter types
- Validate certificate thumbprints before trust decisions

---

### 5.2 Reliability

Reliability rules catch logic errors, scoping issues, pipeline misuse, and patterns that produce incorrect results silently.

| Rule | Severity | Default | What It Catches |
|------|----------|---------|-----------------|
| **ReservedCmdletChar** | Error | Yes | Cmdlet names containing characters reserved by PowerShell parser (`,`, `{`, `}`, `(`, `)`, `$`, etc.) |
| **ReservedParams** | Error | Yes | Using reserved parameter names (`Verbose`, `Debug`, `ErrorAction`, `WarningAction`, `InformationAction`, `ErrorVariable`, `WarningVariable`, `InformationVariable`, `OutVariable`, `OutBuffer`, `PipelineVariable`) |
| **AvoidAssignmentToAutomaticVariable** | Warning | Yes | Assigning to `$_`, `$PSItem`, `$true`, `$false`, `$null` etc. — corrupts runtime state |
| **AvoidDefaultValueForMandatoryParameter** | Warning | Yes | Mandatory params with defaults are contradictory — default is never used, misleads readers |
| **AvoidDefaultValueSwitchParameter** | Warning | Yes | Switch parameters defaulting to `$true` break conventional switch semantics |
| **AvoidInvokingEmptyMembers** | Warning | Yes | Calling empty string member expressions (`$obj.''`) — always a bug |
| **AvoidMultipleTypeAttributes** | Warning | Yes | Multiple `[type]` attributes on a parameter causes unexpected coercion behavior |
| **AvoidShouldContinueWithoutForce** | Warning | Yes | `ShouldContinue` without a `$Force` parameter check prevents non-interactive/automated execution |
| **AvoidUsingEmptyCatchBlock** | Warning | Yes | Empty `catch {}` silently swallows exceptions — masks errors, makes debugging impossible |
| **MisleadingBacktick** | Warning | Yes | Trailing backtick with whitespace after it — line continuation appears to work but doesn't |
| **PossibleIncorrectComparisonWithNull** | Warning | Yes | `$var -eq $null` should be `$null -eq $var` — when `$var` is a collection, left-hand comparison returns filtered results, not Boolean |
| **PossibleIncorrectUsageOfAssignmentOperator** | Warning | Yes | `=` used where `-eq` was intended in conditional expressions |
| **PossibleIncorrectUsageOfRedirectionOperator** | Warning | Yes | `>` used where `-gt` was intended in conditional expressions |
| **ReviewUnusedParameter** | Warning | Yes | Parameters declared but never referenced in function body — likely dead code or typo |
| **ShouldProcess** | Warning | Yes | `SupportsShouldProcess` declared but `ShouldProcess()`/`ShouldContinue()` not called (or vice versa) |
| **UseCmdletCorrectly** | Warning | Yes | Cmdlets invoked without required mandatory parameters |
| **UseDeclaredVarsMoreThanAssignments** | Warning | Yes | Variables assigned but never read — dead assignments, potential logic errors |
| **UseLiteralInitializerForHashtable** | Warning | Yes | `New-Object Hashtable` is slower and less idiomatic than `@{}` literal syntax |
| **UseProcessBlockForPipelineCommand** | Warning | Yes | Functions accepting pipeline input without a `process {}` block only process last pipeline item |
| **UseUsingScopeModifierInNewRunspaces** | Warning | Yes | Variables used in `Start-Job`, `Invoke-Command`, `ForEach-Object -Parallel` need `$using:` scope modifier |

---

### 5.3 Maintainability

Maintainability rules enforce naming conventions, documentation, scoping discipline, and API hygiene that make scripts readable and evolvable.

| Rule | Severity | Default | What It Enforces |
|------|----------|---------|-----------------|
| **UseApprovedVerbs** | Warning | Yes | Function names must use PowerShell's approved verb list (`Get`, `Set`, `New`, `Remove`, etc.) — discoverability and consistency |
| **AvoidUsingCmdletAliases** | Warning | Yes | Aliases (`ls`, `gci`, `%`, `?`, `ft`) are session-dependent, break portability across environments and users |
| **AvoidUsingPositionalParameters** | Warning | Yes | Named parameters are self-documenting; positional parameters break readability and refactoring |
| **AvoidGlobalVars** | Warning | Yes | Global variables create hidden state coupling across modules and functions |
| **AvoidGlobalFunctions** | Warning | Yes | Global functions pollute the global scope; keep functions module-scoped |
| **AvoidGlobalAliases** | Warning | Yes | Creating global aliases can conflict with user aliases and other modules |
| **AvoidOverwritingBuiltInCmdlets** | Warning | Yes | Redefining `Get-ChildItem`, `Write-Host`, etc. causes subtle, hard-to-debug breakage |
| **AvoidReservedWordsAsFunctionNames** | Warning | Yes | Function names matching reserved keywords (`foreach`, `if`, `switch`) cause parse conflicts |
| **AvoidUsingWMICmdlet** | Warning | Yes | WMI cmdlets (`Get-WmiObject`) are deprecated; use CIM cmdlets (`Get-CimInstance`) — WMI lacks PS Remoting support |
| **AvoidUsingWriteHost** | Warning | Yes | `Write-Host` bypasses the pipeline and cannot be captured/redirected; use `Write-Output`, `Write-Verbose`, `Write-Information` |
| **AvoidUsingDeprecatedManifestFields** | Warning | Yes | Module manifests using deprecated fields (`ModuleToProcess` instead of `RootModule`) |
| **AvoidNullOrEmptyHelpMessageAttribute** | Warning | Yes | `[Parameter(HelpMessage='')]` is useless — omit or provide meaningful message |
| **MissingModuleManifestField** | Warning | Yes | Module manifest missing required fields: `Version`, `Author`, `Description`, `LicenseUri` (PSGallery) |
| **UseToExportFieldsInManifest** | Warning | Yes | `FunctionsToExport`, `CmdletsToExport`, `VariablesToExport`, `AliasesToExport` should be explicit arrays, not wildcards |
| **UseShouldProcessForStateChangingFunctions** | Warning | Yes | State-changing functions (verbs: `Set`, `Update`, `Remove`, `New`) should support `-WhatIf`/`-Confirm` |
| **UseSupportsShouldProcess** | Warning | Yes | If a function calls `ShouldProcess`, the `[CmdletBinding(SupportsShouldProcess)]` attribute must be declared |
| **UseSingularNouns** | Warning | Yes | Noun in function name should be singular (`Get-Item`, not `Get-Items`) — PowerShell naming convention |
| **ReviewUnusedParameter** | Warning | Yes | Dead parameters — see Reliability above; also a maintainability signal |
| **ProvideCommentHelp** | Information | Yes | Functions should have comment-based help (`<# .SYNOPSIS .DESCRIPTION .PARAMETER .EXAMPLE #>`) |
| **UseOutputTypeCorrectly** | Information | Yes | `[OutputType()]` attribute should match actual types returned to pipeline |

---

### 5.4 Style & Formatting

Style rules are primarily disabled by default — they're opt-in for teams that want consistent formatting enforced. The **CodeFormatting** preset enables the most important subset.

| Rule | Severity | Default | Configuration |
|------|----------|---------|---------------|
| **AlignAssignmentStatement** | Warning | **No** | Aligns `=` in consecutive assignment blocks for readability |
| **AvoidExclaimOperator** | Warning | **No** | Prefer `-not` over `!` for negation — industry convention for PowerShell |
| **AvoidLongLines** | Warning | **No** | Configurable max line length (default: 120 chars) |
| **AvoidSemicolonsAsLineTerminators** | Warning | **No** | Semicolons as line terminators are legal but unconventional in PowerShell |
| **AvoidTrailingWhitespace** | Warning | Yes | Trailing whitespace causes noise in diffs |
| **AvoidUsingDoubleQuotesForConstantString** | Information | **No** | `"constant"` should be `'constant'` — signals no interpolation needed; minor perf and clarity benefit |
| **PlaceCloseBrace** | Warning | **No** | Brace placement style (Allman vs K&R variants) — configurable |
| **PlaceOpenBrace** | Warning | **No** | Open brace placement — configurable (OnSameLine, NewLineAfter, IgnoreOneLineBlock) |
| **UseConsistentIndentation** | Warning | **No** | Enforces tabs vs spaces, indentation size, pipeline indentation style |
| **UseConsistentWhitespace** | Warning | **No** | Whitespace around operators, braces, parentheses, pipes, separators |
| **UseCorrectCasing** | Information | **No** | Cmdlet names should match canonical casing (`Get-ChildItem`, not `get-childitem`) |

**CodeFormatting preset defaults:**
- Indentation: 4 spaces
- Open brace: same line (`if ($x) {`)
- Pipeline indentation: increase for first pipe
- Consistent whitespace: check inner braces, open braces, open parens, operators, pipes, separators

---

### 5.5 Compatibility

Compatibility rules catch scripts that will break when run on different PowerShell versions or platforms (Windows PowerShell 5.1, PowerShell 7.x, Linux, macOS).

| Rule | Severity | Default | What It Checks |
|------|----------|---------|----------------|
| **UseCompatibleCmdlets** | Warning | Yes | Cmdlets that don't exist on all target platforms/versions (configurable target list) |
| **UseCompatibleCommands** | Warning | **No** | Commands (including external tools) not available in target environments |
| **UseCompatibleSyntax** | Warning | **No** | Syntax features not supported in older PowerShell versions (e.g., ternary `?:` operator requires PS 7.0+) |
| **UseCompatibleTypes** | Warning | **No** | .NET types/static methods/properties unavailable in target PS environments |
| **UseBOMForUnicodeEncodedFile** | Warning | Yes | Unicode-encoded files should include BOM for Windows PowerShell 5.1 compatibility |
| **UseUTF8EncodingForHelpFile** | Warning | Yes | Help files (`.txt`) must be UTF-8 for correct display across locales |

**Configuration example** (target multiple environments):
```powershell
@{
    Rules = @{
        PSUseCompatibleSyntax = @{
            Enable = $true
            TargetVersions = @('5.1', '7.0', '7.2', '7.4')
        }
        PSUseCompatibleCmdlets = @{
            compatibility = @('desktop-5.1.0-windows', 'core-7.4.0-linux')
        }
    }
}
```

---

### 5.6 DSC (Desired State Configuration)

DSC rules are activated via the **DSC preset** (`-Settings DSC`) or by including `PSDSC*` rules.

| Rule | Severity | Default | What It Checks |
|------|----------|---------|----------------|
| **DSCStandardDSCFunctionsInResource** | **Error** | Yes | Class-based or script-based DSC resource must implement `Get`, `Set`, `Test` functions |
| **DSCUseIdenticalMandatoryParametersForDSC** | **Error** | Yes | `Get`, `Set`, `Test` methods must share identical mandatory parameters |
| **DSCUseIdenticalParametersForDSC** | **Error** | Yes | `Set` and `Test` methods must have identical parameter sets |
| **DSCUseVerboseMessageInDSCResource** | **Error** | Yes | DSC resources must use `Write-Verbose` for diagnostic messages |
| **DSCReturnCorrectTypesForDSCFunctions** | Information | Yes | `Get` returns object, `Test` returns Boolean, `Set` returns nothing |
| **DSCDscTestsPresent** | Information | Yes | DSC resource module should include Pester tests |
| **DSCDscExamplesPresent** | Information | Yes | DSC resource module should include usage examples |

---

## 6. PSGallery Requirements

The PowerShell Gallery **enforces PSScriptAnalyzer scanning** on all published packages. As of current policy:

| Requirement | Enforcement |
|-------------|-------------|
| All **Error**-severity violations | **Blocking** — must be fixed before publication |
| All **Warning**-severity violations | **Non-blocking but reviewed** — must be addressed or documented |
| **PSGallery preset** rules | Specific subset enforced (see Section 3) |
| Module manifest completeness | `Version`, `Author`, `Description`, `LicenseUri` required |
| Code signing | Strongly recommended; required for AllSigned execution policy environments |

**PSGallery quality signals that matter:**
- `ProvideCommentHelp` — documentation presence
- `MissingModuleManifestField` — manifest completeness
- `UseToExportFieldsInManifest` — explicit export declarations (not wildcards)
- `UseApprovedVerbs` — discoverability via `Get-Command -Verb`

**Best practice command for PSGallery submission validation:**
```powershell
Invoke-ScriptAnalyzer -Path /path/to/module/ -Settings PSGallery -Recurse
Invoke-ScriptAnalyzer -Path /path/to/module/ -Severity Error, Warning -Recurse
```

---

## 7. PowerShell-Specific Code Hygiene

Beyond PSScriptAnalyzer rules, PowerShell has well-established hygiene patterns. Items marked **TBD** are on the PSScriptAnalyzer roadmap but lack rules today.

### Parameter Validation

| Pattern | Status | Notes |
|---------|--------|-------|
| Use `[ValidateNotNull()]`, `[ValidateNotNullOrEmpty()]` | Best practice | Not currently enforced by PSSA |
| Use `[ValidateSet()]` for constrained values | Best practice | Enables tab completion |
| Use `[ValidateRange()]` for numeric bounds | Best practice | |
| Use `[ValidatePattern()]` for regex-constrained strings | Best practice | |
| Avoid bare `[string]` for passwords | `PSAvoidUsingPlainTextForPassword` | Enforced |
| Typed parameters (avoid `[object]` or untyped) | Best practice | Not enforced |

### Error Handling Patterns

| Pattern | PSScriptAnalyzer Status | Notes |
|---------|------------------------|-------|
| Never use empty `catch {}` | `PSAvoidUsingEmptyCatchBlock` ✓ | Enforced — Warning |
| Use `-ErrorAction Stop` with cmdlets in `try/catch` | **TBD** | No rule yet; community best practice |
| Set `$ErrorActionPreference = 'Stop'` for strict scripts | **TBD** | No rule yet |
| Avoid `$?` for error checking | **TBD** | `$?` is fragile; prefer try/catch |
| Copy `$Error[0]` to local variable before it's overwritten | **TBD** | No rule yet |
| Avoid flag-based error handling | **TBD** | No rule yet |
| Avoid `$null` as error sentinel | **TBD** | No rule yet |

### Pipeline Best Practices

| Pattern | PSScriptAnalyzer Status | Notes |
|---------|------------------------|-------|
| Use `process {}` block for pipeline-accepting functions | `PSUseProcessBlockForPipelineCommand` ✓ | Enforced |
| Avoid breaking pipeline with `Write-Host` | `PSAvoidUsingWriteHost` ✓ | Enforced |
| Write single objects to pipeline per iteration | **TBD** | Prevents array accumulation |
| Use `[OutputType()]` declaration | `PSUseOutputTypeCorrectly` ✓ | Enforced (Information) |
| Avoid pipelines in scripts where performance matters | **TBD** | Community guidance |

### Module Structure

| Pattern | PSScriptAnalyzer Status | Notes |
|---------|------------------------|-------|
| Explicit `FunctionsToExport` (not `'*'`) | `PSUseToExportFieldsInManifest` ✓ | Enforced |
| Complete module manifest fields | `PSMissingModuleManifestField` ✓ | Enforced |
| Avoid deprecated manifest fields | `PSAvoidUsingDeprecatedManifestFields` ✓ | Enforced |
| Module loadable without errors | **TBD** | No rule yet |
| Unresolved dependencies are errors | **TBD** | No rule yet |
| Specify `RequiredModules` in manifest | Best practice | Ensures dependency installation |
| Version all dependencies with `RequiredVersion` or `ModuleVersion` | Best practice | Prevents version mismatch |

### Scope & State Discipline

| Pattern | PSScriptAnalyzer Status | Notes |
|---------|------------------------|-------|
| No global variables | `PSAvoidGlobalVars` ✓ | Enforced |
| No global functions | `PSAvoidGlobalFunctions` ✓ | Enforced |
| No global aliases | `PSAvoidGlobalAliases` ✓ | Enforced |
| Use `$using:` in runspaces | `PSUseUsingScopeModifierInNewRunspaces` ✓ | Enforced |
| No assignment to automatic variables | `PSAvoidAssignmentToAutomaticVariable` ✓ | Enforced |

---

## 8. Agentic & Automation Patterns

Rules with highest relevance to agentic, non-interactive, and infrastructure automation contexts — i.e., scripts that run unattended, handle credentials, access remote systems, or execute dynamically-constructed code.

### 8.1 Credential & Secret Handling

| Rule | Severity | Agentic Concern |
|------|----------|-----------------|
| `PSAvoidUsingConvertToSecureStringWithPlainText` | **Error** | Hardcoded secrets in automation scripts → leaked in version control, logs, process lists |
| `PSAvoidUsingUsernameAndPasswordParams` | **Error** | String-typed credential params → credentials visible in `Get-History`, transcripts, log files |
| `PSAvoidUsingPlainTextForPassword` | Warning | Parameter naming signals → static analysis tools and code reviewers flag these |
| `PSUsePSCredentialType` | Warning | `[PSCredential]` type enforces structured handling; integrates with credential stores, `Get-Credential` |
| `PSAvoidUsingComputerNameHardcoded` | **Error** | Hardcoded hostnames create fragile automation; fails across environments (dev/test/prod) |

**Agentic guidance:** Use `[PSCredential]` with credential stores (Windows Credential Manager, Azure Key Vault, HashiCorp Vault). Never pass secrets as string parameters. Use `-Credential` with PSCredential objects.

### 8.2 Remote Execution Safety

| Rule | Severity | Agentic Concern |
|------|----------|-----------------|
| `PSAvoidUsingAllowUnencryptedAuthentication` | Warning | HTTP credential transmission in automation → credential interception on network |
| `PSAvoidUsingComputerNameHardcoded` | **Error** | Fixed targets in automation prevent parameterization, break multi-environment pipelines |
| `PSUseUsingScopeModifierInNewRunspaces` | Warning | Variables not accessible in `Invoke-Command`, `Start-Job`, `ForEach-Object -Parallel` → silent failures |
| `PSAvoidShouldContinueWithoutForce` | Warning | Interactive prompts in automation hang indefinitely; require `-Force` bypass path |
| `PSUseShouldProcessForStateChangingFunctions` | Warning | `-WhatIf` support essential for dry-run testing of state-changing automation |

**Agentic guidance:** Always test remoting code with `-Force` parameter paths. Use `-ErrorAction Stop` in remote sessions. Validate all `$using:` variable references in parallel/remote contexts.

### 8.3 Code Injection Prevention

| Rule | Severity | Agentic Concern |
|------|----------|-----------------|
| `PSAvoidUsingInvokeExpression` | Warning | Evaluates arbitrary string as PowerShell code → primary injection vector in automation that processes external input (API responses, user data, log files) |
| `PSAvoidUsingBrokenHashAlgorithms` | Warning | MD5/SHA1 for integrity verification → tampered payload passes verification in automated deployment pipelines |

**Agentic guidance:** Never use `Invoke-Expression` with externally-sourced strings. Replace with:
- `[scriptblock]::Create()` + explicit parameter passing (safer but not immune)
- Parameterized invocations
- Parser-level validation before evaluation

### 8.4 Script Signing & Trust

PSScriptAnalyzer does not currently have rules for script signing, but the PowerShell Gallery and enterprise execution policy patterns require:

| Consideration | Guidance |
|---------------|---------|
| Code signing for gallery modules | Use `Set-AuthenticodeSignature` with a code signing certificate |
| `AllSigned` execution policy environments | All scripts and modules must be signed by a trusted publisher |
| `RemoteSigned` execution policy | Downloaded scripts must be signed; local scripts do not |
| Signature verification in automation | `Get-AuthenticodeSignature` before executing downloaded scripts |
| Certificate chain validation | Validate issuer chain, not just signature presence |

### 8.5 Non-Interactive Execution Patterns (TBD Rules)

These have no PSSA rules but are critical for agentic reliability:

```powershell
# Good: Explicit error action in automation
try {
    Invoke-Command -ComputerName $Target -ScriptBlock $sb -ErrorAction Stop
} catch {
    Write-Error "Remote execution failed: $_"
    throw
}

# Good: Force parameter bypass for automation
function Remove-OldLogs {
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
    param(
        [switch]$Force
    )
    if ($Force -or $PSCmdlet.ShouldProcess($Path, 'Delete logs')) {
        # safe to proceed
    }
}

# Bad: Empty catch silences automation failures
try { ... } catch { }  # PSAvoidUsingEmptyCatchBlock fires

# Bad: Prompt in automation
$answer = Read-Host "Continue? (y/n)"  # hangs unattended — no PSSA rule yet
```

---

## 9. Custom Rules & Configuration

### Settings File Structure

```powershell
# PSScriptAnalyzerSettings.psd1
@{
    Severity     = @('Error', 'Warning')
    ExcludeRules = @('PSAvoidUsingWriteHost')
    IncludeRules = @('PSAvoidUsingPlainTextForPassword', 'PSAvoidUsingInvokeExpression')
    Rules        = @{
        PSUseConsistentIndentation = @{
            Enable          = $true
            Kind            = 'space'
            IndentationSize = 4
        }
        PSAvoidLongLines = @{
            Enable            = $true
            MaximumLineLength = 120
        }
    }
}
```

### Suppression Mechanism

Rules can be suppressed in-code with `[SuppressMessageAttribute]`:

```powershell
function MyFunc {
    [Diagnostics.CodeAnalysis.SuppressMessageAttribute(
        'PSAvoidUsingWriteHost', '',
        Justification = 'Interactive UI function; pipeline capture not required'
    )]
    param()
    Write-Host "Output to console"
}
```

Suppression scope can target: Function, Class, or specific parameter names.

### Custom Rule Modules

Custom rules must:
1. Be a PowerShell module (`.psm1` or module folder)
2. Export functions with the verb `Measure` (`Measure-*`)
3. Return `[Microsoft.Windows.PowerShell.ScriptAnalyzer.Generic.DiagnosticRecord]` objects

```powershell
# PSScriptAnalyzerSettings.psd1
@{
    CustomRulePath = @(
        '.\rules\MyCustomRules',
        '.\rules\SecurityRules'
    )
    IncludeRules   = @('Measure-*')
}
```

---

## 10. Quality Dimension Cross-Reference

Summary mapping of all 69 rules to their primary quality dimension:

| Dimension | Rule Count | Error | Warning | Information |
|-----------|-----------|-------|---------|-------------|
| **Security** | 8 | 3 | 5 | 0 |
| **Reliability** | 20 | 2 | 17 | 1 |
| **Maintainability** | 20 | 0 | 17 | 3 |
| **Style/Formatting** | 11 | 0 | 9 | 2 |
| **Compatibility** | 6 | 0 | 6 | 0 |
| **DSC** | 7 | 4 | 0 | 3 |
| **TOTAL** | **72** ¹ | **9** | **54** | **9** |

> ¹ Some rules appear in multiple dimensions (e.g., `ReviewUnusedParameter` spans Reliability and Maintainability). Raw rule count is 69 unique rules.

### Rules by PSGallery Risk Level

| Risk Level | Rules | Action |
|-----------|-------|--------|
| 🔴 **PSGallery Blocking** (Error) | `AvoidUsingConvertToSecureStringWithPlainText`, `AvoidUsingComputerNameHardcoded`, `AvoidUsingUsernameAndPasswordParams`, `ReservedCmdletChar`, `ReservedParams`, `DSCStandardDSCFunctionsInResource`, `DSCUseIdenticalMandatoryParametersForDSC`, `DSCUseIdenticalParametersForDSC`, `DSCUseVerboseMessageInDSCResource` | Must fix |
| 🟡 **PSGallery Reviewed** (Warning, PSGallery preset) | `UseApprovedVerbs`, `ShouldProcess`, `UseSingularNouns`, `MissingModuleManifestField`, `AvoidDefaultValueSwitchParameter`, `AvoidUsingCmdletAliases`, `AvoidUsingWMICmdlet`, `AvoidUsingEmptyCatchBlock`, `UseCmdletCorrectly`, `AvoidUsingPositionalParameters`, `AvoidGlobalVars`, `UseDeclaredVarsMoreThanAssignments`, `AvoidUsingInvokeExpression`, `AvoidUsingPlainTextForPassword`, `AvoidUsingComputerNameHardcoded`, `UsePSCredentialType` | Should fix |
| 🟢 **Quality Enhancement** (Warning/Info, not in PSGallery preset) | All style/formatting rules, compatibility rules (configurable), remaining reliability rules | Opt-in |

---

## References

- [PSScriptAnalyzer Rule List — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/rules/readme)
- [PSScriptAnalyzer Rules & Recommendations — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/rules-recommendations)
- [Using PSScriptAnalyzer — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/using-scriptanalyzer)
- [PowerShell Gallery Publishing Guidelines](https://learn.microsoft.com/en-us/powershell/gallery/concepts/publishing-guidelines)
- [PSScriptAnalyzer GitHub Repository](https://github.com/PowerShell/PSScriptAnalyzer)
- [PSGallery.psd1 Preset](https://github.com/PowerShell/PSScriptAnalyzer/blob/main/Engine/Settings/PSGallery.psd1)
- [CodeFormatting.psd1 Preset](https://github.com/PowerShell/PSScriptAnalyzer/blob/main/Engine/Settings/CodeFormatting.psd1)
- [The Unofficial PowerShell Best Practices and Style Guide](https://github.com/PoshCode/PowerShellPracticeAndStyle)
- [DSC Resource Style Guidelines](https://github.com/PowerShell/DscResources/blob/master/StyleGuidelines.md)
