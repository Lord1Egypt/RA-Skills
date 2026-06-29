---
stage_id: 05-network
stage_type: landing-zone-setup
user_step_name: 网络底座搭建
user_goal: 完成网络账号中的中转路由器、VPC、子网和连接配置
user_progress_text: 正在补齐网络底座
user_completion_text: 网络底座已完成
user_intro_why_now: 前面的组织、权限和日志基础完成后，需要把统一网络底座搭起来，后续业务账号接入才有标准入口
user_intro_value: 帮用户提前建立跨账号可扩展的网络承载能力，减少后续业务接入的重复建设
user_intro_outcome: 完成后会得到可复用的网络底座，便于后续业务 VPC 接入和互通规划
purpose: Provide a reusable network foundation for later workload-account onboarding and cross-account connectivity
---

# Phase 5: Network Foundation (05-network)

**Target directory**: `./volcengine-landing-zone-workspace/blueprints/landing-zone-setup/05-network/`

## Phase Goal

- Create the TR, VPC, dual-AZ subnets, and VPC attachment inside the network account
- Ensure `ServiceRoleForTransitRouter` is ready before creating the VPC attachment

## Minimum Input

- `network_account_id` should default to the network account ID produced by the organization and core-account phases
- Ask for `prefix` only when it is missing, because it is used for default naming of network-foundation resources
- Ask for `network_vpc_cidr`, `network_subnet_cidr_az_a`, and `network_subnet_cidr_az_b` only when address planning is still missing
- When asking about CIDRs, remind the user directly to avoid conflicts with existing networks. If defaults already exist, explain those defaults first and let the user decide whether to override them

## Execution Conventions

- Check the cross-account `AssumeRole` prerequisite only once before entering this phase. If the current login comes from the primary account, stop and ask the user to switch to an IAM sub-user with `STSAssumeRoleAccess`
- Before creating the TR VPC attachment, ensure that `ServiceRoleForTransitRouter` already exists inside the network account
- Prefer the idempotent command `ve iam CreateServiceLinkedRole --ServiceName transitrouter`
- Treat `RoleAlreadyExists` as already authorized
- If it returns insufficient-permission errors, tell the user the current identity lacks the IAM permissions needed for this authorization. If the current identity is an IAM sub-user, the user may refer to the TR FAQ and add `iam:GetRole` plus `iam:CreateRole`
- That service-linked role must be created in the network-account context, not accidentally in the management-account context

## Result Requirements

- After the phase completes, record at least the TR, VPC, subnets, VPC attachment, and the result of the service-linked-role check or authorization step
- In the result summary, state clearly whether the network foundation is complete, which resources were created successfully, whether any manual follow-up items remain, and whether the next recommended step is to start creating workload accounts
