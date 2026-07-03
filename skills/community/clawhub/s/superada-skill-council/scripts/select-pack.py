#!/usr/bin/env python3
import json, sys

text = ' '.join(sys.argv[1:]).lower()

def has(*terms):
    return any(t in text for t in terms)

if has('sales','pricing','pipeline','deal','outbound','prospect','revops','buyer','enterprise'):
    domain='sales'
elif has('support','ticket','sla','escalation','customer support','helpdesk','incident response'):
    domain='support'
elif has('product','prd','roadmap','feature','ux','requirement','requirements','prioritization'):
    domain='product'
elif has('growth','marketing','positioning','campaign','funnel','content','acquisition'):
    domain='growth'
elif has('ops','operations','hiring','workflow','cadence','team structure','operating model'):
    domain='ops'
elif has('engineering','api','architecture','infra','code','backend','frontend','security','database','scaling','system'):
    domain='engineering'
else:
    domain='mixed'

packs = {
  'engineering': ['Systems Architect','Pragmatic Engineer','Reliability Engineer','Security Engineer','Product Engineer'],
  'sales': ['Enterprise AE','Sales Engineer','RevOps Lead','Buyer / CFO Lens','Customer Success Partner'],
  'support': ['Support Lead','Frontline Agent','Customer Success Manager','Knowledge / QA Owner','Escalation / Incident Manager'],
  'product': ['Product Strategist','UX Lead','Delivery Lead','Customer Voice','Metrics / Experimentation Lead'],
  'growth': ['Positioning Strategist','Performance Marketer','Content Operator','Sales Alignment Lead','Skeptical Buyer'],
  'ops': ['Operator','Finance / Efficiency Lens','People / Manager Lens','Risk / Compliance Lens','Execution Coach'],
  'mixed': ['Strategist','Operator','Customer Lens','Domain Expert','Risk Lens']
}
print(json.dumps({'domain': domain, 'personas': packs[domain]}, indent=2))
