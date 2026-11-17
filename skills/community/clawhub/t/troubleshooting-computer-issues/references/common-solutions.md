# Common Solutions Quick Reference Index

Use this index to quickly resolve standard, high-frequency software installation and configuration issues.

---

## 1. Node.js & NPM

### Error: `npm ERR! EACCES: permission denied`
- **Root Cause**: NPM lacks permissions to write to global directory.
- **Solution (macOS/Linux)**:
  ```bash
  # Change owner of npm directories to current user
  sudo chown -R $(whoami) ~/.npm $(npm config get prefix)/{lib/node_modules,bin,share}
  ```
- **Solution (Windows)**: Run PowerShell or Command Prompt as Administrator.

### Error: `node: command not found` / `npm: command not found`
- **Root Cause**: Node.js path is not in the system environment PATH variables.
- **Solution (All OS)**: Add the installation directory to PATH.
  - Windows: `C:\Program Files\nodejs\`
  - macOS/Linux: Verify `PATH` in shell config file (`.zshrc`, `.bashrc`): `export PATH=/usr/local/bin:$PATH`

---

## 2. Python & PIP

### Error: `pip: command not found`
- **Root Cause**: PIP is either not installed or not in system PATH.
- **Solution (macOS/Linux)**:
  ```bash
  python3 -m ensurepip --default-pip
  ```
- **Solution (Windows)**: Re-run the python installer and ensure "Add Python to PATH" checkbox is selected.

### Error: `externally-managed-environment` (PEP 668)
- **Root Cause**: Modern Linux distros restrict global pip installation.
- **Solution**: Use a virtual environment:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
  pip install <package>
  ```

---

## 3. Git & GitHub

### Error: `Permission denied (publickey)`
- **Root Cause**: Git is attempting SSH auth, but the public key isn't registered with GitHub/GitLab, or the local ssh-agent doesn't have the private key loaded.
- **Solution**:
  ```bash
  # Check ssh keys
  ssh-add -l
  # If empty, add key
  ssh-add ~/.ssh/id_ed25519
  # Copy public key to clipboard and add to GitHub settings
  cat ~/.ssh/id_ed25519.pub
  ```

### Error: `gnutls_handshake() failed` / `SSL certificate problem`
- **Root Cause**: Git cannot verify SSL certificate (common behind proxies or corporate firewalls).
- **Solution (Temporary bypass - use with caution)**:
  ```bash
  git config --global http.sslVerify false
  ```

---

## 4. Docker & Containers

### Error: `Cannot connect to the Docker daemon`
- **Root Cause**: Docker service is not running, or current user is not in the `docker` group.
- **Solution (Linux)**:
  ```bash
  sudo systemctl start docker
  sudo usermod -aG docker $USER  # Log out and log back in to apply
  ```
- **Solution (macOS/Windows)**: Verify Docker Desktop application is running and its status icon is green.

---

## 5. System Permissions & Port Allocation

### Error: `EADDRINUSE: address already in use :::<Port>`
- **Root Cause**: Another process is already running on the target port.
- **Solution**:
  - Find the PID and terminate the process:
  - **Windows**:
    ```powershell
    (Get-NetTCPConnection -LocalPort <Port>).OwningProcess | Stop-Process -Force
    ```
  - **macOS/Linux**:
    ```bash
    kill -9 $(lsof -t -i:<Port>)
    ```
