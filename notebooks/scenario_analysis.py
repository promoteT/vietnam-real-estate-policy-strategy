"""
Scenario Analysis

Purpose:
    Translate the Policy Uncertainty Index and policy timeline into a
    consulting-style scenario matrix for Vietnam residential real estate
    developers.

Important:
    These scenarios are planning tools, not predictions. The recommendations
    are qualitative strategic postures derived from coded policy events and the
    rule-based Policy Uncertainty Index.
"""

from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "output"

INDEX_PATH = OUTPUT_DIR / "policy_uncertainty_index.csv"
POLICY_TIMELINE_PATH = DATA_DIR / "policy_timeline.csv"
SCENARIO_OUTPUT_PATH = OUTPUT_DIR / "scenario_matrix.csv"

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

REQUIRED_POLICY_COLUMNS = {
    "date",
    "policy_area",
    "policy_name",
    "institution",
    "summary",
    "affected_market_lever",
    "expected_direction",
    "uncertainty_level",
    "source_url",
    "notes",
}

SCENARIO_COLUMNS = [
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
]


def load_csv(path: Path) -> pd.DataFrame:
    """Load a required CSV with a clear error if the file is missing."""
    if not path.exists():
        raise FileNotFoundError(f"Required input file not found: {path}")
    return pd.read_csv(path)


def validate_columns(df: pd.DataFrame, required_columns: set[str], file_name: str) -> None:
    """Validate that an input file contains the columns needed for scenario work."""
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"{file_name} is missing required columns: {sorted(missing)}")


def summarize_index_evidence(index_df: pd.DataFrame) -> dict[str, str]:
    """Extract concise evidence points from the Policy Uncertainty Index."""
    if index_df.empty:
        raise ValueError("Policy Uncertainty Index is empty.")

    score_series = pd.to_numeric(index_df["policy_uncertainty_score"], errors="coerce")
    if score_series.isna().all():
        raise ValueError("policy_uncertainty_score contains no numeric values.")

    highest_idx = score_series.idxmax()
    highest_year = int(index_df.loc[highest_idx, "year"])
    highest_driver = index_df.loc[highest_idx, "dominant_uncertainty_driver"]

    forward_years = index_df[index_df["year"].isin([2024, 2025])]
    forward_drivers = sorted(
        {
            driver
            for value in forward_years["dominant_uncertainty_driver"].dropna()
            for driver in str(value).split(";")
            if driver
        }
    )

    return {
        "highest_year": str(highest_year),
        "highest_driver": highest_driver,
        "forward_drivers": ";".join(forward_drivers),
    }


def summarize_policy_drivers(policy_df: pd.DataFrame) -> str:
    """Summarize the policy levers represented in the timeline."""
    priority_order = [
        "Land policy",
        "Housing policy",
        "Real estate business regulation",
        "Credit policy",
        "Corporate bond regulation",
        "Social housing policy",
        "Infrastructure/public investment",
        "Project legal bottleneck",
        "Market transparency",
    ]
    present_areas = set(policy_df["policy_area"].dropna())
    ordered_areas = [area for area in priority_order if area in present_areas]
    return "; ".join(ordered_areas)


def build_scenario_matrix(index_df: pd.DataFrame, policy_df: pd.DataFrame) -> pd.DataFrame:
    """Build the three required strategic scenarios."""
    evidence = summarize_index_evidence(index_df)
    linked_policy_drivers = summarize_policy_drivers(policy_df)
    evidence_note = (
        f"Index evidence: {evidence['highest_year']} had the highest uncertainty, "
        f"driven by {evidence['highest_driver']}; 2024-2025 drivers point to "
        f"{evidence['forward_drivers']} as forward-looking uncertainties."
    )

    scenarios = [
        {
            "scenario_name": "Scenario A - Policy Unlock",
            "scenario_definition": (
                "Legal bottlenecks are resolved faster than expected, credit "
                "conditions normalize, social housing and infrastructure policies "
                "are implemented effectively, and buyer confidence improves."
            ),
            "policy_condition": (
                "Land, housing, real estate business, and project-clearance rules "
                "move from uncertainty to practical implementation."
            ),
            "market_condition": (
                "Buyer confidence improves and stronger execution supports broader "
                "project launches, without assuming a quantified demand forecast."
            ),
            "developer_implication": (
                "Offensive posture: prepared developers can accelerate approved "
                "projects and capture demand in legally clear segments."
            ),
            "product_strategy": (
                "Prioritize affordable, mid-market, and social-housing-adjacent "
                "products where policy support and end-user demand align."
            ),
            "land_bank_strategy": (
                "Advance legally clean land parcels and selectively replenish land "
                "banks in infrastructure-supported corridors."
            ),
            "capital_strategy": (
                "Refinance early where possible, diversify bank and bond funding, "
                "and preserve buffers for construction ramp-up."
            ),
            "launch_strategy": (
                "Bring forward launches for projects with complete legal status, "
                "clear buyer demand, and executable construction schedules."
            ),
            "risk_management": (
                "Avoid overextending into unresolved land or approval cases; keep "
                "stage-gates tied to legal clearance and sales absorption."
            ),
            "trigger_indicators": (
                "Faster legal approvals; improving real estate credit growth; "
                "easier corporate bond issuance/refinancing; rising absorption "
                "rate; declining mortgage rate trend; social housing disbursement "
                "progress; infrastructure execution progress; stronger developer "
                "liquidity indicators."
            ),
            "linked_policy_drivers": linked_policy_drivers,
            "confidence_level": "Medium",
            "notes": (
                f"{evidence_note} Scenario is a planning tool, not a prediction."
            ),
        },
        {
            "scenario_name": "Scenario B - Selective Recovery",
            "scenario_definition": (
                "Legally clean and financially strong developers recover first, "
                "while weaker developers and legally unclear projects remain "
                "constrained. Demand recovery is uneven across segments."
            ),
            "policy_condition": (
                "Implementation improves unevenly across provinces, project types, "
                "and approval stages."
            ),
            "market_condition": (
                "Liquidity and demand recover first in transparent projects and "
                "end-user segments; speculative or legally unclear projects lag."
            ),
            "developer_implication": (
                "Selective posture: winners are developers with clean approvals, "
                "credible brands, disciplined leverage, and demand-fit products."
            ),
            "product_strategy": (
                "Focus on end-user housing, affordable and mid-market formats, "
                "and smaller ticket sizes where absorption is more resilient."
            ),
            "land_bank_strategy": (
                "Prioritize land bank legal audit, conversion feasibility, and "
                "capital-light partnerships over broad accumulation."
            ),
            "capital_strategy": (
                "Maintain conservative leverage, stagger maturities, and use joint "
                "ventures or asset recycling for projects outside core priorities."
            ),
            "launch_strategy": (
                "Sequence launches by legal readiness, affordability, presales "
                "visibility, and financing availability."
            ),
            "risk_management": (
                "Segment projects by legal risk, funding risk, and demand depth; "
                "pause launches where one of the three is weak."
            ),
            "trigger_indicators": (
                "Mixed legal approval speed; moderate real estate credit growth; "
                "selective corporate bond refinancing access; uneven absorption "
                "rate; stable or slowly falling mortgage rates; partial social "
                "housing disbursement progress; uneven infrastructure execution; "
                "diverging developer liquidity indicators."
            ),
            "linked_policy_drivers": linked_policy_drivers,
            "confidence_level": "Medium",
            "notes": (
                f"{evidence_note} Base planning case for differentiated recovery; "
                "not a forecast."
            ),
        },
        {
            "scenario_name": "Scenario C - Policy Drag",
            "scenario_definition": (
                "Legal procedures remain slow, credit and bond market access remain "
                "constrained, affordability pressure persists, and developers must "
                "prioritize liquidity and risk control."
            ),
            "policy_condition": (
                "Legal implementation remains slow or inconsistent, while credit "
                "and bond channels remain cautious."
            ),
            "market_condition": (
                "Demand stays price-sensitive, project launches remain limited, "
                "and capital access separates resilient developers from distressed "
                "developers."
            ),
            "developer_implication": (
                "Defensive posture: liquidity preservation and legal-risk reduction "
                "matter more than aggressive growth."
            ),
            "product_strategy": (
                "Shift toward smaller, more affordable units and defer luxury or "
                "speculative products with weak absorption visibility."
            ),
            "land_bank_strategy": (
                "Stop non-core land accumulation, monetize peripheral assets where "
                "needed, and resolve legal documentation before new commitments."
            ),
            "capital_strategy": (
                "Prioritize cash preservation, debt maturity extension, covenant "
                "management, and lower reliance on short-tenor bond funding."
            ),
            "launch_strategy": (
                "Launch only legally complete projects with realistic pricing, "
                "strong presales visibility, and controlled construction cash burn."
            ),
            "risk_management": (
                "Build liquidity dashboards, monitor refinancing windows, protect "
                "customer trust, and set stop-loss rules for delayed projects."
            ),
            "trigger_indicators": (
                "Slow legal approvals; weak real estate credit growth; tight "
                "corporate bond issuance/refinancing; low absorption rate; elevated "
                "mortgage rate trend; slow social housing disbursement progress; "
                "delayed infrastructure execution; deteriorating developer "
                "liquidity indicators."
            ),
            "linked_policy_drivers": linked_policy_drivers,
            "confidence_level": "Medium",
            "notes": (
                f"{evidence_note} Scenario stress-tests strategy under prolonged "
                "policy and capital-market drag; not a prediction."
            ),
        },
    ]

    return pd.DataFrame(scenarios, columns=SCENARIO_COLUMNS)


def save_scenario_matrix(df: pd.DataFrame, path: Path) -> None:
    """Save the scenario matrix to output/scenario_matrix.csv."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def print_console_summary(scenario_df: pd.DataFrame) -> None:
    """Print a concise scenario QA summary."""
    postures = {
        "Scenario A - Policy Unlock": "offensive",
        "Scenario B - Selective Recovery": "selective",
        "Scenario C - Policy Drag": "defensive",
    }

    print("Scenario Matrix summary")
    print(f"- Scenarios created: {len(scenario_df)}")
    print("- Scenario names:")
    for scenario_name in scenario_df["scenario_name"]:
        print(f"  {scenario_name}")
    print("- Key strategic posture:")
    for scenario_name in scenario_df["scenario_name"]:
        print(f"  {scenario_name}: {postures[scenario_name]}")
    print("- Output saved to: output/scenario_matrix.csv")


def main() -> None:
    index_df = load_csv(INDEX_PATH)
    policy_df = load_csv(POLICY_TIMELINE_PATH)
    validate_columns(index_df, REQUIRED_INDEX_COLUMNS, "policy_uncertainty_index.csv")
    validate_columns(policy_df, REQUIRED_POLICY_COLUMNS, "policy_timeline.csv")

    scenario_df = build_scenario_matrix(index_df, policy_df)
    save_scenario_matrix(scenario_df, SCENARIO_OUTPUT_PATH)
    print_console_summary(scenario_df)


if __name__ == "__main__":
    main()
