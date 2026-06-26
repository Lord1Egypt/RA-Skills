# Bulletproof Code Patterns for Computational Biology

## Input Hardening (apply at every function boundary)

The most common crash source in scientific pipelines is type/shape ambiguity
at the boundary between NumPy, BioPython, MDAnalysis, and file I/O.

```python
import numpy as np

def harden_coords(coords) -> np.ndarray:
    """
    Normalize any coordinate-like input to a clean (N, 3) float64 array.
    Handles: nested lists, object arrays, MDAnalysis AtomGroup positions,
    BioPython Vector objects, and single-atom edge cases.
    """
    arr = np.array(coords, dtype=object)          # accept any nesting
    arr = np.array(arr.tolist(), dtype=np.float64) # force numeric cast
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)                   # single atom → (1,3)
    assert arr.shape[-1] == 3, f"Expected (N,3), got {arr.shape}"
    return np.ascontiguousarray(arr)

def to_py_float(val) -> float:
    """
    Strip any NumPy scalar wrapper before PDB formatting or JSON serialization.
    PDB formatters that call str(val) on a np.float64 sometimes emit
    scientific notation, breaking column-fixed PDB format.
    """
    return float(np.squeeze(val))
```

---

## Singular Matrix Fallback (linear algebra ops)

```python
from numpy.linalg import LinAlgError

def safe_eigvals(matrix: np.ndarray, fallback_si: float = 0.0):
    """
    Compute principal curvatures from a 2x2 shape operator matrix.
    Returns fallback (saddle point SI=0) if matrix is singular.
    SI=0 is the physically conservative choice: it avoids
    misclassifying a degenerate surface patch as a pit or cap.
    """
    try:
        eigenvalues = np.linalg.eigvalsh(matrix)
        k1, k2 = sorted(eigenvalues)               # k1 ≤ k2 by convention
        if abs(k1 - k2) < 1e-9:                   # degenerate: umbilic point
            return fallback_si
        si = (2 / np.pi) * np.arctan((k1 + k2) / (k1 - k2))
        return float(si)
    except LinAlgError:
        return fallback_si
```

---

## KD-Tree Spatial Indexing (replace O(N²) distance loops)

```python
from scipy.spatial import cKDTree

def build_interface_shell(
    coords_A: np.ndarray,
    coords_B: np.ndarray,
    cutoff: float = 5.0           # Å — typical interface definition
) -> tuple[np.ndarray, np.ndarray]:
    """
    Return indices of atoms in A and B that are within `cutoff` Å of
    the opposing chain. O(N log N) via KD-Tree vs O(N²) brute force.
    """
    coords_A = harden_coords(coords_A)
    coords_B = harden_coords(coords_B)
    tree_B = cKDTree(coords_B)
    tree_A = cKDTree(coords_A)
    idx_A = np.unique(np.concatenate(tree_B.query_ball_tree(tree_A, r=cutoff)))
    idx_B = np.unique(np.concatenate(tree_A.query_ball_tree(tree_B, r=cutoff)))
    return idx_A, idx_B
```

Complexity note: `cKDTree.query_ball_tree` is $O(N \log N)$ build + $O(N)$ query
for spatially uniform data. For dense protein cores this degrades; apply a coarse
grid pre-filter if $N > 50{,}000$ atoms.

---

## PDB B-factor Column Writer (avoid format crashes)

PDB format requires columns 61–66 to hold a right-justified float in `%6.2f`.
NumPy scalars and nested arrays will silently produce wrong output.

```python
def write_bfactor_pdb(template_pdb: str, output_pdb: str, scores: dict):
    """
    scores: {atom_serial (int): score (float-like)}
    Writes scores into B-factor column. All values are py_float()-hardened.
    """
    lines = []
    with open(template_pdb) as f:
        for line in f:
            if line.startswith(("ATOM", "HETATM")):
                serial = int(line[6:11])
                val = to_py_float(scores.get(serial, 0.0))
                val = max(-99.99, min(99.99, val))   # clamp to column width
                line = line[:60] + f"{val:6.2f}" + line[66:]
            lines.append(line)
    with open(output_pdb, "w") as f:
        f.writelines(lines)
```

---

## MDAnalysis Universe Loading with Error Recovery

```python
import MDAnalysis as mda

def load_universe(topology: str, trajectory: str | None = None) -> mda.Universe:
    """
    Load with format auto-detection. Provides actionable error messages
    instead of opaque MDAnalysis tracebacks.
    """
    try:
        if trajectory:
            u = mda.Universe(topology, trajectory)
        else:
            u = mda.Universe(topology)
        return u
    except Exception as e:
        msg = str(e)
        if "No atoms" in msg or "zero atoms" in msg:
            raise ValueError(
                f"Topology '{topology}' parsed as empty. "
                "Check file format, chain IDs, and CRYST1 record."
            ) from e
        if "FileNotFoundError" in type(e).__name__:
            raise FileNotFoundError(
                f"File not found: {topology!r}. "
                "Verify path and extension (.gro/.pdb/.psf)."
            ) from e
        raise RuntimeError(
            f"MDAnalysis failed to load: {msg}\n"
            "Try: mda.Universe(topology, format='PDB') to force format."
        ) from e
```

---

## Common Error → Root Cause Reference

| Error message | Root cause | Fix |
|--------------|------------|-----|
| `ValueError: too many values to unpack` | Eigenvector return has wrong shape (e.g., `(3,3)` not `(3,)`) | Use `eigvalsh` not `eig`; unpack with `k1,k2 = sorted(vals)` |
| `ValueError: could not broadcast input array` | Mixed (N,3) and (3,) shapes in `np.concatenate` | `harden_coords()` before any concat |
| `struct.error: required argument is not a float` | NumPy scalar passed to PDB formatter | `to_py_float()` before all string formatting |
| `LinAlgError: Singular matrix` | Surface patch has ≤2 neighbors; can't fit quadric | `safe_eigvals()` fallback to `SI=0` |
| `MemoryError` in grid allocation | Voxel grid at 0.5 Å resolution over full PDB | Switch to surface point cloud; only allocate shell atoms |
