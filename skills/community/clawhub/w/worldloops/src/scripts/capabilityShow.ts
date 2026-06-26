import { getCapabilityBoundary } from '../policy/capabilityBoundary';

function main(): void {
  console.log(
    JSON.stringify(
      {
        ok: true,
        source: 'worldloops.local',
        capabilityBoundary: getCapabilityBoundary(),
        safety: { externalWrite: false },
      },
      null,
      2
    )
  );
}

main();
