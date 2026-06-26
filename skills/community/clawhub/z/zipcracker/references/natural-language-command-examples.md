# Natural Language to Command Examples

## Table of Contents

- Generic triage
- Dictionary-driven requests
- Mask-driven requests
- Known-plaintext requests
- Template-KPA requests
- Extraction-first requests

## Generic triage

| User request | Recommended command | Why |
| --- | --- | --- |
| 帮我分析一下这个 ZIP，先别乱跑。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile <zip>` | Clue set is weak, so profile first. |
| 这个压缩包打不开，先看看是不是伪加密。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile <zip>` | Pseudo-encryption suspicion should be checked before brute force. |
| Crack this ZIP like a CTF challenge. | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile <zip>` then `python3 <skill-dir>/scripts/openclaw_zipcracker.py --auto-template-kpa <zip>` | Default world-class flow: inspect, then run the original engine path. |
| 先告诉我最值得跑的命令。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile <zip>` | The profile output includes recommended next commands. |

## Dictionary-driven requests

| User request | Recommended command | Why |
| --- | --- | --- |
| 用这个字典试一下这个 ZIP。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> <dict.txt>` | User already supplied the strongest clue. |
| 跑一下这个目录里的多个字典。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> <dict-dir>` | The bundled engine supports dictionary directories. |
| 这是个超大字典，别先数行数。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --skip-dict-count <zip> <huge-dict.txt>` | Skip upfront counting for better startup and steadier memory. |
| Just try the usual dictionaries first. | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip>` | Uses the bundled default dictionary sequence. |

## Mask-driven requests

| User request | Recommended command | Why |
| --- | --- | --- |
| 密码应该是四位数字。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -m '?d?d?d?d'` | Natural-language structure maps cleanly to a mask. |
| The password starts with `flag` and ends with two digits. | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -m 'flag?d?d'` | Strong structure clue, tighter than a generic wordlist. |
| 形态像一位大写、三位小写、三位数字。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -m '?u?l?l?l?d?d?d'` | Exact password shape is better than brute-force dictionaries. |
| 这个掩码很大，但我确认要跑。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --auto-large-mask <zip> -m '<mask>'` | Auto-confirms the large-mask safety prompt. |

## Known-plaintext requests

| User request | Recommended command | Why |
| --- | --- | --- |
| 我有一份已知明文，帮我走 KPA。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <plain.txt>` | Full plaintext is a stronger clue than dictionaries or masks. |
| 我有一个无密码 ZIP 参考包。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <plain.zip>` | Reference ZIPs are directly supported by the engine. |
| 我只知道一段明文在偏移 78 的位置。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <part.bin> --kpa-offset 78` | Partial KPA with explicit offset. |
| 除了偏移明文，我还知道开头是 `MZ`。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <part.bin> --kpa-offset 78 -x 0 4d5a` | Extra fixed bytes strengthen partial KPA. |
| 只用 `bkcrack`，不要回退其他方法。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> -kpa <plain.txt> --bkcrack` | Enforces a pure `bkcrack` recovery path. |

## Template-KPA requests

| User request | Recommended command | Why |
| --- | --- | --- |
| 这个压缩包里的文件像 PNG，试试模板明文攻击。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> --kpa-template png -c image.png` | Direct template KPA request. |
| The encrypted member looks like an EXE. | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> --kpa-template exe -c app.exe` | EXE templates are built in. |
| 看起来像 pcapng 包头。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py <zip> --kpa-template pcapng -c capture.pcapng` | Maps directly to a bundled template family. |
| 跑完整默认流，失败了就自动跟模板 KPA。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --auto-template-kpa <zip>` | Lets the engine escalate to template KPA when structure suggests it. |

## Extraction-first requests

| User request | Recommended command | Why |
| --- | --- | --- |
| 我只想把文件先拿出来，不在乎原始密码。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --skip-orig-password-recovery <zip> -kpa <plain.txt>` | Skip post-extraction password recovery. |
| 先恢复内容，原始 ZIP 密码以后再说。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --skip-orig-password-recovery <zip> -kpa <plain.txt>` | Same extraction-first preference. |
| 只要能解出来就行。 | `python3 <skill-dir>/scripts/openclaw_zipcracker.py --profile <zip>` | First inspect, then choose the quickest high-confidence route. |
