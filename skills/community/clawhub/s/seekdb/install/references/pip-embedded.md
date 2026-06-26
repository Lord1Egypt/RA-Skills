# Install SeekDB — Embedded (pip)

**Supported platforms:** Linux x86_64, Linux aarch64 only. If the user is on macOS, tell them embedded mode is not supported and suggest Docker or Homebrew instead.

---

## Step 1 — Check Python version

```bash
python3 --version
```
If Python < 3.8 or not found, tell the user and stop. Ask them to install Python 3.8+ first.

## Step 2 — Install pyseekdb

```bash
pip install -U pyseekdb
```
Check the output. If there are errors (network, permission, etc.), diagnose and fix:
- Permission error → suggest `pip install --user -U pyseekdb` or using a venv
- Network error → suggest checking connectivity or using a mirror: `pip install -U pyseekdb -i https://pypi.tuna.tsinghua.edu.cn/simple`

## Step 3 — Verify installation

Run a quick smoke test:
```bash
python3 -c "import seekdb; print('seekdb version:', seekdb.__version__)"
```
If the import fails, diagnose the error output and fix it.

## Step 4 — Done

Tell the user installation is complete and show a minimal usage example:
```python
import seekdb

seekdb.open()
conn = seekdb.connect()
cursor = conn.cursor()
cursor.execute("SELECT * FROM oceanbase.DBA_OB_USERS")
print(cursor.fetchall())
conn.close()
```
Or using the higher-level client:
```python
import pyseekdb

client = pyseekdb.Client(path="./seekdb.db", database="test")
```

---

## References

- pyseekdb embedded install: <https://docs.seekdb.ai/seekdb/pyseekdb-sdk-get-started/#install-pyseekdb>
