from google.cloud import bigquery
import pandas as pd
from datetime import datetime, timedelta

def search_salesloft_transcripts(search_terms=None, days_back=30, limit=100):
    """
    Search Salesloft transcripts for specific terms
    
    Args:
        search_terms (list): List of terms to search for in transcripts
        days_back (int): How many days back to search
        limit (int): Maximum number of results to return
    """
    client = bigquery.Client()
    
    # Base query to get transcripts
    base_query = """
    WITH transcripts AS (
        SELECT 
            t.created_at,
            t.transcript_text,
            t.call_uuid,
            t.duration_seconds,
            c.opportunity_id,
            c.account_name,
            c.owner_name
        FROM `shopify-dw.raw_salesloft.transcriptions` t
        LEFT JOIN `shopify-dw.raw_salesloft.conversations` c
        ON t.call_uuid = c.call_uuid
        WHERE t.created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
    )
    """
    
    # If search terms provided, add search conditions
    if search_terms and len(search_terms) > 0:
        search_conditions = " OR ".join([
            f"LOWER(transcript_text) LIKE LOWER('%{term}%')"
            for term in search_terms
        ])
        search_query = base_query + f"""
        SELECT * FROM transcripts 
        WHERE {search_conditions}
        ORDER BY created_at DESC
        LIMIT {limit}
        """
    else:
        search_query = base_query + f"""
        SELECT * FROM transcripts
        ORDER BY created_at DESC
        LIMIT {limit}
        """
    
    # Format query with days parameter
    final_query = search_query.format(days=days_back)
    
    try:
        # Execute query
        df = client.query(final_query).to_dataframe()
        return df
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        return None

def analyze_transcript_results(df):
    """
    Analyze the transcript search results
    
    Args:
        df (pandas.DataFrame): DataFrame containing transcript results
    """
    if df is None or df.empty:
        print("No results to analyze")
        return
    
    print(f"\nFound {len(df)} matching transcripts")
    print("\nMost recent conversations:")
    recent = df.head(5)[['created_at', 'account_name', 'owner_name', 'duration_seconds']]
    print(recent.to_string())
    
    if 'opportunity_id' in df.columns:
        print("\nUnique opportunities mentioned:", df['opportunity_id'].nunique())

def main():
    # Example usage
    search_terms = ['BigCommerce', 'competitor', 'migration']
    print(f"Searching for terms: {search_terms}")
    
    results = search_salesloft_transcripts(
        search_terms=search_terms,
        days_back=30,
        limit=100
    )
    
    analyze_transcript_results(results)

if __name__ == "__main__":
    main() 