# Install SeekDB — Linux yum (RPM)

**Supported systems:** Anolis OS 8.X/23.X, CentOS 7.X/9.X, openEuler 22.03/24.03 (kernel 4.19+)
**Minimum requirements:** 1-core CPU, 2 GB RAM, `jq` and MySQL client installed, systemd available, sudo privileges.

---

## Step 1 — Check prerequisites

```bash
systemctl --version 2>/dev/null | head -1 || echo "systemd not available"
command -v jq || echo "jq not installed"
```
If `jq` is missing: `sudo yum install -y jq`

## Step 2 — Install SeekDB

Ask the user if they have network access to the internet:

- **Online install — yum repo (recommended):**
```bash
yum-config-manager --add-repo https://mirrors.oceanbase.com/oceanbase/community/stable/el/\$releasever/\$basearch/
sudo yum install -y seekdb
```

- **Online install — script (alternative):**

> **Security note:** The following command downloads and executes a remote script with root privileges. Review the script content before running, or prefer the yum repo method above.

```bash
curl -fsSL https://obbusiness-private.oss-cn-shanghai.aliyuncs.com/download-center/opensource/seekdb/seekdb_install.sh -o /tmp/seekdb_install.sh
# Review the script before executing:
less /tmp/seekdb_install.sh
sudo bash /tmp/seekdb_install.sh
```

- **Offline install** (if user has downloaded the RPM package):
```bash
sudo rpm -ivh seekdb-*.rpm
```
If the user needs to download the RPM first, direct them to the seekdb software download center to pick their version, OS, and CPU architecture.

## Step 3 — (Optional) Edit configuration

Before first start, the user can edit:
```bash
sudo vim /etc/seekdb/seekdb.cnf
```
Key options with defaults:
```
port=2881
data-dir=/var/lib/oceanbase/store   # requires >15G free disk
redo-dir=/var/lib/oceanbase/store/redo
cpu_count=4                          # 0 = auto-detect
memory_limit=2G
```

## Step 4 — Start and enable the service

```bash
sudo systemctl start seekdb
sudo systemctl enable seekdb
```

## Step 5 — Verify service status

```bash
sudo systemctl status seekdb
```
Success: `Active: active (running)` and `Status: seekdb is ready and running`.
If `failed`, check the journal:
```bash
journalctl -u seekdb -n 50 --no-pager
```
Diagnose and fix any errors.

## Step 6 — Verify connectivity

```bash
mysql -h 127.0.0.1 -u root -P 2881 -A -Dtest -e "SELECT 'SeekDB is running!' AS status;"
```

## Step 7 — Done

Confirm success and show:
- MySQL port: `127.0.0.1:2881`
- Config file: `/etc/seekdb/seekdb.cnf`
- Service management: `sudo systemctl {start|stop|status} seekdb`
- Uninstall: `sudo yum erase seekdb && sudo bash /var/lib/seekdb/seekdb_clean.sh`

---

## References

- Deploy by systemd: <https://docs.seekdb.ai/seekdb/deploy-by-systemd/>
