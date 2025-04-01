import pandas as pd
import snowflake.connector
 
def get_provider_summary():
    conn = snowflake.connector.connect(
        user="SAIRAHUL.PERUMALLA@COREWELLHEALTH.ORG",
        account="SPECTRUMHEALTH-ANALYTICS", # e.g., abc12345.east-us-2.azure
        warehouse="ENT_HACKATHON_M_WH",
        database="ENT_AI_HACKATHON_BTWS",
        schema="PERUMALLA",
        authenticator="externalbrowser",
        role="SFK_AI_HACKATHON_DEV"
    )
 
    query = "SELECT * FROM ENT_AI_HACKATHON_BTWS.PERUMALLA.PROVIDER_SUMMARY"
    df = pd.read_sql(query, conn)
    conn.close()
    return df