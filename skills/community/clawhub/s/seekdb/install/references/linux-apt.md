# Install SeekDB — Linux apt (DEB)

**Supported systems:** Debian 11/12/13, Ubuntu 20.04/22.04/24.04 (kernel 4.19+)
**Minimum requirements:** 1-core CPU, 2 GB RAM, `jq` and MySQL client installed, systemd available, sudo privileges.

---

## Step 1 — Check prerequisites

```bash
systemctl --version 2>/dev/null | head -1 || echo "systemd not available"
command -v jq || echo "jq not installed"
lsb_release -a 2>/dev/null
```
If `jq` is missing: `sudo apt install -y jq`

## Step 2 — Install SeekDB

Ask the user if they have network access to the internet:

- **Online install (recommended):**
```bash
echo "deb [trusted=yes] http://mirrors.aliyun.com/oceanbase/community/stable/$(lsb_release -is | awk '{print tolower($0)}')/$(lsb_release -cs)/$(dpkg --print-architecture)/ ./" \
  | sudo tee /etc/apt/sources.list.d/oceanbase.list
sudo apt update
sudo apt install seekdb
```

- **Offline install** (if user has downloaded the DEB package):
```bash
sudo dpkg -i seekdb-*.deb
```
If the user needs to download the DEB first, direct them to the seekdb software download center to pick their version, OS, and CPU architecture.

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
If `failed`, check: `journalctl -u seekdb -n 50 --no-pager`

## Step 6 — Verify connectivity

```bash
mysql -h 127.0.0.1 -u root -P 2881 -A -Dtest -e "SELECT 'SeekDB is running!' AS status;"
```

## Step 7 — Done

Confirm success and show:
- MySQL port: `127.0.0.1:2881`
- Config file: `/etc/seekdb/seekdb.cnf`
- Service management: `sudo systemctl {start|stop|status} seekdb`
- Uninstall: `sudo apt remove seekdb && sudo bash /var/lib/seekdb/seekdb_clean.sh`

---

## References

- Deploy by systemd: <https://docs.seekdb.ai/seekdb/deploy-by-systemd/>
