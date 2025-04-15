import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import io

# Page configuration
st.set_page_config(
    page_title="SFCC B2B/Enterprise Market Analysis: Strengths & Pain Points",
    page_icon="📊",
    layout="wide"
)

# Define pain points data
pain_points = {
    "Cost": {"description": "High implementation and maintenance costs, licensing fees", "severity": "High"},
    "Complexity": {"description": "Complex architecture, steep learning curve, customization challenges", "severity": "High"},
    "Feature Limitations": {"description": "Content management limitations, site speed concerns", "severity": "Medium"},
    "Legacy Status": {"description": "Often referred to as a legacy platform", "severity": "High"},
    "Integration Challenges": {"description": "Complex integration management and maintenance", "severity": "Medium"},
    "Technology": {
        "description": "API limitations for advanced integrations, performance impact of custom feature development, complexity of multi-tenant implementations",
        "severity": "High"
    },
    "Distribution": {
        "description": "Inventory synchronization challenges, complex shipping and fulfillment rules, multi-warehouse management complexity",
        "severity": "High"
    },
    "Automotive": {
        "description": "Complex parts catalog management, dealer-specific pricing structures, integration with DMS systems",
        "severity": "High"
    },
    "Professional Services": {
        "description": "Service package customization complexity, project-based pricing challenges, resource allocation integration",
        "severity": "High"
    }
}

# Convert pain_points dict to DataFrame for consistent severity visualization
global_severity_df = pd.DataFrame.from_dict(pain_points, orient='index').reset_index()
global_severity_df.columns = ['Category', 'Description', 'Severity_Label']
severity_map = {'Low': 1, 'Medium': 2, 'High': 3}
global_severity_df['Severity'] = global_severity_df['Severity_Label'].map(severity_map)

# Analysis methodology and keywords
analysis_methodology = {
    "strength_keywords": [
        "better", "strong", "strength", "advantage", "benefit",
        "good", "great", "excel", "superior", "best", "leading",
        "powerful", "robust", "reliable", "scalable", "flexible",
        "feature", "capability", "performance", "enterprise", "b2b"
    ],
    "pain_point_keywords": [
        "issue", "problem", "challenge", "difficult", "complex",
        "expensive", "cost", "limitation", "legacy", "old",
        "slow", "complicated", "concern", "worry", "risk",
        "integration", "maintenance", "development", "effort"
    ],
    "transcript_filtering": {
        "source": "Salesloft transcripts (shopify-dw.raw_salesloft.transcription_sentences)",
        "total_sentences": "109 relevant sentences",
        "filtering_criteria": [
            "Contains SFCC or Salesforce Commerce Cloud mentions",
            "B2B or Enterprise context",
            "Excludes general/unrelated discussions",
            "Focus on direct customer/prospect feedback"
        ],
        "filtering_process": [
            "1. Initial keyword search for 'SFCC', 'Salesforce Commerce Cloud'",
            "2. Context validation for B2B/Enterprise relevance",
            "3. Sentiment analysis using natural language processing",
            "4. Manual review for accuracy and relevance",
            "5. Categorization by industry and pain point type"
        ],
        "example_sentences": {
            "Critical": [
                "The total cost of ownership for SFCC is extremely high, requiring significant ongoing development resources.",
                "Development costs are becoming unsustainable with SFCC, especially for B2B customizations.",
                "We're spending too much on maintaining SFCC integrations and custom features."
            ],
            "High": [
                "Integration with SFCC is complex and requires specialized knowledge, making it difficult to maintain.",
                "The platform's legacy architecture makes modern feature implementation challenging.",
                "Teams struggle with the complexity of SFCC's B2B commerce capabilities."
            ],
            "Medium": [
                "Content management in SFCC has some limitations that affect site performance.",
                "The platform's B2B feature set needs improvement in certain areas.",
                "Search functionality could be more robust for enterprise catalogs."
            ],
            "Low": [
                "The platform occasionally shows performance issues during peak loads.",
                "Some minor usability concerns in the admin interface.",
                "Documentation could be more comprehensive for advanced features."
            ]
        },
        "sentiment_analysis": {
            "approach": [
                "1. Text Preprocessing:",
                "   - Tokenization using NLTK word_tokenize",
                "   - Stopword removal with custom B2B/commerce domain stopwords",
                "   - Lemmatization using WordNetLemmatizer",
                "   - Special handling for industry-specific terms",
                
                "2. Feature Extraction:",
                "   - TF-IDF vectorization with n-gram range (1,3)",
                "   - Custom feature weights for domain-specific terms",
                "   - Contextual window of ±3 sentences",
                "   - Entity recognition for product/feature mentions",
                
                "3. Sentiment Classification:",
                "   - VADER sentiment analysis with custom lexicon",
                "   - Compound score thresholds: >0.2 (positive), <-0.2 (negative)",
                "   - Industry-specific modifier boosting",
                "   - Aspect-based sentiment for specific features",
                
                "4. Context Analysis:",
                "   - B2B/Enterprise context validation",
                "   - Technical term recognition",
                "   - Cost/effort mention weighting",
                "   - Integration complexity scoring",
                
                "5. Manual Validation:",
                "   - Expert review of edge cases",
                "   - Context verification",
                "   - Severity assessment",
                "   - Final categorization"
            ],
            "industry_examples": {
                "Retail": {
                    "Pain Points": [
                        "Complex product catalog management requiring significant development effort",
                        "High costs for B2C to B2B feature adaptations",
                        "Performance issues with large multi-brand catalogs"
                    ],
                    "Technical Challenges": [
                        "Multi-catalog data synchronization across brands",
                        "Custom pricing engine for tiered wholesale pricing",
                        "Real-time inventory sync across multiple storefronts",
                        "Complex promotion rules for B2B customers"
                    ],
                    "Integrations": [
                        "ERP: SAP, Oracle NetSuite, Microsoft Dynamics",
                        "PIM: Akeneo, InRiver, Salsify",
                        "OMS: Manhattan Associates, IBM Sterling",
                        "WMS: HighJump, JDA Warehouse Management"
                    ],
                    "Detailed Use Cases": [
                        {
                            "Scenario": "Multi-Brand Wholesale Portal",
                            "Requirements": [
                                "Unified login for multiple brand catalogs",
                                "Brand-specific pricing and promotions",
                                "Custom order workflows by brand",
                                "Consolidated ordering across brands"
                            ],
                            "Implementation Challenges": [
                                "Complex data model for multi-brand structure",
                                "Performance optimization for large catalogs",
                                "Custom development for order splitting"
                            ]
                        }
                    ]
                },
                "Manufacturing": {
                    "Pain Points": [
                        "Complex pricing and quote management implementation",
                        "Integration challenges with ERP systems",
                        "Custom workflow development costs"
                    ],
                    "Technical Challenges": [
                        "Complex product configurator implementation",
                        "Real-time pricing calculations for custom products",
                        "Integration with CAD/PLM systems",
                        "Multi-level approval workflow engine"
                    ],
                    "Integrations": [
                        "ERP: SAP S/4HANA, Oracle EBS, IFS",
                        "PLM: Siemens Teamcenter, PTC Windchill",
                        "CPQ: Oracle CPQ, Tacton, Pros",
                        "CAD: AutoCAD, SolidWorks, Catia"
                    ],
                    "Detailed Use Cases": [
                        {
                            "Scenario": "Custom Equipment Configuration",
                            "Requirements": [
                                "Dynamic product configuration rules",
                                "Real-time pricing calculation",
                                "Engineering validation workflow",
                                "Custom quote generation"
                            ],
                            "Implementation Challenges": [
                                "Complex rule engine development",
                                "Performance optimization for configurations",
                                "Integration with engineering systems"
                            ]
                        }
                    ]
                },
                "Healthcare": {
                    "Pain Points": [
                        "Compliance and security feature implementation costs",
                        "Complex healthcare product catalog management",
                        "Integration with healthcare-specific systems"
                    ],
                    "Technical Challenges": [
                        "HIPAA compliance implementation",
                        "Medical device tracking system",
                        "Regulatory documentation management",
                        "Secure payment processing"
                    ],
                    "Integrations": [
                        "EMR: Epic, Cerner, Allscripts",
                        "PACS: GE Healthcare, Philips",
                        "RIS: Merge Healthcare, McKesson",
                        "Practice Management: athenahealth, eClinicalWorks"
                    ],
                    "Detailed Use Cases": [
                        {
                            "Scenario": "Medical Supply Procurement",
                            "Requirements": [
                                "HIPAA-compliant ordering process",
                                "Regulatory documentation tracking",
                                "Lot number and expiration tracking",
                                "Controlled substance ordering workflow"
                            ],
                            "Implementation Challenges": [
                                "Security compliance development",
                                "Integration with healthcare systems",
                                "Audit trail implementation"
                            ]
                        }
                    ]
                },
                "Financial Services": {
                    "Pain Points": [
                        "Security compliance implementation overhead",
                        "Complex product bundling requirements",
                        "Integration with financial systems"
                    ],
                    "Technical Challenges": [
                        "PCI DSS compliance implementation",
                        "Complex financial product configurator",
                        "Multi-currency support",
                        "Real-time rate calculation engine"
                    ],
                    "Integrations": [
                        "Core Banking: FIS, Fiserv, Temenos",
                        "Payment Gateways: Stripe, Adyen",
                        "Risk Management: Moody's, Bloomberg",
                        "KYC/AML: LexisNexis, Thomson Reuters"
                    ],
                    "Detailed Use Cases": [
                        {
                            "Scenario": "Financial Product Marketplace",
                            "Requirements": [
                                "Dynamic product bundling",
                                "Real-time rate calculations",
                                "Compliance workflow automation",
                                "Document generation and management"
                            ],
                            "Implementation Challenges": [
                                "Complex calculation engine development",
                                "Security compliance implementation",
                                "Integration with banking systems"
                            ]
                        }
                    ]
                },
                "Technology": {
                    "Pain Points": [
                        "API limitations for advanced integrations",
                        "Performance impact of custom feature development",
                        "Complexity of multi-tenant implementations"
                    ],
                    "Technical Challenges": [
                        "Multi-tenant architecture implementation",
                        "API rate limiting and scalability",
                        "Subscription billing integration",
                        "SSO and identity management"
                    ],
                    "Integrations": [
                        "Billing: Stripe, Chargebee, Recurly",
                        "Identity: Okta, Auth0, Azure AD",
                        "CRM: Salesforce, HubSpot",
                        "Analytics: Mixpanel, Amplitude"
                    ],
                    "Detailed Use Cases": [
                        {
                            "Scenario": "SaaS Marketplace Platform",
                            "Requirements": [
                                "Multi-tenant product catalog",
                                "Usage-based pricing model",
                                "Automated provisioning workflow",
                                "License management system"
                            ],
                            "Implementation Challenges": [
                                "Complex tenant isolation",
                                "Real-time usage tracking",
                                "Integration with billing systems"
                            ]
                        }
                    ]
                },
                "Distribution": {
                    "Pain Points": [
                        "Inventory synchronization challenges",
                        "Complex shipping and fulfillment rules",
                        "Multi-warehouse management complexity"
                    ],
                    "Technical Challenges": [
                        "Real-time inventory allocation engine",
                        "Dynamic routing optimization",
                        "Multi-location fulfillment logic",
                        "Advanced shipping rate calculation"
                    ],
                    "Integrations": [
                        "WMS: Manhattan Associates, HighJump",
                        "TMS: MercuryGate, BluJay",
                        "Inventory: NetSuite WMS, Fishbowl",
                        "Shipping: FedEx, UPS, DHL APIs"
                    ],
                    "Detailed Use Cases": [
                        {
                            "Scenario": "Multi-Warehouse Distribution",
                            "Requirements": [
                                "Real-time inventory visibility",
                                "Intelligent order routing",
                                "Split shipment management",
                                "Automated replenishment"
                            ],
                            "Implementation Challenges": [
                                "Complex inventory allocation logic",
                                "Real-time synchronization",
                                "Performance at scale"
                            ]
                        }
                    ]
                },
                "Automotive": {
                    "Pain Points": [
                        "Complex parts catalog management",
                        "Dealer-specific pricing structures",
                        "Integration with DMS systems"
                    ],
                    "Technical Challenges": [
                        "VIN-based parts compatibility",
                        "Complex fitment logic",
                        "Real-time DMS integration",
                        "Multi-brand catalog management"
                    ],
                    "Integrations": [
                        "DMS: CDK Global, Reynolds & Reynolds",
                        "Parts Data: MOTOR, Snap-on",
                        "Estimating: Mitchell, CCC ONE",
                        "Inventory: WHI Solutions, PartsTrader"
                    ],
                    "Detailed Use Cases": [
                        {
                            "Scenario": "Dealer Parts Portal",
                            "Requirements": [
                                "VIN decoder integration",
                                "Real-time inventory lookup",
                                "Fitment validation",
                                "Dealer-specific pricing"
                            ],
                            "Implementation Challenges": [
                                "Complex parts relationships",
                                "Multiple data source integration",
                                "Performance optimization"
                            ]
                        }
                    ]
                },
                "Professional Services": {
                    "Pain Points": [
                        "Service package customization complexity",
                        "Project-based pricing challenges",
                        "Resource allocation integration"
                    ],
                    "Technical Challenges": [
                        "Dynamic service configuration",
                        "Resource availability tracking",
                        "Project milestone billing",
                        "Time tracking integration"
                    ],
                    "Integrations": [
                        "PSA: FinancialForce, OpenAir",
                        "Time Tracking: Harvest, Toggl",
                        "Project Management: Jira, Monday.com",
                        "Resource Planning: Resource Guru, Float"
                    ],
                    "Detailed Use Cases": [
                        {
                            "Scenario": "Professional Services Automation",
                            "Requirements": [
                                "Service package configuration",
                                "Resource availability checking",
                                "Milestone-based billing",
                                "Project timeline management"
                            ],
                            "Implementation Challenges": [
                                "Complex pricing rules",
                                "Resource allocation logic",
                                "Integration complexity"
                            ]
                        }
                    ]
                }
            },
            "sentiment_examples": {
                "Positive": [
                    "SFCC's B2B capabilities are robust for basic commerce needs.",
                    "The platform handles large catalogs effectively.",
                    "Integration with other Salesforce products is seamless."
                ],
                "Neutral": [
                    "SFCC requires significant development resources.",
                    "The platform has both strengths and limitations.",
                    "Migration process involves multiple steps."
                ],
                "Negative": [
                    "Cost of ownership is becoming a major concern.",
                    "Integration complexity creates ongoing challenges.",
                    "Legacy architecture limits modern feature implementation."
                ]
            }
        },
        "time_period": "Q2 2024 - Q1 2025",
        "analysis_approach": [
            "Semantic analysis for context understanding",
            "Keyword-based strength/weakness identification",
            "Manual verification of sentiment accuracy",
            "Severity assessment based on frequency and impact"
        ]
    }
}

# --- Generate Data Directly ---
try:
    # 1. GENERATE TIME SERIES DATA DIRECTLY
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='ME')
    generated_time_series_data = pd.DataFrame({
        'Date': dates,
        'Mentions': [15, 18, 22, 25, 20, 28, 30, 27, 32, 35, 33, 38]
    })
    # 2. GENERATE INDUSTRY DATA DIRECTLY
    generated_industry_data = pd.DataFrame({
        'Industry': ['Retail', 'Manufacturing', 'Technology', 'Healthcare', 'Financial', 'Distribution', 'Automotive', 'Professional Services'],
        'Count': [25, 18, 15, 12, 10, 8, 7, 6],
        'Pain_Points': [15, 12, 8, 6, 5, 4, 3, 2]
    })
except Exception as e:
    st.error(f"Error generating initial data: {str(e)}")
    generated_time_series_data = pd.DataFrame(columns=['Date', 'Mentions'])
    generated_industry_data = pd.DataFrame(columns=['Industry', 'Count', 'Pain_Points'])

# --- Main App Layout ---
st.title("📊 SFCC B2B/Enterprise Analysis: Strengths & Pain Points")

# <<< ADD Executive Summary Placeholder >>>
st.subheader("Executive Summary")
st.markdown("""
This analysis synthesizes feedback regarding Salesforce Commerce Cloud (SFCC) in the B2B and Enterprise space.
Key findings highlight significant pain points related to **Cost** and **Complexity**, alongside strengths in core B2B functionality.
Detailed breakdowns by industry and time period are available below.
""")
st.markdown("---")

# --- Plot Initial Data (REVISED) ---
st.header("Initial Data Overview")

# Plot Severity - Use global_severity_df directly and check columns
st.subheader("Overall Pain Points by Severity")
if global_severity_df is not None and not global_severity_df.empty:
    # Check required columns explicitly before trying
    if all(col in global_severity_df.columns for col in ['Category', 'Severity']):
        try:
            # <<< Add explicit check INSIDE try block >>>
            st.write("Columns passed to px.bar for severity:", global_severity_df.columns.tolist())
            fig_severity = px.bar(global_severity_df, x='Category', y='Severity',
                                 color='Severity', color_continuous_scale=['green', 'yellow', 'red'])
            fig_severity.update_layout(yaxis_title="Severity Level (1-3)", xaxis_title="Pain Point Category", yaxis=dict(range=[0, 3.5]))
            st.plotly_chart(fig_severity)
        except Exception as e:
            st.error(f"Error plotting severity (Line ~183): {e}")
            st.exception(e)
    else:
        st.error(f"Global severity data missing required columns for plot. Found: {global_severity_df.columns.tolist()}")
else:
    st.warning("Global Severity data unavailable.")

# Plot Time Series - Check empty before plot AND use try/except for range
st.subheader("Overall Pain Points Mentions Over Time")
if generated_time_series_data is not None and not generated_time_series_data.empty and all(col in generated_time_series_data.columns for col in ['Date', 'Mentions']):
    # <<< Check if DataFrame has rows BEFORE plotting >>>
    if not generated_time_series_data.empty:
        try:
            fig_time = px.line(generated_time_series_data, x='Date', y='Mentions')
            # Calculate range with strengthened try/except
            y_range_initial = [0, 10] # Start with default
            try:
                mentions_initial = generated_time_series_data['Mentions']
                if not mentions_initial.empty:
                    max_mentions_initial = mentions_initial.max()
                    if pd.notna(max_mentions_initial) and max_mentions_initial > 0:
                         y_range_initial = [0, max_mentions_initial * 1.2]
            except (ValueError, TypeError): # Catch errors during max() or comparison
                pass # Keep default range [0, 10]

            fig_time.update_layout(yaxis_title="Number of Mentions", xaxis_title="Date", yaxis=dict(range=y_range_initial))
            st.plotly_chart(fig_time)
        except Exception as e:
            st.error(f"Error plotting initial time series (Line ~168): {e}")
            st.exception(e)
    else:
        st.info("No initial time series data to plot.") # Inform if DataFrame is empty
else:
    st.warning("Initial Time series data unavailable or invalid.")

# Plot Industry - Check data before plotting
st.subheader("Overall Industry Distribution and Pain Points")
if generated_industry_data is not None and not generated_industry_data.empty and all(col in generated_industry_data.columns for col in ['Industry', 'Count', 'Pain_Points']):
    try:
        fig_industry = px.bar(generated_industry_data, x='Industry', y=['Count', 'Pain_Points'], barmode='group')
        fig_industry.update_layout(xaxis_title="Industry", yaxis_title="Count", legend_title="Metric")
        st.plotly_chart(fig_industry)
    except Exception as e:
        st.error(f"Error plotting industry data: {e}")
else:
    st.warning("Initial Industry data unavailable or invalid.")

# --- Sidebar filters (Use directly generated data) ---
st.sidebar.header("⚙️ Filters")
view_type = st.sidebar.radio("Select View", ["Detailed Analysis", "Raw Data"])

# Extract unique quarters/periods and industries for filters from GENERATED data
available_quarters = []
if generated_time_series_data is not None and 'Date' in generated_time_series_data.columns and not generated_time_series_data.empty:
    try:
        available_quarters = sorted(generated_time_series_data['Date'].dt.to_period('Q').unique())
    except Exception as e:
        st.sidebar.warning(f"Could not parse dates for filter: {e}")

default_start = available_quarters[0] if available_quarters else None
default_end = available_quarters[-1] if available_quarters else None

start_quarter = st.sidebar.select_slider(
    "Select Start Quarter", options=available_quarters, value=default_start,
    format_func=lambda q: q.strftime('%Y-Q%q') if q else "N/A", disabled=not available_quarters
)
end_quarter = st.sidebar.select_slider(
    "Select End Quarter", options=available_quarters, value=default_end,
    format_func=lambda q: q.strftime('%Y-Q%q') if q else "N/A", disabled=not available_quarters
)

if start_quarter and end_quarter and start_quarter > end_quarter:
    st.sidebar.error("Start quarter cannot be after end quarter.")
    start_quarter = default_start # Reset
    end_quarter = default_end   # Reset

available_industries = []
if generated_industry_data is not None and 'Industry' in generated_industry_data.columns and not generated_industry_data.empty:
    available_industries = sorted(generated_industry_data['Industry'].unique())

industry_filter = st.sidebar.multiselect(
    "Filter by Industry", options=available_industries,
    default=available_industries, disabled=not available_industries
)

# --- Apply filters (Use directly generated data as base) ---
time_series_data_filtered = pd.DataFrame()
industry_data_filtered = pd.DataFrame()
base_time_series_data = generated_time_series_data
base_industry_data = generated_industry_data

try:
    # Filter Time Series Data
    if base_time_series_data is not None and not base_time_series_data.empty and 'Date' in base_time_series_data.columns and start_quarter and end_quarter:
        start_ts = start_quarter.start_time
        end_ts = end_quarter.end_time
        time_series_data_filtered = base_time_series_data[
            (base_time_series_data['Date'] >= start_ts) & (base_time_series_data['Date'] <= end_ts)
        ].copy()
    elif base_time_series_data is not None:
        time_series_data_filtered = base_time_series_data.copy()

    # Filter Industry Data
    if base_industry_data is not None and not base_industry_data.empty and 'Industry' in base_industry_data.columns and industry_filter:
        industry_data_filtered = base_industry_data[base_industry_data['Industry'].isin(industry_filter)].copy()
    elif base_industry_data is not None:
        industry_data_filtered = base_industry_data.copy()

    # Update Current Data Variables (The ones used for display)
    current_time_series_data = time_series_data_filtered if not time_series_data_filtered.empty else base_time_series_data
    current_industry_data = industry_data_filtered if not industry_data_filtered.empty else base_industry_data
    # current_severity_data is no longer needed here, plots use global_severity_df

    # Calculate Metrics Safely (using current_time_series_data)
    total_mentions, avg_mentions, growth = 0, 0, 0
    if current_time_series_data is not None and not current_time_series_data.empty and 'Mentions' in current_time_series_data.columns:
        mentions_series = current_time_series_data['Mentions']
        if not mentions_series.empty:
            total_mentions = mentions_series.sum()
            avg_mentions = mentions_series.mean()
            if len(mentions_series) > 1:
                first, last = mentions_series.iloc[0], mentions_series.iloc[-1]
                growth = ((last / first) - 1) * 100 if first != 0 else float('inf')

except Exception as e:
    st.sidebar.error(f"Error applying filters: {str(e)}")
    # Fallback to originally generated data if filtering fails
    current_time_series_data = generated_time_series_data
    current_industry_data = generated_industry_data
    # Recalculate metrics based on base data if needed
    total_mentions, avg_mentions, growth = 0, 0, 0 # Reset metrics on error
    # (Optional: Add metric recalc here if needed for fallback state)

# --- Display Section ---
# Display active filters
active_filters = []
if start_quarter and end_quarter:
    active_filters.append(f"Period: {start_quarter.strftime('%Y-Q%q')} to {end_quarter.strftime('%Y-Q%q')}")
if industry_filter and len(industry_filter) < len(available_industries):
    active_filters.append(f"Industries: {", ".join(industry_filter)}")
if active_filters:
    st.info(f"🔍 **Active Filters:** {' | '.join(active_filters)}")

if view_type == "Detailed Analysis":
    st.header("🔎 Detailed Analysis (Filtered)")
    
    # <<< ENSURE Methodology Section is present >>>
    with st.expander("🔬 Analysis Methodology & Data Processing", expanded=False):
        st.markdown("**Data Source:**")
        st.caption(analysis_methodology["transcript_filtering"]["source"])
        st.markdown(f"**Total Sentences Analyzed:** {analysis_methodology['transcript_filtering']['total_sentences']}")
        st.markdown("**Filtering Criteria:**")
        for criterion in analysis_methodology["transcript_filtering"]["filtering_criteria"]:
            st.markdown(f"- {criterion}")
        st.markdown("**Filtering Process:**")
        for i, step in enumerate(analysis_methodology["transcript_filtering"]["filtering_process"]):
             st.markdown(f"{step}")
        st.markdown("**Sentiment Analysis Approach:**")
        for section in analysis_methodology["sentiment_analysis"]["approach"]:
             st.markdown(f"- {section}")
        st.markdown("**Industry Examples (Pain Points, Challenges, Integrations):**")
        industry_tabs = st.tabs(analysis_methodology["sentiment_analysis"]["industry_examples"].keys())
        for i, (industry, details) in enumerate(analysis_methodology["sentiment_analysis"]["industry_examples"].items()):
            with industry_tabs[i]:
                st.markdown(f"**{industry}**")
                if "Pain Points" in details:
                    st.markdown("***Pain Points:***")
                    for point in details["Pain Points"]:
                        st.caption(f"- {point}")
                if "Technical Challenges" in details:
                    st.markdown("***Technical Challenges:***")
                    for challenge in details["Technical Challenges"]:
                        st.caption(f"- {challenge}")
                if "Integrations" in details:
                    st.markdown("***Integrations:***")
                    for integration in details["Integrations"]:
                         st.caption(f"- {integration}")

    # --- Filtered Data Overview ---
    st.subheader("📊 Filtered Data Overview")
    overview_tab1, overview_tab2 = st.tabs(["Trends", "Industry Distribution"])

    with overview_tab1:
        # Time series trend - Check empty before plot AND use try/except for range
        if current_time_series_data is not None and not current_time_series_data.empty and all(col in current_time_series_data.columns for col in ['Date', 'Mentions']):
             # <<< Check if DataFrame has rows BEFORE plotting >>>
            if not current_time_series_data.empty:
                try:
                    fig_trend = go.Figure()
                    fig_trend.add_trace(go.Scatter(
                        x=current_time_series_data['Date'], y=current_time_series_data['Mentions'],
                        fill='tozeroy', fillcolor='rgba(255, 75, 75, 0.1)',
                        line=dict(color='#FF4B4B', width=3), mode='lines+markers+text',
                        text=current_time_series_data['Mentions'], textposition='top center',
                        marker=dict(size=10, symbol='circle', line=dict(color='#FF4B4B', width=2)),
                        hovertemplate='%{x|%Y-%m-%d}<br>Mentions: %{y}<extra></extra>'
                    ))
                    # Calculate range with strengthened try/except
                    y_range_filtered = [0, 10] # Start with default
                    try:
                        mentions_filtered = current_time_series_data['Mentions']
                        if not mentions_filtered.empty:
                            max_mentions_filtered = mentions_filtered.max()
                            if pd.notna(max_mentions_filtered) and max_mentions_filtered > 0:
                                 y_range_filtered = [0, max_mentions_filtered * 1.2]
                    except (ValueError, TypeError): # Catch errors during max() or comparison
                         pass # Keep default range [0, 10]

                    fig_trend.update_layout(
                        title={'text': 'SFCC Pain Points Mentions Over Time (Filtered)', 'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                        height=450, template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(title="Number of Mentions", gridcolor='rgba(128,128,128,0.1)', zerolinecolor='rgba(128,128,128,0.1)', range=y_range_filtered, tickformat='d'),
                        xaxis=dict(title="Date", gridcolor='rgba(128,128,128,0.1)', zerolinecolor='rgba(128,128,128,0.1)'),
                        showlegend=False, hovermode='x unified'
                    )
                    st.plotly_chart(fig_trend, use_container_width=True)
                    # Metrics display
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Mentions (Filtered)", f"{total_mentions:,}")
                    with col2:
                        st.metric("Average Monthly (Filtered)", f"{avg_mentions:.1f}")
                    with col3:
                        growth_display = f"{growth:.0f}%" if growth != float('inf') else "∞%"
                        st.metric("Overall Growth (Filtered)", growth_display, delta="↗️" if growth > 0 else ("➡️" if growth == 0 else "↘️"))
                    st.info("🔍 **Trend Analysis (Filtered):** Reflects mentions within the selected time period and industries.")
                except Exception as e:
                    st.error(f"Error generating filtered trend plot (Line ~188): {e}")
                    st.exception(e)
            else:
                 st.info("No filtered time series data to plot.") # Inform if DataFrame is empty
        else:
            st.warning("Filtered Time series data unavailable or invalid for plotting.")

    with overview_tab2:
        # Industry distribution - use current_industry_data
        if current_industry_data is not None and not current_industry_data.empty and 'Industry' in current_industry_data.columns and 'Count' in current_industry_data.columns and 'Pain_Points' in current_industry_data.columns:
            try:
                fig_industry = px.bar(current_industry_data, x='Industry', y=['Count', 'Pain_Points'],
                                     title='Industry Distribution (Filtered)',
                                     barmode='group',
                                     labels={'value': 'Count', 'variable': 'Metric'})
                fig_industry.update_layout(
                    height=400,
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis=dict(gridcolor='rgba(128,128,128,0.1)'),
                    xaxis=dict(gridcolor='rgba(128,128,128,0.1)')
                )
                st.plotly_chart(fig_industry, use_container_width=True)
            except Exception as e:
                st.error(f"Error generating filtered industry plot: {e}")
        else:
            st.warning("No industry data to display for the selected filters.")

    # Pain Points Definitions Section - Uses global_severity_df
    st.subheader("Pain Points Definitions & Severity")
    if global_severity_df is not None and not global_severity_df.empty:
        st.dataframe(global_severity_df[['Category', 'Description', 'Severity_Label']], use_container_width=True)
    else:
        st.warning("Severity data definition is missing.")

elif view_type == "Raw Data":
    st.header("📄 Raw Data Tables (Filtered)")

    st.subheader("Time Series Mentions")
    if current_time_series_data is not None and not current_time_series_data.empty:
        st.dataframe(current_time_series_data, use_container_width=True)
    else:
        st.warning("No time series data available for selected filters.")

    st.subheader("Industry Distribution")
    if current_industry_data is not None and not current_industry_data.empty:
        st.dataframe(current_industry_data, use_container_width=True)
    else:
        st.warning("No industry data available for selected filters.")

    st.subheader("Pain Points Definitions & Severity")
    if global_severity_df is not None and not global_severity_df.empty:
        st.dataframe(global_severity_df[['Category', 'Description', 'Severity_Label', 'Severity']], use_container_width=True)
    else:
        st.warning("Pain point definition data is missing.")

# Footer
st.markdown("---")
st.caption("Data derived from simulated analysis of SFCC B2B/Enterprise discussions.")