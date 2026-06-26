import {
  AbsoluteFill,
  Easing,
  Sequence,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const Scene = ({
  tone,
  title,
  subtitle,
}: {
  tone: "problem" | "solution" | "use-case" | "cta";
  title: string;
  subtitle: string;
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const enter = spring({frame, fps, config: {damping: 120, stiffness: 120}});
  const y = interpolate(enter, [0, 1], [80, 0], {extrapolateRight: "clamp"});
  const glow = interpolate(frame, [0, 150], [0.2, 0.7], {
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  });

  const bg =
    tone === "problem"
      ? "radial-gradient(circle at 80% 10%, rgba(239,68,68,0.35), #0f172a 45%)"
      : tone === "solution"
        ? "radial-gradient(circle at 20% 20%, rgba(45,212,191,0.35), #0b1120 50%)"
        : tone === "use-case"
          ? "radial-gradient(circle at 70% 30%, rgba(59,130,246,0.35), #0a1022 45%)"
          : "radial-gradient(circle at 50% 20%, rgba(34,197,94,0.35), #051b11 50%)";

  return (
    <AbsoluteFill
      style={{
        background: bg,
        color: "#f8fafc",
        fontFamily: "Inter, ui-sans-serif, system-ui",
        justifyContent: "center",
        padding: 100,
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 40,
          borderRadius: 32,
          border: `1px solid rgba(255,255,255,${glow})`,
          boxShadow: `0 0 140px rgba(255,255,255,${glow * 0.25})`,
        }}
      />
      <div style={{transform: `translateY(${y}px)`, zIndex: 2}}>
        <div style={{fontSize: 24, letterSpacing: 3, opacity: 0.8, marginBottom: 22}}>{tone.toUpperCase()}</div>
        <h1 style={{fontSize: 96, lineHeight: 1.02, margin: 0, maxWidth: 1400}}>{title}</h1>
        <p style={{fontSize: 42, lineHeight: 1.2, opacity: 0.92, marginTop: 24, maxWidth: 1300}}>{subtitle}</p>
      </div>
    </AbsoluteFill>
  );
};

export const CinematicProductVideo = () => {
  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={180}>
        <Scene tone="problem" title="Busy teams lose momentum in tool chaos" subtitle="Pain first: fragmented workflows create slow responses and missed opportunities." />
      </Sequence>
      <Sequence from={180} durationInFrames={180}>
        <Scene tone="solution" title="One command center restores control" subtitle="Introduce the solution with simple visual clarity and confident pacing." />
      </Sequence>
      <Sequence from={360} durationInFrames={270}>
        <Scene tone="use-case" title="Show outcomes in real contexts" subtitle="Use-case proof: onboarding faster, support queues calmer, reporting clearer." />
      </Sequence>
      <Sequence from={630} durationInFrames={270}>
        <Scene tone="cta" title="Start now, get 20% off for 3 months" subtitle="Single CTA, concrete incentive, readable final hold." />
      </Sequence>
    </AbsoluteFill>
  );
};
