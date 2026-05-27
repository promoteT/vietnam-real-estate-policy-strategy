"""
Create Charts

Purpose:
    Generate recruiter-friendly visuals for the Vietnam residential real estate
    policy uncertainty strategy project.

Inputs:
    data/policy_timeline.csv
    output/policy_uncertainty_index.csv
    output/scenario_matrix.csv
    output/developer_archetypes.csv

Outputs:
    PNG charts saved in output/charts/
"""

from pathlib import Path
from textwrap import fill

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "output"
CHART_DIR = OUTPUT_DIR / "charts"

POLICY_TIMELINE_PATH = DATA_DIR / "policy_timeline.csv"
POLICY_INDEX_PATH = OUTPUT_DIR / "policy_uncertainty_index.csv"
SCENARIO_MATRIX_PATH = OUTPUT_DIR / "scenario_matrix.csv"
DEVELOPER_ARCHETYPES_PATH = OUTPUT_DIR / "developer_archetypes.csv"

CHART_PATHS = {
    "policy_score": CHART_DIR / "01_policy_uncertainty_score.png",
    "pillar_scores": CHART_DIR / "02_uncertainty_pillars_by_year.png",
    "events_by_area": CHART_DIR / "03_policy_events_by_area.png",
    "direction_mix": CHART_DIR / "04_policy_direction_mix.png",
    "scenario_matrix": CHART_DIR / "05_scenario_strategy_matrix.png",
    "archetype_map": CHART_DIR / "06_developer_archetype_map.png",
    "posture_map": CHART_DIR / "07_company_posture_map.png",
}

POLICY_INDEX_COLUMNS = {
    "year",
    "legal_uncertainty_score",
    "credit_uncertainty_score",
    "demand_support_uncertainty_score",
    "infrastructure_execution_uncertainty_score",
    "policy_uncertainty_score",
    "interpretation",
}

POLICY_TIMELINE_COLUMNS = {"policy_area", "expected_direction"}

SCENARIO_COLUMNS = {
    "scenario_name",
    "developer_implication",
    "product_strategy",
    "capital_strategy",
    "launch_strategy",
    "risk_management",
}

ARCHETYPE_COLUMNS = {
    "company",
    "archetype",
    "policy_sensitivity",
    "capital_sensitivity",
    "legal_sensitivity",
    "demand_sensitivity",
    "recommended_posture",
    "scenario_a_implication",
    "scenario_b_implication",
    "scenario_c_implication",
}

PILLAR_COLUMNS = [
    "legal_uncertainty_score",
    "credit_uncertainty_score",
    "demand_support_uncertainty_score",
    "infrastructure_execution_uncertainty_score",
]

PILLAR_LABELS = {
    "legal_uncertainty_score": "Legal",
    "credit_uncertainty_score": "Credit",
    "demand_support_uncertainty_score": "Demand support",
    "infrastructure_execution_uncertainty_score": "Infrastructure",
}

COLORS = {
    "navy": "#243B53",
    "blue": "#2F80ED",
    "teal": "#1F9D8A",
    "gold": "#D89E2B",
    "red": "#C94C4C",
    "gray": "#6B7280",
    "light_gray": "#F3F4F6",
    "mid_gray": "#D1D5DB",
    "green": "#2E7D32",
}


def load_csv(path: Path) -> pd.DataFrame:
    """Load a required CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"Required input file not found: {path}")
    return pd.read_csv(path)


def validate_columns(df: pd.DataFrame, required_columns: set[str], file_name: str) -> None:
    """Validate required columns for each input."""
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"{file_name} is missing required columns: {sorted(missing)}")


def setup_chart_dir() -> None:
    """Create the chart output folder."""
    CHART_DIR.mkdir(parents=True, exist_ok=True)


def set_common_style() -> None:
    """Apply a professional, lightweight matplotlib style."""
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": COLORS["mid_gray"],
            "axes.labelcolor": COLORS["navy"],
            "axes.titlecolor": COLORS["navy"],
            "xtick.color": COLORS["gray"],
            "ytick.color": COLORS["gray"],
            "font.size": 10,
            "axes.titlesize": 14,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
        }
    )


def save_figure(fig: plt.Figure, path: Path) -> None:
    """Save and close a figure."""
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def wrap_value(value: object, width: int) -> str:
    """Wrap long table text while preserving blanks."""
    if pd.isna(value):
        return ""
    return fill(str(value), width=width)


def extract_posture(developer_implication: str) -> str:
    """Extract the scenario posture from the scenario implication sentence."""
    text = str(developer_implication)
    if "Offensive posture" in text:
        return "Offensive"
    if "Selective posture" in text:
        return "Selective"
    if "Defensive posture" in text:
        return "Defensive"
    return "Planning"


def plot_policy_uncertainty_score(index_df: pd.DataFrame) -> Path:
    """Chart 1: Annual policy uncertainty score."""
    df = index_df.copy()
    df["year"] = pd.to_numeric(df["year"])
    df["policy_uncertainty_score"] = pd.to_numeric(df["policy_uncertainty_score"])

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(
        df["year"],
        df["policy_uncertainty_score"],
        marker="o",
        linewidth=2.5,
        color=COLORS["blue"],
    )
    ax.fill_between(
        df["year"],
        df["policy_uncertainty_score"],
        1,
        color=COLORS["blue"],
        alpha=0.08,
    )

    for _, row in df.iterrows():
        label = wrap_value(row["interpretation"], 18)
        ax.annotate(
            label,
            (row["year"], row["policy_uncertainty_score"]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=8,
            color=COLORS["navy"],
        )

    ax.set_title("Vietnam Residential Real Estate Policy Uncertainty Score", pad=14)
    ax.set_xlabel("Year")
    ax.set_ylabel("Policy uncertainty score (1=Low, 5=High)")
    ax.set_ylim(1, 5.4)
    ax.set_xticks(df["year"])
    ax.grid(axis="y", color=COLORS["mid_gray"], alpha=0.5, linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    save_figure(fig, CHART_PATHS["policy_score"])
    return CHART_PATHS["policy_score"]


def plot_uncertainty_pillars(index_df: pd.DataFrame) -> Path:
    """Chart 2: Policy uncertainty pillar scores by year."""
    df = index_df.copy()
    df["year"] = pd.to_numeric(df["year"])
    for column in PILLAR_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    fig, ax = plt.subplots(figsize=(10, 5.5))
    palette = [COLORS["blue"], COLORS["red"], COLORS["teal"], COLORS["gold"]]

    for column, color in zip(PILLAR_COLUMNS, palette):
        ax.plot(
            df["year"],
            df[column],
            marker="o",
            linewidth=2,
            label=PILLAR_LABELS[column],
            color=color,
        )

    ax.set_title("Policy Uncertainty Pillar Scores by Year", pad=14)
    ax.set_xlabel("Year")
    ax.set_ylabel("Average uncertainty score")
    ax.set_ylim(1, 5.4)
    ax.set_xticks(df["year"])
    ax.grid(axis="y", color=COLORS["mid_gray"], alpha=0.5, linewidth=0.8)
    ax.legend(loc="upper right", frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    save_figure(fig, CHART_PATHS["pillar_scores"])
    return CHART_PATHS["pillar_scores"]


def plot_policy_events_by_area(policy_df: pd.DataFrame) -> Path:
    """Chart 3: Count of policy events by policy area."""
    counts = policy_df["policy_area"].value_counts().sort_values(ascending=True)

    fig_height = max(5, 0.42 * len(counts) + 1.5)
    fig, ax = plt.subplots(figsize=(10, fig_height))
    ax.barh(counts.index, counts.values, color=COLORS["teal"])

    for idx, value in enumerate(counts.values):
        ax.text(value + 0.1, idx, str(value), va="center", fontsize=9, color=COLORS["navy"])

    ax.set_title("Policy Events by Policy Area", pad=14)
    ax.set_xlabel("Number of policy events")
    ax.set_ylabel("")
    ax.set_xlim(0, max(counts.values) + 1.5)
    ax.grid(axis="x", color=COLORS["mid_gray"], alpha=0.5, linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    save_figure(fig, CHART_PATHS["events_by_area"])
    return CHART_PATHS["events_by_area"]


def plot_policy_direction_mix(policy_df: pd.DataFrame) -> Path:
    """Chart 4: Count of policy events by expected direction."""
    order = ["Unlock", "Drag", "Mixed", "Uncertain"]
    counts = policy_df["expected_direction"].value_counts().reindex(order, fill_value=0)
    color_map = {
        "Unlock": COLORS["green"],
        "Drag": COLORS["red"],
        "Mixed": COLORS["gold"],
        "Uncertain": COLORS["gray"],
    }

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(counts.index, counts.values, color=[color_map[item] for item in counts.index])

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.15,
            str(int(height)),
            ha="center",
            va="bottom",
            fontsize=10,
            color=COLORS["navy"],
        )

    ax.set_title("Policy Events by Expected Direction", pad=14)
    ax.set_xlabel("Expected direction")
    ax.set_ylabel("Number of policy events")
    ax.set_ylim(0, max(counts.values) + 2)
    ax.grid(axis="y", color=COLORS["mid_gray"], alpha=0.5, linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    save_figure(fig, CHART_PATHS["direction_mix"])
    return CHART_PATHS["direction_mix"]


def create_table_image(
    df: pd.DataFrame,
    title: str,
    output_path: Path,
    figsize: tuple[float, float],
    col_widths: list[float],
    font_size: int = 8,
    header_color: str = COLORS["navy"],
) -> Path:
    """Create a readable table-style PNG for text-heavy outputs."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")
    ax.set_title(title, fontsize=14, fontweight="bold", color=COLORS["navy"], pad=16)

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        colWidths=col_widths,
        cellLoc="left",
        bbox=[0.0, 0.02, 1.0, 0.86],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(font_size)
    table.scale(1, 2.25)

    for (row, _col), cell in table.get_celld().items():
        cell.set_edgecolor("white")
        if row == 0:
            cell.set_facecolor(header_color)
            cell.set_text_props(color="white", weight="bold")
        else:
            cell.set_facecolor(COLORS["light_gray"] if row % 2 == 0 else "white")
            cell.set_text_props(color=COLORS["navy"])

    save_figure(fig, output_path)
    return output_path


def plot_scenario_strategy_matrix(scenario_df: pd.DataFrame) -> Path:
    """Chart 5: Scenario strategy table."""
    table_df = pd.DataFrame(
        {
            "Scenario": scenario_df["scenario_name"].str.replace("Scenario ", "", regex=False),
            "Posture": scenario_df["developer_implication"].apply(extract_posture),
            "Product": scenario_df["product_strategy"].apply(lambda x: wrap_value(x, 34)),
            "Capital": scenario_df["capital_strategy"].apply(lambda x: wrap_value(x, 34)),
            "Launch": scenario_df["launch_strategy"].apply(lambda x: wrap_value(x, 34)),
            "Risk Mgmt": scenario_df["risk_management"].apply(lambda x: wrap_value(x, 34)),
        }
    )
    return create_table_image(
        table_df,
        "Scenario Strategy Matrix",
        CHART_PATHS["scenario_matrix"],
        figsize=(18, 4.8),
        col_widths=[0.13, 0.10, 0.19, 0.19, 0.19, 0.20],
        font_size=7,
    )


def sensitivity_to_score(value: str) -> int:
    """Map sensitivity labels to heatmap scores."""
    return {"Low": 1, "Medium": 2, "High": 3}.get(str(value), 0)


def plot_developer_archetype_map(archetypes_df: pd.DataFrame) -> Path:
    """Chart 6: Heatmap-like developer archetype sensitivity table."""
    cols = [
        "policy_sensitivity",
        "capital_sensitivity",
        "legal_sensitivity",
        "demand_sensitivity",
    ]
    labels = ["Policy", "Capital", "Legal", "Demand"]
    heat = archetypes_df[cols].map(sensitivity_to_score).to_numpy()

    fig, ax = plt.subplots(figsize=(12, 5.5))
    im = ax.imshow(heat, cmap="YlOrRd", vmin=1, vmax=3, aspect="auto")

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticks(range(len(archetypes_df)))
    ax.set_yticklabels(archetypes_df["company"])
    ax.set_title("Developer Archetype Sensitivity Map", pad=14)

    for i in range(len(archetypes_df)):
        for j, col in enumerate(cols):
            ax.text(
                j,
                i,
                archetypes_df.iloc[i][col],
                ha="center",
                va="center",
                fontsize=9,
                color=COLORS["navy"],
                weight="bold",
            )
        archetype_text = wrap_value(archetypes_df.iloc[i]["archetype"], 30)
        ax.text(
            len(labels) + 0.25,
            i,
            archetype_text,
            ha="left",
            va="center",
            fontsize=9,
            color=COLORS["navy"],
        )

    ax.text(
        len(labels) + 0.25,
        -0.75,
        "Archetype",
        ha="left",
        va="center",
        fontsize=10,
        color=COLORS["navy"],
        weight="bold",
    )
    ax.set_xlim(-0.5, len(labels) + 2.9)
    ax.tick_params(axis="both", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_ticks([1, 2, 3])
    cbar.set_ticklabels(["Low", "Medium", "High"])
    cbar.outline.set_visible(False)

    save_figure(fig, CHART_PATHS["archetype_map"])
    return CHART_PATHS["archetype_map"]


def plot_company_posture_map(archetypes_df: pd.DataFrame) -> Path:
    """Chart 7: Company posture and scenario implication table."""
    table_df = pd.DataFrame(
        {
            "Company": archetypes_df["company"],
            "Posture": archetypes_df["recommended_posture"],
            "Scenario A": archetypes_df["scenario_a_implication"].apply(
                lambda x: wrap_value(x, 36)
            ),
            "Scenario B": archetypes_df["scenario_b_implication"].apply(
                lambda x: wrap_value(x, 36)
            ),
            "Scenario C": archetypes_df["scenario_c_implication"].apply(
                lambda x: wrap_value(x, 36)
            ),
        }
    )
    return create_table_image(
        table_df,
        "Company Recommended Posture Map",
        CHART_PATHS["posture_map"],
        figsize=(18, 6.8),
        col_widths=[0.10, 0.12, 0.26, 0.26, 0.26],
        font_size=7,
    )


def generate_charts() -> list[Path]:
    """Load data, validate inputs, and generate all required charts."""
    setup_chart_dir()
    set_common_style()

    policy_df = load_csv(POLICY_TIMELINE_PATH)
    index_df = load_csv(POLICY_INDEX_PATH)
    scenario_df = load_csv(SCENARIO_MATRIX_PATH)
    archetypes_df = load_csv(DEVELOPER_ARCHETYPES_PATH)

    validate_columns(policy_df, POLICY_TIMELINE_COLUMNS, "policy_timeline.csv")
    validate_columns(index_df, POLICY_INDEX_COLUMNS, "policy_uncertainty_index.csv")
    validate_columns(scenario_df, SCENARIO_COLUMNS, "scenario_matrix.csv")
    validate_columns(archetypes_df, ARCHETYPE_COLUMNS, "developer_archetypes.csv")

    generated = [
        plot_policy_uncertainty_score(index_df),
        plot_uncertainty_pillars(index_df),
        plot_policy_events_by_area(policy_df),
        plot_policy_direction_mix(policy_df),
        plot_scenario_strategy_matrix(scenario_df),
        plot_developer_archetype_map(archetypes_df),
        plot_company_posture_map(archetypes_df),
    ]
    return generated


def main() -> None:
    generated = generate_charts()
    print("Generated chart files:")
    for path in generated:
        print(f"- output/charts/{path.name}")


if __name__ == "__main__":
    main()
