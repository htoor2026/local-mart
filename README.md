# LocalMart AI — Geo-Aware Retail Promotion Intelligence

An end-to-end retail analytics system that combines demand forecasting, geographic context, demographics, weather, and promotion data to rank and optimize product promotions for individual retail locations.

The project explores the question:

> **How can a retailer choose which products to promote at each store by combining historical demand patterns with local neighborhood characteristics, weather, pricing, and promotion context?**

---

## Project Overview

Traditional retail promotions are often applied broadly across many stores.

However, stores operate in different environments:

* different population densities
* different household incomes
* different commercial activity
* different nearby universities, offices, and industrial areas
* different weather conditions
* different product and discount opportunities

LocalMart AI builds a pipeline for creating **store-specific promotion recommendations** instead of using one generic flyer strategy everywhere.

The system contains two intentionally separate analytical layers:

### 1. Demand Forecasting Benchmark

Historical M5 retail sales data is used to evaluate demand-forecasting models.

Models tested:

* CatBoost
* LightGBM
* XGBoost
* Lag-1 baseline
* Lag-7 baseline
* 28-day rolling-mean baseline

### 2. GTA Promotion Intelligence

A separate localization layer uses real Greater Toronto Area context:

* GTA Walmart locations
* Statistics Canada demographics
* OpenStreetMap points of interest
* Environment Canada weather
* Walmart Canada flyer promotions

These sources are combined to rank promotion opportunities by store.

> The M5 stores are located in California, Texas, and Wisconsin. GTA demographics and weather are therefore **not joined directly to M5 sales**. The forecasting benchmark and Canadian localization system are kept scientifically separate.

---

# System Architecture

```text
                    ┌─────────────────────────┐
                    │     M5 Retail Sales     │
                    └────────────┬────────────┘
                                 │
                         Feature Engineering
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
             CatBoost         LightGBM         XGBoost
                │                │                │
                └──────────── Model Comparison ──┘


                    GTA LOCALIZATION LAYER

                    Walmart GTA Stores
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
    OpenStreetMap      StatsCan          Weather
    POIs / Land Use   Demographics        ECCC
          │                │                 │
          └────────────────┼─────────────────┘
                           │
                  Walmart Flyer Data
                           │
                           ▼
             Integrated Promotion Context
                           │
                           ▼
              Promotion Opportunity Score
                           │
                           ▼
                 Profit-Aware Scoring
                           │
                           ▼
              Constrained Flyer Optimizer
                           │
                           ▼
             Store-Specific Recommendations
```

---

# Data Sources

## M5 Forecasting Data

The M5 forecasting dataset provides:

* daily unit sales
* product hierarchy
* store hierarchy
* selling prices
* calendar features
* events
* SNAP indicators

The processed dataset contains approximately **59 million store-item-day observations**.

Large historical tables are stored as partitioned Parquet rather than MongoDB.

---

## GTA Walmart Locations

A GTA store master was created containing approximately 15 Walmart locations across:

* Toronto
* Brampton
* Mississauga
* Etobicoke

Store attributes include:

```text
store_id
store_name
address
city
latitude
longitude
```

Coordinates are used for geographic feature engineering.

---

## OpenStreetMap

A 5 km geographic context was created around each Walmart store.

Example features:

```text
universities
colleges
schools
offices
industrial areas
commercial areas
retail land use
rail stations
```

These features describe the commercial and institutional environment surrounding each store.

---

## Statistics Canada

The original Census Profile dataset was approximately **2.37 GB** with more than 10 million rows.

Instead of repeatedly loading the full dataset, DuckDB was used to filter it to only the census tracts intersecting Walmart 5 km catchments.

The resulting subset contained:

```text
605 relevant census tracts
242 candidate demographic characteristics
146,410 filtered rows
```

Demographic features were then aggregated to the store level using geographic overlap and population-based weighting.

Examples include:

```text
population_5km
population_density_5km
median_household_income_5km
average_household_size_5km
employment_rate_5km
```

---

## Weather

Historical daily weather was collected from Environment and Climate Change Canada.

The first MVP uses Toronto Pearson as a GTA-wide weather proxy.

Features include:

```text
mean_temperature
min_temperature
max_temperature
total_rain
total_snow
total_precipitation
rain_day
snow_day
```

A future version can assign each Walmart to its nearest weather station.

---

## Walmart Canada Promotions

Public Walmart Canada flyer pages are collected through a lightweight ingestion pipeline.

The pipeline:

```text
Walmart public flyer
        ↓
HTTP request
        ↓
HTML snapshot
        ↓
BeautifulSoup parsing
        ↓
structured promotion records
        ↓
MongoDB + Parquet
```

Collected fields include:

```text
product_id
product_name
current_price
regular_price
promotion_type
discount_amount
discount_pct
snapshot_date
```

Raw HTML snapshots are retained for reproducibility.

The current MVP contains **7 unique flyer products**.

This small sample is intentionally treated as a **pipeline-validation dataset**, not as a production-scale promotion catalogue.

---

# Data Architecture

Different storage systems are used according to workload.

## Parquet

Used for large analytical datasets:

* M5 sales
* engineered features
* StatsCan demographics
* weather
* integrated modeling tables
* rankings

## DuckDB

Used for:

* large CSV filtering
* efficient analytical queries
* processing the 2.37 GB StatsCan Census Profile dataset

## MongoDB

Used for operational and semi-structured data:

* calendar metadata
* price records
* flyer snapshots
* normalized promotions
* future prediction logs
* future monitoring events

---

# Feature Engineering

Demand forecasting features include:

```text
lag_1
lag_7
lag_28
rolling_mean_7
rolling_mean_28
sell_price
weekday
month
year
event information
SNAP indicators
```

Rolling statistics use only preceding observations to prevent target leakage.

---

# Forecasting Results

Evaluation used a time-based holdout rather than a random train/test split.

| Model           |        MAE |       RMSE |
| --------------- | ---------: | ---------: |
| CatBoost        | **1.0385** | **2.0128** |
| LightGBM        |     1.0413 |     2.0212 |
| XGBoost         |     1.0395 |     2.0226 |
| Rolling Mean 28 |     1.0876 |     2.1934 |
| Lag 1           |     1.2817 |     2.7682 |
| Lag 7           |     1.3097 |     2.8066 |

CatBoost produced the best result on the current split, although the three boosting models performed very similarly.

This suggests that **feature engineering contributed more to performance than the choice between modern tree-boosting libraries**.

No claim is made that CatBoost is universally superior without repeated rolling-window validation.

---

# GTA Promotion Context

The localization pipeline combines:

```text
Store
+ neighborhood POIs
+ demographics
+ flyer product
+ discount
+ weather
+ calendar context
```

The resulting modeling unit is approximately:

```text
store × product × flyer snapshot
```

For the current MVP:

```text
15 stores
×
7 flyer products
=
105 store-product context rows
```

---

# Promotion Opportunity Score

Because Walmart Canada store-level sales outcomes are not available, the project does **not** claim to estimate causal promotion uplift.

Instead, an interpretable baseline called the:

> **Promotion Opportunity Score**

is used.

The score combines:

* discount strength
* local population
* commercial activity
* household income context
* weather intensity

The weights are deliberately transparent so each recommendation can be explained.

Example:

```text
Opportunity Score
    = discount contribution
    + population contribution
    + commercial contribution
    + income contribution
    + weather contribution
```

This score should be treated as a ranking heuristic rather than predicted causal uplift.

---

# Profit-Aware Optimization

Promotion opportunity scores are converted into a simple economic scenario.

The MVP assumes:

```text
assumed margin rate = 25%
maximum incremental demand proxy = 10 units
```

These values are scenario assumptions and are **not Walmart financial data**.

The system constructs:

```text
estimated unit margin
incremental demand proxy
profit proxy
economic score
```

The economic score then combines contextual relevance with estimated economic attractiveness.

---

# Flyer Optimization

A constrained greedy optimizer chooses the highest-scoring products for each store.

Constraints include:

* maximum flyer slots
* no duplicate products
* category limits when detailed categories are available

The current Walmart collector contains only 7 unique products, so the optimizer can select at most 7 products per store.

Current final validation:

```text
Economic rows:              105
Optimized rows:             105
Stores:                      15
Maximum flyer slots used:     7
Duplicate store/product:       0
Economic score range: 2.29 – 80.84
```

The 7-slot result is caused by the current promotion sample containing only 7 unique products—not by an optimizer error.

---

# Scientific Limitations

This project deliberately separates what is measured from what is assumed.

### No Canadian Walmart sales outcomes

The GTA promotion system currently has:

```text
promotions
demographics
weather
geographic context
```

but does not have Walmart Canada store-product sales outcomes.

Therefore it cannot currently estimate:

* true promotion uplift
* causal treatment effects
* true incremental revenue
* true incremental profit

The current optimizer should therefore be interpreted as a:

> **promotion opportunity and economic scenario engine**

rather than a causal recommendation model.

### Margin assumptions

True retailer product margins are unavailable.

The 25% margin used in the MVP is only a scenario parameter.

### Limited flyer coverage

The current collector produced 7 unique products.

The end-to-end pipeline is therefore validated, but a production-quality version would collect:

* hundreds of products
* multiple product categories
* multiple flyer weeks
* store-specific availability
* historical promotion observations

### Weather approximation

Toronto Pearson weather is currently used as a GTA-wide proxy.

A future version should assign stores to nearby weather stations.

---

# Repository Structure

```text
retail-promotion-intelligence/
│
├── data/
│   ├── raw/
│   │   └── m5/
│   │
│   ├── external/
│   │   ├── walmart/
│   │   ├── statscan/
│   │   ├── osm/
│   │   ├── weather/
│   │   └── holidays/
│   │
│   ├── interim/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_inspection.ipynb
│   ├── 02_build_enriched_sales.ipynb
│   ├── 03_eda_feature_engineering.ipynb
│   ├── 04_time_split_and_baseline.ipynb
│   ├── 05_catboost_baseline.ipynb
│   ├── 06_model_evaluation.ipynb
│   ├── 07_lightgbm_xgboost_comparison.ipynb
│   ├── 08_external_data_collection.ipynb
│   ├── 08A_prepare_statscan_profile.ipynb
│   ├── 09_statscan_demographics.ipynb
│   ├── 10_weather.ipynb
│   ├── 11_promotions_flyer_data.ipynb
│   ├── 11A_flyer_collection.ipynb
│   ├── 12_build_gta_promotion_context.ipynb
│   ├── 13_promotion_opportunity_scoring.ipynb
│   ├── 14_profit_aware_flyer_optimization.ipynb
│   └── 15_final_validation.ipynb
│
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   ├── optimization/
│   └── monitoring/
│
├── models/
├── results/
├── configs/
├── tests/
├── requirements.txt
└── README.md
```

---

# Main Outputs

```text
models/
└── catboost_ca1.cbm

data/processed/
├── CA_1_features_v1.parquet
└── gta_promotion_context_v1.parquet

results/
├── gta_promotion_rankings_v1.parquet
├── gta_economic_rankings_v1.parquet
├── gta_top10_promotions_per_store_v1.parquet
├── gta_optimized_flyer_v1.parquet
└── gta_optimized_flyer_summary_v1.csv
```

---

# How to Run

Create the environment:

```bash
conda create -n retail-ai python=3.11 -y
conda activate retail-ai
```

Install major dependencies:

```bash
pip install \
    pandas \
    numpy \
    pyarrow \
    duckdb \
    pymongo \
    python-dotenv \
    scikit-learn \
    xgboost \
    lightgbm \
    catboost \
    matplotlib \
    geopandas \
    osmnx \
    shapely \
    requests \
    beautifulsoup4 \
    lxml
```

Run notebooks sequentially from `01` through `15`.

---

# Future Production Version

The next stage would extend the MVP into a production-oriented system.

### Better promotion data

* multiple flyer weeks
* hundreds or thousands of products
* detailed product categories
* store-specific inventory
* historical prices
* true margin data

### Causal promotion modeling

With observed sales outcomes:

```text
treatment = promoted
control = not promoted
outcome = sales / profit
```

Possible approaches:

* regression adjustment
* propensity score methods
* T-Learner
* X-Learner
* doubly robust estimation
* heterogeneous treatment-effect estimation

### Production ML

Planned components:

* FastAPI recommendation service
* MLflow experiment tracking
* model registry
* Docker
* monitoring
* feature drift detection
* scheduled retraining
* champion/challenger models
* rollback capability
* CI/CD
* AWS deployment

### Optimization

Future optimizer constraints could include:

* inventory
* promotion budget
* category diversity
* shelf capacity
* supplier agreements
* minimum margin
* regional availability
* cannibalization
* promotion fatigue

---

# Key Takeaway

This project goes beyond training a single forecasting model.

It demonstrates how a retail ML system can combine:

```text
forecasting
geospatial engineering
large-scale data processing
demographic enrichment
weather signals
promotion ingestion
ranking
economic reasoning
business optimization
```

while keeping the assumptions and limitations of the available data explicit.

The current version should be viewed as an **end-to-end analytical MVP and system-design prototype** for localized retail promotion intelligence.
