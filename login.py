import psycopg2
import streamlit as st

conn = psycopg2.connect(
    host="localhost",
    database="test_db",
    user="postgres",
    password="password"
)
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    
def create_user(email, password):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()

# Define a function to get the user from the database based on email and password
def get_user(email, password):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        return cur.fetchone()

def app():
    st.title("Login/Signup Form")

    # Get the user's email and password
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Check if the user wants to login or signup
    action = st.radio("Login/Signup", ("Login", "Signup"))

    if action == "Login":
        # Try to get the user from the database
        user = get_user(email, password)
        if user is not None:
            st.success("Logged in successfully!")
        else:
            st.error("Invalid email or password.")
    else:
        # Create a new user in the database
        create_user(email, password)
        st.success("Account created successfully!")
        
if __name__ == "__main__":
    app()
