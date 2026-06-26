import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { AppleBg, SceneTag, TagGroup } from "../components/AppleShared";

export const 微压缩: React.FC = () => {
  const frame = useCurrentFrame();

  // 左侧节点
  const leftNodes = [
    { label: "连续对话", sub: "Cache 有效", y: 18, color: "#0A84FF" },
    { label: "Cached Micro Compact", sub: "精细清理", y: 48, color: "#0A84FF" },
  ];
  const rightNodes = [
    { label: "离开后回来", sub: "Cache 过期", y: 18, color: "#BF5AF2" },
    { label: "Time Based Micro Compact", sub: "直接替换", y: 48, color: "#BF5AF2" },
  ];

  return (
    <AppleBg>
      <SceneTag text="第一层 · 微压缩" startFrame={0} color="#0A84FF" />

      {/* 标题区 */}
      <div style={{
        position: "absolute",
        top: "8%",
        left: 0,
        right: 0,
        textAlign: "center",
      }}>
        <div style={{
          fontSize: 28,
          color: "#FFFFFF",
          fontWeight: 800,
          fontFamily: "Inter, -apple-system, sans-serif",
          letterSpacing: "-0.02em",
        }}>
          两条路径 · 处理 Prompt Cache
        </div>
        <div style={{
          fontSize: 15,
          color: "#8E8E93",
          fontFamily: "Inter, -apple-system, sans-serif",
          marginTop: 6,
        }}>
          Anthropic API Prompt Cache 机制决定如何清理
        </div>
      </div>

      {/* 左侧路径 */}
      <div style={{
        position: "absolute",
        top: "26%",
        left: "5%",
        right: "52%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 0,
      }}>
        {/* 节点1 */}
        <div style={{
          width: "100%",
          backgroundColor: "#0A84FF18",
          border: "2px solid #0A84FF55",
          borderRadius: 20,
          padding: "20px 16px",
          textAlign: "center",
        }}>
          <div style={{
            fontSize: 26,
            fontWeight: 800,
            color: "#0A84FF",
            fontFamily: "Inter, -apple-system, sans-serif",
          }}>
            连续对话
          </div>
          <div style={{
            fontSize: 14,
            color: "#0A84FF88",
            fontFamily: "Inter, -apple-system, sans-serif",
            marginTop: 4,
          }}>
            服务端 Cache 仍然有效
          </div>
        </div>

        {/* 箭头 */}
        <div style={{
          width: 3,
          height: 32,
          background: "linear-gradient(180deg, #0A84FF, #0A84FF88)",
          borderRadius: 2,
        }} />

        {/* 节点2 */}
        <div style={{
          width: "100%",
          backgroundColor: "#0A84FF22",
          border: "2px solid #0A84FF",
          borderRadius: 20,
          padding: "20px 16px",
          textAlign: "center",
          boxShadow: "0 0 30px #0A84FF22",
        }}>
          <div style={{
            fontSize: 22,
            fontWeight: 800,
            color: "#0A84FF",
            fontFamily: "Inter, -apple-system, sans-serif",
          }}>
            Cached Micro Compact
          </div>
          <div style={{
            fontSize: 14,
            color: "#0A84FF88",
            fontFamily: "Inter, -apple-system, sans-serif",
            marginTop: 4,
          }}>
            通过 Cache Editing API
          </div>
        </div>

        {/* 结果 */}
        <div style={{
          marginTop: 20,
          backgroundColor: "#0A84FF12",
          border: "1px solid #0A84FF33",
          borderRadius: 14,
          padding: "14px 20px",
          textAlign: "center",
        }}>
          <div style={{ fontSize: 16, color: "#0A84FF", fontWeight: 700, fontFamily: "Inter, sans-serif" }}>
            ✅ 不动缓存前缀
          </div>
          <div style={{ fontSize: 14, color: "#48484A", fontFamily: "Inter, sans-serif", marginTop: 4 }}>
            只删工具结果，Cache 继续命中
          </div>
        </div>
      </div>

      {/* 中间分割线 */}
      <div style={{
        position: "absolute",
        top: "20%",
        bottom: "20%",
        left: "50%",
        width: 1,
        background: "linear-gradient(180deg, transparent, #2C2C2E, transparent)",
      }} />

      {/* 右侧路径 */}
      <div style={{
        position: "absolute",
        top: "26%",
        left: "53%",
        right: "5%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 0,
      }}>
        {/* 节点1 */}
        <div style={{
          width: "100%",
          backgroundColor: "#BF5AF218",
          border: "2px solid #BF5AF255",
          borderRadius: 20,
          padding: "20px 16px",
          textAlign: "center",
        }}>
          <div style={{
            fontSize: 26,
            fontWeight: 800,
            color: "#BF5AF2",
            fontFamily: "Inter, -apple-system, sans-serif",
          }}>
            离开后回来
          </div>
          <div style={{
            fontSize: 14,
            color: "#BF5AF288",
            fontFamily: "Inter, -apple-system, sans-serif",
            marginTop: 4,
          }}>
            服务端 Cache 已过期
          </div>
        </div>

        {/* 箭头 */}
        <div style={{
          width: 3,
          height: 32,
          background: "linear-gradient(180deg, #BF5AF2, #BF5AF288)",
          borderRadius: 2,
        }} />

        {/* 节点2 */}
        <div style={{
          width: "100%",
          backgroundColor: "#BF5AF222",
          border: "2px solid #BF5AF2",
          borderRadius: 20,
          padding: "20px 16px",
          textAlign: "center",
          boxShadow: "0 0 30px #BF5AF222",
        }}>
          <div style={{
            fontSize: 22,
            fontWeight: 800,
            color: "#BF5AF2",
            fontFamily: "Inter, -apple-system, sans-serif",
          }}>
            Time Based Micro Compact
          </div>
          <div style={{
            fontSize: 14,
            color: "#BF5AF288",
            fontFamily: "Inter, -apple-system, sans-serif",
            marginTop: 4,
          }}>
            直接修改消息内容
          </div>
        </div>

        {/* 结果 */}
        <div style={{
          marginTop: 20,
          backgroundColor: "#BF5AF212",
          border: "1px solid #BF5AF233",
          borderRadius: 14,
          padding: "14px 20px",
          textAlign: "center",
        }}>
          <div style={{ fontSize: 16, color: "#BF5AF2", fontWeight: 700, fontFamily: "Inter, sans-serif" }}>
            ✅ 直接替换为占位符
          </div>
          <div style={{ fontSize: 14, color: "#48484A", fontFamily: "Inter, sans-serif", marginTop: 4 }}>
            缓存已失效，无需精细处理
          </div>
        </div>
      </div>

      {/* 底部备注 */}
      <div style={{
        position: "absolute",
        bottom: "10%",
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
      }}>
        <div style={{
          display: "flex",
          gap: 12,
          flexWrap: "wrap",
          justifyContent: "center",
          padding: "0 40px",
        }}>
          {[
            { text: "主线程隔离", color: "#48484A" },
            { text: "query source 区分", color: "#48484A" },
            { text: "子 agent 不受影响", color: "#48484A" },
          ].map((tag, i) => (
            <div key={i} style={{
              backgroundColor: "#1a1a24",
              border: "1px solid #2C2C2E",
              borderRadius: 20,
              padding: "8px 20px",
              fontSize: 14,
              color: tag.color,
              fontFamily: "Inter, -apple-system, sans-serif",
            }}>
              {tag.text}
            </div>
          ))}
        </div>
      </div>
    </AppleBg>
  );
};
