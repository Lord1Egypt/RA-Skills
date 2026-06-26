# CIS Benchmark Summary (Simplified)

This skill implements a **lightweight subset** of CIS Level 1 benchmarks, focused on the highest-impact checks for small teams.

## Source

- Full CIS Benchmark: https://www.cisecurity.org/cis-benchmarks/
- Our subset: ~20 checks covering:
  - SSH security (Level 1, Section 5.2)
  - Firewall configuration (Level 1, Sections 6.1-6.2)
  - Password policies (Level 1, Section 9.1)
  - System logging (Level 1, Section 10.1)
  - File permissions (Level 1, Section 11.1)

## Why Subset?

Full CIS benchmarks have 200+ checks and require manual review. Our goal:
- **Fast** (<10 seconds per node)
- **Automated fixes** (provide CLI commands)
- **High signal-to-noise** (only critical items)

## Compliance Note

This tool helps you *approximate* compliance. For official audits, use the full CIS-CAT tool or engage a qualified assessor.

## Mapping

| Check ID | CIS v1.2.0 Equivalent |
|----------|----------------------|
| ssh_password_auth | 5.2.2 |
| ssh_root_login | 5.2.3 |
| ssh_protocol | 5.2.1 |
| ufw_enabled / firewalld_enabled | 6.1.1, 6.2.1 |
| security_updates | 9.1.2 (package management) |
| password_aging | 9.1.1 |
| auditd_running | 10.1.1 |
| rsylsog_running | 10.2.1 |
| permissions_passwd | 11.1.1 |
| permissions_shadow | 11.1.2 |

---

*Security Audit Assistant is not affiliated with CIS. This guide is for educational purposes.*
