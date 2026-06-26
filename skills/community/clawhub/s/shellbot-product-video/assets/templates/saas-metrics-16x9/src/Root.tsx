import {Composition} from "remotion";
import {SaasMetricsVideo} from "./template";

export const RemotionRoot = () => {
  return (
    <Composition
      id="SaasMetrics16x9"
      component={SaasMetricsVideo}
      width={1920}
      height={1080}
      fps={30}
      durationInFrames={960}
    />
  );
};
