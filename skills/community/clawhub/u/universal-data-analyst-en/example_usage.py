#!/usr/bin/env python3
"""
Universal Data Analyst - Usage Examples

Demonstrates how to use the universal data analysis skill for a complete analysis workflow.
"""

import sys
from pathlib import Path

# Add skill path
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator import DataAnalysisOrchestrator


def example_single_run():
    """
    Example 1: Single-pass full analysis

    Suitable when user intent is clear — completes the entire workflow in one run.
    """
    print("="*80)
    print("Example 1: Single-pass Full Analysis")
    print("="*80)

    # Initialize orchestrator
    orchestrator = DataAnalysisOrchestrator(
        output_dir="./example_output"
    )

    # Run full analysis
    results = orchestrator.run_full_analysis(
        file_path="/path/to/your/data.csv",
        user_intent="Analyze sales trends and customer behavior, identify high-value customer segments"
    )

    print(f"\nAnalysis complete! Results saved at: {results['session_dir']}")
    print("\nGenerated prompt files:")
    for step, info in results['steps'].items():
        if 'prompt_file' in info:
            print(f"  - {step}: {info['prompt_file']}")

    return results


def example_step_by_step():
    """
    Example 2: Step-by-step interactive analysis

    Suitable when you need to manually review results at each step.
    """
    print("="*80)
    print("Example 2: Step-by-step Interactive Analysis")
    print("="*80)

    orchestrator = DataAnalysisOrchestrator()

    # Step 1: Load data
    success, msg = orchestrator.step1_load_data("data.csv")
    if not success:
        print(f"Load failed: {msg}")
        return

    # Step 2: Generate ontology identification prompt
    ontology_prompt, ontology_file = orchestrator.step2_identify_ontology()
    print(f"\nPlease send the prompt in {ontology_file} to an LLM")
    print("Save the JSON result as ontology_result.json")
    input("Press Enter to continue...")

    # Step 3: Data validation
    orchestrator.step3_validate_data()

    # Step 4: Generate analysis planning prompt
    planning_prompt, planning_file = orchestrator.step4_plan_analysis(
        user_intent="Analyze sales trends"
    )
    print(f"\nPlease send the prompt in {planning_file} to an LLM")
    print("Save the JSON result as analysis_plan.json")
    input("Press Enter to continue...")

    # Step 5: Generate script prompt
    script_prompt, script_file = orchestrator.step5_generate_script()
    print(f"\nPlease send the prompt in {script_file} to an LLM")
    print("Save the Python script as analysis_script.py")
    input("Press Enter to continue...")

    # Step 6: Execute and generate report
    orchestrator.step6_execute_analysis("analysis_script.py")

    # Step 7: Generate comprehensive report
    orchestrator.step7_generate_comprehensive_report()

    print("\nAnalysis workflow complete!")


def example_autonomous_mode():
    """
    Example 3: Autonomous mode (no external LLM required)

    Uses rule-based heuristics to infer ontology and strategy.
    """
    print("="*80)
    print("Example 3: Autonomous Mode")
    print("="*80)

    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from main import UniversalDataAnalystV2

    analyst = UniversalDataAnalystV2()

    # Load data
    result = analyst.load_data("/path/to/data.csv")
    print(f"Loaded: {result.rows:,} rows x {result.columns} columns")

    # Autonomous ontology inference (no LLM)
    ontology = analyst.get_ontology_autonomous()
    print(f"\nOntology (autonomous):")
    print(f"  Entity type: {ontology['entity_type']}")
    print(f"  Economic type: {ontology.get('economic_type', 'N/A')}")
    print(f"  Domain: {ontology.get('domain_type', 'N/A')}")
    print(f"  Confidence: {ontology.get('confidence', 'N/A')}")

    # Quality-driven strategy
    strategy = analyst.get_quality_driven_strategy()
    print(f"\nQuality-driven strategy:")
    print(f"  Quality score: {strategy['quality_score']}/100")
    print(f"  Recommended approach: {strategy['recommended_approach']}")
    print(f"  Key warnings: {len(strategy.get('warnings', []))}")


def example_multi_file():
    """
    Example 4: Multi-file join analysis

    Load and join multiple tables automatically.
    """
    print("="*80)
    print("Example 4: Multi-file Join Analysis")
    print("="*80)

    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from main import UniversalDataAnalystV2

    analyst = UniversalDataAnalystV2()

    # Load multiple files
    results = analyst.load_multiple_files([
        "/path/to/users.csv",
        "/path/to/orders.csv",
        "/path/to/products.csv"
    ])

    print(f"Loaded {len(results)} files:")
    for name, result in results.items():
        if result.success:
            print(f"  {name}: {result.rows:,} rows x {result.columns} columns")

    # Analyze join feasibility
    join_report = analyst.analyze_join_feasibility()
    print(f"\nJoin feasibility analysis:")
    print(f"  {join_report['summary']}")
    print(f"  Possible join pairs: {len(join_report['join_pairs'])}")

    # Join tables
    if join_report['join_pairs']:
        first_pair = join_report['join_pairs'][0]
        joined = analyst.join_tables(
            left_table=first_pair['left_table'],
            right_table=first_pair['right_table'],
            join_key=first_pair['join_key']
        )
        if joined is not None:
            print(f"\nJoined table: {len(joined):,} rows x {len(joined.columns)} columns")


def example_different_data_types():
    """
    Example 5: Analysis prompts for different data types
    """
    examples = {
        "Retail transaction data": {
            "file": "sales_data.csv",
            "intent": "Analyze sales trends, customer segmentation, and product portfolio optimization",
            "expected_framework": "Value chain analysis + ABC-XYZ + RFM"
        },
        "User behavior data": {
            "file": "user_events.csv",
            "intent": "Analyze user conversion funnel and recommendation strategy",
            "expected_framework": "Funnel analysis + session mining"
        },
        "Stock price data": {
            "file": "stock_prices.csv",
            "intent": "Analyze price trends and risk characteristics",
            "expected_framework": "Technical analysis + volatility modeling"
        },
        "Scientific experiment data": {
            "file": "experiment_results.csv",
            "intent": "Validate hypotheses and analyze experimental effects",
            "expected_framework": "Hypothesis testing + causal inference"
        }
    }

    print("="*80)
    print("Example 5: Different Data Types")
    print("="*80)

    for data_type, config in examples.items():
        print(f"\n[{data_type}]")
        print(f"  File: {config['file']}")
        print(f"  Intent: {config['intent']}")
        print(f"  Expected framework: {config['expected_framework']}")


def main():
    """Main entry point"""
    print("Universal Data Analyst - Usage Examples")
    print("="*80)

    # Show available examples
    print("\nAvailable examples:")
    print("  1. Single-pass full analysis")
    print("  2. Step-by-step interactive analysis")
    print("  3. Autonomous mode (no external LLM)")
    print("  4. Multi-file join analysis")
    print("  5. Different data type examples")

    # Run demo
    print("\n" + "="*80)
    print("Running Example 5: Different Data Types")
    print("="*80)
    example_different_data_types()

    print("\n" + "="*80)
    print("Tip: Update file paths in example_usage.py to run Examples 1-4")
    print("="*80)


if __name__ == "__main__":
    main()
