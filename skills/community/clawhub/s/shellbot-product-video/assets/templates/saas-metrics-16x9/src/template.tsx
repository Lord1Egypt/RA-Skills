import {AbsoluteFill, Sequence, interpolate, spring, useCurrentFrame, useVideoConfig} from "remotion";

const Bar = ({index, value, color}: {index: number; value: number; color: string}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const rise = spring({frame: frame - index * 4, fps, config: {damping: 200}});
  const height = interpolate(rise, [0, 1], [8, value], {extrapolateRight: "clamp"});

  return (
    <div
      style={{
        width: 120,
        height,
        borderRadius: 16,
        backgroundColor: color,
        boxShadow: "0 20px 40px rgba(0,0,0,0.25)",
      }}
    />
  );
};

const Dashboard = ({title, subtitle}: {title: string; subtitle: string}) => {
  return (
    <AbsoluteFill style={{padding: 86, color: "#e2e8f0", fontFamily: "Inter, ui-sans-serif, system-ui"}}>
      <div style={{fontSize: 22, letterSpacing: 2, opacity: 0.78}}>PRODUCT MARKETING</div>
      <h1 style={{fontSize: 82, marginTop: 18, marginBottom: 14, lineHeight: 1.05}}>{title}</h1>
      <p style={{fontSize: 36, marginTop: 0, opacity: 0.9}}>{subtitle}</p>
      <div
        style={{
          marginTop: 40,
          background: "rgba(15,23,42,0.55)",
          border: "1px solid rgba(148,163,184,0.3)",
          borderRadius: 28,
          padding: "42px 38px",
        }}
      >
        <div style={{display: "flex", gap: 20, alignItems: "flex-end", height: 280}}>
          <Bar index={0} value={120} color="#38bdf8" />
          <Bar index={1} value={168} color="#22d3ee" />
          <Bar index={2} value={210} color="#818cf8" />
          <Bar index={3} value={252} color="#34d399" />
          <Bar index={4} value={290} color="#a78bfa" />
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const SaasMetricsVideo = () => {
  return (
    <AbsoluteFill style={{background: "linear-gradient(150deg, #020617, #0b132b)"}}>
      <Sequence from={0} durationInFrames={180}>
        <Dashboard title="Before: teams guess, react, and scramble" subtitle="Establish the problem with chaos and uncertainty." />
      </Sequence>
      <Sequence from={180} durationInFrames={210}>
        <Dashboard title="After: one system routes the right work" subtitle="Introduce the solution through operational clarity." />
      </Sequence>
      <Sequence from={390} durationInFrames={300}>
        <Dashboard title="Use cases: onboarding, support, weekly reporting" subtitle="Show practical outcomes in recurring business workflows." />
      </Sequence>
      <Sequence from={690} durationInFrames={270}>
        <Dashboard title="Book a demo and get 30 bonus onboarding days" subtitle="One CTA with a specific incentive to act now." />
      </Sequence>
    </AbsoluteFill>
  );
};
