import { apiRequest, output } from '../api';

interface CreatePostArgs {
  title: string;
  content: string;
  spaceId: number;
  date?: string;
  pin?: boolean;
  comment?: string;
  poll?: string;
}

export async function createPost(argv: CreatePostArgs) {
  const body: Record<string, unknown> = {
    title: argv.title,
    content: argv.content,
    space_id: argv.spaceId,
  };
  if (argv.date) body.scheduled_time = argv.date;
  if (argv.pin) body.pin_on_publish = true;
  if (argv.comment) body.first_comment_text = argv.comment;
  if (argv.poll) {
    try { body.poll_options = JSON.parse(argv.poll); } catch { body.poll_options = argv.poll.split(','); }
  }
  output(await apiRequest('POST', '/scheduled-posts/', body));
}

interface ListPostsArgs {
  status?: string;
  draft?: boolean;
  spaceId?: number;
  dateFrom?: string;
  dateTo?: string;
}

export async function listPosts(argv: ListPostsArgs) {
  const query: Record<string, string> = {};
  if (argv.status) query.status = argv.status;
  if (argv.draft !== undefined) query.is_draft = String(argv.draft);
  if (argv.spaceId) query.space_id = String(argv.spaceId);
  if (argv.dateFrom) query.date_from = argv.dateFrom;
  if (argv.dateTo) query.date_to = argv.dateTo;
  output(await apiRequest('GET', '/scheduled-posts/', undefined, query));
}

export async function getPost(argv: { id: number }) {
  output(await apiRequest('GET', `/scheduled-posts/${argv.id}/`));
}

export async function updatePost(argv: { id: number; data: string }) {
  const body = JSON.parse(argv.data);
  output(await apiRequest('PATCH', `/scheduled-posts/${argv.id}/`, body));
}

export async function deletePost(argv: { id: number }) {
  output(await apiRequest('DELETE', `/scheduled-posts/${argv.id}/`));
}

export async function reschedulePost(argv: { id: number; date: string }) {
  output(await apiRequest('POST', `/scheduled-posts/${argv.id}/reschedule/`, { scheduled_time: argv.date }));
}

export async function publishNow(argv: { id: number }) {
  output(await apiRequest('POST', `/scheduled-posts/${argv.id}/publish-now/`));
}

interface BulkScheduleArgs {
  ids: string;
  startTime: string;
  interval?: number;
}

export async function bulkSchedule(argv: BulkScheduleArgs) {
  const postIds = argv.ids.split(',').map(Number);
  output(await apiRequest('POST', '/scheduled-posts/bulk-schedule/', {
    post_ids: postIds,
    start_time: argv.startTime,
    interval_hours: argv.interval ?? 1,
  }));
}
