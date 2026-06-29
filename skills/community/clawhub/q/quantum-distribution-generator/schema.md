# Quantum Distribution Generator Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `quantum-distribution-generator`

x402 availability: not enabled for this product.

## `beta`

Action slug: `beta`

Price: `5` credits

Generate values from a beta distribution, useful for modeling probabilities and proportions.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `alpha` | `number` | no | Alpha shape parameter, must be > 0. |
| `beta_param` | `number` | no | Beta shape parameter, must be > 0. |
| `count` | `integer` | no | Number of values to generate (1-10000, quantum max 50). |
| `source` | `string` | no | Random source: 'quantum' or 'standard'. Quantum max count: 50. |

Sample parameters:

```json
{
  "alpha": 1,
  "beta_param": 1,
  "count": 1,
  "source": "quantum"
}
```

Generated JSON parameter schema:

```json
{
  "alpha": {
    "default": 1,
    "description": "Alpha shape parameter, must be > 0.",
    "required": false,
    "type": "number"
  },
  "beta_param": {
    "default": 1,
    "description": "Beta shape parameter, must be > 0.",
    "required": false,
    "type": "number"
  },
  "count": {
    "default": 1,
    "description": "Number of values to generate (1-10000, quantum max 50).",
    "maximum": 10000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "source": {
    "default": "quantum",
    "description": "Random source: 'quantum' or 'standard'. Quantum max count: 50.",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `binomial`

Action slug: `binomial`

Price: `5` credits

Generate values from a binomial distribution, modeling the number of successes in a fixed number of trials.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `count` | `integer` | no | Number of values to generate (1-10000, quantum max 200). |
| `n_trials` | `integer` | no | Number of trials per sample (1-10000, quantum max 50). |
| `p_success` | `number` | no | Probability of success per trial (0-1). |
| `source` | `string` | no | Random source: 'quantum' or 'standard'. Quantum limits: max 200 count, max 50 trials. |

Sample parameters:

```json
{
  "count": 1,
  "n_trials": 10,
  "p_success": 0.5,
  "source": "quantum"
}
```

Generated JSON parameter schema:

```json
{
  "count": {
    "default": 1,
    "description": "Number of values to generate (1-10000, quantum max 200).",
    "maximum": 10000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "n_trials": {
    "default": 10,
    "description": "Number of trials per sample (1-10000, quantum max 50).",
    "maximum": 10000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "p_success": {
    "default": 0.5,
    "description": "Probability of success per trial (0-1).",
    "maximum": 1,
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "source": {
    "default": "quantum",
    "description": "Random source: 'quantum' or 'standard'. Quantum limits: max 200 count, max 50 trials.",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `exponential`

Action slug: `exponential`

Price: `5` credits

Generate values from an exponential distribution, commonly used for modeling wait times and decay processes.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `count` | `integer` | no | Number of values to generate (1-10000). |
| `rate` | `number` | no | Rate parameter (lambda), must be > 0. |
| `source` | `string` | no | Random source: 'quantum' (default) or 'standard'. |

Sample parameters:

```json
{
  "count": 1,
  "rate": 1,
  "source": "quantum"
}
```

Generated JSON parameter schema:

```json
{
  "count": {
    "default": 1,
    "description": "Number of values to generate (1-10000).",
    "maximum": 10000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "rate": {
    "default": 1,
    "description": "Rate parameter (lambda), must be > 0.",
    "required": false,
    "type": "number"
  },
  "source": {
    "default": "quantum",
    "description": "Random source: 'quantum' (default) or 'standard'.",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `gamma`

Action slug: `gamma`

Price: `5` credits

Generate values from a gamma distribution, used for modeling wait times and skewed data.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `count` | `integer` | no | Number of values to generate (1-10000, quantum max 75). |
| `scale` | `number` | no | Scale parameter, must be > 0. |
| `shape` | `number` | no | Shape parameter, must be > 0. |
| `source` | `string` | no | Random source: 'quantum' or 'standard'. Quantum max count: 75. |

Sample parameters:

```json
{
  "count": 1,
  "scale": 1,
  "shape": 1,
  "source": "quantum"
}
```

Generated JSON parameter schema:

```json
{
  "count": {
    "default": 1,
    "description": "Number of values to generate (1-10000, quantum max 75).",
    "maximum": 10000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "scale": {
    "default": 1,
    "description": "Scale parameter, must be > 0.",
    "required": false,
    "type": "number"
  },
  "shape": {
    "default": 1,
    "description": "Shape parameter, must be > 0.",
    "required": false,
    "type": "number"
  },
  "source": {
    "default": "quantum",
    "description": "Random source: 'quantum' or 'standard'. Quantum max count: 75.",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `montecarlo_sample`

Action slug: `montecarlo-sample`

Price: `5` credits

Generate multi-dimensional Monte Carlo samples from uniform or normal distributions for simulation and analysis.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dimensions` | `integer` | no | Number of dimensions per sample (1-100). |
| `distribution_type` | `string` | no | Distribution for sampling: 'uniform' or 'normal'. |
| `samples` | `integer` | no | Number of samples to generate (1-1000000). |
| `source` | `string` | no | Random source: 'quantum' or 'standard'. |

Sample parameters:

```json
{
  "dimensions": 1,
  "distribution_type": "uniform",
  "samples": 1000,
  "source": "quantum"
}
```

Generated JSON parameter schema:

```json
{
  "dimensions": {
    "default": 1,
    "description": "Number of dimensions per sample (1-100).",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "distribution_type": {
    "default": "uniform",
    "description": "Distribution for sampling: 'uniform' or 'normal'.",
    "enum": [
      "uniform",
      "normal"
    ],
    "required": false,
    "type": "string"
  },
  "samples": {
    "default": 1000,
    "description": "Number of samples to generate (1-1000000).",
    "maximum": 1000000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "source": {
    "default": "quantum",
    "description": "Random source: 'quantum' or 'standard'.",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `poisson`

Action slug: `poisson`

Price: `5` credits

Generate values from a Poisson distribution, used for modeling count-based events (e.g., arrivals per hour).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `count` | `integer` | no | Number of values to generate (1-10000, quantum max 200). |
| `lambda_param` | `number` | no | Expected rate (lambda), must be > 0. |
| `source` | `string` | no | Random source: 'quantum' or 'standard'. Quantum max count: 200. |

Sample parameters:

```json
{
  "count": 1,
  "lambda_param": 1,
  "source": "quantum"
}
```

Generated JSON parameter schema:

```json
{
  "count": {
    "default": 1,
    "description": "Number of values to generate (1-10000, quantum max 200).",
    "maximum": 10000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "lambda_param": {
    "default": 1,
    "description": "Expected rate (lambda), must be > 0.",
    "required": false,
    "type": "number"
  },
  "source": {
    "default": "quantum",
    "description": "Random source: 'quantum' or 'standard'. Quantum max count: 200.",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `randomwalk`

Action slug: `randomwalk`

Price: `5` credits

Simulate a random walk in one or more dimensions starting from the origin. Quantum max 80 steps.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dimensions` | `integer` | no | Number of dimensions (1-100). |
| `source` | `string` | no | Random source: 'quantum' or 'standard'. Quantum max steps: 80. |
| `step_size` | `number` | no | Size of each step, must be > 0. |
| `steps` | `integer` | no | Number of steps (1-10000, quantum max 80). |

Sample parameters:

```json
{
  "dimensions": 1,
  "source": "quantum",
  "step_size": 1,
  "steps": 100
}
```

Generated JSON parameter schema:

```json
{
  "dimensions": {
    "default": 1,
    "description": "Number of dimensions (1-100).",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "source": {
    "default": "quantum",
    "description": "Random source: 'quantum' or 'standard'. Quantum max steps: 80.",
    "enum": [
      "quantum",
      "standard"
    ],
    "required": false,
    "type": "string"
  },
  "step_size": {
    "default": 1,
    "description": "Size of each step, must be > 0.",
    "required": false,
    "type": "number"
  },
  "steps": {
    "default": 100,
    "description": "Number of steps (1-10000, quantum max 80).",
    "maximum": 10000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```
