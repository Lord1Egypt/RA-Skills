# Tripartite Structural Mapping: Laban × Krump × Bloch Sphere

This reference provides the rigorous mathematical, geometric, and kinesthetic foundation connecting Rudolf Laban's Effort taxonomy, authentic Krump foundations across vertical levels, and 3D Bloch-sphere quantum geometry.

---

## 1. Geometric Representation on the Bloch Sphere

The single-qubit quantum state is represented as a point on or inside the unit Bloch sphere $S^2$:
$$|\psi\rangle = \cos\left(\frac{\theta}{2}\right)|0\rangle + e^{i\varphi}\sin\left(\frac{\theta}{2}\right)|1\rangle, \quad \theta \in [0, \pi], \; \varphi \in [0, 2\pi)$$

```
                  |0> [LIVE / Up / Z+]
                       ^
                       |
        |-i> [Back]    |    |i> [Forward]
             \         |   /
              \        |  /
  |-> [Left] <---------+---------> |+> [Right / X+]
                \      |      /
                 \     |     /
                  \    |    /
                       v
                  |1> [BUCK / Down / Z-]
```

---

## 2. Complete Mapping Matrix

| Laban Effort Factor | Polarity | Krump Physical Foundation | Spatial Level | Bloch Coordinate / State | Quantum Pedagogical Analog |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Weight** | Strong (Heavy) | `STOMP` | `BUCK` (Low) | $|1\rangle$ ($Z = -1, \theta = \pi$) | Entangled ground anchor / Projective measurement |
| **Weight** | Light (Buoyant) | Postural Lift | `LIVE` (High) | $|0\rangle$ ($Z = +1, \theta = 0$) | Vacuum ground state / Reset |
| **Time** | Sudden (Percussive) | `CHEST POP` | `KRUMP` (Mid) | $Z = \sigma_z$ (Phase Flip) | Relative phase interference ($\Delta\varphi = \pi$) |
| **Time** | Sustained (Continuous)| Torso Groove | `KRUMP` (Mid) | $\text{ZZPhase}(\theta)$ | Continuous unitary phase evolution |
| **Space** | Direct (Linear) | `JAB` | `KRUMP` (Mid) | $X = \sigma_x$ (Bit Flip) | Pauli $X$ state inversion ($|0\rangle \leftrightarrow |1\rangle$) |
| **Space** | Indirect (Flexible) | Wring / Torso Twist | Multi-zone | Internal subsystem $A \otimes B$ | Internal degrees of freedom / Entanglement bridge |
| **Flow** | Free (Continuous) | `ARM SWING` | All levels | $R_x(\pi/2)$ (Equatorial sweep) | Coherent superposition preparation |
| **Flow** | Bound (Arrested) | `KILL-OFF` / Freeze | Grounded | $\epsilon_D$ (Projection/Cup) | Climax collapse into definitive basis state |

---

## 3. Dual Operational Regimes of `STOMP`

To prevent facilitator and dancer confusion, the framework formalizes two distinct operational roles for `STOMP`:

1. **Isolated Effort Drills (Measurement Collapse)**:
   In isolated Laban quality drills, a forceful, sudden downward `STOMP` embodies the percussive physical jolt of projective measurement, terminating ambiguity by anchoring the body into an unambiguous basis eigenstate ($|1\rangle$ or $|0\rangle$).

2. **Solo Phrase Building & Functor Compilation ($\mathcal{F}_{\mathrm{DisCo}}$)**:
   In choreographic phrase compilation, the opening `STOMP` functions as the phrase-launching Hadamard gate $H$: an explosive ground strike kicks the dancer out of the static, unperturbed vacuum basis posture ($|0\rangle$) into a balanced kinetic superposition ($\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$) that animates the entire movement phrase until a terminal `KILL-OFF` collapses it.

---

## 4. Rhythm as Quantum Phase, Polyrhythmic Beats, and the 140–150 BPM Krump Metric Lattice

While spatial dimensions define the Bloch sphere, **Rhythm** drives quantum time evolution:

### 4.1 Dynamic Phase Accumulation as Quantum Rhythm
For any energy eigenstate $|E_n\rangle$, the time-dependent Schrödinger equation dictates:
$$|\psi_n(t)\rangle = e^{-i E_n t / \hbar} |\psi_n(0)\rangle = e^{-i \omega_n t} |E_n\rangle, \quad \text{where } \omega_n = \frac{E_n}{\hbar}.$$
Every stationary quantum state possesses an intrinsic angular frequency $\omega_n$ (its internal micro-clock).

### 4.2 Polyrhythmic Interference and Quantum Beats
Superpositions of distinct energy eigenstates $|\Psi(0)\rangle = c_1 |E_1\rangle + c_2 |E_2\rangle$ exhibit macroscopic time-dependent modulation:
$$P(x, t) = |c_1|^2 |\psi_1(x)|^2 + |c_2|^2 |\psi_2(x)|^2 + 2 |c_1 c_2| \text{Re}\{\psi_1^*(x)\psi_2(x) e^{-i \Delta\omega t}\},$$
where $\Delta\omega = (E_2 - E_1)/\hbar$ is the Bohr transition frequency. This is the exact quantum equivalent of polyrhythmic musicality (e.g. 3-against-4 cross-rhythms) in Krump dance.

### 4.3 The 140–150 BPM Krump Metric Lattice
- Krump music operates at $140\text{ to }150\text{ BPM}$ (measure duration $\approx 1.655\text{ s}$, 16th-note syncopation intervals $\approx 103.4\text{ ms}$).
- **Beat 1 (Downbeat, $\varphi = 0$)**: Grounding foundation strike (`STOMP`); maximum real positive amplitude ($+1$).
- **Beat 2 (Off-beat accent, $\varphi = \pi/2$)**: Lateral directional impulse (`JAB`); imaginary phase ($+i$).
- **Beat 3 (Backbeat / Climax, $\varphi = \pi$)**: Explosive thoracic expansion (`CHEST POP`); anti-phase inversion ($-1$), creating maximal destructive interference against downbeats.
- **Beat 4 (Pickup / Transition, $\varphi = 3\pi/2$)**: Rotational sweep (`ARM SWING`); negative imaginary phase ($-i$).

### 4.4 Constructive vs. Destructive Rhythmic Interference
- **In-phase sync ($\Delta\varphi = 0$)**: Constructive interference doubles amplitude and quadruples session intensity ("hype").
- **Anti-phase opposition ($\Delta\varphi = \pi$)**: Destructive cancellation ($a_1 - a_2 = 0$) creates dramatic choreographic freezes and negative space.
