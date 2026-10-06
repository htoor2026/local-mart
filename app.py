from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from textwrap import dedent

def render_html(content):
    st.html(
        dedent(content).strip()
    )


# ============================================================
# PATHS
# ============================================================

from pathlib import Path

ROOT = Path(__file__).resolve().parent

RESULTS_DIR = (
    ROOT
    / "notebooks"
    / "results"
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LocalMart AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# PATHS
# ============================================================

from pathlib import Path

PROJECT_ROOT = Path(
    "/Users/toor/Desktop/M5/retail-promotion-intelligence"
)

KEY_FILE = (
    "semisynthetic_demand_model_results_v1.csv"
)


def find_results_dir():

    matches = list(
        PROJECT_ROOT.rglob(KEY_FILE)
    )

    if len(matches) == 0:
        raise FileNotFoundError(
            f"Could not find {KEY_FILE}"
        )

    # The folder containing the actual final results
    return matches[0].parent


RESULTS_DIR = find_results_dir()

st.write(
    "Results folder:",
    RESULTS_DIR
)


# ============================================================
# CUSTOM UI
# ============================================================

st.html(
    """
    <style>

    .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    .hero {
        padding: 2.4rem;
        border-radius: 24px;
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #172554 55%,
            #115e59 100%
        );
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero-small {
        font-size: 0.8rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        opacity: 0.7;
        font-weight: 700;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-top: 0.5rem;
    }

    .hero-text {
        font-size: 1.05rem;
        max-width: 900px;
        opacity: 0.9;
        line-height: 1.65;
        margin-top: 0.7rem;
    }

    .metric-box {
        border: 1px solid #e2e8f0;
        background: white;
        padding: 1.2rem;
        border-radius: 18px;
        min-height: 130px;
    }

    .metric-label {
        color: #64748b;
        font-size: 0.78rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.05em;
    }

    .metric-value {
        color: #0f172a;
        font-size: 2rem;
        font-weight: 800;
        margin-top: 0.4rem;
    }

    .metric-note {
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 0.2rem;
    }

    .business-card {
        padding: 1.3rem;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        background: white;
        min-height: 180px;
    }

    .business-card h3 {
        margin-top: 0;
        font-size: 1.1rem;
    }

    .business-card p {
        color: #475569;
        line-height: 1.55;
    }

    .callout {
        padding: 1.1rem 1.3rem;
        border-radius: 15px;
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        color: #065f46;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .warning {
        padding: 1.1rem 1.3rem;
        border-radius: 15px;
        background: #fffbeb;
        border: 1px solid #fde68a;
        color: #78350f;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    div[data-baseweb="tab-list"] {
        gap: 8px;
    }

    button[data-baseweb="tab"] {
        font-size: 1rem;
        font-weight: 700;
        padding-left: 20px;
        padding-right: 20px;
    }

    footer {
        visibility: hidden;
    }
    .tech-flow {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 14px;
    margin-top: 18px;
    margin-bottom: 32px;
}

    .tech-step {
        position: relative;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 22px 18px;
        background: white;
        min-height: 190px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
    }

    .tech-number {
        display: inline-flex;
        width: 34px;
        height: 34px;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        background: #eef2ff;
        color: #3730a3;
        font-weight: 800;
        margin-bottom: 16px;
    }
    
    .tech-step h3 {
        font-size: 1.05rem;
        margin: 0 0 10px 0;
        color: #0f172a;
    }

    .tech-step p {
        font-size: 0.90rem;
        line-height: 1.55;
        color: #64748b;
        margin: 0;
    }

    .tech-method {
        display: inline-block;
        margin-top: 15px;
        padding: 5px 9px;
        border-radius: 8px;
        background: #f1f5f9;
        color: #475569;
        font-size: 0.76rem;
        font-weight: 700;
    }

    @media (max-width: 1100px) {
    .tech-flow {
        grid-template-columns: repeat(2, 1fr);
    }
}
    </style>
    """
)


# ============================================================
# HELPERS
# ============================================================




@st.cache_data
def load_csv(filename):

    path = RESULTS_DIR / filename

    if not path.exists():
        st.warning(
            f"File not found: {path}"
        )
        return None

    return pd.read_csv(path)


@st.cache_data
def load_parquet(filename):

    path = RESULTS_DIR / filename

    if not path.exists():
        st.warning(
            f"File not found: {path}"
        )
        return None

    return pd.read_parquet(path)

def money(value):
    return f"${value:,.0f}"


def metric_box(label, value, note=""):

    render_html(
        f"""
        <div class="metric-box">
            <div class="metric-label">
                {label}
            </div>

            <div class="metric-value">
                {value}
            </div>

            <div class="metric-note">
                {note}
            </div>
        </div>
        """
    )
def render_html(content):
    st.html(
        dedent(content).strip()
    )

# ============================================================
# LOAD FINAL PROJECT RESULTS
# ============================================================

demand_results = load_csv(
    "semisynthetic_demand_model_results_v1.csv"
)

uplift = load_parquet(
    "promotion_uplift_tlearner_v1.parquet"
)

optimized = load_parquet(
    "profit_optimized_promotions_v2.parquet"
)

strategy = load_csv(
    "promotion_strategy_comparison_v2.csv"
)

final_metrics = load_csv(
    "final_long_version_metrics.csv"
)

store_results = load_csv(
    "final_store_results.csv"
)

category_results = load_csv(
    "final_category_results.csv"
)


# ============================================================
# CHECK FILES
# ============================================================

required_files = {
    "Demand results": demand_results,
    "Uplift predictions": uplift,
    "Optimized promotions": optimized,
    "Strategy comparison": strategy,
}

missing = [
    name
    for name, df in required_files.items()
    if df is None
]

if missing:

    st.error(
        "Missing files: "
        + ", ".join(missing)
    )

    st.stop()


# ============================================================
# DATES
# ============================================================

uplift["week_start"] = pd.to_datetime(
    uplift["week_start"]
)

optimized["week_start"] = pd.to_datetime(
    optimized["week_start"]
)


# ============================================================
# HERO
# ============================================================
render_html(
    """
    <div class="hero">
        <div class="hero-small">
            Retail Promotion Intelligence
        </div>

        <div class="hero-title">
            LocalMart AI
        </div>

        <div class="hero-text">
            A geo-aware retail decision system that combines
            local market context, weather, demand prediction,
            promotion uplift and product economics to decide
            which products each GTA store should promote.
        </div>
    </div>
    """
)

# ============================================================
# MAIN TABS
# ============================================================

business_tab, technical_tab = st.tabs(
    [
        "Business View",
        "Technical Build",
    ]
)


# ============================================================
# BUSINESS VIEW
# ============================================================

with business_tab:

    st.header(
        "What should the business do?"
    )

    st.caption(
        "A non-technical view focused on decisions, "
        "profit and store-level recommendations."
    )

    # --------------------------------------------------------
    # BUSINESS MESSAGE CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        render_html(
            """
            <div class="business-card">
            <h3>Promote for profit</h3>

            <p>
                The biggest discount or highest sales uplift
                is not necessarily the best promotion.
                The system selects products based on
                incremental profit.
            </p>
            </div>
            """
    )

    with col2:

        render_html(
        """
            <div class="business-card">
            <h3>Localize each store</h3>

            <p>
                Store recommendations can vary because nearby
                population, commercial activity, weather and
                category response differ across GTA locations.
            </p>
            </div>
        """
    )

    with col3:

       render_html(
        """
            <div class="business-card">
                <h3>Respect business constraints</h3>

            <p>
                Recommendations must fit flyer space,
                category limits, inventory availability
                and the promotion budget.
            </p>
            </div>
        """
    )

    # --------------------------------------------------------
    # OVERALL BUSINESS RESULTS
    # --------------------------------------------------------

    st.subheader(
        "Business impact"
    )

    strategy_index = strategy.set_index(
        "strategy"
    )

    optimizer_profit = float(
        strategy_index.loc[
            "Profit Optimizer",
            "true_incremental_profit",
        ]
    )

    oracle_profit = float(
        strategy_index.loc[
            "Oracle",
            "true_incremental_profit",
        ]
    )

    discount_profit = float(
        strategy_index.loc[
            "Largest Discount",
            "true_incremental_profit",
        ]
    )

    positive_rate = float(
        strategy_index.loc[
            "Profit Optimizer",
            "positive_profit_rate_pct",
        ]
    )

    regret = (
        (
            oracle_profit
            - optimizer_profit
        )
        / oracle_profit
        * 100
    )


    c1, c2, c3, c4 = st.columns(4)

    with c1:

        metric_box(
            "Profit Optimizer",
            money(optimizer_profit),
            "Incremental profit in simulation",
        )

    with c2:

        metric_box(
            "Gain vs Largest Discount",
            money(
                optimizer_profit
                - discount_profit
            ),
            "Absolute profit improvement",
        )

    with c3:

        metric_box(
            "Profitable Selections",
            f"{positive_rate:.1f}%",
            "Selected promotions with positive profit",
        )

    with c4:

        metric_box(
            "Oracle Regret",
            f"{regret:.1f}%",
            "Gap from perfect information",
        )


    render_html(
        """
        <div class="callout">
            <b>Main business finding:</b><br><br>

            Highest sales uplift does not necessarily mean highest profit.<br><br>

            Deep discounts can increase units while destroying margin.<br><br>

            The optimizer combines predicted promotion response
            with product economics before making the final decision.
        </div>
         """
        )


    # ========================================================
    # STORE RECOMMENDATIONS
    # ========================================================

    st.subheader(
        "Store promotion recommendations"
    )


    stores = (
        optimized[
            [
                "store_id",
                "store_name",
            ]
        ]
        .drop_duplicates()
        .sort_values(
            "store_name"
        )
    )


    selected_store = st.selectbox(
        "Choose a GTA store",
        stores["store_name"].tolist(),
    )


    selected_store_id = (
        stores.loc[
            stores["store_name"]
            == selected_store,
            "store_id",
        ]
        .iloc[0]
    )


    store_data = optimized[
        optimized["store_id"].astype(str)
        == str(selected_store_id)
    ].copy()


    weeks = sorted(
        store_data[
            "week_start"
        ].unique(),
        reverse=True,
    )


    selected_week = st.selectbox(
        "Choose week",
        weeks,
        format_func=lambda x:
        pd.Timestamp(x).strftime(
            "%B %d, %Y"
        ),
    )


    selected = store_data[
        store_data["week_start"]
        == pd.Timestamp(
            selected_week
        )
    ].copy()


    if "optimized_rank" in selected.columns:

        selected = selected.sort_values(
            "optimized_rank"
        )

    else:

        selected = selected.sort_values(
            "pred_incremental_profit",
            ascending=False,
        )


    # --------------------------------------------------------
    # STORE METRICS
    # --------------------------------------------------------

s1, s2, s3, s4 = st.columns(4)

with s1:
    metric_box(
        "Selected Products",
        len(selected),
        "Maximum flyer slots = 20",
    )

with s2:
    metric_box(
        "Predicted Profit",
        money(
            selected[
                "pred_incremental_profit"
            ].sum()
        ),
        "Incremental profit",
    )

with s3:
    metric_box(
        "Promotion Spend",
        money(
            selected[
                "promo_spend_proxy"
            ].sum()
        ),
        "Maximum budget = $300",
    )

with s4:

    avg_uplift = selected[
        "predicted_uplift_units"
    ].mean()

    metric_box(
        "Average Uplift",
        f"{avg_uplift:.1f} units",
        "Predicted incremental units",
    )


# IMPORTANT:
# EVERYTHING FROM HERE MUST HAVE NO `with s4:` INDENTATION

st.subheader(
    "Recommended flyer"
)

def explain_product(row):

    reasons = []

    if row["predicted_uplift_units"] >= 5:
        reasons.append(
            "strong expected sales lift"
        )

    elif row["predicted_uplift_units"] >= 3:
        reasons.append(
            "solid expected sales lift"
        )

    if row["pred_incremental_profit"] >= 10:
        reasons.append(
            "high incremental profit"
        )

    if (
        "vendor_funding_rate" in row.index
        and row["vendor_funding_rate"] >= 0.7
    ):
        reasons.append(
            "strong vendor funding"
        )

    if not reasons:
        reasons.append(
            "best available profit opportunity"
        )

    return (
        ", ".join(reasons).capitalize()
        + "."
    )


selected[
    "Why selected"
] = selected.apply(
    explain_product,
    axis=1,
)


columns = []

if "optimized_rank" in selected.columns:
    columns.append(
        "optimized_rank"
    )


columns += [
    "product_name",
    "category",
    "standard_discount_pct",
    "predicted_uplift_units",
    "pred_incremental_profit",
    "promo_spend_proxy",
    "Why selected",
]


recommendations = (
    selected[columns]
    .rename(
        columns={
            "optimized_rank": "Rank",
            "product_name": "Product",
            "category": "Category",
            "standard_discount_pct": "Discount %",
            "predicted_uplift_units": "Predicted Uplift",
            "pred_incremental_profit": "Predicted Profit",
            "promo_spend_proxy": "Promo Spend",
        }
    )
)


st.dataframe(
    recommendations,
    use_container_width=True,
    hide_index=True,
    column_config={

        "Discount %":
            st.column_config.NumberColumn(
                format="%.0f%%"
            ),

        "Predicted Uplift":
            st.column_config.NumberColumn(
                format="%.2f"
            ),

        "Predicted Profit":
            st.column_config.NumberColumn(
                format="$%.2f"
            ),

        "Promo Spend":
            st.column_config.NumberColumn(
                format="$%.2f"
            ),
    },
)

    # ========================================================
    # STRATEGY COMPARISON
    # ========================================================

chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    st.subheader(
        "Profit by store"
    )

    plot_store = (
        store_results
        .sort_values(
            "true_incremental_profit"
        )
    )

    fig = px.bar(
        plot_store,
        x="true_incremental_profit",
        y="store_name",
        orientation="h",
    )

    fig.update_layout(
        height=550
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


with chart_col2:

    st.subheader(
        "Profit by category"
    )

    category_plot = (
        category_results
        .sort_values(
            "true_profit"
        )
    )

    fig = px.bar(
        category_plot,
        x="true_profit",
        y="category",
        orientation="h",
    )

    fig.update_layout(
        height=550
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# TECHNICAL VIEW
# ============================================================

with technical_tab:

    st.header(
        "Technical Build"
    )

    st.markdown(
        """
        From raw geographic and retail context to a
        constrained promotion decision system.
        """
    )

    render_html(
        """
        <div class="callout">
            <b>Project design</b><br><br>
    
            Real GTA geography, demographics, OpenStreetMap context
            and weather are combined with a controlled semi-synthetic
            retail environment.
    
            This allows the system to evaluate demand prediction,
            heterogeneous promotion effects and profit optimization
            against known ground truth.
        </div>
        """
    )


    # ========================================================
    # ARCHITECTURE
    # ========================================================

    st.subheader(
    "System architecture"
    )

    st.subheader(
    "System architecture"
    )

    st.caption(
    "How raw context becomes a store-level promotion decision."
    )

    render_html(
        """
        <div class="tech-flow">

            <div class="tech-step">
                <div class="tech-number">1</div>

               <h3>Local Context</h3>

                <p>
                    Build a 5 km view around each GTA store using
                    demographics, nearby commercial activity and
                    historical weather.
                </p>

                <span class="tech-method">
                    StatsCan · OSM · ECCC
                </span>
            </div>


            <div class="tech-step">
                <div class="tech-number">2</div>

                <h3>Demand Prediction</h3>

                <p>
                    Estimate expected weekly product demand using
                    historical demand, price, inventory, promotions,
                    weather and store context.
                </p>

                <span class="tech-method">
                    CatBoost
                </span>
            </div>


            <div class="tech-step">
                <div class="tech-number">3</div>

                <h3>Promotion Uplift</h3>

                <p>
                    Estimate how many additional units are caused
                    by promoting a product instead of leaving it
                    under normal conditions.
                </p>

                <span class="tech-method">
                    T-Learner · CATE
                </span>
            </div>


            <div class="tech-step">
                <div class="tech-number">4</div>

             <h3>Profit Economics</h3>

                <p>
                    Translate incremental units into incremental
                    profit using margin, discount depth, vendor
                    funding and inventory constraints.
                </p>

                <span class="tech-method">
                    Unit Economics
                </span>
            </div>


            <div class="tech-step">
                <div class="tech-number">5</div>

                <h3>Optimization</h3>

                <p>
                    Select the most profitable feasible flyer
                    while respecting budget, category and
                    flyer-space constraints.
                </p>

                <span class="tech-method">
                    PuLP · Integer Programming
                </span>
            </div>

        </div>
        """
    )
    # ========================================================
    # DATA SOURCES
    # ========================================================

    st.subheader(
        "Data sources"
    )


    data_sources = pd.DataFrame(
        [

            [
                "GTA Walmart stores",
                "Real",
                "Store geography",
            ],

            [
                "OpenStreetMap",
                "Real",
                "5 km local context",
            ],

            [
                "Statistics Canada",
                "Real",
                "Population and demographics",
            ],

            [
                "ECCC Weather",
                "Real",
                "Historical weather",
            ],

            [
                "300 products",
                "Synthetic",
                "Retail product catalog",
            ],

            [
                "Sales history",
                "Synthetic",
                "Demand outcomes",
            ],

            [
                "Promotion treatment",
                "Synthetic",
                "Known causal effect",
            ],

            [
                "Margins / inventory",
                "Synthetic",
                "Profit simulation",
            ],
        ],

        columns=[
            "Component",
            "Origin",
            "Purpose",
        ],
    )


    st.dataframe(
        data_sources,
        use_container_width=True,
        hide_index=True,
    )


    # ========================================================
    # DEMAND MODEL
    # ========================================================

    st.subheader(
        "1. Demand forecasting"
    )


    st.dataframe(
        demand_results,
        use_container_width=True,
        hide_index=True,
    )


    baseline = demand_results[
        (
            demand_results["split"]
            == "validation"
        )
        &
        (
            demand_results["model"]
            == "Lag-1 Baseline"
        )
    ].iloc[0]


    catboost_validation = demand_results[
        (
            demand_results["split"]
            == "validation"
        )
        &
        (
            demand_results["model"]
            == "CatBoost"
        )
    ].iloc[0]


    catboost_test = demand_results[
        (
            demand_results["split"]
            == "test"
        )
        &
        (
            demand_results["model"]
            == "CatBoost"
        )
    ].iloc[0]


    improvement = (
        (
            baseline["MAE"]
            -
            catboost_validation["MAE"]
        )
        /
        baseline["MAE"]
        *
        100
    )


    d1, d2, d3 = st.columns(3)


    with d1:

        metric_box(
            "MAE Improvement",
            f"{improvement:.1f}%",
            "CatBoost vs Lag-1",
        )


    with d2:

        metric_box(
            "Test MAE",
            f"{catboost_test['MAE']:.2f}",
            "Units",
        )


    with d3:

        metric_box(
            "Test WMAPE",
            f"{catboost_test['WMAPE_pct']:.1f}%",
            "Forecast error",
        )


    st.markdown(
        """
        **Why CatBoost?**

        The dataset contains:

        - product IDs
        - store IDs
        - categories
        - lagged demand
        - rolling demand
        - inventory
        - prices
        - promotions
        - weather
        - demographics
        - local commercial context

        CatBoost works well with mixed numerical and
        categorical features and nonlinear interactions.
        """
    )


    # ========================================================
    # UPLIFT MODEL
    # ========================================================

    st.subheader(
        "2. Promotion uplift modeling"
    )


    true_uplift = (
        uplift[
            "true_incremental_units"
        ]
        .to_numpy()
    )


    predicted_uplift = (
        uplift[
            "predicted_uplift_units"
        ]
        .to_numpy()
    )


    uplift_mae = np.mean(
        np.abs(
            true_uplift
            -
            predicted_uplift
        )
    )


    uplift_rmse = np.sqrt(
        np.mean(
            (
                true_uplift
                -
                predicted_uplift
            ) ** 2
        )
    )


    uplift_corr = np.corrcoef(
        true_uplift,
        predicted_uplift,
    )[0, 1]


    ranked = uplift.sort_values(
        "predicted_uplift_units",
        ascending=False,
    )


    top_10 = ranked.head(
        int(
            len(ranked)
            * 0.10
        )
    )


    top_10_true = (
        top_10[
            "true_incremental_units"
        ]
        .mean()
    )


    overall_true = (
        uplift[
            "true_incremental_units"
        ]
        .mean()
    )


    enrichment = (
        top_10_true
        /
        overall_true
    )


    u1, u2, u3, u4 = st.columns(4)


    with u1:

        metric_box(
            "Uplift MAE",
            f"{uplift_mae:.2f}",
            "Incremental units",
        )


    with u2:

        metric_box(
            "Correlation",
            f"{uplift_corr:.3f}",
            "Predicted vs true uplift",
        )


    with u3:

        metric_box(
            "Top 10% Uplift",
            f"{top_10_true:.2f}",
            "True incremental units",
        )


    with u4:

        metric_box(
            "Top-10 Enrichment",
            f"{enrichment:.2f}x",
            "Compared with average",
        )


    st.markdown(
        """
        ### Why a T-Learner?

        Two separate models are trained:

        **Control model**

        predicts sales if the product is not promoted.

        **Treatment model**

        predicts sales if the product is promoted.

        The difference is:

        ```text
        Predicted Treatment Sales
        -
        Predicted Control Sales
        =
        Predicted Promotion Uplift
        ```
        """
    )


    sample = uplift.sample(
        min(
            1500,
            len(uplift)
        ),
        random_state=42,
    )


    fig = px.scatter(
        sample,
        x="true_incremental_units",
        y="predicted_uplift_units",
        opacity=0.35,

        # Force normal SVG rendering
        # instead of browser WebGL
        render_mode="svg",

        labels={
            "true_incremental_units":
                "True Incremental Units",

            "predicted_uplift_units":
                "Predicted Incremental Units",
        },
    )


    fig.update_traces(
        marker=dict(
            size=6
        )
    )


    fig.update_layout(
        height=450,
        title="Predicted vs True Promotion Uplift",
        xaxis_title="True Incremental Units",
        yaxis_title="Predicted Incremental Units",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )


    st.plotly_chart(
        fig,
        use_container_width=True,
    )
    # ========================================================
    # PROFIT LAYER
    # ========================================================

    st.subheader(
        "3. Profit-aware decision layer"
    )


    p1, p2 = st.columns(2)


    with p1:

        st.markdown(
            """
            ### Control profit

            ```text
            predicted control units
            ×
            regular unit margin
            ```
            """
        )


    with p2:

        st.markdown(
            """
            ### Promotion profit

            ```text
            predicted promoted units
            ×
            promoted unit margin
            ```
            """
        )


    st.markdown(
        """
        Therefore:

        ```text
        Promotion Profit
        -
        Control Profit
        =
        Predicted Incremental Profit
        ```

        This is why the system does **not**
        simply select products with the highest uplift.
        """
    )


    # ========================================================
    # OPTIMIZER
    # ========================================================

    st.subheader(
        "4. Promotion optimization"
    )


    o1, o2, o3, o4 = st.columns(4)


    with o1:

        metric_box(
            "Flyer Slots",
            "≤ 20",
            "Per store/week",
        )


    with o2:

        metric_box(
            "Per Category",
            "≤ 4",
            "Maintains variety",
        )


    with o3:

        metric_box(
            "Promo Budget",
            "≤ $300",
            "Per store/week",
        )


    with o4:

        metric_box(
            "Inventory",
            "Capped",
            "Cannot sell unavailable units",
        )


    st.markdown(
        """
        The project uses **integer programming with PuLP**.

        Objective:

        ```text
        Maximize:

        Σ Predicted Incremental Profit × Product Selected
        ```

        subject to flyer, category, budget and
        inventory constraints.
        """
    )


    # ========================================================
    # STRATEGY EVALUATION
    # ========================================================

    st.subheader(
        "5. Strategy evaluation"
    )


    st.dataframe(
        strategy,
        use_container_width=True,
        hide_index=True,
    )


    fig = px.bar(
        strategy.sort_values(
            "true_incremental_profit"
        ),
        x="true_incremental_profit",
        y="strategy",
        orientation="h",
        text_auto=".3s",
        labels={

            "true_incremental_profit":
                "True Incremental Profit",

            "strategy":
                "",
        },
    )


    fig.update_layout(
        height=400
    )


    st.plotly_chart(
        fig,
        use_container_width=True,
    )


    st.markdown(
        """
        ### Result

        **Largest Discount**

        lost money because deep discounting ignored margins.

        **Highest Predicted Uplift**

        also lost money because high incremental units
        do not guarantee high incremental profit.

        **Profit Optimizer**

        produced positive incremental profit while
        satisfying all business constraints.

        **Oracle**

        represents the upper bound using hidden
        ground-truth information and is only used
        for evaluation.
        """
    )


    # ========================================================
    # WHY THIS DESIGN
    # ========================================================

    st.subheader(
        "6. Why each component exists"
    )


    design_table = pd.DataFrame(
        [

            [
                "Demand forecasting",
                "Estimate future product demand",
                "CatBoost",
            ],

            [
                "Promotion uplift",
                "Estimate causal incremental units",
                "T-Learner",
            ],

            [
                "Profit model",
                "Convert model predictions into business value",
                "Unit economics",
            ],

            [
                "Optimization",
                "Choose a feasible set of products",
                "Integer programming",
            ],

            [
                "Semi-synthetic outcomes",
                "Create known causal ground truth",
                "Controlled simulation",
            ],
        ],

        columns=[
            "Layer",
            "Purpose",
            "Method",
        ],
    )


    st.dataframe(
        design_table,
        use_container_width=True,
        hide_index=True,
    )


    # ========================================================
    # LIMITATIONS
    # ========================================================

    st.subheader(
        "7. Limitations"
    )


    st.markdown(
        """
        - Walmart Canada product-level sales outcomes were not publicly available.
        - Sales, margins, inventory and treatment effects are therefore semi-synthetic.
        - The profit values are evaluation results, not actual Walmart profits.
        - Pearson weather is used as a GTA-wide weather proxy.
        - The T-Learner is a strong baseline, but future work could compare:
          - X-Learner
          - doubly robust estimation
          - causal forests
        - A real production system would require live:
          - POS sales
          - inventory
          - pricing
          - promotion history
          - vendor funding
          - experiment outcomes
        """
    )


    # ========================================================
    # PRODUCTION
    # ========================================================

    st.subheader(
        "8. Production extension"
    )


    st.code(
        """
Live Retail Data
        ↓
Feature Pipeline
        ↓
Demand Model
        ↓
Uplift Model
        ↓
Profit Engine
        ↓
Optimization Service
        ↓
Streamlit Decision Dashboard
        ↓
Monitoring
        ↓
Retraining
        """,
        language="text",
    )