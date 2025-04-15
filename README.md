# SFCC B2B/Enterprise Market Analysis

A comprehensive analysis of Salesforce Commerce Cloud (SFCC) in the B2B and Enterprise market, based on customer feedback and market research.

## Overview

This project provides insights into:
- Industry-specific pain points and challenges
- Technical implementation considerations
- Integration patterns across different sectors
- Market trends and adoption patterns

## Project Structure

- `sfcc_analysis.py`: Main Streamlit application with interactive visualizations
- `sfcc_analysis_landing_page.html`: Static HTML report of findings
- `requirements.txt`: Python dependencies
- Additional utility scripts for data processing

## Local Development

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
.venv\Scripts\activate     # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app locally:
```bash
streamlit run sfcc_analysis.py --server.port 8502
```

## Deployment to Shopify Internal Streamlit

1. Clone this repository to your Shopify workspace
2. Navigate to [streamlit-service](https://github.com/Shopify/streamlit-service)
3. Follow the deployment steps:
   ```bash
   cd SFCC-B2B-Enterprise-Market-Analysis
   dev up
   dev deploy streamlit-service
   ```

4. Access your deployed app at: `https://streamlit.shopify.io/SFCC-B2B-Enterprise-Market-Analysis`

## Data Sources

- Customer feedback transcripts
- Market research data
- Industry analysis reports
- Integration patterns across different sectors

## Contributing

Please follow Shopify's internal contribution guidelines when making changes to this analysis.

## Contact

For questions or feedback about this analysis, please reach out to the team. 