pip install streamlit
pip install sqlite3
pip install bcrypt

import streamlit as st
import sqlite3
from sqlite3 import Error
import bcrypt

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('database.db')
        print(f"Connection to database was successful with SQLite version {sqlite3.version}")
    except Error as e:
        print(e)
    return conn

def login(conn):
    st.title("Login")

    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cursor.fetchone()

            if user:
                hashed_password = user[2].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    st.success("Logged in as {}".format(user[1]))
                else:
                    st.error("Incorrect username or password")
            else:
                st.error("Incorrect username or password")

def create_users_table(conn):
    sql = '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );'''
    with conn:
        conn.execute(sql)

def add_test_user(conn):
    username = "test_user"
    password = "test_password".encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    with conn:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))

conn = create_connection()
create_users_table(conn)
add_test_user(conn)
login(conn)
