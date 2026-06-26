# Real Mistakes This Skill Is Designed To Catch

## 1. Treating preparation as success
```text
Preparing clawhub-release-auditor@0.1.0
```
Wrong conclusion: "Published successfully."
Correct interpretation: partial. Wait for the final publish result.

## 2. Ignoring explicit validation failure
```text
[ERROR] Validation failed: Unexpected key(s) in SKILL.md frontmatter: version.
```
Wrong next step: keep packaging or publishing anyway.
Correct interpretation: failure. Fix frontmatter first.

## 3. Ignoring path errors
```text
Error: Path must be a folder
```
Wrong next step: tell the user publish worked.
Correct interpretation: failure. The publish target path is wrong.

## 4. Treating auth failure as a generic glitch
```text
HTTP 401 authentication_error: invalid api key
```
Wrong next step: retry unrelated commands.
Correct interpretation: failure. Credential state must be fixed first.

## 5. Treating warning-bearing completion as fully done
```text
Security: CLEAN
Warnings: yes
```
Wrong next step: assume nothing else matters.
Correct interpretation: ambiguous. Something completed, but the warnings may still matter.
