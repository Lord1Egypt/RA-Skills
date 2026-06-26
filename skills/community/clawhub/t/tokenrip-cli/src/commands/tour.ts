import { CliError } from '../errors.js';
import { loadTourState, saveTourState, clearTourState, type TourState } from '../tour/state.js';
import { STEPS, TOTAL_STEPS, renderCurrentStep } from '../tour/steps.js';
import { AGENT_SCRIPT } from '../tour/agent-script.js';

export async function tour(options: { agent?: boolean }): Promise<void> {
  if (options.agent) {
    process.stdout.write(AGENT_SCRIPT);
    process.stdout.write('\n');
    return;
  }

  let state = loadTourState();
  if (!state) {
    state = {
      step: 1,
      assetId: null,
      threadId: null,
      startedAt: new Date().toISOString(),
    };
    saveTourState(state);
    process.stdout.write(`Welcome to Tokenrip. Let's take the tour — ${TOTAL_STEPS} steps, about 2 minutes.\n\n`);
  }

  process.stdout.write(renderCurrentStep(state));
  process.stdout.write('\n');
}

export async function tourNext(id: string | undefined): Promise<void> {
  const state = loadTourState();
  if (!state) {
    throw new CliError('NO_TOUR', 'No tour in progress. Run `rip tour` to start.');
  }

  const currentStep = STEPS[state.step - 1];
  if (!currentStep) {
    throw new CliError('INVALID_STATE', `Unexpected step number: ${state.step}`);
  }

  if (currentStep.expectsIdOnNext && !id) {
    const label = currentStep.collectsAs === 'assetId' ? 'asset id' : 'thread id';
    throw new CliError(
      'MISSING_ID',
      `This step needs the ${label} from the previous command. Run: rip tour next <${label.replace(' ', '-')}>`,
    );
  }

  if (currentStep.collectsAs && id) {
    state[currentStep.collectsAs] = id;
  }

  if (state.step >= TOTAL_STEPS) {
    clearTourState();
    process.stdout.write("You've reached the end of the tour. Run `rip tour` again any time.\n");
    return;
  }

  state.step += 1;
  saveTourState(state);

  process.stdout.write(renderCurrentStep(state));
  process.stdout.write('\n');
}

export async function tourRestart(): Promise<void> {
  clearTourState();
  await tour({});
}
