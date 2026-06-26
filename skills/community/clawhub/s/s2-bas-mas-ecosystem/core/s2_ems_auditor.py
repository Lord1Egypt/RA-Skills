import json
from datetime import datetime

# ==========================================
# 1. 物理账本与定价孪生 (Resource & Tariff Twin)
# ==========================================
class ResourceLedgerState:
    def __init__(self):
        # 实时表计物理读数 (模拟本月累计)
        self.current_month_consumption = {
            "electricity_kwh": {"hvac": 125000.0, "lighting": 45000.0, "plug_loads": 30000.0, "elevators": 15000.0},
            "water_tons": {"domestic": 3500.0, "cooling_tower_makeup": 1200.0},
            "gas_m3": {"boiler": 800.0, "kitchen": 2200.0}
        }
        
        # 历史同期基线数据 (去年同月，已剔除气象与人流差异后的修正基线)
        self.baseline_month_consumption = {
            "electricity_kwh": {"total": 268000.0},
            "water_tons": {"total": 5200.0},
            "gas_m3": {"total": 3100.0}
        }

        # 商业定价矩阵 (Tariff Matrix)
        self.tariffs = {
            "electricity_avg_cny_per_kwh": 0.85,  # 综合平均电价
            "water_cny_per_ton": 4.5,             # 商业水价
            "gas_cny_per_m3": 3.8,                # 商业天然气价
            "carbon_tax_cny_per_ton": 60.0        # 模拟碳排交易指导价
        }
        
        # 碳排放因子 (CEF)
        self.carbon_factors = {
            "electricity_kg_co2_per_kwh": 0.58,   # 电网排放因子
            "water_kg_co2_per_ton": 0.25,         # 水处理折算排放
            "gas_kg_co2_per_m3": 2.16             # 天然气直排因子
        }

# ==========================================
# 2. S2 能源与财务审计智能体 (EMS Auditor Agent)
# ==========================================
class S2EMSAuditorAgent:
    def __init__(self, agent_id="S2-EMS-CFO"):
        self.agent_id = agent_id

    def calculate_ledger(self, consumption, tariffs, carbon_factors):
        """核心计算算子：将物理量转化为财务与碳排数字"""
        # 汇总物理量
        total_elec = sum(consumption["electricity_kwh"].values()) if isinstance(consumption["electricity_kwh"], dict) else consumption["electricity_kwh"]["total"]
        total_water = sum(consumption["water_tons"].values()) if isinstance(consumption["water_tons"], dict) else consumption["water_tons"]["total"]
        total_gas = sum(consumption["gas_m3"].values()) if isinstance(consumption["gas_m3"], dict) else consumption["gas_m3"]["total"]

        # 计算财务成本 (OPEX)
        cost_elec = total_elec * tariffs["electricity_avg_cny_per_kwh"]
        cost_water = total_water * tariffs["water_cny_per_ton"]
        cost_gas = total_gas * tariffs["gas_cny_per_m3"]
        total_cost = cost_elec + cost_water + cost_gas

        # 计算碳排放 (吨)
        carbon_elec = (total_elec * carbon_factors["electricity_kg_co2_per_kwh"]) / 1000.0
        carbon_water = (total_water * carbon_factors["water_kg_co2_per_ton"]) / 1000.0
        carbon_gas = (total_gas * carbon_factors["gas_kg_co2_per_m3"]) / 1000.0
        total_carbon_tons = carbon_elec + carbon_water + carbon_gas

        return {
            "physical": {"elec_kwh": total_elec, "water_tons": total_water, "gas_m3": total_gas},
            "financial_cny": {"elec": cost_elec, "water": cost_water, "gas": cost_gas, "total": total_cost},
            "carbon_tons": {"elec": carbon_elec, "water": carbon_water, "gas": carbon_gas, "total": total_carbon_tons}
        }

    def generate_executive_audit_report(self, state):
        """生成高管级能源审计与横向比对报告"""
        print(f"💰 [{self.agent_id}] 正在拉取全维表计网络，执行财务与碳资产结算...")
        
        # 1. 计算当前周期账单
        current_ledger = self.calculate_ledger(state.current_month_consumption, state.tariffs, state.carbon_factors)
        
        # 2. 计算基线周期账单 (去年同期)
        baseline_ledger = self.calculate_ledger(state.baseline_month_consumption, state.tariffs, state.carbon_factors)

        # 3. 核心：计算因果节能效益 (S2 优化带来的真金白银)
        saved_cny = baseline_ledger["financial_cny"]["total"] - current_ledger["financial_cny"]["total"]
        saved_carbon_tons = baseline_ledger["carbon_tons"]["total"] - current_ledger["carbon_tons"]["total"]
        savings_percentage = (saved_cny / baseline_ledger["financial_cny"]["total"]) * 100.0

        report = {
            "report_id": f"EMS-AUDIT-{int(datetime.now().timestamp())}",
            "period": "CURRENT_MONTH",
            "executive_summary": {
                "total_opex_cny": round(current_ledger["financial_cny"]["total"], 2),
                "total_carbon_tons": round(current_ledger["carbon_tons"]["total"], 2),
                "yoy_savings_cny": round(saved_cny, 2),
                "yoy_savings_percentage": f"{round(savings_percentage, 1)}%",
                "carbon_mitigated_tons": round(saved_carbon_tons, 2)
            },
            "subsystem_breakdown": {
                "hvac_share_percent": round((state.current_month_consumption["electricity_kwh"]["hvac"] / current_ledger["physical"]["elec_kwh"]) * 100, 1),
                "lighting_share_percent": round((state.current_month_consumption["electricity_kwh"]["lighting"] / current_ledger["physical"]["elec_kwh"]) * 100, 1)
            },
            "ai_financial_insights": []
        }

        # 智能诊断：寻找可以套现的“隐形资产”
        if savings_percentage > 15.0:
            report["ai_financial_insights"].append("🏆 [绩效评估] S2 智能体群组本月协同表现优异，综合节能率突破 15%，已成功压降运营成本。")
        if saved_carbon_tons > 20.0:
            carbon_value = saved_carbon_tons * state.tariffs["carbon_tax_cny_per_ton"]
            report["ai_financial_insights"].append(f"🍃 [碳资产转化] 本月减排 {round(saved_carbon_tons,1)} 吨碳，若接入碳交易市场，可额外变现约 {round(carbon_value, 2)} 元人民币。")

        return report

# ==========================================
# 3. 运行：EMS 审计结算
# ==========================================
if __name__ == "__main__":
    ledger_state = ResourceLedgerState()
    ems_agent = S2EMSAuditorAgent()

    print("="*75)
    print(" 🧾 S2-EMS-AGENT : 能源账本与碳资产审计引擎")
    print("="*75)

    audit_report = ems_agent.generate_executive_audit_report(ledger_state)
    print("\n📊 [ 董事会级财务与能源审计报告 / Executive EMS Report ]:")
    print(json.dumps(audit_report, indent=2, ensure_ascii=False))