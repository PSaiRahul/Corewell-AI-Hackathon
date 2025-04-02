

![image](https://github.com/user-attachments/assets/b20ded53-26a6-4fef-a4c3-37f03d29fdfc)

 
---
 
Overview
 
DoxIQ is an AI-powered, interactive dashboard that brings context and fairness to evaluating clinical provider performance. It transforms traditional volume-based metrics into nuanced, risk-aware insights that help healthcare leaders make smarter, more equitable decisions.
 
 
---
 
Problem Statement
 
Gap
 
Health systems often struggle to objectively assess provider performance when treating patients of varying complexity. Existing productivity metrics (like number of encounters or procedures) fail to adjust for patient risk, leading to inaccurate comparisons and inefficient resource planning.
 
Orientation
 
While analyzing synthetic clinical data from multiple Snowflake tables (PROVIDERS, ENCOUNTERS, PROCEDURES, PATIENTS, and CONDITIONS), I discovered that productivity insights lacked clinical context. This oversight reflects a common trend in healthcare analytics: volume-focused metrics without adjustments for quality or complexity.
 
Impact
 
   Without proper adjustment for patient risk:
   •	High-performing providers treating complex patients may appear less productive.
   •	Resources may be misallocated, leading to burnout, poor patient outcomes, and financial waste.
   •	Administrators and planners lack meaningful benchmarks to improve care delivery or optimize performance.
 
 
Importance

   With growing pressure on healthcare systems to deliver value-based care, it’s critical to shift from quantity-based evaluations to context-aware provider performance metrics. This directly impacts:
   •	Strategic workforce planning
   •	Quality-of-care initiatives
   •	Financial forecasting
   •	Patient safety and outcomes
 
 
 
---
 
Tech Stack
 
Data Sources
 
   Snowflake: Read-only shared Synthea data, with engineered features
 
 
Backend
 
   Python: Core logic
   Snowflake Connector: Secure connection using external browser auth
 
 
Machine Learning & Analytics
 
   pandas: Data wrangling
   scikit-learn: KMeans clustering
   plotly: Interactive charting
 
 
Frontend
 
   Streamlit: Web UI with filters, charts, and maps
 
 
 
---
 
Solution Features
 
DoxIQ enables smarter provider evaluation by offering:
    
   Risk-adjusted ranking based on procedure volume, encounter count, and patient complexity
   Quantile-based risk scoring (Stable, Monitor, Chronic Risk)
   ML-driven provider clustering: Balanced, Procedure Heavy, Encounter Heavy
   Dynamic filters: specialty, state, and more
   Geographic visualization of providers
   Exportable summaries for leadership analysis and reporting

 
---
 
Glossary of Key Metrics
 
Total Encounters
   Definition: The total number of patient visits or clinical interactions handled by a provider.
   
   Why it matters: Encounters reflect how frequently a provider sees patients. A high encounter count may indicate a provider is managing many patients, but without patient risk context, it doesn't fully reflect complexity or quality.

Total Procedures
   Definition: The total number of medical procedures a provider has performed across all encounters.
   
   Why it matters: This helps differentiate providers who are intervention-heavy from those managing patients through consultation or monitoring. It’s a key dimension of clinical workload.

Average Patient Risk Score
   Definition: The average number of distinct medical conditions associated with a provider’s patients.
   
   How it's calculated: Each patient is assigned a risk score = number of unique conditions A provider's average risk score is computed across all patients they’ve treated

   Why it matters: Not all patients are equal. Treating a patient with 7 conditions is much more complex than treating someone with 1. This metric helps normalize provider performance by patient complexity.

Risk Level
   Definition: A qualitative label that describes the average complexity of a provider’s patient population.

Labels Used: 
   • Stable: Treating mostly low-risk patients 
   • Monitor: Treating moderately complex patients 
   • Chronic Risk: Handling high-complexity or chronic-condition patients

How it's calculated: Based on quantiles (percentiles) of AVG_PATIENT_RISK Dynamically adapts as the data changes

Cluster Label (via KMeans)
   Definition: Grouping providers into meaningful performance types based on their procedures, encounters, and patient risk.

Labels Used:

   Balanced Performer: Steady workload and moderate complexity 
   Procedure Heavy: High number of procedures, may indicate specialization
   Encounter Heavy: High number of patient visits, often managing ongoing cases

   Why it matters: Clustering helps quickly identify patterns across providers without manually analyzing every variable.

Filtered Providers
   Definition: The number of unique providers currently shown based on applied filters (e.g., by state or specialty).

Total Providers
   Definition: The total number of unique providers in the dataset, regardless of filters.

Risk Category Pie Chart
   Definition: A visual distribution of providers across Stable, Monitor, and Chronic Risk categories.

   Why it matters: 
   Gives a high-level view of how complexity is spread across the provider network.
---

 
Author
 
Sai Rahul Perumalla
Team: Table for One
