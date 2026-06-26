# SecLists Wordlist Reference

Expected location: `/usr/share/seclists/`

## Directory/File Fuzzing

| Size | Path | Lines | Use Case |
|------|------|-------|----------|
| Small | Discovery/Web-Content/common.txt | 4,750 | Quick scan |
| Small | Discovery/Web-Content/quickhits.txt | 2,567 | High-value targets (.env, admin, backup) |
| Medium | Discovery/Web-Content/big.txt | 20,481 | Standard scan |
| Medium | Discovery/Web-Content/raft-medium-directories.txt | 29,999 | Thorough directory scan |
| Medium | Discovery/Web-Content/raft-medium-files.txt | 17,129 | File discovery |

## Subdomain Enumeration

| Size | Path | Lines |
|------|------|-------|
| Small | Discovery/DNS/subdomains-top1million-5000.txt | 5,000 |
| Medium | Discovery/DNS/subdomains-top1million-20000.txt | 20,000 |

## Other Useful Lists

| Path | Use Case |
|------|----------|
| Passwords/10k-most-common.txt | Password spraying |
| Fuzzing/LFI-Jhaddix.txt | Local file inclusion |

## Selection Logic

Scripts auto-select wordlists: try medium first, fall back to small, last resort `/usr/share/dirb/`.
