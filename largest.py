import streamlit as st

st.title("Largest Number ")
st.write("Enter three numbers below to find the largest number:")

num1 = st.number_input("Enter first number :")
num2 = st.number_input("Enter second number :")
num3 = st.number_input("Enter third number :")

if st.button("Find Largest Number"):
    largest_number = max(num1, num2, num3)
    st.success(f"The largest number is: {largest_number}")
