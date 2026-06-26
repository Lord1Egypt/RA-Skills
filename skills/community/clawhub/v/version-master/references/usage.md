# Version-Master 3.0 Reference

## CLI Usage

Call `version_tool.py` directly from the command line:

### 1. List Versions
```bash
# List all files with version history
python version_tool.py list

# List version details of a specific file
python version_tool.py list --file report.md
```

### 2. Save Version
```bash
# Save a specific file
python version_tool.py save --file report.md -m "Updated chapter 3"
```

### 3. Diff Versions
```bash
# Compare two historical versions
python version_tool.py diff --file report.md --v1 1 --v2 2

# Compare current file with a historical version
python version_tool.py diff --file report.md --v2 2
```

### 4. Restore Version
```bash
# Requires confirmation
python version_tool.py restore --file report.md --version 1 --confirm
```

### 5. Clean Versions
```bash
# Delete a specific version (requires confirmation)
python version_tool.py clean --file report.md --version 1 --confirm

# Delete all versions (requires confirmation)
python version_tool.py clean --file report.md --confirm
```

## Python API Usage

Call via the `VersionMaster` class in Python:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
from version_tool import VersionMaster

tool = VersionMaster()  # Uses current working directory by default

# Save version
tool.save_version(file_path="report.md", message="Updated chapter 3")

# List versions
tool.list_versions()                        # All files overview
tool.list_versions(file_path="report.md")   # Single file details

# Diff versions
tool.diff_versions(file_path="report.md", version1=1, version2=2)
tool.diff_versions(file_path="report.md", version2=2)  # Current file vs v2

# Restore version (requires confirm=True)
tool.restore_version(file_path="report.md", version=1, confirm=True)

# Clean versions (requires confirm=True)
tool.clean_versions(file_path="report.md", version=1, confirm=True)
tool.clean_versions(file_path="report.md", confirm=True)  # Delete all versions
```

## Return Format

All operations return a dictionary with a `success` field:

```json
{"success": true, "file": "report.md", "version": 3, "summary": "..."}
{"success": false, "error": "Error description"}
{"success": false, "requires_confirmation": true, "message": "Confirmation required..."}
```

## Safety Confirmation

`restore` and `clean` operations require `confirm=True`, otherwise they return a `requires_confirmation` response.
