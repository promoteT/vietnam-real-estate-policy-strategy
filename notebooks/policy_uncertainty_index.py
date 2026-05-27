"""
Policy Uncertainty Index

Purpose:
    Build a simple, transparent Policy Uncertainty Index for Vietnam residential
    real estate from the sourced policy timeline.

Method:
    - Convert coded uncertainty levels into numeric scores.
    - Group policy events into four consulting-style uncertainty pillars.
    - Calculate annual average pillar scores.
    - Average available pillar scores into an overall annual score.

Important:
    This is a rule-based portfolio project index derived from coded policy
    events. It is not an official index and should not be interpreted as a
    statistical or causal estimate.
"""

from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "output"

INPUT_PATH = DATA_DIR / "policy_timeline.csv"
OUTPUT_PATH = OUTPUT_DIR / "policy_uncertainty_index.csv"

REQUIRED_COLUMNS = {
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

UNCERTAINTY_SCORE_MAP = {
    "Low": 1,
    "Medium": 3,
    "High": 5,
}

PILLARS = {
    "legal_uncertainty_score": {
        "Land policy",
        "Housing policy",
        "Real estate business regulation",
        "Project legal bottleneck",
        "Market transparency",
    },
    "credit_uncertainty_score": {
        "Credit policy",
        "Corporate bond regulation",
    },
    "demand_support_uncertainty_score": {
        "Housing policy",
        "Social housing policy",
        "Credit policy",
    },
    "infrastructure_execution_uncertainty_score": {
        "Infrastructure/public investment",
    },
}

INDEX_NOTE = (
    "Rule-based portfolio project index derived from coded policy events; "
    "not an official index."
)


def load_policy_timeline(path: Path) -> pd.DataFrame:
    """Load the real policy timeline dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    return pd.read_csv(path)


def validate_required_columns(df: pd.DataFrame) -> None:
    """Confirm that all required fields are available before scoring."""
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def prepare_policy_events(df: pd.DataFrame) -> pd.DataFrame:
    """Parse dates and convert qualitative uncertainty levels to numeric scores."""
    prepared = df.copy()
    prepared["date"] = pd.to_datetime(prepared["date"], errors="coerce")

    if prepared["date"].isna().any():
        bad_rows = prepared.loc[prepared["date"].isna(), "policy_name"].tolist()
        raise ValueError(f"Invalid or missing dates for policies: {bad_rows}")

    unknown_levels = sorted(
        set(prepared["uncertainty_level"].dropna()) - set(UNCERTAINTY_SCORE_MAP)
    )
    if unknown_levels:
        raise ValueError(f"Unknown uncertainty levels: {unknown_levels}")

    missing_sources = prepared["source_url"].isna() | (
        prepared["source_url"].astype(str).str.strip() == ""
    )
    if missing_sources.any():
        bad_rows = prepared.loc[missing_sources, "policy_name"].tolist()
        raise ValueError(f"Missing source URLs for policies: {bad_rows}")

    prepared["year"] = prepared["date"].dt.year
    prepared["uncertainty_score"] = prepared["uncertainty_level"].map(
        UNCERTAINTY_SCORE_MAP
    )
    return prepared


def calculate_pillar_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate annual average uncertainty score for each policy pillar."""
    years = sorted(df["year"].unique())
    annual_index = pd.DataFrame({"year": years})

    for pillar_name, policy_areas in PILLARS.items():
        pillar_events = df[df["policy_area"].isin(policy_areas)]
        pillar_scores = (
            pillar_events.groupby("year", as_index=False)["uncertainty_score"]
            .mean()
            .rename(columns={"uncertainty_score": pillar_name})
        )
        annual_index = annual_index.merge(pillar_scores, on="year", how="left")

    return annual_index


def interpret_score(score: float) -> str:
    """Convert the numeric index score into a recruiter-friendly label."""
    if pd.isna(score):
        return ""
    if 1.00 <= score <= 2.00:
        return "Low uncertainty"
    if 2.01 <= score <= 3.50:
        return "Moderate uncertainty"
    if 3.51 <= score <= 5.00:
        return "High uncertainty"
    raise ValueError(f"Policy uncertainty score outside expected range: {score}")


def find_dominant_driver(row: pd.Series) -> str:
    """Return the pillar or tied pillars with the highest annual score."""
    pillar_values = row[list(PILLARS.keys())].dropna()
    if pillar_values.empty:
        return ""

    max_score = pillar_values.max()
    tied_pillars = [
        pillar_name
        for pillar_name, score in pillar_values.items()
        if score == max_score
    ]
    return ";".join(tied_pillars)


def build_policy_uncertainty_index(df: pd.DataFrame) -> pd.DataFrame:
    """Build the annual Policy Uncertainty Index from prepared policy events."""
    annual_index = calculate_pillar_scores(df)
    pillar_columns = list(PILLARS.keys())

    annual_index["policy_uncertainty_score"] = annual_index[pillar_columns].mean(
        axis=1, skipna=True
    )
    annual_index["interpretation"] = annual_index["policy_uncertainty_score"].apply(
        interpret_score
    )
    annual_index["dominant_uncertainty_driver"] = annual_index.apply(
        find_dominant_driver, axis=1
    )
    annual_index["notes"] = INDEX_NOTE

    output_columns = [
        "year",
        *pillar_columns,
        "policy_uncertainty_score",
        "interpretation",
        "dominant_uncertainty_driver",
        "notes",
    ]
    return annual_index[output_columns]


def save_policy_uncertainty_index(df: pd.DataFrame, path: Path) -> None:
    """Save the annual index to CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def print_console_summary(events: pd.DataFrame, annual_index: pd.DataFrame) -> None:
    """Print a concise console summary for quick QA."""
    year_min = int(events["year"].min())
    year_max = int(events["year"].max())
    highest_row = annual_index.loc[
        annual_index["policy_uncertainty_score"].idxmax()
    ]

    print("Policy Uncertainty Index summary")
    print(f"- Policy events used: {len(events)}")
    print(f"- Year range: {year_min}-{year_max}")
    print("- Annual policy uncertainty scores:")
    for _, row in annual_index.iterrows():
        print(f"  {int(row['year'])}: {row['policy_uncertainty_score']:.2f}")
    print(
        "- Highest uncertainty year: "
        f"{int(highest_row['year'])} "
        f"({highest_row['policy_uncertainty_score']:.2f})"
    )
    print("- Dominant driver by year:")
    for _, row in annual_index.iterrows():
        print(f"  {int(row['year'])}: {row['dominant_uncertainty_driver']}")


def main() -> None:
    raw_events = load_policy_timeline(INPUT_PATH)
    validate_required_columns(raw_events)
    prepared_events = prepare_policy_events(raw_events)
    annual_index = build_policy_uncertainty_index(prepared_events)
    save_policy_uncertainty_index(annual_index, OUTPUT_PATH)
    print_console_summary(prepared_events, annual_index)
    print("- Output saved to: output/policy_uncertainty_index.csv")


if __name__ == "__main__":
    main()
