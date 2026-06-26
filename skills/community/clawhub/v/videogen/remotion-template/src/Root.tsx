import { Composition } from "remotion";
import { Video } from "./Video";

// 总帧数：300秒 × 30fps = 9000帧
const TOTAL_DURATION_FRAMES = 300 * 30; // 9000
const FPS = 30;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Video"
        component={Video}
        durationInFrames={TOTAL_DURATION_FRAMES}
        fps={FPS}
        width={1080}
        height={1920}
      />
    </>
  );
};
