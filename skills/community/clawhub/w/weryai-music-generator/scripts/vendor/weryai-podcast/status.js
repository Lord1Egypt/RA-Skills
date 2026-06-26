import { createClient } from '../weryai-core/client.js';
import { formatApiError, formatNetworkError, isApiSuccess } from '../weryai-core/errors.js';
import {
  getPodcastFailureMessage,
  getPodcastLifecyclePhase,
  normalizePodcastTask,
} from './normalize.js';

export async function execute(input, ctx) {
  const taskId = input.taskId || input.task_id || input['task-id'];
  if (!taskId) {
    return {
      ok: false,
      phase: 'failed',
      errorCode: 'VALIDATION',
      errorMessage: 'The status script requires `--task-id <task-id>`.',
    };
  }

  const client = createClient(ctx);
  let response;
  try {
    response = await client.get(`/v1/generation/${taskId}/status`, { retries: 3 });
  } catch (err) {
    return formatNetworkError(err);
  }

  if (!isApiSuccess(response)) {
    return formatApiError(response);
  }

  const task = normalizePodcastTask(response.data);
  const phase = getPodcastLifecyclePhase(task);

  return {
    ok: phase !== 'failed',
    phase,
    taskId: task.taskId,
    taskStatus: task.taskStatus,
    contentStatus: task.contentStatus,
    audios: task.audios,
    scripts: task.scripts,
    lyrics: task.lyrics,
    coverUrl: task.coverUrl,
    errorCode: phase === 'failed' ? 'TASK_FAILED' : null,
    errorMessage: phase === 'failed' ? getPodcastFailureMessage(task) : null,
  };
}

export default execute;
