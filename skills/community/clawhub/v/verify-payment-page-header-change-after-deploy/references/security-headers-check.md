# Security Headers Check reference

## Purpose

Security Headers Check reads one public URL's live HTTP response.

It reports the presence and displayed value of eight browser-protection headers:

- Content-Security-Policy
- Strict-Transport-Security
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy
- Cross-Origin-Opener-Policy
- Cross-Origin-Resource-Policy

It also returns a score weighted by how much each header matters.

The granularity is one fetched response from one public page.

The tool is read-only and makes one guarded request.

## Tool

Use `powmcp-security-headers-check:security_headers_check`.

The only input is `url`.

`url` is required and must be a full public URL including the protocol.

Make one call for the payment-page URL. Make another call only after a correction has been deployed and a rerun is required.

The request is capped at 15 seconds.

Measured runs against six live sites on 2026-08-19 took 0.04 to 1.1 seconds.

If an invalid-arguments error identifies `url`, tell the user: “The `url` field was invalid; I will correct the full public URL, including its protocol, and run the check again.”

An invalid-arguments error is not a missing-tool condition.

The packet supplies no other input, default, range, cap, or enumeration.

## Output to retain

Quote the submitted URL and returned `finalUrl`.

Quote the response status.

Quote the weighted score and count without re-deriving or rounding them.

Quote each returned status from `headers.status`.

Quote each displayed header value verbatim.

List missing headers in the order returned, which is weightiest first.

Inspect every returned value separately.

## Interpretation

A score of 100 means all eight headers were present on that fetched response.

It does not mean their policies are effective or that the site is secure.

A set status proves presence only for that header on that response.

A missing status proves that the header was not present on that response.

The result does not determine whether a difference from a baseline was authorized.

The result does not store a dated artifact, perform a baseline diff, schedule recurring monitoring, or route alerts.

A completed authorization conclusion therefore requires a dated capture, an approved baseline, a diff, and an authorization or review record.

## Coverage limits

The result does not inspect TLS or certificates.

It does not inspect loaded JavaScript or application vulnerabilities.

It does not inspect headers returned by other pages and resources.

It is not an overall security verdict.

Displayed header values are truncated to 160 characters.

A full-value comparison is structurally unassessable from a truncated displayed value alone because content beyond that limit is absent from the result.

A response from another page or resource is structurally unassessable because the tool fetches one URL and reports one response.

Authorization is structurally unassessable from the tool result because the tool does not read the approved baseline or authorization record.

## Failure handling

The packet defines no tool-specific failure codes.

When the tool is missing, tell the user: “Security Headers Check could not run in this session, so I cannot report its live score, count, statuses, or displayed values.”

Then offer connection and rerun, or the non-PowMCP path.

When an argument is invalid, name the failing field, correct it, and call again.

Do not turn a failed or absent observation into a clean result.

## Non-PowMCP path

Use curl with a full request that follows redirects and preserves the raw production header block.

Record the URL, date, timestamp, response status, and raw header block, then diff the capture against the stored approved baseline.

This path supplies full raw values for comparison but does not supply the PowMCP weighted score or its eight-header status report.

Send every difference for authorization review, route unauthorized-change alerts, and retain the capture, diff, record, and decision.

## Source of truth

- App page: https://powmcp.com/apps/security-headers-check/
- PCI DSS payment-page requirements: https://cside.com/blog/pci-dss-4-0-1-requirements-6-4-3-11-6-1-client-side-compliance-guide
- PCI DSS v4.0.1 implementation: https://www.sikich.com/insight/preparing-for-pci-dss-v4-0-1-requirements-6-4-3-and-11-6-1/
- Payment-page compliance workflow: https://jscrambler.com/blog/pci-dss-4-0-1/
