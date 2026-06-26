import { apiRequest, output } from '../api';

export async function listSequences(argv: { communityId: number }) {
  output(await apiRequest('GET', '/sequences/', undefined, { community_id: String(argv.communityId) }));
}

export async function getSequence(argv: { id: number; communityId: number }) {
  output(await apiRequest('GET', `/sequences/${argv.id}/`, undefined, { community_id: String(argv.communityId) }));
}

export async function createSequence(argv: { communityId: number; name: string; description?: string; steps?: string }) {
  const body: Record<string, unknown> = {
    community_id: argv.communityId,
    name: argv.name,
  };
  if (argv.description) body.description = argv.description;
  if (argv.steps) body.steps = JSON.parse(argv.steps);
  output(await apiRequest('POST', '/sequences/', body));
}

export async function updateSequence(argv: { id: number; communityId: number; data: string }) {
  const body = JSON.parse(argv.data);
  body.community_id = argv.communityId;
  output(await apiRequest('PATCH', `/sequences/${argv.id}/`, body));
}

export async function deleteSequence(argv: { id: number; communityId: number }) {
  output(await apiRequest('DELETE', `/sequences/${argv.id}/`, undefined, { community_id: String(argv.communityId) }));
}

export async function toggleSequence(argv: { id: number; communityId: number }) {
  output(await apiRequest('POST', `/sequences/${argv.id}/toggle/`, { community_id: argv.communityId }));
}

export async function enrollMember(argv: { id: number; communityId: number; memberId: string }) {
  output(await apiRequest('POST', `/sequences/${argv.id}/enroll/`, {
    community_id: argv.communityId,
    member_id: argv.memberId,
  }));
}

export async function listEnrollments(argv: { id: number; communityId: number; status?: string }) {
  const query: Record<string, string> = { community_id: String(argv.communityId) };
  if (argv.status) query.status = argv.status;
  output(await apiRequest('GET', `/sequences/${argv.id}/enrollments/`, undefined, query));
}

export async function manageEnrollment(argv: { sequenceId: number; enrollmentId: number; communityId: number; action: string }) {
  output(await apiRequest('POST', `/sequences/${argv.sequenceId}/enrollments/${argv.enrollmentId}/manage/`, {
    community_id: argv.communityId,
    action: argv.action,
  }));
}

export async function getStepTypes() {
  output(await apiRequest('GET', '/sequences/step-types/'));
}
