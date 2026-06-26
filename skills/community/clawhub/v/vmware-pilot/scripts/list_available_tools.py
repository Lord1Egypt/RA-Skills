#!/usr/bin/env python3
"""List all available VMware tools grouped by skill for workflow design.

Quick reference for designing workflows — shows every skill and its tools
with risk levels and brief descriptions.

Usage:
    python3 list_available_tools.py          # All skills
    python3 list_available_tools.py aiops    # Specific skill
    python3 list_available_tools.py --json   # JSON output
"""

from __future__ import annotations

import json
import sys
from typing import Any

SKILLS: dict[str, dict[str, Any]] = {
    "aiops": {
        "description": "VM lifecycle and operations (power, clone, deploy, reconfigure, guest ops)",
        "tools": {
            "vm_power_on":               {"risk": "medium", "desc": "Power on a VM"},
            "vm_power_off":              {"risk": "medium", "desc": "Power off a VM (graceful or force)"},
            "deploy_linked_clone":       {"risk": "medium", "desc": "Clone a VM from snapshot"},
            "vm_create_plan":            {"risk": "low",    "desc": "Create a batch operation plan (dry-run)"},
            "vm_apply_plan":             {"risk": "high",   "desc": "Execute a batch operation plan"},
            "vm_rollback_plan":          {"risk": "high",   "desc": "Rollback a batch operation plan"},
            "vm_guest_exec":             {"risk": "medium", "desc": "Run command inside guest OS"},
            "vm_guest_exec_output":      {"risk": "medium", "desc": "Run command inside guest OS and capture output"},
            "vm_guest_upload":           {"risk": "medium", "desc": "Upload file to guest OS"},
            "vm_guest_provision":        {"risk": "medium", "desc": "Bootstrap/provision a new VM"},
            "batch_clone_vms":           {"risk": "high",   "desc": "Clone multiple VMs at once"},
            "vm_clean_slate":            {"risk": "high",   "desc": "Revert VM to snapshot (destructive)"},
            "acknowledge_vcenter_alarm": {"risk": "low",    "desc": "Acknowledge a vCenter alarm"},
            "reset_vcenter_alarm":       {"risk": "low",    "desc": "Reset a vCenter alarm"},
            "cluster_create":            {"risk": "high",   "desc": "Create a new vSphere cluster"},
            "deploy_vm_from_ova":        {"risk": "medium", "desc": "Deploy VM from OVA file"},
            "deploy_vm_from_template":   {"risk": "medium", "desc": "Deploy VM from vCenter template"},
        },
    },
    "monitor": {
        "description": "Read-only vCenter monitoring (inventory, alarms, events, VM details)",
        "tools": {
            "list_virtual_machines": {"risk": "low", "desc": "List all VMs with summary info"},
            "list_esxi_hosts":       {"risk": "low", "desc": "List all ESXi hosts"},
            "list_all_datastores":   {"risk": "low", "desc": "List all datastores"},
            "list_all_clusters":     {"risk": "low", "desc": "List all clusters"},
            "get_alarms":            {"risk": "low", "desc": "Get active alarms"},
            "get_events":            {"risk": "low", "desc": "Get recent events (filterable by severity/hours)"},
            "vm_info":               {"risk": "low", "desc": "Detailed VM information"},
        },
    },
    "nsx": {
        "description": "NSX networking (segments, gateways, NAT, routing)",
        "tools": {
            "list_segments":        {"risk": "low",    "desc": "List network segments"},
            "create_segment":       {"risk": "medium", "desc": "Create overlay/VLAN segment"},
            "delete_segment":       {"risk": "high",   "desc": "Delete a segment"},
            "create_tier1_gateway": {"risk": "medium", "desc": "Create Tier-1 gateway"},
            "create_nat_rule":      {"risk": "medium", "desc": "Add NAT rule to gateway"},
            "list_nat_rules":       {"risk": "low",    "desc": "List NAT rules"},
        },
    },
    "nsx-security": {
        "description": "NSX DFW microsegmentation (firewall policies, groups, traceflow)",
        "tools": {
            "list_dfw_policies": {"risk": "low",    "desc": "List DFW policies"},
            "create_dfw_policy": {"risk": "medium", "desc": "Create DFW policy"},
            "create_dfw_rule":   {"risk": "medium", "desc": "Add rule to DFW policy"},
            "delete_dfw_rule":   {"risk": "high",   "desc": "Delete a DFW rule"},
            "create_group":      {"risk": "medium", "desc": "Create security group"},
            "run_traceflow":     {"risk": "low",    "desc": "Trace packet path through network"},
        },
    },
    "aria": {
        "description": "Aria Operations (vRealize) metrics, alerts, capacity, anomalies",
        "tools": {
            "list_alerts":                      {"risk": "low", "desc": "List active alerts"},
            "acknowledge_alert":                {"risk": "low", "desc": "Acknowledge an alert"},
            "get_capacity_overview":            {"risk": "low", "desc": "Overall capacity summary"},
            "get_remaining_capacity":           {"risk": "low", "desc": "Remaining capacity for a resource"},
            "get_time_remaining":               {"risk": "low", "desc": "Days until capacity exhaustion"},
            "list_anomalies":                   {"risk": "low", "desc": "List detected anomalies"},
            "list_rightsizing_recommendations":  {"risk": "low", "desc": "VM rightsizing suggestions"},
            "generate_report":                  {"risk": "low", "desc": "Generate capacity/health report"},
        },
    },
    "vks": {
        "description": "vSphere with Tanzu (VKS) Kubernetes management",
        "tools": {
            "create_namespace":   {"risk": "medium", "desc": "Create Supervisor Namespace"},
            "delete_namespace":   {"risk": "high",   "desc": "Delete Supervisor Namespace"},
            "create_tkc_cluster": {"risk": "medium", "desc": "Deploy TKC cluster"},
            "scale_tkc_cluster":  {"risk": "medium", "desc": "Scale TKC worker nodes"},
            "delete_tkc_cluster": {"risk": "high",   "desc": "Delete TKC cluster"},
            "get_tkc_kubeconfig": {"risk": "low",    "desc": "Retrieve kubeconfig for TKC cluster"},
        },
    },
    "storage": {
        "description": "Storage management (datastores, iSCSI, vSAN)",
        "tools": {
            "list_all_datastores":     {"risk": "low",    "desc": "List all datastores"},
            "storage_iscsi_enable":    {"risk": "medium", "desc": "Enable iSCSI adapter on host"},
            "storage_iscsi_add_target": {"risk": "medium", "desc": "Add iSCSI target to host"},
            "storage_rescan":          {"risk": "low",    "desc": "Rescan storage adapters"},
            "vsan_health":             {"risk": "low",    "desc": "Check vSAN health"},
            "vsan_capacity":           {"risk": "low",    "desc": "Check vSAN capacity"},
        },
    },
    "pilot": {
        "description": "Workflow orchestration (approval gates, rollback)",
        "tools": {
            "approve": {"risk": "high", "desc": "Human approval gate — pauses workflow"},
        },
    },
}


def print_table(skill_filter: str = "") -> None:
    """Print tools as a formatted table."""
    total_tools = 0

    for skill_name, skill_info in SKILLS.items():
        if skill_filter and skill_name != skill_filter:
            continue

        tools = skill_info["tools"]
        total_tools += len(tools)

        print(f"\n{'=' * 70}")
        print(f"  {skill_name}  ({len(tools)} tools)")
        print(f"  {skill_info['description']}")
        print(f"{'=' * 70}")
        print(f"  {'Tool':<35} {'Risk':<8} Description")
        print(f"  {'-' * 35} {'-' * 7} {'-' * 25}")

        for tool_name, tool_info in tools.items():
            risk = tool_info["risk"]
            desc = tool_info["desc"]
            risk_marker = {"low": " ", "medium": "*", "high": "!"}[risk]
            print(f"  {tool_name:<35} {risk_marker}{risk:<7} {desc}")

    print(f"\n  Total: {total_tools} tools across {len(SKILLS)} skills")
    print(f"  Risk legend:  (space)=low  *=medium  !=high")


def print_json(skill_filter: str = "") -> None:
    """Print tools as JSON."""
    if skill_filter:
        data = {skill_filter: SKILLS[skill_filter]} if skill_filter in SKILLS else {}
    else:
        data = SKILLS
    print(json.dumps(data, indent=2))


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--json"]
    use_json = "--json" in sys.argv

    skill_filter = ""
    if args:
        skill_filter = args[0]
        if skill_filter not in SKILLS:
            print(f"Unknown skill: '{skill_filter}'")
            print(f"Available skills: {', '.join(SKILLS.keys())}")
            return 1

    if use_json:
        print_json(skill_filter)
    else:
        print_table(skill_filter)

    return 0


if __name__ == "__main__":
    sys.exit(main())
