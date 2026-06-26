import { apiRequest, output } from '../api';

export async function listSpaces() {
  output(await apiRequest('GET', '/spaces/'));
}

export async function getSpace(argv: { id: number }) {
  output(await apiRequest('GET', `/spaces/${argv.id}/`));
}
