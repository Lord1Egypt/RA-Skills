# Secure Python Code Sandbox Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `secure-python-code-sandbox`

x402 availability: not enabled for this product.

## `invoke`

Action slug: `invoke`

Price: `10` credits

For safely executing arbitrary Python code snippets within an isolated, secure environment. The sandbox comes pre-installed with common data science and web request libraries, including requests, NumPy, and pandas. It is ideal for performing quick computations, data transformations, or dynamic API calls without requiring external infrastructure.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `code` | `string` | yes | A string containing the Python code to be executed. The code must be self-contained. Constraints: Maximum of 50,000 characters. Example: "import numpy as np\ndata = np.array([1, 2, 3, 4, 5])\nmean = np.mean(data)\nprint(\"The mean is {}\".format(mean))" |
| `timeout_seconds` | `number` | no | The maximum number of seconds to allow the code to run before terminating the execution. Default: 60 Constraints: Must be an integer between 10 and 60. |

Sample parameters:

```json
{
  "code": "example code",
  "timeout_seconds": 10
}
```

Generated JSON parameter schema:

```json
{
  "code": {
    "description": "A string containing the Python code to be executed. The code must be self-contained.\n\nConstraints: Maximum of 50,000 characters.\nExample: \"import numpy as np\\ndata = np.array([1, 2, 3, 4, 5])\\nmean = np.mean(data)\\nprint(\\\"The mean is {}\\\".format(mean))\"",
    "required": true,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "The maximum number of seconds to allow the code to run before terminating the execution.\n\nDefault: 60\nConstraints: Must be an integer between 10 and 60.\n",
    "maximum": 60,
    "minimum": 10,
    "required": false,
    "type": "number"
  }
}
```
