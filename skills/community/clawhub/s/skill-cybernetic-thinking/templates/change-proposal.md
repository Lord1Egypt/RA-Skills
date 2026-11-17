# Change Proposal (cybernetic thinking scaffold)

Fill this in before a non-trivial change. It forces the control-theoretic mindset: name the
plant, the setpoint, the actuator, and how you will know it converged.

## Target
- **Controlled variable x** (what must stay correct):
  _________________________________
- **Setpoint x*** (target / invariant / acceptable range):
  _________________________________

## Plant & model
- **Current behavior** (measured, not assumed):
  _________________________________
- **Mental model of the plant** (and where it may be wrong):
  _________________________________
- **Model validity range** (inputs/sizes/conditions where the model holds):
  _________________________________

## Control action
- **Control variable u** (the lever I will change):
  _________________________________
- **Bounds on u** (max retries / depth / rate / size):
  _________________________________
- **Sensors** (how I will observe x after the change — tests/logs/metrics):
  _________________________________

## Disturbances
- **Known external kicks** (load, network, other services):
  _________________________________
- **Feedforward (if measurable)** / **feedback only (if not)**:
  _________________________________

## Convergence
- **Pass condition** (bounded deviation ||ε|| under which perturbation?):
  _________________________________
- **Test / observation that proves it**:
  _________________________________

## Coupling
- **Subsystems that must stay separate** (decouple harmful coupling):
  _________________________________
- **Subsystems that must stay coordinated** (keep beneficial coupling, regulate relations):
  _________________________________

---
Anti-patterns to avoid:
- Unbounded retry/recursion/allocation → saturation → instability
- Feature creep before the base is stable → divergence
- Optimization before correctness → wrong trajectory
- Guessing the cause without measurement → open-loop patch
