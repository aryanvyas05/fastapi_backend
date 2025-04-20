import psycopg2

def get_connection():
    return psycopg2.connect(
        host="db.pmhvemnvinlqslopxuvp.supabase.co",
        dbname="postgres",
        user="postgres",
        password="Rangoli@2005",
        port=5432
    )
