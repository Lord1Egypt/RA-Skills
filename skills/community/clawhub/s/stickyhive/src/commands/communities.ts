import { apiRequest, output } from '../api';

export async function listCommunities() {
  output(await apiRequest('GET', '/communities/'));
}

export async function getCommunity(argv: { id: number }) {
  output(await apiRequest('GET', `/communities/${argv.id}/`));
}
