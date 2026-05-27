"""
Developer Strategy Cases and Archetypes

Purpose:
    Build a consulting-style developer archetype analysis for Vietnam
    residential real estate developers under public policy uncertainty.

Inputs:
    data/developer_strategy_cases.csv
    output/scenario_matrix.csv
    output/policy_uncertainty_index.csv

Outputs:
    output/developer_archetypes.csv

Important:
    This script classifies sourced qualitative strategy cases. It does not
    calculate valuation metrics or fabricate financial data.
"""

from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "output"

DEVELOPER_CASES_PATH = DATA_DIR / "developer_strategy_cases.csv"
SCENARIO_MATRIX_PATH = OUTPUT_DIR / "scenario_matrix.csv"
POLICY_INDEX_PATH = OUTPUT_DIR / "policy_uncertainty_index.csv"
ARCHETYPES_OUTPUT_PATH = OUTPUT_DIR / "developer_archetypes.csv"

REQUIRED_CASE_COLUMNS = {
    "company",
    "year",
    "segment_focus",
    "land_bank_strategy",
    "capital_strategy",
    "launch_strategy",
    "legal_risk_exposure",
    "liquidity_position",
    "strategic_response",
    "best_fit_scenario",
    "key_risks",
    "source_url",
    "notes",
}

REQUIRED_SCENARIO_COLUMNS = {
    "scenario_name",
    "scenario_definition",
    "policy_condition",
    "market_condition",
    "developer_implication",
    "product_strategy",
    "land_bank_strategy",
    "capital_strategy",
    "launch_strategy",
    "risk_management",
    "trigger_indicators",
    "linked_policy_drivers",
    "confidence_level",
    "notes",
}

REQUIRED_INDEX_COLUMNS = {
    "year",
    "legal_uncertainty_score",
    "credit_uncertainty_score",
    "demand_support_uncertainty_score",
    "infrastructure_execution_uncertainty_score",
    "policy_uncertainty_score",
    "interpretation",
    "dominant_uncertainty_driver",
}

CASE_CONTROLLED_VALUES = {
    "legal_risk_exposure": {"Low", "Medium", "High", "Mixed/Unclear"},
    "liquidity_position": {"Strong", "Moderate", "Stressed", "Mixed/Unclear"},
}

SENSITIVITY_VALUES = {"Low", "Medium", "High"}
POSTURE_VALUES = {"Offensive", "Selective", "Defensive", "Restructuring-first"}

ARCHETYPE_COLUMNS = [
    "company",
    "archetype",
    "archetype_description",
    "policy_sensitivity",
    "capital_sensitivity",
    "legal_sensitivity",
    "demand_sensitivity",
    "recommended_posture",
    "scenario_a_implication",
    "scenario_b_implication",
    "scenario_c_implication",
    "notes",
]


def load_csv(path: Path) -> pd.DataFrame:
    """Load a required CSV file with a clear error if it is missing."""
    if not path.exists():
        raise FileNotFoundError(f"Required input file not found: {path}")
    return pd.read_csv(path)


def validate_columns(df: pd.DataFrame, required_columns: set[str], file_name: str) -> None:
    """Validate that a dataframe includes all expected columns."""
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"{file_name} is missing required columns: {sorted(missing)}")


def validate_developer_cases(df: pd.DataFrame) -> None:
    """Validate required fields, controlled values, and source URLs."""
    validate_columns(df, REQUIRED_CASE_COLUMNS, "developer_strategy_cases.csv")

    for column, allowed_values in CASE_CONTROLLED_VALUES.items():
        invalid_values = sorted(set(df[column].dropna()) - allowed_values)
        if invalid_values:
            raise ValueError(f"{column} has invalid values: {invalid_values}")

    missing_sources = df["source_url"].isna() | (
        df["source_url"].astype(str).str.strip() == ""
    )
    if missing_sources.any():
        companies = df.loc[missing_sources, "company"].tolist()
        raise ValueError(f"Missing source URLs for companies: {companies}")


def validate_archetypes(df: pd.DataFrame) -> None:
    """Validate controlled vocabulary in the generated archetype table."""
    for column in [
        "policy_sensitivity",
        "capital_sensitivity",
        "legal_sensitivity",
        "demand_sensitivity",
    ]:
        invalid_values = sorted(set(df[column].dropna()) - SENSITIVITY_VALUES)
        if invalid_values:
            raise ValueError(f"{column} has invalid values: {invalid_values}")

    invalid_postures = sorted(set(df["recommended_posture"].dropna()) - POSTURE_VALUES)
    if invalid_postures:
        raise ValueError(f"recommended_posture has invalid values: {invalid_postures}")


def get_scenario_names(scenario_df: pd.DataFrame) -> set[str]:
    """Return available scenario names for light consistency checks."""
    return set(scenario_df["scenario_name"].dropna())


def validate_best_fit_scenarios(cases_df: pd.DataFrame, scenario_df: pd.DataFrame) -> None:
    """Ensure case scenario references map to the scenario matrix."""
    scenario_names = get_scenario_names(scenario_df)
    invalid_refs: list[str] = []

    for _, row in cases_df.iterrows():
        refs = [item.strip() for item in str(row["best_fit_scenario"]).split(";")]
        for ref in refs:
            if ref and ref not in scenario_names:
                invalid_refs.append(f"{row['company']}: {ref}")

    if invalid_refs:
        raise ValueError(f"Invalid best_fit_scenario references: {invalid_refs}")


def build_developer_archetypes(cases_df: pd.DataFrame, index_df: pd.DataFrame) -> pd.DataFrame:
    """Classify each developer into a consulting-style strategic archetype."""
    index_context = summarize_policy_index_context(index_df)

    archetype_map = {
        "Vinhomes": {
            "archetype": "Scale leader / integrated mega developer",
            "archetype_description": (
                "Large-scale integrated township developer with strong execution "
                "capacity, brand power, and ecosystem advantages."
            ),
            "policy_sensitivity": "Medium",
            "capital_sensitivity": "Medium",
            "legal_sensitivity": "Medium",
            "demand_sensitivity": "Medium",
            "recommended_posture": "Offensive",
            "scenario_a_implication": (
                "Accelerate legally ready mega projects and use scale to capture "
                "improving buyer confidence."
            ),
            "scenario_b_implication": (
                "Prioritize projects with the clearest approvals, strongest sales "
                "velocity, and infrastructure-backed locations."
            ),
            "scenario_c_implication": (
                "Protect cash conversion, slow marginal launches, and avoid adding "
                "execution risk on unresolved land parcels."
            ),
        },
        "Nam Long": {
            "archetype": "Financially disciplined real-demand developer",
            "archetype_description": (
                "Integrated township and affordable-mid developer oriented toward "
                "end-user demand, partnerships, and disciplined capital use."
            ),
            "policy_sensitivity": "Medium",
            "capital_sensitivity": "Medium",
            "legal_sensitivity": "Medium",
            "demand_sensitivity": "Medium",
            "recommended_posture": "Selective",
            "scenario_a_implication": (
                "Scale affordable and township products while using partnerships "
                "to speed execution."
            ),
            "scenario_b_implication": (
                "Lean into affordable-mid products, handovers, and legally ready "
                "phases in existing townships."
            ),
            "scenario_c_implication": (
                "Preserve financial discipline and prioritize high-absorption, "
                "lower-ticket products."
            ),
        },
        "Khang Dien": {
            "archetype": "Financially disciplined real-demand developer",
            "archetype_description": (
                "HCMC-focused residential developer emphasizing transparent legal "
                "status, controlled phasing, and reputable partnerships."
            ),
            "policy_sensitivity": "Medium",
            "capital_sensitivity": "Medium",
            "legal_sensitivity": "Low",
            "demand_sensitivity": "Medium",
            "recommended_posture": "Selective",
            "scenario_a_implication": (
                "Launch more aggressively from legally clean projects and trusted "
                "partnership platforms."
            ),
            "scenario_b_implication": (
                "Continue phased launches around legal clarity, completed products, "
                "and demand-resilient HCMC locations."
            ),
            "scenario_c_implication": (
                "Maintain balance-sheet discipline and delay higher-ticket phases "
                "if absorption weakens."
            ),
        },
        "Novaland": {
            "archetype": "Turnaround / liquidity-constrained developer",
            "archetype_description": (
                "Large mixed-project developer whose near-term strategy depends on "
                "debt restructuring, legal clearance, and project delivery."
            ),
            "policy_sensitivity": "High",
            "capital_sensitivity": "High",
            "legal_sensitivity": "High",
            "demand_sensitivity": "High",
            "recommended_posture": "Restructuring-first",
            "scenario_a_implication": (
                "Use legal unlocks to restart priority projects and rebuild buyer "
                "and creditor confidence."
            ),
            "scenario_b_implication": (
                "Focus scarce capital on projects with clearer legal status and "
                "near-term handover potential."
            ),
            "scenario_c_implication": (
                "Prioritize liquidity, restructuring milestones, stakeholder trust, "
                "and asset monetization over new launches."
            ),
        },
        "Dat Xanh": {
            "archetype": "Brokerage-linked asset-light developer",
            "archetype_description": (
                "Developer and distribution platform with brokerage reach, project "
                "development exposure, and restructuring toward broader asset roles."
            ),
            "policy_sensitivity": "Medium",
            "capital_sensitivity": "Medium",
            "legal_sensitivity": "Medium",
            "demand_sensitivity": "High",
            "recommended_posture": "Selective",
            "scenario_a_implication": (
                "Use brokerage reach and partner network to capture renewed market "
                "liquidity and accelerate priority launches."
            ),
            "scenario_b_implication": (
                "Concentrate on legally prepared projects and services growth in "
                "markets with clear transaction recovery."
            ),
            "scenario_c_implication": (
                "Keep asset exposure light, protect cash flow from services, and "
                "avoid unclear project commitments."
            ),
        },
    }

    rows = []
    for _, case in cases_df.iterrows():
        company = case["company"]
        if company not in archetype_map:
            raise ValueError(f"No archetype mapping defined for company: {company}")

        row = {"company": company, **archetype_map[company]}
        row["notes"] = (
            f"Derived from sourced developer strategy case and scenario matrix. "
            f"{index_context} Company-specific case note: {case['notes']}"
        )
        rows.append(row)

    return pd.DataFrame(rows, columns=ARCHETYPE_COLUMNS)


def summarize_policy_index_context(index_df: pd.DataFrame) -> str:
    """Create a short context note from the rule-based uncertainty index."""
    score_series = pd.to_numeric(index_df["policy_uncertainty_score"], errors="coerce")
    if score_series.isna().all():
        return "Policy index context unavailable."

    highest_idx = score_series.idxmax()
    highest_year = int(index_df.loc[highest_idx, "year"])
    highest_driver = index_df.loc[highest_idx, "dominant_uncertainty_driver"]
    return (
        f"Policy index context: highest historical uncertainty year is "
        f"{highest_year}, driven by {highest_driver}."
    )


def save_archetypes(archetypes_df: pd.DataFrame, path: Path) -> None:
    """Save archetypes to CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    archetypes_df.to_csv(path, index=False)


def print_console_summary(cases_df: pd.DataFrame, archetypes_df: pd.DataFrame) -> None:
    """Print a concise strategy summary for quick QA."""
    print("Developer Archetype Analysis summary")
    print(f"- Companies analyzed: {cases_df['company'].nunique()}")
    print("- Archetypes:")
    for archetype in sorted(archetypes_df["archetype"].unique()):
        print(f"  {archetype}")
    print("- Recommended posture by company:")
    for _, row in archetypes_df.iterrows():
        print(f"  {row['company']}: {row['recommended_posture']}")
    print("- Key strategic risks:")
    for _, row in cases_df.iterrows():
        print(f"  {row['company']}: {row['key_risks']}")
    print("- Output saved to: output/developer_archetypes.csv")


def main() -> None:
    cases_df = load_csv(DEVELOPER_CASES_PATH)
    scenario_df = load_csv(SCENARIO_MATRIX_PATH)
    index_df = load_csv(POLICY_INDEX_PATH)

    validate_developer_cases(cases_df)
    validate_columns(scenario_df, REQUIRED_SCENARIO_COLUMNS, "scenario_matrix.csv")
    validate_columns(index_df, REQUIRED_INDEX_COLUMNS, "policy_uncertainty_index.csv")
    validate_best_fit_scenarios(cases_df, scenario_df)

    archetypes_df = build_developer_archetypes(cases_df, index_df)
    validate_archetypes(archetypes_df)
    save_archetypes(archetypes_df, ARCHETYPES_OUTPUT_PATH)
    print_console_summary(cases_df, archetypes_df)


if __name__ == "__main__":
    main()
