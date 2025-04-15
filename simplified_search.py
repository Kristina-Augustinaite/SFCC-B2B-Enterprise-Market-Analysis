from google.cloud import bigquery
from google.api_core import retry

def search_transcripts(search_term, days_back=30, location='US'):
    """
    Simple function to search Salesloft transcripts
    
    Args:
        search_term (str): Term to search for in transcripts
        days_back (int): How many days back to search
        location (str): Dataset location (e.g., 'US', 'EU', 'US-CENTRAL1')
    """
    # Initialize client with location
    client = bigquery.Client(location=location)
    
    # List of locations to try if the first one fails
    locations = ['US', 'US-CENTRAL1', 'EU', 'NA'] if location == 'US' else [location]
    
    for try_location in locations:
        try:
            # Set job config with location
            job_config = bigquery.QueryJobConfig(
                use_query_cache=True,
                labels={'purpose': 'salesloft_search'}
            )
            
            query = f"""
            SELECT 
                t.created_at,
                t.transcript_text,
                c.account_name,
                c.owner_name
            FROM `shopify-dw.raw_salesloft.transcriptions` t
            LEFT JOIN `shopify-dw.raw_salesloft.conversations` c
            ON t.call_uuid = c.call_uuid
            WHERE t.created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days_back} DAY)
            AND LOWER(t.transcript_text) LIKE LOWER('%{search_term}%')
            ORDER BY t.created_at DESC
            LIMIT 10
            """
            
            # Execute query with retry
            @retry.Retry(predicate=retry.if_exception_type(Exception))
            def run_with_retry():
                query_job = client.query(
                    query,
                    job_config=job_config,
                    location=try_location
                )
                return query_job.result()
            
            results = run_with_retry()
            
            # If we get here, the query succeeded
            print(f"\nResults for search term '{search_term}' (location: {try_location}):\n")
            result_count = 0
            
            for row in results:
                result_count += 1
                print(f"Date: {row.created_at}")
                print(f"Account: {row.account_name}")
                print(f"Owner: {row.owner_name}")
                print("Transcript excerpt:")
                transcript = row.transcript_text.lower()
                term_pos = transcript.find(search_term.lower())
                start = max(0, term_pos - 100)
                end = min(len(transcript), term_pos + 100)
                print(f"...{transcript[start:end]}...")
                print("-" * 80 + "\n")
            
            if result_count == 0:
                print("No matching transcripts found.")
            
            # If we get here without exception, we found the right location
            return
            
        except Exception as e:
            if try_location == locations[-1]:
                print(f"Error executing query in all locations: {str(e)}")
                print("Please ensure you have:")
                print("1. Proper authentication (run 'gcloud auth application-default login')")
                print("2. Access to the shopify-dw project")
                print("3. Permissions for the raw_salesloft dataset")
            else:
                print(f"Failed in location {try_location}, trying next location...")

if __name__ == "__main__":
    # Example usage
    search_term = input("Enter search term: ")
    days = int(input("How many days back to search (default 30): ") or "30")
    location = input("Enter dataset location (default US): ") or "US"
    search_transcripts(search_term, days, location) 