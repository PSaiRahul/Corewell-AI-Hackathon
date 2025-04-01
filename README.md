Gap:

Health systems often struggle to objectively assess provider performance when treating patients of varying complexity. Existing productivity metrics (like number of encounters or procedures) fail to adjust for patient risk, leading to inaccurate comparisons and inefficient resource planning.
 
Orientation:

While analyzing synthetic clinical data from multiple Snowflake tables (PROVIDERS, ENCOUNTERS, PROCEDURES, PATIENTS, and CONDITIONS), I discovered that productivity insights lacked clinical context. This oversight follows a common trend in healthcare analytics—volume-focused metrics without quality or complexity adjustments.
 
Impact:

Without proper adjustment for patient risk:
•	High-performing providers treating complex patients may appear less productive.
•	Resources may be misallocated, leading to burnout, poor patient outcomes, and financial waste.
•	Administrators and planners lack meaningful benchmarks to improve care delivery or optimize performance.
 
Importance:

With growing pressure on healthcare systems to deliver value-based care, it’s critical to shift from quantity-based evaluations to context-aware provider performance metrics. This directly impacts:
•	Strategic workforce planning
•	Quality-of-care initiatives
•	Financial forecasting
•	Patient safety and outcomes

What Tools Are We Using? 

•	Data Source: Snowflake (read-only shared Synthea data + Feature Engineered fields)
•	Backend: Python with Snowflake Connector (externalbrowser authentication)
•	ML/Analytics: scikit-learn (KMeans), pandas, plotly
•	UI: Streamlit (interactive dashboard with filters, charts, and maps)
 
Our Solution:

I built an interactive Streamlit dashboard that:
•	Ranks providers based on procedure volume, encounter count, and patient risk
•	Uses quantile-based risk scoring to classify providers as Stable, Monitor, or Chronic Risk
•	Applies KMeans clustering to group providers by performance profiles
•	Includes dynamic filters (e.g., state, specialty) and a geographical map of providers
•	Enables exportable summaries for easy analysis and reporting
This dashboard transforms raw volume metrics into actionable, risk-aware insights, empowering smarter staffing, planning, and performance evaluation in healthcare organizations.

Glossary of Metrics and Terms:
 
1. Total Encounters
 
Definition: The total number of patient visits or clinical interactions handled by a provider.
 
Why it matters:
Encounters reflect how frequently a provider sees patients. A high encounter count may indicate a provider is managing many patients, but without patient risk context, it doesn't fully reflect complexity or quality.
 
2. Total Procedures

Definition: The total number of medical procedures a provider has performed across all encounters.
 
Why it matters:
This helps differentiate providers who are intervention-heavy from those managing patients through consultation or monitoring. It’s a key dimension of clinical workload.
 
3. Average Patient Risk Score
 
Definition: The average number of distinct medical conditions associated with a provider’s patients.
 
How it's calculated:
Each patient is assigned a risk score = number of unique conditions 
A provider's average risk score is computed across all patients they’ve treated

Why it matters:
Not all patients are equal. Treating a patient with 7 conditions is much more complex than treating someone with 1. This metric helps normalize provider performance by patient complexity.
 
4. Risk Level
 
Definition: A qualitative label that describes the average complexity of a provider’s patient population.
 
Labels Used:
•	Stable: Treating mostly low-risk patients
•	Monitor: Treating moderately complex patients
•	Chronic Risk: Handling high-complexity or chronic-condition patients
 
How it's calculated:
Based on quantiles (percentiles) of AVG_PATIENT_RISK
Dynamically adapts as the data changes
 
5. Cluster Label (via KMeans)
 
Definition: Grouping providers into meaningful performance types based on their procedures, encounters, and patient risk.
 
Labels Used:
 
•	Balanced Performer: Steady workload and moderate complexity
•	Procedure Heavy: High number of procedures, may indicate specialization
•	Encounter Heavy: High number of patient visits, often managing ongoing cases
 
Why it matters:
Clustering helps quickly identify patterns across providers without manually analyzing every variable.

6. Filtered Providers

Definition: The number of unique providers currently shown based on applied filters (e.g., by state or specialty).

7. Total Providers
 
Definition: The total number of unique providers in the dataset, regardless of filters.

8. Provider Location Map
 
Definition: A geo-visualization of providers using their latitude and longitude, color-coded by Risk Level and sized by Average Risk.
 
Why it matters:
Helps identify geographic clusters of high-risk care, overburdened regions, or resource gaps.

9. Risk Category Pie Chart
 
Definition: A visual distribution of providers across Stable, Monitor, and Chronic Risk categories.
 
Why it matters:
Gives a high-level view of how complexity is spread across the provider network.
