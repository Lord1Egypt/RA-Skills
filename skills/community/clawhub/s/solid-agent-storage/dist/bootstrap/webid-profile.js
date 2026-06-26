/**
 * Generate a SPARQL UPDATE to patch agent metadata into a WebID profile.
 * CSS auto-generates a basic profile; we add agent-specific triples.
 */
export function buildProfilePatch(config, webId) {
    const prefixes = [
        'PREFIX foaf: <http://xmlns.com/foaf/0.1/>',
        'PREFIX solid: <http://www.w3.org/ns/solid/terms#>',
        'PREFIX schema: <http://schema.org/>',
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>',
        'PREFIX interition: <https://vocab.interition.org/agents#>',
    ].join('\n');
    const me = `<${webId}>`;
    const inserts = [
        `${me} a interition:Agent .`,
        `${me} a foaf:Agent .`,
        `${me} foaf:name "${escapeString(config.displayName)}" .`,
        `${me} rdfs:label "${escapeString(config.displayName)}" .`,
        `${me} schema:name "${escapeString(config.displayName)}" .`,
        `${me} interition:agentName "${escapeString(config.name)}" .`,
    ];
    if (config.capabilities?.length) {
        for (const cap of config.capabilities) {
            inserts.push(`${me} interition:capability "${escapeString(cap)}" .`);
        }
    }
    return `${prefixes}

INSERT DATA {
  ${inserts.join('\n  ')}
}`;
}
function escapeString(s) {
    return s.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
}
//# sourceMappingURL=webid-profile.js.map