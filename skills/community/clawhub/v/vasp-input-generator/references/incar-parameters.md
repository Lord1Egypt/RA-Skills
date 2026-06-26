# VASP INCAR Parameters Reference

Comprehensive reference for VASP INCAR parameters.

## Electronic Minimization

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| `ENCUT` | Plane-wave cutoff energy (eV) | 400-600 (check POTCAR) |
| `EDIFF` | Electronic convergence criterion | 1E-5 to 1E-7 |
| `NELM` | Maximum electronic steps | 60-100 |
| `ALGO` | Electronic minimization algorithm | Normal, Fast, Very_Fast, All |

### ALGO Options

- **Normal**: Blocked Davidson algorithm (recommended for most cases)
- **Fast**: Uses RMM-DIIS after a few steps
- **Very_Fast**: RMM-DIIS from the start (may be less stable)
- **All**: Uses all bands (for DOS/band structure)

## Ionic Minimization

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| `EDIFFG` | Ionic convergence criterion | -1E-3 to -1E-5 |
| `NSW` | Maximum ionic steps | 100-500 |
| `IBRION` | Ionic update algorithm | -1, 0, 1, 2, 3 |
| `ISIF` | Stress/force calculation | 2, 3, 4, 7 |
| `POTIM` | Time step for ionic motion | 0.1-1.0 |

### IBRION Options

- **-1**: No ionic updates (static calculation)
- **0**: Molecular dynamics
- **1**: Quasi-Newton (RMM-DIIS)
- **2**: Conjugate gradient (recommended for relaxation)
- **3**: Damped molecular dynamics

### ISIF Options

- **2**: Optimize ions only (fixed cell)
- **3**: Optimize ions + cell shape + volume (full relaxation)
- **4**: Optimize ions + cell shape (fixed volume)
- **7**: Optimize cell only (fixed ions)

## Smearing

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| `ISMEAR` | Smearing method | -5, 0, 1, 2 |
| `SIGMA` | Smearing width (eV) | 0.01-0.2 |

### ISMEAR Options

- **-5**: Tetrahedron method (DOS, insulators)
- **0**: Gaussian smearing (insulators, small gap)
- **1**: Methfessel-Paxton order 1 (metals)
- **2**: Methfessel-Paxton order 2 (metals, high T)

### Recommendations

- **Insulators/semiconductors**: `ISMEAR = 0`, `SIGMA = 0.05`
- **Metals**: `ISMEAR = 1` or `2`, `SIGMA = 0.2`
- **DOS calculations**: `ISMEAR = -5` (tetrahedron)

## Molecular Dynamics

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| `TEBEG` | Beginning temperature (K) | 300-1000 |
| `TEEND` | End temperature (K) | 300-1000 |
| `MDALGO` | MD algorithm | 1, 2, 11, 13 |
| `SMASS` | Nose mass parameter | -3.0 (NVT), 0 (NVE) |

### MDALGO Options

- **1**: Verlet algorithm (NVE ensemble)
- **2**: Nose-Hoover thermostat (NVT ensemble)
- **11**: Andersen thermostat
- **13**: Langevin dynamics

## Output Control

| Parameter | Description | Values |
|-----------|-------------|--------|
| `LREAL` | Real-space projection | Auto, .TRUE., .FALSE. |
| `LWAVE` | Write WAVECAR | .TRUE., .FALSE. |
| `LCHARG` | Write CHGCAR | .TRUE., .FALSE. |
| `LORBIT` | Orbital-resolved DOS | 10, 11, 12 |

### LORBIT Options

- **10**: No DOS, just PROCAR
- **11**: DOS + PROCAR with spherical harmonics
- **12**: DOS + PROCAR with lm-decomposed

## Spin Polarization

| Parameter | Description | Values |
|-----------|-------------|--------|
| `ISPIN` | Spin polarization | 1 (off), 2 (on) |
| `MAGMOM` | Initial magnetic moments | List of values |

### Example for Magnetic System

```
ISPIN = 2
MAGMOM = 5*1.0 3*0.0  # 5 atoms with 1 μB, 3 non-magnetic
```

## Parallelization

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| `NPAR` | Bands parallelization | sqrt(N_cores) |
| `LPLANE` | Plane-based parallelization | .TRUE. |
| `NSIM` | Simultaneous bands | 4-8 |

## van der Waals Corrections

| Parameter | Description | Values |
|-----------|-------------|--------|
| `IVDW` | vdW correction method | 10, 11, 12, 20, 21 |

### Common Options

- **10**: DFT-D2 (Grimme)
- **11**: DFT-D3 (Grimme)
- **12**: DFT-D3 with Becke-Jonson damping (recommended)
- **20**: TS method
- **21**: TS with Hirshfeld charges

## Dipole Corrections (for Slabs)

```
IDIPOL = 3          # Correct in all directions
LDIPOL = .TRUE.     # Enable dipole correction
DIPOL = 0.5 0.5 0.5 # Dipole center (fractional)
```

## Convergence Guidelines

### Electronic Convergence

| System Type | EDIFF |
|-------------|-------|
| Standard | 1E-5 |
| High precision | 1E-6 to 1E-7 |
| Metals (difficult) | 1E-6 |

### Ionic Convergence

| Application | EDIFFG |
|-------------|--------|
| Standard relaxation | -1E-3 |
| High precision | -1E-4 to -1E-5 |
| Transition states | -1E-4 |

## Common Calculation Setups

### Structural Optimization

```
ENCUT = 500
EDIFF = 1E-5
EDIFFG = -1E-3
NSW = 200
IBRION = 2
ISIF = 3
ISMEAR = 0
SIGMA = 0.05
```

### Single-Point Energy

```
ENCUT = 500
EDIFF = 1E-6
NSW = 1
ISMEAR = 0
SIGMA = 0.05
LCHARG = .TRUE.
LWAVE = .TRUE.
```

### Molecular Dynamics (NVT)

```
ENCUT = 500
EDIFF = 1E-5
NSW = 1000
IBRION = 0
POTIM = 1.0
TEBEG = 300
TEEND = 300
MDALGO = 2
SMASS = -3.0
ISMEAR = 1
SIGMA = 0.2
```

### Band Structure (Non-SCF)

```
ENCUT = 500
EDIFF = 1E-6
NSW = 1
ICHARG = 11
ISMEAR = 0
SIGMA = 0.05
LWAVE = .TRUE.
LCHARG = .TRUE.
```

### Density of States

```
ENCUT = 500
EDIFF = 1E-6
NSW = 1
ICHARG = 11
ISMEAR = -5
LORBIT = 11
```
