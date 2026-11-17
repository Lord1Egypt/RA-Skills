# Dependencies and build permissions

Use when adopting/upgrading a dependency or changing how code is built and published.

For a new package, verify its exact registry identity and upstream repository before installation; an agent-suggested name is not evidence that a package exists. Check the intended version's license, relevant advisories and maintenance. Popularity or recent release dates alone do not establish trust.

Use the project's package manager and lockfile. Review the resulting dependency changes, including unexpected transitive updates and install scripts. Run the tests that exercise the changed dependency and any required audit. A routine compatible update does not automatically need a design document; a replacement that changes data formats, runtime behavior or trust does need those effects checked.

For CI and release changes:

- Keep job permissions narrow. Do not expose write credentials or secrets to untrusted pull-request code.
- Pass untrusted event values as data, not interpolated shell code.
- Use the project's artifact integrity/provenance controls. Pin third-party workflow code to reviewed immutable revisions when that is the repository's policy; do not weaken an existing pin.
- Prefer short-lived workload identity where supported. Confirm the intended account, project and permissions before using a deployment credential.
- Review audit findings by affected version, reachability and exposure. Do not silently suppress a finding or claim an audit ran when it did not.

Preserve required license notices. Use an SBOM, signing or formal attestation when the distribution or project requires it.

## Sources

- [OpenSSF Scorecard checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md)
- [GitHub Actions security](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- [OSV vulnerability database](https://osv.dev/)
