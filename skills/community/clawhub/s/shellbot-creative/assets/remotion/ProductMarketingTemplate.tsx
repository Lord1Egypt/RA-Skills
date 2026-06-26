import React from 'react';
import {AbsoluteFill, Audio, Sequence, Video, Img, spring, useCurrentFrame, useVideoConfig} from 'remotion';

type SequenceItem = {
  id: number;
  name: string;
  from: number;
  durationInFrames: number;
  onScreenText?: string;
  asset?: {
    src?: string;
    fallbackImage?: string;
  };
};

type Props = {
  title?: string;
  sequences: SequenceItem[];
  audio?: {
    voiceover?: string;
    music?: string;
    voiceVolume?: number;
    musicVolume?: number;
  };
};

export const ProductMarketingTemplate: React.FC<Props> = ({title, sequences, audio}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <AbsoluteFill style={{backgroundColor: '#09090b', color: 'white', fontFamily: 'Inter, system-ui, sans-serif'}}>
      {sequences.map((scene) => (
        <Sequence key={scene.id} from={scene.from} durationInFrames={scene.durationInFrames}>
          <AbsoluteFill>
            {scene.asset?.src ? (
              <Video src={scene.asset.src} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
            ) : scene.asset?.fallbackImage ? (
              <Img src={scene.asset.fallbackImage} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
            ) : null}
            <AbsoluteFill
              style={{
                justifyContent: 'flex-end',
                padding: 64,
                background: 'linear-gradient(180deg, transparent 30%, rgba(0,0,0,0.75) 100%)',
              }}
            >
              <div
                style={{
                  fontSize: 56,
                  fontWeight: 700,
                  lineHeight: 1.1,
                  transform: `translateY(${(1 - spring({fps, frame, durationInFrames: 18})) * 20}px)`,
                  opacity: spring({fps, frame, durationInFrames: 18}),
                }}
              >
                {scene.onScreenText ?? title ?? 'Creative Video'}
              </div>
            </AbsoluteFill>
          </AbsoluteFill>
        </Sequence>
      ))}

      {audio?.voiceover ? <Audio src={audio.voiceover} volume={audio.voiceVolume ?? 1} /> : null}
      {audio?.music ? <Audio src={audio.music} volume={audio.musicVolume ?? 0.2} /> : null}
    </AbsoluteFill>
  );
};
