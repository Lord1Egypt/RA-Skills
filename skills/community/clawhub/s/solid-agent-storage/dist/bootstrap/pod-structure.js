/**
 * Creates the standard container structure inside an agent's pod.
 * Containers in Solid are created by PUT-ing with the right content type.
 */
export async function createPodContainers(podUrl, authFetch) {
    const containers = ['memory/', 'shared/', 'conversations/'];
    for (const container of containers) {
        const url = new URL(container, podUrl).href;
        const res = await authFetch(url, {
            method: 'PUT',
            headers: {
                'content-type': 'text/turtle',
                'if-none-match': '*',
                link: '<http://www.w3.org/ns/ldp#BasicContainer>; rel="type"',
            },
            body: '',
        });
        // 201 Created or 409 Conflict (already exists) are both fine
        if (!res.ok && res.status !== 409) {
            throw new Error(`Failed to create container ${container}: ${res.status} ${await res.text()}`);
        }
    }
}
//# sourceMappingURL=pod-structure.js.map