# Build SeekDB — Python Wheel

**Constraint:** must be built inside a manylinux container so the resulting wheel is portable
across glibc-compatible Linux distros.

---

## Steps

```bash
# Must run inside quay.io/pypa/manylinux_2_28
PACKAGE_VERSION=0.0.1
for python_home in /opt/python/cp3*/; do
    PACKAGE_VERSION=$PACKAGE_VERSION PYTHON_HOME=$python_home bash package/wheel/build_python.sh
done
# Artifacts: build_python/wheelhouse/seekdb-*.whl  seekdb_lib-*.whl
```

The loop produces one wheel per supported CPython minor version under `/opt/python/cp3*/`.
