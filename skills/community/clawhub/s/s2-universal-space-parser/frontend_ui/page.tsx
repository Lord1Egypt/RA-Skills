"use client";
import React, { useState, useEffect } from 'react';

// =====================================================================
// 🌌 S2-SP-OS: The Space Architect UI (V2.0 - SWM Edition)
// 智能家居空间场景解析器 - 世界模型觉醒版前端驾驶舱
// =====================================================================

const MOCK_PARSED_DATA: Record<string, any> = {
  "智慧客厅": {
    "space_query": "智慧客厅",
    "description": "S2-SWM 核心起居演算节点，高频人机交互与光热力学耦合区。",
    "total_components_suggested": 14,
    "recommended_scenarios": ["全局唤醒", "离家熔断", "沉浸观影 (光声学遮蔽)", "深度疗愈"],
    "s2_6_element_matrix": {
      "Light_光": ["[交互] SSSU 边缘触控阵列", "[执行] DALI/无极调光调色 LED 驱动器", "[执行] 矢量遮阳电机"],
      "Air_气": ["[感知] 五合一空气质量雷达 (实时 S_t 采集)", "[执行] HVAC 底层网关协议"],
      "Sound_声": ["[交互] 远场全息拾音阵列", "[执行] 空间音频全景声发生器"],
      "EM_电磁": ["[计算] S2 OS 边缘计算大本营主机", "[连接] Wi-Fi 7 / Matter 网状网络", "[感知] 77GHz 毫米波空间占位雷达"],
      "Energy_能": ["[计算] 强电箱智能微断总闸 (物理最后防线)"],
      "Vision_视": ["[感知] 3D 仿生入户安防终端"]
    }
  },
  "智能咖啡馆": {
    "space_query": "智能咖啡馆",
    "description": "高密度人流商业节点，强调 Atmos(气) 与 Acoustic(声) 维度的背景控制。",
    "total_components_suggested": 9,
    "recommended_scenarios": ["清晨营业", "高客流强排风", "打烊自清洁预演"],
    "s2_6_element_matrix": {
      "Light_光": ["[执行] 分区多色温聚光矩阵"],
      "Air_气": ["[感知] 商业级 CO2 探测器", "[执行] S2 香氛散发器", "[执行] 强排新风热交换系统"],
      "Sound_声": ["[执行] 多区独立背景白噪音发生器"],
      "EM_电磁": ["[计算] S2 商业边缘计算路由", "[感知] 3D 热成像客流统计雷达"],
      "Energy_能": ["[计算] 商业级三相微断总闸"],
      "Vision_视": []
    }
  }
};

const ELEMENTS_CONFIG: Record<string, { color: string, icon: string, label: string }> = {
  "Light_光": { color: "text-amber-400 border-amber-900/50 bg-amber-950/20", icon: "💡", label: "LUMINA (光)" },
  "Air_气": { color: "text-cyan-400 border-cyan-900/50 bg-cyan-950/20", icon: "🌬️", label: "ATMOS (气)" },
  "Sound_声": { color: "text-fuchsia-400 border-fuchsia-900/50 bg-fuchsia-950/20", icon: "🎵", label: "ACOUSTIC (声)" },
  "EM_电磁": { color: "text-indigo-400 border-indigo-900/50 bg-indigo-950/20", icon: "📡", label: "SPECTRUM (电磁)" },
  "Energy_能": { color: "text-emerald-400 border-emerald-900/50 bg-emerald-950/20", icon: "⚡", label: "ENERGY (能)" },
  "Vision_视": { color: "text-rose-400 border-rose-900/50 bg-rose-950/20", icon: "👁️", label: "VISION (视)" }
};

export default function SpaceArchitectV2() {
  const [selectedSpace, setSelectedSpace] = useState<string>("智慧客厅");
  const data = MOCK_PARSED_DATA[selectedSpace];
  
  // 模拟 S2-SWM 记忆阵列的数据流
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    // 模拟 MCP 服务器不断抓取物理世界动作，并将其转化为 S2-SWM 训练语料的过程
    const interval = setInterval(() => {
      const actions = ["LUMINA.Set_Lux(300)", "ATMOS.Set_Temp(24.5)", "SPECTRUM.Detect_Occupancy()", "ENERGY.Check_Load()"];
      const randomAction = actions[Math.floor(Math.random() * actions.length)];
      const timestamp = new Date().toISOString().split('T')[1].slice(0, 8);
      
      const newLog = `[${timestamp}] 采集: S_t -> ${randomAction} -> S_t+1 | 注入 SWM...`;
      
      setLogs(prev => {
        const nextLogs = [...prev, newLog];
        return nextLogs.length > 8 ? nextLogs.slice(1) : nextLogs; // 保持最多显示 8 条
      });
    }, 2500);

    return () => clearInterval(interval);
  }, []);

  return (
    // 添加暗黑网格背景，营造极客实验室氛围
    <div className="min-h-screen bg-[#020202] text-white font-sans selection:bg-red-500/30 p-4 md:p-8 relative overflow-hidden">
      
      {/* 极客网格背景 */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none"></div>

      {/* 顶部导航 */}
      <header className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between border-b border-zinc-800 pb-6 mb-8">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tighter flex items-center gap-3">
            <span className="bg-red-600 text-black px-2 py-1 rounded text-xl animate-pulse">S2</span> 
            THE SPACE ARCHITECT
          </h1>
          <p className="text-zinc-500 text-xs font-mono mt-2 tracking-widest uppercase">
            SSSU Physical Parser & SWM Data Harvester V2.0
          </p>
        </div>

        {/* 空间选择器 */}
        <div className="mt-4 md:mt-0 flex items-center gap-3">
          <span className="text-xs text-zinc-500 font-mono">TARGET_SPACE:</span>
          <select 
            value={selectedSpace}
            onChange={(e) => setSelectedSpace(e.target.value)}
            className="bg-black/80 border border-zinc-700 text-cyan-400 text-sm font-bold p-2 rounded outline-none focus:border-cyan-500 cursor-pointer backdrop-blur-md"
          >
            {Object.keys(MOCK_PARSED_DATA).map(space => (
              <option key={space} value={space}>{space}</option>
            ))}
          </select>
        </div>
      </header>

      <main className="relative z-10 max-w-[1800px] mx-auto grid grid-cols-1 xl:grid-cols-4 gap-8 animate-in fade-in duration-500">
        
        {/* 左侧主要区域：空间张量矩阵 (占据 3 列) */}
        <div className="xl:col-span-3 space-y-8">
          
          {/* 空间元数据看板 */}
          <div className="bg-gradient-to-br from-zinc-900/60 to-black/80 border border-zinc-800 rounded-2xl p-6 shadow-2xl relative overflow-hidden group hover:border-zinc-700 transition-colors">
            <div className="absolute top-0 right-0 p-4 opacity-5 font-black text-8xl pointer-events-none group-hover:text-cyan-500 transition-colors duration-1000">
              S2-SWM
            </div>
            <h2 className="text-4xl font-black text-white mb-2">{data.space_query}</h2>
            <p className="text-zinc-400 text-sm mb-6 max-w-2xl">{data.description}</p>
            
            <div className="flex flex-wrap gap-2 mb-6">
              <span className="text-[10px] font-bold px-2 py-1 bg-red-950/50 text-red-400 border border-red-900/50 rounded uppercase">
                {data.total_components_suggested} Hardware Atoms
              </span>
              <span className="text-[10px] font-bold px-2 py-1 bg-cyan-950/50 text-cyan-400 border border-cyan-900/50 rounded uppercase flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
                S2-SWM Causal Tracking Active
              </span>
            </div>

            <div className="space-y-2">
              <h3 className="text-xs text-zinc-500 font-bold uppercase tracking-widest">Recommended Scenarios</h3>
              <div className="flex flex-wrap gap-2">
                {data.recommended_scenarios.map((scenario: string, idx: number) => (
                  <div key={idx} className="text-xs bg-black border border-zinc-700 px-3 py-1.5 rounded-full text-zinc-300 shadow-inner">
                    {scenario}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* 六要素物理张量矩阵 */}
          <div>
            <h3 className="text-lg font-black text-white italic border-b border-zinc-800 pb-2 mb-6">
              SIX-ELEMENT HARDWARE MATRIX
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(data.s2_6_element_matrix).map(([elementKey, items]: [string, any]) => {
                const config = ELEMENTS_CONFIG[elementKey] || { color: "text-zinc-400 border-zinc-800 bg-zinc-900", icon: "📦", label: elementKey };
                
                return (
                  <div key={elementKey} className={`border rounded-xl p-5 backdrop-blur-sm flex flex-col ${config.color} shadow-lg transition-all hover:shadow-cyan-900/20 relative overflow-hidden`}>
                    <div className="flex items-center gap-3 mb-4 border-b border-inherit pb-3">
                      <span className="text-2xl drop-shadow-md">{config.icon}</span>
                      <h4 className="font-black tracking-widest text-lg">{config.label}</h4>
                      <span className="ml-auto text-xs font-bold px-2 py-0.5 bg-black/60 rounded-full border border-inherit">
                        {items.length} 节点
                      </span>
                    </div>
                    
                    <div className="flex-1 space-y-2">
                      {items.length > 0 ? (
                        items.map((item: string, idx: number) => {
                          const match = item.match(/^\[(.*?)\]\s*(.*)$/);
                          const tag = match ? match[1] : "";
                          const text = match ? match[2] : item;
                          return (
                            <div key={idx} className="flex items-start gap-2 text-xs bg-black/50 p-2 rounded border border-white/5 hover:bg-black/80 transition-colors">
                              {tag && (
                                <span className="shrink-0 text-[8px] font-black uppercase px-1 py-0.5 rounded bg-white/10 text-white/70 mt-0.5">
                                  {tag}
                                </span>
                              )}
                              <span className="text-white/80 leading-relaxed">{text}</span>
                            </div>
                          );
                        })
                      ) : (
                        <div className="text-xs italic opacity-40 flex h-full items-center justify-center font-mono">
                          NO_HARDWARE_REQUIRED
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* 右侧边栏：Chronos Memzero 数据收割流 */}
        <aside className="xl:col-span-1">
          <div className="bg-black/90 border border-zinc-800 rounded-xl p-4 h-full min-h-[500px] flex flex-col shadow-[0_0_30px_rgba(0,0,0,0.8)] relative">
            <div className="flex items-center justify-between border-b border-zinc-800 pb-3 mb-3">
              <h3 className="text-sm font-black text-cyan-400 tracking-widest uppercase flex items-center gap-2">
                <span className="w-2 h-2 bg-cyan-400 rounded-sm animate-pulse"></span>
                Chronos Memzero
              </h3>
              <span className="text-[9px] text-zinc-500 font-mono bg-zinc-900 px-1 py-0.5 rounded">.jsonl stream</span>
            </div>
            
            <p className="text-[10px] text-zinc-500 font-mono mb-4 leading-relaxed">
              &gt; 正在通过 MCP Server 监听 SSSU 物理动作，持续收割空间状态转移语料，为 S2-SWM 提供第一性原理数据训练集。
            </p>

            {/* 滚动的终端日志 */}
            <div className="flex-1 bg-zinc-950 border border-zinc-900 rounded p-3 font-mono text-[10px] overflow-hidden relative">
              <div className="absolute inset-0 pointer-events-none shadow-[inset_0_0_20px_rgba(0,0,0,1)] z-10"></div>
              <div className="space-y-2 flex flex-col justify-end h-full">
                {logs.length === 0 && <div className="text-zinc-600 animate-pulse">Awaiting causal events...</div>}
                {logs.map((log, idx) => (
                  <div key={idx} className="text-emerald-400/80 animate-in slide-in-from-bottom-2 fade-in">
                    {log}
                  </div>
                ))}
              </div>
            </div>
            
            {/* 底部状态条 */}
            <div className="mt-4 flex items-center justify-between text-[9px] font-mono text-zinc-600 border-t border-zinc-900 pt-2">
              <span>S_t+1 PREDICTION: <span className="text-yellow-500/70">TRAINING</span></span>
              <span>RATE: 0.4 Hz</span>
            </div>
          </div>
        </aside>

      </main>
    </div>
  );
}