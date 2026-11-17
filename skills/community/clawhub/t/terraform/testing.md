# Testing And Policy — Proving A Change Before It Touches Production

## The Ladder

Run them in this order; each one costs more and catches what the previous cannot.

| Level | Tool | Catches | Cost |
|---|---|---|---|
| 1 | `terraform fmt -check -recursive` | Style drift | Instant |
| 2 | `terraform validate` | Type errors, unknown attributes, bad references | Needs `init`, no credentials |
| 3 | `tflint` | Invalid instance types, deprecated arguments, dead declarations — provider-aware, config-only | Seconds |
| 4 | Static scanners (checkov / tfsec / trivy) | Insecure defaults visible in HCL | Seconds, noisy without a baseline |
| 5 | `terraform test` with `command = plan` | Module contract: right resources, right attributes, validation failures | Seconds, no cloud objects |
| 6 | Policy on the plan JSON | What actually happens after variables, defaults, and modules resolve | Seconds |
| 7 | `terraform test` with `command = apply` (or a sandbox apply) | Quotas, IAM, name collisions, eventual consistency | Minutes and real money |
| else | Level 2 + 6 | The minimum any pipeline should have | — |

`validate` type-checks the configuration; it cannot know whether the cloud will accept it. Every failure class in level 7 is invisible to every level above it — which is why a sandbox account you can destroy nightly is infrastructure, not a luxury.

## `terraform test` (>=1.6)

```hcl
# tests/defaults.tftest.hcl
variables {
  name = "unit-test"
}

run "creates_one_bucket_with_encryption" {
  command = plan

  assert {
    condition     = aws_s3_bucket.this.bucket == "unit-test"
    error_message = "bucket name did not follow the naming rule"
  }
}

run "rejects_bad_environment" {
  command = plan
  variables {
    env = "prd"
  }
  expect_failures = [var.env]
}
```

- `command = plan` asserts on planned values without creating anything. `command = apply` creates real objects and destroys them at the end of the file, in reverse order.
- **A failed `apply` run can leave resources behind.** The CI job needs a cleanup step, and the test account needs a scheduled sweep.
- `expect_failures` is how you test `validation`, `precondition`, and `postcondition` blocks — the assertions most likely to be silently wrong.
- Tests live with the module and are its executable documentation. A module with tests gets adopted; a module with a README gets copy-pasted.

## Mocking (>=1.7)

```hcl
mock_provider "aws" {}
```

`mock_provider` lets `command = apply` run without a cloud: the provider returns generated values for computed attributes. That proves your wiring, your `for_each` keys, and your output plumbing. It proves nothing about whether the cloud accepts the request — mocks never reject an invalid instance type or a name that is already taken.

Use mocks for module logic, real applies for module viability. Both, not either.

## Policy On The Plan JSON

Write policies against the plan, not the HCL. The plan is post-resolution: it knows the actual values of variables, the defaults the provider filled in, and what the modules produced.

```bash
terraform show -json tfplan > plan.json
```

The assertions worth having in every repository:

- No deletes above `destroy_gate`, with the addresses printed on failure.
- Every created resource carries the mandatory tags.
- Nothing becomes publicly reachable (public IP, open ingress from `0.0.0.0/0`, public object access).
- No resource type from the banned list (whatever your organization has decided it will not run).
- Encryption enabled on every storage and database resource.
- Monthly cost delta above a threshold requires a named approver (any cost-estimation tool that reads the plan JSON).

Any policy engine works — conftest/OPA runs anywhere, Sentinel if you are on a managed platform, or plain `jq` for the first two or three rules. Starting with `jq` and three rules beats planning a policy framework for a quarter.

## Testing The Destroy Path

A module nobody has ever destroyed usually cannot be: dependency ordering breaks, deletion protection blocks, retained resources leave name collisions that make the next create fail. Run one full create-then-destroy cycle in the sandbox before calling a module done, and again after any resource is added.

## What Not To Test

- Provider behavior. Asserting that a bucket gets an ARN tests the provider's mock, not your code.
- Literal values you just wrote in the same file. A test that restates the config passes forever and catches nothing.
- Everything. The contract worth testing is the part other stacks depend on: outputs, naming, counts, and the guards that stop bad input.
