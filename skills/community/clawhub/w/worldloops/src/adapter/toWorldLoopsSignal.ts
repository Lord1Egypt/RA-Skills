import type { Signal, SignalSource } from '../types';
import type { AdapterSignal } from '../types/adapterSignal';

const KNOWN_SOURCES: SignalSource[] = ['slack', 'gmail', 'calendar', 'github', 'manual'];

export function toWorldLoopsSignal(adapter: AdapterSignal): Signal {
  const source: SignalSource = (KNOWN_SOURCES as string[]).includes(adapter.source)
    ? (adapter.source as SignalSource)
    : 'manual';

  const signal: Signal = {
    source,
    text: adapter.text,
  };

  if (adapter.observedAt) signal.createdAt = adapter.observedAt;
  if (adapter.url) signal.url = adapter.url;

  return signal;
}
