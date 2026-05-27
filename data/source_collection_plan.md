# Source Collection Plan

## 1. Project Research Question

How should Vietnamese residential real estate developers adapt their product, land bank, capital, and launch strategies under public policy uncertainty during 2026-2030?

## 2. Data Collection Principles

- Use only public and verifiable sources.
- Do not fabricate numbers.
- Every data point must have a source URL.
- Prefer primary sources for laws and official statistics.
- Use consulting and research reports for market interpretation.
- Separate raw data from processed data.
- Record uncertainty, source limitations, and interpretation limits clearly.

## 3. Source Map by Data Table

### policy_timeline_template.csv

Use this table to record policy events that may affect residential real estate strategy, market structure, financing conditions, or project execution.

Target source categories:

- Land Law 2024
- Housing Law 2023
- Real Estate Business Law 2023
- Implementing decrees and circulars
- Real estate credit policy
- Corporate bond regulation
- Social housing policy
- Infrastructure and public investment policy

Preferred source types:

- National Assembly documents
- Government decrees
- Ministry circulars and official announcements
- State Bank of Vietnam policy releases
- Ministry of Construction publications
- Official provincial or municipal planning announcements, where relevant

### market_indicators_template.csv

Use this table to collect market indicators that describe residential real estate demand, supply, pricing, liquidity, financing, and inventory conditions.

Target source categories:

- Ministry of Construction real estate market reports
- General Statistics Office
- State Bank of Vietnam
- Savills Vietnam
- CBRE Vietnam
- DKRA
- JLL
- FiinRatings
- Securities company sector reports

Potential metrics to collect:

- New residential supply
- Launch volume
- Transaction volume
- Absorption rate
- Primary selling price
- Inventory level
- Housing credit indicators
- Corporate bond issuance or refinancing pressure
- Construction activity indicators

### developer_strategy_cases_template.csv

Use this table to document how selected developers respond to policy uncertainty, financing pressure, project approval risk, and changing buyer demand.

Target companies:

- Vinhomes
- Nam Long
- Khang Dien
- Novaland
- Dat Xanh

Potential source types:

- Annual reports
- Investor presentations
- Financial statements
- Earnings releases
- Exchange disclosures
- Credit rating reports
- Securities company reports
- Management commentary from public interviews or conferences

### source_log_template.csv

Every source used in this project should be logged in `source_log_template.csv` before any data point is added to an analysis table.

For each source, record:

- Source ID
- Publication date
- Source title
- Publisher
- Source type
- URL or file path
- Reliability notes
- Access date
- Key fields supported by the source

The source log should make it possible to trace every policy event, market indicator, and company case observation back to a public and verifiable source.

## 4. Source Priority Ranking

### Tier 1: Official / Primary Sources

Examples:

- National Assembly
- Government of Vietnam
- Ministry of Construction
- State Bank of Vietnam
- General Statistics Office
- Company annual reports
- Company financial statements
- Official exchange disclosures

Use Tier 1 sources for laws, regulations, official statistics, company-reported figures, and formal policy changes.

### Tier 2: Professional Market Reports

Examples:

- Savills
- CBRE
- JLL
- DKRA
- FiinRatings
- Securities company sector reports

Use Tier 2 sources for market interpretation, sector trends, pricing commentary, supply and demand analysis, financing context, and competitive positioning.

### Tier 3: News and Commentary

Examples:

- Vietnam Investment Review
- VnEconomy
- CafeF
- The Investor
- Nikkei
- Bloomberg
- Reuters

Use Tier 3 sources mainly for context, event tracking, management commentary, and triangulation. Tier 3 sources should not be the sole basis for quantitative claims unless the article directly cites a primary source and the original source is unavailable.

## 5. Data Extraction Checklist

For each source, answer the following questions before extracting data:

- What is the publication date?
- What period does the data cover?
- What geography does it cover?
- Is the source primary or secondary?
- What metric can be extracted?
- Does the source support a market, policy, company, or strategy insight?
- What are the limitations?

Extraction rules:

- Copy only factual data into raw tables.
- Record the original unit and geography.
- Do not normalize or transform data in raw files.
- Add interpretation only in processed files, notebooks, or the memo.
- Flag conflicting data instead of forcing reconciliation too early.

## 6. Minimum Viable Dataset

The first complete version of this project should include the following minimum dataset.

### Policy Timeline

- At least 12 policy events from 2021-2026
- Coverage across land, housing, real estate business, credit, bonds, social housing, and infrastructure or public investment policy
- Each event linked to a logged source

### Market Indicators

- At least annual indicators for 2021-2025
- Include 2026 indicators if available
- Coverage should include at least one demand indicator, one supply indicator, one pricing indicator, and one financing indicator
- Each metric linked to a logged source

### Developer Cases

- At least 5 listed developers
- Minimum target coverage: Vinhomes, Nam Long, Khang Dien, Novaland, and Dat Xanh
- Each case should include business model, product focus, financing profile, policy exposure, and observed strategic response

### Scenario Matrix

- At least 3 policy scenarios
- At least 4 strategic levers
- Strategic levers should cover product, land bank, capital structure, and launch timing

## 7. Next Task

Task 2 - Fill `policy_timeline.csv` using real sources.

