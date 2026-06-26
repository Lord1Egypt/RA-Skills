---
name: yara-authoring
description: Write high-quality YARA-X detection rules for malware identification and threat hunting. Covers naming conventions, string selection, performance optimization, and false positive reduction. Use when writing, reviewing, or optimizing YARA rules, converting IOCs to signatures, or debugging detection issues.
---

# YARA-X Rule Authoring

Write detection rules that catch malware without drowning in false positives. Based on Trail of Bits methodology.

## Core Principles

1. **Strings must generate good atoms** — YARA extracts 4-byte subsequences for fast matching. Strings with repeated bytes, common sequences, or under 4 bytes force slow bytecode scans.
2. **Target specific families, not categories** — "Detects ransomware" is useless. "Detects LockBit 3.0 config extraction routine" is useful.
3. **Test against goodware** — Validate against clean file sets before deployment.
4. **Short-circuit with cheap checks first** — `filesize < 10MB and uint16(0) == 0x5A4D` before expensive string searches.
5. **Metadata is documentation** — Future you needs to know what this catches and why.

## YARA-X Basics

YARA-X is the Rust successor to legacy YARA: 5-10x faster, better errors, built-in formatter, stricter validation, new modules (crx, dex).

**Install:** `brew install yara-x` / `cargo install yara-x`
**Commands:** `yr scan`, `yr check`, `yr fmt`, `yr dump`

## Rule Template

```yara
import "pe"

rule FamilyName_Variant_Technique : tag1 tag2 {
    meta:
        author      = "Solomon Neas"
        date        = "2026-02-14"
        description = "Detects [specific behavior] in [malware family]"
        reference   = "https://..."
        tlp         = "TLP:WHITE"
        hash        = ""
        score       = 75  // 0-100 confidence

    strings:
        // Unique strings from the sample
        $api1 = "VirtualAllocEx" ascii
        $api2 = "WriteProcessMemory" ascii
        $str1 = { 48 8B 05 ?? ?? ?? ?? 48 85 C0 }  // hex with wildcards
        $pdb  = /[A-Z]:\\.*\\Release\\.*\.pdb/ nocase

    condition:
        uint16(0) == 0x5A4D and
        filesize < 5MB and
        (2 of ($api*) and $str1) or
        $pdb
}
```

## Naming Convention

`Family_Variant_Technique` — examples:
- `Emotet_Loader_DocumentMacro`
- `CobaltStrike_Beacon_x64`
- `Generic_Cryptominer_XMRig`

## String Selection

**Good strings (unique, specific):**
- Mutex names, PDB paths, C2 URLs
- Unique byte sequences from disassembly
- Custom encryption constants
- Uncommon API call sequences

**Bad strings (too common, high FP):**
- `http://`, `https://`, common API names alone
- Single common words, short strings (<4 bytes)
- Strings found in Windows system files

## Condition Patterns

```yara
// Performance-ordered (cheap → expensive)
condition:
    uint16(0) == 0x5A4D and     // Magic bytes (instant)
    filesize < 10MB and          // Size filter (instant)
    2 of ($unique*) and          // String matching (fast)
    pe.imports("kernel32.dll")   // Module check (slower)
```

**Common magic bytes:**
| Platform | Check |
|----------|-------|
| PE (Windows) | `uint16(0) == 0x5A4D` |
| ELF (Linux) | `uint32(0) == 0x464C457F` |
| Mach-O 64-bit | `uint32(0) == 0xFEEDFACF` |
| PDF | `uint32(0) == 0x25504446` |
| Office/ZIP | `uint32(0) == 0x504B0304` |

## Performance Rules

1. Put `filesize` and magic byte checks FIRST in condition
2. Never use unbounded regex like `/.*/`
3. Avoid `for all` with complex conditions on large files
4. Use `ascii` or `wide`, not both unless needed
5. Hex strings with specific bytes > wildcards > regex
6. Use `at` for fixed offsets instead of scanning entire file

## Testing

```bash
# Validate syntax
yr check rules/

# Scan a sample
yr scan rules/my_rule.yar suspicious_file.exe

# Scan directory
yr scan rules/ samples/ --threads 4

# Format rules consistently
yr fmt rules/my_rule.yar
```

## False Positive Reduction

- Add `filesize` constraints (malware has typical size ranges)
- Require multiple string matches (`2 of ($str*)` not `any of`)
- Exclude known good paths/publishers via `not` conditions
- Score-based approach: assign confidence scores in metadata, triage by threshold
- Test against goodware corpus before deployment

## Reference

Full methodology, module docs (pe, elf, crx, dex), and migration guide from legacy YARA:
https://github.com/trailofbits/skills/tree/main/plugins/yara-authoring
