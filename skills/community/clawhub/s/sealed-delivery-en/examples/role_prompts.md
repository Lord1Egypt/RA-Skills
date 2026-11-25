# Task brief and licensing templates

Three templates: deliverer brief, customer brief, licensing terms. Fill in the
blanks.

---

## Template A — Deliverer: delivery brief

```
Role: deliverer
Goal: deliver <model / algorithm> v<version> to <customer> without their data leaving the local machine

Deliverables
1. Sealed package (.mgc_file) and sha256
2. Dependency list (packages outside the standard library, with versions)
3. Input format (columns, types, required fields, one sample row)
4. Output format (field meanings, units, precision)
5. Version and change notes

Delivery form
- Trial: free mode, runnable on any MGC 1.5.4+ node
- Production: p2p mode, bound to the customer's node_pub

Quality requirements
- No hardcoded absolute paths
- No network access
- Output written explicitly; the script creates its parent directory
- Dry-run locally on sample data before sealing
```

---

## Template B — Customer: acceptance brief

```
Role: customer
Goal: complete one forecast locally and confirm the data never left the machine

Preconditions
- MGC Blackbox >= 1.6.0 is running locally
- Business data is ready (CSV: month, sales)

Steps
1. Verify the package source and sha256
2. Import the sealed package
3. Run the entry script on local data
4. Check output fields and precision
5. Confirm no outbound network traffic

Acceptance
- The output contains summary.next_forecast and points
- No raw data was uploaded during the run
- The scripts cannot be read or modified
```

---

## Template C — Licensing terms (key points)

```
Licensee: <customer> / first 16 chars of node_pub fingerprint
Scope: <model name> v<version>
Form: p2p node binding
Term: <start> to <end>

Terms
1. The sealed package runs only on the licensed node; no forwarding, copying, or resale
2. The customer must not decompile, bypass, or modify the logic inside the package
3. Upgrades are delivered as new packages; the old package is retired at the same time
4. Customer data belongs to the customer; the deliverer never touches raw data
5. The deliverer is not liable for business decisions made from model output

Support
- Channel: <email / ticket>
- Contact: <support@example.com>
```
