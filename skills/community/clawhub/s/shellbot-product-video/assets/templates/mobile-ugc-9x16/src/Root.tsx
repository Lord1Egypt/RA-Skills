import {Composition} from "remotion";
import {MobileUgcVideo} from "./template";

export const RemotionRoot = () => {
  return (
    <Composition
      id="MobileUgc9x16"
      component={MobileUgcVideo}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={900}
    />
  );
};
