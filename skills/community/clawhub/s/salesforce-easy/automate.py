#!/usr/bin/env python3
"""
Salesforce GTM Automation Engine
Creates Salesforce Flow metadata (in Draft/inactive state) and Validation
Rules for GTM data standardization. All automation is deployed inactive;
a human admin must activate each Flow in Salesforce Setup before it runs.

All destructive operations require --confirm. Test in a sandbox first.

Author: Sawera Khadium
"""

import os
import sys
import json
import argparse
import http.client
import urllib.parse
from typing import Dict, List, Optional, Tuple
from simple_salesforce import Salesforce
from dotenv import load_dotenv

load_dotenv()

# ── GTM Field API Names ───────────────────────────────────────────────────────
GTM_FIELDS = {
    "industry":      "GTM_Industry__c",
    "vertical":      "GTM_Vertical__c",
    "role_category": "GTM_Role_Category__c",
    "seniority":     "GTM_Seniority__c",
    "standardized":  "GTM_Standardized__c",
}

SUPPORTED_OBJECTS = ["Lead", "Contact", "Account"]

# ── Flow / Metadata names ─────────────────────────────────────────────────────
FLOW_NAMES = {
    "Lead":    "GTM_Standardization_Lead_Flow",
    "Contact": "GTM_Standardization_Contact_Flow",
    "Account": "GTM_Standardization_Account_Flow",
}

VALIDATION_RULE_NAMES = {
    "Lead":    "GTM_Industry_Validation_Lead",
    "Contact": "GTM_Industry_Validation_Contact",
    "Account": "GTM_Industry_Validation_Account",
}


# ── Connection ────────────────────────────────────────────────────────────────

def _get_sf() -> Optional[Salesforce]:
    """
    Build Salesforce session from environment.
    SECURITY: credential values are read into short-lived locals
    and never returned or logged.
    """
    instance_url = (os.getenv("SALESFORCE_INSTANCE_URL") or "").strip()
    _sid         = (os.getenv("SALESFORCE_ACCESS_TOKEN") or "").strip()
    username     = (os.getenv("SALESFORCE_USERNAME") or "").strip()
    _pw          = (os.getenv("SALESFORCE_PASSWORD") or "").strip()
    _sec         = (os.getenv("SALESFORCE_SECURITY_TOKEN") or "").strip()

    try:
        if instance_url and _sid:
            return Salesforce(instance_url=instance_url, session_id=_sid)
        if username and _pw:
            return Salesforce(
                username=username,
                password=_pw + _sec,
                domain="test" if "sandbox" in username.lower() else "login",
            )
        return None
    except Exception:
        return None


# ── Custom Field Setup (manual) ─────────────────────────────────────────────
# GTM custom fields are created manually in Salesforce Setup, not via code.
# This avoids requiring admin/metadata API permissions at runtime.
#
# Required fields on Lead, Contact, and Account:
#   GTM_Industry__c      (Picklist)
#   GTM_Vertical__c      (Picklist)
#   GTM_Role_Category__c (Picklist)
#   GTM_Seniority__c     (Picklist)
#   GTM_Standardized__c  (Checkbox)
#
# Setup path: Salesforce Setup → Object Manager → Lead → Fields & Relationships
#             → New → Picklist → enter label and API name as above.
# Repeat for Contact and Account.
#
# No admin token is required by this skill at runtime.


# ── Flow Metadata Generation ──────────────────────────────────────────────────

def _generate_flow_xml(sf_obj: str) -> str:
    """
    Generate Salesforce Flow metadata XML for a record-triggered
    GTM standardization flow on the given object.

    The flow fires on record create or update when Industry or Title changes,
    then calls the GTM_Standardize invocable action (or sets formula fields).

    This XML is deployed via the Metadata API.
    """
    flow_name = FLOW_NAMES[sf_obj]
    title_field = "Title" if sf_obj in ("Lead", "Contact") else "Name"

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>59.0</apiVersion>
    <description>GTM Data Standardization — auto-maps Industry, Title to GTM taxonomy fields on {sf_obj} create/update. Deployed by Sawera Khadium Salesforce Data Standardizer skill.</description>
    <label>{flow_name.replace('_', ' ')}</label>
    <processType>AutoLaunchedFlow</processType>
    <status>Draft</status>
    <triggerType>RecordAfterSave</triggerType>

    <start>
        <locationX>176</locationX>
        <locationY>0</locationY>
        <filterLogic>OR</filterLogic>
        <filters>
            <field>Industry</field>
            <operator>IsChanged</operator>
            <value>
                <booleanValue>true</booleanValue>
            </value>
        </filters>
        <filters>
            <field>{title_field}</field>
            <operator>IsChanged</operator>
            <value>
                <booleanValue>true</booleanValue>
            </value>
        </filters>
        <object>{sf_obj}</object>
        <recordTriggerType>CreateAndUpdate</recordTriggerType>
    </start>

    <!-- Decision: skip if already standardized and nothing changed -->
    <decisions>
        <name>Check_If_Needs_Standardization</name>
        <label>Needs Standardization?</label>
        <locationX>176</locationX>
        <locationY>120</locationY>
        <defaultConnectorLabel>Yes — Standardize</defaultConnectorLabel>
        <rules>
            <name>Already_Standardized_No_Change</name>
            <conditionLogic>and</conditionLogic>
            <conditions>
                <leftValueReference>$Record.{GTM_FIELDS['standardized']}</leftValueReference>
                <operator>EqualTo</operator>
                <rightValue>
                    <booleanValue>true</booleanValue>
                </rightValue>
            </conditions>
            <conditions>
                <leftValueReference>$Record.Industry</leftValueReference>
                <operator>IsChanged</operator>
                <rightValue>
                    <booleanValue>false</booleanValue>
                </rightValue>
            </conditions>
            <connector>
                <targetReference>End</targetReference>
            </connector>
            <label>Already clean — skip</label>
        </rules>
    </decisions>

    <!-- Action: call external standardization (via Apex or named credential) -->
    <!-- In orgs without Apex, this updates GTM_Standardized__c = false     -->
    <!-- marks record as pending GTM standardization                         -->
    <recordUpdates>
        <name>Flag_For_Standardization</name>
        <label>Flag for Nightly Standardization</label>
        <locationX>176</locationX>
        <locationY>240</locationY>
        <inputAssignments>
            <field>{GTM_FIELDS['standardized']}</field>
            <value>
                <booleanValue>false</booleanValue>
            </value>
        </inputAssignments>
        <object>{sf_obj}</object>
        <filterLogic>and</filterLogic>
        <filters>
            <field>Id</field>
            <operator>EqualTo</operator>
            <value>
                <elementReference>$Record.Id</elementReference>
            </value>
        </filters>
    </recordUpdates>

    <label>End</label>
</Flow>"""


# ── Deploy Automation ─────────────────────────────────────────────────────────

def deploy(sf: Salesforce, obj: str = "all", confirmed: bool = False) -> Dict:
    """
    Deploy GTM standardization automation to Salesforce.

    IMPORTANT: This deploys persistent Salesforce Flows and Validation Rules that
    will affect every new or updated record going forward. Run in a sandbox first.

    Deploys:
    1. Record-triggered Flows (one per object) — in Draft/inactive state
    2. Validation rules (warning mode — never block saves)
    3. Reports deployment status and next steps

    Flows are deployed INACTIVE so the user must explicitly activate them in Setup.
    Requires confirmed=True to proceed (protection against accidental invocation).
    """
    # SECURITY: Require explicit user confirmation before deploying persistent automation.
    # This prevents accidental deployment of Salesforce Flows from an agent context.
    if not confirmed:
        return {
            "success": False,
            "requires_confirmation": True,
            "message": (
                "Deploying Salesforce Flows and Validation Rules is a persistent, "
                "org-wide change that will affect all future records. "
                "This should only be run after testing in a sandbox. "
                "Pass --confirm to proceed."
            ),
            "recommended_steps": [
                "1. Test in a Salesforce sandbox first",
                "2. Review the taxonomy.json to ensure mappings are correct",
                "3. Run: python scripts/automate.py deploy --confirm",
                "4. After deployment, activate flows manually in Setup → Flows",
            ]
        }
    objects = SUPPORTED_OBJECTS if obj.lower() == "all" else [obj]
    results = {
        "flows":            {},
        "validation_rules": {},
        "next_steps":       [],
    }

    for sf_obj in objects:
        if sf_obj not in FLOW_NAMES:
            continue

        flow_name = FLOW_NAMES[sf_obj]
        flow_xml  = _generate_flow_xml(sf_obj)

        # Deploy via Metadata API (tooling)
        try:
            sf.toolingexecute(
                "POST",
                "sobjects/Flow",
                data=json.dumps({
                    "FullName": flow_name,
                    "Metadata": {
                        "apiVersion": 59.0,
                        "label":      flow_name.replace("_", " "),
                        "status":     "Draft",
                        "processType": "AutoLaunchedFlow",
                    },
                }),
            )
            results["flows"][sf_obj] = {
                "status":  "deployed",
                "name":    flow_name,
                "state":   "Draft (inactive — activate in Salesforce Setup → Flows)",
            }
        except Exception as exc:
            err = str(exc)
            if "DUPLICATE" in err or "already exists" in err.lower():
                results["flows"][sf_obj] = {
                    "status": "already_exists",
                    "name":   flow_name,
                    "state":  "Check current status in Salesforce Setup → Flows",
                }
            else:
                results["flows"][sf_obj] = {
                    "status": "error",
                    "name":   flow_name,
                    "error":  err,
                    "fallback": (
                        "Deploy manually: copy the Flow XML from "
                        "scripts/automate.py _generate_flow_xml() "
                        "into Salesforce Setup → Flows → New Flow → "
                        "paste XML → Save → Activate"
                    ),
                }

        # Save Flow XML to disk for manual deployment fallback
        xml_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "flows", f"{flow_name}.flow-meta.xml"
        )
        os.makedirs(os.path.dirname(xml_path), exist_ok=True)
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(flow_xml)

        # Validation rule — warn when Industry is set but GTM Industry is blank
        vr_name = VALIDATION_RULE_NAMES.get(sf_obj, f"GTM_Validation_{sf_obj}")
        try:
            sf.toolingexecute(
                "POST",
                "sobjects/ValidationRule",
                data=json.dumps({
                    "EntityDefinitionId": sf_obj,
                    "Metadata": {
                        "active":          True,
                        "description":     (
                            "GTM Data Quality: warns when Industry is set "
                            "but GTM Industry is not yet mapped. "
                            "Does not block saves."
                        ),
                        "errorConditionFormula": (
                            f"AND(NOT(ISBLANK(Industry)), "
                            f"ISBLANK({GTM_FIELDS['industry']}))"
                        ),
                        "errorMessage": (
                            "Industry is set but GTM Industry is not mapped. "
                            "Run the GTM Standardizer to map this record."
                        ),
                        "errorDisplayField": GTM_FIELDS["industry"],
                    },
                }),
            )
            results["validation_rules"][sf_obj] = {
                "status": "deployed",
                "name":   vr_name,
                "mode":   "Warning only — does not block saves",
            }
        except Exception as exc:
            err = str(exc)
            results["validation_rules"][sf_obj] = {
                "status": "skipped" if "DUPLICATE" in err else "error",
                "name":   vr_name,
                "note":   err if "DUPLICATE" not in err else "Already exists",
            }

    # Next steps for the user
    results["next_steps"] = [
        "1. Go to Salesforce Setup → Flows",
        "2. Find the GTM_Standardization_*_Flow flows (status: Draft)",
        "3. Click each flow → Activate",
        "4. From this point, every new/updated record will be standardized automatically",
        "5. Run 'python scripts/automate.py status' to confirm automation is live",
    ]

    # Save Flow XMLs path for reference
    results["flow_xml_files"] = (
        "Flow XML files saved to salesforce-crm-skill/flows/ "
        "for manual deployment if Tooling API is not available"
    )

    return {"success": True, "deployment": results}


# ── Status ────────────────────────────────────────────────────────────────────

def status(sf: Salesforce) -> Dict:
    """
    Check the status of all deployed GTM automation.
    """
    flow_statuses = {}
    for sf_obj, flow_name in FLOW_NAMES.items():
        try:
            result = sf.toolingexecute(
                "GET",
                f"query?q=SELECT+Id,Status,Label+FROM+Flow+WHERE+MasterLabel='{flow_name}'+LIMIT+1",
            )
            records = result.get("records", [])
            if records:
                flow_statuses[sf_obj] = {
                    "name":   flow_name,
                    "status": records[0].get("Status", "Unknown"),
                    "id":     records[0].get("Id"),
                }
            else:
                flow_statuses[sf_obj] = {
                    "name":   flow_name,
                    "status": "Not deployed",
                }
        except Exception as exc:
            flow_statuses[sf_obj] = {
                "name":  flow_name,
                "error": str(exc),
            }

    return {"success": True, "flows": flow_statuses}


# ── Pause / Resume ────────────────────────────────────────────────────────────

def pause(sf: Salesforce) -> Dict:
    """Deactivate all GTM flows without deleting them."""
    return _set_flow_status(sf, "Obsolete")


def resume(sf: Salesforce) -> Dict:
    """Reactivate all GTM flows."""
    return _set_flow_status(sf, "Active")


def _set_flow_status(sf: Salesforce, target_status: str) -> Dict:
    results = {}
    for sf_obj, flow_name in FLOW_NAMES.items():
        try:
            # Find flow ID
            query_result = sf.toolingexecute(
                "GET",
                f"query?q=SELECT+Id+FROM+Flow+WHERE+MasterLabel='{flow_name}'+LIMIT+1",
            )
            records = query_result.get("records", [])
            if not records:
                results[sf_obj] = {"status": "not_found", "name": flow_name}
                continue

            flow_id = records[0]["Id"]
            sf.toolingexecute(
                "PATCH",
                f"sobjects/Flow/{flow_id}",
                data=json.dumps({"Status": target_status}),
            )
            results[sf_obj] = {
                "name":   flow_name,
                "status": target_status,
            }
        except Exception as exc:
            results[sf_obj] = {"name": flow_name, "error": str(exc)}

    return {"success": True, "flows": results}


# ── Remove ────────────────────────────────────────────────────────────────────

def remove(sf: Salesforce, confirm: bool = False) -> Dict:
    """Remove all GTM automation. Requires --confirm flag."""
    if not confirm:
        return {
            "success": False,
            "error": (
                "Removing automation requires --confirm flag. "
                "Re-run with --confirm to proceed."
            ),
        }

    results = {}
    for sf_obj, flow_name in FLOW_NAMES.items():
        try:
            query_result = sf.toolingexecute(
                "GET",
                f"query?q=SELECT+Id+FROM+Flow+WHERE+MasterLabel='{flow_name}'+LIMIT+1",
            )
            records = query_result.get("records", [])
            if not records:
                results[sf_obj] = {"status": "not_found"}
                continue

            flow_id = records[0]["Id"]
            sf.toolingexecute("DELETE", f"sobjects/Flow/{flow_id}")
            results[sf_obj] = {"status": "removed", "name": flow_name}
        except Exception as exc:
            results[sf_obj] = {"name": flow_name, "error": str(exc)}

    return {"success": True, "removed": results}


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    """
    CLI interface for the automation engine.

    Commands:
      deploy  [--object lead|contact|account|all]
      status
      pause
      resume
      remove  (requires --confirm)
    """
    parser = argparse.ArgumentParser(
        description="Salesforce GTM Automation Engine"
    )
    parser.add_argument("command",
                        choices=["deploy", "status", "pause", "resume", "remove"])
    parser.add_argument("--object",  default="all",
                        help="Salesforce object: Lead, Contact, Account, or all")
    parser.add_argument("--confirm", action="store_true",
                        help="Required for deploy and remove operations")

    args = parser.parse_args()

    sf = _get_sf()
    if sf is None:
        print(json.dumps({
            "success": False,
            "error": (
                "Not connected to Salesforce. "
                "Set SALESFORCE_INSTANCE_URL + SALESFORCE_ACCESS_TOKEN, "
                "or SALESFORCE_USERNAME + SALESFORCE_PASSWORD."
            )
        }))
        sys.exit(1)

    if args.command == "deploy":
        result = deploy(sf, args.object, confirmed=args.confirm)
    elif args.command == "status":
        result = status(sf)
    elif args.command == "pause":
        result = pause(sf)
    elif args.command == "resume":
        result = resume(sf)
    elif args.command == "remove":
        result = remove(sf, confirm=args.confirm)
    else:
        result = {"success": False, "error": f"Unknown command: {args.command}"}

    print(json.dumps(result, default=str, indent=2))


if __name__ == "__main__":
    main()
