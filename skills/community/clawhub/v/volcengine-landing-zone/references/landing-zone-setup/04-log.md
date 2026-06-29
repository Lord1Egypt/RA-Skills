---
stage_id: 04-log
stage_type: landing-zone-setup
user_step_name: 统一日志归集能力配置
user_goal: 完成组织级日志存储与审计跟踪配置
user_progress_text: 正在补齐统一日志归集能力
user_completion_text: 统一日志归集能力已完成
user_intro_why_now: 在基础组织、权限和账号关系稳定后，需要尽快把日志归集接上，后续审计和排障才有统一依据
user_intro_value: 帮用户建立统一的审计留痕入口，降低后续排障和合规核查成本
user_intro_outcome: 完成后会得到组织级日志投递和统一审计跟踪能力
purpose: Provide a unified organization-level audit and log-ingestion entry for later compliance and troubleshooting
---

# Phase 4: Centralized Logging (04-log)

**Target directory**: `./volcengine-landing-zone-workspace/blueprints/landing-zone-setup/04-log/`

## Phase Goal

- Create and enable organization-level operation audit trails
- Check and backfill the TOS activation state of the log archive account
- Record the log destination bucket and trail name

## Minimum Input

- `log_archive_account_id` should default to the log archive account ID produced by the organization and core-account phases
- Ask for `prefix` only when it is missing, because it is used for default naming of logging resources
- `trail_event_sources` is optional by default. Ask only when the user explicitly wants to narrow the audit scope
- Do not ask early in this phase for networking variables

## Execution Conventions

- Check the cross-account `AssumeRole` prerequisite only once before entering this phase. If the current login comes from the primary account, stop and ask the user to switch to an IAM sub-user with `STSAssumeRoleAccess`
- First run `ve organization RegisterDelegatedAdministrator --body '{"AccountId":"<log_archive_account_id>","ServicePrincipal":"cloud_trail"}'` in the organization-administrator context
- Duplicate or already-exists style results may be treated as satisfying the delegated-administrator prerequisite. Permission-denied, trusted-service-disabled, or organization-access-restricted errors should stop the phase
- Do not treat `AssumeRole succeeded + export STS environment variables` as a reliable identity-switch strategy for `ve` CLI. Use a temporary log profile instead
- Recommended order: record the original default profile -> register the delegated administrator -> assume role -> write a temporary log profile -> use the temporary profile for the TOS helper and CloudTrail commands -> restore the original profile and delete the temporary profile
- For `CreateTrail`, `StartLogging`, `DescribeTrails`, and `GetCallerIdentity`, pass `--profile <temp_log_profile>` explicitly as a second layer of safety
- The lifecycle of the temporary log profile must be managed with finally-style cleanup semantics. Whether this phase succeeds, fails, or is interrupted, always try to restore the original default profile and delete the temporary profile. Do not place cleanup only in the success branch
- Before this phase starts, if a same-name temporary log profile is left over from a previous run, clean the dirty state first and recreate it. Do not reuse it directly

## TOS Branch

- Check TOS state only in this phase, not earlier in global preflight
- The helper always uses the `cn-beijing` control plane
- If `GetAccountStatus` returns `Activated`, continue immediately
- If it returns `NonActivated`, run `ActiveTosSvc` first, then poll `GetAccountStatus` until it converges to `Activated`
- If it returns `Stopping`, `Closed`, or `Terminate`, or if automatic activation still cannot reach `Activated`, stop the phase and tell the user to handle the account-state or permission issue first

## Acceptance and Output

- Acceptance must include at least two steps: `ve sts GetCallerIdentity --profile <temp_log_profile>` and `ve cloudtrail20180101 DescribeTrails --profile <temp_log_profile> --TrailNames.1 <trail_name> --IncludeOrganizationTrail 1`
- After the phase completes, record at least the log destination bucket and the trail name
- Explain only confirmed results and real blockers to the user. Do not expand helper implementation details, signature details, or CLI parameter trial-and-error
