---
name: windows-package-manager-installer
description: install windows software and windows package manager environments. use when the user wants to install a windows application, explicitly wants to install or configure winget or chocolatey, wants a windows package management environment set up, or wants chatgpt to decide whether to use winget or chocolatey for installation. prefer package-manager-based installation, install missing package managers when needed, configure chocolatey with the tsinghua mirror, and report clear success or failure status.
---

# Windows Package Manager Installer

Use this skill to handle Windows software installation requests through package managers instead of manual download flows whenever possible.

## Workflow decision tree

1. Identify the user's goal.
   - **Install a specific Windows app** -> follow **Software installation workflow**.
   - **Install or configure winget / chocolatey / Windows package management environment** -> follow **Package manager environment workflow**.

2. Prefer package managers over direct-download instructions.
   - Check whether the target software is available in `winget`.
   - Check whether the target software is available in `choco`.
   - If at least one package manager supports the target, use a package-manager-based solution.

3. Decide package manager priority.
   - Prefer `winget` first for mainstream desktop apps available from the Microsoft ecosystem.
   - Prefer `choco` when `winget` is unavailable, broken, missing the package, or when the package is commonly better supported in Chocolatey.
   - If both are supported, choose the one with simpler and more reliable installation commands for the specific software.

4. If the selected package manager is missing, install it first.
   - Missing `winget` -> guide the user to install or repair App Installer / winget availability.
   - Missing `choco` -> install Chocolatey.
   - After Chocolatey installation, configure the Tsinghua mirror.

5. Finish every response with a status-oriented summary.
   - Confirm what is already installed.
   - Confirm what was installed or configured.
   - State the exact command to run next if the user still needs to execute something.
   - End with a clear success/failure-style message in Chinese.

## Software installation workflow

### Step 1: Normalize the target software
Extract the product name and normalize it to the likely package-manager search term.

Examples:
- "安装 vscode" -> search `Visual Studio Code` / `vscode`
- "安装微信" -> search `WeChat`
- "安装 7zip" -> search `7zip` / `7-Zip`

When the user provides a vague app name, prefer a best-effort search-and-install approach instead of asking unnecessary follow-up questions.

### Step 2: Check package-manager suitability
Use this order of reasoning:

1. Is this clearly a Windows desktop or CLI app? If yes, package managers are likely appropriate.
2. Is the app commonly distributed through `winget` or `choco`? If yes, prefer package-manager installation.
3. If the app is not likely to exist in either package manager, say so plainly and fall back to vendor-download guidance.

### Step 3: Check environment state
Before giving install commands, reason through these checks in order:

1. Is the machine Windows?
2. Is PowerShell available?
3. Is the session likely elevated as administrator when needed?
4. Is `winget` available?
5. Is `choco` available?

Use simple verification commands when helpful:

```powershell
$PSVersionTable.PSVersion
Get-Command winget -ErrorAction SilentlyContinue
Get-Command choco -ErrorAction SilentlyContinue
```

### Step 4: Choose commands
Default command patterns:

**winget install**
```powershell
winget search <name>
winget install --id <exact.id> --accept-source-agreements --accept-package-agreements
```

**choco install**
```powershell
choco search <name>
choco install <package-name> -y
```

Do not invent package IDs. If uncertain, tell the user to run the search command first and then provide the exact install command pattern.

### Step 5: Provide concise execution steps
Keep the output action-oriented:

1. Detect / confirm package manager availability
2. Install missing package manager if needed
3. Run the install command for the target software
4. Verify installation if practical

Useful verification examples:

```powershell
winget list --id <exact.id>
choco list --local-only
where.exe <binary-name>
```

## Package manager environment workflow

### winget workflow
Treat `winget` as a built-in-or-repairable Windows capability rather than a mirror-based package manager.

Use this approach:

1. Detect whether `winget` exists.
   ```powershell
   Get-Command winget -ErrorAction SilentlyContinue
   ```
2. If present, repair/update sources when needed.
   ```powershell
   winget source reset --force
   winget source update
   winget --info
   ```
3. If missing, explain that `winget` typically comes from **App Installer** on supported Windows versions.
4. Recommend one of these repair/install approaches in order:
   - Install or update **App Installer** from Microsoft Store
   - If Store is unavailable, use the official offline bundle route only if the exact source is known in the current conversation
5. After repair, verify:
   ```powershell
   winget --version
   winget source list
   ```

Do **not** claim that `winget` supports a standard Tsinghua mirror switch like Chocolatey. It usually does not.

### chocolatey workflow
When Chocolatey is missing, provide the standard elevated PowerShell installation flow and then configure the Tsinghua mirror.

Installation command pattern:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

Then configure the Tsinghua mirror:

```powershell
choco source disable -n chocolatey
choco source add -n tsinghua -s "https://mirrors.tuna.tsinghua.edu.cn/chocolatey/"
choco source list
```

If source replacement is not accepted by the local Chocolatey version or policy, explain that the default community source may remain enabled and clearly state the actual final source status.

### full environment setup checklist
When the user says things like "安装 Windows 包管理环境" or "安装 choco、winget", follow this sequence:

1. Check admin rights if relevant.
2. Check whether `winget` exists.
3. If missing, instruct repair/install through App Installer.
4. Check whether `choco` exists.
5. If missing, install Chocolatey.
6. Configure Chocolatey with the Tsinghua mirror.
7. Verify both tools.
8. End with a clear environment-ready message.

Recommended verification block:

```powershell
winget --version
winget source list
choco --version
choco source list
```

## Output format
Use this response structure by default, adapting as needed:

### 1. 判断结果
State whether the request should use `winget`, `choco`, both, or neither.

### 2. 执行步骤
Provide the exact commands in a minimal sequence.

### 3. 验证命令
Provide one or more commands the user can run to confirm success.

### 4. 最终提示
Always end with one of these styles:

- `环境安装成功：winget 与 Chocolatey 已可用，Chocolatey 已配置清华源。`
- `软件安装成功：已通过 <winget/choco> 完成安装。`
- `环境部分完成：<state what succeeded>；<state what still needs manual action>.`
- `安装失败：<state the blocker plainly>.`

## Guardrails

- Stay within Windows context.
- Prefer package-manager installation over manual website download whenever realistic.
- Never claim a package exists in `winget` or `choco` unless the current conversation already established it.
- Do not fabricate exact package IDs or source states.
- Be explicit when administrator privileges are required.
- When a package manager is missing, solve that before giving the target software install command.
- Always mention that Chocolatey is configured to use the Tsinghua mirror when that step is included.
