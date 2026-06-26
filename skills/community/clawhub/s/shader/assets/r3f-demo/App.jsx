import { useMemo, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";

function RipplePlane() {
  const materialRef = useRef(null);

  const uniforms = useMemo(
    () => ({
      uTime: { value: 0 },
    }),
    [],
  );

  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uniforms.uTime.value = state.clock.getElapsedTime();
    }
  });

  return (
    <mesh>
      <planeGeometry args={[2.8, 2.8, 128, 128]} />
      <shaderMaterial
        ref={materialRef}
        uniforms={uniforms}
        vertexShader={`
          varying vec2 vUv;
          uniform float uTime;

          void main() {
            vUv = uv;
            vec3 transformed = position;
            transformed.z += sin(position.x * 5.0 + uTime * 2.0) * 0.08;
            transformed.z += sin(position.y * 4.0 + uTime * 1.7) * 0.06;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(transformed, 1.0);
          }
        `}
        fragmentShader={`
          precision mediump float;

          varying vec2 vUv;
          uniform float uTime;

          void main() {
            vec2 uv = vUv * 2.0 - 1.0;
            float dist = length(uv);
            float pulse = 0.5 + 0.5 * sin(uTime * 2.5 - dist * 10.0);

            vec3 deep = vec3(0.05, 0.09, 0.22);
            vec3 glow = vec3(0.20, 0.82, 1.00);
            vec3 color = mix(deep, glow, pulse);
            color *= smoothstep(1.2, 0.15, dist);

            gl_FragColor = vec4(color, 1.0);
          }
        `}
      />
    </mesh>
  );
}

export default function App() {
  return (
    <Canvas camera={{ position: [0, 0, 2.5], fov: 45 }}>
      <color attach="background" args={["#07111f"]} />
      <RipplePlane />
    </Canvas>
  );
}
