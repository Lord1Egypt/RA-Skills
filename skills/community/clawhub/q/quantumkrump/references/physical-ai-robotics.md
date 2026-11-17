# Physical AI Humanoid Robotics & Whole-Body Dynamics

This reference specifies how Quantum Krump foundational mechanics translate into humanoid robotics, whole-body Model Predictive Control (MPC), and affective physical AI.

---

## 1. Centroidal Dynamics & Ground Reaction Forces

Translating high-energy Krump movements (particularly `STOMP` and `CHEST POP`) to humanoid robotic platforms requires managing rapid contact force spikes while preserving dynamic stability:

### 1.1 Centroidal Momentum Dynamics
The total linear momentum $\mathbf{p} \in \mathbb{R}^3$ and angular momentum $\mathbf{L}_G \in \mathbb{R}^3$ about the Center of Mass (CoM) $\mathbf{r}_{\text{CoM}}$ follow:
$$\dot{\mathbf{p}} = \sum_{c \in \mathcal{C}} \mathbf{f}_c + m \mathbf{g}$$
$$\dot{\mathbf{L}}_G = \sum_{c \in \mathcal{C}} (\mathbf{r}_c - \mathbf{r}_{\text{CoM}}) \times \mathbf{f}_c + \boldsymbol{\tau}_c$$
where $\mathcal{C}$ denotes active foot contact points, $\mathbf{f}_c$ are contact ground reaction forces (GRFs), and $\boldsymbol{\tau}_c$ are contact torques.

### 1.2 The 3.82× Body-Weight Stomp Impact
In authentic Krump execution, an explosive downward `STOMP` produces a vertical ground reaction force peak:
$$F_z^{\text{peak}} = 3.82 \, m g$$
- **Contact Duration**: $\Delta t \approx 45\text{--}65\,\text{ms}$.
- **Robotic Control Challenge**: Without active compliance and impedance control, such impacts trigger structural damage or slip boundary violations ($\|\mathbf{f}_{\parallel}\| \le \mu f_z$).
- **MPC Solution**: Whole-body MPC schedules contact phase switching, pre-impact leg stiffness modulation, and torso center-of-mass damping to absorb and redirect the kinetic rebound into the subsequent chest pop or arm swing.

---

## 2. Vitality Affects & Affective Kinesthetic Resonance

Physical AI in humanoid performance requires more than trajectory tracking; it demands the communication of intention and emotional vitality:

### 2.1 Daniel Stern's Vitality Affects
Movement is characterized by dynamic shapes: *surging*, *fading*, *fleeting*, *explosive*, or *sustained*.
- In Krump:
  - `JAB`: *Explosive, fleeting linear burst* ($\frac{d^3 x}{dt^3}$ jerk maximization).
  - `CHEST POP`: *Surging, percussive thoracic expansion*.
  - `ARM SWING`: *Flowing, curvilinear momentum transfer*.

### 2.2 Affective Kinesthetic Resonance
Human observers judge robotic dance not by kinematic accuracy, but by somatic empathy—the perception of effort, weight, and commitment. By regulating actuator torque profiles to match Laban Effort polarities (Weight, Time, Space, Flow), the robot achieves genuine kinesthetic resonance with the human audience.
