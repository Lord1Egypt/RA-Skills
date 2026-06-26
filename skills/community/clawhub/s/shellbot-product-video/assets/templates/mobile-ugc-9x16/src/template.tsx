import {AbsoluteFill, Sequence, interpolate, spring, useCurrentFrame, useVideoConfig} from "remotion";

const CaptionCard = ({tag, text}: {tag: string; text: string}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const intro = spring({frame, fps, config: {damping: 140, stiffness: 130}});
  const scale = interpolate(intro, [0, 1], [0.88, 1], {extrapolateRight: "clamp"});

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        padding: 64,
        fontFamily: "Inter, ui-sans-serif, system-ui",
        color: "white",
      }}
    >
      <div
        style={{
          alignSelf: "flex-start",
          fontSize: 24,
          padding: "10px 18px",
          borderRadius: 999,
          background: "rgba(15,23,42,0.6)",
          marginBottom: 20,
          letterSpacing: 1.4,
        }}
      >
        {tag}
      </div>
      <div
        style={{
          transform: `scale(${scale})`,
          transformOrigin: "left bottom",
          background: "rgba(2,6,23,0.62)",
          border: "1px solid rgba(148,163,184,0.45)",
          borderRadius: 28,
          padding: "28px 26px",
          fontSize: 64,
          fontWeight: 700,
          lineHeight: 1.05,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

const Bg = ({hue}: {hue: number}) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(circle at 10% 10%, hsla(${hue},95%,60%,0.55), #020617 52%)`,
    }}
  />
);

export const MobileUgcVideo = () => {
  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={180}>
        <Bg hue={0} />
        <CaptionCard tag="PROBLEM" text="Still doing this the hard way?" />
      </Sequence>
      <Sequence from={180} durationInFrames={180}>
        <Bg hue={174} />
        <CaptionCard tag="SOLUTION" text="This app fixes it in one flow." />
      </Sequence>
      <Sequence from={360} durationInFrames={270}>
        <Bg hue={226} />
        <CaptionCard tag="USE CASES" text="Plan launches. Track issues. Share wins." />
      </Sequence>
      <Sequence from={630} durationInFrames={270}>
        <Bg hue={140} />
        <CaptionCard tag="CTA" text="Try it today. 14 extra trial days." />
      </Sequence>
    </AbsoluteFill>
  );
};
