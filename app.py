import streamlit as st

st.set_page_config(page_title="Privacy Lens", page_icon="🛡️")

st.title("🛡️ Privacy Lens Tool")
st.write("Welcome! Ye aapka online privacy tool hai.")

# Yahan aap apne tool ka kaam bata sakte hain
option = st.selectbox(
    'Aap kya check karna chahte hain?',
    ('Data Privacy', 'Security Settings', 'User Logs'))

if st.button('Check Karein'):
    st.success(f'{option} Scan ho raha hai... Sab theek hai!')
else:
    st.write('Button dabayein scan shuru karne ke liye.')
