# CivicPulse India
### AI-Powered Civic Complaint Intelligence & Ward Prioritization

CivicPulse India is a data-driven civic intelligence platform designed to analyze urban complaints, identify unusual reporting patterns, prioritize wards, and recommend targeted actions for civic authorities.

Using Bengaluru's historical civic complaint data from 2023–2024, the project combines Machine Learning, statistical analysis, and interactive visualization to support evidence-based urban governance.

## Key Features

- **Civic Complaint Analytics:** Analyze complaint trends across 198 Bengaluru wards.
- **Ward Clustering:** Group wards based on their civic complaint patterns using K-Means.
- **Priority Assessment:** Classify wards into High, Medium, and Low historical priority levels.
- **Complaint Forecasting:** Predict monthly complaint volumes using Random Forest regression.
- **Anomaly Detection:** Identify unusual complaint activity using Isolation Forest and Z-scores.
- **Explainable Alerts:** Identify complaint subcategories contributing most to month-over-month increases.
- **Actionable Recommendations:** Suggest issue-specific actions for civic authorities.
- **Interactive Dashboard:** Explore historical ward performance through Streamlit.

## Technologies Used

Python · Pandas · NumPy · Scikit-learn · Machine Learning · Streamlit · Data Visualization

## Model Performance

The improved Random Forest forecasting model achieved the following results on the July–December 2024 test period:

- **MAE:** 22.10 complaints
- **RMSE:** 36.99 complaints
- **R² Score:** 0.845

These results represent historical evaluation rather than validated future forecasting performance.

## Example Finding

In November 2024, Maruthi Seva Nagar recorded 555 complaints, including 485 unauthorized construction complaints.

The anomaly detection model flagged this unusual reporting pattern, while the recommendation system suggested reviewing construction permissions and inspecting reported sites.

## Project Objective

To transform historical civic complaint records into understandable insights that can help authorities identify reporting trends, investigate unusual activity, and prioritize civic service improvements.

## Limitations

This project currently uses historical data from 2023–2024. Its anomaly detection, priority scoring, and recommendations are exploratory and should not be treated as verified real-time alerts or official administrative decisions.

## Future Enhancements

- Live civic complaint data integration
- Geographic ward visualization
- Improved forecasting with rolling backtesting
- Complaint-level duplicate detection
- Dynamic monthly priority scoring
